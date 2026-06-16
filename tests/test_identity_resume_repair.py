"""Identity / resume-checkpoint / repair determinism regression tests.

These pin the fixes for the state/resume/repair bug observed after running
extra model profiles on an already-complete catalog:

* a model response missing market/make/model is patched from the group and can
  still become website-ready;
* a missing identity can never produce the corrupt key ``IL||`` or the corrupt
  profile id ``IL::::``;
* a stale ``IL::::`` checkpoint is ignored (never silently resumes from the
  beginning), and ``select_groups`` raises on a missing ``start_after_key``;
* repair patches a source_indexes-only block deterministically and promotes it;
* repair never mutates the main build resume pointer;
* a corrupt RS5-like ghost (no identity) is quarantined: it neither inflates
  total_models nor overwrites the real clean RS5;
* an Audi RS4 profile with enforced identity is retained/promoted to clean.
"""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

import scripts.catalog_builder as cb
import scripts.catalog_repair as repair
from scripts.catalog_builder import (
    _model_key,
    _profile_id_to_group_key,
    is_corrupt_key,
    merge_and_write_outputs,
)
from scripts.catalog_grouping import group_variants, select_groups
from scripts.catalog_provider import CatalogProviderSettings
from scripts.catalog_validation import is_valid_profile_id, validate_profile
from scripts.openai_catalog_client import CatalogClient, CatalogClientSettings


# ---------------------------------------------------------------------------
# Helpers (mirrors the grounded-profile builders used elsewhere)
# ---------------------------------------------------------------------------


def _grounded_field_sources(refs):
    return {
        "version_or_trim": [],
        "body_type": list(refs),
        "fuel_type": list(refs),
        "engine": list(refs),
        "engine_displacement_l": list(refs),
        "horsepower_hp": list(refs),
        "transmission": list(refs),
        "drivetrain": list(refs),
        "year_start": list(refs),
        "year_end": list(refs),
    }


def _grounded_variant(*, source_indexes=(0,), refs=(0,), **over):
    variant = {
        "version_or_trim": None,
        "body_type": "Estate",
        "fuel_type": "petrol",
        "engine": "2.9L v6 twin-turbo",
        "engine_displacement_l": 2.9,
        "horsepower_hp": 450,
        "transmission": "8-speed automatic",
        "drivetrain": "AWD",
        "year_start": 2020,
        "year_end": 2024,
        "support_level": "direct",
        "source_indexes": list(source_indexes),
        "field_sources": _grounded_field_sources(refs),
        "missing_grounded_fields": [],
    }
    variant.update(over)
    return variant


def _profile(make="Audi", model="RS4", market="IL", **over):
    profile = {
        "market": market,
        "make": make,
        "model": model,
        "canonical_model": model,
        "profile_confidence": "medium",
        "sources": [
            {
                "source_index": 0,
                "title": f"{make} {model} IL spec",
                "url": "https://example.co.il/spec",
                "source_name": "Cartube Israel",
                "source_type": "catalog",
                "supports": ["engine", "horsepower_hp", "transmission"],
            }
        ],
        "technical_variants_il": [_grounded_variant()],
    }
    profile.update(over)
    return profile


def _variant_row(make, model, **std):
    base = {"make": make, "model": model, "market_scope": "IL",
            "year_start": 2015, "year_end": 2020}
    base.update(std)
    return {"validation_id": f"VAL-{make}-{model}", "source_index": 0, "standard_variant": base}


# ---------------------------------------------------------------------------
# 1. model response missing identity is patched from the group and is ready
# ---------------------------------------------------------------------------


def test_model_response_missing_identity_patched_from_group(monkeypatch, tmp_path):
    """A model that drops market/make/model is repaired from the group payload."""

    def fake_build_profile(self, payload):
        self.calls += 1
        prof = _profile(make=payload["make"], model=payload["model"])
        # The model "forgot" the top-level identity.
        prof.pop("market", None)
        prof.pop("make", None)
        prof.pop("model", None)
        prof.pop("canonical_model", None)
        prof.pop("profile_confidence", None)
        return prof

    monkeypatch.setattr(CatalogClient, "build_profile", fake_build_profile)

    result = cb.build_catalog(
        make="Audi", model="RS4", limit_models=1,
        settings=CatalogClientSettings(api_key="sk-test"),
        catalog_path=str(tmp_path / "c.json"),
        readiness_path=str(tmp_path / "r.json"),
        review_path=str(tmp_path / "v.json"),
    )
    models = result.catalog["models"]
    assert len(models) == 1
    m = models[0]
    assert m["market"] == "IL"
    assert m["make"] == "Audi"
    assert m["model"] == "RS4"
    assert m["canonical_model"] == "RS4"
    assert m["profile_confidence"] == "medium"
    assert result.readiness["models_ready_for_website"] == 1


# ---------------------------------------------------------------------------
# 2. missing identity never produces IL|| or IL:::: ; validation blocks it
# ---------------------------------------------------------------------------


def test_missing_identity_never_creates_il_pipe_key():
    corrupt = {"market": "IL", "make": "", "model": "",
               "technical_variants_il": []}
    key = _model_key(corrupt)
    assert key != "IL||"
    assert is_corrupt_key(key)
    assert key.startswith("__CORRUPT__::")


def test_model_key_recovers_from_request_payload():
    entry = {"request_payload": {"market": "IL", "make": "Audi", "model": "RS5"},
             "technical_variants_il": []}
    assert _model_key(entry) == "IL|Audi|RS5"


def test_validate_profile_blocks_missing_make_model():
    prof = _profile()
    prof.pop("make")
    prof.pop("model")
    res = validate_profile(prof)
    assert res.ready is False
    assert any("make" in i for i in res.issues)
    assert any("model" in i for i in res.issues)


# ---------------------------------------------------------------------------
# 3. "IL::::" checkpoint is ignored, never resumes from the beginning
# ---------------------------------------------------------------------------


def test_corrupt_checkpoint_id_is_invalid():
    assert is_valid_profile_id("IL::::") is False
    assert _profile_id_to_group_key("IL::::") is None
    assert is_valid_profile_id("IL::Audi::RS5") is True
    assert _profile_id_to_group_key("IL::Audi::RS5") == "IL|Audi|RS5"


def test_resume_state_ignores_corrupt_checkpoint_and_continues_after_last_real(tmp_path):
    variants = [
        _variant_row("Abarth", "500"),
        _variant_row("Audi", "RS4"),
        _variant_row("Audi", "RS5"),
        _variant_row("BMW", "X5"),
    ]
    variants_path = tmp_path / "variants.json"
    variants_path.write_text(json.dumps({"variants": variants}), encoding="utf-8")

    catalog_path = tmp_path / "c.json"
    readiness_path = tmp_path / "r.json"
    review_path = tmp_path / "v.json"
    # Clean catalog already has the first three models; checkpoint is corrupt.
    catalog_path.write_text(json.dumps({"models": [
        {"market": "IL", "make": "Abarth", "model": "500"},
        {"market": "IL", "make": "Audi", "model": "RS4"},
        {"market": "IL", "make": "Audi", "model": "RS5"},
    ]}), encoding="utf-8")
    readiness_path.write_text(json.dumps({"last_checkpointed_profile_id": "IL::::"}), encoding="utf-8")
    review_path.write_text(json.dumps({"models": []}), encoding="utf-8")

    state = cb.compute_resume_state(
        variants_path=str(variants_path),
        instructions_path=str(tmp_path / "missing.json"),
        catalog_path=str(catalog_path),
        readiness_path=str(readiness_path),
        review_path=str(review_path),
    )
    # Must NOT restart from the beginning: the next model is the one AFTER the
    # last real clean model (RS5) in source order -> BMW X5.
    assert state["resume_after_key"] == "IL|Audi|RS5"
    assert state["next_key"] == "IL|BMW|X5"
    assert state["next_make"] == "BMW"
    assert state["next_model"] == "X5"


def test_select_groups_missing_start_after_raises():
    variants = [_variant_row("Abarth", "500"), _variant_row("BMW", "X5")]
    groups = group_variants(variants)
    with pytest.raises(ValueError):
        select_groups(groups, start_after_key="IL|Ghost|Nope")
    # explicit override does not raise
    out = select_groups(groups, start_after_key="IL|Ghost|Nope", allow_missing_start_after=True)
    assert len(out) == 2


# ---------------------------------------------------------------------------
# 4. repair: source_indexes missing but field_sources valid -> patch + promote
# ---------------------------------------------------------------------------


def _write_outputs(tmp_path, review_models, catalog_models=None):
    catalog_path = tmp_path / "catalog.json"
    readiness_path = tmp_path / "readiness.json"
    review_path = tmp_path / "review.json"
    catalog_path.write_text(json.dumps({"models": catalog_models or []}), encoding="utf-8")
    readiness_path.write_text("{}", encoding="utf-8")
    review_path.write_text(json.dumps({"models": review_models}), encoding="utf-8")
    return str(catalog_path), str(readiness_path), str(review_path)


def _bypass_provider(monkeypatch, client=None):
    monkeypatch.setattr(repair, "check_provider_available", lambda _s: None)
    monkeypatch.setattr(repair, "build_catalog_client", lambda _s: client or object())


def test_repair_patches_source_indexes_and_promotes(monkeypatch, tmp_path):
    """field_sources valid but variant source_indexes missing -> deterministic
    patch (no model call) then promote to clean."""
    blocked = _profile()
    # Remove the variant-level source_indexes (the only blocker).
    blocked["technical_variants_il"][0].pop("source_indexes")
    blocked["validation_issues"] = ["variant[0] has no source_indexes"]
    blocked["repair_attempts"] = 0

    catalog_path, readiness_path, review_path = _write_outputs(tmp_path, [blocked])

    class _NoCallClient:
        def build_repair_profile(self, *a, **k):  # pragma: no cover - must not run
            raise AssertionError("model must not be called for source_indexes-only repair")

    _bypass_provider(monkeypatch, client=_NoCallClient())

    result = repair.repair_review_models(
        selected_keys=["IL|Audi|RS4"],
        provider_settings=CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test"),
        catalog_path=catalog_path,
        readiness_path=readiness_path,
        review_path=review_path,
    )
    assert result["promoted"] == 1
    catalog = json.loads(open(catalog_path, encoding="utf-8").read())
    names = {m["model"] for m in catalog["models"]}
    assert "RS4" in names
    promoted = next(m for m in catalog["models"] if m["model"] == "RS4")
    assert promoted["technical_variants_il"][0]["source_indexes"] == [0]
    # review-only bookkeeping must not leak into clean
    assert "validation_issues" not in promoted
    assert "repair_attempts" not in promoted


# ---------------------------------------------------------------------------
# 5. repair does not mutate the main build resume pointer
# ---------------------------------------------------------------------------


def test_repair_does_not_move_build_checkpoint(monkeypatch, tmp_path):
    blocked = _profile(make="Audi", model="RS4")
    blocked["technical_variants_il"][0].pop("source_indexes")
    blocked["repair_attempts"] = 0
    catalog_path, readiness_path, review_path = _write_outputs(tmp_path, [blocked])
    # Seed a valid build resume pointer pointing elsewhere.
    json.dump({"last_checkpointed_profile_id": "IL::BMW::X5"},
              open(readiness_path, "w", encoding="utf-8"))

    _bypass_provider(monkeypatch)

    repair.repair_review_models(
        selected_keys=["IL|Audi|RS4"],
        provider_settings=CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test"),
        catalog_path=catalog_path,
        readiness_path=readiness_path,
        review_path=review_path,
    )
    readiness = json.loads(open(readiness_path, encoding="utf-8").read())
    # The build pointer must be untouched; the repair pointer tracks the repair.
    assert readiness["last_checkpointed_profile_id"] == "IL::BMW::X5"
    assert readiness["last_repair_checkpointed_profile_id"] == "IL::Audi::RS4"


# ---------------------------------------------------------------------------
# 6. corrupt RS5-like ghost: no count inflation, no overwrite of clean RS5
# ---------------------------------------------------------------------------


def test_corrupt_ghost_does_not_count_or_overwrite_clean(monkeypatch, tmp_path):
    clean_rs5 = _profile(make="Audi", model="RS5")
    clean_rs5["notes"] = ["real clean rs5"]
    ghost = {  # no market/make/model, RS5-like sources, no source_indexes
        "sources": clean_rs5["sources"],
        "technical_variants_il": [
            {k: v for k, v in _grounded_variant().items() if k != "source_indexes"}
        ],
        "validation_issues": ["variant[0] has no source_indexes"],
        "repair_attempts": 2,
        "repair_exhausted": True,
    }
    catalog_path = tmp_path / "c.json"
    readiness_path = tmp_path / "r.json"
    review_path = tmp_path / "v.json"
    catalog_path.write_text(json.dumps({"models": [clean_rs5]}), encoding="utf-8")
    readiness_path.write_text("{}", encoding="utf-8")
    review_path.write_text(json.dumps({"models": [ghost]}), encoding="utf-8")

    catalog, readiness, review = merge_and_write_outputs(
        [], [],
        settings=CatalogClientSettings(api_key="sk-test"),
        catalog_path=str(catalog_path),
        readiness_path=str(readiness_path),
        review_path=str(review_path),
    )
    # Ghost is quarantined out of review entirely.
    assert review["models"] == []
    # Clean RS5 preserved and not overwritten by the ghost.
    rs5 = [m for m in catalog["models"] if m.get("model") == "RS5"]
    assert len(rs5) == 1
    assert rs5[0].get("notes") == ["real clean rs5"]
    # total_models counts only the real clean model.
    assert readiness["total_models"] == 1


# ---------------------------------------------------------------------------
# 7. Audi RS4 with enforced identity is retained / website-ready
# ---------------------------------------------------------------------------


def test_rs4_with_enforced_identity_is_ready():
    res = validate_profile(_profile(make="Audi", model="RS4"))
    assert res.ready is True
    assert not res.issues


def test_resume_source_cursor_uses_clean_and_review_not_stale_checkpoint(tmp_path):
    variants = [
        _variant_row("Audi", "RS6"),
        _variant_row("Audi", "RS7"),
        _variant_row("Audi", "S3"),
        _variant_row("Audi", "S4"),
        _variant_row("Audi", "S5"),
        _variant_row("Audi", "SQ5"),
    ]
    variants_path = tmp_path / "variants.json"
    variants_path.write_text(json.dumps({"variants": variants}), encoding="utf-8")
    catalog_path = tmp_path / "catalog.json"
    review_path = tmp_path / "review.json"
    readiness_path = tmp_path / "readiness.json"
    catalog_path.write_text(json.dumps({"models": [
        {"market": "IL", "make": "Audi", "model": "RS7"},
        {"market": "IL", "make": "Audi", "model": "S3"},
        {"market": "IL", "make": "Audi", "model": "S5"},
    ]}), encoding="utf-8")
    review_path.write_text(json.dumps({"models": [
        {"market": "IL", "make": "Audi", "model": "RS6", "technical_variants_il": []},
        {"market": "IL", "make": "Audi", "model": "S4", "technical_variants_il": []},
    ]}), encoding="utf-8")
    readiness_path.write_text(json.dumps({"last_checkpointed_profile_id": "IL::Audi::S3"}), encoding="utf-8")

    state = cb.compute_resume_state(
        variants_path=str(variants_path),
        instructions_path=str(tmp_path / "missing.json"),
        catalog_path=str(catalog_path),
        readiness_path=str(readiness_path),
        review_path=str(review_path),
    )
    assert state["done_source_cursor"] == 5
    assert state["resume_after_key"] == "IL|Audi|S5"
    assert state["next_key"] == "IL|Audi|SQ5"
    assert state["next_key_to_process"] == "IL|Audi|SQ5"
    assert state["next_make"] == "Audi"
    assert state["next_model"] == "SQ5"
    assert state["ready"] == 3
    assert state["blocked"] == 2


def test_build_error_profile_is_normalized(monkeypatch, tmp_path):
    class _FailClient:
        def build_profile(self, payload):
            raise ValueError("Gemini catalog client returned non-object JSON")

    monkeypatch.setattr(cb, "check_provider_available", lambda _s: None)
    monkeypatch.setattr(cb, "build_catalog_client", lambda _s: _FailClient())
    result = cb.build_catalog(
        make="Audi", model="RS4", limit_models=1,
        provider_settings=CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test"),
        catalog_path=str(tmp_path / "c.json"),
        readiness_path=str(tmp_path / "r.json"),
        review_path=str(tmp_path / "v.json"),
    )
    entry = result.review["models"][0]
    assert entry["market"] == "IL"
    assert entry["make"] == "Audi"
    assert entry["model"] == "RS4"
    assert entry["canonical_model"] == "RS4"
    assert entry["technical_variants_il"] == []
    assert entry["validation_issues"]
    assert entry["request_payload"]["model"] == "RS4"
    assert entry["rebuild_required"] is True


def test_full_rebuild_repair_calls_build_profile_not_targeted(monkeypatch, tmp_path):
    blocked = {"market": "IL", "make": "Audi", "model": "RS6", "canonical_model": "RS6", "technical_variants_il": [],
               "error": "Extra data: line 407 column 1", "rebuild_required": True,
               "request_payload": {"market": "IL", "make": "Audi", "model": "RS6", "variants": []},
               "validation_issues": ["technical_variants_il is empty"], "repair_attempts": 0}
    catalog_path, readiness_path, review_path = _write_outputs(tmp_path, [blocked])
    calls = {"build": 0, "repair": 0}

    class _Client:
        def build_profile(self, payload):
            calls["build"] += 1
            return _profile(make=payload["make"], model=payload["model"])
        def build_repair_profile(self, *a, **k):
            calls["repair"] += 1
            raise AssertionError("targeted repair must not be called")

    _bypass_provider(monkeypatch, _Client())
    result = repair.repair_review_models(
        selected_keys=["IL|Audi|RS6"],
        provider_settings=CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test"),
        catalog_path=catalog_path, readiness_path=readiness_path, review_path=review_path,
    )
    assert calls == {"build": 1, "repair": 0}
    assert result["promoted"] == 1


def test_noop_deterministic_repair_does_not_increment_attempts(monkeypatch, tmp_path):
    blocked = _profile()
    blocked["technical_variants_il"][0]["source_indexes"] = [999]
    blocked["technical_variants_il"][0]["field_sources"] = _grounded_field_sources([999])
    blocked["validation_issues"] = ["source index 999 does not exist"]
    blocked["repair_attempts"] = 1
    catalog_path, readiness_path, review_path = _write_outputs(tmp_path, [blocked])
    monkeypatch.setattr(repair, "derive_repair_targets", lambda _p: {})
    _bypass_provider(monkeypatch, object())
    result = repair.repair_review_models(
        selected_keys=["IL|Audi|RS4"],
        provider_settings=CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test"),
        catalog_path=catalog_path, readiness_path=readiness_path, review_path=review_path,
    )
    entry = result["review"]["models"][0]
    assert entry["repair_attempts"] == 1
    assert entry["rebuild_required"] is True
    assert "full rebuild required" in entry["last_repair_error"]


def test_truthful_repair_logs(monkeypatch, tmp_path):
    full = {"market": "IL", "make": "Audi", "model": "RS6", "canonical_model": "RS6", "technical_variants_il": [],
            "rebuild_required": True, "request_payload": {"market": "IL", "make": "Audi", "model": "RS6", "variants": []}}
    targeted = _profile(make="Audi", model="RS4")
    targeted["technical_variants_il"][0]["horsepower_hp"] = None
    deterministic = _profile(make="Audi", model="S4")
    deterministic["technical_variants_il"][0].pop("source_indexes")
    catalog_path, readiness_path, review_path = _write_outputs(tmp_path, [full, targeted, deterministic])

    class _Client:
        def build_profile(self, payload):
            return _profile(make=payload["make"], model=payload["model"])
        def build_repair_profile(self, make, model, profile, targets):
            fixed = _profile(make=make, model=model)
            fixed["technical_variants_il"][0]["horsepower_hp"] = 450
            return fixed

    _bypass_provider(monkeypatch, _Client())
    logs = []
    repair.repair_review_models(
        selected_keys=["IL|Audi|RS6", "IL|Audi|RS4", "IL|Audi|S4"],
        provider_settings=CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test"),
        catalog_path=catalog_path, readiness_path=readiness_path, review_path=review_path,
        log=logs.append,
    )
    joined = "\n".join(logs)
    assert "REBUILDING WITH GPT-5.4: IL|Audi|RS6 | full rebuild from request_payload" in joined
    assert "REPAIRING WITH GPT-5.4: IL|Audi|RS4 | targets=" in joined
    assert "DETERMINISTIC PATCH ONLY: IL|Audi|S4 | no model call" in joined


def test_resume_state_review_overlap_is_not_active_blocked(tmp_path):
    variants = [_variant_row("Audi", "TT"), _variant_row("BMW", "735i")]
    variants_path = tmp_path / "variants.json"
    variants_path.write_text(json.dumps({"variants": variants}), encoding="utf-8")
    catalog_path = tmp_path / "catalog.json"
    review_path = tmp_path / "review.json"
    readiness_path = tmp_path / "readiness.json"
    catalog_path.write_text(json.dumps({"models": [{"market": "IL", "make": "Audi", "model": "TT"}]}), encoding="utf-8")
    review_path.write_text(json.dumps({"models": [{"market": "IL", "make": "Audi", "model": "TT"}]}), encoding="utf-8")
    readiness_path.write_text(json.dumps({"models_blocked": 0}), encoding="utf-8")

    state = cb.compute_resume_state(
        variants_path=str(variants_path),
        instructions_path=str(tmp_path / "missing.json"),
        catalog_path=str(catalog_path),
        readiness_path=str(readiness_path),
        review_path=str(review_path),
    )

    assert state["clean_count"] == 1
    assert state["review_entries_count"] == 1
    assert state["review_overlap_count"] == 1
    assert state["review_only_blocked_count"] == 0
    assert state["active_blocked_count"] == 0
    assert state["blocked"] == 0
    assert state["resume_after_key"] == "IL|Audi|TT"
    assert state["next_key_to_process"] == "IL|BMW|735i"
    assert state["next_key"] == "IL|BMW|735i"


def test_resume_state_review_only_counts_blocked_without_readiness_override(tmp_path):
    variants = [_variant_row("Audi", "TT"), _variant_row("BMW", "735i")]
    variants_path = tmp_path / "variants.json"
    variants_path.write_text(json.dumps({"variants": variants}), encoding="utf-8")
    catalog_path = tmp_path / "catalog.json"
    review_path = tmp_path / "review.json"
    readiness_path = tmp_path / "readiness.json"
    catalog_path.write_text(json.dumps({"models": []}), encoding="utf-8")
    review_path.write_text(json.dumps({"models": [{"market": "IL", "make": "Audi", "model": "TT"}]}), encoding="utf-8")
    readiness_path.write_text(json.dumps({}), encoding="utf-8")

    state = cb.compute_resume_state(
        variants_path=str(variants_path),
        instructions_path=str(tmp_path / "missing.json"),
        catalog_path=str(catalog_path),
        readiness_path=str(readiness_path),
        review_path=str(review_path),
    )

    assert state["review_only_blocked_count"] == 1
    assert state["active_blocked_count"] == 1
    assert state["blocked"] == 1
    assert state["next_key_to_process"] == "IL|BMW|735i"


def test_resume_state_readiness_models_blocked_overrides_review_only_count(tmp_path):
    variants = [_variant_row("Audi", "TT"), _variant_row("BMW", "735i")]
    variants_path = tmp_path / "variants.json"
    variants_path.write_text(json.dumps({"variants": variants}), encoding="utf-8")
    catalog_path = tmp_path / "catalog.json"
    review_path = tmp_path / "review.json"
    readiness_path = tmp_path / "readiness.json"
    catalog_path.write_text(json.dumps({"models": []}), encoding="utf-8")
    review_path.write_text(json.dumps({"models": [{"market": "IL", "make": "Audi", "model": "TT"}]}), encoding="utf-8")
    readiness_path.write_text(json.dumps({"models_blocked": 3}), encoding="utf-8")

    state = cb.compute_resume_state(
        variants_path=str(variants_path),
        instructions_path=str(tmp_path / "missing.json"),
        catalog_path=str(catalog_path),
        readiness_path=str(readiness_path),
        review_path=str(review_path),
    )

    assert state["review_only_blocked_count"] == 1
    assert state["active_blocked_count"] == 3
    assert state["blocked"] == 3


def test_current_catalog_resume_state_advances_past_repaired_bmw_blockers():
    state = cb.compute_resume_state()

    assert state["clean_count"] == 161
    assert state["review_entries_count"] == 0
    assert state["review_overlap_count"] == 0
    assert state["review_only_blocked_count"] == 0
    assert state["active_blocked_count"] == 0
    assert state["blocked"] == 0
    assert state["resume_after_key"] == "IL|BMW|X3 xDrive30e"
    assert state["next_key_to_process"] == "IL|BMW|X3 xDrive30i"
    assert state["next_key"] == "IL|BMW|X3 xDrive30i"
    assert state["next_make"] == "BMW"
    assert state["next_model"] == "X3 xDrive30i"
    assert state["unmatched_output_keys_count"] == 2
    assert state["unmatched_output_keys_sample"] == [
        "IL|Alfa Romeo|Junior Elettrica",
        "IL|BMW|M850i",
    ]
