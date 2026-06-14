"""Deterministic guard + final-seal consequence tests (v4)."""

from scripts.reconcile import (
    apply_deterministic_quality_guards,
    assess_grounding,
    final_seal,
    is_temporary_grounding_redirect,
)


def _seal(row):
    sealed, flags = final_seal(dict(row), dict(row), None, [])
    return sealed


def test_combined_canonical_trim_is_cleared_to_null():
    row = {
        "validation_id": "VAL-1", "canonical_make": "Abarth", "canonical_model": "500",
        "canonical_trim": "Turismo / Competizione", "validation_decision": "clean_exact",
        "identity_status": "verified", "trim_status": "verified",
    }
    sealed = _seal(row)
    assert sealed["validation_decision"] == "split_required"
    assert sealed["canonical_trim"] is None
    assert sealed["final_route"] == "split_queue"
    assert sealed["publishable_to_clean_catalog"] is False


def test_combined_trim_derives_split_candidates_when_missing():
    flags = []
    row = {
        "canonical_trim": "Competizione / Scorpione / Nuvolari S",
        "fields_left_unresolved": [], "field_validation": {},
    }
    apply_deterministic_quality_guards(row, flags)
    assert row["canonical_trim"] is None
    assert row["split_candidates"] == ["Competizione", "Scorpione", "Nuvolari S"]


def test_unresolved_transmission_text_nullifies_field():
    row = {
        "validation_id": "VAL-1", "canonical_make": "Abarth", "canonical_model": "500",
        "canonical_trim": None, "transmission": "manual",
        "validation_decision": "clean_partial", "identity_status": "likely_valid",
        "trim_status": "unresolved",
        "non_blocking_trim_issues": [
            "Abarth 500C manual transmission is not verified for the Israeli market; transmission left unresolved.",
        ],
    }
    sealed = _seal(row)
    unresolved = set(sealed.get("fields_left_unresolved") or [])
    assert sealed.get("transmission") is None or "transmission" in unresolved
    assert sealed["publishable_to_clean_catalog"] is False


def test_vertex_redirect_only_evidence_is_not_strong():
    assert is_temporary_grounding_redirect(
        "https://vertexaisearch.cloud.google.com/grounding-api-redirect/ABC"
    )
    row = {
        "evidence_auditability": "strong",
        "evidence_sources": [
            {"url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/ABC"},
            {"url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/DEF"},
        ],
    }
    gs = assess_grounding(row, require_gemini=True)
    assert gs["gemini_grounding_present"] is True
    assert gs["gemini_grounding_quality"] != "strong"


def test_stable_url_can_remain_strong():
    row = {
        "evidence_auditability": "strong",
        "evidence_sources": [{"url": "https://www.auto.co.il/article/123"}],
    }
    gs = assess_grounding(row, require_gemini=True)
    assert gs["gemini_grounding_quality"] == "strong"


def test_field_validation_missing_defaults_to_unresolved_and_blocks():
    row = {
        "validation_id": "VAL-1", "canonical_make": "Abarth", "canonical_model": "500",
        "canonical_trim": "Competizione", "validation_decision": "clean_exact",
        "identity_status": "verified", "trim_status": "verified",
        "engine": "1.4L Turbo", "transmission": "manual",
        # No field_validation, no source_support_matrix -> cannot verify.
    }
    sealed = _seal(row)
    assert sealed["publishable_to_clean_catalog"] is False
    assert sealed["final_route"] != "clean_catalog"


def test_summary_current_status_contradiction_rewritten():
    row = {
        "validation_id": "VAL-1", "canonical_make": "Abarth", "canonical_model": "500",
        "canonical_trim": "Competizione", "validation_decision": "clean_exact",
        "identity_status": "verified", "trim_status": "verified",
        "is_currently_produced": False, "is_currently_imported_il": False,
        "grounding_summary": "The model is still currently imported and sold in Israel.",
    }
    sealed = _seal(row)
    assert "currently" not in sealed["grounding_summary"].lower()
