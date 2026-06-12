"""Runtime configuration resolver for the validation engine.

Resolution order for every setting:
  1. Streamlit secrets (when running under Streamlit and secrets exist)
  2. Environment variables
  3. Safe defaults

Supports both secret layouts:

    [google]                                  [google]
    api_key = "..."                           api_key = "..."
    gemini_validator_model_id = "..."         gemini_validator_model_id = "..."
    grounding_enabled = true                  grounding_enabled = true
    token = "..."                # GitHub
    repo_full_name = "..."                    [github]
    target_branch = "..."                     token = "..."
    base_branch = "..."                       repo_full_name = "..."
                                              target_branch = "..."
                                              base_branch = "..."

Security: secret VALUES are never printed, logged, or written to output files.
Only presence booleans are exposed for display.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

DEFAULT_MODEL_ID = "gemini-3.1-pro-preview"
DEFAULT_OPENAI_MODEL_ID = "gpt-5.4"
DEFAULT_ADJUDICATION_SCOPE = "all_non_trivial"
DEFAULT_REPO_FULL_NAME = "giladscore494/yeda-vehicle-variant-agent-v3"
DEFAULT_TARGET_BRANCH = "validation-v2-budgeted-dual-il-trims"
DEFAULT_BASE_BRANCH = "main"


@dataclass
class RuntimeConfig:
    gemini_api_key: str = ""
    model_id: str = DEFAULT_MODEL_ID
    grounding_enabled: bool = True
    openai_api_key: str = ""
    openai_model_id: str = DEFAULT_OPENAI_MODEL_ID
    openai_web_search_enabled: bool = True
    adjudication_scope: str = DEFAULT_ADJUDICATION_SCOPE
    github_token: str = ""
    repo_full_name: str = DEFAULT_REPO_FULL_NAME
    target_branch: str = DEFAULT_TARGET_BRANCH
    base_branch: str = DEFAULT_BASE_BRANCH
    runtime: str = "cli"
    secrets_source: str = "env"

    @property
    def gemini_key_present(self) -> bool:
        return bool(self.gemini_api_key.strip())

    @property
    def openai_key_present(self) -> bool:
        return bool(self.openai_api_key.strip())

    @property
    def github_token_present(self) -> bool:
        return bool(self.github_token.strip())

    def presence_report(self) -> dict:
        """Safe-to-display status. Never includes secret values."""
        return {
            "runtime": self.runtime,
            "secrets_source": self.secrets_source,
            "gemini_api_key": "present" if self.gemini_key_present else "MISSING",
            "openai_api_key": "present" if self.openai_key_present else "MISSING",
            "github_token": "present" if self.github_token_present else "MISSING",
            "model_id": self.model_id,
            "openai_model_id": self.openai_model_id,
            "adjudication_scope": self.adjudication_scope,
            "grounding_enabled": self.grounding_enabled,
            "repo_full_name": self.repo_full_name,
            "target_branch": self.target_branch,
            "base_branch": self.base_branch,
        }


def _load_streamlit_secrets() -> dict | None:
    """Return st.secrets as a plain dict, or None when unavailable.

    Must never raise: local dev without .streamlit/secrets.toml is normal.
    """
    try:
        import streamlit as st
        # Accessing st.secrets raises when no secrets file exists.
        keys = list(st.secrets.keys())
        return {k: st.secrets[k] for k in keys}
    except Exception:
        return None


def _as_bool(value, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes", "on")
    if value is None:
        return default
    return bool(value)


def _section(secrets: dict, name: str) -> dict:
    sec = secrets.get(name)
    if sec is None:
        return {}
    try:
        return dict(sec)
    except (TypeError, ValueError):
        return {}


def resolve(runtime: str = "cli") -> RuntimeConfig:
    """Build the runtime configuration. Safe to call anywhere."""
    secrets = _load_streamlit_secrets()
    google = _section(secrets, "google") if secrets else {}
    github = _section(secrets, "github") if secrets else {}
    openai_sec = _section(secrets, "openai") if secrets else {}
    validation_sec = _section(secrets, "validation") if secrets else {}

    def pick(*candidates, default=""):
        for c in candidates:
            if c is not None and str(c).strip():
                return str(c).strip()
        return default

    grounding_raw = google.get("grounding_enabled")
    if grounding_raw is None:
        grounding_raw = os.environ.get("GROUNDING_ENABLED")

    cfg = RuntimeConfig(
        gemini_api_key=pick(
            google.get("api_key"),
            os.environ.get("GEMINI_API_KEY"),
        ),
        model_id=pick(
            google.get("gemini_validator_model_id"),
            os.environ.get("GEMINI_VALIDATOR_MODEL_ID"),
            default=DEFAULT_MODEL_ID,
        ),
        grounding_enabled=_as_bool(grounding_raw, True),
        openai_api_key=pick(
            openai_sec.get("api_key"),
            os.environ.get("OPENAI_API_KEY"),
        ),
        openai_model_id=pick(
            openai_sec.get("validator_model_id"),
            os.environ.get("OPENAI_VALIDATOR_MODEL_ID"),
            default=DEFAULT_OPENAI_MODEL_ID,
        ),
        openai_web_search_enabled=_as_bool(
            openai_sec.get("web_search_enabled")
            or os.environ.get("OPENAI_WEB_SEARCH_ENABLED"),
            True,
        ),
        adjudication_scope=pick(
            validation_sec.get("openai_adjudication_scope"),
            os.environ.get("OPENAI_ADJUDICATION_SCOPE"),
            default=DEFAULT_ADJUDICATION_SCOPE,
        ),
        github_token=pick(
            github.get("token"),
            google.get("token"),
            os.environ.get("GH_PUSH_TOKEN"),
        ),
        repo_full_name=pick(
            github.get("repo_full_name"),
            google.get("repo_full_name"),
            os.environ.get("GITHUB_REPO_FULL_NAME"),
            default=DEFAULT_REPO_FULL_NAME,
        ),
        target_branch=pick(
            github.get("target_branch"),
            google.get("target_branch"),
            os.environ.get("TARGET_BRANCH"),
            default=DEFAULT_TARGET_BRANCH,
        ),
        base_branch=pick(
            github.get("base_branch"),
            google.get("base_branch"),
            os.environ.get("BASE_BRANCH"),
            default=DEFAULT_BASE_BRANCH,
        ),
        runtime=runtime,
        secrets_source="streamlit_secrets" if secrets else "env",
    )
    return cfg
