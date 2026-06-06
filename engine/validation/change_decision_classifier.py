"""Deterministic classifier for post-model-review change decisions."""
from __future__ import annotations

from typing import Any

_NO_CHANGE_TOKENS = {
    "no_action",
    "no-change",
    "no_change",
    "keep",
    "verified",
    "no_correction_needed",
}
_NEGLIGIBLE_TOKENS = {
    "negligible",
    "cosmetic",
    "minor_formatting",
    "formatting_only",
    "spelling",
    "typo",
}
_UNSAFE_ACTIONS = {
    "reject",
    "merge",
    "change_year_range",
    "change_market_scope",
    "promote_to_verified",
}
_CRITICAL_FIELDS = {
    "model",
    "official_model_name",
    "make",
    "market_scope",
    "israeli_market_existence",
    "year_start",
    "year_end",
    "generation",
    "engine_displacement",
    "engine_family",
    "fuel_type",
    "transmission",
    "body_type",
    "drivetrain",
    "trim",
    "variant_name",
    "variant_identity",
    "duplicate_identity",
}
_CRITICAL_FIELD_ALIASES = {
    "model_name": "model",
    "make_name": "make",
    "market": "market_scope",
    "yearfrom": "year_start",
    "yearto": "year_end",
    "engine_cc": "engine_displacement",
    "engine_capacity": "engine_displacement",
    "engine": "engine_family",
    "transmission_type": "transmission",
    "body": "body_type",
    "drive_type": "drivetrain",
    "drivetrain_type": "drivetrain",
    "trim_name": "trim",
    "variant": "variant_name",
}
_CRITICAL_ISSUE_HINTS = {
    "identity",
    "market_scope",
    "market_presence",
    "make_model",
    "year",
    "generation",
    "engine",
    "fuel",
    "transmission",
    "body_type",
    "drivetrain",
    "duplicate",
}


def _normalized_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip().lower()
    return ""


def _recommendation_tokens(*values: Any) -> set[str]:
    tokens: set[str] = set()
    for raw in values:
        text = _normalized_text(raw)
        if not text:
            continue
        if text.startswith("manual_approval_required:"):
            text = text.split(":", 1)[1]
        tokens.add(text)
    return tokens


def _extract_result_payload(result: Any) -> dict:
    if not isinstance(result, dict):
        return {}
    parsed = result.get("parsed_result")
    if isinstance(parsed, dict):
        return parsed
    return result


def _collect_variant_ids(decision: dict, item: dict | None = None) -> list[str]:
    ids: list[str] = []
    for payload in (decision, item or {}):
        raw = payload.get("variant_ids")
        if isinstance(raw, list):
            ids.extend(str(value).strip() for value in raw if str(value).strip())
        raw_single = payload.get("variant_id")
        if raw_single:
            ids.append(str(raw_single).strip())
    unique: list[str] = []
    for value in ids:
        if value and value not in unique:
            unique.append(value)
    return unique


def _field_changes(decision: dict, gemini: dict, openai: dict) -> Any:
    for payload in (decision, openai, gemini):
        candidate = payload.get("field_changes")
        if isinstance(candidate, dict):
            return candidate
    return {}


def _normalize_field_name(field: str) -> str:
    head = field.replace("[", ".").replace("]", "").split(".", 1)[0]
    normalized = _normalized_text(head)
    return _CRITICAL_FIELD_ALIASES.get(normalized, normalized)


def _critical_fields_from_changes(field_changes: dict) -> list[str]:
    fields: set[str] = set()
    for variant_map in field_changes.values():
        if not isinstance(variant_map, dict):
            continue
        for field_name in variant_map.keys():
            if not isinstance(field_name, str):
                continue
            normalized = _normalize_field_name(field_name)
            if normalized in _CRITICAL_FIELDS:
                fields.add(normalized)
    return sorted(fields)


def _has_exact_field_changes(field_changes: dict, variant_ids: list[str]) -> bool:
    if not isinstance(field_changes, dict) or not field_changes or not variant_ids:
        return False
    for variant_id in variant_ids:
        changes = field_changes.get(variant_id)
        if not isinstance(changes, dict) or not changes:
            return False
        for change in changes.values():
            if not isinstance(change, dict) or "from" not in change or "to" not in change:
                return False
    return True


def _issue_hints(decision: dict, item: dict | None, gemini: dict, openai: dict) -> set[str]:
    hints: set[str] = set()
    for payload in (item or {}, decision, gemini, openai):
        value = payload.get("issue_type")
        text = _normalized_text(value)
        if text:
            hints.add(text)
    return hints


def _is_negligible(decision: dict, gemini: dict, openai: dict) -> bool:
    for payload in (decision, openai, gemini):
        for key in ("change_severity", "severity", "issue_severity"):
            if _normalized_text(payload.get(key)) in {"negligible", "minor", "cosmetic"}:
                return True
        for key in ("summary", "reason", "rationale", "change_reason"):
            text = _normalized_text(payload.get(key))
            if any(token in text for token in _NEGLIGIBLE_TOKENS):
                return True
    return False


def classify_change_decision(decision: dict, item: dict | None = None) -> dict:
    """Return a strict binary change decision payload."""
    decision = decision if isinstance(decision, dict) else {}
    item = item if isinstance(item, dict) else {}
    gemini = _extract_result_payload(decision.get("gemini_result"))
    openai = _extract_result_payload(decision.get("openai_result"))

    tokens = _recommendation_tokens(
        decision.get("final_recommendation"),
        decision.get("recommended_action"),
        decision.get("action"),
        item.get("recommended_action"),
        gemini.get("recommendation"),
        gemini.get("final_recommendation"),
        gemini.get("action"),
        openai.get("recommendation"),
        openai.get("final_recommendation"),
        openai.get("action"),
    )
    risk_level = _normalized_text(
        decision.get("risk_level")
        or item.get("risk_level")
        or openai.get("risk_level")
        or gemini.get("risk_level")
    )
    field_changes = _field_changes(decision, gemini, openai)
    variant_ids = _collect_variant_ids(decision, item)
    has_exact_changes = _has_exact_field_changes(field_changes if isinstance(field_changes, dict) else {}, variant_ids)
    critical_fields_impacted = _critical_fields_from_changes(field_changes if isinstance(field_changes, dict) else {})
    issue_hints = _issue_hints(decision, item, gemini, openai)
    clear_material_issue = bool(critical_fields_impacted) or risk_level in {"high", "critical"} or any(
        any(marker in issue for marker in _CRITICAL_ISSUE_HINTS) for issue in issue_hints
    )

    if tokens & _NO_CHANGE_TOKENS:
        return {
            "change_decision": "NO_CHANGE_REQUIRED",
            "change_severity": "negligible",
            "change_reason": "Model recommendation indicates no actionable data correction.",
            "critical_fields_impacted": [],
            "patchable": False,
            "patchability_reason": "no_change_needed",
        }

    if _is_negligible(decision, gemini, openai):
        return {
            "change_decision": "NO_CHANGE_REQUIRED",
            "change_severity": "negligible",
            "change_reason": "Issue appears cosmetic/negligible and not worth changing database records.",
            "critical_fields_impacted": [],
            "patchable": False,
            "patchability_reason": "no_change_needed",
        }

    unsafe_requested = any(token in _UNSAFE_ACTIONS for token in tokens)
    if unsafe_requested and clear_material_issue:
        severity = "critical" if risk_level == "critical" or len(critical_fields_impacted) >= 2 else "material"
        impacted = critical_fields_impacted or (["market_scope"] if "change_market_scope" in tokens else ["variant_identity"])
        return {
            "change_decision": "CHANGE_REQUIRED",
            "change_severity": severity,
            "change_reason": "Material issue detected but requested action is non-surgical and requires manual approval.",
            "critical_fields_impacted": impacted,
            "patchable": False,
            "patchability_reason": "unsafe_action",
        }

    if has_exact_changes and critical_fields_impacted:
        severity = "critical" if risk_level == "critical" or len(critical_fields_impacted) >= 2 else "material"
        return {
            "change_decision": "CHANGE_REQUIRED",
            "change_severity": severity,
            "change_reason": "Exact factual correction exists for critical/material vehicle-knowledge fields.",
            "critical_fields_impacted": critical_fields_impacted,
            "patchable": True,
            "patchability_reason": "exact_field_changes_available",
        }

    if clear_material_issue and has_exact_changes:
        severity = "critical" if risk_level == "critical" else "material"
        return {
            "change_decision": "CHANGE_REQUIRED",
            "change_severity": severity,
            "change_reason": "Issue is material and has exact field changes, but critical field mapping is indirect.",
            "critical_fields_impacted": critical_fields_impacted,
            "patchable": True,
            "patchability_reason": "exact_field_changes_available",
        }

    if clear_material_issue and not has_exact_changes:
        severity = "critical" if risk_level == "critical" else "material"
        return {
            "change_decision": "CHANGE_REQUIRED",
            "change_severity": severity,
            "change_reason": "Material issue detected but missing exact variant-level from/to field changes.",
            "critical_fields_impacted": critical_fields_impacted,
            "patchable": False,
            "patchability_reason": "no_exact_field_changes",
        }

    return {
        "change_decision": "NO_CHANGE_REQUIRED",
        "change_severity": "minor",
        "change_reason": "Recommendation is vague or unsupported for an exact factual database correction.",
        "critical_fields_impacted": [],
        "patchable": False,
        "patchability_reason": "vague_recommendation",
    }
