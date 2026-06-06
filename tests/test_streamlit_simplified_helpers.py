import json
import os
from pathlib import Path

from core.paths import (
    FINAL_CLEAN_DATABASE_PATH,
    ISSUE_QUEUE_PATH,
    MANIFEST_PATH,
    MODEL_REVIEW_PROGRESS_PATH,
    SOURCE_CANONICAL_PATH,
    VALIDATION_REPORT_PATH,
)
from engine.validation import streamlit_helpers as helpers


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _package(verified_count=2, partial_count=1):
    return {
        "verified_variants": [{"variant_id": f"v_{idx}"} for idx in range(verified_count)],
        "partial_variants": [{"variant_id": f"p_{idx}"} for idx in range(partial_count)],
    }


def _queue_item(idx: int, variant_ids=None):
    return {
        "item_id": f"iq_{idx:06d}",
        "make": "Toyota",
        "model": "Corolla",
        "year_start": 2020,
        "year_end": 2026,
        "issue_type": "evidence_gap",
        "risk_level": "high",
        "recommended_action": "manual_review",
        "requires_model_review": True,
        "variant_ids": variant_ids or [],
    }


def test_status_payload_has_required_fields(tmp_path):
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, _package(verified_count=3, partial_count=2))
    _write_json(
        tmp_path / VALIDATION_REPORT_PATH,
        {
            "issues_total": 7,
            "issues_by_risk": {"critical": 1, "high": 2, "medium": 3, "low": 1},
            "model_review_items_available": 4,
            "manual_review_items_available": 6,
        },
    )
    _write_json(tmp_path / MANIFEST_PATH, {"completed_at": "2026-06-06T00:00:00+00:00"})
    _write_json(tmp_path / helpers.SEEDS_PATH, [{"seed_id": "seed_1"}, {"seed_id": "seed_2"}])
    _write_json(
        tmp_path / ISSUE_QUEUE_PATH,
        {"items": [_queue_item(5, variant_ids=["v5"]), _queue_item(9, variant_ids=["v9"])]},
    )
    _write_json(
        tmp_path / MODEL_REVIEW_PROGRESS_PATH,
        {"items": {"iq_000002": {"item_id": "iq_000002", "status": "pending", "variant_ids": ["stale"]}}},
    )

    payload = helpers.load_status_payload(project_root=tmp_path)

    assert payload["final_banner"]["message"] == "No final clean database exported yet"
    assert payload["source"]["source_path"] == SOURCE_CANONICAL_PATH
    assert payload["source"]["source_variant_count"] == 5
    assert payload["source"]["source_verified_count"] == 3
    assert payload["source"]["source_partial_count"] == 2
    assert payload["source"]["seed_count"] == 2
    assert payload["validation_summary"] == {
        "issues_total": 7,
        "critical": 1,
        "high": 2,
        "medium": 3,
        "low": 1,
        "model_review_items_available": 4,
        "manual_review_items_available": 6,
        "last_run_time": "2026-06-06T00:00:00+00:00",
    }
    assert payload["model_review_progress"]["total_model_review_items"] == 2
    assert payload["model_review_progress"]["remaining_items"] == 2
    assert payload["model_review_progress"]["total_model_review_variants"] == 2
    assert payload["model_review_progress"]["remaining_variants"] == 2


def test_queue_preview_truncates_rows(tmp_path):
    _write_json(tmp_path / ISSUE_QUEUE_PATH, {"items": [_queue_item(idx) for idx in range(30)]})

    preview = helpers.load_queue_preview(project_root=tmp_path)

    assert preview["total_items"] == 30
    assert preview["max_rows"] == helpers.DEFAULT_QUEUE_PREVIEW_LIMIT
    assert len(preview["rows"]) == 25
    assert preview["columns"] == list(helpers.QUEUE_PREVIEW_COLUMNS)
    assert set(preview["rows"][0]) == set(helpers.QUEUE_PREVIEW_COLUMNS)


def test_ai_preview_truncates_rows(monkeypatch):
    def fake_run_model_review(**kwargs):
        assert kwargs["dry_run"] is True
        return {
            "selected_items": 15,
            "planned_gemini_calls": 15,
            "planned_openai_calls": 15,
            "planned_total_calls": 30,
            "estimated_cost_usd": 2.25,
            "items": [
                {
                    "item_id": f"iq_{idx:06d}",
                    "make": "Toyota",
                    "model": "Corolla",
                    "issue_type": "evidence_gap",
                    "risk_level": "high",
                    "routing_policy": "dual_provider",
                    "primary_provider": "gemini",
                    "second_opinion_provider": "openai",
                    "max_expected_calls": 2,
                    "extra_raw": "hidden",
                }
                for idx in range(15)
            ],
        }

    monkeypatch.setattr(helpers, "run_model_review", fake_run_model_review)

    preview = helpers.load_ai_preview(max_items=15, max_rows=helpers.DEFAULT_AI_PREVIEW_LIMIT)

    assert preview["selected_items"] == 15
    assert preview["planned_gemini_calls"] == 15
    assert preview["planned_openai_calls"] == 15
    assert preview["planned_total_calls"] == 30
    assert preview["estimated_cost_usd"] == 2.25
    assert len(preview["rows"]) == 10
    assert preview["columns"] == list(helpers.AI_PREVIEW_COLUMNS)
    assert set(preview["rows"][0]) == set(helpers.AI_PREVIEW_COLUMNS)


def test_final_banner_status_logic(tmp_path):
    source_path = tmp_path / SOURCE_CANONICAL_PATH
    final_path = tmp_path / FINAL_CLEAN_DATABASE_PATH
    _write_json(source_path, _package(verified_count=1, partial_count=0))

    missing = helpers.final_banner_status({"final_exists": False})
    assert missing["state"] == "missing"
    assert missing["message"] == "No final clean database exported yet"

    _write_json(final_path, _package(verified_count=1, partial_count=0))
    os.utime(final_path, (source_path.stat().st_mtime - 10, source_path.stat().st_mtime - 10))
    status = helpers.load_status_payload(project_root=tmp_path)
    assert status["final_banner"]["state"] == "stale"
    assert status["final_banner"]["message"] == "Final clean database is older than source canonical — re-export required"

    os.utime(final_path, (source_path.stat().st_mtime + 10, source_path.stat().st_mtime + 10))
    status = helpers.load_status_payload(project_root=tmp_path)
    assert status["final_banner"]["state"] == "exists"
    assert status["final_banner"]["message"] == f"Final clean database exists: {FINAL_CLEAN_DATABASE_PATH}"


def test_export_final_clean_database_helper_exists():
    assert hasattr(helpers, "export_final_clean_database")


def test_export_final_clean_database_returns_ui_safe_summary(monkeypatch):
    def fake_export():
        return {
            "output_path": "data/final/from_backend.json",
            "input_variant_count": 11,
            "output_variant_count": 9,
            "safe_decisions_applied": 7,
            "manual_review_remaining_count": 2,
            "metadata": {"created_at": "2026-06-06T12:34:56+00:00"},
        }

    monkeypatch.setattr(helpers, "_export_final_clean_database", fake_export)

    summary = helpers.export_final_clean_database()

    assert summary["final_path"] == "data/final/from_backend.json"
    assert summary["total_input_variants"] == 11
    assert summary["total_output_variants"] == 9
    assert summary["safe_decisions_applied"] == 7
    assert summary["manual_review_remaining_count"] == 2
    assert summary["created_at"] == "2026-06-06T12:34:56+00:00"
    assert summary["variant_count_delta"] == 0
    assert summary["blocked_variant_loss"] is False


def test_save_final_clean_database_to_github_wrapper(monkeypatch):
    expected = {"ok": True, "saved_path": "data/final/resume_package_final_clean.json"}
    monkeypatch.setattr(helpers, "_save_final_clean_database_to_github", lambda: expected)
    assert helpers.save_final_clean_database_to_github() == expected


def test_run_final_quality_audit_wrapper(monkeypatch):
    expected = {"status": "PASS", "confidence": 0.93}
    monkeypatch.setattr(helpers, "_audit_final_clean_database_quality", lambda: expected)
    assert helpers.run_final_quality_audit() == expected


def test_load_recent_run_events_wrapper(monkeypatch):
    monkeypatch.setattr(
        helpers,
        "load_recent_events",
        lambda limit: [
            {
                "time": "2026-06-06T00:00:00+00:00",
                "stage": "model_review",
                "provider": "openai",
                "model": "gpt-5.4",
                "item_id": "iq_1",
                "status": "ok",
                "summary": "done",
            }
        ],
    )
    payload = helpers.load_recent_run_events(max_rows=20)
    assert payload["max_rows"] == 20
    assert payload["events_path"] == "data/validation/run_events.jsonl"
    assert payload["columns"] == ["time", "stage", "provider", "model", "item_id", "status", "summary"]
    assert payload["rows"][0]["summary"] == "done"
