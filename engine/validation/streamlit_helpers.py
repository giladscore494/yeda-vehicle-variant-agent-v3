"""Backend payload helpers for the simplified Streamlit validation UI.

The Streamlit app should use these functions instead of reading or shaping raw
validation files directly.  These helpers are intentionally compact and
read-only except for the explicit pipeline/model runner wrappers.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.paths import (
    AI_OUTCOME_AUDITS_PATH,
    DIFF_AUDITS_PATH,
    FINAL_CLEAN_DATABASE_PATH,
    ISSUE_QUEUE_PATH,
    MANIFEST_PATH,
    MODEL_REVIEW_PROGRESS_PATH,
    PATCH_APPLICATIONS_PATH,
    PATCHES_PATH,
    VALIDATION_REPORT_PATH,
    DECISIONS_PATH,
)
from engine.validation.final_github_save import save_final_clean_database_to_github as _save_final_clean_database_to_github
from engine.validation.diff_quality_audit import audit_last_patch_diff_with_openai as _audit_last_patch_diff_with_openai
from engine.validation.final_quality_audit import audit_final_clean_database_quality as _audit_final_clean_database_quality
from engine.validation.file_status import load_database_file_status
from engine.validation.minimal_pipeline import run_full_audit
from engine.validation.model_review_runner import run_model_review
from engine.validation.model_review_runner import backfill_change_decisions_for_completed_ai_reviews as _backfill_change_decisions
from engine.validation.model_review_progress import load_model_review_progress, refresh_model_review_progress
from engine.validation.ai_outcome_audit import (
    audit_next_ai_review_outcome_with_openai as _audit_next_ai_review_outcome_with_openai,
    queue_completed_decisions_for_outcome_audit as _queue_completed_decisions_for_outcome_audit,
)
from engine.validation.final_export import export_final_clean_database as _export_final_clean_database
from engine.validation.run_events import load_recent_events
from engine.validation.surgical_patches import (
    apply_next_safe_patch as _apply_next_safe_patch,
    build_candidate_patches_from_decisions as _build_candidate_patches_from_decisions,
)
from engine.validation.working_copy import (
    initialize_working_copy as _initialize_working_copy,
    reset_working_copy_from_canonical as _reset_working_copy_from_canonical,
)

QUEUE_PREVIEW_COLUMNS = (
    "item_id",
    "make",
    "model",
    "years",
    "issue_type",
    "risk_level",
    "recommended_action",
    "requires_model_review",
)
AI_PREVIEW_COLUMNS = (
    "item_id",
    "make",
    "model",
    "issue_type",
    "risk_level",
    "routing_policy",
    "primary_provider",
    "second_opinion_provider",
    "max_expected_calls",
)
AI_DECISION_OUTCOME_COLUMNS = (
    "item_id",
    "make",
    "model",
    "years",
    "change_decision",
    "change_severity",
    "patchable",
    "patchability_reason",
    "change_reason",
)
DEFAULT_QUEUE_PREVIEW_LIMIT = 25
DEFAULT_AI_PREVIEW_LIMIT = 10
SEEDS_PATH = "data/seeds/vehicle_model_seeds_il.json"


def _load_json_file(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

def _load_jsonl_file(path: Path) -> list[dict]:
    rows: list[dict] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return rows
    for line in lines:
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def _mtime_iso(path: Path) -> str | None:
    try:
        from datetime import datetime, timezone

        return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()
    except OSError:
        return None


def final_banner_status(file_status: dict) -> dict:
    """Return the final clean database banner state and display message."""
    final_path = file_status.get("final_path", "data/final/resume_package_final_clean.json")
    if not file_status.get("final_exists"):
        return {
            "state": "missing",
            "message": "No final clean database exported yet",
        }
    if file_status.get("final_is_older_than_source"):
        return {
            "state": "stale",
            "message": "Final clean database is older than source canonical — re-export required",
        }
    return {
        "state": "exists",
        "message": f"Final clean database exists: {final_path}",
    }


def _seed_count(project_root: str | Path = ".") -> int | None:
    payload = _load_json_file(Path(project_root) / SEEDS_PATH)
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        seeds = payload.get("seeds")
        if isinstance(seeds, list):
            return len(seeds)
    return None


def load_status_payload(project_root: str | Path = ".") -> dict:
    """Build the minimal status payload consumed by the Streamlit app."""
    root = Path(project_root)
    file_status = load_database_file_status(root)
    report = _load_json_file(root / VALIDATION_REPORT_PATH) or {}
    manifest = _load_json_file(root / MANIFEST_PATH) or {}
    queue_items = _load_issue_queue_items(root)
    model_progress = (
        refresh_model_review_progress(queue_items, path=root / MODEL_REVIEW_PROGRESS_PATH)
        if queue_items
        else (_load_json_file(root / MODEL_REVIEW_PROGRESS_PATH) or {})
    )
    issues_by_risk = report.get("issues_by_risk") if isinstance(report, dict) else {}
    if not isinstance(issues_by_risk, dict):
        issues_by_risk = {}

    payload = {
        "final_banner": final_banner_status(file_status),
        "source": {
            "source_path": file_status.get("source_path"),
            "source_exists": file_status.get("source_exists", False),
            "source_variant_count": file_status.get("source_variant_count", 0),
            "source_verified_count": file_status.get("source_verified_count", 0),
            "source_partial_count": file_status.get("source_partial_count", 0),
            "seed_count": _seed_count(root),
            "stale_root_exists": file_status.get("stale_root_exists", False),
            "stale_root_variant_count": file_status.get("stale_root_variant_count"),
            "stale_root_is_stale": file_status.get("stale_root_is_stale", False),
            "working_path": file_status.get("working_path"),
            "working_exists": file_status.get("working_exists", False),
            "working_variant_count": file_status.get("working_variant_count", 0),
            "active_database_path": file_status.get("active_database_path"),
            "active_database_variant_count": file_status.get("active_database_variant_count", 0),
        },
        "validation_summary": {
            "issues_total": int(report.get("issues_total", 0)) if isinstance(report, dict) else 0,
            "critical": int(issues_by_risk.get("critical", 0) or 0),
            "high": int(issues_by_risk.get("high", 0) or 0),
            "medium": int(issues_by_risk.get("medium", 0) or 0),
            "low": int(issues_by_risk.get("low", 0) or 0),
            "model_review_items_available": int(report.get("model_review_items_available", 0)) if isinstance(report, dict) else 0,
            "manual_review_items_available": int(report.get("manual_review_items_available", 0)) if isinstance(report, dict) else 0,
            "last_run_time": manifest.get("completed_at") or manifest.get("started_at") or _mtime_iso(root / VALIDATION_REPORT_PATH),
        },
        "model_review_progress": {
            "total_model_review_items": int(model_progress.get("total_model_review_items", 0))
            if isinstance(model_progress, dict)
            else 0,
            "remaining_items": int(model_progress.get("remaining_items", 0))
            if isinstance(model_progress, dict)
            else 0,
            "total_model_review_variants": int(model_progress.get("total_model_review_variants", 0))
            if isinstance(model_progress, dict)
            else 0,
            "remaining_variants": int(model_progress.get("remaining_variants", 0))
            if isinstance(model_progress, dict)
            else 0,
        },
        "paths": {
            "issue_queue": ISSUE_QUEUE_PATH,
            "manifest": MANIFEST_PATH,
            "validation_report": VALIDATION_REPORT_PATH,
            "decisions": DECISIONS_PATH,
            "model_review_progress": MODEL_REVIEW_PROGRESS_PATH,
            "patches": PATCHES_PATH,
            "patch_applications": PATCH_APPLICATIONS_PATH,
            "diff_audits": DIFF_AUDITS_PATH,
        },
    }
    return payload


def _years_text(item: dict) -> str:
    year_start = item.get("year_start", "")
    year_end = item.get("year_end", "")
    if year_start and year_end:
        return f"{year_start}–{year_end}"
    return str(year_start or year_end or "")


def _compact_queue_row(item: dict) -> dict:
    return {
        "item_id": item.get("item_id", ""),
        "make": item.get("make", ""),
        "model": item.get("model", ""),
        "years": _years_text(item),
        "issue_type": item.get("issue_type", ""),
        "risk_level": item.get("risk_level", ""),
        "recommended_action": item.get("recommended_action", "manual_review"),
        "requires_model_review": bool(item.get("requires_model_review", False)),
    }


def _load_issue_queue_items(project_root: str | Path = ".") -> list[dict]:
    payload = _load_json_file(Path(project_root) / ISSUE_QUEUE_PATH)
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        return [item for item in payload.get("items", []) if isinstance(item, dict)]
    return []


def load_queue_preview(max_rows: int = DEFAULT_QUEUE_PREVIEW_LIMIT, project_root: str | Path = ".") -> dict:
    """Return a compact, truncated issue queue preview."""
    max_rows = max(0, int(max_rows))
    items = _load_issue_queue_items(project_root)
    return {
        "total_items": len(items),
        "max_rows": max_rows,
        "rows": [_compact_queue_row(item) for item in items[:max_rows]],
        "columns": list(QUEUE_PREVIEW_COLUMNS),
    }


def load_queue_filter_options(project_root: str | Path = ".") -> dict:
    """Return compact filter options derived from the backend issue queue."""
    items = _load_issue_queue_items(project_root)
    return {
        "risk_levels": sorted({str(item.get("risk_level")) for item in items if item.get("risk_level")}),
        "issue_types": sorted({str(item.get("issue_type")) for item in items if item.get("issue_type")}),
    }


def _compact_ai_row(item: dict) -> dict:
    return {column: item.get(column, "") for column in AI_PREVIEW_COLUMNS}


def load_ai_preview(
    max_items: int,
    risk_levels: list[str] | None = None,
    issue_types: list[str] | None = None,
    seed_id_filter: str | None = None,
    max_rows: int = DEFAULT_AI_PREVIEW_LIMIT,
) -> dict:
    """Return a dry-run model routing preview, truncated for UI display."""
    result = run_model_review(
        max_items=max_items,
        risk_levels=risk_levels,
        issue_types=issue_types,
        seed_id_filter=seed_id_filter or None,
        dry_run=True,
    )
    rows = [_compact_ai_row(item) for item in result.get("items", [])[: max(0, int(max_rows))]]
    return {
        **result,
        "rows": rows,
        "columns": list(AI_PREVIEW_COLUMNS),
        "max_rows": max_rows,
        "displayed_items": len(rows),
    }


def run_ai_review(
    max_items: int,
    risk_levels: list[str] | None = None,
    issue_types: list[str] | None = None,
    seed_id_filter: str | None = None,
) -> dict:
    """Run model review through the backend runner only."""
    return run_model_review(
        max_items=max_items,
        risk_levels=risk_levels,
        issue_types=issue_types,
        seed_id_filter=seed_id_filter or None,
        dry_run=False,
    )


def _load_decisions_list(project_root: str | Path = ".") -> tuple[list[dict], str | None]:
    decisions_path = Path(project_root) / DECISIONS_PATH
    if not decisions_path.exists():
        return [], None
    try:
        payload = json.loads(decisions_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], f"Failed to load {DECISIONS_PATH}: {exc}"
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)], None
    if isinstance(payload, dict):
        raw = payload.get("decisions", [])
        if isinstance(raw, list):
            return [item for item in raw if isinstance(item, dict)], None
        return [], f"{DECISIONS_PATH} must contain a decisions list"
    return [], f"{DECISIONS_PATH} must be a JSON object or array"


def _next_pending_model_review_item_id(project_root: str | Path = ".") -> str | None:
    progress = load_model_review_progress(path=Path(project_root) / MODEL_REVIEW_PROGRESS_PATH)
    items = progress.get("items") if isinstance(progress.get("items"), dict) else {}
    pending_ids = [
        item_id
        for item_id, item in items.items()
        if isinstance(item, dict) and item.get("status") == "pending"
    ]
    return sorted(pending_ids)[0] if pending_ids else None


def is_current_model_review_phase_complete(project_root: str | Path = ".") -> dict:
    progress = load_model_review_progress(path=Path(project_root) / MODEL_REVIEW_PROGRESS_PATH)
    remaining_items = int(progress.get("remaining_items", 0)) if isinstance(progress, dict) else 0
    decisions, _ = _load_decisions_list(project_root)
    pending_outcome_audits = 0
    failed_outcome_audits = 0
    for decision in decisions:
        status = str(decision.get("outcome_audit_status") or "").strip().lower()
        if status == "pending":
            pending_outcome_audits += 1
        elif status == "failed":
            failed_outcome_audits += 1
    complete = remaining_items == 0 and pending_outcome_audits == 0
    if complete:
        message = "Current model-review phase is complete. Deep deterministic scan can run."
    else:
        message = "Finish the current 3 model-review items and GPT-5.4 outcome audits before running the deep deterministic scan."
    return {
        "complete": complete,
        "remaining_model_review_items": remaining_items,
        "pending_outcome_audits": pending_outcome_audits,
        "failed_outcome_audits": failed_outcome_audits,
        "message": message,
    }


def load_current_model_review_phase(project_root: str | Path = ".") -> dict:
    progress = load_model_review_progress(path=Path(project_root) / MODEL_REVIEW_PROGRESS_PATH)
    phase = is_current_model_review_phase_complete(project_root)
    total = int(progress.get("total_model_review_items", 0)) if isinstance(progress, dict) else 0
    completed = int(progress.get("completed_items", 0)) if isinstance(progress, dict) else 0
    remaining = int(progress.get("remaining_items", 0)) if isinstance(progress, dict) else 0
    return {
        **phase,
        "total_model_review_items": total,
        "completed_model_review_items": completed,
        "remaining_model_review_items": remaining,
        "next_item_id": _next_pending_model_review_item_id(project_root),
    }


def run_audit_and_refresh_queue(project_root: str | Path = ".") -> dict:
    """Run the deterministic backend audit that also refreshes the review queue."""
    phase = is_current_model_review_phase_complete(project_root)
    if phase["remaining_model_review_items"] > 0 or phase["pending_outcome_audits"] > 0:
        return {"ok": False, "error": "deep_scan_blocked", "message": phase["message"], "phase": phase}
    return run_full_audit()


def initialize_working_copy() -> dict:
    """Initialize the active working copy from canonical if needed."""
    return _initialize_working_copy(force=False)


def reset_working_copy_from_canonical(confirm: bool = False) -> dict:
    """Reset the active working copy from canonical when explicitly confirmed."""
    return _reset_working_copy_from_canonical(confirm=confirm)


def load_model_progress() -> dict:
    """Load model-review progress summary."""
    return load_model_review_progress()


def build_candidate_surgical_patches() -> dict:
    """Build candidate surgical patches from exact decisions."""
    return _build_candidate_patches_from_decisions()


def build_candidate_patches() -> dict:
    """Backwards-compatible alias for surgical patch candidate builder."""
    return _build_candidate_patches_from_decisions()


def apply_next_safe_surgical_patch() -> dict:
    """Apply exactly one pending safe candidate patch to the active working copy."""
    return _apply_next_safe_patch()


def apply_next_safe_patch() -> dict:
    """Backwards-compatible alias for applying one pending safe patch."""
    return _apply_next_safe_patch()


def audit_last_surgical_patch_diff() -> dict:
    """Audit the last applied surgical patch diff with GPT-5.4."""
    return _audit_last_patch_diff_with_openai()


def audit_last_patch_diff_with_openai() -> dict:
    """Backwards-compatible alias for last surgical diff audit."""
    return _audit_last_patch_diff_with_openai()


def load_surgical_patch_summary(project_root: str | Path = ".") -> dict:
    """Return counts and last patch/audit details for the main UI."""
    root = Path(project_root)
    patches_path = root / PATCHES_PATH
    summary = {
        "patches_path": PATCHES_PATH,
        "patches_exists": patches_path.exists(),
        "patches_total": 0,
        "pending": 0,
        "applied_pending_audit": 0,
        "audit_passed": 0,
        "audit_failed": 0,
        "blocked": 0,
        "last_patch_id": None,
        "last_variant_ids": [],
        "last_changed_fields": {},
        "last_audit_status": None,
        "last_error": None,
        "change_required": 0,
        "no_change_required": 0,
        "patchable": 0,
        "change_required_not_patchable": 0,
        "manual_review_required": 0,
        "outcome_audit_pending": 0,
        "outcome_audit_failed": 0,
    }

    patches_payload: dict[str, Any] = {}
    patches: list[Any] = []
    if patches_path.exists():
        try:
            raw_payload = json.loads(patches_path.read_text(encoding="utf-8"))
            if not isinstance(raw_payload, dict):
                summary["last_error"] = "patches.json must be a JSON object"
            else:
                patches_payload = raw_payload
                raw_patches = raw_payload.get("patches", [])
                if isinstance(raw_patches, list):
                    patches = raw_patches
                else:
                    summary["last_error"] = "patches.json must contain a patches list"
        except (OSError, json.JSONDecodeError) as exc:
            summary["last_error"] = f"Failed to load patches.json: {exc}"

    summary["patches_total"] = len(patches)
    counts = {status: 0 for status in ("pending", "applied_pending_audit", "audit_passed", "audit_failed", "blocked")}
    for patch in patches:
        if isinstance(patch, dict) and patch.get("status") in counts:
            counts[str(patch.get("status"))] += 1
    applications = _load_jsonl_file(root / PATCH_APPLICATIONS_PATH)
    audits = _load_jsonl_file(root / DIFF_AUDITS_PATH)
    last_application = applications[-1] if applications else {}
    last_audit = audits[-1] if audits else {}
    last_patch = next((patch for patch in reversed(patches) if isinstance(patch, dict)), {})
    summary.update(counts)
    for key in ("pending", "applied_pending_audit", "audit_passed", "audit_failed", "blocked"):
        value = patches_payload.get(key) if isinstance(patches_payload, dict) else None
        if isinstance(value, (int, float)):
            summary[key] = int(value)
    for key in (
        "change_required",
        "no_change_required",
        "patchable",
        "change_required_not_patchable",
        "manual_review_required",
        "outcome_audit_pending",
        "outcome_audit_failed",
    ):
        value = patches_payload.get(key, 0) if isinstance(patches_payload, dict) else 0
        summary[key] = int(value) if isinstance(value, (int, float)) else 0
    summary["last_patch_id"] = (
        last_application.get("patch_id") or last_audit.get("patch_id") or last_patch.get("patch_id") or None
    )

    variant_ids = last_application.get("variant_ids")
    if not isinstance(variant_ids, list):
        variant_ids = last_audit.get("variant_ids")
    summary["last_variant_ids"] = variant_ids if isinstance(variant_ids, list) else []

    changed_fields = last_application.get("changed_fields")
    if not isinstance(changed_fields, dict):
        changed_fields = {}
    summary["last_changed_fields"] = changed_fields

    audit_status = last_audit.get("status")
    summary["last_audit_status"] = str(audit_status) if isinstance(audit_status, str) and audit_status else None
    return summary


def load_ai_review_outcome(project_root: str | Path = ".") -> dict:
    root = Path(project_root)
    decisions_path = root / DECISIONS_PATH
    base_summary = {
        "decisions_path": DECISIONS_PATH,
        "decisions_exists": decisions_path.exists(),
        "decisions_total": 0,
        "completed_decisions": 0,
        "change_required": 0,
        "no_change_required": 0,
        "patchable": 0,
        "change_required_not_patchable": 0,
        "manual_review_required": 0,
        "missing_change_decision": 0,
        "outcome_audit_pending": 0,
        "outcome_audit_passed": 0,
        "outcome_audit_failed": 0,
        "latest_decision_id": None,
        "latest_item_id": None,
        "latest_change_decision": None,
        "latest_change_severity": None,
        "latest_patchable": None,
        "latest_patchability_reason": None,
        "latest_change_reason": None,
        "last_error": None,
        "completed_ai_decisions": 0,
        "patchable_changes": 0,
        "non_patchable_changes": 0,
        "pending_patches": 0,
        "rows": [],
        "columns": list(AI_DECISION_OUTCOME_COLUMNS),
    }
    if not decisions_path.exists():
        return base_summary

    raw_decisions, last_error = _load_decisions_list(root)
    if last_error:
        base_summary["last_error"] = last_error
        return base_summary

    queue_items = _load_issue_queue_items(root)
    queue_by_item_id = {
        str(item.get("item_id") or ""): item
        for item in queue_items
        if isinstance(item, dict) and str(item.get("item_id") or "")
    }

    decisions: list[dict[str, Any]] = [item for item in raw_decisions if isinstance(item, dict)]
    rows: list[dict] = []
    latest: dict[str, Any] | None = None
    for decision in decisions:
        item_id = str(decision.get("item_id") or "").strip()
        queue_item = queue_by_item_id.get(item_id, {})
        change_decision = decision.get("change_decision")
        change_decision_str = change_decision.strip() if isinstance(change_decision, str) else ""
        change_decision_text = change_decision_str.upper() if change_decision_str else None
        patchable_value = decision.get("patchable")
        outcome_audit_status = str(decision.get("outcome_audit_status") or "").strip().lower()

        if change_decision_text == "CHANGE_REQUIRED":
            base_summary["change_required"] += 1
            if patchable_value is not True:
                base_summary["change_required_not_patchable"] += 1
        elif change_decision_text == "NO_CHANGE_REQUIRED":
            base_summary["no_change_required"] += 1
        else:
            base_summary["missing_change_decision"] += 1
            base_summary["manual_review_required"] += 1

        if patchable_value is True:
            base_summary["patchable"] += 1
        if outcome_audit_status == "pending":
            base_summary["outcome_audit_pending"] += 1
        elif outcome_audit_status == "passed":
            base_summary["outcome_audit_passed"] += 1
        elif outcome_audit_status == "failed":
            base_summary["outcome_audit_failed"] += 1

        rows.append(
            {
                "item_id": item_id,
                "make": queue_item.get("make", ""),
                "model": queue_item.get("model", ""),
                "years": _years_text(queue_item),
                "change_decision": change_decision_text or "",
                "change_severity": decision.get("change_severity") if isinstance(decision.get("change_severity"), str) else "",
                "patchable": patchable_value is True,
                "patchability_reason": decision.get("patchability_reason")
                if isinstance(decision.get("patchability_reason"), str)
                else "",
                "change_reason": decision.get("change_reason") if isinstance(decision.get("change_reason"), str) else "",
            }
        )
        latest = decision

    base_summary["decisions_total"] = len(decisions)
    base_summary["completed_decisions"] = len(decisions)
    base_summary["completed_ai_decisions"] = len(decisions)
    base_summary["patchable_changes"] = base_summary["patchable"]
    base_summary["non_patchable_changes"] = base_summary["change_required_not_patchable"]
    base_summary["rows"] = rows
    if isinstance(latest, dict):
        latest_decision_id = latest.get("decision_id")
        if not isinstance(latest_decision_id, str) or not latest_decision_id.strip():
            latest_decision_id = latest.get("id")
        base_summary["latest_decision_id"] = (
            latest_decision_id.strip() if isinstance(latest_decision_id, str) and latest_decision_id.strip() else None
        )
        latest_item_id = latest.get("item_id")
        base_summary["latest_item_id"] = latest_item_id.strip() if isinstance(latest_item_id, str) and latest_item_id.strip() else None
        latest_change_decision = latest.get("change_decision")
        base_summary["latest_change_decision"] = (
            latest_change_decision if isinstance(latest_change_decision, str) and latest_change_decision.strip() else None
        )
        latest_change_severity = latest.get("change_severity")
        base_summary["latest_change_severity"] = (
            latest_change_severity if isinstance(latest_change_severity, str) and latest_change_severity.strip() else None
        )
        latest_patchable = latest.get("patchable")
        base_summary["latest_patchable"] = latest_patchable if isinstance(latest_patchable, bool) else None
        latest_patchability_reason = latest.get("patchability_reason")
        base_summary["latest_patchability_reason"] = (
            latest_patchability_reason
            if isinstance(latest_patchability_reason, str) and latest_patchability_reason.strip()
            else None
        )
        latest_change_reason = latest.get("change_reason")
        base_summary["latest_change_reason"] = (
            latest_change_reason if isinstance(latest_change_reason, str) and latest_change_reason.strip() else None
        )

    patch_summary = load_surgical_patch_summary(root)
    pending = patch_summary.get("pending", 0) if isinstance(patch_summary, dict) else 0
    base_summary["pending_patches"] = int(pending) if isinstance(pending, (int, float)) else 0
    return base_summary


def backfill_ai_review_change_decisions() -> dict:
    """Backfill binary change decisions for completed legacy AI-review decisions."""
    return _backfill_change_decisions()


def queue_completed_ai_review_outcomes_for_audit(*, retry: bool = False) -> dict:
    """Queue completed AI decisions for GPT-5.4 outcome audit."""
    return _queue_completed_decisions_for_outcome_audit(retry=retry)


def audit_next_ai_review_outcome() -> dict:
    """Audit next pending AI decision outcome with GPT-5.4."""
    return _audit_next_ai_review_outcome_with_openai()


def load_debug_snippets(project_root: str | Path = ".", max_chars: int = 1200) -> list[dict]:
    """Return compact snippets for known validation files for Advanced Debug."""
    root = Path(project_root)
    snippets: list[dict] = []
    for rel_path in (
        ISSUE_QUEUE_PATH,
        VALIDATION_REPORT_PATH,
        MANIFEST_PATH,
        DECISIONS_PATH,
        MODEL_REVIEW_PROGRESS_PATH,
        PATCHES_PATH,
        PATCH_APPLICATIONS_PATH,
        DIFF_AUDITS_PATH,
        AI_OUTCOME_AUDITS_PATH,
    ):
        path = root / rel_path
        entry = {"path": rel_path, "exists": path.exists(), "size_bytes": path.stat().st_size if path.exists() else 0}
        if path.exists():
            text = path.read_text(encoding="utf-8")[:max_chars]
            entry["snippet"] = text
            entry["truncated"] = path.stat().st_size > max_chars
        snippets.append(entry)
    return snippets


def export_final_clean_database() -> dict:
    """Export the final clean database and return a UI-safe summary."""
    summary = _export_final_clean_database()
    return {
        "final_path": summary.get("final_path")
        or summary.get("output_path")
        or "data/final/resume_package_final_clean.json",
        "total_input_variants": summary.get("total_input_variants") or summary.get("input_variant_count") or 0,
        "total_output_variants": summary.get("total_output_variants") or summary.get("output_variant_count") or 0,
        "safe_decisions_applied": summary.get("safe_decisions_applied", 0),
        "manual_review_remaining_count": summary.get("manual_review_remaining_count", 0),
        "created_at": summary.get("created_at") or summary.get("metadata", {}).get("created_at") or "",
        "variant_count_delta": summary.get("variant_count_delta", 0),
        "blocked_variant_loss": bool(summary.get("blocked_variant_loss", False)),
    }


def save_final_clean_database_to_github() -> dict:
    """Save only the final clean database to GitHub."""
    return _save_final_clean_database_to_github()


def run_final_quality_audit() -> dict:
    """Run final clean database quality audit."""
    return _audit_final_clean_database_quality()


def load_recent_run_events(max_rows: int = 20) -> dict:
    """Return compact recent run/model events for debug display."""
    rows = load_recent_events(limit=max_rows)
    return {
        "rows": rows,
        "columns": ["time", "stage", "provider", "model", "item_id", "status", "summary"],
        "max_rows": max_rows,
        "events_path": "data/validation/run_events.jsonl",
        "final_path": FINAL_CLEAN_DATABASE_PATH,
    }
