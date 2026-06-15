"""Model-level GitHub checkpointing for the GPT-5.4 technical catalog.

The new pipeline does NOT validate per variant, so it must not push after every
raw variant row. Instead it checkpoints after each completed make/model profile
(``push_every_profiles`` controls the cadence; the real-run default is 1).

After a completed profile it writes the generated catalog files and pushes them
to GitHub via the existing Contents-API saver. Tokens are read from the
``[github].token`` secret, and are never printed, logged, written to output,
or included in errors.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from .github_checkpoint import (
    GitHubCheckpoint,
    GitHubConfig,
    _redact,
    detect_branch,
    detect_repo,
)

GITHUB_SECRET_REQUIRED_MESSAGE = (
    "[github].token is required for GitHub checkpoint pushes, or disable "
    "GitHub autosave for this session."
)


@dataclass
class CatalogCheckpointConfig:
    """Configuration for model-profile GitHub checkpointing."""

    enabled: bool = False
    push_every_profiles: int = 1
    strict: bool = False
    token: str = ""
    repo: Optional[str] = None
    branch: Optional[str] = None


def _default_state(enabled: bool) -> Dict[str, Any]:
    return {
        "github_checkpoint_enabled": bool(enabled),
        "github_checkpoint_unit": "model_profile",
        "github_checkpoint_count": 0,
        "github_checkpoint_fail_count": 0,
        "last_github_checkpoint_error": None,
        "last_checkpointed_profile_id": None,
    }


class CatalogCheckpointer:
    """Pushes generated catalog files to GitHub after each model profile."""

    def __init__(
        self,
        config: CatalogCheckpointConfig,
        repo_root: Optional[str] = None,
        log: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.config = config
        self.log = log or (lambda _msg: None)
        self.state = _default_state(config.enabled)
        self._client: Optional[GitHubCheckpoint] = None
        self._pending = 0

        if config.enabled:
            # [github].token is required ONLY when checkpointing is enabled.
            if not config.token:
                raise ValueError(GITHUB_SECRET_REQUIRED_MESSAGE)
            gh_config = GitHubConfig(
                token=config.token,
                repo=config.repo or "",
                branch=config.branch or "",
            )
            self._client = GitHubCheckpoint(gh_config, repo_root=repo_root)

    @property
    def enabled(self) -> bool:
        return bool(self.config.enabled and self._client is not None)

    def maybe_checkpoint(
        self,
        *,
        profile_id: str,
        paths: List[str],
        market: str,
        make: str,
        model: str,
        force: bool = False,
    ) -> bool:
        """Push generated files after a completed profile, honoring cadence.

        Returns True if a push was attempted (and succeeded). Failures are
        recorded in ``self.state`` and only re-raised when ``strict`` is set.
        """
        if not self.enabled:
            return False

        self._pending += 1
        every = max(1, int(self.config.push_every_profiles))
        if not force and self._pending < every:
            return False
        self._pending = 0

        existing = [p for p in paths if os.path.exists(p)]
        if not existing:
            return False

        # "catalog: checkpoint <market> <make> <model>"
        message = " ".join(
            part for part in ("catalog: checkpoint", market, make, model) if part
        )
        try:
            self._client.save_paths(existing, message)  # type: ignore[union-attr]
        except Exception as exc:  # noqa: BLE001 - sanitized, never crashes unless strict
            self.state["github_checkpoint_fail_count"] += 1
            self.state["last_github_checkpoint_error"] = _redact(str(exc))
            self.log(f"github checkpoint failed for {profile_id}: {_redact(str(exc))}")
            if self.config.strict:
                raise
            return False

        self.state["github_checkpoint_count"] += 1
        self.state["last_github_checkpoint_error"] = None
        self.state["last_checkpointed_profile_id"] = profile_id
        self.log(f"github checkpoint pushed for {profile_id}")
        return True
