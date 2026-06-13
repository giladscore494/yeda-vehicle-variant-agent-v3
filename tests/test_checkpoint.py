import json
import os

from scripts.github_checkpoint import _is_secrets_path, _parse_owner_repo, _redact
from scripts.output_writer import OutputStore, atomic_write_json, build_output_row


def test_atomic_write_no_corruption(tmp_path):
    p = os.path.join(tmp_path, "out.json")
    atomic_write_json(p, {"a": 1, "b": [1, 2, 3]})
    assert json.load(open(p))["b"] == [1, 2, 3]
    # overwrite stays valid
    atomic_write_json(p, {"a": 2})
    assert json.load(open(p)) == {"a": 2}
    assert not os.path.exists(p + ".tmp")


def test_checkpoint_resume_skips_completed(tmp_path):
    out = os.path.join(tmp_path, "o.json")
    cp = os.path.join(tmp_path, "o.checkpoint.json")
    s1 = OutputStore(out, cp)
    s1.record(build_output_row("VAL-000001", validation_decision="clean_partial"))
    s1.record(build_output_row("VAL-000002", validation_decision="reject"))
    s1.flush()

    s2 = OutputStore(out, cp)
    s2.load_existing()
    assert s2.is_completed("VAL-000001")
    assert s2.is_completed("VAL-000002")
    assert s2.metadata["decision_counts"]["clean_partial"] == 1
    assert s2.metadata["decision_counts"]["reject"] == 1


def test_decision_counts_consistent_after_overwrite(tmp_path):
    out = os.path.join(tmp_path, "o.json")
    cp = os.path.join(tmp_path, "o.checkpoint.json")
    s = OutputStore(out, cp)
    s.record(build_output_row("VAL-1", validation_decision="clean_exact"))
    s.record(build_output_row("VAL-1", validation_decision="clean_partial"))
    assert s.metadata["decision_counts"]["clean_exact"] == 0
    assert s.metadata["decision_counts"]["clean_partial"] == 1
    assert len(s.validated_by_id) == 1


def test_parse_owner_repo_handles_proxy_and_ssh():
    assert _parse_owner_repo("git@github.com:owner/repo.git") == "owner/repo"
    assert (
        _parse_owner_repo("http://local_proxy@127.0.0.1:3/git/owner/repo")
        == "owner/repo"
    )


def test_secrets_path_guard():
    assert _is_secrets_path(".streamlit/secrets.toml")
    assert _is_secrets_path("config.env")
    assert not _is_secrets_path("data/validated_vehicle_variants_full_gemini31_v1.json")


def test_redact_strips_tokens():
    msg = "failed with ghp_abcdefghijklmnopqrstuvwxyz0123456789"
    assert "ghp_" not in _redact(msg)


def test_github_module_has_no_token_print():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    text = open(os.path.join(here, "scripts", "github_checkpoint.py")).read()
    # No print statement that references the token.
    for chunk in text.split("print(")[1:]:
        assert "token" not in chunk[:120].lower()
