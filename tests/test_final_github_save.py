from __future__ import annotations

from pathlib import Path

from core.paths import FINAL_CLEAN_DATABASE_PATH
from engine.validation import final_github_save as save_module


def test_refuses_if_final_file_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = save_module.save_final_clean_database_to_github()
    assert result["ok"] is False
    assert result["message"] == "Run Export Final Clean Database first."
    assert result["saved_path"] == FINAL_CLEAN_DATABASE_PATH


def test_blocks_canonical_and_sensitive_paths():
    assert save_module._is_path_blocked("data/canonical/resume_package_canonical.json") is True
    assert save_module._is_path_blocked("resume_package_canonical.json") is True
    assert save_module._is_path_blocked("tmp/test.json") is True
    assert save_module._is_path_blocked(".env") is True
    assert save_module._is_path_blocked("secrets/token.txt") is True
    assert save_module._is_path_blocked("old_project/file.json") is True


def test_saves_only_final_clean_database(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    final_path = Path(FINAL_CLEAN_DATABASE_PATH)
    final_path.parent.mkdir(parents=True, exist_ok=True)
    final_path.write_text('{"metadata":{},"vehicles":[]}', encoding="utf-8")
    (tmp_path / "data/validation/issue_queue.json").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/validation/issue_queue.json").write_text("{}", encoding="utf-8")

    monkeypatch.setattr(
        save_module.config,
        "get",
        lambda group, key, default=None: {
            ("github", "repo_owner"): "giladscore494",
            ("github", "repo_name"): "yeda-vehicle-variant-agent-v3",
            ("github", "target_branch"): "validation-v2-budgeted-dual-il-trims",
            ("github", "token"): "token",
        }.get((group, key), default or ""),
    )
    pushed = {}

    def fake_push_file(*, content, remote_path, commit_message, branch):
        pushed["remote_path"] = remote_path
        pushed["commit_message"] = commit_message
        pushed["branch"] = branch
        return {"ok": True, "commit_sha": "abc123"}

    monkeypatch.setattr(save_module, "push_file", fake_push_file)
    result = save_module.save_final_clean_database_to_github()

    assert result["ok"] is True
    assert pushed["remote_path"] == "data/final/resume_package_final_clean.json"
    assert pushed["commit_message"] == "Save final clean validation database"
    assert pushed["branch"] == "validation-v2-budgeted-dual-il-trims"
    assert "data/validation" not in pushed["remote_path"]
