"""Gemini catalog client implementing the same high-level contract as OpenAI."""
from __future__ import annotations

import json
from typing import Any, Dict, List

from .catalog_provider import CatalogProviderSettings
from .json_utils import parse_strict_json
from .openai_catalog_client import CATALOG_SYSTEM_PROMPT


class GeminiCatalogClient:
    def __init__(self, settings: CatalogProviderSettings) -> None:
        self.settings = settings
        self.calls = 0
        self._client = None

    def _ensure_client(self):
        if self._client is None:
            try:
                from google import genai  # type: ignore
            except Exception as exc:  # noqa: BLE001
                raise RuntimeError("Gemini client library is unavailable") from exc
            self._client = genai.Client(api_key=self.settings.api_key)
        return self._client

    def _generate(self, prompt: str) -> Dict[str, Any]:
        if not self.settings.api_key:
            raise RuntimeError("Google API key missing for catalog client")
        client = self._ensure_client()
        self.calls += 1
        try:
            resp = client.models.generate_content(
                model=self.settings.model_id,
                contents=f"{CATALOG_SYSTEM_PROMPT}\n\nReturn STRICT JSON only.\n\n{prompt}",
            )
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Gemini catalog API call failed: {exc}") from exc
        text = getattr(resp, "text", None) or ""
        profile = parse_strict_json(text)
        if not isinstance(profile, dict):
            raise RuntimeError("Gemini catalog client returned non-object JSON")
        return profile

    def build_profile(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._generate(json.dumps(request_payload, ensure_ascii=False))

    def build_repair_profile(self, make: str, model: str, existing_profile: Dict[str, Any], targets: Dict[int, List[str]]) -> Dict[str, Any]:
        prompt = (
            f"Repair this Israeli-market profile for {make} {model}. Return the same JSON shape. "
            f"Only fill or correct these targeted fields: {json.dumps(targets, ensure_ascii=False)}. "
            "Do not add, remove, reorder, or alter other variants or fields. Existing profile: "
            f"{json.dumps(existing_profile, ensure_ascii=False)}"
        )
        return self._generate(prompt)
