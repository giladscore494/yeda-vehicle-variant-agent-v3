"""GPT-5.4 Israeli-market technical-catalog client.

One grounded request per make/model cluster. GPT-5.4 collects ONLY technical
data (engines, horsepower, transmissions, drivetrain, body type, fuel type,
years, trims/versions, sources). It makes no publication / routing / risk /
guard / readiness decisions — Python validates the returned profile.

This module is Gemini-free and never reads any legacy generated output.

A deterministic offline synthesizer (:meth:`CatalogClient.synthesize_offline`)
is provided so the pipeline plumbing and the one-model test sample can run
without network or an API key. Offline profiles are intentionally conservative
(``support_level="unknown"``, ``profile_confidence="low"``) so they route to
the review output rather than the website-ready output.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .gemini_client import parse_strict_json

CATALOG_SYSTEM_PROMPT = """You build a ready Israeli-market (IL) TECHNICAL catalog for ONE make/model.

You answer only one question: what technical versions of this make/model were
actually sold in Israel?

You return ONLY technical data. You do NOT make any of these decisions:
- no publication logic, no final route, no clean-catalog logic
- no guard flags, no risk score, no upload-readiness decision
- no per-row pass/fail validation

Use Israeli-market sources and web grounding when available. Do not invent
facts, sources, URLs, or impossible combinations.

For each technical version actually sold in Israel, return a row in
technical_variants_il. Every row MUST include:
  body_type, fuel_type, engine, engine_displacement_l, horsepower_hp,
  transmission, drivetrain, year_start, year_end, support_level, source_indexes.

support_level MUST be exactly one of: direct, indirect, unknown, conflict.

Trim rules:
- "Base" is not a trim. "Standard" is not a trim. None/null is not a trim.
- A bare engine size like "1.4" is not a trim.
- Horsepower labels like "145hp"/"165hp"/"180hp" are not trims.
- A body/model designation such as "500C" is not a trim.
- If the version/trim is unknown, set "version_or_trim": null.
- Put rejected labels in invalid_or_non_trim_labels with a classification.

Model identity rules:
- An electric model (e.g. "500e") is a SEPARATE model. Never mix EV and petrol
  versions under the same petrol model profile.
- Do not invent combinations. Each row must be a real sold configuration.
- If there is no source for a row, keep support_level="unknown".

available_values_for_website MUST be derived only from technical_variants_il.

Return STRICT JSON only, matching the requested schema. No prose."""

ALLOWED_SUPPORT_LEVELS = {"direct", "indirect", "unknown", "conflict"}

# Labels that are never valid trims (model-agnostic part).
_GENERIC_NON_TRIMS = {
    "base",
    "standard",
    "std",
    "none",
    "null",
    "n/a",
    "na",
    "unknown",
    "default",
    "",
}

_ENGINE_SIZE_RE = re.compile(r"^\d+(\.\d+)?\s*(l|liter|litre)?$", re.IGNORECASE)
_HP_RE = re.compile(r"^\d+\s*(hp|ps|bhp|kw)$", re.IGNORECASE)


def classify_non_trim(label: Optional[str], model: str) -> Optional[Dict[str, str]]:
    """Return a non-trim classification dict, or None if it could be a trim."""
    if label is None:
        return {"label": label, "classification": "null", "reason": "Null is not a trim."}
    text = str(label).strip()
    low = text.lower()
    if low in _GENERIC_NON_TRIMS:
        return {
            "label": text,
            "classification": "placeholder",
            "reason": "Generic placeholder, not an official trim.",
        }
    if _ENGINE_SIZE_RE.match(low):
        return {
            "label": text,
            "classification": "engine_size",
            "reason": "Engine displacement, not a trim.",
        }
    if _HP_RE.match(low):
        return {
            "label": text,
            "classification": "horsepower",
            "reason": "Power figure, not a trim.",
        }
    model_low = (model or "").strip().lower()
    if model_low and low in {model_low, model_low + "c", model_low + "e"}:
        return {
            "label": text,
            "classification": "body_or_model_designation",
            "reason": "Body/model designation, not a trim.",
        }
    return None


@dataclass
class CatalogClientSettings:
    api_key: str = ""
    model_id: str = "gpt-5.4"
    use_web_search: bool = True
    max_output_tokens: int = 8000


def _output_schema() -> Dict[str, Any]:
    variant_schema = {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "version_or_trim": {"type": ["string", "null"]},
            "body_type": {"type": ["string", "null"]},
            "fuel_type": {"type": ["string", "null"]},
            "engine": {"type": ["string", "null"]},
            "engine_displacement_l": {"type": ["number", "null"]},
            "horsepower_hp": {"type": ["number", "null"]},
            "transmission": {"type": ["string", "null"]},
            "drivetrain": {"type": ["string", "null"]},
            "year_start": {"type": ["integer", "null"]},
            "year_end": {"type": ["integer", "null"]},
            "support_level": {"type": "string"},
            "source_indexes": {"type": "array", "items": {"type": "integer"}},
        },
    }
    return {
        "type": "object",
        "additionalProperties": True,
        "required": ["market", "make", "model", "technical_variants_il"],
        "properties": {
            "market": {"type": "string"},
            "make": {"type": "string"},
            "model": {"type": "string"},
            "canonical_model": {"type": ["string", "null"]},
            "year_start": {"type": ["integer", "null"]},
            "year_end": {"type": ["integer", "null"]},
            "technical_variants_il": {"type": "array", "items": variant_schema},
            "available_values_for_website": {"type": "object", "additionalProperties": True},
            "invalid_or_non_trim_labels": {"type": "array"},
            "sources": {"type": "array"},
            "profile_confidence": {"type": "string"},
            "notes": {"type": "array"},
        },
    }


class CatalogClient:
    """GPT-5.4 catalog client (one call per make/model cluster)."""

    def __init__(self, settings: CatalogClientSettings) -> None:
        self.settings = settings
        self.calls = 0
        self._client = None

    def _ensure_client(self):
        if self._client is None:
            from openai import OpenAI

            self._client = OpenAI(api_key=self.settings.api_key)
        return self._client

    def build_profile(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send one cluster request to GPT-5.4 and return the parsed profile."""
        if not self.settings.api_key:
            raise RuntimeError("OpenAI API key missing for catalog client")
        import json as _json

        client = self._ensure_client()
        self.calls += 1
        kwargs: Dict[str, Any] = {
            "model": self.settings.model_id,
            "input": [
                {"role": "system", "content": CATALOG_SYSTEM_PROMPT},
                {"role": "user", "content": _json.dumps(request_payload, ensure_ascii=False)},
            ],
            "max_output_tokens": self.settings.max_output_tokens,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "israeli_model_technical_catalog",
                    "schema": _output_schema(),
                    "strict": False,
                }
            },
        }
        used_web_search = False
        if self.settings.use_web_search:
            kwargs["tools"] = [{"type": "web_search_preview"}]
            used_web_search = True
        try:
            resp = client.responses.create(**kwargs)
        except Exception as exc:  # web search may be unsupported in this env
            if used_web_search:
                kwargs.pop("tools", None)
                resp = client.responses.create(**kwargs)
            else:
                raise RuntimeError(f"catalog API call failed: {exc}") from exc

        text = getattr(resp, "output_text", None)
        if not text:
            parts: List[str] = []
            for item in getattr(resp, "output", []) or []:
                for c in getattr(item, "content", []) or []:
                    if getattr(c, "text", None):
                        parts.append(c.text)
            text = "\n".join(parts)
        profile = parse_strict_json(text)
        if not isinstance(profile, dict):
            raise RuntimeError("catalog client returned non-object JSON")
        return profile

    # ------------------------------------------------------------------
    # Offline synthesizer (no network / no API key) — for tests & plumbing
    # ------------------------------------------------------------------

    @staticmethod
    def synthesize_offline(request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Build a conservative profile from raw values without a model call.

        Horsepower is unknown offline, so rows are intentionally incomplete and
        will be routed to the review output by the Python validator. This keeps
        the offline sample honest: it exercises grouping/validation/output, but
        never fabricates website-ready data.
        """
        make = request_payload.get("make", "")
        model = request_payload.get("model", "")
        market = request_payload.get("market", "IL")
        raw = request_payload.get("raw_database_values", {}) or {}
        years = [y for y in raw.get("years_seen", []) if isinstance(y, int)]
        year_start = min(years) if years else None
        year_end = max(years) if years else None

        trims_seen = raw.get("trims_seen", []) or []
        invalid_labels: List[Dict[str, str]] = []
        real_trims: List[Optional[str]] = []
        for trim in trims_seen:
            classification = classify_non_trim(trim, model)
            if classification is not None:
                invalid_labels.append(classification)
            else:
                real_trims.append(trim)
        if not real_trims:
            real_trims = [None]

        body = (raw.get("body_types_seen") or [None])[0]
        fuel = (raw.get("fuel_types_seen") or [None])[0]
        engine = (raw.get("engines_seen") or [None])[0]
        transmission = (raw.get("transmissions_seen") or [None])[0]
        drivetrain = (raw.get("drivetrains_seen") or [None])[0]
        source_indexes = request_payload.get("source_indexes", []) or []

        variants = []
        for trim in real_trims:
            variants.append(
                {
                    "version_or_trim": trim,
                    "body_type": body,
                    "fuel_type": fuel,
                    "engine": engine,
                    "engine_displacement_l": None,
                    "horsepower_hp": None,  # unknown offline
                    "transmission": transmission,
                    "drivetrain": drivetrain,
                    "year_start": year_start,
                    "year_end": year_end,
                    "support_level": "unknown",
                    "source_indexes": [],
                }
            )

        return {
            "market": market,
            "make": make,
            "model": model,
            "canonical_model": model,
            "year_start": year_start,
            "year_end": year_end,
            "technical_variants_il": variants,
            "available_values_for_website": {},
            "invalid_or_non_trim_labels": invalid_labels,
            "sources": [],
            "profile_confidence": "low",
            "notes": [
                "Generated offline without GPT-5.4; horsepower/sources unknown. "
                "Run with an OpenAI API key for a grounded catalog."
            ],
        }
