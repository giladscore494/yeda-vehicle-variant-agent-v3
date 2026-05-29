"""Decision resolver — merges Gemini and OpenAI results into final decisions.

Implements the validation status rules:
- trusted_existing_deterministic: low risk, no model call needed
- verified_by_gemini: non-critical, strong evidence from Gemini
- verified_by_dual_model: both models agree
- partial_needs_evidence: weak evidence, not promoted
- manual_review: model disagreement or weak sources
- rejected_no_il_market: no Israeli market evidence
- pending_unchecked: not yet validated
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def resolve_variant_decision(
    variant_id: str,
    risk_level: str,
    gemini_result: dict | None,
    openai_result: dict | None,
) -> dict:
    """Resolve final validation decision for a single variant.

    Returns a decision dict with: validation_status, confidence, quality_flags,
    trim_action, corrected_trim, source_refs, model_audit_refs, reason.
    """
    # Low risk — deterministic trust
    if risk_level == "low" and gemini_result is None and openai_result is None:
        return {
            "validation_status": "trusted_existing_deterministic",
            "validation_confidence": "high",
            "quality_flags": [],
            "trim_action": "keep",
            "corrected_trim": None,
            "source_refs": [],
            "model_audit_refs": [],
            "reason": "Low risk — trusted without model validation",
        }

    g = _find_variant_in_result(variant_id, gemini_result, "validation_results")
    o = _find_variant_in_result(variant_id, openai_result, "review_results")

    # No model results at all
    if g is None and o is None:
        return {
            "validation_status": "pending_unchecked",
            "validation_confidence": "low",
            "quality_flags": ["no_model_response"],
            "trim_action": "keep",
            "corrected_trim": None,
            "source_refs": [],
            "model_audit_refs": [],
            "reason": "No model response received",
        }

    # Gemini only (medium risk)
    if g is not None and o is None:
        return _resolve_gemini_only(g)

    # Both models available
    if g is not None and o is not None:
        return _resolve_dual_model(g, o)

    # OpenAI only (unusual)
    if o is not None:
        return _resolve_single_model(o, "openai")

    return {
        "validation_status": "pending_unchecked",
        "validation_confidence": "low",
        "quality_flags": ["resolution_error"],
        "trim_action": "keep",
        "corrected_trim": None,
        "source_refs": [],
        "model_audit_refs": [],
        "reason": "Unexpected resolution state",
    }


def _find_variant_in_result(
    variant_id: str, result: dict | None, results_key: str
) -> dict | None:
    """Find a variant's result in a model response."""
    if result is None:
        return None
    results = result.get(results_key, [])
    for r in results:
        if r.get("variant_id") == variant_id:
            return r
    # If single variant in group, return first result
    if len(results) == 1:
        return results[0]
    return None


def _resolve_gemini_only(g: dict) -> dict:
    """Resolve using Gemini result only."""
    action = g.get("action", "keep")
    confidence = g.get("confidence", "medium")
    source_refs = g.get("source_refs", [])
    trim_exists = g.get("trim_exists_in_il")
    trim_official = g.get("trim_is_official")

    quality_flags = []
    if not source_refs:
        quality_flags.append("no_source_refs_from_model")
    if trim_exists is False:
        quality_flags.append("trim_not_found_in_il_market")
    if trim_official is False:
        quality_flags.append("trim_not_official")

    # Determine validation status
    if action == "keep" and confidence == "high" and source_refs:
        status = "verified_by_gemini"
    elif action == "correct" and source_refs:
        status = "verified_by_gemini"
        quality_flags.append("trim_corrected")
    elif action == "nullify":
        status = "partial_needs_evidence"
        quality_flags.append("trim_nullified")
    elif action == "manual_review":
        status = "manual_review"
    else:
        status = "partial_needs_evidence"

    # Don't verify without sources
    if status == "verified_by_gemini" and not source_refs:
        status = "partial_needs_evidence"
        quality_flags.append("grounding_unavailable")

    return {
        "validation_status": status,
        "validation_confidence": confidence,
        "quality_flags": quality_flags,
        "trim_action": action,
        "corrected_trim": g.get("suggested_correction"),
        "source_refs": source_refs,
        "model_audit_refs": [{"provider": "gemini", "result": g}],
        "reason": g.get("reason", ""),
    }


def _resolve_dual_model(g: dict, o: dict) -> dict:
    """Resolve using both Gemini and OpenAI results."""
    g_action = g.get("action", "keep")
    o_action = o.get("action", "keep")
    g_confidence = g.get("confidence", "medium")
    o_confidence = o.get("confidence", "medium")
    g_sources = g.get("source_refs", [])
    o_sources = o.get("source_refs", [])
    all_sources = list(set(g_sources + o_sources))
    agrees = o.get("agrees_with_primary", None)

    quality_flags = []
    model_audit_refs = [
        {"provider": "gemini", "result": g},
        {"provider": "openai", "result": o},
    ]

    # Models agree
    if g_action == o_action or agrees is True:
        action = g_action
        confidence = "high" if g_confidence == "high" or o_confidence == "high" else "medium"

        if action == "keep" and all_sources:
            status = "verified_by_dual_model"
        elif action == "correct" and all_sources:
            status = "verified_by_dual_model"
            quality_flags.append("trim_corrected")
        elif action == "nullify":
            status = "partial_needs_evidence"
            quality_flags.append("trim_nullified")
        elif action == "manual_review":
            status = "manual_review"
        else:
            status = "verified_by_dual_model" if all_sources else "partial_needs_evidence"

        corrected = g.get("suggested_correction") or o.get("suggested_correction")
        reason = f"Dual model agreement: {g.get('reason', '')} | {o.get('reason', '')}"

    else:
        # Models disagree
        quality_flags.append("model_disagreement")
        status = "manual_review"
        action = "manual_review"
        confidence = "low"
        corrected = None
        reason = (
            f"Model disagreement — Gemini: {g_action} ({g.get('reason', '')}), "
            f"OpenAI: {o_action} ({o.get('reason', '')})"
        )

    # Don't verify without sources
    if "verified" in status and not all_sources:
        status = "partial_needs_evidence"
        quality_flags.append("no_source_evidence")

    return {
        "validation_status": status,
        "validation_confidence": confidence,
        "quality_flags": quality_flags,
        "trim_action": action,
        "corrected_trim": corrected,
        "source_refs": all_sources,
        "model_audit_refs": model_audit_refs,
        "reason": reason,
    }


def _resolve_single_model(result: dict, provider: str) -> dict:
    """Resolve using a single model result."""
    action = result.get("action", "keep")
    confidence = result.get("confidence", "medium")
    source_refs = result.get("source_refs", [])
    quality_flags = []

    if action == "keep" and confidence == "high" and source_refs:
        status = f"verified_by_{provider}"
    elif action == "manual_review":
        status = "manual_review"
    else:
        status = "partial_needs_evidence"

    return {
        "validation_status": status,
        "validation_confidence": confidence,
        "quality_flags": quality_flags,
        "trim_action": action,
        "corrected_trim": result.get("suggested_correction"),
        "source_refs": source_refs,
        "model_audit_refs": [{"provider": provider, "result": result}],
        "reason": result.get("reason", ""),
    }


class AuditWriter:
    """Writes audit entries to validation_audit.jsonl and trim_corrections.json."""

    def __init__(self, output_dir: str | Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.audit_path = self.output_dir / "validation_audit.jsonl"
        self.corrections_path = self.output_dir / "trim_corrections.json"
        self._corrections: list[dict] = []

    def log_decision(
        self,
        variant: dict,
        group_key: str,
        decision: dict,
        original_status: str,
    ) -> None:
        """Log a validation decision to the audit trail."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "variant_id": variant.get("variant_id", ""),
            "group_key": group_key,
            "original_status": original_status,
            "new_validation_status": decision["validation_status"],
            "decision": decision["trim_action"],
            "confidence": decision["validation_confidence"],
            "source_refs": decision["source_refs"],
            "model_audit_refs": [
                {k: v for k, v in ref.items() if k != "result"}
                for ref in decision.get("model_audit_refs", [])
            ],
            "quality_flags": decision["quality_flags"],
            "reason": decision["reason"],
        }
        with open(self.audit_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        # Track trim corrections
        if decision["trim_action"] == "correct" and decision.get("corrected_trim"):
            from engine.validation.normalizer import safe_str_original

            correction = {
                "variant_id": variant.get("variant_id", ""),
                "make": safe_str_original(variant.get("make")),
                "model": safe_str_original(variant.get("model")),
                "original_trim": safe_str_original(variant.get("trim")),
                "corrected_trim": decision["corrected_trim"],
                "action": "correct",
                "confidence": decision["validation_confidence"],
                "source_refs": decision["source_refs"],
                "approved_by": [
                    ref.get("provider") for ref in decision.get("model_audit_refs", [])
                ],
                "reason": decision["reason"],
            }
            self._corrections.append(correction)

    def save_corrections(self) -> None:
        """Write accumulated trim corrections to JSON."""
        with open(self.corrections_path, "w", encoding="utf-8") as f:
            json.dump(self._corrections, f, ensure_ascii=False, indent=2)

    @property
    def corrections(self) -> list[dict]:
        return list(self._corrections)
