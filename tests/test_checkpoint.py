import os

from scripts.github_checkpoint import _is_secrets_path, _parse_owner_repo, _redact


def test_parse_owner_repo_handles_proxy_and_ssh():
    assert _parse_owner_repo("git@github.com:owner/repo.git") == "owner/repo"
    assert (
        _parse_owner_repo("http://local_proxy@127.0.0.1:3/git/owner/repo")
        == "owner/repo"
    )


def test_secrets_path_guard():
    assert _is_secrets_path(".streamlit/secrets.toml")
    assert _is_secrets_path("config.env")
    assert not _is_secrets_path("data/model_technical_catalog_il.json")


def test_redact_strips_tokens():
    msg = "failed with ghp_abcdefghijklmnopqrstuvwxyz0123456789"
    assert "ghp_" not in _redact(msg)


def test_github_module_has_no_token_print():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    text = open(os.path.join(here, "scripts", "github_checkpoint.py")).read()
    # No print statement that references the token.
    for chunk in text.split("print(")[1:]:
        assert "token" not in chunk[:120].lower()
