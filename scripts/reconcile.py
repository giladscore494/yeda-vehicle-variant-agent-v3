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
from typing import Any, Dict, List, Optional

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
        classified = classify_source_type(source_name or "", url or "")
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
        source_type = classify_source_type(source_name or "", url or "")
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
# v2 post-processing guards
# ---------------------------------------------------------------------------

_SLASH_SEPARATORS = ["/", "|", " or ", " and "]

_UNDER_CONSIDERATION_PHRASES = [
    "under consideration",
    "expected to arrive",
    "may arrive",
    "importer is evaluating",
    "not yet launched",
    "being evaluated",
]

SOURCE_TYPE_MAP = {
    "abarth.co.il": "official_importer",
    "samelet.co.il": "official_importer",
    "abarth.com": "manufacturer",
    "fiat.com": "manufacturer",
    "yad2.co.il": "marketplace",
    "autoboom.co.il": "marketplace",
    "wisecars.co.il": "marketplace",
    "cartube.co.il": "marketplace",
    "icar.co.il": "editorial",
    "auto.co.il": "editorial",
    "gear.co.il": "editorial",
    "wheel.co.il": "editorial",
    "thecar.co.il": "editorial",
    "over-drive.co.il": "editorial",
    "data.gov.il": "government",
}


def classify_source_type(source_name: str, url: str) -> str:
    """Classify an evidence source into a source_type category."""
    name_lower = (source_name or "").lower()
    url_lower = (url or "").lower()
    for domain, stype in SOURCE_TYPE_MAP.items():
        if domain in name_lower or domain in url_lower:
            return stype
    if any(x in name_lower for x in ["yad2", "autoboom", "wisecars"]):
        return "marketplace"
    if any(x in name_lower for x in [
        "icar", "cartube", "gear", "auto.co", "wheel", "thecar",
        "walla", "sport5", "ynet", "over-drive",
    ]):
        return "editorial"
    if any(x in name_lower for x in ["data.gov", "transport ministry", "משרד התחבורה"]):
        return "government"
    if any(x in name_lower for x in ["forum", "community", "reddit"]):
        return "forum_community"
    return "unknown"


def _guard_slash_trim(row: Dict[str, Any]) -> None:
    """Slash/combined trim → cannot be clean_exact."""
    if row["validation_decision"] != "clean_exact":
        return
    trim = row.get("canonical_trim") or ""
    if any(sep in trim for sep in _SLASH_SEPARATORS):
        row["validation_decision"] = "clean_partial"
        row["acceptance_tier"] = "partial"
        issues = row.get("non_blocking_trim_issues")
        if not isinstance(issues, list):
            issues = []
            row["non_blocking_trim_issues"] = issues
        issues.append(
            "Slash/combined trim detected; downgraded from clean_exact to clean_partial."
        )


def _guard_under_consideration(row: Dict[str, Any]) -> None:
    """Under-consideration language → cannot be clean_exact."""
    if row["validation_decision"] != "clean_exact":
        return
    summary = (row.get("grounding_summary") or "").lower()
    if any(phrase in summary for phrase in _UNDER_CONSIDERATION_PHRASES):
        row["validation_decision"] = "clean_partial"
        row["acceptance_tier"] = "partial"
        row["identity_status"] = "likely_valid"
        row["is_currently_imported_il"] = None
        issues = row.get("non_blocking_trim_issues")
        if not isinstance(issues, list):
            issues = []
            row["non_blocking_trim_issues"] = issues
        issues.append(
            "Israeli market sale/import not fully verified; source indicates expected or under consideration."
        )


def _guard_year_end(row: Dict[str, Any]) -> None:
    """year_end normalization: still-active vehicles must not have a current/future year_end."""
    if row.get("is_currently_produced") is True or row.get("is_currently_imported_il") is True:
        current_year = datetime.datetime.now(datetime.timezone.utc).year
        if row.get("year_end") and row["year_end"] >= current_year:
            row["year_end"] = None


def _guard_trim_only_reject(row: Dict[str, Any]) -> None:
    """Trim-only uncertainty never becomes reject."""
    if row["validation_decision"] != "reject":
        return
    has_blocking_identity = bool(row.get("blocking_identity_issues"))
    if not has_blocking_identity:
        row["validation_decision"] = "clean_partial"
        row["acceptance_tier"] = "partial"
        issues = row.get("non_blocking_trim_issues")
        if not isinstance(issues, list):
            issues = []
            row["non_blocking_trim_issues"] = issues
        issues.append(
            "Reject downgraded to clean_partial: no blocking identity issue found."
        )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def reconcile_validation_output(
    source_variant: Dict[str, Any],
    model_output: Dict[str, Any],
    *,
    run_mode: str = "real",
) -> Dict[str, Any]:
    """Deterministically clean & reconcile a validated row.

    Never rejects, never tightens acceptance. Returns the same row, cleaned.
    """
    row = dict(model_output)
    source_std = get_standard(source_variant or {})

    if run_mode != "mock":
        _strip_mock_marker(row)

    row["fields_changed"] = _audit_field_changes(source_std, row)
    row["trim_status"] = _reconcile_trim_status(row)
    row["fields_left_unresolved"] = _clean_unresolved(row)
    row["evidence_sources"] = _normalize_evidence_sources(row.get("evidence_sources"))
    row["possible_trim_names"] = _clean_possible_trim_names(row.get("possible_trim_names"))

    # v2 post-processing guards (deterministic, applied after every Gemini response)
    _guard_slash_trim(row)
    _guard_under_consideration(row)
    _guard_year_end(row)
    _guard_trim_only_reject(row)

    row = enforce_consistency(row)
    decision = row.get("validation_decision")
    if decision in DECISION_TIER:
        row["acceptance_tier"] = DECISION_TIER[decision]
    return row
