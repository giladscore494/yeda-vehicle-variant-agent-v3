"""Robust GitHub auto-save via the Contents API.

After each validated variant the engine pushes the updated output + checkpoint
files to GitHub so progress survives Streamlit's ephemeral filesystem.

Security:
- the token is read from secrets/env and never printed, logged, or returned;
- the Streamlit secrets file is never committed;
- only the explicit data files are uploaded.
"""

from __future__ import annotations

import base64
import os
import re
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import requests

API_ROOT = "https://api.github.com"

# Last-resort fallback if detection fails and no secret/env override is given.
FALLBACK_REPO = "giladscore494/yeda-vehicle-variant-agent-v3"
FALLBACK_BRANCH = "claude/beautiful-mccarthy-jdjy5m"


class GitHubSaveError(RuntimeError):
    """Raised on any GitHub save failure (auth, repo, network, conflict)."""


def _redact(text: str) -> str:
    """Defensive: strip anything that looks like a token from a message."""
    return re.sub(r"gh[pousr]_[A-Za-z0-9]{20,}", "***", text or "")


# ---------------------------------------------------------------------------
# Repository / branch detection
# ---------------------------------------------------------------------------


def _parse_owner_repo(url: str) -> Optional[str]:
    if not url:
        return None
    url = url.strip()
    # git@github.com:owner/repo.git
    m = re.search(r"github\.com[:/]+([^/]+/[^/]+?)(?:\.git)?$", url)
    if m:
        return m.group(1)
    # Any URL ending in .../owner/repo(.git) — handles proxied http remotes.
    m = re.search(r"/([^/]+/[^/]+?)(?:\.git)?/?$", url)
    if m:
        return m.group(1)
    return None


def detect_repo(explicit: Optional[str] = None) -> Optional[str]:
    """Resolve ``owner/repo`` from explicit config, env, git remote, fallback."""
    if explicit:
        return explicit
    for env in ("GITHUB_REPO", "GITHUB_REPOSITORY"):
        if os.environ.get(env):
            return os.environ[env]
    try:
        url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        parsed = _parse_owner_repo(url)
        if parsed:
            return parsed
    except Exception:  # noqa: BLE001
        pass
    return FALLBACK_REPO


def detect_branch(explicit: Optional[str] = None) -> Optional[str]:
    if explicit:
        return explicit
    for env in ("GITHUB_BRANCH", "GITHUB_REF_NAME"):
        if os.environ.get(env):
            return os.environ[env]
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        if branch and branch != "HEAD":
            return branch
    except Exception:  # noqa: BLE001
        pass
    return FALLBACK_BRANCH


# ---------------------------------------------------------------------------
# Saver
# ---------------------------------------------------------------------------


@dataclass
class GitHubConfig:
    token: str
    repo: str
    branch: str

    @property
    def configured(self) -> bool:
        return bool(self.token and self.repo and self.branch)


class GitHubCheckpoint:
    """Uploads files to GitHub via the Contents API, tracking blob SHAs."""

    def __init__(self, config: GitHubConfig, repo_root: Optional[str] = None) -> None:
        if not config.token:
            raise GitHubSaveError("GitHub token is missing")
        if not config.repo or not config.branch:
            raise GitHubSaveError(
                "GitHub repo/branch could not be resolved; add [github].repo "
                "and [github].branch to secrets"
            )
        self.config = config
        self.repo_root = repo_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._sha_cache: Dict[str, str] = {}
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {config.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )

    # -- low-level ---------------------------------------------------------

    def _contents_url(self, repo_rel_path: str) -> str:
        return f"{API_ROOT}/repos/{self.config.repo}/contents/{repo_rel_path}"

    def _get_existing_sha(self, repo_rel_path: str) -> Optional[str]:
        if repo_rel_path in self._sha_cache:
            return self._sha_cache[repo_rel_path]
        try:
            resp = self._session.get(
                self._contents_url(repo_rel_path),
                params={"ref": self.config.branch},
                timeout=30,
            )
        except requests.RequestException as exc:
            raise GitHubSaveError(_redact(f"Network error reading {repo_rel_path}: {exc}"))
        if resp.status_code == 200:
            sha = resp.json().get("sha")
            if sha:
                self._sha_cache[repo_rel_path] = sha
            return sha
        if resp.status_code == 404:
            return None
        raise GitHubSaveError(
            _redact(
                f"Failed to read {repo_rel_path}: HTTP {resp.status_code} {resp.text[:200]}"
            )
        )

    def put_file(self, repo_rel_path: str, content_bytes: bytes, message: str) -> str:
        """Create or update a single file. Returns the new blob SHA."""
        if _is_secrets_path(repo_rel_path):
            raise GitHubSaveError(f"Refusing to commit secrets file: {repo_rel_path}")

        sha = self._get_existing_sha(repo_rel_path)
        payload = {
            "message": message,
            "content": base64.b64encode(content_bytes).decode("ascii"),
            "branch": self.config.branch,
        }
        if sha:
            payload["sha"] = sha
        try:
            resp = self._session.put(
                self._contents_url(repo_rel_path), json=payload, timeout=60
            )
        except requests.RequestException as exc:
            raise GitHubSaveError(_redact(f"Network error writing {repo_rel_path}: {exc}"))

        if resp.status_code in (200, 201):
            new_sha = resp.json().get("content", {}).get("sha")
            if new_sha:
                self._sha_cache[repo_rel_path] = new_sha
            return new_sha or ""
        if resp.status_code == 409:
            # SHA conflict: refresh and retry once.
            self._sha_cache.pop(repo_rel_path, None)
            sha = self._get_existing_sha(repo_rel_path)
            if sha:
                payload["sha"] = sha
            resp = self._session.put(
                self._contents_url(repo_rel_path), json=payload, timeout=60
            )
            if resp.status_code in (200, 201):
                return resp.json().get("content", {}).get("sha", "")
        if resp.status_code in (401, 403):
            raise GitHubSaveError(
                f"GitHub auth failed (HTTP {resp.status_code}) for repo "
                f"{self.config.repo}; check token permissions"
            )
        raise GitHubSaveError(
            _redact(
                f"Failed to write {repo_rel_path}: HTTP {resp.status_code} {resp.text[:200]}"
            )
        )

    # -- high-level --------------------------------------------------------

    def save_paths(self, local_paths: List[str], message: str) -> List[str]:
        """Upload each existing local path (relative to repo root)."""
        saved: List[str] = []
        for local in local_paths:
            if not os.path.exists(local):
                continue
            rel = os.path.relpath(local, self.repo_root).replace(os.sep, "/")
            with open(local, "rb") as fh:
                self.put_file(rel, fh.read(), message)
            saved.append(rel)
        return saved


def _is_secrets_path(path: str) -> bool:
    lowered = path.lower()
    return (
        "secrets.toml" in lowered
        or "/.streamlit/" in f"/{lowered}"
        or lowered.startswith(".streamlit/")
        or lowered.endswith(".env")
    )


# ---------------------------------------------------------------------------
# Secret/config resolution (Streamlit + env)
# ---------------------------------------------------------------------------


def resolve_config_from_streamlit(st_secrets) -> Tuple[Optional[GitHubConfig], List[str]]:
    """Build a GitHubConfig from st.secrets, falling back to detection."""
    notes: List[str] = []
    gh = {}
    try:
        gh = dict(st_secrets.get("github", {}))
    except Exception:  # noqa: BLE001
        gh = {}
    token = gh.get("token") or ""
    repo = detect_repo(gh.get("repo"))
    branch = detect_branch(gh.get("branch"))
    if not token:
        notes.append("github.token missing")
    if not repo:
        notes.append("github.repo could not be detected")
    if not branch:
        notes.append("github.branch could not be detected")
    config = GitHubConfig(token=token, repo=repo or "", branch=branch or "")
    return (config if token else None), notes


def resolve_config_from_env() -> Tuple[Optional[GitHubConfig], List[str]]:
    notes: List[str] = []
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    repo = detect_repo(os.environ.get("GITHUB_REPO"))
    branch = detect_branch(os.environ.get("GITHUB_BRANCH"))
    if not token:
        notes.append("GITHUB_TOKEN missing")
    config = GitHubConfig(token=token, repo=repo or "", branch=branch or "")
    return (config if token else None), notes
