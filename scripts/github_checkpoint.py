"""GitHub checkpointing for the validation engine.

Pushes output files to the target branch. Two transports:

1. GitHub REST API (preferred) — works in deployed Streamlit runtimes that are
   not normal git workspaces. Builds blobs -> tree -> commit -> ref update,
   skipping the commit entirely when no file content changed (compared via
   locally computed git blob SHAs).
2. git CLI fallback — used when REST fails and a .git workspace exists.

The token is read from the supplied config (Streamlit secrets or env) and is
never printed, never placed in argv or remote URLs, and never written to disk.
Push failures are appended to output/push_failures.jsonl and reported back to
the caller; local output is never deleted or lost.
"""

from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

API_BASE = "https://api.github.com"
PUSH_RETRIES = 4
PUSH_BACKOFF_SECONDS = [2, 4, 8, 16]

# git CLI fallback reads the token from the environment at git runtime,
# so nothing secret appears in argv or on disk.
_CREDENTIAL_HELPER = (
    '!f() { echo "username=x-access-token"; echo "password=${GH_PUSH_TOKEN}"; }; f'
)


def _utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _redact(text: str, *secrets: str) -> str:
    for s in secrets:
        if s:
            text = text.replace(s, "***")
    return text


def git_blob_sha(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode()
    return hashlib.sha1(header + content).hexdigest()


def collect_output_files(repo_root: Path, rel_paths: list[str]) -> list[Path]:
    """Expand files/directories into a flat list of existing files."""
    files: list[Path] = []
    for rel in rel_paths:
        p = repo_root / rel
        if p.is_dir():
            files.extend(sorted(f for f in p.rglob("*") if f.is_file()
                                and not f.name.endswith(".tmp")))
        elif p.is_file():
            files.append(p)
    return files


# ---------------------------------------------------------------------------
# REST transport
# ---------------------------------------------------------------------------

def _rest_push_once(token: str, repo_full_name: str, branch: str, message: str,
                    files: list[Path], repo_root: Path, log) -> dict:
    import requests

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    base = f"{API_BASE}/repos/{repo_full_name}"

    ref_resp = requests.get(f"{base}/git/ref/heads/{branch}", headers=headers, timeout=60)
    ref_resp.raise_for_status()
    head_sha = ref_resp.json()["object"]["sha"]

    commit_resp = requests.get(f"{base}/git/commits/{head_sha}", headers=headers, timeout=60)
    commit_resp.raise_for_status()
    base_tree_sha = commit_resp.json()["tree"]["sha"]

    tree_resp = requests.get(f"{base}/git/trees/{base_tree_sha}",
                             headers=headers, params={"recursive": "1"}, timeout=120)
    tree_resp.raise_for_status()
    remote_shas = {e["path"]: e["sha"] for e in tree_resp.json().get("tree", [])
                   if e["type"] == "blob"}

    changed: list[tuple[str, bytes]] = []
    for f in files:
        rel = f.relative_to(repo_root).as_posix()
        content = f.read_bytes()
        if remote_shas.get(rel) != git_blob_sha(content):
            changed.append((rel, content))

    if not changed:
        return {"committed": False, "pushed": False, "skipped": "no_changes",
                "method": "rest"}

    tree_entries = []
    for rel, content in changed:
        blob_resp = requests.post(
            f"{base}/git/blobs", headers=headers, timeout=120,
            json={"content": base64.b64encode(content).decode(), "encoding": "base64"})
        blob_resp.raise_for_status()
        tree_entries.append({"path": rel, "mode": "100644", "type": "blob",
                             "sha": blob_resp.json()["sha"]})

    new_tree = requests.post(f"{base}/git/trees", headers=headers, timeout=120,
                             json={"base_tree": base_tree_sha, "tree": tree_entries})
    new_tree.raise_for_status()

    new_commit = requests.post(
        f"{base}/git/commits", headers=headers, timeout=60,
        json={"message": message, "tree": new_tree.json()["sha"],
              "parents": [head_sha]})
    new_commit.raise_for_status()
    new_sha = new_commit.json()["sha"]

    update = requests.patch(f"{base}/git/refs/heads/{branch}", headers=headers,
                            timeout=60, json={"sha": new_sha, "force": False})
    update.raise_for_status()

    log(f"[checkpoint] pushed {len(changed)} file(s) to {branch} via REST "
        f"({new_sha[:8]})")
    return {"committed": True, "pushed": True, "method": "rest",
            "commit_sha": new_sha, "files_pushed": len(changed)}


# ---------------------------------------------------------------------------
# git CLI fallback
# ---------------------------------------------------------------------------

def _run_git(args: list[str], cwd: str, env: dict | None = None) -> subprocess.CompletedProcess:
    full_env = dict(os.environ)
    if env:
        full_env.update(env)
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True,
                          text=True, timeout=300, env=full_env)


def _git_cli_push(token: str, repo_full_name: str, branch: str, message: str,
                  paths: list[str], repo_root: Path, log) -> dict:
    cwd = str(repo_root)
    if not (repo_root / ".git").exists():
        return {"committed": False, "pushed": False, "method": "git",
                "error": "not a git workspace"}

    for key, default in (("user.email", "validation-bot@users.noreply.github.com"),
                         ("user.name", "validation-engine")):
        r = _run_git(["config", key], cwd)
        if r.returncode != 0 or not r.stdout.strip():
            _run_git(["config", key, default], cwd)

    status = _run_git(["status", "--porcelain", "--"] + paths, cwd)
    committed = False
    if status.stdout.strip():
        _run_git(["add", "--"] + paths, cwd)
        commit = _run_git(["commit", "-m", message], cwd)
        committed = commit.returncode == 0

    token_env = {"GH_PUSH_TOKEN": token}
    push_args = ["-c", f"credential.helper={_CREDENTIAL_HELPER}",
                 "push", f"https://github.com/{repo_full_name}.git",
                 f"HEAD:refs/heads/{branch}"]
    last_err = ""
    for attempt in range(PUSH_RETRIES):
        result = _run_git(push_args, cwd, env=token_env)
        if result.returncode == 0:
            log(f"[checkpoint] pushed to {branch} via git CLI")
            return {"committed": committed, "pushed": True, "method": "git"}
        last_err = _redact(result.stderr.strip(), token)[:300]
        log(f"[checkpoint] git push attempt {attempt + 1}/{PUSH_RETRIES} failed: {last_err}")
        if any(k in last_err for k in ("rejected", "fetch first", "non-fast-forward")):
            _run_git(["-c", f"credential.helper={_CREDENTIAL_HELPER}",
                      "pull", "--rebase",
                      f"https://github.com/{repo_full_name}.git", branch],
                     cwd, env=token_env)
        if attempt < PUSH_RETRIES - 1:
            time.sleep(PUSH_BACKOFF_SECONDS[attempt])
    return {"committed": committed, "pushed": False, "method": "git", "error": last_err}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def checkpoint(message: str, paths: list[str], cfg, repo_root: Path,
               push_failures_file: Path | None = None, log=print) -> dict:
    """Push the given output paths to cfg.target_branch.

    cfg needs: github_token, repo_full_name, target_branch.
    Never raises; on failure logs to push_failures.jsonl and returns the error
    (with the token redacted). Local output is always preserved.
    """
    token = getattr(cfg, "github_token", "") or ""
    repo_full_name = getattr(cfg, "repo_full_name", "")
    branch = getattr(cfg, "target_branch", "")

    if not token.strip():
        log("[checkpoint] GitHub token not configured; skipping push "
            "(local output preserved)")
        return {"committed": False, "pushed": False, "skipped": "no_token"}

    files = collect_output_files(repo_root, paths)
    if not files:
        return {"committed": False, "pushed": False, "skipped": "no_files"}

    rest_error = None
    for attempt in range(PUSH_RETRIES):
        try:
            return _rest_push_once(token, repo_full_name, branch, message,
                                   files, repo_root, log)
        except Exception as e:  # noqa: BLE001 - any transport error is retryable
            rest_error = _redact(f"{e.__class__.__name__}: {e}", token)[:300]
            log(f"[checkpoint] REST push attempt {attempt + 1}/{PUSH_RETRIES} "
                f"failed: {rest_error}")
            if attempt < PUSH_RETRIES - 1:
                time.sleep(PUSH_BACKOFF_SECONDS[attempt])

    log("[checkpoint] REST push failed after retries; trying git CLI fallback")
    try:
        result = _git_cli_push(token, repo_full_name, branch, message, paths,
                               repo_root, log)
    except Exception as e:  # noqa: BLE001
        result = {"committed": False, "pushed": False, "method": "git",
                  "error": _redact(f"{e.__class__.__name__}: {e}", token)[:300]}

    if not result.get("pushed"):
        failure = {
            "failed_at": _utcnow(),
            "message": message,
            "rest_error": rest_error,
            "git_error": result.get("error"),
            "note": "local output preserved; push can be retried",
        }
        if push_failures_file is not None:
            push_failures_file.parent.mkdir(parents=True, exist_ok=True)
            with push_failures_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(failure, ensure_ascii=False) + "\n")
        result["push_failure"] = failure
    return result
