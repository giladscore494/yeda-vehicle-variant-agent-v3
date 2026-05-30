"""Gemini validator — primary grounded validator for Israeli-market trims.

Uses Google Gemini with grounding/search to validate variant groups.
Focus: Israeli-market trim/grade/gimur verification.

Uses the unified model schema from model_schema.py.
"""
from __future__ import annotations

import json
import logging
from typing import Any

from engine import config
from engine.validation.normalizer import safe_str_original, safe_str, extract_value
from engine.validation.model_schema import (
    normalize_model_output,
    parse_model_json,
    validate_item,
    wrap_provider_result,
)

logger = logging.getLogger(__name__)


def _build_validation_prompt(
    group_key: str,
    variants: list[dict],
    trim_candidates: list[str],
) -> str:
    """Build a grounded validation prompt for a group of Israeli-market variants."""
    make = safe_str_original(variants[0].get("make")) if variants else "Unknown"
    model = safe_str_original(variants[0].get("model")) if variants else "Unknown"
    gen = safe_str_original(variants[0].get("generation")) if variants else ""

    variant_summaries = []
    for v in variants:
        vid = v.get("variant_id", "?")
        trim = safe_str_original(v.get("trim"))
        engine = safe_str_original(v.get("engine"))
        fuel = safe_str_original(v.get("fuel_type"))
        marketed = v.get("official_marketed_name_il") or ""
        ms = v.get("market_scope") or ""
        yr_s = extract_value(v.get("year_start"))
        yr_e = extract_value(v.get("year_end"))
        variant_summaries.append(
            f"  - variant_id: {vid}\n"
            f"    trim: {trim}\n"
            f"    engine: {engine}\n"
            f"    fuel: {fuel}\n"
            f"    years: {yr_s}-{yr_e}\n"
            f"    marketed_name_il: {marketed}\n"
            f"    market_scope: {ms}"
        )

    variants_block = "\n".join(variant_summaries)
    trims_block = ", ".join(trim_candidates) if trim_candidates else "(none)"

    return f"""You are an Israeli automotive market expert validator.

TASK: Validate the following vehicle variants for the Israeli market.
Focus especially on trim/grade/gimur names.

Vehicle: {make} {model} {gen}
Group key: {group_key}
Trim candidates found: {trims_block}

Variants:
{variants_block}

For EACH variant, answer:
1. Does this exact trim/grade name exist in the Israeli market?
2. Is it an official Israeli trim, marketing name, engine level, package name, or invented filler?
3. Is there a better official Israeli-market name?
4. Should the trim be kept, corrected, nullified, merged, split, or sent to manual_review?
5. Which sources support the decision?

Source priority (use Israeli sources first):
1. Official importer / official Israeli brochure / price list
2. iCar, Cartube, Auto.co.il
3. Reputable Israeli automotive review/spec pages
4. Yad2/listings only as secondary support
Do NOT use global sources alone to verify Israeli trim existence.

Respond in valid JSON with this structure:
{{
  "group_key": "{group_key}",
  "validation_results": [
    {{
      "variant_id": "...",
      "trim_exists_in_il": true/false/null,
      "trim_is_official": true/false/null,
      "suggested_correction": null or "corrected trim name",
      "action": "keep" | "correct" | "nullify" | "manual_review",
      "confidence": "high" | "medium" | "low",
      "source_refs": ["source1", "source2"],
      "reason": "explanation"
    }}
  ]
}}

Return ONLY valid JSON. No markdown fences. No explanatory text outside JSON."""


def estimate_tokens(prompt: str) -> tuple[int, int]:
    """Estimate input and output tokens for a prompt."""
    input_est = len(prompt) // 3
    output_est = max(500, input_est // 2)
    return input_est, output_est


def validate_group(
    group_key: str,
    variants: list[dict],
    trim_candidates: list[str],
    cost_tracker: Any = None,
) -> dict:
    """Validate a group using Gemini. Returns wrapped provider result dict.

    Uses the unified model schema. Result follows the normalized envelope:
    {ok, provider, model_id, item_id, parsed_result, raw_text, error_type, error_message}
    """
    api_key = config.get("google", "api_key")
    model_id = config.get("google", "gemini_validator_model_id")
    grounding = config.get_bool("google", "grounding_enabled", True)

    if not api_key:
        logger.error("Google API key not configured — cannot validate")
        return wrap_provider_result(
            False, "gemini", model_id or "", group_key,
            error_type="model_auth_error",
            error_message="Google API key not configured",
        )

    prompt = _build_validation_prompt(group_key, variants, trim_candidates)
    input_est, output_est = estimate_tokens(prompt)
    variant_ids = [v.get("variant_id", "") for v in variants]

    if cost_tracker:
        cost_tracker.log_planned(
            "gemini", model_id, group_key, variant_ids,
            input_est, output_est, search_used=grounding,
        )

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        generate_kwargs: dict[str, Any] = {}
        if grounding:
            try:
                from google.genai import types
                generate_kwargs["config"] = types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            except Exception:
                logger.warning("Grounding tool setup failed; proceeding without grounding")

        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            **generate_kwargs,
        )

        raw_text = response.text or ""
        input_actual = getattr(
            getattr(response, "usage_metadata", None), "prompt_token_count", None
        )
        output_actual = getattr(
            getattr(response, "usage_metadata", None), "candidates_token_count", None
        )

        if cost_tracker:
            cost_tracker.log_actual(
                "gemini", model_id, group_key, variant_ids,
                input_est, output_est, input_actual, output_actual,
                search_used=grounding, status="success",
            )

        # Parse using unified schema
        parsed, parse_error = parse_model_json(raw_text)
        if parse_error:
            return wrap_provider_result(
                False, "gemini", model_id, group_key,
                raw_text=raw_text,
                error_type="model_parse_error",
                error_message="Failed to parse Gemini JSON response",
            )

        # Normalize to unified schema
        normalized = normalize_model_output(parsed, group_key, model_id, "primary")
        schema_errors = validate_item(normalized)
        if schema_errors:
            return wrap_provider_result(
                False, "gemini", model_id, group_key,
                parsed_result=normalized, raw_text=raw_text,
                error_type="validation_schema_error",
                error_message=f"Schema validation failed: {'; '.join(schema_errors)}",
            )

        return wrap_provider_result(
            True, "gemini", model_id, group_key,
            parsed_result=normalized, raw_text=raw_text,
        )

    except Exception as exc:
        logger.error("Gemini call failed for %s: %s", group_key, exc)
        if cost_tracker:
            cost_tracker.log_actual(
                "gemini", model_id, group_key, variant_ids,
                input_est, output_est, None, None,
                search_used=grounding, status="error",
            )
        return wrap_provider_result(
            False, "gemini", model_id, group_key,
            error_type="model_call_error",
            error_message=str(exc),
        )

