"""OpenAI guard-scoped verifier for Stage 3 adjudication.

This is intentionally narrow: it only reviews Python GuardFlag objects that
request adjudication and can only return an allowed decision/limited patch.
Final Python guards and routing remain authoritative.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Set

from .gemini_client import parse_strict_json
from .reconcile import GuardFlag

GUARD_VERIFIER_SYSTEM_PROMPT = """You are a guard-scoped verifier for an Israeli-market vehicle variant validation pipeline.

You are NOT the main validator.
You are NOT performing full vehicle validation.
You are NOT doing new research.
You are only reviewing a specific Python guard-flagged issue.

You receive:
- the specific guard or guards that fired
- the original model value before guard correction
- the Python guard-corrected value
- relevant vehicle fields only
- a short grounding summary
- compact evidence source summaries
- allowed decisions
- allowed patch fields

Your job:
1. Decide whether the Python guard correction should stand.
2. If the correction is too strong or too weak, choose the safest allowed correction.
3. Return strict JSON only.

Hard rules:
- Do not revalidate the whole vehicle.
- Do not introduce new evidence.
- Do not invent URLs.
- Do not invent sources.
- Do not add unsupported facts.
- Do not reveal chain-of-thought.
- Do not change fields outside allowed_patch_fields.
- Do not return decisions outside allowed_decisions.
- Do not convert weak/missing/generic trim into reject.
- If uncertain, choose the safer lower-confidence option.
- Prefer clean_partial over clean_exact when exact trim, market status, or technical identity is not fully verified.
- Prefer split_required when combined values represent multiple separate variants.
- Prefer review_queue when an identity-critical technical field remains unresolved.
- Final Python guards and routing will run after your answer and have final authority.

Return strict JSON only."""

VERIFIER_OUTPUT_KEYS = {"verdict", "selected_decision", "allowed_patch", "confidence", "reason", "safety_notes"}
VALID_VERDICTS = {"accept_guard", "modify_guard", "reject_guard"}
NEVER_PATCH_FIELDS = {
    "validation_id", "source_validation_id", "source_cluster_id", "grounding_cluster_id",
    "evidence_sources", "market_scope", "adjudication_log", "blocking_identity_issues",
    "non_blocking_trim_issues", "final_route", "publishable_to_clean_catalog",
    "duplicate_of", "duplicate_group_id",
}
RELEVANT_BY_FIELD = {
    "validation_decision": {"validation_decision", "identity_status", "identity_confidence", "trim_status", "trim_confidence", "fields_left_unresolved"},
    "canonical_trim": {"canonical_trim", "trim_status", "trim_confidence", "possible_trim_names", "split_candidates"},
    "year_start": {"year_start", "year_end", "is_currently_produced", "is_currently_imported_il", "market_scope"},
    "year_end": {"year_start", "year_end", "is_currently_produced", "is_currently_imported_il", "market_scope"},
    "is_currently_produced": {"year_end", "is_currently_produced", "is_currently_imported_il"},
    "is_currently_imported_il": {"year_end", "is_currently_produced", "is_currently_imported_il"},
    "identity_status": {"identity_status", "identity_confidence", "validation_decision", "fields_left_unresolved"},
    "transmission": {"transmission", "engine", "fuel_type", "body_type", "fields_left_unresolved", "validation_decision"},
}
BASE_RELEVANT_FIELDS = {"canonical_make", "canonical_model", "canonical_trim"}

@dataclass
class OpenAIGuardVerifierSettings:
    api_key: str
    model_id: str
    enabled: bool = False
    max_retries: int = 1

class OpenAIGuardVerifier:
    def __init__(self, settings: OpenAIGuardVerifierSettings, client: Any = None) -> None:
        self.settings = settings
        self._client = client
        self.calls = 0

    def _ensure_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.settings.api_key)
        return self._client

    @staticmethod
    def adjudication_flags(flags: List[GuardFlag]) -> List[GuardFlag]:
        return [f for f in flags if f.needs_adjudication and f.recommended_verifier_model == "gpt-5.4"]

    def build_payload(self, row: Dict[str, Any], flags: List[GuardFlag]) -> Dict[str, Any]:
        scoped = self.adjudication_flags(flags)
        relevant: Set[str] = set(BASE_RELEVANT_FIELDS)
        allowed_fields: Set[str] = set()
        allowed_decisions: Set[str] = set()
        for flag in scoped:
            relevant |= RELEVANT_BY_FIELD.get(flag.field_affected, {flag.field_affected})
            allowed_fields |= set(flag.allowed_patch_fields)
            allowed_decisions |= set(flag.allowed_decisions)
        relevant -= NEVER_PATCH_FIELDS
        sources = []
        for src in row.get("evidence_sources") or []:
            if isinstance(src, dict):
                sources.append({"source_name": src.get("source_name"), "source_type": src.get("source_type"), "supports": src.get("supports", [])})
        return {
            "validation_id": row.get("validation_id"),
            "guards": [
                {
                    "guard_name": f.guard_name,
                    "severity": f.severity,
                    "field_affected": f.field_affected,
                    "original_value": f.original_value,
                    "guard_value": f.guard_value,
                    "reason": f.reason,
                    "allowed_decisions": list(f.allowed_decisions),
                    "allowed_patch_fields": [x for x in f.allowed_patch_fields if x not in NEVER_PATCH_FIELDS],
                }
                for f in scoped
            ],
            "relevant_fields": {k: row.get(k) for k in sorted(relevant) if k in row},
            "grounding_summary": (row.get("grounding_summary") or "")[:800],
            "evidence_source_summaries": sources[:8],
            "allowed_decisions": sorted(allowed_decisions),
            "allowed_patch_fields": sorted(x for x in allowed_fields if x not in NEVER_PATCH_FIELDS),
        }

    def _generate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        client = self._ensure_client()
        content = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        last = None
        for attempt in range(self.settings.max_retries + 1):
            try:
                resp = client.responses.create(
                    model=self.settings.model_id,
                    input=[
                        {"role": "system", "content": GUARD_VERIFIER_SYSTEM_PROMPT},
                        {"role": "user", "content": content},
                    ],
                    response_format={"type": "json_object"},
                    max_completion_tokens=700,
                )
                text = getattr(resp, "output_text", None)
                if text is None and getattr(resp, "output", None):
                    parts = []
                    for item in resp.output:
                        for c in getattr(item, "content", []) or []:
                            if getattr(c, "text", None):
                                parts.append(c.text)
                    text = "".join(parts)
                return parse_strict_json(text)
            except TypeError:
                resp = client.responses.create(
                    model=self.settings.model_id,
                    input=[
                        {"role": "system", "content": GUARD_VERIFIER_SYSTEM_PROMPT},
                        {"role": "user", "content": content},
                    ],
                    response_format={"type": "json_object"},
                    max_tokens=700,
                )
                return parse_strict_json(getattr(resp, "output_text", None))
            except Exception as exc:  # noqa: BLE001
                last = exc
                if attempt < self.settings.max_retries:
                    time.sleep(1)
        raise RuntimeError(f"OpenAI guard verifier failed: {last}")

    @staticmethod
    def validate_response(data: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        if set(data) != VERIFIER_OUTPUT_KEYS:
            raise ValueError("guard verifier returned extra or missing keys")
        if data.get("verdict") not in VALID_VERDICTS:
            raise ValueError("invalid verdict")
        allowed_decisions = set(payload.get("allowed_decisions") or [])
        decision = data.get("selected_decision")
        if decision is not None and decision not in allowed_decisions:
            raise ValueError("forbidden selected_decision")
        try:
            conf = float(data.get("confidence"))
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid confidence") from exc
        if not 0.0 <= conf <= 1.0:
            raise ValueError("invalid confidence")
        patch = data.get("allowed_patch")
        if not isinstance(patch, dict):
            raise ValueError("allowed_patch must be object")
        allowed_fields = set(payload.get("allowed_patch_fields") or [])
        data["allowed_patch"] = {k: v for k, v in patch.items() if k in allowed_fields and k not in NEVER_PATCH_FIELDS}
        if not isinstance(data.get("reason"), str):
            raise ValueError("reason must be string")
        if not isinstance(data.get("safety_notes"), list):
            raise ValueError("safety_notes must be list")
        return data

    def adjudicate(self, row: Dict[str, Any], flags: List[GuardFlag], original_model_output: Dict[str, Any] | None = None) -> Dict[str, Any]:
        scoped = self.adjudication_flags(flags)
        out = dict(row)
        log = list(out.get("adjudication_log") or [])
        if not scoped or not self.settings.enabled:
            out["adjudication_log"] = log
            return out
        payload = self.build_payload(out, scoped)
        try:
            self.calls += 1
            data = self.validate_response(self._generate(payload), payload)
            before = out.get("validation_decision")
            for key, value in data["allowed_patch"].items():
                out[key] = value
            if data.get("selected_decision") and "validation_decision" in payload.get("allowed_patch_fields", []):
                out["validation_decision"] = data["selected_decision"]
            log.append({"guard_verifier": self.settings.model_id, "verdict": data["verdict"], "reason": data["reason"]})
            if out.get("validation_decision") != before:
                out["_guard_verifier_overrode_guard"] = int(out.get("_guard_verifier_overrode_guard") or 0) + 1
        except Exception as exc:  # keep Python guard correction
            log.append({"guard_verifier": self.settings.model_id, "verdict": "invalid_or_failed", "reason": f"Guard verifier failed; Python guard correction stands: {exc}"})
        out["adjudication_log"] = log
        return out
