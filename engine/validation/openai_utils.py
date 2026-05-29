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
    """Create a Responses API request and retry once without web search on HTTP 400."""
    create_kwargs: dict[str, Any] = {
        "model": model,
        "input": prompt,
    }
    if web_search:
        create_kwargs["tools"] = WEB_SEARCH_TOOL

    try:
        return client.responses.create(**create_kwargs), web_search
    except Exception as exc:
        if web_search and is_bad_request_error(exc):
            logger.warning(
                "OpenAI web search request failed for %s; retrying without web search: %s",
                item_key, exc,
            )
            return client.responses.create(model=model, input=prompt), False
        raise


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
