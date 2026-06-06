from __future__ import annotations

import json
from pathlib import Path

from engine.validation import run_events


def test_log_event_appends_jsonl(tmp_path, monkeypatch):
    events_path = tmp_path / "data/validation/run_events.jsonl"
    monkeypatch.setattr(run_events, "RUN_EVENTS_PATH", str(events_path))
    run_events.log_event({"stage": "audit", "event_type": "audit_started", "status": "started"})
    run_events.log_event({"stage": "audit", "event_type": "audit_completed", "status": "ok"})

    lines = events_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["event_type"] == "audit_started"
    assert json.loads(lines[1])["event_type"] == "audit_completed"


def test_log_event_does_not_log_api_keys(tmp_path, monkeypatch):
    events_path = tmp_path / "data/validation/run_events.jsonl"
    monkeypatch.setattr(run_events, "RUN_EVENTS_PATH", str(events_path))
    run_events.log_event(
        {
            "stage": "model_review",
            "event_type": "model_call_failed",
            "status": "failed",
            "error": "sk-secret-key-12345678901234567890",
            "request_summary": "AIzaFakeKey12345678901234567890",
        }
    )
    text = events_path.read_text(encoding="utf-8")
    assert "sk-secret-key" not in text
    assert "AIzaFakeKey" not in text
    assert "[REDACTED]" in text


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
