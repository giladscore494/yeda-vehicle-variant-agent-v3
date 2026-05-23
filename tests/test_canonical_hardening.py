"""Tests for canonical persistence/recovery hardening."""
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from engine.state import (
    CanonicalCorruptionError,
    load_canonical,
    load_canonical_with_recovery,
)
from engine.save import save_canonical_atomic


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


class TestCanonicalCorruptionError:
    def test_invalid_json_raises_corruption_error(self, tmp_path):
        p = tmp_path / "canonical.json"
        p.write_text("{bad json", encoding="utf-8")
        with pytest.raises(CanonicalCorruptionError) as exc_info:
            load_canonical(p)
        err = exc_info.value
        assert err.path == p
        assert err.size > 0
        assert err.line >= 1
        assert err.column >= 1
        assert "corrupted" in str(err).lower() or "restore" in str(err).lower()

    def test_invalid_json_does_not_raise_raw_json_error(self, tmp_path):
        p = tmp_path / "canonical.json"
        p.write_text("not json at all", encoding="utf-8")
        with pytest.raises(CanonicalCorruptionError):
            load_canonical(p)
        # Must NOT be raw JSONDecodeError
        try:
            load_canonical(p)
        except CanonicalCorruptionError:
            pass
        except json.JSONDecodeError:
            pytest.fail("Should not raise raw JSONDecodeError")

    def test_missing_file_still_raises_file_not_found(self, tmp_path):
        p = tmp_path / "missing.json"
        with pytest.raises(FileNotFoundError):
            load_canonical(p)

    def test_valid_file_loads_normally(self, tmp_path):
        p = tmp_path / "canonical.json"
        p.write_text(json.dumps(_make_valid_canonical()), encoding="utf-8")
        data = load_canonical(p)
        assert isinstance(data, dict)
        assert "verified_variants" in data


class TestLoadCanonicalWithRecovery:
    def test_valid_primary_returns_directly(self, tmp_path):
        p = tmp_path / "canonical.json"
        p.write_text(json.dumps(_make_valid_canonical()), encoding="utf-8")
        data = load_canonical_with_recovery(p)
        assert "_recovery" not in data
        assert "verified_variants" in data

    def test_corrupted_primary_restores_from_backup(self, tmp_path):
        p = tmp_path / "canonical.json"
        bp = tmp_path / "backup.json"
        p.write_text("{bad", encoding="utf-8")
        bp.write_text(json.dumps(_make_valid_canonical()), encoding="utf-8")

        data = load_canonical_with_recovery(p, backup_path=bp)
        assert "_recovery" in data
        assert data["_recovery"]["restored_from"] == str(bp)
        assert "verified_variants" in data

        # Primary should now be restored on disk
        reloaded = load_canonical(p)
        assert "verified_variants" in reloaded

    def test_corrupted_primary_no_backup_raises(self, tmp_path):
        p = tmp_path / "canonical.json"
        p.write_text("{bad", encoding="utf-8")
        with pytest.raises(CanonicalCorruptionError):
            load_canonical_with_recovery(p)

    def test_corrupted_primary_and_backup_raises(self, tmp_path):
        p = tmp_path / "canonical.json"
        bp = tmp_path / "backup.json"
        p.write_text("{bad", encoding="utf-8")
        bp.write_text("{also bad", encoding="utf-8")
        with pytest.raises(CanonicalCorruptionError):
            load_canonical_with_recovery(p, backup_path=bp)

    def test_corrupted_primary_missing_backup_raises(self, tmp_path):
        p = tmp_path / "canonical.json"
        bp = tmp_path / "nonexistent_backup.json"
        p.write_text("{bad", encoding="utf-8")
        with pytest.raises(CanonicalCorruptionError):
            load_canonical_with_recovery(p, backup_path=bp)


class TestSaveBackupProtection:
    def test_corrupted_canonical_does_not_overwrite_good_backup(self, tmp_path):
        p = tmp_path / "canonical.json"
        backup_p = tmp_path / "canonical_backup_previous.json"

        # Write a valid canonical and save once to create a good backup
        valid = _make_valid_canonical()
        save_canonical_atomic(valid, str(p))
        assert backup_p.exists() is False  # no backup on first save

        # Save again so backup is created
        save_canonical_atomic(valid, str(p))
        assert backup_p.exists()
        good_backup = backup_p.read_text(encoding="utf-8")

        # Now corrupt the canonical on disk
        p.write_text("{corrupted!", encoding="utf-8")

        # Save a new valid canonical — should NOT copy corrupted to backup
        result = save_canonical_atomic(_make_valid_canonical(), str(p))
        assert result["ok"] is True

        # Backup should still be the original good backup
        current_backup = backup_p.read_text(encoding="utf-8")
        assert json.loads(current_backup)  # still valid JSON
        assert current_backup == good_backup

    def test_save_fsync_path_still_passes(self, tmp_path):
        p = tmp_path / "canonical.json"
        result = save_canonical_atomic(_make_valid_canonical(), str(p))
        assert result["ok"] is True
        assert p.exists()

    def test_save_refuses_invalid_tmp(self, tmp_path):
        """Pre-save audit catches bad data before writing."""
        p = tmp_path / "canonical.json"
        bad = _make_valid_canonical()
        bad["batch_state"]["processed_seed_ids"] = [
            "bmw__3__2020__2026__il",
            "bmw__3__2020__2026__il",
        ]
        result = save_canonical_atomic(bad, str(p))
        assert result["ok"] is False


class TestPushUsesReloaded:
    def test_push_receives_reloaded_canonical(self, tmp_path):
        p = tmp_path / "canonical.json"
        canonical = _make_valid_canonical()

        mock_push = MagicMock(return_value={"ok": True})
        mock_module = MagicMock()
        mock_module.push_canonical = mock_push

        with patch.dict("sys.modules", {"storage.github_canonical_store": mock_module}):
            result = save_canonical_atomic(
                canonical, str(p), push_to_github=True,
            )

        assert mock_push.called
        pushed = mock_push.call_args[0][0]
        # The pushed canonical should have been reloaded from disk
        # (it will have "counts" added by _refresh_counts)
        assert "counts" in pushed


class TestAppRefusesCorruptedCanonical:
    def test_batch_refuses_corrupted_canonical(self, tmp_path):
        """run_batch raises CanonicalCorruptionError on corrupted canonical."""
        from engine.batch import run_batch

        p = tmp_path / "canonical.json"
        p.write_text("{bad json", encoding="utf-8")
        seeds_path = tmp_path / "seeds.json"
        seeds_path.write_text(json.dumps([]), encoding="utf-8")

        with pytest.raises(CanonicalCorruptionError):
            run_batch(
                batch_size=1,
                canonical_path=str(p),
                seeds_path=str(seeds_path),
            )
