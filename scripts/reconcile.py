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

None of these steps may convert ``clean_partial`` into ``reject``.
"""

from __future__ import annotations

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
        # Only a genuine value->value modification counts as a change. Pure
        # clears (value -> empty) are unresolved fields, not changes, and pure
        # fills (empty -> value) are enrichment handled by unresolved cleanup.
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
            # Field is filled -> treat as resolved, drop it.
            continue
        if field == "canonical_trim":
            # Keep only if genuinely unresolved (null trim + unresolved status).
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
    # Never touch an explicit invalid trim verdict.
    if trim_status == "invalid":
        return trim_status
    has_trim = canonical_trim not in (None, "", [])
    if not has_trim and trim_status in ("verified", "inferred"):
        # No concrete trim but status claims one — relax to unresolved.
        return "unresolved"
    if has_trim and trim_status == "unresolved":
        # A concrete trim is present — at least inferred.
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
        return {
            "title": title,
            "url": url if isinstance(url, str) else None,
            "source_name": source_name,
            "source_type": item.get("source_type") or "unknown",
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
        return {
            "title": text,
            "url": url,
            "source_name": source_name,
            "source_type": "unknown",
            "supports": [],
        }

    # Unknown shape — preserve as a title string rather than dropping evidence.
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
    """Drop empty/placeholder (weak) candidates; keep real ones, preserve order.

    This is cleanup only: dict-shaped candidates are preserved untouched, and we
    never empty the list just because evidence is imperfect — only obvious
    placeholder/blank strings are removed.
    """
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

    # 6. No mock marker in real output (mock rows keep their sentinel).
    if run_mode != "mock":
        _strip_mock_marker(row)

    # 2. Track actual field changes.
    row["fields_changed"] = _audit_field_changes(source_std, row)

    # 5. trim_status consistent with canonical_trim (before unresolved cleanup).
    row["trim_status"] = _reconcile_trim_status(row)

    # 3. fields_left_unresolved must not contradict filled fields.
    row["fields_left_unresolved"] = _clean_unresolved(row)

    # 4. Structured evidence sources.
    row["evidence_sources"] = _normalize_evidence_sources(row.get("evidence_sources"))

    # possible_trim_names cleanup (no stricter filtering of the row itself).
    row["possible_trim_names"] = _clean_possible_trim_names(row.get("possible_trim_names"))

    # 7. Never convert clean_partial -> reject. We never set 'reject' here; we
    # only re-assert tier/decision coherence via enforce_consistency, which
    # maps the existing decision to its tier without changing the decision.
    row = enforce_consistency(row)
    # Defensive: acceptance_tier must equal the decision's tier.
    decision = row.get("validation_decision")
    if decision in DECISION_TIER:
        row["acceptance_tier"] = DECISION_TIER[decision]
    return row
