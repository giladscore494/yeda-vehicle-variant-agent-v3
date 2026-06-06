"""Queue and audit AI review outcomes before surgical patch extraction."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.paths import (
    ACTIVE_WORKING_DATABASE_PATH,
    AI_OUTCOME_AUDITS_PATH,
    DECISIONS_PATH,
    SOURCE_CANONICAL_PATH,
)
from engine import config
from engine.validation.run_events import log_event
from engine.validation.write_guard import safe_write_json

_DEFAULT_AUDIT_RESULT = {
    "status": "FAIL",
    "change_decision": "NO_CHANGE_REQUIRED",
    "change_severity": "negligible",
    "patchable": False,
    "patchability_reason": "vague_recommendation",
    "blocking_reasons": [],
    "required_fixes": [],
    "summary": "",
}
_VALID_CHANGE_DECISIONS = {"CHANGE_REQUIRED", "NO_CHANGE_REQUIRED"}
_VALID_CHANGE_SEVERITIES = {"critical", "material", "minor", "negligible"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: str | Path, default: Any = None) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def _append_jsonl(path: str | Path, payload: dict) -> None:
    def _sanitize(value: Any) -> Any:
        if isinstance(value, dict):
            cleaned: dict[str, Any] = {}
            for key, item in value.items():
                key_text = str(key).lower()
                if any(token in key_text for token in ("api_key", "token", "secret", "password", "authorization")):
                    continue
                cleaned[str(key)] = _sanitize(item)
            return cleaned
        if isinstance(value, list):
            return [_sanitize(item) for item in value]
        if isinstance(value, str):
            if "sk-" in value or "AIza" in value:
                return "[redacted]"
            return value
        return value

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    sanitized_payload = _sanitize(payload)
    with p.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(sanitized_payload, ensure_ascii=False) + "\n")  # lgtm [py/clear-text-storage-sensitive-data]


def _all_variants(payload: dict) -> list[dict]:
    variants: list[dict] = []
    for key in ("verified_variants", "partial_variants", "vehicles"):
        value = payload.get(key)
        if isinstance(value, list):
            variants.extend(item for item in value if isinstance(item, dict))
    return variants


def _load_working_records_by_variant_ids(variant_ids: list[str]) -> dict[str, dict]:
    if not variant_ids:
        return {}
    payload = _read_json(ACTIVE_WORKING_DATABASE_PATH)
    if not isinstance(payload, dict):
        payload = _read_json(SOURCE_CANONICAL_PATH, {})
    if not isinstance(payload, dict):
        return {}
    records: dict[str, dict] = {}
    wanted = set(variant_ids)
    for variant in _all_variants(payload):
        variant_id = str(variant.get("variant_id") or "").strip()
        if variant_id and variant_id in wanted and variant_id not in records:
            records[variant_id] = variant
    return records


def _load_decisions_payload() -> dict:
    payload = _read_json(DECISIONS_PATH, {"decisions": []})
    if isinstance(payload, list):
        return {"created_at": _utc_now(), "decisions": [item for item in payload if isinstance(item, dict)]}
    if isinstance(payload, dict):
        decisions = payload.get("decisions")
        if not isinstance(decisions, list):
            payload["decisions"] = []
        return payload
    return {"created_at": _utc_now(), "decisions": []}


def _decision_id(decision: dict) -> str:
    for key in ("decision_id", "id", "source_decision_id"):
        value = decision.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _is_completed_decision(decision: dict) -> bool:
    state = str(decision.get("status") or decision.get("decision_status") or "").strip().lower()
    if not state:
        return True
    return state in {"completed", "done", "success"}


def _extract_variant_ids(decision: dict) -> list[str]:
    raw = decision.get("variant_ids")
    if isinstance(raw, list):
        ids: list[str] = []
        for value in raw:
            text = str(value).strip()
            if text:
                ids.append(text)
    else:
        single = str(decision.get("variant_id") or "").strip()
        ids = [single] if single else []
    unique: list[str] = []
    for value in ids:
        if value not in unique:
            unique.append(value)
    return unique


def _decision_summary(result: Any) -> dict:
    if not isinstance(result, dict):
        return {}
    parsed = result.get("parsed_result")
    payload = parsed if isinstance(parsed, dict) else result
    summary = {}
    for key in ("recommendation", "final_recommendation", "action", "summary", "reason", "rationale"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            summary[key] = value.strip()
    return summary


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
    result = dict(_DEFAULT_AUDIT_RESULT)
    if not isinstance(payload, dict):
        return result
    status = str(payload.get("status") or "").upper()
    if status in {"PASS", "FAIL"}:
        result["status"] = status
    change_decision = str(payload.get("change_decision") or "").upper()
    if change_decision in _VALID_CHANGE_DECISIONS:
        result["change_decision"] = change_decision
    change_severity = str(payload.get("change_severity") or "").lower()
    if change_severity in _VALID_CHANGE_SEVERITIES:
        result["change_severity"] = change_severity
    if isinstance(payload.get("patchable"), bool):
        result["patchable"] = payload["patchable"]
    patchability_reason = payload.get("patchability_reason")
    if isinstance(patchability_reason, str) and patchability_reason.strip():
        result["patchability_reason"] = patchability_reason.strip()
    result["blocking_reasons"] = payload.get("blocking_reasons") if isinstance(payload.get("blocking_reasons"), list) else []
    result["required_fixes"] = payload.get("required_fixes") if isinstance(payload.get("required_fixes"), list) else []
    result["summary"] = str(payload.get("summary") or "")
    return result


def queue_completed_decisions_for_outcome_audit(*, retry: bool = False) -> dict:
    payload = _load_decisions_payload()
    decisions = payload.get("decisions") if isinstance(payload.get("decisions"), list) else []
    counts = {"pending": 0, "passed": 0, "failed": 0, "skipped": 0}
    updated = False
    now = _utc_now()
    for decision in decisions:
        if not isinstance(decision, dict):
            counts["skipped"] += 1
            continue
        if not _is_completed_decision(decision):
            counts["skipped"] += 1
            continue
        status = str(decision.get("outcome_audit_status") or "").strip().lower()
        if status in {"passed", "failed"} and not retry:
            counts[status] += 1
            counts["skipped"] += 1
            continue
        if status == "pending" and not retry:
            counts["pending"] += 1
            counts["skipped"] += 1
            continue
        decision["outcome_audit_status"] = "pending"
        decision["outcome_audit_queued_at"] = now
        updated = True
        counts["pending"] += 1
    if updated:
        payload.setdefault("created_at", now)
        payload["updated_at"] = now
        safe_write_json(payload, DECISIONS_PATH)
    return counts


def _call_openai_outcome_audit(model: str, prompt_payload: dict) -> tuple[dict[str, Any], str | None]:
    api_key = config.get("openai", "api_key")
    if not api_key:
        result = dict(_DEFAULT_AUDIT_RESULT)
        result["blocking_reasons"] = ["OpenAI API key not configured."]
        return result, None
    request_summary = f"decision_id={prompt_payload.get('decision_id', '')}"
    log_event(
        {
            "stage": "ai_outcome_audit",
            "event_type": "model_call_started",
            "provider": "openai",
            "model": model,
            "status": "started",
            "request_summary": request_summary,
        }
    )
    prompt = {
        "task": "Audit this AI review outcome only. Return strict JSON only.",
        "required_schema": {
            "status": "PASS | FAIL",
            "change_decision": "CHANGE_REQUIRED | NO_CHANGE_REQUIRED",
            "change_severity": "critical | material | minor | negligible",
            "patchable": "boolean",
            "patchability_reason": "string",
            "blocking_reasons": "list[str]",
            "required_fixes": "list[str]",
            "summary": "string",
        },
        "rules": [
            "Never request full database.",
            "Use only provided decision + target records.",
            "If evidence is weak or vague, choose NO_CHANGE_REQUIRED.",
            "PASS means current or corrected binary decision is acceptable.",
            "FAIL means outcome needs fix before patch proposal extraction.",
        ],
        "ai_review_outcome_payload": prompt_payload,
    }
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
                "stage": "ai_outcome_audit",
                "event_type": "model_call_completed",
                "provider": "openai",
                "model": model,
                "status": "ok",
                "request_summary": request_summary,
                "response_summary": f"status={parsed['status']}",
            }
        )
        return parsed, None
    except Exception as exc:
        log_event(
            {
                "stage": "ai_outcome_audit",
                "event_type": "model_call_failed",
                "provider": "openai",
                "model": model,
                "status": "failed",
                "request_summary": request_summary,
                "error": str(exc),
            }
        )
        result = dict(_DEFAULT_AUDIT_RESULT)
        result["blocking_reasons"] = ["OpenAI outcome audit call failed."]
        return result, str(exc)


def audit_next_ai_review_outcome_with_openai() -> dict:
    payload = _load_decisions_payload()
    decisions = payload.get("decisions") if isinstance(payload.get("decisions"), list) else []
    next_decision: dict | None = None
    for decision in decisions:
        if not isinstance(decision, dict) or not _is_completed_decision(decision):
            continue
        if str(decision.get("outcome_audit_status") or "").strip().lower() == "pending":
            next_decision = decision
            break
    if next_decision is None:
        return {"status": "NO_PENDING_OUTCOME_AUDIT", "message": "No pending AI review outcome audit."}

    decision_id = _decision_id(next_decision)
    variant_ids = _extract_variant_ids(next_decision)
    prompt_payload = {
        "decision_id": decision_id,
        "item_id": next_decision.get("item_id"),
        "issue_type": next_decision.get("issue_type"),
        "risk_level": next_decision.get("risk_level"),
        "variant_ids": variant_ids,
        "target_records": _load_working_records_by_variant_ids(variant_ids),
        "gemini_summary": _decision_summary(next_decision.get("gemini_result")),
        "openai_summary": _decision_summary(next_decision.get("openai_result")),
        "current_change_decision": next_decision.get("change_decision"),
        "current_change_severity": next_decision.get("change_severity"),
        "current_patchable": next_decision.get("patchable"),
        "current_patchability_reason": next_decision.get("patchability_reason"),
    }
    model = config.get("openai", "outcome_audit_model", "gpt-5.4") or "gpt-5.4"
    model_result, error = _call_openai_outcome_audit(model, prompt_payload)
    status = "passed" if model_result["status"] == "PASS" else "failed"
    now = _utc_now()

    next_decision["outcome_audit_status"] = status
    next_decision["outcome_audit_model"] = model
    next_decision["outcome_audit_updated_at"] = now
    next_decision["outcome_audit_blocking_reasons"] = model_result["blocking_reasons"]
    next_decision["outcome_audit_required_fixes"] = model_result["required_fixes"]
    next_decision["outcome_audit_summary"] = model_result["summary"]
    next_decision["change_decision"] = model_result["change_decision"]
    next_decision["change_severity"] = model_result["change_severity"]
    next_decision["patchable"] = model_result["patchable"]
    next_decision["patchability_reason"] = model_result["patchability_reason"]

    payload.setdefault("created_at", now)
    payload["updated_at"] = now
    safe_write_json(payload, DECISIONS_PATH)

    event = {
        "created_at": now,
        "decision_id": decision_id,
        "item_id": next_decision.get("item_id"),
        "variant_ids": variant_ids,
        "model": model,
        "status": model_result["status"],
        "change_decision": model_result["change_decision"],
        "change_severity": model_result["change_severity"],
        "patchable": model_result["patchable"],
        "patchability_reason": model_result["patchability_reason"],
        "blocking_reasons": model_result["blocking_reasons"],
        "required_fixes": model_result["required_fixes"],
        "summary": model_result["summary"],
        "audited_payload_keys": sorted(prompt_payload.keys()),
        "target_record_count": len(prompt_payload["target_records"]),
        "error": error,
    }
    _append_jsonl(AI_OUTCOME_AUDITS_PATH, event)
    return event
