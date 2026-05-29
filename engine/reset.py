"""Reset validation run state without touching canonical data.

Creates a fresh runtime state with a new run_id while preserving
all canonical variants, verified_variants, partial_variants, etc.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from core.config import RUNTIME_STATE_PATH
from engine.progress import generate_run_id
from engine.state import (
    ensure_batch_state_fields,
    seed_id_from_seed,
)


def reset_validation_state(
    canonical: dict,
    seeds: list[dict],
    runtime_state_path: str | None = None,
) -> dict:
    """Reset only runtime/progress state, not canonical data.

    Returns a report dict describing what was reset and the fresh state.
    """
    now = datetime.now(timezone.utc).isoformat()
    new_run_id = generate_run_id()
    state_path = Path(runtime_state_path or RUNTIME_STATE_PATH)

    # Read old state for reporting
    old_state = None
    if state_path.exists():
        try:
            old_state = json.loads(state_path.read_text(encoding="utf-8"))
        except Exception:
            old_state = {"error": "could not read old state"}

    # Write fresh current_run.json
    fresh_state = {
        "run_id": new_run_id,
        "mode": "validation_reset",
        "batch_size": 0,
        "current_index": 0,
        "total": 0,
        "current_seed_id": None,
        "current_stage": "READY",
        "completed_seeds": [],
        "manual_review_seeds": [],
        "failed_seeds": [],
        "last_saved_seed_id": None,
        "last_saved_at": None,
        "last_error": None,
        "reset_at": now,
    }

    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(fresh_state, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return {
        "ok": True,
        "new_run_id": new_run_id,
        "reset_at": now,
        "old_state": old_state,
        "new_state": fresh_state,
    }


def audit_queue_state(canonical: dict, seeds: list[dict]) -> dict:
    """Compute true queue state from canonical + seed catalog.

    Does NOT rely on stale current_run.json.
    """
    ensure_batch_state_fields(canonical)
    bs = canonical["batch_state"]

    all_catalog_ids = [seed_id_from_seed(s) for s in seeds]
    catalog_set = set(all_catalog_ids)

    processed = set(bs.get("processed_seed_ids") or [])
    manual_review = set(bs.get("manual_review_seed_ids") or [])
    failed = set(bs.get("failed_seed_ids") or [])
    handled = processed | manual_review | failed

    unresolved = catalog_set - handled
    orphaned = handled - catalog_set  # processed IDs not in seed catalog

    accounting = bs.get("seed_accounting") or {}

    return {
        "total_catalog_seeds": len(all_catalog_ids),
        "processed_count": len(processed),
        "manual_review_count": len(manual_review),
        "failed_count": len(failed),
        "unresolved_count": len(unresolved),
        "orphaned_count": len(orphaned),
        "processed_seed_ids": sorted(processed),
        "manual_review_seed_ids": sorted(manual_review),
        "failed_seed_ids": sorted(failed),
        "unresolved_seed_ids": sorted(unresolved)[:50],  # cap for display
        "orphaned_seed_ids": sorted(orphaned),
    }


def audit_specific_seed(
    seed_id: str,
    canonical: dict,
    seeds: list[dict],
) -> dict:
    """Audit a specific seed to determine if it truly needs retry.

    Checks:
    - Is it in the seed catalog?
    - Is it in processed/manual_review/failed buckets?
    - Does it have valid variants or valid no-variant closure in accounting?
    - What was the failure reason?

    Returns an audit report dict.
    """
    ensure_batch_state_fields(canonical)
    bs = canonical["batch_state"]
    accounting = bs.get("seed_accounting") or {}

    catalog_ids = set(seed_id_from_seed(s) for s in seeds)
    in_catalog = seed_id in catalog_ids

    in_processed = seed_id in (bs.get("processed_seed_ids") or [])
    in_manual_review = seed_id in (bs.get("manual_review_seed_ids") or [])
    in_failed = seed_id in (bs.get("failed_seed_ids") or [])

    acct = accounting.get(seed_id, {})
    status = acct.get("status", "unknown")
    resolution_type = acct.get("resolution_type", "")
    reason = acct.get("reason", acct.get("last_error", ""))
    error_summary = acct.get("error_summary", "")

    # Determine if properly resolved
    properly_resolved = False
    resolution_detail = "not_resolved"

    if in_processed:
        if resolution_type in ("variants_added", "variants_added_after_failed_retry"):
            properly_resolved = True
            resolution_detail = f"resolved_with_variants (added={acct.get('added_count', 0)}, merged={acct.get('merged_count', 0)})"
        elif resolution_type == "no_variants_proven":
            proof_status = acct.get("proof_status", "")
            source_ids = acct.get("source_ids") or []
            if proof_status == "proven" and source_ids:
                properly_resolved = True
                resolution_detail = "resolved_no_variants_proven"
            else:
                resolution_detail = "in_processed_but_proof_incomplete"
        else:
            resolution_detail = f"in_processed_unknown_resolution: {resolution_type}"

    # Determine failure cause classification
    failure_cause = None
    if in_failed and not properly_resolved:
        error_text = (reason + " " + error_summary).lower()
        if any(kw in error_text for kw in ("api_key", "secret", "token", "auth", "missing key",
                                            "gemini", "config", "credential")):
            failure_cause = "config_error_missing_secrets"
        elif "runner_failed" in error_text:
            failure_cause = "config_error_missing_secrets"  # runner_failed during missing secrets
        else:
            failure_cause = "data_error"

    needs_retry = in_failed and not properly_resolved
    is_stale_failure = in_failed and properly_resolved

    return {
        "seed_id": seed_id,
        "in_catalog": in_catalog,
        "in_processed": in_processed,
        "in_manual_review": in_manual_review,
        "in_failed": in_failed,
        "accounting_status": status,
        "resolution_type": resolution_type,
        "resolution_detail": resolution_detail,
        "properly_resolved": properly_resolved,
        "is_stale_failure": is_stale_failure,
        "needs_retry": needs_retry,
        "failure_cause": failure_cause,
        "reason": reason,
        "error_summary": error_summary,
    }


def remove_stale_failure(
    seed_id: str,
    canonical: dict,
    audit_note: str = "",
) -> dict:
    """Remove a stale failure from failed queue after confirming it's resolved.

    Only call this after audit_specific_seed confirms is_stale_failure=True.
    Writes an audit note to seed_accounting.
    Does NOT modify canonical variants.
    """
    bs = canonical.setdefault("batch_state", {})
    failed = bs.get("failed_seed_ids", [])
    now = datetime.now(timezone.utc).isoformat()

    if seed_id not in failed:
        return {"ok": False, "error": f"{seed_id} not in failed_seed_ids"}

    failed.remove(seed_id)
    bs["failed_seed_ids"] = failed

    # Write audit note
    accounting = bs.setdefault("seed_accounting", {})
    acct = accounting.get(seed_id, {})
    acct["stale_failure_removed_at"] = now
    acct["stale_failure_audit_note"] = audit_note or "Confirmed resolved; stale failure removed."
    accounting[seed_id] = acct

    return {
        "ok": True,
        "seed_id": seed_id,
        "removed_from_failed": True,
        "audit_note": audit_note or "Confirmed resolved; stale failure removed.",
        "removed_at": now,
    }
