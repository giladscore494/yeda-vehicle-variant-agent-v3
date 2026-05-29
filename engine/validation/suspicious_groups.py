"""Suspicious group selection — identifies groups that need model validation.

Only these groups are sent to Gemini/OpenAI.
Does NOT send every variant to models.
"""
from __future__ import annotations

from collections import Counter
from core.source_ids import looks_like_placeholder_source_id
from engine.validation.normalizer import safe_str, extract_year
from engine.validation.risk_scorer import score_variant, classify_risk


def build_suspicious_groups(
    canonical: dict,
    seeds: list[dict] | None = None,
) -> list[dict]:
    """Build a list of suspicious validation groups that need model review.

    Returns a list of group dicts, each with:
      - group_id, seed_id, reason, risk_level, variant_ids, variants
    """
    groups: list[dict] = []
    group_counter = 0

    bs = canonical.get("batch_state") or {}
    failed_seeds = set(bs.get("failed_seed_ids") or [])
    manual_seeds = set(bs.get("manual_review_seed_ids") or [])
    processed_seeds = set(bs.get("processed_seed_ids") or [])
    accounting = bs.get("seed_accounting") or {}

    all_variants = (canonical.get("verified_variants") or []) + \
                   (canonical.get("partial_variants") or [])

    # Index variants by seed_id
    seed_variants: dict[str, list[dict]] = {}
    for v in all_variants:
        if not isinstance(v, dict):
            continue
        sid = str(v.get("seed_id", "")).strip()
        if sid:
            seed_variants.setdefault(sid, []).append(v)

    def _add_group(seed_id: str, reason: str, variants: list[dict],
                   risk_level: str = "medium") -> None:
        nonlocal group_counter
        group_counter += 1
        groups.append({
            "group_id": f"sg_{group_counter:04d}",
            "seed_id": seed_id,
            "reason": reason,
            "risk_level": risk_level,
            "variant_ids": [v.get("variant_id", "") for v in variants],
            "variant_count": len(variants),
        })

    # ── Failed seeds ────────────────────────────────────────────────────

    for sid in sorted(failed_seeds):
        variants = seed_variants.get(sid, [])
        _add_group(sid, "failed_seed", variants, risk_level="high")

    # ── Manual review seeds ─────────────────────────────────────────────

    for sid in sorted(manual_seeds):
        variants = seed_variants.get(sid, [])
        _add_group(sid, "manual_review_seed", variants, risk_level="high")

    # ── Per-seed variant analysis ───────────────────────────────────────

    checked_seeds: set[str] = set()
    for sid, variants in seed_variants.items():
        if sid in checked_seeds:
            continue
        checked_seeds.add(sid)

        reasons: list[str] = []

        # Seed with no variants and weak closure
        if not variants:
            acct = accounting.get(sid, {})
            if acct.get("resolution_type") != "no_variants_proven":
                reasons.append("no_variants_weak_closure")

        # Variants with weak/empty sources
        weak_source_count = sum(
            1 for v in variants
            if not (v.get("source_ids") or []) or all(
                looks_like_placeholder_source_id(str(s))
                for s in (v.get("source_ids") or [])
            )
        )
        if weak_source_count > 0 and weak_source_count == len(variants):
            reasons.append("all_variants_weak_sources")
        elif weak_source_count > 0:
            reasons.append("some_variants_weak_sources")

        # IL-confirmed but no Israeli evidence
        il_confirmed_no_evidence = [
            v for v in variants
            if (v.get("market_scope") or "").lower() == "il-confirmed"
            and (not (v.get("source_ids") or []) or all(
                looks_like_placeholder_source_id(str(s))
                for s in (v.get("source_ids") or [])
            ))
        ]
        if il_confirmed_no_evidence:
            reasons.append("il_confirmed_no_evidence")

        # Duplicate trim names
        trims = [safe_str(v.get("trim")) for v in variants if safe_str(v.get("trim"))]
        trim_counts = Counter(trims)
        if any(c > 1 for c in trim_counts.values()):
            reasons.append("duplicate_trim_names")

        # Inconsistent body/fuel/transmission
        bodies = {safe_str(v.get("body_type")) for v in variants if safe_str(v.get("body_type"))}
        fuels = {safe_str(v.get("fuel_type")) for v in variants if safe_str(v.get("fuel_type"))}
        transmissions = {safe_str(v.get("transmission")) for v in variants if safe_str(v.get("transmission"))}

        if len(bodies) > 2:
            reasons.append("inconsistent_body_types")
        if len(fuels) > 2:
            reasons.append("inconsistent_fuel_types")
        if len(transmissions) > 2:
            reasons.append("inconsistent_transmissions")

        # Too many near-duplicate variants
        if len(variants) > 10:
            reasons.append("too_many_variants")

        # Placeholder source_ids
        placeholder_variants = [
            v for v in variants
            if any(looks_like_placeholder_source_id(str(s)) for s in (v.get("source_ids") or []))
        ]
        if placeholder_variants:
            reasons.append("placeholder_source_ids")

        # Confidence overstated
        overstated = [
            v for v in variants
            if safe_str(v.get("confidence_level") or v.get("confidence")) == "high"
            and (not (v.get("source_ids") or []) or all(
                looks_like_placeholder_source_id(str(s))
                for s in (v.get("source_ids") or [])
            ))
        ]
        if overstated:
            reasons.append("confidence_overstated")

        if reasons and sid not in failed_seeds and sid not in manual_seeds:
            max_risk = max(score_variant(v) for v in variants) if variants else 0
            risk = classify_risk(max_risk)
            if risk in ("medium", "high", "critical"):
                _add_group(sid, "; ".join(reasons), variants, risk_level=risk)

    return groups


def summarize_suspicious_groups(groups: list[dict]) -> dict:
    """Summarize suspicious groups for reporting."""
    risk_counts: dict[str, int] = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    reason_counts: dict[str, int] = {}

    for g in groups:
        risk_counts[g.get("risk_level", "medium")] = \
            risk_counts.get(g.get("risk_level", "medium"), 0) + 1
        for reason in g.get("reason", "").split("; "):
            reason = reason.strip()
            if reason:
                reason_counts[reason] = reason_counts.get(reason, 0) + 1

    return {
        "total_suspicious_groups": len(groups),
        "by_risk_level": risk_counts,
        "by_reason": reason_counts,
        "total_variants_in_groups": sum(g.get("variant_count", 0) for g in groups),
    }
