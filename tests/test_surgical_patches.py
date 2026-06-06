import json
from pathlib import Path

from core.paths import (
    ACTIVE_WORKING_DATABASE_PATH,
    DECISIONS_PATH,
    PATCHES_PATH,
    SOURCE_CANONICAL_PATH,
)
from engine.validation.surgical_patches import build_candidate_surgical_patches, apply_surgical_patches


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def test_build_candidate_surgical_patches_requires_exact_variant_and_field(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_json(
        tmp_path / DECISIONS_PATH,
        {
            "decisions": [
                {
                    "decision_id": "d1",
                    "source": "manual",
                    "variant_id": "v1",
                    "field": "trim.value",
                    "suggested_value": "GLI",
                    "safe_to_auto_apply": True,
                },
                {"decision_id": "d2", "source": "manual", "field": "trim.value", "suggested_value": "X"},
            ]
        },
    )

    payload = build_candidate_surgical_patches()

    assert payload["patch_count"] == 1
    assert payload["patches"][0]["variant_id"] == "v1"
    assert payload["patches"][0]["field"] == "trim.value"
    assert (tmp_path / PATCHES_PATH).exists()


def test_apply_surgical_patches_updates_working_copy_only(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = {
        "verified_variants": [
            {"variant_id": "v1", "trim": {"value": "Old"}},
            {"variant_id": "v2", "trim": {"value": "Keep"}},
        ],
        "partial_variants": [],
    }
    _write_json(tmp_path / SOURCE_CANONICAL_PATH, source)
    _write_json(tmp_path / ACTIVE_WORKING_DATABASE_PATH, source)
    _write_json(
        tmp_path / PATCHES_PATH,
        {
            "patches": [
                {
                    "patch_id": "sp_1",
                    "variant_id": "v1",
                    "field": "trim.value",
                    "suggested_value": "New",
                    "safe_to_auto_apply": True,
                }
            ]
        },
    )

    result = apply_surgical_patches(run_diff_audit=False)

    working = json.loads((tmp_path / ACTIVE_WORKING_DATABASE_PATH).read_text(encoding="utf-8"))
    canonical = json.loads((tmp_path / SOURCE_CANONICAL_PATH).read_text(encoding="utf-8"))
    assert result["applied_count"] == 1
    assert working["verified_variants"][0]["trim"]["value"] == "New"
    assert canonical["verified_variants"][0]["trim"]["value"] == "Old"
