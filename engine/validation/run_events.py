"""Append-only run/model event logging helpers."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.paths import RUN_EVENTS_PATH

_SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_\-]{10,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z\-_]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-+/=]+\b"),
)
SENSITIVE_KEY_PATTERNS = (
    "api_key",
    "apikey",
    "token",
    "secret",
    "password",
    "authorization",
    "bearer",
    "cookie",
    "set-cookie",
    "x-api-key",
    "github_token",
    "openai_api_key",
    "google_api_key",
)
_ALLOWED_EVENT_FIELDS = {
    "created_at",
    "stage",
    "event_type",
    "audit_run_id",
    "item_id",
    "variant_ids",
    "provider",
    "model",
    "status",
    "request_summary",
    "response_summary",
    "cost_estimate",
    "error",
}
_STRING_EVENT_FIELDS = {
    "created_at",
    "stage",
    "event_type",
    "audit_run_id",
    "item_id",
    "provider",
    "model",
    "status",
}
_TEXT_FIELDS = {"request_summary", "response_summary", "error"}
_SECRET_LIKE_TOKEN = re.compile(r"\b[A-Za-z0-9_\-]{32,}\b")
_DEFAULT_LIMIT = 20
_SUMMARY_MAX = 500
_REDACTED = "[REDACTED]"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sanitize_text(value: Any) -> str:
    text = str(value or "")
    if _looks_like_secret(text):
        return _REDACTED
    for pattern in _SENSITIVE_VALUE_PATTERNS:
        text = pattern.sub(_REDACTED, text)
    if _looks_like_secret(text):
        return _REDACTED
    return text


def _compact_summary(value: Any, *, max_chars: int = _SUMMARY_MAX) -> str:
    sanitized = _sanitize_text(value)
    compact = " ".join(sanitized.split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3] + "..."


def _looks_like_secret(value: str) -> bool:
    candidate = value.strip()
    if not candidate:
        return False
    lowered = candidate.lower()
    if lowered.startswith(("sk-", "ghp_", "github_pat_")):
        return True
    if "bearer " in lowered:
        return True
    matches = list(_SECRET_LIKE_TOKEN.finditer(candidate))
    if not matches:
        return False
    for match in matches:
        token = match.group(0)
        has_digit = any(char.isdigit() for char in token)
        has_alpha = any(char.isalpha() for char in token)
        if has_digit and has_alpha:
            return True
    return False


def _is_sensitive_key(key: str) -> bool:
    lowered = key.lower()
    normalized = lowered.replace("-", "").replace("_", "")
    for marker in SENSITIVE_KEY_PATTERNS:
        marker_lower = marker.lower()
        marker_normalized = marker_lower.replace("-", "").replace("_", "")
        if marker_lower in lowered or marker_normalized in normalized:
            return True
    return False


def _sanitize_recursive(value: Any) -> Any:
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for raw_key, raw_value in value.items():
            key = str(raw_key)
            if _is_sensitive_key(key):
                sanitized[key] = _REDACTED
            else:
                sanitized[key] = _sanitize_recursive(raw_value)
        return sanitized
    if isinstance(value, list):
        return [_sanitize_recursive(item) for item in value]
    if isinstance(value, tuple):
        return [_sanitize_recursive(item) for item in value]
    if isinstance(value, str):
        return _sanitize_text(value)
    return value


def _allowlisted_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: payload[key] for key in _ALLOWED_EVENT_FIELDS if key in payload}


def _normalized_event(payload: dict[str, Any]) -> dict[str, Any]:
    raw = payload if isinstance(payload, dict) else {}
    event = _allowlisted_payload(raw)
    event["created_at"] = str(event.get("created_at") or _utc_now())
    for key in _STRING_EVENT_FIELDS - {"created_at"}:
        event[key] = str(event.get(key) or "")
    variant_ids = event.get("variant_ids")
    if isinstance(variant_ids, (list, tuple, set)):
        event["variant_ids"] = [str(item or "") for item in variant_ids]
    else:
        event["variant_ids"] = []
    for key in _TEXT_FIELDS:
        event[key] = event.get(key) or ""
    if "cost_estimate" not in event:
        event["cost_estimate"] = None
    return event


def _truncate_text_fields(event: dict[str, Any]) -> dict[str, Any]:
    for key in _TEXT_FIELDS:
        event[key] = _compact_summary(event.get(key) or "", max_chars=_SUMMARY_MAX)
    return event


def log_event(payload: dict[str, Any]) -> dict[str, Any]:
    """Append one sanitized JSONL event and return the stored payload."""
    event = _truncate_text_fields(_sanitize_recursive(_normalized_event(payload)))
    path = Path(RUN_EVENTS_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        # Payload is strictly allowlisted and recursively sanitized before persistence.
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
