"""Focused failed-seed retry/repair flow.

Allows retrying a single failed seed safely without disturbing the normal cursor.
Does NOT call Gemini or run live seeds — relies on a pre-built Decision being
supplied externally (or dry-run mode).
"""
from __future__ import annotations

import copy
from datetime import datetime, timezone
from pathlib import Path

from engine.apply import apply_decision, ZeroMutationAcceptError
from engine.audit import audit_canonical
from engine.save import save_canonical_atomic
from engine.state import (
    load_canonical,
    load_seeds,
    find_seed_by_id,
    seed_id_from_seed,
    ensure_batch_state_fields,
)
from engine.types import Decision


class RetryPreconditionError(Exception):
    """Raised when a retry precondition is not met."""
    pass


def _validate_preconditions(
    seed_id: str,
    canonical: dict,
    seeds: list[dict],
) -> None:
    """Validate preconditions for retrying a failed seed."""
    bs = canonical.get("batch_state", {})
    failed = bs.get("failed_seed_ids", [])

    if seed_id not in failed:
        raise RetryPreconditionError(
            f"seed_id '{seed_id}' is not in failed_seed_ids. "
            f"Current failed: {failed}"
        )

    seed = find_seed_by_id(seeds, seed_id)
    if seed is None:
        raise RetryPreconditionError(
            f"seed_id '{seed_id}' not found in seed catalog."
        )


def retry_failed_seed(
    seed_id: str,
    decision: Decision,
    canonical: dict,
    seeds: list[dict],
    dry_run: bool = True,
    push_to_github: bool = False,
    canonical_path: str | None = None,
) -> dict:
    """Retry a single failed seed with a pre-built Decision.

    Parameters
    ----------
    seed_id : str
        The seed to retry. Must exist in failed_seed_ids.
    decision : Decision
        The decision to apply (ACCEPT_VARIANTS, MANUAL_REVIEW, or FAIL_TRANSIENT).
    canonical : dict
        The canonical dict (mutated in-place on non-dry-run).
    seeds : list[dict]
        The seed catalog.
    dry_run : bool
        If True, simulate without saving.
    push_to_github : bool
        If True, push to GitHub after save.
    canonical_path : str | None
        Path to canonical file (required for non-dry-run save).

    Returns
    -------
    dict with keys:
        ok, seed_id, action, added_count, merged_count,
        removed_from_failed, moved_to_processed, moved_to_manual_review,
        next_seed_id_unchanged, next_seed_id, last_saved_seed_id, error, dry_run
    """
    now = datetime.now(timezone.utc).isoformat()
    result = {
        "ok": False,
        "seed_id": seed_id,
        "action": decision.action,
        "added_count": 0,
        "merged_count": 0,
        "removed_from_failed": False,
        "moved_to_processed": False,
        "moved_to_manual_review": False,
        "next_seed_id_unchanged": True,
        "next_seed_id": None,
        "last_saved_seed_id": None,
        "error": None,
        "dry_run": dry_run,
    }

    # Validate preconditions
    try:
        _validate_preconditions(seed_id, canonical, seeds)
    except RetryPreconditionError as exc:
        result["error"] = str(exc)
        return result

    # Ensure decision seed_id matches
    if decision.seed_id != seed_id:
        result["error"] = (
            f"Decision seed_id '{decision.seed_id}' does not match "
            f"retry seed_id '{seed_id}'."
        )
        return result

    bs = canonical.get("batch_state", {})
    original_next_seed_id = bs.get("next_seed_id")
    result["next_seed_id"] = original_next_seed_id

    if dry_run:
        # Simulate on a deep copy
        sim_canonical = copy.deepcopy(canonical)
        try:
            sim_result = _apply_retry_decision(sim_canonical, decision, seeds)
        except (ZeroMutationAcceptError, Exception) as exc:
            result["error"] = str(exc)
            return result

        result.update(sim_result)
        result["ok"] = True
        result["next_seed_id_unchanged"] = (
            sim_canonical["batch_state"].get("next_seed_id") == original_next_seed_id
        )
        result["next_seed_id"] = original_next_seed_id
        return result

    # Live apply
    try:
        apply_result = _apply_retry_decision(canonical, decision, seeds)
    except ZeroMutationAcceptError as exc:
        # Technical failure — keep in failed
        _record_failed_retry_accounting(canonical, seed_id, str(exc), now)
        result["error"] = str(exc)
        return result
    except Exception as exc:
        _record_failed_retry_accounting(canonical, seed_id, str(exc), now)
        result["error"] = str(exc)
        return result

    result.update(apply_result)

    # Verify next_seed_id is preserved
    new_next = canonical["batch_state"].get("next_seed_id")
    result["next_seed_id_unchanged"] = (new_next == original_next_seed_id)
    result["next_seed_id"] = new_next

    # Save
    if canonical_path:
        save_result = save_canonical_atomic(
            canonical,
            canonical_path,
            seed_catalog=seeds,
            push_to_github=push_to_github,
            newly_added_variant_ids=apply_result.get("newly_added_variant_ids"),
        )
        if not save_result["ok"]:
            result["error"] = save_result.get("error")
            return result
        result["last_saved_seed_id"] = seed_id

    result["ok"] = True
    return result


def _apply_retry_decision(
    canonical: dict,
    decision: Decision,
    seeds: list[dict],
) -> dict:
    """Apply a retry decision without advancing the normal cursor.

    Returns apply stats dict.
    """
    bs = canonical.setdefault("batch_state", {})
    bs.setdefault("processed_seed_ids", [])
    bs.setdefault("manual_review_seed_ids", [])
    bs.setdefault("failed_seed_ids", [])
    bs.setdefault("seed_accounting", {})

    original_next_seed_id = bs.get("next_seed_id")
    now = datetime.now(timezone.utc).isoformat()

    # Apply decision with is_current_next=False to avoid moving last_completed_seed_id
    stats = apply_decision(canonical, decision, is_current_next=False)

    # Restore next_seed_id — retry must NEVER move the normal cursor
    bs["next_seed_id"] = original_next_seed_id

    # Update seed_accounting with retry-specific metadata
    if decision.action == "ACCEPT_VARIANTS":
        acct = bs["seed_accounting"].get(decision.seed_id, {})
        acct["resolution_type"] = "variants_added_after_failed_retry"
        acct["retry_source"] = "failed_seed_retry"
        acct["status"] = "resolved"
        bs["seed_accounting"][decision.seed_id] = acct

        return {
            "added_count": stats["added_count"],
            "merged_count": stats["merged_count"],
            "newly_added_variant_ids": stats.get("newly_added_variant_ids", []),
            "removed_from_failed": True,
            "moved_to_processed": True,
            "moved_to_manual_review": False,
        }

    elif decision.action == "MANUAL_REVIEW":
        # apply_decision already adds to manual_review_seed_ids
        # But we also need to remove from failed_seed_ids (apply_decision
        # does NOT do this for MANUAL_REVIEW by default)
        if decision.seed_id in bs["failed_seed_ids"]:
            bs["failed_seed_ids"].remove(decision.seed_id)

        acct = bs["seed_accounting"].get(decision.seed_id, {})
        acct["retry_source"] = "failed_seed_retry"
        acct["status"] = "manual_review"
        acct["reason"] = decision.reason
        bs["seed_accounting"][decision.seed_id] = acct

        return {
            "added_count": 0,
            "merged_count": 0,
            "newly_added_variant_ids": [],
            "removed_from_failed": True,
            "moved_to_processed": False,
            "moved_to_manual_review": True,
        }

    else:
        # FAIL_TRANSIENT or any other action — keep in failed
        # apply_decision adds to failed_seed_ids if not present; it's already there
        acct = bs["seed_accounting"].get(decision.seed_id, {})
        acct["retry_source"] = "failed_seed_retry"
        acct["status"] = "failed"
        acct["last_error"] = decision.reason
        acct["last_attempt_at"] = now
        bs["seed_accounting"][decision.seed_id] = acct

        return {
            "added_count": 0,
            "merged_count": 0,
            "newly_added_variant_ids": [],
            "removed_from_failed": False,
            "moved_to_processed": False,
            "moved_to_manual_review": False,
        }


def _record_failed_retry_accounting(
    canonical: dict,
    seed_id: str,
    error: str,
    now: str,
) -> None:
    """Record a failed retry attempt in seed_accounting."""
    bs = canonical.setdefault("batch_state", {})
    bs.setdefault("seed_accounting", {})
    acct = bs["seed_accounting"].get(seed_id, {})
    acct["retry_source"] = "failed_seed_retry"
    acct["status"] = "failed"
    acct["last_error"] = error
    acct["last_attempt_at"] = now
    bs["seed_accounting"][seed_id] = acct
