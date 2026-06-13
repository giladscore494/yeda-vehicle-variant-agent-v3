"""Gemini Flash adjudication for narrow guard conflicts.

Flash is optional and disabled by default. It never performs full validation;
it only chooses among guard-specific allowed decisions/patches. Deterministic
Python guards are run again after adjudication by the engine, so guards retain
final authority. Flash uses the same Google/Gemini API key supplied for Pro.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Set

from .gemini_client import parse_strict_json
from .reconcile import GuardFlag

FLASH_SYSTEM_PROMPT = """You are a narrow vehicle-validation adjudicator.

You are NOT the main validator.
You are NOT doing a full vehicle validation.
You are only adjudicating a specific Python-guard-flagged conflict in an Israeli vehicle variant validation pipeline.

You receive:
- original model output
- Python-guard-corrected output
- guard flags
- a short grounding summary
- limited relevant fields
- allowed outputs for this issue

Your job:
1. Decide whether the Python guard correction should stand.
2. If it is too strong or too weak, choose the safest allowed correction.
3. Return strict JSON only.

Hard rules:
- Do not invent URLs.
- Do not invent new sources.
- Do not add unsupported facts.
- Do not reveal hidden reasoning or chain-of-thought.
- Do not perform broad revalidation.
- Do not override deterministic schema rules.
- Do not convert weak/missing/generic trim into reject.
- Do not return clean_exact unless the evidence clearly verifies Israeli sale/import, exact trim, and key technical fields.
- If uncertain, prefer clean_partial over clean_exact.
- If a combined/slash trim represents multiple distinct trims, prefer split_required.
- If Israeli market sale is only expected/under consideration, prefer clean_partial.
- If a transmission is disputed for the Israeli market, prefer clean_partial with lower identity confidence.

Return strict JSON only."""

ALLOWED_FLASH_PATCH_FIELDS = {
    "validation_decision", "acceptance_tier", "identity_status", "identity_confidence",
    "trim_status", "trim_confidence", "canonical_trim", "year_start", "year_end",
    "is_currently_produced", "is_currently_imported_il",
}
_FORBIDDEN_PATCH_FIELDS = {"engine", "transmission", "drivetrain", "fuel_type", "body_type", "market_scope", "evidence_sources"}
_ALLOWED = {
    "slash_trim": {"split_required", "clean_partial"},
    "grounding_summary_vs_decision": {"split_required", "clean_partial"},
    "under_consideration": {"clean_exact", "clean_partial"},
    "domain_500c_transmission": {"clean_exact", "clean_partial"},
    "year_start_il_market": {"clean_partial", "clean_exact"},
}
VALID_FLASH_DECISIONS = {"clean_exact", "clean_partial", "split_required"}

@dataclass
class FlashSettings:
    api_key: str
    model_id: str = "gemini-2.5-flash"
    enabled: bool = False
    max_retries: int = 1

class FlashAdjudicator:
    def __init__(self, settings: FlashSettings, client: Any = None) -> None:
        self.settings = settings
        self._client = client

    def _ensure_client(self):
        if self._client is None:
            from google import genai
            self._client = genai.Client(api_key=self.settings.api_key)
        return self._client

    def _prompt(self, original: Dict[str, Any], guarded: Dict[str, Any], flag: GuardFlag, allowed: Set[str]) -> str:
        questions = {
            "slash_trim": "Does this combined trim represent multiple distinct variants that must be split, or only a vague candidate list? Forbidden: clean_exact, reject.",
            "grounding_summary_vs_decision": "Does the grounding summary clearly require split_required or downgrade from clean_exact?",
            "under_consideration": "Is there explicit evidence of actual Israeli sale/import/catalog/listing, or only expected/under-consideration status? If uncertain, choose clean_partial.",
            "domain_500c_transmission": "Does the evidence explicitly support manual transmission for Israeli Abarth 500C/Cabriolet, or should this stay partially verified? If ambiguous, choose clean_partial.",
            "year_start_il_market": "Should year_start represent Israeli-market start year or global launch year for this Israeli-market database row? Only patch if clear.",
        }
        sources = [{"source_name": s.get("source_name"), "source_type": s.get("source_type"), "supports": s.get("supports", [])} for s in guarded.get("evidence_sources") or [] if isinstance(s, dict)]
        payload = {
            "validation_id": guarded.get("validation_id"),
            "guard_flags": [{"guard_name": flag.guard_name, "field_affected": flag.field_affected, "original_value": flag.original_decision, "guard_value": flag.new_decision, "reason": flag.reason}],
            "original_model_output": {k: original.get(k) for k in ("validation_decision", "canonical_trim", "trim_status", "identity_status", "identity_confidence", "decision_reason")},
            "guarded_output": {k: guarded.get(k) for k in ("validation_decision", "canonical_trim", "trim_status", "identity_status", "identity_confidence", "guard_corrected_reason", "year_start", "year_end")},
            "relevant_vehicle_fields": {k: guarded.get(k) for k in ("canonical_make", "canonical_model", "body_type", "engine", "transmission", "year_start", "year_end", "market_scope")},
            "grounding_summary": guarded.get("grounding_summary"),
            "evidence_source_summaries": sources,
            "allowed_outputs": {"validation_decision": sorted(allowed), "identity_status": ["verified", "likely_valid", "uncertain"], "trim_status": ["unresolved", "invalid"]},
            "question": questions.get(flag.guard_name, "Choose the safest allowed correction."),
            "required_schema": {"guard_correction_verdict": "accept_guard|modify_guard|reject_guard", "adjudicated_decision": "clean_exact|clean_partial|split_required", "adjudicated_identity_status": "verified|likely_valid|uncertain|invalid|unchanged", "adjudicated_trim_status": "verified|inferred|unresolved|invalid|unchanged", "confidence_adjustment": {"identity_confidence": None, "trim_confidence": None}, "allowed_patch": {k: None for k in sorted(ALLOWED_FLASH_PATCH_FIELDS)}, "reason": "One short sentence.", "safety_notes": []},
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def _generate(self, prompt: str) -> Dict[str, Any]:
        client = self._ensure_client()
        last = None
        for attempt in range(self.settings.max_retries + 1):
            try:
                resp = client.models.generate_content(model=self.settings.model_id, contents=prompt, config={"system_instruction": FLASH_SYSTEM_PROMPT})
                return parse_strict_json(getattr(resp, "text", None))
            except Exception as exc:  # noqa: BLE001
                last = exc
                if attempt < self.settings.max_retries:
                    time.sleep(1)
        raise RuntimeError(f"Flash adjudication failed: {last}")

    def adjudicate(self, variant: Dict[str, Any], flags: List[GuardFlag], original_model_output: Dict[str, Any] | None = None) -> Dict[str, Any]:
        row = dict(variant)
        original = dict(original_model_output or variant)
        log = list(row.get("adjudication_log") or [])
        for flag in flags:
            if not flag.needs_adjudication or flag.guard_name not in _ALLOWED:
                continue
            allowed = _ALLOWED[flag.guard_name]
            try:
                data = self._generate(self._prompt(original, row, flag, allowed))
                decision = data.get("adjudicated_decision")
                patch = data.get("allowed_patch") if isinstance(data.get("allowed_patch"), dict) else {}
                if decision not in allowed or decision not in VALID_FLASH_DECISIONS or decision == "reject":
                    raise ValueError("invalid Flash decision")
                for forbidden in _FORBIDDEN_PATCH_FIELDS:
                    patch.pop(forbidden, None)
                for key, value in patch.items():
                    if key in ALLOWED_FLASH_PATCH_FIELDS and value is not None:
                        row[key] = value
                if not patch.get("validation_decision"):
                    row["validation_decision"] = decision
                log.append({"guard": flag.guard_name, "guard_changed_to": flag.new_decision, "flash_decided": row.get("validation_decision"), "flash_reason": data.get("reason") or ""})
                if row.get("validation_decision") != flag.new_decision:
                    row["_flash_overrode_guard"] = int(row.get("_flash_overrode_guard") or 0) + 1
            except Exception as exc:  # guard decision stands
                log.append({"guard": flag.guard_name, "guard_changed_to": flag.new_decision, "flash_decided": row.get("validation_decision"), "flash_reason": f"Flash failed; guard decision stands: {exc}"})
        row["adjudication_log"] = log
        return row
