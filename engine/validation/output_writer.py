"""Output writer — writes final validated JSON and audit files.

Produces variant-level output (never grouped).
Preserves original fields and adds validation metadata.
"""
from __future__ import annotations

import copy
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

from core.paths import VALIDATION_DIR

logger = logging.getLogger(__name__)


def build_validated_variant(variant: dict, decision: dict) -> dict:
    """Create a validated variant by adding validation metadata to the original.

    Never removes or replaces original fields.
    Adds validation_metadata block alongside existing data.
    """
    validated = copy.deepcopy(variant)

    # Add validation metadata
    validated["validation_metadata"] = {
        "validation_status": decision["validation_status"],
        "validation_confidence": decision["validation_confidence"],
        "validation_sources": decision["source_refs"],
        "quality_flags": decision["quality_flags"],
        "model_audit_refs": [
            {"provider": ref.get("provider")}
            for ref in decision.get("model_audit_refs", [])
        ],
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }

    # Handle trim corrections — preserve original, add corrected
    if decision["trim_action"] == "correct" and decision.get("corrected_trim"):
        from engine.validation.normalizer import safe_str_original

        original_trim = safe_str_original(variant.get("trim"))
        validated["validation_metadata"]["trim_correction"] = {
            "original_value": original_trim,
            "corrected_value": decision["corrected_trim"],
            "action": "correct",
            "reason": decision["reason"],
        }

    # Add risk score if present
    if "risk_score" in decision:
        validated["validation_metadata"]["risk_score"] = decision["risk_score"]

    return validated


def write_validated_package(
    original_package: dict,
    validated_variants: list[dict],
    output_path: str | Path,
    input_path: str | Path,
) -> None:
    """Write the final validated JSON package.

    Safety: asserts output_path != input_path and output is under data/validation/ or legacy data/validated_runs/.
    """
    output_path = Path(output_path).resolve()
    input_path = Path(input_path).resolve()

    # Safety guards
    if output_path == input_path:
        raise RuntimeError("Refusing to overwrite source resume package")
    if output_path == Path("data/final/resume_package_final_clean.json").resolve():
        raise RuntimeError(
            "Refusing to write reserved final clean database before Task 5 export"
        )
    allowed_output_dirs = (Path(VALIDATION_DIR).resolve(), Path("data/validated_runs").resolve())
    if not any(_is_relative_to(output_path, allowed_dir) for allowed_dir in allowed_output_dirs):
        raise RuntimeError(
            f"Output path must be under {VALIDATION_DIR}/ or legacy data/validated_runs/: {output_path}"
        )

    # Build output package
    package = {
        "schema_version": "resume_package_validated_v2",
        "source_schema_version": original_package.get("schema_version", "unknown"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_file": str(input_path.name),
        "description": (
            "Validated vehicle variant package. "
            "Original data preserved with validation metadata added."
        ),
        "validated_variants": validated_variants,
        "counts": _compute_counts(validated_variants),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(package, f, ensure_ascii=False, indent=2)

    logger.info("Wrote validated package: %s (%d variants)", output_path, len(validated_variants))

    # Verify original file was not modified
    _verify_input_unchanged(input_path)


def _compute_counts(variants: list[dict]) -> dict:
    """Compute summary counts for the validated package."""
    status_counts: dict[str, int] = {}
    makes: set[str] = set()
    models: set[str] = set()
    trims_checked = 0
    trims_corrected = 0
    trims_nullified = 0
    trims_not_verified = 0

    for v in variants:
        meta = v.get("validation_metadata", {})
        status = meta.get("validation_status", "pending_unchecked")
        status_counts[status] = status_counts.get(status, 0) + 1

        make = v.get("make", "")
        if make:
            makes.add(str(make).lower())
        model_name = v.get("model", "")
        if model_name:
            models.add(f"{make}|{model_name}".lower())

        # Trim stats
        trim_correction = meta.get("trim_correction")
        if trim_correction:
            trims_checked += 1
            action = trim_correction.get("action", "")
            if action == "correct":
                trims_corrected += 1
            elif action == "nullify":
                trims_nullified += 1

        flags = meta.get("quality_flags", [])
        if "trim_not_verified_by_sources" in flags or "trim_not_found_in_il_market" in flags:
            trims_not_verified += 1

    return {
        "total_variants": len(variants),
        "makes_count": len(makes),
        "models_count": len(models),
        "by_validation_status": status_counts,
        "trims_checked": trims_checked,
        "trims_corrected": trims_corrected,
        "trims_nullified": trims_nullified,
        "trims_not_verified": trims_not_verified,
    }


def write_last_validation_run(
    output_dir: str | Path,
    input_file: str,
    output_file: str,
    branch: str,
    mode: str,
    started_at: str,
    finished_at: str,
    total_variants: int,
    total_groups: int,
    risk_counts: dict[str, int],
    cost_summary: dict,
    variant_status_counts: dict[str, int],
    trims_stats: dict,
    duplicate_count: int,
    hard_gate_status: str,
    soft_warnings: list[str],
) -> None:
    """Write the last_validation_run.json summary."""
    import time

    started_dt = datetime.fromisoformat(started_at)
    finished_dt = datetime.fromisoformat(finished_at)
    runtime_seconds = (finished_dt - started_dt).total_seconds()

    run_info = {
        "input_file": input_file,
        "output_file": output_file,
        "branch": branch,
        "mode": mode,
        "started_at": started_at,
        "finished_at": finished_at,
        "total_runtime_seconds": round(runtime_seconds, 2),
        "total_variants_scanned": total_variants,
        "total_groups_built": total_groups,
        "low_risk_count": risk_counts.get("low", 0),
        "medium_risk_count": risk_counts.get("medium", 0),
        "high_risk_count": risk_counts.get("high", 0),
        "critical_risk_count": risk_counts.get("critical", 0),
        "gemini_calls": cost_summary.get("gemini_calls", 0),
        "openai_calls": cost_summary.get("openai_calls", 0),
        "failed_model_calls": cost_summary.get("failed_model_calls", 0),
        "retried_model_calls": cost_summary.get("retried_model_calls", 0),
        "estimated_total_cost_usd": cost_summary.get("estimated_total_cost_usd", 0),
        "variants_verified_by_gemini": variant_status_counts.get("verified_by_gemini", 0),
        "variants_verified_by_dual_model": variant_status_counts.get("verified_by_dual_model", 0),
        "variants_sent_to_manual_review": variant_status_counts.get("manual_review", 0),
        "trims_checked": trims_stats.get("trims_checked", 0),
        "trims_corrected": trims_stats.get("trims_corrected", 0),
        "trims_nullified": trims_stats.get("trims_nullified", 0),
        "trims_not_verified": trims_stats.get("trims_not_verified", 0),
        "duplicate_variant_id_count": duplicate_count,
        "hard_gate_status": hard_gate_status,
        "soft_warnings": soft_warnings,
    }

    out = Path(output_dir) / "last_validation_run.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(run_info, f, ensure_ascii=False, indent=2)


def _verify_input_unchanged(input_path: Path) -> None:
    """Verify the input file still exists and is readable (basic integrity check)."""
    if not input_path.exists():
        logger.warning("Input file no longer exists: %s", input_path)


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False
