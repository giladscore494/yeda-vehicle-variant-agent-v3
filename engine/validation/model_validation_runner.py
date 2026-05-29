"""Model validation runner — orchestrates Gemini/OpenAI calls for suspicious groups.

Gemini = primary validator (for suspicious groups only).
OpenAI = second opinion only (for risky/low-confidence Gemini results).

Never sends every variant to models.
Never mutates canonical.
"""
from __future__ import annotations

import json
import logging
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from engine import config
from engine.validation.cost_tracker import CostTracker
from engine.validation.model_schema import (
    RISKY_RECOMMENDATIONS,
    normalize_model_output,
    parse_model_json,
    validate_item,
    wrap_provider_result,
    needs_openai_second_opinion,
)
from engine.validation.write_guard import safe_write_json

logger = logging.getLogger(__name__)


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
    """Call Gemini for a model validation item. Returns wrapped result."""
    api_key = config.get("google", "api_key")
    model_id = config.get("google", "gemini_validator_model_id")
    grounding = config.get_bool("google", "grounding_enabled", True)

    if not api_key:
        return wrap_provider_result(
            False, "gemini", model_id or "", item["validation_item_id"],
            error_type="model_auth_error",
            error_message="Google API key not configured",
        )

    prompt = _build_unified_prompt(item, role="primary")
    input_est = len(prompt) // 3
    output_est = max(500, input_est // 2)
    variant_ids = item.get("variant_ids", [])
    group_key = item.get("seed_id", item["validation_item_id"])

    if cost_tracker:
        cost_tracker.log_planned(
            "gemini", model_id, group_key, variant_ids,
            input_est, output_est, search_used=grounding,
        )

    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        generate_kwargs: dict[str, Any] = {}
        if grounding:
            try:
                from google.genai import types
                generate_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]
            except Exception:
                logger.warning("Grounding setup failed; proceeding without")

        response = client.models.generate_content(
            model=model_id, contents=prompt, **generate_kwargs,
        )

        raw_text = response.text or ""
        input_actual = getattr(
            getattr(response, "usage_metadata", None), "prompt_token_count", None
        )
        output_actual = getattr(
            getattr(response, "usage_metadata", None), "candidates_token_count", None
        )

        if cost_tracker:
            cost_tracker.log_actual(
                "gemini", model_id, group_key, variant_ids,
                input_est, output_est, input_actual, output_actual,
                search_used=grounding, status="success",
            )

        parsed, parse_error = parse_model_json(raw_text)
        if parse_error:
            return wrap_provider_result(
                False, "gemini", model_id, item["validation_item_id"],
                raw_text=raw_text,
                error_type="model_parse_error",
                error_message="Failed to parse Gemini JSON response",
            )

        normalized = normalize_model_output(
            parsed, item["validation_item_id"], model_id, "primary",
        )
        schema_errors = validate_item(normalized)
        if schema_errors:
            return wrap_provider_result(
                False, "gemini", model_id, item["validation_item_id"],
                parsed_result=normalized, raw_text=raw_text,
                error_type="validation_schema_error",
                error_message=f"Schema validation failed: {'; '.join(schema_errors)}",
            )

        return wrap_provider_result(
            True, "gemini", model_id, item["validation_item_id"],
            parsed_result=normalized, raw_text=raw_text,
        )

    except Exception as exc:
        logger.error("Gemini call failed for %s: %s", item["validation_item_id"], exc)
        if cost_tracker:
            cost_tracker.log_actual(
                "gemini", model_id, group_key, variant_ids,
                input_est, output_est, None, None,
                search_used=grounding, status="error",
            )
        return wrap_provider_result(
            False, "gemini", model_id, item["validation_item_id"],
            error_type="model_call_error",
            error_message=str(exc),
        )


def _call_openai(item: dict, gemini_result: dict | None,
                 cost_tracker: CostTracker | None) -> dict:
    """Call OpenAI for second-opinion review. Returns wrapped result."""
    api_key = config.get("openai", "api_key")
    model_id = config.get("openai", "validator_model_id")
    web_search = config.get_bool("openai", "web_search_enabled", True)

    if not api_key:
        return wrap_provider_result(
            False, "openai", model_id or "", item["validation_item_id"],
            error_type="model_auth_error",
            error_message="OpenAI API key not configured",
        )

    prompt = _build_unified_prompt(
        item, role="second_opinion", gemini_result=gemini_result,
    )
    input_est = len(prompt) // 3
    output_est = max(500, input_est // 2)
    variant_ids = item.get("variant_ids", [])
    group_key = item.get("seed_id", item["validation_item_id"])

    if cost_tracker:
        cost_tracker.log_planned(
            "openai", model_id, group_key, variant_ids,
            input_est, output_est, search_used=web_search,
        )

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)

        tools = [{"type": "web_search_preview"}] if web_search else None
        create_kwargs: dict = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
        }
        if tools:
            create_kwargs["tools"] = tools

        response = client.chat.completions.create(**create_kwargs)
        raw_text = response.choices[0].message.content or "" if response.choices else ""

        input_actual = getattr(getattr(response, "usage", None), "prompt_tokens", None)
        output_actual = getattr(getattr(response, "usage", None), "completion_tokens", None)

        if cost_tracker:
            cost_tracker.log_actual(
                "openai", model_id, group_key, variant_ids,
                input_est, output_est, input_actual, output_actual,
                search_used=web_search, status="success",
            )

        parsed, parse_error = parse_model_json(raw_text)
        if parse_error:
            return wrap_provider_result(
                False, "openai", model_id, item["validation_item_id"],
                raw_text=raw_text,
                error_type="model_parse_error",
                error_message="Failed to parse OpenAI JSON response",
            )

        normalized = normalize_model_output(
            parsed, item["validation_item_id"], model_id, "second_opinion",
        )
        schema_errors = validate_item(normalized)
        if schema_errors:
            return wrap_provider_result(
                False, "openai", model_id, item["validation_item_id"],
                parsed_result=normalized, raw_text=raw_text,
                error_type="validation_schema_error",
                error_message=f"Schema validation failed: {'; '.join(schema_errors)}",
            )

        return wrap_provider_result(
            True, "openai", model_id, item["validation_item_id"],
            parsed_result=normalized, raw_text=raw_text,
        )

    except Exception as exc:
        logger.error("OpenAI call failed for %s: %s", item["validation_item_id"], exc)
        if cost_tracker:
            cost_tracker.log_actual(
                "openai", model_id, group_key, variant_ids,
                input_est, output_est, None, None,
                search_used=web_search, status="error",
            )
        return wrap_provider_result(
            False, "openai", model_id, item["validation_item_id"],
            error_type="model_call_error",
            error_message=str(exc),
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
    output_dir: str | Path = "data/validated_runs",
) -> dict:
    """Run model validation on a list of validation items.

    1. Call Gemini for each item (primary)
    2. Call OpenAI only for items that need second opinion
    3. Aggregate results
    4. Write model_validation_results_v2.json

    Returns a result dict with summary and items.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    cost_tracker = CostTracker(output_dir)

    started_at = datetime.now(timezone.utc).isoformat()

    gemini_attempted = 0
    gemini_success = 0
    gemini_failed = 0
    openai_attempted = 0
    openai_success = 0
    openai_failed = 0

    completed_items: list[dict] = []
    last_error: str | None = None

    for item in validation_items:
        item_id = item["validation_item_id"]

        # Step 1: Call Gemini (primary)
        gemini_attempted += 1
        gemini_result = _call_gemini(item, cost_tracker)

        if gemini_result["ok"]:
            gemini_success += 1
        else:
            gemini_failed += 1
            last_error = gemini_result.get("error_message")

        # Step 2: Determine if OpenAI is needed
        openai_result = None
        should_call_openai = False

        if gemini_result["ok"]:
            g_parsed = gemini_result.get("parsed_result", {})
            det_issues = item.get("deterministic_issues", [])
            should_call_openai = needs_openai_second_opinion(g_parsed, det_issues)
        elif item.get("requires_openai_second_opinion_initially", False):
            # Gemini failed but item was pre-flagged for dual validation
            should_call_openai = True
        elif item.get("risk_level") in ("high", "critical"):
            # High-risk items with failed Gemini still need OpenAI
            should_call_openai = True

        if should_call_openai:
            openai_attempted += 1
            gemini_parsed = gemini_result.get("parsed_result") if gemini_result["ok"] else None
            openai_result = _call_openai(item, gemini_parsed, cost_tracker)
            if openai_result["ok"]:
                openai_success += 1
            else:
                openai_failed += 1
                last_error = openai_result.get("error_message")

        # Step 3: Aggregate decision
        decision = _aggregate_decision(item, gemini_result, openai_result)

        completed_item = {
            "validation_item_id": item_id,
            "group_type": item.get("group_type"),
            "seed_id": item.get("seed_id"),
            "variant_ids": item.get("variant_ids", []),
            "model_name": gemini_result.get("model_id", ""),
            "model_role": "primary",
            **{k: v for k, v in decision.items()
               if k not in ("gemini_result", "openai_result")},
            # Include evidence from model results
            "evidence": (gemini_result.get("parsed_result") or {}).get("evidence", []),
            "issues_found": (gemini_result.get("parsed_result") or {}).get("issues_found", []),
            "suggested_patch": (gemini_result.get("parsed_result") or {}).get(
                "suggested_patch", {"has_patch": False, "patch_type": "none",
                                    "target_variant_id": None, "field": None,
                                    "current_value": None, "suggested_value": None,
                                    "reason": None, "safe_to_auto_apply": False}
            ),
            "needs_build_retry": (gemini_result.get("parsed_result") or {}).get("needs_build_retry", False),
            "needs_data_correction": (gemini_result.get("parsed_result") or {}).get("needs_data_correction", False),
            "risk_level": item.get("risk_level", "medium"),
        }

        completed_items.append(completed_item)

        # Check for runaway
        warnings = cost_tracker.check_runaway()
        if warnings:
            logger.warning("Cost tracker warnings: %s", warnings)
            break

    completed_at = datetime.now(timezone.utc).isoformat()

    model_calls_summary = {
        "gemini_calls_attempted": gemini_attempted,
        "gemini_calls_success": gemini_success,
        "gemini_calls_failed": gemini_failed,
        "openai_calls_attempted": openai_attempted,
        "openai_calls_success": openai_success,
        "openai_calls_failed": openai_failed,
    }

    failed_count = sum(
        1 for item in completed_items
        if item.get("final_status") == "model_validation_failed"
    )

    results = {
        "validation_run_id": f"model_val_{started_at}",
        "started_at": started_at,
        "completed_at": completed_at,
        "model_validation_ran": True,
        "model_calls_summary": model_calls_summary,
        "items": completed_items,
        "model_validation_items_count": len(completed_items),
        "model_validation_failed_items_count": failed_count,
        "model_validation_output_path": str(
            output_dir / "model_validation_results_v2.json"
        ),
        "last_model_validation_error": last_error,
        "cost_summary": cost_tracker.summary(),
    }

    # Write results
    results_path = output_dir / "model_validation_results_v2.json"
    safe_write_json(results, results_path)

    return results
