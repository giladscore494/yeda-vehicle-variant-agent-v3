"""Deprecated legacy model validation runner.

Task 3 model calls must go through ``model_review_runner.run_model_review()``,
which consumes ``data/validation/issue_queue.json`` and routes only rows marked
``requires_model_review=true``. This module keeps legacy schema/aggregation
helpers for compatibility, but its provider wrappers and public runner are safe
no-call shims.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from engine import config
from engine.validation.cost_tracker import CostTracker
from engine.validation.model_schema import (
    RISKY_RECOMMENDATIONS,
    wrap_provider_result,
)
from engine.validation.write_guard import safe_write_json



# ── Unified prompt builder ──────────────────────────────────────────────

def _build_unified_prompt(item: dict, role: str = "primary",
                          gemini_result: dict | None = None) -> str:
    """Build a model prompt that requests the unified schema output."""
    group_data = item.get("group_data", {})
    variants = group_data.get("variants", [])
    trim_candidates = group_data.get("trim_candidates", [])
    seed_id = item.get("seed_id", "")
    group_type = item.get("group_type", "")
    reason = item.get("reason_for_model_validation", "")
    det_issues = item.get("deterministic_issues", [])

    make = variants[0].get("make", "Unknown") if variants else "Unknown"
    model_name = variants[0].get("model", "Unknown") if variants else "Unknown"
    gen = variants[0].get("generation", "") if variants else ""

    variant_lines = []
    for v in variants:
        variant_lines.append(
            f"  - variant_id: {v.get('variant_id', '?')}\n"
            f"    trim: {v.get('trim')}, engine: {v.get('engine')}, "
            f"fuel: {v.get('fuel_type')}\n"
            f"    years: {v.get('year_start')}-{v.get('year_end')}, "
            f"market_scope: {v.get('market_scope')}\n"
            f"    marketed_name_il: {v.get('official_marketed_name_il', '')}"
        )
    variants_block = "\n".join(variant_lines) if variant_lines else "(no variants)"
    trims_block = ", ".join(trim_candidates) if trim_candidates else "(none)"

    issues_block = ""
    if det_issues:
        issue_lines = [
            f"  - {d.get('issue_type')}: severity={d.get('severity')}"
            for d in det_issues[:10]
        ]
        issues_block = "\nDeterministic issues found:\n" + "\n".join(issue_lines)

    role_instruction = ""
    if role == "second_opinion" and gemini_result:
        role_instruction = f"""
You are providing a SECOND OPINION on this validation.
The primary validator (Gemini) returned this assessment:
{json.dumps(gemini_result, indent=2, ensure_ascii=False)}

If you agree, confirm it. If you disagree, explain why.
"""

    return f"""You are an Israeli automotive market expert validator.
{role_instruction}
TASK: Validate the following vehicle variant group for the Israeli market.
Focus on trim/grade/gimur name accuracy.

Vehicle: {make} {model_name} {gen}
Seed ID: {seed_id}
Group type: {group_type}
Reason for validation: {reason}
Trim candidates: {trims_block}

Variants:
{variants_block}
{issues_block}

Return ONLY valid JSON (no markdown fences, no text outside JSON).
Use this EXACT schema:

{{
  "validation_item_id": "{item.get('validation_item_id', '')}",
  "group_type": "{group_type}",
  "seed_id": {json.dumps(seed_id)},
  "variant_ids": {json.dumps([v.get('variant_id', '') for v in variants])},
  "recommendation": "no_action|needs_evidence|needs_normalization|manual_review|build_retry|merge|rename_trim|promote_to_verified|reject|change_year_range|change_market_scope|resolve_source_conflict",
  "confidence": 0.0,
  "risk_level": "low|medium|high|critical",
  "evidence": [
    {{
      "claim": "string",
      "source": "string or null",
      "source_type": "canonical|deterministic_audit|web|model_reasoning|null",
      "supports_recommendation": true
    }}
  ],
  "issues_found": [],
  "suggested_patch": {{
    "has_patch": false,
    "patch_type": "none|field_update|merge|status_change|manual_review_flag",
    "target_variant_id": null,
    "field": null,
    "current_value": null,
    "suggested_value": null,
    "reason": null,
    "safe_to_auto_apply": false
  }},
  "needs_build_retry": false,
  "needs_manual_review": false,
  "needs_data_correction": false,
  "safe_to_auto_apply": false
}}

Rules:
- confidence must be between 0.0 and 1.0
- safe_to_auto_apply must be false
- Use Israeli sources first (official importer, iCar, Cartube, Auto.co.il)
- Do NOT invent source references"""


# ── Provider call wrappers ──────────────────────────────────────────────

def _call_gemini(item: dict, cost_tracker: CostTracker | None) -> dict:
    """Deprecated legacy provider wrapper.

    Task 3 model access is exclusively gated through
    engine.validation.model_review_runner.run_model_review(), which loads
    data/validation/issue_queue.json and routes only items with
    requires_model_review=true. This compatibility shim never calls Gemini.
    """
    item_id = item.get("validation_item_id") or item.get("item_id", "")
    model_id = config.get("google", "gemini_validator_model_id", "")
    return wrap_provider_result(
        False, "gemini", model_id or "", item_id,
        error_type="legacy_model_validation_disabled",
        error_message=(
            "Legacy direct Gemini validation is disabled. Use "
            "engine.validation.model_review_runner.run_model_review(), which "
            "consumes data/validation/issue_queue.json and enforces "
            "requires_model_review=true routing."
        ),
    )


def _call_openai(
    item: dict,
    gemini_result: dict | None,
    cost_tracker: CostTracker | None,
) -> dict:
    """Deprecated legacy provider wrapper; never calls OpenAI directly."""
    item_id = item.get("validation_item_id") or item.get("item_id", "")
    model_id = config.get("openai", "validator_model_id", "")
    return wrap_provider_result(
        False, "openai", model_id or "", item_id,
        error_type="legacy_model_validation_disabled",
        error_message=(
            "Legacy direct OpenAI validation is disabled. Use "
            "engine.validation.model_review_runner.run_model_review(), which "
            "consumes data/validation/issue_queue.json and enforces "
            "requires_model_review=true routing."
        ),
    )


# ── Aggregation / decision logic ────────────────────────────────────────

def _aggregate_decision(
    item: dict,
    gemini_result: dict,
    openai_result: dict | None,
) -> dict:
    """Aggregate Gemini + optional OpenAI results into a final decision.

    Rules:
    - If Gemini says no_action and risk not high: final = Gemini
    - If Gemini recommends risky action and OpenAI agrees: create patch suggestion
    - If Gemini recommends risky action and OpenAI disagrees: manual_review
    - If Gemini confidence < 0.75: manual_review unless OpenAI strongly confirms
    - If Gemini output invalid: model_validation_failed
    - Never apply patches directly to canonical
    """
    g = gemini_result.get("parsed_result", {})
    g_ok = gemini_result.get("ok", False)

    # Gemini failed
    if not g_ok:
        return {
            "final_status": "model_validation_failed",
            "final_recommendation": "manual_review",
            "primary_model": gemini_result.get("provider", "gemini"),
            "secondary_model": None,
            "confidence": 0.0,
            "reason": f"Gemini validation failed: {gemini_result.get('error_message', 'unknown')}",
            "needs_manual_review": True,
            "safe_to_auto_apply": False,
            "gemini_result": gemini_result,
            "openai_result": openai_result,
        }

    g_rec = g.get("recommendation", "no_action")
    g_conf = g.get("confidence", 0.5)
    g_risk = g.get("risk_level", item.get("risk_level", "medium"))

    # No OpenAI result
    if openai_result is None or not openai_result.get("ok", False):
        openai_failed = openai_result is not None and not openai_result.get("ok", False)

        # Gemini confidence < 0.75 without OpenAI confirmation
        if g_conf < 0.75:
            return {
                "final_status": "needs_manual_review",
                "final_recommendation": "manual_review",
                "primary_model": "gemini",
                "secondary_model": None,
                "confidence": g_conf,
                "reason": f"Gemini confidence {g_conf} < 0.75, no second opinion available",
                "needs_manual_review": True,
                "safe_to_auto_apply": False,
                "gemini_result": gemini_result,
                "openai_result": openai_result,
            }

        # Gemini says no_action and risk is not high
        if g_rec == "no_action" and g_risk not in ("high", "critical"):
            return {
                "final_status": "validated_by_gemini",
                "final_recommendation": g_rec,
                "primary_model": "gemini",
                "secondary_model": None,
                "confidence": g_conf,
                "reason": g.get("reason", "Gemini validated, no issues found"),
                "needs_manual_review": False,
                "safe_to_auto_apply": False,
                "gemini_result": gemini_result,
                "openai_result": openai_result,
            }

        # Risky recommendation without OpenAI
        if g_rec in RISKY_RECOMMENDATIONS:
            return {
                "final_status": "needs_manual_review",
                "final_recommendation": g_rec,
                "primary_model": "gemini",
                "secondary_model": None,
                "confidence": g_conf,
                "reason": f"Risky recommendation '{g_rec}' without second opinion",
                "needs_manual_review": True,
                "safe_to_auto_apply": False,
                "gemini_result": gemini_result,
                "openai_result": openai_result,
            }

        # Default: accept Gemini result
        return {
            "final_status": "validated_by_gemini",
            "final_recommendation": g_rec,
            "primary_model": "gemini",
            "secondary_model": None,
            "confidence": g_conf,
            "reason": g.get("reason", "Gemini primary validation"),
            "needs_manual_review": g_rec == "manual_review",
            "safe_to_auto_apply": False,
            "gemini_result": gemini_result,
            "openai_result": openai_result,
        }

    # Both models available
    o = openai_result.get("parsed_result", {})
    o_rec = o.get("recommendation", "no_action")
    o_conf = o.get("confidence", 0.5)

    # Models agree
    if g_rec == o_rec:
        if g_rec in RISKY_RECOMMENDATIONS:
            return {
                "final_status": "validated_dual_model",
                "final_recommendation": g_rec,
                "primary_model": "gemini",
                "secondary_model": "openai",
                "confidence": max(g_conf, o_conf),
                "reason": f"Both models agree on '{g_rec}'",
                "needs_manual_review": False,
                "safe_to_auto_apply": False,
                "gemini_result": gemini_result,
                "openai_result": openai_result,
            }
        return {
            "final_status": "validated_dual_model",
            "final_recommendation": g_rec,
            "primary_model": "gemini",
            "secondary_model": "openai",
            "confidence": max(g_conf, o_conf),
            "reason": f"Dual model agreement: {g_rec}",
            "needs_manual_review": False,
            "safe_to_auto_apply": False,
            "gemini_result": gemini_result,
            "openai_result": openai_result,
        }

    # Gemini risky, OpenAI disagrees → manual review
    if g_rec in RISKY_RECOMMENDATIONS:
        return {
            "final_status": "needs_manual_review",
            "final_recommendation": "manual_review",
            "primary_model": "gemini",
            "secondary_model": "openai",
            "confidence": min(g_conf, o_conf),
            "reason": f"Model disagreement: Gemini={g_rec}, OpenAI={o_rec}",
            "needs_manual_review": True,
            "safe_to_auto_apply": False,
            "gemini_result": gemini_result,
            "openai_result": openai_result,
        }

    # Gemini low confidence, OpenAI strongly confirms different action
    if g_conf < 0.75 and o_conf >= 0.85:
        return {
            "final_status": "validated_by_openai_override",
            "final_recommendation": o_rec,
            "primary_model": "gemini",
            "secondary_model": "openai",
            "confidence": o_conf,
            "reason": f"OpenAI override (conf={o_conf}): Gemini had low confidence ({g_conf})",
            "needs_manual_review": o_rec in RISKY_RECOMMENDATIONS,
            "safe_to_auto_apply": False,
            "gemini_result": gemini_result,
            "openai_result": openai_result,
        }

    # Default disagreement → manual review
    return {
        "final_status": "needs_manual_review",
        "final_recommendation": "manual_review",
        "primary_model": "gemini",
        "secondary_model": "openai",
        "confidence": min(g_conf, o_conf),
        "reason": f"Model disagreement: Gemini={g_rec} ({g_conf}), OpenAI={o_rec} ({o_conf})",
        "needs_manual_review": True,
        "safe_to_auto_apply": False,
        "gemini_result": gemini_result,
        "openai_result": openai_result,
    }


# ── Main runner ─────────────────────────────────────────────────────────

def run_model_validation(
    validation_items: list[dict],
    output_dir: str | Path = "data/validation",
    dry_run: bool = False,
) -> dict:
    """Deprecated legacy model-validation entry point.

    This function intentionally performs zero provider calls for arbitrary
    ``validation_items``. Task 3 model review must flow through
    ``engine.validation.model_review_runner.run_model_review()``, which loads
    ``data/validation/issue_queue.json`` and lets ``route_issue_item()`` call
    models only for issue-queue rows marked ``requires_model_review=true``.
    """
    started_at = datetime.now(timezone.utc).isoformat()
    completed_at = datetime.now(timezone.utc).isoformat()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "ok": False,
        "error": "legacy_model_validation_disabled",
        "message": (
            "Legacy run_model_validation(validation_items=...) is disabled to "
            "prevent provider calls outside the issue_queue + "
            "requires_model_review=true gate. Use "
            "engine.validation.model_review_runner.run_model_review()."
        ),
        "validation_run_id": f"legacy_model_val_disabled_{started_at}",
        "started_at": started_at,
        "completed_at": completed_at,
        "model_validation_ran": False,
        "dry_run": bool(dry_run),
        "items": [],
        "rejected_items_count": len(validation_items),
        "model_validation_items_count": 0,
        "model_validation_failed_items_count": 0,
        "model_validation_output_path": str(output_dir / "model_validation_results_v2.json"),
        "last_model_validation_error": "legacy_model_validation_disabled",
        "model_calls_summary": {
            "gemini_calls_attempted": 0,
            "gemini_calls_success": 0,
            "gemini_calls_failed": 0,
            "openai_calls_attempted": 0,
            "openai_calls_success": 0,
            "openai_calls_failed": 0,
        },
        "cost_summary": {"estimated_total_usd": 0.0, "actual_total_usd": 0.0},
    }

    safe_write_json(results, output_dir / "model_validation_results_v2.json")
    return results
