from __future__ import annotations

import hashlib
import json
from pathlib import Path

from core.paths import DECISIONS_PATH, FINAL_CLEAN_DATABASE_PATH, SOURCE_CANONICAL_PATH
from engine.validation import final_quality_audit as audit_module


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _source_payload() -> dict:
    return {
        "verified_variants": [
            {"variant_id": "v1", "make": "Toyota", "model": "Corolla", "year_start": 2020, "year_end": 2021},
            {"variant_id": "v2", "make": "Toyota", "model": "Yaris", "year_start": 2021, "year_end": 2022},
        ],
        "partial_variants": [],
    }


def _final_payload(ids: list[str]) -> dict:
    return {
        "metadata": {"manual_review_remaining_count": 0, "rejected_count": 0, "normalized_count": 0},
        "vehicles": [
            {"variant_id": vid, "make": "Toyota", "model": "Model", "year_start": 2020, "year_end": 2021}
            for vid in ids
        ],
    }


def test_quality_audit_fails_if_final_file_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, _source_payload())
    result = audit_module.audit_final_clean_database_quality()
    assert result["status"] == "FAIL"
    assert any("Final clean database is missing" in reason for reason in result["blocking_reasons"])


def test_quality_audit_fails_on_variant_loss_without_approved_reject(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, _source_payload())
    _write_json(tmp_path / FINAL_CLEAN_DATABASE_PATH, _final_payload(["v1"]))
    _write_json(
        tmp_path / DECISIONS_PATH,
        {"decisions": [{"action": "reject", "variant_id": "v2", "safe_to_auto_apply": False}]},
    )

    result = audit_module.audit_final_clean_database_quality()

    assert result["status"] == "FAIL"
    assert any("Output variant count is lower than source" in reason for reason in result["blocking_reasons"])


def test_quality_audit_returns_structured_output(monkeypatch):
    monkeypatch.setattr(audit_module, "_deterministic_checks", lambda: ({"total_input_variants": 2}, [], []))
    monkeypatch.setattr(
        audit_module,
        "_call_openai_audit_model",
        lambda model, summary: (
            {
                "status": "PASS",
                "confidence": 0.9,
                "blocking_reasons": [],
                "non_blocking_warnings": [],
                "required_fixes": [],
                "summary": "ok",
            },
            None,
        ),
    )
    monkeypatch.setattr(audit_module.config, "get", lambda *args, **kwargs: "gpt-5.4")
    result = audit_module.audit_final_clean_database_quality()
    assert set(result.keys()) >= {
        "status",
        "confidence",
        "blocking_reasons",
        "non_blocking_warnings",
        "required_fixes",
        "summary",
        "deterministic_summary",
        "model",
    }
    assert "commit_sha" not in result


def test_quality_audit_does_not_mutate_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, _source_payload())
    _write_json(tmp_path / FINAL_CLEAN_DATABASE_PATH, _final_payload(["v1", "v2"]))
    _write_json(tmp_path / DECISIONS_PATH, {"decisions": []})

    source_before = hashlib.sha256((tmp_path / SOURCE_CANONICAL_PATH).read_bytes()).hexdigest()
    final_before = hashlib.sha256((tmp_path / FINAL_CLEAN_DATABASE_PATH).read_bytes()).hexdigest()

    monkeypatch.setattr(
        audit_module,
        "_call_openai_audit_model",
        lambda model, summary: (
            {
                "status": "PASS",
                "confidence": 0.8,
                "blocking_reasons": [],
                "non_blocking_warnings": [],
                "required_fixes": [],
                "summary": "ok",
            },
            None,
        ),
    )
    monkeypatch.setattr(audit_module.config, "get", lambda *args, **kwargs: "gpt-5.4")
    _ = audit_module.audit_final_clean_database_quality()

    source_after = hashlib.sha256((tmp_path / SOURCE_CANONICAL_PATH).read_bytes()).hexdigest()
    final_after = hashlib.sha256((tmp_path / FINAL_CLEAN_DATABASE_PATH).read_bytes()).hexdigest()
    assert source_before == source_after
    assert final_before == final_after
