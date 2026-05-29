"""OpenAI GPT reviewer — second reviewer for high-risk and critical cases.

Used for: trim corrections, promoted verifications, merge/split decisions,
model disagreement resolution, and sampled audit.
"""
from __future__ import annotations

import json
import logging
from typing import Any

from engine import config
from engine.validation.normalizer import safe_str_original, safe_str, extract_value

logger = logging.getLogger(__name__)


def _build_review_prompt(
    group_key: str,
    variants: list[dict],
    trim_candidates: list[str],
    gemini_result: dict | None = None,
) -> str:
    """Build a review prompt for OpenAI GPT, optionally including Gemini's assessment."""
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
            f"    trim: {trim}, engine: {engine}, fuel: {fuel}\n"
            f"    years: {yr_s}-{yr_e}, marketed_name_il: {marketed}, market_scope: {ms}"
        )

    variants_block = "\n".join(variant_summaries)
    trims_block = ", ".join(trim_candidates) if trim_candidates else "(none)"

    gemini_block = ""
    if gemini_result:
        gemini_block = f"""

PREVIOUS REVIEWER (Gemini) ASSESSMENT:
{json.dumps(gemini_result, indent=2, ensure_ascii=False)}

If you agree with Gemini's assessment, confirm it.
If you disagree, explain why and provide your own assessment."""

    return f"""You are a second-opinion reviewer for Israeli automotive market data.

TASK: Review and validate the following vehicle variants for the Israeli market.
Focus on trim/grade/gimur name accuracy. This is a HIGH-RISK or CRITICAL case.

Vehicle: {make} {model} {gen}
Group key: {group_key}
Trim candidates: {trims_block}

Variants:
{variants_block}
{gemini_block}

For EACH variant, determine:
1. Does this trim/grade name exist in the Israeli market?
2. Is it an official trim or an invented/generic filler?
3. If incorrect, what is the correct Israeli-market name?
4. Should the trim be kept, corrected, nullified, or sent to manual_review?
5. Which Israeli sources support this?

Respond in valid JSON:
{{
  "group_key": "{group_key}",
  "review_results": [
    {{
      "variant_id": "...",
      "agrees_with_primary": true/false,
      "trim_exists_in_il": true/false/null,
      "trim_is_official": true/false/null,
      "suggested_correction": null or "corrected trim",
      "action": "keep" | "correct" | "nullify" | "manual_review",
      "confidence": "high" | "medium" | "low",
      "source_refs": ["source1", "source2"],
      "reason": "explanation"
    }}
  ]
}}

Return ONLY valid JSON."""


def estimate_tokens(prompt: str) -> tuple[int, int]:
    input_est = len(prompt) // 3
    output_est = max(500, input_est // 2)
    return input_est, output_est


def review_group(
    group_key: str,
    variants: list[dict],
    trim_candidates: list[str],
    gemini_result: dict | None = None,
    cost_tracker: Any = None,
) -> dict | None:
    """Review a group using OpenAI GPT. Returns parsed response or None."""
    api_key = config.get("openai", "api_key")
    model_id = config.get("openai", "validator_model_id")
    web_search = config.get_bool("openai", "web_search_enabled", True)

    if not api_key:
        logger.error("OpenAI API key not configured — cannot review")
        return None

    prompt = _build_review_prompt(group_key, variants, trim_candidates, gemini_result)
    input_est, output_est = estimate_tokens(prompt)
    variant_ids = [v.get("variant_id", "") for v in variants]

    if cost_tracker:
        cost_tracker.log_planned(
            "openai", model_id, group_key, variant_ids,
            input_est, output_est, search_used=web_search,
        )

    try:
        import openai

        client = openai.OpenAI(api_key=api_key)

        tools = None
        if web_search:
            tools = [{"type": "web_search_preview"}]

        response = client.responses.create(
            model=model_id,
            input=prompt,
            tools=tools,
        )

        raw_text = ""
        for item in response.output:
            if hasattr(item, "content"):
                for block in item.content:
                    if hasattr(block, "text"):
                        raw_text += block.text

        input_actual = getattr(getattr(response, "usage", None), "input_tokens", None)
        output_actual = getattr(getattr(response, "usage", None), "output_tokens", None)

        if cost_tracker:
            cost_tracker.log_actual(
                "openai", model_id, group_key, variant_ids,
                input_est, output_est, input_actual, output_actual,
                search_used=web_search, status="success",
            )

        return _parse_response(raw_text, group_key)

    except Exception as exc:
        logger.error("OpenAI call failed for %s: %s", group_key, exc)
        if cost_tracker:
            cost_tracker.log_actual(
                "openai", model_id, group_key, variant_ids,
                input_est, output_est, None, None,
                search_used=web_search, status="error",
            )
        return None


def _parse_response(raw_text: str, group_key: str) -> dict | None:
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "review_results" in data:
            return data
        return data if isinstance(data, dict) else None
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse OpenAI JSON for %s: %s", group_key, exc)
        return None
