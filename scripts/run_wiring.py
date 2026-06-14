"""Pure wiring helper shared by the Streamlit app and the CLI runner.

The previous Streamlit path mislabelled the legacy guard verifier as the
"GPT-5.4 grounded repair adjudicator" and never instantiated the real
``OpenAIRepairAdjudicator`` nor passed it into ``run_validation``. As a result
no repair layer ever executed and rows were published without repair/final-seal
artifacts.

This module centralises the decision of *which* objects to build so that both
runners stay consistent and the logic is unit-testable without importing
Streamlit. The pipeline contract is:

    Gemini 3.1 grounded collection
    -> Python deterministic quality filter
    -> GPT-5.4 grounded Repair Adjudicator for everything flagged risky
    -> Python Final Seal as the only publication authority

Both models are required to use web grounding; this helper fails closed when a
repair run is requested without an OpenAI key.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from .validator_engine import RunConfig


@dataclass
class AdjudicatorSetup:
    """Result of resolving run config + model adjudicators.

    ``error`` is non-None when the requested configuration is impossible (for
    example repair enabled but no OpenAI key). Callers must surface the error
    and refuse to run rather than silently degrading to a non-repair run.
    """

    run_config: Optional[RunConfig]
    repair_adjudicator: Any = None
    guard_verifier: Any = None
    error: Optional[str] = None


def build_run_config_and_adjudicators(
    *,
    mode: str,
    limit: Optional[int],
    force_reprocess: bool,
    start_after: Optional[str],
    checkpoint_every: int,
    stop_on_github_failure: bool,
    stop_on_error: bool,
    force_per_variant_validation: bool = True,
    openai_api_key: str = "",
    repair_adjudicator_enabled: bool = True,
    repair_adjudicator_model_id: str = "gpt-5.4",
    repair_adjudicator_mode: str = "all_clean_candidates",
    require_gpt54_grounding_for_repair: bool = True,
    require_gemini_grounding: bool = True,
    final_seal_enabled: bool = True,
    strict_clean_catalog: bool = True,
    legacy_guard_verifier_enabled: bool = False,
    guard_verifier_model_id: str = "gpt-5.4",
) -> AdjudicatorSetup:
    """Resolve the RunConfig and the model objects for a run.

    The repair adjudicator and legacy guard verifier are kept strictly
    separate. The legacy verifier is off by default and is never treated as a
    repair layer. Construction of the adjudicator objects does not import the
    ``openai`` SDK (the client is created lazily on first call), so this helper
    is safe to exercise in tests.
    """

    repair_adjudicator = None
    guard_verifier = None

    if mode == "real" and repair_adjudicator_enabled:
        if not openai_api_key:
            return AdjudicatorSetup(
                run_config=None,
                error=(
                    "GPT-5.4 Repair Adjudicator requested but the OpenAI API key "
                    "is missing (st.secrets['openai']['api_key'])."
                ),
            )
        from .openai_repair_adjudicator import (
            OpenAIRepairAdjudicator,
            OpenAIRepairAdjudicatorSettings,
        )

        repair_adjudicator = OpenAIRepairAdjudicator(
            OpenAIRepairAdjudicatorSettings(
                api_key=openai_api_key,
                model_id=repair_adjudicator_model_id,
                enabled=True,
                grounding_required=require_gpt54_grounding_for_repair,
            )
        )

    if mode == "real" and legacy_guard_verifier_enabled:
        if not openai_api_key:
            return AdjudicatorSetup(
                run_config=None,
                error=(
                    "Legacy GPT guard verifier requested but the OpenAI API key "
                    "is missing (st.secrets['openai']['api_key'])."
                ),
            )
        from .openai_guard_verifier import (
            OpenAIGuardVerifier,
            OpenAIGuardVerifierSettings,
        )

        guard_verifier = OpenAIGuardVerifier(
            OpenAIGuardVerifierSettings(
                api_key=openai_api_key,
                model_id=guard_verifier_model_id,
                enabled=True,
            )
        )

    run_config = RunConfig(
        mode=mode,
        limit=int(limit) if limit else None,
        force_reprocess=force_reprocess,
        start_after_validation_id=(start_after or "").strip() or None,
        checkpoint_every=int(checkpoint_every),
        stop_on_github_failure=stop_on_github_failure,
        stop_on_error=stop_on_error,
        flash_adjudication_enabled=False,
        flash_model_id=repair_adjudicator_model_id,
        guard_verifier_enabled=legacy_guard_verifier_enabled,
        repair_adjudicator_enabled=repair_adjudicator_enabled,
        repair_adjudicator_model_id=repair_adjudicator_model_id,
        repair_adjudicator_mode=repair_adjudicator_mode,
        repair_adjudicator_grounding_required=require_gpt54_grounding_for_repair,
        require_gemini_grounding=require_gemini_grounding,
        final_seal_enabled=final_seal_enabled,
        strict_clean_catalog=strict_clean_catalog,
        force_per_variant_validation=force_per_variant_validation,
    )
    return AdjudicatorSetup(
        run_config=run_config,
        repair_adjudicator=repair_adjudicator,
        guard_verifier=guard_verifier,
        error=None,
    )
