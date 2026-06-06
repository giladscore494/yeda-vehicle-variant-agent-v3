"""Explicit GitHub save for the final clean validation database only."""
from __future__ import annotations

from pathlib import Path

from core.paths import FINAL_CLEAN_DATABASE_PATH, SOURCE_CANONICAL_PATH, STALE_ROOT_CANONICAL_PATH
from engine import config
from engine.github_writer import push_file
from engine.validation.run_events import log_event

_ALLOWED_REPO = "giladscore494/yeda-vehicle-variant-agent-v3"
_ALLOWED_BRANCH = "validation-v2-budgeted-dual-il-trims"
_COMMIT_MESSAGE = "Save final clean validation database"
_BLOCKED_PATH_PARTS = ("secrets", "tmp", "old_project", ".env", "api_key", "apikey")


def _is_path_blocked(path: str) -> bool:
    normalized = path.replace("\\", "/").strip("/")
    lowered = normalized.lower()
    if normalized in (SOURCE_CANONICAL_PATH, STALE_ROOT_CANONICAL_PATH):
        return True
    if normalized.startswith("data/canonical/"):
        return True
    return any(part in lowered for part in _BLOCKED_PATH_PARTS)


def save_final_clean_database_to_github() -> dict:
    """Save only ``data/final/resume_package_final_clean.json`` to GitHub."""
    path = FINAL_CLEAN_DATABASE_PATH
    final_file = Path(path)
    if not final_file.exists():
        return {
            "ok": False,
            "saved_path": path,
            "repo": _ALLOWED_REPO,
            "branch": _ALLOWED_BRANCH,
            "commit_sha": "",
            "message": "Run Export Final Clean Database first.",
        }

    if _is_path_blocked(path):
        return {
            "ok": False,
            "saved_path": path,
            "repo": _ALLOWED_REPO,
            "branch": _ALLOWED_BRANCH,
            "commit_sha": "",
            "message": "Blocked path for GitHub save.",
        }

    repo = f"{config.get('github', 'repo_owner')}/{config.get('github', 'repo_name')}"
    branch = config.get("github", "target_branch")
    token = config.get("github", "token")
    if not token:
        return {
            "ok": False,
            "saved_path": path,
            "repo": repo,
            "branch": branch,
            "commit_sha": "",
            "message": "GitHub token not configured. Cannot save final clean database.",
        }
    if repo != _ALLOWED_REPO:
        return {
            "ok": False,
            "saved_path": path,
            "repo": repo,
            "branch": branch,
            "commit_sha": "",
            "message": f"Repo '{repo}' is not allowed for final clean save.",
        }
    if branch != _ALLOWED_BRANCH:
        return {
            "ok": False,
            "saved_path": path,
            "repo": repo,
            "branch": branch,
            "commit_sha": "",
            "message": f"Branch '{branch}' is not allowed for final clean save.",
        }

    log_event(
        {
            "stage": "github_save",
            "event_type": "github_save_started",
            "status": "started",
            "request_summary": f"path={path}",
            "provider": "github",
            "model": "",
        }
    )

    try:
        result = push_file(
            content=final_file.read_text(encoding="utf-8"),
            remote_path=path,
            commit_message=_COMMIT_MESSAGE,
            branch=branch,
        )
        if not result.get("ok"):
            log_event(
                {
                    "stage": "github_save",
                    "event_type": "github_save_failed",
                    "status": "failed",
                    "provider": "github",
                    "request_summary": f"path={path}",
                    "response_summary": str(result.get("error") or ""),
                    "error": str(result.get("error") or ""),
                }
            )
            return {
                "ok": False,
                "saved_path": path,
                "repo": repo,
                "branch": branch,
                "commit_sha": "",
                "message": str(result.get("error") or "GitHub save failed."),
            }

        commit_sha = str(result.get("commit_sha") or "")
        log_event(
            {
                "stage": "github_save",
                "event_type": "github_save_completed",
                "status": "ok",
                "provider": "github",
                "request_summary": f"path={path}",
                "response_summary": f"commit_sha={commit_sha}",
                "item_id": path,
            }
        )
        return {
            "ok": True,
            "saved_path": path,
            "repo": repo,
            "branch": branch,
            "commit_sha": commit_sha,
            "message": "Saved final clean validation database to GitHub.",
        }
    except Exception as exc:
        log_event(
            {
                "stage": "github_save",
                "event_type": "github_save_failed",
                "status": "failed",
                "provider": "github",
                "request_summary": f"path={path}",
                "error": str(exc),
            }
        )
        return {
            "ok": False,
            "saved_path": path,
            "repo": repo,
            "branch": branch,
            "commit_sha": "",
            "message": "GitHub save failed.",
            "exception": str(exc),
        }
