"""Shared configuration loading for CLI and Streamlit.

Environment variables win. When absent, code may read the same key name from
Streamlit secrets (``OPENAI_API_KEY`` / ``GITHUB_TOKEN``). The documented and
required secret names are exactly:

- ``OPENAI_API_KEY`` — real GPT-5.4 grounded catalog calls.
- ``GITHUB_TOKEN``  — pushing catalog output/checkpoints back to GitHub.

The historical nested shapes (``[openai].api_key`` / ``[github].token``) are
kept ONLY as backward-compatible aliases; never introduce new alternative
secret names.
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
    # GitHub checkpointing for the new model-level catalog flow. Pushes happen
    # after each completed model profile (never after each raw variant).
    github_checkpoint_enabled: bool = False
    push_every_profiles: int = 1
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
        return value.strip().lower() not in {"false", "0", "no"}
    return bool(value)


def _int(value: Any, default: int) -> int:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def load_shared_config(secrets_path: str = ".streamlit/secrets.toml") -> SharedConfig:
    secrets = _read_secrets(secrets_path)
    google = secrets.get("google") or {}
    openai = secrets.get("openai") or {}
    github = secrets.get("github") or {}
    catalog = secrets.get("catalog") or {}

    # Required, documented secret names first; same key name from Streamlit
    # secrets next; legacy nested shapes ONLY as backward-compatible aliases.
    openai_api_key = (
        os.environ.get("OPENAI_API_KEY")
        or secrets.get("OPENAI_API_KEY")
        or openai.get("api_key", "")
        or ""
    )
    github_token = (
        os.environ.get("GITHUB_TOKEN")
        or secrets.get("GITHUB_TOKEN")
        or github.get("token", "")
        or ""
    )
    return SharedConfig(
        github_token=github_token,
        google_api_key=os.environ.get("GEMINI_API_KEY") or google.get("api_key", "") or "",
        gemini_validator_model_id=os.environ.get("GEMINI_MODEL_ID") or google.get("gemini_validator_model_id", DEFAULT_MODEL_ID) or DEFAULT_MODEL_ID,
        openai_api_key=openai_api_key,
        openai_validator_model_id=os.environ.get("OPENAI_VALIDATOR_MODEL_ID") or openai.get("validator_model_id", DEFAULT_OPENAI_VALIDATOR_MODEL_ID) or DEFAULT_OPENAI_VALIDATOR_MODEL_ID,
        grounding_enabled=_bool(os.environ.get("GROUNDING_ENABLED"), _bool(google.get("grounding_enabled"), True)),
        force_per_variant_validation=_bool(google.get("force_per_variant_validation"), True),
        single_gpt54_model_catalog_mode=_bool(
            os.environ.get("SINGLE_GPT54_MODEL_CATALOG_MODE"),
            _bool(catalog.get("single_gpt54_model_catalog_mode"), True),
        ),
        github_checkpoint_enabled=_bool(
            os.environ.get("GITHUB_CHECKPOINT_ENABLED"),
            _bool(catalog.get("github_checkpoint_enabled"), False),
        ),
        push_every_profiles=_int(
            os.environ.get("PUSH_EVERY_PROFILES"),
            _int(catalog.get("push_every_profiles"), 1),
        ),
        strict_github_checkpoint=_bool(
            os.environ.get("STRICT_GITHUB_CHECKPOINT"),
            _bool(catalog.get("strict_github_checkpoint"), False),
        ),
    )
