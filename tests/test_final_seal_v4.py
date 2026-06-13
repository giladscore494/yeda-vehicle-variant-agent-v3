from scripts.output_writer import build_output_row
from scripts.reconcile import final_seal, compute_preflight_risk_tags, compute_repair_risk_score


def base_row(**overrides):
    row = build_output_row("v1", canonical_make="Abarth", canonical_model="500", canonical_trim="Turismo", official_marketed_name_il="אבארט 500", body_type="Hatchback", fuel_type="Petrol", engine="1.4", transmission="automatic", drivetrain="FWD", year_start=2015, year_end=2018, validation_decision="clean_exact", identity_status="verified", trim_status="verified", identity_confidence=0.9, trim_confidence=0.9)
    row.update({
        "evidence_auditability": "acceptable",
        "evidence_sources": [{"title":"icar","url":"https://www.icar.co.il/x","source_name":"icar.co.il","source_type":"editorial","supports":["market_presence_il","exact_trim","transmission"]}],
        "source_support_matrix": [{"field": f, "value": row.get(f), "support_level": "direct", "source_indexes": [0], "reason": "supported"} for f in ("canonical_trim","transmission","engine","fuel_type","body_type","drivetrain","year_start")],
        "field_validation": {f: {"status":"verified","confidence":0.9,"evidence_strength":"strong","source_indexes":[0],"risk_tags":[],"notes":"supported"} for f in ("canonical_make","canonical_model","canonical_series_or_generation","canonical_trim","official_marketed_name_il","body_type","fuel_type","engine","transmission","drivetrain","year_start","year_end","is_currently_produced","is_currently_imported_il")},
        "grounding_status": {"gemini_grounding_required": True, "gemini_grounding_present": True, "gemini_grounding_quality": "acceptable", "gpt54_grounding_required": False, "gpt54_grounding_present": False, "gpt54_grounding_quality": "missing", "final_grounding_gate_passed": True},
    })
    row.update(overrides)
    return row


def test_clean_partial_null_trim_not_publishable():
    row, _ = final_seal(base_row(validation_decision="clean_partial", canonical_trim=None, trim_status="unresolved", trim_confidence=0.0))
    assert row["publishable_to_clean_catalog"] is False
    assert row["final_route"] in {"partial_queue", "review_queue"}


def test_unresolved_transmission_blocks_or_nullifies():
    row, _ = final_seal(base_row(transmission="manual", non_blocking_trim_issues=["manual transmission is not verified"]))
    assert row["transmission"] is None or "transmission" in row["fields_left_unresolved"]
    assert row["final_route"] != "clean_catalog"


def test_summary_current_status_contradiction_rewritten():
    row, flags = final_seal(base_row(is_currently_produced=None, is_currently_imported_il=None, grounding_summary="This variant is still sold/imported in Israel."))
    assert "still sold" not in row["grounding_summary"].lower()
    assert any(f.guard_name == "current_status_contradiction" for f in flags)


def test_split_required_never_clean_catalog():
    row, _ = final_seal(base_row(canonical_trim="Turismo / Competizione", split_candidates=["Turismo", "Competizione"]))
    assert row["validation_decision"] == "split_required"
    assert row["publishable_to_clean_catalog"] is False
    assert row["final_route"] == "split_queue"


def test_body_style_not_trim():
    row, _ = final_seal(base_row(canonical_trim="500C", body_type="Cabriolet"))
    assert row["canonical_trim"] is None
    assert row["trim_status"] == "unresolved"
    assert row["final_route"] != "clean_catalog"


def test_gemini_grounding_missing_blocks_clean_catalog():
    row, _ = final_seal(base_row(evidence_sources=[], source_support_matrix=[], evidence_auditability="missing", grounding_status={}))
    assert row["grounding_status"]["gemini_grounding_present"] is False
    assert row["publishable_to_clean_catalog"] is False


def test_gpt54_grounding_required_when_repair_used():
    row, _ = final_seal(base_row(), repair_result={"repair_decision":"patched"})
    assert row["grounding_status"]["gpt54_grounding_present"] is False
    assert row["grounding_status"]["final_grounding_gate_passed"] is False
    assert row["final_route"] != "clean_catalog"


def test_repair_adjudicator_returns_full_patch():
    patched = base_row(transmission=None, fields_left_unresolved=["transmission"], grounding_summary="Transmission unresolved.", final_route="review_queue", publishable_to_clean_catalog=False)
    row, _ = final_seal(patched, repair_result={"repair_decision":"patched","patched_variant":patched,"field_patches":[{"field":"transmission"}]})
    assert row["transmission"] is None
    assert row["final_route"] == "review_queue"
    assert "Transmission unresolved" not in row["grounding_summary"] or row["publishable_to_clean_catalog"] is False


def test_final_seal_overrides_bad_repair():
    bad = base_row(canonical_trim=None, trim_status="unresolved", final_route="clean_catalog", publishable_to_clean_catalog=True)
    row, _ = final_seal(bad, repair_result={"repair_decision":"patched"}, require_gpt54_grounding_for_repair=False)
    assert row["publishable_to_clean_catalog"] is False
    assert row["final_route"] in {"partial_queue", "review_queue"}


def test_evidence_auditability_weak_blocks_clean_exact_publish():
    row, _ = final_seal(base_row(evidence_auditability="weak"))
    assert row["publishable_to_clean_catalog"] is False
    assert row["final_route"] != "clean_catalog"


def test_field_validation_low_confidence_blocks_publish():
    row = base_row()
    row["field_validation"]["transmission"]["confidence"] = 0.4
    sealed, _ = final_seal(row)
    assert sealed["publishable_to_clean_catalog"] is False
    assert sealed["final_route"] != "clean_catalog"


def test_preflight_tags():
    tags = compute_preflight_risk_tags({"trim":"Base / Standard", "year_end": 2099})
    assert "placeholder_trim" in tags
    assert "multi_trim_string" in tags
    assert "current_or_future_year_end_placeholder" in tags
