"""Partial variants handler — classifies partial variants for validation.

Partial variants are a core validation target.
Does NOT delete, auto-promote, or mutate canonical directly.
"""
from __future__ import annotations

from core.source_ids import looks_like_placeholder_source_id
from engine.validation.normalizer import safe_str, extract_year
from engine.validation.risk_scorer import score_variant, classify_risk


# Possible validation statuses for partial variants
PARTIAL_STATUSES = [
    "valid_partial_keep",
    "needs_evidence",
    "needs_normalization",
    "merge_candidate",
    "promote_to_verified_candidate",
    "manual_review_required",
    "reject_candidate",
]


def classify_partial_variant(variant: dict, all_variants: list[dict]) -> dict:
    """Classify a single partial variant into a validation status.

    Returns a validation output dict for this partial variant.
    """
    vid = variant.get("variant_id", "")
    sid = str(variant.get("seed_id", "")).strip()
    risk_score = score_variant(variant)
    risk_level = classify_risk(risk_score)
    issues: list[str] = []

    source_ids = variant.get("source_ids") or []
    has_real_sources = any(
        not looks_like_placeholder_source_id(str(s)) for s in source_ids
    )
    has_placeholder_sources = any(
        looks_like_placeholder_source_id(str(s)) for s in source_ids
    )
    market_scope = (variant.get("market_scope") or "").strip()
    make = safe_str(variant.get("make"))
    model = safe_str(variant.get("model"))
    trim = safe_str(variant.get("trim"))
    body = safe_str(variant.get("body_type"))
    fuel = safe_str(variant.get("fuel_type"))
    trans = safe_str(variant.get("transmission"))
    ys = extract_year(variant.get("year_start"))
    ye = extract_year(variant.get("year_end"))

    # ── Classification logic ────────────────────────────────────────────

    status = "valid_partial_keep"
    needs_gemini = False
    needs_openai = False

    # Missing or placeholder source_ids
    if not source_ids:
        status = "needs_evidence"
        issues.append("no_source_ids")
        needs_gemini = True
    elif not has_real_sources:
        status = "needs_evidence"
        issues.append("only_placeholder_source_ids")
        needs_gemini = True

    # IL-confirmed but no Israeli evidence
    if market_scope.lower() == "il-confirmed" and not has_real_sources:
        status = "needs_evidence"
        issues.append("il_confirmed_no_israeli_evidence")
        needs_gemini = True

    # Normalization needed
    from core.schemas import BodyType, FuelType, Transmission
    body_types = {e.value for e in BodyType}
    fuel_types = {e.value for e in FuelType}
    transmissions = {e.value for e in Transmission}

    normalization_needed = False
    if body and body not in body_types:
        issues.append("body_type_not_normalized")
        normalization_needed = True
    if fuel and fuel not in fuel_types:
        issues.append("fuel_type_not_normalized")
        normalization_needed = True
    if trans and trans not in transmissions:
        issues.append("transmission_not_normalized")
        normalization_needed = True

    if normalization_needed and status == "valid_partial_keep":
        status = "needs_normalization"

    # Duplicate detection — same trim within same seed
    same_seed_variants = [
        v for v in all_variants
        if isinstance(v, dict) and str(v.get("seed_id", "")).strip() == sid
        and v.get("variant_id") != vid
    ]
    same_trim_count = sum(
        1 for v in same_seed_variants if safe_str(v.get("trim")) == trim
    ) if trim else 0

    if same_trim_count > 0:
        issues.append("duplicate_trim_in_seed")
        if status in ("valid_partial_keep", "needs_normalization"):
            status = "merge_candidate"
        needs_gemini = True

    # Check for near-duplicate of a verified variant
    verified_match = False
    for v in all_variants:
        if not isinstance(v, dict):
            continue
        if v.get("verification_status") != "verified":
            continue
        if v.get("variant_id") == vid:
            continue
        if (safe_str(v.get("make")) == make and safe_str(v.get("model")) == model
                and safe_str(v.get("trim")) == trim
                and extract_year(v.get("year_start")) == ys
                and extract_year(v.get("year_end")) == ye):
            verified_match = True
            break

    if verified_match:
        issues.append("near_duplicate_of_verified")
        if status in ("valid_partial_keep", "needs_normalization", "needs_evidence"):
            status = "merge_candidate"
        needs_gemini = True

    # Confidence too high for weak evidence
    conf = safe_str(variant.get("confidence_level") or variant.get("confidence"))
    if conf == "high" and not has_real_sources:
        issues.append("confidence_overstated")
        needs_gemini = True

    # Year range mismatch
    if ys is not None and ye is not None and ys > ye:
        issues.append("year_range_inverted")
        if status == "valid_partial_keep":
            status = "needs_normalization"

    # Promotion candidate: partial with strong evidence
    if (status == "valid_partial_keep"
            and has_real_sources
            and market_scope.lower() == "il-confirmed"
            and conf in ("high", "medium")
            and len(source_ids) >= 2
            and not has_placeholder_sources):
        status = "promote_to_verified_candidate"
        needs_gemini = True  # Need model confirmation before promotion
        needs_openai = True  # High-risk decision

    # High-risk decisions need OpenAI second opinion
    if status in ("merge_candidate", "reject_candidate"):
        needs_openai = True

    # Manual review for unresolvable cases
    if risk_level == "critical" and status == "valid_partial_keep":
        status = "manual_review_required"
        needs_gemini = True

    return {
        "variant_id": vid,
        "seed_id": sid,
        "current_status": "partial",
        "validation_status": status,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "issues": issues,
        "evidence": [],
        "recommended_action": _action_for_status(status),
        "needs_gemini_review": needs_gemini,
        "needs_openai_second_opinion": needs_openai,
        "safe_to_auto_apply": False,
    }


def _action_for_status(status: str) -> str:
    """Map validation status to recommended action."""
    actions = {
        "valid_partial_keep": "No action — keep as partial",
        "needs_evidence": "Add source evidence before promoting",
        "needs_normalization": "Normalize field values",
        "merge_candidate": "Review for merge with duplicate",
        "promote_to_verified_candidate": "Consider promotion to verified (needs review)",
        "manual_review_required": "Requires manual expert review",
        "reject_candidate": "Consider rejection (needs review)",
    }
    return actions.get(status, "Unknown action")


def classify_all_partial_variants(canonical: dict) -> list[dict]:
    """Classify all partial variants in the canonical database."""
    partial = canonical.get("partial_variants") or []
    all_variants = (canonical.get("verified_variants") or []) + partial

    results = []
    for v in partial:
        if not isinstance(v, dict):
            continue
        result = classify_partial_variant(v, all_variants)
        results.append(result)

    return results


def summarize_partial_variants(classifications: list[dict]) -> dict:
    """Build a partial variants summary for the validation report."""
    status_counts: dict[str, int] = {s: 0 for s in PARTIAL_STATUSES}
    risk_counts: dict[str, int] = {"low": 0, "medium": 0, "high": 0, "critical": 0}

    for c in classifications:
        status = c.get("validation_status", "valid_partial_keep")
        status_counts[status] = status_counts.get(status, 0) + 1
        risk = c.get("risk_level", "low")
        risk_counts[risk] = risk_counts.get(risk, 0) + 1

    return {
        "total_partial_variants": len(classifications),
        **status_counts,
        "risk_low": risk_counts.get("low", 0),
        "risk_medium": risk_counts.get("medium", 0),
        "risk_high": risk_counts.get("high", 0),
        "risk_critical": risk_counts.get("critical", 0),
        "needs_evidence_count": status_counts.get("needs_evidence", 0),
        "needs_manual_review_count": status_counts.get("manual_review_required", 0),
        "merge_candidates_count": status_counts.get("merge_candidate", 0),
        "promote_candidates_count": status_counts.get("promote_to_verified_candidate", 0),
    }
