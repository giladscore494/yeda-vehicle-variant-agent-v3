"""GPT-5.4 audit for the most recently applied surgical patch diff."""
from __future__ import annotations

import difflib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.paths import DIFF_AUDITS_PATH, PATCH_APPLICATIONS_PATH, PATCHES_PATH
from engine import config
from engine.validation.run_events import log_event
from engine.validation.write_guard import safe_write_json

_JSON_SCHEMA = {
    "status": "FAIL",
    "confidence": 0.0,
    "blocking_reasons": [],
    "non_blocking_warnings": [],
    "required_fixes": [],
    "summary": "",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: str | Path, default: Any = None) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def _append_jsonl(path: str | Path, payload: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _read_jsonl(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    rows: list[dict] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def _last_applied_patch_event() -> dict | None:
    for row in reversed(_read_jsonl(PATCH_APPLICATIONS_PATH)):
        if row.get("status") == "applied_pending_audit" and row.get("patch_id"):
            return row
    return None


def _load_patch(patch_id: str) -> tuple[dict, dict]:
    payload = _read_json(PATCHES_PATH, {"patches": []})
    if not isinstance(payload, dict):
        raise ValueError("patches.json must be a JSON object")
    for patch in payload.get("patches", []):
        if isinstance(patch, dict) and patch.get("patch_id") == patch_id:
            return payload, patch
    raise ValueError(f"patch_id not found: {patch_id}")


def _write_patches_payload(payload: dict) -> None:
    safe_write_json(payload, PATCHES_PATH)


def _unified_diff(before: dict, after: dict) -> str:
    before_lines = json.dumps(before, ensure_ascii=False, indent=2, sort_keys=True).splitlines()
    after_lines = json.dumps(after, ensure_ascii=False, indent=2, sort_keys=True).splitlines()
    return "\n".join(difflib.unified_diff(before_lines, after_lines, fromfile="before", tofile="after", lineterm=""))


def _parse_model_json(raw_text: str) -> dict[str, Any] | None:
    try:
        parsed = json.loads(raw_text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start >= 0 and end > start:
        try:
            parsed = json.loads(raw_text[start : end + 1])
        except json.JSONDecodeError:
            return None
        if isinstance(parsed, dict):
            return parsed
    return None


def _normalize_model_result(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return dict(_JSON_SCHEMA)
    status = str(payload.get("status") or "").upper()
    if status not in {"PASS", "FAIL"}:
        status = "FAIL"
    confidence = payload.get("confidence")
    confidence_value = max(0.0, min(1.0, float(confidence))) if isinstance(confidence, (int, float)) else 0.0
    return {
        "status": status,
        "confidence": confidence_value,
        "blocking_reasons": payload.get("blocking_reasons") if isinstance(payload.get("blocking_reasons"), list) else [],
        "non_blocking_warnings": payload.get("non_blocking_warnings") if isinstance(payload.get("non_blocking_warnings"), list) else [],
        "required_fixes": payload.get("required_fixes") if isinstance(payload.get("required_fixes"), list) else [],
        "summary": str(payload.get("summary") or ""),
    }


def _build_prompt_payload(application: dict, patch: dict) -> dict:
    before = application.get("before") if isinstance(application.get("before"), dict) else {}
    after = application.get("after") if isinstance(application.get("after"), dict) else {}
    diffs = {
        variant_id: _unified_diff(before.get(variant_id, {}), after.get(variant_id, {}))
        for variant_id in sorted(set(before) | set(after))
    }
    return {
        "patch_id": patch.get("patch_id"),
        "source_decision_id": patch.get("source_decision_id"),
        "variant_ids": patch.get("variant_ids", []),
        "before_records": before,
        "after_records": after,
        "exact_changed_fields": patch.get("field_changes", {}),
        "diff": diffs,
        "variant_count_before": application.get("variant_count_before"),
        "variant_count_after": application.get("variant_count_after"),
        "decision_summary": patch.get("reason", ""),
    }


def _call_openai_diff_audit(model: str, prompt_payload: dict) -> tuple[dict[str, Any], str | None]:
    api_key = config.get("openai", "api_key")
    if not api_key:
        result = dict(_JSON_SCHEMA)
        result["blocking_reasons"] = ["OpenAI API key not configured."]
        return result, "OpenAI API key not configured."

    prompt = {
        "task": "Audit only this surgical patch before/after/diff. Return strict JSON only.",
        "required_schema": {
            "status": "PASS | FAIL",
            "confidence": "0.0-1.0",
            "blocking_reasons": "list[str]",
            "non_blocking_warnings": "list[str]",
            "required_fixes": "list[str]",
            "summary": "string",
        },
        "pass_rules": [
            "PASS only if only requested fields changed.",
            "PASS only if changed values match the decision.",
            "PASS only if no unrelated valuable fields were removed.",
            "PASS only if no variant disappeared.",
            "PASS only if IDs stayed stable unless explicitly allowed.",
        ],
        "fail_rules": [
            "FAIL if unexpected fields changed.",
            "FAIL if a variant was lost.",
            "FAIL if ID changed without approval.",
            "FAIL if important data was overwritten with null or empty values.",
            "FAIL if patch is broader than the decision.",
        ],
        "patch_diff_payload": prompt_payload,
    }
    request_summary = f"patch_id={prompt_payload.get('patch_id')} variants={len(prompt_payload.get('variant_ids') or [])}"
    log_event(
        {
            "stage": "diff_quality_audit",
            "event_type": "model_call_started",
            "provider": "openai",
            "model": model,
            "status": "started",
            "request_summary": request_summary,
        }
    )
    try:
        import openai

        client = openai.OpenAI(api_key=api_key)
        response = None
        raw_text = ""
        if hasattr(client, "chat") and hasattr(client.chat, "completions"):
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Return strict JSON only."},
                    {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
                ],
            )
            choices = getattr(response, "choices", None)
            if choices and isinstance(choices, list):
                raw_text = str(getattr(getattr(choices[0], "message", None), "content", "") or "")
        elif hasattr(client, "responses"):
            response = client.responses.create(model=model, input=json.dumps(prompt, ensure_ascii=False))
            raw_text = str(getattr(response, "output_text", "") or "")
        if not raw_text and response is not None:
            raw_text = str(response)
        parsed = _normalize_model_result(_parse_model_json(raw_text))
        log_event(
            {
                "stage": "diff_quality_audit",
                "event_type": "model_call_completed",
                "provider": "openai",
                "model": model,
                "status": "ok",
                "request_summary": request_summary,
                "response_summary": f"status={parsed['status']} confidence={parsed['confidence']}",
            }
        )
        return parsed, None
    except Exception as exc:
        log_event(
            {
                "stage": "diff_quality_audit",
                "event_type": "model_call_failed",
                "provider": "openai",
                "model": model,
                "status": "failed",
                "request_summary": request_summary,
                "error": str(exc),
            }
        )
        result = dict(_JSON_SCHEMA)
        result["blocking_reasons"] = [str(exc)]
        return result, str(exc)


def audit_last_patch_diff_with_openai() -> dict:
    """Audit the most recently applied patch using only before/after/diff payload."""
    application = _last_applied_patch_event()
    if application is None:
        return {"status": "NO_APPLIED_PATCH", "message": "No applied patch found."}
    patches_payload, patch = _load_patch(str(application["patch_id"]))
    prompt_payload = _build_prompt_payload(application, patch)
    model = config.get("openai", "diff_audit_model", "gpt-5.4") or "gpt-5.4"
    model_result, error = _call_openai_diff_audit(model, prompt_payload)
    patch["status"] = "audit_passed" if model_result["status"] == "PASS" else "audit_failed"
    patch["blocking_reason"] = None if model_result["status"] == "PASS" else "; ".join(model_result["blocking_reasons"])
    _write_patches_payload(patches_payload)

    audit_event = {
        "created_at": _utc_now(),
        "patch_id": patch.get("patch_id"),
        "source_decision_id": patch.get("source_decision_id"),
        "variant_ids": patch.get("variant_ids", []),
        "model": model,
        "request_payload": prompt_payload,
        "status": model_result["status"],
        "confidence": model_result["confidence"],
        "blocking_reasons": model_result["blocking_reasons"],
        "non_blocking_warnings": model_result["non_blocking_warnings"],
        "required_fixes": model_result["required_fixes"],
        "summary": model_result["summary"],
    }
    if error:
        audit_event["error"] = error
    _append_jsonl(DIFF_AUDITS_PATH, audit_event)
    return audit_event
