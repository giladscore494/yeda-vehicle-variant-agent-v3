"""Load and validate the two source-of-truth JSON files.

The two source files are the source of truth and must never be modified:

- data/validation_variants_data_v1.json      (key: ``variants``)
- data/validation_instructions_by_id_v1.json  (key: ``instructions_by_validation_id``)

This module only reads them, validates their join, and exposes convenient
accessors. It never writes to them.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")

VARIANTS_PATH = os.path.join(DATA_DIR, "validation_variants_data_v1.json")
INSTRUCTIONS_PATH = os.path.join(DATA_DIR, "validation_instructions_by_id_v1.json")

VARIANTS_KEY = "variants"
INSTRUCTIONS_KEY = "instructions_by_validation_id"
JOIN_KEY = "validation_id"
STANDARD_VARIANT_KEY = "standard_variant"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class JoinResult:
    """Result of joining variants with per-id instructions."""

    variants: List[Dict[str, Any]]
    instructions: Dict[str, Any]
    ordered_ids: List[str]
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def variant_count(self) -> int:
        return len(self.variants)

    @property
    def instruction_count(self) -> int:
        return len(self.instructions)

    def summary(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "variant_count": self.variant_count,
            "instruction_count": self.instruction_count,
            "joined_ids": len(self.ordered_ids),
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_variants(path: str = VARIANTS_PATH) -> List[Dict[str, Any]]:
    """Load the raw variants list (under the ``variants`` key)."""
    doc = _load_json(path)
    if not isinstance(doc, dict) or VARIANTS_KEY not in doc:
        raise ValueError(
            f"Variants file {path!r} missing required key {VARIANTS_KEY!r}"
        )
    variants = doc[VARIANTS_KEY]
    if not isinstance(variants, list):
        raise ValueError(f"{VARIANTS_KEY!r} must be a list")
    return variants


def load_instructions(path: str = INSTRUCTIONS_PATH) -> Dict[str, Any]:
    """Load the per-id instruction mapping."""
    doc = _load_json(path)
    if not isinstance(doc, dict) or INSTRUCTIONS_KEY not in doc:
        raise ValueError(
            f"Instructions file {path!r} missing required key {INSTRUCTIONS_KEY!r}"
        )
    mapping = doc[INSTRUCTIONS_KEY]
    if not isinstance(mapping, dict):
        raise ValueError(f"{INSTRUCTIONS_KEY!r} must be an object/mapping")
    return mapping


# ---------------------------------------------------------------------------
# Accessors
# ---------------------------------------------------------------------------


def get_validation_id(variant: Dict[str, Any]) -> Optional[str]:
    return variant.get(JOIN_KEY)


def get_standard(variant: Dict[str, Any]) -> Dict[str, Any]:
    """Return the ``standard_variant`` sub-object (the identity payload)."""
    std = variant.get(STANDARD_VARIANT_KEY)
    return std if isinstance(std, dict) else {}


# ---------------------------------------------------------------------------
# Join validation
# ---------------------------------------------------------------------------


def files_present() -> Dict[str, bool]:
    return {
        VARIANTS_PATH: os.path.exists(VARIANTS_PATH),
        INSTRUCTIONS_PATH: os.path.exists(INSTRUCTIONS_PATH),
    }


def validate_and_join(
    variants_path: str = VARIANTS_PATH,
    instructions_path: str = INSTRUCTIONS_PATH,
) -> JoinResult:
    """Run all deterministic pre-checks and build the join.

    Critical failures land in ``errors`` (the run must stop before any model
    call). Non-critical observations land in ``warnings``.
    """
    errors: List[str] = []
    warnings: List[str] = []

    if not os.path.exists(variants_path):
        errors.append(f"Variants file not found: {variants_path}")
    if not os.path.exists(instructions_path):
        errors.append(f"Instructions file not found: {instructions_path}")
    if errors:
        return JoinResult([], {}, [], errors, warnings)

    try:
        variants = load_variants(variants_path)
    except Exception as exc:  # noqa: BLE001 - surfaced to caller
        errors.append(f"Failed to parse variants file: {exc}")
        variants = []
    try:
        instructions = load_instructions(instructions_path)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Failed to parse instructions file: {exc}")
        instructions = {}

    if errors:
        return JoinResult(variants, instructions, [], errors, warnings)

    ordered_ids: List[str] = []
    seen: set = set()

    for idx, variant in enumerate(variants):
        vid = get_validation_id(variant)
        if not vid:
            errors.append(f"Variant at index {idx} is missing {JOIN_KEY!r}")
            continue
        if vid in seen:
            errors.append(f"Duplicate {JOIN_KEY}: {vid}")
            continue
        seen.add(vid)
        ordered_ids.append(vid)  # preserve input order
        if vid not in instructions:
            errors.append(f"Variant {vid} has no matching instruction record")

    # Instructions without a variant (informational, not fatal).
    extra_instructions = [k for k in instructions if k not in seen]
    if extra_instructions:
        warnings.append(
            f"{len(extra_instructions)} instruction record(s) have no matching variant"
        )

    if len(variants) != len(instructions):
        warnings.append(
            f"Count mismatch: {len(variants)} variants vs "
            f"{len(instructions)} instruction records"
        )

    return JoinResult(variants, instructions, ordered_ids, errors, warnings)
