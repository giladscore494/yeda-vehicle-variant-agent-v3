"""v4 strict-routing + final-seal regression tests.

These lock in the non-negotiable rules from the architecture brief:

- clean_partial must never enter clean_catalog
- canonical_trim=null must never enter clean_catalog
- split_required must route to split_queue with canonical_trim=null
- unresolved technical fields must not remain populated as verified
- redirect-only evidence is never "strong" auditability
- repair/final-seal metadata survives a checkpoint resume
"""

import json
import os

from scripts.output_writer import (
    OutputStore,
    build_output_row,
    route_validated_rows,
)
from scripts.reconcile import (
    final_seal,
    assess_grounding,
    is_temporary_grounding_redirect,
)

REDIRECT = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/ABC123"


def _grounded(**over):
    row = build_output_row(
        "v",
        canonical_make="Abarth", canonical_model="500", canonical_trim="Turismo",
        official_marketed_name_il="אבארט 500", body_type="Hatchback", fuel_type="petrol",
        engine="1.4", transmission="automatic", drivetrain="FWD", year_start=2015, year_end=2018,
        validation_decision="clean_exact", identity_status="verified", trim_status="verified",
        identity_confidence=0.9, trim_confidence=0.9,
    )
    row.update({
        "evidence_auditability": "acceptable",
        "evidence_sources": [{"title": "icar", "url": "https://www.icar.co.il/x", "source_name": "icar.co.il", "source_type": "editorial", "supports": ["exact_trim"]}],
        "source_support_matrix": [{"field": f, "value": row.get(f), "support_level": "direct", "source_indexes": [0], "reason": "ok"} for f in ("canonical_trim", "transmission", "engine", "fuel_type", "body_type", "drivetrain", "year_start")],
        "field_validation": {f: {"status": "verified", "confidence": 0.9, "evidence_strength": "strong", "source_indexes": [0], "risk_tags": [], "notes": "ok"} for f in ("canonical_make", "canonical_model", "canonical_series_or_generation", "canonical_trim", "official_marketed_name_il", "body_type", "fuel_type", "engine", "transmission", "drivetrain", "year_start", "year_end", "is_currently_produced", "is_currently_imported_il")},
        "grounding_status": {"gemini_grounding_required": True, "gemini_grounding_present": True, "gemini_grounding_quality": "acceptable", "gpt54_grounding_required": False, "gpt54_grounding_present": False, "gpt54_grounding_quality": "missing", "final_grounding_gate_passed": True},
    })
    row.update(over)
    return row


# --------------------------------------------------------------------------
# 5.3 output routing
# --------------------------------------------------------------------------


def test_output_writer_never_publishes_clean_partial_without_final_seal():
    rows = route_validated_rows([
        build_output_row("P", canonical_make="X", canonical_model="Y", validation_decision="clean_partial", identity_status="likely_valid", canonical_trim=None, trim_status="unresolved"),
    ])
    assert rows[0]["publishable_to_clean_catalog"] is False
    assert rows[0]["final_route"] != "clean_catalog"


def test_output_writer_never_publishes_clean_partial_with_null_trim():
    sealed, _ = final_seal(_grounded(validation_decision="clean_partial", canonical_trim=None, trim_status="unresolved", trim_confidence=0.0))
    routed = route_validated_rows([sealed])
    assert routed[0]["publishable_to_clean_catalog"] is False
    assert routed[0]["final_route"] != "clean_catalog"


def test_output_writer_strict_fallback_blocks_unsealed_clean_exact_without_grounding():
    rows = route_validated_rows([
        build_output_row("E", canonical_make="X", canonical_model="Y", canonical_trim="Sport", validation_decision="clean_exact", identity_status="verified", trim_status="verified"),
    ])
    # No grounding_status / auditability -> strict gate blocks publish.
    assert rows[0]["publishable_to_clean_catalog"] is False
    assert rows[0]["final_route"] != "clean_catalog"


def test_output_writer_mixed_sealed_unsealed_rows_routes_each_safely():
    sealed_clean, _ = final_seal(_grounded())
    unsealed_partial = build_output_row("U", canonical_make="X", canonical_model="Y", validation_decision="clean_partial", identity_status="likely_valid", canonical_trim=None, trim_status="unresolved")
    routed = route_validated_rows([sealed_clean, unsealed_partial])
    by = {r["validation_id"]: r for r in routed}
    assert by[sealed_clean["validation_id"]]["final_route"] == "clean_catalog"
    assert by["U"]["publishable_to_clean_catalog"] is False
    assert by["U"]["final_route"] != "clean_catalog"


def test_absorb_checkpoint_preserves_repair_metadata_counters(tmp_path):
    out = str(tmp_path / "out.json")
    cp = str(tmp_path / "cp.json")
    store = OutputStore(output_path=out, checkpoint_path=cp, run_mode="real")
    store.metadata["stage25_repair_triggered_rows"] = 4
    store.metadata["stage3_repair_adjudicator_calls"] = 3
    store.metadata["stage4_final_seal_blocks"] = 2
    store.metadata["stage25_repair_required_but_missing_adjudicator"] = 1
    store.flush()

    fresh = OutputStore(output_path=out, checkpoint_path=cp, run_mode="real")
    fresh.load_existing()
    assert fresh.metadata["stage25_repair_triggered_rows"] == 4
    assert fresh.metadata["stage3_repair_adjudicator_calls"] == 3
    assert fresh.metadata["stage4_final_seal_blocks"] == 2
    assert fresh.metadata["stage25_repair_required_but_missing_adjudicator"] == 1


# --------------------------------------------------------------------------
# 5.4 guard / final seal
# --------------------------------------------------------------------------


def test_split_required_clears_combined_canonical_trim():
    sealed, _ = final_seal(_grounded(canonical_trim="Turismo / Competizione", split_candidates=["Turismo", "Competizione"]))
    assert sealed["validation_decision"] == "split_required"
    assert sealed["canonical_trim"] is None
    assert sealed["final_route"] == "split_queue"
    assert sealed["publishable_to_clean_catalog"] is False


def test_split_required_derives_candidates_when_missing():
    sealed, _ = final_seal(_grounded(canonical_trim="Competizione / Scorpione / Nuvolari S", split_candidates=[]))
    assert sealed["canonical_trim"] is None
    assert sealed["validation_decision"] == "split_required"
    assert set(sealed["split_candidates"]) == {"Competizione", "Scorpione", "Nuvolari S"}


def test_unresolved_transmission_issue_nullifies_or_marks_transmission_unresolved():
    sealed, _ = final_seal(_grounded(
        transmission="manual",
        non_blocking_trim_issues=["manual transmission is not verified for the Israeli market; transmission left unresolved."],
    ))
    assert sealed["transmission"] is None or "transmission" in sealed["fields_left_unresolved"]
    assert sealed["final_route"] != "clean_catalog"
    assert sealed["publishable_to_clean_catalog"] is False


def test_vertex_redirect_only_evidence_not_strong_auditability():
    assert is_temporary_grounding_redirect(REDIRECT) is True
    row = _grounded(evidence_auditability="strong", evidence_sources=[{"title": "x", "url": REDIRECT, "source_name": "vertex", "source_type": "editorial", "supports": []}])
    gs = assess_grounding(row)
    assert gs["gemini_grounding_quality"] != "strong"
    assert row["evidence_auditability"] != "strong"


def test_field_validation_missing_defaults_to_unresolved_and_blocks_clean_catalog():
    row = _grounded()
    row["field_validation"] = {}
    sealed, _ = final_seal(row)
    assert isinstance(sealed["field_validation"], dict) and sealed["field_validation"]
    # Missing per-field validation downgrades confidence and blocks publish.
    assert sealed["publishable_to_clean_catalog"] is False


# --------------------------------------------------------------------------
# 5.5 latest 5-row sample fixture
# --------------------------------------------------------------------------


def _sample_partial(vid, *, year_end, transmission="manual"):
    return _grounded(
        validation_decision="clean_partial", canonical_trim=None, trim_status="unresolved",
        trim_confidence=0.0, identity_status="likely_valid", year_end=year_end,
        transmission=transmission,
        evidence_sources=[{"title": "t", "url": REDIRECT, "source_name": "auto.co.il", "source_type": "editorial", "supports": ["market_presence_il"]}],
    )


def test_sample_five_rows_route_safely():
    val1, _ = final_seal(_sample_partial("VAL-000001", year_end=2016))
    val3, _ = final_seal(_grounded(validation_decision="split_required", canonical_trim="Competizione / Scorpione / Nuvolari S", split_candidates=["Competizione", "Scorpione", "Nuvolari S"]))
    val4, _ = final_seal(_grounded(validation_decision="split_required", canonical_trim="Turismo / Competizione", split_candidates=["Turismo", "Competizione"]))
    val5, _ = final_seal(_grounded(
        validation_decision="clean_partial", canonical_trim=None, trim_status="unresolved",
        identity_status="uncertain", transmission="manual",
        non_blocking_trim_issues=["Abarth 500C/Cabriolet manual transmission is not verified for the Israeli market; transmission left unresolved."],
    ))

    for row in (val1, val3, val4, val5):
        assert row["final_route"] != "clean_catalog"
        assert row["publishable_to_clean_catalog"] is False
        assert row.get("final_seal_result")

    assert val1["final_route"] in {"partial_queue", "review_queue"}
    assert val3["final_route"] == "split_queue" and val3["canonical_trim"] is None
    assert val4["final_route"] == "split_queue" and val4["canonical_trim"] is None
    assert val5["transmission"] is None or "transmission" in val5["fields_left_unresolved"]
