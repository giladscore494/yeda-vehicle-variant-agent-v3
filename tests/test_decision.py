"""Tests for engine/decision.py — decision rules."""
import pytest
from engine.types import SeedRunResult, Decision
from engine.decision import decide_seed_result


def _make_result(**kwargs) -> SeedRunResult:
    defaults = {"seed_id": "test__model__2020__2026__il", "ok": True}
    defaults.update(kwargs)
    return SeedRunResult(**defaults)


class TestDecisionRules:
    def test_candidates_accept(self):
        result = _make_result(
            candidate_variants=[{"make": "BMW", "model": "3 Series", "variant_id": "v1"}]
        )
        decision = decide_seed_result(result)
        assert decision.action == "ACCEPT_VARIANTS"
        assert len(decision.variants_to_add) == 1

    def test_zero_candidates_with_real_proof_closes(self):
        result = _make_result(
            candidate_variants=[],
            no_variants_reason="model_not_sold_in_market",
            no_variants_source_ids=["ministry_transport_il_2023"],
            no_variants_source_basis="Ministry of Transport IL confirms no registration",
            no_variants_confidence="high",
            sources=[{"source_id": "ministry_transport_il_2023", "url": "https://example.com"}],
        )
        decision = decide_seed_result(result)
        assert decision.action == "CLOSE_NO_VARIANTS_PROVEN"
        assert decision.proof is not None
        assert decision.proof["proof_status"] == "proven"

    def test_zero_candidates_with_placeholder_proof_manual_review(self):
        """Creta/Geely-style bug: placeholder source IDs must NOT close."""
        result = _make_result(
            candidate_variants=[],
            no_variants_reason="model_not_sold_in_market",
            no_variants_source_ids=["src_1", "src_2"],
            no_variants_source_basis="Not found in market",
            no_variants_confidence="high",
        )
        decision = decide_seed_result(result)
        assert decision.action == "MANUAL_REVIEW"
        assert decision.proof is None

    def test_zero_candidates_no_proof_manual_review(self):
        result = _make_result(
            candidate_variants=[],
            no_variants_reason="model_not_sold_in_market",
            no_variants_source_ids=[],
            no_variants_source_basis="",
            no_variants_confidence=None,
        )
        decision = decide_seed_result(result)
        assert decision.action == "MANUAL_REVIEW"

    def test_insufficient_data_manual_review(self):
        result = _make_result(
            candidate_variants=[],
            no_variants_reason="insufficient_grounded_data",
        )
        decision = decide_seed_result(result)
        assert decision.action == "MANUAL_REVIEW"

    def test_source_conflict_manual_review(self):
        result = _make_result(
            candidate_variants=[],
            no_variants_reason="source_conflict_unresolved",
        )
        decision = decide_seed_result(result)
        assert decision.action == "MANUAL_REVIEW"

    def test_runner_failed_transient(self):
        result = _make_result(ok=False, errors=["API timeout"])
        decision = decide_seed_result(result)
        assert decision.action == "FAIL_TRANSIENT"
        assert "API timeout" in decision.warnings

    def test_empty_result_manual_review(self):
        result = _make_result(candidate_variants=[], no_variants_reason=None)
        decision = decide_seed_result(result)
        assert decision.action == "MANUAL_REVIEW"
        assert decision.reason == "unresolved_or_empty_result"

    def test_low_confidence_proof_manual_review(self):
        result = _make_result(
            candidate_variants=[],
            no_variants_reason="model_not_sold_in_market",
            no_variants_source_ids=["real_source_id"],
            no_variants_source_basis="Some basis",
            no_variants_confidence="low",
            sources=[{"source_id": "real_source_id"}],
        )
        decision = decide_seed_result(result)
        assert decision.action == "MANUAL_REVIEW"

    def test_source_id_not_in_sources_manual_review(self):
        result = _make_result(
            candidate_variants=[],
            no_variants_reason="model_not_sold_in_market",
            no_variants_source_ids=["nonexistent_source"],
            no_variants_source_basis="Some basis",
            no_variants_confidence="high",
            sources=[{"source_id": "other_source"}],
        )
        decision = decide_seed_result(result)
        assert decision.action == "MANUAL_REVIEW"


class TestVariantIdEnrichment:
    """Tests for variant_id generation in the decision layer."""

    def test_candidate_without_variant_id_gets_one(self):
        """Candidate with required fields but no variant_id gets deterministic variant_id."""
        result = _make_result(
            candidate_variants=[{
                "make": "Volkswagen", "model": "Jetta",
                "year_start": 2019, "year_end": 2024,
                "body_type": "sedan", "engine": "1.4 TSI",
                "transmission": "automatic", "fuel_type": "petrol",
            }]
        )
        decision = decide_seed_result(result)
        assert decision.action == "ACCEPT_VARIANTS"
        assert len(decision.variants_to_add) == 1
        assert decision.variants_to_add[0].get("variant_id")
        assert "volkswagen" in decision.variants_to_add[0]["variant_id"]

    def test_candidate_with_existing_variant_id_preserved(self):
        """Candidate that already has variant_id keeps it unchanged."""
        result = _make_result(
            candidate_variants=[{
                "variant_id": "my_custom_id",
                "make": "BMW", "model": "3 Series",
                "year_start": 2020, "year_end": 2025,
            }]
        )
        decision = decide_seed_result(result)
        assert decision.action == "ACCEPT_VARIANTS"
        assert decision.variants_to_add[0]["variant_id"] == "my_custom_id"

    def test_seven_candidates_without_variant_id_all_enriched(self):
        """ACCEPT_VARIANTS with 7 candidates missing variant_id no longer results in zero mutation."""
        candidates = []
        for i in range(7):
            candidates.append({
                "make": "Volkswagen", "model": "Jetta",
                "year_start": 2019 + i, "year_end": 2020 + i,
                "body_type": "sedan", "engine": f"1.{i} TSI",
                "transmission": "automatic", "fuel_type": "petrol",
            })
        result = _make_result(candidate_variants=candidates)
        decision = decide_seed_result(result)
        assert decision.action == "ACCEPT_VARIANTS"
        assert len(decision.variants_to_add) == 7
        for v in decision.variants_to_add:
            assert v.get("variant_id"), f"variant_id missing: {v}"

    def test_candidate_missing_required_fields_excluded(self):
        """Candidate missing year_start/year_end cannot get variant_id → excluded."""
        result = _make_result(
            candidate_variants=[
                {"make": "VW", "model": "Jetta"},  # missing year_start, year_end
                {"make": "VW", "model": "Jetta", "year_start": 2020, "year_end": 2025},
            ]
        )
        decision = decide_seed_result(result)
        assert decision.action == "ACCEPT_VARIANTS"
        assert len(decision.variants_to_add) == 1
        assert decision.warnings  # warning about excluded candidate

    def test_all_candidates_fail_variant_id_manual_review(self):
        """If all candidates cannot get variant_id, decision becomes MANUAL_REVIEW."""
        result = _make_result(
            candidate_variants=[
                {"make": "VW", "model": "Jetta"},  # missing year_start, year_end
                {"make": "VW", "model": "Golf"},    # missing year_start, year_end
            ]
        )
        decision = decide_seed_result(result)
        assert decision.action == "MANUAL_REVIEW"
        assert decision.reason == "no_mergeable_candidates_after_variant_id_generation"

    def test_enriched_candidates_merge_correctly(self):
        """Enriched candidates actually merge into canonical without zero-mutation error."""
        from engine.apply import apply_decision

        result = _make_result(
            candidate_variants=[{
                "make": "Volkswagen", "model": "Jetta",
                "year_start": 2019, "year_end": 2024,
                "body_type": "sedan", "engine": "1.4 TSI",
                "transmission": "automatic", "fuel_type": "petrol",
            }]
        )
        decision = decide_seed_result(result)
        assert decision.action == "ACCEPT_VARIANTS"

        canonical = {
            "verified_variants": [],
            "partial_variants": [],
            "batch_state": {
                "processed_seed_ids": [],
                "manual_review_seed_ids": [],
                "failed_seed_ids": [],
                "seed_accounting": {},
            },
        }
        stats = apply_decision(canonical, decision)
        assert stats["added_count"] == 1

    def test_zero_mutation_invariant_still_active(self):
        """Zero-mutation invariant remains active for truly empty apply."""
        from engine.apply import apply_decision, ZeroMutationAcceptError

        decision = Decision(
            action="ACCEPT_VARIANTS",
            seed_id="test__model__2020__2026__il",
            reason="valid",
            variants_to_add=[],
        )
        canonical = {
            "verified_variants": [],
            "partial_variants": [],
            "batch_state": {
                "processed_seed_ids": [],
                "manual_review_seed_ids": [],
                "failed_seed_ids": [],
                "seed_accounting": {},
            },
        }
        with pytest.raises(ZeroMutationAcceptError):
            apply_decision(canonical, decision)
