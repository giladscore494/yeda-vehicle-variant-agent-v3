"""Tests for tools/migrate_legacy_state.py."""
import copy
import json
import tempfile
from pathlib import Path

import pytest

from engine.state import load_canonical, get_all_variants


def _make_legacy_canonical():
    return {
        "verified_variants": [
            {"variant_id": f"v{i}", "make": "BMW", "model": "3 Series",
             "verification_status": "verified"} for i in range(5)
        ],
        "partial_variants": [
            {"variant_id": f"p{i}", "make": "Kia", "model": "Sportage"} for i in range(3)
        ],
        "batch_state": {
            "processed_seed_ids": [
                "bmw__3_series__2020__2026__il",
                "hyundai__creta__2020__2026__il",
            ],
            "needs_retry_seed_ids": ["geely__coolray__2023__2026__il"],
            "failed_seed_ids": [],
            "next_seed_id": "volkswagen__jetta__1990__2026__il",
            "last_completed_seed_id": "volkswagen__golf_plus__2005__2020__il",
            "seed_accounting": {
                "hyundai__creta__2020__2026__il": {
                    "status": "resolved",
                    "resolution_type": "no_variants_proven",
                    "proof_status": "proven",
                    "source_ids": ["src_1", "src_2"],
                    "source_basis": "Not sold",
                },
            },
        },
        "counts": {"total_variants": 8},
    }


class TestMigration:
    def test_preserves_variant_count(self, tmp_path):
        canonical = _make_legacy_canonical()
        p = tmp_path / "canonical.json"
        p.write_text(json.dumps(canonical), encoding="utf-8")

        from tools.migrate_legacy_state import migrate
        report = migrate(canonical_path=str(p), dry_run=True)
        assert report["variants_preserved"] is True
        assert report["pre_variants"] == 8
        assert report["post_variants"] == 8

    def test_moves_problematic_to_manual_review(self, tmp_path):
        canonical = _make_legacy_canonical()
        p = tmp_path / "canonical.json"
        p.write_text(json.dumps(canonical), encoding="utf-8")

        from tools.migrate_legacy_state import migrate
        report = migrate(canonical_path=str(p), dry_run=True)
        assert "hyundai__creta__2020__2026__il" in report["moved_to_manual_review"]

    def test_preserves_next_seed_id(self, tmp_path):
        canonical = _make_legacy_canonical()
        p = tmp_path / "canonical.json"
        p.write_text(json.dumps(canonical), encoding="utf-8")

        from tools.migrate_legacy_state import migrate
        report = migrate(canonical_path=str(p), dry_run=True)
        assert report["next_seed_id"] == "volkswagen__jetta__1990__2026__il"

    def test_does_not_delete_variants(self, tmp_path):
        canonical = _make_legacy_canonical()
        pre_count = len(get_all_variants(canonical))
        p = tmp_path / "canonical.json"
        p.write_text(json.dumps(canonical), encoding="utf-8")

        from tools.migrate_legacy_state import migrate
        report = migrate(canonical_path=str(p), dry_run=True)
        assert report["post_variants"] >= pre_count
