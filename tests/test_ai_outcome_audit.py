import json
from pathlib import Path

from core.paths import ACTIVE_WORKING_DATABASE_PATH, AI_OUTCOME_AUDITS_PATH, DECISIONS_PATH, SOURCE_CANONICAL_PATH
from engine.validation import ai_outcome_audit as outcome_audit


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_queue_completed_decisions_for_outcome_audit_sets_pending(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(
        tmp_path / DECISIONS_PATH,
        {
            "decisions": [
                {"decision_id": "d1", "item_id": "iq_000005"},
                {"decision_id": "d2", "item_id": "iq_000009", "outcome_audit_status": "passed"},
            ]
        },
    )

    result = outcome_audit.queue_completed_decisions_for_outcome_audit()
    payload = _read_json(tmp_path / DECISIONS_PATH)

    assert result["pending"] == 1
    assert result["passed"] == 1
    assert payload["decisions"][0]["outcome_audit_status"] == "pending"
    assert payload["decisions"][1]["outcome_audit_status"] == "passed"


def test_audit_next_ai_review_outcome_uses_compact_payload_and_updates_pass(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(
        tmp_path / DECISIONS_PATH,
        {
            "decisions": [
                {
                    "decision_id": "d1",
                    "item_id": "iq_000005",
                    "issue_type": "identity_mismatch",
                    "risk_level": "high",
                    "variant_ids": ["v1"],
                    "change_decision": "CHANGE_REQUIRED",
                    "patchable": False,
                    "patchability_reason": "no_exact_field_changes",
                    "outcome_audit_status": "pending",
                    "gemini_result": {"parsed_result": {"summary": "gemini-summary"}},
                    "openai_result": {"parsed_result": {"summary": "openai-summary"}},
                }
            ]
        },
    )
    _write_json(
        tmp_path / ACTIVE_WORKING_DATABASE_PATH,
        {"verified_variants": [{"variant_id": "v1", "model": "Corolla"}, {"variant_id": "v2", "model": "Yaris"}]},
    )
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, {"verified_variants": []})
    seen = {}

    def fake_call(model, prompt_payload):
        seen.update(prompt_payload)
        return (
            {
                "status": "PASS",
                "change_decision": "CHANGE_REQUIRED",
                "change_severity": "material",
                "patchable": True,
                "patchability_reason": "exact_field_changes_available",
                "blocking_reasons": [],
                "required_fixes": [],
                "summary": "ok",
            },
            None,
        )

    monkeypatch.setattr(outcome_audit, "_call_openai_outcome_audit", fake_call)
    result = outcome_audit.audit_next_ai_review_outcome_with_openai()

    updated = _read_json(tmp_path / DECISIONS_PATH)["decisions"][0]
    assert result["status"] == "PASS"
    assert set(seen) == {
        "decision_id",
        "item_id",
        "issue_type",
        "risk_level",
        "variant_ids",
        "target_records",
        "gemini_summary",
        "openai_summary",
        "current_change_decision",
        "current_change_severity",
        "current_patchable",
        "current_patchability_reason",
    }
    assert list(seen["target_records"]) == ["v1"]
    assert "verified_variants" not in json.dumps(seen)
    assert updated["outcome_audit_status"] == "passed"
    assert updated["change_decision"] == "CHANGE_REQUIRED"
    assert (tmp_path / AI_OUTCOME_AUDITS_PATH).exists()


def test_audit_next_ai_review_outcome_fail_stores_required_fixes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(
        tmp_path / DECISIONS_PATH,
        {"decisions": [{"decision_id": "d1", "item_id": "iq_000005", "variant_ids": ["v1"], "outcome_audit_status": "pending"}]},
    )
    _write_json(tmp_path / ACTIVE_WORKING_DATABASE_PATH, {"verified_variants": [{"variant_id": "v1"}]})

    monkeypatch.setattr(
        outcome_audit,
        "_call_openai_outcome_audit",
        lambda model, payload: (
            {
                "status": "FAIL",
                "change_decision": "NO_CHANGE_REQUIRED",
                "change_severity": "minor",
                "patchable": False,
                "patchability_reason": "vague_recommendation",
                "blocking_reasons": ["needs review"],
                "required_fixes": ["clarify evidence"],
                "summary": "failed",
            },
            None,
        ),
    )

    event = outcome_audit.audit_next_ai_review_outcome_with_openai()
    updated = _read_json(tmp_path / DECISIONS_PATH)["decisions"][0]

    assert event["status"] == "FAIL"
    assert updated["outcome_audit_status"] == "failed"
    assert updated["outcome_audit_required_fixes"] == ["clarify evidence"]
