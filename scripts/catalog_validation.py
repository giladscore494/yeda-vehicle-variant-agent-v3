"""Python validation for GPT-5.4 model technical-catalog profiles.

This is profile-level (per make/model) validation, NOT per-row variant
validation. It enforces the simple technical schema, removes duplicate
technical variants, derives the website value lists only from
``technical_variants_il``, and decides whether a profile is website-ready or
must go to the review output.

Website-readiness now requires real web grounding: every non-null technical
field must be backed by ``field_sources`` that reference real entries in the
profile ``sources`` array. Raw database values are never evidence.

No publication/route/risk/guard logic lives here beyond the deterministic
schema/identity/grounding checks listed in the spec.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from .catalog_normalization import merge_year_variants, normalize_variant
from .openai_catalog_client import (
    ALLOWED_SUPPORT_LEVELS,
    GROUNDED_TECHNICAL_FIELDS,
    classify_non_trim,
)

# Required website fields — must be non-null AND grounded for website-ready.
REQUIRED_WEBSITE_FIELDS = (
    "body_type",
    "fuel_type",
    "engine",
    "horsepower_hp",
    "transmission",
    "drivetrain",
)

# Fields surfaced in the website value lists.
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


def is_valid_profile_id(profile_id: Any) -> bool:
    """True only when a checkpoint/profile id carries a real make AND model.

    Corrupt ids such as ``"IL::::"`` (empty make/model) must never be treated as
    a valid resume pointer; they would otherwise rebuild from the beginning or
    poison the readiness report.
    """
    if not profile_id:
        return False
    text = str(profile_id)
    parts = text.split("::")
    if len(parts) == 3:
        _market, make, model = parts
        return bool(make.strip() and model.strip())
    parts = text.split("|")
    if len(parts) == 3:
        return bool(parts[1].strip() and parts[2].strip())
    return False


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


def _valid_source_indexes(sources: Any) -> Set[int]:
    """The set of source_index values declared by the profile ``sources``."""
    valid: Set[int] = set()
    if not isinstance(sources, list):
        return valid
    for i, src in enumerate(sources):
        if isinstance(src, dict) and isinstance(src.get("source_index"), int):
            valid.add(src["source_index"])
        else:
            valid.add(i)
    return valid


@dataclass
class _VariantCheck:
    website_ready: bool
    issues: List[str]
    has_sources: bool
    has_field_sources: bool
    missing_required_grounding: bool
    has_missing_grounded_fields: bool
    invalid_source_references: int


def _check_variant(
    idx: int,
    variant: Dict[str, Any],
    model: str,
    valid_source_indexes: Set[int],
    profile_is_petrol: bool,
    profile_has_petrol_label: bool,
) -> _VariantCheck:
    issues: List[str] = []
    website_ready = True

    def block(msg: str) -> None:
        nonlocal website_ready
        issues.append(f"variant[{idx}] {msg}")
        website_ready = False

    # 5. support_level enum (only the four allowed values).
    support = variant.get("support_level")
    if support not in ALLOWED_SUPPORT_LEVELS:
        block(
            f"support_level {support!r} not in {sorted(ALLOWED_SUPPORT_LEVELS)}"
        )

    # 1. source_indexes is non-empty.
    src_indexes = variant.get("source_indexes")
    has_sources = isinstance(src_indexes, list) and bool(src_indexes)
    if not has_sources:
        block("has no source_indexes")
        src_indexes = src_indexes if isinstance(src_indexes, list) else []

    # 2. field_sources exists.
    field_sources = variant.get("field_sources")
    has_field_sources = isinstance(field_sources, dict) and bool(field_sources)
    if not isinstance(field_sources, dict):
        block("missing field_sources")
        field_sources = {}

    missing_grounded = variant.get("missing_grounded_fields") or []
    if not isinstance(missing_grounded, list):
        missing_grounded = []

    # 4. all source indexes referenced (variant + field_sources) exist in sources.
    invalid_refs = 0
    for ref in src_indexes:
        if isinstance(ref, int) and ref not in valid_source_indexes:
            invalid_refs += 1
    for fname, refs in field_sources.items():
        if not isinstance(refs, list):
            continue
        for ref in refs:
            if isinstance(ref, int) and ref not in valid_source_indexes:
                invalid_refs += 1
    if invalid_refs:
        block(f"field_sources/source_indexes reference {invalid_refs} unknown source(s)")

    # 3. every non-null technical field has at least one field_sources entry.
    missing_required_grounding = False
    for fname in GROUNDED_TECHNICAL_FIELDS:
        value = variant.get(fname)
        if value in (None, ""):
            continue
        refs = field_sources.get(fname) if isinstance(field_sources, dict) else None
        if not (isinstance(refs, list) and refs):
            missing_required_grounding = True
            block(f"non-null field {fname!r} has no field_sources entry")

    # 7. required website fields are non-null.
    for fname in REQUIRED_WEBSITE_FIELDS:
        if variant.get(fname) in (None, ""):
            block(f"required website field {fname!r} is null/empty")

    # 8. missing_grounded_fields must not include a required website field.
    for fname in missing_grounded:
        if fname in REQUIRED_WEBSITE_FIELDS:
            block(f"required field {fname!r} listed in missing_grounded_fields")

    # 6. support_level=direct needs at least one source directly supporting it.
    if support == "direct" and not has_sources:
        block("support_level=direct but no source directly supports it")

    # 10. version_or_trim may be null only if the technical engine/transmission
    #     configuration is directly sourced; an invalid trim label is blocked.
    trim = variant.get("version_or_trim")
    if trim is not None:
        classification = classify_non_trim(trim, model)
        if classification is not None:
            block(
                f"version_or_trim {trim!r} is a "
                f"{classification['classification']}, not a trim"
            )

    # No EV data inside explicitly combustion-labelled model profiles (identity rule).
    # Mixed EV/PHEV nameplates such as BYD Seal U / Seal U DM-i are legitimate
    # when the model label itself is not an explicit petrol/diesel designation.
    combustion_markers = ("petrol", "diesel", "tdi", "tfsi", "tsi", "30d", "40d", "35i", "40i", "50i", "3.0d", "3.0i", "4.4i")
    explicitly_combustion_model = any(marker in str(model).strip().lower() for marker in combustion_markers)
    if explicitly_combustion_model and profile_has_petrol_label and profile_is_petrol and _is_ev_fuel(variant.get("fuel_type")):
        block("is electric inside a petrol model profile")

    return _VariantCheck(
        website_ready=website_ready,
        issues=issues,
        has_sources=has_sources,
        has_field_sources=has_field_sources,
        missing_required_grounding=missing_required_grounding,
        has_missing_grounded_fields=bool(missing_grounded),
        invalid_source_references=invalid_refs,
    )


def validate_profile(profile: Dict[str, Any]) -> ProfileValidation:
    """Validate one model profile and return a cleaned, routed result."""
    issues: List[str] = []
    profile = dict(profile)  # shallow copy; we mutate top-level keys only
    model = profile.get("model", "")

    # --- hard top-level identity checks ---------------------------------
    # A profile with a missing make/model must never be website-ready and must
    # never be allowed to masquerade as a real model. ``canonical_model``
    # defaults to ``model`` (never invents a new identity).
    market = profile.get("market")
    make = profile.get("make")
    if not (isinstance(market, str) and market.strip()):
        issues.append("top-level market is missing/empty")
    if not (isinstance(make, str) and make.strip()):
        issues.append("top-level make is missing/empty")
    if not (isinstance(model, str) and str(model).strip()):
        issues.append("top-level model is missing/empty")
    else:
        canonical = profile.get("canonical_model")
        if not (isinstance(canonical, str) and canonical.strip()):
            profile["canonical_model"] = model

    variants = profile.get("technical_variants_il")
    if not isinstance(variants, list):
        variants = []
        issues.append("technical_variants_il missing or not a list")
    if not variants:
        issues.append("technical_variants_il is empty")

    valid_source_indexes = _valid_source_indexes(profile.get("sources"))

    profile_is_petrol = any(
        not _is_ev_fuel(v.get("fuel_type")) for v in variants if isinstance(v, dict)
    )
    model_label = str(model).strip().lower() if model else ""
    # BMW i-family models such as i3 and i8 are electrified model profiles.
    # They may legitimately mix pure-electric and range-extender/PHEV rows, so
    # do not infer a petrol-only profile from the presence of a non-EV variant.
    profile_has_petrol_label = not (
        model_label.startswith("i")
        or model_label.startswith("ix")
        or model_label.endswith("e")
    )

    cleaned_variants: List[Dict[str, Any]] = []
    seen_signatures: set = set()
    duplicate_count = 0
    variants_with_sources = 0
    variants_with_field_sources = 0
    variants_missing_required_grounding = 0
    variants_missing_grounded_fields = 0
    invalid_source_references = 0
    unknown_support = 0
    ev_in_petrol = 0
    all_variants_ready = True

    for idx, variant in enumerate(variants):
        if not isinstance(variant, dict):
            issues.append(f"variant[{idx}] is not an object")
            all_variants_ready = False
            continue

        # Enforce canonical values + the support_level invariant before any
        # check, signature, or website derivation sees the row.
        variant = normalize_variant(variant)

        if variant.get("support_level") in ("unknown", None):
            unknown_support += 1
        combustion_markers = ("petrol", "diesel", "tdi", "tfsi", "tsi", "30d", "40d", "35i", "40i", "50i", "3.0d", "3.0i", "4.4i")
        explicitly_combustion_model = any(marker in model_label for marker in combustion_markers)
        if _is_ev_fuel(variant.get("fuel_type")) and explicitly_combustion_model and profile_is_petrol and profile_has_petrol_label:
            ev_in_petrol += 1

        check = _check_variant(
            idx,
            variant,
            model,
            valid_source_indexes,
            profile_is_petrol,
            profile_has_petrol_label,
        )
        issues.extend(check.issues)
        if check.has_sources:
            variants_with_sources += 1
        if check.has_field_sources:
            variants_with_field_sources += 1
        if check.missing_required_grounding:
            variants_missing_required_grounding += 1
        if check.has_missing_grounded_fields:
            variants_missing_grounded_fields += 1
        invalid_source_references += check.invalid_source_references
        if not check.website_ready:
            all_variants_ready = False

        # 7 (dedupe). Remove duplicate technical variants.
        sig = _variant_signature(variant)
        if sig in seen_signatures:
            duplicate_count += 1
            continue
        seen_signatures.add(sig)
        cleaned_variants.append(variant)

    # Merge rows that differ only by year into one row spanning the range.
    cleaned_variants, merged_year_variants_count = merge_year_variants(cleaned_variants)

    profile["technical_variants_il"] = cleaned_variants
    profile["available_values_for_website"] = derive_available_values(cleaned_variants)

    has_grounding = bool(valid_source_indexes) and variants_with_field_sources > 0

    stats = {
        "technical_variant_count": len(cleaned_variants),
        "duplicate_technical_variants": duplicate_count,
        "merged_year_variants": merged_year_variants_count,
        "technical_variants_with_sources": variants_with_sources,
        "technical_variants_with_field_sources": variants_with_field_sources,
        "technical_variants_missing_required_grounding": variants_missing_required_grounding,
        "technical_variants_missing_grounded_fields": variants_missing_grounded_fields,
        "invalid_source_references": invalid_source_references,
        "unknown_support_values": unknown_support,
        "model_identity_conflicts": ev_in_petrol,
        "invalid_non_trim_labels": len(profile.get("invalid_or_non_trim_labels") or []),
        "has_web_grounding": 1 if has_grounding else 0,
    }

    ready = not issues and bool(cleaned_variants) and all_variants_ready
    return ProfileValidation(profile=profile, ready=ready, issues=issues, stats=stats)


def build_readiness_report(
    validations: List[ProfileValidation],
    *,
    web_search_enabled: bool = True,
    checkpoint_state: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Aggregate QA readiness across profiles + expose run/grounding/checkpoint."""
    checkpoint_state = checkpoint_state or {}
    total_models = len(validations)
    total_variants = sum(v.stats.get("technical_variant_count", 0) for v in validations)
    ready_models = sum(1 for v in validations if v.ready)
    blocked = total_models - ready_models

    def _sum(key: str) -> int:
        return sum(v.stats.get(key, 0) for v in validations)

    real_grounded_run = bool(web_search_enabled)
    ready_for_website_upload = (
        real_grounded_run and blocked == 0 and ready_models > 0
    )

    # Never preserve an invalid/stale build resume pointer (e.g. "IL::::").
    last_checkpointed_profile_id = checkpoint_state.get("last_checkpointed_profile_id")
    if not is_valid_profile_id(last_checkpointed_profile_id):
        last_checkpointed_profile_id = None
    last_repair_checkpointed_profile_id = checkpoint_state.get(
        "last_repair_checkpointed_profile_id"
    )
    if not is_valid_profile_id(last_repair_checkpointed_profile_id):
        last_repair_checkpointed_profile_id = None

    return {
        # --- run identity / grounding ---------------------------------------
        "real_grounded_run": real_grounded_run,
        "openai_api_key_env_name": "OPENAI_API_KEY",
        "web_search_enabled": bool(web_search_enabled),
        # --- github checkpoint status ---------------------------------------
        "github_checkpoint_enabled": bool(checkpoint_state.get("github_checkpoint_enabled", False)),
        "github_checkpoint_unit": checkpoint_state.get("github_checkpoint_unit", "model_profile"),
        "github_checkpoint_count": int(checkpoint_state.get("github_checkpoint_count", 0)),
        "github_checkpoint_fail_count": int(checkpoint_state.get("github_checkpoint_fail_count", 0)),
        "last_github_checkpoint_error": checkpoint_state.get("last_github_checkpoint_error"),
        "last_checkpointed_profile_id": last_checkpointed_profile_id,
        # Repair runs advance a SEPARATE pointer; they must never move the main
        # build resume pointer above.
        "last_repair_checkpointed_profile_id": last_repair_checkpointed_profile_id,
        # --- aggregate counts (legacy keys kept for the UI) -----------------
        "total_models": total_models,
        "total_technical_variants": total_variants,
        "models_ready_for_website": ready_models,
        "models_blocked": blocked,
        "models_with_web_grounding": _sum("has_web_grounding"),
        "technical_variants_total": total_variants,
        "technical_variants_with_sources": _sum("technical_variants_with_sources"),
        "technical_variants_with_field_sources": _sum("technical_variants_with_field_sources"),
        "technical_variants_missing_required_grounding": _sum(
            "technical_variants_missing_required_grounding"
        ),
        "technical_variants_missing_grounded_fields": _sum(
            "technical_variants_missing_grounded_fields"
        ),
        "technical_variants_without_sources": total_variants - _sum("technical_variants_with_sources"),
        "invalid_source_references": _sum("invalid_source_references"),
        "unknown_support_values": _sum("unknown_support_values"),
        "duplicate_technical_variants": _sum("duplicate_technical_variants"),
        "merged_year_variants": _sum("merged_year_variants"),
        "model_identity_conflicts": _sum("model_identity_conflicts"),
        # --- final gate -----------------------------------------------------
        "ready_for_website_upload": ready_for_website_upload,
    }
