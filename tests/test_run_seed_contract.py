"""Tests for engine/run_seed.py — contract tests."""
from engine.types import SeedRunResult
from engine.run_seed import run_seed


class TestRunSeedContract:
    def test_dry_run_returns_seed_run_result(self):
        seed = {"make": "BMW", "model": "3 Series", "year_start": 2020, "year_end": 2026}
        result = run_seed(seed, "bmw__3_series__2020__2026__il", dry_run=True)
        assert isinstance(result, SeedRunResult)
        assert result.ok is True
        assert result.seed_id == "bmw__3_series__2020__2026__il"
        assert result.no_variants_reason == "dry_run"

    def test_missing_api_key_returns_error(self):
        """Without API key, run_seed should return FAIL_TRANSIENT-compatible result."""
        seed = {"make": "BMW", "model": "3 Series", "year_start": 2020, "year_end": 2026}
        result = run_seed(seed, "bmw__3_series__2020__2026__il", dry_run=False)
        assert isinstance(result, SeedRunResult)
        assert result.ok is False
        assert len(result.errors) > 0
