"""Helpers for reporting canonical, validation, and final database file status."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.paths import (
    FINAL_CLEAN_DATABASE_PATH,
    SOURCE_CANONICAL_PATH,
    STALE_ROOT_CANONICAL_PATH,
)


def _load_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _variant_counts(payload: Any) -> tuple[int, int, int]:
    """Return total, verified, and partial variant counts for known payload shapes."""
    if isinstance(payload, dict):
        verified = payload.get("verified_variants")
        partial = payload.get("partial_variants")
        verified_count = len(verified) if isinstance(verified, list) else 0
        partial_count = len(partial) if isinstance(partial, list) else 0
        if verified_count or partial_count or "verified_variants" in payload or "partial_variants" in payload:
            return verified_count + partial_count, verified_count, partial_count

        variants = payload.get("variants")
        if isinstance(variants, list):
            return len(variants), 0, 0

        validated_variants = payload.get("validated_variants")
        if isinstance(validated_variants, list):
            return len(validated_variants), 0, 0

    if isinstance(payload, list):
        return len(payload), 0, 0

    return 0, 0, 0


def _variant_count_or_none(path: Path) -> int | None:
    payload = _load_json(path)
    if payload is None:
        return None
    total, _, _ = _variant_counts(payload)
    return total


def load_database_file_status(project_root: str | Path = ".") -> dict:
    """Return status for the source, stale root copy, and final clean database.

    The source canonical is treated as read-only.  The optional ``project_root``
    lets tests or callers evaluate a checked-out tree without changing global
    path constants.
    """
    root = Path(project_root)
    source_path = root / SOURCE_CANONICAL_PATH
    stale_root_path = root / STALE_ROOT_CANONICAL_PATH
    final_path = root / FINAL_CLEAN_DATABASE_PATH

    source_exists = source_path.exists()
    source_payload = _load_json(source_path) if source_exists else None
    source_variant_count, source_verified_count, source_partial_count = _variant_counts(source_payload)

    stale_root_exists = stale_root_path.exists()
    stale_root_variant_count = _variant_count_or_none(stale_root_path) if stale_root_exists else None
    stale_root_is_stale = (
        stale_root_exists
        and stale_root_variant_count is not None
        and source_exists
        and stale_root_variant_count < source_variant_count
    )

    final_exists = final_path.exists()
    final_variant_count = _variant_count_or_none(final_path) if final_exists else None
    final_is_older_than_source = (
        final_exists
        and source_exists
        and final_path.stat().st_mtime < source_path.stat().st_mtime
    )

    return {
        "source_path": SOURCE_CANONICAL_PATH,
        "source_exists": source_exists,
        "source_variant_count": source_variant_count,
        "source_verified_count": source_verified_count,
        "source_partial_count": source_partial_count,
        "stale_root_exists": stale_root_exists,
        "stale_root_variant_count": stale_root_variant_count,
        "stale_root_is_stale": stale_root_is_stale,
        "final_path": FINAL_CLEAN_DATABASE_PATH,
        "final_exists": final_exists,
        "final_variant_count": final_variant_count,
        "final_is_older_than_source": final_is_older_than_source,
    }
