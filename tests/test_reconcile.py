"""Anti-regression tests for deterministic audit post-processing.

These confirm the tolerant validation policy is preserved while the output is
cleaned and made internally consistent. None of these may make acceptance
stricter or convert ``clean_partial`` into ``reject``.
"""

import pytest

from scripts.reconcile import reconcile_validation_output
from scripts.output_writer import build_output_row
from scripts.run_paths import MOCK_GROUNDING_SENTINEL
from scripts.validator_engine import build_mock_row, decide_mock
from scripts.clustering import Cluster


def _variant(**std):
    base = {
        "make": "Abarth", "model": "500", "engine": "1.4L Turbo",
        "transmission": "manual", "fuel_type": "petrol", "drivetrain": "FWD",
        "body_type": "Hatchback", "year_start": 2008, "year_end": 2015,
        "generation": None, "trim": None, "official_marketed_name_il": None,
        "market_scope": "IL",
    }
    base.update(std)
    return {"standard_variant": base}


def _ident(**kw):
    base = {
        "make": "Abarth", "model": "500", "engine": "1.4L Turbo",
        "transmission": "manual", "fuel_type": "petrol", "drivetrain": "FWD",
        "body_type": "Hatchback", "year_start": 2008, "year_end": 2015,
        "generation": None, "market_scope": "IL",
    }
    base.update(kw)
    return base


def _trim(value, weak):
    return {"trim": value, "official_marketed_name_il": None, "local_brand_name_il": None,
            "alternate_names": [], "trim_is_weak": weak}


def _cluster():
    return Cluster(cluster_id="CLU-test", cluster_key="k", member_ids=["VAL-000001"])


# --------------------------------------------------------------------------
# Fix 6 items 1-5: tolerant decision policy preserved.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("value,weak", [
    ("Base", True), ("Standard", True), (None, True), ("", True),
])
def test_valid_identity_weak_trim_is_clean_partial(value, weak):
    result = decide_mock(_ident(), _trim(value, weak))
    assert result["validation_decision"] == "clean_partial"


def test_missing_official_marketed_name_is_clean_partial():
    row = build_mock_row("VAL-000001", _ident(), _trim(None, True), _cluster())
    assert row["validation_decision"] == "clean_partial"
    assert row["official_marketed_name_il"] is None


def test_trim_only_uncertainty_never_becomes_reject():
    # Reconciliation must never flip a clean_partial into reject.
    row = build_output_row(
        "VAL-000001",
        validation_decision="clean_partial",
        canonical_trim=None,
        trim_status="unresolved",
    )
    out = reconcile_validation_output(_variant(), row)
    assert out["validation_decision"] == "clean_partial"
    assert out["acceptance_tier"] == "partial"


# --------------------------------------------------------------------------
# Fix 6 item 6: fields_changed records changed year_start.
# --------------------------------------------------------------------------


def test_fields_changed_records_changed_year_start():
    row = build_output_row(
        "VAL-000001",
        validation_decision="clean_partial",
        year_start=2010,  # source is 2008
        year_end=2015,
    )
    out = reconcile_validation_output(_variant(year_start=2008), row)
    changed = {c["field"]: c for c in out["fields_changed"]}
    assert "year_start" in changed
    assert changed["year_start"]["from"] == 2008
    assert changed["year_start"]["to"] == 2010


def test_unchanged_fields_are_not_recorded():
    row = build_output_row(
        "VAL-000001", validation_decision="clean_partial",
        year_start=2008, year_end=2015, canonical_make="Abarth",
    )
    out = reconcile_validation_output(_variant(), row)
    assert out["fields_changed"] == []


# --------------------------------------------------------------------------
# Fix 6 item 7: filled official_marketed_name_il is not left unresolved.
# --------------------------------------------------------------------------


def test_filled_official_name_not_left_unresolved():
    row = build_output_row(
        "VAL-000001",
        validation_decision="clean_partial",
        official_marketed_name_il="אבארט 500",
        fields_left_unresolved=["official_marketed_name_il", "canonical_trim"],
        canonical_trim=None,
        trim_status="unresolved",
    )
    out = reconcile_validation_output(_variant(), row)
    assert "official_marketed_name_il" not in out["fields_left_unresolved"]
    # canonical_trim genuinely unresolved -> stays.
    assert "canonical_trim" in out["fields_left_unresolved"]


def test_filled_engine_year_removed_from_unresolved():
    row = build_output_row(
        "VAL-000001", validation_decision="clean_partial",
        engine="1.4L Turbo", year_start=2008, year_end=2015,
        fields_left_unresolved=["engine", "year_start", "year_end"],
    )
    out = reconcile_validation_output(_variant(), row)
    assert out["fields_left_unresolved"] == ["official_marketed_name_il"]


# --------------------------------------------------------------------------
# Fix 6 item 8: evidence_sources are normalized to structured objects.
# --------------------------------------------------------------------------


def test_evidence_sources_normalized_to_objects():
    row = build_output_row(
        "VAL-000001", validation_decision="clean_partial",
        evidence_sources=[
            "iCar.co.il Abarth 500 historical reviews and catalog data",
            {"title": "Abarth catalog", "url": "https://icar.co.il/abarth"},
        ],
    )
    out = reconcile_validation_output(_variant(), row)
    for src in out["evidence_sources"]:
        assert isinstance(src, dict)
        assert set(src.keys()) == {"title", "url", "source_name", "source_type", "supports"}
    first = out["evidence_sources"][0]
    assert first["source_name"] == "iCar.co.il"
    assert first["source_type"] == "editorial"
    second = out["evidence_sources"][1]
    assert second["url"] == "https://icar.co.il/abarth"
    assert second["source_name"] == "icar.co.il"


# --------------------------------------------------------------------------
# Fix 6 item 9: real output cannot contain mock rows/markers.
# --------------------------------------------------------------------------


def test_real_output_strips_mock_marker():
    row = build_output_row(
        "VAL-000001", validation_decision="clean_partial",
        grounding_summary=MOCK_GROUNDING_SENTINEL,
        evidence_sources=[MOCK_GROUNDING_SENTINEL],
    )
    out = reconcile_validation_output(_variant(), row, run_mode="real")
    assert out["grounding_summary"] != MOCK_GROUNDING_SENTINEL
    assert all(
        s.get("title") != MOCK_GROUNDING_SENTINEL for s in out["evidence_sources"]
    )


def test_mock_mode_keeps_sentinel():
    row = build_output_row(
        "VAL-000001", validation_decision="clean_partial",
        grounding_summary=MOCK_GROUNDING_SENTINEL,
    )
    out = reconcile_validation_output(_variant(), row, run_mode="mock")
    assert out["grounding_summary"] == MOCK_GROUNDING_SENTINEL


# --------------------------------------------------------------------------
# trim_status / acceptance_tier consistency + possible_trim_names cleanup.
# --------------------------------------------------------------------------


def test_trim_status_consistent_with_canonical_trim():
    # Null trim but status claims verified -> relaxed to unresolved.
    row = build_output_row(
        "VAL-000001", validation_decision="clean_partial",
        canonical_trim=None, trim_status="verified",
    )
    out = reconcile_validation_output(_variant(), row)
    assert out["trim_status"] == "unresolved"

    # Concrete trim but unresolved -> at least inferred.
    row2 = build_output_row(
        "VAL-000001", validation_decision="clean_exact",
        canonical_trim="Scorpione", trim_status="unresolved",
    )
    out2 = reconcile_validation_output(_variant(), row2)
    assert out2["trim_status"] == "inferred"


def test_acceptance_tier_matches_decision():
    for decision, tier in (
        ("clean_exact", "exact"), ("clean_partial", "partial"),
        ("split_required", "none"),
    ):
        row = build_output_row("VAL-1", validation_decision=decision)
        out = reconcile_validation_output(_variant(), row)
        assert out["acceptance_tier"] == tier


def test_reject_without_blocking_issues_downgraded_to_partial():
    row = build_output_row("VAL-1", validation_decision="reject")
    out = reconcile_validation_output(_variant(), row)
    assert out["validation_decision"] == "clean_partial"
    assert out["acceptance_tier"] == "partial"


def test_reject_with_blocking_issues_stays_reject():
    row = build_output_row(
        "VAL-1", validation_decision="reject",
        blocking_identity_issues=["make/model combination does not exist"],
    )
    out = reconcile_validation_output(_variant(), row)
    assert out["validation_decision"] == "reject"
    assert out["acceptance_tier"] == "none"


def test_possible_trim_names_drops_placeholders_keeps_real():
    row = build_output_row(
        "VAL-000001", validation_decision="clean_partial",
        possible_trim_names=["Scorpione", "base", "", "None", "Scorpione", "Esseesse"],
    )
    out = reconcile_validation_output(_variant(), row)
    assert out["possible_trim_names"] == ["Scorpione", "Esseesse"]


# --------------------------------------------------------------------------
# v2 post-processing guards
# --------------------------------------------------------------------------


def test_slash_trim_downgrades_clean_exact():
    row = build_output_row(
        "VAL-1", validation_decision="clean_exact",
        canonical_trim="Turismo / Competizione",
    )
    out = reconcile_validation_output(_variant(), row)
    assert out["validation_decision"] == "clean_partial"
    assert out["acceptance_tier"] == "partial"
    assert any("Slash" in i for i in out["non_blocking_trim_issues"])


def test_under_consideration_downgrades_clean_exact():
    row = build_output_row(
        "VAL-1", validation_decision="clean_exact",
        grounding_summary="This model is under consideration for Israeli import.",
    )
    out = reconcile_validation_output(_variant(), row)
    assert out["validation_decision"] == "clean_partial"
    assert out["is_currently_imported_il"] is None


def test_year_end_cleared_when_still_produced():
    row = build_output_row(
        "VAL-1", validation_decision="clean_exact",
        is_currently_produced=True, year_end=2026,
    )
    out = reconcile_validation_output(_variant(), row)
    assert out["year_end"] is None


def test_source_type_classification():
    from scripts.reconcile import classify_source_type
    assert classify_source_type("yad2.co.il", "") == "marketplace"
    assert classify_source_type("icar.co.il", "") == "editorial"
    assert classify_source_type("data.gov.il", "") == "government"
    assert classify_source_type("abarth.co.il", "") == "official_importer"
    assert classify_source_type("reddit", "") == "forum_community"
    assert classify_source_type("some random thing", "") == "unknown"
