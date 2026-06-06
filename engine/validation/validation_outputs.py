"""Validation output writer — writes all validation output files.

Validation working output: a FULL canonical-style JSON package at the legacy
  data/validated_runs/resume_package_canonical_validated_v2.json

This file keeps the same top-level structure as the original canonical so the
app/code can load it like the original.  Validation metadata is added in a
non-breaking way.

Primary validation working files:
  data/validation/validation_report.json
  data/validation/issue_queue.json
  data/validation/decisions.json

Legacy reports under data/validated_runs/ remain supported for backward compatibility.
"""
from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path

from core.paths import (
    DECISIONS_PATH,
    ISSUE_QUEUE_PATH,
    SOURCE_CANONICAL_PATH,
    VALIDATION_REPORT_PATH,
)
from engine.validation.write_guard import check_write_allowed, safe_write_json


# ── Primary output: full canonical-style validated package ──────────────


def write_validated_package(
    canonical: dict,
    deterministic_issues: list[dict],
    partial_classifications: list[dict],
    suspicious_groups: list[dict],
    targeted_seed_result: dict | None,
    validation_run_id: str,
    output_path: str | Path = "data/validated_runs/resume_package_canonical_validated_v2.json",
    input_path: str | Path = SOURCE_CANONICAL_PATH,
) -> None:
    """Write the full validated canonical-style JSON package.

    Preserves ALL original fields and structure.  Adds validation metadata
    alongside the existing data in a non-breaking way.  Never removes or
    renames original fields.
    """
    check_write_allowed(output_path)

    out_p = Path(output_path).resolve()
    in_p = Path(input_path).resolve()
    if out_p == in_p:
        raise RuntimeError("Refusing to overwrite source canonical file")

    # Deep-copy the canonical so we never modify the in-memory original
    package = copy.deepcopy(canonical)

    now = datetime.now(timezone.utc).isoformat()

    # ── Build per-variant validation status index ───────────────────────

    # Index partial classifications by variant_id for fast lookup
    partial_index: dict[str, dict] = {}
    for pc in partial_classifications:
        vid = pc.get("variant_id", "")
        if vid:
            partial_index[vid] = pc

    # Index deterministic issues by variant_id
    det_by_variant: dict[str, list[dict]] = {}
    for issue in deterministic_issues:
        vid = issue.get("variant_id", "")
        if vid:
            det_by_variant.setdefault(vid, []).append(issue)

    # ── Annotate variants with validation_metadata ──────────────────────

    for vlist_key in ("verified_variants", "partial_variants"):
        variants = package.get(vlist_key) or []
        for v in variants:
            if not isinstance(v, dict):
                continue
            vid = v.get("variant_id", "")

            v_issues = det_by_variant.get(vid, [])
            pc = partial_index.get(vid)

            vmeta: dict = {
                "validated_at": now,
                "validation_run_id": validation_run_id,
                "deterministic_issues": [
                    {"issue_type": i["issue_type"], "severity": i["severity"]}
                    for i in v_issues
                ],
                "deterministic_issue_count": len(v_issues),
            }

            if pc:
                vmeta["partial_validation_status"] = pc.get("validation_status")
                vmeta["partial_risk_level"] = pc.get("risk_level")
                vmeta["partial_risk_score"] = pc.get("risk_score")
                vmeta["partial_issues"] = pc.get("issues", [])
                vmeta["partial_recommended_action"] = pc.get("recommended_action")
                vmeta["needs_gemini_review"] = pc.get("needs_gemini_review", False)
                vmeta["needs_openai_second_opinion"] = pc.get("needs_openai_second_opinion", False)

            v["validation_metadata"] = vmeta

    # ── Per-seed validation status ──────────────────────────────────────
    # Include ALL seeds from catalog + any bucket-only seeds

    det_by_seed: dict[str, list[dict]] = {}
    for issue in deterministic_issues:
        sid = issue.get("seed_id", "")
        if sid:
            det_by_seed.setdefault(sid, []).append(issue)

    suspicious_by_seed: dict[str, dict] = {}
    for sg in suspicious_groups:
        sid = sg.get("seed_id", "")
        if sid:
            suspicious_by_seed[sid] = sg

    # Build seed catalog index for make/model/year lookup
    from engine.state import seed_id_from_seed, load_seeds as _load_seeds

    seed_catalog = _load_seeds("data/seeds/vehicle_model_seeds_il.json")
    seed_catalog_index: dict[str, dict] = {}
    catalog_ids: set[str] = set()
    for s in seed_catalog:
        sid = seed_id_from_seed(s)
        seed_catalog_index[sid] = s
        catalog_ids.add(sid)

    # Collect all variant counts by seed
    all_v = (package.get("verified_variants") or []) + \
            (package.get("partial_variants") or [])
    variant_count_by_seed: dict[str, int] = {}
    for v in all_v:
        if isinstance(v, dict):
            sid = str(v.get("seed_id", "")).strip()
            if sid:
                variant_count_by_seed[sid] = variant_count_by_seed.get(sid, 0) + 1

    validation_status_by_seed: dict[str, dict] = {}
    bs = package.get("batch_state") or {}

    processed_set = set(bs.get("processed_seed_ids") or [])
    failed_set = set(bs.get("failed_seed_ids") or [])
    manual_set = set(bs.get("manual_review_seed_ids") or [])
    retry_set = set(bs.get("needs_retry_seed_ids") or [])
    next_seed = bs.get("next_seed_id")

    # Union of catalog + all bucket seed IDs
    all_seed_ids = catalog_ids | processed_set | failed_set | manual_set | retry_set

    for sid in sorted(all_seed_ids):
        s_issues = det_by_seed.get(sid, [])
        sg = suspicious_by_seed.get(sid)
        seed_info = seed_catalog_index.get(sid, {})
        vcount = variant_count_by_seed.get(sid, 0)

        validation_status_by_seed[sid] = {
            "seed_id": sid,
            "make": seed_info.get("make", ""),
            "model": seed_info.get("model", ""),
            "year_start": seed_info.get("year_start"),
            "year_end": seed_info.get("year_end"),
            "in_catalog": sid in catalog_ids,
            "in_processed": sid in processed_set,
            "in_failed": sid in failed_set,
            "in_needs_retry": sid in retry_set,
            "in_manual_review": sid in manual_set,
            "is_next_seed": sid == next_seed if next_seed else False,
            "has_variants": vcount > 0,
            "variant_count": vcount,
            "deterministic_issue_count": len(s_issues),
            "is_suspicious": sg is not None,
            "suspicious_reason": sg.get("reason") if sg else None,
            "risk_level": sg.get("risk_level") if sg else "low",
            "recommended_action": (
                "manual_review" if sid in manual_set
                else "retry" if sid in retry_set
                else "investigate" if sg is not None
                else "no_action"
            ),
        }

    # ── Add top-level validation summary ────────────────────────────────

    all_variants = (package.get("verified_variants") or []) + \
                   (package.get("partial_variants") or [])

    from engine.validation.deterministic_audit import summarize_deterministic_issues
    from engine.validation.suspicious_groups import summarize_suspicious_groups
    from engine.validation.partial_variants import summarize_partial_variants

    package["validation_summary"] = {
        "validation_run_id": validation_run_id,
        "validated_at": now,
        "source_canonical_path": str(input_path),
        "total_variants_scanned": len(all_variants),
        "total_verified_variants": len(package.get("verified_variants") or []),
        "total_partial_variants": len(package.get("partial_variants") or []),
        "deterministic_checks": summarize_deterministic_issues(deterministic_issues),
        "suspicious_groups": summarize_suspicious_groups(suspicious_groups),
        "partial_variants_summary": summarize_partial_variants(partial_classifications),
        "targeted_seed_result": {
            "seed_id": targeted_seed_result.get("seed_id", "") if targeted_seed_result else "",
            "validation_status": targeted_seed_result.get("validation_status", "") if targeted_seed_result else "",
        } if targeted_seed_result else None,
    }

    package["validation_status_by_seed"] = validation_status_by_seed

    # Write the full package
    out_p.parent.mkdir(parents=True, exist_ok=True)
    safe_write_json(package, out_p)


# ── Secondary reports ───────────────────────────────────────────────────


def write_validation_report(
    validation_run_id: str,
    canonical: dict,
    deterministic_issues: list[dict],
    suspicious_groups: list[dict],
    partial_classifications: list[dict],
    targeted_seed_result: dict | None,
    model_calls_summary: dict | None = None,
    started_at: str = "",
    completed_at: str = "",
    output_path: str | Path = VALIDATION_REPORT_PATH,
) -> None:
    """Write the validation report summary."""
    check_write_allowed(output_path)

    all_variants = (canonical.get("verified_variants") or []) + \
                   (canonical.get("partial_variants") or [])
    bs = canonical.get("batch_state") or {}

    from engine.validation.deterministic_audit import summarize_deterministic_issues
    from engine.validation.suspicious_groups import summarize_suspicious_groups
    from engine.validation.partial_variants import summarize_partial_variants

    report = {
        "validation_run_id": validation_run_id,
        "source_canonical_path": SOURCE_CANONICAL_PATH,
        "output_path": str(output_path),
        "started_at": started_at,
        "completed_at": completed_at,
        "total_variants": len(all_variants),
        "total_verified_variants": len(canonical.get("verified_variants") or []),
        "total_partial_variants": len(canonical.get("partial_variants") or []),
        "total_seeds": len(set(
            (bs.get("processed_seed_ids") or []) +
            (bs.get("failed_seed_ids") or []) +
            (bs.get("manual_review_seed_ids") or [])
        )),
        "deterministic_checks_summary": summarize_deterministic_issues(deterministic_issues),
        "suspicious_groups_summary": summarize_suspicious_groups(suspicious_groups),
        "partial_variants_summary": summarize_partial_variants(partial_classifications),
        "model_calls_summary": model_calls_summary or {
            "gemini_calls": 0,
            "openai_calls": 0,
            "total_model_calls": 0,
        },
        "final_recommendations": _build_recommendations(
            deterministic_issues, suspicious_groups, partial_classifications, targeted_seed_result
        ),
    }

    safe_write_json(report, output_path)


def write_validation_issues(
    issues: list[dict],
    output_path: str | Path = ISSUE_QUEUE_PATH,
) -> None:
    """Write the validation issues file."""
    check_write_allowed(output_path)
    safe_write_json(issues, output_path)


def write_patch_suggestions(
    deterministic_issues: list[dict],
    partial_classifications: list[dict],
    model_validation_items: list[dict] | None = None,
    output_path: str | Path = DECISIONS_PATH,
) -> None:
    """Write patch suggestions. These are suggestions only — never applied to canonical."""
    check_write_allowed(output_path)

    patches: list[dict] = []
    patch_counter = 0

    for issue in deterministic_issues:
        action = issue.get("recommended_action", "")
        if not action or action.startswith("No action"):
            continue

        itype = issue.get("issue_type", "")
        if itype in ("body_type_not_normalized", "fuel_type_not_normalized",
                      "transmission_not_normalized"):
            patch_counter += 1
            patches.append({
                "patch_id": f"patch_{patch_counter:05d}",
                "source": "deterministic_audit",
                "seed_id": issue.get("seed_id", ""),
                "variant_id": issue.get("variant_id", ""),
                "field": itype.replace("_not_normalized", ""),
                "current_value": issue.get("current_value", ""),
                "suggested_value": "",
                "reason": f"Field needs normalization: {itype}",
                "evidence": issue.get("evidence", []),
                "confidence": 0.0,
                "primary_model": None,
                "secondary_model": None,
                "safe_to_auto_apply": False,
            })
        elif itype == "year_range_inverted":
            patch_counter += 1
            patches.append({
                "patch_id": f"patch_{patch_counter:05d}",
                "source": "deterministic_audit",
                "seed_id": issue.get("seed_id", ""),
                "variant_id": issue.get("variant_id", ""),
                "field": "year_range",
                "current_value": issue.get("current_value", ""),
                "suggested_value": "swap year_start and year_end",
                "reason": "Year range is inverted",
                "evidence": [],
                "confidence": 0.8,
                "primary_model": None,
                "secondary_model": None,
                "safe_to_auto_apply": False,
            })
        elif itype == "placeholder_source_ids":
            patch_counter += 1
            patches.append({
                "patch_id": f"patch_{patch_counter:05d}",
                "source": "deterministic_audit",
                "seed_id": issue.get("seed_id", ""),
                "variant_id": issue.get("variant_id", ""),
                "field": "source_ids",
                "current_value": issue.get("current_value", ""),
                "suggested_value": "Replace with real source references",
                "reason": "Placeholder source_ids detected",
                "evidence": [],
                "confidence": 0.0,
                "primary_model": None,
                "secondary_model": None,
                "safe_to_auto_apply": False,
            })

    for pc in partial_classifications:
        status = pc.get("validation_status", "")
        if status in ("needs_normalization", "merge_candidate", "needs_evidence"):
            patch_counter += 1
            patches.append({
                "patch_id": f"patch_{patch_counter:05d}",
                "source": "partial_classification",
                "seed_id": pc.get("seed_id", ""),
                "variant_id": pc.get("variant_id", ""),
                "field": "partial_variant",
                "current_value": status,
                "suggested_value": pc.get("recommended_action", ""),
                "reason": f"Partial variant classified as {status}",
                "evidence": pc.get("evidence", []),
                "confidence": 0.0,
                "primary_model": None,
                "secondary_model": None,
                "safe_to_auto_apply": False,
            })

    # Add model validation suggestions
    if model_validation_items:
        for mvi in model_validation_items:
            patch_info = mvi.get("suggested_patch") or {}
            if not patch_info.get("has_patch", False):
                continue
            patch_counter += 1
            patches.append({
                "patch_id": f"patch_{patch_counter:05d}",
                "source": "model_validation",
                "seed_id": mvi.get("seed_id", ""),
                "variant_id": patch_info.get("target_variant_id", ""),
                "field": patch_info.get("field", ""),
                "current_value": patch_info.get("current_value"),
                "suggested_value": patch_info.get("suggested_value"),
                "reason": patch_info.get("reason", ""),
                "evidence": mvi.get("evidence", []),
                "confidence": mvi.get("confidence", 0.0),
                "primary_model": mvi.get("primary_model", "gemini"),
                "secondary_model": mvi.get("secondary_model"),
                "safe_to_auto_apply": False,
            })

    safe_write_json(patches, output_path)


def write_targeted_seed_validation(
    result: dict,
    output_path: str | Path = "data/validated_runs/targeted_seed_validation_v2.json",
) -> None:
    """Write the targeted seed validation result."""
    check_write_allowed(output_path)
    safe_write_json(result, output_path)


def _build_recommendations(
    deterministic_issues: list[dict],
    suspicious_groups: list[dict],
    partial_classifications: list[dict],
    targeted_seed_result: dict | None,
) -> list[str]:
    """Build human-readable recommendations from validation results."""
    recs: list[str] = []

    high_critical = [i for i in deterministic_issues if i.get("severity") in ("high", "critical")]
    if high_critical:
        recs.append(f"{len(high_critical)} high/critical deterministic issues found — review required")

    if suspicious_groups:
        high_risk = [g for g in suspicious_groups if g.get("risk_level") in ("high", "critical")]
        if high_risk:
            recs.append(f"{len(high_risk)} high-risk suspicious groups — model validation recommended")

    needs_evidence = [p for p in partial_classifications if p.get("validation_status") == "needs_evidence"]
    if needs_evidence:
        recs.append(f"{len(needs_evidence)} partial variants need evidence before promotion")

    merge_candidates = [p for p in partial_classifications if p.get("validation_status") == "merge_candidate"]
    if merge_candidates:
        recs.append(f"{len(merge_candidates)} partial variants are merge candidates")

    if targeted_seed_result:
        sid = targeted_seed_result.get("seed_id", "")
        action = targeted_seed_result.get("recommended_action", "")
        recs.append(f"Targeted seed {sid}: {action}")

    if not recs:
        recs.append("No critical issues found — database looks clean")

    return recs
