"""Regression test against the real low-quality run that motivated the v4 fix.

`tests/fixtures/latest_run_sample.json` is the actual output that published
``clean_partial`` rows (with null trims) into the clean catalog and kept
combined trims as canonical values. Running those rows back through Python's
final seal + routing must now produce safe outcomes and never reproduce the
defects.
"""

import json
import os

from scripts.reconcile import final_seal
from scripts.output_writer import route_validated_rows

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "latest_run_sample.json")


def _sealed_and_routed():
    data = json.load(open(FIXTURE, encoding="utf-8"))
    sealed = []
    for raw in data["validated_variants"]:
        row, _ = final_seal(dict(raw), dict(raw), None, [])
        sealed.append(row)
    return {r["validation_id"]: r for r in route_validated_rows(sealed)}


def test_no_clean_partial_reaches_clean_catalog():
    rows = _sealed_and_routed()
    for vid, row in rows.items():
        if row.get("validation_decision") == "clean_partial":
            assert row["final_route"] != "clean_catalog", vid
            assert row["publishable_to_clean_catalog"] is False, vid


def test_no_row_publishes_with_null_or_unresolved_trim():
    rows = _sealed_and_routed()
    for vid, row in rows.items():
        if row["publishable_to_clean_catalog"]:
            assert row.get("canonical_trim") not in (None, "", []), vid
            assert "canonical_trim" not in set(row.get("fields_left_unresolved") or []), vid


def test_split_rows_have_null_canonical_trim_and_candidates():
    rows = _sealed_and_routed()
    for vid in ("VAL-000003", "VAL-000004"):
        row = rows[vid]
        assert row["validation_decision"] == "split_required", vid
        assert row["canonical_trim"] is None, vid
        assert row["final_route"] == "split_queue", vid
        assert len(row.get("split_candidates") or []) >= 2, vid


def test_unresolved_transmission_row_is_blocked():
    rows = _sealed_and_routed()
    row = rows["VAL-000005"]
    assert row["publishable_to_clean_catalog"] is False
    # transmission was flagged unresolved in the issues; it must not remain a
    # confident canonical value.
    unresolved = set(row.get("fields_left_unresolved") or [])
    assert row.get("transmission") is None or "transmission" in unresolved


def test_every_row_is_sealed_and_routed_safely():
    rows = _sealed_and_routed()
    assert len(rows) == 5
    for vid, row in rows.items():
        assert row.get("final_seal_result") is not None, vid
        assert row["final_route"] in {
            "clean_catalog", "partial_queue", "split_queue",
            "duplicate_queue", "review_queue", "rejected",
            "configurable_group_queue",
        }, vid
        # The headline defect: none of these five may publish.
        assert row["publishable_to_clean_catalog"] is False, vid
