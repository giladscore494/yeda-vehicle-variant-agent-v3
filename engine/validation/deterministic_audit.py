"""Deterministic validation audit — runs over the entire canonical database.

No model calls. Scans every variant and seed relation.
Returns structured issues for the validation report.
"""
from __future__ import annotations

from collections import Counter
from core.schemas import BodyType, FuelType, Transmission, Market
from core.source_ids import looks_like_placeholder_source_id
from engine.state import seed_id_from_seed
from engine.validation.normalizer import safe_str, extract_value, extract_year


# Allowed enum values for quick membership checks
_BODY_TYPES = {e.value for e in BodyType}
_FUEL_TYPES = {e.value for e in FuelType}
_TRANSMISSIONS = {e.value for e in Transmission}
_MARKETS = {e.value for e in Market}
_CONFIDENCE_LEVELS = {"high", "medium", "low"}
_MARKET_SCOPES = {
    "IL-confirmed", "IL-likely", "global-reference-only",
    "il-confirmed", "il-likely", "global-reference-only",
}

# Impossible engine/fuel combos
_IMPOSSIBLE_ENGINE_FUEL = [
    # Electric vehicles don't have petrol/diesel engines
    (lambda e, f: "electric" in f and any(
        k in e for k in ("turbo", "v6", "v8", "inline", "boxer", "naturally aspirated")
    )),
]


def run_deterministic_audit(canonical: dict, seeds: list[dict] | None = None) -> list[dict]:
    """Run all deterministic checks over the canonical database.

    Returns a list of issue dicts.
    """
    issues: list[dict] = []
    issue_counter = 0

    def _add(issue_type: str, severity: str, **kwargs) -> None:
        nonlocal issue_counter
        issue_counter += 1
        issue = {
            "issue_id": f"det_{issue_counter:05d}",
            "issue_type": issue_type,
            "severity": severity,
            **kwargs,
        }
        issue.setdefault("seed_id", "")
        issue.setdefault("variant_id", "")
        issue.setdefault("current_value", "")
        issue.setdefault("evidence", [])
        issue.setdefault("recommended_action", "")
        issue.setdefault("requires_model_review", False)
        issue.setdefault("requires_manual_review", False)
        issues.append(issue)

    # ── Structural checks ───────────────────────────────────────────────

    if not isinstance(canonical, dict):
        _add("json_structure_error", "critical",
             current_value="root is not a dict",
             recommended_action="Fix canonical JSON structure")
        return issues

    # Required top-level keys
    for key in ("verified_variants", "partial_variants", "batch_state"):
        if key not in canonical:
            _add("missing_top_level_key", "high",
                 current_value=key,
                 recommended_action=f"Add missing key: {key}")

    verified = canonical.get("verified_variants") or []
    partial = canonical.get("partial_variants") or []
    if not isinstance(verified, list):
        _add("variants_not_list", "critical",
             current_value=f"verified_variants is {type(verified).__name__}")
        verified = []
    if not isinstance(partial, list):
        _add("variants_not_list", "critical",
             current_value=f"partial_variants is {type(partial).__name__}")
        partial = []

    all_variants = verified + partial

    bs = canonical.get("batch_state")
    if not isinstance(bs, dict):
        _add("missing_batch_state", "high",
             recommended_action="Add batch_state dict")
        bs = {}

    # ── Variant-level checks ────────────────────────────────────────────

    seen_vids: dict[str, int] = {}
    sources_index: set[str] = set()

    # Build sources index from top-level sources if present
    for src in canonical.get("sources", []):
        if isinstance(src, dict) and src.get("source_id"):
            sources_index.add(str(src["source_id"]).strip())

    for idx, v in enumerate(all_variants):
        if not isinstance(v, dict):
            _add("variant_not_dict", "high",
                 current_value=f"index {idx}")
            continue

        vid = str(v.get("variant_id", "")).strip()
        sid_v = v.get("seed_id", "")

        # variant_id uniqueness
        if vid:
            if vid in seen_vids:
                _add("duplicate_variant_id", "high",
                     variant_id=vid, seed_id=str(sid_v),
                     current_value=f"duplicate at index {seen_vids[vid]} and {idx}",
                     recommended_action="Remove or merge duplicate")
            else:
                seen_vids[vid] = idx

        # make/model/year presence
        make = safe_str(v.get("make"))
        model = safe_str(v.get("model"))
        ys = extract_year(v.get("year_start"))
        ye = extract_year(v.get("year_end"))

        if not make:
            _add("missing_make", "medium", variant_id=vid,
                 recommended_action="Add make field")
        if not model:
            _add("missing_model", "medium", variant_id=vid,
                 recommended_action="Add model field")
        if ys is None:
            _add("missing_year_start", "medium", variant_id=vid,
                 recommended_action="Add year_start field")
        if ye is None:
            _add("missing_year_end", "medium", variant_id=vid,
                 recommended_action="Add year_end field")

        # year_start <= year_end
        if ys is not None and ye is not None and ys > ye:
            _add("year_range_inverted", "high", variant_id=vid,
                 current_value=f"{ys}-{ye}",
                 recommended_action="Fix year range")

        # body_type normalized
        bt = safe_str(v.get("body_type"))
        if bt and bt not in _BODY_TYPES:
            _add("body_type_not_normalized", "low", variant_id=vid,
                 current_value=bt,
                 recommended_action="Normalize body_type")

        # fuel_type normalized
        ft = safe_str(v.get("fuel_type"))
        if ft and ft not in _FUEL_TYPES:
            _add("fuel_type_not_normalized", "low", variant_id=vid,
                 current_value=ft,
                 recommended_action="Normalize fuel_type")

        # transmission normalized
        tr = safe_str(v.get("transmission"))
        if tr and tr not in _TRANSMISSIONS:
            _add("transmission_not_normalized", "low", variant_id=vid,
                 current_value=tr,
                 recommended_action="Normalize transmission")

        # market_scope allowed value
        ms = (v.get("market_scope") or "").strip()
        if ms and ms not in _MARKET_SCOPES:
            _add("market_scope_invalid", "medium", variant_id=vid,
                 current_value=ms,
                 recommended_action="Set valid market_scope")

        # confidence_level allowed value
        cl = safe_str(v.get("confidence_level") or v.get("confidence"))
        if cl and cl not in _CONFIDENCE_LEVELS:
            _add("confidence_level_invalid", "low", variant_id=vid,
                 current_value=cl)

        # Source IDs quality
        source_ids = v.get("source_ids") or []
        if not source_ids:
            _add("empty_source_ids", "medium", variant_id=vid,
                 recommended_action="Add source evidence")

        placeholder_sids = [s for s in source_ids if looks_like_placeholder_source_id(str(s))]
        if placeholder_sids:
            _add("placeholder_source_ids", "high", variant_id=vid,
                 current_value=str(placeholder_sids),
                 recommended_action="Replace placeholder source_ids with real references")

        # IL-confirmed must have Israeli-market source evidence
        if ms in ("IL-confirmed", "il-confirmed"):
            if not source_ids or all(looks_like_placeholder_source_id(str(s)) for s in source_ids):
                _add("il_confirmed_no_evidence", "high", variant_id=vid,
                     current_value=ms,
                     recommended_action="Add Israeli-market source evidence",
                     requires_model_review=True)

        # Source IDs must exist in top-level sources (if sources index available)
        if sources_index:
            for sid_ref in source_ids:
                sid_str = str(sid_ref).strip()
                if sid_str and not looks_like_placeholder_source_id(sid_str) and sid_str not in sources_index:
                    _add("source_id_not_in_sources", "medium", variant_id=vid,
                         current_value=sid_str,
                         recommended_action="Add missing source to sources array")

        # field_sources must reference real source_ids
        field_sources = v.get("field_sources")
        if isinstance(field_sources, dict):
            for field_name, fsids in field_sources.items():
                if isinstance(fsids, list):
                    for fsid in fsids:
                        if looks_like_placeholder_source_id(str(fsid)):
                            _add("field_source_placeholder", "medium", variant_id=vid,
                                 current_value=f"{field_name}:{fsid}")

        # Empty evidence with high confidence
        vc = safe_str(v.get("confidence_level") or v.get("confidence") or "")
        vs = v.get("verification_status", "")
        if vc == "high" and not source_ids:
            _add("high_confidence_no_evidence", "high", variant_id=vid,
                 recommended_action="Downgrade confidence or add evidence",
                 requires_model_review=True)

        # Impossible engine/fuel combos
        engine_str = safe_str(v.get("engine"))
        fuel_str = safe_str(v.get("fuel_type"))
        if engine_str and fuel_str:
            for check in _IMPOSSIBLE_ENGINE_FUEL:
                if check(engine_str, fuel_str):
                    _add("impossible_engine_fuel", "high", variant_id=vid,
                         current_value=f"engine={engine_str}, fuel={fuel_str}",
                         requires_model_review=True)

    # ── Duplicate trims within same seed ────────────────────────────────

    seed_trims: dict[str, list[str]] = {}
    for v in all_variants:
        if not isinstance(v, dict):
            continue
        sid_v = str(v.get("seed_id", "")).strip()
        trim = safe_str(v.get("trim"))
        if sid_v and trim:
            seed_trims.setdefault(sid_v, []).append(trim)

    for sid_v, trims in seed_trims.items():
        counts = Counter(trims)
        for trim_val, cnt in counts.items():
            if cnt > 1:
                _add("duplicate_trim_in_seed", "medium", seed_id=sid_v,
                     current_value=f"{trim_val} x{cnt}",
                     recommended_action="Merge or differentiate duplicates")

    # ── Seed-level checks ───────────────────────────────────────────────

    if seeds is not None:
        catalog_ids = {seed_id_from_seed(s) for s in seeds}
        processed = set(bs.get("processed_seed_ids") or [])
        failed = set(bs.get("failed_seed_ids") or [])
        manual_review = set(bs.get("manual_review_seed_ids") or [])

        # Seeds in queues must exist in catalog
        for sid in processed:
            if sid not in catalog_ids:
                _add("processed_seed_not_in_catalog", "medium", seed_id=sid)

        for sid in failed:
            if sid not in catalog_ids:
                _add("failed_seed_not_in_catalog", "medium", seed_id=sid)

        for sid in manual_review:
            if sid not in catalog_ids:
                _add("manual_seed_not_in_catalog", "medium", seed_id=sid)

        # Bucket overlap detection
        pf = processed & failed
        pm = processed & manual_review
        mf = manual_review & failed

        for sid in pf:
            _add("seed_in_processed_and_failed", "high", seed_id=sid,
                 recommended_action="Remove from one bucket")
        for sid in pm:
            _add("seed_in_processed_and_manual", "high", seed_id=sid,
                 recommended_action="Remove from one bucket")
        for sid in mf:
            _add("seed_in_manual_and_failed", "medium", seed_id=sid)

        # Seeds missing from all buckets
        all_bucketed = processed | failed | manual_review
        missing_seeds = catalog_ids - all_bucketed
        for sid in sorted(missing_seeds)[:50]:
            _add("seed_missing_from_buckets", "low", seed_id=sid,
                 recommended_action="Seed not yet processed")

        # Processed seeds without variants or closure
        accounting = bs.get("seed_accounting") or {}
        for sid in processed:
            acct = accounting.get(sid, {})
            res_type = acct.get("resolution_type", "")
            if res_type == "no_variants_proven":
                continue
            if res_type in ("variants_added", "variants_added_after_failed_retry"):
                continue
            _add("processed_seed_no_closure", "medium", seed_id=sid,
                 current_value=f"resolution_type={res_type}",
                 recommended_action="Verify seed processing result")

        # Failed seeds that are already resolved
        for sid in failed:
            if sid in processed:
                _add("failed_seed_already_resolved", "medium", seed_id=sid,
                     recommended_action="Remove from failed queue (stale failure)")

        # Manual review seeds that are already resolved
        for sid in manual_review:
            if sid in processed:
                _add("manual_seed_already_resolved", "medium", seed_id=sid,
                     recommended_action="Remove from manual review queue")

    return issues


def summarize_deterministic_issues(issues: list[dict]) -> dict:
    """Build a summary of deterministic audit issues."""
    severity_counts: dict[str, int] = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    type_counts: dict[str, int] = {}

    for issue in issues:
        sev = issue.get("severity", "low")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
        itype = issue.get("issue_type", "unknown")
        type_counts[itype] = type_counts.get(itype, 0) + 1

    return {
        "total_issues": len(issues),
        "by_severity": severity_counts,
        "by_type": type_counts,
    }
