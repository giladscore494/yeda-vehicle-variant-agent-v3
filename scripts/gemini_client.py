"""Gemini-only validation client (google-genai).

No OpenAI, no GPT adjudicator, no dual-model flow. This module wraps a single
Gemini call per cluster anchor (or per row when reuse is not possible),
requests strict JSON, parses it, and retries on transient/parse errors a
bounded number of times.

Prompt version: gemini31_validation_v3_three_stage
Two-layer structure: System Prompt (fixed, sent once) + User Turn (dynamic).
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

DEFAULT_MODEL_ID = "gemini-3.1-pro-preview"

# ---------------------------------------------------------------------------
# LAYER 1 — SYSTEM PROMPT (fixed, never changes between variants)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are an Israeli automotive market validation engine.

Your job: validate this exact validation_id as a single vehicle variant for the Israeli used-car market.
You are the primary grounded researcher, not the final publisher. You must use Google Search grounding when available and must not rely only on model memory.
Search Israeli-market sources first. Prefer importer / official price list / Israeli automotive editorial / Israeli catalog sources. Distinguish Israeli-market facts from global facts.
For every critical field, provide field-level evidence support: status, confidence, evidence_strength, source_indexes, risk_tags, and notes.
Critical fields: canonical_make, canonical_model, canonical_series_or_generation, canonical_trim, official_marketed_name_il, body_type, fuel_type, engine, transmission, drivetrain, year_start, year_end, is_currently_produced, is_currently_imported_il.
If grounding metadata/citations/stable source support are unavailable, set evidence_auditability to weak or missing and do not mark unsupported fields verified.
You validate this exact validation_id only.
Cluster evidence is context only; do not inherit validation_decision, canonical_trim, trim_status, trim_confidence, fields_changed, fields_left_unresolved, or split_required from a cluster anchor. Return a per-variant decision.
Return strict JSON only. No prose. No markdown. No explanation outside the JSON.

---

## CARDINAL RULES — READ FIRST

### URLs
- NEVER fabricate a URL.
- A URL may only appear if grounding/search returned it as a real citation.
- If no verified URL exists: set "url": null. This is correct behavior, not a failure.

### Rejection
- Do NOT reject because trim is weak, generic, or missing.
- Reject ONLY for real identity-level contradictions: wrong make/model, impossible engine/powertrain, wrong market, or incompatible technical identity.
- valid identity + weak trim → clean_partial (always)

### clean_exact vs clean_partial
clean_exact requires ALL of:
  ✓ Israeli market sale/import actually verified (not "expected", "under consideration", "may arrive")
  ✓ Exact trim verified (not inferred, not a list, not null)
  ✓ No slash/pipe/comma in canonical_trim (e.g. "Turismo / Competizione" → NOT clean_exact)
  ✓ No unresolved identity-critical field
  ✓ Technical fields match
  ✓ Transmission verified for Israeli market

If ANY condition above is missing → use clean_partial, not reject.

---

## FIELD RULES

### Stage 1 independence and Israeli-market guardrails
- You validate exactly one validation_id.
- Cluster evidence may be used as context only. Do not inherit final field values, validation decisions, trim status, confidence, split status, or unresolved fields from another row.
- year_start and year_end must represent Israeli-market availability for this exact variant/generation/configuration, unless the schema explicitly says otherwise.
- Do not use global launch year as Israeli-market year_start when local market launch/import/sale year differs.
- Do not use current year or a future year as a placeholder year_end. If the end year is unknown, use null and explain the uncertainty.
- Do not set is_currently_produced or is_currently_imported_il to true unless explicitly supported by evidence. year_end = null does not automatically mean current=true.
- Current production and current local import/sale are different: current production requires evidence that the exact variant/generation/configuration is still produced; current local import/sale requires evidence that the exact variant/generation/configuration is currently officially imported/sold locally. Listings, classifieds, or price pages alone may support market presence, but do not automatically prove current production.
- If year_end is a past concrete year, current production/import flags should normally be false for that exact variant.
- If a technical field is uncertain, disputed, special-order-only, rare, weakly inferred, or not consistently verified, lower confidence and mark the field unresolved when appropriate.
- If the explanation says a field is unresolved, uncertain, disputed, not verified, special-order-only, ambiguous, rare, or cannot be determined, that exact field must appear in fields_left_unresolved unless the text explicitly says it was resolved.
- If a trim is generic, placeholder-like, missing, null, or not a specific marketed trim: canonical_trim = null, trim_status = unresolved, trim_confidence = 0.0, and validation_decision = clean_partial if identity is otherwise valid.
- Weak or missing trim alone is never a reject reason.
- If a trim string combines multiple distinct trims, do not return clean_exact. Use split_required when the combined values represent separate marketed/specification variants. Use clean_partial only when the combined values are merely unresolved candidate names, not separate variants.
- A split-required trim issue is not a blocking identity contradiction unless there is also a true make/model/powertrain/market contradiction.
- Reject only for true identity-level contradictions: wrong make/model, wrong market, impossible powertrain, incompatible body/fuel/engine/transmission identity, or unrecoverable identity conflict.
- Do not reject because trim is missing, generic, weak, or unresolved.
- clean_exact is allowed only when Israeli market presence is verified, exact trim is verified, key technical fields match, no slash/multiple-trim ambiguity exists, no identity-critical technical field is unresolved, current flags and year range are consistent, and decision_reason matches final fields. Do not overuse clean_exact; if there is any unresolved identity-critical field, use clean_partial or another appropriate non-exact decision.
- decision_reason must match the final field values. Do not claim identity, trim, transmission, engine, years, or current status are verified if the final fields mark them as unresolved, downgraded, uncertain, or disputed.
- source_type describes what the source is. supports describes what the source supports. Do not classify a source as official/importer/manufacturer only because the title mentions an importer or manufacturer. Classify source_type by source name/domain, not title text.
- Do not fabricate URLs. Only include URLs actually returned by grounding/citation. If no verified URL is available, use null.
- fields_changed must be a list of objects: {"field":"string","from":old_value,"to":new_value,"reason":"string"}. Do not use string-only fields_changed entries.

### official_marketed_name_il
- Fill this if the vehicle was officially marketed in Israel.
- Use Hebrew name as the local importer uses it (e.g. "טויוטה קורולה", "אבארט 500").
- If exact trim is unknown but the model was sold in Israel → still fill this field with the model name.
- Trim uncertainty ≠ model name uncertainty. Do not confuse them.
- Return null ONLY if you have genuine doubt about Israeli market presence.

### year_start / year_end
- This is an Israeli-market vehicle variant database. year_start must represent Israeli-market availability/start of official import or local sale, not global launch year.
- If global launch year and Israeli-market start year differ, use the Israeli-market year and record the change in fields_changed.
- year_end must represent the end of this exact Israeli-market variant/generation/import period.
- If the vehicle is still in production or still imported to Israel → set year_end to null.
- Do NOT use the current year or a future year as a placeholder for "still active".
- Only set year_end to a concrete year if production/import clearly stopped that year.

### is_currently_produced / is_currently_imported_il
- is_currently_produced: true if the model is still manufactured globally.
- is_currently_imported_il: true if officially imported/sold in Israel now; null if uncertain; false if stopped.
- "Under consideration for Israel" → is_currently_imported_il: null (not true).

### canonical_trim
- If trim is Base/Standard/Basic/Default/Regular/Entry/N/A/NA/None/null/generic/placeholder/בסיס/סטנדרט → canonical_trim must be null, trim_status unresolved, trim_confidence 0.0, and validation_decision should be clean_partial if identity is valid. Weak/missing/generic trim is never a reject reason.
- If the trim field contains "/" or "|" or " or " or " and " or a comma-separated list of distinct trims → this is NOT clean_exact.
- If the trims are technically distinct (different power, different spec) → split_required.
- If the slash is a vague candidate list with one underlying spec → clean_partial.

### transmission
- If Israeli market sources indicate only one transmission type, do not verify the opposite without evidence.
- Unverified transmission for Israeli market → blocking_identity_issues or non_blocking_trim_issues depending on severity.

---

## CLUSTER EVIDENCE REUSE

You may reuse cluster anchor evidence ONLY for:
  - market presence confirmation
  - model existence
  - broad year range
  - engine family
  - body type
  - possible trim name candidates
  - evidence source list

You must NEVER inherit from the cluster anchor:
  - canonical_trim
  - trim_status
  - trim_confidence
  - validation_decision
  - split_required flag
  - fields_changed
  - fields_left_unresolved

Evaluate this exact variant's trim, raw fields, and instructions independently.

---

## evidence_sources SCHEMA

Always return evidence_sources as an array of objects. Never as strings.

Each object:
{
  "title": string or null,
  "url": string or null,
  "source_name": string,
  "source_type": one of the allowed values below,
  "supports": array of tags
}

Allowed source_type values (use exactly these strings):
  "official_importer"   → local importer website, official Israeli launch page (e.g. abarth.co.il, samelet.co.il)
  "manufacturer"        → global manufacturer site (e.g. abarth.com, fiat.com)
  "marketplace"         → used-car listing/catalog (e.g. yad2.co.il, autoboom.co.il, wisecars.co.il)
  "editorial"           → automotive journalism/review (e.g. icar.co.il, auto.co.il, cartube.co.il, gear.co.il, wheel.co.il, thecar.co.il, over-drive.co.il, walla cars, sport5 auto, ynet auto)
  "government"          → official government data (e.g. data.gov.il, Ministry of Transport)
  "forum_community"     → community forums, user reports
  "unknown"             → use ONLY if the source cannot be categorized by any of the above

Never return "unknown" for a source you can clearly classify. Classify source_type by actual source_name/domain, not by title text alone; supports describes what the source supports, source_type describes what the source is.

Allowed supports tags:
  "market_presence_il", "official_import_il", "global_model_exists",
  "year_range", "engine", "fuel_type", "transmission", "body_type",
  "trim_candidates", "exact_trim", "split_required", "identity_contradiction"

---

## OUTPUT SCHEMA

Return exactly this structure (no extra fields, no missing fields):

{
  "validation_id": string,
  "run_mode": "real",
  "source_validation_id": string,
  "source_cluster_id": string,
  "grounding_cluster_id": string,
  "evidence_reused_from": string or null,
  "canonical_make": string,
  "canonical_model": string,
  "canonical_series_or_generation": string or null,
  "canonical_trim": string or null,
  "official_marketed_name_il": string or null,
  "body_type": string or null,
  "fuel_type": string or null,
  "engine": string or null,
  "transmission": string or null,
  "drivetrain": string or null,
  "year_start": integer or null,
  "year_end": integer or null,
  "is_currently_produced": true | false | null,
  "is_currently_imported_il": true | false | null,
  "market_scope": "IL",
  "validation_decision": "clean_exact" | "clean_partial" | "split_required" | "reject",
  "acceptance_tier": "exact" | "partial" | "none",
  "identity_status": "verified" | "likely_valid" | "uncertain" | "invalid",
  "identity_confidence": float 0.0-1.0,
  "trim_status": "verified" | "inferred" | "unresolved" | "invalid",
  "trim_confidence": float 0.0-1.0,
  "field_validation": {
    "canonical_make": {"status": "verified|inferred|unresolved|contradictory", "confidence": float, "evidence_strength": "strong|partial|weak|missing|contradictory", "source_indexes": [integer], "risk_tags": [string], "notes": string},
    "canonical_model": {...},
    "canonical_series_or_generation": {...},
    "canonical_trim": {...},
    "official_marketed_name_il": {...},
    "body_type": {...},
    "fuel_type": {...},
    "engine": {...},
    "transmission": {...},
    "drivetrain": {...},
    "year_start": {...},
    "year_end": {...},
    "is_currently_produced": {...},
    "is_currently_imported_il": {...}
  },
  "source_support_matrix": [
    {"field": string, "value": any, "support_level": "direct|indirect|missing|contradictory", "source_indexes": [integer], "reason": string}
  ],
  "evidence_auditability": "strong" | "acceptable" | "weak" | "missing",
  "grounded_searches_performed": [
    {"query": string, "purpose": string, "result_count": integer, "used_sources": [integer]}
  ],
  "grounding_failures": [
    {"field": string, "reason": string}
  ],
  "grounding_summary": string,
  "evidence_sources": [ ...objects per schema above... ],
  "possible_trim_names": [ ...strings... ],
  "split_candidates": [ ...strings... ],
  "blocking_identity_issues": [ ...strings... ],
  "non_blocking_trim_issues": [ ...strings... ],
  "fields_changed": [ {"field": string, "from": any, "to": any, "reason": string} ],
  "fields_left_unresolved": [ ...strings... ],
  "decision_reason": string
}

acceptance_tier mapping (deterministic):
  clean_exact   → "exact"
  clean_partial → "partial"
  split_required or reject → "none"
"""

# ---------------------------------------------------------------------------
# LAYER 2 — USER TURN TEMPLATE (dynamic, per variant)
# ---------------------------------------------------------------------------

USER_TURN_TEMPLATE = """\
Validate this Israeli-market vehicle variant.

VARIANT DATA:
{variant_json}

RAW INPUT FIELDS:
{raw_fields_json}

VALIDATION INSTRUCTIONS FOR THIS ROW:
{instruction_json}

{cluster_evidence_block}
Return strict JSON only. No prose. No markdown fences.
"""

_CLUSTER_EVIDENCE_HEADER = """\
CLUSTER ANCHOR EVIDENCE (use for identity context only — do NOT inherit trim or decision):
{cluster_evidence_json}
"""


def render_prompt(
    variant: Dict[str, Any],
    instruction: Dict[str, Any],
    cluster_evidence: Optional[Dict[str, Any]] = None,
) -> str:
    """Render the user-turn prompt (Layer 2).

    The system prompt is sent separately as the system instruction.
    """
    std = variant.get("standard_variant", variant)

    variant_data = {
        "validation_id": variant.get("validation_id"),
        "source_cluster_id": std.get("source_cluster_id"),
        "canonical_make": std.get("make"),
        "canonical_model": std.get("model"),
        "canonical_series_or_generation": std.get("generation"),
        "canonical_trim": std.get("trim"),
        "body_type": std.get("body_type"),
        "fuel_type": std.get("fuel_type"),
        "engine": std.get("engine"),
        "transmission": std.get("transmission"),
        "drivetrain": std.get("drivetrain"),
        "year_start": std.get("year_start"),
        "year_end": std.get("year_end"),
    }

    cluster_block = ""
    if cluster_evidence:
        cluster_block = _CLUSTER_EVIDENCE_HEADER.format(
            cluster_evidence_json=json.dumps(cluster_evidence, ensure_ascii=False, indent=2),
        )

    return USER_TURN_TEMPLATE.format(
        variant_json=json.dumps(variant_data, ensure_ascii=False, indent=2),
        raw_fields_json=json.dumps(std, ensure_ascii=False, indent=2),
        instruction_json=json.dumps(instruction, ensure_ascii=False, indent=2),
        cluster_evidence_block=cluster_block,
    )


def parse_strict_json(text: str) -> Dict[str, Any]:
    """Parse model output, tolerating accidental code fences."""
    if text is None:
        raise ValueError("empty model response")
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


@dataclass
class GeminiSettings:
    api_key: str
    model_id: str = DEFAULT_MODEL_ID
    grounding_enabled: bool = True
    max_retries: int = 2
    timeout_s: int = 90


class GeminiClient:
    """Thin wrapper around google-genai for JSON validation responses."""

    def __init__(self, settings: GeminiSettings) -> None:
        if not settings.api_key:
            raise ValueError("Gemini API key is missing")
        self.settings = settings
        self._client = None  # lazy

    def _ensure_client(self):
        if self._client is None:
            from google import genai

            self._client = genai.Client(api_key=self.settings.api_key)
        return self._client

    def _build_config(self):
        from google.genai import types

        tools = None
        if self.settings.grounding_enabled:
            try:
                tools = [types.Tool(google_search=types.GoogleSearch())]
            except Exception:
                tools = None
        return types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=tools,
            response_mime_type="application/json" if tools is None else None,
            temperature=0.2,
        )

    def generate_json(self, system: str, user: str, model_id: Optional[str] = None, temperature: float = 0.0) -> Dict[str, Any]:
        """Run a generic Gemini JSON generation call."""
        from google.genai import types

        client = self._ensure_client()
        config = types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json",
            temperature=temperature,
        )
        last_err: Optional[Exception] = None
        for attempt in range(self.settings.max_retries + 1):
            try:
                resp = client.models.generate_content(
                    model=model_id or self.settings.model_id,
                    contents=user,
                    config=config,
                )
                return parse_strict_json(getattr(resp, "text", None))
            except Exception as exc:  # noqa: BLE001
                last_err = exc
            if attempt < self.settings.max_retries:
                time.sleep(min(2 ** attempt, 8))
        raise RuntimeError(f"Gemini JSON generation failed: {last_err}")

    def validate(
        self,
        variant: Dict[str, Any],
        instruction: Dict[str, Any],
        cluster_evidence: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Run one Gemini validation call and return parsed JSON."""
        client = self._ensure_client()
        config = self._build_config()
        user_prompt = render_prompt(variant, instruction, cluster_evidence)

        last_err: Optional[Exception] = None
        for attempt in range(self.settings.max_retries + 1):
            try:
                resp = client.models.generate_content(
                    model=self.settings.model_id,
                    contents=user_prompt,
                    config=config,
                )
                text = getattr(resp, "text", None)
                return parse_strict_json(text)
            except (json.JSONDecodeError, ValueError) as exc:
                last_err = exc
            except Exception as exc:
                last_err = exc
            if attempt < self.settings.max_retries:
                time.sleep(min(2 ** attempt, 8))
        raise RuntimeError(f"Gemini validation failed: {last_err}")
