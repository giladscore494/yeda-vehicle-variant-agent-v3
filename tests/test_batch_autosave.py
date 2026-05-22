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
        """Candidates missing variant_id fields → MANUAL_REVIEW, not zero-mutation crash."""
        canonical_path = tmp_path / "canonical.json"
        canonical_path.write_text(json.dumps(_make_canonical()), encoding="utf-8")

        seeds_path = tmp_path / "seeds.json"
        seeds_path.write_text(json.dumps(_make_seeds()), encoding="utf-8")

        def mock_run_seed(seed, seed_id, dry_run=False):
            # Return candidates with no variant_id and no year fields
            # → cannot generate variant_id → MANUAL_REVIEW
            return SeedRunResult(
                seed_id=seed_id,
                ok=True,
                candidate_variants=[
                    {"make": seed["make"], "model": seed["model"]}  # no variant_id, no years
                ],
            )

        with patch("engine.batch.run_seed", side_effect=mock_run_seed):
            result = run_batch(
                batch_size=3,
                canonical_path=str(canonical_path),
                seeds_path=str(seeds_path),
            )

        # Batch succeeds but seeds go to manual_review (not processed)
        assert result["ok"] is True

        from engine.state import load_canonical as lc
        reloaded = lc(canonical_path)
        assert len(reloaded["batch_state"]["processed_seed_ids"]) == 0
        assert len(reloaded["batch_state"]["manual_review_seed_ids"]) >= 1

    def test_zero_mutation_accept_does_not_advance_cursor(self, tmp_path):
        """Candidates without variant_id fields → MANUAL_REVIEW, cursor does not mark processed."""
        canonical_path = tmp_path / "canonical.json"
        canonical_path.write_text(json.dumps(_make_canonical()), encoding="utf-8")

        seeds_path = tmp_path / "seeds.json"
        seeds_path.write_text(json.dumps(_make_seeds()), encoding="utf-8")

        def mock_run_seed(seed, seed_id, dry_run=False):
            return SeedRunResult(
                seed_id=seed_id,
                ok=True,
                candidate_variants=[
                    {"make": seed["make"], "model": seed["model"]}  # no variant_id, no years
                ],
            )

        with patch("engine.batch.run_seed", side_effect=mock_run_seed):
            result = run_batch(
                batch_size=3,
                canonical_path=str(canonical_path),
                seeds_path=str(seeds_path),
            )

        assert result["ok"] is True

        from engine.state import load_canonical as lc
        reloaded = lc(canonical_path)
        # Seeds go to manual_review, not processed — cursor not advanced past them
        assert len(reloaded["batch_state"]["processed_seed_ids"]) == 0
        assert len(reloaded["batch_state"]["manual_review_seed_ids"]) >= 1

    def test_zero_mutation_accept_variants_unchanged(self, tmp_path):
        """Variants remain unchanged when candidates go to MANUAL_REVIEW."""
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
            # Has make+model (passes quality filter) but no year fields
            # → cannot generate variant_id → MANUAL_REVIEW
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

        assert result["ok"] is True

        from engine.state import load_canonical as lc
        reloaded = lc(canonical_path)
        all_v = reloaded["verified_variants"] + reloaded.get("partial_variants", [])
        assert len(all_v) == 1
        assert all_v[0]["variant_id"] == "existing_v1"

    def test_zero_mutation_accept_tracker_records_error(self, tmp_path):
        """Seeds with un-enrichable candidates go to manual_review in seed_accounting."""
        canonical_path = tmp_path / "canonical.json"
        canonical_path.write_text(json.dumps(_make_canonical()), encoding="utf-8")

        seeds_path = tmp_path / "seeds.json"
        seeds_path.write_text(json.dumps(_make_seeds()), encoding="utf-8")

        def mock_run_seed(seed, seed_id, dry_run=False):
            # Has make+model (passes quality filter) but no year fields
            # → cannot generate variant_id → MANUAL_REVIEW
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

        assert result["ok"] is True

        from engine.state import load_canonical as lc
        reloaded = lc(canonical_path)
        acct = reloaded["batch_state"]["seed_accounting"]
        first_seed_id = "make_a__model_a__2020__2026__il"
        assert first_seed_id in acct
        assert acct[first_seed_id]["status"] == "manual_review"
        assert acct[first_seed_id]["reason"] == "no_mergeable_candidates_after_variant_id_generation"
