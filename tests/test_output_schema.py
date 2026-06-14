from scripts.output_writer import (
    DECISION_TIER,
    build_output_row,
    empty_output_row,
    enforce_consistency,
    validate_output_row,
)


def test_empty_row_has_all_fields_and_is_valid():
    row = empty_output_row("VAL-000000")
    assert not validate_output_row(row)
    assert row["validation_id"] == "VAL-000000"
    assert row["market_scope"] == "IL"


def test_decision_drives_acceptance_tier():
    for decision, tier in DECISION_TIER.items():
        row = build_output_row("VAL-1", validation_decision=decision)
        assert row["acceptance_tier"] == tier
        assert not validate_output_row(row)


def test_validation_id_always_preserved_and_backfilled():
    # Overrides may try to blank source_validation_id; the id is preserved
    # and source_validation_id is backfilled from it.
    row = build_output_row("VAL-123", canonical_make="X", source_validation_id="")
    assert row["validation_id"] == "VAL-123"
    assert row["source_validation_id"] == "VAL-123"


def test_enforce_consistency_clamps_confidence_and_enums():
    row = empty_output_row("VAL-1")
    row["identity_confidence"] = 5.0
    row["trim_confidence"] = -2.0
    row["identity_status"] = "bogus"
    row["trim_status"] = "bogus"
    row = enforce_consistency(row)
    assert row["identity_confidence"] == 1.0
    assert row["trim_confidence"] == 0.0
    assert row["identity_status"] == "uncertain"
    assert row["trim_status"] == "unresolved"


def test_weak_trim_partial_shape():
    row = build_output_row(
        "VAL-1",
        validation_decision="clean_partial",
        trim_status="unresolved",
    )
    assert row["validation_decision"] == "clean_partial"
    assert row["acceptance_tier"] == "partial"
    assert row["trim_status"] == "unresolved"


def test_final_routing_and_duplicates():
    from scripts.output_writer import route_validated_rows

    # The clean_exact anchor must satisfy the strict catalog gate (verified
    # identity + trim, grounded, gate passed) to legitimately publish.
    clean_anchor = build_output_row(
        "VAL-1", canonical_make="Abarth", canonical_model="500", canonical_trim="Turismo",
        validation_decision="clean_exact", identity_status="verified", trim_status="verified",
        evidence_auditability="acceptable",
    )
    clean_anchor["grounding_status"] = {"gemini_grounding_required": True, "gemini_grounding_present": True, "gemini_grounding_quality": "acceptable", "gpt54_grounding_required": False, "gpt54_grounding_present": False, "gpt54_grounding_quality": "missing", "final_grounding_gate_passed": True}
    rows = [
        clean_anchor,
        build_output_row("VAL-2", canonical_make="Abarth", canonical_model="500", canonical_trim="Turismo", validation_decision="clean_partial", identity_status="likely_valid"),
        build_output_row("VAL-3", validation_decision="split_required"),
        build_output_row("VAL-4", validation_decision="reject"),
    ]
    routed = route_validated_rows(rows)
    assert routed[0]["final_route"] == "clean_catalog"
    assert routed[0]["publishable_to_clean_catalog"] is True
    assert routed[1]["final_route"] == "duplicate_queue"
    assert routed[1]["duplicate_of"] == "VAL-1"
    assert routed[2]["final_route"] == "split_queue"
    assert routed[2]["publishable_to_clean_catalog"] is False
    assert routed[3]["final_route"] == "rejected"
