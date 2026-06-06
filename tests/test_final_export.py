"""Tests for the Task 5 final clean database export."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from core.paths import (
    DECISIONS_PATH,
    FINAL_CLEAN_DATABASE_PATH,
    MANIFEST_PATH,
    SOURCE_CANONICAL_PATH,
)
from engine.validation.final_export import export_final_clean_database


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _source_package() -> dict:
    return {
        "schema_version": "test",
        "verified_variants": [
            {
                "variant_id": "variant_safe",
                "make": "Toyota",
                "model": "Corolla",
                "trim": {"value": "  gli   plus  ", "status": "verified"},
                "source_ids": ["src_1", "src_1", "src_2"],
                "verification_status": "verified",
            },
            {
                "variant_id": "variant_reject",
                "make": "Mazda",
                "model": "3",
                "trim": {"value": "Sport", "status": "verified"},
                "verification_status": "verified",
            },
        ],
        "partial_variants": [
            {
                "variant_id": "variant_model",
                "make": "Honda",
                "model": "Civic",
                "trim": {"value": " LX ", "status": "partial"},
                "verification_status": "partial",
            }
        ],
    }


def _prepare(tmp_path: Path, monkeypatch, decisions: list[dict], *, write_manifest: bool = True) -> dict:
    monkeypatch.chdir(tmp_path)
    source = _source_package()
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, source)
    _write_json(tmp_path / DECISIONS_PATH, {"decisions": decisions})
    if write_manifest:
        _write_json(tmp_path / MANIFEST_PATH, {"validation_run_id": "test_run"})
    return source


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_export_creates_final_clean_database_and_metadata(tmp_path, monkeypatch):
    source = _prepare(tmp_path, monkeypatch, [])

    summary = export_final_clean_database()

    final_path = tmp_path / FINAL_CLEAN_DATABASE_PATH
    assert final_path.exists()
    payload = _load(final_path)
    assert summary["path"] == FINAL_CLEAN_DATABASE_PATH
    assert payload["metadata"]["source_file"] == SOURCE_CANONICAL_PATH
    assert payload["metadata"]["decisions_file"] == DECISIONS_PATH
    assert payload["metadata"]["manifest_file"] == MANIFEST_PATH
    assert payload["metadata"]["total_input_variants"] == 3
    assert payload["metadata"]["total_output_variants"] == 3
    assert payload["metadata"]["safe_decisions_applied"] == 0
    assert payload["metadata"]["model_decisions_not_auto_applied"] == 0
    assert payload["metadata"]["manual_review_remaining_count"] == 0
    assert payload["metadata"]["rejected_count"] == 0
    assert payload["metadata"]["normalized_count"] == 0
    assert payload["vehicles"] == source["verified_variants"] + source["partial_variants"]


def test_export_writes_only_final_output_and_preserves_source(tmp_path, monkeypatch):
    source = _prepare(tmp_path, monkeypatch, [], write_manifest=False)
    original = copy.deepcopy(source)

    summary = export_final_clean_database()

    final_path = tmp_path / FINAL_CLEAN_DATABASE_PATH
    assert final_path.exists()
    assert not (tmp_path / MANIFEST_PATH).exists()
    assert _load(tmp_path / SOURCE_CANONICAL_PATH) == original

    payload = _load(final_path)
    assert summary["path"] == FINAL_CLEAN_DATABASE_PATH
    assert "metadata" in payload
    assert payload["metadata"]["source_file"] == SOURCE_CANONICAL_PATH
    assert payload["metadata"]["decisions_file"] == DECISIONS_PATH
    assert payload["metadata"]["manifest_file"] == MANIFEST_PATH
    assert payload["metadata"]["total_output_variants"] == 3


def test_export_does_not_overwrite_source_canonical(tmp_path, monkeypatch):
    source = _prepare(tmp_path, monkeypatch, [
        {
            "decision_id": "safe_trim",
            "source": "deterministic_audit",
            "action": "whitespace_normalization",
            "variant_id": "variant_safe",
            "field": "trim.value",
        }
    ])
    original = copy.deepcopy(source)

    export_final_clean_database()

    assert _load(tmp_path / SOURCE_CANONICAL_PATH) == original
    assert not (tmp_path / "resume_package_canonical.json").exists()


def test_safe_deterministic_normalization_can_apply(tmp_path, monkeypatch):
    _prepare(tmp_path, monkeypatch, [
        {
            "decision_id": "safe_trim",
            "source": "deterministic_audit",
            "action": "whitespace_normalization",
            "variant_id": "variant_safe",
            "field": "trim.value",
        },
        {
            "decision_id": "safe_sources",
            "source": "deterministic_audit",
            "action": "duplicate_source_id_removal",
            "variant_id": "variant_safe",
            "field": "source_ids",
        },
    ])

    summary = export_final_clean_database()
    payload = _load(tmp_path / FINAL_CLEAN_DATABASE_PATH)
    safe_variant = next(v for v in payload["vehicles"] if v["variant_id"] == "variant_safe")

    assert safe_variant["trim"]["value"] == "gli plus"
    assert safe_variant["source_ids"] == ["src_1", "src_2"]
    assert summary["safe_decisions_applied"] == 2
    assert summary["normalized_count"] == 2


def test_reject_decision_is_not_auto_applied(tmp_path, monkeypatch):
    _prepare(tmp_path, monkeypatch, [
        {
            "decision_id": "reject_1",
            "source": "deterministic_audit",
            "action": "reject",
            "variant_id": "variant_reject",
        }
    ])

    summary = export_final_clean_database()
    payload = _load(tmp_path / FINAL_CLEAN_DATABASE_PATH)

    assert any(v["variant_id"] == "variant_reject" for v in payload["vehicles"])
    assert summary["rejected_count"] == 1
    assert summary["manual_review_remaining_count"] == 1


def test_model_decision_with_safe_to_auto_apply_false_is_not_applied(tmp_path, monkeypatch):
    _prepare(tmp_path, monkeypatch, [
        {
            "decision_id": "model_1",
            "source": "model_review",
            "action": "whitespace_normalization",
            "variant_id": "variant_model",
            "field": "trim.value",
            "safe_to_auto_apply": False,
            "gemini_result": {"parsed_result": {"recommendation": "whitespace_normalization"}},
        }
    ])

    summary = export_final_clean_database()
    payload = _load(tmp_path / FINAL_CLEAN_DATABASE_PATH)
    model_variant = next(v for v in payload["vehicles"] if v["variant_id"] == "variant_model")

    assert model_variant["trim"]["value"] == " LX "
    assert summary["model_decisions_not_auto_applied"] == 1
    assert summary["manual_review_remaining_count"] == 1


def test_unsupported_decision_becomes_manual_review_remaining(tmp_path, monkeypatch):
    _prepare(tmp_path, monkeypatch, [
        {
            "decision_id": "unsupported_1",
            "source": "deterministic_audit",
            "action": "rewrite_engine_family",
            "variant_id": "variant_safe",
            "field": "engine.value",
        }
    ])

    summary = export_final_clean_database()

    assert summary["safe_decisions_applied"] == 0
    assert summary["manual_review_remaining_count"] == 1
