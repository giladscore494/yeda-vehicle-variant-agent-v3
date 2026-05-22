"""Run one seed through the LLM discovery pipeline.

Does NOT save, push, or mark processed.
Returns a SeedRunResult.
"""
from __future__ import annotations

from engine.types import SeedRunResult
from llm.client import call_model
from llm.parse import parse_llm_response
from llm.prompts import build_discovery_prompt


def run_seed(seed: dict, seed_id: str, dry_run: bool = False) -> SeedRunResult:
    """Run a single seed through LLM discovery. Returns SeedRunResult."""
    try:
        prompt = build_discovery_prompt(seed)

        if dry_run:
            return SeedRunResult(
                seed_id=seed_id,
                ok=True,
                candidate_variants=[],
                no_variants_reason="dry_run",
                raw_response={"dry_run": True, "prompt_preview": prompt[:500]},
            )

        raw_text = call_model(prompt)
        result = parse_llm_response(raw_text, seed_id=seed_id)
        return result

    except Exception as exc:
        return SeedRunResult(
            seed_id=seed_id,
            ok=False,
            errors=[f"{type(exc).__name__}: {exc}"],
        )
