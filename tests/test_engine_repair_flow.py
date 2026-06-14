"""Engine-level tests for the repair/final-seal flow.

These prove the engine fails closed when repair is enabled without an
adjudicator, that newly processed real rows always carry a final seal, that the
repair adjudicator is actually invoked on risky rows, and that the legacy guard
verifier is never counted as a repair adjudicator.
"""

import os
import tempfile

from scripts.data_loader import JoinResult
from scripts.output_writer import OutputStore
from scripts.validator_engine import RunConfig, run_validation


def _variant(vid, trim):
    return {
        "validation_id": vid,
        "standard_variant": {
            "make": "Abarth", "model": "500", "trim": trim, "engine": "1.4L Turbo",
            "transmission": "manual", "fuel_type": "petrol", "drivetrain": "FWD",
            "body_type": "Hatchback", "year_start": 2010, "year_end": 2016,
            "generation": "1st Gen", "market_scope": "IL",
        },
    }


def _join(*variants):
    ids = [v["validation_id"] for v in variants]
    return JoinResult(
        variants=list(variants),
        instructions={vid: {} for vid in ids},
        ordered_ids=ids,
    )


def _store(tmp):
    return OutputStore(
        output_path=os.path.join(tmp, "out.json"),
        checkpoint_path=os.path.join(tmp, "cp.json"),
        run_mode="real",
    )


class _DummyGemini:
    """Returns a clean_exact-looking row that the guards will find risky."""

    def __init__(self, raw):
        self._raw = raw

    def validate(self, payload, instruction, evidence):
        return dict(self._raw)


class _FakeRepairAdjudicator:
    def __init__(self):
        self.calls = 0
        self.payloads = []

    def build_payload(self, **kwargs):
        self.payloads.append(kwargs)
        return {"guarded_output": kwargs.get("guarded_output", {})}

    def adjudicate(self, payload):
        self.calls += 1
        guarded = dict(payload.get("guarded_output") or {})
        guarded["_repaired"] = True
        return {
            "repair_decision": "patched",
            "patched_variant": guarded,
            "field_patches": [{"field": "canonical_trim", "to": None}],
            "summary_patch": {},
            "routing_patch": {},
            "grounding_patch": {"gpt54_grounding_present": True},
            "remaining_uncertainties": [],
            "confidence": 0.6,
        }


def test_repair_enabled_missing_adjudicator_fails_closed(tmp_path):
    join = _join(_variant("VAL-1", "Turismo"))
    config = RunConfig(mode="real", repair_adjudicator_enabled=True, force_reprocess=True)
    store = _store(str(tmp_path))
    result = run_validation(
        join, config, store=store,
        gemini_client=_DummyGemini({"validation_decision": "clean_exact"}),
        repair_adjudicator=None,
    )
    assert result.stopped_reason == "missing_repair_adjudicator"
    assert result.processed == 0


def test_new_real_rows_always_have_final_seal_result(tmp_path):
    join = _join(_variant("VAL-1", "Turismo"))
    config = RunConfig(mode="real", repair_adjudicator_enabled=False, force_reprocess=True)
    store = _store(str(tmp_path))
    raw = {
        "canonical_make": "Abarth", "canonical_model": "500", "canonical_trim": "Turismo",
        "validation_decision": "clean_exact", "identity_status": "verified",
        "trim_status": "verified", "engine": "1.4L Turbo", "transmission": "manual",
    }
    run_validation(join, config, store=store, gemini_client=_DummyGemini(raw))
    row = store.validated_by_id["VAL-1"]
    assert row.get("final_seal_result") is not None
    assert "grounding_status" in row


def test_repair_adjudicator_called_on_risky_row_and_counted(tmp_path):
    # A combined trim guarantees a high-severity guard flag -> repair triggers.
    join = _join(_variant("VAL-1", "Turismo / Competizione"))
    config = RunConfig(
        mode="real", repair_adjudicator_enabled=True, force_reprocess=True,
        repair_adjudicator_mode="all_clean_candidates",
    )
    store = _store(str(tmp_path))
    raw = {
        "canonical_make": "Abarth", "canonical_model": "500",
        "canonical_trim": "Turismo / Competizione",
        "validation_decision": "clean_exact", "identity_status": "verified",
        "trim_status": "verified",
        "split_candidates": ["Turismo", "Competizione"],
    }
    fake = _FakeRepairAdjudicator()
    run_validation(
        join, config, store=store,
        gemini_client=_DummyGemini(raw), repair_adjudicator=fake,
    )
    assert fake.calls >= 1
    assert store.metadata.get("stage25_repair_triggered_rows", 0) >= 1
    assert store.metadata.get("stage3_repair_adjudicator_calls", 0) >= 1
    row = store.validated_by_id["VAL-1"]
    assert row.get("final_seal_result") is not None
    # Repair-adjudicator counters are independent of the legacy guard verifier.
    assert store.metadata.get("stage3_guard_verifier_calls", 0) == 0


def test_repair_triggered_counter_increments_independent_of_adjudicator(tmp_path):
    # Even with repair disabled, the risk-scoring counter is recorded so the
    # metadata can never silently hide risky rows.
    join = _join(_variant("VAL-1", "Turismo / Competizione"))
    config = RunConfig(mode="real", repair_adjudicator_enabled=False, force_reprocess=True)
    store = _store(str(tmp_path))
    raw = {
        "canonical_make": "Abarth", "canonical_model": "500",
        "canonical_trim": "Turismo / Competizione",
        "validation_decision": "clean_exact", "identity_status": "verified",
        "split_candidates": ["Turismo", "Competizione"],
    }
    run_validation(join, config, store=store, gemini_client=_DummyGemini(raw))
    assert store.metadata.get("stage25_repair_risk_scored_rows", 0) >= 1
    assert store.metadata.get("stage25_repair_triggered_rows", 0) >= 1


class _FakeLegacyGuardVerifier:
    def __init__(self):
        self.calls = 0
        self.settings = type("Settings", (), {"model_id": "gpt-5.4"})()

    def adjudicate(self, row, flags, original_model_output=None):
        self.calls += 1
        updated = dict(row)
        updated["_guard_verifier_success"] = True
        return updated


def test_legacy_guard_verifier_not_counted_as_repair(tmp_path):
    join = _join(_variant("VAL-1", "Turismo / Competizione"))
    config = RunConfig(
        mode="real",
        repair_adjudicator_enabled=False,
        guard_verifier_enabled=True,
        force_reprocess=True,
    )
    store = _store(str(tmp_path))
    raw = {
        "canonical_make": "Abarth", "canonical_model": "500",
        "canonical_trim": "Turismo / Competizione",
        "validation_decision": "clean_exact", "identity_status": "verified",
        "trim_status": "verified",
        "split_candidates": ["Turismo", "Competizione"],
    }
    guard = _FakeLegacyGuardVerifier()
    run_validation(join, config, store=store, gemini_client=_DummyGemini(raw), guard_verifier=guard)
    assert guard.calls >= 1
    assert store.metadata.get("stage3_guard_verifier_calls", 0) >= 1
    assert store.metadata.get("stage3_repair_adjudicator_calls", 0) == 0


def test_repair_adjudicator_success_increments_success_counter(tmp_path):
    # A valid structured repair response must count as a success and count its
    # field patches. The final seal still owns publication routing.
    join = _join(_variant("VAL-1", "Turismo / Competizione"))
    config = RunConfig(
        mode="real", repair_adjudicator_enabled=True, force_reprocess=True,
        repair_adjudicator_mode="all_clean_candidates",
    )
    store = _store(str(tmp_path))
    raw = {
        "canonical_make": "Abarth", "canonical_model": "500",
        "canonical_trim": "Turismo / Competizione",
        "validation_decision": "clean_exact", "identity_status": "verified",
        "trim_status": "verified",
        "split_candidates": ["Turismo", "Competizione"],
    }
    fake = _FakeRepairAdjudicator()
    run_validation(join, config, store=store, gemini_client=_DummyGemini(raw), repair_adjudicator=fake)

    assert store.metadata.get("stage3_repair_adjudicator_calls", 0) > 0
    assert store.metadata.get("stage3_repair_adjudicator_successes", 0) > 0
    assert store.metadata.get("stage3_repair_adjudicator_failures", 0) == 0
    assert store.metadata.get("stage3_repair_adjudicator_patches", 0) > 0


class _FailingRepairAdjudicator(_FakeRepairAdjudicator):
    def adjudicate(self, payload):
        self.calls += 1
        raise RuntimeError("simulated repair failure")


def test_repair_failure_does_not_leave_clean_catalog_unprotected(tmp_path):
    join = _join(_variant("VAL-1", "Turismo / Competizione"))
    config = RunConfig(
        mode="real", repair_adjudicator_enabled=True, force_reprocess=True,
        repair_adjudicator_mode="all_clean_candidates",
    )
    store = _store(str(tmp_path))
    raw = {
        "canonical_make": "Abarth", "canonical_model": "500",
        "canonical_trim": "Turismo / Competizione",
        "validation_decision": "clean_exact", "identity_status": "verified",
        "trim_status": "verified",
        "split_candidates": ["Turismo", "Competizione"],
    }
    run_validation(join, config, store=store, gemini_client=_DummyGemini(raw), repair_adjudicator=_FailingRepairAdjudicator())
    row = store.validated_by_id["VAL-1"]

    assert row.get("final_route") != "clean_catalog"
    assert row.get("publishable_to_clean_catalog") is False
    assert row.get("final_seal_result") is not None
    assert "simulated repair failure" in row.get("_repair_adjudicator_error", "")
