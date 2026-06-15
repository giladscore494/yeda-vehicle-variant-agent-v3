import builtins
import json

import pytest

import scripts.catalog_builder as cb
import scripts.catalog_repair as repair
from scripts.catalog_checkpoint import CatalogCheckpointConfig
from scripts.catalog_provider import CatalogProviderSettings, ProviderUnavailableError
from scripts.openai_catalog_client import CatalogClientSettings


def _block_google_genai(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "google" and "genai" in (fromlist or ()):  # from google import genai
            raise ImportError("no google genai")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)


def _review_entry():
    return {
        "market": "IL",
        "make": "A",
        "model": "One",
        "technical_variants_il": [],
        "validation_issues": ["blocked"],
        "repair_attempts": 1,
    }


def test_requirements_includes_google_genai():
    assert "google-genai" in {line.strip() for line in open("requirements.txt", encoding="utf-8")}


def test_gemini_missing_library_blocks_repair_before_writes(monkeypatch, tmp_path):
    _block_google_genai(monkeypatch)
    catalog_path = tmp_path / "catalog.json"
    readiness_path = tmp_path / "readiness.json"
    review_path = tmp_path / "review.json"
    catalog_path.write_text('{"models": []}', encoding="utf-8")
    readiness_path.write_text("{}", encoding="utf-8")
    original = {"models": [_review_entry()]}
    review_path.write_text(json.dumps(original), encoding="utf-8")

    settings = CatalogProviderSettings("google", "Gemini 3.1", "gemini-3.1-pro-preview", "key")
    with pytest.raises(ProviderUnavailableError):
        repair.repair_review_models(
            batch=1,
            provider_settings=settings,
            catalog_path=str(catalog_path),
            readiness_path=str(readiness_path),
            review_path=str(review_path),
        )

    assert json.loads(review_path.read_text(encoding="utf-8")) == original


def test_gemini_missing_library_blocks_build_before_review_or_checkpoint(monkeypatch, tmp_path):
    _block_google_genai(monkeypatch)
    calls = []

    class RecordingCheckpointer:
        def __init__(self, *args, **kwargs):
            self.state = {"github_checkpoint_count": 0, "github_checkpoint_fail_count": 0}
        def maybe_checkpoint(self, **kwargs):
            calls.append(kwargs)

    monkeypatch.setattr(cb, "CatalogCheckpointer", RecordingCheckpointer)
    settings = CatalogProviderSettings("google", "Gemini 3.1", "gemini-3.1-pro-preview", "key")
    with pytest.raises(ProviderUnavailableError):
        cb.build_catalog(
            limit_models=1,
            provider_settings=settings,
            catalog_path=str(tmp_path / "catalog.json"),
            readiness_path=str(tmp_path / "readiness.json"),
            review_path=str(tmp_path / "review.json"),
        )

    assert calls == []
    assert not (tmp_path / "review.json").exists()


def test_per_model_build_error_routes_to_review_and_checkpoints(monkeypatch, tmp_path):
    class FailingClient:
        def build_profile(self, payload):
            raise RuntimeError("temporary api failure")

    class RecordingCheckpointer:
        def __init__(self, *args, **kwargs):
            self.state = {"github_checkpoint_count": 0, "github_checkpoint_fail_count": 0, "last_checkpointed_profile_id": None}
            self.calls = []
        def maybe_checkpoint(self, **kwargs):
            self.calls.append(kwargs)
            self.state["github_checkpoint_count"] += 1
            return True

    rec = RecordingCheckpointer()
    monkeypatch.setattr(cb, "build_catalog_client", lambda settings: FailingClient())
    monkeypatch.setattr(cb, "CatalogCheckpointer", lambda *a, **k: rec)

    result = cb.build_catalog(
        make="Abarth",
        model="500",
        limit_models=1,
        settings=CatalogClientSettings(api_key="sk-test"),
        checkpoint=CatalogCheckpointConfig(enabled=False),
        catalog_path=str(tmp_path / "catalog.json"),
        readiness_path=str(tmp_path / "readiness.json"),
        review_path=str(tmp_path / "review.json"),
    )

    assert result.review["models"]
    assert "temporary api failure" in result.review["models"][0]["error"]
    assert rec.calls and rec.calls[0]["force"] is True


def test_repair_per_model_failure_increments_only_failed_model(monkeypatch, tmp_path):
    catalog_path = tmp_path / "catalog.json"
    readiness_path = tmp_path / "readiness.json"
    review_path = tmp_path / "review.json"
    catalog_path.write_text('{"models": []}', encoding="utf-8")
    readiness_path.write_text("{}", encoding="utf-8")
    model_a = {
        "market": "IL", "make": "A", "model": "One", "technical_variants_il": [
            {"body_type": None, "field_sources": {}, "missing_grounded_fields": ["body_type"]}
        ], "validation_issues": ["x"], "repair_attempts": 0,
    }
    model_b = {"market": "IL", "make": "B", "model": "Two", "technical_variants_il": [], "validation_issues": ["y"], "repair_attempts": 0}
    review_path.write_text(json.dumps({"models": [model_a, model_b]}), encoding="utf-8")

    class FailingRepairClient:
        def build_repair_profile(self, *args, **kwargs):
            raise RuntimeError("single model api failure")

    monkeypatch.setattr(repair, "build_catalog_client", lambda settings: FailingRepairClient())
    result = repair.repair_review_models(
        selected_keys=["IL|A|One", "IL|B|Two"],
        settings=CatalogClientSettings(api_key="sk-test"),
        catalog_path=str(catalog_path),
        readiness_path=str(readiness_path),
        review_path=str(review_path),
    )

    by_model = {m["model"]: m for m in result["review"]["models"]}
    assert by_model["One"]["repair_attempts"] == 1
    assert "single model api failure" in by_model["One"]["last_repair_error"]
    assert by_model["Two"].get("last_repair_error") is None


def test_no_fallback_for_selected_provider_failures(monkeypatch):
    _block_google_genai(monkeypatch)
    google = CatalogProviderSettings("google", "Gemini 3.1", "gemini-3.1-pro-preview", "key")
    with pytest.raises(ProviderUnavailableError):
        cb.build_catalog(limit_models=1, provider_settings=google)

    openai_missing_key = CatalogProviderSettings("openai", "GPT-5.4", "gpt-5.4", "")
    with pytest.raises(ProviderUnavailableError):
        repair.repair_review_models(batch=1, provider_settings=openai_missing_key)
