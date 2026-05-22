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
