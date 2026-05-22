"""Migrate legacy canonical state to v3 format.

- Adds manual_review_seed_ids if missing.
- Moves problematic zero-variant placeholder closures to manual_review.
- Removes from processed if falsely processed.
- Preserves all variants.
- Preserves next_seed_id.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.state import load_canonical, get_all_variants
from engine.save import save_canonical_atomic
from core.source_ids import looks_like_placeholder_source_id


KNOWN_PROBLEMATIC_SEEDS = [
    "hyundai__creta__2020__2026__il",
    "geely__coolray__2023__2026__il",
    "fiat__freemont__2011__2016__il",
    "ford__ecosport__2013__2022__il",
]


def migrate(
    canonical_path: str = "data/canonical/resume_package_canonical.json",
    seeds_path: str = "data/seeds/vehicle_model_seeds_il.json",
    dry_run: bool = True,
) -> dict:
    """Migrate canonical to v3 state model. Returns migration report."""
    canonical = load_canonical(canonical_path)
    bs = canonical.setdefault("batch_state", {})

    # Preserve variant counts
    pre_variants = len(get_all_variants(canonical))

    # Ensure new fields
    bs.setdefault("processed_seed_ids", [])
    bs.setdefault("manual_review_seed_ids", [])
    bs.setdefault("failed_seed_ids", [])
    bs.setdefault("seed_accounting", {})
    bs.setdefault("next_seed_id", None)
    bs.setdefault("last_completed_seed_id", None)

    moved_to_manual: list[str] = []
    removed_from_processed: list[str] = []

    accounting = bs.get("seed_accounting") or {}
    processed = list(bs.get("processed_seed_ids", []))

    # Find problematic zero-variant placeholder closures
    for sid in list(processed):
        acct = accounting.get(sid, {})

        # Check seed_accounting for proof issues
        is_problematic = False

        resolution_type = acct.get("resolution_type", "")
        if resolution_type == "no_variants_proven":
            source_ids = acct.get("source_ids") or []
            source_basis = acct.get("source_basis") or ""
            proof_status = acct.get("proof_status")

            if not source_ids:
                is_problematic = True
            elif all(looks_like_placeholder_source_id(str(s)) for s in source_ids):
                is_problematic = True
            elif not source_basis.strip():
                is_problematic = True
            elif proof_status != "proven":
                is_problematic = True

        # Also check legacy zero_variant_resolution
        zvr = acct.get("zero_variant_resolution", {})
        if isinstance(zvr, dict) and zvr.get("proof_status") == "proven":
            zvr_sids = zvr.get("source_ids") or []
            if zvr_sids and all(looks_like_placeholder_source_id(str(s)) for s in zvr_sids):
                is_problematic = True

        # Check known problematic seeds
        if sid in KNOWN_PROBLEMATIC_SEEDS:
            # Only move if actually in processed AND has no real variants
            is_problematic = True

        if is_problematic:
            if sid in processed:
                processed.remove(sid)
                removed_from_processed.append(sid)
            if sid not in bs["manual_review_seed_ids"]:
                bs["manual_review_seed_ids"].append(sid)
                moved_to_manual.append(sid)
            # Update accounting
            accounting[sid] = {
                "status": "manual_review",
                "reason": "migrated_from_v2_invalid_proof",
                "previous_resolution_type": resolution_type or "unknown",
                "migrated_at": None,  # Will be set by save
            }

    # Also move from needs_retry to manual_review if they're in manual now
    needs_retry = list(bs.get("needs_retry_seed_ids") or [])
    moved_from_retry: list[str] = []
    for sid in list(needs_retry):
        if sid in bs["manual_review_seed_ids"]:
            needs_retry.remove(sid)
            moved_from_retry.append(sid)

    bs["processed_seed_ids"] = processed
    bs["needs_retry_seed_ids"] = needs_retry

    # Remove duplicates from all buckets
    bs["processed_seed_ids"] = list(dict.fromkeys(bs["processed_seed_ids"]))
    bs["manual_review_seed_ids"] = list(dict.fromkeys(bs["manual_review_seed_ids"]))
    bs["failed_seed_ids"] = list(dict.fromkeys(bs.get("failed_seed_ids", [])))

    # Remove cross-bucket overlaps (manual_review wins over failed)
    manual_set = set(bs["manual_review_seed_ids"])
    bs["failed_seed_ids"] = [s for s in bs["failed_seed_ids"] if s not in manual_set]

    # Post-migration variant count
    post_variants = len(get_all_variants(canonical))

    report = {
        "pre_variants": pre_variants,
        "post_variants": post_variants,
        "variants_preserved": pre_variants == post_variants,
        "moved_to_manual_review": moved_to_manual,
        "removed_from_processed": removed_from_processed,
        "moved_from_needs_retry": moved_from_retry,
        "next_seed_id": bs.get("next_seed_id"),
        "processed_count": len(bs["processed_seed_ids"]),
        "manual_review_count": len(bs["manual_review_seed_ids"]),
        "failed_count": len(bs["failed_seed_ids"]),
    }

    if not dry_run:
        # Load seeds for audit
        seeds = None
        seeds_p = Path(seeds_path)
        if seeds_p.exists():
            seeds = json.loads(seeds_p.read_text(encoding="utf-8"))

        save_result = save_canonical_atomic(canonical, canonical_path, seed_catalog=seeds)
        report["save_result"] = save_result

    return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Migrate canonical to v3")
    parser.add_argument("--apply", action="store_true", help="Actually apply migration")
    args = parser.parse_args()

    report = migrate(dry_run=not args.apply)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
