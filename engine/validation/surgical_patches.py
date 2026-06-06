"""Build, apply, and audit surgical working-copy patches by variant_id."""
from __future__ import annotations

import difflib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.paths import (
    DECISIONS_PATH,
    DIFF_AUDITS_PATH,
    PATCH_APPLICATIONS_PATH,
    PATCHES_PATH,
)
from engine import config
from engine.validation.run_events import log_event
from engine.validation.working_copy import get_active_database_path, initialize_working_copy
from engine.validation.write_guard import safe_write_json


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: str | Path, default: Any) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _append_jsonl(path: str | Path, payload: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _decisions_list(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        return [item for item in payload.get("decisions", []) if isinstance(item, dict)]
    return []


def _field_parts(field: str) -> list[str]:
    return [part for part in field.replace("[", ".").replace("]", "").split(".") if part]


def _get_field(container: Any, field: str) -> Any:
    current = container
    for part in _field_parts(field):
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit():
            index = int(part)
            current = current[index] if index < len(current) else None
        else:
            return None
    return current


def _set_field(container: Any, field: str, value: Any) -> bool:
    parts = _field_parts(field)
    if not parts:
        return False
    current = container
    for part in parts[:-1]:
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit():
            index = int(part)
            current = current[index] if index < len(current) else None
        else:
            return False
    last = parts[-1]
    if isinstance(current, dict):
        current[last] = value
        return True
    if isinstance(current, list) and last.isdigit():
        index = int(last)
        if index < len(current):
            current[index] = value
            return True
    return False


def _all_variant_lists(payload: dict) -> list[list[dict]]:
    lists: list[list[dict]] = []
    for key in ("verified_variants", "partial_variants", "vehicles"):
        raw = payload.get(key)
        if isinstance(raw, list):
            lists.append(raw)
    return lists


def _find_variant(payload: dict, variant_id: str) -> dict | None:
    for variants in _all_variant_lists(payload):
        for variant in variants:
            if isinstance(variant, dict) and str(variant.get("variant_id") or "") == variant_id:
                return variant
    return None


def _extract_suggested_patch(decision: dict) -> dict | None:
    parsed_candidates = []
    for result_key in ("openai_result", "gemini_result"):
        result = decision.get(result_key)
        if isinstance(result, dict):
            parsed = result.get("parsed_result")
            if isinstance(parsed, dict):
                parsed_candidates.append(parsed)
    parsed_candidates.append(decision)

    for payload in parsed_candidates:
        suggested_patch = payload.get("suggested_patch") if isinstance(payload, dict) else None
        if isinstance(suggested_patch, dict) and suggested_patch.get("has_patch"):
            return suggested_patch
    return None


def _patch_from_decision(decision: dict) -> dict | None:
    suggested_patch = _extract_suggested_patch(decision)
    variant_id = ""
    field = ""
    new_value: Any = None
    current_value: Any = None
    patch_type = "field_update"

    if suggested_patch:
        variant_id = str(suggested_patch.get("target_variant_id") or decision.get("variant_id") or "").strip()
        field = str(suggested_patch.get("field") or "").strip()
        new_value = suggested_patch.get("suggested_value")
        current_value = suggested_patch.get("current_value")
        patch_type = str(suggested_patch.get("patch_type") or "field_update")
    else:
        variant_id = str(decision.get("variant_id") or "").strip()
        field = str(decision.get("field") or decision.get("target_field") or "").strip()
        new_value = decision.get("suggested_value", decision.get("new_value"))
        current_value = decision.get("current_value")

    if not variant_id or not field or patch_type not in {"field_update", "status_change", "manual_review_flag"}:
        return None

    return {
        "patch_id": f"sp_{uuid.uuid4().hex}",
        "decision_id": decision.get("decision_id", ""),
        "source": decision.get("source") or "decision",
        "variant_id": variant_id,
        "patch_type": patch_type,
        "field": field,
        "current_value": current_value,
        "suggested_value": new_value,
        "reason": decision.get("reason") or (suggested_patch or {}).get("reason") or "",
        "safe_to_auto_apply": decision.get("safe_to_auto_apply") is True,
        "created_at": _utc_now(),
    }


def build_candidate_surgical_patches(
    decisions_path: str | Path = DECISIONS_PATH,
    output_path: str | Path = PATCHES_PATH,
) -> dict:
    """Build candidate surgical patches from exact variant-targeted decisions."""
    decisions = _decisions_list(_read_json(decisions_path, {"decisions": []}))
    patches = [patch for decision in decisions if (patch := _patch_from_decision(decision))]
    payload = {
        "created_at": _utc_now(),
        "decisions_path": str(decisions_path),
        "patch_count": len(patches),
        "patches": patches,
    }
    safe_write_json(payload, output_path)
    return payload


def _diff(before: dict, after: dict) -> str:
    before_lines = json.dumps(before, ensure_ascii=False, indent=2, sort_keys=True).splitlines()
    after_lines = json.dumps(after, ensure_ascii=False, indent=2, sort_keys=True).splitlines()
    return "\n".join(difflib.unified_diff(before_lines, after_lines, fromfile="before", tofile="after", lineterm=""))


def _audit_variant_diff(change: dict, model: str = "gpt-5.4") -> dict:
    audit_payload = {
        "variant_id": change["variant_id"],
        "before": change["before"],
        "after": change["after"],
        "diff": change["diff"],
    }
    result = {
        "created_at": _utc_now(),
        "provider": "openai",
        "model": model,
        "variant_id": change["variant_id"],
        "request": audit_payload,
        "status": "skipped",
        "summary": "OpenAI API key not configured.",
    }
    api_key = config.get("openai", "api_key")
    if not api_key:
        _append_jsonl(DIFF_AUDITS_PATH, result)
        return result

    log_event(
        {
            "stage": "diff_audit",
            "event_type": "model_call_started",
            "provider": "openai",
            "model": model,
            "item_id": change["variant_id"],
            "status": "started",
            "request_summary": f"variant_id={change['variant_id']}",
        }
    )
    try:
        import openai

        client = openai.OpenAI(api_key=api_key)
        prompt = {
            "task": "Audit only this variant surgical patch. Return strict JSON.",
            "rules": [
                "Use only before, after, and diff.",
                "Do not assume access to the full database.",
                "Flag data loss, changed identity, or unsafe field changes.",
            ],
            **audit_payload,
        }
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
                first = choices[0]
                message = getattr(first, "message", None)
                raw_text = str(getattr(message, "content", "") or "")
        elif hasattr(client, "responses"):
            response = client.responses.create(model=model, input=json.dumps(prompt, ensure_ascii=False))
            raw_text = getattr(response, "output_text", "") or ""
        if not raw_text and response is not None:
            raw_text = str(response)
        result.update({"status": "ok", "summary": raw_text[:1000]})
        log_event(
            {
                "stage": "diff_audit",
                "event_type": "model_call_completed",
                "provider": "openai",
                "model": model,
                "item_id": change["variant_id"],
                "status": "ok",
                "response_summary": raw_text[:500],
            }
        )
    except Exception as exc:
        result.update({"status": "failed", "summary": str(exc)})
        log_event(
            {
                "stage": "diff_audit",
                "event_type": "model_call_failed",
                "provider": "openai",
                "model": model,
                "item_id": change["variant_id"],
                "status": "failed",
                "error": str(exc),
            }
        )
    _append_jsonl(DIFF_AUDITS_PATH, result)
    return result


def apply_surgical_patches(
    patch_ids: list[str] | None = None,
    *,
    require_safe: bool = True,
    run_diff_audit: bool = True,
) -> dict:
    """Apply exact variant_id patches to the active working copy only."""
    initialize_working_copy(force=False)
    working_path = Path(get_active_database_path())
    patches_payload = _read_json(PATCHES_PATH, {"patches": []})
    patches = patches_payload.get("patches") if isinstance(patches_payload, dict) else []
    selected_ids = set(patch_ids or [])
    database = _read_json(working_path, {})
    if not isinstance(database, dict):
        raise ValueError("Working database must be a JSON object.")

    applied: list[dict] = []
    skipped: list[dict] = []
    changes: list[dict] = []
    for patch in [p for p in patches if isinstance(p, dict)]:
        if selected_ids and patch.get("patch_id") not in selected_ids:
            continue
        if require_safe and patch.get("safe_to_auto_apply") is not True:
            skipped.append({"patch_id": patch.get("patch_id"), "reason": "safe_to_auto_apply is not true"})
            continue
        variant_id = str(patch.get("variant_id") or "").strip()
        variant = _find_variant(database, variant_id)
        if variant is None:
            skipped.append({"patch_id": patch.get("patch_id"), "reason": "variant_id not found"})
            continue
        before = json.loads(json.dumps(variant, ensure_ascii=False))
        if not _set_field(variant, str(patch.get("field") or ""), patch.get("suggested_value")):
            skipped.append({"patch_id": patch.get("patch_id"), "reason": "field not set"})
            continue
        after = json.loads(json.dumps(variant, ensure_ascii=False))
        if before == after:
            skipped.append({"patch_id": patch.get("patch_id"), "reason": "no change"})
            continue
        change = {"patch_id": patch.get("patch_id"), "variant_id": variant_id, "before": before, "after": after}
        change["diff"] = _diff(before, after)
        changes.append(change)
        applied.append({"patch_id": patch.get("patch_id"), "variant_id": variant_id, "field": patch.get("field")})

    working_path.write_text(json.dumps(database, ensure_ascii=False, indent=2), encoding="utf-8")
    audits = [_audit_variant_diff(change) for change in changes] if run_diff_audit else []
    application = {
        "created_at": _utc_now(),
        "working_path": str(working_path),
        "applied_count": len(applied),
        "skipped_count": len(skipped),
        "applied": applied,
        "skipped": skipped,
        "diff_audits": audits,
    }
    _append_jsonl(PATCH_APPLICATIONS_PATH, application)
    return application
