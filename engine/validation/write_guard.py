"""Write guard — blocks any write to the source canonical file in validation mode.

Allowed writes:
  - data/validation/*
  - data/validated_runs/* (legacy compatibility)
  - data/runtime/current_validation_run.json

Reserved until Task 5 export:
  - data/final/resume_package_final_clean.json
"""
from __future__ import annotations

from pathlib import Path

from core.paths import SOURCE_CANONICAL_PATH, VALIDATION_DIR

_CANONICAL_PATH = Path(SOURCE_CANONICAL_PATH).resolve()
_FINAL_CLEAN_DATABASE_PATH = Path("data/final/resume_package_final_clean.json").resolve()
_VALIDATION_DIR = Path(VALIDATION_DIR).resolve()
_VALIDATED_RUNS_DIR = Path("data/validated_runs").resolve()
_RUNTIME_STATE_PATH = Path("data/runtime/current_validation_run.json").resolve()

# Paths that are allowed for validation writes.
_ALLOWED_PREFIXES = [
    _VALIDATION_DIR,
    _VALIDATED_RUNS_DIR,
    _RUNTIME_STATE_PATH,
]
_ALLOWED_DIRS = {
    _VALIDATION_DIR,
    _VALIDATED_RUNS_DIR,
}


class CanonicalWriteBlockedError(Exception):
    """Raised when a code path attempts to write to the canonical file."""
    pass


def check_write_allowed(target_path: str | Path) -> None:
    """Raise CanonicalWriteBlockedError if target_path resolves to the canonical file.

    Call this before any file write in validation mode.  The source canonical
    and final clean database are deliberately protected; validation outputs
    must go to data/validation/, legacy data/validated_runs/, or validation
    runtime state.
    """
    resolved = Path(target_path).resolve()

    if resolved == _CANONICAL_PATH:
        raise CanonicalWriteBlockedError(
            f"canonical_write_blocked: Attempted to write to protected canonical "
            f"file at {resolved}. Validation mode does not permit canonical mutations."
        )

    if resolved == _FINAL_CLEAN_DATABASE_PATH:
        raise CanonicalWriteBlockedError(
            f"final_clean_database_write_blocked: Attempted to write to reserved "
            f"final clean database at {resolved}. Only the Task 5 final export "
            f"function may write this file."
        )


def is_allowed_validation_write(target_path: str | Path) -> bool:
    """Return True if the target path is an allowed validation output location."""
    resolved = Path(target_path).resolve()

    if resolved in (_CANONICAL_PATH, _FINAL_CLEAN_DATABASE_PATH):
        return False

    for allowed in _ALLOWED_PREFIXES:
        if allowed in _ALLOWED_DIRS:
            try:
                resolved.relative_to(allowed)
                return True
            except ValueError:
                pass
        elif resolved == allowed:
            return True

    return False


def safe_write_json(data: dict | list, target_path: str | Path, **json_kwargs) -> None:
    """Write JSON data to a path, blocking canonical writes."""
    import json

    check_write_allowed(target_path)

    p = Path(target_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    json_kwargs.setdefault("ensure_ascii", False)
    json_kwargs.setdefault("indent", 2)

    p.write_text(json.dumps(data, **json_kwargs), encoding="utf-8")
