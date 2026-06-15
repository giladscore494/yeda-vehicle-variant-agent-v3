"""Shared configuration loading for CLI and Streamlit.

Environment variables win. When absent, CLI code may read the existing
.streamlit/secrets.toml shape. No additional secret names are introduced.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from .gemini_client import DEFAULT_MODEL_ID

DEFAULT_OPENAI_VALIDATOR_MODEL_ID = "gpt-5.4"

@dataclass(frozen=True)
class SharedConfig:
    github_token: str = ""
    google_api_key: str = ""
    gemini_validator_model_id: str = DEFAULT_MODEL_ID
    openai_api_key: str = ""
    openai_validator_model_id: str = DEFAULT_OPENAI_VALIDATOR_MODEL_ID
    grounding_enabled: bool = True
    force_per_variant_validation: bool = True
    # New single-GPT-5.4 model technical-catalog mode. When true the new
    # catalog pipeline is active and Gemini / legacy guard / repair adjudicator
    # / per-row validation are all disabled.
    single_gpt54_model_catalog_mode: bool = True


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
        return value.strip().lower() not in {"false", "0", "no"}
    return bool(value)


def load_shared_config(secrets_path: str = ".streamlit/secrets.toml") -> SharedConfig:
    secrets = _read_secrets(secrets_path)
    google = secrets.get("google") or {}
    openai = secrets.get("openai") or {}
    github = secrets.get("github") or {}
    return SharedConfig(
        github_token=os.environ.get("GITHUB_TOKEN") or github.get("token", "") or "",
        google_api_key=os.environ.get("GEMINI_API_KEY") or google.get("api_key", "") or "",
        gemini_validator_model_id=os.environ.get("GEMINI_MODEL_ID") or google.get("gemini_validator_model_id", DEFAULT_MODEL_ID) or DEFAULT_MODEL_ID,
        openai_api_key=os.environ.get("OPENAI_API_KEY") or openai.get("api_key", "") or "",
        openai_validator_model_id=os.environ.get("OPENAI_VALIDATOR_MODEL_ID") or openai.get("validator_model_id", DEFAULT_OPENAI_VALIDATOR_MODEL_ID) or DEFAULT_OPENAI_VALIDATOR_MODEL_ID,
        grounding_enabled=_bool(os.environ.get("GROUNDING_ENABLED"), _bool(google.get("grounding_enabled"), True)),
        force_per_variant_validation=_bool(google.get("force_per_variant_validation"), True),
        single_gpt54_model_catalog_mode=_bool(
            os.environ.get("SINGLE_GPT54_MODEL_CATALOG_MODE"),
            _bool((secrets.get("catalog") or {}).get("single_gpt54_model_catalog_mode"), True),
        ),
    )
