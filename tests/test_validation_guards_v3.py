from scripts.output_writer import build_output_row
from scripts.reconcile import reconcile_validation_output_with_flags
from scripts.flash_adjudicator import FlashAdjudicator, FlashSettings


def variant(**std):
    base = {"validation_id": "VAL-X", "standard_variant": {"make": "Abarth", "model": "500", "body_type": "Cabriolet", "transmission": "manual"}}
    base["standard_variant"].update(std)
    return base


def rec(row, v=None):
    return reconcile_validation_output_with_flags(v or variant(), row)


def test_generic_base_and_standard_trim_reset():
    for trim in ("Base", "Standard"):
        row = build_output_row("VAL-X", validation_decision="clean_exact", canonical_trim=trim, trim_status="verified")
        out, flags = rec(row)
        assert out["canonical_trim"] is None
        assert out["trim_status"] == "unresolved"
        assert out["trim_confidence"] == 0.0
        assert out["validation_decision"] == "clean_partial"
        assert any(f.guard_name == "generic_trim" for f in flags)


def test_slash_trim_clean_exact_downgrades_and_split_summary_prefers_split():
    row = build_output_row("VAL-X", validation_decision="clean_exact", canonical_trim="Turismo / Competizione", grounding_summary="distinct trims with different power outputs; split is required")
    out, flags = rec(row)
    assert out["validation_decision"] == "split_required"
    assert any(f.guard_name == "slash_trim" and f.needs_adjudication for f in flags)


def test_under_consideration_clean_exact_becomes_partial():
    row = build_output_row("VAL-X", validation_decision="clean_exact", grounding_summary="Importer is evaluating and expected to arrive.", is_currently_imported_il=True)
    out, _ = rec(row)
    assert out["validation_decision"] == "clean_partial"
    assert out["identity_status"] == "likely_valid"
    assert out["is_currently_imported_il"] is None


def test_title_based_source_classification():
    cases = [("iCar Israel", "editorial"), ("Auto.co.il", "editorial"), ("Yad2 Israel", "marketplace"), ("Cartube Israel", "editorial")]
    for title, typ in cases:
        row = build_output_row("VAL-X", evidence_sources=[{"title": title, "source_type": "unknown"}])
        out, _ = rec(row)
        assert out["evidence_sources"][0]["source_type"] == typ


def test_year_end_current_true_becomes_null():
    row = build_output_row("VAL-X", year_end=2099, is_currently_produced=True)
    out, _ = rec(row)
    assert out["year_end"] is None


def test_500c_cabriolet_trim_cleanup_and_manual_guard():
    row = build_output_row("VAL-X", canonical_make="Abarth", canonical_model="500C", body_type="Cabriolet", canonical_trim="500C", transmission="manual", identity_status="verified", identity_confidence=0.95, validation_decision="clean_exact")
    out, flags = rec(row)
    assert out["canonical_trim"] is None
    assert out["trim_status"] == "unresolved"
    assert out["identity_status"] == "likely_valid"
    assert out["validation_decision"] == "clean_partial"
    assert any(f.guard_name == "domain_500c_transmission" for f in flags)


def test_reject_without_blocking_identity_issue_becomes_partial():
    row = build_output_row("VAL-X", validation_decision="reject", blocking_identity_issues=[])
    out, _ = rec(row)
    assert out["validation_decision"] == "clean_partial"


def test_official_marketed_name_unresolved_sync():
    filled = build_output_row("VAL-X", official_marketed_name_il="אבארט 500", fields_left_unresolved=["official_marketed_name_il"])
    out, _ = rec(filled)
    assert "official_marketed_name_il" not in out["fields_left_unresolved"]
    missing = build_output_row("VAL-X", official_marketed_name_il=None, identity_status="verified", fields_left_unresolved=[])
    out, _ = rec(missing)
    assert "official_marketed_name_il" in out["fields_left_unresolved"]


class RejectingFakeFlash:
    class models:
        @staticmethod
        def generate_content(**kwargs):
            class R: text = '{"adjudicated_decision":"reject","reason":"bad"}'
            return R()


def test_flash_cannot_return_reject_guard_stands():
    row = build_output_row("VAL-X", validation_decision="clean_partial", canonical_trim="Turismo / Competizione")
    _, flags = rec(build_output_row("VAL-X", validation_decision="clean_exact", canonical_trim="Turismo / Competizione"))
    adj = FlashAdjudicator(FlashSettings(api_key="x", enabled=True), client=RejectingFakeFlash())
    out = adj.adjudicate(row, flags)
    assert out["validation_decision"] == "clean_partial"
    assert out["adjudication_log"]


def test_clean_partial_slash_with_explicit_split_evidence_becomes_split_required():
    row = build_output_row(
        "VAL-X",
        canonical_trim="Competizione / Scorpione / Nuvolari S",
        split_candidates=["Competizione", "Scorpione", "Nuvolari S"],
        grounding_summary="These are distinct trims with different power outputs. A split is required.",
        validation_decision="clean_partial",
    )
    out, _ = rec(row)
    assert out["validation_decision"] == "split_required"
    assert out["acceptance_tier"] == "none"
    assert out["trim_status"] == "invalid"
    assert out["trim_confidence"] == 0.0
    assert any("Combined trim contains multiple distinct marketed trims" in issue for issue in out["non_blocking_trim_issues"])


def test_500c_manual_guard_does_not_trigger_on_abarth_500_hatchback():
    row = build_output_row(
        "VAL-X",
        canonical_make="Abarth",
        canonical_model="500",
        body_type="Hatchback",
        canonical_trim="Competizione / Scorpione / Nuvolari S",
        transmission="manual",
        identity_status="verified",
        identity_confidence=0.95,
    )
    out, _ = rec(row, variant(body_type="Hatchback"))
    issues = " ".join(out.get("non_blocking_trim_issues") or [])
    assert "500C/Cabriolet manual transmission" not in issues


def test_500c_manual_guard_triggers_on_cabriolet_body():
    row = build_output_row(
        "VAL-X",
        canonical_make="Abarth",
        canonical_model="500",
        body_type="Cabriolet",
        canonical_trim=None,
        transmission="manual",
        identity_status="verified",
        identity_confidence=0.95,
        validation_decision="clean_exact",
    )
    out, _ = rec(row)
    assert out["identity_status"] == "likely_valid"
    assert out["identity_confidence"] == 0.7
    assert out["validation_decision"] == "clean_partial"
    assert any("manual transmission is not verified" in issue for issue in out["non_blocking_trim_issues"])


def test_past_year_end_corrects_current_flags_false():
    row = build_output_row("VAL-X", year_end=2016, is_currently_produced=True, is_currently_imported_il=True)
    out, _ = rec(row)
    assert out["is_currently_produced"] is False
    assert out["is_currently_imported_il"] is False
    assert any("year_end is a past year" in issue for issue in out["non_blocking_trim_issues"])


def test_guard_corrected_reason_added_for_key_field_change():
    row = build_output_row("VAL-X", canonical_make="Abarth", canonical_model="500", body_type="Cabriolet", transmission="manual", identity_status="verified", identity_confidence=0.95, validation_decision="clean_exact")
    out, _ = rec(row)
    assert "guard_corrected_reason" in out
    assert "identity_status" in out["guard_corrected_reason"]


def test_israeli_market_year_start_guard_updates_clear_later_year():
    row = build_output_row(
        "VAL-X",
        year_start=2008,
        grounding_summary="officially imported to Israel starting in 2010",
        decision_reason="global launch was earlier",
    )
    out, flags = rec(row)
    assert out["year_start"] == 2010
    assert any(c["field"] == "year_start" and c["from"] == 2008 and c["to"] == 2010 for c in out["fields_changed"])
    assert any(f.guard_name == "year_start_il_market" for f in flags)


def test_israeli_market_year_start_guard_ignores_vague_evidence():
    row = build_output_row("VAL-X", year_start=2008, grounding_summary="imported to Israel around the early 2010s")
    out, _ = rec(row)
    assert out["year_start"] == 2008


def test_girafa_source_remains_editorial_with_official_import_support():
    row = build_output_row(
        "VAL-X",
        evidence_sources=[{"source_name": "Girafa", "title": "סמלת משיקה", "source_type": "official_importer", "supports": ["official_import_il"]}],
    )
    out, _ = rec(row)
    src = out["evidence_sources"][0]
    assert src["source_type"] == "editorial"
    assert "official_import_il" in src["supports"]


def test_fields_changed_strings_are_normalized_to_objects():
    row = build_output_row("VAL-X", fields_changed=["year_start"])
    out, _ = rec(row)
    assert all(isinstance(item, dict) for item in out["fields_changed"])
