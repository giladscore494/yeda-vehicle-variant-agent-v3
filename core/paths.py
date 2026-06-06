"""Canonical repository paths for validation inputs and outputs.

This module intentionally defines the single source canonical, validation
working files, and final clean database output in one place.
"""

SOURCE_CANONICAL_PATH = "data/canonical/resume_package_canonical.json"
STALE_ROOT_CANONICAL_PATH = "resume_package_canonical.json"

WORKING_DIR = "data/working"
ACTIVE_WORKING_DATABASE_PATH = "data/working/resume_package_working.json"
WORKING_BACKUPS_DIR = "data/working/backups"

VALIDATION_DIR = "data/validation"
ISSUE_QUEUE_PATH = "data/validation/issue_queue.json"
DECISIONS_PATH = "data/validation/decisions.json"
MANIFEST_PATH = "data/validation/manifest.json"
VALIDATION_REPORT_PATH = "data/validation/validation_report.json"
RUN_EVENTS_PATH = "data/validation/run_events.jsonl"
PATCHES_PATH = "data/validation/patches.json"
PATCH_APPLICATIONS_PATH = "data/validation/patch_applications.jsonl"
DIFF_AUDITS_PATH = "data/validation/diff_audits.jsonl"
AI_OUTCOME_AUDITS_PATH = "data/validation/ai_outcome_audits.jsonl"
MODEL_REVIEW_PROGRESS_PATH = "data/validation/model_review_progress.json"

FINAL_DIR = "data/final"
FINAL_CLEAN_DATABASE_PATH = "data/final/resume_package_final_clean.json"
