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


def test_validate_profile_ready():
    profile = {
        "market": "IL",
        "make": "Abarth",
        "model": "500",
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
            }
        ],
    }
    result = validate_profile(profile)
    assert result.ready is True
    assert not result.issues
    # Website values derived from the variants.
    avw = result.profile["available_values_for_website"]
    assert avw["version_or_trim"] == ["Scorpione"]
    assert avw["horsepower_hp"] == [145]


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
        use_openai=False,
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
