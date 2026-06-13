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

from .data_loader import DATA_DIR

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

OUTPUT_PATH = os.path.join(DATA_DIR, "validated_vehicle_variants_full_gemini31_v1.json")
CHECKPOINT_PATH = os.path.join(
    DATA_DIR, "validated_vehicle_variants_full_gemini31_v1.checkpoint.json"
)
RUN_SUMMARY_PATH = os.path.join(DATA_DIR, "validation_run_summary_gemini31.json")

MODEL_DEFAULT = "gemini-3.1-pro-preview"

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
    ) -> None:
        self.output_path = output_path
        self.checkpoint_path = checkpoint_path
        self.model = model

        self.metadata: Dict[str, Any] = {
            "engine": "gemini31_streamlit_sampled_validation",
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
        }
        # Ordered storage by id (preserves input order on flush).
        self.validated_by_id: Dict[str, Dict[str, Any]] = {}
        self.order: List[str] = []
        self.completed_ids: List[str] = []
        self.failed_ids: List[str] = []
        self.cluster_cache: Dict[str, Any] = {}

    # -- load / resume -----------------------------------------------------

    def load_existing(self) -> None:
        """Reconcile any on-disk output + checkpoint into memory."""
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
        for k in ("gemini_call_count", "github_checkpoint_count", "grounding_cluster_count"):
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

    def flush(self) -> None:
        """Atomically persist both the output and checkpoint files locally."""
        atomic_write_json(self.output_path, self.output_document())
        atomic_write_json(self.checkpoint_path, self.checkpoint_document())

    def latest_row(self) -> Optional[Dict[str, Any]]:
        vid = self.metadata.get("last_validated_id")
        if vid:
            return self.validated_by_id.get(vid)
        return None
