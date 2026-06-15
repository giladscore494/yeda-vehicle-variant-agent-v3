"""Tests for non-mutating catalog quality scanning."""

from scripts.catalog_quality_scan import scan_quality


def test_scan_quality_accepts_unhashable_variant_signature_values(tmp_path):
    """Unexpected structured values in variant fields should not crash scan."""
    catalog = {
        "models": [
            {
                "make": "Abarth",
                "model": "500",
                "sources": [],
                "technical_variants_il": [
                    {
                        "body_type": "Hatchback",
                        "fuel_type": ["petrol"],
                        "engine": {"label": "1.4L Turbo"},
                        "horsepower_hp": 145,
                        "transmission": "manual",
                        "drivetrain": "FWD",
                        "year_start": 2010,
                        "year_end": 2016,
                        "field_sources": {},
                    }
                ],
            }
        ]
    }

    report = scan_quality(catalog, {}, output_path=str(tmp_path / "scan.json"))

    assert report["totals"]["models"] == 1
    assert (tmp_path / "scan.json").exists()
