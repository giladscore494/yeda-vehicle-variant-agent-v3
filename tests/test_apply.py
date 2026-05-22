"""Tests for engine/apply.py — apply layer."""
import copy
from engine.types import Decision
from engine.apply import apply_decision


def _make_canonical():
    return {
        "verified_variants": [],
        "partial_variants": [],
        "batch_state": {
            "processed_seed_ids": [],
            "manual_review_seed_ids": [],
            "failed_seed_ids": [],
            "seed_accounting": {},
            "next_seed_id": "test__model__2020__2026__il",
        },
    }


class TestApply:
    def test_accept_adds_and_marks_processed(self):
        canonical = _make_canonical()
        decision = Decision(
            action="ACCEPT_VARIANTS",
            seed_id="test__model__2020__2026__il",
            reason="valid",
            variants_to_add=[{"variant_id": "v1", "make": "Test", "model": "Model"}],
        )
        stats = apply_decision(canonical, decision)
        assert stats["added_count"] == 1
        assert "test__model__2020__2026__il" in canonical["batch_state"]["processed_seed_ids"]

    def test_close_no_variants_marks_processed(self):
        canonical = _make_canonical()
        decision = Decision(
            action="CLOSE_NO_VARIANTS_PROVEN",
            seed_id="test__model__2020__2026__il",
            reason="proven",
            proof={"proof_status": "proven", "source_ids": ["real_src"], "source_basis": "text", "confidence": "high"},
        )
        stats = apply_decision(canonical, decision)
        assert stats["added_count"] == 0
        assert "test__model__2020__2026__il" in canonical["batch_state"]["processed_seed_ids"]
        acct = canonical["batch_state"]["seed_accounting"]["test__model__2020__2026__il"]
        assert acct["resolution_type"] == "no_variants_proven"

    def test_manual_review_does_not_mark_processed(self):
        canonical = _make_canonical()
        decision = Decision(
            action="MANUAL_REVIEW",
            seed_id="test__model__2020__2026__il",
            reason="placeholder_proof",
        )
        apply_decision(canonical, decision)
        assert "test__model__2020__2026__il" not in canonical["batch_state"]["processed_seed_ids"]
        assert "test__model__2020__2026__il" in canonical["batch_state"]["manual_review_seed_ids"]

    def test_manual_review_does_not_block_next(self):
        """Manual review does not prevent advancing to next seed."""
        canonical = _make_canonical()
        canonical["batch_state"]["next_seed_id"] = "other__seed__2020__2026__il"
        decision = Decision(
            action="MANUAL_REVIEW",
            seed_id="test__model__2020__2026__il",
            reason="placeholder_proof",
        )
        apply_decision(canonical, decision)
        # next_seed_id should not be changed by manual review
        assert canonical["batch_state"]["next_seed_id"] == "other__seed__2020__2026__il"

    def test_fail_transient_does_not_mark_processed(self):
        canonical = _make_canonical()
        decision = Decision(
            action="FAIL_TRANSIENT",
            seed_id="test__model__2020__2026__il",
            reason="api_error",
            warnings=["timeout"],
        )
        apply_decision(canonical, decision)
        assert "test__model__2020__2026__il" not in canonical["batch_state"]["processed_seed_ids"]
        assert "test__model__2020__2026__il" in canonical["batch_state"]["failed_seed_ids"]

    def test_accept_removes_from_manual_review(self):
        canonical = _make_canonical()
        canonical["batch_state"]["manual_review_seed_ids"] = ["test__model__2020__2026__il"]
        decision = Decision(
            action="ACCEPT_VARIANTS",
            seed_id="test__model__2020__2026__il",
            reason="valid",
            variants_to_add=[{"variant_id": "v1", "make": "Test", "model": "Model"}],
        )
        apply_decision(canonical, decision)
        assert "test__model__2020__2026__il" not in canonical["batch_state"]["manual_review_seed_ids"]
        assert "test__model__2020__2026__il" in canonical["batch_state"]["processed_seed_ids"]

    def test_merge_does_not_overwrite_rich_data(self):
        canonical = _make_canonical()
        canonical["verified_variants"] = [{
            "variant_id": "v1",
            "make": "BMW",
            "model": "3 Series",
            "engine": "2.0L turbo",
            "verification_status": "verified",
        }]
        decision = Decision(
            action="ACCEPT_VARIANTS",
            seed_id="test__model__2020__2026__il",
            reason="valid",
            variants_to_add=[{"variant_id": "v1", "make": "BMW", "model": "3 Series", "engine": ""}],
        )
        stats = apply_decision(canonical, decision)
        assert stats["merged_count"] == 1
        # Engine should still be "2.0L turbo" — not overwritten with empty
        all_v = canonical["verified_variants"] + canonical["partial_variants"]
        v1 = [v for v in all_v if v.get("variant_id") == "v1"][0]
        assert v1["engine"] == "2.0L turbo"
