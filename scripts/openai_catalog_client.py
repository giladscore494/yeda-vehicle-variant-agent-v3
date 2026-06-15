"""GPT-5.4 Israeli-market technical-catalog client.

One grounded request per make/model cluster. GPT-5.4 collects ONLY technical
data (engines, horsepower, transmissions, drivetrain, body type, fuel type,
years, trims/versions, sources). It makes no publication / routing / risk /
guard / readiness decisions — Python validates the returned profile.

This module never reads any legacy generated output. A run always calls GPT-5.4
with web_search grounding and requires ``OPENAI_API_KEY``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .json_utils import parse_strict_json

CATALOG_SYSTEM_PROMPT = """You build a ready Israeli-market (IL) TECHNICAL catalog for ONE make/model.

You answer only one question: what technical versions of this make/model were
actually sold in Israel?

You must use web_search grounding for this task. Do not answer from memory. For \
every technical configuration you return, every non-null technical field must \
be supported by at least one Israeli-market source. Raw database values are \
only hints and are not evidence. If you cannot find a source for a field, set \
that field to null and list it under missing_grounded_fields. Do not invent \
trims, engines, horsepower values, transmissions, drivetrain, body types, or \
year ranges.

Prefer Israeli official importer pages/PDFs first, then Israeli \
catalog/spec/editorial sources, then marketplaces only as secondary evidence.

You return ONLY technical data. You do NOT make any of these decisions:
- no publication logic, no final route, no clean-catalog logic
- no guard flags, no risk score, no upload-readiness decision
- no per-row pass/fail validation

For each technical version actually sold in Israel, return a row in
technical_variants_il. Every row MUST include:
  body_type, fuel_type, engine, engine_displacement_l, horsepower_hp,
  transmission, drivetrain, year_start, year_end, support_level, source_indexes,
  field_sources, missing_grounded_fields.

field_sources maps each technical field to a list of source_index values that
support it, e.g. {"horsepower_hp": [0], "year_end": []}. Every non-null
technical field MUST have at least one source_index in field_sources. Any
field you cannot ground MUST be null and listed in missing_grounded_fields.

source_indexes reference entries in the top-level "sources" array. Each source
MUST include: source_index, title, url, source_name, source_type, supports
(the list of fields that source backs).

support_level MUST be exactly one of: direct, indirect, unknown, conflict.
Never use: acceptable, partial, candidate, moderate, limited, inferred,
contextual, conflicting_options, policy_consistent, patched_not_verified,
guardrail.

Do not infer horsepower from trim unless a source supports it. Do not infer
transmission from model architecture unless a source supports it. Do not infer
drivetrain unless sourced (if inferred from source context, support_level must
be "indirect" and field_sources must point to that source). Do not infer
year_end from the current year or from a raw database placeholder.

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
FORBIDDEN_SUPPORT_LEVELS = {
    "acceptable",
    "partial",
    "candidate",
    "moderate",
    "limited",
    "inferred",
    "contextual",
    "conflicting_options",
    "policy_consistent",
    "patched_not_verified",
    "guardrail",
}

# The ten technical fields that must each be web-grounded via field_sources.
GROUNDED_TECHNICAL_FIELDS = (
    "version_or_trim",
    "body_type",
    "fuel_type",
    "engine",
    "engine_displacement_l",
    "horsepower_hp",
    "transmission",
    "drivetrain",
    "year_start",
    "year_end",
)

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
    field_index_list = {"type": "array", "items": {"type": "integer"}}
    field_sources_schema = {
        "type": "object",
        "additionalProperties": True,
        "properties": {f: field_index_list for f in GROUNDED_TECHNICAL_FIELDS},
    }
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
            "field_sources": field_sources_schema,
            "missing_grounded_fields": {"type": "array", "items": {"type": "string"}},
        },
    }
    source_schema = {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "source_index": {"type": "integer"},
            "title": {"type": ["string", "null"]},
            "url": {"type": ["string", "null"]},
            "source_name": {"type": ["string", "null"]},
            "source_type": {"type": ["string", "null"]},
            "supports": {"type": "array", "items": {"type": "string"}},
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
            "sources": {"type": "array", "items": source_schema},
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

    def build_request_kwargs(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Assemble the Responses API kwargs for one real grounded cluster call.

        Real catalog runs MUST use web_search; we never silently drop it. A run
        with ``use_web_search=False`` is rejected here so it can never produce
        ungrounded "real" output.
        """
        import json as _json

        if not self.settings.use_web_search:
            raise RuntimeError(
                "web_search is required for real GPT-5.4 grounded catalog runs; "
                "refusing to call the model without the web_search tool."
            )
        return {
            "model": self.settings.model_id,
            "input": [
                {"role": "system", "content": CATALOG_SYSTEM_PROMPT},
                {"role": "user", "content": _json.dumps(request_payload, ensure_ascii=False)},
            ],
            "max_output_tokens": self.settings.max_output_tokens,
            "tools": [{"type": "web_search"}],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "israeli_model_technical_catalog",
                    "schema": _output_schema(),
                    "strict": False,
                }
            },
        }

    def build_profile(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send one cluster request to GPT-5.4 and return the parsed profile."""
        if not self.settings.api_key:
            raise RuntimeError("OpenAI API key missing for catalog client")

        client = self._ensure_client()
        self.calls += 1
        kwargs = self.build_request_kwargs(request_payload)
        try:
            resp = client.responses.create(**kwargs)
        except Exception as exc:  # noqa: BLE001 - surface a clean, sanitized error
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
