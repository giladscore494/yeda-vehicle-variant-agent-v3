"""Write guard — blocks any write to the canonical file in validation mode.

Allowed writes:
  - data/validated_runs/*
  - data/runtime/current_validation_run.json
"""
from __future__ import annotations

import os
from pathlib import Path

_CANONICAL_PATH = Path("data/canonical/resume_package_canonical.json").resolve()

# Paths that are allowed for validation writes
_ALLOWED_PREFIXES = [
    Path("data/validated_runs").resolve(),
    Path("data/runtime/current_validation_run.json").resolve(),
]


class CanonicalWriteBlockedError(Exception):
    """Raised when a code path attempts to write to the canonical file."""
    pass


def check_write_allowed(target_path: str | Path) -> None:
    """Raise CanonicalWriteBlockedError if target_path resolves to the canonical file.

    Call this before any file write in validation mode.
    """
    resolved = Path(target_path).resolve()

    if resolved == _CANONICAL_PATH:
        raise CanonicalWriteBlockedError(
            f"canonical_write_blocked: Attempted to write to protected canonical "
            f"file at {resolved}. Validation mode does not permit canonical mutations."
        )


def is_allowed_validation_write(target_path: str | Path) -> bool:
    """Return True if the target path is an allowed validation output location."""
    resolved = Path(target_path).resolve()

    if resolved == _CANONICAL_PATH:
        return False

    for allowed in _ALLOWED_PREFIXES:
        if allowed.is_dir():
            try:
                resolved.relative_to(allowed)
                return True
            except ValueError:
                pass
        elif resolved == allowed:
            return True

    # Also allow anything under data/validated_runs
    validated_runs = Path("data/validated_runs").resolve()
    try:
        resolved.relative_to(validated_runs)
        return True
    except ValueError:
        pass

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
