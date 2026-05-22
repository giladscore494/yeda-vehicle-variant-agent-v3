"""Apply layer — the ONLY place that mutates canonical in memory."""
from __future__ import annotations

import copy
from datetime import datetime, timezone

from engine.types import Decision


def _merge_variant(existing: dict, incoming: dict) -> dict:
    """Merge incoming fields into existing, never overwriting rich data with empty."""
    out = copy.deepcopy(existing)
    _EMPTY = (None, "", [], {})

    for key in ("body_type", "seats", "engine", "transmission", "fuel_type",
                "drivetrain", "trim", "doors", "generation"):
        if key in incoming:
            existing_val = out.get(key)
            incoming_val = incoming[key]
            # If existing value is a VerifiedField dict, check .value
            if isinstance(existing_val, dict):
                if existing_val.get("value") in _EMPTY:
                    out[key] = incoming_val
            elif existing_val in _EMPTY:
                out[key] = incoming_val

    for key in ("year_start", "year_end", "market", "aliases", "notes",
                "official_marketed_name_il", "market_scope", "source_basis",
                "source_ids", "confidence_level"):
        if key in incoming and out.get(key) in _EMPTY:
            out[key] = incoming[key]

    out["updated_at"] = datetime.now(timezone.utc).isoformat()
    return out


def _merge_variants_into_canonical(canonical: dict, new_variants: list[dict]) -> dict:
    """Merge new variants into canonical. Returns merge stats."""
    verified = canonical.get("verified_variants") or []
    partial = canonical.get("partial_variants") or []
    all_variants = verified + partial

    index: dict[str, int] = {}
    for i, v in enumerate(all_variants):
        vid = str(v.get("variant_id", "")).strip()
        if vid and vid not in index:
            index[vid] = i

    added = 0
    merged = 0

    for incoming in new_variants:
        if not isinstance(incoming, dict):
            continue
        vid = str(incoming.get("variant_id", "")).strip()
        if not vid:
            continue
        if vid in index:
            idx = index[vid]
            all_variants[idx] = _merge_variant(all_variants[idx], incoming)
            merged += 1
        else:
            index[vid] = len(all_variants)
            all_variants.append(copy.deepcopy(incoming))
            added += 1

    # Rebuild verified/partial split
    new_verified = []
    new_partial = []
    for v in all_variants:
        if isinstance(v, dict) and v.get("verification_status") == "verified":
            new_verified.append(v)
        else:
            new_partial.append(v)

    canonical["verified_variants"] = new_verified
    canonical["partial_variants"] = new_partial

    return {"added_count": added, "merged_count": merged}


def apply_decision(canonical: dict, decision: Decision, is_current_next: bool = False) -> dict:
    """Apply a Decision to canonical in memory. Returns apply stats."""
    bs = canonical.setdefault("batch_state", {})
    bs.setdefault("processed_seed_ids", [])
    bs.setdefault("manual_review_seed_ids", [])
    bs.setdefault("failed_seed_ids", [])
    bs.setdefault("seed_accounting", {})
    now = datetime.now(timezone.utc).isoformat()
    stats = {"added_count": 0, "merged_count": 0}

    if decision.action == "ACCEPT_VARIANTS":
        merge_result = _merge_variants_into_canonical(canonical, decision.variants_to_add)
        stats["added_count"] = merge_result["added_count"]
        stats["merged_count"] = merge_result["merged_count"]

        if decision.seed_id not in bs["processed_seed_ids"]:
            bs["processed_seed_ids"].append(decision.seed_id)
        if decision.seed_id in bs["manual_review_seed_ids"]:
            bs["manual_review_seed_ids"].remove(decision.seed_id)
        if decision.seed_id in bs.get("failed_seed_ids", []):
            bs["failed_seed_ids"].remove(decision.seed_id)

        bs["seed_accounting"][decision.seed_id] = {
            "status": "resolved",
            "resolution_type": "variants_added",
            "added_count": merge_result["added_count"],
            "merged_count": merge_result["merged_count"],
            "warnings": decision.warnings,
            "resolved_at": now,
        }

        if is_current_next:
            bs["last_completed_seed_id"] = decision.seed_id

    elif decision.action == "CLOSE_NO_VARIANTS_PROVEN":
        if decision.seed_id not in bs["processed_seed_ids"]:
            bs["processed_seed_ids"].append(decision.seed_id)
        if decision.seed_id in bs["manual_review_seed_ids"]:
            bs["manual_review_seed_ids"].remove(decision.seed_id)
        if decision.seed_id in bs.get("failed_seed_ids", []):
            bs["failed_seed_ids"].remove(decision.seed_id)

        bs["seed_accounting"][decision.seed_id] = {
            "status": "resolved",
            "resolution_type": "no_variants_proven",
            "no_variants_reason": decision.reason,
            "proof_status": (decision.proof or {}).get("proof_status", "proven"),
            "source_ids": (decision.proof or {}).get("source_ids", []),
            "source_basis": (decision.proof or {}).get("source_basis", ""),
            "confidence": (decision.proof or {}).get("confidence", ""),
            "resolved_at": now,
        }

        if is_current_next:
            bs["last_completed_seed_id"] = decision.seed_id

    elif decision.action == "MANUAL_REVIEW":
        # Do NOT mark processed
        if decision.seed_id not in bs["manual_review_seed_ids"]:
            bs["manual_review_seed_ids"].append(decision.seed_id)

        bs["seed_accounting"][decision.seed_id] = {
            "status": "manual_review",
            "reason": decision.reason,
            "last_attempt_at": now,
        }

    elif decision.action == "FAIL_TRANSIENT":
        # Do NOT mark processed
        if decision.seed_id not in bs.get("failed_seed_ids", []):
            bs.setdefault("failed_seed_ids", []).append(decision.seed_id)

        bs["seed_accounting"][decision.seed_id] = {
            "status": "failed_transient",
            "reason": decision.reason,
            "error_summary": "; ".join(decision.warnings) if decision.warnings else "",
            "last_attempt_at": now,
        }

    return stats


def advance_cursor(canonical: dict, seeds: list[dict], current_seed_id: str) -> str | None:
    """Advance next_seed_id to the next unprocessed seed after current_seed_id.
    Returns the new next_seed_id or None if all done."""
    from engine.state import seed_id_from_seed
    bs = canonical.setdefault("batch_state", {})
    processed = set(bs.get("processed_seed_ids", []))
    manual = set(bs.get("manual_review_seed_ids", []))
    failed = set(bs.get("failed_seed_ids", []))
    skip = processed | manual | failed

    seed_ids = [seed_id_from_seed(s) for s in seeds]

    # Find the index of current_seed_id
    try:
        current_idx = seed_ids.index(current_seed_id)
    except ValueError:
        return bs.get("next_seed_id")

    # Find next unprocessed seed after current
    for i in range(current_idx + 1, len(seed_ids)):
        if seed_ids[i] not in skip:
            bs["next_seed_id"] = seed_ids[i]
            return seed_ids[i]

    # All remaining seeds are processed/manual/failed
    bs["next_seed_id"] = None
    return None
