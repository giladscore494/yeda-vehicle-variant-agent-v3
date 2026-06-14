"""OpenAI Responses API helper with web-search tool fallback.

Call order for ``web_search_generate``:
    1. Try ``tools=[{"type": "web_search"}]``
    2. On HTTP 400 → retry with ``tools=[{"type": "web_search_preview"}]``
    3. On HTTP 400 again → retry without tools

This handles API version skew where the exact tool name differs between
OpenAI SDK releases.
"""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

_WEB_SEARCH_TOOL_NAMES = ("web_search", "web_search_preview")


def web_search_generate(
    client: Any,
    model: str,
    input: str,  # noqa: A002  (mirrors the OpenAI Responses API kwarg name)
    **kwargs: Any,
) -> Any:
    """Call the OpenAI Responses API with automatic web-search tool fallback.

    Parameters
    ----------
    client:
        An instantiated ``openai.OpenAI`` (or compatible) client.
    model:
        The model ID to pass to ``client.responses.create``.
    input:
        The user-facing input string.
    **kwargs:
        Additional keyword arguments forwarded to ``client.responses.create``
        on every attempt.

    Returns
    -------
    The first successful response object.

    Raises
    ------
    Exception
        Re-raises the last exception if all attempts fail.
    """
    attempts: list[list[dict] | None] = [
        [{"type": tool_name}] for tool_name in _WEB_SEARCH_TOOL_NAMES
    ] + [None]  # final attempt: no tools

    last_exc: Exception | None = None

    for tools in attempts:
        try:
            call_kwargs: dict[str, Any] = dict(kwargs)
            if tools is not None:
                call_kwargs["tools"] = tools
            response = client.responses.create(
                model=model,
                input=input,
                **call_kwargs,
            )
            tool_label = tools[0]["type"] if tools else "none"
            logger.debug("web_search_generate succeeded with tools=%s", tool_label)
            return response
        except Exception as exc:  # noqa: BLE001
            status = getattr(exc, "status_code", None)
            if status == 400:
                tool_label = tools[0]["type"] if tools else "none"
                logger.warning(
                    "web_search_generate HTTP 400 with tools=%s; trying next fallback",
                    tool_label,
                )
                last_exc = exc
                continue
            # Non-400 errors are not retried.
            raise

    assert last_exc is not None
    raise last_exc
