"""Git checkpointing for the validation engine.

Commits output files locally and pushes to the target branch using
GH_PUSH_TOKEN. The token is passed to git through a credential helper that
reads it from the environment, so it never appears in argv, remote URLs,
or logs.
"""

from __future__ import annotations

import os
import subprocess
import time

REPO_FULL_NAME = os.environ.get("REPO_FULL_NAME", "giladscore494/yeda-vehicle-variant-agent-v3")
TARGET_BRANCH = os.environ.get("TARGET_BRANCH", "validation-v2-budgeted-dual-il-trims")
PUSH_RETRIES = 4
PUSH_BACKOFF_SECONDS = [2, 4, 8, 16]

# Reads the token from the environment at git runtime; nothing secret on disk.
_CREDENTIAL_HELPER = (
    '!f() { echo "username=x-access-token"; echo "password=${GH_PUSH_TOKEN}"; }; f'
)


def _run(args: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=300)


def ensure_git_identity(cwd: str | None = None) -> None:
    for key, default in (("user.email", "validation-bot@users.noreply.github.com"),
                         ("user.name", "validation-engine")):
        result = _run(["git", "config", key], cwd=cwd)
        if result.returncode != 0 or not result.stdout.strip():
            _run(["git", "config", key, default], cwd=cwd)


def has_changes(paths: list[str], cwd: str | None = None) -> bool:
    result = _run(["git", "status", "--porcelain", "--"] + paths, cwd=cwd)
    return bool(result.stdout.strip())


def commit_outputs(message: str, paths: list[str], cwd: str | None = None) -> bool:
    """Stage and commit the given paths. Returns True if a commit was created."""
    ensure_git_identity(cwd)
    if not has_changes(paths, cwd):
        return False
    add = _run(["git", "add", "--"] + paths, cwd=cwd)
    if add.returncode != 0:
        print(f"[checkpoint] git add failed: {add.stderr.strip()}")
        return False
    commit = _run(["git", "commit", "-m", message], cwd=cwd)
    if commit.returncode != 0:
        if "nothing to commit" in (commit.stdout + commit.stderr):
            return False
        print(f"[checkpoint] git commit failed: {commit.stderr.strip()}")
        return False
    return True


def push(branch: str | None = None, cwd: str | None = None) -> bool:
    """Push committed work to origin/<branch> with retries and backoff.

    Requires GH_PUSH_TOKEN in the environment. Returns True on success;
    on persistent failure returns False (work stays committed locally).
    """
    branch = branch or TARGET_BRANCH
    if not os.environ.get("GH_PUSH_TOKEN"):
        print("[checkpoint] GH_PUSH_TOKEN not set; skipping push (commit kept locally)")
        return False

    push_args = [
        "git",
        "-c", f"credential.helper={_CREDENTIAL_HELPER}",
        "-c", "credential.useHttpPath=true",
        "push", f"https://github.com/{REPO_FULL_NAME}.git",
        f"HEAD:refs/heads/{branch}",
    ]
    for attempt in range(PUSH_RETRIES):
        result = _run(push_args, cwd=cwd)
        if result.returncode == 0:
            print(f"[checkpoint] pushed to {branch}")
            return True
        err = result.stderr.strip()
        if "GH_PUSH_TOKEN" in err:
            err = err.replace(os.environ.get("GH_PUSH_TOKEN", ""), "***")
        print(f"[checkpoint] push attempt {attempt + 1}/{PUSH_RETRIES} failed: {err[:300]}")
        if "rejected" in err or "fetch first" in err or "non-fast-forward" in err:
            pull = _run([
                "git",
                "-c", f"credential.helper={_CREDENTIAL_HELPER}",
                "pull", "--rebase",
                f"https://github.com/{REPO_FULL_NAME}.git",
                branch,
            ], cwd=cwd)
            if pull.returncode != 0:
                print(f"[checkpoint] rebase pull failed: {pull.stderr.strip()[:300]}")
        if attempt < PUSH_RETRIES - 1:
            time.sleep(PUSH_BACKOFF_SECONDS[attempt])
    print("[checkpoint] push failed after retries; results remain committed locally")
    return False


def checkpoint(message: str, paths: list[str], branch: str | None = None,
               cwd: str | None = None, do_push: bool = True) -> dict:
    committed = commit_outputs(message, paths, cwd=cwd)
    pushed = False
    if committed and do_push:
        pushed = push(branch, cwd=cwd)
    return {"committed": committed, "pushed": pushed}
