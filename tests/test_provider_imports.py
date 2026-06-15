"""Guard against app.py / repair importing provider symbols that do not exist.

These tests fail loudly if scripts.catalog_provider stops exporting any symbol
that app.py or scripts.catalog_repair import at module load time, so the app can
never deploy with a broken provider import (e.g. the ImportError seen in
Streamlit for ProviderUnavailableError).
"""
from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest


def test_catalog_provider_exports_all_required_symbols():
    # Direct import must succeed for every symbol app.py / repair rely on.
    from scripts.catalog_provider import (  # noqa: F401
        CatalogProviderSettings,
        ProviderUnavailableError,
        check_provider_available,
        build_catalog_client,
    )

    assert issubclass(ProviderUnavailableError, RuntimeError)
    assert callable(check_provider_available)
    assert callable(build_catalog_client)


def test_provider_module_all_lists_public_symbols():
    module = importlib.import_module("scripts.catalog_provider")
    for symbol in (
        "CatalogProviderSettings",
        "ProviderUnavailableError",
        "check_provider_available",
        "build_catalog_client",
    ):
        assert hasattr(module, symbol), f"missing export: {symbol}"


def _provider_imports_in(source_path: str) -> list[str]:
    """Names imported `from scripts.catalog_provider import ...` in a file."""
    tree = ast.parse(Path(source_path).read_text(encoding="utf-8"))
    names: list[str] = []
    for node in ast.walk(tree):
        # Match both absolute (scripts.catalog_provider) and relative
        # (.catalog_provider) import forms used across the codebase.
        if isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[-1] == "catalog_provider":
            names.extend(alias.name for alias in node.names)
    return names


@pytest.mark.parametrize("source_path", ["app.py", "scripts/catalog_repair.py"])
def test_provider_consumers_only_import_existing_symbols(source_path):
    """Static guard: every provider symbol a consumer imports must exist.

    Parses the source without executing it (importing app.py would run
    Streamlit), so it catches a missing export before deploy regardless of
    whether the import is reachable at runtime.
    """
    module = importlib.import_module("scripts.catalog_provider")
    imported = _provider_imports_in(source_path)
    assert imported, f"expected {source_path} to import from scripts.catalog_provider"
    missing = [name for name in imported if not hasattr(module, name)]
    assert not missing, f"{source_path} imports missing provider symbols: {missing}"
