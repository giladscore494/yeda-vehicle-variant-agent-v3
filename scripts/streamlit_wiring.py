"""Pure (non-Streamlit) wiring helper shared by ``app.py`` and tests.

Keeping this out of ``app.py`` lets the repair/legacy adjudicator wiring be unit
tested without importing the Streamlit module (which renders on import).
"""
from __future__ import annotations

from typing import Any, Optional, Tuple

from .validator_engine import RunConfig


def build_run_config_and_adjudicators(
    *,
    mode: str,
    limit: Any,
    force_reprocess: bool,
    start_after: str,
    checkpoint_every: int,
    stop_on_github_failure: bool,
    stop_on_error: bool,
    force_per_variant_validation: bool,
    repair_adjudicator_enabled: bool,
    repair_adjudicator_model_id: str,
    repair_adjudicator_mode: str,
    require_gpt54_grounding_for_repair: bool,
    require_gemini_grounding: bool,
    final_seal_enabled: bool,
    strict_clean_catalog: bool,
    legacy_guard_verifier_enabled: bool,
    legacy_guard_verifier_model_id: str,
    openai_api_key: str,
) -> Tuple[RunConfig, Optional[Any], Optional[Any], Optional[str]]:
    """Build a ``RunConfig`` plus optional GPT-5.4 repair/legacy objects.

    Returns ``(run_config, guard_verifier, repair_adjudicator, error)`` where
    ``error`` is a user-facing string or ``None``.
    """
    run_config = RunConfig(
        mode=mode,
        limit=int(limit) if limit else None,
        force_reprocess=force_reprocess,
        start_after_validation_id=(start_after or "").strip() or None,
        checkpoint_every=int(checkpoint_every),
        stop_on_github_failure=stop_on_github_failure,
        stop_on_error=stop_on_error,
        flash_adjudication_enabled=False,
        flash_model_id=legacy_guard_verifier_model_id,
        guard_verifier_enabled=legacy_guard_verifier_enabled,
        repair_adjudicator_enabled=repair_adjudicator_enabled,
        repair_adjudicator_model_id=repair_adjudicator_model_id,
        repair_adjudicator_mode=repair_adjudicator_mode,
        repair_adjudicator_grounding_required=require_gpt54_grounding_for_repair,
        final_seal_enabled=final_seal_enabled,
        require_gemini_grounding=require_gemini_grounding,
        strict_clean_catalog=strict_clean_catalog,
        force_per_variant_validation=force_per_variant_validation,
    )

    repair_adjudicator = None
    guard_verifier = None
    if mode == "real" and repair_adjudicator_enabled:
        if not openai_api_key:
            return run_config, None, None, (
                "Repair adjudicator requested but st.secrets['openai']['api_key'] is missing."
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
            return run_config, None, repair_adjudicator, (
                "Legacy guard verifier requested but st.secrets['openai']['api_key'] is missing."
            )
        from .openai_guard_verifier import (
            OpenAIGuardVerifier,
            OpenAIGuardVerifierSettings,
        )

        guard_verifier = OpenAIGuardVerifier(
            OpenAIGuardVerifierSettings(
                api_key=openai_api_key, model_id=legacy_guard_verifier_model_id, enabled=True
            )
        )
    return run_config, guard_verifier, repair_adjudicator, None
