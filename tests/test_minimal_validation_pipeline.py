import json
from pathlib import Path

from core.paths import DECISIONS_PATH, ISSUE_QUEUE_PATH, MANIFEST_PATH, SOURCE_CANONICAL_PATH
from engine.validation.minimal_pipeline import build_issue_queue, run_full_audit


def _field(value, *, status="verified", confidence="high", sources_count=2):
    return {
        "value": value,
        "status": status,
        "confidence": confidence,
        "sources_count": sources_count,
        "source_ids": [f"src_{idx}" for idx in range(sources_count)],
    }


def _variant(variant_id="clean_1", **overrides):
    data = {
        "variant_id": variant_id,
        "seed_id": "toyota__corolla__2020__2026__il",
        "make": "Toyota",
        "model": "Corolla",
        "aliases": [],
        "year_start": {"value": 2020},
        "year_end": {"value": 2026},
        "market": "IL",
        "generation": _field("E210"),
        "body_type": _field("Sedan"),
        "seats": _field(5),
        "engine": _field("1.8L Petrol"),
        "transmission": _field("automatic"),
        "fuel_type": _field("petrol"),
        "drivetrain": _field("FWD"),
        "trim": _field("Active"),
        "verification_status": "verified",
        "confidence": "high",
        "sources_count": 14,
    }
    data.update(overrides)
    return data


def _package(*, verified=None, partial=None, batch_state=None):
    return {
        "verified_variants": verified if verified is not None else [_variant()],
        "partial_variants": partial if partial is not None else [],
        "batch_state": batch_state if batch_state is not None else {},
    }


def _write_source(tmp_path: Path, source: dict):
    path = tmp_path / SOURCE_CANONICAL_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(source), encoding="utf-8")
    return path


def test_run_full_audit_creates_issue_queue_and_manifest(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = _package(
        verified=[_variant(), _variant("bad_1", model="", sources_count=0)],
    )
    _write_source(tmp_path, source)

    summary = run_full_audit()

    assert (tmp_path / ISSUE_QUEUE_PATH).exists()
    assert (tmp_path / MANIFEST_PATH).exists()
    queue_doc = json.loads((tmp_path / ISSUE_QUEUE_PATH).read_text(encoding="utf-8"))
    manifest = json.loads((tmp_path / MANIFEST_PATH).read_text(encoding="utf-8"))
    assert queue_doc["source_variant_count"] == 2
    assert queue_doc["items"]
    assert manifest["source_variant_count"] == 2
    assert manifest["issues_total"] == summary["issues_total"]
    assert manifest["final_clean_database_path"] == "data/final/resume_package_final_clean.json"


def test_queue_contains_only_problematic_items_and_excludes_clean_verified_item():
    clean = _variant("clean_verified")
    bad = _variant("bad_missing_make", make="")

    queue = build_issue_queue(_package(verified=[clean, bad]))

    queued_variant_ids = {vid for item in queue for vid in item["variant_ids"]}
    assert "bad_missing_make" in queued_variant_ids
    assert "clean_verified" not in queued_variant_ids
    assert all(item["issue_type"] != "ui_only_warning" for item in queue)


def test_low_level_harmless_formatting_does_not_generate_model_review():
    formatted = _variant(
        "harmless_formatting",
        trim=_field("Active  Plus"),
        candidate_raw={"trim": "Active Plus"},
    )

    queue = build_issue_queue(_package(verified=[formatted]))

    assert queue == []


def test_high_risk_evidence_gap_sets_requires_model_review_true():
    weak = _variant(
        "weak_verified",
        sources_count=0,
        body_type=_field("Sedan", sources_count=0),
        seats=_field(5, sources_count=0),
        engine=_field("1.8L Petrol", sources_count=0),
        transmission=_field("automatic", sources_count=0),
        fuel_type=_field("petrol", sources_count=0),
        drivetrain=_field("FWD", sources_count=0),
        trim=_field("Active", sources_count=0),
    )

    queue = build_issue_queue(_package(verified=[weak]))

    assert len(queue) == 1
    assert queue[0]["issue_type"] == "stale_or_weak_source_evidence"
    assert queue[0]["risk_level"] == "high"
    assert queue[0]["requires_model_review"] is True


def test_decisions_json_is_initialized_but_not_filled_with_fake_decisions(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_source(tmp_path, _package(verified=[_variant()]))

    run_full_audit()

    decisions = json.loads((tmp_path / DECISIONS_PATH).read_text(encoding="utf-8"))
    assert decisions["source_file"] == SOURCE_CANONICAL_PATH
    assert decisions["decisions"] == []


def test_unsafe_alias_mismatch_is_problematic_but_not_model_review():
    variant = _variant("alias_variant", make="Lynk & Co", aliases=["Lynk and Co"])

    queue = build_issue_queue(_package(verified=[variant]))

    assert len(queue) == 1
    assert queue[0]["issue_type"] == "unsafe_alias_mismatch"
    assert queue[0]["requires_model_review"] is False
    assert queue[0]["requires_manual_review"] is True


def test_risk_levels_are_limited_to_required_values():
    bad = _variant("bad_years", year_start={"value": 2026}, year_end={"value": 2020})

    queue = build_issue_queue(_package(verified=[bad]))

    assert queue
    assert {item["risk_level"] for item in queue} <= {"critical", "high", "medium", "low"}
