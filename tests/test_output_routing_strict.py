"""Strict output-routing regression tests.

The legacy router published any ``clean_partial`` row (even with a null trim)
straight into the clean catalog whenever rows lacked a final seal. These tests
lock the strict v4 behaviour: clean_partial never publishes, unsealed rows fall
back safely, and a mix of sealed/unsealed rows is routed row-by-row.
"""

from scripts.output_writer import route_validated_rows


def _row(vid, **kw):
    base = {
        "validation_id": vid,
        "canonical_make": "Abarth",
        "canonical_model": "500",
        "canonical_trim": None,
        "validation_decision": "clean_partial",
        "identity_status": "likely_valid",
        "trim_status": "unresolved",
        "fields_left_unresolved": ["canonical_trim"],
        "blocking_identity_issues": [],
        "split_candidates": [],
    }
    base.update(kw)
    return base


def test_never_publishes_clean_partial_without_final_seal():
    routed = route_validated_rows([_row("VAL-1")])
    assert routed[0]["publishable_to_clean_catalog"] is False
    assert routed[0]["final_route"] != "clean_catalog"


def test_never_publishes_clean_partial_with_null_trim():
    routed = route_validated_rows([_row("VAL-1", canonical_trim=None)])
    assert routed[0]["final_route"] == "partial_queue"
    assert routed[0]["publishable_to_clean_catalog"] is False


def test_strict_fallback_blocks_unsealed_clean_partial_even_if_marked_publishable():
    # An upstream/legacy row may arrive pre-marked publishable; strict routing
    # must override it.
    row = _row("VAL-1", publishable_to_clean_catalog=True, final_route="clean_catalog")
    routed = route_validated_rows([row])
    assert routed[0]["publishable_to_clean_catalog"] is False
    assert routed[0]["final_route"] != "clean_catalog"


def test_mixed_sealed_unsealed_rows_routes_each_safely():
    sealed_clean = {
        "validation_id": "VAL-SEAL",
        "canonical_make": "Abarth", "canonical_model": "595",
        "canonical_trim": "Competizione", "validation_decision": "clean_exact",
        "identity_status": "verified", "trim_status": "verified",
        "fields_left_unresolved": [], "blocking_identity_issues": [],
        "split_candidates": [],
        "publishable_to_clean_catalog": True, "final_route": "clean_catalog",
        "final_seal_result": {"passed": True, "blocks_clean_catalog": False},
    }
    unsealed_partial = _row("VAL-UNSEALED")
    routed = route_validated_rows([sealed_clean, unsealed_partial])
    by_id = {r["validation_id"]: r for r in routed}
    # Sealed authoritative clean row is preserved.
    assert by_id["VAL-SEAL"]["final_route"] == "clean_catalog"
    assert by_id["VAL-SEAL"]["publishable_to_clean_catalog"] is True
    # Unsealed partial is blocked.
    assert by_id["VAL-UNSEALED"]["publishable_to_clean_catalog"] is False
    assert by_id["VAL-UNSEALED"]["final_route"] != "clean_catalog"


def test_sealed_row_routing_is_only_made_stricter_by_duplicates():
    seal = {"passed": True, "blocks_clean_catalog": False}
    common = dict(
        canonical_make="Abarth", canonical_model="595", canonical_trim="Competizione",
        canonical_series_or_generation="1st Gen", body_type="Hatchback",
        fuel_type="petrol", engine="1.4L Turbo", transmission="manual",
        drivetrain="FWD", year_start=2016, year_end=2021, market_scope="IL",
        validation_decision="clean_exact", identity_status="verified",
        trim_status="verified", final_seal_result=seal,
        publishable_to_clean_catalog=True, final_route="clean_catalog",
    )
    rows = [
        dict(validation_id="VAL-A", **common),
        dict(validation_id="VAL-B", **common),
    ]
    routed = route_validated_rows(rows)
    by_id = {r["validation_id"]: r for r in routed}
    assert by_id["VAL-A"]["final_route"] == "clean_catalog"
    assert by_id["VAL-B"]["final_route"] == "duplicate_queue"
    assert by_id["VAL-B"]["duplicate_of"] == "VAL-A"


def test_absorb_checkpoint_preserves_repair_metadata_counters(tmp_path):
    import json
    from scripts.output_writer import OutputStore

    cp = {
        "validated_variants_by_id": {},
        "completed_validation_ids": [],
        "metadata": {
            "stage25_repair_triggered_rows": 7,
            "stage3_repair_adjudicator_calls": 4,
            "stage4_final_seal_blocks": 3,
            "clean_catalog_blocks_by_clean_partial": 2,
        },
    }
    cp_path = tmp_path / "cp.json"
    cp_path.write_text(json.dumps(cp), encoding="utf-8")
    store = OutputStore(
        output_path=str(tmp_path / "out.json"),
        checkpoint_path=str(cp_path),
        run_mode="real",
    )
    store.load_existing()
    assert store.metadata["stage25_repair_triggered_rows"] == 7
    assert store.metadata["stage3_repair_adjudicator_calls"] == 4
    assert store.metadata["stage4_final_seal_blocks"] == 3
    assert store.metadata["clean_catalog_blocks_by_clean_partial"] == 2
