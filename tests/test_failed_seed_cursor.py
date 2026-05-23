"""Tests for failed-seed cursor advancement bug fix.

Covers:
  - FAIL_TRANSIENT advances cursor (next_seed_id never equals failed seed)
  - repair_cursor fixes next_seed_id_in_failed
  - failed seed does not become processed
  - variants unchanged after failed decision
  - audit fails if next_seed_id is in failed_seed_ids
"""
from __future__ import annotations

import copy

import pytest

from engine.apply import apply_decision, advance_cursor
from engine.audit import audit_canonical
from engine.state import repair_cursor, seed_id_from_seed
from engine.types import Decision


SEEDS = [
    {"make": "mg", "model": "mg4", "year_start": 2022, "year_end": 2026, "market": "il"},
    {"make": "mg", "model": "zs", "year_start": 2020, "year_end": 2025, "market": "il"},
    {"make": "mg", "model": "hs", "year_start": 2021, "year_end": 2026, "market": "il"},
]

SEED_IDS = [seed_id_from_seed(s) for s in SEEDS]


def _make_canonical(next_seed_id=None):
    return {
        "verified_variants": [
            {"variant_id": "v1", "make": "Existing", "model": "Car", "verification_status": "verified"}
        ],
        "partial_variants": [],
        "batch_state": {
            "processed_seed_ids": [],
            "manual_review_seed_ids": [],
            "failed_seed_ids": [],
            "seed_accounting": {},
            "next_seed_id": next_seed_id or SEED_IDS[0],
            "last_completed_seed_id": None,
        },
        "counts": {"total_variants": 1},
    }


class TestFailTransientCursorAdvancement:
    """FAIL_TRANSIENT must advance cursor past the failed seed."""

    def test_fail_transient_advances_cursor(self):
        """After FAIL_TRANSIENT, advance_cursor moves to next unhandled seed."""
        canonical = _make_canonical(next_seed_id=SEED_IDS[0])
        decision = Decision(
            action="FAIL_TRANSIENT",
            seed_id=SEED_IDS[0],
            reason="api_error",
            warnings=["timeout"],
        )
        apply_decision(canonical, decision, is_current_next=True)
        # Now advance cursor
        new_next = advance_cursor(canonical, SEEDS, SEED_IDS[0])
        assert new_next == SEED_IDS[1]
        assert canonical["batch_state"]["next_seed_id"] == SEED_IDS[1]

    def test_failed_seed_cannot_remain_next_seed_id(self):
        """next_seed_id must never equal a seed in failed_seed_ids."""
        canonical = _make_canonical(next_seed_id=SEED_IDS[0])
        decision = Decision(
            action="FAIL_TRANSIENT",
            seed_id=SEED_IDS[0],
            reason="api_error",
        )
        apply_decision(canonical, decision, is_current_next=True)
        advance_cursor(canonical, SEEDS, SEED_IDS[0])

        bs = canonical["batch_state"]
        assert SEED_IDS[0] in bs["failed_seed_ids"]
        assert bs["next_seed_id"] != SEED_IDS[0]
        assert bs["next_seed_id"] not in bs["failed_seed_ids"]

    def test_failed_seed_not_in_processed(self):
        """FAIL_TRANSIENT must not add seed to processed_seed_ids."""
        canonical = _make_canonical(next_seed_id=SEED_IDS[0])
        decision = Decision(
            action="FAIL_TRANSIENT",
            seed_id=SEED_IDS[0],
            reason="api_error",
        )
        apply_decision(canonical, decision, is_current_next=True)
        assert SEED_IDS[0] not in canonical["batch_state"]["processed_seed_ids"]
        assert SEED_IDS[0] in canonical["batch_state"]["failed_seed_ids"]

    def test_variants_unchanged_after_fail(self):
        """FAIL_TRANSIENT must not modify variants."""
        canonical = _make_canonical(next_seed_id=SEED_IDS[0])
        variants_before = copy.deepcopy(
            canonical["verified_variants"] + canonical["partial_variants"]
        )
        decision = Decision(
            action="FAIL_TRANSIENT",
            seed_id=SEED_IDS[0],
            reason="api_error",
        )
        apply_decision(canonical, decision, is_current_next=True)
        variants_after = canonical["verified_variants"] + canonical["partial_variants"]
        assert variants_after == variants_before


class TestRepairCursor:
    """repair_cursor must fix next_seed_id when it points to a handled seed."""

    def test_repair_fixes_next_seed_id_in_failed(self):
        """If next_seed_id is in failed_seed_ids, repair must advance it."""
        canonical = _make_canonical(next_seed_id=SEED_IDS[0])
        canonical["batch_state"]["failed_seed_ids"] = [SEED_IDS[0]]
        canonical["batch_state"]["last_completed_seed_id"] = SEED_IDS[0]

        result = repair_cursor(canonical, SEEDS)

        assert result["new_next_seed_id"] == SEED_IDS[1]
        assert canonical["batch_state"]["next_seed_id"] == SEED_IDS[1]
        assert canonical["batch_state"]["next_seed_id"] not in canonical["batch_state"]["failed_seed_ids"]

    def test_repair_fixes_next_seed_id_in_processed(self):
        """If next_seed_id is in processed_seed_ids, repair must advance it."""
        canonical = _make_canonical(next_seed_id=SEED_IDS[0])
        canonical["batch_state"]["processed_seed_ids"] = [SEED_IDS[0]]
        canonical["batch_state"]["last_completed_seed_id"] = SEED_IDS[0]

        result = repair_cursor(canonical, SEEDS)
        assert result["new_next_seed_id"] == SEED_IDS[1]
        assert canonical["batch_state"]["next_seed_id"] not in canonical["batch_state"]["processed_seed_ids"]

    def test_repair_fixes_next_seed_id_in_manual_review(self):
        """If next_seed_id is in manual_review_seed_ids, repair must advance it."""
        canonical = _make_canonical(next_seed_id=SEED_IDS[0])
        canonical["batch_state"]["manual_review_seed_ids"] = [SEED_IDS[0]]
        canonical["batch_state"]["last_completed_seed_id"] = SEED_IDS[0]

        result = repair_cursor(canonical, SEEDS)
        assert result["new_next_seed_id"] == SEED_IDS[1]
        assert canonical["batch_state"]["next_seed_id"] not in canonical["batch_state"]["manual_review_seed_ids"]

    def test_repair_preserves_variants(self):
        """repair_cursor must never modify variants."""
        canonical = _make_canonical(next_seed_id=SEED_IDS[0])
        canonical["batch_state"]["failed_seed_ids"] = [SEED_IDS[0]]
        canonical["batch_state"]["last_completed_seed_id"] = SEED_IDS[0]
        variants_before = copy.deepcopy(
            canonical["verified_variants"] + canonical["partial_variants"]
        )

        repair_cursor(canonical, SEEDS)

        variants_after = canonical["verified_variants"] + canonical["partial_variants"]
        assert variants_after == variants_before

    def test_repair_all_handled_returns_none(self):
        """If all seeds are handled, next_seed_id should be None."""
        canonical = _make_canonical()
        canonical["batch_state"]["processed_seed_ids"] = [SEED_IDS[1]]
        canonical["batch_state"]["failed_seed_ids"] = [SEED_IDS[0]]
        canonical["batch_state"]["manual_review_seed_ids"] = [SEED_IDS[2]]
        canonical["batch_state"]["last_completed_seed_id"] = SEED_IDS[2]

        result = repair_cursor(canonical, SEEDS)
        assert result["new_next_seed_id"] is None
        assert canonical["batch_state"]["next_seed_id"] is None


class TestAuditBlocksFailedNext:
    """Audit must reject next_seed_id in failed_seed_ids."""

    def test_audit_fails_next_in_failed(self):
        """Audit must produce next_seed_id_in_failed error."""
        canonical = _make_canonical(next_seed_id=SEED_IDS[0])
        canonical["batch_state"]["failed_seed_ids"] = [SEED_IDS[0]]
        canonical["batch_state"]["last_completed_seed_id"] = SEED_IDS[0]

        ok, errors = audit_canonical(canonical)
        assert ok is False
        assert any("next_seed_id_in_failed" in e for e in errors)

    def test_audit_passes_after_repair(self):
        """After repair_cursor, audit should pass."""
        canonical = _make_canonical(next_seed_id=SEED_IDS[0])
        canonical["batch_state"]["failed_seed_ids"] = [SEED_IDS[0]]
        canonical["batch_state"]["last_completed_seed_id"] = SEED_IDS[0]

        repair_cursor(canonical, SEEDS)

        ok, errors = audit_canonical(canonical, seed_catalog=SEEDS)
        assert ok is True, f"Audit errors: {errors}"
