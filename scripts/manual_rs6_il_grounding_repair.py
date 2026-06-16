"""One-off manual, web-grounded repair for the blocked ``IL|Audi|RS6`` profile.

Context
-------
The catalog runner left ``IL|Audi|RS6`` in review (repair-exhausted). Unlike an
empty parse/API failure it carries three REAL ``technical_variants_il`` rows and
has NO ``request_payload`` — so it is a targeted/manual data-repair case, never a
full rebuild from payload. The two blocking validation issues were:

  * variant[1] (RS6 Avant *performance*, 630 hp, Estate, 2022-2024)
    ``fuel_type = "petrol"`` had no ``field_sources`` grounding and was listed in
    ``missing_grounded_fields``.
  * variant[2] (a 2024 "RS6 - S6" iCar *catalog* row, 560 hp, ``support_level =
    "unknown"``) had a null ``body_type``.

Manual web research (June 2026)
-------------------------------
The Israeli source pages already in the profile (iCar / Wheel) block automated
fetching (HTTP 403), so their bodies could not be re-read here. The *values*
were instead verified externally via web search against multiple independent
technical catalogs, all agreeing on the C8 RS6 Avant performance:

  petrol 4.0 TFSI V8 twin-turbo, 630 hp, 8-speed automatic (tiptronic),
  quattro AWD, 5-door estate, 48V mild-hybrid.

  - https://www.auto-data.net/en/audi-rs6-avant-c8-performance-4.0-tfsi-v8-630hp-mild-hybrid-quattro-tiptronic-46941
  - https://www.autodata1.com/en/car/audi/rs-6/rs-6-avant-c8-performance-40-tfsi-v8-630-hp-mhev-quattro-tiptronic
  - https://en.wikipedia.org/wiki/Audi_RS_6

Repair actions (no invented data)
---------------------------------
1. variant[1] ``fuel_type=petrol`` is grounded to a reliable global technical
   catalog source (auto-data.net) added to ``sources``. The Israeli sources
   establish the variant's Israeli-market presence; the catalog source grounds
   the technical fuel field. ``support_level`` stays ``"indirect"`` per the
   Israeli-presence + global-technical rule. ``fuel_type`` is removed from
   ``missing_grounded_fields`` only after it is actually grounded.
2. variant[2] (the 560 hp 2024 "RS6 - S6" row) is DROPPED, not force-grounded.
   560 hp matches no real C8 RS6 Avant (600/630 hp); the source page conflates
   RS6/S6 and the profile notes already flag it as conflicting with
   ``support_level="unknown"``. It cannot be Israeli-market validated, so it is
   removed from the clean candidate rather than fabricating a ``body_type``.

The profile is then re-validated; it is promoted to clean ONLY if
``validate_profile`` returns ready. Repair-only bookkeeping fields are stripped
before writing to clean. This script is deterministic and safe to re-run.
"""

from __future__ import annotations

import copy
from typing import Any, Callable, Dict, List, Optional

from .catalog_builder import (
    CATALOG_OUTPUT_PATH,
    READINESS_OUTPUT_PATH,
    REVIEW_OUTPUT_PATH,
    _model_key,
    load_existing_outputs,
    merge_and_write_outputs,
)
from .catalog_repair import _CHECKPOINT_STATE_FIELDS, _REVIEW_ONLY_KEYS
from .catalog_validation import validate_profile
from .openai_catalog_client import CatalogClientSettings

RS6_KEY = "IL|Audi|RS6"
S4_KEY = "IL|Audi|S4"

# Reliable global technical catalog source for the C8 RS6 Avant performance.
# Used (support_level "indirect") to ground the technical fuel_type field; the
# value was verified against several independent catalogs (see module docstring).
RS6_PERFORMANCE_FUEL_SOURCE = {
    "title": "Audi RS6 Avant (C8) performance 4.0 TFSI V8 (630 Hp) Mild Hybrid quattro tiptronic",
    "url": "https://www.auto-data.net/en/audi-rs6-avant-c8-performance-4.0-tfsi-v8-630hp-mild-hybrid-quattro-tiptronic-46941",
    "source_name": "auto-data.net",
    "source_type": "catalog",
    "supports": [
        "fuel_type",
        "engine",
        "engine_displacement_l",
        "horsepower_hp",
        "transmission",
        "drivetrain",
    ],
}


def _next_source_index(sources: List[Dict[str, Any]]) -> int:
    used = [
        s["source_index"]
        for s in sources
        if isinstance(s, dict) and isinstance(s.get("source_index"), int)
    ]
    return (max(used) + 1) if used else 0


def _is_performance_petrol_variant(variant: Dict[str, Any]) -> bool:
    return (
        str(variant.get("version_or_trim") or "").strip().lower() == "performance"
        and variant.get("horsepower_hp") == 630
        and str(variant.get("fuel_type") or "").strip().lower() == "petrol"
    )


def _is_conflicting_560_variant(variant: Dict[str, Any]) -> bool:
    return (
        variant.get("horsepower_hp") == 560
        and str(variant.get("support_level") or "").strip().lower() == "unknown"
        and variant.get("body_type") in (None, "")
    )


def repair_rs6_profile(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Apply the two justified, web-grounded edits. Returns a repaired copy."""
    profile = copy.deepcopy(entry)
    sources = profile.get("sources") or []

    # 1. Ground variant[1] fuel_type via an added global technical catalog source.
    new_index = _next_source_index(sources)
    fuel_source = dict(RS6_PERFORMANCE_FUEL_SOURCE)
    fuel_source["source_index"] = new_index

    kept_variants: List[Dict[str, Any]] = []
    grounded_perf = False
    dropped_560 = False
    for variant in profile.get("technical_variants_il") or []:
        if not isinstance(variant, dict):
            kept_variants.append(variant)
            continue
        # 2. Drop the conflicting/unknown 560 hp "RS6 - S6" row.
        if _is_conflicting_560_variant(variant):
            dropped_560 = True
            continue
        if _is_performance_petrol_variant(variant):
            v = copy.deepcopy(variant)
            fs = dict(v.get("field_sources") or {})
            fs["fuel_type"] = [new_index]
            v["field_sources"] = fs
            src_idx = list(v.get("source_indexes") or [])
            if new_index not in src_idx:
                src_idx.append(new_index)
            v["source_indexes"] = sorted(src_idx)
            v["missing_grounded_fields"] = [
                f for f in (v.get("missing_grounded_fields") or []) if f != "fuel_type"
            ]
            kept_variants.append(v)
            grounded_perf = True
        else:
            kept_variants.append(variant)

    if grounded_perf:
        profile.setdefault("sources", [])
        if isinstance(profile["sources"], list):
            profile["sources"] = sources + [fuel_source]
        notes = list(profile.get("notes") or [])
        notes.append(
            "Manual web-grounded repair (June 2026): RS6 Avant performance fuel_type=petrol "
            "grounded to a reliable global technical catalog (auto-data.net) at support_level "
            "indirect; the Israeli editorial sources establish Israeli-market presence. Value "
            "cross-verified against multiple independent catalogs (auto-data.net, autodata1.com, "
            "Wikipedia)."
        )
        if dropped_560:
            notes.append(
                "Manual web-grounded repair (June 2026): dropped the conflicting 2024 'RS6 - S6' "
                "560 hp catalog row (support_level unknown); 560 hp matches no real C8 RS6 Avant "
                "output (600/630 hp) and the source page conflates RS6/S6."
            )
        profile["notes"] = notes
    profile["technical_variants_il"] = kept_variants
    profile["_repair_grounded_performance_fuel"] = grounded_perf
    profile["_repair_dropped_560_variant"] = dropped_560
    return profile


def run(
    *,
    catalog_path: str = CATALOG_OUTPUT_PATH,
    readiness_path: str = READINESS_OUTPUT_PATH,
    review_path: str = REVIEW_OUTPUT_PATH,
    settings: Optional[CatalogClientSettings] = None,
    log: Optional[Callable[[str], None]] = None,
) -> Dict[str, Any]:
    emit = log or print
    settings = settings or CatalogClientSettings()
    catalog, readiness, review = load_existing_outputs(catalog_path, readiness_path, review_path)

    checkpoint_state = {f: readiness[f] for f in _CHECKPOINT_STATE_FIELDS if f in readiness}

    review_models = [m for m in review.get("models", []) if isinstance(m, dict)]

    # --- S4: keep clean if locally valid; drop any stale review duplicate -----
    clean_by_key = {_model_key(m): m for m in catalog.get("models", []) if isinstance(m, dict)}
    s4_clean = clean_by_key.get(S4_KEY)
    s4_status = "absent"
    if s4_clean is not None:
        s4_result = validate_profile(s4_clean)
        s4_status = "valid_clean" if s4_result.ready else "invalid_clean"
        emit(
            f"S4 local validation: ready={s4_result.ready} | "
            f"variants={len(s4_clean.get('technical_variants_il') or [])} | "
            f"issues={len(s4_result.issues)}"
        )
    delta_ready: List[Dict[str, Any]] = []
    delta_review: List[Dict[str, Any]] = []

    # --- Catalog hygiene: strip stale repair-only fields from clean profiles ---
    # Promotion via older paths left some clean profiles carrying stale
    # ``repair_attempts`` / ``validation_issues``. They must never appear in the
    # clean catalog. Strip them ONLY when the profile still validates ready, so
    # this is a safe, non-destructive cleanup (no profile is demoted/changed).
    hygiene_cleaned = 0
    for cm in catalog.get("models", []):
        if not isinstance(cm, dict):
            continue
        leaked = [k for k in _REVIEW_ONLY_KEYS if k in cm]
        if not leaked:
            continue
        if not validate_profile(cm).ready:
            emit(f"HYGIENE SKIP (would not validate clean): {_model_key(cm)} keys={leaked}")
            continue
        cleaned = {k: v for k, v in cm.items() if k not in _REVIEW_ONLY_KEYS}
        delta_ready.append(cleaned)
        hygiene_cleaned += 1
    if hygiene_cleaned:
        emit(f"HYGIENE: stripped stale repair-only fields from {hygiene_cleaned} clean profile(s)")

    stale_s4_review = [m for m in review_models if _model_key(m) == S4_KEY]
    if stale_s4_review and s4_status == "valid_clean":
        emit(f"Removing {len(stale_s4_review)} stale {S4_KEY} duplicate(s) from review")
        # Re-assert the valid clean S4 so merge_and_write_outputs drops the
        # duplicate review entry (the merge dedups review against new_ready).
        delta_ready.append(s4_clean)
    review_models = [m for m in review_models if _model_key(m) != S4_KEY or s4_status != "valid_clean"]

    # --- RS6: inspect + manual web-grounded repair ----------------------------
    rs6 = next((m for m in review_models if _model_key(m) == RS6_KEY), None)
    rs6_status = "absent"
    if rs6 is None:
        emit(f"{RS6_KEY} not found in review; nothing to repair")
    else:
        before = validate_profile(rs6)
        emit(f"MANUAL WEB REPAIR: {RS6_KEY}")
        emit(f"  has request_payload: {isinstance(rs6.get('request_payload'), dict)}")
        emit(f"  variants: {len(rs6.get('technical_variants_il') or [])}")
        for i, v in enumerate(rs6.get("technical_variants_il") or []):
            emit(
                f"  variant[{i}]: trim={v.get('version_or_trim')} hp={v.get('horsepower_hp')} "
                f"body={v.get('body_type')} fuel={v.get('fuel_type')} support={v.get('support_level')} "
                f"missing_grounded={v.get('missing_grounded_fields')}"
            )
        emit(f"  current validation issues ({len(before.issues)}):")
        for issue in before.issues:
            emit(f"    - {issue}")
        emit(f"  sources used: {[s.get('source_name') for s in rs6.get('sources') or []]}")

        repaired = repair_rs6_profile(rs6)
        grounded = repaired.pop("_repair_grounded_performance_fuel", False)
        dropped = repaired.pop("_repair_dropped_560_variant", False)
        if grounded:
            emit("  fields repaired: variant 'performance' fuel_type=petrol grounded to "
                 "auto-data.net (support_level indirect)")
        if dropped:
            emit("  variant dropped: 560 hp 2024 'RS6 - S6' row (support_level unknown, "
                 "conflicting; not an Israeli-market RS6 Avant output)")

        after = validate_profile(repaired)
        if after.ready:
            clean_profile = dict(after.profile)
            for k in (*_REVIEW_ONLY_KEYS, "notes_internal"):
                clean_profile.pop(k, None)
            delta_ready.append(clean_profile)
            rs6_status = "promoted"
            emit(f"PROMOTE {RS6_KEY} after manual web-grounded repair")
        else:
            kept = dict(after.profile)
            kept["validation_issues"] = after.issues
            delta_review.append(kept)
            rs6_status = "kept"
            emit(f"KEEP {RS6_KEY}: unresolved Israeli-market grounding issues")
            for issue in after.issues:
                emit(f"    - {issue}")

    # Repair must not advance the main build pointer; record a repair pointer.
    if delta_ready or rs6_status == "promoted":
        checkpoint_state["last_repair_checkpointed_profile_id"] = "IL::Audi::RS6"

    catalog, readiness, review = merge_and_write_outputs(
        delta_ready,
        delta_review,
        settings=settings,
        checkpoint_state=checkpoint_state,
        catalog_path=catalog_path,
        readiness_path=readiness_path,
        review_path=review_path,
    )
    return {
        "s4_status": s4_status,
        "rs6_status": rs6_status,
        "readiness": readiness,
    }


if __name__ == "__main__":  # pragma: no cover - manual invocation
    result = run()
    r = result["readiness"]
    print(
        f"DONE | S4={result['s4_status']} RS6={result['rs6_status']} | "
        f"ready={r.get('models_ready_for_website')} blocked={r.get('models_blocked')}"
    )
