"""Gemini 3.1 sampled Israeli-market vehicle variant validation engine.

Core principle: vehicle identity is strict, trim enrichment is flexible.
A real Israeli-market variant must not be rejected only because the trim is
weak, generic, missing, or hard to verify.
"""

__all__ = [
    "data_loader",
    "normalization",
    "clustering",
    "output_writer",
    "validator_engine",
    "gemini_client",
    "github_checkpoint",
    "run_paths",
    "contamination",
]
