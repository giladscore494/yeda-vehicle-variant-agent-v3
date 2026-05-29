"""Tests for engine/normalize_validate.py and engine/validation/openai_utils.py."""
from __future__ import annotations

import pytest

from engine.normalize_validate import (
    get_model_id,
    normalize_variant,
    validate_variant_fields,
)
from engine.validation.openai_utils import web_search_generate


# ---------------------------------------------------------------------------
# Model ID
# ---------------------------------------------------------------------------

class TestModelId:
    def test_model_id_is_gemini_3_pro_preview(self):
        """Engine model ID must use the official gemini-3-pro-preview identifier."""
        mid = get_model_id()
        assert mid == "gemini-3-pro-preview", (
            f"Expected 'gemini-3-pro-preview', got '{mid}'. "
            "Update engine/config.py or core/config.py to fix the model ID."
        )

    def test_model_id_not_gemini_3_1(self):
        """Gemini 3.1 model IDs are invalid; must not appear in engine config."""
        mid = get_model_id()
        assert "3.1" not in mid, (
            f"Invalid model ID '{mid}' contains '3.1'. "
            "Replace with 'gemini-3-pro-preview'."
        )


# ---------------------------------------------------------------------------
# validate_variant_fields
# ---------------------------------------------------------------------------

class TestValidateVariantFields:
    def test_valid_variant_returns_no_errors(self):
        variant = {
            "make": "Toyota",
            "model": "Corolla",
            "year_start": 2020,
            "year_end": 2024,
        }
        assert validate_variant_fields(variant) == []

    def test_missing_make_is_error(self):
        variant = {"model": "Corolla", "year_start": 2020, "year_end": 2024}
        errors = validate_variant_fields(variant)
        assert any("make" in e for e in errors)

    def test_missing_model_is_error(self):
        variant = {"make": "Toyota", "year_start": 2020, "year_end": 2024}
        errors = validate_variant_fields(variant)
        assert any("model" in e for e in errors)

    def test_inverted_years_is_error(self):
        variant = {
            "make": "Toyota",
            "model": "Corolla",
            "year_start": 2025,
            "year_end": 2020,
        }
        errors = validate_variant_fields(variant)
        assert any("year_start" in e for e in errors)

    def test_equal_years_is_valid(self):
        variant = {
            "make": "Toyota",
            "model": "Corolla",
            "year_start": 2022,
            "year_end": 2022,
        }
        assert validate_variant_fields(variant) == []

    def test_missing_years_does_not_error(self):
        """year_start / year_end are optional."""
        variant = {"make": "Toyota", "model": "Corolla"}
        assert validate_variant_fields(variant) == []


# ---------------------------------------------------------------------------
# normalize_variant
# ---------------------------------------------------------------------------

class TestNormalizeVariant:
    def test_strips_whitespace(self):
        variant = {"make": "  Toyota  ", "model": " Corolla "}
        out = normalize_variant(variant)
        assert out["make"] == "Toyota"
        assert out["model"] == "Corolla"

    def test_lowercases_market_scope(self):
        variant = {"make": "Toyota", "model": "Corolla", "market_scope": "IL-Confirmed"}
        out = normalize_variant(variant)
        assert out["market_scope"] == "il-confirmed"

    def test_does_not_mutate_original(self):
        variant = {"make": "  Toyota  "}
        _ = normalize_variant(variant)
        assert variant["make"] == "  Toyota  "

    def test_non_string_fields_unchanged(self):
        variant = {"make": "Toyota", "model": "Corolla", "year_start": 2020}
        out = normalize_variant(variant)
        assert out["year_start"] == 2020


# ---------------------------------------------------------------------------
# web_search_generate (openai_utils)
# ---------------------------------------------------------------------------

class _FakeResponse:
    def __init__(self, text: str = "ok"):
        self.text = text


class _BadRequest(Exception):
    status_code = 400


class _ServerError(Exception):
    status_code = 500


class TestWebSearchGenerate:
    """Unit tests using a fake OpenAI-like client."""

    class _ClientAlwaysOk:
        def __init__(self):
            self.calls: list[dict] = []

        class responses:
            pass

        def __init__(self):
            self.calls: list[dict] = []
            self.responses = self._Responses(self)

        class _Responses:
            def __init__(self, parent):
                self._parent = parent

            def create(self, **kwargs):
                self._parent.calls.append(kwargs)
                return _FakeResponse()

    def _make_client(self, fail_tools=None):
        """Return a fake client.  fail_tools is a set of tool-type strings that raise 400."""
        fail_tools = fail_tools or set()

        class _Responses:
            def __init__(self, calls, fail_tools_):
                self._calls = calls
                self._fail = fail_tools_

            def create(self_, **kwargs):  # noqa: N805
                self_.calls = getattr(self_, "calls", [])
                tools = kwargs.get("tools")
                tool_type = tools[0]["type"] if tools else None
                self_._calls.append({"tool_type": tool_type, **kwargs})
                if tool_type in self_._fail:
                    raise _BadRequest(f"unsupported tool: {tool_type}")
                return _FakeResponse(text=f"response-with-{tool_type}")

        client = type("FakeClient", (), {})()
        client._calls: list[dict] = []
        client.responses = _Responses(client._calls, fail_tools)
        return client

    def test_first_attempt_succeeds(self):
        client = self._make_client()
        resp = web_search_generate(client, "gpt-4o", input="hello")
        assert resp.text == "response-with-web_search"
        assert client._calls[0]["tool_type"] == "web_search"

    def test_falls_back_to_web_search_preview_on_400(self):
        client = self._make_client(fail_tools={"web_search"})
        resp = web_search_generate(client, "gpt-4o", input="hello")
        assert resp.text == "response-with-web_search_preview"

    def test_falls_back_to_no_tools_on_double_400(self):
        client = self._make_client(fail_tools={"web_search", "web_search_preview"})
        resp = web_search_generate(client, "gpt-4o", input="hello")
        assert resp.text == "response-with-None"

    def test_raises_on_non_400_error(self):
        client = self._make_client()
        # Patch responses.create to always raise a 500
        def _bad_create(**kwargs):
            raise _ServerError("internal error")

        client.responses.create = _bad_create
        with pytest.raises(_ServerError):
            web_search_generate(client, "gpt-4o", input="hello")

    def test_raises_when_all_attempts_fail(self):
        client = self._make_client(
            fail_tools={"web_search", "web_search_preview", None}
        )

        def _always_400(**kwargs):
            raise _BadRequest("always 400")

        client.responses.create = _always_400
        with pytest.raises(_BadRequest):
            web_search_generate(client, "gpt-4o", input="hello")
