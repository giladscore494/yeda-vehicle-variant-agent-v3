"""Output schema construction, atomic writes, and checkpoint management.

Two artifacts are maintained side by side:

- the full output file  ``validated_vehicle_variants_full_gemini31_v1.json``
- the checkpoint file    ``...checkpoint.json``  (enables resume)

All writes are atomic: write to ``<path>.tmp``, flush+fsync, then ``os.replace``.
"""

from __future__ import annotations

import datetime
import json
import os
from typing import Any, Dict, List, Optional, Tuple

from .contamination import assert_file_matches_mode
from .run_paths import (
    REAL_CHECKPOINT_PATH,
    REAL_ENGINE,
    REAL_MODEL_DEFAULT,
    REAL_OUTPUT_PATH,
    REAL_SUMMARY_PATH,
)

# ---------------------------------------------------------------------------
# Paths (default to the real-mode dataset; see scripts/run_paths.py for the
# full mode-aware bundle). Kept as names for backwards compatibility.
# ---------------------------------------------------------------------------

OUTPUT_PATH = REAL_OUTPUT_PATH
CHECKPOINT_PATH = REAL_CHECKPOINT_PATH
RUN_SUMMARY_PATH = REAL_SUMMARY_PATH

MODEL_DEFAULT = REAL_MODEL_DEFAULT

# ---------------------------------------------------------------------------
# Allowed enums
# ---------------------------------------------------------------------------

VALIDATION_DECISIONS = ("clean_exact", "clean_partial", "split_required", "reject")
ACCEPTANCE_TIERS = ("exact", "partial", "none")
IDENTITY_STATUSES = ("verified", "likely_valid", "uncertain", "invalid")
TRIM_STATUSES = ("verified", "inferred", "unresolved", "invalid")
PUBLICATION_TYPES = ("exact_variant", "configurable_group", "review_only")

# decision -> required acceptance tier
DECISION_TIER = {
    "clean_exact": "exact",
    "clean_partial": "partial",
    "split_required": "none",
    "reject": "none",
}


def utc_now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Output row schema
# ---------------------------------------------------------------------------


def empty_output_row(validation_id: str) -> Dict[str, Any]:
    """A fully-defaulted output row with every required field present."""
    return {
        "validation_id": validation_id,
        "run_mode": None,
        "source_validation_id": validation_id,
        "source_cluster_id": None,
        "grounding_cluster_id": None,
        "evidence_reused_from": None,
        "canonical_make": None,
        "canonical_model": None,
        "canonical_series_or_generation": None,
        "canonical_trim": None,
        "official_marketed_name_il": None,
        "body_type": None,
        "fuel_type": None,
        "engine": None,
        "transmission": None,
        "drivetrain": None,
        "year_start": None,
        "year_end": None,
        "is_currently_produced": None,
        "is_currently_imported_il": None,
        "market_scope": "IL",
        "validation_decision": "clean_exact",
        "acceptance_tier": "exact",
        "identity_status": "verified",
        "identity_confidence": 0.0,
        "trim_status": "verified",
        "trim_confidence": 0.0,
        "field_validation": {},
        "source_support_matrix": [],
        "evidence_auditability": "missing",
        "grounding_status": {
            "gemini_grounding_required": True,
            "gemini_grounding_present": False,
            "gemini_grounding_quality": "missing",
            "gpt54_grounding_required": False,
            "gpt54_grounding_present": False,
            "gpt54_grounding_quality": "missing",
            "final_grounding_gate_passed": False,
        },
        "grounding_summary": "",
        "evidence_sources": [],
        "possible_trim_names": [],
        "split_candidates": [],
        "blocking_identity_issues": [],
        "non_blocking_trim_issues": [],
        "fields_changed": [],
        "fields_left_unresolved": [],
        "decision_reason": "",
        "_pipeline_version": None,
        "_flags_count": 0,
        "_flash_used": False,
        "adjudication_log": [],
        "publishable_to_clean_catalog": False,
        "final_route": "review_queue",
        "route_reason": "Routing not yet assigned.",
        "duplicate_group_id": None,
        "duplicate_of": None,
        # Israeli option-matrix publication model.
        "publication_type": "review_only",
        "user_selectable_fields": {},
        "option_matrix": [],
        "candidate_values": {},
    }


def build_output_row(validation_id: str, **overrides: Any) -> Dict[str, Any]:
    """Build a schema-complete row, applying overrides and enforcing rules."""
    row = empty_output_row(validation_id)
    for key, value in overrides.items():
        if key in row:
            row[key] = value
    # Always preserve the validation id (never let an override drop it).
    row["validation_id"] = validation_id
    if not row.get("source_validation_id"):
        row["source_validation_id"] = validation_id
    return enforce_consistency(row)


def enforce_consistency(row: Dict[str, Any]) -> Dict[str, Any]:
    """Force decision/tier coherence and clamp enums/confidences."""
    decision = row.get("validation_decision")
    if decision not in VALIDATION_DECISIONS:
        decision = "clean_partial"
        row["validation_decision"] = decision
    # Acceptance tier is fully determined by the decision.
    row["acceptance_tier"] = DECISION_TIER[decision]

    if row.get("identity_status") not in IDENTITY_STATUSES:
        row["identity_status"] = "uncertain"
    if row.get("trim_status") not in TRIM_STATUSES:
        row["trim_status"] = "unresolved"
    if row.get("publication_type") not in PUBLICATION_TYPES:
        row["publication_type"] = "review_only"
    for dict_field in ("user_selectable_fields", "candidate_values"):
        if not isinstance(row.get(dict_field), dict):
            row[dict_field] = {}
    if not isinstance(row.get("option_matrix"), list):
        row["option_matrix"] = []

    for conf in ("identity_confidence", "trim_confidence"):
        try:
            val = float(row.get(conf) or 0.0)
        except (TypeError, ValueError):
            val = 0.0
        row[conf] = max(0.0, min(1.0, val))

    for list_field in (
        "evidence_sources",
        "possible_trim_names",
        "split_candidates",
        "blocking_identity_issues",
        "non_blocking_trim_issues",
        "fields_changed",
        "fields_left_unresolved",
    ):
        if not isinstance(row.get(list_field), list):
            row[list_field] = []
    return row


def validate_output_row(row: Dict[str, Any]) -> List[str]:
    """Return a list of schema problems (empty == valid)."""
    problems: List[str] = []
    template = empty_output_row(row.get("validation_id", ""))
    for key in template:
        if key not in row:
            problems.append(f"missing field: {key}")
    if not row.get("validation_id"):
        problems.append("empty validation_id")
    if row.get("validation_decision") not in VALIDATION_DECISIONS:
        problems.append(f"bad validation_decision: {row.get('validation_decision')}")
    if row.get("acceptance_tier") not in ACCEPTANCE_TIERS:
        problems.append(f"bad acceptance_tier: {row.get('acceptance_tier')}")
    decision = row.get("validation_decision")
    if decision in DECISION_TIER and row.get("acceptance_tier") != DECISION_TIER[decision]:
        problems.append(
            f"acceptance_tier {row.get('acceptance_tier')} inconsistent with "
            f"decision {decision}"
        )
    return problems



# ---------------------------------------------------------------------------
# Final catalog routing + duplicate detection
# ---------------------------------------------------------------------------

_DUP_FIELDS = (
    "canonical_make", "canonical_model", "canonical_series_or_generation", "canonical_trim",
    "body_type", "fuel_type", "engine", "transmission", "drivetrain",
    "year_start", "year_end", "market_scope",
)

def _norm_fingerprint_value(value: Any) -> str:
    if value in (None, "", []):
        return "∅"
    text = " ".join(str(value).strip().lower().split())
    aliases = {"automatic": "auto", "automated manual": "robotic", "amt": "robotic", "fwd": "front"}
    return aliases.get(text, text)

def content_fingerprint(row: Dict[str, Any]) -> str:
    return "|".join(_norm_fingerprint_value(row.get(f)) for f in _DUP_FIELDS)

IDENTITY_CRITICAL_UNRESOLVED_FIELDS = {"fuel_type", "engine", "transmission", "drivetrain", "body_type", "year_start", "year_end"}

def _blocking_publish_issues(row: Dict[str, Any]) -> List[str]:
    issues = list(row.get("blocking_identity_issues") or [])
    if row.get("identity_status") not in {"verified", "likely_valid"}:
        issues.append("identity_status blocks clean catalog publishing")
    unresolved = set(row.get("fields_left_unresolved") or [])
    for field in sorted(unresolved & IDENTITY_CRITICAL_UNRESOLVED_FIELDS):
        issues.append(f"{field} remains unresolved")
    return issues

def _strict_unsealed_publish_ok(row: Dict[str, Any]) -> bool:
    """Strict clean_catalog gate for legacy rows that lack a final seal.

    ``clean_partial``, null/unresolved trims, splits and duplicates can never
    enter the canonical catalog. Only a complete ``clean_exact`` row qualifies.
    """
    unresolved = set(row.get("fields_left_unresolved") or [])
    return (
        row.get("validation_decision") == "clean_exact"
        and row.get("identity_status") in {"verified", "likely_valid"}
        and row.get("trim_status") == "verified"
        and row.get("canonical_trim") not in (None, "", [])
        and "canonical_trim" not in unresolved
        and not (unresolved & IDENTITY_CRITICAL_UNRESOLVED_FIELDS)
        and not row.get("split_candidates")
        and not row.get("blocking_identity_issues")
        and not _blocking_publish_issues(row)
    )


_PUBLICATION_RANK = {"exact_variant": 3, "configurable_group": 2, "review_only": 1}
_DECISION_RANK = {"clean_exact": 3, "clean_partial": 2, "split_required": 1, "reject": 0}


def _primary_score(row: Dict[str, Any]) -> tuple:
    """Higher is a better primary for a duplicate group (spec ordering)."""
    pub_rank = _PUBLICATION_RANK.get(row.get("publication_type"), 0)
    dec_rank = _DECISION_RANK.get(row.get("validation_decision"), 0)
    fv = row.get("field_validation") if isinstance(row.get("field_validation"), dict) else {}
    verified = sum(1 for v in fv.values() if isinstance(v, dict) and v.get("status") == "verified")
    direct_urls = sum(
        1 for s in (row.get("evidence_sources") or [])
        if isinstance(s, dict) and s.get("url") and s.get("source_type") not in (None, "unknown")
    )
    unresolved = len(row.get("fields_left_unresolved") or [])
    flags = len(row.get("guard_flags") or [])
    idc = float(row.get("identity_confidence") or 0.0)
    tc = float(row.get("trim_confidence") or 0.0)
    return (pub_rank, dec_rank, verified, direct_urls, -unresolved, -flags, idc, tc)


def _select_duplicate_primaries(rows: List[Dict[str, Any]]) -> Dict[str, str]:
    """Pick one primary validation_id per fingerprint group (materially same rows)."""
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(content_fingerprint(row), []).append(row)
    primary: Dict[str, str] = {}
    for fp, grp in groups.items():
        if len(grp) == 1:
            primary[fp] = grp[0].get("validation_id")
            continue
        # max() keeps the first row on ties, preserving input order.
        best = max(grp, key=_primary_score)
        primary[fp] = best.get("validation_id")
    return primary


def route_validated_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Assign final routing for the catalog.

    Rows are handled individually so a mix of final-sealed (new) and unsealed
    (legacy/checkpoint) rows is always safe:

    * Final-sealed rows keep their Python-authoritative routing. Routing is only
      ever made *stricter* here (cross-row duplicate detection), never relaxed.
    * Unsealed rows fall back to strict routing that can never publish a
      ``clean_partial`` row or a row with a null/unresolved trim.

    A primary row is chosen per duplicate group via :func:`_primary_score`
    (exact > configurable > review, more verified fields, stronger evidence,
    fewer unresolved/flags). Every other materially-identical row is routed away
    from the clean catalog with ``duplicate_of`` set to the primary.
    """
    primary_by_fp = _select_duplicate_primaries(rows)
    first_by_fp: Dict[str, str] = {}
    group_by_fp: Dict[str, str] = {}
    routed: List[Dict[str, Any]] = []
    for row in rows:
        row = dict(row)
        fp = content_fingerprint(row)
        row["duplicate_group_id"] = group_by_fp.setdefault(fp, f"dup-{abs(hash(fp)) & 0xffffffff:08x}")
        decision = row.get("validation_decision")
        primary_id = primary_by_fp.get(fp)
        is_dup = primary_id is not None and row.get("validation_id") != primary_id

        if row.get("final_seal_result"):
            # Final seal is authoritative. Apply only stricter duplicate routing.
            if is_dup and row.get("final_route") not in {"rejected", "split_queue"}:
                row["duplicate_of"] = primary_id
                row["publishable_to_clean_catalog"] = False
                row["final_route"] = "duplicate_queue"
                row["route_reason"] = f"Content duplicate of {row['duplicate_of']}; kept in full staging output only."
            else:
                row.setdefault("duplicate_of", None)
                if row.get("publishable_to_clean_catalog") and row.get("final_route") == "clean_catalog":
                    first_by_fp.setdefault(fp, row.get("validation_id"))
            routed.append(row)
            continue

        # Unsealed legacy row: strict fallback, never publish clean_partial.
        row["duplicate_of"] = None
        blocking = _blocking_publish_issues(row)
        if is_dup and decision in {"clean_exact", "clean_partial"}:
            row["duplicate_of"] = primary_id
            row["publishable_to_clean_catalog"] = False
            row["final_route"] = "duplicate_queue"
            row["route_reason"] = f"Content duplicate of {row['duplicate_of']}; kept in full staging output only."
        elif decision == "split_required" or row.get("split_candidates"):
            row["publishable_to_clean_catalog"] = False
            row["final_route"] = "split_queue"
            row["route_reason"] = "split_required rows must be split before clean catalog publishing."
        elif decision == "reject":
            row["publishable_to_clean_catalog"] = False
            row["final_route"] = "rejected"
            row["route_reason"] = "Rejected by validation decision."
        elif _strict_unsealed_publish_ok(row):
            row["publishable_to_clean_catalog"] = True
            row["final_route"] = "clean_catalog"
            row["route_reason"] = "Identity and trim verified; row meets strict clean_catalog policy."
            first_by_fp.setdefault(fp, row.get("validation_id"))
        elif not blocking and (
            decision == "clean_partial"
            or (
                row.get("identity_status") in {"verified", "likely_valid"}
                and row.get("trim_status") == "unresolved"
            )
        ):
            row["publishable_to_clean_catalog"] = False
            row["final_route"] = "partial_queue"
            row["route_reason"] = "clean_partial/unresolved trim is retained for partial review; strict routing blocks clean catalog."
        else:
            row["publishable_to_clean_catalog"] = False
            row["final_route"] = "review_queue"
            row["route_reason"] = "; ".join(blocking) or "Unresolved issue blocks clean catalog publishing."
        routed.append(row)
    return routed


# ---------------------------------------------------------------------------
# Upload readiness report (lightweight QA)
# ---------------------------------------------------------------------------


def _exact_publish_gate_ok(row: Dict[str, Any]) -> bool:
    """The strict gate a row must pass to belong in the exact clean catalog."""
    unresolved = set(row.get("fields_left_unresolved") or [])
    grounding = row.get("grounding_status") or {}
    return (
        row.get("publication_type") == "exact_variant"
        and row.get("validation_decision") == "clean_exact"
        and row.get("identity_status") == "verified"
        and row.get("trim_status") == "verified"
        and row.get("canonical_trim") not in (None, "", [])
        and "canonical_trim" not in unresolved
        and not (unresolved & IDENTITY_CRITICAL_UNRESOLVED_FIELDS)
        and not row.get("split_candidates")
        and not row.get("blocking_identity_issues")
        and row.get("duplicate_of") in (None, "")
        and not row.get("_unknown_enums")
        and grounding.get("final_grounding_gate_passed") is True
    )


def verify_row_consistency(row: Dict[str, Any]) -> List[tuple]:
    """Return (severity, message) consistency problems for a routed row."""
    errs: List[tuple] = []
    unresolved = set(row.get("fields_left_unresolved") or [])
    fv = row.get("field_validation") if isinstance(row.get("field_validation"), dict) else {}
    for f in sorted(unresolved):
        if row.get(f) not in (None, "", []):
            errs.append(("critical", f"{f} populated but listed in fields_left_unresolved"))
        info = fv.get(f)
        if isinstance(info, dict) and info.get("status") == "verified":
            errs.append(("critical", f"{f} unresolved but field_validation status is verified"))
    in_clean = row.get("final_route") == "clean_catalog" or row.get("publishable_to_clean_catalog")
    if in_clean:
        if not _exact_publish_gate_ok(row):
            errs.append(("critical", "row routed to clean_catalog but fails the strict exact publish gate"))
        if row.get("validation_decision") in {"clean_partial", "split_required", "reject"}:
            errs.append(("critical", "non-exact validation_decision in clean_catalog"))
        if row.get("publication_type") != "exact_variant":
            errs.append(("high", "clean_catalog row is not publication_type=exact_variant"))
        if row.get("duplicate_of"):
            errs.append(("critical", "duplicate row routed to clean_catalog"))
    if row.get("_unknown_enums"):
        errs.append(("high", "unknown enum survived final consistency"))
    return errs


def _configurable_group_consistent(row: Dict[str, Any]) -> bool:
    """A configurable group must offer real options and never publish as exact."""
    if row.get("publication_type") != "configurable_group":
        return True
    if row.get("publishable_to_clean_catalog") or row.get("final_route") == "clean_catalog":
        return False
    if row.get("identity_status") not in {"verified", "likely_valid"}:
        return False
    usf = row.get("user_selectable_fields") if isinstance(row.get("user_selectable_fields"), dict) else {}
    matrix = row.get("option_matrix") if isinstance(row.get("option_matrix"), list) else []
    has_options = matrix or any(isinstance(v, list) and v for v in usf.values()) or row.get("split_candidates")
    return bool(has_options)


def build_upload_readiness_report(rows: List[Dict[str, Any]], metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Lightweight end-of-run QA summary; never raises."""
    total = len(rows)
    exact = sum(1 for r in rows if r.get("publication_type") == "exact_variant")
    config = sum(1 for r in rows if r.get("publication_type") == "configurable_group")
    review = sum(1 for r in rows if r.get("publication_type") == "review_only")
    clean = sum(1 for r in rows if r.get("final_route") == "clean_catalog" and r.get("publishable_to_clean_catalog"))
    unknown_enum_errors = sum(1 for r in rows if r.get("_unknown_enums"))

    critical = 0
    high = 0
    for r in rows:
        for severity, _msg in verify_row_consistency(r):
            if severity == "critical":
                critical += 1
            elif severity == "high":
                high += 1

    # Duplicate group errors: groups with >1 row where none was marked primary.
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for r in rows:
        groups.setdefault(content_fingerprint(r), []).append(r)
    duplicate_group_errors = 0
    for grp in groups.values():
        if len(grp) > 1 and all(not g.get("duplicate_of") for g in grp):
            duplicate_group_errors += 1

    calls = int(metadata.get("stage3_repair_adjudicator_calls", 0) or 0)
    successes = int(metadata.get("stage3_repair_adjudicator_successes", 0) or 0)
    repair_success_rate = (successes / calls) if calls else 1.0
    grounded = sum(1 for r in rows if (r.get("grounding_status") or {}).get("final_grounding_gate_passed"))
    grounding_pass_rate = (grounded / total) if total else 0.0

    clean_rows = [r for r in rows if r.get("final_route") == "clean_catalog"]
    every_clean_passes = all(_exact_publish_gate_ok(r) for r in clean_rows)
    no_clean_partial_in_clean = not any(r.get("validation_decision") == "clean_partial" for r in clean_rows)
    no_split_in_clean = not any(r.get("validation_decision") == "split_required" for r in clean_rows)
    no_dup_in_clean = not any(r.get("duplicate_of") for r in clean_rows)

    ready_exact = bool(
        total > 0
        and critical == 0
        and unknown_enum_errors == 0
        and duplicate_group_errors == 0
        and every_clean_passes
        and no_clean_partial_in_clean
        and no_split_in_clean
        and no_dup_in_clean
    )
    config_rows = [r for r in rows if r.get("publication_type") == "configurable_group"]
    ready_config = bool(
        config_rows
        and unknown_enum_errors == 0
        and all(_configurable_group_consistent(r) for r in config_rows)
    )

    return {
        "ready_for_exact_clean_upload": ready_exact,
        "ready_for_configurable_group_upload": ready_config,
        "total_rows": total,
        "exact_variant_rows": exact,
        "configurable_group_rows": config,
        "review_only_rows": review,
        "clean_catalog_rows": clean,
        "critical_consistency_errors": critical,
        "high_consistency_errors": high,
        "unknown_enum_errors": unknown_enum_errors,
        "duplicate_group_errors": duplicate_group_errors,
        "repair_success_rate": round(repair_success_rate, 4),
        "grounding_pass_rate": round(grounding_pass_rate, 4),
    }


# ---------------------------------------------------------------------------
# Atomic write
# ---------------------------------------------------------------------------


def atomic_write_json(path: str, data: Any) -> None:
    """Write JSON atomically to avoid partial/corrupt files."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def _new_decision_counts() -> Dict[str, int]:
    return {d: 0 for d in VALIDATION_DECISIONS}


# ---------------------------------------------------------------------------
# Reset helpers (mode-scoped; never touch the two source files)
# ---------------------------------------------------------------------------


def _reset_paths(paths: List[str], log: Optional[Any] = None) -> List[str]:
    """Delete the given runtime files if present. Returns what was removed."""
    removed: List[str] = []
    for path in paths:
        if path and os.path.exists(path):
            os.remove(path)
            removed.append(os.path.basename(path))
            if log:
                log(f"reset: removed {path}")
    if log and not removed:
        log("reset: nothing to remove")
    return removed


def reset_mock_outputs(log: Optional[Any] = None) -> List[str]:
    """Delete only the mock output/checkpoint/summary files."""
    from .run_paths import resolve_run_paths

    rp = resolve_run_paths("mock")
    return _reset_paths([rp.output_path, rp.checkpoint_path, rp.summary_path], log)


def reset_real_outputs(log: Optional[Any] = None) -> List[str]:
    """Delete only the real output/checkpoint/summary files."""
    from .run_paths import resolve_run_paths

    rp = resolve_run_paths("real")
    return _reset_paths([rp.output_path, rp.checkpoint_path, rp.summary_path], log)


# ---------------------------------------------------------------------------
# Output + checkpoint store
# ---------------------------------------------------------------------------


class OutputStore:
    """Manages the output file and checkpoint, supporting resume."""

    def __init__(
        self,
        output_path: str = OUTPUT_PATH,
        checkpoint_path: str = CHECKPOINT_PATH,
        model: str = MODEL_DEFAULT,
        total_input_variants: int = 0,
        total_instruction_records: int = 0,
        *,
        run_mode: str = "real",
        engine: Optional[str] = None,
        summary_path: Optional[str] = None,
        is_mock_output: Optional[bool] = None,
    ) -> None:
        self.output_path = output_path
        self.checkpoint_path = checkpoint_path
        # When no summary path is given, derive one next to the output file so
        # an ad-hoc store (e.g. in tests) never writes into the real data dir.
        self.summary_path = summary_path or f"{output_path}.summary.json"
        self.model = model
        self.run_mode = run_mode
        if engine is None:
            engine = REAL_ENGINE
        if is_mock_output is None:
            is_mock_output = run_mode == "mock"

        self.metadata: Dict[str, Any] = {
            "engine": engine,
            "run_mode": run_mode,
            "is_mock_output": is_mock_output,
            "model": model,
            "market": "IL",
            "run_timestamp_utc": None,
            "total_input_variants": total_input_variants,
            "total_instruction_records": total_instruction_records,
            "total_validated_variants": 0,
            "decision_counts": _new_decision_counts(),
            "grounding_cluster_count": 0,
            "gemini_call_count": 0,
            "github_checkpoint_enabled": False,
            "github_checkpoint_count": 0,
            "github_checkpoint_fail_count": 0,
            "last_github_checkpoint_error": None,
            "last_validated_id": None,
            "schema_version": "v3_three_stage",
            "pipeline_version": "v3_three_stage",
            "stage1_pro_calls": 0,
            "stage2_guard_flags_total": 0,
            "stage3_flash_calls": 0,
            "flash_overrode_guard": 0,
            "guard_overrode_flash": 0,
            "stage3_guard_verifier_calls": 0,
            "stage3_guard_verifier_attempts": 0,
            "stage3_guard_verifier_successes": 0,
            "stage3_guard_verifier_failures": 0,
            "stage3_guard_verifier_model": "gpt-5.4",
            "stage3_openai_guard_verifier_calls": 0,
            "stage3_adjudicator_calls_total": 0,
            "last_guard_verifier_error": None,
            "guard_verifier_overrode_guard": 0,
            "guard_overrode_verifier": 0,
            "force_per_variant_validation": True,
            "stage0_preflight_risk_rows": 0,
            "stage1_gemini_grounding_required": 0,
            "stage1_gemini_grounding_present": 0,
            "stage1_gemini_grounding_missing": 0,
            "stage1_gemini_weak_grounding_rows": 0,
            "stage2_guard_flags_low": 0,
            "stage2_guard_flags_medium": 0,
            "stage2_guard_flags_high": 0,
            "stage2_guard_flags_critical": 0,
            "stage2_guard_patches_applied": 0,
            "stage25_repair_risk_scored_rows": 0,
            "stage25_repair_triggered_rows": 0,
            "stage3_repair_adjudicator_calls": 0,
            "stage3_repair_adjudicator_successes": 0,
            "stage3_repair_adjudicator_failures": 0,
            "stage3_repair_adjudicator_patches": 0,
            "stage3_repair_adjudicator_routing_changes": 0,
            "stage3_repair_adjudicator_summary_rewrites": 0,
            "stage3_repair_adjudicator_grounding_required": 0,
            "stage3_repair_adjudicator_grounding_present": 0,
            "stage3_repair_adjudicator_grounding_missing": 0,
            "stage4_final_seal_passed": 0,
            "stage4_final_seal_blocks": 0,
            "stage4_final_guard_conflicts_remaining": 0,
            "clean_catalog_blocks_by_repair": 0,
            "clean_catalog_blocks_by_final_seal": 0,
            "clean_catalog_blocks_by_grounding": 0,
            "clean_catalog_blocks_by_unresolved_trim": 0,
            "clean_catalog_blocks_by_unresolved_critical_field": 0,
        }
        # Ordered storage by id (preserves input order on flush).
        self.validated_by_id: Dict[str, Dict[str, Any]] = {}
        self.order: List[str] = []
        self.completed_ids: List[str] = []
        self.failed_ids: List[str] = []
        self.cluster_cache: Dict[str, Any] = {}

    @classmethod
    def for_paths(
        cls,
        run_paths,
        *,
        total_input_variants: int = 0,
        total_instruction_records: int = 0,
    ) -> "OutputStore":
        """Construct a store wired to a mode-resolved ``RunPaths`` bundle."""
        return cls(
            output_path=run_paths.output_path,
            checkpoint_path=run_paths.checkpoint_path,
            model=run_paths.model,
            total_input_variants=total_input_variants,
            total_instruction_records=total_instruction_records,
            run_mode=run_paths.mode,
            engine=run_paths.engine,
            summary_path=run_paths.summary_path,
            is_mock_output=run_paths.is_mock_output,
        )

    # -- load / resume -----------------------------------------------------

    def check_contamination(self) -> None:
        """Fail safely if any target file belongs to the other run mode."""
        for path in (self.output_path, self.checkpoint_path):
            assert_file_matches_mode(path, self.run_mode)

    def load_existing(self) -> None:
        """Reconcile any on-disk output + checkpoint into memory.

        Refuses to absorb a file that belongs to the other run mode so a real
        run can never reuse mock checkpoint data (and vice versa).
        """
        self.check_contamination()
        if os.path.exists(self.checkpoint_path):
            try:
                cp = json.load(open(self.checkpoint_path, encoding="utf-8"))
                self._absorb_checkpoint(cp)
            except Exception:  # noqa: BLE001 - tolerate corrupt checkpoint
                pass
        if os.path.exists(self.output_path):
            try:
                out = json.load(open(self.output_path, encoding="utf-8"))
                self._absorb_output(out)
            except Exception:  # noqa: BLE001
                pass

    def _absorb_checkpoint(self, cp: Dict[str, Any]) -> None:
        for row in (cp.get("validated_variants_by_id") or {}).values():
            self._index_row(row)
        for vid in cp.get("completed_validation_ids") or []:
            if vid not in self.completed_ids:
                self.completed_ids.append(vid)
        self.failed_ids = list(cp.get("failed_validation_ids") or [])
        self.cluster_cache.update(cp.get("cluster_cache") or {})
        cached_meta = cp.get("metadata") or {}
        if cached_meta.get("decision_counts"):
            for k in self.metadata["decision_counts"]:
                self.metadata["decision_counts"][k] = cached_meta["decision_counts"].get(k, 0)
        for k in ("gemini_call_count", "github_checkpoint_count", "grounding_cluster_count",
                  "stage1_pro_calls", "stage2_guard_flags_total", "stage3_flash_calls",
                  "flash_overrode_guard", "guard_overrode_flash", "stage3_guard_verifier_calls",
                  "stage3_openai_guard_verifier_calls", "stage3_guard_verifier_attempts",
                  "stage3_guard_verifier_successes", "stage3_guard_verifier_failures",
                  "stage3_adjudicator_calls_total", "guard_verifier_overrode_guard",
                  "guard_overrode_verifier", "github_checkpoint_fail_count",
                  # Stage 0/1 grounding + repair/final-seal counters (v4).
                  "stage0_preflight_risk_rows",
                  "stage1_gemini_grounding_required", "stage1_gemini_grounding_present",
                  "stage1_gemini_grounding_missing", "stage1_gemini_weak_grounding_rows",
                  "stage25_repair_risk_scored_rows", "stage25_repair_triggered_rows",
                  "stage25_repair_required_but_missing_adjudicator",
                  "stage3_repair_adjudicator_calls", "stage3_repair_adjudicator_successes",
                  "stage3_repair_adjudicator_failures", "stage3_repair_adjudicator_patches",
                  "stage3_repair_adjudicator_routing_changes",
                  "stage3_repair_adjudicator_summary_rewrites",
                  "stage3_repair_adjudicator_grounding_required",
                  "stage3_repair_adjudicator_grounding_present",
                  "stage3_repair_adjudicator_grounding_missing",
                  "stage4_final_seal_passed", "stage4_final_seal_blocks",
                  "stage4_final_guard_conflicts_remaining",
                  "clean_catalog_blocks_by_repair", "clean_catalog_blocks_by_final_seal",
                  "clean_catalog_blocks_by_grounding", "clean_catalog_blocks_by_unresolved_trim",
                  "clean_catalog_blocks_by_unresolved_critical_field",
                  "clean_catalog_blocks_by_clean_partial",
                  "clean_catalog_blocks_by_split_required",
                  "legacy_guard_verifier_calls", "legacy_guard_verifier_used"):
            if cached_meta.get(k):
                self.metadata[k] = cached_meta[k]
        if "github_checkpoint_enabled" in cached_meta:
            self.metadata["github_checkpoint_enabled"] = bool(cached_meta.get("github_checkpoint_enabled"))
        if "last_github_checkpoint_error" in cached_meta:
            self.metadata["last_github_checkpoint_error"] = cached_meta.get("last_github_checkpoint_error")
        if cp.get("last_validated_id"):
            self.metadata["last_validated_id"] = cp["last_validated_id"]

    def _absorb_output(self, out: Dict[str, Any]) -> None:
        for row in out.get("validated_variants") or []:
            self._index_row(row)

    def _index_row(self, row: Dict[str, Any]) -> None:
        vid = row.get("validation_id")
        if not vid:
            return
        # Backfill run_mode on absorbed rows (contamination is already ruled out).
        if not row.get("run_mode"):
            row["run_mode"] = self.run_mode
        if vid not in self.validated_by_id:
            self.order.append(vid)
        self.validated_by_id[vid] = row
        if vid not in self.completed_ids:
            self.completed_ids.append(vid)

    # -- mutation ----------------------------------------------------------

    def is_completed(self, validation_id: str) -> bool:
        return validation_id in self.validated_by_id

    def record(self, row: Dict[str, Any]) -> None:
        """Add/replace a validated row and update counts."""
        # Every row is stamped with this store's run mode so contamination is
        # deterministically detectable later.
        row["run_mode"] = self.run_mode
        vid = row["validation_id"]
        previous = self.validated_by_id.get(vid)
        if previous is not None:
            prev_dec = previous.get("validation_decision")
            if prev_dec in self.metadata["decision_counts"]:
                self.metadata["decision_counts"][prev_dec] -= 1
        else:
            self.order.append(vid)
        self.validated_by_id[vid] = row
        if vid not in self.completed_ids:
            self.completed_ids.append(vid)
        if vid in self.failed_ids:
            self.failed_ids.remove(vid)

        dec = row.get("validation_decision")
        if dec in self.metadata["decision_counts"]:
            self.metadata["decision_counts"][dec] += 1
        self.metadata["last_validated_id"] = vid
        self.metadata["total_validated_variants"] = len(self.validated_by_id)
        if row.get("final_seal_result"):
            if row["final_seal_result"].get("blocks_clean_catalog"):
                self.metadata["stage4_final_seal_blocks"] = self.metadata.get("stage4_final_seal_blocks", 0) + 1
                self.metadata["clean_catalog_blocks_by_final_seal"] = self.metadata.get("clean_catalog_blocks_by_final_seal", 0) + 1
            else:
                self.metadata["stage4_final_seal_passed"] = self.metadata.get("stage4_final_seal_passed", 0) + 1
        gs = row.get("grounding_status") if isinstance(row.get("grounding_status"), dict) else {}
        if gs:
            self.metadata["stage1_gemini_grounding_required"] = self.metadata.get("stage1_gemini_grounding_required", 0) + int(bool(gs.get("gemini_grounding_required")))
            self.metadata["stage1_gemini_grounding_present"] = self.metadata.get("stage1_gemini_grounding_present", 0) + int(bool(gs.get("gemini_grounding_present")))
            self.metadata["stage1_gemini_grounding_missing"] = self.metadata.get("stage1_gemini_grounding_missing", 0) + int(not bool(gs.get("gemini_grounding_present")))
            self.metadata["stage1_gemini_weak_grounding_rows"] = self.metadata.get("stage1_gemini_weak_grounding_rows", 0) + int(gs.get("gemini_grounding_quality") in {"weak", "missing"})
            if gs.get("gpt54_grounding_required"):
                self.metadata["stage3_repair_adjudicator_grounding_required"] = self.metadata.get("stage3_repair_adjudicator_grounding_required", 0) + 1
                if gs.get("gpt54_grounding_present"):
                    self.metadata["stage3_repair_adjudicator_grounding_present"] = self.metadata.get("stage3_repair_adjudicator_grounding_present", 0) + 1
                else:
                    self.metadata["stage3_repair_adjudicator_grounding_missing"] = self.metadata.get("stage3_repair_adjudicator_grounding_missing", 0) + 1
            if not gs.get("final_grounding_gate_passed"):
                self.metadata["clean_catalog_blocks_by_grounding"] = self.metadata.get("clean_catalog_blocks_by_grounding", 0) + 1
        unresolved = set(row.get("fields_left_unresolved") or [])
        if row.get("canonical_trim") in (None, "", []) or row.get("trim_status") == "unresolved" or "canonical_trim" in unresolved:
            self.metadata["clean_catalog_blocks_by_unresolved_trim"] = self.metadata.get("clean_catalog_blocks_by_unresolved_trim", 0) + 1
        if unresolved & IDENTITY_CRITICAL_UNRESOLVED_FIELDS:
            self.metadata["clean_catalog_blocks_by_unresolved_critical_field"] = self.metadata.get("clean_catalog_blocks_by_unresolved_critical_field", 0) + 1

    def record_failure(self, validation_id: str) -> None:
        if validation_id not in self.failed_ids:
            self.failed_ids.append(validation_id)

    def bump_gemini_calls(self, n: int = 1) -> None:
        self.metadata["gemini_call_count"] += n

    def set_github_checkpoint_enabled(self, value: bool) -> None:
        self.metadata["github_checkpoint_enabled"] = bool(value)

    def bump_github_checkpoints(self, n: int = 1) -> None:
        self.metadata["github_checkpoint_count"] += n
        self.metadata["last_github_checkpoint_error"] = None

    def record_github_checkpoint_failure(self, error: str) -> None:
        self.metadata["github_checkpoint_fail_count"] += 1
        self.metadata["last_github_checkpoint_error"] = str(error)

    def bump_stage1_pro_calls(self, n: int = 1) -> None:
        self.metadata["stage1_pro_calls"] += n

    def bump_stage2_guard_flags(self, n: int = 1) -> None:
        self.metadata["stage2_guard_flags_total"] += n

    def bump_stage3_flash_calls(self, n: int = 1) -> None:
        self.metadata["stage3_flash_calls"] += n

    def bump_flash_overrode_guard(self, n: int = 1) -> None:
        self.metadata["flash_overrode_guard"] += n

    def bump_guard_overrode_flash(self, n: int = 1) -> None:
        self.metadata["guard_overrode_flash"] += n

    def bump_stage3_guard_verifier_attempts(self, n: int = 1) -> None:
        self.metadata["stage3_guard_verifier_calls"] += n
        self.metadata["stage3_guard_verifier_attempts"] += n
        self.metadata["stage3_openai_guard_verifier_calls"] += n
        self.metadata["stage3_adjudicator_calls_total"] += n

    def bump_stage3_guard_verifier_successes(self, n: int = 1) -> None:
        self.metadata["stage3_guard_verifier_successes"] += n
        self.metadata["last_guard_verifier_error"] = None

    def bump_stage3_guard_verifier_failures(self, n: int = 1, error: str | None = None) -> None:
        self.metadata["stage3_guard_verifier_failures"] += n
        if error:
            self.metadata["last_guard_verifier_error"] = str(error)

    def bump_stage3_guard_verifier_calls(self, n: int = 1) -> None:
        self.bump_stage3_guard_verifier_attempts(n)

    def bump_guard_verifier_overrode_guard(self, n: int = 1) -> None:
        self.metadata["guard_verifier_overrode_guard"] += n
        self.metadata["flash_overrode_guard"] += n

    def bump_guard_overrode_verifier(self, n: int = 1) -> None:
        self.metadata["guard_overrode_verifier"] += n
        self.metadata["guard_overrode_flash"] += n

    def set_guard_verifier_model(self, model_id: str) -> None:
        self.metadata["stage3_guard_verifier_model"] = model_id

    def set_force_per_variant_validation(self, value: bool) -> None:
        self.metadata["force_per_variant_validation"] = bool(value)

    def set_cluster_count(self, n: int) -> None:
        self.metadata["grounding_cluster_count"] = n

    # -- serialization -----------------------------------------------------

    def output_document(self) -> Dict[str, Any]:
        self.metadata["run_timestamp_utc"] = self.metadata.get("run_timestamp_utc") or utc_now_iso()
        self.metadata["total_validated_variants"] = len(self.validated_by_id)
        rows = route_validated_rows([self.validated_by_id[v] for v in self.order if v in self.validated_by_id])
        self.metadata["upload_readiness"] = build_upload_readiness_report(rows, self.metadata)
        return {"metadata": dict(self.metadata), "validated_variants": rows}

    def checkpoint_document(self) -> Dict[str, Any]:
        return {
            "metadata": dict(self.metadata),
            "completed_validation_ids": list(self.completed_ids),
            "failed_validation_ids": list(self.failed_ids),
            "validated_variants_by_id": dict(self.validated_by_id),
            "cluster_cache": dict(self.cluster_cache),
            "decision_counts": dict(self.metadata["decision_counts"]),
            "last_validated_id": self.metadata["last_validated_id"],
            "updated_at_utc": utc_now_iso(),
        }

    def summary_document(self) -> Dict[str, Any]:
        return {
            "engine": self.metadata["engine"],
            "run_mode": self.run_mode,
            "is_mock_output": self.metadata["is_mock_output"],
            "model": self.metadata["model"],
            "market": self.metadata["market"],
            "run_timestamp_utc": self.metadata.get("run_timestamp_utc") or utc_now_iso(),
            "output_path": os.path.basename(self.output_path),
            "checkpoint_path": os.path.basename(self.checkpoint_path),
            "total_input_variants": self.metadata["total_input_variants"],
            "total_validated_variants": len(self.validated_by_id),
            "decision_counts": dict(self.metadata["decision_counts"]),
            "gemini_call_count": self.metadata["gemini_call_count"],
            "github_checkpoint_enabled": self.metadata["github_checkpoint_enabled"],
            "github_checkpoint_count": self.metadata["github_checkpoint_count"],
            "github_checkpoint_fail_count": self.metadata["github_checkpoint_fail_count"],
            "last_github_checkpoint_error": self.metadata["last_github_checkpoint_error"],
            "grounding_cluster_count": self.metadata["grounding_cluster_count"],
            "stage1_pro_calls": self.metadata["stage1_pro_calls"],
            "stage2_guard_flags_total": self.metadata["stage2_guard_flags_total"],
            "stage3_flash_calls": self.metadata["stage3_flash_calls"],
            "flash_overrode_guard": self.metadata["flash_overrode_guard"],
            "guard_overrode_flash": self.metadata["guard_overrode_flash"],
            "stage3_guard_verifier_calls": self.metadata["stage3_guard_verifier_calls"],
            "stage3_guard_verifier_model": self.metadata["stage3_guard_verifier_model"],
            "stage3_openai_guard_verifier_calls": self.metadata["stage3_openai_guard_verifier_calls"],
            "stage3_guard_verifier_attempts": self.metadata["stage3_guard_verifier_attempts"],
            "stage3_guard_verifier_successes": self.metadata["stage3_guard_verifier_successes"],
            "stage3_guard_verifier_failures": self.metadata["stage3_guard_verifier_failures"],
            "stage3_adjudicator_calls_total": self.metadata["stage3_adjudicator_calls_total"],
            "last_guard_verifier_error": self.metadata["last_guard_verifier_error"],
            "guard_verifier_overrode_guard": self.metadata["guard_verifier_overrode_guard"],
            "guard_overrode_verifier": self.metadata["guard_overrode_verifier"],
            "force_per_variant_validation": self.metadata["force_per_variant_validation"],
            "failed_validation_ids": list(self.failed_ids),
            "last_validated_id": self.metadata["last_validated_id"],
            "updated_at_utc": utc_now_iso(),
        }

    def flush(self) -> None:
        """Atomically persist the output, checkpoint, summary, and QA report."""
        document = self.output_document()
        atomic_write_json(self.output_path, document)
        atomic_write_json(self.checkpoint_path, self.checkpoint_document())
        atomic_write_json(self.summary_path, self.summary_document())
        readiness_path = os.path.join(os.path.dirname(self.output_path), "upload_readiness_report.json")
        atomic_write_json(readiness_path, document["metadata"].get("upload_readiness", {}))

    def latest_row(self) -> Optional[Dict[str, Any]]:
        vid = self.metadata.get("last_validated_id")
        if vid:
            return self.validated_by_id.get(vid)
        return None
