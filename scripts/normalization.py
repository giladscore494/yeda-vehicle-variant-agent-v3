"""Normalization helpers and identity extraction.

These helpers implement the *flexible trim* / *strict identity* principle at
the deterministic layer. Crucially, they classify weak trims but never use a
weak trim as grounds for rejection.
"""

from __future__ import annotations

import datetime
import re
from typing import Any, Dict, List, Optional

from .data_loader import get_standard, get_validation_id

# Values that mean "no real trim" — these must NOT trigger rejection.
PLACEHOLDER_TRIMS = {
    "",
    "base",
    "standard",
    "none",
    "null",
    "n/a",
    "na",
    "unknown",
    "undefined",
    "tbd",
    "-",
    "—",
    "generic",
    "default",
}

# Identity-critical fields (strict).
IDENTITY_FIELDS = [
    "make",
    "model",
    "engine",
    "transmission",
    "fuel_type",
    "drivetrain",
    "body_type",
    "year_start",
    "year_end",
]

# Trim / enrichment fields (flexible).
TRIM_FIELDS = [
    "trim",
    "trim_name",
    "trim_name_il",
    "official_marketed_name_il",
    "local_brand_name_il",
    "local_variant_name",
    "alternate_names",
]

_MIN_YEAR = 1885  # first automobile
_MAX_YEAR = datetime.datetime.utcnow().year + 2


# ---------------------------------------------------------------------------
# Scalar normalization
# ---------------------------------------------------------------------------


def norm_str(value: Any) -> Optional[str]:
    """Trim whitespace; map empty/placeholder-empty strings to ``None``."""
    if value is None:
        return None
    if not isinstance(value, str):
        value = str(value)
    cleaned = value.strip()
    if cleaned == "" or cleaned.lower() in {"null", "none", "n/a", "na"}:
        return None
    return cleaned


def norm_key(value: Any) -> str:
    """Lowercase, collapse whitespace/punctuation — for cluster keys."""
    s = norm_str(value)
    if s is None:
        return ""
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def norm_year(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        year = int(str(value).strip())
    except (TypeError, ValueError):
        return None
    return year


def is_weak_trim(value: Any) -> bool:
    """True when the trim is missing, empty, or a generic placeholder."""
    if value is None:
        return True
    if isinstance(value, (list, tuple)):
        return len([v for v in value if not is_weak_trim(v)]) == 0
    s = norm_str(value)
    if s is None:
        return True
    return s.lower() in PLACEHOLDER_TRIMS


# ---------------------------------------------------------------------------
# Identity extraction
# ---------------------------------------------------------------------------


def extract_identity(variant: Dict[str, Any]) -> Dict[str, Any]:
    """Pull the strict identity fields out of a raw variant record."""
    std = get_standard(variant)
    return {
        "make": norm_str(std.get("make")),
        "model": norm_str(std.get("model")),
        "global_model_name": norm_str(std.get("global_model_name")),
        "generation": norm_str(std.get("generation")),
        "engine": norm_str(std.get("engine")),
        "transmission": norm_str(std.get("transmission")),
        "fuel_type": norm_str(std.get("fuel_type")),
        "drivetrain": norm_str(std.get("drivetrain")),
        "body_type": norm_str(std.get("body_type")),
        "year_start": norm_year(std.get("year_start")),
        "year_end": norm_year(std.get("year_end")),
        "market_scope": norm_str(std.get("market_scope")) or "IL",
    }


def extract_trim(variant: Dict[str, Any]) -> Dict[str, Any]:
    """Pull the flexible trim/enrichment fields out of a raw variant record."""
    std = get_standard(variant)
    alt = std.get("alternate_names")
    if not isinstance(alt, list):
        alt = []
    return {
        "trim": norm_str(std.get("trim")),
        "official_marketed_name_il": norm_str(std.get("official_marketed_name_il")),
        "local_brand_name_il": norm_str(std.get("local_brand_name_il")),
        "alternate_names": [a for a in (norm_str(x) for x in alt) if a],
        "trim_is_weak": is_weak_trim(std.get("trim")),
    }


# ---------------------------------------------------------------------------
# Deterministic pre-checks — identity-level ONLY.
# ---------------------------------------------------------------------------


def detect_identity_blockers(identity: Dict[str, Any]) -> List[str]:
    """Return obvious identity-level problems (never trim-only issues).

    These are the *only* deterministic reasons a row may be pre-rejected
    before Gemini. Weak/missing trim is intentionally ignored here.
    """
    issues: List[str] = []

    if not identity.get("make"):
        issues.append("missing_make")
    if not identity.get("model"):
        issues.append("missing_model")

    ys, ye = identity.get("year_start"), identity.get("year_end")
    if ys is not None and (ys < _MIN_YEAR or ys > _MAX_YEAR):
        issues.append("implausible_year_start")
    if ye is not None and (ye < _MIN_YEAR or ye > _MAX_YEAR):
        issues.append("implausible_year_end")
    if ys is not None and ye is not None and ys > ye:
        issues.append("year_start_after_year_end")

    # Powertrain contradiction: a pure-electric fuel type with a combustion
    # displacement engine signature is internally inconsistent.
    fuel = (identity.get("fuel_type") or "").lower()
    engine = (identity.get("engine") or "").lower()
    if fuel in {"electric", "ev", "bev"} and re.search(r"\d+\.\d+\s*l|turbo|tdi|tsi", engine):
        issues.append("electric_fuel_with_combustion_engine")

    return issues
