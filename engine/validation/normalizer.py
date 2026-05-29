"""Deterministic normalizer for validation.

Reuses core.normalize and core.variant_id but adds validation-specific
field extraction helpers (extracting values from VerifiedField objects).
"""
from __future__ import annotations

import re
from typing import Any


def extract_value(field: Any) -> Any:
    """Extract the raw value from a VerifiedField or plain value."""
    if isinstance(field, dict) and "value" in field:
        return field["value"]
    return field


def extract_year(field: Any) -> int | None:
    """Extract year integer from year field (may be {value, used_in_compare} or int)."""
    if isinstance(field, dict) and "value" in field:
        v = field["value"]
    else:
        v = field
    if v is None:
        return None
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


def safe_str(value: Any) -> str:
    """Return a safe lowercase string for comparison."""
    v = extract_value(value)
    if v is None:
        return ""
    return str(v).strip().lower()


def safe_str_original(value: Any) -> str:
    """Return the string value preserving original case."""
    v = extract_value(value)
    if v is None:
        return ""
    return str(v).strip()


def normalize_variant_for_grouping(variant: dict) -> dict:
    """Extract normalized fields from a variant for grouping purposes."""
    return {
        "make": safe_str(variant.get("make")),
        "model": safe_str(variant.get("model")),
        "generation": safe_str(variant.get("generation")),
        "year_start": extract_year(variant.get("year_start")),
        "year_end": extract_year(variant.get("year_end")),
        "engine_family": _engine_family(safe_str(variant.get("engine"))),
        "fuel_type": safe_str(variant.get("fuel_type")),
        "transmission": safe_str(variant.get("transmission")),
        "drivetrain": safe_str(variant.get("drivetrain")),
        "body_type": safe_str(variant.get("body_type")),
        "market": safe_str(variant.get("market")),
        "market_scope": safe_str(variant.get("market_scope")),
    }


def _engine_family(engine_str: str) -> str:
    """Derive a broad engine family for grouping (e.g., '2.0l turbo petrol')."""
    if not engine_str:
        return ""
    # Remove HP/kW/PS ratings to group similar engines
    family = re.sub(r"\d+\s*(?:hp|bhp|ps|kw)\b", "", engine_str, flags=re.IGNORECASE)
    family = re.sub(r"\s+", " ", family).strip()
    return family
