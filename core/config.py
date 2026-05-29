"""Configuration loader.

Reads settings from:
1. Flat environment variables (e.g. GEMINI_API_KEY)
2. Sectioned Streamlit secrets (e.g. st.secrets["google"]["api_key"])
3. Local ``secrets.py`` file (git-ignored)

Supports BOTH flat and sectioned Streamlit secrets formats.
All string values are stripped of leading/trailing whitespace.
"""
from __future__ import annotations

import os
import warnings
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


def _try_streamlit_flat(key: str) -> str | None:
    """Try to read a flat key from Streamlit secrets (top-level)."""
    try:
        import streamlit as st
        val = st.secrets.get(key)
        if val is not None:
            return str(val).strip()
    except Exception:
        pass
    return None


def _try_streamlit_sectioned(group: str, key: str) -> str | None:
    """Try to read a sectioned key from Streamlit secrets."""
    try:
        import streamlit as st
        secrets = st.secrets
        if group in secrets:
            section = secrets[group]
            val = None
            if hasattr(section, "get"):
                val = section.get(key)
            elif isinstance(section, dict):
                val = section.get(key)
            if val is not None:
                return str(val).strip()
    except Exception:
        pass
    return None


def _get(key: str, default: str = "", sectioned_fallbacks: list[tuple[str, str]] | None = None) -> str:
    """Get a config value with fallback chain:
    1. Environment variable
    2. Flat Streamlit secret (top-level key)
    3. Sectioned Streamlit secrets (group.key)
    4. Local secrets.py
    5. Default
    """
    # 1. Environment variable
    val = os.environ.get(key)
    if val is not None:
        return val.strip()

    # 2. Flat Streamlit secret
    val = _try_streamlit_flat(key)
    if val is not None:
        return val

    # 3. Sectioned Streamlit secrets fallbacks
    if sectioned_fallbacks:
        for group, skey in sectioned_fallbacks:
            val = _try_streamlit_sectioned(group, skey)
            if val is not None:
                return val

    # 4. Local secrets.py
    val = _secrets.get(key)
    if val is not None:
        return str(val).strip()

    return default.strip()


def _resolve_github_branch() -> str:
    """Resolve GITHUB_BRANCH with special priority:
    1. Flat GITHUB_BRANCH env/secret
    2. validation.target_branch (sectioned Streamlit)
    3. github.target_branch (sectioned Streamlit)
    4. Default "main"
    """
    # 1. Flat env var
    val = os.environ.get("GITHUB_BRANCH")
    if val and val.strip():
        return val.strip()

    # 1b. Flat Streamlit secret
    val = _try_streamlit_flat("GITHUB_BRANCH")
    if val:
        return val

    # 1c. Local secrets.py
    val = _secrets.get("GITHUB_BRANCH")
    if val and str(val).strip():
        return str(val).strip()

    # 2. validation.target_branch
    val = _try_streamlit_sectioned("validation", "target_branch")
    if val:
        return val

    # 3. github.target_branch
    val = _try_streamlit_sectioned("github", "target_branch")
    if val:
        return val

    return "main"


# ── Resolved config values ──────────────────────────────────────────────

GEMINI_API_KEY: str = _get("GEMINI_API_KEY", sectioned_fallbacks=[("google", "api_key")])
GEMINI_MODEL_FAST: str = _get("GEMINI_MODEL_FAST", "gemini-3.1-pro-preview",
                              sectioned_fallbacks=[("google", "gemini_validator_model_id")])
GEMINI_MODEL_STRONG: str = _get("GEMINI_MODEL_STRONG", "gemini-3.1-pro-preview",
                                sectioned_fallbacks=[("google", "gemini_validator_model_id")])

GITHUB_TOKEN: str = _get("GITHUB_TOKEN", sectioned_fallbacks=[("github", "token")])
GITHUB_REPO: str = _get("GITHUB_REPO", "giladscore494/yeda-vehicle-variant-agent-v3",
                         sectioned_fallbacks=[("github", "repo_full_name")])
GITHUB_BRANCH: str = _resolve_github_branch()

CANONICAL_RESUME_PATH: str = _get(
    "CANONICAL_RESUME_PATH", "data/canonical/resume_package_canonical.json"
)
CANONICAL_BACKUP_PATH: str = _get(
    "CANONICAL_BACKUP_PATH", "data/canonical/resume_package_backup_previous.json"
)
RUNTIME_STATE_PATH: str = _get(
    "RUNTIME_STATE_PATH", "data/runtime/current_run.json"
)

# ── Branch safety warning ───────────────────────────────────────────────

_BRANCH_WARNING: str | None = None

if GITHUB_BRANCH == "main":
    # Check if validation.target_branch or github.target_branch exists
    _val_branch = _try_streamlit_sectioned("validation", "target_branch")
    _gh_branch = _try_streamlit_sectioned("github", "target_branch")
    if _val_branch or _gh_branch:
        _configured = _val_branch or _gh_branch
        _BRANCH_WARNING = (
            f"⚠️ Branch resolved to 'main' but a target branch "
            f"'{_configured}' is configured. Check your secrets."
        )
        warnings.warn(_BRANCH_WARNING, stacklevel=1)


def get_branch_warning() -> str | None:
    """Return a branch warning message if branch resolved to main while
    a target branch was configured in sectioned secrets."""
    return _BRANCH_WARNING


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
        "branch_warning": get_branch_warning(),
    }
