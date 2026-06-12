"""OpenAI GPT-5.4 adjudicator client for the two-model validation architecture.

GPT-5.4 is the final semantic judge. It receives:
  - The original variant row
  - Active model context
  - Gemini's normalized research pack
  - Deterministic QA warnings
  - Previous attempt/correction context

It returns one of:
  auto_resolved | split_required | needs_more_grounding | rejected_from_clean

Security: API keys are never logged or written to output.
"""

from __future__ import annotations

import json
import time
from typing import Any

# ── Adjudicator system prompt ─────────────────────────────────────────────

ADJUDICATOR_SYSTEM_PROMPT = """\
You are the final adjudicator for a clean Israeli-market canonical vehicle variants database.

You are given:
1. The original source variant row.
2. Active model context for this make/model.
3. Gemini research pack with grounded evidence.
4. Deterministically normalized source strengths.
5. QA warnings and unresolved reasons.
6. The current attempt number and max attempts.

Your job is to decide the final canonical action.

Gemini is only the researcher. Do not blindly follow Gemini.
Use the evidence, source hierarchy, and deterministic QA rules.

## Source hierarchy (strict)
- official_importer, price_list, brochure => strong evidence
- israeli_auto_site, dealer_page => medium evidence
- used_listing, non_israeli_technical_source => weak evidence only

## Decision rules

Use `auto_resolved` ONLY if:
- Israeli-market evidence verifies the exact marketed trim/variant
- The row can be uniquely mapped to one trim
- The corrected name is not invented
- The evidence is strong enough (official/price list preferred)
- There is no unresolved split risk
- There is no critical field change without evidence

Use `split_required` if:
- The row appears to represent a model/family with multiple Israeli trims
- Israeli evidence shows multiple real trims/variants
- The row cannot distinguish between them
- Creating one clean row would collapse multiple variants
- Or the raw trim itself combines multiple trims (e.g. "Turismo / Competizione")

Use `needs_more_grounding` if:
- Promising Israeli evidence exists
- But it's not enough to safely map, split, or reject
- And attempts remain

Use `rejected_from_clean` if:
- After targeted grounding, the row still cannot be uniquely mapped
- And there is no useful split task
- Or the name is only generic/model-family level with no candidate split
- Or the trim remains missing/unverified
- Or attempts are exhausted after needs_more_grounding

## Important rules
- Never invent Israeli trim names
- Never collapse multiple real trims into one clean row
- Base/Standard/Unknown/None/null are NOT authoritative trims
- Short values like "595" may indicate model family, not trim
- Missing trim means the dataset failed to capture trim, not that no trim existed
- Treat Gemini output as evidence, not as authority

## Output format
Return ONLY valid JSON matching the adjudicator schema. No markdown, no prose.
"""

# ── Adjudicator output schema ─────────────────────────────────────────────

ADJUDICATOR_SCHEMA = {
    "type": "object",
    "required": [
        "validation_id", "make", "model",
        "input_raw_trim_name", "input_raw_official_marketed_name_il",
        "israeli_market_presence", "recovered_identity",
        "trim_name_il_status", "field_corrections",
        "possible_israeli_trims_found", "split_review",
        "evidence_items", "grounding_attempts",
        "adjudicator_notes", "final_decision",
        "final_confidence", "final_reason",
        "clean_database_action",
    ],
    "properties": {
        "validation_id": {"type": "string"},
        "make": {"type": "string"},
        "model": {"type": "string"},
        "input_raw_trim_name": {"type": ["string", "null"]},
        "input_raw_official_marketed_name_il": {"type": ["string", "null"]},
        "israeli_market_presence": {
            "type": "object",
            "properties": {
                "status": {"type": "string",
                           "enum": ["verified", "likely", "uncertain", "not_verified"]},
                "summary": {"type": "string"},
            },
        },
        "recovered_identity": {
            "type": "object",
            "properties": {
                "official_marketed_name_il": {"type": ["string", "null"]},
                "official_marketed_name_en": {"type": ["string", "null"]},
                "trim_name_il": {"type": ["string", "null"]},
                "trim_name_en": {"type": ["string", "null"]},
                "model_family": {"type": ["string", "null"]},
                "confidence": {"type": "number"},
            },
        },
        "trim_name_il_status": {
            "type": "string",
            "enum": ["verified", "recovered", "generic_family_only",
                     "not_available", "uncertain"],
        },
        "field_corrections": {"type": "object"},
        "possible_israeli_trims_found": {"type": "array"},
        "split_review": {
            "type": "object",
            "properties": {
                "split_recommended": {"type": "boolean"},
                "reason": {"type": "string"},
                "candidate_child_variants": {"type": "array"},
            },
        },
        "evidence_items": {"type": "array"},
        "grounding_attempts": {"type": "object"},
        "adjudicator_notes": {"type": "object"},
        "final_decision": {
            "type": "string",
            "enum": ["auto_resolved", "split_required",
                     "needs_more_grounding", "rejected_from_clean"],
        },
        "final_confidence": {"type": "number"},
        "final_reason": {"type": "string"},
        "clean_database_action": {
            "type": "object",
            "properties": {
                "insert_into_clean": {"type": "boolean"},
                "create_split_tasks": {"type": "boolean"},
                "send_to_retry": {"type": "boolean"},
                "reject_reason": {"type": "string"},
            },
        },
    },
}

# Valid final decisions from the adjudicator
ADJUDICATOR_DECISIONS = frozenset({
    "auto_resolved",
    "split_required",
    "needs_more_grounding",
    "rejected_from_clean",
})


def build_adjudicator_prompt(
    merged_context: dict,
    research_pack: dict,
    qa_warnings: list[str],
    unresolved_reasons: list[str],
    attempt_number: int,
    max_attempts: int,
) -> str:
    """Build the user prompt for GPT-5.4 adjudication."""
    sv = merged_context.get("standard_variant") or {}
    payload = {
        "validation_id": merged_context["validation_id"],
        "original_variant": {
            "make": sv.get("make"),
            "model": sv.get("model"),
            "trim": sv.get("trim"),
            "official_marketed_name_il": sv.get("official_marketed_name_il"),
            "year_start": sv.get("year_start"),
            "year_end": sv.get("year_end"),
            "engine": sv.get("engine"),
            "transmission": sv.get("transmission"),
            "fuel_type": sv.get("fuel_type"),
            "drivetrain": sv.get("drivetrain"),
            "body_type": sv.get("body_type"),
            "generation": sv.get("generation"),
            "seats": sv.get("seats"),
            "variant_id": sv.get("variant_id"),
        },
        "active_model_context": merged_context.get("active_model_context"),
        "gemini_research_pack": research_pack,
        "deterministic_qa_warnings": qa_warnings,
        "unresolved_reasons": unresolved_reasons,
        "attempt_number": attempt_number,
        "max_attempts": max_attempts,
        "source_trim_was_generic": merged_context.get("source_trim_was_generic", False),
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def parse_adjudicator_response(text: str) -> dict:
    """Parse the adjudicator response, tolerating markdown fences."""
    import re
    if not isinstance(text, str) or not text.strip():
        raise ValueError("empty adjudicator response")
    candidate = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", candidate, re.DOTALL)
    if fence:
        candidate = fence.group(1)
    else:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("no JSON object found in adjudicator response")
        candidate = candidate[start:end + 1]
    parsed = json.loads(candidate)
    if not isinstance(parsed, dict):
        raise ValueError("adjudicator response is not a JSON object")
    decision = parsed.get("final_decision")
    if decision not in ADJUDICATOR_DECISIONS:
        raise ValueError(f"invalid final_decision: {decision}")
    return parsed


# ── Map adjudicator decision to engine final status ───────────────────────

def map_decision_to_engine_status(decision: str) -> str | None:
    """Map adjudicator decision to engine final decision.
    Returns None for needs_more_grounding (not a final decision)."""
    mapping = {
        "auto_resolved": "auto_resolved",
        "split_required": "split_required",
        "rejected_from_clean": "rejected_from_clean",
        "needs_more_grounding": None,  # not final
    }
    return mapping.get(decision)


# ── OpenAI client ─────────────────────────────────────────────────────────

class OpenAIAdjudicatorClient:
    """REST client for GPT-5.4 final adjudication."""

    def __init__(self, api_key: str, model_id: str, log=print):
        self.api_key = api_key
        self.model_id = model_id
        self.log = log

    def adjudicate(
        self,
        merged_context: dict,
        research_pack: dict,
        qa_warnings: list[str],
        unresolved_reasons: list[str],
        attempt_number: int,
        max_attempts: int,
        rate_limit_max_retries: int = 6,
        rate_limit_base_backoff: int = 10,
    ) -> dict:
        """Call GPT-5.4 and return the parsed adjudication response."""
        import requests

        user_prompt = build_adjudicator_prompt(
            merged_context, research_pack, qa_warnings,
            unresolved_reasons, attempt_number, max_attempts,
        )

        body = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": ADJUDICATOR_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.0,
            "max_tokens": 4096,
            "response_format": {"type": "json_object"},
        }

        attempt = 0
        while True:
            try:
                resp = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": "Bearer " + self.api_key,
                        "Content-Type": "application/json",
                    },
                    json=body,
                    timeout=120,
                )
            except requests.RequestException as e:
                if attempt >= rate_limit_max_retries:
                    raise RuntimeError(
                        f"OpenAI network failure after retries: "
                        f"{e.__class__.__name__}") from e
                wait = rate_limit_base_backoff * (2 ** attempt)
                self.log(f"  OpenAI network error ({e.__class__.__name__}); "
                         f"retrying in {wait}s")
                time.sleep(wait)
                attempt += 1
                continue

            if resp.status_code in (429, 500, 502, 503, 504):
                if attempt >= rate_limit_max_retries:
                    raise RuntimeError(
                        f"OpenAI API {resp.status_code} after "
                        f"{rate_limit_max_retries} retries: {resp.text[:300]}")
                retry_after = resp.headers.get("retry-after")
                wait = (int(retry_after) if retry_after and retry_after.isdigit()
                        else rate_limit_base_backoff * (2 ** attempt))
                self.log(f"  OpenAI API {resp.status_code}; backing off {wait}s "
                         f"(attempt {attempt + 1}/{rate_limit_max_retries})")
                time.sleep(wait)
                attempt += 1
                continue

            if resp.status_code != 200:
                raise RuntimeError(
                    f"OpenAI API error {resp.status_code}: {resp.text[:500]}")

            data = resp.json()
            choices = data.get("choices") or []
            if not choices:
                raise ValueError("no choices in OpenAI response")
            text = (choices[0].get("message") or {}).get("content") or ""
            return parse_adjudicator_response(text)


class MockAdjudicatorClient:
    """Deterministic offline mock for GPT-5.4 adjudication. Used by mock mode."""

    def __init__(self, *_args, **_kwargs):
        pass

    def adjudicate(
        self,
        merged_context: dict,
        research_pack: dict,
        qa_warnings: list[str],
        unresolved_reasons: list[str],
        attempt_number: int,
        max_attempts: int,
        **_kwargs,
    ) -> dict:
        sv = merged_context.get("standard_variant") or {}
        vid = merged_context["validation_id"]
        trim = sv.get("trim")
        il_name = sv.get("official_marketed_name_il")

        # Deterministic mock logic based on input characteristics
        split_indicators = research_pack.get("split_indicators") or {}
        split_likely = split_indicators.get("split_likely", False)

        # Check for combined trims
        combined = False
        for sep in ("/", " or ", " & ", "|", ", "):
            if isinstance(trim, str) and sep in trim:
                combined = True
                break

        if combined or split_likely:
            decision = "split_required"
            confidence = 0.8
        elif trim is None or (isinstance(trim, str) and
                              trim.strip().lower() in {"", "base", "standard",
                                                       "unknown", "none", "null",
                                                       "n/a", "na"}):
            decision = "rejected_from_clean"
            confidence = 0.6
        else:
            decision = "auto_resolved"
            confidence = 0.9

        return {
            "validation_id": vid,
            "make": sv.get("make", ""),
            "model": sv.get("model", ""),
            "input_raw_trim_name": trim,
            "input_raw_official_marketed_name_il": il_name,
            "israeli_market_presence": {
                "status": "likely",
                "summary": "mock adjudication",
            },
            "recovered_identity": {
                "official_marketed_name_il": il_name,
                "official_marketed_name_en": None,
                "trim_name_il": trim if decision == "auto_resolved" else None,
                "trim_name_en": trim if decision == "auto_resolved" else None,
                "model_family": sv.get("model"),
                "confidence": confidence,
            },
            "trim_name_il_status": (
                "verified" if decision == "auto_resolved"
                else "generic_family_only" if decision == "split_required"
                else "not_available"
            ),
            "field_corrections": {
                "trim_name": {
                    "original": trim,
                    "corrected": trim if decision == "auto_resolved" else None,
                    "status": "unchanged" if decision == "auto_resolved" else "rejected",
                    "reason": "mock adjudication",
                },
                "official_marketed_name_il": {
                    "original": il_name,
                    "corrected": il_name,
                    "status": "unchanged",
                    "reason": "mock adjudication",
                },
            },
            "possible_israeli_trims_found": [],
            "split_review": {
                "split_recommended": decision == "split_required",
                "reason": ("combined trim detected" if combined
                           else "split indicated by research" if split_likely
                           else "no split needed"),
                "candidate_child_variants": (
                    [t.strip() for t in trim.split("/")]
                    if combined and isinstance(trim, str) else []
                ),
            },
            "evidence_items": [],
            "grounding_attempts": {
                "queries_used": [],
                "sources_checked": [],
                "no_source_found_for": [],
            },
            "adjudicator_notes": {
                "gemini_research_used": True,
                "gemini_research_limitations": [],
                "deterministic_source_normalization_applied": True,
                "qa_warnings_considered": qa_warnings,
            },
            "final_decision": decision,
            "final_confidence": confidence,
            "final_reason": f"mock adjudication: {decision}",
            "clean_database_action": {
                "insert_into_clean": decision == "auto_resolved",
                "create_split_tasks": decision == "split_required",
                "send_to_retry": False,
                "reject_reason": ("" if decision != "rejected_from_clean"
                                  else "mock: no unique mapping"),
            },
        }
