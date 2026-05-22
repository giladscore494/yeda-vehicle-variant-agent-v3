"""Parse raw LLM JSON response into SeedRunResult."""
from __future__ import annotations

import json
import re

from engine.types import SeedRunResult


def _extract_json(text: str) -> dict:
    """Extract JSON object from text that may contain markdown fences."""
    text = text.strip()
    # Remove markdown code fences
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()
    # Try to parse
    return json.loads(text)


def parse_llm_response(raw_text: str, seed_id: str) -> SeedRunResult:
    """Parse raw LLM response text into a SeedRunResult."""
    try:
        data = _extract_json(raw_text)
    except (json.JSONDecodeError, ValueError) as exc:
        return SeedRunResult(
            seed_id=seed_id,
            ok=False,
            errors=[f"JSON parse error: {exc}"],
            raw_response={"raw_text": raw_text[:2000]},
        )

    if not isinstance(data, dict):
        return SeedRunResult(
            seed_id=seed_id,
            ok=False,
            errors=["response is not a JSON object"],
            raw_response={"raw_text": raw_text[:2000]},
        )

    return SeedRunResult(
        seed_id=seed_id,
        ok=True,
        candidate_variants=data.get("candidate_variants") or [],
        no_variants_reason=data.get("no_variants_reason"),
        no_variants_source_ids=data.get("no_variants_source_ids") or [],
        no_variants_source_basis=data.get("no_variants_source_basis"),
        no_variants_confidence=data.get("no_variants_confidence"),
        sources=data.get("sources") or [],
        raw_response=data,
    )
