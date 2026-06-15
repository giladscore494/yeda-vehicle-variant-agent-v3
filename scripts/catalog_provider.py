"""Provider abstraction for selectable catalog validation models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .openai_catalog_client import CatalogClientSettings, CatalogClient as OpenAICatalogClient


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
