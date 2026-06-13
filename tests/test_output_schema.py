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
