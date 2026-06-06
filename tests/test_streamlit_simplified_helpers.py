"""Regression tests for streamlit helper export wiring."""
from __future__ import annotations

from engine.validation import streamlit_helpers


def test_export_final_clean_database_exists():
    assert hasattr(streamlit_helpers, "export_final_clean_database")


def test_export_final_clean_database_maps_summary_fields(monkeypatch):
    def _fake_backend_summary():
        return {
            "output_path": "data/final/custom.json",
            "input_variant_count": 12,
            "output_variant_count": 7,
            "safe_decisions_applied": 3,
            "manual_review_remaining_count": 2,
            "metadata": {"created_at": "2026-01-01T00:00:00Z"},
        }

    monkeypatch.setattr(
        streamlit_helpers,
        "_export_final_clean_database",
        _fake_backend_summary,
    )

    summary = streamlit_helpers.export_final_clean_database()

    assert summary["final_path"] == "data/final/custom.json"
    assert summary["total_input_variants"] == 12
    assert summary["total_output_variants"] == 7
    assert summary["safe_decisions_applied"] == 3
    assert summary["manual_review_remaining_count"] == 2
    assert summary["created_at"] == "2026-01-01T00:00:00Z"
