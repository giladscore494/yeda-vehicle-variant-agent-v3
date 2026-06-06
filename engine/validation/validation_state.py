"""Validation session state — separate from build runtime state.

Manages data/runtime/current_validation_run.json independently.
Never touches canonical or old build state.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from core.config import VALIDATION_RUNTIME_STATE_PATH
from core.paths import SOURCE_CANONICAL_PATH, VALIDATION_REPORT_PATH
from engine.progress import generate_run_id


def _default_state(run_id: str | None = None) -> dict:
    """Return a fresh validation runtime state dict."""
    return {
        "validation_run_id": run_id or generate_run_id(),
        "mode": "targeted-dual-validation",
        "source_canonical_path": SOURCE_CANONICAL_PATH,
        "output_validation_path": VALIDATION_REPORT_PATH,
        "current_validation_item": None,
        # Pipeline stage tracking (deterministic_audit, partial_classification, etc.)
        "pipeline_stages_total": 4,
        "pipeline_stages_completed": [],
        # Model validation item tracking (separate from pipeline stages)
        "model_validation_items_available": 0,
        "model_validation_items_selected": 0,
        "model_validation_items_completed": 0,
        # Legacy fields kept for backward compatibility
        "total_validation_items": 0,
        "completed_validation_items": [],
        "failed_validation_items": [],
        "manual_review_validation_items": [],
        "current_stage": "READY",
        "last_error_type": None,
        "last_error_message": None,
        "last_error_traceback_short": None,
        "started_at": None,
        "updated_at": None,
        "completed_at": None,
    }


def load_validation_state(path: str | None = None) -> dict:
    """Load the validation runtime state, creating a fresh one if missing."""
    p = Path(path or VALIDATION_RUNTIME_STATE_PATH)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return _default_state()


def save_validation_state(state: dict, path: str | None = None) -> None:
    """Persist the validation runtime state."""
    p = Path(path or VALIDATION_RUNTIME_STATE_PATH)
    p.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    p.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def reset_validation_session(path: str | None = None) -> dict:
    """Reset ONLY validation runtime state. Returns the new state.

    Does NOT:
    - modify canonical
    - reset old build state
    - clear processed seeds
    - clear failed/manual queues in canonical
    - remove variants
    """
    new_run_id = generate_run_id()
    state = _default_state(new_run_id)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_validation_state(state, path)
    return state


def update_validation_progress(
    state: dict,
    *,
    stage: str | None = None,
    current_item: str | None = None,
    total_items: int | None = None,
    path: str | None = None,
) -> None:
    """Update progress fields and persist."""
    if stage is not None:
        state["current_stage"] = stage
    if current_item is not None:
        state["current_validation_item"] = current_item
    if total_items is not None:
        state["total_validation_items"] = total_items
    save_validation_state(state, path)


def mark_validation_item_completed(
    state: dict, item_id: str, path: str | None = None
) -> None:
    """Mark a validation item as completed."""
    completed = state.get("completed_validation_items") or []
    if item_id not in completed:
        completed.append(item_id)
    state["completed_validation_items"] = completed
    save_validation_state(state, path)


def mark_validation_item_failed(
    state: dict, item_id: str, error_type: str, error_message: str,
    path: str | None = None,
) -> None:
    """Mark a validation item as failed with error details."""
    failed = state.get("failed_validation_items") or []
    if item_id not in failed:
        failed.append(item_id)
    state["failed_validation_items"] = failed
    state["last_error_type"] = error_type
    state["last_error_message"] = error_message
    save_validation_state(state, path)


def mark_validation_item_manual_review(
    state: dict, item_id: str, path: str | None = None
) -> None:
    """Mark a validation item for manual review."""
    manual = state.get("manual_review_validation_items") or []
    if item_id not in manual:
        manual.append(item_id)
    state["manual_review_validation_items"] = manual
    save_validation_state(state, path)


def update_model_validation_counts(
    state: dict,
    *,
    available: int | None = None,
    selected: int | None = None,
    completed: int | None = None,
    path: str | None = None,
) -> None:
    """Update model validation item counts (separate from pipeline stages)."""
    if available is not None:
        state["model_validation_items_available"] = available
    if selected is not None:
        state["model_validation_items_selected"] = selected
    if completed is not None:
        state["model_validation_items_completed"] = completed
    save_validation_state(state, path)


def mark_pipeline_stage_completed(
    state: dict, stage_name: str, path: str | None = None
) -> None:
    """Mark a pipeline stage as completed (separate from model items)."""
    stages = state.get("pipeline_stages_completed") or []
    if stage_name not in stages:
        stages.append(stage_name)
    state["pipeline_stages_completed"] = stages
    save_validation_state(state, path)


def mark_validation_started(state: dict, path: str | None = None) -> None:
    """Mark the validation session as started."""
    state["started_at"] = datetime.now(timezone.utc).isoformat()
    state["current_stage"] = "RUNNING"
    save_validation_state(state, path)


def mark_validation_completed(state: dict, path: str | None = None) -> None:
    """Mark the validation session as completed."""
    state["completed_at"] = datetime.now(timezone.utc).isoformat()
    state["current_stage"] = "COMPLETED"
    state["current_validation_item"] = None
    save_validation_state(state, path)
