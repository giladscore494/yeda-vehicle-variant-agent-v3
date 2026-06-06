"""Minimal deterministic-first validation pipeline.

This module implements the Task 2 backend flow:

    Source canonical -> deterministic audit -> issue queue -> decisions

It deliberately does not call AI providers, does not mutate the source canonical,
and does not export the reserved final clean database.
"""
from __future__ import annotations

import json
import re
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.paths import (
    DECISIONS_PATH,
    FINAL_CLEAN_DATABASE_PATH,
    ISSUE_QUEUE_PATH,
    MANIFEST_PATH,
    SOURCE_CANONICAL_PATH,
    VALIDATION_REPORT_PATH,
)
from engine.validation.normalizer import extract_value, extract_year
from engine.validation.run_events import log_event
from engine.validation.write_guard import safe_write_json

_RISK_LEVELS = ("critical", "high", "medium", "low")
_CRITICAL_FIELDS = ("variant_id", "make", "model", "year_start", "year_end", "market")
_IDENTITY_FIELDS = (
    "make",
    "model",
    "year_start",
    "year_end",
    "generation",
    "trim",
    "engine",
    "transmission",
    "fuel_type",
    "body_type",
    "market",
)
_EVIDENCE_FIELDS = ("body_type", "seats", "engine", "transmission", "fuel_type", "drivetrain", "trim")
_SOURCE_CONFLICT_FIELDS = ("generation", *_EVIDENCE_FIELDS)
_CURRENT_YEAR = 2026
_MIN_YEAR = 1886
_MAX_REASONABLE_FUTURE_YEAR = _CURRENT_YEAR + 2


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _source_variant_count(source_data: dict) -> int:
    return len(source_data.get("verified_variants") or []) + len(source_data.get("partial_variants") or [])


def _value(value: Any) -> Any:
    return extract_value(value)


def _clean_str(value: Any) -> str:
    raw = _value(value)
    if raw is None:
        return ""
    return str(raw).strip()


def _norm(value: Any) -> str:
    return re.sub(r"\s+", " ", _clean_str(value).casefold()).strip()


def _norm_identity(value: Any) -> str:
    text = _norm(value)
    text = text.replace("&", "and").replace("+", "plus")
    text = re.sub(r"[\s/_-]+", " ", text)
    return text.strip()


def _field_source_count(value: Any) -> int:
    if isinstance(value, dict):
        raw = value.get("sources_count")
        if isinstance(raw, int):
            return raw
        source_ids = value.get("source_ids")
        if isinstance(source_ids, list):
            return len([sid for sid in source_ids if str(sid).strip()])
    return 0


def _variant_source_count(variant: dict) -> int:
    raw = variant.get("sources_count")
    if isinstance(raw, int):
        return raw
    source_ids = variant.get("source_ids")
    if isinstance(source_ids, list):
        return len([sid for sid in source_ids if str(sid).strip()])
    return sum(_field_source_count(variant.get(field)) for field in _EVIDENCE_FIELDS)


def _variant_years(variant: dict) -> str:
    ys = extract_year(variant.get("year_start"))
    ye = extract_year(variant.get("year_end"))
    if ys is None and ye is None:
        return ""
    if ys is None:
        return f"?-{ye}"
    if ye is None:
        return f"{ys}-?"
    return f"{ys}-{ye}"


def _variant_identity_key(variant: dict) -> tuple[str, ...]:
    key: list[str] = []
    for field in _IDENTITY_FIELDS:
        if field in ("year_start", "year_end"):
            key.append(str(extract_year(variant.get(field)) or ""))
        else:
            key.append(_norm_identity(variant.get(field)))
    return tuple(key)


def _seed_parts(seed_id: str) -> dict[str, Any]:
    parts = seed_id.split("__")
    if len(parts) < 5:
        return {"make": "", "model": "", "year_start": None, "year_end": None}
    return {
        "make": parts[0].replace("_", " ").title(),
        "model": parts[1].replace("_", " ").title(),
        "year_start": int(parts[2]) if parts[2].isdigit() else None,
        "year_end": int(parts[3]) if parts[3].isdigit() else None,
    }


def _variant_base(variant: dict) -> dict[str, Any]:
    return {
        "scope": "variant",
        "seed_id": _clean_str(variant.get("seed_id")),
        "variant_ids": [_clean_str(variant.get("variant_id"))] if _clean_str(variant.get("variant_id")) else [],
        "make": _clean_str(variant.get("make")),
        "model": _clean_str(variant.get("model")),
        "years": _variant_years(variant),
    }


def _has_useful_evidence(variant: dict) -> bool:
    if _variant_source_count(variant) > 0:
        return True
    for field in _EVIDENCE_FIELDS:
        if _field_source_count(variant.get(field)) > 0:
            return True
    return False


def _alias_mismatches(left: str, right: str) -> list[str]:
    mismatches: list[str] = []
    l, r = left.casefold(), right.casefold()
    if ("&" in left or "&" in right) and re.sub(r"\s*&\s*", " and ", l) == re.sub(r"\s*&\s*", " and ", r):
        mismatches.append("&_vs_and")
    if ("+" in left or "+" in right) and l.replace("+", "plus") == r.replace("+", "plus"):
        mismatches.append("plus_vs_+")
    if (("/" in left or "/" in right) and l.replace("/", "-") == r.replace("/", "-")):
        mismatches.append("slash_vs_hyphen")
    kgm_aliases = {"kgm", "k g m", "kg mobility", "ssangyong", "ssang yong"}
    if _norm_identity(left) in kgm_aliases and _norm_identity(right) in kgm_aliases and _norm_identity(left) != _norm_identity(right):
        mismatches.append("kgm_vs_ssangyong")
    return mismatches


def _has_source_conflict(field: Any) -> bool:
    if not isinstance(field, dict):
        return False
    if field.get("conflict") or field.get("source_conflict") or field.get("has_conflict"):
        return True
    status = _norm(field.get("status"))
    reason = _norm(field.get("reason"))
    return "conflict" in status or "conflict" in reason or "contradict" in reason


def build_issue_queue(source_data: dict) -> list[dict]:
    """Build compact issue queue rows for problematic source items only."""
    raw_items: list[dict[str, Any]] = []

    def add_issue(
        *,
        issue_type: str,
        risk_level: str,
        recommended_action: str,
        reason: str,
        evidence_summary: str,
        requires_model_review: bool = False,
        requires_manual_review: bool = False,
        deterministic_safe_fix: bool = False,
        **base: Any,
    ) -> None:
        if risk_level not in _RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {risk_level}")
        raw_items.append(
            {
                "scope": base.get("scope", "variant"),
                "seed_id": base.get("seed_id", ""),
                "variant_ids": base.get("variant_ids", []),
                "make": base.get("make", ""),
                "model": base.get("model", ""),
                "years": base.get("years", ""),
                "issue_type": issue_type,
                "risk_level": risk_level,
                "requires_model_review": bool(requires_model_review),
                "requires_manual_review": bool(requires_manual_review),
                "recommended_action": recommended_action,
                "reason": reason,
                "evidence_summary": evidence_summary,
                "deterministic_safe_fix": bool(deterministic_safe_fix),
            }
        )

    if not isinstance(source_data, dict):
        add_issue(
            scope="group",
            issue_type="invalid_source_structure",
            risk_level="critical",
            recommended_action="repair_source_json",
            reason="Source canonical root is not a JSON object.",
            evidence_summary=f"root_type={type(source_data).__name__}",
            requires_manual_review=True,
        )
        return _assign_item_ids(raw_items)

    verified = source_data.get("verified_variants") or []
    partial = source_data.get("partial_variants") or []
    all_variants = [v for v in [*verified, *partial] if isinstance(v, dict)]

    seen_variant_ids: dict[str, dict] = {}
    seen_identities: dict[tuple[str, ...], dict] = {}
    variants_by_seed: dict[str, list[dict]] = defaultdict(list)

    for variant in all_variants:
        base = _variant_base(variant)
        vid = _clean_str(variant.get("variant_id"))
        seed_id = _clean_str(variant.get("seed_id"))
        if seed_id:
            variants_by_seed[seed_id].append(variant)

        missing = [field for field in _CRITICAL_FIELDS if not _clean_str(variant.get(field))]
        if missing:
            add_issue(
                **base,
                issue_type="missing_critical_fields",
                risk_level="critical",
                recommended_action="manual_repair_required_fields",
                reason="Variant is missing fields required to establish identity.",
                evidence_summary="missing=" + ",".join(missing),
                requires_manual_review=True,
                deterministic_safe_fix=False,
            )

        ys = extract_year(variant.get("year_start"))
        ye = extract_year(variant.get("year_end"))
        if ys is not None and ye is not None:
            suspicious_reason = ""
            if ys > ye:
                suspicious_reason = "year_start is after year_end"
            elif ys < _MIN_YEAR or ye > _MAX_REASONABLE_FUTURE_YEAR:
                suspicious_reason = "year range falls outside plausible vehicle bounds"
            elif ye - ys > 40:
                suspicious_reason = "year range is unusually broad"
            if suspicious_reason:
                add_issue(
                    **base,
                    issue_type="suspicious_year_range",
                    risk_level="high",
                    recommended_action="verify_year_range",
                    reason=suspicious_reason,
                    evidence_summary=f"year_start={ys}; year_end={ye}",
                    requires_model_review=True,
                    requires_manual_review=True,
                )

        if vid:
            previous = seen_variant_ids.get(vid)
            if previous is not None:
                add_issue(
                    **{**base, "scope": "group", "variant_ids": [previous.get("variant_id", ""), vid]},
                    issue_type="duplicate_variant_identity",
                    risk_level="high",
                    recommended_action="merge_or_remove_duplicate_variant",
                    reason="The same variant_id appears more than once.",
                    evidence_summary=f"variant_id={vid}",
                    requires_manual_review=True,
                    deterministic_safe_fix=False,
                )
            else:
                seen_variant_ids[vid] = variant

        identity_key = _variant_identity_key(variant)
        if any(identity_key):
            previous = seen_identities.get(identity_key)
            if previous is not None and _clean_str(previous.get("variant_id")) != vid:
                add_issue(
                    **{**base, "scope": "group", "variant_ids": [_clean_str(previous.get("variant_id")), vid]},
                    issue_type="duplicate_variant_identity",
                    risk_level="high",
                    recommended_action="merge_or_differentiate_duplicate_identity",
                    reason="Two variants share the same normalized identity fields.",
                    evidence_summary="identity_fields=" + ",".join(_IDENTITY_FIELDS),
                    requires_manual_review=True,
                )
            else:
                seen_identities[identity_key] = variant

        evidence_count = _variant_source_count(variant)
        verification_status = _norm(variant.get("verification_status"))
        confidence = _norm(variant.get("confidence"))
        if verification_status == "verified" and evidence_count <= 0 and not _has_useful_evidence(variant):
            add_issue(
                **base,
                issue_type="stale_or_weak_source_evidence",
                risk_level="high",
                recommended_action="add_current_source_evidence_or_downgrade",
                reason="Verified variant has no usable source evidence.",
                evidence_summary=f"verification_status=verified; sources_count={evidence_count}",
                requires_model_review=True,
                requires_manual_review=True,
            )
        elif verification_status == "partial" and evidence_count < 2:
            add_issue(
                **base,
                issue_type="partial_variant_too_little_evidence",
                risk_level="high",
                recommended_action="collect_more_evidence_before_promotion",
                reason="Partial variant has too little supporting evidence.",
                evidence_summary=f"verification_status=partial; sources_count={evidence_count}",
                requires_model_review=True,
                requires_manual_review=False,
            )
        elif confidence == "high" and evidence_count <= 0:
            add_issue(
                **base,
                issue_type="stale_or_weak_source_evidence",
                risk_level="medium",
                recommended_action="add_evidence_or_lower_confidence",
                reason="High confidence item has no explicit evidence count.",
                evidence_summary=f"confidence=high; sources_count={evidence_count}",
                requires_model_review=True,
            )

        market = _clean_str(variant.get("market"))
        if market and market.upper() != "IL":
            add_issue(
                **base,
                issue_type="market_plausibility_gap",
                risk_level="medium",
                recommended_action="confirm_market_or_move_to_global_reference",
                reason="Variant is in the Israel canonical file but is not marked for the IL market.",
                evidence_summary=f"market={market}",
                requires_model_review=True,
                requires_manual_review=True,
            )

        for field in _SOURCE_CONFLICT_FIELDS:
            if _has_source_conflict(variant.get(field)):
                add_issue(
                    **base,
                    issue_type="source_conflict",
                    risk_level="high",
                    recommended_action="resolve_conflicting_sources",
                    reason=f"Field {field} records conflicting source evidence.",
                    evidence_summary=f"field={field}; value={_clean_str(variant.get(field))}",
                    requires_model_review=True,
                    requires_manual_review=True,
                )

        aliases = variant.get("aliases") if isinstance(variant.get("aliases"), list) else []
        canonical_names = [_clean_str(variant.get("make")), _clean_str(variant.get("model"))]
        for alias in aliases:
            alias_text = _clean_str(alias)
            for canonical_text in canonical_names:
                mismatches = _alias_mismatches(alias_text, canonical_text)
                if mismatches:
                    add_issue(
                        **base,
                        issue_type="unsafe_alias_mismatch",
                        risk_level="medium",
                        recommended_action="manual_alias_identity_check",
                        reason="Alias differs from canonical identity by a potentially unsafe token substitution.",
                        evidence_summary=f"alias={alias_text}; canonical={canonical_text}; mismatch={','.join(mismatches)}",
                        requires_manual_review=True,
                    )

    batch_state = source_data.get("batch_state") if isinstance(source_data.get("batch_state"), dict) else {}
    seed_ids = set()
    for key in ("processed_seed_ids", "failed_seed_ids", "needs_retry_seed_ids", "manual_review_seed_ids", "zero_variant_seed_ids"):
        values = batch_state.get(key) or []
        if isinstance(values, list):
            seed_ids.update(str(value).strip() for value in values if str(value).strip())
    no_variants_by_seed = batch_state.get("no_variants_by_seed") or {}
    if isinstance(no_variants_by_seed, dict):
        seed_ids.update(str(seed_id).strip() for seed_id in no_variants_by_seed if str(seed_id).strip())

    for seed_id in sorted(seed_ids):
        if seed_id in variants_by_seed:
            continue
        parts = _seed_parts(seed_id)
        years = ""
        if parts["year_start"] or parts["year_end"]:
            years = f"{parts['year_start'] or '?'}-{parts['year_end'] or '?'}"
        add_issue(
            scope="seed",
            seed_id=seed_id,
            variant_ids=[],
            make=parts["make"],
            model=parts["model"],
            years=years,
            issue_type="seed_exists_but_no_variants",
            risk_level="medium",
            recommended_action="retry_seed_or_mark_intentional_zero_variant",
            reason="Seed is present in source accounting but has no variants in canonical lists.",
            evidence_summary=f"seed_id={seed_id}",
            requires_manual_review=True,
        )

    return _assign_item_ids(raw_items)


def _assign_item_ids(items: list[dict]) -> list[dict]:
    for idx, item in enumerate(items, start=1):
        item["item_id"] = f"iq_{idx:06d}"
    return items


def _summarize_queue(queue: list[dict], source_data: dict, *, run_id: str | None = None) -> dict[str, Any]:
    issues_by_risk = {risk: 0 for risk in _RISK_LEVELS}
    for item in queue:
        issues_by_risk[item["risk_level"]] += 1
    verified_count = len(source_data.get("verified_variants") or []) if isinstance(source_data, dict) else 0
    partial_count = len(source_data.get("partial_variants") or []) if isinstance(source_data, dict) else 0
    issue_type_counts = Counter(item["issue_type"] for item in queue)
    return {
        "run_id": run_id or f"audit_{uuid.uuid4().hex[:12]}",
        "source_file": SOURCE_CANONICAL_PATH,
        "source_variant_count": verified_count + partial_count,
        "verified_count": verified_count,
        "partial_count": partial_count,
        "issues_total": len(queue),
        "issues_by_risk": issues_by_risk,
        "model_review_items_available": sum(1 for item in queue if item["requires_model_review"]),
        "manual_review_items_available": sum(1 for item in queue if item["requires_manual_review"]),
        "top_issue_types": [
            {"issue_type": issue_type, "count": count}
            for issue_type, count in issue_type_counts.most_common(10)
        ],
    }


def write_validation_outputs(queue: list[dict], summary: dict) -> None:
    """Write issue queue, decisions, manifest, and compact validation report."""
    started_at = summary.get("started_at") or _utc_now()
    completed_at = summary.get("completed_at") or _utc_now()

    queue_doc = {
        "created_at": completed_at,
        "source_file": SOURCE_CANONICAL_PATH,
        "source_variant_count": int(summary["source_variant_count"]),
        "items": queue,
    }
    safe_write_json(queue_doc, ISSUE_QUEUE_PATH)

    decisions_path = Path(DECISIONS_PATH)
    if not decisions_path.exists():
        safe_write_json(
            {
                "created_at": completed_at,
                "source_file": SOURCE_CANONICAL_PATH,
                "decisions": [],
            },
            DECISIONS_PATH,
        )

    manifest = {
        "run_id": summary["run_id"],
        "stage": "audit",
        "source_file": SOURCE_CANONICAL_PATH,
        "started_at": started_at,
        "completed_at": completed_at,
        "source_variant_count": int(summary["source_variant_count"]),
        "issues_total": int(summary["issues_total"]),
        "issues_by_risk": summary["issues_by_risk"],
        "model_review_items_available": int(summary["model_review_items_available"]),
        "final_clean_database_path": FINAL_CLEAN_DATABASE_PATH,
    }
    safe_write_json(manifest, MANIFEST_PATH)

    report = {
        "source_variant_count": int(summary["source_variant_count"]),
        "verified_count": int(summary["verified_count"]),
        "partial_count": int(summary["partial_count"]),
        "issues_total": int(summary["issues_total"]),
        "issues_by_risk": summary["issues_by_risk"],
        "model_review_items_available": int(summary["model_review_items_available"]),
        "manual_review_items_available": int(summary["manual_review_items_available"]),
        "top_issue_types": summary["top_issue_types"],
    }
    safe_write_json(report, VALIDATION_REPORT_PATH)


def run_full_audit() -> dict:
    """Run the deterministic audit over the full source canonical file."""
    started_at = _utc_now()
    log_event(
        {
            "stage": "audit",
            "event_type": "audit_started",
            "status": "started",
            "request_summary": f"source={SOURCE_CANONICAL_PATH}",
        }
    )
    source_path = Path(SOURCE_CANONICAL_PATH)
    source_data = json.loads(source_path.read_text(encoding="utf-8"))
    queue = build_issue_queue(source_data)
    completed_at = _utc_now()
    summary = _summarize_queue(queue, source_data)
    summary["started_at"] = started_at
    summary["completed_at"] = completed_at
    write_validation_outputs(queue, summary)
    result = {
        "run_id": summary["run_id"],
        "source_file": SOURCE_CANONICAL_PATH,
        "source_variant_count": summary["source_variant_count"],
        "issues_total": summary["issues_total"],
        "issues_by_risk": summary["issues_by_risk"],
        "model_review_items_available": summary["model_review_items_available"],
        "manual_review_items_available": summary["manual_review_items_available"],
    }
    log_event(
        {
            "stage": "audit",
            "event_type": "audit_completed",
            "status": "ok",
            "request_summary": f"source={SOURCE_CANONICAL_PATH}",
            "response_summary": f"issues_total={summary['issues_total']}",
        }
    )
    return result
