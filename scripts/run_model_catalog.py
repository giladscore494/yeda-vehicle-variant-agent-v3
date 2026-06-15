"""CLI runner for the GPT-5.4 Israeli model technical catalog.

This is the single production entrypoint. It reads ONLY the two source files
and uses GPT-5.4 (with web_search grounding) as the only model. There is no
per-row validation. ``OPENAI_API_KEY`` is required; the run fails closed
without it.

Examples
--------
Process at most 10 clusters::

    python -m scripts.run_model_catalog --limit-models 10

One real cluster with GPT-5.4::

    python -m scripts.run_model_catalog --make "Alfa Romeo" --model Tonale --limit-models 1

Resume after a given cluster key (``market|make|model``)::

    python -m scripts.run_model_catalog --start-after-key "IL|Abarth|500" --limit-models 5
"""

from __future__ import annotations

import argparse
import json
import sys

from .catalog_builder import OPENAI_KEY_REQUIRED_MESSAGE, build_catalog
from .catalog_checkpoint import CatalogCheckpointConfig
from .config import load_shared_config
from .openai_catalog_client import CatalogClientSettings


def _format_progress(info: dict) -> str:
    phase = info.get("phase")
    idx = info.get("index")
    total = info.get("total")
    if phase == "running":
        ids = ", ".join(info.get("validation_ids") or []) or "(none)"
        return (
            f"[{idx}/{total}] RUNNING GPT-5.4: {info.get('market_scope')} :: "
            f"{info.get('make')} :: {info.get('model')} | "
            f"raw_variants={info.get('raw_variants')} | sample_ids={ids}"
        )
    if phase == "done":
        return (
            f"[{idx}/{total}] DONE: {info.get('make')} {info.get('model')} | "
            f"technical_variants={info.get('technical_variants')} | "
            f"ready={str(info.get('ready_profile')).lower()} | "
            f"issues={info.get('issues')}"
        )
    if phase == "error":
        return f"[{idx}/{total}] ERROR: {info.get('make')} {info.get('model')} routed to review"
    return ""


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--make", default=None, help="Only this make (e.g. 'Alfa Romeo')")
    parser.add_argument("--model", default=None, help="Only this model (e.g. Tonale)")
    parser.add_argument(
        "--limit-models",
        type=int,
        default=None,
        help="Process at most N make/model clusters this run.",
    )
    parser.add_argument(
        "--start-after-key",
        default=None,
        help="Resume after this cluster key (format: 'market|make|model').",
    )
    parser.add_argument(
        "--github-checkpoint",
        action="store_true",
        help="Push generated catalog files to GitHub after each model profile.",
    )
    args = parser.parse_args(argv)

    cfg = load_shared_config()

    # Fail closed for grounded runs without an OpenAI key.
    if not cfg.openai_api_key:
        print(OPENAI_KEY_REQUIRED_MESSAGE, file=sys.stderr)
        return 2

    settings = CatalogClientSettings(
        api_key=cfg.openai_api_key,
        model_id=cfg.openai_validator_model_id,
        use_web_search=True,  # runs always use web_search grounding
    )

    checkpoint_enabled = args.github_checkpoint or cfg.github_checkpoint_enabled
    checkpoint = CatalogCheckpointConfig(
        enabled=checkpoint_enabled,
        push_every_profiles=cfg.push_every_profiles,
        strict=cfg.strict_github_checkpoint,
        token=cfg.github_token,
    )

    def _emit(msg: str) -> None:
        print(msg, file=sys.stderr)

    def _progress(info: dict) -> None:
        line = _format_progress(info)
        if line:
            print(line, file=sys.stderr)

    try:
        result = build_catalog(
            make=args.make,
            model=args.model,
            limit_models=args.limit_models,
            start_after_key=args.start_after_key,
            settings=settings,
            checkpoint=checkpoint,
            log=_emit,
            on_progress=_progress,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(json.dumps(result.readiness, indent=2, ensure_ascii=False))
    print(f"\ncatalog   -> {result.catalog_path}", file=sys.stderr)
    print(f"readiness -> {result.readiness_path}", file=sys.stderr)
    print(f"review    -> {result.review_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
