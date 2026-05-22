"""Tests for engine/decision.py — decision rules."""
import pytest
from engine.types import SeedRunResult
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
