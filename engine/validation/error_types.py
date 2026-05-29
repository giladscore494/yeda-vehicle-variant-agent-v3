"""Specific error categories for the validation engine.

Replaces generic 'runner_failed' with structured error types.
"""
from __future__ import annotations

from datetime import datetime, timezone

# All recognized error types
ERROR_TYPES = [
    "config_error_missing_gemini_key",
    "config_error_missing_openai_key",
    "config_error_missing_github_token",
    "config_error_invalid_branch",
    "model_auth_error",
    "model_not_found",
    "model_grounding_error",
    "model_timeout",
    "model_empty_response",
    "model_parse_error",
    "validation_schema_error",
    "canonical_read_error",
    "canonical_write_blocked",
    "github_read_error",
    "github_write_error",
    "unexpected_exception",
]


def make_error(
    error_type: str,
    error_message: str,
    *,
    failed_stage: str = "",
    seed_id: str = "",
    validation_item: str = "",
    model_called: str = "",
    model_response_received: bool = False,
    parse_success: bool = False,
    github_write_attempted: bool = False,
    github_write_success: bool = False,
    canonical_write_attempted: bool = False,
    canonical_write_success: bool = False,
    traceback_short: str = "",
) -> dict:
    """Build a structured error record."""
    return {
        "error_type": error_type,
        "error_message": str(error_message),
        "failed_stage": failed_stage,
        "seed_id": seed_id,
        "validation_item": validation_item,
        "model_called": model_called,
        "model_response_received": model_response_received,
        "parse_success": parse_success,
        "github_write_attempted": github_write_attempted,
        "github_write_success": github_write_success,
        "canonical_write_attempted": canonical_write_attempted,
        "canonical_write_success": canonical_write_success,
        "traceback_short": traceback_short,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def classify_exception(exc: Exception) -> str:
    """Classify an exception into an error_type string."""
    name = type(exc).__name__.lower()
    msg = str(exc).lower()

    if "api_key" in msg or "auth" in msg or "credential" in msg or "secret" in msg:
        if "gemini" in msg or "google" in msg:
            return "config_error_missing_gemini_key"
        if "openai" in msg:
            return "config_error_missing_openai_key"
        if "github" in msg:
            return "config_error_missing_github_token"
        return "model_auth_error"

    if "timeout" in name or "timeout" in msg:
        return "model_timeout"

    if "not found" in msg and "model" in msg:
        return "model_not_found"

    if "grounding" in msg:
        return "model_grounding_error"

    if "json" in name or "parse" in msg or "decode" in msg:
        return "model_parse_error"

    if "canonical" in msg and "write" in msg:
        return "canonical_write_blocked"

    if "canonical" in msg:
        return "canonical_read_error"

    if "github" in msg:
        return "github_read_error"

    return "unexpected_exception"
