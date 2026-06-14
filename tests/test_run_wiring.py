"""Tests for the shared run-wiring helper.

These prove the production path actually builds and passes a GPT-5.4 Repair
Adjudicator (the previous Streamlit bug never did), keeps the legacy guard
verifier separate and off by default, and fails closed when repair is requested
without an OpenAI key.
"""

import ast
import dataclasses
import inspect
from pathlib import Path

import scripts.run_wiring as run_wiring
from scripts.validator_engine import RunConfig

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


def test_run_wiring_constructs_run_config_without_type_error():
    setup = build_run_config_and_adjudicators(
        mode="real",
        limit=5,
        force_reprocess=True,
        start_after="",
        checkpoint_every=1,
        stop_on_github_failure=False,
        stop_on_error=False,
        openai_api_key="test-key",
        repair_adjudicator_enabled=True,
        legacy_guard_verifier_enabled=False,
        final_seal_enabled=True,
        strict_clean_catalog=True,
        require_gemini_grounding=True,
        require_gpt54_grounding_for_repair=True,
    )
    assert setup.error is None
    assert setup.run_config is not None
    assert setup.repair_adjudicator is not None
    assert setup.guard_verifier is None


def test_run_config_accepts_all_run_wiring_fields():
    kwargs = run_wiring.build_run_config_kwargs(
        mode="real",
        limit=5,
        force_reprocess=True,
        start_after="",
        checkpoint_every=1,
        stop_on_github_failure=False,
        stop_on_error=False,
    )
    fields = set(RunConfig.__dataclass_fields__)
    assert set(kwargs) == set(run_wiring.RUN_CONFIG_WIRING_FIELDS)
    assert set(kwargs) <= fields
    required_without_defaults = {
        name
        for name, field in RunConfig.__dataclass_fields__.items()
        if field.default is field.default_factory is dataclasses.MISSING
    }
    assert required_without_defaults <= set(kwargs)


def test_app_call_matches_build_run_config_signature():
    app_source = Path("app.py").read_text()
    tree = ast.parse(app_source)
    signature = set(inspect.signature(build_run_config_and_adjudicators).parameters)
    calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and getattr(node.func, "id", "") == "build_run_config_and_adjudicators"
    ]
    assert calls
    for call in calls:
        names = {kw.arg for kw in call.keywords if kw.arg is not None}
        assert names <= signature


def test_single_authoritative_run_config():
    repo_defs = []
    for path in Path(".").rglob("*.py"):
        tree = ast.parse(path.read_text(errors="ignore"))
        if any(isinstance(node, ast.ClassDef) and node.name == "RunConfig" for node in ast.walk(tree)):
            repo_defs.append(path)
    assert repo_defs == [Path("scripts/validator_engine.py")]
    assert run_wiring.RunConfig is RunConfig


def test_streamlit_sanity_fields_available():
    app_source = Path("app.py").read_text()
    for field in (
        "repair_adjudicator_enabled",
        "repair_adjudicator_object_created",
        "legacy_guard_verifier_enabled",
        "guard_verifier_object_created",
        "final_seal_enabled",
        "strict_clean_catalog",
    ):
        assert field in app_source
