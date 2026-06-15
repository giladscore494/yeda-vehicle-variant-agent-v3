"""Shared configuration loading for the Streamlit vehicle catalog app.

Only the current Streamlit secrets shape is supported: ``[github]``,
``[openai]``, and ``[google]``. Legacy validation settings and environment
variable aliases are intentionally ignored.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

DEFAULT_OPENAI_VALIDATOR_MODEL_ID = "gpt-5.4"
DEFAULT_GEMINI_VALIDATOR_MODEL_ID = "gemini-3.1-pro-preview"


@dataclass(frozen=True)
class SharedConfig:
    github_token: str = ""
    github_repo_full_name: str = ""
    github_target_branch: str = ""
    openai_api_key: str = ""
    openai_validator_model_id: str = DEFAULT_OPENAI_VALIDATOR_MODEL_ID
    openai_web_search_enabled: bool = True
    google_api_key: str = ""
    gemini_validator_model_id: str = DEFAULT_GEMINI_VALIDATOR_MODEL_ID
    gemini_grounding_enabled: bool = True
    strict_github_checkpoint: bool = False


def _read_secrets(path: str = ".streamlit/secrets.toml") -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {}
    with p.open("rb") as fh:
        return tomllib.load(fh)


def _bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip().lower() not in {"false", "0", "no", "off"}
    return bool(value)


def load_shared_config(secrets_path: str = ".streamlit/secrets.toml") -> SharedConfig:
    secrets = _read_secrets(secrets_path)
    github = secrets.get("github") or {}
    openai = secrets.get("openai") or {}
    google = secrets.get("google") or {}
    return SharedConfig(
        github_token=github.get("token", "") or "",
        github_repo_full_name=github.get("repo_full_name", "") or "",
        github_target_branch=github.get("target_branch", "") or "",
        openai_api_key=openai.get("api_key", "") or "",
        openai_validator_model_id=openai.get("validator_model_id", DEFAULT_OPENAI_VALIDATOR_MODEL_ID) or DEFAULT_OPENAI_VALIDATOR_MODEL_ID,
        openai_web_search_enabled=_bool(openai.get("web_search_enabled"), True),
        google_api_key=google.get("api_key", "") or "",
        gemini_validator_model_id=google.get("gemini_validator_model_id", DEFAULT_GEMINI_VALIDATOR_MODEL_ID) or DEFAULT_GEMINI_VALIDATOR_MODEL_ID,
        gemini_grounding_enabled=_bool(google.get("grounding_enabled"), True),
    )
