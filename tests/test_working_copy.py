import json
from pathlib import Path

from core.paths import ACTIVE_WORKING_DATABASE_PATH, SOURCE_CANONICAL_PATH
from engine.validation.working_copy import (
    get_active_database_path,
    initialize_working_copy,
    load_active_database,
    reset_working_copy_from_canonical,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def test_initialize_working_copy_creates_from_canonical(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = {"verified_variants": [{"variant_id": "v1"}], "partial_variants": []}
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, source)

    result = initialize_working_copy()

    assert result["ok"] is True
    assert result["status"] == "created"
    assert result["canonical_variant_count"] == 1
    assert result["working_variant_count"] == 1
    assert json.loads((tmp_path / ACTIVE_WORKING_DATABASE_PATH).read_text(encoding="utf-8")) == source
    assert get_active_database_path() == ACTIVE_WORKING_DATABASE_PATH
    assert load_active_database() == source


def test_initialize_working_copy_does_not_overwrite_existing_without_force(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, {"verified_variants": [{"variant_id": "canonical"}]})
    _write_json(tmp_path / ACTIVE_WORKING_DATABASE_PATH, {"verified_variants": [{"variant_id": "working"}]})

    result = initialize_working_copy()

    assert result["status"] == "already_exists"
    assert load_active_database()["verified_variants"][0]["variant_id"] == "working"


def test_reset_working_copy_requires_confirmation_and_backs_up(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = {"verified_variants": [{"variant_id": "canonical"}], "partial_variants": []}
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, source)
    _write_json(tmp_path / ACTIVE_WORKING_DATABASE_PATH, {"verified_variants": [{"variant_id": "working"}]})

    blocked = reset_working_copy_from_canonical(confirm=False)
    assert blocked["status"] == "blocked"
    assert load_active_database()["verified_variants"][0]["variant_id"] == "working"

    result = reset_working_copy_from_canonical(confirm=True)
    assert result["status"] == "reset"
    assert result["backup_path"]
    assert Path(result["backup_path"]).exists()
    assert load_active_database() == source
