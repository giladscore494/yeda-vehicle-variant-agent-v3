"""Canonical state helpers — load, parse batch_state, get all variants."""
from __future__ import annotations

import json
from pathlib import Path


def load_canonical(path: str | Path) -> dict:
    """Load canonical JSON from disk. Raises on missing/invalid."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Canonical file not found: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Canonical root is not a JSON object")
    return data


def get_all_variants(canonical: dict) -> list[dict]:
    """Return the combined list of all variants (verified + partial)."""
    verified = canonical.get("verified_variants") or []
    partial = canonical.get("partial_variants") or []
    return verified + partial


def get_batch_state(canonical: dict) -> dict:
    """Return batch_state dict, creating if missing."""
    if "batch_state" not in canonical:
        canonical["batch_state"] = {}
    return canonical["batch_state"]


def ensure_batch_state_fields(canonical: dict) -> dict:
    """Ensure all required batch_state fields exist."""
    bs = get_batch_state(canonical)
    bs.setdefault("processed_seed_ids", [])
    bs.setdefault("manual_review_seed_ids", [])
    bs.setdefault("failed_seed_ids", [])
    bs.setdefault("next_seed_id", None)
    bs.setdefault("last_completed_seed_id", None)
    bs.setdefault("seed_accounting", {})
    return canonical


def load_seeds(path: str | Path) -> list[dict]:
    """Load seed catalog from disk."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Seed catalog not found: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Seed catalog root is not a JSON array")
    return data


def seed_id_from_seed(seed: dict) -> str:
    """Generate a seed_id string from a seed dict."""
    make = (seed.get("make") or "").strip().lower().replace(" ", "_")
    model = (seed.get("model") or "").strip().lower().replace(" ", "_")
    ys = seed.get("year_start", "")
    ye = seed.get("year_end", "")
    market = (seed.get("market") or "il").strip().lower()
    return f"{make}__{model}__{ys}__{ye}__{market}"


def find_seed_by_id(seeds: list[dict], seed_id: str) -> dict | None:
    """Find a seed dict by its generated seed_id."""
    for s in seeds:
        if seed_id_from_seed(s) == seed_id:
            return s
    return None


def repair_cursor(canonical: dict, seeds: list[dict]) -> dict:
    """Repair cursor (next_seed_id / last_completed_seed_id) without
    modifying variants, processed_seed_ids, manual_review, or failed buckets.

    Algorithm:
      1. Walk the seed catalog in exact order.
      2. A seed is "handled" if it appears in processed ∪ manual_review ∪ failed.
      3. The contiguous handled prefix ends at the first unhandled seed.
      4. last_completed_seed_id = last handled seed in that prefix (None if
         prefix is empty).
      5. next_seed_id = first unhandled seed after the prefix (None if all
         seeds are handled).

    Returns dict with old/new cursor values for reporting.
    """
    bs = get_batch_state(canonical)
    processed = set(bs.get("processed_seed_ids") or [])
    manual = set(bs.get("manual_review_seed_ids") or [])
    failed = set(bs.get("failed_seed_ids") or [])
    handled = processed | manual | failed

    catalog_ids = [seed_id_from_seed(s) for s in seeds]

    old_next = bs.get("next_seed_id")
    old_last = bs.get("last_completed_seed_id")

    # Walk catalog to find end of contiguous handled prefix
    last_handled_id: str | None = None
    first_unhandled_id: str | None = None

    for sid in catalog_ids:
        if sid in handled:
            last_handled_id = sid
        else:
            first_unhandled_id = sid
            break

    # If no gap was found, all catalog seeds are handled
    if first_unhandled_id is None:
        # Check if there are any seeds at all
        if catalog_ids:
            last_handled_id = catalog_ids[-1]

    # Only update cursor fields — never touch variants or buckets
    bs["last_completed_seed_id"] = last_handled_id
    bs["next_seed_id"] = first_unhandled_id

    return {
        "old_next_seed_id": old_next,
        "old_last_completed_seed_id": old_last,
        "new_next_seed_id": first_unhandled_id,
        "new_last_completed_seed_id": last_handled_id,
    }
