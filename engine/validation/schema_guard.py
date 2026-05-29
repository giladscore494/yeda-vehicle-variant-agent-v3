"""Schema guard — hard quality gates for validation output.

Validates the final output before it is written or committed.
Fails the run if any hard gate is violated.
"""
from __future__ import annotations

import json
import logging
import os
from collections import Counter
from pathlib import Path

logger = logging.getLogger(__name__)


class SchemaGuardError(Exception):
    """Raised when a hard quality gate is violated."""
    pass


def run_hard_gates(
    validated_variants: list[dict],
    output_path: str | Path,
    input_path: str | Path,
    original_input_hash: str | None = None,
) -> tuple[str, list[str]]:
    """Run all hard quality gates. Returns (status, warnings).

    Raises SchemaGuardError if any hard gate fails.
    """
    warnings: list[str] = []
    output_path = Path(output_path).resolve()
    input_path = Path(input_path).resolve()

    # Gate 1: Final JSON must be valid (we're checking in-memory)
    if not isinstance(validated_variants, list):
        raise SchemaGuardError("Final output is not a list of variants")

    # Gate 2: Final output must be variant-level (not grouped)
    for v in validated_variants:
        if not isinstance(v, dict):
            raise SchemaGuardError("Variant entry is not a dict — possible grouped output")
        if "variants" in v and isinstance(v["variants"], list):
            raise SchemaGuardError(
                "Final output appears grouped (contains nested 'variants' list). "
                "Output must be flat variant-level."
            )

    # Gate 3: No duplicate variant_ids
    ids = [v.get("variant_id", "") for v in validated_variants]
    id_counts = Counter(ids)
    duplicates = {vid: count for vid, count in id_counts.items() if count > 1 and vid}
    if duplicates:
        raise SchemaGuardError(
            f"Duplicate variant_id detected: {duplicates}"
        )

    # Gate 4: All markets must be IL
    non_il = []
    for v in validated_variants:
        market = v.get("market", "")
        if isinstance(market, str) and market.upper() not in ("IL", ""):
            non_il.append(v.get("variant_id", "?"))
    if non_il:
        raise SchemaGuardError(
            f"Non-IL market variants in output: {non_il[:10]}"
        )

    # Gate 5: Corrected trims must have source evidence
    for v in validated_variants:
        meta = v.get("validation_metadata", {})
        tc = meta.get("trim_correction")
        if tc and tc.get("action") == "correct":
            sources = meta.get("validation_sources", [])
            if not sources:
                warnings.append(
                    f"Trim correction without sources: {v.get('variant_id', '?')}"
                )

    # Gate 6: Verified variants must have Israeli market support
    for v in validated_variants:
        meta = v.get("validation_metadata", {})
        status = meta.get("validation_status", "")
        if "verified" in status:
            sources = meta.get("validation_sources", [])
            ms = (v.get("market_scope") or "").lower()
            if ms == "global-reference-only" and not sources:
                warnings.append(
                    f"Verified variant lacks IL support: {v.get('variant_id', '?')}"
                )

    # Gate 7: Output path != input path
    if output_path == input_path:
        raise SchemaGuardError("Output path equals input path — refusing to overwrite")

    # Gate 8: Output path is under data/validated_runs/
    if "validated_runs" not in str(output_path):
        raise SchemaGuardError(
            f"Output path not under data/validated_runs/: {output_path}"
        )

    # Gate 9: Original input file was not modified (if hash provided)
    if original_input_hash:
        current_hash = _file_hash(input_path)
        if current_hash and current_hash != original_input_hash:
            raise SchemaGuardError(
                "Original input file has been modified during validation!"
            )

    # Gate 10: Check for hardcoded secrets in output
    output_json = json.dumps(validated_variants)
    secret_patterns = ["sk-", "AIza", "ghp_", "gho_", "github_pat_"]
    for pattern in secret_patterns:
        if pattern in output_json:
            raise SchemaGuardError(
                f"Possible secret/token found in output (pattern: {pattern})"
            )

    status = "passed" if not warnings else "passed_with_warnings"
    return status, warnings


def check_duplicate_variant_ids(variants: list[dict]) -> int:
    """Return count of duplicate variant_ids."""
    ids = [v.get("variant_id", "") for v in variants if v.get("variant_id")]
    return sum(count - 1 for count in Counter(ids).values() if count > 1)


def _file_hash(path: Path) -> str | None:
    """Compute SHA-256 hash of a file."""
    import hashlib

    if not path.exists():
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_input_hash(input_path: str | Path) -> str | None:
    """Compute hash of the input file for integrity verification."""
    return _file_hash(Path(input_path).resolve())
