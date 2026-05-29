"""Validation engine CLI entrypoint.

Usage:
    python -m engine.normalize_validate \\
        --input "resume_package_canonical (23).json" \\
        --output-dir data/validated_runs \\
        --mode targeted-dual-validation \\
        --primary-model gemini-3.1-pro \\
        --reviewer-model gpt-5.4 \\
        --resume true \\
        --group-level true \\
        --enable-repo-write true \\
        --target-branch validation-v2-budgeted-dual-il-trims

Dry run:
    python -m engine.normalize_validate \\
        --input "resume_package_canonical (23).json" \\
        --output-dir data/validated_runs \\
        --mode targeted-dual-validation \\
        --resume true \\
        --group-level true \\
        --enable-repo-write false \\
        --dry-run true
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Setup logging ────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("validation_engine")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    _run_validation(args)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Vehicle variant validation engine",
        prog="python -m engine.normalize_validate",
    )
    p.add_argument("--input", required=True, help="Path to input resume package JSON")
    p.add_argument("--output-dir", default="data/validated_runs", help="Output directory")
    p.add_argument("--mode", default="targeted-dual-validation",
                   choices=["targeted-dual-validation", "exhaustive", "dry-run"])
    p.add_argument("--primary-model", default=None, help="Gemini model ID override")
    p.add_argument("--reviewer-model", default=None, help="OpenAI model ID override")
    p.add_argument("--resume", default="true", help="Resume from checkpoint (true/false)")
    p.add_argument("--group-level", default="true", help="Use group-level validation (true/false)")
    p.add_argument("--enable-repo-write", default="false", help="Push to GitHub (true/false)")
    p.add_argument("--target-branch", default=None, help="Target branch for GitHub push")
    p.add_argument("--dry-run", default="false", help="Dry run mode (true/false)")
    return p.parse_args(argv)


def _bool_arg(val: str) -> bool:
    return val.lower() in ("true", "1", "yes")


def _run_validation(args: argparse.Namespace) -> None:
    """Main validation pipeline."""
    from engine import config
    from engine.validation.normalizer import safe_str, extract_value
    from engine.validation.group_builder import (
        build_groups,
        get_group_trim_candidates,
        group_needs_variant_level,
    )
    from engine.validation.risk_scorer import (
        score_variant,
        score_group,
        classify_risk,
        determine_action,
    )
    from engine.validation.cost_tracker import CostTracker
    from engine.validation.decision_resolver import (
        resolve_variant_decision,
        AuditWriter,
    )
    from engine.validation.output_writer import (
        build_validated_variant,
        write_validated_package,
        write_last_validation_run,
    )
    from engine.validation.schema_guard import (
        run_hard_gates,
        check_duplicate_variant_ids,
        compute_input_hash,
        SchemaGuardError,
    )

    started_at = datetime.now(timezone.utc).isoformat()
    dry_run = _bool_arg(args.dry_run) or args.mode == "dry-run"
    use_groups = _bool_arg(args.group_level)
    resume = _bool_arg(args.resume)
    enable_repo_write = _bool_arg(args.enable_repo_write)

    # Apply model overrides
    if args.primary_model:
        os.environ["GEMINI_VALIDATOR_MODEL_ID"] = args.primary_model
    if args.reviewer_model:
        os.environ["OPENAI_VALIDATOR_MODEL_ID"] = args.reviewer_model
    if args.target_branch:
        os.environ["GITHUB_TARGET_BRANCH"] = args.target_branch

    # ── Resolve paths ────────────────────────────────────────────────
    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = (output_dir / "resume_package_canonical_validated_v2.json").resolve()

    # Safety checks
    if input_path == output_path:
        raise RuntimeError("Refusing to overwrite source resume package")
    if "validated_runs" not in str(output_path):
        raise RuntimeError(f"Output must be under data/validated_runs/: {output_path}")

    logger.info("Input:  %s", input_path)
    logger.info("Output: %s", output_path)
    logger.info("Mode:   %s (dry_run=%s, groups=%s)", args.mode, dry_run, use_groups)

    # ── Load input ───────────────────────────────────────────────────
    if not input_path.exists():
        logger.error("Input file not found: %s", input_path)
        sys.exit(1)

    input_hash = compute_input_hash(input_path)
    with open(input_path, "r", encoding="utf-8") as f:
        package = json.load(f)

    # Extract all variants
    all_variants = list(package.get("verified_variants", []))
    all_variants.extend(package.get("partial_variants", []))
    logger.info("Loaded %d variants from input", len(all_variants))

    if not all_variants:
        logger.error("No variants found in input package")
        sys.exit(1)

    # ── Initialize tracking ──────────────────────────────────────────
    cost_tracker = CostTracker(output_dir)
    audit_writer = AuditWriter(output_dir)
    checkpoint_dir = output_dir / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    # ── Load checkpoint if resuming ──────────────────────────────────
    completed_variant_ids: set[str] = set()
    completed_group_keys: set[str] = set()
    checkpoint_path = checkpoint_dir / "validation_checkpoint.json"

    if resume and checkpoint_path.exists():
        try:
            with open(checkpoint_path, "r", encoding="utf-8") as f:
                cp = json.load(f)
            completed_variant_ids = set(cp.get("completed_variant_ids", []))
            completed_group_keys = set(cp.get("completed_group_keys", []))
            cost_tracker.cumulative_cost_usd = cp.get("cumulative_cost_usd", 0.0)
            logger.info(
                "Resumed from checkpoint: %d variants, %d groups completed",
                len(completed_variant_ids), len(completed_group_keys),
            )
        except Exception as exc:
            logger.warning("Failed to load checkpoint: %s — starting fresh", exc)

    # ── Phase 1: Score all variants ──────────────────────────────────
    logger.info("Phase 1: Scoring variants...")
    variant_scores: dict[str, int] = {}
    risk_counts: dict[str, int] = {"low": 0, "medium": 0, "high": 0, "critical": 0}

    for v in all_variants:
        vid = v.get("variant_id", "")
        score = score_variant(v)
        variant_scores[vid] = score
        risk_counts[classify_risk(score)] += 1

    logger.info("Risk distribution: %s", risk_counts)

    # ── Phase 2: Build groups ────────────────────────────────────────
    logger.info("Phase 2: Building groups...")
    groups = build_groups(all_variants) if use_groups else {
        v.get("variant_id", f"single_{i}"): [v]
        for i, v in enumerate(all_variants)
    }
    logger.info("Built %d groups from %d variants", len(groups), len(all_variants))

    # ── Phase 3: Validate groups ─────────────────────────────────────
    logger.info("Phase 3: Validating groups...")
    variant_decisions: dict[str, dict] = {}
    failed_calls: list[dict] = []
    pending_groups: list[str] = []

    for group_idx, (group_key, group_variants) in enumerate(groups.items()):
        # Skip completed groups
        if group_key in completed_group_keys:
            # Mark variants as already done
            for v in group_variants:
                vid = v.get("variant_id", "")
                if vid not in variant_decisions:
                    variant_decisions[vid] = {
                        "validation_status": "trusted_existing_deterministic",
                        "validation_confidence": "high",
                        "quality_flags": ["resumed_from_checkpoint"],
                        "trim_action": "keep",
                        "corrected_trim": None,
                        "source_refs": [],
                        "model_audit_refs": [],
                        "reason": "Resumed from checkpoint",
                    }
            continue

        group_score = score_group(group_variants)
        group_risk = classify_risk(group_score)
        action = determine_action(group_risk)
        trim_candidates = get_group_trim_candidates(group_variants)

        if group_idx % 100 == 0:
            logger.info(
                "Processing group %d/%d: %s (risk=%s, action=%s)",
                group_idx + 1, len(groups), group_key[:60], group_risk, action,
            )

        gemini_result = None
        openai_result = None

        if action == "trusted_existing_deterministic":
            # No model call needed
            pass

        elif action == "gemini_only" and not dry_run:
            # Medium risk — Gemini only
            try:
                from engine.validation.providers.gemini_validator import validate_group
                gemini_result = validate_group(
                    group_key, group_variants, trim_candidates, cost_tracker
                )
            except Exception as exc:
                logger.error("Gemini validation failed for %s: %s", group_key, exc)
                failed_calls.append({
                    "group_key": group_key,
                    "provider": "gemini",
                    "error": str(exc),
                })

        elif action in ("gemini_and_openai", "dual_model_required") and not dry_run:
            # High/critical risk — both models
            try:
                from engine.validation.providers.gemini_validator import validate_group
                gemini_result = validate_group(
                    group_key, group_variants, trim_candidates, cost_tracker
                )
            except Exception as exc:
                logger.error("Gemini validation failed for %s: %s", group_key, exc)
                failed_calls.append({
                    "group_key": group_key,
                    "provider": "gemini",
                    "error": str(exc),
                })

            try:
                from engine.validation.providers.openai_reviewer import review_group
                openai_result = review_group(
                    group_key, group_variants, trim_candidates,
                    gemini_result=gemini_result,
                    cost_tracker=cost_tracker,
                )
            except Exception as exc:
                logger.error("OpenAI review failed for %s: %s", group_key, exc)
                failed_calls.append({
                    "group_key": group_key,
                    "provider": "openai",
                    "error": str(exc),
                })

        elif dry_run and action != "trusted_existing_deterministic":
            pending_groups.append(group_key)

        # Resolve decisions for each variant in group
        for v in group_variants:
            vid = v.get("variant_id", "")
            original_status = v.get("verification_status", "unknown")

            decision = resolve_variant_decision(
                vid, group_risk, gemini_result, openai_result
            )
            decision["risk_score"] = variant_scores.get(vid, 0)
            variant_decisions[vid] = decision

            audit_writer.log_decision(v, group_key, decision, original_status)
            completed_variant_ids.add(vid)

        completed_group_keys.add(group_key)

        # Checkpoint every 50 groups
        if (group_idx + 1) % 50 == 0:
            _save_checkpoint(
                checkpoint_dir, completed_variant_ids, completed_group_keys,
                pending_groups, failed_calls, cost_tracker,
            )

        # Runaway check
        runaway = cost_tracker.check_runaway()
        if runaway:
            logger.error("Runaway detected: %s", runaway)
            _save_checkpoint(
                checkpoint_dir, completed_variant_ids, completed_group_keys,
                pending_groups, failed_calls, cost_tracker,
            )
            break

    # ── Phase 4: Build final output ──────────────────────────────────
    logger.info("Phase 4: Building validated output...")
    validated_variants = []
    for v in all_variants:
        vid = v.get("variant_id", "")
        decision = variant_decisions.get(vid, {
            "validation_status": "pending_unchecked",
            "validation_confidence": "low",
            "quality_flags": ["not_processed"],
            "trim_action": "keep",
            "corrected_trim": None,
            "source_refs": [],
            "model_audit_refs": [],
            "reason": "Not processed in this run",
        })
        validated = build_validated_variant(v, decision)
        validated_variants.append(validated)

    # ── Phase 5: Quality gates ───────────────────────────────────────
    logger.info("Phase 5: Running quality gates...")
    try:
        gate_status, gate_warnings = run_hard_gates(
            validated_variants, output_path, input_path, input_hash
        )
    except SchemaGuardError as exc:
        logger.error("HARD GATE FAILURE: %s", exc)
        gate_status = "failed"
        gate_warnings = [str(exc)]

    duplicate_count = check_duplicate_variant_ids(validated_variants)

    # ── Phase 6: Write outputs ───────────────────────────────────────
    logger.info("Phase 6: Writing outputs...")

    # Write validated package
    write_validated_package(package, validated_variants, output_path, input_path)

    # Write trim corrections
    audit_writer.save_corrections()

    # Compute final stats
    finished_at = datetime.now(timezone.utc).isoformat()
    cost_summary = cost_tracker.summary()

    status_counts: dict[str, int] = {}
    for v in validated_variants:
        s = v.get("validation_metadata", {}).get("validation_status", "pending_unchecked")
        status_counts[s] = status_counts.get(s, 0) + 1

    counts = validated_variants[0].get("validation_metadata", {}) if validated_variants else {}
    trims_stats = {
        "trims_checked": len(audit_writer.corrections),
        "trims_corrected": sum(
            1 for c in audit_writer.corrections if c.get("action") == "correct"
        ),
        "trims_nullified": sum(
            1 for c in audit_writer.corrections if c.get("action") == "nullify"
        ),
        "trims_not_verified": sum(
            1 for v in validated_variants
            if "trim_not_verified_by_sources" in v.get("validation_metadata", {}).get("quality_flags", [])
        ),
    }

    soft_warnings = list(gate_warnings)
    soft_warnings.extend(cost_tracker.check_runaway())

    # Write last validation run
    write_last_validation_run(
        output_dir, str(input_path), str(output_path),
        config.get("github", "target_branch"),
        args.mode, started_at, finished_at,
        len(all_variants), len(groups), risk_counts,
        cost_summary, status_counts, trims_stats,
        duplicate_count, gate_status, soft_warnings,
    )

    # Save final checkpoint
    _save_checkpoint(
        checkpoint_dir, completed_variant_ids, completed_group_keys,
        pending_groups, failed_calls, cost_tracker,
    )

    # ── Phase 7: Optional GitHub push ────────────────────────────────
    if enable_repo_write and not dry_run and gate_status != "failed":
        logger.info("Phase 7: Pushing to GitHub...")
        _push_to_github(output_dir, config)
    else:
        logger.info("Skipping GitHub push (repo_write=%s, dry_run=%s, gate=%s)",
                     enable_repo_write, dry_run, gate_status)

    # ── Summary ──────────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("Validation complete!")
    logger.info("  Total variants: %d", len(all_variants))
    logger.info("  Groups: %d", len(groups))
    logger.info("  Risk: %s", risk_counts)
    logger.info("  Status: %s", status_counts)
    logger.info("  Cost: $%.4f", cost_summary.get("estimated_total_cost_usd", 0))
    logger.info("  Gate: %s", gate_status)
    logger.info("  Output: %s", output_path)
    logger.info("=" * 60)


def _save_checkpoint(
    checkpoint_dir: Path,
    completed_variant_ids: set[str],
    completed_group_keys: set[str],
    pending_groups: list[str],
    failed_calls: list[dict],
    cost_tracker,
) -> None:
    """Save checkpoint for resumability."""
    checkpoint = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "completed_variant_ids": sorted(completed_variant_ids),
        "completed_group_keys": sorted(completed_group_keys),
        "cumulative_cost_usd": cost_tracker.cumulative_cost_usd,
    }
    with open(checkpoint_dir / "validation_checkpoint.json", "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)

    with open(checkpoint_dir / "completed_group_keys.json", "w", encoding="utf-8") as f:
        json.dump(sorted(completed_group_keys), f, ensure_ascii=False, indent=2)

    with open(checkpoint_dir / "completed_variant_ids.json", "w", encoding="utf-8") as f:
        json.dump(sorted(completed_variant_ids), f, ensure_ascii=False, indent=2)

    with open(checkpoint_dir / "pending_group_keys.json", "w", encoding="utf-8") as f:
        json.dump(pending_groups, f, ensure_ascii=False, indent=2)

    with open(checkpoint_dir / "failed_validation_calls.json", "w", encoding="utf-8") as f:
        json.dump(failed_calls, f, ensure_ascii=False, indent=2)


def _push_to_github(output_dir: Path, config_module) -> None:
    """Push validation outputs to GitHub."""
    from engine.github_writer import push_file

    files_to_push = [
        "resume_package_canonical_validated_v2.json",
        "last_validation_run.json",
        "validation_audit.jsonl",
        "trim_corrections.json",
        "cost_ledger.jsonl",
        "validation_engine_discovery_report.md",
    ]

    for filename in files_to_push:
        local = output_dir / filename
        if local.exists():
            content = local.read_text(encoding="utf-8")
            remote = f"data/validated_runs/{filename}"
            result = push_file(
                content, remote,
                commit_message="Add validated vehicle variants package",
            )
            if result.get("ok"):
                logger.info("Pushed %s", remote)
            else:
                logger.error("Failed to push %s", remote)

    # Push checkpoint files
    checkpoint_dir = output_dir / "checkpoints"
    if checkpoint_dir.exists():
        for cp_file in checkpoint_dir.iterdir():
            if cp_file.is_file():
                content = cp_file.read_text(encoding="utf-8")
                remote = f"data/validated_runs/checkpoints/{cp_file.name}"
                result = push_file(
                    content, remote,
                    commit_message="Add validated vehicle variants package",
                )
                if result.get("ok"):
                    logger.info("Pushed %s", remote)


if __name__ == "__main__":
    main()
