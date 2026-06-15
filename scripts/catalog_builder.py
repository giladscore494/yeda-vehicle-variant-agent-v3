"""Orchestrate the GPT-5.4 Israeli model technical-catalog build.

One production path only (GPT-5.4 is the only model):

1. Load the two source files (variants + optional instruction metadata).
2. Group variants by ``market_scope + make + model``.
3. For each cluster, send ONE grounded GPT-5.4 request (web_search).
4. Python validates the returned profile, de-dupes, derives website values.
5. Ready profiles → main catalog; blocked profiles → review output.
6. Write the three output files (atomically).

A run always requires ``OPENAI_API_KEY`` (via ``settings.api_key``); there is no
escape that runs without it.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from .catalog_checkpoint import CatalogCheckpointConfig, CatalogCheckpointer
from .catalog_grouping import group_variants, select_groups
from .catalog_validation import (
    ProfileValidation,
    build_readiness_report,
    validate_profile,
)
from .data_loader import (
    DATA_DIR,
    INSTRUCTIONS_PATH,
    VARIANTS_PATH,
    load_instructions,
    load_variants,
)
from .openai_catalog_client import CatalogClientSettings
from .catalog_provider import CatalogProviderSettings, build_catalog_client
from .security import sanitize_error

CATALOG_OUTPUT_PATH = os.path.join(DATA_DIR, "model_technical_catalog_il.json")
READINESS_OUTPUT_PATH = os.path.join(DATA_DIR, "model_technical_catalog_il_readiness.json")
REVIEW_OUTPUT_PATH = os.path.join(DATA_DIR, "model_technical_catalog_il_review.json")

SOURCE_FILES = [
    "data/validation_variants_data_v1.json",
    "data/validation_instructions_by_id_v1.json",
]

MODEL_KEY_REQUIRED_MESSAGE = "Selected provider API key is missing; the run was not started."


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atomic_write_json(path: str, payload: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def _load_json_file(path: str, default: Any) -> Any:
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default


def _model_key(model: Dict[str, Any]) -> str:
    market = model.get("market") or "IL"
    return f"{market}|{model.get('make', '')}|{model.get('model', '')}"


def _profile_id_to_group_key(profile_id: Optional[str]) -> Optional[str]:
    if not profile_id:
        return None
    parts = str(profile_id).split("::")
    if len(parts) == 3:
        return "|".join(parts)
    return str(profile_id).replace("::", "|")


def _sort_models(models: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(models, key=lambda m: (str(m.get("make", "")).lower(), str(m.get("model", "")).lower()))


def load_existing_outputs(
    catalog_path: str = CATALOG_OUTPUT_PATH,
    readiness_path: str = READINESS_OUTPUT_PATH,
    review_path: str = REVIEW_OUTPUT_PATH,
) -> tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    return (
        _load_json_file(catalog_path, {"models": []}),
        _load_json_file(readiness_path, {}),
        _load_json_file(review_path, {"models": []}),
    )


def merge_and_write_outputs(
    new_ready: List[Dict[str, Any]],
    new_review: List[Dict[str, Any]],
    *,
    settings: CatalogClientSettings,
    checkpoint_state: Optional[Dict[str, Any]] = None,
    catalog_path: str = CATALOG_OUTPUT_PATH,
    readiness_path: str = READINESS_OUTPUT_PATH,
    review_path: str = REVIEW_OUTPUT_PATH,
) -> tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    old_catalog, old_readiness, old_review = load_existing_outputs(catalog_path, readiness_path, review_path)
    ready_by_key = {_model_key(m): m for m in old_catalog.get("models", []) if isinstance(m, dict)}
    review_by_key = {_model_key(m): m for m in old_review.get("models", []) if isinstance(m, dict)}
    for entry in new_ready:
        key = _model_key(entry)
        ready_by_key[key] = entry
        review_by_key.pop(key, None)
    for entry in new_review:
        key = _model_key(entry)
        review_by_key[key] = entry
        ready_by_key.pop(key, None)
    ready_models = _sort_models(list(ready_by_key.values()))
    review_models = _sort_models(list(review_by_key.values()))
    validations = [validate_profile(m) for m in ready_models]
    for m in review_models:
        validations.append(validate_profile(m))
    readiness = build_readiness_report(validations, web_search_enabled=True, checkpoint_state=checkpoint_state or {})
    if old_readiness.get("last_checkpointed_profile_id") and not readiness.get("last_checkpointed_profile_id"):
        readiness["last_checkpointed_profile_id"] = old_readiness.get("last_checkpointed_profile_id")
    catalog = {
        "generated_at": _now_iso(), "market": "IL", "mode": "online_selectable_provider",
        "model_id": settings.model_id, "source_files": SOURCE_FILES, "models": ready_models,
    }
    catalog["ready_for_website_upload"] = readiness["ready_for_website_upload"]
    review = {"generated_at": _now_iso(), "market": "IL", "models": review_models}
    _atomic_write_json(catalog_path, catalog)
    _atomic_write_json(readiness_path, readiness)
    _atomic_write_json(review_path, review)
    return catalog, readiness, review


def compute_resume_state(
    *,
    variants_path: str = VARIANTS_PATH,
    instructions_path: str = INSTRUCTIONS_PATH,
    catalog_path: str = CATALOG_OUTPUT_PATH,
    readiness_path: str = READINESS_OUTPUT_PATH,
    review_path: str = REVIEW_OUTPUT_PATH,
) -> Dict[str, Any]:
    variants = load_variants(variants_path)
    try:
        instructions = load_instructions(instructions_path)
    except Exception:
        instructions = {}
    groups = group_variants(variants, instructions)
    catalog, readiness, review = load_existing_outputs(catalog_path, readiness_path, review_path)
    keys = {_model_key(m) for m in catalog.get("models", []) if isinstance(m, dict)} | {_model_key(m) for m in review.get("models", []) if isinstance(m, dict)}
    next_key = _profile_id_to_group_key(readiness.get("last_checkpointed_profile_id"))
    if not next_key and keys:
        ordered = [g.key for g in groups if g.key in keys]
        next_key = ordered[-1] if ordered else sorted(keys)[-1]
    done = len(keys)
    ready = int(readiness.get("models_ready_for_website") or len(catalog.get("models", [])))
    blocked = int(readiness.get("models_blocked") or len(review.get("models", [])))
    total = len(groups)
    upcoming = select_groups(groups, start_after_key=next_key, limit_models=1)
    return {"next_key": next_key, "total_universe": total, "done": done, "ready": ready, "blocked": blocked, "remaining": max(total - done, 0), "next_make": upcoming[0].make if upcoming else None, "next_model": upcoming[0].model if upcoming else None}


@dataclass
class BuildResult:
    catalog: Dict[str, Any]
    readiness: Dict[str, Any]
    review: Dict[str, Any]
    catalog_path: str
    readiness_path: str
    review_path: str


def build_catalog(
    *,
    make: Optional[str] = None,
    model: Optional[str] = None,
    limit_models: Optional[int] = None,
    start_after_key: Optional[str] = None,
    settings: Optional[CatalogClientSettings] = None,
    provider_settings: Optional[CatalogProviderSettings] = None,
    checkpoint: Optional[CatalogCheckpointConfig] = None,
    variants_path: str = VARIANTS_PATH,
    instructions_path: str = INSTRUCTIONS_PATH,
    catalog_path: str = CATALOG_OUTPUT_PATH,
    readiness_path: str = READINESS_OUTPUT_PATH,
    review_path: str = REVIEW_OUTPUT_PATH,
    log: Optional[Callable[[str], None]] = None,
    on_progress: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> BuildResult:
    """Build the model technical catalog and write the three output files.

    Always uses GPT-5.4 with web_search grounding and requires
    ``OPENAI_API_KEY`` (via ``settings.api_key``); it fails closed otherwise.

    When ``checkpoint`` is enabled the generated files are pushed to GitHub
    after each completed model profile (never after each raw variant).
    """
    emit = log or (lambda _msg: None)
    progress = on_progress or (lambda _info: None)
    if provider_settings is None:
        settings = settings or CatalogClientSettings()
        provider_settings = CatalogProviderSettings(
            provider="openai",
            display_name="GPT-5.4",
            model_id=settings.model_id,
            api_key=settings.api_key,
            web_search_enabled=settings.use_web_search,
        )
    settings = settings or CatalogClientSettings(
        api_key=provider_settings.api_key,
        model_id=provider_settings.model_id,
        use_web_search=provider_settings.web_search_enabled,
    )

    if not provider_settings.api_key:
        raise ValueError(MODEL_KEY_REQUIRED_MESSAGE)

    # [github].token is required only when checkpointing is enabled (constructor
    # raises a clear, sanitized error if so and the token is missing).
    checkpointer = CatalogCheckpointer(
        checkpoint or CatalogCheckpointConfig(), log=emit
    )

    variants = load_variants(variants_path)
    try:
        instructions = load_instructions(instructions_path)
    except Exception as exc:  # instructions are optional metadata only
        emit(f"instructions metadata unavailable ({exc}); continuing without hints")
        instructions = {}

    all_groups = group_variants(variants, instructions)
    groups = select_groups(
        all_groups,
        make=make,
        model=model,
        limit_models=limit_models,
        start_after_key=start_after_key,
    )
    total = len(groups)
    emit(
        f"Grouped {len(variants)} variants into {len(all_groups)} model clusters; "
        f"processing {total} this run."
    )

    client = build_catalog_client(provider_settings)

    validations: List[ProfileValidation] = []
    ready_models: List[Dict[str, Any]] = []
    review_models: List[Dict[str, Any]] = []
    processed = 0
    ready_count = 0
    review_count = 0

    def _snapshot() -> tuple:
        return merge_and_write_outputs(
            ready_models,
            review_models,
            settings=settings,
            checkpoint_state=checkpointer.state,
            catalog_path=catalog_path,
            readiness_path=readiness_path,
            review_path=review_path,
        )

    def _emit_progress(group, idx: int, phase: str, result=None) -> None:
        info = {
            "phase": phase,
            "index": idx,
            "total": total,
            "make": group.make,
            "model": group.model,
            "market_scope": group.market_scope or "IL",
            "raw_variants": group.raw_variant_count,
            "validation_ids": group.validation_ids[:5],
            "source_indexes": group.source_indexes[:25],
            "processed": processed,
            "ready": ready_count,
            "review": review_count,
        }
        if result is not None:
            info["technical_variants"] = result.stats.get("technical_variant_count", 0)
            info["ready_profile"] = result.ready
            info["issues"] = len(result.issues)
        progress(info)

    catalog: Dict[str, Any] = {}
    readiness: Dict[str, Any] = {}
    review: Dict[str, Any] = {}

    for idx, group in enumerate(groups, start=1):
        payload = group.request_payload()
        sample_ids = group.validation_ids[:5]
        market = group.market_scope or "IL"
        emit(
            f"[{idx}/{total}] RUNNING {provider_settings.display_name}: {market} :: {group.make} :: "
            f"{group.model} | raw_variants={group.raw_variant_count} | "
            f"sample_ids={', '.join(sample_ids) or '(none)'}"
        )
        _emit_progress(group, idx, "running")

        try:
            profile = client.build_profile(payload)
        except Exception as exc:  # noqa: BLE001 - keep building other models
            review_count += 1
            safe_error = sanitize_error(exc)
            emit(f"[{idx}/{total}] ERROR: {group.make} {group.model} routed to review: {safe_error}")
            review_models.append(
                {
                    "make": group.make,
                    "model": group.model,
                    "error": safe_error,
                    "request_payload": payload,
                }
            )
            catalog, readiness, review = _snapshot()
            _emit_progress(group, idx, "error")
            continue

        result = validate_profile(profile)
        validations.append(result)
        entry = result.profile
        processed += 1
        if result.ready:
            ready_count += 1
            ready_models.append(entry)
        else:
            review_count += 1
            review_entry = dict(entry)
            review_entry["validation_issues"] = result.issues
            review_models.append(review_entry)

        emit(
            f"[{idx}/{total}] DONE: {group.make} {group.model} | "
            f"technical_variants={result.stats.get('technical_variant_count', 0)} | "
            f"ready={str(result.ready).lower()} | issues={len(result.issues)}"
        )

        # Write the three files, then checkpoint AFTER this completed profile.
        profile_id = f"{market}::{group.make}::{group.model}"
        checkpointer.state["last_checkpointed_profile_id"] = profile_id
        catalog, readiness, review = _snapshot()
        checkpointer.maybe_checkpoint(
            profile_id=profile_id,
            paths=[catalog_path, readiness_path, review_path],
            market=market,
            make=group.make,
            model=group.model,
        )
        _emit_progress(group, idx, "done", result=result)

    # Ensure files exist even when no group was processed.
    if not catalog:
        catalog, readiness, review = _snapshot()

    catalog, readiness, review = _snapshot()

    emit(
        f"Wrote catalog ({len(ready_models)} ready) + readiness + review "
        f"({len(review_models)} blocked). "
        f"github_checkpoints={checkpointer.state['github_checkpoint_count']} "
        f"fails={checkpointer.state['github_checkpoint_fail_count']}."
    )

    return BuildResult(
        catalog=catalog,
        readiness=readiness,
        review=review,
        catalog_path=catalog_path,
        readiness_path=readiness_path,
        review_path=review_path,
    )
