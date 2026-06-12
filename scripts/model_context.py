"""Per-model validation context manager.

Maintains temporary working memory for one make/model at a time.
The active context accumulates known trims, evidence, and processed variants
while the engine processes all source variants for a single model.  When the
model is completed the context is finalized to an audit file and then reset
so the next model starts with a clean slate.

Important: this is NOT a global catalog.  It is short-lived per-model state.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


def _utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _slug(value: Any) -> str:
    s = str(value).strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_") or "unknown"


# ── Generic / weak source name detection ──────────────────────────────────

WEAK_SOURCE_NAMES: set[str] = {
    "", "base", "standard", "unknown", "n/a", "na", "none", "null",
    "tbd", "generic", "default", "-", "?", "...",
}


def is_weak_source_name(name: Any) -> bool:
    """Return True if *name* is generic / translated / empty / placeholder."""
    if name is None:
        return True
    if not isinstance(name, str):
        return False
    return name.strip().lower() in WEAK_SOURCE_NAMES or name.strip() == ""


# ── Trim candidate inside a model context ─────────────────────────────────

def empty_trim_candidate() -> dict:
    return {
        "trim_name": None,
        "official_marketed_name_il": None,
        "local_name_il": None,
        "lineup_position": "unknown",
        "unique_differentiator": None,
        "known_year_range": None,
        "known_engine": None,
        "known_transmission": None,
        "known_fuel_type": None,
        "known_body_type": None,
        "known_drivetrain": None,
        "evidence_strength": None,
        "evidence_summary": None,
        "status": "candidate",  # verified | candidate | ambiguous | rejected
    }


# ── Active model context ──────────────────────────────────────────────────

def fresh_context(make: str, model: str, global_model_name: str | None = None) -> dict:
    """Create a blank active model context."""
    return {
        "make": make,
        "model": model,
        "global_model_name": global_model_name,
        "market_scope": "IL",
        "processed_model_variants_count": 0,
        "known_or_candidate_israeli_trims": [],
        "official_marketed_names_found": [],
        "aliases_found": [],
        "trim_lineup_positions": {},
        "unique_differentiator_per_trim": {},
        "technical_fingerprints_seen": [],
        "already_resolved_variants": [],
        "already_rejected_variants": [],
        "ambiguous_fingerprints": [],
        "duplicate_groups_encountered": [],
        "evidence_summaries_discovered": [],
        "source_quality_warnings": [],
        "unresolved_questions": [],
        "completed": False,
        "started_at": _utcnow(),
        "last_updated_at": _utcnow(),
    }


def build_technical_fingerprint(sv: dict) -> dict:
    """Extract the technical fingerprint from a standard_variant."""
    return {
        "make": sv.get("make"),
        "model": sv.get("model"),
        "year_start": sv.get("year_start"),
        "year_end": sv.get("year_end"),
        "engine": sv.get("engine"),
        "transmission": sv.get("transmission"),
        "fuel_type": sv.get("fuel_type"),
        "body_type": sv.get("body_type"),
        "drivetrain": sv.get("drivetrain"),
        "seats": sv.get("seats"),
        "generation": sv.get("generation"),
        "market_scope": sv.get("market_scope", "IL"),
    }


def update_context_after_variant(
    ctx: dict,
    validation_id: str,
    sv: dict,
    decision: str,
    response: dict | None,
    fingerprint: dict,
) -> dict:
    """Mutate *ctx* in-place after processing one source variant."""
    ctx["processed_model_variants_count"] += 1
    ctx["last_updated_at"] = _utcnow()

    # Record fingerprint
    fp_key = json.dumps(fingerprint, sort_keys=True, ensure_ascii=False)
    if fp_key not in [json.dumps(f, sort_keys=True, ensure_ascii=False)
                      for f in ctx["technical_fingerprints_seen"]]:
        ctx["technical_fingerprints_seen"].append(fingerprint)

    trim = (sv.get("trim") or "").strip()
    source_weak = is_weak_source_name(trim)

    if source_weak:
        ctx["source_quality_warnings"].append(
            f"{validation_id}: source trim '{trim}' is weak/generic")

    if decision in ("auto_accept", "auto_resolved"):
        ctx["already_resolved_variants"].append(validation_id)
        # Extract trim info from response
        if response:
            cv = response.get("corrected_variant") or {}
            resolved_trim = cv.get("trim")
            if resolved_trim and not is_weak_source_name(resolved_trim):
                if resolved_trim not in ctx["known_or_candidate_israeli_trims"]:
                    ctx["known_or_candidate_israeli_trims"].append(resolved_trim)
                il_name = cv.get("official_marketed_name_il")
                if il_name and il_name not in ctx["official_marketed_names_found"]:
                    ctx["official_marketed_names_found"].append(il_name)
            ev = response.get("evidence_summary")
            if ev:
                ctx["evidence_summaries_discovered"].append(
                    f"{validation_id}: {ev[:200]}")
    elif decision in ("rejected_from_clean", "split_required", "failed"):
        ctx["already_rejected_variants"].append(validation_id)

    # Check for duplicate groups
    dup_group = sv.get("possible_duplicate_group")
    if dup_group and dup_group not in ctx["duplicate_groups_encountered"]:
        ctx["duplicate_groups_encountered"].append(dup_group)

    return ctx


def context_summary_for_prompt(ctx: dict) -> dict:
    """Return a compact summary of the active model context suitable for
    inclusion in a Gemini prompt.  Keeps only actionable information."""
    return {
        "make": ctx["make"],
        "model": ctx["model"],
        "global_model_name": ctx.get("global_model_name"),
        "market_scope": ctx["market_scope"],
        "processed_so_far": ctx["processed_model_variants_count"],
        "known_or_candidate_trims": ctx["known_or_candidate_israeli_trims"],
        "official_marketed_names": ctx["official_marketed_names_found"],
        "aliases": ctx["aliases_found"],
        "lineup_positions": ctx["trim_lineup_positions"],
        "already_resolved_count": len(ctx["already_resolved_variants"]),
        "already_rejected_count": len(ctx["already_rejected_variants"]),
        "ambiguous_fingerprints_count": len(ctx["ambiguous_fingerprints"]),
        "source_quality_warnings_count": len(ctx["source_quality_warnings"]),
    }


# ── Finalize / reset ──────────────────────────────────────────────────────

def finalize_context(ctx: dict) -> dict:
    """Mark the context as completed and return it as the final audit."""
    ctx["completed"] = True
    ctx["completed_at"] = _utcnow()
    ctx["last_updated_at"] = _utcnow()
    return ctx


def save_active_context(ctx: dict, output_dir: Path) -> Path:
    """Persist the active context to output/active_model_context.json."""
    path = output_dir / "active_model_context.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ctx, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def clear_active_context(output_dir: Path) -> None:
    """Delete or reset the active model context file."""
    path = output_dir / "active_model_context.json"
    if path.exists():
        path.write_text(json.dumps(
            {"status": "no_active_model", "cleared_at": _utcnow()},
            ensure_ascii=False, indent=2,
        ), encoding="utf-8")


def save_final_model_context(ctx: dict, model_run_dir: Path) -> Path:
    """Write the finalized model context to the model-level audit directory."""
    model_run_dir.mkdir(parents=True, exist_ok=True)
    path = model_run_dir / "final_model_context.json"
    path.write_text(json.dumps(ctx, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def model_run_dir(output_dir: Path, make: str, model: str) -> Path:
    """Return output/model_runs/{make_slug}/{model_slug}/."""
    return output_dir / "model_runs" / _slug(make) / _slug(model)


# ── Discovered missing variants ───────────────────────────────────────────

_discovery_counter = 0


def next_discovery_id() -> str:
    global _discovery_counter
    _discovery_counter += 1
    return f"DISC-{_discovery_counter:06d}"


def reset_discovery_counter() -> None:
    global _discovery_counter
    _discovery_counter = 0


def build_discovered_missing_variant(
    make: str,
    model: str,
    global_model_name: str | None,
    discovered_trim: str,
    evidence: dict,
    source_validation_id: str,
) -> dict:
    """Build a discovered-missing-variant record for the side-output."""
    return {
        "discovery_id": next_discovery_id(),
        "make": make,
        "model": model,
        "global_model_name": global_model_name,
        "market_scope": "IL",
        "discovered_trim": discovered_trim,
        "official_marketed_name_il": evidence.get("official_marketed_name_il"),
        "local_name_il": evidence.get("local_name_il"),
        "lineup_position": evidence.get("lineup_position", "unknown"),
        "unique_differentiator": evidence.get("unique_differentiator"),
        "year_start": evidence.get("year_start"),
        "year_end": evidence.get("year_end"),
        "engine": evidence.get("engine"),
        "transmission": evidence.get("transmission"),
        "fuel_type": evidence.get("fuel_type"),
        "body_type": evidence.get("body_type"),
        "drivetrain": evidence.get("drivetrain"),
        "seats": evidence.get("seats"),
        "evidence_strength": evidence.get("evidence_strength"),
        "evidence_summary": evidence.get("evidence_summary"),
        "source_urls_or_source_summaries": evidence.get(
            "source_urls_or_source_summaries", []),
        "discovered_while_processing_validation_id": source_validation_id,
        "reason_not_added_to_clean":
            "expansion candidate only; current run validates existing "
            "source variants only",
        "suggested_future_action":
            "review in future missing-variant expansion pass",
    }


def append_discovered_missing(
    record: dict,
    global_path: Path,
    model_path: Path,
) -> None:
    """Append a discovered-missing-variant record to both global and
    model-level JSONL files."""
    line = json.dumps(record, ensure_ascii=False) + "\n"
    for p in (global_path, model_path):
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as f:
            f.write(line)


# ── Group variants by make/model ──────────────────────────────────────────

def group_by_make_model(variants_by_id: dict) -> dict[tuple[str, str], list[str]]:
    """Return {(make, model): [validation_id, ...]} preserving insertion order."""
    groups: dict[tuple[str, str], list[str]] = {}
    for vid, variant in variants_by_id.items():
        sv = variant.get("standard_variant") or {}
        make = (sv.get("make") or "").strip()
        mdl = (sv.get("model") or "").strip()
        groups.setdefault((make, mdl), []).append(vid)
    return groups
