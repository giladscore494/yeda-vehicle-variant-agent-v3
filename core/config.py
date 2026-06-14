"""Central configuration consumed by the ``engine`` package.

The ``engine`` layer (added alongside the scripts-based validation pipeline)
re-exports these names through ``engine/config.py``. Values come from the
environment so the engine layer stays consistent with ``scripts/config.py``.
The strong Gemini model id is pinned to the official ``gemini-3-pro-preview``
identifier (``3.1`` ids are not valid model names).
"""
from __future__ import annotations

import os

# Official Gemini model identifiers. The strong model is the engine default.
GEMINI_MODEL_STRONG: str = os.environ.get("GEMINI_MODEL_STRONG", "gemini-3-pro-preview")
GEMINI_MODEL_FAST: str = os.environ.get("GEMINI_MODEL_FAST", "gemini-2.5-flash")

GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")
GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO: str = os.environ.get("GITHUB_REPO", "")
GITHUB_BRANCH: str = os.environ.get("GITHUB_BRANCH", "")

CANONICAL_RESUME_PATH: str = os.environ.get("CANONICAL_RESUME_PATH", "data/canonical_resume.json")
CANONICAL_BACKUP_PATH: str = os.environ.get("CANONICAL_BACKUP_PATH", "data/canonical_backup.json")
RUNTIME_STATE_PATH: str = os.environ.get("RUNTIME_STATE_PATH", "data/runtime_state.json")


def gemini_configured() -> bool:
    return bool(GEMINI_API_KEY)


def github_configured() -> bool:
    return bool(GITHUB_TOKEN and GITHUB_REPO and GITHUB_BRANCH)


def config_summary() -> dict:
    return {
        "gemini_configured": gemini_configured(),
        "github_configured": github_configured(),
        "model_strong": GEMINI_MODEL_STRONG,
        "model_fast": GEMINI_MODEL_FAST,
    }
