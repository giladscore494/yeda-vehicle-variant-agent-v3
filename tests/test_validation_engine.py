"""Tests for the validation engine — model validation, GitHub save, schema, UI contracts.

Covers requirements 1–12 of the validation engine specification.
"""
from __future__ import annotations

import importlib
import json
import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest


# ── Test helpers ────────────────────────────────────────────────────────

def _minimal_canonical():
    """Return a minimal canonical dict for testing."""
    return {
        "verified_variants": [
            {
                "variant_id": "test__sedan__2020__2023__il",
                "make": "Test",
                "model": "Sedan",
                "generation": "Gen1",
                "trim": "Base",
                "engine": "2.0L",
                "fuel_type": "petrol",
                "transmission": "automatic",
                "drivetrain": "FWD",
                "body_type": "sedan",
                "year_start": 2020,
                "year_end": 2023,
                "market_scope": "IL-confirmed",
                "confidence_level": "high",
                "source_ids": ["icar_test_2020"],
                "seed_id": "test__sedan__2020__2023__il",
            }
        ],
        "partial_variants": [
            {
                "variant_id": "test__suv__2021__2024__il",
                "make": "Test",
                "model": "SUV",
                "generation": "Gen2",
                "trim": None,
                "engine": "1.5L",
                "fuel_type": "petrol",
                "transmission": "manual",
                "drivetrain": "AWD",
                "body_type": "SUV",
                "year_start": 2021,
                "year_end": 2024,
                "market_scope": "IL-confirmed",
                "confidence_level": "medium",
                "source_ids": [],
                "seed_id": "test__suv__2021__2024__il",
            }
        ],
        "batch_state": {
            "processed_seed_ids": ["test__sedan__2020__2023__il"],
            "failed_seed_ids": ["mg_(british_era)__tf__2002__2005__il"],
            "manual_review_seed_ids": ["test__manual__2020__2022__il"],
            "last_completed_seed_id": "test__sedan__2020__2023__il",
            "next_seed_id": None,
            "needs_retry_seed_ids": [],
        },
        "counts": {
            "total_verified": 1,
            "total_partial": 1,
        },
    }


def _minimal_seeds():
    return [
        {"make": "Test", "model": "Sedan", "year_start": 2020, "year_end": 2023, "market": "IL"},
        {"make": "Test", "model": "SUV", "year_start": 2021, "year_end": 2024, "market": "IL"},
        {"make": "MG (British era)", "model": "TF", "year_start": 2002, "year_end": 2005, "market": "IL"},
    ]


# ======================================================================
# 1. Model Schema Tests
# ======================================================================


class TestModelSchema:
    """Tests for engine/validation/model_schema.py"""

    def test_valid_item_accepted(self):
        from engine.validation.model_schema import validate_item
        item = {
            "validation_item_id": "test_001",
            "group_type": "partial_group",
            "seed_id": None,
            "variant_ids": ["v1", "v2"],
            "model_name": "gemini-3.1-pro-preview",
            "model_role": "primary",
            "recommendation": "no_action",
            "confidence": 0.85,
            "risk_level": "medium",
            "evidence": [],
            "issues_found": [],
            "suggested_patch": {"has_patch": False, "patch_type": "none"},
            "needs_build_retry": False,
            "needs_manual_review": False,
            "needs_data_correction": False,
            "safe_to_auto_apply": False,
        }
        errors = validate_item(item)
        assert errors == [], f"Expected no errors, got {errors}"

    def test_invalid_enum_rejected(self):
        from engine.validation.model_schema import validate_item
        item = {
            "validation_item_id": "test_001",
            "group_type": "INVALID_TYPE",
            "model_name": "test",
            "model_role": "primary",
            "recommendation": "INVALID_REC",
            "confidence": 0.5,
            "risk_level": "medium",
            "variant_ids": [],
            "safe_to_auto_apply": False,
        }
        errors = validate_item(item)
        assert any("group_type" in e for e in errors)
        assert any("recommendation" in e for e in errors)

    def test_confidence_outside_range_rejected(self):
        from engine.validation.model_schema import validate_item
        item = {
            "validation_item_id": "test_001",
            "group_type": "partial_group",
            "model_name": "test",
            "model_role": "primary",
            "recommendation": "no_action",
            "confidence": 1.5,
            "risk_level": "medium",
            "variant_ids": [],
            "safe_to_auto_apply": False,
        }
        errors = validate_item(item)
        assert any("confidence" in e for e in errors)

    def test_negative_confidence_rejected(self):
        from engine.validation.model_schema import validate_item
        item = {
            "validation_item_id": "test_001",
            "group_type": "partial_group",
            "model_name": "test",
            "model_role": "primary",
            "recommendation": "no_action",
            "confidence": -0.1,
            "risk_level": "medium",
            "variant_ids": [],
            "safe_to_auto_apply": False,
        }
        errors = validate_item(item)
        assert any("confidence" in e for e in errors)

    def test_safe_to_auto_apply_must_be_false(self):
        from engine.validation.model_schema import validate_item
        item = {
            "validation_item_id": "test_001",
            "group_type": "partial_group",
            "model_name": "test",
            "model_role": "primary",
            "recommendation": "no_action",
            "confidence": 0.5,
            "risk_level": "medium",
            "variant_ids": [],
            "safe_to_auto_apply": True,
        }
        errors = validate_item(item)
        assert any("safe_to_auto_apply" in e for e in errors)

    def test_invalid_json_returns_model_parse_error(self):
        from engine.validation.model_schema import parse_model_json
        parsed, error = parse_model_json("this is not json {{{")
        assert parsed is None
        assert error == "model_parse_error"

    def test_valid_json_parsed(self):
        from engine.validation.model_schema import parse_model_json
        parsed, error = parse_model_json('{"key": "value"}')
        assert parsed == {"key": "value"}
        assert error is None

    def test_markdown_fenced_json_parsed(self):
        from engine.validation.model_schema import parse_model_json
        text = '```json\n{"key": "value"}\n```'
        parsed, error = parse_model_json(text)
        assert parsed == {"key": "value"}
        assert error is None

    def test_trailing_comma_repaired(self):
        from engine.validation.model_schema import parse_model_json
        text = '{"key": "value",}'
        parsed, error = parse_model_json(text)
        assert parsed == {"key": "value"}
        assert error is None

    def test_normalize_model_output_fills_defaults(self):
        from engine.validation.model_schema import normalize_model_output
        raw = {"recommendation": "merge"}
        result = normalize_model_output(raw, "item_1", "gemini-3.1-pro-preview", "primary")
        assert result["validation_item_id"] == "item_1"
        assert result["model_name"] == "gemini-3.1-pro-preview"
        assert result["recommendation"] == "merge"
        assert result["safe_to_auto_apply"] is False
        assert isinstance(result["confidence"], float)

    def test_normalize_maps_string_confidence(self):
        from engine.validation.model_schema import normalize_model_output
        raw = {"confidence": "high"}
        result = normalize_model_output(raw, "x", "m", "primary")
        assert result["confidence"] == 0.9

    def test_is_risky_recommendation(self):
        from engine.validation.model_schema import is_risky_recommendation
        assert is_risky_recommendation("merge") is True
        assert is_risky_recommendation("reject") is True
        assert is_risky_recommendation("no_action") is False
        assert is_risky_recommendation("needs_evidence") is False

    def test_needs_openai_second_opinion_risky(self):
        from engine.validation.model_schema import needs_openai_second_opinion
        result = {"recommendation": "merge", "confidence": 0.9}
        assert needs_openai_second_opinion(result) is True

    def test_needs_openai_second_opinion_low_confidence(self):
        from engine.validation.model_schema import needs_openai_second_opinion
        result = {"recommendation": "no_action", "confidence": 0.5}
        assert needs_openai_second_opinion(result) is True

    def test_no_openai_for_low_risk_no_action(self):
        from engine.validation.model_schema import needs_openai_second_opinion
        result = {"recommendation": "no_action", "confidence": 0.9}
        assert needs_openai_second_opinion(result) is False

    def test_invalid_shape_returns_validation_schema_error(self):
        """validate_item returns errors for invalid schema shapes."""
        from engine.validation.model_schema import validate_item
        item = {"not_a_valid_field": True}
        errors = validate_item(item)
        assert len(errors) > 0


# ======================================================================
# 2. Model Validation Items Builder Tests
# ======================================================================


class TestModelValidationItems:
    """Tests for engine/validation/model_validation_items.py"""

    def test_items_are_group_level(self):
        """Items are built at group level, not per-variant."""
        from engine.validation.model_validation_items import build_model_validation_items
        groups = [
            {
                "group_id": "sg_0001",
                "seed_id": "test__sedan__2020__2023__il",
                "reason": "failed_seed",
                "risk_level": "high",
                "variant_ids": ["v1", "v2", "v3"],
                "variant_count": 3,
            }
        ]
        canonical = _minimal_canonical()
        items = build_model_validation_items(groups, canonical)
        # Should create 1 group-level item, not 3 per-variant items
        assert len(items) == 1
        assert items[0]["variant_ids"] == ["v1", "v2", "v3"]

    def test_item_has_required_fields(self):
        from engine.validation.model_validation_items import build_model_validation_items
        groups = [
            {
                "group_id": "sg_0001",
                "seed_id": "test__sedan__2020__2023__il",
                "reason": "manual_review_seed",
                "risk_level": "high",
                "variant_ids": [],
                "variant_count": 0,
            }
        ]
        canonical = _minimal_canonical()
        items = build_model_validation_items(groups, canonical)
        assert len(items) == 1
        item = items[0]
        assert "validation_item_id" in item
        assert "group_type" in item
        assert "seed_id" in item
        assert "variant_ids" in item
        assert "risk_level" in item
        assert "reason_for_model_validation" in item
        assert "requires_openai_second_opinion_initially" in item

    def test_group_type_classification(self):
        from engine.validation.model_validation_items import build_model_validation_items
        groups = [
            {"group_id": "sg_0001", "seed_id": "s1", "reason": "failed_seed",
             "risk_level": "high", "variant_ids": [], "variant_count": 0},
            {"group_id": "sg_0002", "seed_id": "s2", "reason": "manual_review_seed",
             "risk_level": "high", "variant_ids": [], "variant_count": 0},
            {"group_id": "sg_0003", "seed_id": "s3", "reason": "il_confirmed_no_evidence",
             "risk_level": "medium", "variant_ids": [], "variant_count": 0},
        ]
        canonical = _minimal_canonical()
        items = build_model_validation_items(groups, canonical)
        assert items[0]["group_type"] == "targeted_seed"
        assert items[1]["group_type"] == "manual_review_seed"
        assert items[2]["group_type"] == "il_market_plausibility"


# ======================================================================
# 3. Model Validation Runner Tests
# ======================================================================


class TestModelValidationRunner:
    """Tests for engine/validation/model_validation_runner.py"""

    def test_runner_module_exists(self):
        import engine.validation.model_validation_runner as mvr
        assert hasattr(mvr, "run_model_validation")

    def test_run_model_validation_on_suspicious_groups_exists(self):
        from engine.validation import validation_runner
        assert hasattr(validation_runner, "run_model_validation_on_suspicious_groups")

    def test_validation_runner_imports_when_model_runner_unavailable(self):
        original_validation_runner = sys.modules.pop(
            "engine.validation.validation_runner", None
        )
        original_model_runner = sys.modules.pop(
            "engine.validation.model_validation_runner", None
        )

        try:
            with mock.patch.dict(
                sys.modules,
                {"engine.validation.model_validation_runner": None},
            ):
                validation_runner = importlib.import_module(
                    "engine.validation.validation_runner"
                )

            assert hasattr(
                validation_runner, "run_model_validation_on_suspicious_groups"
            )
        finally:
            sys.modules.pop("engine.validation.validation_runner", None)
            sys.modules.pop("engine.validation.model_validation_runner", None)
            if original_validation_runner is not None:
                sys.modules["engine.validation.validation_runner"] = (
                    original_validation_runner
                )
            if original_model_runner is not None:
                sys.modules["engine.validation.model_validation_runner"] = (
                    original_model_runner
                )

    def test_aggregate_decision_gemini_no_action_low_risk(self):
        from engine.validation.model_validation_runner import _aggregate_decision
        item = {"risk_level": "low", "validation_item_id": "test"}
        gemini = {
            "ok": True,
            "parsed_result": {"recommendation": "no_action", "confidence": 0.9, "risk_level": "low"},
        }
        decision = _aggregate_decision(item, gemini, None)
        assert decision["final_status"] == "validated_by_gemini"
        assert decision["needs_manual_review"] is False

    def test_aggregate_decision_gemini_risky_no_openai(self):
        from engine.validation.model_validation_runner import _aggregate_decision
        item = {"risk_level": "high", "validation_item_id": "test"}
        gemini = {
            "ok": True,
            "parsed_result": {"recommendation": "merge", "confidence": 0.8, "risk_level": "high"},
        }
        decision = _aggregate_decision(item, gemini, None)
        assert decision["needs_manual_review"] is True

    def test_aggregate_decision_dual_model_agree(self):
        from engine.validation.model_validation_runner import _aggregate_decision
        item = {"risk_level": "high", "validation_item_id": "test"}
        gemini = {
            "ok": True,
            "parsed_result": {"recommendation": "merge", "confidence": 0.85, "risk_level": "high"},
        }
        openai = {
            "ok": True,
            "parsed_result": {"recommendation": "merge", "confidence": 0.9, "risk_level": "high"},
        }
        decision = _aggregate_decision(item, gemini, openai)
        assert decision["final_status"] == "validated_dual_model"
        assert decision["final_recommendation"] == "merge"

    def test_aggregate_decision_dual_model_disagree(self):
        from engine.validation.model_validation_runner import _aggregate_decision
        item = {"risk_level": "high", "validation_item_id": "test"}
        gemini = {
            "ok": True,
            "parsed_result": {"recommendation": "merge", "confidence": 0.85, "risk_level": "high"},
        }
        openai = {
            "ok": True,
            "parsed_result": {"recommendation": "no_action", "confidence": 0.9, "risk_level": "medium"},
        }
        decision = _aggregate_decision(item, gemini, openai)
        assert decision["final_status"] == "needs_manual_review"

    def test_aggregate_decision_gemini_failed(self):
        from engine.validation.model_validation_runner import _aggregate_decision
        item = {"risk_level": "high", "validation_item_id": "test"}
        gemini = {"ok": False, "error_message": "API error"}
        decision = _aggregate_decision(item, gemini, None)
        assert decision["final_status"] == "model_validation_failed"
        assert decision["needs_manual_review"] is True

    def test_aggregate_decision_low_confidence_manual_review(self):
        from engine.validation.model_validation_runner import _aggregate_decision
        item = {"risk_level": "medium", "validation_item_id": "test"}
        gemini = {
            "ok": True,
            "parsed_result": {"recommendation": "no_action", "confidence": 0.5, "risk_level": "medium"},
        }
        decision = _aggregate_decision(item, gemini, None)
        assert decision["final_status"] == "needs_manual_review"

    def test_call_openai_uses_responses_api_for_web_search(self):
        from engine.validation.model_validation_runner import _call_openai

        item = {
            "validation_item_id": "test_openai_item",
            "variant_ids": ["v1"],
            "risk_level": "high",
        }
        fake_response = SimpleNamespace(
            output_text=json.dumps({
                "recommendation": "no_action",
                "confidence": 0.9,
                "risk_level": "low",
                "safe_to_auto_apply": False,
            }),
            usage=SimpleNamespace(input_tokens=12, output_tokens=18),
        )
        create = mock.Mock(return_value=fake_response)
        fake_client = SimpleNamespace(responses=SimpleNamespace(create=create))
        fake_openai = SimpleNamespace(OpenAI=mock.Mock(return_value=fake_client))

        def fake_get(group, key, default=None):
            if (group, key) == ("openai", "api_key"):
                return "test-key"
            if (group, key) == ("openai", "validator_model_id"):
                return "gpt-5.4"
            return default or ""

        with mock.patch("engine.validation.model_validation_runner.config.get", side_effect=fake_get):
            with mock.patch(
                "engine.validation.model_validation_runner.config.get_bool",
                return_value=True,
            ):
                with mock.patch.dict(sys.modules, {"openai": fake_openai}):
                    result = _call_openai(item, None, None)

        assert result["ok"] is True
        create.assert_called_once()
        assert create.call_args.kwargs["model"] == "gpt-5.4"
        assert create.call_args.kwargs["input"]
        assert create.call_args.kwargs["tools"] == [{"type": "web_search"}]

    def test_call_openai_retries_without_web_search_on_bad_request(self):
        from engine.validation.model_validation_runner import _call_openai

        item = {
            "validation_item_id": "test_openai_item",
            "variant_ids": ["v1"],
            "risk_level": "high",
        }

        class BadRequestError(Exception):
            status_code = 400

        fake_response = SimpleNamespace(
            output_text=json.dumps({
                "recommendation": "no_action",
                "confidence": 0.9,
                "risk_level": "low",
                "safe_to_auto_apply": False,
            }),
            usage=SimpleNamespace(input_tokens=12, output_tokens=18),
        )
        create = mock.Mock(side_effect=[BadRequestError("bad request"), fake_response])
        fake_client = SimpleNamespace(responses=SimpleNamespace(create=create))
        fake_openai = SimpleNamespace(OpenAI=mock.Mock(return_value=fake_client))

        def fake_get(group, key, default=None):
            if (group, key) == ("openai", "api_key"):
                return "test-key"
            if (group, key) == ("openai", "validator_model_id"):
                return "gpt-5.4"
            return default or ""

        with mock.patch("engine.validation.model_validation_runner.config.get", side_effect=fake_get):
            with mock.patch(
                "engine.validation.model_validation_runner.config.get_bool",
                return_value=True,
            ):
                with mock.patch.dict(sys.modules, {"openai": fake_openai}):
                    result = _call_openai(item, None, None)

        assert result["ok"] is True
        assert create.call_count == 2
        assert create.call_args_list[0].kwargs["tools"] == [{"type": "web_search"}]
        assert "tools" not in create.call_args_list[1].kwargs


class TestOpenAIReviewer:
    def test_review_group_uses_responses_api_for_web_search(self):
        from engine.validation.providers.openai_reviewer import review_group

        fake_response = SimpleNamespace(
            output_text=json.dumps({
                "recommendation": "no_action",
                "confidence": 0.85,
                "risk_level": "low",
                "safe_to_auto_apply": False,
            }),
            usage=SimpleNamespace(input_tokens=10, output_tokens=15),
        )
        create = mock.Mock(return_value=fake_response)
        fake_client = SimpleNamespace(responses=SimpleNamespace(create=create))
        fake_openai = SimpleNamespace(OpenAI=mock.Mock(return_value=fake_client))
        variants = [{
            "variant_id": "v1",
            "make": "Test",
            "model": "Sedan",
            "generation": "Gen1",
        }]

        def fake_get(group, key, default=None):
            if (group, key) == ("openai", "api_key"):
                return "test-key"
            if (group, key) == ("openai", "validator_model_id"):
                return "gpt-5.4"
            return default or ""

        with mock.patch("engine.validation.providers.openai_reviewer.config.get", side_effect=fake_get):
            with mock.patch(
                "engine.validation.providers.openai_reviewer.config.get_bool",
                return_value=True,
            ):
                with mock.patch.dict(sys.modules, {"openai": fake_openai}):
                    result = review_group("group_key", variants, ["Base"])

        assert result["ok"] is True
        create.assert_called_once()
        assert create.call_args.kwargs["model"] == "gpt-5.4"
        assert create.call_args.kwargs["input"]
        assert create.call_args.kwargs["tools"] == [{"type": "web_search"}]

    def test_review_group_extracts_text_from_response_output(self):
        from engine.validation.providers.openai_reviewer import review_group

        fake_response = SimpleNamespace(
            output_text="",
            output=[
                SimpleNamespace(
                    content=[
                        SimpleNamespace(
                            type="output_text",
                            text=json.dumps({
                                "recommendation": "no_action",
                                "confidence": 0.85,
                                "risk_level": "low",
                                "safe_to_auto_apply": False,
                            }),
                        ),
                    ],
                ),
            ],
            usage=SimpleNamespace(input_tokens=10, output_tokens=15),
        )
        create = mock.Mock(return_value=fake_response)
        fake_client = SimpleNamespace(responses=SimpleNamespace(create=create))
        fake_openai = SimpleNamespace(OpenAI=mock.Mock(return_value=fake_client))
        variants = [{
            "variant_id": "v1",
            "make": "Test",
            "model": "Sedan",
            "generation": "Gen1",
        }]

        def fake_get(group, key, default=None):
            if (group, key) == ("openai", "api_key"):
                return "test-key"
            if (group, key) == ("openai", "validator_model_id"):
                return "gpt-5.4"
            return default or ""

        with mock.patch("engine.validation.providers.openai_reviewer.config.get", side_effect=fake_get):
            with mock.patch(
                "engine.validation.providers.openai_reviewer.config.get_bool",
                return_value=True,
            ):
                with mock.patch.dict(sys.modules, {"openai": fake_openai}):
                    result = review_group("group_key", variants, ["Base"])

        assert result["ok"] is True


# ======================================================================
# 4. Full Validation Does Not Auto-Call Models
# ======================================================================


class TestFullValidationNoAutoModels:
    """Full Validation Session must NOT automatically call models."""

    def test_run_full_validation_does_not_import_model_runner(self):
        """run_full_validation should not call run_model_validation."""
        from engine.validation.validation_runner import run_full_validation
        import inspect
        source = inspect.getsource(run_full_validation)
        assert "run_model_validation(" not in source
        assert "_call_gemini" not in source
        assert "_call_openai" not in source


# ======================================================================
# 5. GitHub Save Tests
# ======================================================================


class TestGitHubSave:
    """Tests for engine/validation/github_save.py"""

    def test_allowed_file_list(self):
        from engine.validation.github_save import ALLOWED_FILES, BLOCKED_FILES
        assert "data/validated_runs/resume_package_canonical_validated_v2.json" in ALLOWED_FILES
        assert "data/validated_runs/model_validation_results_v2.json" in ALLOWED_FILES
        assert "data/runtime/current_validation_run.json" in ALLOWED_FILES
        assert "data/canonical/resume_package_canonical.json" in BLOCKED_FILES

    def test_blocks_main_branch(self):
        from engine.validation.github_save import _check_guards
        with mock.patch("engine.config.get") as mock_get:
            mock_get.side_effect = lambda g, k, **kw: {
                ("github", "target_branch"): "main",
                ("github", "repo_owner"): "giladscore494",
                ("github", "repo_name"): "yeda-vehicle-variant-agent-v3",
                ("github", "token"): "test_token",
            }.get((g, k), "")
            error = _check_guards()
            assert error is not None
            assert "main" in error

    def test_blocks_wrong_branch(self):
        from engine.validation.github_save import _check_guards
        with mock.patch("engine.config.get") as mock_get:
            mock_get.side_effect = lambda g, k, **kw: {
                ("github", "target_branch"): "some-other-branch",
                ("github", "repo_owner"): "giladscore494",
                ("github", "repo_name"): "yeda-vehicle-variant-agent-v3",
                ("github", "token"): "test_token",
            }.get((g, k), "")
            error = _check_guards()
            assert error is not None
            assert "some-other-branch" in error

    def test_blocks_canonical_file(self):
        from engine.validation.github_save import _is_file_blocked
        assert _is_file_blocked("data/canonical/resume_package_canonical.json") is True
        assert _is_file_blocked("data/canonical/anything.json") is True

    def test_allows_validation_files(self):
        from engine.validation.github_save import _is_file_allowed
        assert _is_file_allowed("data/validated_runs/resume_package_canonical_validated_v2.json") is True
        assert _is_file_allowed("data/validated_runs/model_validation_results_v2.json") is True

    def test_blocks_missing_token(self):
        from engine.validation.github_save import _check_guards
        with mock.patch("engine.config.get") as mock_get:
            mock_get.side_effect = lambda g, k, **kw: {
                ("github", "target_branch"): "validation-v2-budgeted-dual-il-trims",
                ("github", "repo_owner"): "giladscore494",
                ("github", "repo_name"): "yeda-vehicle-variant-agent-v3",
                ("github", "token"): "",
            }.get((g, k), "")
            error = _check_guards()
            assert error is not None
            assert "token" in error.lower()


# ======================================================================
# 6. Canonical Write Guard Tests
# ======================================================================


class TestCanonicalWriteGuard:
    """Canonical write guard must block canonical mutation."""

    def test_write_guard_blocks_canonical(self):
        from engine.validation.write_guard import (
            check_write_allowed,
            CanonicalWriteBlockedError,
        )
        with pytest.raises(CanonicalWriteBlockedError):
            check_write_allowed("data/canonical/resume_package_canonical.json")

    def test_write_guard_allows_validated_runs(self):
        from engine.validation.write_guard import check_write_allowed
        # Should not raise
        check_write_allowed("data/validated_runs/test.json")

    def test_write_guard_allows_runtime(self):
        from engine.validation.write_guard import check_write_allowed
        check_write_allowed("data/runtime/current_validation_run.json")


# ======================================================================
# 7. Model Validation Results Writer Tests
# ======================================================================


class TestModelValidationResultsWriter:
    """model_validation_results_v2.json writer."""

    def test_results_file_structure(self):
        """run_model_validation should produce correct structure."""
        from engine.validation.model_validation_runner import run_model_validation
        with tempfile.TemporaryDirectory() as tmpdir:
            # Run with empty items (no actual model calls needed)
            results = run_model_validation([], output_dir=tmpdir)
            assert results["model_validation_ran"] is True
            assert "model_calls_summary" in results
            assert "items" in results
            assert results["model_calls_summary"]["gemini_calls_attempted"] == 0

            # Check file was written
            results_file = Path(tmpdir) / "model_validation_results_v2.json"
            assert results_file.exists()
            data = json.loads(results_file.read_text())
            assert data["model_validation_ran"] is True


# ======================================================================
# 8. Validation Report Tests
# ======================================================================


class TestValidationReportModelSummary:
    """validation_report_v2.json must include model_calls_summary."""

    def test_report_includes_model_calls_summary(self):
        from engine.validation.validation_outputs import write_validation_report
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "validation_report_v2.json")
            model_calls = {
                "model_validation_ran": True,
                "gemini_calls_attempted": 5,
                "gemini_calls_success": 4,
                "gemini_calls_failed": 1,
                "openai_calls_attempted": 2,
                "openai_calls_success": 2,
                "openai_calls_failed": 0,
            }
            write_validation_report(
                validation_run_id="test_run",
                canonical=_minimal_canonical(),
                deterministic_issues=[],
                suspicious_groups=[],
                partial_classifications=[],
                targeted_seed_result=None,
                model_calls_summary=model_calls,
                output_path=output_path,
            )
            data = json.loads(Path(output_path).read_text())
            assert data["model_calls_summary"]["model_validation_ran"] is True
            assert data["model_calls_summary"]["gemini_calls_attempted"] == 5


# ======================================================================
# 9. Validated Package Tests
# ======================================================================


class TestValidatedPackage:
    """resume_package_canonical_validated_v2.json must remain full canonical-style."""

    def test_validated_package_preserves_structure(self):
        from engine.validation.validation_outputs import write_validated_package
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(
                tmpdir, "resume_package_canonical_validated_v2.json"
            )
            canonical = _minimal_canonical()
            write_validated_package(
                canonical=canonical,
                deterministic_issues=[],
                partial_classifications=[],
                suspicious_groups=[],
                targeted_seed_result=None,
                validation_run_id="test_run",
                output_path=output_path,
            )
            data = json.loads(Path(output_path).read_text())
            # Must preserve original keys
            assert "verified_variants" in data
            assert "partial_variants" in data
            assert "batch_state" in data
            # Must add validation metadata
            assert "validation_summary" in data
            assert "validation_status_by_seed" in data


# ======================================================================
# 10. Legacy Build Mutation Disabled Tests
# ======================================================================


class TestLegacyBuildDisabled:
    """Legacy build mutation actions must be unreachable/disabled."""

    def test_app_legacy_tab_is_read_only(self):
        """app.py legacy tab must include disabled message."""
        app_source = Path("app.py").read_text()
        assert "legacy_build_action_disabled_in_validation_branch" in app_source
        assert "Read-Only" in app_source

    def test_no_batch_run_in_app(self):
        """app.py must not have batch run / build generation buttons."""
        app_source = Path("app.py").read_text()
        assert "run_batch(" not in app_source
        assert "Batch size for generation" not in app_source


# ======================================================================
# 11. App UI Contract Tests
# ======================================================================


class TestAppUIContracts:
    """app.py must expose the required buttons."""

    def test_app_has_model_validation_button(self):
        app_source = Path("app.py").read_text()
        assert "Run Model Validation on Suspicious Groups" in app_source

    def test_app_has_save_to_github_button(self):
        app_source = Path("app.py").read_text()
        assert "Save Validation Outputs to GitHub" in app_source

    def test_app_shows_model_validation_status(self):
        app_source = Path("app.py").read_text()
        assert "model_validation_ran" in app_source
        assert "gemini_calls_attempted" in app_source
        assert "openai_calls_attempted" in app_source
        assert "model_validation_items_count" in app_source

    def test_app_shows_no_model_message(self):
        app_source = Path("app.py").read_text()
        assert "No model-based validation was executed; deterministic audit only." in app_source

    def test_full_validation_does_not_auto_call_models_message(self):
        app_source = Path("app.py").read_text()
        assert "does NOT automatically call models" in app_source


# ======================================================================
# 12. Gemini/OpenAI Provider Schema Alignment Tests
# ======================================================================


class TestProviderSchemaAlignment:
    """Gemini and OpenAI providers must use the same unified schema."""

    def test_gemini_imports_unified_schema(self):
        source = Path("engine/validation/providers/gemini_validator.py").read_text()
        assert "from engine.validation.model_schema import" in source
        assert "wrap_provider_result" in source
        assert "normalize_model_output" in source

    def test_openai_imports_unified_schema(self):
        source = Path("engine/validation/providers/openai_reviewer.py").read_text()
        assert "from engine.validation.model_schema import" in source
        assert "wrap_provider_result" in source
        assert "normalize_model_output" in source

    def test_no_schema_mismatch(self):
        """Neither provider should use old validation_results/review_results keys."""
        gemini_src = Path("engine/validation/providers/gemini_validator.py").read_text()
        openai_src = Path("engine/validation/providers/openai_reviewer.py").read_text()
        # Old key patterns should not appear in actual code (only in prompts is ok)
        # Check that _parse_response is gone (replaced by unified parser)
        assert "def _parse_response" not in gemini_src
        assert "def _parse_response" not in openai_src


# ======================================================================
# 13. Patch Suggestions Tests
# ======================================================================


class TestPatchSuggestions:
    """Model suggestions must be suggestions only with safe_to_auto_apply=False."""

    def test_patch_suggestions_model_source(self):
        from engine.validation.validation_outputs import write_patch_suggestions
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "patches.json")
            model_items = [{
                "validation_item_id": "mvi_001",
                "seed_id": "test_seed",
                "suggested_patch": {
                    "has_patch": True,
                    "patch_type": "field_update",
                    "target_variant_id": "v1",
                    "field": "trim",
                    "current_value": "Comfort",
                    "suggested_value": "קומפורט",
                    "reason": "Israeli market name",
                },
                "evidence": [],
                "confidence": 0.8,
                "primary_model": "gemini",
                "secondary_model": "openai",
            }]
            write_patch_suggestions([], [], model_validation_items=model_items,
                                    output_path=output_path)
            data = json.loads(Path(output_path).read_text())
            assert len(data) == 1
            assert data[0]["source"] == "model_validation"
            assert data[0]["safe_to_auto_apply"] is False
            assert data[0]["primary_model"] == "gemini"


# ======================================================================
# 14. Gemini Model ID Normalization Tests
# ======================================================================


class TestGeminiModelNormalization:
    """engine/config.py must normalize known bad Gemini model IDs."""

    def test_normalize_function_direct(self):
        """normalize_gemini_model_id must map known aliases."""
        from engine.config import normalize_gemini_model_id
        assert normalize_gemini_model_id("gemini-3.1-pro") == "gemini-3.1-pro-preview"
        assert normalize_gemini_model_id("models/gemini-3.1-pro") == "gemini-3.1-pro-preview"
        assert normalize_gemini_model_id("gemini-3-pro-preview") == "gemini-3.1-pro-preview"
        assert normalize_gemini_model_id("models/gemini-3-pro-preview") == "gemini-3.1-pro-preview"
        assert normalize_gemini_model_id("models/gemini-3.1-pro-preview") == "gemini-3.1-pro-preview"
        # Unknown values passed through unchanged
        assert normalize_gemini_model_id("gemini-1.5-pro") == "gemini-1.5-pro"
        assert normalize_gemini_model_id("") == ""

    def test_env_var_gemini_validator_model_id_normalized(self):
        """Test A: GEMINI_VALIDATOR_MODEL_ID=gemini-3.1-pro is normalized."""
        import importlib
        import engine.config as cfg
        with mock.patch.dict(os.environ, {"GEMINI_VALIDATOR_MODEL_ID": "gemini-3.1-pro"}, clear=False):
            importlib.reload(cfg)
            result = cfg.get("google", "gemini_validator_model_id")
        importlib.reload(cfg)
        assert result == "gemini-3.1-pro-preview"

    def test_env_var_gemini_model_strong_normalized(self):
        """Test B: GEMINI_MODEL_STRONG=gemini-3.1-pro is normalized."""
        import importlib
        import engine.config as cfg
        with mock.patch.dict(os.environ, {"GEMINI_MODEL_STRONG": "gemini-3.1-pro"}, clear=False):
            # Ensure the more-specific alias is not set
            env = {k: v for k, v in os.environ.items()}
            env.pop("GEMINI_VALIDATOR_MODEL_ID", None)
            env["GEMINI_MODEL_STRONG"] = "gemini-3.1-pro"
            with mock.patch.dict(os.environ, env, clear=True):
                importlib.reload(cfg)
                result = cfg.get("google", "gemini_validator_model_id")
        importlib.reload(cfg)
        assert result == "gemini-3.1-pro-preview"

    def test_default_is_preview(self):
        """Test C: default (no env/secrets) must be gemini-3.1-pro-preview."""
        import importlib
        import engine.config as cfg
        env = {k: v for k, v in os.environ.items()}
        env.pop("GEMINI_VALIDATOR_MODEL_ID", None)
        env.pop("GEMINI_MODEL_STRONG", None)
        with mock.patch.dict(os.environ, env, clear=True):
            importlib.reload(cfg)
            result = cfg.get("google", "gemini_validator_model_id")
        importlib.reload(cfg)
        assert result == "gemini-3.1-pro-preview"

    def test_no_bad_model_ids_in_validation_code(self):
        """Test D: validation source files must not contain raw bad model IDs."""
        bad_ids = ["gemini-3.1-pro", "models/gemini-3.1-pro", "gemini-3-pro-preview"]
        files_to_check = [
            "engine/validation/model_validation_runner.py",
            "engine/validation/providers/gemini_validator.py",
        ]
        for filepath in files_to_check:
            source = Path(filepath).read_text()
            for bad_id in bad_ids:
                # Allow it only inside comments or docstrings (as explanation text)
                # but not as a string literal that would be sent to the API.
                # We check that the bare string is not a Python string literal.
                assert f'"{bad_id}"' not in source, (
                    f"{filepath} contains raw bad model ID literal: {bad_id!r}"
                )
                assert f"'{bad_id}'" not in source, (
                    f"{filepath} contains raw bad model ID literal: {bad_id!r}"
                )
