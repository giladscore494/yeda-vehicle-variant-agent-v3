"""Run-mode isolation: mock vs real never share files, metadata, or pushes.

This module is the single source of truth for *where* a given run mode is
allowed to read and write. Mock and real outputs are kept in completely
separate files so a final dataset can never mix mock validation rows with
real Gemini validation rows.

    mock  ->  data/mock/validated_vehicle_variants_mock_gemini31_v1.json
    real  ->  data/validated_vehicle_variants_full_gemini31_v1.json

Use :func:`resolve_run_paths` to obtain the full, immutable bundle of paths
and policy flags for a mode. Nothing else in the codebase should hard-code
these paths.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from .data_loader import DATA_DIR

# ---------------------------------------------------------------------------
# Directories
# ---------------------------------------------------------------------------

MOCK_DIR = os.path.join(DATA_DIR, "mock")

# ---------------------------------------------------------------------------
# Real-mode paths (the clean, real-only dataset)
# ---------------------------------------------------------------------------

REAL_OUTPUT_PATH = os.path.join(DATA_DIR, "validated_vehicle_variants_full_gemini31_v1.json")
REAL_CHECKPOINT_PATH = os.path.join(
    DATA_DIR, "validated_vehicle_variants_full_gemini31_v1.checkpoint.json"
)
REAL_SUMMARY_PATH = os.path.join(DATA_DIR, "validation_run_summary_gemini31.json")

# ---------------------------------------------------------------------------
# Mock-mode paths (dedicated testing stage, never the real dataset)
# ---------------------------------------------------------------------------

MOCK_OUTPUT_PATH = os.path.join(MOCK_DIR, "validated_vehicle_variants_mock_gemini31_v1.json")
MOCK_CHECKPOINT_PATH = os.path.join(
    MOCK_DIR, "validated_vehicle_variants_mock_gemini31_v1.checkpoint.json"
)
MOCK_SUMMARY_PATH = os.path.join(MOCK_DIR, "validation_run_summary_mock_gemini31.json")

# ---------------------------------------------------------------------------
# Engine / model identity per mode
# ---------------------------------------------------------------------------

REAL_ENGINE = "gemini31_streamlit_sampled_validation"
MOCK_ENGINE = "gemini31_streamlit_sampled_validation_mock"

REAL_MODEL_DEFAULT = "gemini-3.1-pro-preview"
MOCK_MODEL = "mock-validator"

# Sentinel only ever produced by mock grounding; forbidden in real output.
MOCK_GROUNDING_SENTINEL = "mock: no external grounding performed"

VALID_MODES = ("mock", "real")


@dataclass(frozen=True)
class RunPaths:
    """Immutable bundle describing everything a run mode is allowed to do."""

    mode: str
    output_path: str
    checkpoint_path: str
    summary_path: str
    allow_gemini_calls: bool
    allow_github_push: bool
    engine: str
    model: str
    is_mock_output: bool
    ui_label: str
    commit_prefix: str

    @property
    def github_paths(self) -> list:
        """The only files this mode may push to GitHub."""
        return [self.output_path, self.checkpoint_path, self.summary_path]


def resolve_run_paths(mode: str, model: str = REAL_MODEL_DEFAULT) -> RunPaths:
    """Resolve the path/policy bundle for ``mode`` ("mock" or "real").

    The selected mode deterministically decides output/checkpoint/summary
    paths, whether Gemini may be called, whether a real GitHub push is
    allowed, the metadata engine + model names, and the UI label.
    """
    normalized = (mode or "").strip().lower()
    if normalized == "mock":
        return RunPaths(
            mode="mock",
            output_path=MOCK_OUTPUT_PATH,
            checkpoint_path=MOCK_CHECKPOINT_PATH,
            summary_path=MOCK_SUMMARY_PATH,
            allow_gemini_calls=False,
            # Mock never pushes to the real dataset. By default it does not
            # push at all; mock-only pushes (under data/mock/) are opt-in.
            allow_github_push=False,
            engine=MOCK_ENGINE,
            model=MOCK_MODEL,
            is_mock_output=True,
            ui_label="Mock validation (no Gemini, testing stage)",
            commit_prefix="mock checkpoint",
        )
    if normalized == "real":
        return RunPaths(
            mode="real",
            output_path=REAL_OUTPUT_PATH,
            checkpoint_path=REAL_CHECKPOINT_PATH,
            summary_path=REAL_SUMMARY_PATH,
            allow_gemini_calls=True,
            allow_github_push=True,
            engine=REAL_ENGINE,
            model=model or REAL_MODEL_DEFAULT,
            is_mock_output=False,
            ui_label="Real Gemini validation (clean real-only dataset)",
            commit_prefix="checkpoint",
        )
    raise ValueError(f"Unknown run mode {mode!r}; expected one of {VALID_MODES}")


def ensure_mode_dirs(run_paths: RunPaths) -> None:
    """Create the directory for the mode's output if it is missing."""
    os.makedirs(os.path.dirname(run_paths.output_path), exist_ok=True)
