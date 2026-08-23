"""Streamlit/engine repair-adjudicator wiring regression tests (brief 5.1/5.2)."""

from scripts.streamlit_wiring import build_run_config_and_adjudicators
from scripts.validator_engine import RunConfig, run_validation
from scripts.data_loader import JoinResult
from scripts.output_writer import OutputStore


def _wire(**over):
    kwargs = dict(
        mode="real", limit=5, force_reprocess=True, start_after="", checkpoint_every=1,
        stop_on_github_failure=False, stop_on_error=False, force_per_variant_validation=True,
        repair_adjudicator_enabled=True, repair_adjudicator_model_id="gpt-5.4",
        repair_adjudicator_mode="all_clean_candidates", require_gpt54_grounding_for_repair=True,
        require_gemini_grounding=True, final_seal_enabled=True, strict_clean_catalog=True,
        legacy_guard_verifier_enabled=False, legacy_guard_verifier_model_id="gpt-5.4",
        openai_api_key="sk-test",
    )
    kwargs.update(over)
    return build_run_config_and_adjudicators(**kwargs)


# --------------------------------------------------------------------------
# 5.1 wiring helper
# --------------------------------------------------------------------------


def test_build_helper_creates_repair_adjudicator_when_enabled():
    cfg, guard, repair, err = _wire()
    assert err is None
    assert repair is not None
    assert repair.settings.model_id == "gpt-5.4"
    assert repair.settings.grounding_required is True
    assert cfg.repair_adjudicator_enabled is True


def test_build_helper_repair_enabled_missing_openai_key_fails_visibly():
    cfg, guard, repair, err = _wire(openai_api_key="")
    assert err is not None and "api_key" in err
    assert repair is None


def test_legacy_guard_verifier_is_separate_and_default_false():
    cfg, guard, repair, err = _wire()
    # Default config keeps the legacy verifier off and repair on.
    assert cfg.guard_verifier_enabled is False
    assert guard is None
    assert RunConfig().repair_adjudicator_enabled is True
    assert RunConfig().guard_verifier_enabled is False


def test_legacy_guard_verifier_created_only_when_explicitly_enabled():
    cfg, guard, repair, err = _wire(legacy_guard_verifier_enabled=True)
    assert err is None
    assert guard is not None
    assert repair is not None  # repair stays the primary path


# --------------------------------------------------------------------------
# 5.2 engine behaviour
# --------------------------------------------------------------------------


class _FakeGemini:
    def __init__(self, raw):
        self._raw = raw

    def validate(self, payload, instruction, evidence):
        return dict(self._raw)


def _join_one():
    std = {
        "make": "Abarth", "model": "500", "engine": "1.4L Turbo", "transmission": "manual",
        "fuel_type": "petrol", "drivetrain": "FWD", "body_type": "Hatchback",
        "year_start": 2010, "year_end": 2016, "generation": "1st Gen", "trim": "Base",
        "official_marketed_name_il": None, "market_scope": "IL",
    }
    variant = {"validation_id": "VAL-000001", "standard_variant": dict(std)}
    return JoinResult(variants=[variant], instructions={"VAL-000001": {}}, ordered_ids=["VAL-000001"])


def _store(tmp_path):
    return OutputStore(output_path=str(tmp_path / "o.json"), checkpoint_path=str(tmp_path / "c.json"), run_mode="real")


def test_run_validation_fails_closed_when_repair_enabled_but_missing(tmp_path):
    cfg = RunConfig(mode="real", repair_adjudicator_enabled=True, limit=1)
    result = run_validation(_join_one(), cfg, store=_store(tmp_path), gemini_client=_FakeGemini({}), repair_adjudicator=None)
    assert result.stopped_reason == "repair_adjudicator_not_wired"
    assert result.store.metadata.get("repair_setup_failed") is True
    assert result.processed == 0


def test_new_real_rows_always_have_final_seal_result(tmp_path):
    raw = {
        "validation_decision": "clean_partial", "identity_status": "likely_valid",
        "canonical_trim": None, "trim_status": "unresolved",
        "grounding_summary": "Verified Israeli-market identity; trim unresolved.",
        "evidence_sources": [{"title": "t", "url": "https://www.icar.co.il/x", "source_name": "icar.co.il", "source_type": "editorial", "supports": ["market_presence_il"]}],
    }
    cfg = RunConfig(mode="real", repair_adjudicator_enabled=False, limit=1, final_seal_enabled=True)
    store = _store(tmp_path)
    result = run_validation(_join_one(), cfg, store=store, gemini_client=_FakeGemini(raw))
    assert result.processed == 1
    row = store.validated_by_id["VAL-000001"]
    assert row.get("final_seal_result")
    assert row["publishable_to_clean_catalog"] is False
    assert row["final_route"] != "clean_catalog"


def test_repair_triggered_counter_increments_before_adjudicator_check(tmp_path):
    raw = {
        "validation_decision": "clean_partial", "identity_status": "likely_valid",
        "canonical_trim": None, "trim_status": "unresolved",
        "grounding_summary": "Verified identity; trim unresolved.",
        "evidence_sources": [{"title": "t", "url": "https://www.icar.co.il/x", "source_name": "icar.co.il", "source_type": "editorial", "supports": ["market_presence_il"]}],
    }
    cfg = RunConfig(mode="real", repair_adjudicator_enabled=False, limit=1, repair_adjudicator_mode="all_rows")
    store = _store(tmp_path)
    run_validation(_join_one(), cfg, store=store, gemini_client=_FakeGemini(raw))
    # Counted even though no adjudicator object was provided.
    assert store.metadata["stage25_repair_risk_scored_rows"] == 1
    assert store.metadata["stage25_repair_triggered_rows"] == 1
    # No repair calls were made (no adjudicator), but the trigger is visible.
    assert store.metadata["stage3_repair_adjudicator_calls"] == 0
