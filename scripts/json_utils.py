"""Neutral JSON helpers shared by the GPT-5.4 catalog client.

This module is model-agnostic on purpose: it must never import from any
provider-specific client so the GPT-5.4 code path has no dependency on retired
pipelines.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict


def parse_strict_json(text: str) -> Dict[str, Any]:
    """Parse model output, tolerating accidental code fences."""
    if text is None:
        raise ValueError("empty model response")
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise
