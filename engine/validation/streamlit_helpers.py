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
    FINAL_CLEAN_DATABASE_PATH,
    ISSUE_QUEUE_PATH,
    MANIFEST_PATH,
    VALIDATION_REPORT_PATH,
    DECISIONS_PATH,
)
from engine.validation.final_github_save import save_final_clean_database_to_github as _save_final_clean_database_to_github
from engine.validation.final_quality_audit import audit_final_clean_database_quality as _audit_final_clean_database_quality
from engine.validation.file_status import load_database_file_status
from engine.validation.minimal_pipeline import run_full_audit
from engine.validation.model_review_runner import run_model_review
from engine.validation.final_export import export_final_clean_database as _export_final_clean_database
from engine.validation.run_events import load_recent_events

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
DEFAULT_QUEUE_PREVIEW_LIMIT = 25
DEFAULT_AI_PREVIEW_LIMIT = 10
SEEDS_PATH = "data/seeds/vehicle_model_seeds_il.json"


def _load_json_file(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


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
        "paths": {
            "issue_queue": ISSUE_QUEUE_PATH,
            "manifest": MANIFEST_PATH,
            "validation_report": VALIDATION_REPORT_PATH,
            "decisions": DECISIONS_PATH,
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


def run_audit_and_refresh_queue() -> dict:
    """Run the deterministic backend audit that also refreshes the review queue."""
    return run_full_audit()


def load_debug_snippets(project_root: str | Path = ".", max_chars: int = 1200) -> list[dict]:
    """Return compact snippets for known validation files for Advanced Debug."""
    root = Path(project_root)
    snippets: list[dict] = []
    for rel_path in (ISSUE_QUEUE_PATH, VALIDATION_REPORT_PATH, MANIFEST_PATH, DECISIONS_PATH):
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
