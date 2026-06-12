"""Deterministic QA for Gemini variant-validation responses.

Runs after every Gemini response. Never trusts the model: a response can be
forced into manual_review, sent back for a stricter retry, or rejected,
regardless of what the model claimed.

QA outcomes:
    pass            -> response is structurally and semantically acceptable
    manual_review   -> structurally valid but must be routed to manual review
    retry           -> malformed / schema-invalid; retry with stricter prompt
    reject          -> unrecoverable contradiction
"""

from __future__ import annotations

import json
import re
from typing import Any

try:
    import jsonschema
except ImportError:  # pragma: no cover - validated by smoke test
    jsonschema = None

QA_PASS = "pass"
QA_MANUAL_REVIEW = "manual_review"
QA_RETRY = "retry"
QA_REJECT = "reject"


def _norm(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    return value


def is_missing_value(value: Any, rules: dict) -> bool:
    """Rule 9: unknown / null / empty string / empty list/dict / N/A == missing."""
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {
            str(v).strip().lower() for v in rules["missing_equivalent_values"] if v is not None
        } or value.strip() == ""
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def is_generic_placeholder(value: Any, rules: dict) -> bool:
    if not isinstance(value, str):
        return False
    return value.strip().lower() in {p.lower() for p in rules["generic_placeholders"]}


def looks_like_combined_trim(trim: Any, rules: dict) -> bool:
    if not isinstance(trim, str) or not trim.strip():
        return False
    for sep in rules["combined_trim_separators"]:
        if sep in trim:
            return True
    return False


def _powertrain_contradictions(cv: dict) -> list[str]:
    """Rule 12: engine/transmission/fuel_type/drivetrain must not contradict."""
    issues = []
    engine = (cv.get("engine") or "").lower() if isinstance(cv.get("engine"), str) else ""
    fuel = (cv.get("fuel_type") or "").lower() if isinstance(cv.get("fuel_type"), str) else ""
    trans = (cv.get("transmission") or "").lower() if isinstance(cv.get("transmission"), str) else ""

    has_displacement = bool(re.search(r"\d+(\.\d+)?\s*l\b|\d{3,4}\s*cc", engine))
    is_pure_electric = fuel in {"electric", "ev", "bev"}
    engine_says_electric = "electric" in engine or re.search(r"\bkw\b|\bmotor\b", engine) is not None

    if is_pure_electric and has_displacement and "range extender" not in engine and "rex" not in engine:
        issues.append(
            f"fuel_type '{cv.get('fuel_type')}' contradicts combustion engine '{cv.get('engine')}'"
        )
    if fuel in {"petrol", "gasoline", "diesel"} and engine_says_electric and not has_displacement \
            and "hybrid" not in engine and "hybrid" not in fuel:
        issues.append(
            f"fuel_type '{cv.get('fuel_type')}' contradicts electric engine description '{cv.get('engine')}'"
        )
    if is_pure_electric and "manual" in trans:
        issues.append("electric vehicle with manual transmission is almost certainly wrong")
    return issues


def values_differ(old: Any, new: Any, rules: dict) -> bool:
    """A real change: both sides meaningful and not equal (case/space-insensitive)."""
    if is_missing_value(old, rules) or is_missing_value(new, rules):
        return False
    o, n = _norm(old), _norm(new)
    if isinstance(o, str) and isinstance(n, str):
        return o.strip().lower() != n.strip().lower()
    return o != n


def schema_validate(response: dict, schema: dict) -> list[str]:
    if jsonschema is None:
        # Minimal fallback: required top-level keys only.
        missing = [k for k in schema.get("required", []) if k not in response]
        return [f"missing required key: {k}" for k in missing]
    validator = jsonschema.Draft7Validator(schema)
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
            for e in validator.iter_errors(response)]


def run_qa(
    response: dict,
    merged_context: dict,
    rules: dict,
    schema: dict,
    grounding_enabled: bool,
) -> dict:
    """Run all deterministic QA rules. Returns
    {"status": ..., "issues": [...], "forced_decision": ...}.
    """
    issues: list[str] = []
    manual_reasons: list[str] = []
    reject_reasons: list[str] = []

    # --- Rules 1-3: structure ---
    if not isinstance(response, dict):
        return {"status": QA_RETRY, "issues": ["response is not a JSON object"],
                "forced_decision": None}

    schema_errors = schema_validate(response, schema)
    if schema_errors:
        return {"status": QA_RETRY,
                "issues": [f"schema: {e}" for e in schema_errors],
                "forced_decision": None}

    expected_id = merged_context["validation_id"]
    if response.get("validation_id") != expected_id:
        return {"status": QA_RETRY,
                "issues": [f"validation_id mismatch: expected {expected_id}, "
                           f"got {response.get('validation_id')}"],
                "forced_decision": None}

    cv = response.get("corrected_variant")
    if not isinstance(cv, dict):
        return {"status": QA_RETRY, "issues": ["corrected_variant missing or not an object"],
                "forced_decision": None}

    original = merged_context.get("standard_variant") or {}

    # --- Rules 4-5: make/model not empty ---
    for field in ("make", "model"):
        if is_missing_value(cv.get(field), rules):
            reject_reasons.append(f"corrected_variant.{field} is empty/missing")

    # --- Rule 6: year sanity ---
    ys, ye = cv.get("year_start"), cv.get("year_end")
    if isinstance(ys, int) and isinstance(ye, int) and ys > ye:
        issues.append(f"year_start {ys} > year_end {ye}")
        manual_reasons.append("year range invalid (year_start > year_end)")
    for y in (ys, ye):
        if isinstance(y, int) and not (1950 <= y <= 2030):
            manual_reasons.append(f"implausible year value {y}")

    # --- Rule 7: market_scope stays IL ---
    scope = cv.get("market_scope")
    if scope != "IL":
        ev = (response.get("evidence_summary") or "")
        if not ev or "market" not in ev.lower():
            manual_reasons.append(
                f"market_scope changed to '{scope}' without clear market-related evidence")

    # --- Rule 8: generic placeholders in critical fields ---
    for field in rules["critical_fields"]:
        if is_generic_placeholder(cv.get(field), rules):
            manual_reasons.append(f"critical field '{field}' set to generic placeholder "
                                  f"'{cv.get(field)}'")

    # --- Rule 10: IL names cannot be random translations ---
    il_filled_now = []
    for field in rules["il_name_fields"]:
        new_val = cv.get(field)
        old_val = original.get(field)
        if is_missing_value(old_val, rules) and not is_missing_value(new_val, rules):
            il_filled_now.append(field)
    name_val = response.get("name_validation") or {}
    if il_filled_now:
        model_status = name_val.get("model_name_il_status")
        if model_status not in ("verified", "corrected"):
            manual_reasons.append(
                f"IL name field(s) {il_filled_now} were filled but model_name_il_status="
                f"{model_status}")
        if is_missing_value(response.get("evidence_summary"), rules):
            manual_reasons.append(
                f"IL name field(s) {il_filled_now} were filled without evidence_summary")

    # --- Detect actual changes ourselves (never trust fields_changed alone) ---
    detected_changes = []
    for field in rules["critical_fields"]:
        if field in cv and values_differ(original.get(field), cv.get(field), rules):
            detected_changes.append(field)

    declared_changed = set(response.get("fields_changed") or [])
    evidence = response.get("evidence_summary") or ""
    confidence = response.get("confidence")
    if not isinstance(confidence, (int, float)):
        confidence = 0.0
    strong_evidence = (
        isinstance(confidence, (int, float))
        and confidence >= rules["strong_evidence_confidence_threshold"]
        and len(evidence.strip()) >= rules["min_evidence_summary_length_for_change"]
    )

    # --- Rule 11: trim cannot be silently changed ---
    if "trim" in detected_changes and "trim" not in declared_changed:
        manual_reasons.append("trim was changed but not declared in fields_changed")
    if "trim" in detected_changes and is_missing_value(evidence, rules):
        manual_reasons.append("trim was changed without evidence_summary")

    # --- Dangerous critical-field changes need strong evidence ---
    dangerous_changed = [f for f in detected_changes
                         if f in rules["dangerous_critical_fields"]]
    if dangerous_changed and not strong_evidence:
        manual_reasons.append(
            f"critical field(s) {dangerous_changed} changed without strong evidence "
            f"(confidence={confidence}, evidence_len={len(evidence.strip())})")

    # --- Rule 12: powertrain consistency ---
    for c in _powertrain_contradictions(cv):
        manual_reasons.append(f"powertrain contradiction: {c}")

    # --- Rule 13: duplicate review must be filled when a group exists ---
    dup_group = merged_context.get("possible_duplicate_group")
    dup_review = response.get("duplicate_review") or {}
    if dup_group:
        decision = dup_review.get("duplicate_decision")
        if decision in (None, "", "not_applicable"):
            manual_reasons.append(
                f"variant belongs to duplicate group {dup_group} but duplicate_review "
                f"is not filled (decision={decision})")
        elif decision == "manual_review_required":
            manual_reasons.append(f"duplicate group {dup_group} requires manual review")

    # --- Rule 14: combined trims must have split_review filled ---
    split_review = response.get("split_review") or {}
    orig_trim = original.get("trim")
    if looks_like_combined_trim(orig_trim, rules) or looks_like_combined_trim(cv.get("trim"), rules):
        if "split_recommended" not in split_review:
            return {"status": QA_RETRY,
                    "issues": ["trim looks combined but split_review.split_recommended missing"],
                    "forced_decision": None}
        if split_review.get("split_recommended") is True:
            manual_reasons.append(
                f"split recommended for combined trim '{orig_trim or cv.get('trim')}'")
        elif is_missing_value(split_review.get("split_reason"), rules):
            manual_reasons.append(
                f"trim '{orig_trim or cv.get('trim')}' looks combined but split_review has "
                f"no reasoning")

    if split_review.get("split_recommended") is True:
        manual_reasons.append("model recommends splitting this row into multiple trims")

    # --- Grounding conservatism ---
    if not grounding_enabled:
        risky_activity = (
            bool(response.get("fields_completed"))
            or bool(detected_changes)
            or name_val.get("model_name_il_status") == "corrected"
            or name_val.get("trim_name_il_status") == "corrected"
        )
        if risky_activity:
            manual_reasons.append(
                "grounding unavailable for this run but fields were completed/changed; "
                "routing to manual review for safety")

    # --- Model-flagged states ---
    if response.get("is_real_variant") is False:
        reject_reasons.append("model determined the variant is not real")
    if response.get("decision") == "reject":
        reject_reasons.append(
            f"model rejected: {response.get('manual_review_reason') or evidence or 'no reason'}")

    # --- Rules 15-16: decision gating ---
    forced_decision = None
    if reject_reasons:
        issues.extend(reject_reasons)
        return {"status": QA_REJECT, "issues": issues + manual_reasons,
                "forced_decision": "reject"}

    if manual_reasons:
        issues.extend(manual_reasons)
        forced_decision = "manual_review"
    elif response.get("requires_manual_review") is True:
        forced_decision = "manual_review"
        issues.append(f"model requested manual review: "
                      f"{response.get('manual_review_reason') or 'unspecified'}")
    elif confidence < rules["confidence_auto_accept_threshold"]:
        forced_decision = "manual_review"
        issues.append(f"confidence {confidence} below auto-accept threshold "
                      f"{rules['confidence_auto_accept_threshold']}")
    elif response.get("decision") == "manual_review":
        forced_decision = "manual_review"

    if forced_decision == "manual_review":
        return {"status": QA_MANUAL_REVIEW, "issues": issues,
                "forced_decision": "manual_review"}

    return {"status": QA_PASS, "issues": issues, "forced_decision": "auto_accept"}


def parse_strict_json(text: str) -> dict:
    """Parse a model response that must be strict JSON.

    Tolerates accidental markdown fences / surrounding prose by extracting the
    outermost JSON object, but the content itself must be valid JSON.
    Raises ValueError when no valid JSON object can be extracted.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("empty model response")
    candidate = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", candidate, re.DOTALL)
    if fence:
        candidate = fence.group(1)
    else:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("no JSON object found in model response")
        candidate = candidate[start:end + 1]
    parsed = json.loads(candidate)
    if not isinstance(parsed, dict):
        raise ValueError("model response JSON is not an object")
    return parsed
