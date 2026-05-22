"""Tests for engine/audit.py."""
import copy
import pytest
from engine.audit import audit_canonical
from engine.state import repair_cursor


def _make_valid_canonical():
    return {
        "verified_variants": [
            {"variant_id": "v1", "make": "BMW", "model": "3", "verification_status": "verified"}
        ],
        "partial_variants": [],
        "batch_state": {
            "processed_seed_ids": ["bmw__3__2020__2026__il"],
            "manual_review_seed_ids": [],
            "failed_seed_ids": [],
            "last_completed_seed_id": "bmw__3__2020__2026__il",
            "seed_accounting": {
                "bmw__3__2020__2026__il": {
                    "status": "resolved",
                    "resolution_type": "variants_added",
                    "added_count": 1,
                }
            },
        },
        "counts": {"total_variants": 1},
    }


class TestAudit:
    def test_valid_canonical_passes(self):
        ok, errs = audit_canonical(_make_valid_canonical())
        assert ok is True
        assert errs == []

    def test_rejects_processed_zero_variant_placeholder_proof(self):
        canonical = _make_valid_canonical()
        canonical["batch_state"]["processed_seed_ids"].append("creta__seed")
        canonical["batch_state"]["seed_accounting"]["creta__seed"] = {
            "status": "resolved",
            "resolution_type": "no_variants_proven",
            "proof_status": "proven",
            "source_ids": ["src_1", "src_2"],
            "source_basis": "Not sold",
        }
        ok, errs = audit_canonical(canonical)
        assert ok is False
        assert any("placeholder" in e for e in errs)

    def test_rejects_proven_zvr_with_src_1(self):
        """Regression: Creta-style bug."""
        canonical = _make_valid_canonical()
        canonical["batch_state"]["seed_accounting"]["bad_seed"] = {
            "zero_variant_resolution": {
                "proof_status": "proven",
                "source_ids": ["src_1", "src_3"],
            }
        }
        ok, errs = audit_canonical(canonical)
        assert ok is False
        assert any("placeholder_sources_in_proven_zvr" in e for e in errs)

    def test_passes_manual_review_unresolved(self):
        canonical = _make_valid_canonical()
        canonical["batch_state"]["manual_review_seed_ids"] = ["unresolved_seed"]
        canonical["batch_state"]["seed_accounting"]["unresolved_seed"] = {
            "status": "manual_review",
            "reason": "insufficient_data",
        }
        ok, errs = audit_canonical(canonical)
        assert ok is True

    def test_fails_same_seed_multiple_buckets(self):
        canonical = _make_valid_canonical()
        canonical["batch_state"]["manual_review_seed_ids"] = ["bmw__3__2020__2026__il"]
        ok, errs = audit_canonical(canonical)
        assert ok is False
        assert any("both_processed_and_manual" in e for e in errs)

    def test_fails_duplicate_in_bucket(self):
        canonical = _make_valid_canonical()
        canonical["batch_state"]["processed_seed_ids"] = [
            "bmw__3__2020__2026__il",
            "bmw__3__2020__2026__il",
        ]
        ok, errs = audit_canonical(canonical)
        assert ok is False
        assert any("duplicate" in e for e in errs)

    def test_count_mismatch(self):
        canonical = _make_valid_canonical()
        canonical["counts"]["total_variants"] = 999
        ok, errs = audit_canonical(canonical)
        assert ok is False
        assert any("mismatch" in e for e in errs)

    def test_il_confirmed_placeholder_sources_is_warning(self):
        """IL-confirmed with placeholder sources is a warning, not a blocking error."""
        canonical = _make_valid_canonical()
        canonical["verified_variants"].append({
            "variant_id": "v2",
            "make": "Test",
            "model": "Test",
            "market_scope": "IL-confirmed",
            "source_ids": ["src_1"],
        })
        canonical["counts"]["total_variants"] = 2
        ok, errs = audit_canonical(canonical)
        # Should pass — il_confirmed_placeholder is a warning, not blocking
        assert ok is True

    def test_new_il_confirmed_placeholder_is_hard_error(self):
        """Newly added IL-confirmed variant with placeholder sources MUST block save."""
        canonical = _make_valid_canonical()
        canonical["verified_variants"].append({
            "variant_id": "v_new",
            "make": "Test",
            "model": "Test",
            "market_scope": "IL-confirmed",
            "source_ids": ["src_1"],
        })
        canonical["counts"]["total_variants"] = 2
        ok, errs = audit_canonical(
            canonical, newly_added_variant_ids=["v_new"],
        )
        assert ok is False
        assert any("new_il_confirmed_placeholder_sources" in e for e in errs)

    def test_new_il_confirmed_with_real_sources_passes(self):
        """Newly added IL-confirmed variant with real sources should pass."""
        canonical = _make_valid_canonical()
        canonical["verified_variants"].append({
            "variant_id": "v_new",
            "make": "Test",
            "model": "Test",
            "market_scope": "IL-confirmed",
            "source_ids": ["ministry_transport_il_2023"],
        })
        canonical["counts"]["total_variants"] = 2
        ok, errs = audit_canonical(
            canonical, newly_added_variant_ids=["v_new"],
        )
        assert ok is True

    def test_rejects_variants_added_zero_mutation(self):
        """Accounting with resolution_type=variants_added but 0 added + 0 merged must fail."""
        canonical = _make_valid_canonical()
        canonical["batch_state"]["seed_accounting"]["zero_mut_seed"] = {
            "status": "resolved",
            "resolution_type": "variants_added",
            "added_count": 0,
            "merged_count": 0,
        }
        canonical["batch_state"]["processed_seed_ids"].append("zero_mut_seed")
        ok, errs = audit_canonical(canonical)
        assert ok is False
        assert any("accept_variants_zero_mutation" in e for e in errs)

    def test_passes_variants_added_with_mutations(self):
        """Accounting with resolution_type=variants_added and positive counts should pass."""
        canonical = _make_valid_canonical()
        # The existing entry already has added_count=1, so it should pass
        ok, errs = audit_canonical(canonical)
        assert ok is True


# ---------------------------------------------------------------------------
# Helper: build a minimal seed catalog for cursor tests
# ---------------------------------------------------------------------------

def _make_seed(make: str, model: str, ys: int = 2020, ye: int = 2026) -> dict:
    return {"make": make, "model": model, "year_start": ys, "year_end": ye, "market": "il"}


def _seed_id(make: str, model: str, ys: int = 2020, ye: int = 2026) -> str:
    return f"{make.lower()}__{model.lower()}__{ys}__{ye}__il"


_CATALOG = [
    _make_seed("Alpha", "A1"),
    _make_seed("Alpha", "A2"),
    _make_seed("Beta", "B1"),
    _make_seed("Gamma", "G1"),
    _make_seed("Delta", "D1"),
]

_CATALOG_IDS = [_seed_id(s["make"], s["model"]) for s in _CATALOG]


def _make_canonical_with_cursor(
    processed_ids: list[str],
    manual_ids: list[str] | None = None,
    failed_ids: list[str] | None = None,
    next_seed_id: str | None = None,
    last_completed_seed_id: str | None = None,
) -> dict:
    """Build a minimal canonical with cursor fields for testing."""
    return {
        "verified_variants": [
            {"variant_id": "v1", "make": "BMW", "model": "3", "verification_status": "verified"}
        ],
        "partial_variants": [],
        "batch_state": {
            "processed_seed_ids": list(processed_ids),
            "manual_review_seed_ids": list(manual_ids or []),
            "failed_seed_ids": list(failed_ids or []),
            "next_seed_id": next_seed_id,
            "last_completed_seed_id": last_completed_seed_id,
            "seed_accounting": {
                sid: {"status": "resolved", "resolution_type": "variants_added",
                      "added_count": 1, "merged_count": 0}
                for sid in processed_ids
            },
        },
        "counts": {"total_variants": 1},
    }


class TestCursorAuditRule:
    """Audit must reject next_seed_id that is already processed/manual/failed."""

    def test_next_seed_already_processed_fails_audit(self):
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[0], _CATALOG_IDS[1]],
            next_seed_id=_CATALOG_IDS[1],  # already processed
            last_completed_seed_id=_CATALOG_IDS[0],
        )
        ok, errs = audit_canonical(canonical)
        assert ok is False
        assert any("next_seed_id_already_processed" in e for e in errs)

    def test_next_seed_in_manual_fails_audit(self):
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[0]],
            manual_ids=[_CATALOG_IDS[1]],
            next_seed_id=_CATALOG_IDS[1],
        )
        ok, errs = audit_canonical(canonical)
        assert ok is False
        assert any("next_seed_id_in_manual_review" in e for e in errs)

    def test_next_seed_in_failed_fails_audit(self):
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[0]],
            failed_ids=[_CATALOG_IDS[1]],
            next_seed_id=_CATALOG_IDS[1],
        )
        ok, errs = audit_canonical(canonical)
        assert ok is False
        assert any("next_seed_id_in_failed" in e for e in errs)

    def test_next_seed_unprocessed_passes_audit(self):
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[0]],
            next_seed_id=_CATALOG_IDS[1],
            last_completed_seed_id=_CATALOG_IDS[0],
        )
        ok, errs = audit_canonical(canonical)
        assert ok is True


class TestCursorRepair:
    """repair_cursor must fix the cursor without touching variants or buckets."""

    def test_repair_advances_past_processed(self):
        """If next_seed_id points to an already-processed seed, repair fixes it."""
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[0], _CATALOG_IDS[1]],
            next_seed_id=_CATALOG_IDS[1],
            last_completed_seed_id=_CATALOG_IDS[0],
        )
        result = repair_cursor(canonical, _CATALOG)
        bs = canonical["batch_state"]

        # Contiguous prefix is [0, 1], so last_completed = CATALOG_IDS[1]
        assert bs["last_completed_seed_id"] == _CATALOG_IDS[1]
        # next = CATALOG_IDS[2] (first unhandled)
        assert bs["next_seed_id"] == _CATALOG_IDS[2]
        assert result["old_next_seed_id"] == _CATALOG_IDS[1]
        assert result["new_next_seed_id"] == _CATALOG_IDS[2]

    def test_repair_respects_gap(self):
        """If there is a gap, cursor does not jump across it."""
        # Processed: [0] and [2] — gap at [1]
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[0], _CATALOG_IDS[2]],
            next_seed_id=_CATALOG_IDS[2],
        )
        result = repair_cursor(canonical, _CATALOG)
        bs = canonical["batch_state"]

        # Contiguous prefix is [0] only, gap at [1]
        assert bs["last_completed_seed_id"] == _CATALOG_IDS[0]
        assert bs["next_seed_id"] == _CATALOG_IDS[1]

    def test_repair_skips_manual_and_failed_in_prefix(self):
        """Manual/failed seeds count as handled in the contiguous prefix."""
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[0]],
            manual_ids=[_CATALOG_IDS[1]],
            failed_ids=[_CATALOG_IDS[2]],
            next_seed_id=_CATALOG_IDS[0],
        )
        result = repair_cursor(canonical, _CATALOG)
        bs = canonical["batch_state"]

        # Contiguous prefix includes [0]=processed, [1]=manual, [2]=failed
        assert bs["last_completed_seed_id"] == _CATALOG_IDS[2]
        assert bs["next_seed_id"] == _CATALOG_IDS[3]

    def test_repair_does_not_modify_variants(self):
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[0]],
            next_seed_id=_CATALOG_IDS[0],
        )
        variants_before = copy.deepcopy(canonical["verified_variants"])
        partial_before = copy.deepcopy(canonical["partial_variants"])

        repair_cursor(canonical, _CATALOG)

        assert canonical["verified_variants"] == variants_before
        assert canonical["partial_variants"] == partial_before

    def test_repair_does_not_modify_buckets(self):
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[0], _CATALOG_IDS[1]],
            manual_ids=[_CATALOG_IDS[2]],
            failed_ids=[_CATALOG_IDS[3]],
            next_seed_id=_CATALOG_IDS[1],
        )
        proc_before = list(canonical["batch_state"]["processed_seed_ids"])
        man_before = list(canonical["batch_state"]["manual_review_seed_ids"])
        fail_before = list(canonical["batch_state"]["failed_seed_ids"])

        repair_cursor(canonical, _CATALOG)

        assert canonical["batch_state"]["processed_seed_ids"] == proc_before
        assert canonical["batch_state"]["manual_review_seed_ids"] == man_before
        assert canonical["batch_state"]["failed_seed_ids"] == fail_before

    def test_repair_all_handled(self):
        """When all catalog seeds are handled, next_seed_id should be None."""
        canonical = _make_canonical_with_cursor(
            processed_ids=list(_CATALOG_IDS),
            next_seed_id=_CATALOG_IDS[-1],
        )
        repair_cursor(canonical, _CATALOG)
        bs = canonical["batch_state"]
        assert bs["next_seed_id"] is None
        assert bs["last_completed_seed_id"] == _CATALOG_IDS[-1]

    def test_repair_none_handled(self):
        """When no seeds are handled, cursor starts at beginning."""
        canonical = _make_canonical_with_cursor(
            processed_ids=[],
            next_seed_id=_CATALOG_IDS[3],
        )
        repair_cursor(canonical, _CATALOG)
        bs = canonical["batch_state"]
        assert bs["next_seed_id"] == _CATALOG_IDS[0]
        assert bs["last_completed_seed_id"] is None

    def test_repair_no_contiguous_prefix_but_later_handled(self):
        """When first seed is unhandled but later seeds are processed,
        last_completed_seed_id must not be None."""
        # Processed: [2] and [3] — gap at start ([0] and [1] unhandled)
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[2], _CATALOG_IDS[3]],
            next_seed_id=_CATALOG_IDS[3],
        )
        repair_cursor(canonical, _CATALOG)
        bs = canonical["batch_state"]

        # next_seed_id should be [0] (first unhandled)
        assert bs["next_seed_id"] == _CATALOG_IDS[0]
        # last_completed_seed_id must NOT be None — fallback to last handled
        assert bs["last_completed_seed_id"] == _CATALOG_IDS[3]

    def test_repair_never_none_when_processed_exist(self):
        """Cursor repair never leaves last_completed_seed_id as None
        when processed seeds exist."""
        # Process only the last seed, leaving a big gap from start
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[-1]],
            next_seed_id=_CATALOG_IDS[-1],
        )
        repair_cursor(canonical, _CATALOG)
        bs = canonical["batch_state"]

        assert bs["last_completed_seed_id"] is not None
        assert bs["last_completed_seed_id"] == _CATALOG_IDS[-1]
        assert bs["next_seed_id"] == _CATALOG_IDS[0]


class TestLastCompletedAuditRule:
    """Audit must reject last_completed_seed_id=None when processed seeds exist."""

    def test_none_last_completed_with_processed_fails(self):
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[0]],
            next_seed_id=_CATALOG_IDS[1],
            last_completed_seed_id=None,
        )
        ok, errs = audit_canonical(canonical)
        assert ok is False
        assert any("last_completed_seed_id_none_with_processed_seeds" in e for e in errs)

    def test_none_last_completed_no_processed_passes(self):
        canonical = _make_canonical_with_cursor(
            processed_ids=[],
            next_seed_id=_CATALOG_IDS[0],
            last_completed_seed_id=None,
        )
        ok, errs = audit_canonical(canonical)
        assert ok is True

    def test_valid_last_completed_passes(self):
        canonical = _make_canonical_with_cursor(
            processed_ids=[_CATALOG_IDS[0]],
            next_seed_id=_CATALOG_IDS[1],
            last_completed_seed_id=_CATALOG_IDS[0],
        )
        ok, errs = audit_canonical(canonical)
        assert ok is True
