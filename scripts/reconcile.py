"""Deterministic audit post-processing for validated rows.

This module runs *after* Gemini returns JSON. It only cleans and reconciles the
output — it NEVER rejects a row and NEVER makes acceptance stricter. The core
acceptance policy (valid identity + weak/missing trim -> ``clean_partial``) is
left completely untouched here.

Responsibilities (cleanup only):

1. Populate ``fields_changed`` when an output field meaningfully differs from
   the source variant (e.g. ``year_start`` 2008 -> 2010).
2. Drop fields from ``fields_left_unresolved`` once they are filled/usable.
3. Keep ``acceptance_tier`` consistent with ``validation_decision``.
4. Keep ``trim_status`` consistent with ``canonical_trim``.
5. Normalize ``evidence_sources`` into structured, audit-friendly objects.
6. Trim obviously unsupported (placeholder) ``possible_trim_names`` candidates.
7. Strip any mock marker from real output.
8. Post-processing guards from v2 prompt spec (slash trim, under-consideration,
   year_end normalization, source_type classification, trim-only reject guard).

None of these steps may convert ``clean_partial`` into ``reject``.
"""

from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .data_loader import get_standard
from .normalization import is_weak_trim, norm_str, norm_year
from .output_writer import DECISION_TIER, enforce_consistency
from .run_paths import MOCK_GROUNDING_SENTINEL

# Output field -> source (standard) field. These are the fields whose value
# changes we audit and, where relevant, reconcile.
_OUTPUT_TO_SOURCE = {
    "canonical_make": "make",
    "canonical_model": "model",
    "canonical_series_or_generation": "generation",
    "canonical_trim": "trim",
    "official_marketed_name_il": "official_marketed_name_il",
    "body_type": "body_type",
    "fuel_type": "fuel_type",
    "engine": "engine",
    "transmission": "transmission",
    "drivetrain": "drivetrain",
    "year_start": "year_start",
    "year_end": "year_end",
    "market_scope": "market_scope",
}

_YEAR_FIELDS = {"year_start", "year_end"}

# Output fields that should be removed from ``fields_left_unresolved`` once they
# hold a non-null value (they are then treated as resolved/usable).
_RESOLVE_WHEN_FILLED = (
    "official_marketed_name_il",
    "engine",
    "transmission",
    "fuel_type",
    "body_type",
    "year_start",
    "year_end",
    "canonical_trim",
)

_CHANGE_REASON = (
    "Model changed value during validation; see decision_reason/grounding_summary"
)


@dataclass
class GuardFlag:
    guard_name: str
    original_decision: str | None
    new_decision: str | None
    field_affected: str
    reason: str
    needs_adjudication: bool

NEEDS_ADJUDICATION = {
    "slash_trim",
    "grounding_summary_vs_decision",
    "under_consideration",
    "domain_500c_transmission",
}

NO_ADJUDICATION_NEEDED = {
    "normalize_evidence_sources",
    "classify_source_types",
    "generic_trim",
    "year_end_current",
    "official_name_unresolved",
    "no_reject_without_blocking_issue",
    "acceptance_tier_sync",
}

def _add_flag(flags, name, old, new, field, reason):
    flags.append(GuardFlag(name, old, new, field, reason, name in NEEDS_ADJUDICATION))

def _add_issue(row, msg):
    issues = row.get("non_blocking_trim_issues")
    if not isinstance(issues, list):
        issues = []
        row["non_blocking_trim_issues"] = issues
    if msg not in issues:
        issues.append(msg)


def _normalize_for_compare(field: str, value: Any) -> Any:
    """Normalize a value so source/output comparison is meaningful."""
    if field in _YEAR_FIELDS:
        return norm_year(value)
    s = norm_str(value)
    return s.lower() if isinstance(s, str) else s


def _audit_field_changes(
    source_std: Dict[str, Any], row: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Append change records for fields whose value meaningfully differs.

    A *change* is only recorded when the source already carried a value and the
    output differs from it. Pure fills (source empty -> output value) are
    enrichment, not changes, and are handled by the unresolved cleanup instead.
    """
    existing = row.get("fields_changed")
    if not isinstance(existing, list):
        existing = []
    already_tracked = {
        e.get("field") for e in existing if isinstance(e, dict) and e.get("field")
    }

    changes: List[Dict[str, Any]] = list(existing)
    for out_field, src_field in _OUTPUT_TO_SOURCE.items():
        if out_field in already_tracked:
            continue
        src_raw = source_std.get(src_field)
        out_raw = row.get(out_field)
        src_cmp = _normalize_for_compare(out_field, src_raw)
        out_cmp = _normalize_for_compare(out_field, out_raw)
        if src_cmp in (None, "") or out_cmp in (None, ""):
            continue
        if src_cmp == out_cmp:
            continue
        from_val = norm_year(src_raw) if out_field in _YEAR_FIELDS else norm_str(src_raw)
        to_val = norm_year(out_raw) if out_field in _YEAR_FIELDS else row.get(out_field)
        changes.append(
            {
                "field": out_field,
                "from": from_val,
                "to": to_val,
                "reason": _CHANGE_REASON,
            }
        )
    return changes


def _clean_unresolved(row: Dict[str, Any]) -> List[str]:
    """Remove filled/usable fields from ``fields_left_unresolved``.

    ``canonical_trim`` stays unresolved only when it is null AND
    ``trim_status`` is ``unresolved`` — cleanup, never a rejection.
    """
    unresolved = row.get("fields_left_unresolved")
    if not isinstance(unresolved, list):
        return []

    cleaned: List[str] = []
    seen: set = set()
    for field in unresolved:
        if not isinstance(field, str) or field in seen:
            continue
        seen.add(field)
        if field in _RESOLVE_WHEN_FILLED and row.get(field) not in (None, "", []):
            continue
        if field == "canonical_trim":
            if row.get("canonical_trim") in (None, "", []) and row.get(
                "trim_status"
            ) == "unresolved":
                cleaned.append(field)
            continue
        cleaned.append(field)
    return cleaned


def _reconcile_trim_status(row: Dict[str, Any]) -> str:
    """Keep ``trim_status`` consistent with ``canonical_trim`` (no rejection)."""
    trim_status = row.get("trim_status")
    canonical_trim = row.get("canonical_trim")
    if trim_status == "invalid":
        return trim_status
    has_trim = canonical_trim not in (None, "", [])
    if not has_trim and trim_status in ("verified", "inferred"):
        return "unresolved"
    if has_trim and trim_status == "unresolved":
        return "inferred"
    return trim_status


_DOMAIN_RE = re.compile(r"^[\w-]+(?:\.[\w-]+)+$")
_URL_RE = re.compile(r"https?://\S+")


def _looks_like_domain(token: str) -> bool:
    return bool(_DOMAIN_RE.match(token))


def _normalize_evidence_source(item: Any) -> Optional[Dict[str, Any]]:
    """Coerce one evidence source into a structured, audit-friendly object."""
    if isinstance(item, dict):
        url = item.get("url")
        source_name = item.get("source_name")
        if not source_name and isinstance(url, str):
            m = _URL_RE.search(url)
            host = re.sub(r"^https?://", "", url).split("/")[0] if m else None
            source_name = host or None
        supports = item.get("supports")
        if not isinstance(supports, list):
            supports = []
        title = item.get("title") or item.get("name") or (url if isinstance(url, str) else "")
        raw_type = item.get("source_type") or "unknown"
        classified = classify_source_type(source_name or "", url or "", title or "")
        source_type = classified if classified != "unknown" else raw_type
        return {
            "title": title,
            "url": url if isinstance(url, str) else None,
            "source_name": source_name,
            "source_type": source_type,
            "supports": supports,
        }

    if isinstance(item, str):
        text = item.strip()
        if not text:
            return None
        tokens = text.split()
        url_match = _URL_RE.search(text)
        url = url_match.group(0) if url_match else None
        source_name = None
        if url:
            source_name = re.sub(r"^https?://", "", url).split("/")[0] or None
        elif tokens and _looks_like_domain(tokens[0]):
            source_name = tokens[0]
        source_type = classify_source_type(source_name or "", url or "", text)
        return {
            "title": text,
            "url": url,
            "source_name": source_name,
            "source_type": source_type,
            "supports": [],
        }

    if item is None:
        return None
    return {
        "title": str(item),
        "url": None,
        "source_name": None,
        "source_type": "unknown",
        "supports": [],
    }


def _normalize_evidence_sources(sources: Any) -> List[Dict[str, Any]]:
    if not isinstance(sources, list):
        return []
    normalized: List[Dict[str, Any]] = []
    for item in sources:
        obj = _normalize_evidence_source(item)
        if obj is not None:
            normalized.append(obj)
    return normalized


def _clean_possible_trim_names(names: Any) -> List[Any]:
    """Drop empty/placeholder (weak) candidates; keep real ones, preserve order."""
    if not isinstance(names, list):
        return []
    cleaned: List[Any] = []
    seen: set = set()
    for item in names:
        if isinstance(item, dict):
            cleaned.append(item)
            continue
        s = norm_str(item)
        if s is None or is_weak_trim(s):
            continue
        key = s.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(s)
    return cleaned


def _strip_mock_marker(row: Dict[str, Any]) -> None:
    """Ensure no mock grounding sentinel survives in real output."""
    if row.get("grounding_summary") == MOCK_GROUNDING_SENTINEL:
        row["grounding_summary"] = ""
    sources = row.get("evidence_sources")
    if isinstance(sources, list):
        row["evidence_sources"] = [
            s for s in sources if s != MOCK_GROUNDING_SENTINEL
        ]


# ---------------------------------------------------------------------------
# v3 post-processing guards
# ---------------------------------------------------------------------------

_SLASH_SEPARATORS = ["/", "|", " or ", " and "]
_GENERIC_TRIMS = {"base", "standard", "basic", "default", "regular", "entry", "n/a", "na", "none", "null", "בסיס", "סטנדרט"}
_UNDER_CONSIDERATION_PHRASES = [
    "under consideration", "expected to arrive", "may arrive", "importer is evaluating",
    "not yet launched", "being evaluated", "could arrive", "might be imported",
    "לא הושק", "בשלב בחינה", "צפוי להגיע",
]
_SPLIT_PHRASES = ["split is required", "must be split", "should be split", "requires splitting", "different power outputs", "distinct trims"]
_CURRENT_PHRASES = ["still current", "available", "launched recently", "currently sold", "currently produced", "imported now", "still imported"]

SOURCE_TYPE_KEYWORDS = {
    "official_importer": ["abarth.co.il", "samelet.co.il", "kolmemotors", "colmobil", "importer", "סמלת"],
    "manufacturer": ["abarth.com", "fiat.com", "stellantis.com"],
    "marketplace": ["yad2", "autoboom", "wisecars", "ad.co.il", "lomoto"],
    "editorial": ["icar", "auto.co.il", "cartube", "gear.co.il", "wheel.co.il", "thecar", "over-drive", "walla", "sport5", "ynet", "mako", "car-pad", "queen of road"],
    "government": ["data.gov.il", "transport ministry", "משרד התחבורה", "רשות הרישוי"],
    "forum_community": ["forum", "community", "reddit"],
}

def classify_source_type(source_name: str, url: str, title: str = "") -> str:
    text = " ".join(str(x or "").lower() for x in (source_name, url, title))
    for stype in ("official_importer", "manufacturer", "marketplace", "editorial", "government", "forum_community"):
        if any(k.lower() in text for k in SOURCE_TYPE_KEYWORDS[stype]):
            return stype
    return "unknown"

def _has_combined_trim(trim: Any) -> bool:
    if not isinstance(trim, str) or not trim.strip():
        return False
    low = f" {trim.lower()} "
    return any(sep in low for sep in _SLASH_SEPARATORS) or ("," in trim and len([p for p in trim.split(",") if p.strip()]) > 1)

def _summary_wants_split(summary: str) -> bool:
    low = (summary or "").lower()
    return any(p in low for p in _SPLIT_PHRASES)

def _prefer_split(row):
    return bool(row.get("split_candidates")) or _summary_wants_split(row.get("grounding_summary", ""))

def _apply_v3_guards(row: Dict[str, Any], flags: List[GuardFlag]) -> None:
    trim = row.get("canonical_trim")
    if isinstance(trim, str) and trim.strip().lower() in _GENERIC_TRIMS:
        old = row.get("validation_decision")
        row["canonical_trim"] = None; row["trim_status"] = "unresolved"; row["trim_confidence"] = 0.0
        if old == "clean_exact": row["validation_decision"] = "clean_partial"
        _add_issue(row, f"Trim '{trim}' is a generic placeholder; reset to null/unresolved.")
        _add_flag(flags, "generic_trim", old, row.get("validation_decision"), "canonical_trim", "Generic trim reset to unresolved.")

    if _has_combined_trim(row.get("canonical_trim")) and row.get("validation_decision") == "clean_exact":
        old = row.get("validation_decision")
        row["validation_decision"] = "split_required" if _prefer_split(row) else "clean_partial"
        _add_issue(row, "Slash/combined trim cannot be clean_exact.")
        _add_flag(flags, "slash_trim", old, row.get("validation_decision"), "validation_decision", "Slash/combined trim cannot be clean_exact.")

    if row.get("validation_decision") == "clean_exact" and _summary_wants_split(row.get("grounding_summary", "")):
        old = row.get("validation_decision")
        row["validation_decision"] = "split_required" if any(p in (row.get("grounding_summary") or "").lower() for p in ["different power outputs", "distinct trims", "split is required", "must be split"]) else "clean_partial"
        _add_issue(row, "Grounding summary conflicts with clean_exact decision.")
        _add_flag(flags, "grounding_summary_vs_decision", old, row.get("validation_decision"), "validation_decision", "Grounding summary indicates split/partial, not clean_exact.")

    if row.get("validation_decision") == "clean_exact" and any(p in (row.get("grounding_summary") or "").lower() for p in _UNDER_CONSIDERATION_PHRASES):
        old = row.get("validation_decision")
        row["validation_decision"] = "clean_partial"; row["identity_status"] = "likely_valid"; row["is_currently_imported_il"] = None
        _add_issue(row, "Israeli market sale/import not fully verified; source indicates expected or under consideration.")
        _add_flag(flags, "under_consideration", old, "clean_partial", "validation_decision", "Only expected/under consideration market status found.")

    cur = datetime.datetime.now(datetime.timezone.utc).year
    ye = row.get("year_end")
    if isinstance(ye, int) and ye >= cur:
        summary = (row.get("grounding_summary") or "").lower()
        if row.get("is_currently_produced") is True or row.get("is_currently_imported_il") is True or any(p in summary for p in _CURRENT_PHRASES):
            row["year_end"] = None
            _add_flag(flags, "year_end_current", None, None, "year_end", "Current/future year_end reset to null for active vehicle.")
        else:
            _add_issue(row, "year_end is current/future; verify it is not a placeholder for active production/import.")

    make = str(row.get("canonical_make") or "").lower(); model = str(row.get("canonical_model") or "").lower()
    body = str(row.get("body_type") or "").lower(); trim_s = str(row.get("canonical_trim") or "").lower(); trans = str(row.get("transmission") or "").lower()
    is_500c = make == "abarth" and (model in {"500", "500c"} or "500c" in (model+body+trim_s)) and any(x in body+model+trim_s for x in ["cabrio", "convertible", "500c"])
    if is_500c and trim_s in {"500c", "cabrio", "cabriolet", "convertible"}:
        row["canonical_trim"] = None; row["trim_status"] = "unresolved"; row["trim_confidence"] = 0.0
        _add_issue(row, "500C/Cabriolet is a body/model designation, not a verified trim.")
        _add_flag(flags, "generic_trim", None, None, "canonical_trim", "500C/Cabriolet trim cleanup.")
    if is_500c and "manual" in trans and row.get("identity_status") == "verified":
        old = row.get("validation_decision")
        row["identity_status"] = "likely_valid"; row["identity_confidence"] = min(float(row.get("identity_confidence") or 0.7), 0.7); row["validation_decision"] = "clean_partial"
        _add_issue(row, "Abarth 500C/Cabriolet manual transmission is not verified for the Israeli market; local sources indicate robotic/automated-manual only.")
        _add_flag(flags, "domain_500c_transmission", old, "clean_partial", "identity_status", "Manual transmission not verified for Israeli Abarth 500C/Cabriolet.")

    if row.get("validation_decision") == "reject" and not row.get("blocking_identity_issues"):
        old = row.get("validation_decision")
        row["validation_decision"] = "clean_partial"
        _add_issue(row, "Reject downgraded to clean_partial: no blocking identity issue found.")
        _add_flag(flags, "no_reject_without_blocking_issue", old, "clean_partial", "validation_decision", "Reject without blocking identity issue downgraded.")

    unresolved = row.get("fields_left_unresolved") if isinstance(row.get("fields_left_unresolved"), list) else []
    if row.get("official_marketed_name_il") not in (None, "", []):
        row["fields_left_unresolved"] = [f for f in unresolved if f != "official_marketed_name_il"]
    elif row.get("identity_status") in {"verified", "likely_valid"} and "official_marketed_name_il" not in unresolved:
        unresolved.append("official_marketed_name_il"); row["fields_left_unresolved"] = unresolved

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def reconcile_validation_output_with_flags(
    source_variant: Dict[str, Any],
    model_output: Dict[str, Any],
    *,
    run_mode: str = "real",
    final_pass: bool = False,
) -> Tuple[Dict[str, Any], List[GuardFlag]]:
    """Deterministically clean & reconcile a validated row and return guard flags."""
    flags: List[GuardFlag] = []
    row = dict(model_output)
    source_std = get_standard(source_variant or {})

    if run_mode != "mock":
        _strip_mock_marker(row)

    row["fields_changed"] = _audit_field_changes(source_std, row)
    row["trim_status"] = _reconcile_trim_status(row)
    row["fields_left_unresolved"] = _clean_unresolved(row)
    before_sources = row.get("evidence_sources")
    row["evidence_sources"] = _normalize_evidence_sources(before_sources)
    row["possible_trim_names"] = _clean_possible_trim_names(row.get("possible_trim_names"))

    _apply_v3_guards(row, flags)

    before_decision = row.get("validation_decision")
    row = enforce_consistency(row)
    if before_decision != row.get("validation_decision"):
        _add_flag(flags, "acceptance_tier_sync", before_decision, row.get("validation_decision"), "validation_decision", "Decision/tier consistency enforced.")
    decision = row.get("validation_decision")
    if decision in DECISION_TIER:
        row["acceptance_tier"] = DECISION_TIER[decision]
    return row, flags

def reconcile_validation_output(
    source_variant: Dict[str, Any],
    model_output: Dict[str, Any],
    *,
    run_mode: str = "real",
) -> Dict[str, Any]:
    """Backwards-compatible deterministic cleanup API."""
    row, _flags = reconcile_validation_output_with_flags(source_variant, model_output, run_mode=run_mode)
    return row
