"""Runtime progress state for UI observability."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.config import RUNTIME_STATE_PATH

# Valid stages
STAGES = [
    "QUEUED",
    "LOADING_SEED",
    "BUILDING_PROMPT",
    "LLM_DISCOVERY",
    "PARSING_RESPONSE",
    "NORMALIZING",
    "QUALITY_GATE",
    "DECISION",
    "APPLYING_TO_CANONICAL",
    "AUDIT_BEFORE_SAVE",
    "SAVING_JSON",
    "RELOADING_JSON",
    "POST_SAVE_AUDIT",
    "PUSHING_REMOTE",
    "DONE",
    "MANUAL_REVIEW",
    "ERROR",
]


class ProgressTracker:
    """Tracks batch/seed progress. Never decides anything — only records."""

    def __init__(self, run_id: str, mode: str = "normal_batch",
                 batch_size: int = 1, state_path: str | None = None):
        self.run_id = run_id
        self.mode = mode
        self.batch_size = batch_size
        self.state_path = Path(state_path or RUNTIME_STATE_PATH)
        self.current_index = 0
        self.total = batch_size
        self.current_seed_id: str | None = None
        self.current_stage: str = "QUEUED"
        self.completed_seeds: list[dict] = []
        self.manual_review_seeds: list[str] = []
        self.failed_seeds: list[str] = []
        self.last_saved_seed_id: str | None = None
        self.last_saved_at: str | None = None
        self.last_error: str | None = None

    def set_seed(self, seed_id: str, index: int) -> None:
        self.current_seed_id = seed_id
        self.current_index = index
        self.current_stage = "LOADING_SEED"
        self._write()

    def set_stage(self, stage: str) -> None:
        self.current_stage = stage
        self._write()

    def mark_completed(self, seed_id: str, action: str,
                       added: int = 0, merged: int = 0) -> None:
        self.completed_seeds.append({
            "seed_id": seed_id,
            "action": action,
            "added_count": added,
            "merged_count": merged,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        })
        self.current_stage = "DONE"
        self._write()

    def mark_manual_review(self, seed_id: str) -> None:
        self.manual_review_seeds.append(seed_id)
        self.current_stage = "MANUAL_REVIEW"
        self._write()

    def mark_failed(self, seed_id: str, error: str) -> None:
        self.failed_seeds.append(seed_id)
        self.last_error = error
        self.current_stage = "ERROR"
        self._write()

    def mark_saved(self, seed_id: str) -> None:
        self.last_saved_seed_id = seed_id
        self.last_saved_at = datetime.now(timezone.utc).isoformat()
        self._write()

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "mode": self.mode,
            "batch_size": self.batch_size,
            "current_index": self.current_index,
            "total": self.total,
            "current_seed_id": self.current_seed_id,
            "current_stage": self.current_stage,
            "completed_seeds": self.completed_seeds,
            "manual_review_seeds": self.manual_review_seeds,
            "failed_seeds": self.failed_seeds,
            "last_saved_seed_id": self.last_saved_seed_id,
            "last_saved_at": self.last_saved_at,
            "last_error": self.last_error,
        }

    def _write(self) -> None:
        try:
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            self.state_path.write_text(
                json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception:
            pass  # Progress writing is best-effort


def generate_run_id() -> str:
    return "run_" + datetime.now(timezone.utc).strftime("%Y_%m_%d_%H%M%S")


def generate_seed_run_id(run_id: str, index: int, seed_id: str) -> str:
    return f"{run_id}__{index:03d}__{seed_id}"
