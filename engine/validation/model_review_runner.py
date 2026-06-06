"""Budgeted deterministic-first model review runner.

This runner consumes the deterministic ``issue_queue.json`` and sends only the
eligible issue rows to routed model providers. It never sends the whole vehicle
database, never mutates the source canonical, and appends model decisions only
under ``data/validation``.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.paths import DECISIONS_PATH, ISSUE_QUEUE_PATH
from engine import config
from engine.validation.model_router import ModelRoutingDecision, route_issue_item
from engine.validation.run_events import log_event
from engine.validation.write_guard import safe_write_json

MAX_MODEL_ITEMS_PER_RUN = 10
MAX_MODEL_CALLS_PER_RUN = 20
MAX_MODEL_COST_USD_PER_RUN = 2.00

_GEMINI_ESTIMATED_COST_USD = 0.05
_OPENAI_ESTIMATED_COST_USD = 0.10
_NEVER_AUTO_APPLY_ACTIONS = {
    "reject",
    "merge",
    "change_year_range",
    "change_market_scope",
    "promote_to_verified",
    "resolve_source_conflict",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_issue_items() -> list[dict]:
    path = Path(ISSUE_QUEUE_PATH)
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        return [item for item in payload.get("items", []) if isinstance(item, dict)]
    return []


def _load_decisions_payload() -> dict:
    path = Path(DECISIONS_PATH)
    if not path.exists():
        return {"created_at": _utc_now(), "decisions": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return {"created_at": _utc_now(), "decisions": payload}
    if isinstance(payload, dict):
        decisions = payload.get("decisions")
        if not isinstance(decisions, list):
            payload["decisions"] = []
        return payload
    return {"created_at": _utc_now(), "decisions": []}


def _routing_to_dict(routing: ModelRoutingDecision) -> dict:
    return routing.to_dict()


def _preview_item(item: dict, routing: ModelRoutingDecision) -> dict:
    return {
        "item_id": item.get("item_id", ""),
        "seed_id": item.get("seed_id", ""),
        "make": item.get("make", ""),
        "model": item.get("model", ""),
        "issue_type": item.get("issue_type", ""),
        "risk_level": item.get("risk_level", ""),
        "routing_policy": routing.decision_policy,
        "primary_provider": routing.primary_provider,
        "primary_web_required": routing.primary_web_required,
        "second_opinion_provider": routing.second_opinion_provider,
        "second_opinion_web_required": routing.second_opinion_web_required,
        "max_expected_calls": routing.max_expected_calls,
    }


def _estimate_cost(planned_gemini_calls: int, planned_openai_calls: int) -> float:
    return round(
        planned_gemini_calls * _GEMINI_ESTIMATED_COST_USD
        + planned_openai_calls * _OPENAI_ESTIMATED_COST_USD,
        4,
    )


def _planned_counts(routings: list[ModelRoutingDecision]) -> dict:
    planned_gemini_calls = sum(1 for r in routings if r.should_call_models and r.primary_provider == "gemini")
    planned_openai_calls = sum(1 for r in routings if r.should_call_models and r.second_opinion_provider == "openai")
    planned_total_calls = planned_gemini_calls + planned_openai_calls
    return {
        "planned_gemini_calls": planned_gemini_calls,
        "planned_openai_calls": planned_openai_calls,
        "planned_total_calls": planned_total_calls,
        "estimated_cost_usd": _estimate_cost(planned_gemini_calls, planned_openai_calls),
    }


def _build_preview(selected: list[dict], routings: list[ModelRoutingDecision]) -> dict:
    counts = _planned_counts(routings)
    return {
        "selected_items": len(selected),
        **counts,
        "items": [_preview_item(item, routing) for item, routing in zip(selected, routings)],
    }


def _budget_error(preview: dict) -> dict | None:
    errors: list[str] = []
    if preview["selected_items"] > MAX_MODEL_ITEMS_PER_RUN:
        errors.append(f"selected_items exceeds {MAX_MODEL_ITEMS_PER_RUN}")
    if preview["planned_total_calls"] > MAX_MODEL_CALLS_PER_RUN:
        errors.append(f"planned_total_calls exceeds {MAX_MODEL_CALLS_PER_RUN}")
    if preview["estimated_cost_usd"] > MAX_MODEL_COST_USD_PER_RUN:
        errors.append(f"estimated_cost_usd exceeds {MAX_MODEL_COST_USD_PER_RUN:.2f}")
    if not errors:
        return None
    return {
        "ok": False,
        "error": "budget_guardrail_blocked",
        "reasons": errors,
        **preview,
    }


def _filter_items(
    items: list[dict],
    risk_levels: list[str] | None,
    issue_types: list[str] | None,
    seed_id_filter: str | None,
) -> list[dict]:
    risk_set = {str(level).lower() for level in risk_levels} if risk_levels else None
    issue_set = {str(issue) for issue in issue_types} if issue_types else None
    selected: list[dict] = []
    for item in items:
        if not item.get("requires_model_review", False):
            continue
        if risk_set and str(item.get("risk_level") or "").lower() not in risk_set:
            continue
        if issue_set and str(item.get("issue_type") or "") not in issue_set:
            continue
        if seed_id_filter is not None and str(item.get("seed_id") or "") != seed_id_filter:
            continue
        selected.append(item)
    return selected


def _prompt_payload(item: dict, routing: ModelRoutingDecision, role: str, gemini_result: dict | None = None) -> dict:
    """Build a compact issue-only payload for providers; never includes full DB."""
    payload = {
        "role": role,
        "item": item,
        "routing_policy": routing.decision_policy,
        "instructions": {
            "safe_to_auto_apply": False,
            "requires_manual_approval": True,
            "do_not_mutate_source_canonical": True,
            "return_json_only": True,
        },
    }
    if gemini_result is not None:
        payload["primary_result"] = gemini_result
    return payload


def _provider_unconfigured(provider: str, model: str, item: dict, message: str) -> dict:
    return {
        "ok": False,
        "provider": provider,
        "model": model,
        "item_id": item.get("item_id", ""),
        "error_type": "model_auth_error",
        "error_message": message,
        "safe_to_auto_apply": False,
    }


def call_gemini_for_issue(item: dict, routing: ModelRoutingDecision) -> dict:
    """Call Gemini for one issue item using the routed web-grounding setting."""
    model = routing.primary_model or config.get("google", "gemini_validator_model_id")
    api_key = config.get("google", "api_key")
    if not api_key:
        return _provider_unconfigured("gemini", model, item, "Google API key not configured")

    prompt = json.dumps(_prompt_payload(item, routing, "primary_factual_validator"), ensure_ascii=False, indent=2)
    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        generate_kwargs: dict[str, Any] = {}
        if routing.primary_web_required:
            try:
                from google.genai import types

                generate_kwargs["config"] = types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            except Exception:
                generate_kwargs = {}
        response = client.models.generate_content(model=model, contents=prompt, **generate_kwargs)
        raw_text = response.text or ""
        parsed: dict[str, Any]
        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError:
            parsed = {"raw_text": raw_text}
        parsed["safe_to_auto_apply"] = False
        return {"ok": True, "provider": "gemini", "model": model, "parsed_result": parsed, "raw_text": raw_text}
    except Exception as exc:
        return {
            "ok": False,
            "provider": "gemini",
            "model": model,
            "item_id": item.get("item_id", ""),
            "error_type": "model_call_error",
            "error_message": str(exc),
            "safe_to_auto_apply": False,
        }


def call_openai_for_issue(item: dict, routing: ModelRoutingDecision, gemini_result: dict | None) -> dict:
    """Call OpenAI for one issue item as a strict second-opinion reviewer."""
    model = routing.second_opinion_model or config.get("openai", "validator_model_id")
    api_key = config.get("openai", "api_key")
    if not api_key:
        return _provider_unconfigured("openai", model, item, "OpenAI API key not configured")

    prompt = json.dumps(
        _prompt_payload(item, routing, "strict_second_opinion_reviewer", gemini_result),
        ensure_ascii=False,
        indent=2,
    )
    try:
        import openai

        client = openai.OpenAI(api_key=api_key)
        if routing.second_opinion_web_required:
            response = client.responses.create(
                model=model,
                input=prompt,
                tools=[{"type": "web_search_preview"}],
            )
        else:
            response = client.responses.create(model=model, input=prompt)
        raw_text = getattr(response, "output_text", "") or str(response)
        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError:
            parsed = {"raw_text": raw_text}
        parsed["safe_to_auto_apply"] = False
        return {"ok": True, "provider": "openai", "model": model, "parsed_result": parsed, "raw_text": raw_text}
    except Exception as exc:
        return {
            "ok": False,
            "provider": "openai",
            "model": model,
            "item_id": item.get("item_id", ""),
            "error_type": "model_call_error",
            "error_message": str(exc),
            "safe_to_auto_apply": False,
        }


def _result_recommendation(result: dict | None) -> str | None:
    if not isinstance(result, dict):
        return None
    parsed = result.get("parsed_result") if isinstance(result.get("parsed_result"), dict) else result
    value = parsed.get("recommendation") or parsed.get("final_recommendation") or parsed.get("action")
    return str(value) if value else None


def _result_confidence(result: dict | None) -> float | None:
    if not isinstance(result, dict):
        return None
    parsed = result.get("parsed_result") if isinstance(result.get("parsed_result"), dict) else result
    raw = parsed.get("confidence")
    if isinstance(raw, (int, float)):
        return max(0.0, min(1.0, float(raw)))
    if isinstance(raw, str):
        mapping = {"high": 0.85, "medium": 0.6, "low": 0.35}
        if raw.lower() in mapping:
            return mapping[raw.lower()]
        try:
            return max(0.0, min(1.0, float(raw)))
        except ValueError:
            return None
    return None


def _build_decision(
    item: dict,
    routing: ModelRoutingDecision,
    gemini_result: dict | None,
    openai_result: dict | None,
) -> dict:
    openai_recommendation = _result_recommendation(openai_result)
    gemini_recommendation = _result_recommendation(gemini_result)
    recommendation = openai_recommendation or gemini_recommendation or "manual_review"
    if recommendation in _NEVER_AUTO_APPLY_ACTIONS:
        recommendation = f"manual_approval_required:{recommendation}"

    confidences = [c for c in (_result_confidence(gemini_result), _result_confidence(openai_result)) if c is not None]
    confidence = min(confidences) if confidences else 0.0

    return {
        "decision_id": f"md_{uuid.uuid4().hex}",
        "item_id": item.get("item_id", ""),
        "seed_id": item.get("seed_id", ""),
        "issue_type": item.get("issue_type", ""),
        "risk_level": item.get("risk_level", ""),
        "routing": _routing_to_dict(routing),
        "gemini_result": gemini_result,
        "openai_result": openai_result,
        "final_recommendation": recommendation,
        "confidence": confidence,
        "safe_to_auto_apply": False,
        "requires_manual_approval": True,
        "created_at": _utc_now(),
    }


def _append_decisions(decisions: list[dict]) -> None:
    if not decisions:
        return
    payload = _load_decisions_payload()
    payload.setdefault("created_at", _utc_now())
    payload["updated_at"] = _utc_now()
    payload.setdefault("decisions", [])
    payload["decisions"].extend(decisions)
    safe_write_json(payload, DECISIONS_PATH)


def run_model_review(
    max_items: int = 1,
    risk_levels: list[str] | None = None,
    issue_types: list[str] | None = None,
    seed_id_filter: str | None = None,
    dry_run: bool = False,
) -> dict:
    """Run or preview budgeted model review for deterministic issue-queue items."""
    max_items = max(0, int(max_items))
    candidate_items = _filter_items(_load_issue_items(), risk_levels, issue_types, seed_id_filter)
    selected = candidate_items[:max_items]
    routings = [route_issue_item(item) for item in selected]
    preview = _build_preview(selected, routings)

    log_event(
        {
            "stage": "model_review",
            "event_type": "ai_preview_started",
            "status": "started",
            "request_summary": f"max_items={max_items} selected={len(selected)} dry_run={dry_run}",
        }
    )
    budget_error = _budget_error(preview)
    if budget_error:
        log_event(
            {
                "stage": "model_review",
                "event_type": "ai_preview_completed",
                "status": "failed",
                "response_summary": budget_error.get("error", "budget_guardrail_blocked"),
            }
        )
        return budget_error

    if dry_run:
        log_event(
            {
                "stage": "model_review",
                "event_type": "ai_preview_completed",
                "status": "ok",
                "response_summary": (
                    f"planned_calls={preview.get('planned_total_calls', 0)} "
                    f"estimated_cost={preview.get('estimated_cost_usd', 0)}"
                ),
            }
        )
        return preview

    decisions: list[dict] = []
    for item, routing in zip(selected, routings):
        if not routing.should_call_models:
            continue

        gemini_result = None
        openai_result = None
        if routing.primary_provider == "gemini":
            log_event(
                {
                    "stage": "model_review",
                    "event_type": "model_call_planned",
                    "item_id": item.get("item_id", ""),
                    "provider": "gemini",
                    "model": routing.primary_model or config.get("google", "gemini_validator_model_id"),
                    "status": "planned",
                    "request_summary": f"issue_type={item.get('issue_type', '')}",
                }
            )
            log_event(
                {
                    "stage": "model_review",
                    "event_type": "model_call_started",
                    "item_id": item.get("item_id", ""),
                    "provider": "gemini",
                    "model": routing.primary_model or config.get("google", "gemini_validator_model_id"),
                    "status": "started",
                }
            )
            gemini_result = call_gemini_for_issue(item, routing)
            if isinstance(gemini_result, dict):
                gemini_result["safe_to_auto_apply"] = False
                log_event(
                    {
                        "stage": "model_review",
                        "event_type": "model_call_completed" if gemini_result.get("ok") else "model_call_failed",
                        "item_id": item.get("item_id", ""),
                        "provider": "gemini",
                        "model": gemini_result.get("model", routing.primary_model or ""),
                        "status": "ok" if gemini_result.get("ok") else "failed",
                        "response_summary": str(gemini_result.get("error_message") or gemini_result.get("parsed_result") or ""),
                        "error": str(gemini_result.get("error_message") or ""),
                    }
                )

        if routing.second_opinion_provider == "openai":
            log_event(
                {
                    "stage": "model_review",
                    "event_type": "model_call_planned",
                    "item_id": item.get("item_id", ""),
                    "provider": "openai",
                    "model": routing.second_opinion_model or config.get("openai", "validator_model_id"),
                    "status": "planned",
                    "request_summary": f"issue_type={item.get('issue_type', '')}",
                }
            )
            log_event(
                {
                    "stage": "model_review",
                    "event_type": "model_call_started",
                    "item_id": item.get("item_id", ""),
                    "provider": "openai",
                    "model": routing.second_opinion_model or config.get("openai", "validator_model_id"),
                    "status": "started",
                }
            )
            openai_result = call_openai_for_issue(item, routing, gemini_result)
            if isinstance(openai_result, dict):
                openai_result["safe_to_auto_apply"] = False
                log_event(
                    {
                        "stage": "model_review",
                        "event_type": "model_call_completed" if openai_result.get("ok") else "model_call_failed",
                        "item_id": item.get("item_id", ""),
                        "provider": "openai",
                        "model": openai_result.get("model", routing.second_opinion_model or ""),
                        "status": "ok" if openai_result.get("ok") else "failed",
                        "response_summary": str(openai_result.get("error_message") or openai_result.get("parsed_result") or ""),
                        "error": str(openai_result.get("error_message") or ""),
                    }
                )

        decision = _build_decision(item, routing, gemini_result, openai_result)
        decisions.append(decision)
        log_event(
            {
                "stage": "model_review",
                "event_type": "decision_appended",
                "item_id": item.get("item_id", ""),
                "status": "ok",
                "response_summary": f"final_recommendation={decision.get('final_recommendation', '')}",
            }
        )

    _append_decisions(decisions)
    log_event(
        {
            "stage": "model_review",
            "event_type": "ai_preview_completed",
            "status": "ok",
            "response_summary": f"decisions_written={len(decisions)}",
        }
    )
    return {
        "ok": True,
        **preview,
        "decisions_written": len(decisions),
        "decisions_path": DECISIONS_PATH,
    }
