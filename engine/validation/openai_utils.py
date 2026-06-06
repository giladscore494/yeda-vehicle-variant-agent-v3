"""Shared helpers for OpenAI Responses API calls."""
from __future__ import annotations

from typing import Any

WEB_SEARCH_TOOL = [{"type": "web_search"}]


def _read_value(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def create_response_with_fallback(
    client: Any,
    model: str,
    prompt: str,
    web_search: bool,
    logger: Any,
    item_key: str,
) -> tuple[Any, bool]:
    """Disabled compatibility helper; use the gated model-review runner."""
    raise RuntimeError(
        "Legacy OpenAI response helper is disabled; use "
        "engine.validation.model_review_runner.run_model_review()."
    )


def extract_response_text(response: Any) -> str:
    """Extract text safely from a Responses API response."""
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text:
        return output_text

    output = getattr(response, "output", None) or []
    text_parts: list[str] = []
    for item in output:
        content = _read_value(item, "content", []) or []
        for part in content:
            text = _read_value(part, "text")
            if isinstance(text, str) and text:
                text_parts.append(text)

    return "\n".join(text_parts).strip()


def is_bad_request_error(exc: Exception) -> bool:
    """Return True when the provider exception maps to HTTP 400."""
    status_code = getattr(exc, "status_code", None)
    if status_code is None:
        status_code = getattr(getattr(exc, "response", None), "status_code", None)
    if status_code is None:
        status_code = getattr(exc, "http_status", None)
    return status_code == 400
