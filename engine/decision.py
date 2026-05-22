"""Decision engine — the ONLY place that decides final action for a seed run."""
from __future__ import annotations

import logging

from engine.types import SeedRunResult, Decision
from core.source_ids import (
    has_only_placeholder_source_ids,
    filter_real_source_ids,
    looks_like_placeholder_source_id,
)
from core.variant_id import generate_variant_id

logger = logging.getLogger(__name__)

_DEFAULT_MARKET = "il"


def _quality_filter(candidates: list[dict]) -> list[dict]:
    """Filter out candidates that are obviously invalid."""
    valid = []
    for c in candidates:
        if not isinstance(c, dict):
            continue
        # Must have at least make and model
        if not c.get("make") or not c.get("model"):
            continue
        valid.append(c)
    return valid


_VARIANT_ID_REQUIRED_FIELDS = ("make", "model", "year_start", "year_end")


def _ensure_variant_ids(candidates: list[dict]) -> tuple[list[dict], list[str]]:
    """Ensure every candidate has a deterministic variant_id.

    Returns (enriched_candidates, warnings) where enriched_candidates only
    contains candidates that received a valid variant_id.
    """
    enriched = []
    warnings: list[str] = []
    for c in candidates:
        if str(c.get("variant_id", "")).strip():
            enriched.append(c)
            continue
        # Check required fields for variant_id generation
        missing = [f for f in _VARIANT_ID_REQUIRED_FIELDS if not c.get(f)]
        if missing:
            warnings.append(
                f"candidate missing {missing} — cannot generate variant_id, skipped"
            )
            continue
        vid = generate_variant_id(
            make=c["make"],
            model=c["model"],
            year_start=c["year_start"],
            year_end=c["year_end"],
            market=c.get("market_scope") or c.get("market") or _DEFAULT_MARKET,
            generation=c.get("generation"),
            engine=c.get("engine"),
            transmission=c.get("transmission"),
            body_type=c.get("body_type"),
            fuel_type=c.get("fuel_type"),
        )
        c["variant_id"] = vid
        enriched.append(c)
    return enriched, warnings


def _has_valid_no_variants_proof(result: SeedRunResult) -> bool:
    """Check if zero-variant closure has valid, non-placeholder proof."""
    # Must have source_ids
    if not result.no_variants_source_ids:
        return False

    # Must not be all placeholders
    real_ids = filter_real_source_ids(result.no_variants_source_ids)
    if not real_ids:
        return False

    # Must have source_basis
    if not (result.no_variants_source_basis or "").strip():
        return False

    # Confidence must be medium or high
    if result.no_variants_confidence not in ("medium", "high"):
        return False

    # If sources are provided, verify source_ids reference actual sources
    if result.sources:
        available_ids = {
            str(s.get("source_id", "")).strip()
            for s in result.sources
            if isinstance(s, dict) and s.get("source_id")
        }
        for sid in real_ids:
            if sid not in available_ids:
                return False

    return True


def decide_seed_result(result: SeedRunResult) -> Decision:
    """Decide the final action for a seed run result."""
    if not result.ok:
        return Decision(
            action="FAIL_TRANSIENT",
            seed_id=result.seed_id,
            reason="runner_failed",
            variants_to_add=[],
            proof=None,
            warnings=result.errors,
        )

    valid_candidates = _quality_filter(result.candidate_variants)

    if valid_candidates:
        enriched, id_warnings = _ensure_variant_ids(valid_candidates)
        if not enriched:
            return Decision(
                action="MANUAL_REVIEW",
                seed_id=result.seed_id,
                reason="no_mergeable_candidates_after_variant_id_generation",
                variants_to_add=[],
                proof=None,
                warnings=id_warnings,
            )
        return Decision(
            action="ACCEPT_VARIANTS",
            seed_id=result.seed_id,
            reason="valid_candidates_found",
            variants_to_add=enriched,
            proof=None,
            warnings=id_warnings,
        )

    # No valid candidates — check no_variants_reason
    if result.no_variants_reason == "model_not_sold_in_market":
        if _has_valid_no_variants_proof(result):
            return Decision(
                action="CLOSE_NO_VARIANTS_PROVEN",
                seed_id=result.seed_id,
                reason="model_not_sold_in_market_proven",
                variants_to_add=[],
                proof={
                    "proof_status": "proven",
                    "source_ids": result.no_variants_source_ids,
                    "source_basis": result.no_variants_source_basis,
                    "confidence": result.no_variants_confidence,
                },
                warnings=[],
            )
        return Decision(
            action="MANUAL_REVIEW",
            seed_id=result.seed_id,
            reason="zero_variants_without_valid_non_placeholder_sources",
            variants_to_add=[],
            proof=None,
            warnings=[],
        )

    if result.no_variants_reason in {
        "no_reliable_sources_found",
        "insufficient_grounded_data",
        "source_conflict_unresolved",
        "blocked_by_validation",
    }:
        return Decision(
            action="MANUAL_REVIEW",
            seed_id=result.seed_id,
            reason=result.no_variants_reason,
            variants_to_add=[],
            proof=None,
            warnings=[],
        )

    return Decision(
        action="MANUAL_REVIEW",
        seed_id=result.seed_id,
        reason="unresolved_or_empty_result",
        variants_to_add=[],
        proof=None,
        warnings=[],
    )
