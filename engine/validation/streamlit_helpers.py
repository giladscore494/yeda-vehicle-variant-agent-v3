"""Streamlit-facing helper wrappers for validation/export flows."""
from __future__ import annotations

from engine.validation.final_export import (
    export_final_clean_database as _export_final_clean_database,
)


def export_final_clean_database() -> dict:
    """Export the final clean database and return a UI-safe summary."""
    summary = _export_final_clean_database()
    return {
        "final_path": summary.get("final_path")
        or summary.get("output_path")
        or "data/final/resume_package_final_clean.json",
        "total_input_variants": summary.get("total_input_variants")
        or summary.get("input_variant_count")
        or 0,
        "total_output_variants": summary.get("total_output_variants")
        or summary.get("output_variant_count")
        or 0,
        "safe_decisions_applied": summary.get("safe_decisions_applied", 0),
        "manual_review_remaining_count": summary.get(
            "manual_review_remaining_count", 0
        ),
        "created_at": summary.get("created_at")
        or summary.get("metadata", {}).get("created_at")
        or "",
    }
