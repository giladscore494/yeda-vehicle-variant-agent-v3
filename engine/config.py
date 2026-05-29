"""Engine-level config — re-exports core settings for use within the engine package."""
from __future__ import annotations

from core.config import (  # noqa: F401  (re-export)
    GEMINI_API_KEY,
    GEMINI_MODEL_FAST,
    GEMINI_MODEL_STRONG,
    GITHUB_TOKEN,
    GITHUB_REPO,
    GITHUB_BRANCH,
    CANONICAL_RESUME_PATH,
    CANONICAL_BACKUP_PATH,
    RUNTIME_STATE_PATH,
    gemini_configured,
    github_configured,
    config_summary,
)

# Default model used by engine-layer callers.
# Override via GEMINI_MODEL_STRONG env-var or secrets.py.
ENGINE_MODEL: str = GEMINI_MODEL_STRONG
