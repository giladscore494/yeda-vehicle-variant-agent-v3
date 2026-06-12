"""Tests for per-model context manager and reset outputs."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import model_context as mctx  # noqa: E402
import reset_outputs  # noqa: E402


# ── model_context tests ──────────────────────────────────────────────────

class TestWeakSourceName:
    def test_none_is_weak(self):
        assert mctx.is_weak_source_name(None) is True

    def test_empty_is_weak(self):
        assert mctx.is_weak_source_name("") is True

    def test_base_is_weak(self):
        assert mctx.is_weak_source_name("Base") is True

    def test_standard_is_weak(self):
        assert mctx.is_weak_source_name("standard") is True

    def test_unknown_is_weak(self):
        assert mctx.is_weak_source_name("Unknown") is True

    def test_na_is_weak(self):
        assert mctx.is_weak_source_name("N/A") is True

    def test_null_string_is_weak(self):
        assert mctx.is_weak_source_name("null") is True

    def test_real_trim_not_weak(self):
        assert mctx.is_weak_source_name("Sport") is False

    def test_real_trim_competizione(self):
        assert mctx.is_weak_source_name("Competizione") is False


class TestFreshContext:
    def test_creates_with_defaults(self):
        ctx = mctx.fresh_context("Toyota", "Corolla")
        assert ctx["make"] == "Toyota"
        assert ctx["model"] == "Corolla"
        assert ctx["market_scope"] == "IL"
        assert ctx["completed"] is False
        assert ctx["processed_model_variants_count"] == 0
        assert ctx["known_or_candidate_israeli_trims"] == []

    def test_accepts_global_model_name(self):
        ctx = mctx.fresh_context("BMW", "3 Series", "BMW 3 Series")
        assert ctx["global_model_name"] == "BMW 3 Series"


class TestTechnicalFingerprint:
    def test_builds_from_sv(self):
        sv = {
            "make": "Toyota", "model": "Corolla",
            "year_start": 2020, "year_end": 2023,
            "engine": "1.6L", "transmission": "CVT",
            "fuel_type": "Gasoline", "body_type": "Sedan",
            "drivetrain": "FWD", "seats": 5, "generation": "E210",
        }
        fp = mctx.build_technical_fingerprint(sv)
        assert fp["make"] == "Toyota"
        assert fp["engine"] == "1.6L"
        assert fp["market_scope"] == "IL"

    def test_missing_fields_get_none(self):
        fp = mctx.build_technical_fingerprint({"make": "BMW"})
        assert fp["model"] is None
        assert fp["market_scope"] == "IL"


class TestUpdateContext:
    def test_increments_count(self):
        ctx = mctx.fresh_context("Abarth", "500")
        mctx.update_context_after_variant(
            ctx, "VAL-001", {"trim": "Competizione"}, "auto_accept",
            {"corrected_variant": {"trim": "Competizione"}}, {})
        assert ctx["processed_model_variants_count"] == 1
        assert "VAL-001" in ctx["already_resolved_variants"]

    def test_records_weak_source(self):
        ctx = mctx.fresh_context("Abarth", "500")
        mctx.update_context_after_variant(
            ctx, "VAL-002", {"trim": "Base"}, "auto_resolved",
            {"corrected_variant": {"trim": "Turismo"}}, {})
        assert any("weak" in w for w in ctx["source_quality_warnings"])
        assert "Turismo" in ctx["known_or_candidate_israeli_trims"]

    def test_records_rejected(self):
        ctx = mctx.fresh_context("Abarth", "500")
        mctx.update_context_after_variant(
            ctx, "VAL-003", {"trim": "?"}, "rejected_from_clean", None, {})
        assert "VAL-003" in ctx["already_rejected_variants"]


class TestFinalizeAndReset:
    def test_finalize_sets_completed(self):
        ctx = mctx.fresh_context("Toyota", "Corolla")
        final = mctx.finalize_context(ctx)
        assert final["completed"] is True
        assert "completed_at" in final

    def test_save_and_clear_active(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir)
            ctx = mctx.fresh_context("BMW", "X5")
            mctx.save_active_context(ctx, out)
            active_path = out / "active_model_context.json"
            assert active_path.exists()
            loaded = json.loads(active_path.read_text())
            assert loaded["make"] == "BMW"

            mctx.clear_active_context(out)
            cleared = json.loads(active_path.read_text())
            assert cleared["status"] == "no_active_model"

    def test_save_final_model_context(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir) / "model_runs" / "bmw" / "x5"
            ctx = mctx.fresh_context("BMW", "X5")
            ctx = mctx.finalize_context(ctx)
            path = mctx.save_final_model_context(ctx, run_dir)
            assert path.exists()
            loaded = json.loads(path.read_text())
            assert loaded["completed"] is True


class TestContextSummaryForPrompt:
    def test_compact_summary(self):
        ctx = mctx.fresh_context("Toyota", "Corolla")
        ctx["known_or_candidate_israeli_trims"] = ["LE", "XLE"]
        summary = mctx.context_summary_for_prompt(ctx)
        assert summary["make"] == "Toyota"
        assert summary["known_or_candidate_trims"] == ["LE", "XLE"]
        assert "processed_so_far" in summary
        # Should not have raw internal lists
        assert "already_resolved_variants" not in summary


class TestDiscoveredMissingVariants:
    def test_build_record(self):
        mctx.reset_discovery_counter()
        rec = mctx.build_discovered_missing_variant(
            "Toyota", "Corolla", "Toyota Corolla", "GR Sport",
            {"evidence_summary": "found on yad2.co.il", "lineup_position": "performance"},
            "VAL-000042")
        assert rec["discovery_id"] == "DISC-000001"
        assert rec["discovered_trim"] == "GR Sport"
        assert rec["make"] == "Toyota"
        assert "expansion candidate" in rec["reason_not_added_to_clean"]
        assert rec["suggested_future_action"] == "review in future missing-variant expansion pass"

    def test_append_to_files(self):
        mctx.reset_discovery_counter()
        with tempfile.TemporaryDirectory() as tmpdir:
            global_path = Path(tmpdir) / "discovered.jsonl"
            model_path = Path(tmpdir) / "model" / "discovered.jsonl"
            rec = mctx.build_discovered_missing_variant(
                "BMW", "3 Series", None, "M340i",
                {"evidence_summary": "test"}, "VAL-001")
            mctx.append_discovered_missing(rec, global_path, model_path)
            assert global_path.exists()
            assert model_path.exists()
            g_lines = global_path.read_text().strip().split("\n")
            assert len(g_lines) == 1
            assert json.loads(g_lines[0])["discovered_trim"] == "M340i"


class TestGroupByMakeModel:
    def test_groups_correctly(self):
        variants = {
            "V1": {"standard_variant": {"make": "Toyota", "model": "Corolla"}},
            "V2": {"standard_variant": {"make": "Toyota", "model": "Corolla"}},
            "V3": {"standard_variant": {"make": "BMW", "model": "X5"}},
        }
        groups = mctx.group_by_make_model(variants)
        assert ("Toyota", "Corolla") in groups
        assert len(groups[("Toyota", "Corolla")]) == 2
        assert ("BMW", "X5") in groups


class TestModelRunDir:
    def test_correct_path(self):
        d = mctx.model_run_dir(Path("/output"), "Abarth", "500")
        assert d == Path("/output/model_runs/abarth/500")


# ── reset_outputs tests ──────────────────────────────────────────────────

class TestResetOutputs:
    def test_archive_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "output"
            out.mkdir()
            result = reset_outputs.archive_and_reset(out, log=lambda _: None)
            assert result["status"] == "nothing_to_archive"

    def test_archive_generated_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "output"
            out.mkdir()
            (out / "validation_results.jsonl").write_text("{}\n")
            (out / "canonical_variants_clean.jsonl").write_text("{}\n")
            (out / "validation_progress.json").write_text("{}")

            result = reset_outputs.archive_and_reset(out, log=lambda _: None)
            assert result["status"] == "archived"
            assert result["files_archived"] == 3
            # Originals should be gone
            assert not (out / "validation_results.jsonl").exists()
            assert not (out / "canonical_variants_clean.jsonl").exists()
            # .gitkeep should survive/be created
            assert (out / ".gitkeep").exists()
            # Archive should exist
            archive_dirs = [d for d in out.iterdir() if d.name.startswith("archive_reset_")]
            assert len(archive_dirs) == 1

    def test_does_not_touch_protected_files(self):
        """Reset only operates on output/ — data/ files are never touched."""
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / "data"
            data_dir.mkdir()
            src = data_dir / "validation_variants_data_v1.json"
            src.write_text('{"variants": []}')
            out = Path(tmpdir) / "output"
            out.mkdir()
            reset_outputs.archive_and_reset(out, log=lambda _: None)
            # Source file must still exist
            assert src.exists()
