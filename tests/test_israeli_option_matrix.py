"""Israeli option-matrix + final-consistency tests (production-readiness v3).

These lock the conservative "exact_variant vs configurable_group vs review_only"
publication model, the deterministic final consistency pass, enum normalization,
duplicate-primary selection, and the separation of the exact clean catalog from
configurable-group output.
"""

from scripts.output_writer import build_output_row, route_validated_rows
from scripts.reconcile import (
    GuardFlag,
    build_option_matrix,
    detect_unknown_enums,
    final_seal,
    normalize_field_enums,
    reconcile_validation_output_with_flags,
)


def _grounded(**overrides):
    """A schema-complete, well-grounded base row for final_seal tests."""
    row = build_output_row(
        "VAL-1",
        canonical_make="Abarth", canonical_model="500",
        canonical_trim="Turismo", official_marketed_name_il="אבארט 500",
        body_type="Hatchback", fuel_type="Petrol", engine="1.4",
        transmission="automatic", drivetrain="FWD",
        year_start=2015, year_end=2018,
        validation_decision="clean_exact", identity_status="verified",
        trim_status="verified", identity_confidence=0.9, trim_confidence=0.9,
    )
    row.update({
        "evidence_auditability": "acceptable",
        "evidence_sources": [{"title": "icar", "url": "https://www.icar.co.il/x", "source_name": "icar.co.il", "source_type": "editorial", "supports": ["exact_trim", "transmission"]}],
        "source_support_matrix": [{"field": f, "value": row.get(f), "support_level": "direct", "source_indexes": [0], "reason": "supported"} for f in ("canonical_trim", "transmission", "engine", "fuel_type", "body_type", "drivetrain", "year_start")],
        "field_validation": {f: {"status": "verified", "confidence": 0.9, "evidence_strength": "strong", "source_indexes": [0], "risk_tags": [], "notes": "supported"} for f in ("canonical_make", "canonical_model", "canonical_series_or_generation", "canonical_trim", "official_marketed_name_il", "body_type", "fuel_type", "engine", "transmission", "drivetrain", "year_start", "year_end", "is_currently_produced", "is_currently_imported_il")},
        "grounding_status": {"gemini_grounding_required": True, "gemini_grounding_present": True, "gemini_grounding_quality": "acceptable", "gpt54_grounding_required": False, "gpt54_grounding_present": False, "gpt54_grounding_quality": "missing", "final_grounding_gate_passed": True},
    })
    row.update(overrides)
    return row


# 1 -------------------------------------------------------------------------
def test_repair_success_does_not_leave_critical_null_guard_unapplied():
    flag = GuardFlag(
        guard_name="populated_field_marked_unresolved", severity="critical",
        field_affected="transmission", original_value="manual", guard_value=None,
        reason="Transmission marked unresolved by adjudicator.",
    )
    sealed, _ = final_seal(_grounded(transmission="manual"), None, {"repair_decision": "patched"}, [flag], require_gpt54_grounding_for_repair=False)
    # Either the value is nulled and listed unresolved, or the guard was removed.
    assert sealed["transmission"] is None
    assert "transmission" in sealed["fields_left_unresolved"]
    # The two invalid states must never co-exist.
    assert not (sealed.get("transmission") == "manual" and "transmission" in sealed["fields_left_unresolved"])


# 2 -------------------------------------------------------------------------
def test_unresolved_field_not_verified():
    row = _grounded(fields_left_unresolved=["transmission"])
    sealed, _ = final_seal(row)
    assert sealed["field_validation"]["transmission"]["status"] != "verified"
    assert sealed["publishable_to_clean_catalog"] is False
    assert sealed["final_route"] != "clean_catalog"


# 3 -------------------------------------------------------------------------
def test_combined_trim_becomes_configurable_group_or_split_queue():
    sealed, _ = final_seal(_grounded(canonical_trim="Turismo / Competizione", split_candidates=["Turismo", "Competizione"]))
    assert sealed["canonical_trim"] is None
    assert sealed["publication_type"] != "exact_variant"
    assert sealed["final_route"] != "clean_catalog"
    assert (sealed.get("split_candidates") or sealed.get("option_matrix"))


# 4 -------------------------------------------------------------------------
def test_option_matrix_preserves_valid_combinations():
    row = _grounded(
        canonical_trim=None, trim_status="unresolved", trim_confidence=0.0,
        validation_decision="clean_partial",
        possible_trim_names=[
            {"trim": "Turismo", "transmission": "robotic"},
            {"trim": "Competizione", "transmission": "manual"},
        ],
    )
    sealed, _ = final_seal(row)
    assert sealed["publication_type"] == "configurable_group"
    matrix = sealed["option_matrix"]
    pairs = {(e["trim"], e["transmission"]) for e in matrix}
    assert pairs == {("Turismo", "robotic"), ("Competizione", "manual")}
    # The impossible cross combinations must never appear.
    assert ("Turismo", "manual") not in pairs
    assert ("Competizione", "robotic") not in pairs


# 5 -------------------------------------------------------------------------
def test_placeholder_trim_not_clean():
    sealed, _ = final_seal(_grounded(canonical_trim="Base"))
    assert sealed["canonical_trim"] is None
    assert sealed["trim_status"] != "verified"
    assert sealed["final_route"] != "clean_catalog"
    assert sealed["publication_type"] in {"configurable_group", "review_only"}


# 6 -------------------------------------------------------------------------
def test_israeli_year_start_overrides_global_year():
    model_output = build_output_row(
        "VAL-1", canonical_make="Abarth", canonical_model="500",
        year_start=2008, validation_decision="clean_partial",
        identity_status="likely_valid", trim_status="unresolved",
        grounding_summary="The Abarth 500 was launched in Israel in 2010, two years after the global debut.",
    )
    row, _ = reconcile_validation_output_with_flags({}, model_output, run_mode="real")
    assert row["year_start"] == 2010


# 7 -------------------------------------------------------------------------
def test_unknown_enums_are_normalized_or_blocked():
    # Known model-invented enums are normalized onto the allowed set.
    row = {
        "field_validation": {
            "transmission": {"status": "candidate_unverified", "evidence_strength": "limited"},
        },
        "source_support_matrix": [{"field": "transmission", "support_level": "strong"}],
    }
    normalize_field_enums(row)
    assert row["field_validation"]["transmission"]["status"] == "candidate"
    assert row["field_validation"]["transmission"]["evidence_strength"] == "weak"
    assert row["source_support_matrix"][0]["support_level"] == "direct"

    # A truly unknown enum survives and blocks the clean export.
    bad = _grounded()
    bad["field_validation"]["engine"]["status"] = "totally_invented_status"
    sealed, _ = final_seal(bad)
    assert detect_unknown_enums(sealed)
    assert sealed["publishable_to_clean_catalog"] is False
    assert sealed["final_route"] != "clean_catalog"


# 8 -------------------------------------------------------------------------
def test_duplicate_group_assigns_primary():
    seal = {"seal_completed": True, "clean_catalog_passed": True, "blocks_clean_catalog": False, "passed": True}
    common = dict(
        canonical_make="Abarth", canonical_model="595", canonical_trim="Competizione",
        canonical_series_or_generation="1st Gen", body_type="Hatchback",
        fuel_type="petrol", engine="1.4L Turbo", transmission="manual",
        drivetrain="FWD", year_start=2016, year_end=2021, market_scope="IL",
        validation_decision="clean_exact", identity_status="verified",
        trim_status="verified", publication_type="exact_variant",
        final_seal_result=seal, publishable_to_clean_catalog=True,
        final_route="clean_catalog",
    )
    rows = [dict(validation_id="VAL-A", **common), dict(validation_id="VAL-B", **common)]
    routed = route_validated_rows(rows)
    by_id = {r["validation_id"]: r for r in routed}
    primaries = [r for r in routed if not r.get("duplicate_of")]
    assert len(primaries) == 1
    primary_id = primaries[0]["validation_id"]
    dup = by_id["VAL-B"] if primary_id == "VAL-A" else by_id["VAL-A"]
    assert dup["duplicate_of"] == primary_id
    assert dup["final_route"] == "duplicate_queue"
    assert dup["publishable_to_clean_catalog"] is False


# 9 -------------------------------------------------------------------------
def test_clean_export_gate():
    sealed, _ = final_seal(_grounded(validation_decision="clean_partial", canonical_trim=None, trim_status="unresolved", trim_confidence=0.0))
    assert sealed["publishable_to_clean_catalog"] is False
    assert sealed["final_route"] != "clean_catalog"
    # And the cross-row exporter agrees.
    routed = route_validated_rows([sealed])
    assert routed[0]["final_route"] != "clean_catalog"


# 10 ------------------------------------------------------------------------
def test_configurable_group_export_separate_from_clean_catalog():
    row = _grounded(
        canonical_trim=None, trim_status="unresolved", trim_confidence=0.0,
        transmission=None, validation_decision="clean_partial",
        possible_trim_names=["Turismo", "Competizione"],
        candidate_values={"transmission": {"values": ["manual", "robotic"], "status": "candidate", "reason": "Both sold in IL."}},
    )
    sealed, _ = final_seal(row)
    assert sealed["publication_type"] == "configurable_group"
    assert sealed["final_route"] != "clean_catalog"
    assert sealed["publishable_to_clean_catalog"] is False
    usf = sealed["user_selectable_fields"]
    assert "manual" in usf.get("transmission", []) and "robotic" in usf.get("transmission", [])
    # The configurable group is exportable via its own queue, never clean catalog.
    routed = route_validated_rows([sealed])
    assert routed[0]["final_route"] == "configurable_group_queue"
    assert routed[0]["publishable_to_clean_catalog"] is False
