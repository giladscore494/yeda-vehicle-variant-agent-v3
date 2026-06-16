"""Mode-aware repair: full-rebuild classification, one-shot exhausted override,
no-op attempt accounting, and the manual web-grounded RS6 data repair.

No real provider/network calls — providers are bypassed and clients mocked.
"""
from __future__ import annotations

import json

import pytest

import scripts.catalog_repair as repair
from scripts.catalog_repair import requires_full_rebuild
from scripts.catalog_provider import CatalogProviderSettings


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
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


_SETTINGS = CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test")


def _empty_parse_entry(model="RS6", *, request_payload=True, attempts=0, marker="Extra data: line 407 column 1"):
    entry = {
        "market": "IL", "make": "Audi", "model": model, "canonical_model": model,
        "technical_variants_il": [],
        "error": marker,
        "rebuild_required": True,
        "validation_issues": ["technical_variants_il is empty"],
        "repair_attempts": attempts,
    }
    if request_payload:
        entry["request_payload"] = {"market": "IL", "make": "Audi", "model": model, "variants": []}
    return entry


# --------------------------------------------------------------------------- #
# requires_full_rebuild classification
# --------------------------------------------------------------------------- #
def test_requires_full_rebuild_empty_with_parse_marker():
    assert requires_full_rebuild(_empty_parse_entry()) is True


def test_requires_full_rebuild_empty_non_object_json_marker():
    entry = {"technical_variants_il": [],
             "last_repair_error": "Gemini catalog client returned non-object JSON"}
    assert requires_full_rebuild(entry) is True


def test_requires_full_rebuild_rebuild_required_flag():
    assert requires_full_rebuild({"technical_variants_il": [{"x": 1}], "rebuild_required": True}) is True


def test_non_empty_profile_with_field_issues_is_not_full_rebuild():
    """A profile with real variants + field-level grounding issues (the real RS6
    shape) is a targeted/deterministic case, never a full rebuild."""
    entry = _profile(make="Audi", model="RS6")
    entry["validation_issues"] = ["variant[1] non-null field 'fuel_type' has no field_sources entry"]
    assert requires_full_rebuild(entry) is False


def test_empty_without_marker_is_not_full_rebuild():
    assert requires_full_rebuild({"technical_variants_il": [], "validation_issues": ["x"]}) is False


# --------------------------------------------------------------------------- #
# 1 + 6 + 7. exhausted empty parse profile, one-shot full rebuild override
# --------------------------------------------------------------------------- #
def test_exhausted_empty_parse_automatic_batch_skips(monkeypatch, tmp_path):
    entry = _empty_parse_entry(attempts=repair.MAX_REPAIR_ATTEMPTS)
    cat, rdy, rev = _write_outputs(tmp_path, [entry])

    class _Client:
        def build_profile(self, payload):  # pragma: no cover
            raise AssertionError("automatic batch must not call the model on exhausted")

    _bypass_provider(monkeypatch, _Client())
    logs = []
    result = repair.repair_review_models(
        batch=5, provider_settings=_SETTINGS, log=logs.append,
        catalog_path=cat, readiness_path=rdy, review_path=rev,
    )
    assert result["skipped"] == 1 and result["promoted"] == 0
    assert "SKIP exhausted: IL|Audi|RS6" in "\n".join(logs)


def test_exhausted_empty_parse_manual_override_calls_build_profile(monkeypatch, tmp_path):
    entry = _empty_parse_entry(attempts=repair.MAX_REPAIR_ATTEMPTS)
    cat, rdy, rev = _write_outputs(tmp_path, [entry])
    calls = {"build": 0, "repair": 0}

    class _Client:
        def build_profile(self, payload):
            calls["build"] += 1
            return _profile(make=payload["make"], model=payload["model"])

        def build_repair_profile(self, *a, **k):  # pragma: no cover
            calls["repair"] += 1
            raise AssertionError("full rebuild must not call targeted repair")

    _bypass_provider(monkeypatch, _Client())
    logs = []
    result = repair.repair_review_models(
        selected_keys=["IL|Audi|RS6"], allow_exhausted_full_rebuild_once=True,
        provider_settings=_SETTINGS, log=logs.append,
        catalog_path=cat, readiness_path=rdy, review_path=rev,
    )
    assert calls == {"build": 1, "repair": 0}
    assert result["promoted"] == 1
    joined = "\n".join(logs)
    assert "REBUILDING WITH GPT-5.4: IL|Audi|RS6 | full rebuild from request_payload" in joined
    assert "PROMOTE IL|Audi|RS6 after full rebuild" in joined
    # build pointer untouched; only repair pointer advances
    readiness = json.loads(open(rdy, encoding="utf-8").read())
    assert readiness.get("last_checkpointed_profile_id") in (None,)
    assert readiness.get("last_repair_checkpointed_profile_id") == "IL::Audi::RS6"
    # clean profile carries no repair-only fields
    catalog = json.loads(open(cat, encoding="utf-8").read())
    promoted = next(m for m in catalog["models"] if m["model"] == "RS6")
    for k in ("request_payload", "rebuild_required", "repair_attempts", "error", "validation_issues"):
        assert k not in promoted


def test_full_rebuild_failure_consumes_one_attempt(monkeypatch, tmp_path):
    entry = _empty_parse_entry(attempts=0)
    cat, rdy, rev = _write_outputs(tmp_path, [entry])

    class _Client:
        def build_profile(self, payload):
            # returns an empty/invalid profile -> still not ready
            return {"technical_variants_il": []}

    _bypass_provider(monkeypatch, _Client())
    result = repair.repair_review_models(
        selected_keys=["IL|Audi|RS6"], provider_settings=_SETTINGS,
        catalog_path=cat, readiness_path=rdy, review_path=rev,
    )
    assert result["promoted"] == 0 and result["kept"] == 1
    kept = result["review"]["models"][0]
    assert kept["repair_attempts"] == 1  # one real provider call consumed
    assert kept["validation_issues"]
    assert kept["rebuild_required"] is True
    assert kept["request_payload"]


# --------------------------------------------------------------------------- #
# 2 + 3. empty profile classification / missing request_payload
# --------------------------------------------------------------------------- #
def test_empty_non_object_json_full_rebuild_no_deterministic(monkeypatch, tmp_path):
    entry = _empty_parse_entry(marker="catalog client returned non-object JSON")
    cat, rdy, rev = _write_outputs(tmp_path, [entry])

    class _Client:
        def build_profile(self, payload):
            return _profile(make=payload["make"], model=payload["model"])

        def build_repair_profile(self, *a, **k):  # pragma: no cover
            raise AssertionError("no deterministic/targeted repair for empty parse profile")

    _bypass_provider(monkeypatch, _Client())
    result = repair.repair_review_models(
        selected_keys=["IL|Audi|RS6"], provider_settings=_SETTINGS,
        catalog_path=cat, readiness_path=rdy, review_path=rev,
    )
    assert result["promoted"] == 1


def test_full_rebuild_without_request_payload_blocks_no_model_call(monkeypatch, tmp_path):
    entry = _empty_parse_entry(request_payload=False, attempts=0)
    cat, rdy, rev = _write_outputs(tmp_path, [entry])

    class _Client:
        def build_profile(self, payload):  # pragma: no cover
            raise AssertionError("must not call model without request_payload")

    _bypass_provider(monkeypatch, _Client())
    logs = []
    result = repair.repair_review_models(
        selected_keys=["IL|Audi|RS6"], provider_settings=_SETTINGS, log=logs.append,
        catalog_path=cat, readiness_path=rdy, review_path=rev,
    )
    assert result["promoted"] == 0 and result["kept"] == 1
    kept = result["review"]["models"][0]
    assert kept.get("repair_attempts", 0) == 0  # no attempt consumed
    assert "FULL REBUILD BLOCKED: IL|Audi|RS6 | missing request_payload" in "\n".join(logs)


# --------------------------------------------------------------------------- #
# 8 + 9. non-empty exhausted profile: NOT full rebuild; targeted override
# --------------------------------------------------------------------------- #
def _non_empty_exhausted_entry():
    entry = _profile(make="Audi", model="RS6")
    entry["technical_variants_il"][0]["horsepower_hp"] = None  # forces a target
    entry["technical_variants_il"][0]["field_sources"]["horsepower_hp"] = []
    entry["validation_issues"] = ["variant[0] required website field 'horsepower_hp' is null/empty"]
    entry["repair_attempts"] = repair.MAX_REPAIR_ATTEMPTS
    entry["repair_exhausted"] = True
    return entry


def test_non_empty_exhausted_no_payload_is_targeted_not_full_rebuild(monkeypatch, tmp_path):
    entry = _non_empty_exhausted_entry()
    assert requires_full_rebuild(entry) is False
    cat, rdy, rev = _write_outputs(tmp_path, [entry])

    class _Client:
        def build_profile(self, payload):  # pragma: no cover
            raise AssertionError("non-empty exhausted profile must NOT full rebuild")

        def build_repair_profile(self, make, model, profile, targets):
            fixed = _profile(make=make, model=model)
            fixed["technical_variants_il"][0]["horsepower_hp"] = 450
            return fixed

    _bypass_provider(monkeypatch, _Client())
    logs = []
    result = repair.repair_review_models(
        selected_keys=["IL|Audi|RS6"], allow_exhausted_full_rebuild_once=True,
        provider_settings=_SETTINGS, log=logs.append,
        catalog_path=cat, readiness_path=rdy, review_path=rev,
    )
    # targeted manual override repaired and promoted it
    assert result["promoted"] == 1
    assert "REPAIRING WITH GPT-5.4: IL|Audi|RS6 | targets=" in "\n".join(logs)


def test_non_empty_exhausted_automatic_batch_skips(monkeypatch, tmp_path):
    entry = _non_empty_exhausted_entry()
    cat, rdy, rev = _write_outputs(tmp_path, [entry])
    _bypass_provider(monkeypatch, object())
    logs = []
    result = repair.repair_review_models(
        batch=5, provider_settings=_SETTINGS, log=logs.append,
        catalog_path=cat, readiness_path=rdy, review_path=rev,
    )
    assert result["skipped"] == 1 and result["promoted"] == 0
    assert "SKIP exhausted: IL|Audi|RS6" in "\n".join(logs)


# --------------------------------------------------------------------------- #
# 4. no-op deterministic patch does not consume an attempt
# --------------------------------------------------------------------------- #
def test_noop_deterministic_does_not_increment_attempts(monkeypatch, tmp_path):
    blocked = _profile()
    blocked["technical_variants_il"][0]["source_indexes"] = [999]
    blocked["technical_variants_il"][0]["field_sources"] = _grounded_field_sources([999])
    blocked["validation_issues"] = ["source index 999 does not exist"]
    blocked["repair_attempts"] = 1
    cat, rdy, rev = _write_outputs(tmp_path, [blocked])
    monkeypatch.setattr(repair, "derive_repair_targets", lambda _p: {})
    _bypass_provider(monkeypatch, object())
    logs = []
    result = repair.repair_review_models(
        selected_keys=["IL|Audi|RS4"], provider_settings=_SETTINGS, log=logs.append,
        catalog_path=cat, readiness_path=rdy, review_path=rev,
    )
    entry = result["review"]["models"][0]
    assert entry["repair_attempts"] == 1
    assert entry["rebuild_required"] is True
    assert "full rebuild required" in entry["last_repair_error"]
    assert "NO-OP REPAIR BLOCKED: IL|Audi|RS4 | full rebuild required; no attempt consumed" in "\n".join(logs)
