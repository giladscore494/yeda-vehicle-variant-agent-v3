"""Orchestrate the single-GPT-5.4 Israeli model technical-catalog build.

Flow (no per-row validation, no Gemini, no legacy guard/repair):

1. Load the two source files (variants + optional instruction metadata).
2. Group variants by ``market_scope + make + model``.
3. For each cluster, send ONE GPT-5.4 request (or synthesize offline).
4. Python validates the returned profile, de-dupes, derives website values.
5. Ready profiles → main catalog; blocked profiles → review output.
6. Write the three new output files.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from .catalog_checkpoint import CatalogCheckpointConfig, CatalogCheckpointer
from .catalog_grouping import ModelGroup, group_variants, select_groups
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
    "OPENAI_API_KEY is required for real GPT-5.4 grounded catalog runs. Set it "
    "in environment variables or secrets. Use --offline only for plumbing tests."
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
    offline: bool = False,
    settings: Optional[CatalogClientSettings] = None,
    checkpoint: Optional[CatalogCheckpointConfig] = None,
    variants_path: str = VARIANTS_PATH,
    instructions_path: str = INSTRUCTIONS_PATH,
    catalog_path: str = CATALOG_OUTPUT_PATH,
    readiness_path: str = READINESS_OUTPUT_PATH,
    review_path: str = REVIEW_OUTPUT_PATH,
    log: Optional[Callable[[str], None]] = None,
) -> BuildResult:
    """Build the model technical catalog and write the three output files.

    A real run requires ``OPENAI_API_KEY`` (via ``settings.api_key``) and uses
    GPT-5.4 with web_search grounding. ``offline=True`` uses the deterministic
    offline synthesizer so the pipeline can be exercised without network — its
    output is always marked as a stub and never website-ready.

    When ``checkpoint`` is enabled the generated files are pushed to GitHub
    after each completed model profile (never after each raw variant).
    """
    emit = log or (lambda _msg: None)
    settings = settings or CatalogClientSettings()
    online = not offline

    # Fail fast for real runs without an OpenAI key (offline is the only escape).
    if online and not settings.api_key:
        raise ValueError(OPENAI_KEY_REQUIRED_MESSAGE)

    web_search_enabled = bool(online and settings.use_web_search)

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
    groups = select_groups(all_groups, make=make, model=model, limit_models=limit_models)
    emit(
        f"Grouped {len(variants)} variants into {len(all_groups)} model clusters; "
        f"processing {len(groups)} this run."
    )

    client = CatalogClient(settings)
    if not online:
        emit("Running OFFLINE (offline stub); synthesizing profiles — never website-ready.")

    validations: List[ProfileValidation] = []
    ready_models: List[Dict[str, Any]] = []
    review_models: List[Dict[str, Any]] = []

    def _snapshot() -> tuple:
        catalog = {
            "generated_at": _now_iso(),
            "market": "IL",
            "mode": "online_gpt54" if online else "offline_synthesized",
            "offline_stub": not online,
            "ready_for_website_upload": online,  # gated again by readiness report
            "source_files": SOURCE_FILES,
            "models": ready_models,
        }
        readiness = build_readiness_report(
            validations,
            online=online,
            web_search_enabled=web_search_enabled,
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

    catalog: Dict[str, Any] = {}
    readiness: Dict[str, Any] = {}
    review: Dict[str, Any] = {}

    for group in groups:
        payload = group.request_payload()
        try:
            if online:
                profile = client.build_profile(payload)
            else:
                profile = CatalogClient.synthesize_offline(payload)
        except Exception as exc:  # noqa: BLE001 - keep building other models
            emit(f"[{group.key}] model call failed: {exc}")
            review_models.append(
                {
                    "make": group.make,
                    "model": group.model,
                    "error": str(exc),
                    "request_payload": payload,
                }
            )
            catalog, readiness, review = _snapshot()
            continue

        result = validate_profile(profile)
        validations.append(result)
        entry = result.profile
        emit(
            f"[{group.key}] variants={result.stats.get('technical_variant_count', 0)} "
            f"ready={result.ready} issues={len(result.issues)}"
        )
        if result.ready:
            ready_models.append(entry)
        else:
            review_entry = dict(entry)
            review_entry["validation_issues"] = result.issues
            review_models.append(review_entry)

        # Write the three files, then checkpoint AFTER this completed profile.
        catalog, readiness, review = _snapshot()
        profile_id = f"{group.market_scope or 'IL'}::{group.make}::{group.model}"
        checkpointer.maybe_checkpoint(
            profile_id=profile_id,
            paths=[catalog_path, readiness_path, review_path],
            market=group.market_scope or "IL",
            make=group.make,
            model=group.model,
        )

    # Ensure files exist even when no group was processed.
    if not catalog:
        catalog, readiness, review = _snapshot()

    # Re-write readiness one last time so the final checkpoint counters land.
    readiness = build_readiness_report(
        validations,
        online=online,
        web_search_enabled=web_search_enabled,
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
