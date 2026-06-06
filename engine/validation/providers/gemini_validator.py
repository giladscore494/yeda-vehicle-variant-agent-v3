"""Disabled legacy Gemini group validator compatibility wrapper.

Actual Gemini execution is centralized in
``engine.validation.model_review_runner.run_model_review()`` so provider calls can
only happen for items loaded from the validation issue queue and routed through
the new model-review gate.

Uses the unified model schema from model_schema.py.
"""
from __future__ import annotations

from typing import Any

from engine.validation.model_schema import (  # noqa: F401 - retained for import/schema compatibility tests
    normalize_model_output,
    parse_model_json,
    validate_item,
    wrap_provider_result,
)

_DISABLED_MESSAGE = (
    "Use engine.validation.model_review_runner.run_model_review() with issue_queue gating."
)


def estimate_tokens(prompt: str) -> tuple[int, int]:
    """Retained for import compatibility with legacy callers."""
    input_est = len(prompt) // 3
    output_est = max(500, input_est // 2)
    return input_est, output_est


def validate_group(
    group_key: str,
    variants: list[dict],
    trim_candidates: list[str],
    cost_tracker: Any = None,
) -> dict:
    """Return a disabled no-call result for the retired group-validation path.

    Legacy callers may still import this function, but it must never instantiate
    provider SDK clients or execute model requests. Use the issue-queue gated
    model-review runner for all real model reviews.
    """
    return {
        "status": "legacy_provider_disabled",
        "provider": "gemini",
        "model_calls_attempted": 0,
        "message": _DISABLED_MESSAGE,
        "group_key": group_key,
    }
