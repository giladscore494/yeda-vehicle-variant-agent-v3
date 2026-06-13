"""CLI runner for non-UI use.

Examples:
    python scripts/run_gemini31_sampled_validation.py --mock --limit 20
    python scripts/run_gemini31_sampled_validation.py --real --limit 20
    python scripts/run_gemini31_sampled_validation.py --real

Reads configuration from environment variables (not Streamlit secrets):
    GEMINI_API_KEY, GITHUB_TOKEN, GITHUB_REPO, GITHUB_BRANCH
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.contamination import ContaminationError  # noqa: E402
from scripts.data_loader import validate_and_join  # noqa: E402
from scripts.output_writer import MODEL_DEFAULT, OutputStore  # noqa: E402
from scripts.run_paths import ensure_mode_dirs, resolve_run_paths  # noqa: E402
from scripts.validator_engine import GitHubSaver, RunConfig, run_validation  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Gemini 3.1 sampled validation runner")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--mock", action="store_true", help="run mock mode (no Gemini)")
    mode.add_argument("--real", action="store_true", help="run real Gemini mode")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--force-reprocess", action="store_true")
    p.add_argument("--start-after-validation-id", default=None)
    p.add_argument("--checkpoint-every", type=int, default=1)
    p.add_argument("--dry-run", action="store_true", help="validate join only; do not write")
    p.add_argument("--no-github-push", action="store_true")
    p.add_argument("--flash-adjudication", action="store_true", help="enable optional Gemini Flash adjudication for flagged guard conflicts")
    p.add_argument("--flash-model-id", default=os.environ.get("GEMINI_FLASH_MODEL_ID", "gemini-2.5-flash"))
    p.add_argument("--no-force-per-variant-validation", action="store_true", help="legacy mode: allow cluster row reuse in real mode")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    mode = "real" if args.real else "mock"
    model_id = os.environ.get("GEMINI_MODEL_ID", MODEL_DEFAULT)
    run_paths = resolve_run_paths(mode, model=model_id)

    join = validate_and_join()
    print(f"Join: ok={join.ok} variants={join.variant_count} "
          f"instructions={join.instruction_count}")
    for w in join.warnings:
        print(f"  warning: {w}")
    for e in join.errors:
        print(f"  ERROR: {e}")
    if not join.ok:
        print("Stopping before any model call due to join errors.")
        return 2
    if args.dry_run:
        print("Dry run complete (no validation performed).")
        return 0

    ensure_mode_dirs(run_paths)

    gemini_client = None
    if mode == "real":
        from scripts.gemini_client import GeminiClient, GeminiSettings

        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            print("ERROR: GEMINI_API_KEY not set; cannot run real mode.")
            return 2
        grounding = os.environ.get("GROUNDING_ENABLED", "true").lower() != "false"
        gemini_client = GeminiClient(
            GeminiSettings(api_key=api_key, model_id=model_id, grounding_enabled=grounding)
        )

    github_saver = None
    if not args.no_github_push and run_paths.allow_github_push and os.environ.get("GITHUB_TOKEN"):
        from scripts.github_checkpoint import GitHubCheckpoint, resolve_config_from_env

        config, notes = resolve_config_from_env()
        if config and config.configured:
            try:
                checkpoint = GitHubCheckpoint(config)
                github_saver = GitHubSaver(
                    checkpoint, run_paths.github_paths, commit_prefix=run_paths.commit_prefix
                )
                print(f"GitHub auto-save enabled: {config.repo}@{config.branch}")
            except Exception as exc:  # noqa: BLE001
                print(f"GitHub auto-save disabled: {exc}")
        else:
            print(f"GitHub auto-save disabled: {', '.join(notes)}")
    elif not run_paths.allow_github_push:
        print("GitHub auto-save disabled for mock mode.")

    store = OutputStore.for_paths(
        run_paths,
        total_input_variants=join.variant_count,
        total_instruction_records=join.instruction_count,
    )
    try:
        store.load_existing()
    except ContaminationError as exc:
        print(f"ERROR: {exc}")
        return 3

    config = RunConfig(
        mode=mode,
        limit=args.limit,
        force_reprocess=args.force_reprocess,
        start_after_validation_id=args.start_after_validation_id,
        checkpoint_every=args.checkpoint_every,
        stop_on_github_failure=not args.no_github_push,
        flash_adjudication_enabled=args.flash_adjudication,
        flash_model_id=args.flash_model_id,
        force_per_variant_validation=not args.no_force_per_variant_validation,
    )

    flash_adjudicator = None
    if mode == "real" and args.flash_adjudication:
        from scripts.flash_adjudicator import FlashAdjudicator, FlashSettings
        flash_adjudicator = FlashAdjudicator(FlashSettings(api_key=os.environ.get("GEMINI_API_KEY", ""), model_id=args.flash_model_id, enabled=True))

    result = run_validation(
        join,
        config,
        store=store,
        gemini_client=gemini_client,
        github_saver=github_saver,
        model_id=model_id,
        log=lambda m: print(m),
        flash_adjudicator=flash_adjudicator,
    )

    print("\n=== SUMMARY ===")
    print(f"mode={mode} processed={result.processed} stopped={result.stopped_reason}")
    print(f"decision_counts={store.metadata['decision_counts']}")
    print(f"gemini_call_count={store.metadata['gemini_call_count']}")
    print(f"github_checkpoint_count={store.metadata['github_checkpoint_count']}")
    print(f"stage1_pro_calls={store.metadata.get('stage1_pro_calls', 0)}")
    print(f"stage2_guard_flags_total={store.metadata.get('stage2_guard_flags_total', 0)}")
    print(f"stage3_flash_calls={store.metadata.get('stage3_flash_calls', 0)}")
    print(f"output -> {run_paths.output_path}")
    print(f"summary -> {run_paths.summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
