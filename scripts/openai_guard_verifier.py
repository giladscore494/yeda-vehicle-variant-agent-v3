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

from pydantic import BaseModel, ConfigDict, Field

from .gemini_client import parse_strict_json
from .reconcile import GuardFlag

GUARD_VERIFIER_SYSTEM_PROMPT = """You are a guard-scoped verifier for an Israeli-market vehicle variant validation pipeline.

You are NOT the main validator.
You are NOT doing new research.
You are NOT validating the entire vehicle from scratch.
You are only reviewing the specific Python guard-flagged issue(s) provided.

You receive the guard(s) that fired, original Stage 1 values for affected fields, Python-guarded values, relevant vehicle fields only, a short grounding summary, compact evidence source summaries, allowed decisions, and allowed patch fields.

Your job:
1. Decide whether the Python guard correction should stand.
2. If it is too strong or too weak, choose the safest allowed correction.
3. If audit text contradicts final fields, require the text/fields to be aligned.
4. Return strict JSON only.

Return exactly this JSON object with no markdown, no extra keys, and no chain-of-thought:
{"verdict":"accept_guard|modify_guard|reject_guard","selected_decision":null,"allowed_patch":{},"confidence":0.0,"reason":"One short sentence.","safety_notes":[]}

Hard rules:
- Do not revalidate the whole row.
- Do not introduce new evidence.
- Do not invent URLs.
- Do not invent sources.
- Do not add unsupported facts.
- Do not reveal chain-of-thought.
- Do not patch fields outside allowed_patch_fields.
- Do not return decisions outside allowed_decisions.
- Do not directly set routing fields unless routing fields are explicitly included in allowed_patch_fields.
- Prefer lower-confidence output when evidence is ambiguous.
- Prefer review_queue when an identity-critical technical field remains unresolved.
- Prefer split_required when combined values represent multiple separate variants.
- Weak/missing/generic trim alone is not a reject reason.
- A split-required trim issue is not an identity contradiction unless a true identity conflict also exists.
- Final Python guards and routing will run after your answer and have final authority.
- Return strict JSON only."""

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
    "year_start": {"year_start", "year_end", "is_currently_produced", "is_currently_imported_il"},
    "year_end": {"year_start", "year_end", "is_currently_produced", "is_currently_imported_il"},
    "is_currently_produced": {"year_end", "is_currently_produced", "is_currently_imported_il"},
    "is_currently_imported_il": {"year_end", "is_currently_produced", "is_currently_imported_il"},
    "identity_status": {"identity_status", "identity_confidence", "validation_decision", "fields_left_unresolved"},
    "transmission": {"transmission", "engine", "fuel_type", "body_type", "fields_left_unresolved", "validation_decision"},
}
BASE_RELEVANT_FIELDS = {"canonical_make", "canonical_model", "canonical_trim"}

class VerifierOutputModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    verdict: str
    selected_decision: str | None = None
    allowed_patch: Dict[str, Any] = Field(default_factory=dict)
    confidence: float
    reason: str
    safety_notes: List[Any] = Field(default_factory=list)

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
        self.successes = 0
        self.failures = 0
        self.last_error: str | None = None

    def _ensure_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.settings.api_key)
        return self._client

    @staticmethod
    def adjudication_flags(flags: List[GuardFlag]) -> List[GuardFlag]:
        return [f for f in flags if f.needs_adjudication and f.recommended_verifier_model == "gpt-5.4"]

    def build_payload(self, row: Dict[str, Any], flags: List[GuardFlag], original_model_output: Dict[str, Any] | None = None) -> Dict[str, Any]:
        scoped = self.adjudication_flags(flags)
        relevant: Set[str] = set(BASE_RELEVANT_FIELDS)
        allowed_fields: Set[str] = set()
        allowed_decisions: Set[str] = set()
        high_or_critical = any(f.severity in {"high", "critical"} for f in scoped)
        for flag in scoped:
            relevant |= RELEVANT_BY_FIELD.get(flag.field_affected, {flag.field_affected})
            allowed_fields |= set(flag.allowed_patch_fields)
            allowed_decisions |= set(flag.allowed_decisions)
        relevant -= NEVER_PATCH_FIELDS
        sources = []
        for src in row.get("evidence_sources") or []:
            if isinstance(src, dict):
                sources.append({"source_name": src.get("source_name"), "source_type": src.get("source_type"), "supports": src.get("supports", [])})
        guards = [{
            "guard_name": f.guard_name, "severity": f.severity, "field_affected": f.field_affected,
            "original_value": f.original_value, "guard_value": f.guard_value, "reason": f.reason,
            "risk_tags": list(getattr(f, "risk_tags", []) or []),
            "allowed_decisions": list(f.allowed_decisions),
            "allowed_patch_fields": [x for x in f.allowed_patch_fields if x not in NEVER_PATCH_FIELDS],
        } for f in scoped]
        allowed_patch_fields = sorted(x for x in allowed_fields if x not in NEVER_PATCH_FIELDS)
        base = {
            "validation_id": row.get("validation_id"),
            "guards": guards,
            "grounding_summary": (row.get("grounding_summary") or "")[:500],
            "evidence_source_summaries": sources[:8],
            "allowed_decisions": sorted(allowed_decisions),
            "allowed_patch_fields": allowed_patch_fields,
        }
        if not high_or_critical:
            base["payload_mode"] = "standard_guard_payload"
            base["relevant_fields"] = {k: row.get(k) for k in sorted(relevant) if k in row}
            return base
        original = original_model_output or {}
        keys = ("validation_decision", "identity_status", "identity_confidence", "trim_status", "trim_confidence", "year_start", "year_end", "is_currently_produced", "is_currently_imported_il", "fields_left_unresolved", "decision_reason")
        guarded_keys = ("validation_decision", "identity_status", "identity_confidence", "trim_status", "trim_confidence", "year_start", "year_end", "is_currently_produced", "is_currently_imported_il", "fields_left_unresolved", "guard_corrected_reason", "final_route", "publishable_to_clean_catalog")
        base["relevant_fields"] = {k: row.get(k) for k in sorted(relevant) if k in row}
        base.update({
            "payload_mode": "strict_guard_payload",
            "original_stage1_values": {k: original.get(k) for k in keys},
            "guarded_values": {k: row.get(k) for k in guarded_keys},
            "relevant_vehicle_fields": {k: row.get(k) for k in ("canonical_make", "canonical_model", "canonical_trim", "body_type", "fuel_type", "engine", "transmission", "drivetrain", "market_scope")},
            "decision_reason": row.get("decision_reason"),
            "relevant_issues": {"blocking_identity_issues": row.get("blocking_identity_issues") or [], "non_blocking_trim_issues": row.get("non_blocking_trim_issues") or []},
        })
        return base

    @staticmethod
    def _extract_text(resp: Any) -> str | None:
        text = getattr(resp, "output_text", None)
        if text is not None:
            return text
        parsed = getattr(resp, "output_parsed", None)
        if parsed is not None:
            if hasattr(parsed, "model_dump"):
                return json.dumps(parsed.model_dump(), ensure_ascii=False)
            if isinstance(parsed, dict):
                return json.dumps(parsed, ensure_ascii=False)
        parts = []
        for item in getattr(resp, "output", []) or []:
            for c in getattr(item, "content", []) or []:
                if getattr(c, "text", None):
                    parts.append(c.text)
        return "".join(parts) if parts else None

    def _input(self, content: str):
        return [{"role": "system", "content": GUARD_VERIFIER_SYSTEM_PROMPT}, {"role": "user", "content": content}]

    def _generate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        client = self._ensure_client()
        content = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        schema = VerifierOutputModel.model_json_schema()
        failures: List[str] = []
        attempts = ["responses.parse", "responses.create.text_schema", "responses.create.plain_json"]
        for method in attempts:
            try:
                if method == "responses.parse":
                    parse = getattr(client.responses, "parse", None)
                    if parse is None:
                        raise TypeError("responses.parse unavailable")
                    resp = parse(model=self.settings.model_id, input=self._input(content), text_format=VerifierOutputModel, max_output_tokens=700)
                    parsed = getattr(resp, "output_parsed", None)
                    if parsed is not None:
                        return parsed.model_dump() if hasattr(parsed, "model_dump") else dict(parsed)
                    return parse_strict_json(self._extract_text(resp))
                if method == "responses.create.text_schema":
                    resp = client.responses.create(
                        model=self.settings.model_id,
                        input=self._input(content),
                        text={"format": {"type": "json_schema", "name": "guard_verifier_output", "schema": schema, "strict": True}},
                        max_output_tokens=700,
                    )
                    return parse_strict_json(self._extract_text(resp))
                json_prompt = content + "\nReturn JSON only matching the required schema."
                resp = client.responses.create(model=self.settings.model_id, input=self._input(json_prompt), max_output_tokens=700)
                return parse_strict_json(self._extract_text(resp))
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{method} failed: {exc}")
                continue
        raise RuntimeError("OpenAI guard verifier failed; " + " | ".join(failures))

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
        conf = float(data.get("confidence"))
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
        out["_guard_verifier_success"] = False
        out["_guard_verifier_error"] = None
        if not scoped or not self.settings.enabled:
            out["adjudication_log"] = log
            return out
        payload = self.build_payload(out, scoped, original_model_output=original_model_output)
        try:
            self.calls += 1
            data = self.validate_response(self._generate(payload), payload)
            self.successes += 1
            self.last_error = None
            before = out.get("validation_decision")
            for key, value in data["allowed_patch"].items():
                out[key] = value
            if data.get("selected_decision") and "validation_decision" in payload.get("allowed_patch_fields", []):
                out["validation_decision"] = data["selected_decision"]
            log.append({"guard_verifier": self.settings.model_id, "verdict": data["verdict"], "reason": data["reason"]})
            out["_guard_verifier_success"] = True
            if out.get("validation_decision") != before:
                out["_guard_verifier_overrode_guard"] = int(out.get("_guard_verifier_overrode_guard") or 0) + 1
        except Exception as exc:  # keep Python guard correction
            self.failures += 1
            self.last_error = str(exc)
            out["_guard_verifier_error"] = str(exc)
            log.append({"guard_verifier": self.settings.model_id, "verdict": "invalid_or_failed", "reason": f"Guard verifier failed; Python guard correction stands: {exc}"})
        out["adjudication_log"] = log
        return out
