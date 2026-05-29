"""Configuration loader.

Reads settings from environment variables first, falls back to a local
``secrets.py`` file (git-ignored) if present.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _load_secrets_file() -> dict:
    """Try to import the local secrets.py (git-ignored) as a fallback."""
    secrets_path = Path(__file__).resolve().parent.parent / "secrets.py"
    if not secrets_path.exists():
        return {}
    import importlib.util
    spec = importlib.util.spec_from_file_location("_secrets", str(secrets_path))
    if spec is None or spec.loader is None:
        return {}
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    result = {}
    for key in dir(mod):
        if key.isupper():
            result[key] = getattr(mod, key)
    return result


_secrets = _load_secrets_file()


def _get(key: str, default: str = "") -> str:
    return os.environ.get(key, _secrets.get(key, default))


GEMINI_API_KEY: str = _get("GEMINI_API_KEY")
GEMINI_MODEL_FAST: str = _get("GEMINI_MODEL_FAST", "gemini-3-pro-preview")
GEMINI_MODEL_STRONG: str = _get("GEMINI_MODEL_STRONG", "gemini-3-pro-preview")

GITHUB_TOKEN: str = _get("GITHUB_TOKEN")
GITHUB_REPO: str = _get("GITHUB_REPO", "giladscore494/yeda-vehicle-variant-agent-v3")
GITHUB_BRANCH: str = _get("GITHUB_BRANCH", "main")

CANONICAL_RESUME_PATH: str = _get(
    "CANONICAL_RESUME_PATH", "data/canonical/resume_package_canonical.json"
)
CANONICAL_BACKUP_PATH: str = _get(
    "CANONICAL_BACKUP_PATH", "data/canonical/resume_package_backup_previous.json"
)
RUNTIME_STATE_PATH: str = _get(
    "RUNTIME_STATE_PATH", "data/runtime/current_run.json"
)


def gemini_configured() -> bool:
    return bool(GEMINI_API_KEY)


def github_configured() -> bool:
    return bool(GITHUB_TOKEN)


def config_summary() -> dict:
    """Return a safe summary (no secret values)."""
    return {
        "gemini_key": "configured" if gemini_configured() else "missing",
        "github_token": "configured" if github_configured() else "missing",
        "github_repo": GITHUB_REPO,
        "github_branch": GITHUB_BRANCH,
        "canonical_path": CANONICAL_RESUME_PATH,
        "backup_path": CANONICAL_BACKUP_PATH,
        "runtime_state_path": RUNTIME_STATE_PATH,
    }
