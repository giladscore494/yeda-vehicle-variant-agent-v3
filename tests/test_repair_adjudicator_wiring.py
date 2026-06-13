"""Regression tests for Stage 3 GPT-5.4 repair adjudicator wiring.

These guard the core failure mode from the latest run: the repair adjudicator
was labelled as enabled in the UI but never actually instantiated or passed into
``run_validation`` (the legacy guard verifier ran instead). They also assert the
fail-closed behaviour: an enabled-but-unwired adjudicator must refuse to run so
partial/unsafe rows can never reach clean_catalog.
"""
from __future__ import annotations

import os
import tempfile
from typing import Any, Dict, List

from scripts.data_loader import JoinResult
from scripts.output_writer import OutputStore
from scripts.validator_engine import RunConfig, run_validation


def _make_join() -> JoinResult:
    variant = {
        "validation_id": "VAL-000001",
        "make": "Abarth",
        "model": "500",
        "trim": "Turismo",
        "body_type": "Hatchback",
        "fuel_type": "Petrol",
        "engine": "1.4",
        "transmission": "manual",
        "drivetrain": "FWD",
        "year_start": 2015,
        "year_end": 2018,
        "evidence_sources": [{"title": "icar", "url": "https://www.icar.co.il/x", "source_name": "icar.co.il"}],
    }
    return JoinResult([variant], {"VAL-000001": {}}, ["VAL-000001"])


def _real_store(tmp: str) -> OutputStore:
    return OutputStore(
        os.path.join(tmp, "r.json"),
        os.path.join(tmp, "r.cp.json"),
        run_mode="real",
        engine="gemini",
        summary_path=os.path.join(tmp, "r.sum.json"),
        is_mock_output=False,
    )


class _FakeGemini:
    def validate(self, payload: Dict[str, Any], instruction: Dict[str, Any], evidence: Any) -> Dict[str, Any]:
        return {
            "canonical_make": "Abarth",
            "canonical_model": "500",
            "canonical_trim": "Turismo",
            "transmission": "manual",
            "validation_decision": "clean_exact",
            "identity_status": "verified",
            "trim_status": "verified",
            "identity_confidence": 0.9,
            "trim_confidence": 0.9,
        }


class _FakeRepairAdjudicator:
    """Records that it was actually invoked and returns a full repaired row."""

    def __init__(self) -> None:
        self.calls = 0
        self.settings = type("S", (), {"model_id": "gpt-5.4"})()

    def build_payload(self, **kwargs: Any) -> Dict[str, Any]:
        self._guarded = kwargs.get("guarded_output", {})
        return {"evidence_sources": [{"url": "https://x"}], "external_search_results_for_gpt54": [{"url": "https://x"}]}

    def adjudicate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.calls += 1
        patched = dict(self._guarded)
        return {
            "repair_decision": "patched",
            "patched_variant": patched,
            "field_patches": [{"field": "transmission", "patch_type": "nullification"}],
            "summary_patch": {"changed": True},
            "routing_patch": {"changed": True},
            "grounding_patch": {"changed": False},
            "remaining_uncertainties": [],
            "blocking_issues_after_repair": [],
            "non_blocking_issues_after_repair": [],
            "confidence": 0.5,
        }


def test_real_run_refuses_when_repair_enabled_but_not_wired():
    join = _make_join()
    with tempfile.TemporaryDirectory() as tmp:
        store = _real_store(tmp)
        result = run_validation(
            join,
            RunConfig(mode="real", limit=1, repair_adjudicator_enabled=True),
            store=store,
            gemini_client=_FakeGemini(),
            repair_adjudicator=None,
        )
    assert result.stopped_reason == "repair_adjudicator_not_wired"
    assert result.store.metadata.get("repair_setup_failed") is True


def test_real_run_invokes_repair_adjudicator_and_counts_patches():
    join = _make_join()
    adj = _FakeRepairAdjudicator()
    with tempfile.TemporaryDirectory() as tmp:
        store = _real_store(tmp)
        run_validation(
            join,
            RunConfig(mode="real", limit=1, repair_adjudicator_enabled=True, repair_adjudicator_grounding_required=False),
            store=store,
            gemini_client=_FakeGemini(),
            repair_adjudicator=adj,
        )
    meta = store.metadata
    assert adj.calls >= 1
    assert meta.get("stage3_repair_adjudicator_calls", 0) >= 1
    assert meta.get("stage3_repair_adjudicator_successes", 0) >= 1
    assert meta.get("stage3_repair_adjudicator_patches", 0) >= 1
    assert meta.get("stage3_repair_adjudicator_routing_changes", 0) >= 1
    assert meta.get("stage3_repair_adjudicator_summary_rewrites", 0) >= 1
    assert meta.get("stage25_repair_triggered_rows", 0) >= 1


def test_repair_triggered_but_not_called_blocks_clean_catalog():
    """Repair enabled in config but no adjudicator object: engine refuses to run,
    so no row is ever emitted to clean_catalog."""
    join = _make_join()
    with tempfile.TemporaryDirectory() as tmp:
        store = _real_store(tmp)
        result = run_validation(
            join,
            RunConfig(mode="real", limit=1, repair_adjudicator_enabled=True),
            store=store,
            gemini_client=_FakeGemini(),
            repair_adjudicator=None,
        )
    assert result.processed == 0
    assert all(r.get("final_route") != "clean_catalog" for r in store.validated_by_id.values())
