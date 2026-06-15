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

from .catalog_builder import build_catalog
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
        "--no-web-search",
        action="store_true",
        help="Disable the GPT-5.4 web_search tool (still calls the model).",
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

    use_openai = not args.offline and bool(cfg.openai_api_key)
    if not args.offline and not cfg.openai_api_key:
        print(
            "No OpenAI API key found — falling back to OFFLINE synthesis. "
            "Set OPENAI_API_KEY (or secrets [openai].api_key) for a grounded run.",
            file=sys.stderr,
        )

    settings = CatalogClientSettings(
        api_key=cfg.openai_api_key,
        model_id=cfg.openai_validator_model_id,
        use_web_search=not args.no_web_search,
    )

    result = build_catalog(
        make=args.make,
        model=args.model,
        limit_models=args.limit_models,
        use_openai=use_openai,
        settings=settings,
        log=lambda msg: print(msg, file=sys.stderr),
    )

    print(json.dumps(result.readiness, indent=2, ensure_ascii=False))
    print(f"\ncatalog   -> {result.catalog_path}", file=sys.stderr)
    print(f"readiness -> {result.readiness_path}", file=sys.stderr)
    print(f"review    -> {result.review_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
