"""Gemini-only validation client (google-genai).

No OpenAI, no GPT adjudicator, no dual-model flow. This module wraps a single
Gemini call per cluster anchor (or per row when reuse is not possible),
requests strict JSON, parses it, and retries on transient/parse errors a
bounded number of times.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

DEFAULT_MODEL_ID = "gemini-3.1-pro-preview"

PROMPT_TEMPLATE = """You are validating one Israeli-market vehicle variant for a practical car-knowledge database.

This is not a deep research task.
Perform a short, high-quality grounded check.
Answer like a sharp automotive expert after checking the relevant market facts.

Your goal:
Decide whether the core vehicle identity is real, plausible, internally consistent, and relevant to the Israeli market.

Core principle:
Acceptance depends primarily on vehicle identity confidence, not trim confidence.
Vehicle identity is strict.
Trim enrichment is flexible.

Do not reject because trim is missing, generic, placeholder-like, or not strongly verified.

If identity is valid but trim remains unresolved, return clean_partial.

Input variant JSON:
{variant_json}

Per-ID instruction JSON:
{instruction_json}

Known/reused cluster evidence:
{cluster_evidence_json}

Grounding task:
Perform a short grounded check to understand:
- whether this model was sold in Israel
- relevant Israeli years
- available body / engine / fuel / transmission combinations
- known trim levels or marketed names under this model in Israel
- whether the row is one usable variant, a partial model-level identity, or split_required

Decision options:
- clean_exact
- clean_partial
- split_required
- reject

Rules:
1. If identity is valid and trim is missing, return clean_partial.
2. If identity is valid and trim is generic, return clean_partial.
3. If exact Israeli marketed name is unknown, leave it null unless supported.
4. If multiple trims are possible but the technical identity is one usable model-level identity, return clean_partial and list possible_trim_names.
5. If the row clearly combines multiple distinct trims, return split_required and provide split_candidates.
6. Reject only for identity-level contradictions.
7. Never reject solely because trim is Base, Standard, None, null, empty, generic, or unverified.
8. Do not invent exact trim names.
9. Do not over-research.
10. Keep output practical and concise.

Return strict JSON only.
No markdown.
No commentary.

Output schema:
{{
  "validation_id": "...",
  "source_validation_id": "...",
  "source_cluster_id": null,
  "grounding_cluster_id": null,
  "evidence_reused_from": null,
  "canonical_make": null,
  "canonical_model": null,
  "canonical_series_or_generation": null,
  "canonical_trim": null,
  "official_marketed_name_il": null,
  "body_type": null,
  "fuel_type": null,
  "engine": null,
  "transmission": null,
  "drivetrain": null,
  "year_start": null,
  "year_end": null,
  "market_scope": "IL",
  "validation_decision": "clean_exact | clean_partial | split_required | reject",
  "acceptance_tier": "exact | partial | none",
  "identity_status": "verified | likely_valid | uncertain | invalid",
  "identity_confidence": 0.0,
  "trim_status": "verified | inferred | unresolved | invalid",
  "trim_confidence": 0.0,
  "grounding_summary": "",
  "evidence_sources": [],
  "possible_trim_names": [],
  "split_candidates": [],
  "blocking_identity_issues": [],
  "non_blocking_trim_issues": [],
  "fields_changed": [],
  "fields_left_unresolved": [],
  "decision_reason": ""
}}
"""


def render_prompt(
    variant: Dict[str, Any],
    instruction: Dict[str, Any],
    cluster_evidence: Optional[Dict[str, Any]] = None,
) -> str:
    return PROMPT_TEMPLATE.format(
        variant_json=json.dumps(variant, ensure_ascii=False),
        instruction_json=json.dumps(instruction, ensure_ascii=False),
        cluster_evidence_json=json.dumps(cluster_evidence or {}, ensure_ascii=False),
    )


def parse_strict_json(text: str) -> Dict[str, Any]:
    """Parse model output, tolerating accidental code fences."""
    if text is None:
        raise ValueError("empty model response")
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Last resort: grab the first balanced JSON object.
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


@dataclass
class GeminiSettings:
    api_key: str
    model_id: str = DEFAULT_MODEL_ID
    grounding_enabled: bool = True
    max_retries: int = 2
    timeout_s: int = 90


class GeminiClient:
    """Thin wrapper around google-genai for JSON validation responses."""

    def __init__(self, settings: GeminiSettings) -> None:
        if not settings.api_key:
            raise ValueError("Gemini API key is missing")
        self.settings = settings
        self._client = None  # lazy

    def _ensure_client(self):
        if self._client is None:
            from google import genai  # imported lazily so mock mode needs no dep

            self._client = genai.Client(api_key=self.settings.api_key)
        return self._client

    def _build_config(self):
        from google.genai import types

        tools = None
        if self.settings.grounding_enabled:
            try:
                tools = [types.Tool(google_search=types.GoogleSearch())]
            except Exception:  # noqa: BLE001 - grounding optional
                tools = None
        return types.GenerateContentConfig(
            tools=tools,
            response_mime_type="application/json" if tools is None else None,
            temperature=0.2,
        )

    def validate(
        self,
        variant: Dict[str, Any],
        instruction: Dict[str, Any],
        cluster_evidence: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Run one Gemini validation call and return parsed JSON."""
        client = self._ensure_client()
        config = self._build_config()
        prompt = render_prompt(variant, instruction, cluster_evidence)

        last_err: Optional[Exception] = None
        for attempt in range(self.settings.max_retries + 1):
            try:
                resp = client.models.generate_content(
                    model=self.settings.model_id,
                    contents=prompt,
                    config=config,
                )
                text = getattr(resp, "text", None)
                return parse_strict_json(text)
            except (json.JSONDecodeError, ValueError) as exc:
                # Parse failure: retry once or twice, never loop on trim doubt.
                last_err = exc
            except Exception as exc:  # noqa: BLE001 - transient API errors
                last_err = exc
            if attempt < self.settings.max_retries:
                time.sleep(min(2 ** attempt, 8))
        raise RuntimeError(f"Gemini validation failed: {last_err}")
