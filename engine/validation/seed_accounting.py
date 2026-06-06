"""Seed accounting — compares seed catalog with batch state.

Computes exact overlaps, mismatches, and logical ID alias warnings.
"""
from __future__ import annotations

from engine.state import seed_id_from_seed


# ── Logical alias patterns that cause silent mismatches ─────────────────

_ALIAS_PATTERNS = [
    ("/", "-"),
    ("&", "and"),
    ("+", "plus"),
    ("_&_", "_and_"),
]


def detect_alias_warnings(
    processed_not_in_catalog: set[str],
    catalog_not_processed: set[str],
) -> list[dict]:
    """Detect common logical ID alias mismatches between sets."""
    warnings: list[dict] = []
    for pid in sorted(processed_not_in_catalog):
        for cid in sorted(catalog_not_processed):
            for old, new in _ALIAS_PATTERNS:
                if pid.replace(old, new) == cid or cid.replace(old, new) == pid:
                    warnings.append({
                        "processed_id": pid,
                        "catalog_id": cid,
                        "pattern": f"'{old}' vs '{new}'",
                        "warning": (
                            f"Possible alias mismatch: '{pid}' ↔ '{cid}' "
                            f"(pattern: '{old}' vs '{new}')"
                        ),
                    })
    return warnings


def compute_seed_accounting(canonical: dict, seeds: list[dict]) -> dict:
    """Compute full seed accounting between catalog and batch state."""
    bs = canonical.get("batch_state") or {}
    catalog_ids = {seed_id_from_seed(s) for s in seeds}

    processed = set(bs.get("processed_seed_ids") or [])
    failed = set(bs.get("failed_seed_ids") or [])
    manual_review = set(bs.get("manual_review_seed_ids") or [])
    needs_retry = set(bs.get("needs_retry_seed_ids") or [])

    all_bucket_ids = processed | failed | manual_review | needs_retry

    processed_in_catalog = processed & catalog_ids
    processed_not_in_catalog = processed - catalog_ids
    catalog_not_processed = catalog_ids - all_bucket_ids

    alias_warnings = detect_alias_warnings(processed_not_in_catalog, catalog_not_processed)

    return {
        "seed_catalog_count": len(catalog_ids),
        "processed_exact_count": len(processed),
        "processed_in_catalog_count": len(processed_in_catalog),
        "processed_not_in_catalog": sorted(processed_not_in_catalog),
        "catalog_not_processed": sorted(catalog_not_processed),
        "failed_seed_ids": sorted(failed),
        "manual_review_seed_ids": sorted(manual_review),
        "needs_retry_seed_ids": sorted(needs_retry),
        "next_seed_id": bs.get("next_seed_id"),
        "last_completed_seed_id": bs.get("last_completed_seed_id"),
        "logical_seed_id_alias_warnings": alias_warnings,
    }
