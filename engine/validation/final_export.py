"""Final clean database export for the validation workflow.

This module is the only validation component that writes
``data/final/resume_package_final_clean.json``.  It reads the immutable source
canonical package plus validation decisions, applies only explicitly supported
safe deterministic cleanup actions, and leaves higher-risk/model decisions for
manual review.
"""
from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.paths import (
    DECISIONS_PATH,
    FINAL_CLEAN_DATABASE_PATH,
    MANIFEST_PATH,
    SOURCE_CANONICAL_PATH,
)
from engine.validation.write_guard import safe_write_json

_ALLOWED_SAFE_ACTIONS = {
    "whitespace_normalization",
    "casing_normalization",
    "slug_alias_normalization",
    "empty_string_to_null",
    "duplicate_source_id_removal",
}
_NEVER_AUTO_APPLY_ACTIONS = {
    "reject",
    "merge",
    "change_year_range",
    "change_market_scope",
    "promote_to_verified",
    "resolve_source_conflict",
}
_MODEL_SOURCES = {"model", "gemini", "openai", "llm", "ai", "model_review"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: str | Path, default: Any | None = None) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def _write_final_clean_database(payload: dict) -> None:
    """Write the final clean DB path.

    This deliberately does not use ``safe_write_json`` because the shared write
    guard must continue blocking ordinary validation writers from this reserved
    final output.  Keep this private so the public export function is the only
    module entry point that can write the file.
    """
    p = Path(FINAL_CLEAN_DATABASE_PATH)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _decisions_list(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return [d for d in payload if isinstance(d, dict)]
    if isinstance(payload, dict):
        decisions = payload.get("decisions", [])
        if isinstance(decisions, list):
            return [d for d in decisions if isinstance(d, dict)]
    return []


def _all_variants(canonical: dict) -> list[dict]:
    return list(canonical.get("verified_variants") or []) + list(canonical.get("partial_variants") or [])


def _decision_action(decision: dict) -> str:
    for key in ("action", "decision_action", "recommended_action", "final_recommendation"):
        value = decision.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _is_model_generated(decision: dict) -> bool:
    source = str(decision.get("source", "")).lower()
    if any(marker in source for marker in _MODEL_SOURCES):
        return True
    return any(key in decision for key in ("gemini_result", "openai_result", "routing", "primary_model", "secondary_model"))


def _target_matches(variant: dict, decision: dict) -> bool:
    variant_id = decision.get("variant_id")
    if variant_id:
        return variant.get("variant_id") == variant_id

    seed_id = decision.get("seed_id")
    if seed_id:
        if variant.get("seed_id") == seed_id:
            return True
        candidate = variant.get("candidate_raw")
        if isinstance(candidate, dict) and candidate.get("seed_id") == seed_id:
            return True

    # If no target is supplied, the decision is not safely applicable.
    return False


def _field_parts(field: str) -> list[str]:
    return [part for part in field.replace("[", ".").replace("]", "").split(".") if part]


def _get_field(container: Any, field: str) -> Any:
    current = container
    for part in _field_parts(field):
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit():
            idx = int(part)
            current = current[idx] if idx < len(current) else None
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
            idx = int(part)
            current = current[idx] if idx < len(current) else None
        else:
            return False
    last = parts[-1]
    if isinstance(current, dict) and last in current:
        current[last] = value
        return True
    if isinstance(current, list) and last.isdigit():
        idx = int(last)
        if idx < len(current):
            current[idx] = value
            return True
    return False


def _normalize_value(action: str, value: Any, suggested: Any = None) -> tuple[Any, bool]:
    if suggested is not None:
        return suggested, suggested != value
    if action == "whitespace_normalization" and isinstance(value, str):
        normalized = " ".join(value.split())
        return normalized, normalized != value
    if action == "casing_normalization" and isinstance(value, str):
        normalized = value.strip().title()
        return normalized, normalized != value
    if action == "slug_alias_normalization" and isinstance(value, str):
        normalized = "-".join(value.strip().lower().replace("_", "-").split())
        return normalized, normalized != value
    if action == "empty_string_to_null" and isinstance(value, str) and value.strip() == "":
        return None, True
    return value, False


def _dedupe_source_ids(value: Any) -> tuple[Any, bool]:
    if not isinstance(value, list):
        return value, False
    deduped = list(dict.fromkeys(value))
    return deduped, deduped != value


def _apply_safe_decision(variants: list[dict], decision: dict, action: str) -> int:
    field = decision.get("field") or decision.get("target_field")
    suggested = decision.get("suggested_value", decision.get("new_value"))
    applied = 0

    for variant in variants:
        if not _target_matches(variant, decision):
            continue

        if action == "duplicate_source_id_removal":
            candidate_fields = [field] if isinstance(field, str) and field else ["source_ids"]
            for candidate_field in candidate_fields:
                current = _get_field(variant, candidate_field)
                normalized, changed = _dedupe_source_ids(current)
                if changed and _set_field(variant, candidate_field, normalized):
                    applied += 1
            continue

        if not isinstance(field, str) or not field:
            continue
        current = _get_field(variant, field)
        normalized, changed = _normalize_value(action, current, suggested)
        if changed and _set_field(variant, field, normalized):
            applied += 1

    return applied


def _load_manifest() -> dict:
    manifest = _read_json(MANIFEST_PATH, {})
    return manifest if isinstance(manifest, dict) else {}


def export_final_clean_database() -> dict:
    """Export ``data/final/resume_package_final_clean.json`` and return a summary.

    Only supported safe deterministic normalization decisions are applied.  All
    rejection/merge/year/scope/promote/source-conflict actions, unsupported
    actions, untargeted decisions, and model decisions with
    ``safe_to_auto_apply=false`` remain manual-review items.
    """
    canonical = _read_json(SOURCE_CANONICAL_PATH)
    if not isinstance(canonical, dict):
        raise FileNotFoundError(f"Source canonical not found or invalid: {SOURCE_CANONICAL_PATH}")

    decisions_payload = _read_json(DECISIONS_PATH, {"decisions": []})
    decisions = _decisions_list(decisions_payload)
    vehicles = copy.deepcopy(_all_variants(canonical))

    safe_decisions_applied = 0
    model_decisions_not_auto_applied = 0
    manual_review_remaining_count = 0
    rejected_count = 0
    normalized_count = 0

    for decision in decisions:
        action = _decision_action(decision)
        is_model = _is_model_generated(decision)
        safe_to_auto_apply = decision.get("safe_to_auto_apply") is True

        if is_model and not safe_to_auto_apply:
            model_decisions_not_auto_applied += 1
            manual_review_remaining_count += 1
            continue

        if action in _NEVER_AUTO_APPLY_ACTIONS or action.startswith("manual_approval_required:"):
            if action == "reject" or action.endswith(":reject"):
                rejected_count += 1
            manual_review_remaining_count += 1
            continue

        if action not in _ALLOWED_SAFE_ACTIONS:
            manual_review_remaining_count += 1
            continue

        # Deterministic decisions may omit safe_to_auto_apply; model decisions
        # must explicitly opt in above before reaching this point.
        changed = _apply_safe_decision(vehicles, decision, action)
        if changed:
            safe_decisions_applied += 1
            normalized_count += changed
        else:
            manual_review_remaining_count += 1

    created_at = _utc_now()
    manifest = _load_manifest()
    manifest.update({
        "final_clean_database_path": FINAL_CLEAN_DATABASE_PATH,
        "final_clean_database_exported_at": created_at,
        "final_clean_database_source_file": SOURCE_CANONICAL_PATH,
        "final_clean_database_decisions_file": DECISIONS_PATH,
        "final_clean_database_total_output_variants": len(vehicles),
        "final_clean_database_safe_decisions_applied": safe_decisions_applied,
        "final_clean_database_manual_review_remaining_count": manual_review_remaining_count,
    })
    safe_write_json(manifest, MANIFEST_PATH)

    output = {
        "metadata": {
            "created_at": created_at,
            "source_file": SOURCE_CANONICAL_PATH,
            "decisions_file": DECISIONS_PATH,
            "manifest_file": MANIFEST_PATH,
            "total_input_variants": len(_all_variants(canonical)),
            "total_output_variants": len(vehicles),
            "safe_decisions_applied": safe_decisions_applied,
            "model_decisions_not_auto_applied": model_decisions_not_auto_applied,
            "manual_review_remaining_count": manual_review_remaining_count,
            "rejected_count": rejected_count,
            "normalized_count": normalized_count,
        },
        "vehicles": vehicles,
    }
    _write_final_clean_database(output)
    return {"ok": True, "path": FINAL_CLEAN_DATABASE_PATH, **output["metadata"]}
