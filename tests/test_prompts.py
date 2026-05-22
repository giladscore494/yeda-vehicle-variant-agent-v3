"""Tests for llm/prompts.py — prompt content policy assertions."""
from llm.prompts import build_discovery_prompt


_SEED = {"make": "Volkswagen", "model": "Jetta", "year_start": 2020, "year_end": 2026}


def _prompt() -> str:
    return build_discovery_prompt(_SEED, market="IL")


class TestPromptILConfirmedPolicy:
    """Prompt must contain strict IL-confirmed / source_ids policies."""

    def test_il_confirmed_requires_israeli_evidence(self):
        p = _prompt()
        assert "IL-confirmed" in p
        assert "Israeli-market evidence" in p or "Israeli-market source" in p

    def test_global_specs_do_not_prove_il_confirmed(self):
        p = _prompt()
        assert "global technical sources alone do NOT prove IL-confirmed" in p

    def test_candidate_source_ids_required(self):
        p = _prompt()
        assert "Every candidate variant MUST include source_ids" in p

    def test_placeholder_source_ids_forbidden(self):
        p = _prompt()
        assert "NEVER use placeholder IDs" in p
        for placeholder in ("src_1", "src_2", "source_1", "ref_1", "citation_1"):
            assert placeholder in p  # listed as forbidden examples

    def test_downgrade_to_il_likely_when_no_il_proof(self):
        p = _prompt()
        assert "IL-likely" in p
        assert "global-reference-only" in p
        # The prompt must instruct downgrading when IL proof is missing
        assert "do NOT mark the variant" in p or "do NOT use market_scope" in p

    def test_model_not_sold_requires_real_proof(self):
        p = _prompt()
        assert "model_not_sold_in_market" in p
        assert "reliable IL-market evidence" in p or "reliable IL-market" in p

    def test_anti_pattern_examples_present(self):
        p = _prompt()
        assert "ANTI-PATTERNS" in p
        assert "BLOCKED by engine" in p

    def test_source_shape_no_placeholder_example(self):
        """Source shape example must NOT use src_1 as source_id."""
        p = _prompt()
        # The source shape example should use a descriptive ID
        assert '"source_id": "yad2_il_jetta_2023"' in p
        # Must not have the old placeholder example
        lines = p.split("\n")
        for line in lines:
            if '"source_id"' in line and "source_type" in line:
                assert "src_1" not in line
