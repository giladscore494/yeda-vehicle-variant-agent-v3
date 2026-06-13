"""Gemini-only validation client (google-genai).

No OpenAI, no GPT adjudicator, no dual-model flow. This module wraps a single
Gemini call per cluster anchor (or per row when reuse is not possible),
requests strict JSON, parses it, and retries on transient/parse errors a
bounded number of times.

Prompt version: gemini31_validation_v2_evidence_current_year
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

Your job: validate a single vehicle variant for the Israeli used-car market.
Return strict JSON only. No prose. No markdown. No explanation outside the JSON.

---

## CARDINAL RULES — READ FIRST

### URLs
- NEVER fabricate a URL.
- A URL may only appear if grounding/search returned it as a real citation.
- If no verified URL exists: set "url": null. This is correct behavior, not a failure.

### Rejection
- Do NOT reject because trim is weak, generic, or missing.
- Reject ONLY for identity-level contradictions (wrong make/model/engine combination that cannot exist).
- valid identity + weak trim → clean_partial (always)

### clean_exact vs clean_partial
clean_exact requires ALL of:
  ✓ Israeli market sale/import actually verified (not "expected", "under consideration", "may arrive")
  ✓ Exact trim verified (not inferred, not a list, not null)
  ✓ No slash/pipe/comma in canonical_trim (e.g. "Turismo / Competizione" → NOT clean_exact)
  ✓ No unresolved identity-critical field
  ✓ Transmission verified for Israeli market

If ANY condition above is missing → use clean_partial, not reject.

---

## FIELD RULES

### official_marketed_name_il
- Fill this if the vehicle was officially marketed in Israel.
- Use Hebrew name as the local importer uses it (e.g. "טויוטה קורולה", "אבארט 500").
- If exact trim is unknown but the model was sold in Israel → still fill this field with the model name.
- Trim uncertainty ≠ model name uncertainty. Do not confuse them.
- Return null ONLY if you have genuine doubt about Israeli market presence.

### year_end
- If the vehicle is still in production or still imported to Israel → set year_end to null.
- Do NOT use the current year or a future year as a placeholder for "still active".
- Only set year_end to a concrete year if production/import clearly stopped that year.

### is_currently_produced / is_currently_imported_il
- is_currently_produced: true if the model is still manufactured globally.
- is_currently_imported_il: true if officially imported/sold in Israel now; null if uncertain; false if stopped.
- "Under consideration for Israel" → is_currently_imported_il: null (not true).

### canonical_trim
- If the trim field contains "/" or "|" or a comma-separated list of distinct trims → this is NOT clean_exact.
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

Never return "unknown" for a source you can clearly classify.

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
  "grounding_summary": string,
  "evidence_sources": [ ...objects per schema above... ],
  "possible_trim_names": [ ...strings... ],
  "split_candidates": [ ...strings... ],
  "blocking_identity_issues": [ ...strings... ],
  "non_blocking_trim_issues": [ ...strings... ],
  "fields_changed": [ ...strings... ],
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
