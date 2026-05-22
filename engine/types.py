"""Core data contracts for the engine."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class SeedRunResult:
    """Output of running one seed through the LLM discovery pipeline."""
    seed_id: str
    ok: bool
    candidate_variants: list[dict] = field(default_factory=list)
    no_variants_reason: str | None = None
    no_variants_source_ids: list[str] = field(default_factory=list)
    no_variants_source_basis: str | None = None
    no_variants_confidence: str | None = None
    sources: list[dict] = field(default_factory=list)
    raw_response: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


@dataclass
class Decision:
    """Final engine decision for a seed run."""
    action: Literal[
        "ACCEPT_VARIANTS",
        "CLOSE_NO_VARIANTS_PROVEN",
        "MANUAL_REVIEW",
        "FAIL_TRANSIENT",
    ]
    seed_id: str
    reason: str
    variants_to_add: list[dict] = field(default_factory=list)
    proof: dict | None = None
    warnings: list[str] = field(default_factory=list)
