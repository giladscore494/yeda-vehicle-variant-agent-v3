"""Core validation engine: mock + real Gemini, clustering reuse, resume.

The engine is model-agnostic at its core: it accepts an optional Gemini client
and an optional GitHub saver. In mock mode it never touches Gemini. In real
mode it grounds once per cluster anchor and reuses that evidence across the
cluster's member rows for cost control.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .clustering import Cluster, ClusterIndex, build_clusters
from .data_loader import JoinResult, get_standard
from .normalization import (
    detect_identity_blockers,
    extract_identity,
    extract_trim,
)
from .output_writer import (
    MODEL_DEFAULT,
    OutputStore,
    build_output_row,
)
from .reconcile import reconcile_validation_output

# Delimiters that suggest a single row bundles multiple distinct trims.
_SPLIT_DELIMITERS = (" / ", "/", " or ", ",", " + ", "+", " & ", "&", ";", "|")


# ---------------------------------------------------------------------------
# Pure decision helpers (covered by unit tests)
# ---------------------------------------------------------------------------


def looks_like_multi_trim(value: Optional[str]) -> bool:
    if not value:
        return False
    text = value.strip()
    for delim in _SPLIT_DELIMITERS:
        if delim in text:
            left, _, right = text.partition(delim.strip() if delim.strip() else delim)
            if left.strip() and right.strip():
                return True
    return False


def merge_identity_and_trim(identity_status: str, trim_weak: bool) -> str:
    """Combine an identity verdict with trim strength into a final decision.

    This encodes the core principle: a valid identity with weak trim becomes
    ``clean_partial`` (a success state), never ``reject``.
    """
    if identity_status == "invalid":
        return "reject"
    if trim_weak:
        return "clean_partial"
    return "clean_exact"


def decide_mock(identity: Dict[str, Any], trim_info: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic mock decision. Identity-strict, trim-flexible."""
    blockers = detect_identity_blockers(identity)
    trim_weak = bool(trim_info.get("trim_is_weak", True))
    trim_value = trim_info.get("trim")

    if blockers:
        return {
            "validation_decision": "reject",
            "identity_status": "invalid",
            "trim_status": "invalid" if trim_weak else "unresolved",
            "identity_confidence": 0.1,
            "trim_confidence": 0.0,
            "blocking_identity_issues": blockers,
            "non_blocking_trim_issues": [],
            "decision_reason": "Identity-level problem(s): " + ", ".join(blockers),
        }

    # Identity is valid from here on — trim can never cause a reject.
    # A weak/placeholder trim is resolved to clean_partial before any split
    # detection (e.g. "N/A" must not be misread as two trims "N" and "A").
    if trim_weak:
        return {
            "validation_decision": "clean_partial",
            "identity_status": "likely_valid",
            "trim_status": "unresolved",
            "identity_confidence": 0.7,
            "trim_confidence": 0.2,
            "non_blocking_trim_issues": ["trim_weak_or_missing"],
            "decision_reason": "Valid Israeli-market identity; trim weak/missing -> clean_partial.",
        }

    if looks_like_multi_trim(trim_value):
        candidates = [
            part.strip()
            for delim in (" / ", "/", ",", " or ", "+", "&", ";", "|")
            for part in (trim_value.split(delim) if delim in trim_value else [])
            if part.strip()
        ]
        # de-dup, keep order
        seen: set = set()
        split_candidates = []
        for c in candidates:
            if c.lower() not in seen:
                seen.add(c.lower())
                split_candidates.append({"trim": c})
        return {
            "validation_decision": "split_required",
            "identity_status": "likely_valid",
            "trim_status": "inferred",
            "identity_confidence": 0.7,
            "trim_confidence": 0.4,
            "split_candidates": split_candidates,
            "decision_reason": "Row appears to bundle multiple distinct trims.",
        }

    # Valid identity with a concrete, single, non-weak trim.
    return {
        "validation_decision": "clean_exact",
        "identity_status": "likely_valid",
        "trim_status": "verified",
        "identity_confidence": 0.8,
        "trim_confidence": 0.7,
        "decision_reason": "Valid identity with a concrete trim.",
    }


# ---------------------------------------------------------------------------
# Row builders
# ---------------------------------------------------------------------------


def _identity_overrides(identity: Dict[str, Any], trim_info: Dict[str, Any]) -> Dict[str, Any]:
    canonical_trim = None if trim_info.get("trim_is_weak") else trim_info.get("trim")
    unresolved = []
    if trim_info.get("trim_is_weak"):
        unresolved.append("canonical_trim")
    if not trim_info.get("official_marketed_name_il"):
        unresolved.append("official_marketed_name_il")
    return {
        "canonical_make": identity.get("make"),
        "canonical_model": identity.get("model"),
        "canonical_series_or_generation": identity.get("generation"),
        "canonical_trim": canonical_trim,
        "official_marketed_name_il": trim_info.get("official_marketed_name_il"),
        "body_type": identity.get("body_type"),
        "fuel_type": identity.get("fuel_type"),
        "engine": identity.get("engine"),
        "transmission": identity.get("transmission"),
        "drivetrain": identity.get("drivetrain"),
        "year_start": identity.get("year_start"),
        "year_end": identity.get("year_end"),
        "market_scope": identity.get("market_scope") or "IL",
        "fields_left_unresolved": unresolved,
    }


def build_mock_row(
    validation_id: str,
    identity: Dict[str, Any],
    trim_info: Dict[str, Any],
    cluster: Cluster,
) -> Dict[str, Any]:
    overrides = _identity_overrides(identity, trim_info)
    overrides.update(decide_mock(identity, trim_info))
    overrides["source_cluster_id"] = cluster.cluster_id
    overrides["grounding_cluster_id"] = cluster.cluster_id
    overrides["grounding_summary"] = "mock: no external grounding performed"
    return build_output_row(validation_id, **overrides)


def coerce_gemini_row(
    validation_id: str,
    raw: Dict[str, Any],
    identity: Dict[str, Any],
    trim_info: Dict[str, Any],
    cluster: Cluster,
    variant: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Map a raw Gemini JSON response into a schema-complete output row."""
    overrides = _identity_overrides(identity, trim_info)
    # Prefer model-provided values where present; fall back to input identity.
    for key in (
        "canonical_make",
        "canonical_model",
        "canonical_series_or_generation",
        "canonical_trim",
        "official_marketed_name_il",
        "body_type",
        "fuel_type",
        "engine",
        "transmission",
        "drivetrain",
        "year_start",
        "year_end",
        "validation_decision",
        "identity_status",
        "identity_confidence",
        "trim_status",
        "trim_confidence",
        "grounding_summary",
        "evidence_sources",
        "possible_trim_names",
        "split_candidates",
        "blocking_identity_issues",
        "non_blocking_trim_issues",
        "decision_reason",
    ):
        if raw.get(key) not in (None, "", []):
            overrides[key] = raw[key]
    overrides["source_cluster_id"] = cluster.cluster_id
    overrides["grounding_cluster_id"] = cluster.cluster_id
    row = build_output_row(validation_id, **overrides)
    # Deterministic audit post-processing (cleanup only; never rejects).
    return reconcile_validation_output(variant or {}, row, run_mode="real")


def build_reused_row(
    validation_id: str,
    identity: Dict[str, Any],
    trim_info: Dict[str, Any],
    cluster: Cluster,
    evidence: Dict[str, Any],
    variant: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Derive a member row from cached cluster (identity-level) evidence.

    Identity verdict is reused; the per-row trim still decides exact vs partial.
    """
    overrides = _identity_overrides(identity, trim_info)
    identity_status = evidence.get("identity_status", "likely_valid")
    trim_weak = bool(trim_info.get("trim_is_weak", True))
    decision = merge_identity_and_trim(identity_status, trim_weak)
    overrides.update(
        {
            "validation_decision": decision,
            "identity_status": identity_status,
            "identity_confidence": evidence.get("identity_confidence", 0.6),
            "trim_status": "unresolved" if trim_weak else "verified",
            "trim_confidence": 0.2 if trim_weak else 0.6,
            "grounding_summary": evidence.get("grounding_summary", ""),
            "evidence_sources": evidence.get("evidence_sources", []),
            "source_cluster_id": cluster.cluster_id,
            "grounding_cluster_id": cluster.cluster_id,
            "evidence_reused_from": evidence.get("anchor_id"),
            "decision_reason": (
                "Identity grounding reused from cluster anchor "
                f"{evidence.get('anchor_id')}; trim evaluated per-row."
            ),
        }
    )
    if decision == "clean_partial":
        overrides["non_blocking_trim_issues"] = ["trim_weak_or_missing"]
    row = build_output_row(validation_id, **overrides)
    # Deterministic audit post-processing (cleanup only; never rejects).
    return reconcile_validation_output(variant or {}, row, run_mode="real")


def evidence_from_row(row: Dict[str, Any], anchor_id: str) -> Dict[str, Any]:
    return {
        "anchor_id": anchor_id,
        "identity_status": row.get("identity_status"),
        "identity_confidence": row.get("identity_confidence"),
        "grounding_summary": row.get("grounding_summary"),
        "evidence_sources": row.get("evidence_sources", []),
    }


# ---------------------------------------------------------------------------
# Run configuration & engine
# ---------------------------------------------------------------------------


@dataclass
class RunConfig:
    mode: str = "mock"  # "mock" | "real"
    limit: Optional[int] = None
    force_reprocess: bool = False
    start_after_validation_id: Optional[str] = None
    checkpoint_every: int = 1
    stop_on_github_failure: bool = True
    stop_on_error: bool = False


@dataclass
class RunResult:
    store: OutputStore
    processed: int = 0
    gemini_called: bool = False
    github_attempted: bool = False
    stopped_reason: Optional[str] = None
    logs: List[str] = field(default_factory=list)


class GitHubSaver:
    """Adapter that pushes the store's files after a validated variant.

    ``commit_prefix`` is mode-specific so mock pushes are clearly labelled
    ("mock checkpoint: ...") and never masquerade as real checkpoints.
    """

    def __init__(self, checkpoint, paths: List[str], commit_prefix: str = "checkpoint") -> None:
        self._checkpoint = checkpoint
        self._paths = paths
        self._commit_prefix = commit_prefix

    def save(self, validation_id: str) -> List[str]:
        message = f"{self._commit_prefix}: validate {validation_id}"
        return self._checkpoint.save_paths(self._paths, message)


def run_validation(
    join: JoinResult,
    config: RunConfig,
    *,
    store: Optional[OutputStore] = None,
    gemini_client=None,
    github_saver: Optional[GitHubSaver] = None,
    model_id: str = MODEL_DEFAULT,
    log: Optional[Callable[[str], None]] = None,
    on_progress: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> RunResult:
    """Run validation over the joined dataset and persist after each variant."""
    logs: List[str] = []

    def _log(msg: str) -> None:
        logs.append(msg)
        if log:
            log(msg)

    if not join.ok:
        _log("Refusing to run: join validation failed.")
        return RunResult(store=store or OutputStore(), stopped_reason="join_failed", logs=logs)

    if config.mode == "real" and gemini_client is None:
        _log("Real mode requested but no Gemini client provided.")
        return RunResult(store=store or OutputStore(), stopped_reason="no_gemini_client", logs=logs)

    clusters: ClusterIndex = build_clusters(join.variants, join.ordered_ids)

    if store is None:
        from .run_paths import resolve_run_paths

        run_paths = resolve_run_paths(config.mode, model=model_id)
        store = OutputStore.for_paths(
            run_paths,
            total_input_variants=join.variant_count,
            total_instruction_records=join.instruction_count,
        )
        store.load_existing()

    # Hard guard: the store's run mode must match the requested run mode so a
    # mock run can never append to real output (and vice versa).
    if store.run_mode != config.mode:
        _log(
            f"Refusing to run: store run_mode={store.run_mode!r} does not match "
            f"config.mode={config.mode!r}."
        )
        return RunResult(store=store, stopped_reason="mode_mismatch", logs=logs)
    store.set_cluster_count(clusters.cluster_count)

    by_id = {v.get("validation_id"): v for v in join.variants}

    # Honor "start after" by trimming the head of the ordered id list.
    work_ids = list(join.ordered_ids)
    if config.start_after_validation_id and config.start_after_validation_id in work_ids:
        idx = work_ids.index(config.start_after_validation_id)
        work_ids = work_ids[idx + 1 :]

    result = RunResult(store=store, logs=logs)

    for vid in work_ids:
        if config.limit is not None and result.processed >= config.limit:
            result.stopped_reason = "limit_reached"
            break
        if not config.force_reprocess and store.is_completed(vid):
            continue

        variant = by_id.get(vid)
        instruction = join.instructions.get(vid, {})
        if variant is None:
            continue

        identity = extract_identity(variant)
        trim_info = extract_trim(variant)
        cluster = clusters.cluster_for(vid)

        try:
            if config.mode == "mock":
                row = build_mock_row(vid, identity, trim_info, cluster)
            else:
                evidence = store.cluster_cache.get(cluster.cluster_id)
                if evidence is None:
                    # Anchor: perform the single grounded Gemini call.
                    payload = {"validation_id": vid, "standard_variant": get_standard(variant)}
                    raw = gemini_client.validate(payload, instruction, None)
                    store.bump_gemini_calls()
                    result.gemini_called = True
                    row = coerce_gemini_row(vid, raw, identity, trim_info, cluster, variant)
                    store.cluster_cache[cluster.cluster_id] = evidence_from_row(row, vid)
                else:
                    # Member: reuse cluster identity grounding (no Gemini call).
                    row = build_reused_row(vid, identity, trim_info, cluster, evidence, variant)

            store.record(row)
            _log(
                f"{vid} [{cluster.cluster_id}] -> {row['validation_decision']}"
                f" :: {row['decision_reason'][:80]}"
            )
        except Exception as exc:  # noqa: BLE001 - per-row isolation
            store.record_failure(vid)
            store.flush()
            _log(f"ERROR {vid}: {exc}")
            if config.stop_on_error:
                result.stopped_reason = "row_error"
                break
            continue

        # Persist locally after every variant.
        if (result.processed + 1) % max(1, config.checkpoint_every) == 0:
            store.flush()
        else:
            store.flush()  # cheap enough; always keep disk current

        # Auto-save to GitHub after the local save completes.
        if github_saver is not None:
            result.github_attempted = True
            try:
                github_saver.save(vid)
                store.bump_github_checkpoints()
            except Exception as exc:  # noqa: BLE001 - surfaced to UI
                _log(f"GITHUB SAVE FAILED {vid}: {exc}")
                if config.stop_on_github_failure:
                    result.stopped_reason = "github_save_failed"
                    store.flush()
                    break

        result.processed += 1
        if on_progress:
            on_progress(
                {
                    "validation_id": vid,
                    "cluster_id": cluster.cluster_id,
                    "decision": row["validation_decision"],
                    "decision_reason": row["decision_reason"],
                    "processed": result.processed,
                    "decision_counts": dict(store.metadata["decision_counts"]),
                    "gemini_call_count": store.metadata["gemini_call_count"],
                    "github_checkpoint_count": store.metadata["github_checkpoint_count"],
                }
            )

    store.flush()
    if result.stopped_reason is None:
        result.stopped_reason = "completed"
    _log(f"Run finished: {result.stopped_reason}; processed={result.processed}")
    return result
