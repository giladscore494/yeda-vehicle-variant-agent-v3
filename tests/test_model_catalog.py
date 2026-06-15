"""Tests for the single-GPT-5.4 Israeli model technical-catalog pipeline."""

from __future__ import annotations

import json
import os

import pytest

from scripts.catalog_grouping import group_variants, select_groups
from scripts.catalog_validation import (
    build_readiness_report,
    derive_available_values,
    validate_profile,
)
from scripts.openai_catalog_client import CatalogClient, classify_non_trim


def _variant(make, model, **std):
    base = {
        "make": make,
        "model": model,
        "market_scope": "IL",
        "year_start": std.pop("year_start", 2015),
        "year_end": std.pop("year_end", 2020),
    }
    base.update(std)
    return {
        "validation_id": std.get("validation_id", f"VAL-{make}-{model}"),
        "source_index": std.get("source_index", 0),
        "standard_variant": base,
    }


def test_group_by_market_make_model():
    variants = [
        _variant("Abarth", "500", trim="Base", engine="1.4L Turbo", transmission="manual",
                 body_type="Hatchback", fuel_type="petrol", drivetrain="FWD",
                 validation_id="VAL-1", source_index=3),
        _variant("Abarth", "500", trim="Scorpione", engine="1.4L Turbo", transmission="automatic",
                 body_type="Hatchback", fuel_type="petrol", drivetrain="FWD",
                 validation_id="VAL-2", source_index=5),
        _variant("BMW", "X5", trim="xDrive40i", validation_id="VAL-3"),
    ]
    groups = group_variants(variants)
    assert len(groups) == 2
    abarth = next(g for g in groups if g.make == "Abarth")
    assert abarth.raw_database_values["trims_seen"] == ["Base", "Scorpione"]
    assert abarth.raw_database_values["transmissions_seen"] == ["automatic", "manual"]
    assert abarth.source_indexes == [3, 5]
    assert abarth.validation_ids == ["VAL-1", "VAL-2"]


def test_select_groups_one_model_sample():
    variants = [
        _variant("Abarth", "500", validation_id="VAL-1"),
        _variant("BMW", "X5", validation_id="VAL-2"),
    ]
    groups = group_variants(variants)
    sel = select_groups(groups, make="Abarth", model="500", limit_models=1)
    assert len(sel) == 1 and sel[0].make == "Abarth"


def test_classify_non_trim():
    assert classify_non_trim("Base", "500")["classification"] == "placeholder"
    assert classify_non_trim("Standard", "500")["classification"] == "placeholder"
    assert classify_non_trim(None, "500")["classification"] == "null"
    assert classify_non_trim("1.4", "500")["classification"] == "engine_size"
    assert classify_non_trim("145hp", "500")["classification"] == "horsepower"
    assert classify_non_trim("500C", "500")["classification"] == "body_or_model_designation"
    # A real trim is not flagged.
    assert classify_non_trim("Scorpione", "500") is None


def _grounded_field_sources(year_end=True):
    fs = {
        "version_or_trim": [0],
        "body_type": [0],
        "fuel_type": [0],
        "engine": [0],
        "engine_displacement_l": [0],
        "horsepower_hp": [0],
        "transmission": [0],
        "drivetrain": [0],
        "year_start": [0],
        "year_end": [0] if year_end else [],
    }
    return fs


def _grounded_profile():
    return {
        "market": "IL",
        "make": "Abarth",
        "model": "500",
        "sources": [
            {
                "source_index": 0,
                "title": "Abarth 500 Competizione spec",
                "url": "https://example.co.il/abarth-500",
                "source_name": "Cartube",
                "source_type": "catalog",
                "supports": ["engine", "horsepower_hp", "transmission"],
            }
        ],
        "technical_variants_il": [
            {
                "version_or_trim": "Scorpione",
                "body_type": "Hatchback",
                "fuel_type": "petrol",
                "engine": "1.4L Turbo",
                "engine_displacement_l": 1.4,
                "horsepower_hp": 145,
                "transmission": "manual",
                "drivetrain": "FWD",
                "year_start": 2010,
                "year_end": 2016,
                "support_level": "direct",
                "source_indexes": [0],
                "field_sources": _grounded_field_sources(year_end=True),
                "missing_grounded_fields": [],
            }
        ],
    }


def test_validate_profile_ready():
    result = validate_profile(_grounded_profile())
    assert result.ready is True
    assert not result.issues
    # Website values derived from the variants.
    avw = result.profile["available_values_for_website"]
    assert avw["version_or_trim"] == ["Scorpione"]
    assert avw["horsepower_hp"] == [145]


def test_technical_variant_requires_field_sources():
    """Every technical variant must include field_sources (spec test 8)."""
    profile = _grounded_profile()
    del profile["technical_variants_il"][0]["field_sources"]
    result = validate_profile(profile)
    assert result.ready is False
    assert any("field_sources" in i for i in result.issues)


def test_non_null_fields_require_sources():
    """A non-null field with no field_sources entry is blocked (spec test 9)."""
    profile = _grounded_profile()
    profile["technical_variants_il"][0]["field_sources"]["horsepower_hp"] = []
    result = validate_profile(profile)
    assert result.ready is False
    assert any("horsepower_hp" in i for i in result.issues)


def test_invalid_field_source_index_blocks_ready():
    """field_sources cannot reference missing source indexes (spec test 10)."""
    profile = _grounded_profile()
    profile["technical_variants_il"][0]["field_sources"]["engine"] = [7]
    result = validate_profile(profile)
    assert result.ready is False
    assert any("unknown source" in i for i in result.issues)


def test_missing_grounded_fields_blocks_website_ready():
    """Missing a REQUIRED field via missing_grounded_fields blocks (spec test 11)."""
    profile = _grounded_profile()
    profile["technical_variants_il"][0]["horsepower_hp"] = None
    profile["technical_variants_il"][0]["field_sources"]["horsepower_hp"] = []
    profile["technical_variants_il"][0]["missing_grounded_fields"] = ["horsepower_hp"]
    result = validate_profile(profile)
    assert result.ready is False
    # year_end being optional/missing must NOT block on its own.
    ok = _grounded_profile()
    ok["technical_variants_il"][0]["year_end"] = None
    ok["technical_variants_il"][0]["field_sources"]["year_end"] = []
    ok["technical_variants_il"][0]["missing_grounded_fields"] = ["year_end"]
    assert validate_profile(ok).ready is True


def test_raw_database_values_are_not_evidence():
    """Raw input values alone cannot make a variant website-ready (spec test 12).

    The offline synthesizer fills fields from raw DB hints but provides no
    sources/field_sources, so the variant must never become website-ready.
    """
    payload = {
        "market": "IL",
        "make": "Abarth",
        "model": "500",
        "raw_database_values": {
            "years_seen": [2010, 2016],
            "trims_seen": ["Scorpione"],
            "engines_seen": ["1.4L Turbo"],
            "horsepower_seen": [180],
            "transmissions_seen": ["manual"],
            "body_types_seen": ["Hatchback"],
            "fuel_types_seen": ["petrol"],
            "drivetrains_seen": ["FWD"],
        },
        "source_indexes": [0],
    }
    profile = CatalogClient.synthesize_offline(payload)
    result = validate_profile(profile)
    assert result.ready is False


def test_validate_profile_blocks_missing_source_and_hp():
    profile = {
        "make": "Abarth",
        "model": "500",
        "technical_variants_il": [
            {
                "version_or_trim": None,
                "body_type": "Hatchback",
                "fuel_type": "petrol",
                "engine": "1.4L Turbo",
                "engine_displacement_l": 1.4,
                "horsepower_hp": None,
                "transmission": "manual",
                "drivetrain": "FWD",
                "year_start": 2010,
                "year_end": 2016,
                "support_level": "unknown",
                "source_indexes": [],
            }
        ],
    }
    result = validate_profile(profile)
    assert result.ready is False
    assert any("horsepower_hp" in i for i in result.issues)
    assert any("source_indexes" in i for i in result.issues)


def test_validate_profile_dedupes_and_blocks_bad_support():
    row = {
        "version_or_trim": "Scorpione",
        "body_type": "Hatchback",
        "fuel_type": "petrol",
        "engine": "1.4L Turbo",
        "engine_displacement_l": 1.4,
        "horsepower_hp": 145,
        "transmission": "manual",
        "drivetrain": "FWD",
        "year_start": 2010,
        "year_end": 2016,
        "support_level": "bogus",  # invalid enum
        "source_indexes": [0],
    }
    profile = {"make": "Abarth", "model": "500", "technical_variants_il": [dict(row), dict(row)]}
    result = validate_profile(profile)
    assert result.stats["duplicate_technical_variants"] == 1
    assert len(result.profile["technical_variants_il"]) == 1
    assert any("support_level" in i for i in result.issues)
    assert result.ready is False


def test_derive_available_values_only_from_variants():
    variants = [
        {"version_or_trim": "A", "body_type": "Hatchback", "fuel_type": "petrol"},
        {"version_or_trim": "A", "body_type": "Cabriolet", "fuel_type": "petrol"},
    ]
    avw = derive_available_values(variants)
    assert avw["version_or_trim"] == ["A"]  # de-duped
    assert avw["body_type"] == ["Hatchback", "Cabriolet"]


def test_offline_synthesize_and_readiness():
    payload = {
        "market": "IL",
        "make": "Abarth",
        "model": "500",
        "raw_database_values": {
            "years_seen": [2010, 2016],
            "trims_seen": ["Base", "Scorpione", "500C"],
            "engines_seen": ["1.4L Turbo"],
            "horsepower_seen": [],
            "transmissions_seen": ["manual"],
            "body_types_seen": ["Hatchback"],
            "fuel_types_seen": ["petrol"],
            "drivetrains_seen": ["FWD"],
        },
        "source_indexes": [0],
    }
    profile = CatalogClient.synthesize_offline(payload)
    # Base and 500C must be classified as non-trims.
    labels = {x["label"] for x in profile["invalid_or_non_trim_labels"]}
    assert {"Base", "500C"} <= labels
    result = validate_profile(profile)
    report = build_readiness_report([result])
    assert report["total_models"] == 1
    assert report["ready_for_website_upload"] is False  # hp/sources unknown offline


def test_end_to_end_offline_writes_three_files(tmp_path):
    from scripts.catalog_builder import build_catalog

    catalog_p = tmp_path / "catalog.json"
    readiness_p = tmp_path / "readiness.json"
    review_p = tmp_path / "review.json"
    result = build_catalog(
        make="Abarth",
        model="500",
        limit_models=1,
        offline=True,
        catalog_path=str(catalog_p),
        readiness_path=str(readiness_p),
        review_path=str(review_p),
    )
    assert os.path.exists(result.catalog_path)
    assert os.path.exists(result.readiness_path)
    assert os.path.exists(result.review_path)
    catalog = json.loads(catalog_p.read_text())
    assert catalog["source_files"] == [
        "data/validation_variants_data_v1.json",
        "data/validation_instructions_by_id_v1.json",
    ]
    assert result.readiness["total_models"] == 1
    # Offline output is always a stub and never website-ready (spec test 13).
    assert result.readiness["offline_stub"] is True
    assert result.readiness["real_grounded_run"] is False
    assert result.readiness["ready_for_website_upload"] is False
    assert catalog["offline_stub"] is True
    assert catalog["ready_for_website_upload"] is False


# ---------------------------------------------------------------------------
# Secrets / env-var standardization
# ---------------------------------------------------------------------------


def test_openai_key_env_name(monkeypatch, tmp_path):
    """The shared config reads the OpenAI key from OPENAI_API_KEY (spec test 1)."""
    from scripts.config import load_shared_config

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    missing = tmp_path / "no_secrets.toml"
    assert load_shared_config(str(missing)).openai_api_key == ""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-123")
    assert load_shared_config(str(missing)).openai_api_key == "sk-test-123"


def test_github_token_env_name(monkeypatch, tmp_path):
    """GitHub checkpoint config reads the token from GITHUB_TOKEN (spec test 2)."""
    from scripts.config import load_shared_config
    from scripts.github_checkpoint import resolve_config_from_env

    missing = tmp_path / "no_secrets.toml"
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    assert load_shared_config(str(missing)).github_token == ""
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_token_value")
    assert load_shared_config(str(missing)).github_token == "ghp_token_value"
    config, _notes = resolve_config_from_env()
    assert config is not None and config.token == "ghp_token_value"


def test_no_legacy_gh_token_alias(monkeypatch):
    """GH_TOKEN must NOT be honored — only GITHUB_TOKEN (spec forbids GH_TOKEN)."""
    from scripts.github_checkpoint import resolve_config_from_env

    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("GH_TOKEN", "ghp_should_be_ignored")
    config, notes = resolve_config_from_env()
    assert config is None
    assert any("GITHUB_TOKEN missing" in n for n in notes)


# ---------------------------------------------------------------------------
# Fail-fast / offline gating
# ---------------------------------------------------------------------------


def test_missing_openai_key_fails_real_run():
    """Real run (offline=False) without an OpenAI key fails fast (spec test 3)."""
    from scripts.catalog_builder import OPENAI_KEY_REQUIRED_MESSAGE, build_catalog
    from scripts.openai_catalog_client import CatalogClientSettings

    with pytest.raises(ValueError) as exc:
        build_catalog(
            make="Abarth",
            model="500",
            limit_models=1,
            offline=False,
            settings=CatalogClientSettings(api_key=""),
        )
    assert "OPENAI_API_KEY is required" in str(exc.value)
    assert str(exc.value) == OPENAI_KEY_REQUIRED_MESSAGE


def test_offline_does_not_require_openai_key(tmp_path):
    """Offline mode runs plumbing without an OpenAI key (spec test 5)."""
    from scripts.catalog_builder import build_catalog

    result = build_catalog(
        make="Abarth",
        model="500",
        limit_models=1,
        offline=True,
        catalog_path=str(tmp_path / "c.json"),
        readiness_path=str(tmp_path / "r.json"),
        review_path=str(tmp_path / "v.json"),
    )
    assert result.readiness["offline_stub"] is True


def test_offline_does_not_require_github_token_when_checkpoint_disabled(tmp_path, monkeypatch):
    """Offline + checkpoint disabled runs without a GitHub token (spec test 6)."""
    from scripts.catalog_builder import build_catalog
    from scripts.catalog_checkpoint import CatalogCheckpointConfig

    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    result = build_catalog(
        make="Abarth",
        model="500",
        limit_models=1,
        offline=True,
        checkpoint=CatalogCheckpointConfig(enabled=False, token=""),
        catalog_path=str(tmp_path / "c.json"),
        readiness_path=str(tmp_path / "r.json"),
        review_path=str(tmp_path / "v.json"),
    )
    assert result.readiness["github_checkpoint_enabled"] is False


def test_missing_github_token_fails_only_when_checkpoint_enabled():
    """Enabled checkpointing without a token fails gracefully (spec test 4)."""
    from scripts.catalog_checkpoint import (
        GITHUB_TOKEN_REQUIRED_MESSAGE,
        CatalogCheckpointConfig,
        CatalogCheckpointer,
    )

    # Disabled: no token needed.
    CatalogCheckpointer(CatalogCheckpointConfig(enabled=False, token=""))
    # Enabled without token: clear, sanitized error.
    with pytest.raises(ValueError) as exc:
        CatalogCheckpointer(CatalogCheckpointConfig(enabled=True, token=""))
    assert str(exc.value) == GITHUB_TOKEN_REQUIRED_MESSAGE


# ---------------------------------------------------------------------------
# Web search grounding
# ---------------------------------------------------------------------------


def test_real_run_requires_web_search_tool():
    """A real Responses request includes {"type": "web_search"} (spec test 7)."""
    from scripts.openai_catalog_client import CatalogClient, CatalogClientSettings

    client = CatalogClient(CatalogClientSettings(api_key="sk-x", use_web_search=True))
    kwargs = client.build_request_kwargs({"make": "Abarth", "model": "500"})
    assert {"type": "web_search"} in kwargs["tools"]

    # With web_search disabled a real call is rejected (cannot ground).
    off = CatalogClient(CatalogClientSettings(api_key="sk-x", use_web_search=False))
    with pytest.raises(RuntimeError):
        off.build_request_kwargs({"make": "Abarth", "model": "500"})


def test_catalog_prompt_requires_web_grounding():
    """The GPT-5.4 prompt forbids answering from memory (spec acceptance 6)."""
    from scripts.openai_catalog_client import CATALOG_SYSTEM_PROMPT

    assert "You must use web_search grounding for this task." in CATALOG_SYSTEM_PROMPT
    assert "Do not answer from memory." in CATALOG_SYSTEM_PROMPT
    assert "Raw database values are only hints" in CATALOG_SYSTEM_PROMPT


# ---------------------------------------------------------------------------
# Checkpoint cadence — per model profile, never per raw variant
# ---------------------------------------------------------------------------


class _RecordingCheckpointer:
    """Stand-in that records each push attempt with its profile id."""

    def __init__(self):
        self.state = {
            "github_checkpoint_enabled": True,
            "github_checkpoint_unit": "model_profile",
            "github_checkpoint_count": 0,
            "github_checkpoint_fail_count": 0,
            "last_github_checkpoint_error": None,
            "last_checkpointed_profile_id": None,
        }
        self.calls = []

    def maybe_checkpoint(self, *, profile_id, paths, market, make, model, force=False):
        self.calls.append(profile_id)
        self.state["github_checkpoint_count"] += 1
        self.state["last_checkpointed_profile_id"] = profile_id
        return True


def test_checkpoint_after_each_model_profile(tmp_path, monkeypatch):
    """push_every_profiles=1 → one checkpoint per completed profile (spec test 14)."""
    import scripts.catalog_builder as cb

    rec = _RecordingCheckpointer()
    monkeypatch.setattr(cb, "CatalogCheckpointer", lambda *a, **k: rec)
    cb.build_catalog(
        limit_models=2,
        offline=True,
        catalog_path=str(tmp_path / "c.json"),
        readiness_path=str(tmp_path / "r.json"),
        review_path=str(tmp_path / "v.json"),
    )
    # Exactly one checkpoint attempt per processed model profile.
    assert len(rec.calls) == 2
    assert all("::" in c for c in rec.calls)


def test_no_checkpoint_after_each_raw_variant(tmp_path, monkeypatch):
    """A multi-variant profile checkpoints once, not once per raw variant (spec test 15)."""
    import scripts.catalog_builder as cb

    rec = _RecordingCheckpointer()
    monkeypatch.setattr(cb, "CatalogCheckpointer", lambda *a, **k: rec)
    # Abarth/500 spans multiple raw variant rows but is ONE model profile.
    cb.build_catalog(
        make="Abarth",
        model="500",
        limit_models=1,
        offline=True,
        catalog_path=str(tmp_path / "c.json"),
        readiness_path=str(tmp_path / "r.json"),
        review_path=str(tmp_path / "v.json"),
    )
    assert len(rec.calls) == 1
