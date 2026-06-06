import json
from pathlib import Path

from core.paths import (
    DECISIONS_PATH,
    FINAL_CLEAN_DATABASE_PATH,
    FINAL_DIR,
    ISSUE_QUEUE_PATH,
    MANIFEST_PATH,
    SOURCE_CANONICAL_PATH,
    STALE_ROOT_CANONICAL_PATH,
    VALIDATION_DIR,
    VALIDATION_REPORT_PATH,
)
from engine.validation.file_status import load_database_file_status


def _write_package(path: Path, verified_count: int, partial_count: int = 0) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "verified_variants": [
                    {"variant_id": f"verified_{idx}"} for idx in range(verified_count)
                ],
                "partial_variants": [
                    {"variant_id": f"partial_{idx}"} for idx in range(partial_count)
                ],
            }
        ),
        encoding="utf-8",
    )


def test_validation_path_constants_point_to_expected_files():
    assert SOURCE_CANONICAL_PATH == "data/canonical/resume_package_canonical.json"
    assert STALE_ROOT_CANONICAL_PATH == "resume_package_canonical.json"
    assert VALIDATION_DIR == "data/validation"
    assert ISSUE_QUEUE_PATH == "data/validation/issue_queue.json"
    assert DECISIONS_PATH == "data/validation/decisions.json"
    assert MANIFEST_PATH == "data/validation/manifest.json"
    assert VALIDATION_REPORT_PATH == "data/validation/validation_report.json"
    assert FINAL_DIR == "data/final"
    assert FINAL_CLEAN_DATABASE_PATH == "data/final/resume_package_final_clean.json"


def test_source_canonical_is_not_final_clean_file():
    assert SOURCE_CANONICAL_PATH != FINAL_CLEAN_DATABASE_PATH


def test_stale_root_detection_uses_temp_json_files(tmp_path):
    _write_package(tmp_path / SOURCE_CANONICAL_PATH, verified_count=3, partial_count=2)
    _write_package(tmp_path / STALE_ROOT_CANONICAL_PATH, verified_count=2)

    status = load_database_file_status(project_root=tmp_path)

    assert status["source_path"] == SOURCE_CANONICAL_PATH
    assert status["source_exists"] is True
    assert status["source_variant_count"] == 5
    assert status["source_verified_count"] == 3
    assert status["source_partial_count"] == 2
    assert status["stale_root_exists"] is True
    assert status["stale_root_variant_count"] == 2
    assert status["stale_root_is_stale"] is True


def test_final_output_status_path_and_counts(tmp_path):
    _write_package(tmp_path / SOURCE_CANONICAL_PATH, verified_count=1)
    _write_package(tmp_path / FINAL_CLEAN_DATABASE_PATH, verified_count=4, partial_count=1)

    status = load_database_file_status(project_root=tmp_path)

    assert status["final_path"] == "data/final/resume_package_final_clean.json"
    assert status["final_exists"] is True
    assert status["final_variant_count"] == 5
    assert status["final_is_older_than_source"] is False


def test_validation_package_writer_does_not_create_final_clean_database(tmp_path, monkeypatch):
    from engine.validation.validation_outputs import write_validated_package

    monkeypatch.chdir(tmp_path)
    (tmp_path / "data/seeds").mkdir(parents=True)
    (tmp_path / "data/seeds/vehicle_model_seeds_il.json").write_text("[]", encoding="utf-8")

    canonical = {
        "verified_variants": [{"variant_id": "v1", "seed_id": "seed_1"}],
        "partial_variants": [],
        "batch_state": {},
    }

    write_validated_package(
        canonical=canonical,
        deterministic_issues=[],
        partial_classifications=[],
        suspicious_groups=[],
        targeted_seed_result=None,
        validation_run_id="test_run",
    )

    assert not (tmp_path / FINAL_CLEAN_DATABASE_PATH).exists()
    assert (tmp_path / "data/validated_runs/resume_package_canonical_validated_v2.json").exists()


def test_final_clean_database_path_is_reserved_for_task_5_export_only():
    from engine.validation.write_guard import check_write_allowed, is_allowed_validation_write
    from engine.validation.write_guard import CanonicalWriteBlockedError

    assert is_allowed_validation_write(FINAL_CLEAN_DATABASE_PATH) is False
    try:
        check_write_allowed(FINAL_CLEAN_DATABASE_PATH)
    except CanonicalWriteBlockedError as exc:
        assert "Task 5 final export" in str(exc)
    else:
        raise AssertionError("FINAL_CLEAN_DATABASE_PATH should be blocked for validation writers")
