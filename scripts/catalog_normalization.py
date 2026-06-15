"""Canonical normalization for technical-catalog variants.

Normalization maps a sourced value to a fixed canonical label so the same
configuration reads identically across every row and every run. It never
invents a value no source supports: it only rewrites a value that is already
present into its canonical spelling. A ``None`` stays ``None``.

The canonical vocabularies (body_type, fuel_type, transmission, drivetrain,
engine) and the two logical invariants (the ``support_level`` rule and
year-only variant merging) are defined by the catalog spec and enforced here
deterministically, after the model returns a profile.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Canonical vocabularies
# ---------------------------------------------------------------------------

# body_type — Title Case, singular. Order matters: the first keyword found in
# the sourced label wins, so more specific terms are listed before generic ones
# (e.g. "crossover" before "suv", "cabrio" before "sedan").
_BODY_TYPE_KEYWORDS: Tuple[Tuple[str, str], ...] = (
    ("liftback", "Liftback"),
    ("fastback", "Liftback"),
    ("crossover", "Crossover"),
    ("cuv", "Crossover"),
    ("suv", "SUV"),
    ("roadster", "Roadster"),
    ("spider", "Roadster"),
    ("spyder", "Roadster"),
    ("convertible", "Convertible"),
    ("cabriolet", "Convertible"),
    ("cabrio", "Convertible"),
    ("coupe", "Coupe"),
    ("coupé", "Coupe"),
    ("hatchback", "Hatchback"),
    ("hatch", "Hatchback"),
    ("liftgate", "Hatchback"),
    ("estate", "Estate"),
    ("station wagon", "Estate"),
    ("stationwagon", "Estate"),
    ("wagon", "Estate"),
    ("touring", "Estate"),
    ("avant", "Estate"),
    ("variant", "Estate"),
    ("kombi", "Estate"),
    ("sportbrake", "Estate"),
    ("minivan", "MPV"),
    ("mpv", "MPV"),
    ("people carrier", "MPV"),
    ("multivan", "MPV"),
    ("pickup", "Pickup"),
    ("pick-up", "Pickup"),
    ("pick up", "Pickup"),
    ("van", "Van"),
    ("saloon", "Sedan"),
    ("sedan", "Sedan"),
    ("notchback", "Sedan"),
)

# fuel_type — lowercase, underscore for compounds. Order matters so that the
# qualified hybrids match before the bare "hybrid".
_FUEL_TYPE_KEYWORDS: Tuple[Tuple[str, str], ...] = (
    ("plug-in hybrid", "plug_in_hybrid"),
    ("plug in hybrid", "plug_in_hybrid"),
    ("plug_in_hybrid", "plug_in_hybrid"),
    ("plugin hybrid", "plug_in_hybrid"),
    ("phev", "plug_in_hybrid"),
    ("mild hybrid", "mild_hybrid"),
    ("mild-hybrid", "mild_hybrid"),
    ("mild_hybrid", "mild_hybrid"),
    ("mhev", "mild_hybrid"),
    ("hybrid", "hybrid"),
    ("hev", "hybrid"),
    ("electric", "electric"),
    ("bev", "electric"),
    ("ev", "electric"),
    ("gasoline", "petrol"),
    ("benzin", "petrol"),
    ("petrol", "petrol"),
    ("gas", "petrol"),
    ("diesel", "diesel"),
    ("hydrogen", "hydrogen"),
    ("fuel cell", "hydrogen"),
    ("fcev", "hydrogen"),
    ("lpg", "lpg"),
    ("cng", "cng"),
)

# drivetrain — exactly one of FWD, RWD, AWD, 4WD.
_DRIVETRAIN_KEYWORDS: Tuple[Tuple[str, str], ...] = (
    ("fwd", "FWD"),
    ("front-wheel", "FWD"),
    ("front wheel", "FWD"),
    ("rwd", "RWD"),
    ("rear-wheel", "RWD"),
    ("rear wheel", "RWD"),
    ("4wd", "4WD"),
    ("4x4", "4WD"),
    ("4×4", "4WD"),
    ("four-wheel", "4WD"),
    ("four wheel", "4WD"),
    ("awd", "AWD"),
    ("all-wheel", "AWD"),
    ("all wheel", "AWD"),
    ("quattro", "AWD"),
    ("4motion", "AWD"),
    ("xdrive", "AWD"),
    ("4matic", "AWD"),
)

# transmission — exactly one base type. Speed counts are preserved only as a
# "N-speed <type>" prefix when the source carried one.
_TRANSMISSION_KEYWORDS: Tuple[Tuple[str, str], ...] = (
    ("dual-clutch", "dual_clutch"),
    ("dual clutch", "dual_clutch"),
    ("dual_clutch", "dual_clutch"),
    ("twin-clutch", "dual_clutch"),
    ("twin clutch", "dual_clutch"),
    ("dct", "dual_clutch"),
    ("dsg", "dual_clutch"),
    ("pdk", "dual_clutch"),
    ("s tronic", "dual_clutch"),
    ("s-tronic", "dual_clutch"),
    ("e-cvt", "cvt"),
    ("ecvt", "cvt"),
    ("cvt", "cvt"),
    ("single-speed", "single_speed"),
    ("single speed", "single_speed"),
    ("single_speed", "single_speed"),
    ("reduction gear", "single_speed"),
    ("manual", "manual"),
    ("automatic", "automatic"),
    ("auto", "automatic"),
    ("tiptronic", "automatic"),
    ("torque converter", "automatic"),
)

_EV_FUELS = {"electric"}

_SPEED_RE = re.compile(r"(\d+)\s*[- ]?\s*speed", re.IGNORECASE)
_FUEL_WORDS_RE = re.compile(r"\b(gasoline|petrol|diesel|gas|benzin)\b", re.IGNORECASE)
_DISPLACEMENT_RE = re.compile(
    r"(\d+\.\d+)\s*l?\b|\b(\d+)\s*(?:l|liter|litre|liters|litres)\b",
    re.IGNORECASE,
)


def _match_keyword(value: Any, table: Tuple[Tuple[str, str], ...]) -> Optional[str]:
    if value is None:
        return None
    low = str(value).strip().lower()
    if not low:
        return None
    for needle, canonical in table:
        if needle in low:
            return canonical
    return None


def normalize_body_type(value: Any) -> Any:
    """Map a sourced body label to a canonical Title Case singular form.

    A trim/engine suffix ("Turismo Cabrio") is dropped — only the body keyword
    survives. Unrecognized labels are returned unchanged so the validator can
    still surface them rather than silently dropping grounded data.
    """
    canonical = _match_keyword(value, _BODY_TYPE_KEYWORDS)
    return canonical if canonical is not None else value


def normalize_fuel_type(value: Any) -> Any:
    canonical = _match_keyword(value, _FUEL_TYPE_KEYWORDS)
    return canonical if canonical is not None else value


def normalize_drivetrain(value: Any) -> Any:
    canonical = _match_keyword(value, _DRIVETRAIN_KEYWORDS)
    return canonical if canonical is not None else value


def normalize_transmission(value: Any) -> Any:
    """Map to a base transmission type, keeping a sourced "N-speed" prefix."""
    if value is None:
        return None
    base = _match_keyword(value, _TRANSMISSION_KEYWORDS)
    if base is None:
        return value
    speed = _SPEED_RE.search(str(value))
    if speed:
        return f"{speed.group(1)}-speed {base}"
    return base


def normalize_engine(value: Any, fuel_type: Any = None) -> Any:
    """Canonical engine string: "<displacement>L <aspiration?> <config?>".

    Always includes the "L" suffix on the displacement, lowercases descriptors,
    drops fuel words, and collapses an electric powertrain to "electric".
    """
    fuel_low = str(fuel_type).strip().lower() if fuel_type is not None else ""
    if value is None:
        return "electric" if fuel_low in _EV_FUELS else None

    text = str(value).strip()
    low = text.lower()
    if "electric" in low or low in {"ev", "bev"} or fuel_low in _EV_FUELS:
        return "electric"

    low = _FUEL_WORDS_RE.sub(" ", low)
    match = _DISPLACEMENT_RE.search(low)
    displacement = None
    if match:
        displacement = match.group(1) or match.group(2)
        low = low[: match.start()] + " " + low[match.end():]

    tokens = [
        tok
        for tok in re.split(r"[\s,]+", low)
        if tok and tok not in {"l", "liter", "litre", "liters", "litres"}
    ]
    descriptor = " ".join(tokens)

    if displacement is not None:
        result = f"{displacement}L"
        if descriptor:
            result += f" {descriptor}"
        return result
    return descriptor or text.lower()


# ---------------------------------------------------------------------------
# support_level invariant
# ---------------------------------------------------------------------------

# Technical fields that, when present and grounded, count toward "direct".
_GROUNDED_FIELDS = (
    "version_or_trim",
    "body_type",
    "fuel_type",
    "engine",
    "engine_displacement_l",
    "horsepower_hp",
    "transmission",
    "drivetrain",
    "year_start",
    "year_end",
)


def normalize_support_level(variant: Dict[str, Any]) -> Any:
    """Enforce the support_level logical invariant.

    ``indirect`` is valid ONLY if at least one non-null field lacks direct
    grounding (i.e. was inferred). When every non-null technical field is
    directly grounded via ``field_sources`` AND ``missing_grounded_fields`` is
    empty, a fully-grounded complete row marked ``indirect`` is corrected to
    ``direct``. Other values (direct / unknown / conflict) are left untouched.
    """
    support = variant.get("support_level")
    if support != "indirect":
        return support

    missing = variant.get("missing_grounded_fields") or []
    if isinstance(missing, list) and missing:
        return "indirect"  # something was not directly grounded — keep indirect

    field_sources = variant.get("field_sources")
    if not isinstance(field_sources, dict):
        return "indirect"

    for fname in _GROUNDED_FIELDS:
        if variant.get(fname) in (None, ""):
            continue
        refs = field_sources.get(fname)
        if not (isinstance(refs, list) and refs):
            # A non-null field with no direct source — genuinely indirect.
            return "indirect"

    # Fully grounded and complete: must be direct.
    return "direct"


def normalize_variant(variant: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``variant`` with canonical technical values applied."""
    if not isinstance(variant, dict):
        return variant
    out = dict(variant)
    out["body_type"] = normalize_body_type(out.get("body_type"))
    out["fuel_type"] = normalize_fuel_type(out.get("fuel_type"))
    out["transmission"] = normalize_transmission(out.get("transmission"))
    out["drivetrain"] = normalize_drivetrain(out.get("drivetrain"))
    out["engine"] = normalize_engine(out.get("engine"), out.get("fuel_type"))
    out["support_level"] = normalize_support_level(out)
    return out


# ---------------------------------------------------------------------------
# Year-only variant merging
# ---------------------------------------------------------------------------

# Configurations identical across these fields are the SAME variant; a year
# boundary alone must not split them into separate rows. version_or_trim is
# included so two genuinely distinct trims that happen to share an engine are
# never collapsed (which would drop a website-selectable option).
_MERGE_KEYS = (
    "version_or_trim",
    "body_type",
    "fuel_type",
    "engine",
    "horsepower_hp",
    "transmission",
    "drivetrain",
)


def _merge_key(variant: Dict[str, Any]) -> Tuple:
    return tuple(
        str(variant.get(k)).strip().lower() if variant.get(k) is not None else None
        for k in _MERGE_KEYS
    )


def _union_list(existing: Any, incoming: Any) -> List[Any]:
    out = list(existing) if isinstance(existing, list) else []
    for item in incoming if isinstance(incoming, list) else []:
        if item not in out:
            out.append(item)
    return out


def _merge_into(target: Dict[str, Any], other: Dict[str, Any]) -> None:
    starts = [
        y for y in (target.get("year_start"), other.get("year_start"))
        if isinstance(y, int)
    ]
    if starts:
        target["year_start"] = min(starts)

    ends = (target.get("year_end"), other.get("year_end"))
    if None in ends:
        target["year_end"] = None  # an open-ended period keeps the range open
    else:
        end_years = [y for y in ends if isinstance(y, int)]
        if end_years:
            target["year_end"] = max(end_years)

    target["source_indexes"] = _union_list(
        target.get("source_indexes"), other.get("source_indexes")
    )

    target_fs = dict(target.get("field_sources") or {})
    for fname, refs in (other.get("field_sources") or {}).items():
        target_fs[fname] = _union_list(target_fs.get(fname), refs)
    if target_fs:
        target["field_sources"] = target_fs

    # A field is missing only if it was missing in every merged period.
    tm = set(target.get("missing_grounded_fields") or [])
    om = set(other.get("missing_grounded_fields") or [])
    target["missing_grounded_fields"] = sorted(tm & om)

    if other.get("support_level") == "direct":
        target["support_level"] = "direct"


def merge_year_variants(
    variants: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], int]:
    """Merge rows that differ only by year into one row spanning the range.

    Rows are merged only when all merge-key fields are non-null and equal; a
    row missing any merge-key field is left untouched (we cannot prove it is
    the same configuration). Returns ``(merged_variants, merged_count)``.
    """
    merged: List[Dict[str, Any]] = []
    index: Dict[Tuple, Dict[str, Any]] = {}
    merged_count = 0

    for variant in variants:
        if not isinstance(variant, dict) or any(
            variant.get(k) in (None, "") for k in _MERGE_KEYS
        ):
            merged.append(variant)
            continue
        key = _merge_key(variant)
        if key in index:
            _merge_into(index[key], variant)
            merged_count += 1
        else:
            row = dict(variant)
            index[key] = row
            merged.append(row)

    return merged, merged_count
