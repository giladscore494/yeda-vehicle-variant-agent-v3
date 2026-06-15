"""Provider abstraction for selectable catalog validation models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .openai_catalog_client import CatalogClientSettings, CatalogClient as OpenAICatalogClient


GEMINI_CLIENT_MISSING_MESSAGE = "Gemini client library is not installed. Add google-genai to requirements.txt and redeploy Streamlit."


class ProviderUnavailableError(RuntimeError):
    """Selected catalog provider cannot be used before a run starts."""


def check_provider_available(settings: CatalogProviderSettings) -> None:
    """Fail fast if the selected provider lacks credentials or client library."""
    if not settings.api_key:
        if settings.provider == "openai":
            raise ProviderUnavailableError("OpenAI API key is missing for the selected GPT-5.4 validation model. No fallback was used.")
        if settings.provider == "google":
            raise ProviderUnavailableError("Google API key is missing for the selected Gemini 3.1 validation model. No fallback was used.")
        raise ProviderUnavailableError("Selected provider API key is missing; no fallback was used.")
    if settings.provider == "openai":
        try:
            from openai import OpenAI  # noqa: F401
        except ImportError as exc:
            raise ProviderUnavailableError("OpenAI client library is not installed. Add openai to requirements.txt and redeploy Streamlit.") from exc
        return
    if settings.provider == "google":
        try:
            from google import genai  # noqa: F401
        except ImportError as exc:
            raise ProviderUnavailableError(GEMINI_CLIENT_MISSING_MESSAGE) from exc
        return
    raise ProviderUnavailableError(f"Unsupported catalog provider: {settings.provider}")


@dataclass(frozen=True)
class CatalogProviderSettings:
    provider: Literal["openai", "google"]
    display_name: str
    model_id: str
    api_key: str
    web_search_enabled: bool = True
    grounding_enabled: bool = True


def build_catalog_client(settings: CatalogProviderSettings):
    if settings.provider == "openai":
        return OpenAICatalogClient(
            CatalogClientSettings(
                api_key=settings.api_key,
                model_id=settings.model_id,
                use_web_search=settings.web_search_enabled,
            )
        )
    if settings.provider == "google":
        from .gemini_catalog_client import GeminiCatalogClient

        return GeminiCatalogClient(settings)
    raise ValueError(f"Unsupported catalog provider: {settings.provider}")
