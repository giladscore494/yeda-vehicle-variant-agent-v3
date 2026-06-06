"""Final clean database quality audit with deterministic checks + model verdict."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from core.paths import (
    DECISIONS_PATH,
    FINAL_CLEAN_DATABASE_PATH,
    SOURCE_CANONICAL_PATH,
    VALIDATION_REPORT_PATH,
)
from engine import config
from engine.validation.run_events import log_event

_REQUIRED_FIELDS = ("variant_id", "make", "model", "year_start", "year_end")
_JSON_SCHEMA = {
    "status": "FAIL",
    "confidence": 0.0,
    "blocking_reasons": [],
    "non_blocking_warnings": [],
    "required_fixes": [],
    "summary": "",
}


def _read_json(path: str) -> Any | None:
    file_path = Path(path)
    if not file_path.exists():
        return None
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _all_source_variants(source_payload: dict) -> list[dict]:
    return list(source_payload.get("verified_variants") or []) + list(source_payload.get("partial_variants") or [])


def _all_output_variants(final_payload: dict) -> list[dict]:
    vehicles = final_payload.get("vehicles")
    if isinstance(vehicles, list):
        return [item for item in vehicles if isinstance(item, dict)]
    return []


def _sha256(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _decision_action(decision: dict) -> str:
    for key in ("action", "decision_action", "recommended_action", "final_recommendation"):
        value = decision.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _approved_reject_decisions(decisions_payload: Any) -> set[str]:
    decisions: list[dict] = []
    if isinstance(decisions_payload, list):
        decisions = [d for d in decisions_payload if isinstance(d, dict)]
    elif isinstance(decisions_payload, dict):
        raw = decisions_payload.get("decisions")
        if isinstance(raw, list):
            decisions = [d for d in raw if isinstance(d, dict)]
    approved: set[str] = set()
    for decision in decisions:
        action = _decision_action(decision).lower()
        if action != "reject":
            continue
        if decision.get("safe_to_auto_apply") is not True:
            continue
        variant_id = str(decision.get("variant_id") or "").strip()
        if variant_id:
            approved.add(variant_id)
    return approved


def _missing_required_field_counts(variants: list[dict]) -> dict[str, int]:
    counts = {field: 0 for field in _REQUIRED_FIELDS}
    for variant in variants:
        for field in _REQUIRED_FIELDS:
            value = variant.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                counts[field] += 1
    return counts


def _duplicate_id_count(variants: list[dict]) -> int:
    seen: set[str] = set()
    duplicates = 0
    for variant in variants:
        variant_id = str(variant.get("variant_id") or "").strip()
        if not variant_id:
            continue
        if variant_id in seen:
            duplicates += 1
        else:
            seen.add(variant_id)
    return duplicates


def _suspicious_sample(variants: list[dict], *, max_items: int = 5) -> list[dict]:
    sample: list[dict] = []
    for variant in variants:
        missing = [field for field in _REQUIRED_FIELDS if not variant.get(field)]
        if missing:
            sample.append(
                {
                    "variant_id": variant.get("variant_id", ""),
                    "missing_fields": missing,
                    "seed_id": variant.get("seed_id", ""),
                }
            )
        if len(sample) >= max_items:
            break
    return sample


def _changed_records_sample(source_variants: list[dict], output_variants: list[dict], *, max_items: int = 5) -> list[dict]:
    source_by_id = {str(v.get("variant_id") or ""): v for v in source_variants if isinstance(v, dict) and v.get("variant_id")}
    changed: list[dict] = []
    for output in output_variants:
        variant_id = str(output.get("variant_id") or "")
        if not variant_id:
            continue
        source = source_by_id.get(variant_id)
        if not source:
            continue
        changed_keys = sorted(
            key for key in output.keys() | source.keys() if source.get(key) != output.get(key)
        )
        if changed_keys:
            changed.append({"variant_id": variant_id, "changed_fields": changed_keys[:10]})
        if len(changed) >= max_items:
            break
    return changed


def _model_decisions_not_applied_sample(decisions_payload: Any, *, max_items: int = 5) -> list[dict]:
    sample: list[dict] = []
    decisions: list[dict] = []
    if isinstance(decisions_payload, list):
        decisions = [d for d in decisions_payload if isinstance(d, dict)]
    elif isinstance(decisions_payload, dict):
        raw = decisions_payload.get("decisions")
        if isinstance(raw, list):
            decisions = [d for d in raw if isinstance(d, dict)]
    for decision in decisions:
        source = str(decision.get("source") or "").lower()
        is_model = any(marker in source for marker in ("model", "gemini", "openai", "ai", "llm"))
        if not is_model:
            continue
        if decision.get("safe_to_auto_apply") is True:
            continue
        sample.append(
            {
                "decision_id": decision.get("decision_id", ""),
                "variant_id": decision.get("variant_id", ""),
                "action": _decision_action(decision),
            }
        )
        if len(sample) >= max_items:
            break
    return sample


def _top_unresolved_issue_types(report_payload: Any) -> list[dict]:
    if not isinstance(report_payload, dict):
        return []
    raw = report_payload.get("top_issue_types")
    if not isinstance(raw, list):
        return []
    return [item for item in raw if isinstance(item, dict)][:10]


def _parse_model_json(raw_text: str) -> dict[str, Any] | None:
    try:
        payload = json.loads(raw_text)
        if isinstance(payload, dict):
            return payload
    except json.JSONDecodeError:
        pass
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start >= 0 and end > start:
        try:
            payload = json.loads(raw_text[start : end + 1])
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError:
            return None
    return None


def _normalize_model_result(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return dict(_JSON_SCHEMA)
    status = str(payload.get("status") or "").upper()
    if status not in ("PASS", "FAIL"):
        status = "FAIL"
    confidence = payload.get("confidence")
    if isinstance(confidence, (int, float)):
        confidence_value = max(0.0, min(1.0, float(confidence)))
    else:
        confidence_value = 0.0
    blocking_reasons = payload.get("blocking_reasons")
    non_blocking_warnings = payload.get("non_blocking_warnings")
    required_fixes = payload.get("required_fixes")
    return {
        "status": status,
        "confidence": confidence_value,
        "blocking_reasons": blocking_reasons if isinstance(blocking_reasons, list) else [],
        "non_blocking_warnings": non_blocking_warnings if isinstance(non_blocking_warnings, list) else [],
        "required_fixes": required_fixes if isinstance(required_fixes, list) else [],
        "summary": str(payload.get("summary") or ""),
    }


def _deterministic_checks() -> tuple[dict[str, Any], list[str], list[str]]:
    summary: dict[str, Any] = {}
    blocking_reasons: list[str] = []
    warnings: list[str] = []

    final_payload = _read_json(FINAL_CLEAN_DATABASE_PATH)
    source_payload = _read_json(SOURCE_CANONICAL_PATH)
    decisions_payload = _read_json(DECISIONS_PATH) or {"decisions": []}
    report_payload = _read_json(VALIDATION_REPORT_PATH) or {}

    if final_payload is None:
        blocking_reasons.append("Final clean database is missing.")
    if source_payload is None:
        blocking_reasons.append("Source canonical is missing.")
    if final_payload is None or source_payload is None:
        return summary, blocking_reasons, warnings

    if not isinstance(final_payload, dict):
        blocking_reasons.append("Final clean database is not a valid JSON object.")
        return summary, blocking_reasons, warnings
    if not isinstance(source_payload, dict):
        blocking_reasons.append("Source canonical is not a valid JSON object.")
        return summary, blocking_reasons, warnings

    output_variants = _all_output_variants(final_payload)
    source_variants = _all_source_variants(source_payload)
    input_count = len(source_variants)
    output_count = len(output_variants)
    delta = output_count - input_count

    output_schema_keys = sorted(final_payload.keys())
    missing_counts = _missing_required_field_counts(output_variants)
    duplicate_count = _duplicate_id_count(output_variants)
    metadata = final_payload.get("metadata") if isinstance(final_payload.get("metadata"), dict) else {}
    manual_review_remaining_count = int(metadata.get("manual_review_remaining_count", 0) or 0)
    rejected_count = int(metadata.get("rejected_count", 0) or 0)
    normalized_count = int(metadata.get("normalized_count", 0) or 0)
    model_not_applied_sample = _model_decisions_not_applied_sample(decisions_payload)

    summary.update(
        {
            "total_input_variants": input_count,
            "total_output_variants": output_count,
            "variant_count_delta": delta,
            "output_schema_keys": output_schema_keys,
            "missing_required_field_counts": missing_counts,
            "duplicate_id_count": duplicate_count,
            "rejected_count": rejected_count,
            "normalized_count": normalized_count,
            "manual_review_remaining_count": manual_review_remaining_count,
            "sample_of_suspicious_records": _suspicious_sample(output_variants),
            "sample_of_changed_records": _changed_records_sample(source_variants, output_variants),
            "sample_of_model_decisions_not_applied": model_not_applied_sample,
            "top_issue_types_still_unresolved": _top_unresolved_issue_types(report_payload),
            "final_path": FINAL_CLEAN_DATABASE_PATH,
            "source_path": SOURCE_CANONICAL_PATH,
            "source_hash_before": _sha256(SOURCE_CANONICAL_PATH),
            "final_hash_before": _sha256(FINAL_CLEAN_DATABASE_PATH),
        }
    )

    if output_count == 0:
        blocking_reasons.append("Final output is empty.")
    if not metadata:
        blocking_reasons.append("Final output metadata is missing.")
    if "vehicles" not in final_payload:
        blocking_reasons.append("Final output must contain 'vehicles'.")
    if final_payload.get("verified_variants") is not None or final_payload.get("partial_variants") is not None:
        blocking_reasons.append("Final output appears to be canonical/root structure, not final clean structure.")
    mistaken_keys = ("issues_total", "issues_by_risk", "decisions", "items")
    if any(key in final_payload for key in mistaken_keys) and "vehicles" not in final_payload:
        blocking_reasons.append("Final output appears to be a validation working file, not final clean database.")
    if any(count > 0 for count in missing_counts.values()):
        blocking_reasons.append("Final output contains variants missing required fields.")
    if duplicate_count > 0:
        blocking_reasons.append("Final output contains duplicate variant_id values.")
    if output_count < input_count:
        source_ids = {str(v.get("variant_id") or "") for v in source_variants if v.get("variant_id")}
        output_ids = {str(v.get("variant_id") or "") for v in output_variants if v.get("variant_id")}
        removed_ids = sorted(variant_id for variant_id in source_ids if variant_id not in output_ids)
        approved_rejects = _approved_reject_decisions(decisions_payload)
        unexplained = [variant_id for variant_id in removed_ids if variant_id not in approved_rejects]
        if unexplained or not removed_ids:
            blocking_reasons.append(
                "Output variant count is lower than source without approved safe reject decisions for all removals."
            )
            summary["unexplained_removed_variant_ids"] = unexplained[:25]
    if output_count > input_count:
        warnings.append("Output variant count is higher than source; review for unexpected additions.")

    summary["source_hash_after"] = _sha256(SOURCE_CANONICAL_PATH)
    summary["final_hash_after"] = _sha256(FINAL_CLEAN_DATABASE_PATH)
    return summary, blocking_reasons, warnings


def _call_openai_audit_model(model: str, audit_summary: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
    api_key = config.get("openai", "api_key")
    if not api_key:
        return dict(_JSON_SCHEMA), "OpenAI API key not configured."

    prompt = {
        "task": "Audit the final clean validation database summary and return strict JSON only.",
        "required_schema": {
            "status": "PASS | FAIL",
            "confidence": "0.0-1.0",
            "blocking_reasons": "list[str]",
            "non_blocking_warnings": "list[str]",
            "required_fixes": "list[str]",
            "summary": "string",
        },
        "rules": [
            "FAIL if data integrity or safety risks remain.",
            "FAIL if variant-loss explanation is insufficient.",
            "Never propose auto-save; save is explicit and separate.",
            "Return valid JSON only with no markdown.",
        ],
        "audit_summary": audit_summary,
    }

    request_summary = (
        f"model={model} input={audit_summary.get('total_input_variants', 0)} "
        f"output={audit_summary.get('total_output_variants', 0)}"
    )
    log_event(
        {
            "stage": "final_quality_audit",
            "event_type": "model_call_planned",
            "provider": "openai",
            "model": model,
            "status": "planned",
            "request_summary": request_summary,
        }
    )
    try:
        import openai

        client = openai.OpenAI(api_key=api_key)
        log_event(
            {
                "stage": "final_quality_audit",
                "event_type": "model_call_started",
                "provider": "openai",
                "model": model,
                "status": "started",
                "request_summary": request_summary,
            }
        )
        response = None
        raw_text = ""
        if hasattr(client, "chat") and hasattr(client.chat, "completions"):
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Return strict JSON only."},
                    {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
                ],
            )
            choices = getattr(response, "choices", None)
            if choices and isinstance(choices, list):
                first = choices[0]
                message = getattr(first, "message", None)
                raw_text = str(getattr(message, "content", "") or "")
        elif hasattr(client, "responses"):
            response = client.responses.create(model=model, input=json.dumps(prompt, ensure_ascii=False))
            raw_text = getattr(response, "output_text", "") or ""
        if not raw_text and response is not None:
            raw_text = str(response)
        parsed = _normalize_model_result(_parse_model_json(raw_text))
        log_event(
            {
                "stage": "final_quality_audit",
                "event_type": "model_call_completed",
                "provider": "openai",
                "model": model,
                "status": "ok",
                "request_summary": request_summary,
                "response_summary": f"status={parsed['status']} confidence={parsed['confidence']}",
            }
        )
        return parsed, None
    except Exception as exc:
        log_event(
            {
                "stage": "final_quality_audit",
                "event_type": "model_call_failed",
                "provider": "openai",
                "model": model,
                "status": "failed",
                "request_summary": request_summary,
                "error": str(exc),
            }
        )
        return dict(_JSON_SCHEMA), str(exc)


def audit_final_clean_database_quality() -> dict[str, Any]:
    """Run deterministic checks and a final OpenAI model quality verdict."""
    log_event(
        {
            "stage": "final_quality_audit",
            "event_type": "final_quality_audit_started",
            "status": "started",
            "request_summary": f"final_path={FINAL_CLEAN_DATABASE_PATH}",
        }
    )
    summary, blocking_reasons, warnings = _deterministic_checks()
    model_id = config.get("openai", "validator_model_id") or "gpt-5.4"

    if blocking_reasons:
        result = {
            "status": "FAIL",
            "confidence": 0.0,
            "blocking_reasons": blocking_reasons,
            "non_blocking_warnings": warnings,
            "required_fixes": [
                "Resolve deterministic blocking checks before model QA can pass.",
            ],
            "summary": "Deterministic checks failed.",
            "deterministic_summary": summary,
            "model": model_id,
        }
        log_event(
            {
                "stage": "final_quality_audit",
                "event_type": "final_quality_audit_completed",
                "provider": "openai",
                "model": model_id,
                "status": "failed",
                "response_summary": f"status={result['status']}",
            }
        )
        return result

    model_result, model_error = _call_openai_audit_model(model_id, summary)
    if model_error:
        result = {
            "status": "FAIL",
            "confidence": 0.0,
            "blocking_reasons": ["Final quality model audit failed to execute."],
            "non_blocking_warnings": warnings,
            "required_fixes": [f"Model call error: {model_error}"],
            "summary": "Final quality audit model call failed.",
            "deterministic_summary": summary,
            "model": model_id,
        }
        log_event(
            {
                "stage": "final_quality_audit",
                "event_type": "final_quality_audit_completed",
                "provider": "openai",
                "model": model_id,
                "status": "failed",
                "response_summary": "status=FAIL model_call_failed",
            }
        )
        return result

    model_result["deterministic_summary"] = summary
    model_result["model"] = model_id
    if warnings:
        model_result["non_blocking_warnings"] = list(model_result.get("non_blocking_warnings", [])) + warnings

    log_event(
        {
            "stage": "final_quality_audit",
            "event_type": "final_quality_audit_completed",
            "provider": "openai",
            "model": model_id,
            "status": "ok" if model_result.get("status") == "PASS" else "failed",
            "response_summary": f"status={model_result.get('status')} confidence={model_result.get('confidence')}",
        }
    )
    return model_result
