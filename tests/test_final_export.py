from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from core.paths import ACTIVE_WORKING_DATABASE_PATH, FINAL_CLEAN_DATABASE_PATH, SOURCE_CANONICAL_PATH
from engine.validation.final_export import export_final_clean_database


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _package(variant_id="v1") -> dict:
    return {
        "verified_variants": [
            {"variant_id": variant_id, "make": "Toyota", "model": "Corolla", "year_start": 2020, "year_end": 2021}
        ],
        "partial_variants": [],
    }


def test_export_reads_working_copy_and_metadata(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    canonical = _package("canonical")
    working = _package("working")
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, canonical)
    _write_json(tmp_path / ACTIVE_WORKING_DATABASE_PATH, working)

    summary = export_final_clean_database()
    payload = _load(tmp_path / FINAL_CLEAN_DATABASE_PATH)

    assert summary["source_file"] == ACTIVE_WORKING_DATABASE_PATH
    assert payload["metadata"]["golden_source_file"] == SOURCE_CANONICAL_PATH
    assert payload["metadata"]["active_source_file"] == ACTIVE_WORKING_DATABASE_PATH
    assert payload["metadata"]["working_copy_used"] is True
    assert payload["metadata"]["golden_source_hash"]
    assert payload["metadata"]["active_source_hash"]
    assert payload["metadata"]["total_input_variants"] == 1
    assert payload["metadata"]["total_output_variants"] == 1
    assert payload["metadata"]["variant_count_delta"] == 0
    assert payload["vehicles"] == working["verified_variants"]


def test_export_refuses_if_working_copy_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, _package("canonical"))

    with pytest.raises(FileNotFoundError, match="Initialize Working Copy first"):
        export_final_clean_database()

    assert not (tmp_path / FINAL_CLEAN_DATABASE_PATH).exists()


def test_export_does_not_mutate_working_or_canonical(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    canonical = _package("canonical")
    working = _package("working")
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, canonical)
    _write_json(tmp_path / ACTIVE_WORKING_DATABASE_PATH, working)
    canonical_before = copy.deepcopy(canonical)
    working_before = copy.deepcopy(working)
    canonical_hash = hashlib.sha256((tmp_path / SOURCE_CANONICAL_PATH).read_bytes()).hexdigest()
    working_hash = hashlib.sha256((tmp_path / ACTIVE_WORKING_DATABASE_PATH).read_bytes()).hexdigest()

    export_final_clean_database()

    assert _load(tmp_path / SOURCE_CANONICAL_PATH) == canonical_before
    assert _load(tmp_path / ACTIVE_WORKING_DATABASE_PATH) == working_before
    assert hashlib.sha256((tmp_path / SOURCE_CANONICAL_PATH).read_bytes()).hexdigest() == canonical_hash
    assert hashlib.sha256((tmp_path / ACTIVE_WORKING_DATABASE_PATH).read_bytes()).hexdigest() == working_hash
