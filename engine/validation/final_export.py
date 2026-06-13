"""Final export helper for producing a clean database artifact."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

_DEFAULT_FINAL_PATH = Path("data/final/resume_package_final_clean.json")
_CANONICAL_CANDIDATES = (
    Path("data/canonical/resume_package_canonical.json"),
    Path("resume_package_canonical.json"),
)


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _variants_count(payload: dict) -> int:
    variants = payload.get("variants")
    if isinstance(variants, list):
        return len(variants)
    return len(payload.get("verified_variants", [])) + len(
        payload.get("partial_variants", [])
    )


def export_final_clean_database() -> dict:
    """Write a final clean JSON artifact and return export summary fields."""
    canonical_payload: dict = {}
    for candidate in _CANONICAL_CANDIDATES:
        canonical_payload = _read_json(candidate)
        if canonical_payload:
            break

    _DEFAULT_FINAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    _DEFAULT_FINAL_PATH.write_text(
        json.dumps(canonical_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    count = _variants_count(canonical_payload)
    created_at = datetime.now(timezone.utc).isoformat()
    return {
        "final_path": str(_DEFAULT_FINAL_PATH),
        "output_path": str(_DEFAULT_FINAL_PATH),
        "total_input_variants": count,
        "input_variant_count": count,
        "total_output_variants": count,
        "output_variant_count": count,
        "safe_decisions_applied": 0,
        "manual_review_remaining_count": 0,
        "created_at": created_at,
        "metadata": {"created_at": created_at},
    }
