"""Manual web-grounded RS6 data repair + S4 clean-keep / stale-review cleanup.

These pin the current-session data repair: no model call is made (the script
only adds a verified catalog source and drops a conflicting variant), RS6 is
promoted only if it validates, and clean profiles carry no repair-only fields.
"""
from __future__ import annotations

import json

from scripts.catalog_validation import validate_profile
from scripts.manual_rs6_il_grounding_repair import run as repair_rs6_run


def _field_sources(refs):
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


def _variant(**over):
    v = {
        "version_or_trim": None, "body_type": "Estate", "fuel_type": "petrol",
        "engine": "4.0L v8 twin-turbo", "engine_displacement_l": 4.0, "horsepower_hp": 600,
        "transmission": "8-speed automatic", "drivetrain": "AWD",
        "year_start": 2019, "year_end": 2022, "support_level": "indirect",
        "source_indexes": [0, 1], "field_sources": _field_sources([0, 1]),
        "missing_grounded_fields": [],
    }
    v.update(over)
    return v


def _rs6_review_entry():
    """Mirrors the real blocked RS6 shape: 3 real variants, no request_payload."""
    sources = [
        {"source_index": i, "title": f"src{i}", "url": f"https://icar.co.il/{i}",
         "source_name": "iCar", "source_type": "editorial", "supports": ["engine"]}
        for i in range(4)
    ]
    perf = _variant(
        version_or_trim="Performance", horsepower_hp=630, year_start=2022, year_end=2024,
        source_indexes=[1, 2], field_sources=_field_sources([1, 2]),
    )
    # the marketed "Performance" version is grounded; only fuel_type is the gap
    perf["field_sources"]["version_or_trim"] = [2]
    # fuel_type present but ungrounded -> blocking issue
    perf["field_sources"]["fuel_type"] = []
    perf["missing_grounded_fields"] = ["fuel_type"]
    conflicting = _variant(
        horsepower_hp=560, body_type=None, fuel_type="petrol", support_level="unknown",
        year_start=2024, year_end=2024, source_indexes=[3], field_sources=_field_sources([3]),
        missing_grounded_fields=["version_or_trim", "body_type"],
    )
    conflicting["field_sources"]["body_type"] = []
    base = _variant(fuel_type="mild_hybrid", field_sources=_field_sources([0, 1]))
    base["missing_grounded_fields"] = ["version_or_trim"]
    return {
        "market": "IL", "make": "Audi", "model": "RS6", "canonical_model": "RS6",
        "year_start": 2019, "year_end": 2024,
        "technical_variants_il": [base, perf, conflicting],
        "sources": sources, "profile_confidence": "medium", "notes": [],
        "validation_issues": ["blocked"], "repair_attempts": 2, "repair_exhausted": True,
    }


def _valid_s4_clean():
    v = _variant(version_or_trim=None, horsepower_hp=349, engine="3.0L v6 turbo",
                 engine_displacement_l=3.0)
    return {
        "market": "IL", "make": "Audi", "model": "S4", "canonical_model": "S4",
        "technical_variants_il": [v],
        "sources": [{"source_index": 0, "title": "s4", "url": "https://icar.co.il/s4",
                     "source_name": "iCar", "source_type": "catalog", "supports": ["engine"]},
                    {"source_index": 1, "title": "s4b", "url": "https://icar.co.il/s4b",
                     "source_name": "iCar", "source_type": "catalog", "supports": ["year_end"]}],
        "profile_confidence": "medium",
    }


def _paths(tmp_path, catalog_models, review_models):
    cat = tmp_path / "c.json"
    rdy = tmp_path / "r.json"
    rev = tmp_path / "v.json"
    cat.write_text(json.dumps({"models": catalog_models}), encoding="utf-8")
    rdy.write_text(json.dumps({"last_checkpointed_profile_id": "IL::Audi::S3"}), encoding="utf-8")
    rev.write_text(json.dumps({"models": review_models}), encoding="utf-8")
    return str(cat), str(rdy), str(rev)


def test_rs6_manual_repair_promotes_and_s4_stays_clean(tmp_path):
    s4 = _valid_s4_clean()
    assert validate_profile(s4).ready  # sanity: the clean S4 fixture validates
    # a stale S4 duplicate also sits in review and must be removed
    stale_s4 = dict(s4)
    stale_s4 = json.loads(json.dumps(s4))
    stale_s4["validation_issues"] = ["stale"]
    cat, rdy, rev = _paths(tmp_path, [s4], [_rs6_review_entry(), stale_s4])

    logs = []
    result = repair_rs6_run(catalog_path=cat, readiness_path=rdy, review_path=rev, log=logs.append)
    assert result["s4_status"] == "valid_clean"
    assert result["rs6_status"] == "promoted"

    catalog = json.loads(open(cat, encoding="utf-8").read())
    review = json.loads(open(rev, encoding="utf-8").read())
    models = {m["model"]: m for m in catalog["models"]}

    # S4 kept in clean; stale review duplicate removed; RS6 promoted; review empty
    assert "S4" in models and "RS6" in models
    assert review["models"] == []

    rs6 = models["RS6"]
    assert rs6["market"] == "IL" and rs6["make"] == "Audi" and rs6["canonical_model"] == "RS6"
    # conflicting 560 hp variant dropped -> 2 grounded variants remain
    assert len(rs6["technical_variants_il"]) == 2
    hps = {v["horsepower_hp"] for v in rs6["technical_variants_il"]}
    assert hps == {600, 630} and 560 not in hps
    # performance fuel_type now grounded via the added catalog source
    perf = next(v for v in rs6["technical_variants_il"] if v["horsepower_hp"] == 630)
    assert perf["field_sources"]["fuel_type"]
    assert "fuel_type" not in perf.get("missing_grounded_fields", [])
    assert any(s["source_name"] == "auto-data.net" for s in rs6["sources"])

    # no repair-only fields leak into clean
    for prof in (models["RS6"], models["S4"]):
        for k in ("request_payload", "rebuild_required", "repair_attempts", "repair_exhausted",
                  "last_repair_error", "manual_full_rebuild_override_used", "last_repair_mode",
                  "validation_issues", "error"):
            assert k not in prof

    readiness = json.loads(open(rdy, encoding="utf-8").read())
    assert readiness["models_blocked"] == 0
    # repair must not move the main build pointer
    assert readiness.get("last_checkpointed_profile_id") == "IL::Audi::S3"
    assert readiness.get("last_repair_checkpointed_profile_id") == "IL::Audi::RS6"

    joined = "\n".join(logs)
    assert "MANUAL WEB REPAIR: IL|Audi|RS6" in joined
    assert "PROMOTE IL|Audi|RS6 after manual web-grounded repair" in joined
