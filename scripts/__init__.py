"""GPT-5.4 Israeli-market vehicle model technical-catalog runner.

One production path only: for each make/model cluster, GPT-5.4 answers a single
grounded question — what technical versions were actually sold in Israel? —
and Python validates the returned profile. GPT-5.4 is the only model and there
is no fallback model.
"""

__all__ = [
    "config",
    "data_loader",
    "json_utils",
    "catalog_grouping",
    "catalog_normalization",
    "catalog_validation",
    "openai_catalog_client",
    "catalog_builder",
    "catalog_checkpoint",
    "github_checkpoint",
]
