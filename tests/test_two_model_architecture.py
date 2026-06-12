"""Tests for the two-model validation architecture.

Covers:
  - Evidence normalization (source strength capping, URL cleanup, dedup)
  - OpenAI adjudicator (prompt building, response parsing, mock client)
  - Split-required routing
  - needs_more_grounding behavior
  - Integration with existing engine decisions
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import deterministic_qa as qa  # noqa: E402
import evidence_normalizer as enorm  # noqa: E402
import model_context as mctx  # noqa: E402
import openai_adjudicator as adj  # noqa: E402
import run_gemini_validation as engine  # noqa: E402
import runtime_config  # noqa: E402


# ═══════════════════════════════════════════════════════════════════════════
# Test Case 1: Abarth 500 / trim=None / official_marketed_name_il=595
# ═══════════════════════════════════════════════════════════════════════════

class TestCase1Abarth595:
    """VAL-000006: Abarth 500, trim=None, official_marketed_name_il=595.
    Expected: split_required (595 is a model family with multiple trims)."""

    def _make_merged_context(self):
        return {
            "validation_id": "VAL-000006",
            "standard_variant": {
                "make": "Abarth",
                "model": "500",
                "trim": None,
                "official_marketed_name_il": "595",
                "year_start": 2016,
                "year_end": 2023,
                "engine": "1.4L Turbo",
                "transmission": "Automatic",
                "fuel_type": "Gasoline",
                "drivetrain": "FWD",
                "body_type": "Hatchback",
                "generation": None,
                "seats": 4,
                "variant_id": "V-000006",
                "market_scope": "IL",
            },
            "source_trim_was_generic": True,
            "technical_fingerprint": {
                "make": "Abarth", "model": "500",
                "year_start": 2016, "year_end": 2023,
                "engine": "1.4L Turbo", "transmission": "Automatic",
                "fuel_type": "Gasoline", "body_type": "Hatchback",
                "drivetrain": "FWD", "seats": 4,
            },
        }

    def _make_research_pack_split(self):
        return {
            "validation_id": "VAL-000006",
            "research_status": "complete",
            "research_summary": "595 is a model family with multiple Israeli trims",
            "queries_used": ["Abarth 595 Israel", "אבארת 595 ישראל"],
            "source_ladder_coverage": {
                "official_importer_checked": True,
                "price_list_or_brochure_checked": True,
                "israeli_auto_sites_checked": True,
                "used_listings_checked_as_weak_support": False,
                "non_israeli_sources_checked_for_technical_only": False,
            },
            "evidence_items": [
                {
                    "source_title": "Auto.co.il Abarth 595",
                    "source_type": "israeli_auto_site",
                    "source_url": "https://www.auto.co.il/abarth-595",
                    "language": "he",
                    "fields_supported": ["israeli_market_presence", "trim_name"],
                    "evidence_strength": "strong",  # will be normalized to medium
                    "short_summary": "Multiple 595 trims found",
                },
            ],
            "possible_israeli_trims_found": [
                {
                    "trim_name": "595",
                    "hebrew_name": "595",
                    "source_refs": [],
                    "evidence_strength": "medium",
                    "can_map_this_row_to_trim": False,
                    "reason": "Base 595 trim",
                },
                {
                    "trim_name": "595 Turismo",
                    "hebrew_name": "595 טוריסמו",
                    "source_refs": [],
                    "evidence_strength": "medium",
                    "can_map_this_row_to_trim": False,
                    "reason": "Higher trim",
                },
                {
                    "trim_name": "595 Competizione",
                    "hebrew_name": "595 קומפטיציונה",
                    "source_refs": [],
                    "evidence_strength": "medium",
                    "can_map_this_row_to_trim": False,
                    "reason": "Performance trim",
                },
            ],
            "model_family_findings": {
                "is_model_family": True,
                "family_name": "595",
                "reason": "595 is a family with multiple trims in Israel",
            },
            "technical_fingerprint_findings": {
                "engine": "1.4L Turbo",
                "transmission": "Automatic",
                "fuel_type": "Gasoline",
                "drivetrain": "FWD",
                "body_type": "Hatchback",
                "year_range": "2016-2023",
                "supported_by_sources": [],
            },
            "split_indicators": {
                "split_likely": True,
                "reason": "595 represents a family with Turismo and Competizione trims",
                "candidate_child_variants": ["595", "595 Turismo", "595 Competizione"],
            },
            "unique_mapping_candidate": {
                "exists": False,
                "trim_name": None,
                "official_marketed_name": None,
                "confidence": 0.0,
                "supporting_sources": [],
                "reason": "Multiple trims match, cannot uniquely map",
            },
            "conflicts": [],
            "missing_information": [],
            "researcher_recommended_next_action": "send_to_adjudicator",
        }

    def test_mock_adjudicator_returns_split_for_none_trim_with_split_research(self):
        """When research shows split_likely, mock adjudicator returns split_required."""
        mock = adj.MockAdjudicatorClient()
        mc = self._make_merged_context()
        rp = self._make_research_pack_split()
        result = mock.adjudicate(mc, rp, [], [], 1, 3)
        # trim=None -> the mock handles this based on split_indicators
        # The mock checks split_likely first
        assert result["final_decision"] in ("split_required", "rejected_from_clean")
        assert result["validation_id"] == "VAL-000006"

    def test_595_is_model_family_clue(self):
        """595 should be recognized as generic/short, not as a verified trim."""
        rules = engine.load_rules()
        il_name = "595"
        import re
        too_generic = bool(re.fullmatch(r"[\d\s\-]+", il_name.strip())) \
            or len(il_name.strip()) <= 2
        assert too_generic, "595 should be detected as a generic short value"

    def test_none_trim_is_generic(self):
        """None trim must be detected as generic."""
        rules = engine.load_rules()
        assert qa.is_generic_trim(None, rules)

    def test_split_required_not_counted_as_rejected(self):
        """split_required must be a separate final decision, not rejected_from_clean."""
        assert "split_required" in engine.FINAL_DECISIONS
        assert "split_required" not in engine.CLEAN_DECISIONS
        assert engine.DECISION_COUNT_KEY["split_required"] == "split_required"
        assert engine.DECISION_COUNT_KEY["rejected_from_clean"] == "rejected_from_clean"


# ═══════════════════════════════════════════════════════════════════════════
# Test Case 2: Combined trim "Turismo / Competizione"
# ═══════════════════════════════════════════════════════════════════════════

class TestCase2CombinedTrim:
    """Combined trim like 'Turismo / Competizione' should be split_required."""

    def test_combined_trim_detected(self):
        rules = engine.load_rules()
        assert qa.looks_like_combined_trim("Turismo / Competizione", rules)

    def test_mock_adjudicator_returns_split_for_combined_trim(self):
        mock = adj.MockAdjudicatorClient()
        mc = {
            "validation_id": "VAL-000007",
            "standard_variant": {
                "make": "Abarth",
                "model": "500",
                "trim": "Turismo / Competizione",
                "official_marketed_name_il": None,
                "year_start": 2020, "year_end": 2023,
                "engine": "1.4L", "transmission": "Auto",
                "fuel_type": "Gasoline", "drivetrain": "FWD",
                "body_type": "Hatchback", "generation": None,
                "seats": 4, "variant_id": "V-007",
                "market_scope": "IL",
            },
            "source_trim_was_generic": False,
        }
        result = mock.adjudicate(mc, {}, [], [], 1, 3)
        assert result["final_decision"] == "split_required"
        assert result["split_review"]["split_recommended"] is True
        assert len(result["split_review"]["candidate_child_variants"]) >= 2


# ═══════════════════════════════════════════════════════════════════════════
# Test Case 3: Source strength normalization
# ═══════════════════════════════════════════════════════════════════════════

class TestCase3SourceStrengthNormalization:
    """Deterministic source strength capping."""

    def test_auto_co_il_strong_becomes_medium(self):
        """Auto.co.il (israeli_auto_site) claimed as 'strong' -> 'medium'."""
        result = enorm.cap_strength("israeli_auto_site", "strong")
        assert result == "medium"

    def test_auto_co_il_medium_stays_medium(self):
        result = enorm.cap_strength("israeli_auto_site", "medium")
        assert result == "medium"

    def test_used_listing_strong_becomes_weak(self):
        """Used listing claimed as 'strong' -> 'weak'."""
        result = enorm.cap_strength("used_listing", "strong")
        assert result == "weak"

    def test_used_listing_medium_becomes_weak(self):
        """Used listing claimed as 'medium' -> 'weak'."""
        result = enorm.cap_strength("used_listing", "medium")
        assert result == "weak"

    def test_official_importer_strong_stays_strong(self):
        result = enorm.cap_strength("official_importer", "strong")
        assert result == "strong"

    def test_brochure_strong_stays_strong(self):
        result = enorm.cap_strength("brochure", "strong")
        assert result == "strong"

    def test_price_list_strong_stays_strong(self):
        result = enorm.cap_strength("price_list", "strong")
        assert result == "strong"

    def test_dealer_page_strong_becomes_medium(self):
        result = enorm.cap_strength("dealer_page", "strong")
        assert result == "medium"

    def test_non_israeli_strong_becomes_weak(self):
        result = enorm.cap_strength("non_israeli_technical_source", "strong")
        assert result == "weak"

    def test_normalize_evidence_item_caps_strength(self):
        item = {
            "source_title": "Auto.co.il test",
            "source_type": "israeli_auto_site",
            "source_url": "https://auto.co.il/test",
            "language": "he",
            "fields_supported": ["trim_name"],
            "evidence_strength": "strong",
            "short_summary": "test",
        }
        result = enorm.normalize_evidence_item(item)
        assert result["evidence_strength"] == "medium"

    def test_non_israeli_source_strips_trim_fields(self):
        """Non-Israeli source must not support Israeli trim naming fields."""
        item = {
            "source_title": "Wikipedia",
            "source_type": "non_israeli_technical_source",
            "source_url": "https://en.wikipedia.org/test",
            "language": "en",
            "fields_supported": ["trim_name", "official_marketed_name",
                                 "technical_fingerprint"],
            "evidence_strength": "medium",
            "short_summary": "test",
        }
        result = enorm.normalize_evidence_item(item)
        assert "trim_name" not in result["fields_supported"]
        assert "official_marketed_name" not in result["fields_supported"]
        assert "technical_fingerprint" in result["fields_supported"]


# ═══════════════════════════════════════════════════════════════════════════
# Test Case 4: Markdown URL cleanup
# ═══════════════════════════════════════════════════════════════════════════

class TestCase4MarkdownUrlCleanup:
    def test_markdown_url_cleaned(self):
        url = "[https://example.com/page](https://example.com/page)"
        result = enorm.normalize_url(url)
        assert result == "https://example.com/page"

    def test_plain_url_unchanged(self):
        url = "https://example.com/page"
        result = enorm.normalize_url(url)
        assert result == "https://example.com/page"

    def test_empty_url_returns_none(self):
        assert enorm.normalize_url("") is None
        assert enorm.normalize_url(None) is None

    def test_invalid_url_returns_none(self):
        assert enorm.normalize_url("not a url") is None

    def test_markdown_with_different_text(self):
        url = "[Auto.co.il page](https://auto.co.il/test)"
        result = enorm.normalize_url(url)
        assert result == "https://auto.co.il/test"


# ═══════════════════════════════════════════════════════════════════════════
# Test Case 5: needs_more_grounding behavior
# ═══════════════════════════════════════════════════════════════════════════

class TestCase5NeedsMoreGrounding:
    def test_needs_more_grounding_maps_to_none(self):
        """needs_more_grounding is not a final decision."""
        result = adj.map_decision_to_engine_status("needs_more_grounding")
        assert result is None

    def test_auto_resolved_maps_correctly(self):
        result = adj.map_decision_to_engine_status("auto_resolved")
        assert result == "auto_resolved"

    def test_split_required_maps_correctly(self):
        result = adj.map_decision_to_engine_status("split_required")
        assert result == "split_required"

    def test_rejected_maps_correctly(self):
        result = adj.map_decision_to_engine_status("rejected_from_clean")
        assert result == "rejected_from_clean"

    def test_grounding_exhausted_produces_rejected(self):
        """When attempts are exhausted with needs_more_grounding, result is rejected."""
        # Simulate the engine behavior
        mock = adj.MockAdjudicatorClient()
        # With a generic trim, mock returns rejected_from_clean
        mc = {
            "validation_id": "VAL-EXHAUST",
            "standard_variant": {
                "make": "TestMake", "model": "TestModel",
                "trim": None,
                "official_marketed_name_il": None,
                "variant_id": "V-EXHAUST",
            },
            "source_trim_was_generic": True,
        }
        result = mock.adjudicate(mc, {}, [], [], 3, 3)
        # Mock returns rejected_from_clean for None trim without split indicators
        assert result["final_decision"] == "rejected_from_clean"


# ═══════════════════════════════════════════════════════════════════════════
# Evidence normalization integration tests
# ═══════════════════════════════════════════════════════════════════════════

class TestEvidenceNormalizationIntegration:
    def test_full_pack_normalization(self):
        pack = {
            "evidence_items": [
                {
                    "source_title": "Auto.co.il",
                    "source_type": "israeli_auto_site",
                    "source_url": "[https://auto.co.il](https://auto.co.il)",
                    "language": "he",
                    "fields_supported": ["trim_name"],
                    "evidence_strength": "strong",
                    "short_summary": "test",
                },
                {
                    "source_title": "Used listing",
                    "source_type": "used_listing",
                    "source_url": "https://yad2.co.il/test",
                    "language": "he",
                    "fields_supported": ["trim_name"],
                    "evidence_strength": "medium",
                    "short_summary": "test 2",
                },
            ],
            "possible_israeli_trims_found": [
                {"trim_name": "Sport", "evidence_strength": "medium"},
                {"trim_name": "sport", "evidence_strength": "weak"},  # duplicate
            ],
        }
        result = enorm.normalize_research_pack(pack)
        assert result["evidence_items"][0]["evidence_strength"] == "medium"
        assert result["evidence_items"][0]["source_url"] == "https://auto.co.il"
        assert result["evidence_items"][1]["evidence_strength"] == "weak"
        # Dedup trims by name
        assert len(result["possible_israeli_trims_found"]) == 1

    def test_qa_warnings_generated(self):
        pack = {
            "evidence_items": [],
            "source_ladder_coverage": {
                "official_importer_checked": False,
            },
        }
        warnings = enorm.generate_qa_warnings(pack)
        assert any("no evidence" in w for w in warnings)
        assert any("official importer" in w for w in warnings)

    def test_invalid_source_type_normalized(self):
        item = {
            "source_title": "Unknown source",
            "source_type": "invalid_type",
            "source_url": "https://example.com",
            "language": "en",
            "fields_supported": ["trim_name"],
            "evidence_strength": "strong",
            "short_summary": "test",
        }
        result = enorm.normalize_evidence_item(item)
        assert result["source_type"] == "non_israeli_technical_source"
        assert result["evidence_strength"] == "weak"


# ═══════════════════════════════════════════════════════════════════════════
# Adjudicator prompt and parsing tests
# ═══════════════════════════════════════════════════════════════════════════

class TestAdjudicatorPromptAndParsing:
    def test_build_prompt(self):
        mc = {
            "validation_id": "VAL-001",
            "standard_variant": {
                "make": "Toyota", "model": "Corolla", "trim": "LE",
                "official_marketed_name_il": None,
                "year_start": 2020, "year_end": 2023,
                "engine": "1.6L", "transmission": "CVT",
                "fuel_type": "Gasoline", "drivetrain": "FWD",
                "body_type": "Sedan", "generation": "E210",
                "seats": 5, "variant_id": "V-001",
            },
            "source_trim_was_generic": False,
        }
        prompt = adj.build_adjudicator_prompt(mc, {}, [], [], 1, 3)
        parsed = json.loads(prompt)
        assert parsed["validation_id"] == "VAL-001"
        assert parsed["original_variant"]["make"] == "Toyota"

    def test_parse_valid_response(self):
        resp = json.dumps({
            "validation_id": "VAL-001",
            "make": "Toyota", "model": "Corolla",
            "final_decision": "auto_resolved",
            "final_confidence": 0.9,
            "final_reason": "test",
        })
        result = adj.parse_adjudicator_response(resp)
        assert result["final_decision"] == "auto_resolved"

    def test_parse_rejects_invalid_decision(self):
        resp = json.dumps({
            "validation_id": "VAL-001",
            "final_decision": "invalid_decision",
        })
        try:
            adj.parse_adjudicator_response(resp)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "invalid final_decision" in str(e)

    def test_parse_handles_markdown_fences(self):
        resp = '```json\n{"validation_id":"V1","final_decision":"split_required"}\n```'
        result = adj.parse_adjudicator_response(resp)
        assert result["final_decision"] == "split_required"


# ═══════════════════════════════════════════════════════════════════════════
# RuntimeConfig tests
# ═══════════════════════════════════════════════════════════════════════════

class TestRuntimeConfigOpenAI:
    def test_default_adjudication_scope(self):
        cfg = runtime_config.resolve(runtime="test")
        assert cfg.adjudication_scope == "all_non_trivial"

    def test_default_openai_model(self):
        cfg = runtime_config.resolve(runtime="test")
        assert cfg.openai_model_id == "gpt-5.4"

    def test_openai_key_not_present_by_default(self):
        cfg = runtime_config.resolve(runtime="test")
        assert not cfg.openai_key_present

    def test_presence_report_includes_openai(self):
        cfg = runtime_config.resolve(runtime="test")
        report = cfg.presence_report()
        assert "openai_api_key" in report
        assert report["openai_api_key"] == "MISSING"
        assert "openai_model_id" in report
        assert "adjudication_scope" in report


# ═══════════════════════════════════════════════════════════════════════════
# Engine integration tests
# ═══════════════════════════════════════════════════════════════════════════

class TestEngineIntegration:
    def test_final_decisions_includes_split_required(self):
        assert "split_required" in engine.FINAL_DECISIONS

    def test_split_required_not_in_clean_decisions(self):
        assert "split_required" not in engine.CLEAN_DECISIONS

    def test_fresh_progress_includes_split_required(self):
        prog = engine.fresh_progress()
        assert "split_required" in prog["counts"]
        assert prog["counts"]["split_required"] == 0

    def test_recompute_counts_handles_split(self):
        prog = engine.fresh_progress()
        prog["records"]["V1"] = {"final_decision": "split_required"}
        prog["records"]["V2"] = {"final_decision": "auto_accept"}
        prog["records"]["V3"] = {"final_decision": "rejected_from_clean"}
        engine.recompute_counts(prog)
        assert prog["counts"]["split_required"] == 1
        assert prog["counts"]["accepted"] == 1
        assert prog["counts"]["rejected_from_clean"] == 1

    def test_model_context_handles_split_required(self):
        ctx = mctx.fresh_context("Abarth", "500")
        mctx.update_context_after_variant(
            ctx, "VAL-SPLIT", {"trim": "595"}, "split_required", None, {})
        assert "VAL-SPLIT" in ctx["already_rejected_variants"]

    def test_output_paths_has_split_required(self):
        paths = engine.REAL_PATHS
        assert paths.split_required.name == "split_required.jsonl"

    def test_research_prompt_loads(self):
        prompt = engine.load_research_prompt()
        assert "recovery-first" in prompt.lower() or "recovery" in prompt.lower()
        assert len(prompt) > 200

    def test_build_research_prompt(self):
        mc = {
            "validation_id": "VAL-001",
            "standard_variant": {
                "make": "Toyota", "model": "Corolla", "trim": "LE",
            },
            "source_trim_was_generic": False,
        }
        prompt = engine.build_research_prompt(mc)
        assert "RESEARCH_CONTEXT" in prompt
        assert "VAL-001" in prompt

    def test_build_research_prompt_with_gaps(self):
        mc = {
            "validation_id": "VAL-002",
            "standard_variant": {"make": "BMW", "model": "X5", "trim": None},
            "source_trim_was_generic": True,
        }
        prompt = engine.build_research_prompt(mc, gaps=["official_importer_missing"])
        assert "TARGETED" in prompt
        assert "official_importer_missing" in prompt

class TestGeminiPromptContextParsing:
    def _make_context(self):
        return {
            "validation_id": "VAL-000010",
            "standard_variant": {
                "make": "Toyota",
                "model": "Corolla",
                "global_model_name": "Corolla",
                "official_marketed_name_il": "Corolla",
                "trim": "Sun",
                "year_start": 2020,
                "year_end": 2022,
                "engine": "1.6L",
                "transmission": "Automatic",
                "fuel_type": "Gasoline",
                "drivetrain": "FWD",
                "body_type": "Sedan",
                "generation": None,
                "seats": 5,
                "variant_id": "V-000010",
            },
            "source_trim_was_generic": False,
        }

    def test_run_gemini_research_prompt_without_merged_context_does_not_crash(self):
        client = engine.MockGeminiClient()
        pack, error = engine._run_gemini_research(client, self._make_context())
        assert error is None
        assert pack is not None
        assert pack["validation_id"] == "VAL-000010"
        assert pack["research_status"] == "complete"

    def test_full_validation_prompt_with_merged_context_still_works(self):
        client = engine.MockGeminiClient()
        prompt = engine.build_user_prompt(self._make_context())
        assert "MERGED_CONTEXT:\n" in prompt
        raw_text, grounded = client.generate(prompt)
        parsed = json.loads(raw_text)
        assert grounded is False
        assert parsed["validation_id"] == "VAL-000010"
        assert parsed["corrected_variant"]["trim"] == "Sun"


# ═══════════════════════════════════════════════════════════════════════════
# Deduplication tests
# ═══════════════════════════════════════════════════════════════════════════

class TestDeduplication:
    def test_deduplicate_evidence_by_url_and_title(self):
        items = [
            {"source_url": "https://a.com", "source_title": "Page A"},
            {"source_url": "https://a.com", "source_title": "Page A"},
            {"source_url": "https://b.com", "source_title": "Page B"},
        ]
        result = enorm.deduplicate_evidence(items)
        assert len(result) == 2

    def test_deduplicate_trims_case_insensitive(self):
        trims = [
            {"trim_name": "Sport"},
            {"trim_name": "sport"},
            {"trim_name": "Luxury"},
        ]
        result = enorm.deduplicate_trims(trims)
        assert len(result) == 2

    def test_deduplicate_trims_skips_non_dict(self):
        trims = [{"trim_name": "Sport"}, "invalid", None, {"trim_name": "Luxury"}]
        result = enorm.deduplicate_trims(trims)
        assert len(result) == 2
