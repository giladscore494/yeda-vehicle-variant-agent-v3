"""GitHub writer for the validation engine.

Reads repo/branch/token from engine.config.
Reuses the REST API pattern from storage/github_canonical_store.py.
Never hardcodes tokens. Never prints secrets.
"""
from __future__ import annotations

import base64
import json
import logging
from urllib.parse import quote

import requests

from engine import config

logger = logging.getLogger(__name__)


def _contents_url(owner: str, repo: str, path: str) -> str:
    return f"https://api.github.com/repos/{owner}/{repo}/contents/{quote(path)}"


def _headers(token: str) -> dict:
    return {
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _get_existing_sha(
    owner: str, repo: str, path: str, branch: str, token: str
) -> tuple[str | None, str | None]:
    """Return (sha, error). sha is None when file does not yet exist."""
    try:
        resp = requests.get(
            _contents_url(owner, repo, path),
            headers=_headers(token),
            params={"ref": branch},
            timeout=30,
        )
    except Exception as exc:
        return None, f"Failed to fetch from GitHub: {type(exc).__name__}"
    if resp.status_code == 404:
        return None, None
    if resp.status_code >= 400:
        return None, f"GitHub HTTP {resp.status_code}"
    body = resp.json() if resp.content else {}
    return body.get("sha"), None


def push_file(
    content: str | bytes,
    remote_path: str,
    commit_message: str,
    *,
    token: str | None = None,
    owner: str | None = None,
    repo_name: str | None = None,
    branch: str | None = None,
) -> dict:
    """Push a single file to the GitHub repository.

    Returns dict with ok, error, sha, commit_sha.
    """
    t = token or config.get("github", "token")
    o = owner or config.get("github", "repo_owner")
    r = repo_name or config.get("github", "repo_name")
    b = branch or config.get("github", "target_branch")

    if not t:
        return {
            "ok": False,
            "error": "GitHub token not configured. Set github.token in secrets.",
        }
    if not o or not r:
        return {"ok": False, "error": "GitHub repo_owner/repo_name not configured."}

    sha, fetch_err = _get_existing_sha(o, r, remote_path, b, t)
    if fetch_err:
        return {"ok": False, "error": fetch_err}

    if isinstance(content, str):
        content = content.encode("utf-8")
    content_b64 = base64.b64encode(content).decode("utf-8")

    payload: dict = {"message": commit_message, "content": content_b64, "branch": b}
    if sha:
        payload["sha"] = sha

    try:
        resp = requests.put(
            _contents_url(o, r, remote_path),
            headers=_headers(t),
            json=payload,
            timeout=60,
        )
    except Exception as exc:
        return {"ok": False, "error": f"Push failed: {type(exc).__name__}"}

    if resp.status_code >= 400:
        return {"ok": False, "error": f"Push failed: HTTP {resp.status_code}"}

    body = resp.json() if resp.content else {}
    commit_obj = body.get("commit") if isinstance(body, dict) else {}
    content_obj = body.get("content") if isinstance(body, dict) else {}
    logger.info("Pushed %s to %s/%s branch=%s", remote_path, o, r, b)
    return {
        "ok": True,
        "path": remote_path,
        "sha": (content_obj or {}).get("sha"),
        "commit_sha": (commit_obj or {}).get("sha"),
    }


def push_json(
    data: dict | list,
    remote_path: str,
    commit_message: str,
    **kwargs,
) -> dict:
    """Push a JSON-serializable object as a file."""
    content = json.dumps(data, ensure_ascii=False, indent=2)
    return push_file(content, remote_path, commit_message, **kwargs)


def push_validation_outputs(
    outputs: dict[str, str | bytes],
    commit_message: str = "Add validated vehicle variants package",
    **kwargs,
) -> list[dict]:
    """Push multiple validation output files. Returns list of results."""
    results = []
    for remote_path, content in outputs.items():
        result = push_file(content, remote_path, commit_message, **kwargs)
        results.append(result)
        if not result.get("ok"):
            logger.error("Failed to push %s: %s", remote_path, result.get("error"))
    return results
