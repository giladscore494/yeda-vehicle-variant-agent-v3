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
from typing import Any, Dict, List, Optional

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
            "github_checkpoint_count": 0,
            "last_validated_id": None,
            "schema_version": "v3_three_stage",
            "pipeline_version": "v3_three_stage",
            "stage1_pro_calls": 0,
            "stage2_guard_flags_total": 0,
            "stage3_flash_calls": 0,
            "flash_overrode_guard": 0,
            "guard_overrode_flash": 0,
            "force_per_variant_validation": True,
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
                  "flash_overrode_guard", "guard_overrode_flash"):
            if cached_meta.get(k):
                self.metadata[k] = cached_meta[k]
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

    def record_failure(self, validation_id: str) -> None:
        if validation_id not in self.failed_ids:
            self.failed_ids.append(validation_id)

    def bump_gemini_calls(self, n: int = 1) -> None:
        self.metadata["gemini_call_count"] += n

    def bump_github_checkpoints(self, n: int = 1) -> None:
        self.metadata["github_checkpoint_count"] += n

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

    def set_force_per_variant_validation(self, value: bool) -> None:
        self.metadata["force_per_variant_validation"] = bool(value)

    def set_cluster_count(self, n: int) -> None:
        self.metadata["grounding_cluster_count"] = n

    # -- serialization -----------------------------------------------------

    def output_document(self) -> Dict[str, Any]:
        self.metadata["run_timestamp_utc"] = self.metadata.get("run_timestamp_utc") or utc_now_iso()
        self.metadata["total_validated_variants"] = len(self.validated_by_id)
        rows = [self.validated_by_id[v] for v in self.order if v in self.validated_by_id]
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
            "github_checkpoint_count": self.metadata["github_checkpoint_count"],
            "grounding_cluster_count": self.metadata["grounding_cluster_count"],
            "stage1_pro_calls": self.metadata["stage1_pro_calls"],
            "stage2_guard_flags_total": self.metadata["stage2_guard_flags_total"],
            "stage3_flash_calls": self.metadata["stage3_flash_calls"],
            "flash_overrode_guard": self.metadata["flash_overrode_guard"],
            "guard_overrode_flash": self.metadata["guard_overrode_flash"],
            "force_per_variant_validation": self.metadata["force_per_variant_validation"],
            "failed_validation_ids": list(self.failed_ids),
            "last_validated_id": self.metadata["last_validated_id"],
            "updated_at_utc": utc_now_iso(),
        }

    def flush(self) -> None:
        """Atomically persist the output, checkpoint, and summary files."""
        atomic_write_json(self.output_path, self.output_document())
        atomic_write_json(self.checkpoint_path, self.checkpoint_document())
        atomic_write_json(self.summary_path, self.summary_document())

    def latest_row(self) -> Optional[Dict[str, Any]]:
        vid = self.metadata.get("last_validated_id")
        if vid:
            return self.validated_by_id.get(vid)
        return None
