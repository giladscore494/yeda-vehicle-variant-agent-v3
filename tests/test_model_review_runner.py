import json
import pytest

from engine.validation import model_review_runner as runner


def _issue(idx, **overrides):
    item = {
        "item_id": f"iq_{idx:06d}",
        "seed_id": f"seed_{idx}",
        "make": "Toyota",
        "model": "Corolla",
        "issue_type": "evidence_gap",
        "risk_level": "high",
        "requires_model_review": True,
    }
    item.update(overrides)
    return item


def _write_queue(path, items):
    path.write_text(json.dumps({"items": items}, ensure_ascii=False), encoding="utf-8")


def _write_decisions(path):
    path.write_text(json.dumps({"decisions": []}, ensure_ascii=False), encoding="utf-8")


@pytest.fixture(autouse=True)
def _isolate_runner_side_effects(monkeypatch, tmp_path):
    monkeypatch.setattr(runner, "MODEL_REVIEW_PROGRESS_PATH", str(tmp_path / "model_review_progress.json"))
    monkeypatch.setattr(runner, "log_event", lambda *args, **kwargs: None)


def test_dry_run_performs_zero_model_calls(monkeypatch, tmp_path):
    issue_path = tmp_path / "issue_queue.json"
    decisions_path = tmp_path / "decisions.json"
    _write_queue(issue_path, [_issue(1)])
    _write_decisions(decisions_path)
    monkeypatch.setattr(runner, "ISSUE_QUEUE_PATH", str(issue_path))
    monkeypatch.setattr(runner, "DECISIONS_PATH", str(decisions_path))

    calls = {"gemini": 0, "openai": 0}
    monkeypatch.setattr(runner, "call_gemini_for_issue", lambda *args, **kwargs: calls.__setitem__("gemini", calls["gemini"] + 1))
    monkeypatch.setattr(runner, "call_openai_for_issue", lambda *args, **kwargs: calls.__setitem__("openai", calls["openai"] + 1))

    result = runner.run_model_review(dry_run=True)

    assert result["selected_items"] == 1
    assert result["planned_gemini_calls"] == 1
    assert result["planned_openai_calls"] == 1
    assert calls == {"gemini": 0, "openai": 0}
    assert json.loads(decisions_path.read_text(encoding="utf-8"))["decisions"] == []


def test_max_items_limits_selected_items(monkeypatch, tmp_path):
    issue_path = tmp_path / "issue_queue.json"
    _write_queue(issue_path, [_issue(i) for i in range(5)])
    monkeypatch.setattr(runner, "ISSUE_QUEUE_PATH", str(issue_path))

    result = runner.run_model_review(max_items=2, dry_run=True)

    assert result["selected_items"] == 2
    assert len(result["items"]) == 2


def test_risk_issue_and_seed_filters_work(monkeypatch, tmp_path):
    issue_path = tmp_path / "issue_queue.json"
    _write_queue(
        issue_path,
        [
            _issue(1, risk_level="high", issue_type="evidence_gap", seed_id="target_seed"),
            _issue(2, risk_level="medium", issue_type="trim_completeness", seed_id="target_seed"),
            _issue(3, risk_level="high", issue_type="source_conflict", seed_id="other_seed"),
        ],
    )
    monkeypatch.setattr(runner, "ISSUE_QUEUE_PATH", str(issue_path))

    result = runner.run_model_review(
        max_items=10,
        risk_levels=["high"],
        issue_types=["evidence_gap"],
        seed_id_filter="target_seed",
        dry_run=True,
    )

    assert result["selected_items"] == 1
    assert result["items"][0]["item_id"] == "iq_000001"


def test_budget_guardrail_blocks_too_large_run(monkeypatch, tmp_path):
    issue_path = tmp_path / "issue_queue.json"
    _write_queue(issue_path, [_issue(i) for i in range(11)])
    monkeypatch.setattr(runner, "ISSUE_QUEUE_PATH", str(issue_path))

    result = runner.run_model_review(max_items=11, dry_run=True)

    assert result["ok"] is False
    assert result["error"] == "budget_guardrail_blocked"
    assert result["selected_items"] == 11
    assert result["planned_total_calls"] == 22


def test_model_decisions_always_safe_to_auto_apply_false(monkeypatch, tmp_path):
    issue_path = tmp_path / "issue_queue.json"
    decisions_path = tmp_path / "decisions.json"
    _write_queue(issue_path, [_issue(1)])
    _write_decisions(decisions_path)
    monkeypatch.setattr(runner, "ISSUE_QUEUE_PATH", str(issue_path))
    monkeypatch.setattr(runner, "DECISIONS_PATH", str(decisions_path))

    monkeypatch.setattr(
        runner,
        "call_gemini_for_issue",
        lambda *args, **kwargs: {
            "ok": True,
            "provider": "gemini",
            "parsed_result": {"recommendation": "reject", "confidence": 0.9, "safe_to_auto_apply": True},
        },
    )
    monkeypatch.setattr(
        runner,
        "call_openai_for_issue",
        lambda *args, **kwargs: {
            "ok": True,
            "provider": "openai",
            "parsed_result": {"recommendation": "merge", "confidence": 0.8, "safe_to_auto_apply": True},
        },
    )

    result = runner.run_model_review(max_items=1, dry_run=False)

    payload = json.loads(decisions_path.read_text(encoding="utf-8"))
    decision = payload["decisions"][0]
    assert result["decisions_written"] == 1
    assert decision["safe_to_auto_apply"] is False
    assert decision["requires_manual_approval"] is True
    assert decision["gemini_result"]["safe_to_auto_apply"] is False
    assert decision["openai_result"]["safe_to_auto_apply"] is False
    assert decision["final_recommendation"] == "manual_approval_required:merge"


def test_requires_model_review_false_filtered_before_routing(monkeypatch, tmp_path):
    issue_path = tmp_path / "issue_queue.json"
    _write_queue(issue_path, [_issue(1, requires_model_review=False), _issue(2)])
    monkeypatch.setattr(runner, "ISSUE_QUEUE_PATH", str(issue_path))

    result = runner.run_model_review(max_items=10, dry_run=True)

    assert result["selected_items"] == 1
    assert result["items"][0]["item_id"] == "iq_000002"


def test_failed_item_is_not_selected_again(monkeypatch, tmp_path):
    issue_path = tmp_path / "issue_queue.json"
    decisions_path = tmp_path / "decisions.json"
    _write_queue(issue_path, [_issue(1), _issue(2)])
    _write_decisions(decisions_path)
    monkeypatch.setattr(runner, "ISSUE_QUEUE_PATH", str(issue_path))
    monkeypatch.setattr(runner, "DECISIONS_PATH", str(decisions_path))
    monkeypatch.setattr(
        runner,
        "call_gemini_for_issue",
        lambda *args, **kwargs: {"ok": False, "provider": "gemini", "error_message": "unconfigured"},
    )
    monkeypatch.setattr(
        runner,
        "call_openai_for_issue",
        lambda *args, **kwargs: {"ok": False, "provider": "openai", "error_message": "unconfigured"},
    )

    first = runner.run_model_review(max_items=1, dry_run=False)
    second = runner.run_model_review(max_items=1, dry_run=True)

    assert first["model_review_progress"]["items"]["iq_000001"]["status"] == "failed"
    assert first["model_review_progress"]["remaining_items"] == 1
    assert second["selected_items"] == 1
    assert second["items"][0]["item_id"] == "iq_000002"
