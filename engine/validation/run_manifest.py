"""Run manifest writer — writes a persistent manifest after every validation run.

Output: data/validation/manifest.json
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from core.paths import (
    MANIFEST_PATH,
    SOURCE_CANONICAL_PATH,
    VALIDATION_REPORT_PATH,
)
from engine.validation.write_guard import safe_write_json
from engine.validation.seed_accounting import compute_seed_accounting


def _get_git_info() -> tuple[str, str]:
    """Try to resolve current repo and branch from git."""
    repo = ""
    branch = ""
    try:
        repo = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        pass
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        pass
    return repo, branch


def write_run_manifest(
    *,
    validation_run_id: str,
    mode: str,
    started_at: str,
    completed_at: str,
    canonical: dict,
    seeds: list[dict],
    stages_completed: list[dict],
    model_items_selected: list[dict] | None = None,
    targeted_seed_id: str | None = None,
    output_path: str | Path = MANIFEST_PATH,
) -> dict:
    """Write the run manifest and return it."""
    git_repo, git_branch = _get_git_info()

    verified = canonical.get("verified_variants") or []
    partial = canonical.get("partial_variants") or []

    seed_acct = compute_seed_accounting(canonical, seeds)
    bs = canonical.get("batch_state") or {}

    manifest = {
        "validation_run_id": validation_run_id,
        "mode": mode,
        "started_at": started_at,
        "completed_at": completed_at,
        "github_repo": git_repo,
        "github_branch": git_branch,
        "source_canonical_path": SOURCE_CANONICAL_PATH,
        "source_canonical_variant_count": len(verified) + len(partial),
        "source_canonical_verified_count": len(verified),
        "source_canonical_partial_count": len(partial),
        "seed_catalog_path": "data/seeds/vehicle_model_seeds_il.json",
        "seed_catalog_count": seed_acct["seed_catalog_count"],
        "batch_state_total_seeds": len(set(
            (bs.get("processed_seed_ids") or []) +
            (bs.get("failed_seed_ids") or []) +
            (bs.get("manual_review_seed_ids") or [])
        )),
        "batch_state_processed_seed_ids_count": seed_acct["processed_exact_count"],
        "true_catalog_processed_count": seed_acct["processed_in_catalog_count"],
        "catalog_not_processed_seed_ids": seed_acct["catalog_not_processed"],
        "processed_not_in_catalog_seed_ids": seed_acct["processed_not_in_catalog"],
        "logical_seed_id_alias_warnings": seed_acct["logical_seed_id_alias_warnings"],
        "targeted_seed_id": targeted_seed_id,
        "stages_completed": stages_completed,
        "model_items_selected": model_items_selected or [],
        "validation_working_package_file": "data/validated_runs/resume_package_canonical_validated_v2.json",
        "model_validation_output_file": "data/validated_runs/model_validation_results_v2.json",
        "report_file": VALIDATION_REPORT_PATH,
    }

    safe_write_json(manifest, output_path)
    return manifest
