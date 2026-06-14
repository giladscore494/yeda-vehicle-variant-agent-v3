"""Tests for the shared run-wiring helper.

These prove the production path actually builds and passes a GPT-5.4 Repair
Adjudicator (the previous Streamlit bug never did), keeps the legacy guard
verifier separate and off by default, and fails closed when repair is requested
without an OpenAI key.
"""

from scripts.run_wiring import build_run_config_and_adjudicators


def _base(**kw):
    args = dict(
        mode="real",
        limit=5,
        force_reprocess=True,
        start_after="",
        checkpoint_every=1,
        stop_on_github_failure=False,
        stop_on_error=False,
        openai_api_key="sk-test",
    )
    args.update(kw)
    return build_run_config_and_adjudicators(**args)


def test_execute_run_creates_repair_adjudicator_when_enabled():
    setup = _base(repair_adjudicator_enabled=True)
    assert setup.error is None
    assert setup.repair_adjudicator is not None
    assert setup.run_config.repair_adjudicator_enabled is True
    # Construction must not require the openai SDK to be importable.
    assert setup.repair_adjudicator.settings.model_id == "gpt-5.4"


def test_repair_enabled_missing_openai_key_fails_visibly():
    setup = _base(repair_adjudicator_enabled=True, openai_api_key="")
    assert setup.run_config is None
    assert setup.error and "OpenAI API key" in setup.error
    assert setup.repair_adjudicator is None


def test_legacy_guard_verifier_is_separate_and_default_false():
    setup = _base()
    # By default only repair is on; the legacy verifier stays off.
    assert setup.guard_verifier is None
    assert setup.run_config.guard_verifier_enabled is False
    assert setup.run_config.repair_adjudicator_enabled is True


def test_legacy_guard_verifier_can_be_enabled_independently():
    setup = _base(legacy_guard_verifier_enabled=True)
    assert setup.guard_verifier is not None
    assert setup.run_config.guard_verifier_enabled is True
    # Repair and legacy verifier are independent objects.
    assert setup.repair_adjudicator is not None
    assert setup.guard_verifier is not setup.repair_adjudicator


def test_mock_mode_never_builds_real_adjudicators():
    setup = _base(mode="mock", openai_api_key="")
    assert setup.error is None
    assert setup.repair_adjudicator is None
    assert setup.guard_verifier is None


def test_grounding_requirements_propagate_to_config_and_object():
    setup = _base(require_gpt54_grounding_for_repair=True, require_gemini_grounding=True)
    assert setup.run_config.repair_adjudicator_grounding_required is True
    assert setup.run_config.require_gemini_grounding is True
    assert setup.repair_adjudicator.settings.grounding_required is True
