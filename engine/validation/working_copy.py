"""Active working-copy helpers for validation workflows."""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.paths import (
    ACTIVE_WORKING_DATABASE_PATH,
    SOURCE_CANONICAL_PATH,
    WORKING_BACKUPS_DIR,
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _variant_count(payload: Any) -> int:
    if not isinstance(payload, dict):
        return 0
    verified = payload.get("verified_variants")
    partial = payload.get("partial_variants")
    if isinstance(verified, list) or isinstance(partial, list):
        return (len(verified) if isinstance(verified, list) else 0) + (
            len(partial) if isinstance(partial, list) else 0
        )
    vehicles = payload.get("vehicles")
    if isinstance(vehicles, list):
        return len(vehicles)
    return 0


def _status(status: str, canonical_path: Path, working_path: Path, created_at: str) -> dict:
    canonical_payload = _read_json(canonical_path)
    working_payload = _read_json(working_path) if working_path.exists() else {}
    return {
        "ok": True,
        "status": status,
        "canonical_path": str(canonical_path),
        "working_path": str(working_path),
        "canonical_variant_count": _variant_count(canonical_payload),
        "working_variant_count": _variant_count(working_payload),
        "canonical_hash": _sha256(canonical_path),
        "working_hash": _sha256(working_path) if working_path.exists() else "",
        "created_at": created_at,
    }


def initialize_working_copy(force: bool = False) -> dict:
    """Create the active working copy from canonical, unless it already exists."""
    canonical_path = Path(SOURCE_CANONICAL_PATH)
    working_path = Path(ACTIVE_WORKING_DATABASE_PATH)
    created_at = _utc_now()

    if not canonical_path.exists():
        return {
            "ok": False,
            "status": "missing_canonical",
            "canonical_path": str(canonical_path),
            "working_path": str(working_path),
            "created_at": created_at,
        }

    if working_path.exists() and not force:
        return _status("already_exists", canonical_path, working_path, created_at)

    working_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(canonical_path, working_path)
    return _status("reset" if force else "created", canonical_path, working_path, created_at)


def get_active_database_path() -> str:
    """Return the working copy when present; otherwise fall back to canonical."""
    if Path(ACTIVE_WORKING_DATABASE_PATH).exists():
        return ACTIVE_WORKING_DATABASE_PATH
    return SOURCE_CANONICAL_PATH


def load_active_database() -> dict:
    """Load the current active validation database."""
    payload = _read_json(get_active_database_path())
    if not isinstance(payload, dict):
        raise ValueError("Active database root must be a JSON object.")
    return payload


def reset_working_copy_from_canonical(confirm: bool = False) -> dict:
    """Back up the working copy, then reset it from canonical when confirmed."""
    canonical_path = Path(SOURCE_CANONICAL_PATH)
    working_path = Path(ACTIVE_WORKING_DATABASE_PATH)
    created_at = _utc_now()

    if confirm is not True:
        return {
            "ok": False,
            "status": "blocked",
            "message": "Reset requires explicit confirm=True.",
            "canonical_path": str(canonical_path),
            "working_path": str(working_path),
            "created_at": created_at,
        }

    backup_path = None
    if working_path.exists():
        backups_dir = Path(WORKING_BACKUPS_DIR)
        backups_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup_path = backups_dir / f"resume_package_working_backup_{stamp}.json"
        shutil.copyfile(working_path, backup_path)

    result = initialize_working_copy(force=True)
    result["status"] = "reset"
    result["backup_path"] = str(backup_path) if backup_path else None
    return result
