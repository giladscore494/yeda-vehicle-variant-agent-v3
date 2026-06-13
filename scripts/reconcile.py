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
from dataclasses import dataclass, field
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
    severity: str
    field_affected: str
    original_value: Any
    guard_value: Any
    reason: str
    needs_adjudication: bool = False
    recommended_verifier_model: str = "none"
    allowed_decisions: List[str] = field(default_factory=list)
    allowed_patch_fields: List[str] = field(default_factory=list)
    risk_tags: List[str] = field(default_factory=list)

    @property
    def original_decision(self) -> Any:  # backwards-compatible test/API alias
        return self.original_value

    @property
    def new_decision(self) -> Any:  # backwards-compatible test/API alias
        return self.guard_value

NEEDS_ADJUDICATION = {
    "slash_trim",
    "grounding_summary_vs_decision",
    "under_consideration",
    "domain_500c_transmission",
    "year_start_il_market",
    "market_year_conflict",
    "current_status_conflict",
    "decision_reason_conflict",
    "identity_confidence_downgrade",
    "technical_unresolved_publishability",
}

NO_ADJUDICATION_NEEDED = {
    "normalize_evidence_sources",
    "classify_source_types",
    "generic_trim",
    "year_end_current",
    "year_start_il_market",
    "official_name_unresolved",
    "no_reject_without_blocking_issue",
    "acceptance_tier_sync",
}

_ALLOWED_DECISIONS_BY_GUARD = {
    "slash_trim": ["split_required", "clean_partial"],
    "grounding_summary_vs_decision": ["split_required", "clean_partial"],
    "under_consideration": ["clean_exact", "clean_partial"],
    "domain_500c_transmission": ["clean_exact", "clean_partial"],
    "year_start_il_market": ["clean_exact", "clean_partial"],
    "market_year_conflict": ["clean_exact", "clean_partial"],
    "current_status_conflict": ["clean_exact", "clean_partial"],
    "decision_reason_conflict": ["clean_exact", "clean_partial", "split_required"],
    "identity_confidence_downgrade": ["clean_exact", "clean_partial"],
    "technical_unresolved_publishability": ["clean_partial"],
    "clean_catalog_safety": ["clean_partial"],
    "no_clean_exact_unresolved": ["clean_partial", "split_required"],
    "unresolved_field_sync": ["clean_exact", "clean_partial"],
    "split_issue_blocking_identity": ["split_required", "clean_partial"],
    "source_classification_risk": ["clean_exact", "clean_partial", "split_required"],
}


_ALLOWED_PATCH_FIELDS_BY_GUARD = {
    "slash_trim": ["validation_decision", "trim_status", "trim_confidence", "canonical_trim"],
    "grounding_summary_vs_decision": ["validation_decision", "identity_status", "identity_confidence", "trim_status"],
    "under_consideration": ["validation_decision", "identity_status", "identity_confidence", "is_currently_imported_il"],
    "domain_500c_transmission": ["validation_decision", "identity_status", "identity_confidence", "fields_left_unresolved"],
    "year_start_il_market": ["year_start", "validation_decision", "identity_status", "identity_confidence"],
    "market_year_conflict": ["year_start", "year_end", "validation_decision", "identity_status", "identity_confidence"],
    "current_status_conflict": ["year_end", "is_currently_produced", "is_currently_imported_il", "validation_decision"],
    "decision_reason_conflict": ["validation_decision", "identity_status", "identity_confidence", "fields_left_unresolved"],
    "identity_confidence_downgrade": ["identity_status", "identity_confidence", "validation_decision"],
    "technical_unresolved_publishability": ["validation_decision", "identity_status", "identity_confidence", "fields_left_unresolved"],
    "clean_catalog_safety": ["validation_decision", "identity_status", "identity_confidence", "fields_left_unresolved"],
    "no_clean_exact_unresolved": ["validation_decision", "identity_status", "identity_confidence", "trim_status", "trim_confidence", "canonical_trim"],
    "unresolved_field_sync": ["fields_left_unresolved", "identity_status", "identity_confidence", "validation_decision"],
    "split_issue_blocking_identity": ["blocking_identity_issues", "non_blocking_trim_issues", "validation_decision"],
    "source_classification_risk": ["evidence_sources"],
}


def _add_flag(flags, name, old, new, field, reason, severity="medium", risk_tags=None):
    needs = name in NEEDS_ADJUDICATION or severity in {"high", "critical"}
    flags.append(GuardFlag(
        guard_name=name,
        severity=severity,
        field_affected=field,
        original_value=old,
        guard_value=new,
        reason=reason,
        needs_adjudication=needs,
        recommended_verifier_model="gpt-5.4" if needs else "none",
        allowed_decisions=list(_ALLOWED_DECISIONS_BY_GUARD.get(name, [])),
        allowed_patch_fields=list(_ALLOWED_PATCH_FIELDS_BY_GUARD.get(name, [])),
        risk_tags=list(risk_tags or []),
    ))

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
    normalized_existing: List[Dict[str, Any]] = []
    for item in existing:
        if isinstance(item, dict) and item.get("field"):
            normalized_existing.append(item)
        elif isinstance(item, str):
            normalized_existing.append({"field": item, "from": None, "to": None, "reason": "Legacy string change normalized by guard."})
    already_tracked = {
        e.get("field") for e in normalized_existing if isinstance(e, dict) and e.get("field")
    }

    changes: List[Dict[str, Any]] = list(normalized_existing)
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
_SPLIT_PHRASES = ["split is required", "must be split", "should be split", "requires splitting", "different power outputs", "distinct trims", "different specifications", "separate variants"]
_CURRENT_IMPORT_PHRASES = ["currently sold", "officially sold", "currently imported", "imported now", "still imported", "available from the importer"]
_CURRENT_PRODUCTION_PHRASES = ["currently produced", "still produced", "still manufactured", "in production"]
_UNRESOLVED_TERMS = ["unresolved", "uncertain", "not verified", "disputed", "ambiguous", "special-order-only", "rare", "weakly inferred", "cannot be determined", "left unresolved"]
_IDENTITY_CRITICAL_FIELDS = {"fuel_type", "engine", "transmission", "drivetrain", "body_type", "year_start", "year_end"}

SOURCE_TYPE_KEYWORDS = {
    "official_importer": ["abarth.co.il", "samelet", "samelet.co.il", "סמלת", "kolmemotors", "colmobil"],
    "manufacturer": ["abarth.com", "fiat.com", "stellantis.com"],
    "marketplace": ["yad2", "autoboom", "wisecars", "ad.co.il", "lomoto"],
    "editorial": ["icar", "auto.co.il", "cartube", "gear", "wheel", "thecar", "over-drive", "walla", "sport5", "ynet", "mako", "girafa", "carzone", "car-pad", "queen of road", "גלגלים", "אוטו"],
    "government": ["data.gov.il", "transport ministry", "ministry of transport", "משרד התחבורה", "רשות הרישוי"],
    "forum_community": ["forum", "community", "reddit"],
}

_SOURCE_TYPE_ORDER = ("editorial", "official_importer", "manufacturer", "marketplace", "government", "forum_community")

def classify_source_type(source_name: str, url: str, title: str = "") -> str:
    # Classify by source_name/domain first. Title is intentionally ignored for
    # known source/domain matches so editorial articles mentioning importers do
    # not become official_importer sources.
    source_text = " ".join(str(x or "").lower() for x in (source_name, url))
    for stype in _SOURCE_TYPE_ORDER:
        if any(k.lower() in source_text for k in SOURCE_TYPE_KEYWORDS[stype]):
            return stype
    title_text = str(title or "").lower()
    for stype in ("manufacturer", "marketplace", "government", "forum_community", "editorial"):
        if any(k.lower() in title_text for k in SOURCE_TYPE_KEYWORDS[stype]):
            return stype
    return "unknown"


_IL_YEAR_PATTERNS = [
    re.compile(r"(?:officially\s+imported\s+to\s+israel\s+starting(?:\s+around)?\s+in|launched\s+in\s+israel\s+in|arrived\s+in\s+israel\s+in)\s+(20\d{2}|19\d{2})", re.I),
    re.compile(r"(?:הושק\s+בישראל\s+ב|החל\s+שיווק\s+בישראל\s+ב)[-־]?(20\d{2}|19\d{2})"),
]

def _extract_clear_il_start_year(text: str) -> Optional[int]:
    for pat in _IL_YEAR_PATTERNS:
        m = pat.search(text or "")
        if m:
            return int(m.group(1))
    return None

def _record_change(row: Dict[str, Any], field: str, old: Any, new: Any, reason: str) -> None:
    changes = row.get("fields_changed")
    if not isinstance(changes, list):
        changes = []
    normalized = []
    for item in changes:
        if isinstance(item, dict) and item.get("field"):
            normalized.append(item)
        elif isinstance(item, str):
            normalized.append({"field": item, "from": None, "to": None, "reason": "Legacy string change normalized by guard."})
    if not any(c.get("field") == field and c.get("to") == new for c in normalized):
        normalized.append({"field": field, "from": old, "to": new, "reason": reason})
    row["fields_changed"] = normalized

def _has_combined_trim(trim: Any) -> bool:
    if not isinstance(trim, str) or not trim.strip():
        return False
    low = f" {trim.lower()} "
    return any(sep in low for sep in _SLASH_SEPARATORS) or ("," in trim and len([p for p in trim.split(",") if p.strip()]) > 1)

def _summary_wants_split(summary: str) -> bool:
    low = (summary or "").lower()
    return any(p in low for p in _SPLIT_PHRASES)

def _split_evidence_text(row: Dict[str, Any]) -> str:
    return " ".join(str(row.get(k) or "") for k in ("grounding_summary", "decision_reason"))

def _prefer_split(row):
    return bool(row.get("split_candidates")) or _summary_wants_split(_split_evidence_text(row))

def _split_candidates_count(row: Dict[str, Any]) -> int:
    candidates = row.get("split_candidates")
    return len(candidates) if isinstance(candidates, list) else 0

def _has_explicit_split_evidence(row: Dict[str, Any]) -> bool:
    return _has_combined_trim(row.get("canonical_trim")) and _split_candidates_count(row) >= 2 and _summary_wants_split(_split_evidence_text(row))

def _has_explicit_500c_cabriolet_evidence(row: Dict[str, Any]) -> bool:
    make = str(row.get("canonical_make") or "").lower()
    if make != "abarth":
        return False
    model = str(row.get("canonical_model") or "").lower()
    trim_s = str(row.get("canonical_trim") or "").lower()
    body = str(row.get("body_type") or "").lower()
    marketed_il = str(row.get("official_marketed_name_il") or "")
    return (
        "500c" in model
        or "500c" in trim_s
        or any(x in body for x in ("cabriolet", "cabrio", "convertible"))
        or "קבריולה" in marketed_il
        or "קבריו" in marketed_il
    )

def _sync_unresolved_language(row: Dict[str, Any]) -> None:
    unresolved = row.get("fields_left_unresolved") if isinstance(row.get("fields_left_unresolved"), list) else []
    text_by_field = {str(f).lower(): f for f in _OUTPUT_TO_SOURCE}
    haystack = " ".join(str(row.get(k) or "") for k in ("grounding_summary", "decision_reason", "guard_corrected_reason"))
    low = haystack.lower()
    if not any(term in low for term in _UNRESOLVED_TERMS):
        row["fields_left_unresolved"] = unresolved
        return
    sentences = re.split(r"[.!?;\n]+", low)
    unresolved_patterns = ("unresolved", "uncertain", "not verified", "disputed", "ambiguous", "cannot be determined", "left unresolved", "weakly inferred", "special-order-only", "rare")
    for key, field in text_by_field.items():
        for sentence in sentences:
            if key not in sentence:
                continue
            if any(term in sentence for term in unresolved_patterns) and not any(f"{key} is verified" in sentence or f"{key} verified" in sentence for _ in [0]):
                if field not in unresolved:
                    unresolved.append(field)
                break
    row["fields_left_unresolved"] = unresolved

def _add_guard_corrected_reason(row: Dict[str, Any], before: Dict[str, Any]) -> None:
    watched = ["validation_decision", "identity_status", "identity_confidence", "canonical_trim", "trim_status", "trim_confidence", "year_start", "year_end", "is_currently_produced", "is_currently_imported_il", "transmission"]
    changes = [f"{k}: {before.get(k)!r} -> {row.get(k)!r}" for k in watched if before.get(k) != row.get(k)]
    if changes:
        note = "Python guards corrected the model output: " + "; ".join(changes) + "."
        row["guard_corrected_reason"] = note
        reason = row.get("decision_reason") or ""
        if "Guard correction:" not in reason:
            row["decision_reason"] = (reason + " " if reason else "") + "Guard correction: " + note


def _sentence_mentions_unresolved(sentence: str) -> bool:
    return any(term in sentence for term in ("unresolved", "uncertain", "not verified", "disputed", "ambiguous", "cannot be determined", "left unresolved", "weakly inferred", "special-order-only", "rare", "unknown"))

def _text_fields_unresolved(row: Dict[str, Any]) -> List[str]:
    """Precise sync: only add a field when the same sentence marks it unresolved."""
    aliases = {
        "transmission": ("transmission", "gearbox"),
        "engine": ("engine",),
        "year_end": ("year_end", "end year"),
        "canonical_trim": ("canonical_trim", "trim"),
        "fuel_type": ("fuel_type", "fuel"),
        "body_type": ("body_type", "body"),
        "drivetrain": ("drivetrain",),
        "year_start": ("year_start", "start year"),
    }
    haystack = " ".join(str(row.get(k) or "") for k in ("grounding_summary", "decision_reason", "guard_corrected_reason", "blocking_identity_issues", "non_blocking_trim_issues"))
    sentences = re.split(r"[.!?;\n]+", haystack.lower())
    found: List[str] = []
    for sentence in sentences:
        if not _sentence_mentions_unresolved(sentence):
            continue
        if " verified" in sentence and not any(x in sentence for x in ("not verified", "unverified")):
            continue
        for field, names in aliases.items():
            if any(name in sentence for name in names) and field not in found:
                found.append(field)
    return found

def _is_split_only_issue(text: str) -> bool:
    low = str(text or "").lower()
    if not any(p in low for p in _SPLIT_PHRASES + ["split_required", "combined trim", "multiple trims"]):
        return False
    contradiction_terms = ("wrong make", "wrong model", "wrong market", "impossible", "incompatible", "identity contradiction", "powertrain contradiction")
    return not any(t in low for t in contradiction_terms)

def _apply_strict_audit_guards(row: Dict[str, Any], flags: List[GuardFlag]) -> None:
    unresolved = row.get("fields_left_unresolved") if isinstance(row.get("fields_left_unresolved"), list) else []
    for field in _text_fields_unresolved(row):
        if field not in unresolved:
            unresolved.append(field)
            sev = "high" if field in _IDENTITY_CRITICAL_FIELDS else "medium"
            _add_flag(flags, "unresolved_field_sync", None, field, field, f"Audit text marks {field} unresolved but fields_left_unresolved omitted it.", severity=sev, risk_tags=["audit_consistency", "identity_critical"] if sev == "high" else ["audit_consistency"])
    row["fields_left_unresolved"] = unresolved

    blocking = row.get("blocking_identity_issues") if isinstance(row.get("blocking_identity_issues"), list) else []
    moved = [issue for issue in blocking if _is_split_only_issue(issue)]
    if moved:
        row["blocking_identity_issues"] = [issue for issue in blocking if issue not in moved]
        nonblocking = row.get("non_blocking_trim_issues") if isinstance(row.get("non_blocking_trim_issues"), list) else []
        for issue in moved:
            if issue not in nonblocking:
                nonblocking.append(issue)
        row["non_blocking_trim_issues"] = nonblocking
        _add_flag(flags, "split_issue_blocking_identity", blocking, row["blocking_identity_issues"], "blocking_identity_issues", "Split-only trim issue moved out of blocking identity issues.", severity="medium", risk_tags=["split", "audit_consistency"])

    # Explanation/final-field contradictions that can affect audit or publishability.
    text = " ".join(str(row.get(k) or "") for k in ("decision_reason", "grounding_summary", "guard_corrected_reason")).lower()
    if row.get("identity_status") in {"likely_valid", "uncertain"} and re.search(r"identity (?:is |was )?verified|verified identity", text):
        _add_flag(flags, "decision_reason_conflict", row.get("identity_status"), row.get("identity_status"), "identity_status", "Audit text claims verified identity while final identity_status is not verified.", severity="high", risk_tags=["audit_consistency", "publishability"])
    if row.get("trim_status") in {"unresolved", "invalid"} and re.search(r"(?:exact )?trim (?:is |was )?verified|verified trim", text):
        _add_flag(flags, "decision_reason_conflict", row.get("trim_status"), row.get("trim_status"), "canonical_trim", "Audit text claims verified trim while final trim_status is unresolved/invalid.", severity="medium", risk_tags=["audit_consistency"])
    if (row.get("is_currently_produced") in {False, None} or row.get("is_currently_imported_il") in {False, None}) and re.search(r"current(?:ly)? (?:produced|imported|sold)|still (?:produced|imported|sold)", text):
        _add_flag(flags, "current_status_conflict", None, None, "is_currently_imported_il", "Audit text contains current-status claims not supported by final current flags.", severity="high", risk_tags=["current_status", "publishability"])

    # Source classification risk: flag likely title-derived official classifications.
    for src in row.get("evidence_sources") or []:
        if not isinstance(src, dict):
            continue
        actual = classify_source_type(str(src.get("source_name") or ""), str(src.get("url") or ""), "")
        claimed = src.get("source_type")
        if claimed in {"official_importer", "manufacturer"} and actual not in {claimed, "unknown"}:
            old = claimed
            src["source_type"] = actual
            _add_flag(flags, "source_classification_risk", old, actual, "source_type", "source_type corrected using source_name/domain rather than title text.", severity="medium", risk_tags=["source_classification", "audit_consistency"])

    # Confidence mismatch deterministic downgrades.
    if row.get("identity_status") == "likely_valid" and float(row.get("identity_confidence") or 0) >= 0.99:
        old = row.get("identity_confidence"); row["identity_confidence"] = 0.85
        _add_flag(flags, "identity_confidence_downgrade", old, row["identity_confidence"], "identity_confidence", "likely_valid identity should not retain exact-level confidence.", severity="medium")
    if row.get("identity_status") == "uncertain" and float(row.get("identity_confidence") or 0) > 0.7:
        old = row.get("identity_confidence"); row["identity_confidence"] = 0.7
        _add_flag(flags, "identity_confidence_downgrade", old, row["identity_confidence"], "identity_confidence", "uncertain identity should not retain very high confidence.", severity="high")
    if row.get("trim_status") in {"unresolved", "invalid"} and float(row.get("trim_confidence") or 0) > 0.2:
        old = row.get("trim_confidence"); row["trim_confidence"] = 0.0
        _add_flag(flags, "confidence_mismatch", old, 0.0, "trim_confidence", "Unresolved/invalid trim confidence reset to 0.0.", severity="low")

    # clean_exact and clean catalog safety restrictions.
    unresolved = row.get("fields_left_unresolved") if isinstance(row.get("fields_left_unresolved"), list) else []
    clean_exact_bad = (
        row.get("validation_decision") == "clean_exact" and row.get("canonical_make") not in (None, "", []) and row.get("canonical_model") not in (None, "", []) and (
            row.get("canonical_trim") in (None, "", [])
            or row.get("trim_status") in {"unresolved", "invalid"}
            or row.get("identity_status") != "verified"
            or any(f in unresolved for f in _IDENTITY_CRITICAL_FIELDS)
            or _has_combined_trim(row.get("canonical_trim"))
            or bool(row.get("split_candidates"))
            or any(is_weak_trim(str(row.get("canonical_trim") or "")) for _ in [0])
        )
    )
    if clean_exact_bad:
        old = row.get("validation_decision")
        row["validation_decision"] = "split_required" if (row.get("split_candidates") or _prefer_split(row)) else "clean_partial"
        _add_flag(flags, "no_clean_exact_unresolved", old, row["validation_decision"], "validation_decision", "clean_exact violated exact-publishability restrictions.", severity="high", risk_tags=["publishability", "clean_exact"])

    if row.get("final_route") == "clean_catalog":
        bad = row.get("identity_status") != "verified" or row.get("validation_decision") not in {"clean_exact", "clean_partial"} or any(f in unresolved for f in _IDENTITY_CRITICAL_FIELDS) or bool(row.get("blocking_identity_issues")) or bool(row.get("split_candidates"))
        if bad:
            _add_flag(flags, "clean_catalog_safety", True, False, "final_route", "clean_catalog route contains identity-critical unresolved, blocking, split, or non-publishable state.", severity="high", risk_tags=["publishability", "routing"])

def _final_audit_consistency(row: Dict[str, Any], original: Dict[str, Any]) -> None:
    """Rebuild final audit text from actual final fields; no stale guard diffs."""
    unresolved = row.get("fields_left_unresolved") if isinstance(row.get("fields_left_unresolved"), list) else []
    parts = [f"Final decision {row.get('validation_decision')} with identity_status={row.get('identity_status')} and trim_status={row.get('trim_status')}."]
    if unresolved:
        parts.append("Unresolved fields: " + ", ".join(map(str, unresolved)) + ".")
    if row.get("is_currently_produced") is not True and row.get("is_currently_imported_il") is not True:
        parts.append("Current production/import is not verified by final fields.")
    row["decision_reason"] = " ".join(parts)
    watched = ["validation_decision", "identity_status", "identity_confidence", "canonical_trim", "trim_status", "trim_confidence", "year_start", "year_end", "is_currently_produced", "is_currently_imported_il", "transmission", "fields_left_unresolved"]
    changes = [f"{k}: {original.get(k)!r} -> {row.get(k)!r}" for k in watched if original.get(k) != row.get(k)]
    row["guard_corrected_reason"] = "Final guards made no material changes." if not changes else "Final Python guards corrected the Stage 1 output: " + "; ".join(changes) + "."

def _apply_v3_guards(row: Dict[str, Any], flags: List[GuardFlag]) -> None:
    before_guard_fields = dict(row)
    trim = row.get("canonical_trim")
    if isinstance(trim, str) and trim.strip().lower() in _GENERIC_TRIMS:
        old = row.get("validation_decision")
        row["canonical_trim"] = None; row["trim_status"] = "unresolved"; row["trim_confidence"] = 0.0
        if old == "clean_exact": row["validation_decision"] = "clean_partial"
        _add_issue(row, f"Trim '{trim}' is a generic placeholder; reset to null/unresolved.")
        _add_flag(flags, "generic_trim", old, row.get("validation_decision"), "canonical_trim", "Generic trim reset to unresolved.")

    if _has_explicit_split_evidence(row):
        old = row.get("validation_decision")
        row["validation_decision"] = "split_required"
        row["acceptance_tier"] = "none"
        row["trim_status"] = "invalid"
        row["trim_confidence"] = 0.0
        _add_issue(row, "Combined trim contains multiple distinct marketed trims and must be split into separate variants.")
        _add_flag(flags, "slash_trim", old, "split_required", "validation_decision", "Combined trim has split candidates and explicit split evidence.")
    elif _has_combined_trim(row.get("canonical_trim")) and row.get("validation_decision") == "clean_exact":
        old = row.get("validation_decision")
        row["validation_decision"] = "split_required" if _prefer_split(row) else "clean_partial"
        _add_issue(row, "Slash/combined trim cannot be clean_exact.")
        _add_flag(flags, "slash_trim", old, row.get("validation_decision"), "validation_decision", "Slash/combined trim cannot be clean_exact.")

    if row.get("validation_decision") == "clean_exact" and _summary_wants_split(_split_evidence_text(row)):
        old = row.get("validation_decision")
        row["validation_decision"] = "split_required" if any(p in _split_evidence_text(row).lower() for p in ["different power outputs", "distinct trims", "different specifications", "separate variants", "split is required", "must be split"]) else "clean_partial"
        _add_issue(row, "Grounding summary conflicts with clean_exact decision.")
        _add_flag(flags, "grounding_summary_vs_decision", old, row.get("validation_decision"), "validation_decision", "Grounding summary indicates split/partial, not clean_exact.")

    if row.get("validation_decision") == "clean_exact" and any(p in (row.get("grounding_summary") or "").lower() for p in _UNDER_CONSIDERATION_PHRASES):
        old = row.get("validation_decision")
        row["validation_decision"] = "clean_partial"; row["identity_status"] = "likely_valid"; row["is_currently_imported_il"] = None
        _add_issue(row, "Israeli market sale/import not fully verified; source indicates expected or under consideration.")
        _add_flag(flags, "under_consideration", old, "clean_partial", "validation_decision", "Only expected/under consideration market status found.")

    il_start = _extract_clear_il_start_year(" ".join(str(row.get(k) or "") for k in ("grounding_summary", "decision_reason")))
    ys = row.get("year_start")
    if isinstance(ys, int) and isinstance(il_start, int) and il_start > ys:
        reason = f"Israeli-market import/start year is {il_start}; {ys} appears to be global launch year."
        row["year_start"] = il_start
        _record_change(row, "year_start", ys, il_start, reason)
        _add_issue(row, reason)
        _add_flag(flags, "year_start_il_market", None, None, "year_start", reason)

    cur = datetime.datetime.now(datetime.timezone.utc).year
    ye = row.get("year_end")
    current_text = " ".join(str(row.get(k) or "") for k in ("grounding_summary", "decision_reason")).lower()
    has_prod_evidence = any(p in current_text for p in _CURRENT_PRODUCTION_PHRASES)
    has_import_evidence = any(p in current_text for p in _CURRENT_IMPORT_PHRASES)
    if ye is None and row.get("is_currently_produced") is True and not has_prod_evidence:
        old = row.get("is_currently_produced")
        row["is_currently_produced"] = None
        _add_issue(row, "Current production was not explicitly supported; year_end=null alone is not current-production evidence.")
        _add_flag(flags, "current_status_conflict", old, None, "is_currently_produced", "Current production requires explicit production evidence.", severity="high")
    if ye is None and row.get("is_currently_imported_il") is True and not has_import_evidence:
        old = row.get("is_currently_imported_il")
        row["is_currently_imported_il"] = None
        _add_issue(row, "Current official Israel import/sale was not explicitly supported; year_end=null alone is not current-import evidence.")
        _add_flag(flags, "current_status_conflict", old, None, "is_currently_imported_il", "Current import requires explicit local sale/import evidence.", severity="high")
    if isinstance(ye, int) and ye < cur and (row.get("is_currently_produced") is True or row.get("is_currently_imported_il") is True):
        row["is_currently_produced"] = False
        row["is_currently_imported_il"] = False
        _add_issue(row, "Current-production/import flags corrected to false because year_end is a past year for this variant.")
        _add_flag(flags, "year_end_current", None, None, "is_currently_produced", "Past year_end corrected active flags to false.")
    elif isinstance(ye, int) and ye >= cur:
        old = ye
        row["year_end"] = None
        _record_change(row, "year_end", old, None, "Current/future year_end was not kept as a placeholder; reset to null unless strongly supported as an end year.")
        _add_issue(row, "year_end was current/future and not kept as a placeholder.")
        _add_flag(flags, "year_end_current", old, None, "year_end", "Current/future year_end reset to null because placeholder end years are not allowed.")

    trim_s = str(row.get("canonical_trim") or "").lower(); trans = str(row.get("transmission") or "").lower()
    is_500c = _has_explicit_500c_cabriolet_evidence(row)
    if is_500c and trim_s in {"500c", "cabrio", "cabriolet", "convertible"}:
        row["canonical_trim"] = None; row["trim_status"] = "unresolved"; row["trim_confidence"] = 0.0
        _add_issue(row, "500C/Cabriolet is a body/model designation, not a verified trim.")
        _add_flag(flags, "generic_trim", None, None, "canonical_trim", "500C/Cabriolet trim cleanup.")
    if is_500c and "manual" in trans and row.get("identity_status") == "verified":
        old = row.get("validation_decision")
        row["identity_status"] = "likely_valid"; row["identity_confidence"] = min(float(row.get("identity_confidence") or 0.7), 0.7); row["validation_decision"] = "clean_partial"
        unresolved = row.get("fields_left_unresolved") if isinstance(row.get("fields_left_unresolved"), list) else []
        if "transmission" not in unresolved:
            unresolved.append("transmission")
        row["fields_left_unresolved"] = unresolved
        _add_issue(row, "Abarth 500C/Cabriolet manual transmission is not verified for the Israeli market; transmission left unresolved.")
        _add_flag(flags, "domain_500c_transmission", old, "clean_partial", "identity_status", "Manual transmission not verified for Israeli Abarth 500C/Cabriolet.")

    if row.get("validation_decision") == "reject" and not row.get("blocking_identity_issues"):
        old = row.get("validation_decision")
        row["validation_decision"] = "clean_partial"
        _add_issue(row, "Reject downgraded to clean_partial: no blocking identity issue found.")
        _add_flag(flags, "no_reject_without_blocking_issue", old, "clean_partial", "validation_decision", "Reject without blocking identity issue downgraded.")

    unresolved = row.get("fields_left_unresolved") if isinstance(row.get("fields_left_unresolved"), list) else []
    if row.get("validation_decision") == "clean_exact" and float(row.get("identity_confidence") or 0.0) > 0 and (
        row.get("trim_status") in {"unresolved", "invalid"}
        or row.get("split_candidates")
        or _has_combined_trim(row.get("canonical_trim"))
        or row.get("identity_status") in {"likely_valid", "uncertain"}
        or any(f in unresolved for f in _IDENTITY_CRITICAL_FIELDS)
        or any(p in (row.get("grounding_summary") or "").lower() for p in _UNDER_CONSIDERATION_PHRASES)
    ):
        old = row.get("validation_decision")
        row["validation_decision"] = "split_required" if (row.get("split_candidates") or _prefer_split(row)) else "clean_partial"
        _add_issue(row, "clean_exact downgraded because trim/identity/market evidence remains unresolved or corrected.")
        _add_flag(flags, "no_clean_exact_unresolved", old, row.get("validation_decision"), "validation_decision", "clean_exact is not allowed with unresolved/corrected identity or trim issues.")

    _sync_unresolved_language(row)
    _apply_strict_audit_guards(row, flags)
    unresolved = row.get("fields_left_unresolved") if isinstance(row.get("fields_left_unresolved"), list) else []
    if row.get("validation_decision") == "clean_exact" and any(f in _IDENTITY_CRITICAL_FIELDS for f in unresolved):
        old = row.get("validation_decision")
        row["validation_decision"] = "clean_partial"
        row["identity_status"] = "likely_valid" if row.get("identity_status") == "verified" else row.get("identity_status")
        _add_issue(row, "clean_exact downgraded because an identity-critical technical field remains unresolved.")
        _add_flag(flags, "technical_unresolved_publishability", old, "clean_partial", "validation_decision", "Identity-critical technical field unresolved.", severity="high")

    if row.get("official_marketed_name_il") not in (None, "", []):
        row["fields_left_unresolved"] = [f for f in unresolved if f != "official_marketed_name_il"]
    elif row.get("identity_status") in {"verified", "likely_valid"} and "official_marketed_name_il" not in unresolved:
        unresolved.append("official_marketed_name_il"); row["fields_left_unresolved"] = unresolved

    _add_guard_corrected_reason(row, before_guard_fields)

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
    if final_pass:
        _apply_strict_audit_guards(row, flags)
        _final_audit_consistency(row, model_output)
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
