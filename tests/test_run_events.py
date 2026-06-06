from __future__ import annotations

import json
from pathlib import Path

from engine.validation import run_events


def _read_events(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_log_event_appends_jsonl_and_drops_unknown_fields(tmp_path, monkeypatch):
    events_path = tmp_path / "data/validation/run_events.jsonl"
    monkeypatch.setattr(run_events, "RUN_EVENTS_PATH", str(events_path))
    run_events.log_event(
        {
            "stage": "audit",
            "event_type": "audit_started",
            "status": "started",
            "extra_field": "must_drop",
            "raw_prompt": "must_not_persist",
        }
    )
    run_events.log_event({"stage": "audit", "event_type": "audit_completed", "status": "ok", "raw_response": "hidden"})

    rows = _read_events(events_path)
    assert len(rows) == 2
    assert rows[0]["event_type"] == "audit_started"
    assert rows[1]["event_type"] == "audit_completed"
    assert "extra_field" not in rows[0]
    assert "raw_prompt" not in rows[0]
    assert "raw_response" not in rows[1]


def test_log_event_redacts_sensitive_keys_and_values(tmp_path, monkeypatch):
    events_path = tmp_path / "data/validation/run_events.jsonl"
    monkeypatch.setattr(run_events, "RUN_EVENTS_PATH", str(events_path))
    run_events.log_event(
        {
            "stage": "model_review",
            "event_type": "model_call_failed",
            "status": "failed",
            "request_summary": {
                "Authorization": "******",
                "nested": [{"api_key": "sk-secret-key-12345678901234567890"}],
            },
            "response_summary": {
                "token": "ghp_abcdefghijklmnopqrstuvwxyz123456",
                "details": [{"github_token": "github_pat_abcdefghijklmnopqrstuvwxyz1234567890"}],
            },
            "error": "sk-error-token-12345678901234567890",
        }
    )
    stored = _read_events(events_path)[0]
    assert "[REDACTED]" in stored["request_summary"]
    assert "[REDACTED]" in stored["response_summary"]
    assert stored["error"] == "[REDACTED]"
    text = events_path.read_text(encoding="utf-8")
    assert "sk-error-token-12345678901234567890" not in text
    assert "ghp_abcdefghijklmnopqrstuvwxyz123456" not in text
    assert "github_pat_abcdefghijklmnopqrstuvwxyz1234567890" not in text


def test_log_event_redacts_nested_secrets_and_truncates_text_fields(tmp_path, monkeypatch):
    events_path = tmp_path / "data/validation/run_events.jsonl"
    monkeypatch.setattr(run_events, "RUN_EVENTS_PATH", str(events_path))
    long_text = "x" * 800
    run_events.log_event(
        {
            "stage": "model_review",
            "event_type": "model_call_completed",
            "status": "ok",
            "variant_ids": ["v1", "v2"],
            "request_summary": long_text,
            "response_summary": long_text,
            "error": long_text,
            "cost_estimate": {"secret": "value", "nested": [{"password": "abc123"}]},
        }
    )
    stored = _read_events(events_path)[0]
    assert stored["variant_ids"] == ["v1", "v2"]
    assert len(stored["request_summary"]) <= 500
    assert len(stored["response_summary"]) <= 500
    assert len(stored["error"]) <= 500
    assert stored["cost_estimate"]["secret"] == "[REDACTED]"
    assert stored["cost_estimate"]["nested"][0]["password"] == "[REDACTED]"


def test_load_recent_events_returns_compact_list(tmp_path, monkeypatch):
    events_path = tmp_path / "data/validation/run_events.jsonl"
    monkeypatch.setattr(run_events, "RUN_EVENTS_PATH", str(events_path))
    for idx in range(30):
        run_events.log_event(
            {
                "stage": "model_review",
                "event_type": "model_call_completed",
                "status": "ok",
                "provider": "openai",
                "model": "gpt-5.4",
                "item_id": f"iq_{idx}",
                "response_summary": f"done-{idx}",
            }
        )

    rows = run_events.load_recent_events(limit=20)
    assert len(rows) == 20
    assert rows[-1]["summary"] == "done-29"
    assert set(rows[-1].keys()) == {"time", "stage", "provider", "model", "item_id", "status", "summary"}


def test_log_event_redacts_secret_like_token_prefixes(tmp_path, monkeypatch):
    events_path = tmp_path / "data/validation/run_events.jsonl"
    monkeypatch.setattr(run_events, "RUN_EVENTS_PATH", str(events_path))
    run_events.log_event(
        {
            "stage": "github_save",
            "event_type": "github_save_failed",
            "status": "failed",
            "request_summary": "save attempt",
            "response_summary": "github_pat_abcdefghijklmnopqrstuvwxyz1234567890",
            "error": "sk-abcdefghijklmnopqrstuvwxyz1234567890",
        }
    )
    text = events_path.read_text(encoding="utf-8")
    assert "github_pat_abcdefghijklmnopqrstuvwxyz1234567890" not in text
    assert "sk-abcdefghijklmnopqrstuvwxyz1234567890" not in text
