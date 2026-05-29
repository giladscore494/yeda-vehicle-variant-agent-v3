"""Validation runner — main orchestrator for the validation engine.

Coordinates:
1. Deterministic audit over the entire canonical database
2. Partial variant classification
3. Suspicious group detection
4. Targeted failed seed validation
5. Writing all output files

Does NOT mutate canonical. Treats it as read-only input.
"""
from __future__ import annotations

import traceback
from datetime import datetime, timezone
from pathlib import Path

from core.config import (
    CANONICAL_RESUME_PATH,
    GITHUB_BRANCH,
    VALIDATION_OUTPUT_PATH,
)
from engine.state import load_canonical, load_seeds, ensure_batch_state_fields
from engine.validation.deterministic_audit import (
    run_deterministic_audit,
    summarize_deterministic_issues,
)
from engine.validation.suspicious_groups import (
    build_suspicious_groups,
    summarize_suspicious_groups,
)
from engine.validation.partial_variants import (
    classify_all_partial_variants,
    summarize_partial_variants,
)
from engine.validation.targeted_seed_validator import validate_targeted_seed
from engine.validation.validation_state import (
    load_validation_state,
    save_validation_state,
    update_validation_progress,
    mark_validation_item_completed,
    mark_validation_item_failed,
    mark_validation_started,
    mark_validation_completed,
)
from engine.validation.validation_outputs import (
    write_validated_package,
    write_validation_report,
    write_validation_issues,
    write_patch_suggestions,
    write_targeted_seed_validation,
)
from engine.validation.error_types import make_error, classify_exception


_TARGET_SEED_ID = "mg_(british_era)__tf__2002__2005__il"


def _check_branch() -> str | None:
    """Validate the resolved branch. Returns error message or None."""
    if GITHUB_BRANCH == "main":
        return "config_error_invalid_branch: resolved branch is 'main' — stopping"
    if GITHUB_BRANCH and GITHUB_BRANCH != "validation-v2-budgeted-dual-il-trims":
        return (
            f"config_error_invalid_branch: resolved branch is '{GITHUB_BRANCH}', "
            f"expected 'validation-v2-budgeted-dual-il-trims' — stopping"
        )
    if not GITHUB_BRANCH:
        return "config_error_invalid_branch: no branch resolved — stopping"
    return None


def run_deterministic_audit_only(
    canonical_path: str | None = None,
    seeds_path: str = "data/seeds/vehicle_model_seeds_il.json",
) -> dict:
    """Run only the deterministic audit. Returns result dict."""
    try:
        canonical = load_canonical(canonical_path or CANONICAL_RESUME_PATH)
        ensure_batch_state_fields(canonical)
        seeds = load_seeds(seeds_path)
    except Exception as exc:
        return {"ok": False, "error": make_error(
            classify_exception(exc), str(exc),
            failed_stage="load_canonical",
            traceback_short=traceback.format_exc()[-500:],
        )}

    issues = run_deterministic_audit(canonical, seeds)
    summary = summarize_deterministic_issues(issues)

    return {
        "ok": True,
        "total_issues": len(issues),
        "summary": summary,
        "issues": issues,
    }


def run_targeted_seed_validation(
    seed_id: str = _TARGET_SEED_ID,
    canonical_path: str | None = None,
    seeds_path: str = "data/seeds/vehicle_model_seeds_il.json",
) -> dict:
    """Run targeted validation for a specific failed seed. Returns result dict."""
    try:
        canonical = load_canonical(canonical_path or CANONICAL_RESUME_PATH)
        ensure_batch_state_fields(canonical)
        seeds = load_seeds(seeds_path)
    except Exception as exc:
        return {"ok": False, "error": make_error(
            classify_exception(exc), str(exc),
            failed_stage="load_canonical", seed_id=seed_id,
            traceback_short=traceback.format_exc()[-500:],
        )}

    result = validate_targeted_seed(seed_id, canonical, seeds)

    # Write the targeted result
    try:
        write_targeted_seed_validation(result)
    except Exception:
        pass  # Non-fatal — result is still returned

    return {"ok": True, "result": result}


def run_suspicious_groups_validation(
    canonical_path: str | None = None,
    seeds_path: str = "data/seeds/vehicle_model_seeds_il.json",
) -> dict:
    """Run suspicious groups detection. Returns result dict."""
    try:
        canonical = load_canonical(canonical_path or CANONICAL_RESUME_PATH)
        ensure_batch_state_fields(canonical)
        seeds = load_seeds(seeds_path)
    except Exception as exc:
        return {"ok": False, "error": make_error(
            classify_exception(exc), str(exc),
            failed_stage="load_canonical",
            traceback_short=traceback.format_exc()[-500:],
        )}

    groups = build_suspicious_groups(canonical, seeds)
    summary = summarize_suspicious_groups(groups)

    return {
        "ok": True,
        "total_groups": len(groups),
        "summary": summary,
        "groups": groups,
    }


def run_full_validation(
    canonical_path: str | None = None,
    seeds_path: str = "data/seeds/vehicle_model_seeds_il.json",
    state_path: str | None = None,
) -> dict:
    """Run the full validation session.

    1. Load canonical as read-only
    2. Run deterministic audit on all variants
    3. Classify all partial variants
    4. Build suspicious groups
    5. Run targeted failed seed validation
    6. Write all output files

    Does NOT call models (Gemini/OpenAI). Model calls are separate steps
    that can be triggered individually for suspicious groups.

    Returns a result dict with summary information.
    """
    started_at = datetime.now(timezone.utc).isoformat()

    # Branch guard
    branch_err = _check_branch()
    if branch_err:
        return {"ok": False, "error": make_error(
            "config_error_invalid_branch", branch_err,
            failed_stage="branch_check",
        )}

    # Load validation state
    state = load_validation_state(state_path)
    mark_validation_started(state, state_path)

    try:
        # ── Load data ───────────────────────────────────────────────────
        update_validation_progress(state, stage="LOADING_DATA", path=state_path)

        canonical = load_canonical(canonical_path or CANONICAL_RESUME_PATH)
        ensure_batch_state_fields(canonical)
        seeds = load_seeds(seeds_path)

        all_variants = (canonical.get("verified_variants") or []) + \
                       (canonical.get("partial_variants") or [])

        update_validation_progress(
            state, stage="DATA_LOADED", total_items=len(all_variants),
            path=state_path,
        )

        # ── Step 1: Deterministic audit ─────────────────────────────────
        update_validation_progress(
            state, stage="DETERMINISTIC_AUDIT",
            current_item="All variants", path=state_path,
        )

        deterministic_issues = run_deterministic_audit(canonical, seeds)
        mark_validation_item_completed(state, "deterministic_audit", state_path)

        # ── Step 2: Partial variant classification ──────────────────────
        update_validation_progress(
            state, stage="PARTIAL_VARIANT_CLASSIFICATION",
            current_item="All partial variants", path=state_path,
        )

        partial_classifications = classify_all_partial_variants(canonical)
        mark_validation_item_completed(state, "partial_classification", state_path)

        # ── Step 3: Suspicious groups ───────────────────────────────────
        update_validation_progress(
            state, stage="SUSPICIOUS_GROUP_DETECTION",
            current_item="Building suspicious groups", path=state_path,
        )

        suspicious_groups = build_suspicious_groups(canonical, seeds)
        mark_validation_item_completed(state, "suspicious_groups", state_path)

        # ── Step 4: Targeted seed validation ────────────────────────────
        update_validation_progress(
            state, stage="TARGETED_SEED_VALIDATION",
            current_item=_TARGET_SEED_ID, path=state_path,
        )

        targeted_result = validate_targeted_seed(_TARGET_SEED_ID, canonical, seeds)
        mark_validation_item_completed(state, "targeted_seed", state_path)

        # ── Step 5: Write all outputs ───────────────────────────────────
        update_validation_progress(
            state, stage="WRITING_OUTPUTS",
            current_item="Writing validation files", path=state_path,
        )

        run_id = state.get("validation_run_id", "unknown")
        completed_at = datetime.now(timezone.utc).isoformat()

        # Primary output: full canonical-style validated package
        write_validated_package(
            canonical=canonical,
            deterministic_issues=deterministic_issues,
            partial_classifications=partial_classifications,
            suspicious_groups=suspicious_groups,
            targeted_seed_result=targeted_result,
            validation_run_id=run_id,
        )

        # Secondary reports
        write_validation_report(
            validation_run_id=run_id,
            canonical=canonical,
            deterministic_issues=deterministic_issues,
            suspicious_groups=suspicious_groups,
            partial_classifications=partial_classifications,
            targeted_seed_result=targeted_result,
            started_at=started_at,
            completed_at=completed_at,
        )

        write_validation_issues(deterministic_issues)

        write_patch_suggestions(deterministic_issues, partial_classifications)

        write_targeted_seed_validation(targeted_result)

        # ── Done ────────────────────────────────────────────────────────
        mark_validation_completed(state, state_path)

        return {
            "ok": True,
            "validation_run_id": run_id,
            "started_at": started_at,
            "completed_at": completed_at,
            "total_variants_scanned": len(all_variants),
            "total_seeds_scanned": len(set(
                (canonical.get("batch_state", {}).get("processed_seed_ids") or []) +
                (canonical.get("batch_state", {}).get("failed_seed_ids") or []) +
                (canonical.get("batch_state", {}).get("manual_review_seed_ids") or [])
            )),
            "deterministic_issues": summarize_deterministic_issues(deterministic_issues),
            "suspicious_groups": summarize_suspicious_groups(suspicious_groups),
            "partial_variants": summarize_partial_variants(partial_classifications),
            "targeted_seed": {
                "seed_id": targeted_result.get("seed_id"),
                "validation_status": targeted_result.get("validation_status"),
                "recommended_action": targeted_result.get("recommended_action"),
            },
        }

    except Exception as exc:
        error_type = classify_exception(exc)
        error_record = make_error(
            error_type, str(exc),
            failed_stage=state.get("current_stage", "unknown"),
            traceback_short=traceback.format_exc()[-500:],
        )
        mark_validation_item_failed(
            state,
            state.get("current_validation_item") or "unknown",
            error_type, str(exc),
            state_path,
        )
        return {"ok": False, "error": error_record}
