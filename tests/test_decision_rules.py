"""The anti-regression heart: weak trim must never cause a reject."""

import pytest

from scripts.validator_engine import decide_mock, merge_identity_and_trim


def ident(**kw):
    base = {
        "make": "Hyundai", "model": "i30", "engine": "1.6L", "transmission": "automatic",
        "fuel_type": "petrol", "drivetrain": "FWD", "body_type": "Hatchback",
        "year_start": 2017, "year_end": 2020, "generation": "PD", "market_scope": "IL",
    }
    base.update(kw)
    return base


def trim(value, weak):
    return {"trim": value, "official_marketed_name_il": None, "local_brand_name_il": None,
            "alternate_names": [], "trim_is_weak": weak}


@pytest.mark.parametrize("value", [None, "", "Base", "Standard", "None", "N/A", "generic", "unknown"])
def test_weak_or_missing_trim_with_valid_identity_is_clean_partial(value):
    weak = value in (None, "") or value.lower() in {
        "base", "standard", "none", "n/a", "generic", "unknown"
    }
    result = decide_mock(ident(), trim(value, weak))
    assert result["validation_decision"] == "clean_partial"
    assert result["trim_status"] == "unresolved"


def test_concrete_trim_with_valid_identity_is_clean_exact():
    result = decide_mock(ident(), trim("N Line", False))
    assert result["validation_decision"] == "clean_exact"


def test_identity_contradiction_year_range_rejects():
    result = decide_mock(ident(year_start=2020, year_end=2010), trim("N Line", False))
    assert result["validation_decision"] == "reject"


def test_missing_make_rejects():
    result = decide_mock(ident(make=None), trim("N Line", False))
    assert result["validation_decision"] == "reject"


def test_electric_with_combustion_engine_rejects():
    result = decide_mock(
        ident(fuel_type="electric", engine="1.6L Turbo"), trim("N Line", False)
    )
    assert result["validation_decision"] == "reject"


def test_split_required_lists_candidates():
    result = decide_mock(ident(), trim("Sport / Luxury", False))
    assert result["validation_decision"] == "split_required"
    assert len(result["split_candidates"]) >= 2


def test_merge_rule_never_rejects_valid_identity_for_weak_trim():
    assert merge_identity_and_trim("likely_valid", True) == "clean_partial"
    assert merge_identity_and_trim("verified", True) == "clean_partial"
    assert merge_identity_and_trim("verified", False) == "clean_exact"
    assert merge_identity_and_trim("invalid", False) == "reject"
