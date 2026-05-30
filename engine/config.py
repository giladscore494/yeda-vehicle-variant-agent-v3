"""Centralized configuration loader for the validation engine.

Supports:
1. Streamlit st.secrets (when running in Streamlit)
2. Environment variables
3. Local secrets.py fallback (git-ignored)

Never hardcodes API keys. Never prints secrets.
"""
from __future__ import annotations

import os
from pathlib import Path


def _load_secrets_file() -> dict:
    """Import the local secrets.py (git-ignored) as a fallback."""
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


_file_secrets = _load_secrets_file()


def _try_streamlit(group: str, key: str):
    """Try to read from Streamlit secrets (nested dict style)."""
    try:
        import streamlit as st

        secrets = st.secrets
        if group in secrets:
            section = secrets[group]
            if hasattr(section, "get"):
                return section.get(key)
            if isinstance(section, dict):
                return section.get(key)
    except Exception:
        pass
    return None


# Mapping: (logical_group, logical_key) -> list of env var names to try
_ENV_ALIASES: dict[tuple[str, str], list[str]] = {
    # GitHub
    ("github", "token"): ["GITHUB_TOKEN"],
    ("github", "repo_owner"): ["GITHUB_REPO_OWNER"],
    ("github", "repo_name"): ["GITHUB_REPO_NAME"],
    ("github", "target_branch"): ["GITHUB_TARGET_BRANCH", "GITHUB_BRANCH"],
    ("github", "base_branch"): ["GITHUB_BASE_BRANCH"],
    ("github", "commit_author_name"): ["GITHUB_COMMIT_AUTHOR_NAME"],
    ("github", "commit_author_email"): ["GITHUB_COMMIT_AUTHOR_EMAIL"],
    # OpenAI
    ("openai", "api_key"): ["OPENAI_API_KEY"],
    ("openai", "validator_model_id"): ["OPENAI_VALIDATOR_MODEL_ID"],
    ("openai", "web_search_enabled"): ["OPENAI_WEB_SEARCH_ENABLED"],
    # Google
    ("google", "api_key"): ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
    ("google", "gemini_validator_model_id"): [
        "GEMINI_VALIDATOR_MODEL_ID",
        "GEMINI_MODEL_STRONG",
    ],
    ("google", "grounding_enabled"): ["GEMINI_GROUNDING_ENABLED"],
    # Validation
    ("validation", "mode"): ["VALIDATION_MODE"],
    ("validation", "output_dir"): ["VALIDATION_OUTPUT_DIR"],
    ("validation", "output_file"): ["VALIDATION_OUTPUT_FILE"],
    ("validation", "input_file"): ["VALIDATION_INPUT_FILE"],
    ("validation", "use_group_level_validation"): ["VALIDATION_USE_GROUP_LEVEL"],
    ("validation", "enable_repo_write"): ["VALIDATION_ENABLE_REPO_WRITE"],
    ("validation", "enable_dry_run"): ["VALIDATION_ENABLE_DRY_RUN"],
}

_DEFAULTS: dict[tuple[str, str], str] = {
    ("github", "repo_owner"): "giladscore494",
    ("github", "repo_name"): "yeda-vehicle-variant-agent-v3",
    ("github", "target_branch"): "validation-v2-budgeted-dual-il-trims",
    ("github", "base_branch"): "main",
    ("github", "commit_author_name"): "Validation Engine",
    ("github", "commit_author_email"): "validation@yeda.bot",
    ("google", "gemini_validator_model_id"): "gemini-3.1-pro-preview",
    ("google", "grounding_enabled"): "true",
    ("openai", "validator_model_id"): "gpt-5.4",
    ("openai", "web_search_enabled"): "true",
    ("validation", "mode"): "targeted-dual-validation",
    ("validation", "output_dir"): "data/validated_runs",
    ("validation", "output_file"): "resume_package_canonical_validated_v2.json",
    ("validation", "use_group_level_validation"): "true",
    ("validation", "enable_repo_write"): "false",
    ("validation", "enable_dry_run"): "false",
}


def get(group: str, key: str, default: str | None = None) -> str:
    """Retrieve a config value.

    Priority: Streamlit secrets → env vars → secrets.py → defaults → provided default.
    """
    # 1. Streamlit
    val = _try_streamlit(group, key)
    if val is not None:
        return str(val)

    # 2. Env vars (check all known aliases)
    aliases = _ENV_ALIASES.get((group, key), [])
    for alias in aliases:
        val = os.environ.get(alias)
        if val is not None:
            return val

    # 3. secrets.py (try UPPER_CASE versions of aliases)
    for alias in aliases:
        val = _file_secrets.get(alias)
        if val is not None:
            return str(val)

    # 4. Built-in defaults
    builtin = _DEFAULTS.get((group, key))
    if builtin is not None:
        return builtin

    # 5. Caller default
    return default or ""


def get_bool(group: str, key: str, default: bool = False) -> bool:
    """Retrieve a boolean config value."""
    val = get(group, key, str(default).lower())
    return val.lower() in ("true", "1", "yes")


def require(group: str, key: str) -> str:
    """Retrieve a required config value. Raises if missing."""
    val = get(group, key)
    if not val:
        raise RuntimeError(
            f"Missing required config: [{group}].{key}. "
            f"Set via Streamlit secrets, env var, or secrets.py."
        )
    return val


# ── Compatibility with existing core.config consumers ────────────────────

def github_configured() -> bool:
    return bool(get("github", "token"))


def gemini_configured() -> bool:
    return bool(get("google", "api_key"))


def openai_configured() -> bool:
    return bool(get("openai", "api_key"))


def config_summary() -> dict:
    """Return a safe summary (no secret values)."""
    return {
        "gemini_key": "configured" if gemini_configured() else "missing",
        "openai_key": "configured" if openai_configured() else "missing",
        "github_token": "configured" if github_configured() else "missing",
        "github_repo": f"{get('github', 'repo_owner')}/{get('github', 'repo_name')}",
        "target_branch": get("github", "target_branch"),
        "validation_mode": get("validation", "mode"),
        "gemini_model": get("google", "gemini_validator_model_id"),
        "openai_model": get("openai", "validator_model_id"),
        "output_dir": get("validation", "output_dir"),
    }
