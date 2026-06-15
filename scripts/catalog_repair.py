"""Targeted repair mode for quality-blocked catalog profiles."""

from __future__ import annotations

import copy
import json
from typing import Any, Callable, Dict, List, Optional

from .catalog_builder import (
    CATALOG_OUTPUT_PATH,
    READINESS_OUTPUT_PATH,
    REVIEW_OUTPUT_PATH,
    _model_key,
    load_existing_outputs,
    merge_and_write_outputs,
)
from .catalog_validation import REQUIRED_WEBSITE_FIELDS, derive_available_values, validate_profile
from .openai_catalog_client import CatalogClientSettings, GROUNDED_TECHNICAL_FIELDS
from .catalog_provider import CatalogProviderSettings, build_catalog_client
from .security import sanitize_error

MAX_REPAIR_ATTEMPTS = 2


def derive_repair_targets(profile: Dict[str, Any]) -> Dict[int, List[str]]:
    targets: Dict[int, List[str]] = {}
    variants = profile.get("technical_variants_il") or []
    for idx, variant in enumerate(variants):
        if not isinstance(variant, dict):
            continue
        field_sources = variant.get("field_sources") if isinstance(variant.get("field_sources"), dict) else {}
        missing = set(variant.get("missing_grounded_fields") or [])
        fields = set()
        for fname in REQUIRED_WEBSITE_FIELDS:
            if variant.get(fname) in (None, ""):
                fields.add(fname)
        for fname in GROUNDED_TECHNICAL_FIELDS:
            if variant.get(fname) not in (None, "") and not field_sources.get(fname):
                fields.add(fname)
        fields.update(f for f in missing if isinstance(f, str))
        if fields:
            targets[idx] = sorted(fields)
    return targets


def _stable(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def merge_repair(existing: Dict[str, Any], repaired: Dict[str, Any], targets: Dict[int, List[str]]) -> Dict[str, Any]:
    patched = copy.deepcopy(existing)
    old_variants = existing.get("technical_variants_il") or []
    new_variants = repaired.get("technical_variants_il") or []
    if len(old_variants) != len(new_variants):
        raise ValueError("repair changed variant count")
    for idx, (old_v, new_v) in enumerate(zip(old_variants, new_variants)):
        allowed = set(targets.get(idx, []))
        if not allowed:
            if _stable(old_v) != _stable(new_v):
                raise ValueError(f"repair altered untargeted variant[{idx}]")
            continue
        for key, old_value in old_v.items():
            if key in allowed or key in {"field_sources", "missing_grounded_fields", "source_indexes", "support_level"}:
                continue
            if _stable(old_value) != _stable(new_v.get(key)):
                raise ValueError(f"repair altered untargeted variant[{idx}].{key}")
        for field in allowed:
            patched["technical_variants_il"][idx][field] = new_v.get(field)
        for meta in ("field_sources", "missing_grounded_fields", "source_indexes", "support_level"):
            if meta in new_v:
                patched["technical_variants_il"][idx][meta] = copy.deepcopy(new_v[meta])
    if _stable(existing.get("sources")) != _stable(repaired.get("sources")):
        patched["sources"] = copy.deepcopy(repaired.get("sources", []))
    patched["available_values_for_website"] = derive_available_values(patched.get("technical_variants_il") or [])
    return patched


def repair_review_models(
    batch: Optional[int] = None,
    *,
    selected_keys: Optional[list[str]] = None,
    provider_settings: Optional[CatalogProviderSettings] = None,
    settings: Optional[CatalogClientSettings] = None,
    log: Optional[Callable[[str], None]] = None,
    catalog_path: str = CATALOG_OUTPUT_PATH,
    readiness_path: str = READINESS_OUTPUT_PATH,
    review_path: str = REVIEW_OUTPUT_PATH,
) -> Dict[str, Any]:
    emit = log or (lambda _msg: None)
    if provider_settings is None:
        settings = settings or CatalogClientSettings()
        provider_settings = CatalogProviderSettings(
            provider="openai", display_name="GPT-5.4", model_id=settings.model_id,
            api_key=settings.api_key, web_search_enabled=settings.use_web_search
        )
    settings = settings or CatalogClientSettings(api_key=provider_settings.api_key, model_id=provider_settings.model_id, use_web_search=provider_settings.web_search_enabled)
    if not provider_settings.api_key:
        raise ValueError("Selected provider API key is missing; repair was not started.")
    client = build_catalog_client(provider_settings)
    catalog, readiness, review = load_existing_outputs(catalog_path, readiness_path, review_path)
    review_models = [m for m in review.get("models", []) if isinstance(m, dict)]
    processed = promoted = kept = skipped = 0
    new_ready: List[Dict[str, Any]] = []
    new_review: List[Dict[str, Any]] = []

    selected_set = set(selected_keys or [])
    for model_entry in review_models:
        key = _model_key(model_entry)
        if selected_keys is not None and key not in selected_set:
            skipped += 1
            continue
        if batch is not None and not selected_keys and processed >= batch:
            break
        attempts = int(model_entry.get("repair_attempts", 0) or 0)
        if attempts >= MAX_REPAIR_ATTEMPTS:
            skipped += 1
            emit(f"SKIP exhausted: {key}")
            continue
        targets = derive_repair_targets(model_entry)
        emit(f"REPAIRING WITH {provider_settings.display_name}: {key} | {targets or 'stale block; re-validating only'}")
        processed += 1
        try:
            if targets:
                repaired = client.build_repair_profile(model_entry.get("make", ""), model_entry.get("model", ""), model_entry, targets)
                patched = merge_repair(model_entry, repaired, targets)
            else:
                patched = dict(model_entry)
            result = validate_profile(patched)
            if result.ready:
                new_ready.append(result.profile)
                promoted += 1
                emit(f"PROMOTE {key}")
            else:
                kept_entry = dict(result.profile)
                kept_entry["validation_issues"] = result.issues
                kept_entry["repair_attempts"] = attempts + 1
                if kept_entry["repair_attempts"] >= MAX_REPAIR_ATTEMPTS:
                    kept_entry["repair_exhausted"] = True
                new_review.append(kept_entry)
                kept += 1
                emit(f"KEEP {key}: {len(result.issues)} issue(s)")
        except Exception as exc:  # noqa: BLE001
            failed = dict(model_entry)
            failed["repair_attempts"] = attempts + 1
            failed["last_repair_error"] = sanitize_error(exc)
            if failed["repair_attempts"] >= MAX_REPAIR_ATTEMPTS:
                failed["repair_exhausted"] = True
            new_review.append(failed)
            kept += 1
            emit(f"KEEP {key}: repair failed: {sanitize_error(exc)}")

    merged_catalog, merged_readiness, merged_review = merge_and_write_outputs(
        new_ready,
        new_review,
        settings=settings,
        checkpoint_state={
            "github_checkpoint_count": readiness.get("github_checkpoint_count", 0),
            "last_checkpointed_profile_id": readiness.get("last_checkpointed_profile_id"),
        },
        catalog_path=catalog_path,
        readiness_path=readiness_path,
        review_path=review_path,
    )
    return {"selected": selected_keys or [], "processed": processed, "promoted": promoted, "kept": kept, "skipped": skipped, "catalog": merged_catalog, "readiness": merged_readiness, "review": merged_review}
