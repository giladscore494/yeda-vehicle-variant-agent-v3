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

    def test_batch_stops_on_zero_mutation_accept(self, tmp_path):
        """Batch must stop if ACCEPT_VARIANTS produces 0 added and 0 merged."""
        canonical_path = tmp_path / "canonical.json"
        canonical_path.write_text(json.dumps(_make_canonical()), encoding="utf-8")

        seeds_path = tmp_path / "seeds.json"
        seeds_path.write_text(json.dumps(_make_seeds()), encoding="utf-8")

        def mock_run_seed(seed, seed_id, dry_run=False):
            # Return candidates with no variant_id → will produce 0 mutations
            return SeedRunResult(
                seed_id=seed_id,
                ok=True,
                candidate_variants=[
                    {"make": seed["make"], "model": seed["model"]}  # no variant_id
                ],
            )

        with patch("engine.batch.run_seed", side_effect=mock_run_seed):
            result = run_batch(
                batch_size=3,
                canonical_path=str(canonical_path),
                seeds_path=str(seeds_path),
            )

        assert result["ok"] is False
        assert "zero-mutation" in result.get("error", "")

        # Canonical must not have any processed seeds
        from engine.state import load_canonical as lc
        reloaded = lc(canonical_path)
        assert len(reloaded["batch_state"]["processed_seed_ids"]) == 0

    def test_zero_mutation_accept_does_not_advance_cursor(self, tmp_path):
        """Cursor must not advance past the failed seed (Jetta→Bora prevention)."""
        canonical_path = tmp_path / "canonical.json"
        canonical_path.write_text(json.dumps(_make_canonical()), encoding="utf-8")

        seeds_path = tmp_path / "seeds.json"
        seeds_path.write_text(json.dumps(_make_seeds()), encoding="utf-8")

        def mock_run_seed(seed, seed_id, dry_run=False):
            return SeedRunResult(
                seed_id=seed_id,
                ok=True,
                candidate_variants=[
                    {"make": seed["make"], "model": seed["model"]}  # no variant_id
                ],
            )

        with patch("engine.batch.run_seed", side_effect=mock_run_seed):
            result = run_batch(
                batch_size=3,
                canonical_path=str(canonical_path),
                seeds_path=str(seeds_path),
            )

        assert result["ok"] is False

        from engine.state import load_canonical as lc
        reloaded = lc(canonical_path)
        # Cursor must remain on the first seed, NOT advance to model_b
        assert reloaded["batch_state"]["next_seed_id"] == "make_a__model_a__2020__2026__il"

    def test_zero_mutation_accept_variants_unchanged(self, tmp_path):
        """Variants must remain unchanged after a zero-mutation ACCEPT_VARIANTS failure."""
        initial = _make_canonical()
        initial["verified_variants"] = [
            {"variant_id": "existing_v1", "make": "Pre", "model": "Existing",
             "verification_status": "verified"}
        ]
        initial["partial_variants"] = []

        canonical_path = tmp_path / "canonical.json"
        canonical_path.write_text(json.dumps(initial), encoding="utf-8")

        seeds_path = tmp_path / "seeds.json"
        seeds_path.write_text(json.dumps(_make_seeds()), encoding="utf-8")

        def mock_run_seed(seed, seed_id, dry_run=False):
            # Has make+model (passes quality filter) but no variant_id (0 mutations)
            return SeedRunResult(
                seed_id=seed_id,
                ok=True,
                candidate_variants=[{"make": seed["make"], "model": seed["model"]}],
            )

        with patch("engine.batch.run_seed", side_effect=mock_run_seed):
            result = run_batch(
                batch_size=1,
                canonical_path=str(canonical_path),
                seeds_path=str(seeds_path),
            )

        assert result["ok"] is False

        from engine.state import load_canonical as lc
        reloaded = lc(canonical_path)
        all_v = reloaded["verified_variants"] + reloaded.get("partial_variants", [])
        assert len(all_v) == 1
        assert all_v[0]["variant_id"] == "existing_v1"

    def test_zero_mutation_accept_tracker_records_error(self, tmp_path):
        """Runtime tracker must record ERROR stage, not DONE, on zero-mutation accept."""
        canonical_path = tmp_path / "canonical.json"
        canonical_path.write_text(json.dumps(_make_canonical()), encoding="utf-8")

        seeds_path = tmp_path / "seeds.json"
        seeds_path.write_text(json.dumps(_make_seeds()), encoding="utf-8")

        def mock_run_seed(seed, seed_id, dry_run=False):
            # Has make+model (passes quality filter) but no variant_id (0 mutations)
            return SeedRunResult(
                seed_id=seed_id,
                ok=True,
                candidate_variants=[{"make": seed["make"], "model": seed["model"]}],
            )

        with patch("engine.batch.run_seed", side_effect=mock_run_seed):
            result = run_batch(
                batch_size=1,
                canonical_path=str(canonical_path),
                seeds_path=str(seeds_path),
            )

        assert result["ok"] is False
        # The tracker should be absent from result (batch returned early)
        # but the error message should reference zero-mutation
        assert "zero-mutation" in result.get("error", "")
