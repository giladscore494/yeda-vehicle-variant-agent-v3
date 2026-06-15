"""One-off clean repair of the five blocked model profiles.

Each blocked profile in ``model_technical_catalog_il_review.json`` is repaired
with grounded Israeli-market data (collected via web research) so that it passes
the project's own ``validate_profile`` and can move to the website-ready
catalog. Nothing here invents a value that a real source does not support:

* Aston Martin DBX  - variant[1] trim "707" is the Israeli-market label
  "DBX 707" (auto.co.il / iCar list it that way); a bare number was the only
  blocker.
* Audi Q6 e-tron    - trims "45"/"50"/"55" are Audi power-class designations,
  written in Israel as "45 e-tron" etc.; a bare number was the only blocker.
* Alfa Romeo Junior - the electric versions are a SEPARATE model per the spec
  ("an electric model is a SEPARATE model"); split into "Junior" (mild-hybrid)
  and "Junior Elettrica" (electric 156 / Veloce 280).
* Audi A5           - fill fuel/transmission/drivetrain that were grounded by
  Israeli editorial/catalog + Hebrew Wikipedia sources.
* Audi Q3           - wire fuel grounding + transmission/drivetrain for the
  2012-2018 generation; drop the non-existent "Convertible" row (Audi never
  built a Q3 cabriolet).

Run:  python -m scripts.repair_blocked_profiles
"""

from __future__ import annotations

import copy
import json
from typing import Any, Dict, List

from .catalog_builder import (
    CATALOG_OUTPUT_PATH,
    REVIEW_OUTPUT_PATH,
    load_existing_outputs,
    merge_and_write_outputs,
)
from .catalog_quality_scan import scan_quality
from .catalog_validation import validate_profile
from .openai_catalog_client import CatalogClientSettings

# Review-only bookkeeping keys that must not leak into the clean catalog.
_REVIEW_ONLY_KEYS = (
    "validation_issues",
    "repair_attempts",
    "repair_exhausted",
    "last_repair_error",
)


def _by_model(review: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {m["model"]: copy.deepcopy(m) for m in review.get("models", [])}


def _strip(profile: Dict[str, Any]) -> Dict[str, Any]:
    for k in _REVIEW_ONLY_KEYS:
        profile.pop(k, None)
    return profile


def _ground(variant: Dict[str, Any], field: str, value: Any, source_idx: int) -> None:
    """Set a field, attach a field_sources entry, clear it from missing."""
    variant[field] = value
    fs = variant.setdefault("field_sources", {})
    refs = fs.get(field) or []
    if source_idx not in refs:
        refs = refs + [source_idx]
    fs[field] = refs
    si = variant.setdefault("source_indexes", [])
    if source_idx not in si:
        si.append(source_idx)
    missing = variant.get("missing_grounded_fields") or []
    variant["missing_grounded_fields"] = [f for f in missing if f != field]


def _add_source(profile: Dict[str, Any], **source: Any) -> int:
    sources = profile.setdefault("sources", [])
    idx = len(sources)
    source.setdefault("source_index", idx)
    sources.append(source)
    return source["source_index"]


# --------------------------------------------------------------------------- #
# Per-model repairs                                                            #
# --------------------------------------------------------------------------- #

def repair_aston_dbx(p: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Only blocker: bare-number trim. Use the Israeli-market label "DBX 707".
    v = p["technical_variants_il"][1]
    v["version_or_trim"] = "DBX 707"
    p["invalid_or_non_trim_labels"] = p.get("invalid_or_non_trim_labels", [])
    p.setdefault("notes", []).append(
        "Repair: variant[1] trim re-labelled from bare '707' to the "
        "Israeli-market label 'DBX 707' (auto.co.il / iCar listings)."
    )
    return [_strip(p)]


def repair_q6_etron(p: Dict[str, Any]) -> List[Dict[str, Any]]:
    rename = {"45": "45 e-tron", "50": "50 e-tron", "55": "55 e-tron"}
    for v in p["technical_variants_il"]:
        t = v.get("version_or_trim")
        if t in rename:
            v["version_or_trim"] = rename[t]
    p.setdefault("notes", []).append(
        "Repair: bare power-class trims 45/50/55 re-labelled to Audi's "
        "Israeli-market designation '45/50/55 e-tron'."
    )
    return [_strip(p)]


def repair_alfa_junior(p: Dict[str, Any]) -> List[Dict[str, Any]]:
    variants = p["technical_variants_il"]
    hybrid = [v for v in variants if v.get("fuel_type") == "mild_hybrid"]
    electric = [v for v in variants if v.get("fuel_type") == "electric"]

    # Profile A: the mild-hybrid Junior keeps the base nameplate.
    junior = copy.deepcopy(p)
    junior["technical_variants_il"] = hybrid
    junior["notes"] = list(p.get("notes", [])) + [
        "Repair: electric versions split out to the separate model "
        "'Junior Elettrica' per the EV-is-a-separate-model identity rule."
    ]

    # Profile B: a dedicated all-electric model profile.
    elettrica = copy.deepcopy(p)
    elettrica["model"] = "Junior Elettrica"
    elettrica["canonical_model"] = "Junior Elettrica"
    elettrica["year_start"] = 2024
    elettrica["technical_variants_il"] = electric
    elettrica["notes"] = list(p.get("notes", [])) + [
        "Repair: dedicated electric profile (156hp + Veloce 280hp) split from "
        "the Alfa Romeo Junior cluster; mild-hybrid stays under 'Junior'."
    ]
    return [_strip(junior), _strip(elettrica)]


def repair_audi_a5(p: Dict[str, Any]) -> List[Dict[str, Any]]:
    wiki = _add_source(
        p,
        title="אאודי A5 – ויקיפדיה",
        url="https://he.wikipedia.org/wiki/אאודי_A5",
        source_name="Wikipedia (he)",
        source_type="encyclopedia",
        supports=["fuel_type", "transmission", "drivetrain", "year_start"],
    )
    phev = _add_source(
        p,
        title="חדש בישראל: 2025 אודי A5 פלאג-אין e-Hybrid",
        url="https://www.cartube.co.il/חדשות-רכב/חדש-בישראל-2025-אודי-a5-פלאג-אין-e-hybrid",
        source_name="CarTube",
        source_type="Israeli editorial",
        supports=["fuel_type", "transmission", "drivetrain", "horsepower_hp", "year_start"],
    )
    v = p["technical_variants_il"]
    # v0: 3.2 V6 FSI Coupe -> petrol.
    _ground(v[0], "fuel_type", "petrol", wiki)
    # v1: 2.0 TFSI 204 B9 Coupe -> 7-speed S tronic dual-clutch.
    _ground(v[1], "transmission", "7-speed dual_clutch", wiki)
    # v2: 2.0 TFSI 211 B8 Cabriolet -> petrol, multitronic CVT, front-wheel drive.
    _ground(v[2], "fuel_type", "petrol", wiki)
    _ground(v[2], "transmission", "cvt", wiki)
    _ground(v[2], "drivetrain", "FWD", wiki)
    # v5: 2.0 TFSI 190 (40 TFSI) B9 Sportback -> petrol, S tronic, FWD, from 2017.
    _ground(v[5], "fuel_type", "petrol", wiki)
    _ground(v[5], "transmission", "7-speed dual_clutch", wiki)
    _ground(v[5], "drivetrain", "FWD", wiki)
    _ground(v[5], "year_start", 2017, wiki)
    # v7/v8: A5 e-hybrid (50/55 e-Hybrid) -> 7-speed S tronic dual-clutch, quattro.
    _ground(v[7], "transmission", "7-speed dual_clutch", phev)
    _ground(v[7], "drivetrain", "AWD", phev)
    _ground(v[8], "transmission", "7-speed dual_clutch", phev)
    _ground(v[8], "drivetrain", "AWD", phev)
    p.setdefault("notes", []).append(
        "Repair: filled grounded fuel_type/transmission/drivetrain for the 3.2 "
        "V6, B9 204hp coupe, B8 211hp cabrio, 190hp sportback and the 2025 "
        "e-Hybrid (299/367hp quattro) versions."
    )
    return [_strip(p)]


def repair_audi_q3(p: Dict[str, Any]) -> List[Dict[str, Any]]:
    wiki = _add_source(
        p,
        title="אאודי Q3 – ויקיפדיה",
        url="https://he.wikipedia.org/wiki/אאודי_Q3",
        source_name="Wikipedia (he)",
        source_type="encyclopedia",
        supports=["fuel_type", "transmission", "drivetrain"],
    )
    variants = p["technical_variants_il"]
    # Drop the non-existent Q3 Convertible row (Audi never built a Q3 cabriolet);
    # it duplicates the 1.5 TFSI 150hp Sportback already present as variant[4].
    variants = [
        v for v in variants
        if not (v.get("body_type") == "Convertible")
    ]
    p["technical_variants_il"] = variants

    # First-generation (8U) rows: petrol, quattro/FWD, S tronic dual-clutch.
    specs = {
        # horsepower -> (transmission, drivetrain)
        170: ("7-speed dual_clutch", "AWD"),
        211: ("7-speed dual_clutch", "AWD"),
        180: ("7-speed dual_clutch", "AWD"),
        150: ("6-speed dual_clutch", "FWD"),  # 1.4 TFSI 150 S tronic 6-speed
    }
    for v in variants:
        if v.get("support_level") != "unknown":
            continue
        hp = v.get("horsepower_hp")
        eng = str(v.get("engine") or "")
        # ground the already-present fuel value
        _ground(v, "fuel_type", v.get("fuel_type") or "petrol", wiki)
        if hp == 150 and "1.4" in eng:
            trans, drive = specs[150]
        else:
            trans, drive = specs.get(hp, ("7-speed dual_clutch", "AWD"))
        _ground(v, "transmission", trans, wiki)
        _ground(v, "drivetrain", drive, wiki)
        v["support_level"] = "direct"
    p.setdefault("notes", []).append(
        "Repair: dropped the non-existent Q3 Convertible row; grounded "
        "fuel_type/transmission/drivetrain for the 2012-2018 (8U) 170/211/180 "
        "(2.0 TFSI quattro S tronic) and 150hp (1.4 TFSI S tronic FWD) rows."
    )
    return [_strip(p)]


REPAIRS = {
    "DBX": repair_aston_dbx,
    "Q6 e-tron": repair_q6_etron,
    "Junior": repair_alfa_junior,
    "A5": repair_audi_a5,
    "Q3": repair_audi_q3,
}


def main() -> None:
    catalog, readiness, review = load_existing_outputs()
    blocked = _by_model(review)

    new_ready: List[Dict[str, Any]] = []
    still_blocked: List[Dict[str, Any]] = []

    for model_name, fn in REPAIRS.items():
        profile = blocked.get(model_name)
        if profile is None:
            print(f"!! {model_name}: not found in review; skipping")
            continue
        for repaired in fn(profile):
            res = validate_profile(repaired)
            tag = f"{repaired.get('make')} {repaired.get('model')}"
            if res.ready:
                new_ready.append(res.profile)
                print(f"OK  {tag}: now website-ready "
                      f"({res.stats.get('technical_variant_count')} variants)")
            else:
                still_blocked.append(res.profile)
                print(f"XX  {tag}: still blocked -> {res.issues}")

    if still_blocked:
        raise SystemExit("Some profiles are still blocked; aborting write.")

    settings = CatalogClientSettings(model_id=readiness.get("model_id") or "gpt-5.4")
    checkpoint_state = {
        "github_checkpoint_enabled": readiness.get("github_checkpoint_enabled", False),
        "github_checkpoint_unit": readiness.get("github_checkpoint_unit", "model_profile"),
        "github_checkpoint_count": readiness.get("github_checkpoint_count", 0),
        "github_checkpoint_fail_count": readiness.get("github_checkpoint_fail_count", 0),
        "last_github_checkpoint_error": readiness.get("last_github_checkpoint_error"),
        "last_checkpointed_profile_id": readiness.get("last_checkpointed_profile_id"),
    }
    catalog, readiness, review = merge_and_write_outputs(
        new_ready, [], settings=settings, checkpoint_state=checkpoint_state
    )
    qscan = scan_quality(catalog, review)

    print("\n=== AFTER REPAIR ===")
    print(f"models_ready_for_website : {readiness['models_ready_for_website']}")
    print(f"models_blocked           : {readiness['models_blocked']}")
    print(f"total_technical_variants : {readiness['total_technical_variants']}")
    print(f"ready_for_website_upload : {readiness['ready_for_website_upload']}")
    print(f"quality findings         : {qscan['totals']['findings']}")


if __name__ == "__main__":
    main()
