"""Tests for core/source_ids.py — placeholder detection."""
import pytest
from core.source_ids import (
    looks_like_placeholder_source_id,
    has_only_placeholder_source_ids,
    filter_real_source_ids,
)


class TestPlaceholderDetection:
    @pytest.mark.parametrize("sid", [
        "src_1", "src_2", "src_3", "src_99",
        "source_1", "source_2",
        "citation_1", "citation_2",
        "ref_1", "ref_2",
        "1", "2", "3", "42",
        "SRC_1", "SOURCE_1", "REF_1",
    ])
    def test_placeholder_ids_rejected(self, sid):
        assert looks_like_placeholder_source_id(sid) is True

    @pytest.mark.parametrize("sid", [
        "carwow_uk_2023_bmw_3",
        "yad2_listing_12345",
        "autocar_review_golf_mk8",
        "kia_official_il_sportage_2022",
        "https://example.com/source",
        "ministry_of_transport_il",
        "euro_ncap_2021_tucson",
    ])
    def test_real_ids_accepted(self, sid):
        assert looks_like_placeholder_source_id(sid) is False

    def test_has_only_placeholders(self):
        assert has_only_placeholder_source_ids(["src_1", "src_2"]) is True
        assert has_only_placeholder_source_ids(["src_1", "real_source"]) is False
        assert has_only_placeholder_source_ids([]) is False

    def test_filter_real(self):
        result = filter_real_source_ids(["src_1", "real_id", "ref_2", "another_real"])
        assert result == ["real_id", "another_real"]

    def test_empty_and_none(self):
        assert looks_like_placeholder_source_id("") is False
        assert looks_like_placeholder_source_id(None) is False
        assert filter_real_source_ids(None) == []
        assert filter_real_source_ids([]) == []
