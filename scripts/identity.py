"""Deterministic identity key / hash / variant-id helpers.

Reproduces exactly the recipe used to build `canonical_identity_key` and
`canonical_identity_hash` in data/validation_variants_data_v1.json
(verified 3712/3712 against the source data):

    key  = make|model|year_start|year_end|generation|engine|transmission|
           body_type|fuel_type|drivetrain|trim          (normalized, see below)
    hash = sha256(key)[:16]

The same recipe is applied to validated fields to produce
`validated_identity_hash`, so a record whose critical identity fields were
corrected by validation gets a different hash, while an unchanged record
keeps a hash equal to its original one.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any

# Field order of the canonical identity key (seats is NOT part of the key).
IDENTITY_KEY_FIELDS = (
    "make", "model", "year_start", "year_end", "generation", "engine",
    "transmission", "body_type", "fuel_type", "drivetrain", "trim",
)

# Critical identity fields per product rules (superset of the key fields
# minus make/model, plus seats).
CRITICAL_IDENTITY_FIELDS = (
    "year_start", "year_end", "engine", "transmission", "fuel_type",
    "drivetrain", "trim", "body_type", "seats", "generation",
)

MISSING_MARKER = "<missing>"


def normalize_identity_value(value: Any) -> str:
    """Normalize one identity field the same way the source data did."""
    if value is None or str(value).strip() == "":
        return MISSING_MARKER
    s = str(value).strip().lower()
    s = re.sub(r"[_\-]", " ", s)
    s = re.sub(r"\bpetrol\b", "gasoline", s)
    s = re.sub(r"\bdct\b", "dual clutch", s)
    s = re.sub(r"\bauto\b", "automatic", s)
    s = re.sub(r"\s+", " ", s)
    return s


def identity_key(fields: dict) -> str:
    return "|".join(normalize_identity_value(fields.get(f))
                    for f in IDENTITY_KEY_FIELDS)


def identity_hash(fields: dict) -> str:
    return hashlib.sha256(identity_key(fields).encode("utf-8")).hexdigest()[:16]


def _slug(value: Any) -> str:
    s = str(value).strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def build_validated_variant_id(fields: dict) -> str:
    """Build a variant id from validated fields, following the source pattern
    make_model_ys_ye_il_generation_engine_transmission_body_fuel (+trim when
    present, so distinct trims never collide)."""
    parts = [fields.get("make"), fields.get("model"),
             fields.get("year_start"), fields.get("year_end"), "il",
             fields.get("generation"), fields.get("engine"),
             fields.get("transmission"), fields.get("body_type"),
             fields.get("fuel_type")]
    trim = fields.get("trim")
    if trim not in (None, "") and str(trim).strip():
        parts.append(trim)
    return "_".join(_slug(p) for p in parts if p not in (None, "")
                    and str(p).strip())
