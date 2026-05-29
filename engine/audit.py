"""Audit layer — validates canonical before and after every write."""
from __future__ import annotations

from core.source_ids import looks_like_placeholder_source_id


def audit_canonical(
    canonical: dict,
    seed_catalog: list[dict] | None = None,
    newly_added_variant_ids: list[str] | None = None,
) -> tuple[bool, list[str]]:
    """Validate canonical integrity. Returns (ok, errors).

    Hard errors block save. Pre-existing data quality issues in individual
    variants (e.g. IL-confirmed with placeholder source_ids) are collected
    but do NOT block save — they are legacy issues to be cleaned up over time.

    However, if ``newly_added_variant_ids`` is supplied, any variant whose
    variant_id appears in that list AND has IL-confirmed market_scope with
    placeholder/empty source_ids is a HARD error that blocks save.
    """
    errors: list[str] = []
    warnings: list[str] = []  # non-blocking
    new_ids: set[str] = set(newly_added_variant_ids or [])

    if not isinstance(canonical, dict):
        return False, ["root_not_dict"]

    # 1. Check JSON structure
    bs = canonical.get("batch_state")
    if not isinstance(bs, dict):
        errors.append("missing_batch_state")
        bs = {}

    verified = canonical.get("verified_variants")
    partial = canonical.get("partial_variants")
    if not isinstance(verified, list):
        errors.append("verified_variants_not_a_list")
        verified = []
    if not isinstance(partial, list):
        errors.append("partial_variants_not_a_list")
        partial = []

    all_variants = verified + partial

    # 2. Counts match
    counts = canonical.get("counts")
    if isinstance(counts, dict):
        stored_total = counts.get("total_variants")
        if stored_total is not None and stored_total != len(all_variants):
            errors.append(
                f"counts_total_mismatch: stored={stored_total} actual={len(all_variants)}"
            )

    # 3. Processed seeds with zero variants must have valid proof
    processed = bs.get("processed_seed_ids") or []
    accounting = bs.get("seed_accounting") or {}

    # Build variant count per seed
    variant_seeds: dict[str, int] = {}
    for v in all_variants:
        if not isinstance(v, dict):
            continue
        make = (v.get("make") or "").strip().lower().replace(" ", "_")
        model = (v.get("model") or "").strip().lower().replace(" ", "_")
        ys = v.get("year_start", "")
        ye = v.get("year_end", "")
        # We can't perfectly reconstruct seed_id from variant, so check accounting
        pass

    for seed_id in processed:
        acct = accounting.get(seed_id)
        if not isinstance(acct, dict):
            continue

        resolution_type = acct.get("resolution_type", "")
        if resolution_type == "no_variants_proven":
            # Must have valid proof
            proof_status = acct.get("proof_status")
            source_ids = acct.get("source_ids") or []
            source_basis = acct.get("source_basis") or ""

            if proof_status != "proven":
                errors.append(
                    f"processed_no_variants_missing_proof: {seed_id}"
                )
            elif not source_ids:
                errors.append(
                    f"processed_no_variants_empty_source_ids: {seed_id}"
                )
            elif all(looks_like_placeholder_source_id(str(s)) for s in source_ids):
                errors.append(
                    f"processed_no_variants_placeholder_sources: {seed_id}"
                )
            elif not source_basis.strip():
                errors.append(
                    f"processed_no_variants_empty_source_basis: {seed_id}"
                )

    # 4. Check placeholder sources in proven ZVR (legacy field too)
    zvr_field = "zero_variant_resolution"
    for sa_seed_id, sa_entry in accounting.items():
        if not isinstance(sa_entry, dict):
            continue
        zvr = sa_entry.get(zvr_field)
        if isinstance(zvr, dict) and zvr.get("proof_status") == "proven":
            sids = zvr.get("source_ids") or []
            if sids and all(looks_like_placeholder_source_id(str(s)) for s in sids):
                errors.append(
                    f"placeholder_sources_in_proven_zvr: {sa_seed_id}"
                )

    # 5. IL-confirmed with placeholder source_ids
    #    - Legacy (not in newly_added_variant_ids): warning only, non-blocking
    #    - Newly added by v3 engine: HARD error, blocks save
    for v in all_variants:
        if not isinstance(v, dict):
            continue
        if v.get("market_scope") == "IL-confirmed":
            sids = v.get("source_ids") or []
            if not sids or all(looks_like_placeholder_source_id(str(s)) for s in sids):
                vid = v.get("variant_id", "unknown")
                if vid in new_ids:
                    errors.append(
                        f"new_il_confirmed_placeholder_sources: {vid}"
                    )
                else:
                    warnings.append(
                        f"il_confirmed_placeholder_sources: {vid}"
                    )

    # 7. next_seed_id in seed catalog
    if seed_catalog is not None:
        from engine.state import seed_id_from_seed
        next_sid = bs.get("next_seed_id")
        if next_sid:
            catalog_ids = {seed_id_from_seed(s) for s in seed_catalog}
            if next_sid not in catalog_ids:
                errors.append(f"next_seed_id_not_in_catalog: {next_sid}")

    # 8. No duplicates in buckets
    for bucket_name in ("processed_seed_ids", "manual_review_seed_ids", "failed_seed_ids"):
        bucket = bs.get(bucket_name) or []
        if len(bucket) != len(set(bucket)):
            errors.append(f"duplicate_in_{bucket_name}")

    # 9. Same seed in multiple buckets
    processed_set = set(bs.get("processed_seed_ids") or [])
    manual_set = set(bs.get("manual_review_seed_ids") or [])
    failed_set = set(bs.get("failed_seed_ids") or [])

    overlap_pm = processed_set & manual_set
    overlap_pf = processed_set & failed_set
    overlap_mf = manual_set & failed_set

    if overlap_pm:
        errors.append(f"seed_in_both_processed_and_manual: {sorted(overlap_pm)[:3]}")
    if overlap_pf:
        errors.append(f"seed_in_both_processed_and_failed: {sorted(overlap_pf)[:3]}")
    if overlap_mf:
        errors.append(f"seed_in_both_manual_and_failed: {sorted(overlap_mf)[:3]}")

    # 10. If processed seeds exist, last_completed_seed_id must not be None
    #     (last_handled_seed_id or last_failed_seed_id also satisfy this if
    #     only manual/failed seeds have been handled so far)
    last_completed = bs.get("last_completed_seed_id")
    last_handled = bs.get("last_handled_seed_id")
    last_failed = bs.get("last_failed_seed_id")
    any_handled = processed_set or manual_set or failed_set
    if any_handled and last_completed is None and last_handled is None and last_failed is None:
        errors.append("last_completed_seed_id_none_with_processed_seeds")

    # 11. next_seed_id must not be in processed/manual_review/failed
    next_sid_check = bs.get("next_seed_id")
    if next_sid_check:
        if next_sid_check in processed_set:
            errors.append(f"next_seed_id_already_processed: {next_sid_check}")
        if next_sid_check in manual_set:
            errors.append(f"next_seed_id_in_manual_review: {next_sid_check}")
        if next_sid_check in failed_set:
            errors.append(f"next_seed_id_in_failed: {next_sid_check}")

    # 6. ACCEPT_VARIANTS / variants_added accounting must have added + merged > 0
    for sa_seed_id, sa_entry in accounting.items():
        if not isinstance(sa_entry, dict):
            continue
        res_type = sa_entry.get("resolution_type", "")
        if res_type in ("variants_added", "variants_added_after_failed_retry"):
            ac = sa_entry.get("added_count") or 0
            mc = sa_entry.get("merged_count") or 0
            if ac + mc == 0:
                errors.append(
                    f"accept_variants_zero_mutation: {sa_seed_id}"
                )

    # 7. Duplicate variant_ids
    seen_vids: set[str] = set()
    dup_count = 0
    for v in all_variants:
        if not isinstance(v, dict):
            continue
        vid = str(v.get("variant_id", "")).strip()
        if vid:
            if vid in seen_vids:
                dup_count += 1
            else:
                seen_vids.add(vid)
    if dup_count:
        errors.append(f"duplicate_variant_ids: {dup_count}")

    return (len(errors) == 0), errors
