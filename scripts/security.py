"""Small helpers for redacting secret-looking values from logs/UI/output."""
from __future__ import annotations

import re


def sanitize_error(value: object) -> str:
    text = str(value or "")
    text = re.sub(r"gh[pousr]_[A-Za-z0-9_]{10,}", "***", text)
    text = re.sub(r"sk-[A-Za-z0-9_-]{10,}", "***", text)
    text = re.sub(r"AIza[A-Za-z0-9_-]{10,}", "***", text)
    return text
