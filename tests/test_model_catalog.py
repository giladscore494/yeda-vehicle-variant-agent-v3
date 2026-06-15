"""Tests for the single-GPT-5.4 Israeli model technical-catalog pipeline.

The pipeline has one production path: GPT-5.4 with web_search grounding.
``OPENAI_API_KEY`` is required and the run fails closed without it. The
tests below also assert the retired pipelines stay gone (see the negative
contract tests).
"""

from __future__ import annotations

import json
import os

import pytest

import scripts.catalog_builder as cb
from scripts.catalog_grouping import group_variants, select_groups
from scripts.catalog_validation import (
    build_readiness_report,
    derive_available_values,
    validate_profile,
)
from scripts.catalog_normalization import (
    merge_year_variants,
    normalize_body_type,
    normalize_drivetrain,
    normalize_engine,
    normalize_fuel_type,
    normalize_support_level,
    normalize_transmission,
    normalize_variant,
)
from scripts.openai_catalog_client import (
    CatalogClient,
    CatalogClientSettings,
    classify_non_trim,
)


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------


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


def _grounded_field_sources(year_end=True):
    return {
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


def _grounded_profile(make="Abarth", model="500", market="IL"):
    return {
        "market": market,
        "make": make,
        "model": model,
        "sources": [
            {
                "source_index": 0,
                "title": f"{make} {model} spec",
                "url": "https://example.co.il/spec",
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


def _patch_client(monkeypatch, profile_factory=None):
    """Make CatalogClient.build_profile return a grounded profile (no network)."""
    factory = profile_factory or (lambda payload: _grounded_profile(
        make=payload.get("make", "Abarth"), model=payload.get("model", "500"),
        market=payload.get("market", "IL"),
    ))

    def fake_build_profile(self, request_payload):
        self.calls += 1
        return factory(request_payload)

    monkeypatch.setattr(CatalogClient, "build_profile", fake_build_profile)


# ---------------------------------------------------------------------------
# Grouping / selection (run-count limiting)
# ---------------------------------------------------------------------------


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
    assert abarth.source_indexes == [3, 5]
    assert abarth.validation_ids == ["VAL-1", "VAL-2"]
    assert abarth.raw_variant_count == 2


def test_select_groups_limits_clusters():
    """Run count limits how many make/model clusters are processed (spec 11)."""
    variants = [
        _variant("Abarth", "500", validation_id="VAL-1"),
        _variant("BMW", "X5", validation_id="VAL-2"),
        _variant("Audi", "A3", validation_id="VAL-3"),
    ]
    groups = group_variants(variants)
    assert len(select_groups(groups, limit_models=1)) == 1
    assert len(select_groups(groups, limit_models=2)) == 2
    sel = select_groups(groups, make="Abarth", model="500", limit_models=1)
    assert len(sel) == 1 and sel[0].make == "Abarth"


def test_select_groups_start_after_key():
    variants = [
        _variant("Abarth", "500", validation_id="VAL-1"),
        _variant("BMW", "X5", validation_id="VAL-2"),
        _variant("Audi", "A3", validation_id="VAL-3"),
    ]
    groups = group_variants(variants)
    after_first = select_groups(groups, start_after_key=groups[0].key)
    assert [g.key for g in after_first] == [groups[1].key, groups[2].key]


def test_classify_non_trim():
    assert classify_non_trim("Base", "500")["classification"] == "placeholder"
    assert classify_non_trim(None, "500")["classification"] == "null"
    assert classify_non_trim("1.4", "500")["classification"] == "engine_size"
    assert classify_non_trim("145hp", "500")["classification"] == "horsepower"
    assert classify_non_trim("500C", "500")["classification"] == "body_or_model_designation"
    assert classify_non_trim("Scorpione", "500") is None


# ---------------------------------------------------------------------------
# Canonical normalization
# ---------------------------------------------------------------------------


def test_normalize_body_type_canonical():
    assert normalize_body_type("Cabriolet") == "Convertible"
    assert normalize_body_type("Turismo Cabrio") == "Convertible"
    assert normalize_body_type("station wagon") == "Estate"
    assert normalize_body_type("Avant") == "Estate"
    assert normalize_body_type("Saloon") == "Sedan"
    assert normalize_body_type("Crossover SUV") == "Crossover"
    assert normalize_body_type("MPV") == "MPV"
    assert normalize_body_type(None) is None


def test_normalize_fuel_type_canonical():
    assert normalize_fuel_type("Gasoline") == "petrol"
    assert normalize_fuel_type("Plug-in Hybrid") == "plug_in_hybrid"
    assert normalize_fuel_type("MHEV") == "mild_hybrid"
    assert normalize_fuel_type("Hybrid") == "hybrid"
    assert normalize_fuel_type("BEV") == "electric"
    assert normalize_fuel_type("Fuel Cell") == "hydrogen"


def test_normalize_transmission_keeps_sourced_speed_count():
    assert normalize_transmission("Automatic") == "automatic"
    assert normalize_transmission("DSG") == "dual_clutch"
    assert normalize_transmission("7-speed DSG") == "7-speed dual_clutch"
    assert normalize_transmission("6 speed manual") == "6-speed manual"
    assert normalize_transmission("e-CVT") == "cvt"


def test_normalize_drivetrain_canonical():
    assert normalize_drivetrain("all-wheel drive") == "AWD"
    assert normalize_drivetrain("Quattro") == "AWD"
    assert normalize_drivetrain("4x4") == "4WD"
    assert normalize_drivetrain("front wheel drive") == "FWD"


def test_normalize_engine_canonical_string():
    assert normalize_engine("1.4") == "1.4L"
    assert normalize_engine("1.4L Turbo") == "1.4L turbo"
    assert normalize_engine("2.0 V6 Turbo") == "2.0L v6 turbo"
    assert normalize_engine("2.0L gasoline turbo") == "2.0L turbo"
    assert normalize_engine(None, fuel_type="electric") == "electric"
    assert normalize_engine("Single Motor", fuel_type="electric") == "electric"


def test_normalize_support_level_invariant():
    grounded = {
        "body_type": "SUV",
        "fuel_type": "petrol",
        "engine": "2.0L turbo",
        "horsepower_hp": 200,
        "transmission": "automatic",
        "drivetrain": "AWD",
        "year_start": 2018,
        "year_end": 2022,
        "support_level": "indirect",
        "field_sources": {
            "body_type": [0], "fuel_type": [0], "engine": [0],
            "horsepower_hp": [0], "transmission": [0], "drivetrain": [0],
            "year_start": [0], "year_end": [0],
        },
        "missing_grounded_fields": [],
    }
    # Fully grounded + complete -> must be direct.
    assert normalize_support_level(grounded) == "direct"
    # An inferred (ungrounded) non-null field keeps it indirect.
    inferred = dict(grounded, field_sources=dict(grounded["field_sources"], drivetrain=[]))
    assert normalize_support_level(inferred) == "indirect"
    # A listed missing field keeps it indirect.
    missing = dict(grounded, missing_grounded_fields=["year_end"], year_end=None)
    assert normalize_support_level(missing) == "indirect"
    # Other levels are untouched.
    assert normalize_support_level(dict(grounded, support_level="conflict")) == "conflict"


def test_normalize_variant_applies_all_fields():
    out = normalize_variant({
        "body_type": "Cabriolet",
        "fuel_type": "Gasoline",
        "engine": "1.4L Turbo",
        "transmission": "7-speed DSG",
        "drivetrain": "Quattro",
        "support_level": "unknown",
    })
    assert out["body_type"] == "Convertible"
    assert out["fuel_type"] == "petrol"
    assert out["engine"] == "1.4L turbo"
    assert out["transmission"] == "7-speed dual_clutch"
    assert out["drivetrain"] == "AWD"


def test_merge_year_variants_spans_range():
    base = {
        "version_or_trim": "Sport",
        "body_type": "SUV",
        "fuel_type": "petrol",
        "engine": "2.0L turbo",
        "horsepower_hp": 200,
        "transmission": "automatic",
        "drivetrain": "AWD",
        "source_indexes": [0],
        "field_sources": {"engine": [0]},
        "missing_grounded_fields": [],
    }
    rows = [
        dict(base, year_start=2015, year_end=2018),
        dict(base, year_start=2019, year_end=2022, source_indexes=[1]),
    ]
    merged, count = merge_year_variants(rows)
    assert count == 1
    assert len(merged) == 1
    assert merged[0]["year_start"] == 2015
    assert merged[0]["year_end"] == 2022
    assert merged[0]["source_indexes"] == [0, 1]


def test_merge_year_variants_keeps_distinct_horsepower():
    base = {
        "version_or_trim": "Sport", "body_type": "SUV", "fuel_type": "petrol",
        "engine": "2.0L turbo", "transmission": "automatic", "drivetrain": "AWD",
    }
    rows = [
        dict(base, horsepower_hp=180, year_start=2015, year_end=2018),
        dict(base, horsepower_hp=200, year_start=2019, year_end=2022),
    ]
    merged, count = merge_year_variants(rows)
    assert count == 0
    assert len(merged) == 2


# ---------------------------------------------------------------------------
# Profile validation
# ---------------------------------------------------------------------------


def test_validate_profile_ready():
    result = validate_profile(_grounded_profile())
    assert result.ready is True
    assert not result.issues
    avw = result.profile["available_values_for_website"]
    assert avw["version_or_trim"] == ["Scorpione"]
    assert avw["horsepower_hp"] == [145]


def test_validate_profile_normalizes_canonical_values():
    profile = _grounded_profile()
    profile["technical_variants_il"][0]["body_type"] = "Cabriolet"
    profile["technical_variants_il"][0]["fuel_type"] = "Gasoline"
    profile["technical_variants_il"][0]["drivetrain"] = "Quattro"
    result = validate_profile(profile)
    variant = result.profile["technical_variants_il"][0]
    assert variant["body_type"] == "Convertible"
    assert variant["fuel_type"] == "petrol"
    assert variant["engine"] == "1.4L turbo"
    assert variant["drivetrain"] == "AWD"
    assert result.profile["available_values_for_website"]["body_type"] == ["Convertible"]


def test_validate_profile_merges_year_split_rows():
    profile = _grounded_profile()
    second = dict(profile["technical_variants_il"][0])
    profile["technical_variants_il"][0]["year_start"] = 2010
    profile["technical_variants_il"][0]["year_end"] = 2015
    second["year_start"] = 2016
    second["year_end"] = 2020
    profile["technical_variants_il"].append(second)
    result = validate_profile(profile)
    assert result.stats["merged_year_variants"] == 1
    assert len(result.profile["technical_variants_il"]) == 1
    assert result.profile["technical_variants_il"][0]["year_start"] == 2010
    assert result.profile["technical_variants_il"][0]["year_end"] == 2020
    assert result.ready is True


def test_technical_variant_requires_field_sources():
    profile = _grounded_profile()
    del profile["technical_variants_il"][0]["field_sources"]
    result = validate_profile(profile)
    assert result.ready is False
    assert any("field_sources" in i for i in result.issues)


def test_non_null_fields_require_sources():
    profile = _grounded_profile()
    profile["technical_variants_il"][0]["field_sources"]["horsepower_hp"] = []
    result = validate_profile(profile)
    assert result.ready is False
    assert any("horsepower_hp" in i for i in result.issues)


def test_invalid_field_source_index_blocks_ready():
    profile = _grounded_profile()
    profile["technical_variants_il"][0]["field_sources"]["engine"] = [7]
    result = validate_profile(profile)
    assert result.ready is False
    assert any("unknown source" in i for i in result.issues)


def test_missing_grounded_fields_blocks_website_ready():
    profile = _grounded_profile()
    profile["technical_variants_il"][0]["horsepower_hp"] = None
    profile["technical_variants_il"][0]["field_sources"]["horsepower_hp"] = []
    profile["technical_variants_il"][0]["missing_grounded_fields"] = ["horsepower_hp"]
    assert validate_profile(profile).ready is False
    # year_end being optional/missing must NOT block on its own.
    ok = _grounded_profile()
    ok["technical_variants_il"][0]["year_end"] = None
    ok["technical_variants_il"][0]["field_sources"]["year_end"] = []
    ok["technical_variants_il"][0]["missing_grounded_fields"] = ["year_end"]
    assert validate_profile(ok).ready is True


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
    assert avw["version_or_trim"] == ["A"]
    assert avw["body_type"] == ["Hatchback", "Cabriolet"]


def test_readiness_report_is_grounded_by_default():
    result = validate_profile(_grounded_profile())
    report = build_readiness_report([result])
    assert report["total_models"] == 1
    assert report["real_grounded_run"] is True
    assert report["openai_api_key_env_name"] == "OPENAI_API_KEY"
    assert report["ready_for_website_upload"] is True
    # The retired stub concept does not survive in the readiness report.
    assert "offline_stub" not in report


# ---------------------------------------------------------------------------
# Fail-closed without OPENAI_API_KEY
# ---------------------------------------------------------------------------


def test_missing_openai_key_fails_closed():
    """A run without an OpenAI key fails closed (spec 2 & 11)."""
    from scripts.catalog_provider import ProviderUnavailableError

    with pytest.raises(ProviderUnavailableError) as exc:
        cb.build_catalog(
            make="Abarth", model="500", limit_models=1,
            settings=CatalogClientSettings(api_key=""),
        )
    assert "OpenAI API key is missing" in str(exc.value)
    assert "No fallback" in str(exc.value)


def test_cli_does_not_accept_offline_flag():
    """The CLI no longer accepts --offline (spec 11)."""
    from scripts.run_model_catalog import main

    with pytest.raises(SystemExit):
        main(["--offline"])


def test_no_synthesize_offline_on_client():
    """The OpenAI client has no offline synthesizer (spec 11)."""
    assert not hasattr(CatalogClient, "synthesize_offline")
    import scripts.openai_catalog_client as mod

    src = open(mod.__file__).read()
    assert "synthesize_offline" not in src
    assert "offline" not in src.lower()


def test_openai_client_imports_json_utils_not_gemini():
    """parse_strict_json comes from json_utils, never gemini_client (spec 4)."""
    import scripts.openai_catalog_client as mod

    src = open(mod.__file__).read()
    assert "from .json_utils import parse_strict_json" in src
    assert "gemini_client" not in src


# ---------------------------------------------------------------------------
# End-to-end build (client patched — no network)
# ---------------------------------------------------------------------------


def test_build_calls_build_profile_never_synthesize(monkeypatch, tmp_path):
    """build_catalog drives CatalogClient.build_profile (spec 11)."""
    seen = {}
    _patch_client(monkeypatch)
    # synthesize_offline must not exist to be called.
    assert not hasattr(CatalogClient, "synthesize_offline")

    result = cb.build_catalog(
        make="Abarth", model="500", limit_models=1,
        settings=CatalogClientSettings(api_key="sk-test"),
        catalog_path=str(tmp_path / "c.json"),
        readiness_path=str(tmp_path / "r.json"),
        review_path=str(tmp_path / "v.json"),
        log=lambda m: seen.setdefault("logged", True),
    )
    assert os.path.exists(result.catalog_path)
    assert os.path.exists(result.readiness_path)
    assert os.path.exists(result.review_path)
    catalog = json.loads((tmp_path / "c.json").read_text())
    assert catalog["mode"] == "online_selectable_provider"
    assert catalog["source_files"] == [
        "data/validation_variants_data_v1.json",
        "data/validation_instructions_by_id_v1.json",
    ]
    assert result.readiness["total_models"] == 1
    assert result.readiness["ready_for_website_upload"] is True


def test_atomic_write_leaves_no_tmp_file(monkeypatch, tmp_path):
    """Output files are written atomically (no leftover .tmp) (spec 11)."""
    _patch_client(monkeypatch)
    cb.build_catalog(
        make="Abarth", model="500", limit_models=1,
        settings=CatalogClientSettings(api_key="sk-test"),
        catalog_path=str(tmp_path / "c.json"),
        readiness_path=str(tmp_path / "r.json"),
        review_path=str(tmp_path / "v.json"),
    )
    leftovers = [p for p in os.listdir(tmp_path) if p.endswith(".tmp")]
    assert leftovers == []


def test_progress_callback_receives_make_model_index_total(monkeypatch, tmp_path):
    """on_progress reports make/model/index/total/sample ids (spec 6 & 11)."""
    _patch_client(monkeypatch)
    events = []
    cb.build_catalog(
        limit_models=2,
        settings=CatalogClientSettings(api_key="sk-test"),
        catalog_path=str(tmp_path / "c.json"),
        readiness_path=str(tmp_path / "r.json"),
        review_path=str(tmp_path / "v.json"),
        on_progress=lambda info: events.append(info),
    )
    running = [e for e in events if e["phase"] == "running"]
    done = [e for e in events if e["phase"] == "done"]
    assert running and done
    first = running[0]
    assert first["index"] == 1
    assert first["total"] == 2
    assert "make" in first and "model" in first
    assert "validation_ids" in first
    assert isinstance(first["validation_ids"], list)
    assert done[0]["technical_variants"] >= 0


# ---------------------------------------------------------------------------
# Web search grounding
# ---------------------------------------------------------------------------


def test_real_run_requires_web_search_tool():
    client = CatalogClient(CatalogClientSettings(api_key="sk-x", use_web_search=True))
    kwargs = client.build_request_kwargs({"make": "Abarth", "model": "500"})
    assert {"type": "web_search"} in kwargs["tools"]

    off = CatalogClient(CatalogClientSettings(api_key="sk-x", use_web_search=False))
    with pytest.raises(RuntimeError):
        off.build_request_kwargs({"make": "Abarth", "model": "500"})


def test_catalog_prompt_requires_web_grounding():
    from scripts.openai_catalog_client import CATALOG_SYSTEM_PROMPT

    assert "You must use web_search grounding for this task." in CATALOG_SYSTEM_PROMPT
    assert "Do not answer from memory." in CATALOG_SYSTEM_PROMPT
    assert "Raw database values are only hints" in CATALOG_SYSTEM_PROMPT


def test_catalog_prompt_states_canonical_normalization():
    from scripts.openai_catalog_client import CATALOG_SYSTEM_PROMPT

    assert "Normalization" in CATALOG_SYSTEM_PROMPT
    assert "plug_in_hybrid" in CATALOG_SYSTEM_PROMPT
    assert "dual_clutch" in CATALOG_SYSTEM_PROMPT
    assert "do NOT split by year alone" in CATALOG_SYSTEM_PROMPT
    assert 'support_level MUST be "direct"' in CATALOG_SYSTEM_PROMPT


# ---------------------------------------------------------------------------
# Config: current Streamlit secrets format
# ---------------------------------------------------------------------------


def test_config_reads_current_secrets_format(tmp_path):
    from scripts.config import load_shared_config

    path = tmp_path / "secrets.toml"
    path.write_text(
        """[github]
token = "ghp_test"
repo_full_name = "owner/repo"
target_branch = "validation-v2-budgeted-dual-il-trims"

[openai]
api_key = "sk-test"
validator_model_id = "gpt-5.4"
web_search_enabled = true

[google]
api_key = "google-test"
gemini_validator_model_id = "gemini-3.1-pro-preview"
grounding_enabled = false
""",
        encoding="utf-8",
    )
    cfg = load_shared_config(str(path))
    assert cfg.github_token == "ghp_test"
    assert cfg.github_repo_full_name == "owner/repo"
    assert cfg.github_target_branch == "validation-v2-budgeted-dual-il-trims"
    assert cfg.openai_api_key == "sk-test"
    assert cfg.openai_validator_model_id == "gpt-5.4"
    assert cfg.openai_web_search_enabled is True
    assert cfg.google_api_key == "google-test"
    assert cfg.gemini_validator_model_id == "gemini-3.1-pro-preview"
    assert cfg.gemini_grounding_enabled is False


def test_default_model_is_gpt54(tmp_path):
    from scripts.config import load_shared_config

    cfg = load_shared_config(str(tmp_path / "missing.toml"))
    assert cfg.openai_validator_model_id == "gpt-5.4"
    assert cfg.gemini_validator_model_id == "gemini-3.1-pro-preview"


def test_config_does_not_require_base_branch(tmp_path):
    from scripts.config import load_shared_config

    path = tmp_path / "secrets.toml"
    path.write_text(
        """[github]
token = "t"
repo_full_name = "owner/repo"
target_branch = "target"
[openai]
api_key = "sk"
[google]
api_key = "g"
""",
        encoding="utf-8",
    )
    cfg = load_shared_config(str(path))
    assert cfg.github_target_branch == "target"
    assert not hasattr(cfg, "base_branch")


def test_github_env_resolver_is_disabled_for_current_secrets(monkeypatch):
    from scripts.github_checkpoint import resolve_config_from_env

    monkeypatch.setenv("UNUSED_TOKEN_NAME", "ghp_token_value")
    config, notes = resolve_config_from_env()
    assert config is None
    assert notes


# ---------------------------------------------------------------------------
# GitHub checkpoint: optional and only when enabled
# ---------------------------------------------------------------------------


def test_missing_github_token_fails_only_when_checkpoint_enabled():
    from scripts.catalog_checkpoint import (
        GITHUB_SECRET_REQUIRED_MESSAGE,
        CatalogCheckpointConfig,
        CatalogCheckpointer,
    )

    # Disabled: no token needed.
    CatalogCheckpointer(CatalogCheckpointConfig(enabled=False, token=""))
    # Enabled without token: clear, sanitized error.
    with pytest.raises(ValueError) as exc:
        CatalogCheckpointer(CatalogCheckpointConfig(enabled=True, token=""))
    assert str(exc.value) == GITHUB_SECRET_REQUIRED_MESSAGE


def test_checkpoint_disabled_by_default_does_not_trigger(monkeypatch, tmp_path):
    """With checkpointing disabled, no push is attempted (spec 11)."""
    _patch_client(monkeypatch)
    result = cb.build_catalog(
        make="Abarth", model="500", limit_models=1,
        settings=CatalogClientSettings(api_key="sk-test"),
        checkpoint=None,
        catalog_path=str(tmp_path / "c.json"),
        readiness_path=str(tmp_path / "r.json"),
        review_path=str(tmp_path / "v.json"),
    )
    assert result.readiness["github_checkpoint_enabled"] is False
    assert result.readiness["github_checkpoint_count"] == 0


class _RecordingCheckpointer:
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


def test_checkpoint_after_each_model_profile(monkeypatch, tmp_path):
    """One checkpoint per completed profile, never per raw variant (spec 11)."""
    _patch_client(monkeypatch)
    rec = _RecordingCheckpointer()
    monkeypatch.setattr(cb, "CatalogCheckpointer", lambda *a, **k: rec)
    cb.build_catalog(
        limit_models=2,
        settings=CatalogClientSettings(api_key="sk-test"),
        catalog_path=str(tmp_path / "c.json"),
        readiness_path=str(tmp_path / "r.json"),
        review_path=str(tmp_path / "v.json"),
    )
    assert len(rec.calls) == 2
    assert all("::" in c for c in rec.calls)


def test_no_checkpoint_after_each_raw_variant(monkeypatch, tmp_path):
    """A multi-variant profile checkpoints once, not once per raw variant (spec 11)."""
    _patch_client(monkeypatch)
    rec = _RecordingCheckpointer()
    monkeypatch.setattr(cb, "CatalogCheckpointer", lambda *a, **k: rec)
    cb.build_catalog(
        make="Abarth", model="500", limit_models=1,
        settings=CatalogClientSettings(api_key="sk-test"),
        catalog_path=str(tmp_path / "c.json"),
        readiness_path=str(tmp_path / "r.json"),
        review_path=str(tmp_path / "v.json"),
    )
    assert len(rec.calls) == 1
