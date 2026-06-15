"""CLI runner for the single-GPT-5.4 Israeli model technical catalog.

Examples
--------
One-model test sample (offline, no API key needed)::

    python scripts/run_model_catalog.py --make Abarth --model 500 --limit-models 1 --offline

One real cluster with GPT-5.4 (needs OPENAI_API_KEY)::

    python scripts/run_model_catalog.py --make Abarth --model 500 --limit-models 1

Full run (only after the one-model sample passes)::

    python scripts/run_model_catalog.py

The pipeline reads ONLY the two source files and uses GPT-5.4 only. Gemini,
the legacy guard verifier, the repair adjudicator and per-row validation are
all disabled in this mode.
"""

from __future__ import annotations

import argparse
import json
import sys

from .catalog_builder import build_catalog, OPENAI_KEY_REQUIRED_MESSAGE
from .catalog_checkpoint import CatalogCheckpointConfig
from .config import load_shared_config
from .openai_catalog_client import CatalogClientSettings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--make", default=None, help="Only this make (e.g. Abarth)")
    parser.add_argument("--model", default=None, help="Only this model (e.g. 500)")
    parser.add_argument(
        "--limit-models",
        type=int,
        default=None,
        help="Process at most N model clusters (e.g. 1 for the sample).",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Synthesize profiles deterministically without calling GPT-5.4.",
    )
    parser.add_argument(
        "--github-checkpoint",
        action="store_true",
        help="Push generated catalog files to GitHub after each model profile.",
    )
    args = parser.parse_args(argv)

    cfg = load_shared_config()
    if not cfg.single_gpt54_model_catalog_mode:
        print(
            "SINGLE_GPT54_MODEL_CATALOG_MODE is disabled; refusing to run the "
            "new catalog pipeline. Set it to true to enable.",
            file=sys.stderr,
        )
        return 2

    # Fail fast for real grounded runs without an OpenAI key.
    if not args.offline and not cfg.openai_api_key:
        print(OPENAI_KEY_REQUIRED_MESSAGE, file=sys.stderr)
        return 2

    settings = CatalogClientSettings(
        api_key=cfg.openai_api_key,
        model_id=cfg.openai_validator_model_id,
        use_web_search=True,  # real runs always use web_search grounding
    )

    checkpoint_enabled = args.github_checkpoint or cfg.github_checkpoint_enabled
    checkpoint = CatalogCheckpointConfig(
        enabled=checkpoint_enabled,
        push_every_profiles=cfg.push_every_profiles,
        strict=cfg.strict_github_checkpoint,
        token=cfg.github_token,
    )

    try:
        result = build_catalog(
            make=args.make,
            model=args.model,
            limit_models=args.limit_models,
            offline=args.offline,
            settings=settings,
            checkpoint=checkpoint,
            log=lambda msg: print(msg, file=sys.stderr),
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
