"""Model validation item builder — creates group-level items for model validation.

Each item represents a group of related variants that should be validated together.
Items are NOT created per-variant by default; they are group-level.
"""
from __future__ import annotations

from typing import Any

from engine.validation.normalizer import safe_str
from engine.validation.risk_scorer import score_variant, classify_risk


def build_model_validation_items(
    suspicious_groups: list[dict],
    canonical: dict,
    deterministic_issues: list[dict] | None = None,
    partial_classifications: list[dict] | None = None,
) -> list[dict]:
    """Build group-level model validation items from suspicious groups.

    Each item contains all information needed for a model call:
    - validation_item_id
    - group_type
    - seed_id
    - variant_ids
    - group_data (variants and context)
    - deterministic_issues (for this group)
    - partial_classifications (for this group)
    - risk_level
    - reason_for_model_validation
    - requires_openai_second_opinion_initially

    Returns a list of model validation items.
    """
    det_issues = deterministic_issues or []
    partial_class = partial_classifications or []

    # Index deterministic issues by variant_id
    det_by_variant: dict[str, list[dict]] = {}
    for issue in det_issues:
        vid = issue.get("variant_id", "")
        if vid:
            det_by_variant.setdefault(vid, []).append(issue)

    # Index partial classifications by variant_id
    partial_by_variant: dict[str, dict] = {}
    for pc in partial_class:
        vid = pc.get("variant_id", "")
        if vid:
            partial_by_variant[vid] = pc

    # Index all variants by seed_id
    all_variants = (canonical.get("verified_variants") or []) + \
                   (canonical.get("partial_variants") or [])
    variants_by_seed: dict[str, list[dict]] = {}
    for v in all_variants:
        if isinstance(v, dict):
            sid = str(v.get("seed_id", "")).strip()
            if sid:
                variants_by_seed.setdefault(sid, []).append(v)

    items: list[dict] = []

    for group in suspicious_groups:
        seed_id = group.get("seed_id", "")
        reason = group.get("reason", "")
        risk_level = group.get("risk_level", "medium")
        variant_ids = group.get("variant_ids", [])

        # Get the actual variant dicts
        seed_variants = variants_by_seed.get(seed_id, [])
        group_variants = [
            v for v in seed_variants
            if v.get("variant_id") in variant_ids
        ] if variant_ids else seed_variants

        # Collect deterministic issues for this group
        group_det_issues = []
        for vid in variant_ids:
            group_det_issues.extend(det_by_variant.get(vid, []))

        # Collect partial classifications for this group
        group_partial = []
        for vid in variant_ids:
            pc = partial_by_variant.get(vid)
            if pc:
                group_partial.append(pc)

        # Determine group_type
        group_type = _classify_group_type(reason, risk_level, group_partial)

        # Determine if OpenAI second opinion is needed initially
        needs_openai = _initial_openai_needed(
            risk_level, reason, group_det_issues, group_partial
        )

        item = {
            "validation_item_id": f"mvi_{group.get('group_id', seed_id)}",
            "group_type": group_type,
            "seed_id": seed_id,
            "variant_ids": variant_ids,
            "group_data": {
                "variants": _slim_variants(group_variants),
                "variant_count": len(group_variants),
                "trim_candidates": _extract_trim_candidates(group_variants),
            },
            "deterministic_issues": [
                {"issue_type": i.get("issue_type"), "severity": i.get("severity"),
                 "variant_id": i.get("variant_id")}
                for i in group_det_issues
            ],
            "partial_classifications": [
                {"variant_id": pc.get("variant_id"),
                 "validation_status": pc.get("validation_status"),
                 "risk_level": pc.get("risk_level")}
                for pc in group_partial
            ],
            "risk_level": risk_level,
            "reason_for_model_validation": reason,
            "requires_openai_second_opinion_initially": needs_openai,
        }

        items.append(item)

    return items


def _classify_group_type(
    reason: str, risk_level: str, partial_class: list[dict]
) -> str:
    """Classify the group type based on reason and context."""
    reason_lower = reason.lower()

    if "failed_seed" in reason_lower:
        return "targeted_seed"
    if "manual_review" in reason_lower:
        return "manual_review_seed"
    if "merge" in reason_lower:
        return "merge_candidate"
    if "no_evidence" in reason_lower or "weak_source" in reason_lower:
        return "evidence_gap"
    if "source_conflict" in reason_lower or "inconsistent" in reason_lower:
        return "source_conflict"
    if "il_confirmed" in reason_lower or "il_market" in reason_lower:
        return "il_market_plausibility"

    # Check partial classifications for merge candidates
    if any(pc.get("validation_status") == "merge_candidate" for pc in partial_class):
        return "merge_candidate"

    return "partial_group"


def _initial_openai_needed(
    risk_level: str,
    reason: str,
    det_issues: list[dict],
    partial_class: list[dict],
) -> bool:
    """Determine if OpenAI is needed from the start (before seeing Gemini results)."""
    # Critical risk always needs dual validation
    if risk_level == "critical":
        return True

    # High risk with critical deterministic issues
    if risk_level == "high":
        has_critical = any(i.get("severity") == "critical" for i in det_issues)
        if has_critical:
            return True

    # Source conflicts need dual validation
    if "source_conflict" in reason.lower():
        return True

    return False


def _slim_variants(variants: list[dict]) -> list[dict]:
    """Return slim variant dicts for model prompts (exclude large fields)."""
    slim = []
    for v in variants:
        slim.append({
            "variant_id": v.get("variant_id", ""),
            "make": v.get("make", ""),
            "model": v.get("model", ""),
            "generation": v.get("generation"),
            "trim": v.get("trim"),
            "engine": v.get("engine"),
            "fuel_type": v.get("fuel_type"),
            "transmission": v.get("transmission"),
            "drivetrain": v.get("drivetrain"),
            "body_type": v.get("body_type"),
            "year_start": v.get("year_start"),
            "year_end": v.get("year_end"),
            "market_scope": v.get("market_scope"),
            "official_marketed_name_il": v.get("official_marketed_name_il"),
            "confidence_level": v.get("confidence_level"),
            "source_ids": v.get("source_ids", []),
        })
    return slim


def _extract_trim_candidates(variants: list[dict]) -> list[str]:
    """Extract unique trim candidates from variants."""
    trims = set()
    for v in variants:
        t = safe_str(v.get("trim"))
        if t:
            trims.add(t)
    return sorted(trims)
