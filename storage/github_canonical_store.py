"""GitHub canonical store — pushes canonical to GitHub via REST API.

Reads credentials from core.config (env vars / secrets.py fallback).
Never pushes without explicit call from engine/save.py.
"""
from __future__ import annotations

import base64
import json
from urllib.parse import quote

import requests

from core.config import GITHUB_TOKEN, GITHUB_REPO, GITHUB_BRANCH, CANONICAL_RESUME_PATH


def _contents_url(repo: str, path: str) -> str:
    return f"https://api.github.com/repos/{repo}/contents/{quote(path)}"


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _get_existing_sha(path: str, token: str, repo: str, branch: str) -> tuple[str | None, str | None]:
    """Return (sha, error). sha is None when file does not yet exist."""
    try:
        resp = requests.get(
            _contents_url(repo, path),
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


def push_canonical(
    canonical: dict,
    commit_message: str | None = None,
    token: str | None = None,
    repo: str | None = None,
    branch: str | None = None,
    remote_path: str | None = None,
) -> dict:
    """Push canonical to GitHub. Returns dict with ok, error, sha, commit_sha."""
    t = token or GITHUB_TOKEN
    r = repo or GITHUB_REPO
    b = branch or GITHUB_BRANCH
    p = remote_path or CANONICAL_RESUME_PATH

    if not t:
        return {"ok": False, "error": "GITHUB_TOKEN not configured. Remote push disabled."}
    if not r:
        return {"ok": False, "error": "GITHUB_REPO not configured."}

    sha, fetch_err = _get_existing_sha(p, t, r, b)
    if fetch_err:
        return {"ok": False, "error": fetch_err}

    content_b64 = base64.b64encode(
        json.dumps(canonical, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")

    msg = commit_message or "Update canonical resume_package_canonical.json"
    payload: dict = {"message": msg, "content": content_b64, "branch": b}
    if sha:
        payload["sha"] = sha

    try:
        resp = requests.put(
            _contents_url(r, p),
            headers=_headers(t),
            json=payload,
            timeout=60,
        )
    except Exception as exc:
        return {"ok": False, "error": f"Push failed: {type(exc).__name__}"}

    if resp.status_code >= 400:
        return {"ok": False, "error": f"Push failed: HTTP {resp.status_code}"}

    body = resp.json() if resp.content else {}
    commit = body.get("commit") if isinstance(body, dict) else {}
    content_obj = body.get("content") if isinstance(body, dict) else {}
    return {
        "ok": True,
        "path": p,
        "sha": (content_obj or {}).get("sha"),
        "commit_sha": (commit or {}).get("sha"),
    }
