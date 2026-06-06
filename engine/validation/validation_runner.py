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
from core.paths import ISSUE_QUEUE_PATH
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
    mark_pipeline_stage_completed,
    update_model_validation_counts,
)
from engine.validation.validation_outputs import (
    write_validated_package,
    write_validation_report,
    write_validation_issues,
    write_patch_suggestions,
    write_targeted_seed_validation,
)
from engine.validation.error_types import make_error, classify_exception
from engine.validation.model_validation_items import build_model_validation_items
from engine.validation.run_manifest import write_run_manifest
from engine.validation.seed_accounting import compute_seed_accounting


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
        mark_pipeline_stage_completed(state, "deterministic_audit", state_path)

        # ── Step 2: Partial variant classification ──────────────────────
        update_validation_progress(
            state, stage="PARTIAL_VARIANT_CLASSIFICATION",
            current_item="All partial variants", path=state_path,
        )

        partial_classifications = classify_all_partial_variants(canonical)
        mark_validation_item_completed(state, "partial_classification", state_path)
        mark_pipeline_stage_completed(state, "partial_classification", state_path)

        # ── Step 3: Suspicious groups ───────────────────────────────────
        update_validation_progress(
            state, stage="SUSPICIOUS_GROUP_DETECTION",
            current_item="Building suspicious groups", path=state_path,
        )

        suspicious_groups = build_suspicious_groups(canonical, seeds)
        mark_validation_item_completed(state, "suspicious_groups", state_path)
        mark_pipeline_stage_completed(state, "suspicious_groups", state_path)

        # ── Step 4: Targeted seed validation ────────────────────────────
        update_validation_progress(
            state, stage="TARGETED_SEED_VALIDATION",
            current_item=_TARGET_SEED_ID, path=state_path,
        )

        targeted_result = validate_targeted_seed(_TARGET_SEED_ID, canonical, seeds)
        mark_validation_item_completed(state, "targeted_seed", state_path)
        mark_pipeline_stage_completed(state, "targeted_seed", state_path)

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

        # Write the run manifest
        write_run_manifest(
            validation_run_id=run_id,
            mode="full-validation",
            started_at=started_at,
            completed_at=completed_at,
            canonical=canonical,
            seeds=seeds,
            targeted_seed_id=_TARGET_SEED_ID,
            stages_completed=[
                {
                    "stage": "deterministic_audit",
                    "input_count": len(all_variants),
                    "output_count": len(deterministic_issues),
                    "output_file": ISSUE_QUEUE_PATH,
                },
                {
                    "stage": "partial_classification",
                    "input_count": len(canonical.get("partial_variants") or []),
                    "output_count": len(partial_classifications),
                },
                {
                    "stage": "suspicious_groups",
                    "input_count": len(all_variants),
                    "output_count": len(suspicious_groups),
                },
                {
                    "stage": "targeted_seed",
                    "input_count": 1,
                    "output_count": 1,
                    "output_file": "data/validated_runs/targeted_seed_validation_v2.json",
                },
            ],
        )

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


def run_model_validation_on_suspicious_groups(
    canonical_path: str | None = None,
    seeds_path: str = "data/seeds/vehicle_model_seeds_il.json",
    state_path: str | None = None,
    max_items: int | None = None,
    risk_levels: list[str] | None = None,
    group_types: list[str] | None = None,
    seed_id_filter: str | None = None,
    dry_run_preview: bool = False,
) -> dict:
    """Run model validation on suspicious groups ONLY.

    This is a separate step from the full validation session.
    Full Validation does NOT automatically call models.

    Parameters:
        max_items: Maximum number of model validation items to run.
        risk_levels: Only include items with these risk levels.
        group_types: Only include items with these group types.
        seed_id_filter: Only include items whose seed_id contains this string.
        dry_run_preview: If True, return the selected queue preview without
            calling Gemini/OpenAI.

    Steps:
    1. Load canonical (read-only)
    2. Load seed catalog for coverage checks
    3. Recompute deterministic audit / suspicious groups / partial classifications
    4. Build group-level model validation items
    5. Apply filters and slicing
    6. Call Gemini for suspicious groups only (unless dry_run_preview)
    7. Call OpenAI for second-opinion high-risk cases only
    8. Aggregate results
    9. Write model_validation_results_v2.json
    10. Write run manifest
    11. Never write to canonical
    """
    # Branch guard
    branch_err = _check_branch()
    if branch_err:
        return {"ok": False, "error": make_error(
            "config_error_invalid_branch", branch_err,
            failed_stage="branch_check",
        )}

    state = load_validation_state(state_path)
    mark_validation_started(state, state_path)

    try:
        # ── Load data ───────────────────────────────────────────────────
        update_validation_progress(
            state, stage="MODEL_VALIDATION_LOADING", path=state_path,
        )

        canonical = load_canonical(canonical_path or CANONICAL_RESUME_PATH)
        ensure_batch_state_fields(canonical)
        seeds = load_seeds(seeds_path)

        # ── Recompute deterministic pipeline ────────────────────────────
        update_validation_progress(
            state, stage="MODEL_VALIDATION_DETERMINISTIC_PREP", path=state_path,
        )

        deterministic_issues = run_deterministic_audit(canonical, seeds)
        partial_classifications = classify_all_partial_variants(canonical)
        suspicious_groups = build_suspicious_groups(canonical, seeds)

        if not suspicious_groups:
            mark_validation_completed(state, state_path)
            return {
                "ok": True,
                "model_validation_ran": False,
                "reason": "No suspicious groups found — model validation not needed",
                "deterministic_validation_ran": True,
                "model_calls_summary": {
                    "gemini_calls_attempted": 0, "gemini_calls_success": 0,
                    "gemini_calls_failed": 0, "openai_calls_attempted": 0,
                    "openai_calls_success": 0, "openai_calls_failed": 0,
                },
            }

        # ── Build model validation items ────────────────────────────────
        update_validation_progress(
            state, stage="MODEL_VALIDATION_BUILDING_ITEMS", path=state_path,
        )

        validation_items = build_model_validation_items(
            suspicious_groups, canonical,
            deterministic_issues, partial_classifications,
        )

        # ── Apply filters and slicing ───────────────────────────────────
        all_items = validation_items  # keep original list for accounting
        filtered_items = list(validation_items)

        if risk_levels:
            filtered_items = [
                it for it in filtered_items
                if it.get("risk_level", "medium") in risk_levels
            ]

        if group_types:
            filtered_items = [
                it for it in filtered_items
                if it.get("group_type", "") in group_types
            ]

        if seed_id_filter:
            filtered_items = [
                it for it in filtered_items
                if seed_id_filter in (it.get("seed_id") or "")
            ]

        # Sort priority: critical > high > medium > low,
        # manual_review_seed before evidence_gap at same risk
        _risk_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        _type_order = {"manual_review_seed": 0}

        filtered_items.sort(key=lambda it: (
            _risk_order.get(it.get("risk_level", "medium"), 2),
            _type_order.get(it.get("group_type", ""), 1),
        ))

        if max_items is not None:
            filtered_items = filtered_items[:max_items]

        selected_items = filtered_items

        # Update model validation counts in state
        update_model_validation_counts(
            state,
            available=len(all_items),
            selected=len(selected_items),
            path=state_path,
        )

        # ── Dry run preview ─────────────────────────────────────────────
        if dry_run_preview:
            mark_validation_completed(state, state_path)
            return {
                "ok": True,
                "dry_run_preview": True,
                "model_validation_ran": False,
                "total_available_items": len(all_items),
                "selected_items_count": len(selected_items),
                "selected_items": _build_queue_preview(selected_items, canonical, seeds),
                "filters_applied": {
                    "max_items": max_items,
                    "risk_levels": risk_levels,
                    "group_types": group_types,
                    "seed_id_filter": seed_id_filter,
                },
            }

        if not selected_items:
            mark_validation_completed(state, state_path)
            return {
                "ok": True,
                "model_validation_ran": False,
                "reason": "No items matched the selected filters",
                "deterministic_validation_ran": True,
                "total_available_items": len(all_items),
                "model_calls_summary": {
                    "gemini_calls_attempted": 0, "gemini_calls_success": 0,
                    "gemini_calls_failed": 0, "openai_calls_attempted": 0,
                    "openai_calls_success": 0, "openai_calls_failed": 0,
                },
            }

        # ── Run model validation ────────────────────────────────────────
        update_validation_progress(
            state, stage="MODEL_VALIDATION_RUNNING",
            total_items=len(selected_items), path=state_path,
        )

        from engine.validation.model_validation_runner import run_model_validation

        model_results = run_model_validation(
            selected_items,
            output_dir=VALIDATION_OUTPUT_PATH,
        )

        # ── Update output files ─────────────────────────────────────────
        update_validation_progress(
            state, stage="MODEL_VALIDATION_WRITING_OUTPUTS", path=state_path,
        )

        run_id = state.get("validation_run_id", "unknown")
        started_at = model_results.get("started_at", "")
        completed_at = model_results.get("completed_at", "")

        # Update validated package with model validation metadata
        write_validated_package(
            canonical=canonical,
            deterministic_issues=deterministic_issues,
            partial_classifications=partial_classifications,
            suspicious_groups=suspicious_groups,
            targeted_seed_result=None,
            validation_run_id=run_id,
        )

        # Update validation report with model_calls_summary
        model_calls_summary = model_results.get("model_calls_summary", {})
        model_calls_summary["model_validation_ran"] = True
        model_calls_summary["model_validation_items_count"] = model_results.get(
            "model_validation_items_count", 0
        )
        model_calls_summary["model_validation_failed_items_count"] = model_results.get(
            "model_validation_failed_items_count", 0
        )
        model_calls_summary["model_validation_output_path"] = model_results.get(
            "model_validation_output_path", ""
        )

        write_validation_report(
            validation_run_id=run_id,
            canonical=canonical,
            deterministic_issues=deterministic_issues,
            suspicious_groups=suspicious_groups,
            partial_classifications=partial_classifications,
            targeted_seed_result=None,
            model_calls_summary=model_calls_summary,
            started_at=started_at,
            completed_at=completed_at,
        )

        # Update patch suggestions with model suggestions
        write_patch_suggestions(
            deterministic_issues, partial_classifications,
            model_validation_items=model_results.get("items", []),
        )

        # Write run manifest
        mcs = model_results.get("model_calls_summary", {})
        write_run_manifest(
            validation_run_id=run_id,
            mode="model-validation",
            started_at=started_at,
            completed_at=completed_at,
            canonical=canonical,
            seeds=seeds,
            stages_completed=[
                {
                    "stage": "deterministic_audit",
                    "input_count": len(
                        (canonical.get("verified_variants") or []) +
                        (canonical.get("partial_variants") or [])
                    ),
                    "output_count": len(deterministic_issues),
                    "output_file": ISSUE_QUEUE_PATH,
                },
                {
                    "stage": "partial_classification",
                    "input_count": len(canonical.get("partial_variants") or []),
                    "output_count": len(partial_classifications),
                },
                {
                    "stage": "suspicious_groups",
                    "input_count": len(all_items),
                    "output_count": len(suspicious_groups),
                },
                {
                    "stage": "model_validation",
                    "available_items": len(all_items),
                    "selected_items": len(selected_items),
                    "gemini_calls_attempted": mcs.get("gemini_calls_attempted", 0),
                    "gemini_calls_success": mcs.get("gemini_calls_success", 0),
                    "openai_calls_attempted": mcs.get("openai_calls_attempted", 0),
                    "openai_calls_success": mcs.get("openai_calls_success", 0),
                },
            ],
            model_items_selected=[
                {
                    "validation_item_id": it.get("validation_item_id", ""),
                    "group_type": it.get("group_type", ""),
                    "seed_id": it.get("seed_id", ""),
                    "risk_level": it.get("risk_level", ""),
                    "variant_count": it.get("group_data", {}).get("variant_count", 0),
                }
                for it in selected_items
            ],
        )

        # ── Done ────────────────────────────────────────────────────────
        mark_validation_completed(state, state_path)

        return {
            "ok": True,
            "deterministic_validation_ran": True,
            "model_validation_ran": True,
            **model_results.get("model_calls_summary", {}),
            "model_validation_items_count": model_results.get(
                "model_validation_items_count", 0
            ),
            "model_validation_failed_items_count": model_results.get(
                "model_validation_failed_items_count", 0
            ),
            "model_validation_output_path": model_results.get(
                "model_validation_output_path", ""
            ),
            "last_model_validation_error": model_results.get(
                "last_model_validation_error"
            ),
            "suspicious_groups_count": len(suspicious_groups),
            "validation_items_count": len(all_items),
            "selected_items_count": len(selected_items),
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
            state.get("current_validation_item") or "model_validation",
            error_type, str(exc),
            state_path,
        )
        return {"ok": False, "error": error_record}


def _build_queue_preview(
    items: list[dict],
    canonical: dict,
    seeds: list[dict],
) -> list[dict]:
    """Build a human-readable preview of model validation items."""
    from engine.state import seed_id_from_seed

    # Build seed catalog index for resolving make/model/year on no-variant items
    seed_index: dict[str, dict] = {}
    for s in seeds:
        sid = seed_id_from_seed(s)
        seed_index[sid] = s

    from core.config import GEMINI_MODEL_STRONG, OPENAI_VALIDATOR_MODEL_ID

    preview: list[dict] = []
    for idx, item in enumerate(items):
        seed_id = item.get("seed_id", "")
        gd = item.get("group_data", {})
        variant_count = gd.get("variant_count", 0)
        variant_ids = item.get("variant_ids", [])

        # Resolve make/model/year — prefer group data, fall back to seed catalog
        make = ""
        model = ""
        year_start = None
        year_end = None

        variants = gd.get("variants", [])
        if variants:
            v0 = variants[0]
            make = v0.get("make", "")
            model = v0.get("model", "")
            year_start = v0.get("year_start")
            year_end = v0.get("year_end")
        elif seed_id in seed_index:
            s = seed_index[seed_id]
            make = s.get("make", "")
            model = s.get("model", "")
            year_start = s.get("year_start")
            year_end = s.get("year_end")

        needs_openai = item.get("requires_openai_second_opinion_initially", False)

        preview.append({
            "item_index": idx,
            "validation_item_id": item.get("validation_item_id", ""),
            "group_type": item.get("group_type", ""),
            "seed_id": seed_id,
            "make": make,
            "model": model,
            "year_start": year_start,
            "year_end": year_end,
            "risk_level": item.get("risk_level", "medium"),
            "reason_for_model_validation": item.get("reason_for_model_validation", ""),
            "variant_count": variant_count,
            "variant_ids_count": len(variant_ids),
            "requires_openai_second_opinion_initially": needs_openai,
            "planned_primary_provider": "gemini",
            "planned_secondary_provider": "openai" if needs_openai else None,
            "planned_gemini_model": GEMINI_MODEL_STRONG,
            "planned_openai_model": OPENAI_VALIDATOR_MODEL_ID if needs_openai else None,
        })

    return preview


def compute_model_validation_preview(
    canonical_path: str | None = None,
    seeds_path: str = "data/seeds/vehicle_model_seeds_il.json",
) -> dict:
    """Compute the model validation queue preview without running models.

    Returns deterministic issues, partial classifications, suspicious groups,
    and the full model validation item queue preview.
    """
    try:
        canonical = load_canonical(canonical_path or CANONICAL_RESUME_PATH)
        ensure_batch_state_fields(canonical)
        seeds = load_seeds(seeds_path)
    except Exception as exc:
        return {"ok": False, "error": str(exc)}

    deterministic_issues = run_deterministic_audit(canonical, seeds)
    partial_classifications = classify_all_partial_variants(canonical)
    suspicious_groups = build_suspicious_groups(canonical, seeds)

    validation_items = build_model_validation_items(
        suspicious_groups, canonical,
        deterministic_issues, partial_classifications,
    )

    preview = _build_queue_preview(validation_items, canonical, seeds)

    return {
        "ok": True,
        "deterministic_issues_count": len(deterministic_issues),
        "partial_classifications_count": len(partial_classifications),
        "suspicious_groups_count": len(suspicious_groups),
        "validation_items_count": len(validation_items),
        "validation_items": validation_items,
        "queue_preview": preview,
    }