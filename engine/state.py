"""Canonical state helpers — load, parse batch_state, get all variants."""
from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path


class CanonicalCorruptionError(Exception):
    """Raised when a canonical JSON file exists but contains invalid JSON."""

    def __init__(self, path: Path, size: int, line: int, column: int,
                 pos: int, message: str | None = None):
        self.path = path
        self.size = size
        self.line = line
        self.column = column
        self.pos = pos
        msg = (
            message
            or (
                f"Canonical JSON is corrupted at {path} "
                f"(size={size}, line={line}, col={column}, pos={pos}). "
                "Restore from backup before running."
            )
        )
        super().__init__(msg)


def load_canonical(path: str | Path) -> dict:
    """Load canonical JSON from disk.

    Raises FileNotFoundError when the file is missing.
    Raises CanonicalCorruptionError when the file contains invalid JSON.
    Raises ValueError when the root element is not a dict.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Canonical file not found: {p}")
    text = p.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise CanonicalCorruptionError(
            path=p,
            size=len(text),
            line=exc.lineno,
            column=exc.colno,
            pos=exc.pos,
        ) from exc
    if not isinstance(data, dict):
        raise ValueError("Canonical root is not a JSON object")
    return data


def load_canonical_with_recovery(
    path: str | Path,
    backup_path: str | Path | None = None,
) -> dict:
    """Load canonical, falling back to backup on corruption.

    Returns the canonical dict.  When recovery from backup occurs the dict
    includes a ``_recovery`` key with metadata about the restore.

    Raises CanonicalCorruptionError when neither the primary nor the backup
    file contains valid JSON.
    """
    p = Path(path)
    try:
        return load_canonical(p)
    except CanonicalCorruptionError:
        if backup_path is None:
            raise
        bp = Path(backup_path)
        if not bp.exists():
            raise

        # Validate backup
        try:
            backup_data = load_canonical(bp)
        except (CanonicalCorruptionError, ValueError, FileNotFoundError):
            raise CanonicalCorruptionError(
                path=p,
                size=p.stat().st_size if p.exists() else 0,
                line=0,
                column=0,
                pos=0,
                message=(
                    f"Canonical JSON is corrupted at {p} and backup at {bp} "
                    "is also invalid. Manual intervention required."
                ),
            )

        # Restore backup to canonical path using atomic replace
        fd, tmp_path = tempfile.mkstemp(
            prefix=".canonical_restore_", suffix=".json", dir=str(p.parent),
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(backup_data, fh, ensure_ascii=False, indent=2)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp_path, str(p))
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

        # Fsync parent directory
        try:
            dir_fd = os.open(str(p.parent), os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError:
            pass

        # Reload restored canonical
        restored = load_canonical(p)
        restored["_recovery"] = {
            "restored_from": str(bp),
            "original_path": str(p),
        }
        return restored


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

    # Fallback: if no contiguous prefix from start but handled seeds exist,
    # find the last handled seed in catalog order.  This covers the case
    # where the first seed(s) in the catalog are unhandled but later seeds
    # have been processed (out-of-order processing).
    if last_handled_id is None and handled:
        for sid in reversed(catalog_ids):
            if sid in handled:
                last_handled_id = sid
                break

    # Only update cursor fields — never touch variants or buckets
    bs["last_completed_seed_id"] = last_handled_id
    bs["next_seed_id"] = first_unhandled_id

    return {
        "old_next_seed_id": old_next,
        "old_last_completed_seed_id": old_last,
        "new_next_seed_id": first_unhandled_id,
        "new_last_completed_seed_id": last_handled_id,
    }
