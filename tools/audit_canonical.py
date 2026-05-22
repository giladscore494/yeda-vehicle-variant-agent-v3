"""Standalone canonical audit tool. Run from command line."""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.state import load_canonical, get_all_variants, get_batch_state
from engine.audit import audit_canonical
from core.source_ids import looks_like_placeholder_source_id


def audit_report(canonical_path: str = "data/canonical/resume_package_canonical.json",
                 seeds_path: str = "data/seeds/vehicle_model_seeds_il.json") -> dict:
    """Generate a full audit report of the canonical data."""
    canonical = load_canonical(canonical_path)
    bs = get_batch_state(canonical)
    all_variants = get_all_variants(canonical)

    # Load seeds if available
    seeds = None
    seeds_p = Path(seeds_path)
    if seeds_p.exists():
        seeds = json.loads(seeds_p.read_text(encoding="utf-8"))

    ok, errors = audit_canonical(canonical, seed_catalog=seeds)

    # Zero-variant processed seeds with invalid proof
    accounting = bs.get("seed_accounting") or {}
    zero_variant_issues: list[str] = []
    for sid in bs.get("processed_seed_ids", []):
        acct = accounting.get(sid, {})
        if acct.get("resolution_type") == "no_variants_proven":
            source_ids = acct.get("source_ids") or []
            if not source_ids or all(looks_like_placeholder_source_id(str(s)) for s in source_ids):
                zero_variant_issues.append(sid)

    report = {
        "audit_ok": ok,
        "audit_errors": errors,
        "variants_count": len(all_variants),
        "verified_count": len(canonical.get("verified_variants") or []),
        "partial_count": len(canonical.get("partial_variants") or []),
        "processed_count": len(bs.get("processed_seed_ids") or []),
        "needs_retry_count": len(bs.get("needs_retry_seed_ids") or []),
        "manual_review_count": len(bs.get("manual_review_seed_ids") or []),
        "failed_count": len(bs.get("failed_seed_ids") or []),
        "next_seed_id": bs.get("next_seed_id"),
        "last_completed_seed_id": bs.get("last_completed_seed_id"),
        "zero_variant_placeholder_issues": zero_variant_issues,
    }
    return report


def main():
    report = audit_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
