import hashlib
import json
from pathlib import Path

import pytest

from core.paths import (
    ACTIVE_WORKING_DATABASE_PATH,
    DECISIONS_PATH,
    DIFF_AUDITS_PATH,
    PATCH_APPLICATIONS_PATH,
    PATCHES_PATH,
    SOURCE_CANONICAL_PATH,
)
from engine.validation import diff_quality_audit as diff_audit
from engine.validation.surgical_patches import (
    apply_next_safe_patch,
    apply_surgical_patch,
    assert_no_unexplained_variant_loss,
    build_candidate_patches_from_decisions,
)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _db(extra=None):
    payload = {
        "verified_variants": [
            {"variant_id": "v1", "make": "Toyota", "model": "Corolla", "trim": {"value": "Old"}},
            {"variant_id": "v2", "make": "Toyota", "model": "Yaris", "trim": {"value": "Keep"}},
        ],
        "partial_variants": [],
    }
    if extra:
        payload.update(extra)
    return payload


def _patch(patch_id="p1", variant_id="v1", from_value="Old", to_value="New", status="pending"):
    return {
        "patch_id": patch_id,
        "created_at": "now",
        "source_decision_id": "d1",
        "audit_run_id": "run1",
        "active_source_hash": "",
        "golden_source_hash": "",
        "variant_ids": [variant_id],
        "action": "update_fields",
        "safe_to_apply": True,
        "requires_diff_audit": True,
        "field_changes": {variant_id: {"trim.value": {"from": from_value, "to": to_value}}},
        "reason": "exact change",
        "confidence": 0.9,
        "status": status,
        "blocking_reason": None,
    }


def test_build_candidate_patches_creates_only_exact_field_changes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(tmp_path / ACTIVE_WORKING_DATABASE_PATH, _db())
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, _db())
    _write_json(
        tmp_path / DECISIONS_PATH,
        {
            "decisions": [
                {
                    "decision_id": "d1",
                    "action": "update_fields",
                    "variant_ids": ["v1"],
                    "field_changes": {"v1": {"trim.value": {"from": "Old", "to": "New"}}},
                    "safe_to_apply": True,
                    "confidence": 0.8,
                },
                {"decision_id": "vague", "variant_ids": ["v2"], "recommendation": "clean this up"},
                {
                    "decision_id": "missing_from",
                    "variant_ids": ["v2"],
                    "field_changes": {"v2": {"trim.value": {"to": "X"}}},
                    "safe_to_apply": True,
                },
                {
                    "decision_id": "blocked_safe",
                    "variant_ids": ["v2"],
                    "field_changes": {"v2": {"trim.value": {"from": "Keep", "to": "Safer"}}},
                    "safe_to_apply": False,
                },
            ]
        },
    )

    result = build_candidate_patches_from_decisions()
    payload = _read_json(tmp_path / PATCHES_PATH)

    assert result["created_count"] == 2
    assert result["pending"] == 1
    assert result["blocked"] == 1
    assert result["manual_review_required"] == 2
    assert len(payload["patches"]) == 2
    assert payload["patches"][0]["variant_ids"] == ["v1"]
    assert payload["patches"][0]["field_changes"]["v1"]["trim.value"] == {"from": "Old", "to": "New"}


@pytest.mark.parametrize("action", ["reject", "merge", "change_year_range", "change_market_scope", "promote_to_verified", "resolve_source_conflict"])
def test_build_candidate_patches_blocks_broad_actions(tmp_path, monkeypatch, action):
    monkeypatch.chdir(tmp_path)
    _write_json(
        tmp_path / DECISIONS_PATH,
        {
            "decisions": [
                {
                    "decision_id": action,
                    "action": action,
                    "variant_ids": ["v1"],
                    "field_changes": {"v1": {"trim.value": {"from": "Old", "to": "New"}}},
                    "safe_to_apply": True,
                }
            ]
        },
    )

    result = build_candidate_patches_from_decisions()

    assert result["created_count"] == 0
    assert result["manual_review_required"] == 1


def test_apply_next_safe_patch_applies_one_working_only_and_logs(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = _db()
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, source)
    _write_json(tmp_path / ACTIVE_WORKING_DATABASE_PATH, source)
    source_hash = hashlib.sha256((tmp_path / SOURCE_CANONICAL_PATH).read_bytes()).hexdigest()
    _write_json(tmp_path / PATCHES_PATH, {"patches": [_patch("p1"), _patch("p2", "v2", "Keep", "Changed")]})

    result = apply_next_safe_patch()

    working = _read_json(tmp_path / ACTIVE_WORKING_DATABASE_PATH)
    patches = _read_json(tmp_path / PATCHES_PATH)["patches"]
    assert result["status"] == "applied_pending_audit"
    assert result["patch_id"] == "p1"
    assert working["verified_variants"][0]["trim"]["value"] == "New"
    assert working["verified_variants"][1]["trim"]["value"] == "Keep"
    assert hashlib.sha256((tmp_path / SOURCE_CANONICAL_PATH).read_bytes()).hexdigest() == source_hash
    assert patches[0]["status"] == "applied_pending_audit"
    assert patches[1]["status"] == "pending"
    assert (tmp_path / PATCH_APPLICATIONS_PATH).exists()


def test_apply_surgical_patch_blocks_missing_duplicate_and_from_mismatch(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    duplicate = _db()
    duplicate["partial_variants"] = [{"variant_id": "v1", "trim": {"value": "Other"}}]
    _write_json(tmp_path / ACTIVE_WORKING_DATABASE_PATH, duplicate)
    _write_json(tmp_path / PATCHES_PATH, {"patches": [_patch("dup")]})
    assert apply_surgical_patch("dup")["status"] == "blocked"

    _write_json(tmp_path / ACTIVE_WORKING_DATABASE_PATH, _db())
    _write_json(tmp_path / PATCHES_PATH, {"patches": [_patch("missing", "nope")]})
    assert "not found" in apply_surgical_patch("missing")["blocking_reason"]

    _write_json(tmp_path / PATCHES_PATH, {"patches": [_patch("mismatch", "v1", "Wrong", "New")]})
    assert "from value mismatch" in apply_surgical_patch("mismatch")["blocking_reason"]


def test_no_pending_patch_does_not_rewrite_working_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(tmp_path / ACTIVE_WORKING_DATABASE_PATH, _db())
    _write_json(tmp_path / PATCHES_PATH, {"patches": [_patch(status="blocked")]})
    before = (tmp_path / ACTIVE_WORKING_DATABASE_PATH).read_bytes()

    result = apply_next_safe_patch()

    assert result["status"] == "no_pending_safe_patch"
    assert (tmp_path / ACTIVE_WORKING_DATABASE_PATH).read_bytes() == before


def test_variant_loss_guard_blocks_unexplained_loss():
    with pytest.raises(ValueError):
        assert_no_unexplained_variant_loss(
            [{"variant_id": "v1"}, {"variant_id": "v2"}],
            [{"variant_id": "v1"}],
            {"action": "update_fields", "safe_to_apply": True, "variant_ids": ["v2"]},
        )


def test_diff_audit_sends_only_before_after_diff_and_pass_updates_status(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(tmp_path / PATCHES_PATH, {"patches": [_patch("p1", status="applied_pending_audit")]})
    application = {
        "created_at": "now",
        "patch_id": "p1",
        "source_decision_id": "d1",
        "variant_ids": ["v1"],
        "changed_fields": {"v1": ["trim.value"]},
        "before": {"v1": {"variant_id": "v1", "trim": {"value": "Old"}}},
        "after": {"v1": {"variant_id": "v1", "trim": {"value": "New"}}},
        "field_changes": {"v1": {"trim.value": {"from": "Old", "to": "New"}}},
        "variant_count_before": 2,
        "variant_count_after": 2,
        "status": "applied_pending_audit",
    }
    (tmp_path / PATCH_APPLICATIONS_PATH).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / PATCH_APPLICATIONS_PATH).write_text(json.dumps(application) + "\n", encoding="utf-8")
    seen = {}

    def fake_call(model, prompt_payload):
        seen.update(prompt_payload)
        return {
            "status": "PASS",
            "confidence": 0.95,
            "blocking_reasons": [],
            "non_blocking_warnings": [],
            "required_fixes": [],
            "summary": "ok",
        }, None

    monkeypatch.setattr(diff_audit, "_call_openai_diff_audit", fake_call)
    result = diff_audit.audit_last_patch_diff_with_openai()

    assert result["status"] == "PASS"
    assert set(seen) == {
        "patch_id",
        "source_decision_id",
        "variant_ids",
        "before_records",
        "after_records",
        "exact_changed_fields",
        "diff",
        "variant_count_before",
        "variant_count_after",
        "decision_summary",
    }
    assert "verified_variants" not in json.dumps(seen)
    assert _read_json(tmp_path / PATCHES_PATH)["patches"][0]["status"] == "audit_passed"
    assert (tmp_path / DIFF_AUDITS_PATH).exists()


def test_diff_audit_fail_updates_status_and_required_fixes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(tmp_path / PATCHES_PATH, {"patches": [_patch("p1", status="applied_pending_audit")]})
    (tmp_path / PATCH_APPLICATIONS_PATH).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / PATCH_APPLICATIONS_PATH).write_text(json.dumps({"patch_id": "p1", "before": {}, "after": {}, "status": "applied_pending_audit"}) + "\n", encoding="utf-8")

    monkeypatch.setattr(
        diff_audit,
        "_call_openai_diff_audit",
        lambda model, payload: (
            {
                "status": "FAIL",
                "confidence": 0.4,
                "blocking_reasons": ["bad"],
                "non_blocking_warnings": [],
                "required_fixes": ["restore field"],
                "summary": "failed",
            },
            None,
        ),
    )

    result = diff_audit.audit_last_patch_diff_with_openai()

    assert result["status"] == "FAIL"
    assert result["required_fixes"] == ["restore field"]
    assert _read_json(tmp_path / PATCHES_PATH)["patches"][0]["status"] == "audit_failed"
    assert "api" not in (tmp_path / DIFF_AUDITS_PATH).read_text(encoding="utf-8").lower()
