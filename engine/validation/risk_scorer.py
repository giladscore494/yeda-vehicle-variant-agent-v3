"""Risk scorer for validation.

Assigns risk_score (0-100) to each variant and group based on:
- verification status, market scope, source coverage
- trim confidence, duplicate conflicts, field completeness
"""
from __future__ import annotations

from engine.validation.normalizer import safe_str
from engine.validation.group_builder import group_has_conflicts, get_group_trim_candidates

LOW_RISK_MAX = 25
MEDIUM_RISK_MAX = 50
HIGH_RISK_MAX = 75


def score_variant(variant: dict) -> int:
    """Score a single variant from 0 (safe) to 100 (critical)."""
    score = 0

    # Verification status
    vs = safe_str(variant.get("verification_status"))
    if vs == "partial":
        score += 15
    elif vs != "verified":
        score += 30

    # Market scope
    ms = safe_str(variant.get("market_scope"))
    if ms == "il-confirmed":
        pass
    elif ms == "il-likely":
        score += 10
    elif ms == "global-reference-only":
        score += 25
    else:
        score += 15

    # Source coverage
    sources_count = variant.get("sources_count") or 0
    if isinstance(sources_count, dict):
        sources_count = sources_count.get("value", 0) or 0
    try:
        sources_count = int(sources_count)
    except (ValueError, TypeError):
        sources_count = 0

    if sources_count == 0:
        score += 20
    elif sources_count == 1:
        score += 10
    elif sources_count <= 2:
        score += 5

    # Source IDs quality
    source_ids = variant.get("source_ids") or []
    if not source_ids:
        score += 10
    else:
        from core.source_ids import looks_like_placeholder_source_id

        placeholder_count = sum(1 for s in source_ids if looks_like_placeholder_source_id(s))
        if placeholder_count == len(source_ids):
            score += 15
        elif placeholder_count > 0:
            score += 5

    # Trim confidence
    trim_field = variant.get("trim")
    if trim_field is None:
        score += 10
    else:
        trim_val = safe_str(trim_field)
        if not trim_val or trim_val in ("unknown", "base", "standard", "n/a"):
            score += 10
        if isinstance(trim_field, dict):
            if safe_str(trim_field.get("status")) == "partial":
                score += 5
            trim_conf = safe_str(trim_field.get("confidence"))
            if trim_conf == "low":
                score += 10
            elif trim_conf == "medium":
                score += 5

    # Identity confidence
    ic = safe_str(variant.get("identity_confidence"))
    if ic == "candidate_unverified":
        score += 10
    elif not ic or ic == "unknown":
        score += 5

    # Official marketed name
    if not variant.get("official_marketed_name_il"):
        score += 5

    # Confidence level
    conf = safe_str(variant.get("confidence"))
    if conf == "low":
        score += 10
    elif conf == "medium":
        score += 5

    return min(score, 100)


def score_group(group: list[dict]) -> int:
    """Score a group by combining individual scores and conflict analysis."""
    if not group:
        return 0
    max_individual = max(score_variant(v) for v in group)
    conflicts = group_has_conflicts(group)
    conflict_count = sum(1 for c in conflicts.values() if c)
    conflict_bonus = conflict_count * 10
    trims = get_group_trim_candidates(group)
    if len(trims) > 3:
        conflict_bonus += 10
    return min(max_individual + conflict_bonus, 100)


def classify_risk(score: int) -> str:
    """Classify a risk score into a risk level."""
    if score <= LOW_RISK_MAX:
        return "low"
    if score <= MEDIUM_RISK_MAX:
        return "medium"
    if score <= HIGH_RISK_MAX:
        return "high"
    return "critical"


def determine_action(risk_level: str) -> str:
    """Determine validation action based on risk level."""
    if risk_level == "low":
        return "trusted_existing_deterministic"
    if risk_level == "medium":
        return "gemini_only"
    if risk_level == "high":
        return "gemini_and_openai"
    return "dual_model_required"
