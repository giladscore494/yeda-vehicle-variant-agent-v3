import json
from pathlib import Path

from core.paths import ISSUE_QUEUE_PATH, MODEL_REVIEW_PROGRESS_PATH
from engine.validation.model_review_progress import (
    completed_or_skipped_item_ids,
    mark_model_review_items,
    refresh_model_review_progress,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_refresh_model_review_progress_counts_items_and_unique_variants(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(
        tmp_path / ISSUE_QUEUE_PATH,
        {
            "items": [
                {"item_id": "iq_1", "requires_model_review": True, "variant_ids": ["v1", "v2"]},
                {"item_id": "iq_2", "requires_model_review": True, "variant_ids": ["v2"]},
                {"item_id": "iq_3", "requires_model_review": False, "variant_ids": ["v3"]},
            ]
        },
    )

    progress = refresh_model_review_progress()

    assert progress["total_model_review_items"] == 2
    assert progress["total_model_review_variants"] == 2
    assert progress["remaining_items"] == 2
    assert progress["remaining_variants"] == 2
    assert (tmp_path / MODEL_REVIEW_PROGRESS_PATH).exists()


def test_mark_model_review_items_updates_remaining_counts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(
        tmp_path / ISSUE_QUEUE_PATH,
        {
            "items": [
                {"item_id": "iq_1", "requires_model_review": True, "variant_ids": ["v1"]},
                {"item_id": "iq_2", "requires_model_review": True, "variant_ids": ["v2"]},
            ]
        },
    )
    refresh_model_review_progress()

    progress = mark_model_review_items({"iq_1": "completed", "iq_2": "skipped"})

    assert progress["completed_items"] == 1
    assert progress["skipped_items"] == 1
    assert progress["remaining_items"] == 0
    assert completed_or_skipped_item_ids() == {"iq_1", "iq_2"}
