"""Targeted failed seed validator.

Validates a specific seed inside the validation session.
Does NOT retry through the build engine.
Does NOT mutate canonical.
"""
from __future__ import annotations

from engine.state import seed_id_from_seed
from engine.validation.normalizer import safe_str, extract_year
from core.source_ids import looks_like_placeholder_source_id


def validate_targeted_seed(
    seed_id: str,
    canonical: dict,
    seeds: list[dict],
) -> dict:
    """Validate a targeted failed seed and produce a structured result.

    Answers all 11 questions from the spec without mutating canonical.
    """
    bs = canonical.get("batch_state") or {}
    accounting = bs.get("seed_accounting") or {}
    catalog_ids = {seed_id_from_seed(s) for s in seeds}

    processed = set(bs.get("processed_seed_ids") or [])
    failed = set(bs.get("failed_seed_ids") or [])
    manual_review = set(bs.get("manual_review_seed_ids") or [])

    # 1. Present in seed catalog?
    in_catalog = seed_id in catalog_ids

    # 2-4. Bucket membership
    in_processed = seed_id in processed
    in_failed = seed_id in failed
    in_manual = seed_id in manual_review

    # 5-6. Variants for this seed?
    all_variants = (canonical.get("verified_variants") or []) + \
                   (canonical.get("partial_variants") or [])
    seed_variants = [
        v for v in all_variants
        if isinstance(v, dict) and str(v.get("seed_id", "")).strip() == seed_id
    ]
    has_variants = len(seed_variants) > 0

    # 7. No-variants/resolved closure?
    acct = accounting.get(seed_id, {})
    resolution_type = acct.get("resolution_type", "")
    has_closure = resolution_type in (
        "no_variants_proven", "variants_added", "variants_added_after_failed_retry"
    )

    # 8. Structural validity of variants
    structural_issues: list[str] = []
    for v in seed_variants:
        vid = v.get("variant_id", "")
        if not v.get("make"):
            structural_issues.append(f"{vid}: missing make")
        if not v.get("model"):
            structural_issues.append(f"{vid}: missing model")
        ys = extract_year(v.get("year_start"))
        ye = extract_year(v.get("year_end"))
        if ys is None:
            structural_issues.append(f"{vid}: missing year_start")
        if ye is None:
            structural_issues.append(f"{vid}: missing year_end")
        if ys and ye and ys > ye:
            structural_issues.append(f"{vid}: year_range_inverted {ys}-{ye}")
        sids = v.get("source_ids") or []
        if all(looks_like_placeholder_source_id(str(s)) for s in sids) if sids else True:
            structural_issues.append(f"{vid}: placeholder_or_empty_sources")

    variants_structurally_valid = len(structural_issues) == 0

    # 9. Plausibility — basic checks for the specific seed
    plausibility_notes: list[str] = []
    parts = seed_id.split("__")
    if len(parts) >= 4:
        expected_make = parts[0].replace("_", " ").strip()
        expected_model = parts[1].replace("_", " ").strip()
        expected_ys = parts[2]
        expected_ye = parts[3]

        for v in seed_variants:
            v_make = safe_str(v.get("make"))
            v_model = safe_str(v.get("model"))
            if expected_make.lower() not in v_make and v_make not in expected_make.lower():
                plausibility_notes.append(
                    f"{v.get('variant_id', '')}: make mismatch (expected ~{expected_make}, got {v_make})"
                )
            try:
                ys_int = int(expected_ys)
                ye_int = int(expected_ye)
                v_ys = extract_year(v.get("year_start"))
                v_ye = extract_year(v.get("year_end"))
                if v_ys and v_ye:
                    if v_ye < ys_int or v_ys > ye_int:
                        plausibility_notes.append(
                            f"{v.get('variant_id', '')}: year range {v_ys}-{v_ye} outside seed {ys_int}-{ye_int}"
                        )
            except ValueError:
                pass

    variants_plausible = len(plausibility_notes) == 0 or not seed_variants

    # 10. Was previous failure a real data issue or stale state?
    failure_was_stale = False
    if in_failed and has_closure:
        failure_was_stale = True
    elif in_failed and in_processed:
        failure_was_stale = True

    error_text = (acct.get("reason", "") + " " + acct.get("error_summary", "")).lower()
    failure_cause = "unknown"
    if in_failed:
        if any(kw in error_text for kw in ("api_key", "secret", "token", "auth", "config",
                                             "credential", "gemini", "runner_failed")):
            failure_cause = "config_error_missing_secrets"
        elif "timeout" in error_text:
            failure_cause = "model_timeout"
        elif "parse" in error_text or "json" in error_text:
            failure_cause = "model_parse_error"
        elif error_text.strip():
            failure_cause = "data_error"

    # 11. Determine needed action
    needs_build_retry = False
    needs_manual_review = False
    needs_data_correction = False
    recommended_action = "no_action"

    if failure_was_stale:
        recommended_action = "no_action — stale failure, already resolved"
    elif in_failed and not has_variants and not has_closure:
        if failure_cause == "config_error_missing_secrets":
            needs_build_retry = True
            recommended_action = "build_retry — previous failure was config/secrets error"
        elif failure_cause in ("model_timeout", "model_parse_error"):
            needs_build_retry = True
            recommended_action = f"build_retry — previous failure was {failure_cause}"
        else:
            needs_manual_review = True
            recommended_action = "manual_review — unresolved failure with no variants"
    elif in_failed and has_variants and not variants_structurally_valid:
        needs_data_correction = True
        recommended_action = "data_normalization — variants exist but have structural issues"
    elif in_failed and has_variants and variants_structurally_valid:
        failure_was_stale = True
        recommended_action = "no_action — variants exist and are valid, stale failure"
    elif not in_failed and not has_variants and not has_closure and in_catalog:
        recommended_action = "build_retry — seed not yet processed"
        needs_build_retry = True
    else:
        recommended_action = "no_action"

    evidence = []
    if structural_issues:
        evidence.append({"type": "structural_issues", "details": structural_issues})
    if plausibility_notes:
        evidence.append({"type": "plausibility_notes", "details": plausibility_notes})
    if acct:
        evidence.append({"type": "accounting", "details": {
            "status": acct.get("status"),
            "resolution_type": resolution_type,
            "reason": acct.get("reason", ""),
            "error_summary": acct.get("error_summary", ""),
        }})

    return {
        "seed_id": seed_id,
        "in_catalog": in_catalog,
        "in_processed": in_processed,
        "in_failed": in_failed,
        "in_manual_review": in_manual,
        "has_variants": has_variants,
        "variant_count": len(seed_variants),
        "has_closure": has_closure,
        "variants_structurally_valid": variants_structurally_valid,
        "variants_plausible": variants_plausible,
        "failure_cause": failure_cause if in_failed else None,
        "failure_was_stale_state": failure_was_stale,
        "validation_status": "resolved" if failure_was_stale else (
            "needs_action" if (needs_build_retry or needs_manual_review or needs_data_correction)
            else "clean"
        ),
        "needs_build_retry": needs_build_retry,
        "needs_manual_review": needs_manual_review,
        "needs_data_correction": needs_data_correction,
        "evidence": evidence,
        "recommended_action": recommended_action,
    }
