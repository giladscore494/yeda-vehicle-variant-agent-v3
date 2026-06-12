"""Reset / archive generated output files before a fresh validation run.

Rules:
  - NEVER delete or modify source input files under data/.
  - NEVER delete code, tests, README, requirements, or config.
  - Move generated output artifacts under output/ into a timestamped archive
    folder, then recreate a clean output/ with only the .gitkeep.
"""

from __future__ import annotations

import datetime as dt
import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "output"

# Files/dirs that are generated and should be archived/reset.
GENERATED_PATTERNS = [
    "validation_results.jsonl",
    "canonical_variants_clean.jsonl",
    "canonical_vehicle_variants_clean_v1.json",
    "rejected_from_clean.jsonl",
    "failures.jsonl",
    "push_failures.jsonl",
    "validation_progress.json",
    "validation_run_summary.json",
    "validation-v2-budgeted-dual-il-trims.json",
    "manual_review.jsonl",
    "startup_failure_report.json",
    "active_model_context.json",
    "discovered_missing_variants.jsonl",
    "model_runs",
    "mock",
]

# Source input files that must NEVER be deleted.
PROTECTED_PATHS = {
    "data/validation_variants_data_v1.json",
    "data/validation_instructions_by_id_v1.json",
    "data/validation_instructions_by_id_v1.jsonl",
}


def _timestamp_tag() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def archive_and_reset(output_dir: Path | None = None,
                      log=print) -> dict:
    """Archive generated files and reset the output directory.

    Returns a summary dict with archive path and counts.
    """
    output_dir = output_dir or OUTPUT_DIR
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        log(f"output directory created: {output_dir}")
        return {"status": "no_files_to_archive", "archive_path": None}

    tag = _timestamp_tag()
    archive_dir = output_dir / f"archive_reset_{tag}"

    moved_count = 0
    for name in GENERATED_PATTERNS:
        src = output_dir / name
        if not src.exists():
            continue
        dest = archive_dir / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.move(str(src), str(dest))
        else:
            shutil.move(str(src), str(dest))
        moved_count += 1
        log(f"  archived: {name}")

    # Ensure .gitkeep survives
    gitkeep = output_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.touch()

    summary = {
        "status": "archived" if moved_count > 0 else "nothing_to_archive",
        "archive_path": str(archive_dir) if moved_count > 0 else None,
        "archived_at": _timestamp_tag(),
        "files_archived": moved_count,
    }
    if moved_count > 0:
        # Write a small manifest inside the archive
        manifest = archive_dir / "archive_manifest.json"
        manifest.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        log(f"Archived {moved_count} item(s) to {archive_dir.name}")
    else:
        log("No generated output files to archive.")

    return summary


def main() -> None:
    """CLI entry point."""
    import argparse
    p = argparse.ArgumentParser(description="Reset generated output files")
    p.add_argument("--output-dir", type=Path, default=None)
    args = p.parse_args()
    result = archive_and_reset(args.output_dir)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
