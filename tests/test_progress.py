"""Tests for engine/progress.py."""
import json
from pathlib import Path

from engine.progress import ProgressTracker, generate_run_id, generate_seed_run_id, STAGES


class TestProgress:
    def test_run_id_format(self):
        rid = generate_run_id()
        assert rid.startswith("run_")

    def test_seed_run_id_format(self):
        srid = generate_seed_run_id("run_2026_05_22_143000", 7, "volkswagen__jetta__1990__2026__il")
        assert "007" in srid
        assert "volkswagen__jetta" in srid

    def test_tracker_records_state(self, tmp_path):
        state_path = tmp_path / "current_run.json"
        tracker = ProgressTracker(
            run_id="test_run",
            batch_size=3,
            state_path=str(state_path),
        )
        tracker.set_seed("seed_1", 0)
        tracker.set_stage("LLM_DISCOVERY")

        data = json.loads(state_path.read_text())
        assert data["run_id"] == "test_run"
        assert data["current_seed_id"] == "seed_1"
        assert data["current_stage"] == "LLM_DISCOVERY"

    def test_stages_update_order(self, tmp_path):
        state_path = tmp_path / "current_run.json"
        tracker = ProgressTracker(run_id="test", state_path=str(state_path))
        tracker.set_seed("s1", 0)

        stages_seen = []
        for stage in ["LOADING_SEED", "BUILDING_PROMPT", "LLM_DISCOVERY", "DECISION", "DONE"]:
            tracker.set_stage(stage)
            stages_seen.append(stage)

        data = json.loads(state_path.read_text())
        assert data["current_stage"] == "DONE"

    def test_progress_does_not_mutate_canonical(self, tmp_path):
        """Progress tracker never touches canonical data."""
        state_path = tmp_path / "current_run.json"
        tracker = ProgressTracker(run_id="test", state_path=str(state_path))
        d = tracker.to_dict()
        # Should not have any canonical keys
        assert "verified_variants" not in d
        assert "batch_state" not in d

    def test_completed_tracking(self, tmp_path):
        state_path = tmp_path / "current_run.json"
        tracker = ProgressTracker(run_id="test", state_path=str(state_path))
        tracker.mark_completed("s1", "ACCEPT_VARIANTS", added=3, merged=1)
        assert len(tracker.completed_seeds) == 1
        assert tracker.completed_seeds[0]["added_count"] == 3

    def test_all_stages_valid(self):
        assert "QUEUED" in STAGES
        assert "DONE" in STAGES
        assert "ERROR" in STAGES
        assert len(STAGES) == 17
