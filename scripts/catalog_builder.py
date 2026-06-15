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
from .openai_catalog_client import CatalogClient, CatalogClientSettings

CATALOG_OUTPUT_PATH = os.path.join(DATA_DIR, "model_technical_catalog_il.json")
READINESS_OUTPUT_PATH = os.path.join(DATA_DIR, "model_technical_catalog_il_readiness.json")
REVIEW_OUTPUT_PATH = os.path.join(DATA_DIR, "model_technical_catalog_il_review.json")

SOURCE_FILES = [
    "data/validation_variants_data_v1.json",
    "data/validation_instructions_by_id_v1.json",
]

OPENAI_KEY_REQUIRED_MESSAGE = (
    "OPENAI_API_KEY is required for GPT-5.4 grounded catalog runs. Set it in "
    "environment variables or secrets."
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atomic_write_json(path: str, payload: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


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
    settings = settings or CatalogClientSettings()

    # Fail closed: a run without an OpenAI key never continues, synthesizes, or
    # falls back.
    if not settings.api_key:
        raise ValueError(OPENAI_KEY_REQUIRED_MESSAGE)

    # GITHUB_TOKEN is required only when checkpointing is enabled (constructor
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

    client = CatalogClient(settings)

    validations: List[ProfileValidation] = []
    ready_models: List[Dict[str, Any]] = []
    review_models: List[Dict[str, Any]] = []
    processed = 0
    ready_count = 0
    review_count = 0

    def _snapshot() -> tuple:
        catalog = {
            "generated_at": _now_iso(),
            "market": "IL",
            "mode": "online_gpt54",
            "model_id": settings.model_id,
            "source_files": SOURCE_FILES,
            "models": ready_models,
        }
        readiness = build_readiness_report(
            validations,
            web_search_enabled=True,
            checkpoint_state=checkpointer.state,
        )
        catalog["ready_for_website_upload"] = readiness["ready_for_website_upload"]
        review = {
            "generated_at": _now_iso(),
            "market": "IL",
            "models": review_models,
        }
        _atomic_write_json(catalog_path, catalog)
        _atomic_write_json(readiness_path, readiness)
        _atomic_write_json(review_path, review)
        return catalog, readiness, review

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
            f"[{idx}/{total}] RUNNING GPT-5.4: {market} :: {group.make} :: "
            f"{group.model} | raw_variants={group.raw_variant_count} | "
            f"sample_ids={', '.join(sample_ids) or '(none)'}"
        )
        _emit_progress(group, idx, "running")

        try:
            profile = client.build_profile(payload)
        except Exception as exc:  # noqa: BLE001 - keep building other models
            review_count += 1
            emit(f"[{idx}/{total}] ERROR: {group.make} {group.model} routed to review: {exc}")
            review_models.append(
                {
                    "make": group.make,
                    "model": group.model,
                    "error": str(exc),
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
        catalog, readiness, review = _snapshot()
        profile_id = f"{market}::{group.make}::{group.model}"
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

    # Re-write readiness one last time so the final checkpoint counters land.
    readiness = build_readiness_report(
        validations,
        web_search_enabled=True,
        checkpoint_state=checkpointer.state,
    )
    _atomic_write_json(readiness_path, readiness)

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
