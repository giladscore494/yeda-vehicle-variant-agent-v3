"""GitHub save wrapper — safe commit of validation outputs to GitHub.

Guards:
- Must be on branch validation-v2-budgeted-dual-il-trims
- Must NOT be on main
- Must NOT commit canonical
- Must NOT commit secrets or tmp files
- Only allowed files in data/validated_runs/ and data/runtime/
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

from engine import config
from engine.github_writer import push_file

logger = logging.getLogger(__name__)

_ALLOWED_REPO = "giladscore494/yeda-vehicle-variant-agent-v3"
_ALLOWED_BRANCH = "validation-v2-budgeted-dual-il-trims"
_BLOCKED_BRANCH = "main"

# Files that are allowed to be committed
ALLOWED_FILES = [
    "data/validated_runs/resume_package_canonical_validated_v2.json",
    "data/validated_runs/validation_report_v2.json",
    "data/validated_runs/validation_issues_v2.json",
    "data/validated_runs/validation_patch_suggestions_v2.json",
    "data/validated_runs/targeted_seed_validation_v2.json",
    "data/validated_runs/model_validation_results_v2.json",
    "data/runtime/current_validation_run.json",
]

# Files that must NEVER be committed
BLOCKED_FILES = [
    "data/canonical/resume_package_canonical.json",
]


def _check_guards() -> str | None:
    """Check all safety guards. Returns error message or None."""
    branch = config.get("github", "target_branch")
    repo = f"{config.get('github', 'repo_owner')}/{config.get('github', 'repo_name')}"
    token = config.get("github", "token")

    if branch == _BLOCKED_BRANCH:
        return "Cannot save to main branch. Branch guard triggered."

    if branch != _ALLOWED_BRANCH:
        return (
            f"Branch '{branch}' is not the allowed branch "
            f"'{_ALLOWED_BRANCH}'. Stopping."
        )

    if repo != _ALLOWED_REPO:
        return (
            f"Repo '{repo}' is not the allowed repo "
            f"'{_ALLOWED_REPO}'. Stopping."
        )

    if not token:
        return "GitHub token not configured. Cannot save to GitHub."

    return None


def _is_file_allowed(file_path: str) -> bool:
    """Check if a file path is in the allowed list."""
    # Normalize path
    normalized = file_path.replace("\\", "/").strip("/")
    for allowed in ALLOWED_FILES:
        if normalized == allowed.strip("/"):
            return True
    return False


def _is_file_blocked(file_path: str) -> bool:
    """Check if a file path is in the blocked list."""
    normalized = file_path.replace("\\", "/").strip("/")
    for blocked in BLOCKED_FILES:
        if normalized == blocked.strip("/"):
            return True
    # Also block anything in data/canonical/
    if normalized.startswith("data/canonical/"):
        return True
    return False


def get_files_to_save() -> list[dict]:
    """Get list of files that exist and can be saved.

    Returns list of dicts with: path, exists, size, allowed.
    """
    files = []
    for file_path in ALLOWED_FILES:
        p = Path(file_path)
        files.append({
            "path": file_path,
            "exists": p.exists(),
            "size": p.stat().st_size if p.exists() else 0,
            "allowed": True,
        })
    return files


def save_validation_outputs_to_github(
    validation_run_id: str = "unknown",
    dry_run: bool = False,
) -> dict:
    """Save validation outputs to GitHub.

    Guards:
    - Branch must be validation-v2-budgeted-dual-il-trims
    - Branch must NOT be main
    - Repo must be giladscore494/yeda-vehicle-variant-agent-v3
    - Token must be present
    - Only allowed files are committed
    - Canonical file is NEVER committed

    Returns result dict with files, repo, branch, commit result.
    """
    # Check guards
    guard_error = _check_guards()
    if guard_error:
        return {
            "ok": False,
            "error": guard_error,
            "files_selected": [],
            "repo": "",
            "target_branch": "",
        }

    branch = config.get("github", "target_branch")
    repo = f"{config.get('github', 'repo_owner')}/{config.get('github', 'repo_name')}"

    # Find files that exist
    files_to_save = []
    for file_path in ALLOWED_FILES:
        p = Path(file_path)
        if p.exists():
            # Double-check it's not blocked
            if _is_file_blocked(file_path):
                logger.error("Blocked file in allowed list: %s", file_path)
                return {
                    "ok": False,
                    "error": f"SECURITY: Blocked file '{file_path}' found in allowed list. Aborting.",
                    "files_selected": [],
                    "repo": repo,
                    "target_branch": branch,
                }
            files_to_save.append(file_path)

    if not files_to_save:
        return {
            "ok": False,
            "error": "No validation output files found to save.",
            "files_selected": [],
            "repo": repo,
            "target_branch": branch,
        }

    commit_message = f"Save validation outputs for {validation_run_id}"

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "files_selected": files_to_save,
            "repo": repo,
            "target_branch": branch,
            "commit_message": commit_message,
            "commit_sha": None,
        }

    # Push files
    results = []
    all_ok = True
    last_commit_sha = None

    for file_path in files_to_save:
        p = Path(file_path)
        content = p.read_text(encoding="utf-8")

        result = push_file(
            content=content,
            remote_path=file_path,
            commit_message=commit_message,
            branch=branch,
        )

        results.append({
            "path": file_path,
            "ok": result.get("ok", False),
            "error": result.get("error"),
            "sha": result.get("sha"),
            "commit_sha": result.get("commit_sha"),
        })

        if result.get("ok"):
            last_commit_sha = result.get("commit_sha")
        else:
            all_ok = False

    return {
        "ok": all_ok,
        "files_selected": files_to_save,
        "repo": repo,
        "target_branch": branch,
        "commit_message": commit_message,
        "commit_sha": last_commit_sha,
        "file_results": results,
        "error": None if all_ok else "Some files failed to push",
    }
