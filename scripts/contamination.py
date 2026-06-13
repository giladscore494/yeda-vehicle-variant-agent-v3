"""Contamination guards: refuse to mix mock and real rows in one file.

Before any output/checkpoint file is loaded, resumed, or appended to, it is
checked against the selected run mode. If a real run targets a file that
carries any mock fingerprint (or vice versa) we stop loudly instead of
silently merging mixed data.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from .run_paths import MOCK_GROUNDING_SENTINEL, MOCK_MODEL


class ContaminationError(RuntimeError):
    """Raised when a target file does not match the selected run mode."""


def _iter_rows(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not isinstance(doc, dict):
        return []
    rows = doc.get("validated_variants")
    if isinstance(rows, list):
        out = list(rows)
    else:
        out = []
    by_id = doc.get("validated_variants_by_id")
    if isinstance(by_id, dict):
        out.extend(v for v in by_id.values() if isinstance(v, dict))
    return [r for r in out if isinstance(r, dict)]


def detect_contamination(doc: Dict[str, Any], mode: str) -> List[str]:
    """Return a list of contamination reasons (empty == clean for ``mode``)."""
    problems: List[str] = []
    meta = doc.get("metadata", {}) if isinstance(doc, dict) else {}
    if not isinstance(meta, dict):
        meta = {}
    rows = _iter_rows(doc)

    if mode == "real":
        if meta.get("run_mode") == "mock":
            problems.append('metadata.run_mode == "mock"')
        if meta.get("is_mock_output") is True:
            problems.append("metadata.is_mock_output == true")
        if meta.get("model") == MOCK_MODEL:
            problems.append(f'metadata.model == "{MOCK_MODEL}"')
        mock_rows = [r for r in rows if r.get("run_mode") == "mock"]
        if mock_rows:
            problems.append(f"{len(mock_rows)} row(s) with run_mode == 'mock'")
        sentinel_rows = [
            r for r in rows if r.get("grounding_summary") == MOCK_GROUNDING_SENTINEL
        ]
        if sentinel_rows:
            problems.append(
                f"{len(sentinel_rows)} row(s) with mock grounding_summary sentinel"
            )
    elif mode == "mock":
        if meta.get("run_mode") == "real":
            problems.append('metadata.run_mode == "real"')
        if meta.get("is_mock_output") is False:
            problems.append("metadata.is_mock_output == false")
        real_rows = [r for r in rows if r.get("run_mode") == "real"]
        if real_rows:
            problems.append(f"{len(real_rows)} row(s) with run_mode == 'real'")
    else:
        problems.append(f"unknown mode {mode!r}")

    return problems


def assert_file_matches_mode(path: str, mode: str) -> None:
    """Raise :class:`ContaminationError` if ``path`` does not match ``mode``.

    A missing or empty file is always clean (nothing to contaminate).
    """
    if not path or not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
    except Exception:  # noqa: BLE001 - a corrupt file cannot be trusted to match
        raise ContaminationError(
            f"Cannot verify run mode of {os.path.basename(path)}: file is unreadable. "
            "Reset the output before continuing."
        )
    problems = detect_contamination(doc, mode)
    if problems:
        raise ContaminationError(
            f"Output file contamination detected in {os.path.basename(path)} "
            f"(expected {mode} mode): " + "; ".join(problems)
        )
