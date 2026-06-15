"""Python validation for GPT-5.4 model technical-catalog profiles.

This is profile-level (per make/model) validation, NOT per-row variant
validation. It enforces the simple technical schema, removes duplicate
technical variants, derives the website value lists only from
``technical_variants_il``, and decides whether a profile is website-ready or
must go to the review output.

No publication/route/risk/guard logic lives here beyond the deterministic
schema/identity checks listed in the spec.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .openai_catalog_client import ALLOWED_SUPPORT_LEVELS, classify_non_trim

REQUIRED_VARIANT_FIELDS = (
    "engine",
    "horsepower_hp",
    "transmission",
    "body_type",
    "fuel_type",
    "drivetrain",
    "year_start",
    "year_end",
)

WEBSITE_VALUE_FIELDS = (
    "version_or_trim",
    "body_type",
    "fuel_type",
    "engine",
    "horsepower_hp",
    "transmission",
    "drivetrain",
)


@dataclass
class ProfileValidation:
    profile: Dict[str, Any]
    ready: bool
    issues: List[str] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=dict)


def _variant_signature(variant: Dict[str, Any]) -> Tuple:
    return tuple(
        str(variant.get(k)).strip().lower() if variant.get(k) is not None else None
        for k in (
            "version_or_trim",
            "body_type",
            "fuel_type",
            "engine",
            "horsepower_hp",
            "transmission",
            "drivetrain",
            "year_start",
            "year_end",
        )
    )


def derive_available_values(variants: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
    """Website choices come ONLY from technical_variants_il (spec rule 6)."""
    out: Dict[str, List[Any]] = {f: [] for f in WEBSITE_VALUE_FIELDS}
    seen: Dict[str, set] = {f: set() for f in WEBSITE_VALUE_FIELDS}
    for variant in variants:
        for field_name in WEBSITE_VALUE_FIELDS:
            value = variant.get(field_name)
            if value is None:
                continue
            marker = str(value).strip().lower()
            if marker in seen[field_name]:
                continue
            seen[field_name].add(marker)
            out[field_name].append(value)
    return out


def _is_ev_fuel(value: Any) -> bool:
    if value is None:
        return False
    low = str(value).strip().lower()
    return low in {"electric", "ev", "bev"}


def validate_profile(profile: Dict[str, Any]) -> ProfileValidation:
    """Validate one model profile and return a cleaned, routed result."""
    issues: List[str] = []
    profile = dict(profile)  # shallow copy; we mutate top-level keys only
    model = profile.get("model", "")

    variants = profile.get("technical_variants_il")
    if not isinstance(variants, list):
        variants = []
        issues.append("technical_variants_il missing or not a list")

    # 3. technical_variants_il is not empty.
    if not variants:
        issues.append("technical_variants_il is empty")

    cleaned_variants: List[Dict[str, Any]] = []
    seen_signatures: set = set()
    duplicate_count = 0
    without_sources = 0
    unknown_support = 0
    ev_in_petrol = 0

    profile_is_petrol = any(
        not _is_ev_fuel(v.get("fuel_type")) for v in variants if isinstance(v, dict)
    )
    profile_has_petrol_label = "e" not in str(model).strip().lower()[-1:] if model else True

    for idx, variant in enumerate(variants):
        if not isinstance(variant, dict):
            issues.append(f"variant[{idx}] is not an object")
            continue

        # 2. support_level enum.
        support = variant.get("support_level")
        if support not in ALLOWED_SUPPORT_LEVELS:
            issues.append(
                f"variant[{idx}] support_level {support!r} not in {sorted(ALLOWED_SUPPORT_LEVELS)}"
            )
        if support == "unknown" or support is None:
            unknown_support += 1

        # 5. required technical fields present (non-null).
        missing = [f for f in REQUIRED_VARIANT_FIELDS if variant.get(f) in (None, "")]
        if missing:
            issues.append(f"variant[{idx}] missing required fields: {missing}")

        # 4. every variant has source_indexes.
        src = variant.get("source_indexes")
        if not isinstance(src, list) or not src:
            without_sources += 1
            issues.append(f"variant[{idx}] has no source_indexes")

        # 10. Base/Standard/None/etc. not treated as trim.
        trim = variant.get("version_or_trim")
        if trim is not None:
            classification = classify_non_trim(trim, model)
            if classification is not None:
                issues.append(
                    f"variant[{idx}] version_or_trim {trim!r} is a "
                    f"{classification['classification']}, not a trim"
                )

        # 8. No EV data inside a petrol model profile.
        if profile_has_petrol_label and profile_is_petrol and _is_ev_fuel(variant.get("fuel_type")):
            ev_in_petrol += 1
            issues.append(f"variant[{idx}] is electric inside a petrol model profile")

        # 7. de-duplicate technical variants.
        sig = _variant_signature(variant)
        if sig in seen_signatures:
            duplicate_count += 1
            continue
        seen_signatures.add(sig)
        cleaned_variants.append(variant)

    profile["technical_variants_il"] = cleaned_variants

    # 6. available_values_for_website derived only from technical_variants_il.
    profile["available_values_for_website"] = derive_available_values(cleaned_variants)

    stats = {
        "technical_variant_count": len(cleaned_variants),
        "duplicate_technical_variants": duplicate_count,
        "technical_variants_without_sources": without_sources,
        "unknown_support_values": unknown_support,
        "model_identity_conflicts": ev_in_petrol,
        "invalid_non_trim_labels": len(profile.get("invalid_or_non_trim_labels") or []),
    }

    ready = (
        not issues
        and bool(cleaned_variants)
        and without_sources == 0
        and ev_in_petrol == 0
    )
    return ProfileValidation(profile=profile, ready=ready, issues=issues, stats=stats)


def build_readiness_report(validations: List[ProfileValidation]) -> Dict[str, Any]:
    """Aggregate the QA readiness numbers across all validated profiles."""
    total_models = len(validations)
    total_variants = sum(v.stats.get("technical_variant_count", 0) for v in validations)
    ready_models = sum(1 for v in validations if v.ready)
    blocked = total_models - ready_models
    return {
        "total_models": total_models,
        "total_technical_variants": total_variants,
        "models_ready_for_website": ready_models,
        "models_blocked": blocked,
        "technical_variants_without_sources": sum(
            v.stats.get("technical_variants_without_sources", 0) for v in validations
        ),
        "unknown_support_values": sum(
            v.stats.get("unknown_support_values", 0) for v in validations
        ),
        "duplicate_technical_variants": sum(
            v.stats.get("duplicate_technical_variants", 0) for v in validations
        ),
        "model_identity_conflicts": sum(
            v.stats.get("model_identity_conflicts", 0) for v in validations
        ),
        "ready_for_website_upload": blocked == 0 and ready_models > 0,
    }
