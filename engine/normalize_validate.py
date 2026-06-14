"""LLM-assisted normalisation and validation for engine-layer variant data.

Uses the configured Gemini model to verify and normalise field values that
cannot be handled by pure rule-based logic in core/normalize.py.
"""
from __future__ import annotations

import logging

from engine.config import ENGINE_MODEL

logger = logging.getLogger(__name__)

# Official Gemini 3 Pro model ID used for all engine-layer LLM calls.
_MODEL_ID: str = ENGINE_MODEL


def get_model_id() -> str:
    """Return the model ID currently configured for engine-layer normalisation."""
    return _MODEL_ID


def validate_variant_fields(variant: dict) -> list[str]:
    """Return a list of validation error messages for the given variant dict.

    This is a rule-based pre-flight check; no LLM call is made here.
    LLM-assisted enrichment happens in llm/client.py via call_model().
    """
    errors: list[str] = []
    if not variant.get("make"):
        errors.append("missing required field: make")
    if not variant.get("model"):
        errors.append("missing required field: model")
    year_start = variant.get("year_start")
    year_end = variant.get("year_end")
    if year_start is not None and year_end is not None:
        try:
            if int(year_start) > int(year_end):
                errors.append(
                    f"year_start ({year_start}) must not exceed year_end ({year_end})"
                )
        except (TypeError, ValueError):
            errors.append("year_start / year_end must be integers")
    return errors


def normalize_variant(variant: dict) -> dict:
    """Return a shallow-normalised copy of *variant* (no LLM call).

    Strips leading/trailing whitespace from string fields and
    lower-cases ``market_scope`` when present.
    """
    out = dict(variant)
    for key, val in out.items():
        if isinstance(val, str):
            out[key] = val.strip()
    if "market_scope" in out and isinstance(out["market_scope"], str):
        out["market_scope"] = out["market_scope"].lower()
    return out
