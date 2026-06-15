"""Repair mode must checkpoint after every completed blocked model, not only at the end.

Tests A-E correspond directly to the acceptance criteria:
A. repair_review_models writes after each processed blocked model.
B. promoted blocked model lands in the catalog file, not a separate file.
C. maybe_checkpoint called once per completed model with force=True.
D. app.py passes checkpoint=_checkpoint() into repair_review_models.
E. no final-only manual_push_outputs is used for repair autosave.
"""
from __future__ import annotations

import inspect
import json
from types import SimpleNamespace
from typing import Any, Dict, List

import pytest

import scripts.catalog_repair as repair
from scripts.catalog_checkpoint import CatalogCheckpointConfig
from scripts.catalog_provider import CatalogProviderSettings
from scripts.openai_catalog_client import CatalogClientSettings


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _write_outputs(tmp_path, review_models, catalog_models=None):
    catalog_path = tmp_path / "catalog.json"
    readiness_path = tmp_path / "readiness.json"
    review_path = tmp_path / "review.json"
    catalog_payload = {"models": catalog_models or []}
    catalog_path.write_text(json.dumps(catalog_payload), encoding="utf-8")
    readiness_path.write_text("{}", encoding="utf-8")
    review_path.write_text(json.dumps({"models": review_models}), encoding="utf-8")
    return str(catalog_path), str(readiness_path), str(review_path)


def _bypass_provider(monkeypatch, client=None):
    monkeypatch.setattr(repair, "check_provider_available", lambda _s: None)
    monkeypatch.setattr(repair, "build_catalog_client", lambda _s: client or object())


def _ready_validation(profile):
    return SimpleNamespace(ready=True, profile=profile, issues=[])


def _blocked_validation(profile):
    return SimpleNamespace(ready=False, profile=profile, issues=["still blocked"])


# ---------------------------------------------------------------------------
# Test A — write after each processed model, not only at end
# ---------------------------------------------------------------------------

def test_writes_after_each_model_not_only_at_end(monkeypatch, tmp_path):
    """Each model must be persisted immediately after it is processed.

    Strategy: spy on merge_and_write_outputs to capture the catalog state after
    every call. With 3 models, the spy must record 4 calls (3 per-model + 1 final
    refresh). The per-model calls must show incremental progress, proving that
    each model is flushed immediately rather than accumulated until the end.
    """
    entries = [
        {"market": "IL", "make": "A", "model": "One", "technical_variants_il": [], "validation_issues": ["x"]},
        {"market": "IL", "make": "A", "model": "Two", "technical_variants_il": [], "validation_issues": ["x"]},
        {"market": "IL", "make": "A", "model": "Three", "technical_variants_il": [], "validation_issues": ["x"]},
    ]
    catalog_path, readiness_path, review_path = _write_outputs(tmp_path, entries)

    catalog_snapshots: List[set] = []  # catalog model names captured after each write
    real_merge = repair.merge_and_write_outputs

    def spy_merge(new_ready, new_review, *, settings, checkpoint_state,
                  catalog_path=None, readiness_path=None, review_path=None, **kw):
        result = real_merge(
            new_ready, new_review, settings=settings,
            checkpoint_state=checkpoint_state,
            catalog_path=catalog_path,
            readiness_path=readiness_path,
            review_path=review_path,
        )
        catalog_data = json.loads(open(catalog_path, encoding="utf-8").read())
        catalog_snapshots.append({m["model"] for m in catalog_data.get("models", [])})
        return result

    _bypass_provider(monkeypatch)
    monkeypatch.setattr(repair, "merge_and_write_outputs", spy_merge)
    monkeypatch.setattr(repair, "validate_profile", lambda p: _ready_validation(p))

    result = repair.repair_review_models(
        selected_keys=["IL|A|One", "IL|A|Two", "IL|A|Three"],
        provider_settings=CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test"),
        catalog_path=catalog_path,
        readiness_path=readiness_path,
        review_path=review_path,
    )

    assert result["promoted"] == 3

    # 3 per-model writes + 1 final refresh = 4 total calls
    assert len(catalog_snapshots) == 4, (
        f"Expected 4 merge_and_write_outputs calls, got {len(catalog_snapshots)}"
    )

    # After the first model is processed, only One should be in catalog.
    assert "One" in catalog_snapshots[0], "One must be flushed after its own per-model write"
    assert "Two" not in catalog_snapshots[0], "Two must not appear before its own per-model write"
    assert "Three" not in catalog_snapshots[0]

    # After second model: One and Two present.
    assert "One" in catalog_snapshots[1]
    assert "Two" in catalog_snapshots[1]
    assert "Three" not in catalog_snapshots[1]

    # After third model: all three present.
    assert {"One", "Two", "Three"}.issubset(catalog_snapshots[2])

    # Final refresh (4th call) also has all three.
    assert {"One", "Two", "Three"}.issubset(catalog_snapshots[3])

    # All three removed from review (promoted).
    review_data = json.loads(open(review_path, encoding="utf-8").read())
    review_names = {m["model"] for m in review_data.get("models", [])}
    assert not review_names & {"One", "Two", "Three"}, (
        f"Promoted models must be removed from review, found: {review_names}"
    )


# ---------------------------------------------------------------------------
# Test B — promoted model enters catalog file, removed from review file
# ---------------------------------------------------------------------------

def test_promoted_model_enters_catalog_not_separate_file(monkeypatch, tmp_path):
    entries = [
        {"market": "IL", "make": "Toyota", "model": "Camry",
         "technical_variants_il": [], "validation_issues": ["missing field"]},
    ]
    catalog_path, readiness_path, review_path = _write_outputs(tmp_path, entries)

    _bypass_provider(monkeypatch)
    monkeypatch.setattr(repair, "validate_profile", lambda p: _ready_validation(p))

    result = repair.repair_review_models(
        selected_keys=["IL|Toyota|Camry"],
        provider_settings=CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test"),
        catalog_path=catalog_path,
        readiness_path=readiness_path,
        review_path=review_path,
    )

    assert result["promoted"] == 1

    # Must be in the regular catalog file.
    catalog_data = json.loads(open(catalog_path, encoding="utf-8").read())
    catalog_names = {m["model"] for m in catalog_data.get("models", [])}
    assert "Camry" in catalog_names, "Promoted model must be in catalog file"

    # Must be removed from the review file.
    review_data = json.loads(open(review_path, encoding="utf-8").read())
    review_names = {m["model"] for m in review_data.get("models", [])}
    assert "Camry" not in review_names, "Promoted model must be removed from review file"

    # No separate repair output file must exist.
    import os
    for fname in os.listdir(tmp_path):
        assert "repair" not in fname.lower() or fname == "review.json", (
            f"Unexpected repair-specific file created: {fname}"
        )


# ---------------------------------------------------------------------------
# Test C — maybe_checkpoint called once per completed model with force=True
# ---------------------------------------------------------------------------

class _FakeCheckpointer:
    def __init__(self, config, log=None):
        self.config = config
        self.state: Dict[str, Any] = {
            "github_checkpoint_enabled": False,
            "github_checkpoint_unit": "model_profile",
            "github_checkpoint_count": 0,
            "github_checkpoint_fail_count": 0,
            "last_github_checkpoint_error": None,
            "last_checkpointed_profile_id": None,
        }
        self.calls: List[Dict[str, Any]] = []

    def maybe_checkpoint(self, *, profile_id, paths, market, make, model, force=False):
        self.calls.append({"profile_id": profile_id, "paths": paths, "market": market,
                           "make": make, "model": model, "force": force})
        return False


def test_maybe_checkpoint_called_once_per_completed_model(monkeypatch, tmp_path):
    entries = [
        {"market": "IL", "make": "X", "model": "M1", "technical_variants_il": [], "validation_issues": ["v"]},
        {"market": "IL", "make": "X", "model": "M2", "technical_variants_il": [], "validation_issues": ["v"]},
    ]
    catalog_path, readiness_path, review_path = _write_outputs(tmp_path, entries)

    fake_cp = _FakeCheckpointer(CatalogCheckpointConfig())
    monkeypatch.setattr(repair, "CatalogCheckpointer", lambda config, log=None: fake_cp)
    _bypass_provider(monkeypatch)
    monkeypatch.setattr(repair, "validate_profile", lambda p: _blocked_validation(p))

    repair.repair_review_models(
        selected_keys=["IL|X|M1", "IL|X|M2"],
        provider_settings=CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test"),
        catalog_path=catalog_path,
        readiness_path=readiness_path,
        review_path=review_path,
    )

    assert len(fake_cp.calls) == 2, f"Expected 2 checkpoint calls, got {len(fake_cp.calls)}"
    for call in fake_cp.calls:
        assert call["force"] is True, "Repair checkpoints must use force=True"
        assert catalog_path in call["paths"]
        assert readiness_path in call["paths"]
        assert review_path in call["paths"]

    profile_ids = {c["profile_id"] for c in fake_cp.calls}
    assert "IL::X::M1" in profile_ids
    assert "IL::X::M2" in profile_ids


# ---------------------------------------------------------------------------
# Test D — app.py passes checkpoint=_checkpoint() into repair_review_models
# ---------------------------------------------------------------------------

def test_app_repair_passes_checkpoint_arg():
    import app
    src = inspect.getsource(app)
    # The repair call must include checkpoint=_checkpoint()
    assert "checkpoint=_checkpoint()" in src, (
        "app.py must pass checkpoint=_checkpoint() to repair_review_models"
    )


# ---------------------------------------------------------------------------
# Test E — no final-only manual_push_outputs for repair autosave
# ---------------------------------------------------------------------------

def test_app_repair_no_post_completion_manual_push():
    import app
    src = inspect.getsource(app)
    # The old checkbox and post-repair push pattern must be gone.
    assert "push_after_repair" not in src, (
        "push_after_repair checkbox must be removed from app.py"
    )
    # Confirm repair block does not call manual_push_outputs immediately after repair.
    # Locate the repair_clicked block and check no manual_push_outputs follows repair_review_models
    # within that block (the manual push button is a separate independent widget).
    repair_block_start = src.find("if repair_clicked:")
    assert repair_block_start != -1
    # The next top-level if (scan_clicked) marks the end of the repair block.
    scan_block_start = src.find("if scan_clicked:", repair_block_start)
    repair_block = src[repair_block_start:scan_block_start]
    assert "manual_push_outputs" not in repair_block, (
        "manual_push_outputs must not be called inside the repair_clicked block"
    )
