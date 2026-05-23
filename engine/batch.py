"""Batch orchestrator — runs N seeds with autosave after each."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from core.config import CANONICAL_RESUME_PATH
from engine.apply import apply_decision, advance_cursor, ZeroMutationAcceptError
from engine.audit import audit_canonical
from engine.decision import decide_seed_result
from engine.progress import ProgressTracker, generate_run_id, generate_seed_run_id
from engine.run_seed import run_seed
from engine.save import save_canonical_atomic
from engine.state import (
    load_canonical,
    load_seeds,
    find_seed_by_id,
    seed_id_from_seed,
    ensure_batch_state_fields,
)


def run_batch(
    batch_size: int = 1,
    canonical_path: str | None = None,
    seeds_path: str = "data/seeds/vehicle_model_seeds_il.json",
    dry_run: bool = False,
    push_to_github: bool = False,
) -> dict:
    """Run a batch of seeds. Autosaves after each seed."""
    c_path = canonical_path or CANONICAL_RESUME_PATH
    run_id = generate_run_id()
    tracker = ProgressTracker(run_id=run_id, batch_size=batch_size)

    # Load
    canonical = load_canonical(c_path)
    seeds = load_seeds(seeds_path)
    ensure_batch_state_fields(canonical)
    bs = canonical["batch_state"]

    # Pre-batch audit
    ok, errs = audit_canonical(canonical, seed_catalog=seeds)
    if not ok:
        return {"ok": False, "run_id": run_id, "error": f"pre-batch audit failed: {errs}"}

    results: list[dict] = []
    processed = set(bs.get("processed_seed_ids", []))
    manual = set(bs.get("manual_review_seed_ids", []))
    failed = set(bs.get("failed_seed_ids", []))

    # Collect seeds to run
    next_seed_id = bs.get("next_seed_id")
    all_seed_ids = [seed_id_from_seed(s) for s in seeds]

    seeds_to_run: list[str] = []
    if next_seed_id and next_seed_id in all_seed_ids:
        start_idx = all_seed_ids.index(next_seed_id)
    else:
        start_idx = 0

    for i in range(start_idx, len(all_seed_ids)):
        sid = all_seed_ids[i]
        if sid not in processed and sid not in manual and sid not in failed:
            seeds_to_run.append(sid)
        if len(seeds_to_run) >= batch_size:
            break

    tracker.total = len(seeds_to_run)

    for idx, seed_id in enumerate(seeds_to_run):
        tracker.set_seed(seed_id, idx)

        seed = find_seed_by_id(seeds, seed_id)
        if not seed:
            tracker.mark_failed(seed_id, "seed_not_found_in_catalog")
            results.append({"seed_id": seed_id, "action": "FAIL_TRANSIENT", "error": "not found"})
            continue

        # Run seed
        tracker.set_stage("LLM_DISCOVERY")
        seed_result = run_seed(seed, seed_id, dry_run=dry_run)

        # Decision
        tracker.set_stage("DECISION")
        decision = decide_seed_result(seed_result)

        # Apply
        tracker.set_stage("APPLYING_TO_CANONICAL")
        is_current_next = (bs.get("next_seed_id") == seed_id)
        try:
            stats = apply_decision(canonical, decision, is_current_next=is_current_next)
        except ZeroMutationAcceptError as exc:
            tracker.mark_failed(seed_id, str(exc))
            return {
                "ok": False,
                "run_id": run_id,
                "error": f"zero-mutation accept invariant violated at seed {seed_id}: {exc}",
                "results": results,
            }

        # Advance cursor
        if decision.action in ("ACCEPT_VARIANTS", "CLOSE_NO_VARIANTS_PROVEN", "MANUAL_REVIEW", "FAIL_TRANSIENT"):
            if is_current_next:
                advance_cursor(canonical, seeds, seed_id)

        if not dry_run:
            # Save
            tracker.set_stage("SAVING_JSON")
            save_result = save_canonical_atomic(
                canonical, c_path,
                seed_catalog=seeds,
                push_to_github=push_to_github,
                newly_added_variant_ids=stats.get("newly_added_variant_ids"),
            )
            if not save_result["ok"]:
                tracker.mark_failed(seed_id, save_result.get("error", "save failed"))
                return {
                    "ok": False,
                    "run_id": run_id,
                    "error": f"save failed at seed {seed_id}: {save_result.get('error')}",
                    "results": results,
                }

            tracker.set_stage("RELOADING_JSON")
            canonical = load_canonical(c_path)
            ensure_batch_state_fields(canonical)
            bs = canonical["batch_state"]

            tracker.mark_saved(seed_id)

        # Track result
        seed_result_info = {
            "seed_id": seed_id,
            "action": decision.action,
            "reason": decision.reason,
            "added_count": stats["added_count"],
            "merged_count": stats["merged_count"],
        }
        results.append(seed_result_info)

        if decision.action == "MANUAL_REVIEW":
            tracker.mark_manual_review(seed_id)
        elif decision.action == "FAIL_TRANSIENT":
            tracker.mark_failed(seed_id, decision.reason)
            return {
                "ok": False,
                "run_id": run_id,
                "error": f"transient failure at seed {seed_id}",
                "results": results,
            }
        else:
            tracker.mark_completed(
                seed_id, decision.action,
                added=stats["added_count"],
                merged=stats["merged_count"],
            )

    return {
        "ok": True,
        "run_id": run_id,
        "results": results,
        "tracker": tracker.to_dict(),
    }
