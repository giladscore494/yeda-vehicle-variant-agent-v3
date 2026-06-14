"""GPT-5.4 grounded repair adjudicator.

Legacy guard verifier returns guard verdicts. This adjudicator asks GPT-5.4 for a
complete repaired row and then relies on Python final seal as the publisher.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .gemini_client import parse_strict_json

REPAIR_ADJUDICATOR_SYSTEM_PROMPT = """You are the final grounded repair adjudicator for an Israeli-market vehicle variant validation pipeline.

You must use web grounding / search if available.
You must not rely only on memory.
You must not invent facts.
You must not invent sources.
You must not add URLs unless they came from grounding/search/evidence payload.
You must return a complete repaired JSON row.

Your role is not to decide whether guards are correct.
Your role is to repair the full row so that:
- fields
- statuses
- confidence
- summaries
- issues
- source support
- grounding status
- final route
are all internally consistent.

If a field is not verified, it cannot remain verified.
If a field is unresolved, it must be listed as unresolved.
If a row is partial, it cannot enter clean_catalog.
If trim is null/unresolved, it cannot enter clean_catalog.
If grounding is missing/weak, it cannot enter clean_catalog.
If current import/production is not grounded, do not claim it in summary.

Return strict JSON only."""

KNOWN_FAILURE_EXAMPLES = [
    "unresolved transmission text but transmission field still populated",
    "summary claims current sale/import while current flags are null/false",
    "clean_partial with null trim routed to clean_catalog",
    "body style accepted as trim",
    "combined trim accepted as one canonical trim",
]


REQUIRED_RESPONSE_KEYS = (
    "repair_decision",
    "patched_variant",
    "field_patches",
    "summary_patch",
    "routing_patch",
    "grounding_patch",
    "remaining_uncertainties",
    "confidence",
)


@dataclass
class OpenAIRepairAdjudicatorSettings:
    api_key: str
    model_id: str = "gpt-5.4"
    enabled: bool = True
    grounding_required: bool = True
    use_web_search: bool = True
    max_completion_tokens: int = 6000


class OpenAIRepairAdjudicator:
    def __init__(self, settings: OpenAIRepairAdjudicatorSettings) -> None:
        self.settings = settings
        self.calls = 0
        self._client = None

    def _ensure_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.settings.api_key)
        return self._client

    def build_payload(self, *, raw_input_variant: Dict[str, Any], original_gemini_output: Dict[str, Any], guarded_output: Dict[str, Any], guard_flags: List[Any], risk_score: int, preflight_risk_tags: List[str], external_search_results_for_gpt54: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        return {
            "raw_input_variant": raw_input_variant or {},
            "original_gemini_output": original_gemini_output or {},
            "guarded_output": guarded_output or {},
            "guard_flags": [f if isinstance(f, dict) else getattr(f, "__dict__", str(f)) for f in guard_flags or []],
            "risk_score": risk_score,
            "preflight_risk_tags": preflight_risk_tags or [],
            "field_validation": guarded_output.get("field_validation", {}),
            "source_support_matrix": guarded_output.get("source_support_matrix", []),
            "evidence_sources": guarded_output.get("evidence_sources", []),
            "gemini_grounding_metadata": guarded_output.get("gemini_grounding_metadata") or guarded_output.get("grounding_metadata") or {},
            "external_search_results_for_gpt54": external_search_results_for_gpt54 or [],
            "routing_policy": {"clean_partial_never_clean_catalog": True, "split_required_route": "split_queue", "duplicate_route": "duplicate_queue"},
            "clean_catalog_policy": {"requires_clean_exact": True, "requires_verified_identity_trim": True, "requires_grounding_gate": True, "requires_no_unresolved_critical": True},
            "schema": "patched_variant must be complete output row with grounding_status, field_validation, source_support_matrix, evidence_auditability, routing fields.",
            "known_failure_examples": KNOWN_FAILURE_EXAMPLES,
        }

    def adjudicate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.settings.enabled:
            raise RuntimeError("repair adjudicator disabled")
        if not self.settings.api_key:
            raise RuntimeError("OpenAI API key missing")
        if self.settings.grounding_required and not payload.get("external_search_results_for_gpt54") and not payload.get("evidence_sources"):
            raise RuntimeError("GPT-5.4 grounding required but no evidence/search payload was supplied")
        client = self._ensure_client()
        self.calls += 1
        schema = {
            "type": "object",
            "additionalProperties": True,
            "required": ["repair_decision", "patched_variant", "field_patches", "summary_patch", "routing_patch", "grounding_patch", "remaining_uncertainties", "blocking_issues_after_repair", "non_blocking_issues_after_repair", "confidence"],
            "properties": {
                "repair_decision": {"type": "string", "enum": ["no_change", "patched", "review_required", "split_required", "reject_required"]},
                "patched_variant": {"type": "object", "additionalProperties": True},
                "field_patches": {"type": "array", "items": {"type": "object", "additionalProperties": True}},
                "summary_patch": {"type": "object", "additionalProperties": True},
                "routing_patch": {"type": "object", "additionalProperties": True},
                "grounding_patch": {"type": "object", "additionalProperties": True},
                "remaining_uncertainties": {"type": "array"},
                "blocking_issues_after_repair": {"type": "array"},
                "non_blocking_issues_after_repair": {"type": "array"},
                "confidence": {"type": "number"},
            },
        }
        kwargs = {
            "model": self.settings.model_id,
            "input": [
                {"role": "system", "content": REPAIR_ADJUDICATOR_SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
            "max_output_tokens": self.settings.max_completion_tokens,
            "text": {"format": {"type": "json_schema", "name": "repair_adjudicator_output", "schema": schema, "strict": False}},
        }
        web_search_used = False
        if self.settings.use_web_search:
            kwargs["tools"] = [{"type": "web_search_preview"}]
            web_search_used = True
        try:
            resp = client.responses.create(**kwargs)
        except Exception as exc:  # web search may be unsupported for this model/env
            if web_search_used:
                # Retry without the tool. Without grounding the repair cannot
                # unlock clean_catalog; the final seal enforces that.
                kwargs.pop("tools", None)
                web_search_used = False
                resp = client.responses.create(**kwargs)
            else:
                raise RuntimeError(f"repair adjudicator API call failed: {exc}") from exc

        text = getattr(resp, "output_text", None)
        if not text:
            parts: List[str] = []
            for item in getattr(resp, "output", []) or []:
                for c in getattr(item, "content", []) or []:
                    if getattr(c, "text", None):
                        parts.append(c.text)
            text = "\n".join(parts)
        result = parse_strict_json(text)
        if not isinstance(result, dict):
            raise RuntimeError("Repair adjudicator returned non-object JSON")
        missing = [k for k in REQUIRED_RESPONSE_KEYS if k not in result]
        if missing:
            raise RuntimeError(f"Repair adjudicator returned invalid schema; missing: {missing}")
        if not isinstance(result.get("patched_variant"), dict) or not result["patched_variant"]:
            raise RuntimeError("Repair adjudicator returned empty/invalid patched_variant")
        # Record whether GPT-5.4 grounding is present so the final seal can keep
        # ungrounded repairs out of the clean catalog.
        grounding_patch = result.get("grounding_patch") if isinstance(result.get("grounding_patch"), dict) else {}
        gpt_present = bool(
            web_search_used
            or grounding_patch.get("gpt54_grounding_present")
            or grounding_patch.get("gpt54_grounding_assessment")
            or result.get("gpt54_citations")
            or result.get("gpt54_grounding_metadata")
        )
        result["_gpt54_grounding_present"] = gpt_present
        result["_web_search_used"] = web_search_used
        patched = result["patched_variant"]
        if isinstance(patched, dict):
            patched["gpt54_grounding_present"] = gpt_present
            existing_status = patched.get("grounding_status") if isinstance(patched.get("grounding_status"), dict) else {}
            existing_status["gpt54_grounding_present"] = gpt_present
            if not gpt_present:
                existing_status["gpt54_grounding_quality"] = "missing"
            patched["grounding_status"] = existing_status
        return result
