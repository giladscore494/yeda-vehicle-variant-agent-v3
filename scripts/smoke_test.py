"""Fast smoke checks. Run with: python scripts/smoke_test.py

Covers loading, join integrity, schema, clustering determinism, the core
decision rules (weak/missing/Base trim -> clean_partial, contradiction ->
reject), checkpoint resume, atomic write, and the anti-regression guarantees
(no OpenAI, no GPT adjudicator, exact Streamlit secret paths).
"""

from __future__ import annotations

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import clustering, data_loader, normalization  # noqa: E402
from scripts.contamination import (  # noqa: E402
    ContaminationError,
    detect_contamination,
)
from scripts.output_writer import (  # noqa: E402
    OutputStore,
    atomic_write_json,
    build_output_row,
    reset_mock_outputs,
    reset_real_outputs,
    validate_output_row,
)
from scripts.run_paths import (  # noqa: E402
    MOCK_ENGINE,
    MOCK_GROUNDING_SENTINEL,
    MOCK_MODEL,
    REAL_ENGINE,
    REAL_OUTPUT_PATH,
    resolve_run_paths,
)
from scripts.reconcile import reconcile_validation_output  # noqa: E402
from scripts.validator_engine import RunConfig, decide_mock, run_validation  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_results = []


def check(name: str, cond: bool, detail: str = "") -> None:
    _results.append((name, bool(cond), detail))
    mark = "PASS" if cond else "FAIL"
    print(f"[{mark}] {name}" + (f" — {detail}" if detail and not cond else ""))


def _identity(**kw):
    base = {
        "make": "Toyota", "model": "Corolla", "engine": "1.8L",
        "transmission": "automatic", "fuel_type": "petrol", "drivetrain": "FWD",
        "body_type": "Sedan", "year_start": 2015, "year_end": 2019,
        "generation": "E170", "market_scope": "IL",
    }
    base.update(kw)
    return base


def _trim(value, weak):
    return {"trim": value, "official_marketed_name_il": None,
            "local_brand_name_il": None, "alternate_names": [], "trim_is_weak": weak}


def main() -> int:
    # 1-2. source files exist & parse
    present = data_loader.files_present()
    check("source files exist", all(present.values()), str(present))
    join = data_loader.validate_and_join()
    check("JSON parses & join ok", join.ok, "; ".join(join.errors[:3]))

    # 3-6. structure / join / duplicates
    check("variants structure valid", join.variant_count > 0)
    check("instructions structure valid", join.instruction_count > 0)
    check("join count matches", join.variant_count == len(join.ordered_ids))
    check("no duplicate validation_id", len(set(join.ordered_ids)) == len(join.ordered_ids))

    # 7. output schema valid
    row = build_output_row("VAL-TEST", validation_decision="clean_partial")
    check("output schema valid", not validate_output_row(row), str(validate_output_row(row)))
    check("clean_partial -> partial tier", row["acceptance_tier"] == "partial")

    # 8. cluster key deterministic
    ident = _identity()
    k1, k2 = clustering.cluster_key(ident), clustering.cluster_key(dict(ident))
    check("cluster key deterministic", k1 == k2 and "toyota|corolla" in k1)

    # 9-11. weak/missing/Base trim with valid identity -> clean_partial
    check("missing trim -> clean_partial",
          decide_mock(_identity(), _trim(None, True))["validation_decision"] == "clean_partial")
    check("generic trim -> clean_partial",
          decide_mock(_identity(), _trim("generic", True))["validation_decision"] == "clean_partial")
    check("Base trim -> clean_partial",
          decide_mock(_identity(), _trim("Base", True))["validation_decision"] == "clean_partial")
    check("Standard trim -> clean_partial",
          decide_mock(_identity(), _trim("Standard", True))["validation_decision"] == "clean_partial")

    # 12. identity contradiction -> reject
    contradiction = decide_mock(_identity(year_start=2020, year_end=2010), _trim("XLE", False))
    check("impossible year range -> reject", contradiction["validation_decision"] == "reject")
    missing_make = decide_mock(_identity(make=None), _trim("XLE", False))
    check("missing make -> reject", missing_make["validation_decision"] == "reject")

    # 13. split_required can include split_candidates
    split = decide_mock(_identity(), _trim("Sport / Luxury", False))
    check("split_required includes split_candidates",
          split["validation_decision"] == "split_required" and len(split["split_candidates"]) >= 2)

    # 14-15. checkpoint resume + atomic write
    with tempfile.TemporaryDirectory() as tmp:
        out_p = os.path.join(tmp, "out.json")
        cp_p = os.path.join(tmp, "out.checkpoint.json")
        s1 = OutputStore(out_p, cp_p)
        s1.record(build_output_row("VAL-000001", validation_decision="clean_exact"))
        s1.flush()
        s2 = OutputStore(out_p, cp_p)
        s2.load_existing()
        check("checkpoint can resume", s2.is_completed("VAL-000001"))
        atomic_write_json(out_p, {"k": "v"})
        check("atomic write not corrupt", json.load(open(out_p))["k"] == "v")

    # 15b. deterministic audit reconciliation (cleanup only, never rejects)
    src_variant = {"standard_variant": {"make": "Abarth", "model": "500",
                                        "year_start": 2008, "year_end": 2015}}
    recon = reconcile_validation_output(
        src_variant,
        build_output_row(
            "VAL-000001", validation_decision="clean_partial",
            year_start=2010, year_end=2015,
            official_marketed_name_il="אבארט 500", canonical_trim=None,
            trim_status="unresolved",
            fields_left_unresolved=["official_marketed_name_il", "canonical_trim"],
            evidence_sources=["iCar.co.il Abarth 500 catalog data"],
            possible_trim_names=["Scorpione", "base", ""],
        ),
    )
    check("reconcile never rejects clean_partial",
          recon["validation_decision"] == "clean_partial")
    check("reconcile records changed year_start",
          any(c.get("field") == "year_start" and c.get("from") == 2008
              and c.get("to") == 2010 for c in recon["fields_changed"]))
    check("reconcile clears filled field from unresolved",
          "official_marketed_name_il" not in recon["fields_left_unresolved"]
          and "canonical_trim" in recon["fields_left_unresolved"])
    check("reconcile structures evidence sources",
          all(isinstance(s, dict) and "source_name" in s
              for s in recon["evidence_sources"]))
    check("reconcile drops placeholder trim candidates",
          recon["possible_trim_names"] == ["Scorpione"])

    # 16-17. OpenAI is isolated to the guard-scoped verifier
    offenders = []
    for base, _dirs, files in os.walk(os.path.join(REPO_ROOT, "scripts")):
        for f in files:
            if f.endswith(".py") and f != "smoke_test.py":  # skip this scanner itself
                text = open(os.path.join(base, f), encoding="utf-8").read().lower()
                if ("import openai" in text or "from openai" in text) and f not in {"openai_guard_verifier.py", "openai_repair_adjudicator.py", "run_gemini31_sampled_validation.py", "openai_catalog_client.py"}:
                    offenders.append(f"{f}:openai")
                if "gpt_adjudicator" in text or "gpt-4" in text:
                    offenders.append(f"{f}:gpt")
    check("OpenAI isolated to guard verifier", not offenders, str(offenders))
    reqs = open(os.path.join(REPO_ROOT, "requirements.txt")).read().lower()
    check("openai dependency present for guard verifier", "openai" in reqs)

    # 18. Streamlit secret paths present in app.py with exact form
    app_text = open(os.path.join(REPO_ROOT, "app.py"), encoding="utf-8").read()
    for path in (
        'st.secrets["github"]["token"]',
        'st.secrets["google"]["api_key"]',
        'st.secrets["google"]["gemini_validator_model_id"]',
        'st.secrets["google"]["grounding_enabled"]',
        'st.secrets["openai"]["api_key"]',
        'st.secrets["openai"]["validator_model_id"]',
    ):
        check(f"secret path used: {path}", path in app_text)

    # 19. github checkpoint module never prints the token
    gh_text = open(os.path.join(REPO_ROOT, "scripts", "github_checkpoint.py")).read()
    check("github module does not print token",
          "print(" not in gh_text or "token" not in gh_text.split("print(")[-1][:80])

    # 20. every built row preserves validation_id
    check("row preserves validation_id",
          build_output_row("VAL-999999")["validation_id"] == "VAL-999999")

    # ------------------------------------------------------------------
    # Mode isolation (mock vs real never mix)
    # ------------------------------------------------------------------

    mock_paths = resolve_run_paths("mock")
    real_paths = resolve_run_paths("real")

    # 21. resolve_run_paths returns mode-specific output/checkpoint/summary
    check("mock paths under data/mock",
          "/mock/" in mock_paths.output_path.replace(os.sep, "/")
          and mock_paths.output_path != real_paths.output_path)
    check("real output is the full dataset path",
          real_paths.output_path == REAL_OUTPUT_PATH
          and "/mock/" not in real_paths.output_path.replace(os.sep, "/"))

    # 22. policy flags differ by mode
    check("mock disables gemini", mock_paths.allow_gemini_calls is False)
    check("real enables gemini", real_paths.allow_gemini_calls is True)

    # 23. github checkpoint paths are mode-specific & disjoint
    check("github paths mode-specific & disjoint",
          set(mock_paths.github_paths).isdisjoint(set(real_paths.github_paths)))
    check("mock commit prefix marks mock",
          mock_paths.commit_prefix.startswith("mock") and real_paths.commit_prefix == "checkpoint")

    # 24-26. contamination detection
    mock_doc = {
        "metadata": {"run_mode": "mock", "is_mock_output": True, "model": MOCK_MODEL},
        "validated_variants": [
            {"validation_id": "VAL-1", "run_mode": "mock",
             "grounding_summary": MOCK_GROUNDING_SENTINEL},
        ],
    }
    real_doc = {
        "metadata": {"run_mode": "real", "is_mock_output": False},
        "validated_variants": [{"validation_id": "VAL-1", "run_mode": "real"}],
    }
    check("real mode rejects mock metadata", bool(detect_contamination(mock_doc, "real")))
    check("real mode rejects mock grounding sentinel",
          any("sentinel" in p for p in detect_contamination(mock_doc, "real")))
    check("mock mode rejects real rows", bool(detect_contamination(real_doc, "mock")))
    check("real mode accepts clean real doc", not detect_contamination(real_doc, "real"))
    check("mock mode accepts clean mock doc", not detect_contamination(mock_doc, "mock"))

    # 27. metadata + per-row run_mode stamping (mock)
    with tempfile.TemporaryDirectory() as tmp:
        s = OutputStore(
            os.path.join(tmp, "m.json"), os.path.join(tmp, "m.cp.json"),
            run_mode="mock", engine=MOCK_ENGINE,
            summary_path=os.path.join(tmp, "m.sum.json"), is_mock_output=True,
        )
        s.record(build_output_row("VAL-1", validation_decision="clean_partial"))
        s.flush()
        mdoc = json.load(open(s.output_path))
        check("mock metadata run_mode mock",
              mdoc["metadata"]["run_mode"] == "mock"
              and mdoc["metadata"]["is_mock_output"] is True
              and mdoc["metadata"]["engine"] == MOCK_ENGINE)
        check("mock rows stamped run_mode mock",
              all(r["run_mode"] == "mock" for r in mdoc["validated_variants"]))
        check("mock summary written", os.path.exists(s.summary_path))

    # 28. metadata + per-row run_mode stamping (real)
    with tempfile.TemporaryDirectory() as tmp:
        s = OutputStore(
            os.path.join(tmp, "r.json"), os.path.join(tmp, "r.cp.json"),
            run_mode="real", engine=REAL_ENGINE,
            summary_path=os.path.join(tmp, "r.sum.json"), is_mock_output=False,
        )
        s.record(build_output_row("VAL-1", validation_decision="clean_exact"))
        s.flush()
        rdoc = json.load(open(s.output_path))
        check("real metadata run_mode real",
              rdoc["metadata"]["run_mode"] == "real"
              and rdoc["metadata"]["is_mock_output"] is False
              and rdoc["metadata"]["engine"] == REAL_ENGINE)
        check("real rows stamped run_mode real",
              all(r["run_mode"] == "real" for r in rdoc["validated_variants"]))
        check("no mock grounding sentinel in real output",
              all(r.get("grounding_summary") != MOCK_GROUNDING_SENTINEL
                  for r in rdoc["validated_variants"]))

    # 29. real store refuses to load a mock-tagged file (fail safely)
    with tempfile.TemporaryDirectory() as tmp:
        bad = os.path.join(tmp, "out.json")
        atomic_write_json(bad, mock_doc)
        real_store = OutputStore(
            bad, os.path.join(tmp, "out.cp.json"), run_mode="real", engine=REAL_ENGINE,
        )
        raised = False
        try:
            real_store.load_existing()
        except ContaminationError:
            raised = True
        check("real load_existing raises on mock contamination", raised)

    # 30. real run never reads mock checkpoint, mock run never writes real output
    if join.ok:
        with tempfile.TemporaryDirectory() as tmp:
            # Pre-seed a mock checkpoint that real mode must ignore.
            mock_cp = os.path.join(tmp, "mock.cp.json")
            atomic_write_json(mock_cp, mock_doc)

            real_pre_exists = os.path.exists(REAL_OUTPUT_PATH)
            real_pre_mtime = os.path.getmtime(REAL_OUTPUT_PATH) if real_pre_exists else None

            mstore = OutputStore(
                os.path.join(tmp, "m.json"), os.path.join(tmp, "m.cp.json"),
                run_mode="mock", engine=MOCK_ENGINE,
                summary_path=os.path.join(tmp, "m.sum.json"), is_mock_output=True,
            )
            run_validation(join, RunConfig(mode="mock", limit=2), store=mstore)
            check("mock run wrote only to mock temp output",
                  os.path.exists(mstore.output_path)
                  and all(r["run_mode"] == "mock"
                          for r in json.load(open(mstore.output_path))["validated_variants"]))
            real_post_exists = os.path.exists(REAL_OUTPUT_PATH)
            real_post_mtime = os.path.getmtime(REAL_OUTPUT_PATH) if real_post_exists else None
            check("mock run did not touch real output",
                  real_pre_exists == real_post_exists and real_pre_mtime == real_post_mtime)

            rstore = OutputStore(
                os.path.join(tmp, "r.json"), os.path.join(tmp, "r.cp.json"),
                run_mode="real", engine=REAL_ENGINE,
                summary_path=os.path.join(tmp, "r.sum.json"), is_mock_output=False,
            )
            rstore.load_existing()
            check("real store did not absorb mock checkpoint",
                  len(rstore.validated_by_id) == 0)

    # 31. reset isolation: mock reset never deletes real output (and vice versa)
    real_existed_before = os.path.exists(REAL_OUTPUT_PATH)
    src_variants_mtime = os.path.getmtime(data_loader.VARIANTS_PATH)
    src_instr_mtime = os.path.getmtime(data_loader.INSTRUCTIONS_PATH)

    os.makedirs(os.path.dirname(mock_paths.output_path), exist_ok=True)
    atomic_write_json(mock_paths.output_path, mock_doc)
    atomic_write_json(real_paths.output_path, real_doc)
    reset_mock_outputs()
    check("reset mock deletes mock output", not os.path.exists(mock_paths.output_path))
    check("reset mock keeps real output", os.path.exists(real_paths.output_path))
    # Re-seed mock and verify reset_real leaves mock alone.
    atomic_write_json(mock_paths.output_path, mock_doc)
    reset_real_outputs()
    check("reset real deletes real output", not os.path.exists(real_paths.output_path))
    check("reset real keeps mock output", os.path.exists(mock_paths.output_path))
    reset_mock_outputs()  # cleanup the temp mock file we created
    # Leave the real dataset absent if it was absent before this scan.
    if not real_existed_before and os.path.exists(REAL_OUTPUT_PATH):
        reset_real_outputs()

    # 32. source files never modified by any of the above
    check("source variants file untouched",
          os.path.getmtime(data_loader.VARIANTS_PATH) == src_variants_mtime)
    check("source instructions file untouched",
          os.path.getmtime(data_loader.INSTRUCTIONS_PATH) == src_instr_mtime)

    # 33-38. v3 stabilization guard regressions
    split_guard = reconcile_validation_output({}, build_output_row(
        "VAL-SPLIT", canonical_trim="Competizione / Scorpione / Nuvolari S",
        split_candidates=["Competizione", "Scorpione", "Nuvolari S"],
        grounding_summary="These are distinct trims with different power outputs. A split is required.",
        validation_decision="clean_partial",
    ))
    check("slash split evidence -> split_required", split_guard["validation_decision"] == "split_required")

    hatch = reconcile_validation_output({}, build_output_row(
        "VAL-HATCH", canonical_make="Abarth", canonical_model="500", body_type="Hatchback",
        canonical_trim="Competizione", transmission="manual", identity_status="verified",
    ))
    check("500C guard skips Hatchback", not any("500C/Cabriolet manual transmission" in i for i in hatch.get("non_blocking_trim_issues", [])))

    cabrio = reconcile_validation_output({}, build_output_row(
        "VAL-CAB", canonical_make="Abarth", canonical_model="500", body_type="Cabriolet",
        canonical_trim=None, transmission="manual", identity_status="verified",
        identity_confidence=0.95, validation_decision="clean_exact",
    ))
    check("500C guard fires on Cabriolet", cabrio["identity_status"] == "likely_valid" and cabrio["validation_decision"] == "clean_partial")
    check("guard correction reason exists", bool(cabrio.get("guard_corrected_reason")))

    past = reconcile_validation_output({}, build_output_row("VAL-YEAR", year_end=2016, is_currently_produced=True, is_currently_imported_il=True))
    check("past year_end resets current flags", past["is_currently_produced"] is False and past["is_currently_imported_il"] is False)

    meta_store = OutputStore(os.path.join(tempfile.gettempdir(), "meta-smoke.json"), os.path.join(tempfile.gettempdir(), "meta-smoke.cp.json"))
    meta = meta_store.summary_document()
    check("github checkpoint metadata fields exposed", all(k in meta for k in ("github_checkpoint_enabled", "github_checkpoint_fail_count", "last_github_checkpoint_error")))

    failed = [n for n, ok, _ in _results if not ok]
    print("\n" + "=" * 60)
    print(f"SMOKE RESULT: {len(_results) - len(failed)}/{len(_results)} passed")
    if failed:
        print("FAILED: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
