"""Append-only run/model event logging helpers."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.paths import RUN_EVENTS_PATH

_SENSITIVE_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_\-]{10,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z\-_]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
)
_DEFAULT_LIMIT = 20
_SUMMARY_MAX = 280


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sanitize_text(value: Any) -> str:
    text = str(value or "")
    for pattern in _SENSITIVE_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text


def _compact_summary(value: Any, *, max_chars: int = _SUMMARY_MAX) -> str:
    sanitized = _sanitize_text(value)
    compact = " ".join(sanitized.split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3] + "..."


def _normalized_event(payload: dict[str, Any]) -> dict[str, Any]:
    has_error = bool(payload.get("error"))
    return {
        "created_at": payload.get("created_at") or _utc_now(),
        "stage": str(payload.get("stage") or ""),
        "event_type": str(payload.get("event_type") or ""),
        "item_id": str(payload.get("item_id") or ""),
        "provider": str(payload.get("provider") or ""),
        "model": str(payload.get("model") or ""),
        "request_summary": str(payload.get("stage") or ""),
        "response_summary": str(payload.get("event_type") or ""),
        "status": str(payload.get("status") or ""),
        "cost_estimate": payload.get("cost_estimate"),
        "error": "present" if has_error else None,
    }


def log_event(payload: dict[str, Any]) -> dict[str, Any]:
    """Append one sanitized JSONL event and return the stored payload."""
    event = _normalized_event(payload)
    path = Path(RUN_EVENTS_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def load_recent_events(limit: int = _DEFAULT_LIMIT) -> list[dict[str, Any]]:
    """Return compact recent events for the debug UI."""
    path = Path(RUN_EVENTS_PATH)
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        request_summary = _compact_summary(event.get("request_summary") or "")
        response_summary = _compact_summary(event.get("response_summary") or "")
        rows.append(
            {
                "time": str(event.get("created_at") or ""),
                "stage": str(event.get("stage") or ""),
                "provider": str(event.get("provider") or ""),
                "model": str(event.get("model") or ""),
                "item_id": str(event.get("item_id") or ""),
                "status": str(event.get("status") or ""),
                "summary": response_summary or request_summary,
            }
        )
    capped = max(0, int(limit))
    if capped == 0:
        return []
    return rows[-capped:]
