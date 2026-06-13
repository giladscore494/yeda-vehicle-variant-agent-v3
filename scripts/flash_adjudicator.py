"""Gemini Flash adjudication for narrow guard conflicts.

Flash is optional and disabled by default. It never performs full validation;
it only chooses among guard-specific allowed decisions. Deterministic guards are
run again after adjudication by the engine, so guards retain final authority.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Set

from .gemini_client import parse_strict_json
from .reconcile import GuardFlag


@dataclass
class FlashSettings:
    api_key: str
    model_id: str = "gemini-2.5-flash"
    enabled: bool = False
    max_retries: int = 1


_ALLOWED = {
    "slash_trim": {"split_required", "clean_partial"},
    "grounding_summary_vs_decision": {"split_required", "clean_partial"},
    "under_consideration": {"clean_exact", "clean_partial"},
    "domain_500c_transmission": {"clean_exact", "clean_partial"},
}
VALID_FLASH_DECISIONS = {"clean_exact", "clean_partial", "split_required"}


class FlashAdjudicator:
    def __init__(self, settings: FlashSettings, client: Any = None) -> None:
        self.settings = settings
        self._client = client

    def _ensure_client(self):
        if self._client is None:
            from google import genai
            self._client = genai.Client(api_key=self.settings.api_key)
        return self._client

    def _prompt(self, row: Dict[str, Any], flag: GuardFlag, allowed: Set[str]) -> str:
        sources = []
        for src in row.get("evidence_sources") or []:
            if isinstance(src, dict):
                sources.append({"source_name": src.get("source_name"), "source_type": src.get("source_type"), "title": src.get("title")})
        questions = {
            "slash_trim": "Should this slash/combined trim be split_required or clean_partial? Do not return clean_exact.",
            "grounding_summary_vs_decision": "Does the summary truly require split_required, or is clean_partial sufficient?",
            "under_consideration": "Is there explicit evidence of actual Israeli sale/import, or only expected/under consideration status? If there is no explicit evidence of actual Israeli sale/import/catalog/listing, return clean_partial.",
            "domain_500c_transmission": "Given the guard concern, should this stay clean_partial or can it be clean_exact? Do not return clean_exact unless the summary/evidence explicitly supports manual transmission for Israeli Abarth 500C/Cabriolet.",
        }
        payload = {
            "vehicle": {k: row.get(k) for k in ("canonical_make", "canonical_model", "canonical_trim", "body_type", "transmission")},
            "grounding_summary": row.get("grounding_summary"),
            "evidence_sources": sources,
            "guard_name": flag.guard_name,
            "guard_reason": flag.reason,
            "allowed_decisions": sorted(allowed),
            "question": questions.get(flag.guard_name, "Choose the best allowed decision."),
        }
        return "Return strict JSON only: {\"adjudicated_decision\": one allowed decision, \"reason\": one sentence}.\n" + json.dumps(payload, ensure_ascii=False, indent=2)

    def _generate(self, prompt: str) -> Dict[str, Any]:
        client = self._ensure_client()
        last = None
        for attempt in range(self.settings.max_retries + 1):
            try:
                resp = client.models.generate_content(model=self.settings.model_id, contents=prompt)
                return parse_strict_json(getattr(resp, "text", None))
            except Exception as exc:  # noqa: BLE001
                last = exc
                if attempt < self.settings.max_retries:
                    time.sleep(1)
        raise RuntimeError(f"Flash adjudication failed: {last}")

    def adjudicate(self, variant: Dict[str, Any], flags: List[GuardFlag]) -> Dict[str, Any]:
        row = dict(variant)
        log = list(row.get("adjudication_log") or [])
        for flag in flags:
            if not flag.needs_adjudication or flag.guard_name not in _ALLOWED:
                continue
            allowed = _ALLOWED[flag.guard_name]
            try:
                data = self._generate(self._prompt(row, flag, allowed))
                decision = data.get("adjudicated_decision")
                if decision not in allowed or decision not in VALID_FLASH_DECISIONS or decision == "reject":
                    raise ValueError("invalid Flash decision")
                old = row.get("validation_decision")
                row["validation_decision"] = decision
                log.append({"guard": flag.guard_name, "guard_changed_to": flag.new_decision, "flash_decided": decision, "flash_reason": data.get("reason") or ""})
                if old != decision and decision != flag.new_decision:
                    row["_flash_overrode_guard"] = int(row.get("_flash_overrode_guard") or 0) + 1
            except Exception as exc:  # guard decision stands
                log.append({"guard": flag.guard_name, "guard_changed_to": flag.new_decision, "flash_decided": row.get("validation_decision"), "flash_reason": f"Flash failed; guard decision stands: {exc}"})
        row["adjudication_log"] = log
        return row
