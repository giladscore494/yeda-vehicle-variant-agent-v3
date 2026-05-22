"""Tests for engine/audit.py."""
import pytest
from engine.audit import audit_canonical


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
