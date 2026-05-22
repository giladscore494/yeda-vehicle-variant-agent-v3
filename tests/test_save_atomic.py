"""Tests for engine/save.py — atomic save."""
import json
import os
from pathlib import Path

import pytest
from engine.save import save_canonical_atomic
from engine.state import load_canonical


def _make_valid_canonical():
    return {
        "verified_variants": [
            {"variant_id": "v1", "make": "BMW", "model": "3", "verification_status": "verified"}
        ],
        "partial_variants": [],
        "batch_state": {
            "processed_seed_ids": ["bmw__3__2020__2026__il"],
            "manual_review_seed_ids": [],
            "failed_seed_ids": [],
            "last_completed_seed_id": "bmw__3__2020__2026__il",
            "seed_accounting": {
                "bmw__3__2020__2026__il": {
                    "status": "resolved",
                    "resolution_type": "variants_added",
                    "added_count": 1,
                }
            },
        },
    }


class TestAtomicSave:
    def test_save_writes_and_reloads(self, tmp_path):
        p = tmp_path / "canonical.json"
        canonical = _make_valid_canonical()
        result = save_canonical_atomic(canonical, str(p))
        assert result["ok"] is True
        reloaded = load_canonical(p)
        assert len(reloaded.get("verified_variants", [])) == 1

    def test_reload_after_save(self, tmp_path):
        p = tmp_path / "canonical.json"
        canonical = _make_valid_canonical()
        save_canonical_atomic(canonical, str(p))
        reloaded = load_canonical(p)
        assert reloaded["batch_state"]["processed_seed_ids"] == ["bmw__3__2020__2026__il"]

    def test_audit_failure_prevents_save(self, tmp_path):
        p = tmp_path / "canonical.json"
        # Write valid first
        valid = _make_valid_canonical()
        save_canonical_atomic(valid, str(p))

        # Try invalid
        bad = _make_valid_canonical()
        bad["batch_state"]["processed_seed_ids"] = ["bmw__3__2020__2026__il", "bmw__3__2020__2026__il"]
        result = save_canonical_atomic(bad, str(p))
        assert result["ok"] is False
        assert "audit" in result["error"].lower() or "duplicate" in result["error"].lower()

    def test_corrupted_tmp_does_not_replace(self, tmp_path):
        """Audit failure at pre-save prevents replacement."""
        p = tmp_path / "canonical.json"
        valid = _make_valid_canonical()
        save_canonical_atomic(valid, str(p))

        # Create canonical with duplicate in bucket (audit will fail)
        bad = _make_valid_canonical()
        bad["batch_state"]["processed_seed_ids"] = [
            "bmw__3__2020__2026__il",
            "bmw__3__2020__2026__il",
        ]
        result = save_canonical_atomic(bad, str(p))
        assert result["ok"] is False

        # Original should still be loadable and valid
        reloaded = load_canonical(p)
        assert len(reloaded.get("verified_variants", [])) == 1
