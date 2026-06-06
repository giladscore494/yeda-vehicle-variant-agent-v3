"""Progress tracking for issue-queue model review."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.paths import ISSUE_QUEUE_PATH, MODEL_REVIEW_PROGRESS_PATH
from engine.validation.write_guard import safe_write_json


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(path: str | Path, default: Any) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def load_issue_queue_items(path: str | Path = ISSUE_QUEUE_PATH) -> list[dict]:
    payload = _load_json(path, [])
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        return [item for item in payload.get("items", []) if isinstance(item, dict)]
    return []


def load_model_review_progress(path: str | Path = MODEL_REVIEW_PROGRESS_PATH) -> dict:
    payload = _load_json(path, {})
    return payload if isinstance(payload, dict) else {}


def _model_items(items: list[dict]) -> list[dict]:
    return [item for item in items if item.get("requires_model_review") is True]


def _item_id(item: dict) -> str:
    return str(item.get("item_id") or "").strip()


def _variant_ids(items: list[dict]) -> set[str]:
    ids: set[str] = set()
    for item in items:
        raw = item.get("variant_ids")
        if isinstance(raw, list):
            ids.update(str(vid).strip() for vid in raw if str(vid).strip())
        elif item.get("variant_id"):
            ids.add(str(item.get("variant_id")).strip())
    return ids


def refresh_model_review_progress(
    items: list[dict] | None = None,
    *,
    path: str | Path = MODEL_REVIEW_PROGRESS_PATH,
) -> dict:
    """Create or refresh model-review progress from the current issue queue."""
    queue_items = load_issue_queue_items() if items is None else items
    model_items = _model_items(queue_items)
    current = load_model_review_progress(path)
    existing = current.get("items") if isinstance(current.get("items"), dict) else {}
    now = _utc_now()

    item_status: dict[str, dict] = {}
    for item in model_items:
        item_id = _item_id(item)
        if not item_id:
            continue
        previous = existing.get(item_id, {}) if isinstance(existing, dict) else {}
        status = previous.get("status") if previous.get("status") in {"pending", "completed", "failed", "skipped"} else "pending"
        item_status[item_id] = {
            "item_id": item_id,
            "status": status,
            "variant_ids": list(_variant_ids([item])),
            "updated_at": previous.get("updated_at") or now,
        }

    counts = _counts(item_status)
    progress = {
        "created_at": current.get("created_at") or now,
        "updated_at": now,
        "issue_queue_path": ISSUE_QUEUE_PATH,
        "total_model_review_items": len(model_items),
        "total_model_review_variants": len(_variant_ids(model_items)),
        **counts,
        "items": item_status,
    }
    safe_write_json(progress, path)
    return progress


def _counts(item_status: dict[str, dict]) -> dict:
    completed = sum(1 for item in item_status.values() if item.get("status") == "completed")
    failed = sum(1 for item in item_status.values() if item.get("status") == "failed")
    skipped = sum(1 for item in item_status.values() if item.get("status") == "skipped")
    pending = sum(1 for item in item_status.values() if item.get("status") == "pending")
    done_variant_ids = _variant_ids([item for item in item_status.values() if item.get("status") in {"completed", "skipped"}])
    remaining_variant_ids = _variant_ids([item for item in item_status.values() if item.get("status") in {"pending", "failed"}])
    return {
        "completed_items": completed,
        "failed_items": failed,
        "skipped_items": skipped,
        "remaining_items": pending + failed,
        "completed_or_skipped_variants": len(done_variant_ids),
        "remaining_variants": len(remaining_variant_ids),
    }


def mark_model_review_items(
    statuses: dict[str, str],
    *,
    path: str | Path = MODEL_REVIEW_PROGRESS_PATH,
) -> dict:
    """Mark selected issue-queue items as completed, failed, or skipped."""
    progress = refresh_model_review_progress(path=path)
    items = progress.get("items") if isinstance(progress.get("items"), dict) else {}
    now = _utc_now()
    for item_id, status in statuses.items():
        if status not in {"completed", "failed", "skipped"}:
            continue
        if item_id not in items:
            continue
        items[item_id]["status"] = status
        items[item_id]["updated_at"] = now
    progress.update({"updated_at": now, **_counts(items), "items": items})
    safe_write_json(progress, path)
    return progress


def completed_or_skipped_item_ids(path: str | Path = MODEL_REVIEW_PROGRESS_PATH) -> set[str]:
    progress = load_model_review_progress(path)
    items = progress.get("items") if isinstance(progress.get("items"), dict) else {}
    return {
        item_id
        for item_id, item in items.items()
        if isinstance(item, dict) and item.get("status") in {"completed", "skipped"}
    }
