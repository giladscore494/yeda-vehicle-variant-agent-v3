"""Build and apply exact surgical patches to the active working copy."""
from __future__ import annotations

import copy
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.paths import (
    ACTIVE_WORKING_DATABASE_PATH,
    DECISIONS_PATH,
    PATCH_APPLICATIONS_PATH,
    PATCHES_PATH,
    SOURCE_CANONICAL_PATH,
)
from engine.validation.run_events import log_event
from engine.validation.write_guard import safe_write_json

_ALLOWED_PATCH_ACTIONS = {
    "update_fields",
    "normalize_fields",
    "differentiate_duplicate",
    "mark_manual_review",
}
_NEVER_AUTO_PATCH_ACTIONS = {
    "reject",
    "reject_candidate",
    "merge",
    "merge_variant",
    "change_year_range",
    "change_market_scope",
    "promote_to_verified",
    "resolve_source_conflict",
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


def _sha256_file(path: str | Path) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _hash_record(record: Any) -> str:
    raw = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _decisions_list(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        return [item for item in payload.get("decisions", []) if isinstance(item, dict)]
    return []


def _all_variant_lists(payload: dict) -> list[list[dict]]:
    lists: list[list[dict]] = []
    for key in ("verified_variants", "partial_variants", "vehicles"):
        value = payload.get(key)
        if isinstance(value, list):
            lists.append(value)
    return lists


def _all_variants(payload: dict) -> list[dict]:
    variants: list[dict] = []
    for variant_list in _all_variant_lists(payload):
        variants.extend(item for item in variant_list if isinstance(item, dict))
    return variants


def _variant_ids(payload: dict) -> list[str]:
    return [str(v.get("variant_id") or "") for v in _all_variants(payload) if v.get("variant_id")]


def _find_exact_variant(payload: dict, variant_id: str) -> dict:
    matches = [v for v in _all_variants(payload) if str(v.get("variant_id") or "") == variant_id]
    if len(matches) != 1:
        if not matches:
            raise ValueError(f"variant_id not found exactly once: {variant_id}")
        raise ValueError(f"variant_id is duplicated: {variant_id}")
    return matches[0]


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


def _set_existing_field(container: Any, field: str, value: Any) -> None:
    parts = _field_parts(field)
    if not parts:
        raise ValueError("empty field path")
    current = container
    for part in parts[:-1]:
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            raise ValueError(f"field path does not exist: {field}")
    last = parts[-1]
    if isinstance(current, dict) and last in current:
        current[last] = value
        return
    if isinstance(current, list) and last.isdigit() and int(last) < len(current):
        current[int(last)] = value
        return
    raise ValueError(f"field path does not exist: {field}")


def _decision_id(decision: dict) -> str:
    for key in ("decision_id", "id", "source_decision_id"):
        value = decision.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return f"decision_{uuid.uuid4().hex}"


def _decision_action(decision: dict) -> str:
    for key in ("action", "decision_action", "recommended_action", "final_recommendation"):
        value = decision.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "update_fields"


def _audit_run_id(decision: dict) -> str:
    for key in ("audit_run_id", "validation_run_id", "run_id"):
        value = decision.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _extract_variant_ids(decision: dict) -> list[str]:
    raw = decision.get("variant_ids")
    if isinstance(raw, list):
        ids = [str(item).strip() for item in raw if str(item).strip()]
    else:
        single = str(decision.get("variant_id") or "").strip()
        ids = [single] if single else []
    return ids if len(ids) == len(set(ids)) else []


def _extract_field_changes(decision: dict, variant_ids: list[str]) -> dict[str, dict[str, dict[str, Any]]] | None:
    raw = decision.get("field_changes")
    if not isinstance(raw, dict) or not raw:
        return None

    # Preferred schema: {variant_id: {field_name: {from: ..., to: ...}}}
    if all(isinstance(raw.get(variant_id), dict) for variant_id in variant_ids):
        normalized: dict[str, dict[str, dict[str, Any]]] = {}
        for variant_id in variant_ids:
            field_map = raw.get(variant_id)
            if not isinstance(field_map, dict) or not field_map:
                return None
            normalized[variant_id] = {}
            for field_name, change in field_map.items():
                if not isinstance(field_name, str) or not field_name.strip() or not isinstance(change, dict):
                    return None
                if "from" not in change or "to" not in change:
                    return None
                normalized[variant_id][field_name.strip()] = {"from": change.get("from"), "to": change.get("to")}
        return normalized

    # Single-variant convenience schema: {field_name: {from: ..., to: ...}}
    if len(variant_ids) == 1 and all(isinstance(change, dict) for change in raw.values()):
        field_map: dict[str, dict[str, Any]] = {}
        for field_name, change in raw.items():
            if not isinstance(field_name, str) or not field_name.strip():
                return None
            if "from" not in change or "to" not in change:
                return None
            field_map[field_name.strip()] = {"from": change.get("from"), "to": change.get("to")}
        return {variant_ids[0]: field_map}

    return None


def _decision_summary(decision: dict) -> str:
    for key in ("summary", "reason", "rationale", "notes", "recommendation"):
        value = decision.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "Exact field-change decision."


def _patch_from_decision(decision: dict) -> tuple[dict | None, str]:
    action = _decision_action(decision)
    action_key = action.lower()
    if action_key in _NEVER_AUTO_PATCH_ACTIONS:
        return None, "manual_review_required"

    variant_ids = _extract_variant_ids(decision)
    field_changes = _extract_field_changes(decision, variant_ids) if variant_ids else None
    if not variant_ids or field_changes is None:
        return None, "manual_review_required"

    patch_action = action if action in _ALLOWED_PATCH_ACTIONS else "update_fields"
    explicit_safe = decision.get("safe_to_apply", decision.get("safe_to_auto_apply", False)) is True
    status = "pending" if explicit_safe else "blocked"
    return (
        {
            "patch_id": f"patch_{uuid.uuid4().hex}",
            "created_at": _utc_now(),
            "source_decision_id": _decision_id(decision),
            "audit_run_id": _audit_run_id(decision),
            "active_source_hash": _sha256_file(ACTIVE_WORKING_DATABASE_PATH),
            "golden_source_hash": _sha256_file(SOURCE_CANONICAL_PATH),
            "variant_ids": variant_ids,
            "action": patch_action,
            "safe_to_apply": explicit_safe,
            "requires_diff_audit": True,
            "field_changes": field_changes,
            "reason": _decision_summary(decision),
            "confidence": float(decision.get("confidence", 0.0) or 0.0),
            "status": status,
            "blocking_reason": None if explicit_safe else "safe_to_apply is not true",
        },
        "pending" if explicit_safe else "blocked",
    )


def build_candidate_patches_from_decisions() -> dict:
    """Create candidate patches only from exact variant IDs and exact from/to changes."""
    decisions = _decisions_list(_read_json(DECISIONS_PATH, {"decisions": []}))
    patches: list[dict] = []
    summary = {"pending": 0, "blocked": 0, "manual_review_required": 0, "created_count": 0}
    for decision in decisions:
        patch, category = _patch_from_decision(decision)
        if patch is None:
            summary["manual_review_required"] += 1
            continue
        patches.append(patch)
        summary[category] += 1
        summary["created_count"] += 1

    payload = {"created_at": _utc_now(), "decisions_path": DECISIONS_PATH, "patches": patches, **summary}
    payload["patch_count"] = summary["created_count"]
    safe_write_json(payload, PATCHES_PATH)
    return payload


def _load_patches_payload() -> dict:
    payload = _read_json(PATCHES_PATH, {"patches": []})
    if not isinstance(payload, dict):
        raise ValueError("patches.json must be a JSON object")
    patches = payload.get("patches")
    if not isinstance(patches, list):
        raise ValueError("patches.json must contain a patches list")
    return payload


def _write_patches_payload(payload: dict) -> None:
    patches = [p for p in payload.get("patches", []) if isinstance(p, dict)]
    payload["pending"] = sum(1 for p in patches if p.get("status") == "pending")
    payload["blocked"] = sum(1 for p in patches if p.get("status") == "blocked")
    payload["created_count"] = len(patches)
    payload["patch_count"] = len(patches)
    safe_write_json(payload, PATCHES_PATH)


def _patch_changed_fields(patch: dict) -> dict[str, list[str]]:
    return {
        variant_id: sorted(field_changes.keys())
        for variant_id, field_changes in (patch.get("field_changes") or {}).items()
        if isinstance(field_changes, dict)
    }


def assert_no_unexplained_variant_loss(before_variants: list[dict], after_variants: list[dict], patch: dict) -> None:
    """Block any variant removal not explicitly safe reject-approved by the patch."""
    if len(after_variants) >= len(before_variants):
        return
    before_ids = {str(v.get("variant_id") or "") for v in before_variants if isinstance(v, dict) and v.get("variant_id")}
    after_ids = {str(v.get("variant_id") or "") for v in after_variants if isinstance(v, dict) and v.get("variant_id")}
    removed = sorted(before_ids - after_ids)
    approved = set(str(v) for v in patch.get("variant_ids") or [])
    if not removed or patch.get("action") != "reject_candidate" or patch.get("safe_to_apply") is not True:
        raise ValueError(f"unexplained variant loss blocked: {removed}")
    if any(variant_id not in approved for variant_id in removed):
        raise ValueError(f"unexplained variant loss blocked: {removed}")


def _apply_patch_object(patch: dict, database: dict) -> dict:
    if patch.get("safe_to_apply") is not True:
        raise ValueError("patch is not safe_to_apply")
    if patch.get("status") != "pending":
        raise ValueError("patch is not pending")
    variant_ids = patch.get("variant_ids")
    field_changes = patch.get("field_changes")
    if not isinstance(variant_ids, list) or not variant_ids:
        raise ValueError("patch must contain variant_ids")
    if not isinstance(field_changes, dict) or not field_changes:
        raise ValueError("patch must contain field_changes")

    before_variants = copy.deepcopy(_all_variants(database))
    before_snapshots: dict[str, dict] = {}
    after_snapshots: dict[str, dict] = {}
    before_hashes: dict[str, str] = {}
    after_hashes: dict[str, str] = {}

    for raw_variant_id in variant_ids:
        variant_id = str(raw_variant_id).strip()
        changes = field_changes.get(variant_id)
        if not isinstance(changes, dict) or not changes:
            raise ValueError(f"missing field changes for variant_id: {variant_id}")
        variant = _find_exact_variant(database, variant_id)
        before_snapshots[variant_id] = copy.deepcopy(variant)
        before_hashes[variant_id] = _hash_record(variant)
        for field_name, change in changes.items():
            if not isinstance(change, dict) or "from" not in change or "to" not in change:
                raise ValueError(f"invalid field change for {variant_id}.{field_name}")
            current = _get_field(variant, str(field_name))
            if current != change.get("from"):
                raise ValueError(f"from value mismatch for {variant_id}.{field_name}")
        for field_name, change in changes.items():
            _set_existing_field(variant, str(field_name), change.get("to"))
        after_snapshots[variant_id] = copy.deepcopy(variant)
        after_hashes[variant_id] = _hash_record(variant)

    after_variants = copy.deepcopy(_all_variants(database))
    assert_no_unexplained_variant_loss(before_variants, after_variants, patch)
    return {
        "before": before_snapshots,
        "after": after_snapshots,
        "before_hashes": before_hashes,
        "after_hashes": after_hashes,
        "variant_count_before": len(before_variants),
        "variant_count_after": len(after_variants),
        "variant_count_delta": len(after_variants) - len(before_variants),
    }


def _block_patch(patches_payload: dict, patch: dict, reason: str) -> dict:
    patch["status"] = "blocked"
    patch["blocking_reason"] = reason
    _write_patches_payload(patches_payload)
    return {"patch_id": patch.get("patch_id"), "status": "blocked", "blocking_reason": reason}


def _apply_selected_patch(patch: dict, patches_payload: dict) -> dict:
    working_path = Path(ACTIVE_WORKING_DATABASE_PATH)
    if not working_path.exists():
        return _block_patch(patches_payload, patch, "Initialize Working Copy first.")
    database = _read_json(working_path)
    if not isinstance(database, dict):
        return _block_patch(patches_payload, patch, "working database must be a JSON object")

    original_database = copy.deepcopy(database)
    try:
        application = _apply_patch_object(patch, database)
    except Exception as exc:
        return _block_patch(patches_payload, patch, str(exc))

    if database == original_database:
        return {"patch_id": patch.get("patch_id"), "status": "no_change", "variant_ids": patch.get("variant_ids", [])}

    working_path.write_text(json.dumps(database, ensure_ascii=False, indent=2), encoding="utf-8")
    patch["status"] = "applied_pending_audit"
    patch["blocking_reason"] = None
    _write_patches_payload(patches_payload)

    event = {
        "created_at": _utc_now(),
        "patch_id": patch.get("patch_id"),
        "source_decision_id": patch.get("source_decision_id"),
        "variant_ids": patch.get("variant_ids", []),
        "changed_fields": _patch_changed_fields(patch),
        "before": application["before"],
        "after": application["after"],
        "field_changes": patch.get("field_changes", {}),
        "variant_count_before": application["variant_count_before"],
        "variant_count_after": application["variant_count_after"],
        "variant_count_delta": application["variant_count_delta"],
        "status": "applied_pending_audit",
        "working_path": ACTIVE_WORKING_DATABASE_PATH,
    }
    _append_jsonl(PATCH_APPLICATIONS_PATH, event)
    log_event(
        {
            "stage": "surgical_patch",
            "event_type": "patch_applied",
            "status": "applied_pending_audit",
            "item_id": str(patch.get("patch_id") or ""),
            "request_summary": f"variant_ids={','.join(patch.get('variant_ids', []))}",
        }
    )
    return {
        "patch_id": patch.get("patch_id"),
        "variant_ids": patch.get("variant_ids", []),
        "changed_fields": _patch_changed_fields(patch),
        "status": "applied_pending_audit",
        "before_hashes": application["before_hashes"],
        "after_hashes": application["after_hashes"],
    }


def apply_next_safe_patch() -> dict:
    """Apply exactly one pending safe patch to the working copy."""
    patches_payload = _load_patches_payload()
    for patch in patches_payload.get("patches", []):
        if isinstance(patch, dict) and patch.get("status") == "pending" and patch.get("safe_to_apply") is True:
            return _apply_selected_patch(patch, patches_payload)
    return {"status": "no_pending_safe_patch", "patch_id": None, "variant_ids": [], "changed_fields": {}}


def apply_surgical_patch(patch_id: str) -> dict:
    """Apply one explicit pending patch by patch_id using exact variant_id matching only."""
    patches_payload = _load_patches_payload()
    for patch in patches_payload.get("patches", []):
        if isinstance(patch, dict) and patch.get("patch_id") == patch_id:
            return _apply_selected_patch(patch, patches_payload)
    raise ValueError(f"patch_id not found: {patch_id}")


# Backwards-compatible wrappers for the previous Streamlit helper/tests.
def build_candidate_surgical_patches() -> dict:
    return build_candidate_patches_from_decisions()


def apply_surgical_patches(*, require_safe: bool = True, run_diff_audit: bool = False, patch_ids: list[str] | None = None) -> dict:
    if patch_ids:
        results = [apply_surgical_patch(patch_id) for patch_id in patch_ids]
    else:
        results = [apply_next_safe_patch()]
    applied = [r for r in results if r.get("status") == "applied_pending_audit"]
    skipped = [r for r in results if r.get("status") != "applied_pending_audit"]
    return {"applied_count": len(applied), "skipped_count": len(skipped), "applied": applied, "skipped": skipped, **results[-1]}
