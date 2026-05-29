"""Unified model validation schema — shared by Gemini and OpenAI providers.

Both providers MUST return the SAME strict JSON schema.
This module validates, normalizes, and wraps model outputs.
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

# ── Enum constants ──────────────────────────────────────────────────────

VALID_GROUP_TYPES = frozenset([
    "targeted_seed", "manual_review_seed", "partial_group",
    "merge_candidate", "evidence_gap", "source_conflict",
    "il_market_plausibility",
])

VALID_RECOMMENDATIONS = frozenset([
    "no_action", "needs_evidence", "needs_normalization", "manual_review",
    "build_retry", "merge", "rename_trim", "promote_to_verified",
    "reject", "change_year_range", "change_market_scope",
    "resolve_source_conflict",
])

VALID_RISK_LEVELS = frozenset(["low", "medium", "high", "critical"])

VALID_SOURCE_TYPES = frozenset([
    "canonical", "deterministic_audit", "web", "model_reasoning", None,
])

VALID_PATCH_TYPES = frozenset([
    "none", "field_update", "merge", "status_change", "manual_review_flag",
])

VALID_MODEL_ROLES = frozenset(["primary", "second_opinion"])

# Recommendations that are "risky" and require OpenAI second opinion
RISKY_RECOMMENDATIONS = frozenset([
    "build_retry", "merge", "rename_trim", "promote_to_verified",
    "reject", "change_year_range", "change_market_scope",
    "resolve_source_conflict",
])


def _default_evidence() -> list[dict]:
    return []


def _default_suggested_patch() -> dict:
    return {
        "has_patch": False,
        "patch_type": "none",
        "target_variant_id": None,
        "field": None,
        "current_value": None,
        "suggested_value": None,
        "reason": None,
        "safe_to_auto_apply": False,
    }


def _default_validation_item() -> dict:
    """Return a blank validation item with all required fields."""
    return {
        "validation_item_id": "",
        "group_type": "partial_group",
        "seed_id": None,
        "variant_ids": [],
        "model_name": "",
        "model_role": "primary",
        "recommendation": "no_action",
        "confidence": 0.0,
        "risk_level": "medium",
        "evidence": _default_evidence(),
        "issues_found": [],
        "suggested_patch": _default_suggested_patch(),
        "needs_build_retry": False,
        "needs_manual_review": False,
        "needs_data_correction": False,
        "safe_to_auto_apply": False,
    }


# ── Validation ──────────────────────────────────────────────────────────

class SchemaValidationError(Exception):
    """Raised when model output fails schema validation."""
    pass


def validate_item(item: dict) -> list[str]:
    """Validate a single model validation item against the unified schema.

    Returns a list of error strings.  Empty list means valid.
    """
    errors: list[str] = []

    if not isinstance(item, dict):
        return ["item is not a dict"]

    # Required string fields
    for field in ("validation_item_id", "model_name"):
        if not isinstance(item.get(field), str) or not item[field]:
            errors.append(f"missing or empty required field: {field}")

    # group_type enum
    gt = item.get("group_type")
    if gt not in VALID_GROUP_TYPES:
        errors.append(f"invalid group_type: {gt!r}")

    # model_role enum
    mr = item.get("model_role")
    if mr not in VALID_MODEL_ROLES:
        errors.append(f"invalid model_role: {mr!r}")

    # recommendation enum
    rec = item.get("recommendation")
    if rec not in VALID_RECOMMENDATIONS:
        errors.append(f"invalid recommendation: {rec!r}")

    # confidence range
    conf = item.get("confidence")
    if not isinstance(conf, (int, float)) or conf < 0.0 or conf > 1.0:
        errors.append(f"confidence must be 0..1, got {conf!r}")

    # risk_level enum
    rl = item.get("risk_level")
    if rl not in VALID_RISK_LEVELS:
        errors.append(f"invalid risk_level: {rl!r}")

    # variant_ids must be list
    vids = item.get("variant_ids")
    if not isinstance(vids, list):
        errors.append("variant_ids must be a list")

    # evidence validation
    evidence = item.get("evidence")
    if evidence is not None:
        if not isinstance(evidence, list):
            errors.append("evidence must be a list")
        else:
            for i, ev in enumerate(evidence):
                if not isinstance(ev, dict):
                    errors.append(f"evidence[{i}] is not a dict")
                    continue
                st = ev.get("source_type")
                if st is not None and st not in VALID_SOURCE_TYPES:
                    errors.append(f"evidence[{i}].source_type invalid: {st!r}")

    # suggested_patch validation
    patch = item.get("suggested_patch")
    if patch is not None and isinstance(patch, dict):
        pt = patch.get("patch_type")
        if pt is not None and pt not in VALID_PATCH_TYPES:
            errors.append(f"suggested_patch.patch_type invalid: {pt!r}")

    # safe_to_auto_apply must always be False
    if item.get("safe_to_auto_apply") is not False:
        errors.append("safe_to_auto_apply must always be False")

    return errors


def normalize_model_output(raw: dict, item_id: str, model_name: str,
                           model_role: str = "primary") -> dict:
    """Normalize a raw model output dict into the unified schema.

    Fills in defaults for missing fields.  Forces safe_to_auto_apply=False.
    """
    base = _default_validation_item()

    # Map known fields
    base["validation_item_id"] = raw.get("validation_item_id") or item_id
    base["group_type"] = raw.get("group_type") or "partial_group"
    base["seed_id"] = raw.get("seed_id")
    base["variant_ids"] = raw.get("variant_ids") or []
    base["model_name"] = model_name
    base["model_role"] = model_role

    # Map recommendation (handle legacy field names)
    rec = (raw.get("recommendation")
           or raw.get("action")
           or "no_action")
    if rec in VALID_RECOMMENDATIONS:
        base["recommendation"] = rec
    else:
        base["recommendation"] = "manual_review"

    # Map confidence
    conf = raw.get("confidence")
    if isinstance(conf, str):
        conf_map = {"high": 0.9, "medium": 0.6, "low": 0.3}
        conf = conf_map.get(conf.lower(), 0.5)
    if isinstance(conf, (int, float)) and 0.0 <= conf <= 1.0:
        base["confidence"] = float(conf)
    else:
        base["confidence"] = 0.5

    # risk_level
    rl = raw.get("risk_level", "medium")
    base["risk_level"] = rl if rl in VALID_RISK_LEVELS else "medium"

    # evidence
    evidence = raw.get("evidence") or []
    if isinstance(evidence, list):
        normalized_evidence = []
        for ev in evidence:
            if isinstance(ev, dict):
                normalized_evidence.append({
                    "claim": ev.get("claim", ""),
                    "source": ev.get("source"),
                    "source_type": ev.get("source_type") if ev.get("source_type") in VALID_SOURCE_TYPES else None,
                    "supports_recommendation": ev.get("supports_recommendation", True),
                })
            elif isinstance(ev, str):
                normalized_evidence.append({
                    "claim": ev, "source": None,
                    "source_type": "model_reasoning",
                    "supports_recommendation": True,
                })
        base["evidence"] = normalized_evidence

    # issues_found
    base["issues_found"] = raw.get("issues_found") or []

    # suggested_patch
    patch = raw.get("suggested_patch")
    if isinstance(patch, dict):
        base["suggested_patch"] = {
            "has_patch": patch.get("has_patch", False),
            "patch_type": patch.get("patch_type", "none") if patch.get("patch_type") in VALID_PATCH_TYPES else "none",
            "target_variant_id": patch.get("target_variant_id"),
            "field": patch.get("field"),
            "current_value": patch.get("current_value"),
            "suggested_value": patch.get("suggested_value"),
            "reason": patch.get("reason"),
            "safe_to_auto_apply": False,
        }

    # Boolean flags
    base["needs_build_retry"] = bool(raw.get("needs_build_retry", False))
    base["needs_manual_review"] = bool(raw.get("needs_manual_review", False))
    base["needs_data_correction"] = bool(raw.get("needs_data_correction", False))
    base["safe_to_auto_apply"] = False  # Always false

    return base


# ── JSON parsing with repair ────────────────────────────────────────────

def parse_model_json(raw_text: str) -> tuple[dict | None, str | None]:
    """Parse JSON from model response text.

    Returns (parsed_dict, error_type).
    error_type is None on success, 'model_parse_error' on JSON failure.
    Attempts one repair pass (strip markdown fences, trailing commas).
    """
    text = raw_text.strip()

    # Strip markdown fences
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()

    # First attempt
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data, None
        return None, "model_parse_error"
    except json.JSONDecodeError:
        pass

    # Repair attempt: remove trailing commas before } or ]
    repaired = re.sub(r",\s*([}\]])", r"\1", text)
    try:
        data = json.loads(repaired)
        if isinstance(data, dict):
            return data, None
        return None, "model_parse_error"
    except json.JSONDecodeError:
        return None, "model_parse_error"


def wrap_provider_result(
    ok: bool,
    provider: str,
    model_id: str,
    item_id: str,
    parsed_result: dict | None = None,
    raw_text: str = "",
    error_type: str | None = None,
    error_message: str | None = None,
) -> dict:
    """Wrap a provider call result in the normalized envelope."""
    return {
        "ok": ok,
        "provider": provider,
        "model_id": model_id,
        "item_id": item_id,
        "parsed_result": parsed_result or {},
        "raw_text": raw_text,
        "error_type": error_type,
        "error_message": error_message,
    }


def is_risky_recommendation(recommendation: str) -> bool:
    """Return True if the recommendation is considered risky."""
    return recommendation in RISKY_RECOMMENDATIONS


def needs_openai_second_opinion(
    gemini_result: dict,
    deterministic_issues: list[dict] | None = None,
) -> bool:
    """Determine if a Gemini result requires OpenAI second opinion.

    Triggers:
    - Gemini recommends a risky action
    - Gemini confidence < 0.75
    - Gemini response is internally inconsistent
    - Gemini evidence conflicts with deterministic audit
    """
    rec = gemini_result.get("recommendation", "no_action")
    conf = gemini_result.get("confidence", 1.0)

    # Risky recommendation
    if is_risky_recommendation(rec):
        return True

    # Low confidence
    if isinstance(conf, (int, float)) and conf < 0.75:
        return True

    # Evidence conflicts with deterministic audit
    if deterministic_issues:
        det_critical = any(
            i.get("severity") in ("critical", "high")
            for i in deterministic_issues
        )
        if det_critical and rec == "no_action":
            return True

    return False
