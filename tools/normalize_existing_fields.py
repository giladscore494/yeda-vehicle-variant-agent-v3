"""Normalize existing variant fields in canonical."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.normalize import (
    normalize_fuel_type,
    normalize_transmission,
    normalize_drivetrain,
    normalize_body_type,
)
from engine.state import load_canonical, get_all_variants


def normalize_canonical_fields(
    canonical_path: str = "data/canonical/resume_package_canonical.json",
) -> dict:
    """Report which fields would be normalized."""
    canonical = load_canonical(canonical_path)
    changes: list[dict] = []

    for bucket_name in ("verified_variants", "partial_variants"):
        variants = canonical.get(bucket_name) or []
        for v in variants:
            if not isinstance(v, dict):
                continue
            vid = v.get("variant_id", "unknown")

            # Check drivetrain
            dt = v.get("drivetrain")
            if isinstance(dt, dict):
                dt_val = dt.get("value")
            else:
                dt_val = dt
            if dt_val and isinstance(dt_val, str):
                normalized = normalize_drivetrain(dt_val)
                if normalized != dt_val:
                    changes.append({
                        "variant_id": vid,
                        "field": "drivetrain",
                        "old": dt_val,
                        "new": normalized,
                    })

    return {"changes_count": len(changes), "changes": changes[:20]}


def main():
    report = normalize_canonical_fields()
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
