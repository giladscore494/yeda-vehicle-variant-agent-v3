"""Tests for engine/batch.py — autosave behavior."""
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from engine.types import SeedRunResult
from engine.batch import run_batch


def _make_canonical():
    return {
        "verified_variants": [],
        "partial_variants": [],
        "batch_state": {
            "processed_seed_ids": [],
            "manual_review_seed_ids": [],
            "failed_seed_ids": [],
            "seed_accounting": {},
            "next_seed_id": "make_a__model_a__2020__2026__il",
        },
        "counts": {},
    }


def _make_seeds():
    return [
        {"make": "Make_A", "model": "Model_A", "year_start": 2020, "year_end": 2026, "market": "IL"},
        {"make": "Make_B", "model": "Model_B", "year_start": 2020, "year_end": 2026, "market": "IL"},
        {"make": "Make_C", "model": "Model_C", "year_start": 2020, "year_end": 2026, "market": "IL"},
    ]


class TestBatchAutosave:
    def test_seeds_saved_before_failure(self, tmp_path):
        """In a batch of 3, seeds 1 and 2 save before seed 3 fails."""
        canonical_path = tmp_path / "canonical.json"
        canonical_path.write_text(json.dumps(_make_canonical()), encoding="utf-8")

        seeds_path = tmp_path / "seeds.json"
        seeds_path.write_text(json.dumps(_make_seeds()), encoding="utf-8")

        call_count = 0

        def mock_run_seed(seed, seed_id, dry_run=False):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                return SeedRunResult(
                    seed_id=seed_id,
                    ok=True,
                    candidate_variants=[
                        {"variant_id": f"v_{call_count}", "make": seed["make"], "model": seed["model"]}
                    ],
                )
            else:
                return SeedRunResult(
                    seed_id=seed_id,
                    ok=False,
                    errors=["simulated failure"],
                )

        with patch("engine.batch.run_seed", side_effect=mock_run_seed):
            result = run_batch(
                batch_size=3,
                canonical_path=str(canonical_path),
                seeds_path=str(seeds_path),
            )

        # Batch should have failed
        assert result["ok"] is False

        # But canonical should still be valid with seeds 1-2 saved
        from engine.state import load_canonical
        reloaded = load_canonical(canonical_path)
        processed = reloaded["batch_state"]["processed_seed_ids"]
        assert len(processed) >= 2

    def test_failure_stops_batch(self, tmp_path):
        """Failure at any seed stops the entire batch."""
        canonical_path = tmp_path / "canonical.json"
        canonical_path.write_text(json.dumps(_make_canonical()), encoding="utf-8")

        seeds_path = tmp_path / "seeds.json"
        seeds_path.write_text(json.dumps(_make_seeds()), encoding="utf-8")

        def mock_run_seed(seed, seed_id, dry_run=False):
            return SeedRunResult(
                seed_id=seed_id,
                ok=False,
                errors=["API error"],
            )

        with patch("engine.batch.run_seed", side_effect=mock_run_seed):
            result = run_batch(
                batch_size=3,
                canonical_path=str(canonical_path),
                seeds_path=str(seeds_path),
            )

        assert result["ok"] is False

    def test_canonical_valid_after_reload(self, tmp_path):
        """After autosave, canonical can be loaded and is valid."""
        canonical_path = tmp_path / "canonical.json"
        canonical_path.write_text(json.dumps(_make_canonical()), encoding="utf-8")

        seeds_path = tmp_path / "seeds.json"
        seeds_path.write_text(json.dumps(_make_seeds()), encoding="utf-8")

        def mock_run_seed(seed, seed_id, dry_run=False):
            return SeedRunResult(
                seed_id=seed_id,
                ok=True,
                candidate_variants=[
                    {"variant_id": f"v_{seed_id}", "make": seed["make"], "model": seed["model"]}
                ],
            )

        with patch("engine.batch.run_seed", side_effect=mock_run_seed):
            result = run_batch(
                batch_size=2,
                canonical_path=str(canonical_path),
                seeds_path=str(seeds_path),
            )

        assert result["ok"] is True

        from engine.state import load_canonical
        from engine.audit import audit_canonical
        reloaded = load_canonical(canonical_path)
        ok, errs = audit_canonical(reloaded)
        assert ok is True
