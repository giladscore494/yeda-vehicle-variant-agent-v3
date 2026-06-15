"""Repair must not stay stuck on provider/setup pollution.

Earlier provider/setup failures (notably the missing google-genai dependency)
consumed repair_attempts and marked models repair_exhausted. After the
dependency was added, repair mode skipped those models forever. These tests
pin the corrected behavior: provider/setup failures never consume a genuine
repair attempt, and previously-polluted entries are retried.
"""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

import scripts.catalog_repair as repair
from scripts.catalog_provider import CatalogProviderSettings
from scripts.openai_catalog_client import CatalogClientSettings


@pytest.mark.parametrize(
    "value",
    [
        {"last_repair_error": "Gemini client library is unavailable"},
        {"last_repair_error": "Add google-genai to requirements.txt"},
        {"error": "No module named 'google.genai'"},
        {"last_repair_error": "OpenAI API key is missing for the selected GPT-5.4 validation model."},
        {"last_repair_error": "cannot import name 'ProviderUnavailableError' from 'scripts.catalog_provider'"},
        ImportError("no google genai"),
        ModuleNotFoundError("No module named 'google'"),
        "Google API key is missing",
    ],
)
def test_is_provider_setup_error_true(value):
    assert repair.is_provider_setup_error(value) is True


@pytest.mark.parametrize(
    "value",
    [
        None,
        {},
        {"last_repair_error": "single model api failure"},
        {"error": "repair altered untargeted variant[0]"},
        RuntimeError("temporary api failure"),
        "validation issues remain",
    ],
)
def test_is_provider_setup_error_false(value):
    assert repair.is_provider_setup_error(value) is False


def _write_outputs(tmp_path, review_models):
    catalog_path = tmp_path / "catalog.json"
    readiness_path = tmp_path / "readiness.json"
    review_path = tmp_path / "review.json"
    catalog_path.write_text('{"models": []}', encoding="utf-8")
    readiness_path.write_text("{}", encoding="utf-8")
    review_path.write_text(json.dumps({"models": review_models}), encoding="utf-8")
    return catalog_path, readiness_path, review_path


def _bypass_provider(monkeypatch, client):
    monkeypatch.setattr(repair, "check_provider_available", lambda settings: None)
    monkeypatch.setattr(repair, "build_catalog_client", lambda settings: client)


def test_polluted_exhausted_entry_is_reset_and_retried(monkeypatch, tmp_path):
    polluted = {
        "market": "IL", "make": "Abarth", "model": "500",
        "technical_variants_il": [],
        "validation_issues": ["blocked"],
        "repair_attempts": repair.MAX_REPAIR_ATTEMPTS,
        "repair_exhausted": True,
        "last_repair_error": "Gemini client library is unavailable; add google-genai",
    }
    catalog_path, readiness_path, review_path = _write_outputs(tmp_path, [polluted])

    # No targets -> the entry is simply re-validated; force it to pass.
    monkeypatch.setattr(
        repair, "validate_profile",
        lambda profile: SimpleNamespace(ready=True, profile=profile, issues=[]),
    )
    _bypass_provider(monkeypatch, client=object())

    logs: list[str] = []
    result = repair.repair_review_models(
        selected_keys=["IL|Abarth|500"],
        provider_settings=CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test"),
        log=logs.append,
        catalog_path=str(catalog_path),
        readiness_path=str(readiness_path),
        review_path=str(review_path),
    )

    assert result["skipped"] == 0
    assert result["processed"] == 1
    assert result["promoted"] == 1
    assert any("RESET provider/setup pollution" in line for line in logs)
    assert not any("SKIP exhausted" in line for line in logs)


def test_provider_setup_failure_during_repair_does_not_consume_attempt(monkeypatch, tmp_path):
    entry = {
        "market": "IL", "make": "Abarth", "model": "500",
        "technical_variants_il": [
            {"body_type": None, "field_sources": {}, "missing_grounded_fields": ["body_type"]}
        ],
        "validation_issues": ["blocked"],
        "repair_attempts": 0,
    }
    catalog_path, readiness_path, review_path = _write_outputs(tmp_path, [entry])

    class GeminiBrokenClient:
        def build_repair_profile(self, *args, **kwargs):
            raise ImportError("No module named 'google.genai'")

    _bypass_provider(monkeypatch, client=GeminiBrokenClient())

    result = repair.repair_review_models(
        selected_keys=["IL|Abarth|500"],
        provider_settings=CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test"),
        catalog_path=str(catalog_path),
        readiness_path=str(readiness_path),
        review_path=str(review_path),
    )

    kept = {m["model"]: m for m in result["review"]["models"]}["500"]
    assert kept["repair_attempts"] == 0
    assert "repair_exhausted" not in kept
    assert "No module named" in kept["last_repair_error"]


def test_genuine_repair_failure_still_consumes_attempt(monkeypatch, tmp_path):
    entry = {
        "market": "IL", "make": "Abarth", "model": "500",
        "technical_variants_il": [
            {"body_type": None, "field_sources": {}, "missing_grounded_fields": ["body_type"]}
        ],
        "validation_issues": ["blocked"],
        "repair_attempts": 0,
    }
    catalog_path, readiness_path, review_path = _write_outputs(tmp_path, [entry])

    class FlakyClient:
        def build_repair_profile(self, *args, **kwargs):
            raise RuntimeError("temporary api failure")

    _bypass_provider(monkeypatch, client=FlakyClient())

    result = repair.repair_review_models(
        selected_keys=["IL|Abarth|500"],
        settings=CatalogClientSettings(api_key="sk-test"),
        provider_settings=CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "sk-test"),
        catalog_path=str(catalog_path),
        readiness_path=str(readiness_path),
        review_path=str(review_path),
    )

    kept = {m["model"]: m for m in result["review"]["models"]}["500"]
    assert kept["repair_attempts"] == 1
    assert "temporary api failure" in kept["last_repair_error"]
