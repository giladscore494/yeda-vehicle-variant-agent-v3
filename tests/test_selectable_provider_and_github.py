import json

import pytest

from app import can_start_provider, provider_settings_for_label
from scripts.catalog_repair import repair_review_models
from scripts.config import SharedConfig
from scripts.github_checkpoint import OUTPUT_JSON_PATHS, github_autosave_enabled, manual_push_outputs


def test_provider_selection_defaults_and_mapping():
    cfg = SharedConfig(openai_api_key="sk", google_api_key="g")
    assert provider_settings_for_label("GPT-5.4", cfg).provider == "openai"
    assert provider_settings_for_label("GPT-5.4", cfg).model_id == "gpt-5.4"
    assert provider_settings_for_label("Gemini 3.1", cfg).provider == "google"
    assert provider_settings_for_label("Gemini 3.1", cfg).model_id == "gemini-3.1-pro-preview"


def test_no_fallback_when_selected_provider_key_missing():
    cfg = SharedConfig(openai_api_key="", google_api_key="google-ok")
    ok, msg = can_start_provider(provider_settings_for_label("GPT-5.4", cfg))
    assert ok is False
    assert "No fallback" in msg
    cfg = SharedConfig(openai_api_key="sk-ok", google_api_key="")
    ok, msg = can_start_provider(provider_settings_for_label("Gemini 3.1", cfg))
    assert ok is False
    assert "No fallback" in msg


def test_manual_push_filters_files_and_secrets(monkeypatch, tmp_path):
    existing = tmp_path / "data" / "model_technical_catalog_il.json"
    existing.parent.mkdir()
    existing.write_text("{}", encoding="utf-8")
    secret = tmp_path / ".streamlit" / "secrets.toml"
    secret.parent.mkdir()
    secret.write_text("token='secret'", encoding="utf-8")
    pushed = []

    class FakeGitHubCheckpoint:
        def __init__(self, config):
            self.config = config
        def save_paths(self, paths, message):
            pushed.extend(paths)
            return [str(p) for p in paths]

    monkeypatch.setattr("scripts.github_checkpoint.GitHubCheckpoint", FakeGitHubCheckpoint)
    result = manual_push_outputs(
        token="ghp_test",
        repo_full_name="owner/repo",
        target_branch="target",
        paths=[str(existing), str(tmp_path / "missing.json"), str(secret)],
    )
    assert result["ok"] is True
    assert pushed == [str(existing)]


def test_autosave_enabled_by_current_github_secrets():
    assert github_autosave_enabled(token="t", repo_full_name="owner/repo", target_branch="target") is True
    assert github_autosave_enabled(token="", repo_full_name="owner/repo", target_branch="target") is False


def test_selected_blocked_repair_filtering(monkeypatch, tmp_path):
    review_path = tmp_path / "review.json"
    catalog_path = tmp_path / "catalog.json"
    readiness_path = tmp_path / "readiness.json"
    catalog_path.write_text('{"models": []}', encoding="utf-8")
    readiness_path.write_text("{}", encoding="utf-8")
    review = {
        "models": [
            {"market": "IL", "make": "A", "model": "One", "technical_variants_il": [], "validation_issues": ["x"]},
            {"market": "IL", "make": "B", "model": "Two", "technical_variants_il": [], "validation_issues": ["y"]},
        ]
    }
    review_path.write_text(json.dumps(review), encoding="utf-8")
    calls = []

    def fake_validate(profile):
        from scripts.catalog_validation import ProfileValidation
        calls.append(profile["model"])
        return ProfileValidation(profile=profile, ready=False, issues=["still blocked"], stats={})

    monkeypatch.setattr("scripts.catalog_repair.validate_profile", fake_validate)
    result = repair_review_models(
        selected_keys=["IL|A|One"],
        settings=__import__("scripts.openai_catalog_client", fromlist=["CatalogClientSettings"]).CatalogClientSettings(api_key="sk"),
        catalog_path=str(catalog_path),
        readiness_path=str(readiness_path),
        review_path=str(review_path),
    )
    assert calls == ["One"]
    assert result["processed"] == 1
    merged = json.loads(review_path.read_text(encoding="utf-8"))
    assert any(m["model"] == "Two" and m["validation_issues"] == ["y"] for m in merged["models"])
