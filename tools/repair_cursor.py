"""Repair cursor tool — fixes next_seed_id when it points to a handled seed.

Usage:
    python tools/repair_cursor.py [canonical_path] [seeds_path]

This tool:
  - Loads the current canonical
  - Preserves variants unchanged
  - Preserves processed/manual_review/failed lists unchanged
  - Recomputes next_seed_id from the seed catalog
  - Writes canonical only if audit passes
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.audit import audit_canonical
from engine.state import (
    load_canonical,
    load_seeds,
    repair_cursor,
    get_batch_state,
    get_all_variants,
)


def run_repair(
    canonical_path: str = "resume_package_canonical.json",
    seeds_path: str = "data/seeds/vehicle_model_seeds_il.json",
    dry_run: bool = False,
) -> dict:
    """Repair the cursor in the canonical file.

    Returns a report dict with old/new values and whether the write succeeded.
    """
    canonical = load_canonical(canonical_path)
    seeds = load_seeds(seeds_path)

    # Snapshot before repair
    bs = get_batch_state(canonical)
    variants_before = get_all_variants(canonical)
    processed_before = list(bs.get("processed_seed_ids", []))
    manual_before = list(bs.get("manual_review_seed_ids", []))
    failed_before = list(bs.get("failed_seed_ids", []))

    # Repair cursor
    result = repair_cursor(canonical, seeds)

    # Confirm invariants
    variants_after = get_all_variants(canonical)
    assert variants_before == variants_after, "variants must not change during repair"
    assert list(bs.get("processed_seed_ids", [])) == processed_before
    assert list(bs.get("manual_review_seed_ids", [])) == manual_before
    assert list(bs.get("failed_seed_ids", [])) == failed_before

    # Audit
    ok, errors = audit_canonical(canonical, seed_catalog=seeds)
    result["audit_ok"] = ok
    result["audit_errors"] = errors

    if not ok:
        print(f"[repair_cursor] Audit FAILED after repair: {errors}")
        print("[repair_cursor] NOT writing to disk.")
        result["written"] = False
        return result

    if dry_run:
        print("[repair_cursor] Dry run — not writing to disk.")
        result["written"] = False
        return result

    # Atomic write
    p = Path(canonical_path)
    tmp_path = p.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(canonical, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(p)
    result["written"] = True
    print(f"[repair_cursor] Written repaired canonical to {p}")

    return result


def main():
    canonical_path = sys.argv[1] if len(sys.argv) > 1 else "resume_package_canonical.json"
    seeds_path = sys.argv[2] if len(sys.argv) > 2 else "data/seeds/vehicle_model_seeds_il.json"
    dry_run = "--dry-run" in sys.argv

    report = run_repair(canonical_path, seeds_path, dry_run=dry_run)

    print("\n=== Repair Cursor Report ===")
    print(f"  Old next_seed_id:           {report['old_next_seed_id']}")
    print(f"  New next_seed_id:           {report['new_next_seed_id']}")
    print(f"  Old last_completed_seed_id: {report['old_last_completed_seed_id']}")
    print(f"  New last_completed_seed_id: {report['new_last_completed_seed_id']}")
    print(f"  Audit OK:                   {report['audit_ok']}")
    print(f"  Written:                    {report['written']}")
    if report.get("audit_errors"):
        print(f"  Audit errors:               {report['audit_errors']}")


if __name__ == "__main__":
    main()
