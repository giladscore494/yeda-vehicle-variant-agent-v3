import json
import os
from pathlib import Path

from core.paths import (
    DECISIONS_PATH,
    DIFF_AUDITS_PATH,
    FINAL_CLEAN_DATABASE_PATH,
    ISSUE_QUEUE_PATH,
    MANIFEST_PATH,
    MODEL_REVIEW_PROGRESS_PATH,
    PATCH_APPLICATIONS_PATH,
    PATCHES_PATH,
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


def test_load_surgical_patch_summary_helper_exists():
    assert hasattr(helpers, "load_surgical_patch_summary")


def test_load_ai_review_outcome_helper_exists():
    assert hasattr(helpers, "load_ai_review_outcome")


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


def test_surgical_patch_summary_and_wrappers(monkeypatch, tmp_path):
    expected_build = {"created_count": 1, "pending": 1}
    expected_apply = {"status": "applied_pending_audit", "patch_id": "p1"}
    expected_audit = {"status": "PASS", "patch_id": "p1"}
    monkeypatch.setattr(helpers, "_build_candidate_patches_from_decisions", lambda: expected_build)
    monkeypatch.setattr(helpers, "_apply_next_safe_patch", lambda: expected_apply)
    monkeypatch.setattr(helpers, "_audit_last_patch_diff_with_openai", lambda: expected_audit)
    assert helpers.build_candidate_patches() == expected_build
    assert helpers.apply_next_safe_surgical_patch() == expected_apply
    assert helpers.apply_next_safe_patch() == expected_apply
    assert helpers.audit_last_surgical_patch_diff() == expected_audit
    assert helpers.audit_last_patch_diff_with_openai() == expected_audit


def test_load_surgical_patch_summary_missing_files_returns_safe_defaults(tmp_path):
    summary = helpers.load_surgical_patch_summary(project_root=tmp_path)

    expected_keys = {
        "patches_path",
        "patches_exists",
        "patches_total",
        "pending",
        "applied_pending_audit",
        "audit_passed",
        "audit_failed",
        "blocked",
        "last_patch_id",
        "last_variant_ids",
        "last_changed_fields",
        "last_audit_status",
        "last_error",
        "change_required",
        "no_change_required",
        "patchable",
        "change_required_not_patchable",
        "manual_review_required",
    }
    assert expected_keys.issubset(summary.keys())
    assert summary["patches_path"] == PATCHES_PATH
    assert summary["patches_exists"] is False
    assert summary["patches_total"] == 0
    assert summary["pending"] == 0
    assert summary["applied_pending_audit"] == 0
    assert summary["audit_passed"] == 0
    assert summary["audit_failed"] == 0
    assert summary["blocked"] == 0
    assert summary["last_patch_id"] is None
    assert summary["last_variant_ids"] == []
    assert summary["last_changed_fields"] == {}
    assert summary["last_audit_status"] is None
    assert summary["last_error"] is None
    assert summary["change_required"] == 0
    assert summary["no_change_required"] == 0
    assert summary["patchable"] == 0
    assert summary["change_required_not_patchable"] == 0
    assert summary["manual_review_required"] == 0


def test_load_surgical_patch_summary_handles_malformed_patches_json(tmp_path):
    path = tmp_path / PATCHES_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{bad-json", encoding="utf-8")

    summary = helpers.load_surgical_patch_summary(project_root=tmp_path)

    assert summary["patches_exists"] is True
    assert summary["patches_total"] == 0
    assert summary["pending"] == 0
    assert summary["applied_pending_audit"] == 0
    assert summary["audit_passed"] == 0
    assert summary["audit_failed"] == 0
    assert summary["blocked"] == 0
    assert isinstance(summary["last_error"], str)
    assert summary["last_error"]


def test_load_surgical_patch_summary_counts_and_last_values(tmp_path):
    _write_json(
        tmp_path / PATCHES_PATH,
        {
            "change_required": 2,
            "no_change_required": 1,
            "patchable": 1,
            "change_required_not_patchable": 1,
            "manual_review_required": 0,
            "patches": [
                {"patch_id": "p1", "status": "pending"},
                {"patch_id": "p2", "status": "applied_pending_audit"},
                {"patch_id": "p3", "status": "audit_passed"},
                {"patch_id": "p4", "status": "audit_failed"},
                {"patch_id": "p5", "status": "blocked"},
            ]
        },
    )
    apps = tmp_path / PATCH_APPLICATIONS_PATH
    apps.parent.mkdir(parents=True, exist_ok=True)
    apps.write_text(
        json.dumps({"patch_id": "p2", "variant_ids": ["v_2"], "changed_fields": {"v_2": ["model"]}}, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    audits = tmp_path / DIFF_AUDITS_PATH
    audits.parent.mkdir(parents=True, exist_ok=True)
    audits.write_text(
        json.dumps({"patch_id": "p2", "variant_ids": ["v_2"], "status": "PASS"}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    summary = helpers.load_surgical_patch_summary(project_root=tmp_path)

    assert summary["patches_exists"] is True
    assert summary["patches_total"] == 5
    assert summary["pending"] == 1
    assert summary["applied_pending_audit"] == 1
    assert summary["audit_passed"] == 1
    assert summary["audit_failed"] == 1
    assert summary["blocked"] == 1
    assert summary["change_required"] == 2
    assert summary["no_change_required"] == 1
    assert summary["patchable"] == 1
    assert summary["change_required_not_patchable"] == 1
    assert summary["manual_review_required"] == 0
    assert summary["last_patch_id"] == "p2"
    assert summary["last_variant_ids"] == ["v_2"]
    assert summary["last_changed_fields"] == {"v_2": ["model"]}
    assert summary["last_audit_status"] == "PASS"
    assert summary["last_error"] is None


def test_streamlit_app_has_surgical_patch_workflow_section():
    app_source = Path("app.py").read_text(encoding="utf-8")
    assert "Surgical Patch Workflow" in app_source
    assert "Build Candidate Patches" in app_source
    assert "Apply Next Safe Patch" in app_source
    assert "Audit Last Patch Diff with GPT-5.4" in app_source
    assert "AI Review outcome" in app_source
    assert "CHANGE_REQUIRED" in app_source
    assert "NO_CHANGE_REQUIRED" in app_source
    assert "Advanced Debug / Raw Files" in app_source
    assert "Apply Surgical Patch" not in app_source


def test_load_ai_review_outcome_counts(tmp_path):
    _write_json(
        tmp_path / ISSUE_QUEUE_PATH,
        {"items": [_queue_item(1, ["v1"]), _queue_item(2, ["v2"])]},
    )
    _write_json(
        tmp_path / MODEL_REVIEW_PROGRESS_PATH,
        {
            "items": {
                "iq_000001": {"item_id": "iq_000001", "status": "completed"},
                "iq_000002": {"item_id": "iq_000002", "status": "completed"},
            }
        },
    )
    _write_json(
        tmp_path / DECISIONS_PATH,
        {
            "decisions": [
                {
                    "item_id": "iq_000001",
                    "change_decision": "CHANGE_REQUIRED",
                    "change_severity": "material",
                    "patchable": False,
                    "patchability_reason": "no_exact_field_changes",
                    "change_reason": "year mismatch",
                },
                {
                    "item_id": "iq_000002",
                    "change_decision": "NO_CHANGE_REQUIRED",
                    "change_severity": "negligible",
                    "patchable": False,
                    "patchability_reason": "no_change_needed",
                    "change_reason": "cosmetic only",
                },
            ]
        },
    )
    _write_json(tmp_path / PATCHES_PATH, {"pending": 3, "patches": []})
    payload = helpers.load_ai_review_outcome(project_root=tmp_path)
    assert payload["completed_ai_decisions"] == 2
    assert payload["change_required"] == 1
    assert payload["no_change_required"] == 1
    assert payload["patchable_changes"] == 0
    assert payload["non_patchable_changes"] == 1
    assert payload["pending_patches"] == 3


def test_load_ai_review_outcome_missing_decisions_file_returns_safe_defaults(tmp_path):
    payload = helpers.load_ai_review_outcome(project_root=tmp_path)
    assert payload["decisions_exists"] is False
    assert payload["decisions_total"] == 0
    assert payload["completed_decisions"] == 0
    assert payload["change_required"] == 0
    assert payload["no_change_required"] == 0
    assert payload["patchable"] == 0
    assert payload["change_required_not_patchable"] == 0
    assert payload["manual_review_required"] == 0
    assert payload["missing_change_decision"] == 0
    assert payload["latest_decision_id"] is None
    assert payload["latest_item_id"] is None
    assert payload["latest_change_decision"] is None
    assert payload["latest_change_severity"] is None
    assert payload["latest_patchable"] is None
    assert payload["latest_patchability_reason"] is None
    assert payload["latest_change_reason"] is None
    assert payload["last_error"] is None


def test_load_ai_review_outcome_empty_decisions_list_returns_safe_defaults(tmp_path):
    _write_json(tmp_path / DECISIONS_PATH, {"decisions": []})
    payload = helpers.load_ai_review_outcome(project_root=tmp_path)
    assert payload["decisions_exists"] is True
    assert payload["decisions_total"] == 0
    assert payload["completed_decisions"] == 0
    assert payload["change_required"] == 0
    assert payload["no_change_required"] == 0
    assert payload["patchable"] == 0
    assert payload["change_required_not_patchable"] == 0
    assert payload["manual_review_required"] == 0
    assert payload["missing_change_decision"] == 0


def test_load_ai_review_outcome_old_decision_without_change_decision_counts_missing(tmp_path):
    _write_json(
        tmp_path / DECISIONS_PATH,
        {
            "decisions": [
                {
                    "item_id": "iq_000001",
                    "change_reason": "legacy payload",
                }
            ]
        },
    )
    payload = helpers.load_ai_review_outcome(project_root=tmp_path)
    assert payload["decisions_total"] == 1
    assert payload["missing_change_decision"] == 1
    assert payload["manual_review_required"] == 1
    assert payload["change_required"] == 0
    assert payload["no_change_required"] == 0


def test_load_ai_review_outcome_binary_decision_and_patchability_counts(tmp_path):
    _write_json(
        tmp_path / DECISIONS_PATH,
        {
            "decisions": [
                {"item_id": "iq_000001", "change_decision": "CHANGE_REQUIRED", "patchable": True},
                {"item_id": "iq_000002", "change_decision": "CHANGE_REQUIRED", "patchable": False},
                {"item_id": "iq_000003", "change_decision": "NO_CHANGE_REQUIRED", "patchable": False},
            ]
        },
    )
    payload = helpers.load_ai_review_outcome(project_root=tmp_path)
    assert payload["change_required"] == 2
    assert payload["no_change_required"] == 1
    assert payload["patchable"] == 1
    assert payload["change_required_not_patchable"] == 1
    assert payload["missing_change_decision"] == 0


def test_load_ai_review_outcome_malformed_decisions_json_sets_last_error(tmp_path):
    path = tmp_path / DECISIONS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{bad-json", encoding="utf-8")
    payload = helpers.load_ai_review_outcome(project_root=tmp_path)
    assert payload["decisions_exists"] is True
    assert payload["decisions_total"] == 0
    assert isinstance(payload["last_error"], str)
    assert payload["last_error"]


def test_load_ai_review_outcome_contains_all_app_facing_and_stable_keys(tmp_path):
    _write_json(tmp_path / DECISIONS_PATH, {"decisions": []})
    payload = helpers.load_ai_review_outcome(project_root=tmp_path)
    expected = {
        "decisions_path",
        "decisions_exists",
        "decisions_total",
        "completed_decisions",
        "change_required",
        "no_change_required",
        "patchable",
        "change_required_not_patchable",
        "manual_review_required",
        "missing_change_decision",
        "latest_decision_id",
        "latest_item_id",
        "latest_change_decision",
        "latest_change_severity",
        "latest_patchable",
        "latest_patchability_reason",
        "latest_change_reason",
        "last_error",
        "completed_ai_decisions",
        "patchable_changes",
        "non_patchable_changes",
        "pending_patches",
        "rows",
        "columns",
    }
    assert expected.issubset(payload.keys())
