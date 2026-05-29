"""Group builder for validation.

Groups variants to reduce model calls while preserving variant-level output.
Groups share: make, model, generation, year range, engine family, fuel type,
transmission, drivetrain, and Israeli market scope.
"""
from __future__ import annotations

from collections import defaultdict

from engine.validation.normalizer import (
    normalize_variant_for_grouping,
    safe_str,
    extract_value,
    extract_year,
)


def build_group_key(variant: dict) -> str:
    """Generate a deterministic group key for a variant."""
    n = normalize_variant_for_grouping(variant)
    parts = [
        n["make"] or "unknown_make",
        n["model"] or "unknown_model",
        n["generation"] or "unknown_gen",
        f"{n['year_start'] or '?'}-{n['year_end'] or '?'}",
        n["engine_family"] or "unknown_engine",
        n["fuel_type"] or "unknown_fuel",
        n["transmission"] or "unknown_trans",
        n["drivetrain"] or "unknown_drive",
        n["market_scope"] or "unknown_scope",
    ]
    return "|".join(parts)


def build_groups(variants: list[dict]) -> dict[str, list[dict]]:
    """Group variants by shared characteristics.

    Returns a dict mapping group_key -> list of variants in that group.
    """
    groups: dict[str, list[dict]] = defaultdict(list)
    for v in variants:
        key = build_group_key(v)
        groups[key].append(v)
    return dict(groups)


def get_group_trim_candidates(group: list[dict]) -> list[str]:
    """Extract all unique trim values from a group."""
    trims: set[str] = set()
    for v in group:
        trim_val = safe_str(v.get("trim"))
        if trim_val:
            trims.add(trim_val)
        for opt in v.get("trim_options") or []:
            t = opt.get("value", "")
            if t:
                trims.add(str(t).strip().lower())
    return sorted(trims)


def group_has_conflicts(group: list[dict]) -> dict[str, bool]:
    """Check if a group has conflicting values across variants."""

    def _collect(field: str) -> set:
        vals: set[str] = set()
        for v in group:
            raw = extract_value(v.get(field))
            if raw is not None:
                vals.add(str(raw).strip().lower())
        return vals

    conflicts = {
        "trim": len(_collect("trim")) > 1,
        "engine": len(_collect("engine")) > 1,
        "fuel_type": len(_collect("fuel_type")) > 1,
        "transmission": len(_collect("transmission")) > 1,
        "year_range": len({
            (extract_year(v.get("year_start")), extract_year(v.get("year_end")))
            for v in group
        }) > 1,
        "market_evidence": len({
            safe_str(v.get("market_scope")) for v in group
        }) > 1,
    }
    return conflicts


def group_needs_variant_level(group: list[dict]) -> bool:
    """Determine if a group needs variant-level validation (escalation)."""
    if len(group) <= 1:
        return False
    conflicts = group_has_conflicts(group)
    return any(conflicts.values())
