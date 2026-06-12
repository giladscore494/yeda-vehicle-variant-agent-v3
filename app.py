"""Streamlit validation runner/dashboard for the Gemini vehicle variant
validation engine (validation-v2-budgeted-dual-il-trims).

Main runtime for the real validation run. Secrets come from st.secrets
(with env fallback for local dev). The engine core lives in
scripts/run_gemini_validation.py; this app only orchestrates it.

There is NO human manual review: every variant is processed by the
automatic multi-pass flow (Pass 1 -> Pass 2 -> Pass 3) until it reaches one
final machine decision: auto_accept / auto_resolved / rejected_from_clean /
failed. Records that fail all automatic attempts are excluded from the
clean output, not sent to manual review.

Safety: nothing runs on page load. Real Gemini calls happen only after
startup checks pass, secrets are present, and the user explicitly confirms.
"""

from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import github_checkpoint  # noqa: E402
import run_gemini_validation as engine  # noqa: E402
import runtime_config  # noqa: E402
import smoke_test  # noqa: E402

st.set_page_config(page_title="Gemini Variant Validation Runner",
                   page_icon="🚗", layout="wide")

cfg = runtime_config.resolve(runtime="streamlit")
rules = engine.load_rules()
TOTAL = rules["expected_total_variants"]
paths = engine.REAL_PATHS

st.title("🚗 Gemini Variant Validation Runner")
st.caption(
    f"Runtime mode: **Streamlit validation runner** · "
    f"target branch: **{cfg.target_branch}** · model: **{cfg.model_id}** · "
    f"total input variants: **{TOTAL}**"
)
st.info("Records that fail all automatic attempts are excluded from the clean "
        "output, not sent to manual review.")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def tail_jsonl(path: Path, n: int = 10) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows[-n:]


def run_with_log(fn, *args, **kwargs):
    """Run an engine function, streaming its log lines into the UI."""
    log_box = st.empty()
    lines: list[str] = []

    def ui_log(msg: str) -> None:
        lines.append(str(msg))
        log_box.code("\n".join(lines[-40:]), language="text")

    result = fn(*args, log=ui_log, **kwargs)
    return result, lines


def progress_state() -> dict:
    raw = read_json(paths.progress)
    if raw is None:
        return engine.fresh_progress()
    return engine.migrate_progress(raw)


def startup_state() -> tuple[list[str], int, int]:
    failures, variants_by_id, instructions_by_id = engine.startup_checks(rules)
    return failures, len(variants_by_id), len(instructions_by_id)


# ---------------------------------------------------------------------------
# Sidebar: configuration & status (presence only — never secret values)
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("Status")
    rep = cfg.presence_report()
    st.write(f"**Secrets source:** {rep['secrets_source']}")
    st.write(("✅" if cfg.gemini_key_present else "❌") +
             f" Gemini API key: **{rep['gemini_api_key']}**")
    st.write(("✅" if cfg.github_token_present else "❌") +
             f" GitHub token: **{rep['github_token']}**")
    st.write(f"🌐 Grounding enabled: **{cfg.grounding_enabled}**")
    st.write(f"📦 Repo: `{cfg.repo_full_name}`")
    st.write(f"🌿 Target branch: `{cfg.target_branch}` (base: `{cfg.base_branch}`)")

    st.divider()
    st.header("Run settings")
    max_attempts = st.selectbox(
        "max_attempts (automatic validation passes per variant)",
        options=rules["allowed_max_attempts"],
        index=rules["allowed_max_attempts"].index(
            rules["max_validation_attempts_default"]),
        help="Pass 1 = full validation; passes 2+ are targeted automatic "
             "correction passes. A variant that fails every pass is "
             "rejected_from_clean (excluded from the clean output).")
    push_every = st.number_input("push_every (checkpoint push frequency)",
                                 min_value=1, max_value=500, value=1,
                                 help="1 = push after every variant (maximum safety)")
    force_reprocess = st.toggle("force_reprocess", value=False,
                                help="Reprocess validation_ids that already reached "
                                     "a final decision")
    dry_run = st.toggle("dry_run", value=False,
                        help="Build contexts only; no Gemini calls, no outputs")
    mock_mode = st.toggle("mock_mode", value=False,
                          help="Offline mock client; outputs to output/mock/; no cost")
    push_enabled = st.toggle("push checkpoints to GitHub", value=True)

    st.divider()
    st.header("Input files")
    for name in ("validation_variants_data_v1.json",
                 "validation_instructions_by_id_v1.json"):
        p = engine.resolve_input_file(name)
        st.write(("✅" if p.exists() else "❌") +
                 f" `{p.relative_to(REPO_ROOT) if p.exists() else name}`")


# ---------------------------------------------------------------------------
# Progress metrics (automatic final decisions only — no manual review)
# ---------------------------------------------------------------------------

prog = progress_state()
counts = prog["counts"]
completed = len(engine.completed_ids(prog))
in_progress = {vid: rec for vid, rec in prog["records"].items()
               if not rec.get("final_decision")}
c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
c1.metric("Total variants", TOTAL)
c2.metric("Completed", completed)
c3.metric("Accepted", counts["accepted"])
c4.metric("Auto-resolved", counts["auto_resolved"])
c5.metric("Rejected from clean", counts["rejected_from_clean"])
c6.metric("Failed", counts["failed"])
c7.metric("Max attempts", int(max_attempts))
if in_progress:
    sample_vid, sample_rec = next(iter(in_progress.items()))
    st.write(f"⏳ {len(in_progress)} variant(s) pending retry, e.g. "
             f"`{sample_vid}` at attempt {sample_rec.get('attempt_count', 0)} — "
             f"they stay in the automatic loop until a final decision.")
st.write(f"Last processed validation_id: "
         f"`{prog.get('last_processed_validation_id') or '—'}` · "
         f"run started: {prog.get('run_started_at') or '—'} · "
         f"last updated: {prog.get('last_updated_at') or '—'}")

with st.expander("Output file status"):
    for p in (paths.results, paths.canonical_jsonl, paths.rejected,
              paths.failures, paths.push_failures, paths.progress,
              paths.run_summary, paths.final_clean, paths.final_compat):
        rel = p.relative_to(REPO_ROOT)
        if p.exists():
            st.write(f"✅ `{rel}` — {p.stat().st_size:,} bytes")
        else:
            st.write(f"⬜ `{rel}` — not created yet")
    if paths.manual_review.exists():
        st.write(f"🗄️ `{paths.manual_review.relative_to(REPO_ROOT)}` — deprecated "
                 f"legacy file, no longer used by the pipeline")

st.divider()

# ---------------------------------------------------------------------------
# Section 1: checks & safe tests (no Gemini cost)
# ---------------------------------------------------------------------------

st.subheader("1 · Checks and safe tests (no Gemini calls)")
col_a, col_b, col_c, col_d = st.columns(4)

if col_a.button("Run startup checks", use_container_width=True):
    with st.spinner("Validating both input files and the ID join..."):
        failures, n_var, n_ins = startup_state()
    if failures:
        engine.write_startup_failure(paths, failures)
        st.session_state["startup_ok"] = False
        st.error(f"Startup validation FAILED ({len(failures)} issue(s)). "
                 f"Report written to `output/startup_failure_report.json`. "
                 f"Real runs are blocked.")
        st.json(failures[:20])
    else:
        st.session_state["startup_ok"] = True
        st.success(f"Startup validation passed: {n_var} variants joined 1:1 with "
                   f"{n_ins} instruction records (expected {TOTAL}).")

if col_b.button("Run smoke test", use_container_width=True):
    buf = io.StringIO()
    with st.spinner("Running smoke test..."), redirect_stdout(buf):
        ok, checks = smoke_test.run_checks()
    st.code(buf.getvalue(), language="text")
    if ok:
        st.session_state["startup_ok"] = True
        st.success(f"Smoke test PASSED ({len(checks)} checks).")
    else:
        st.session_state["startup_ok"] = False
        st.error("Smoke test FAILED — real runs are blocked until this passes.")

if col_c.button("Run dry-run (limit=3)", use_container_width=True):
    options = engine.RunOptions(limit=3, dry_run=True, push_enabled=False,
                                max_attempts=int(max_attempts))
    result, _ = run_with_log(engine.run_validation, options, cfg=cfg)
    if result["status"] == "dry_run_ok":
        st.success("Dry-run completed: contexts built, no Gemini calls made.")
    else:
        st.error(f"Dry-run failed: {result['status']}")

if col_d.button("Run mock validation (limit=3)", use_container_width=True):
    options = engine.RunOptions(limit=3, mock_mode=True,
                                push_every=int(push_every), push_enabled=False,
                                max_attempts=int(max_attempts))
    result, _ = run_with_log(engine.run_validation, options, cfg=cfg)
    if result["status"] == "ok":
        st.success(f"Mock validation completed: {result['processed_this_run']} "
                   f"variant(s) into `output/mock/` (real progress untouched, "
                   f"no Gemini calls). Counts: {result['counts']}")
    else:
        st.error(f"Mock validation failed: {result['status']}")

st.divider()

# ---------------------------------------------------------------------------
# Section 2: real validation (Gemini, gated)
# ---------------------------------------------------------------------------

st.subheader("2 · Real validation (calls Gemini)")

startup_ok = st.session_state.get("startup_ok", False)
if not startup_ok:
    st.info("Run **startup checks** or the **smoke test** above first — "
            "real validation stays locked until they pass.")
if not cfg.gemini_key_present:
    st.error("Gemini API key is missing (st.secrets `[google].api_key` or env "
             "`GEMINI_API_KEY`). Real validation is blocked.")
if not cfg.github_token_present:
    st.warning("GitHub token is missing — checkpoints will NOT be pushed. "
               "Local output is still saved after every variant.")

confirmed = st.checkbox("I understand this will call Gemini and may cost money.")
real_allowed = startup_ok and cfg.gemini_key_present and confirmed and not dry_run \
    and not mock_mode
if (dry_run or mock_mode) and confirmed:
    st.warning("dry_run / mock_mode is enabled in the sidebar — disable it to run "
               "real validation.")


def run_real(limit: int | None, label: str) -> None:
    options = engine.RunOptions(
        limit=limit,
        force_reprocess=force_reprocess,
        push_every=int(push_every),
        push_enabled=push_enabled,
        max_attempts=int(max_attempts),
    )
    st.write(f"Starting **{label}** (push_every={int(push_every)}, "
             f"force_reprocess={force_reprocess}, max_attempts={int(max_attempts)})...")
    attempt_box = st.empty()

    def on_progress(info: dict) -> None:
        if "attempt" in info:
            attempt_box.write(
                f"🔄 `{info['validation_id']}` — attempt "
                f"{info['attempt']}/{info['max_attempts']} "
                f"({info.get('decision')})")

    result, _ = run_with_log(engine.run_validation, options, cfg=cfg,
                             progress_callback=on_progress)
    status = result.get("status")
    if status == "ok":
        st.success(
            f"{label} finished: {result['processed_this_run']} processed this run, "
            f"{result['processed_total']}/{result['total_expected']} total. "
            f"Counts: {result['counts']}")
        if result.get("push_failures"):
            st.error(f"{result['push_failures']} checkpoint push(es) failed — see "
                     f"`output/push_failures.jsonl`. Local output is safe; use "
                     f"'Push current output checkpoint' to retry.")
    elif status == "startup_failed":
        st.error("Startup validation failed; see "
                 "`output/startup_failure_report.json`.")
    elif status == "blocked_no_api_key":
        st.error("Blocked: Gemini API key missing.")
    else:
        st.warning(f"Run ended with status: {status}")


col1, col2, col3 = st.columns(3)
if col1.button("▶ Run real validation (limit=3)", disabled=not real_allowed,
               use_container_width=True, type="primary"):
    run_real(3, "real validation limit=3")
if col2.button("▶ Run real validation (limit=25)", disabled=not real_allowed,
               use_container_width=True):
    run_real(25, "real validation limit=25")

with col3:
    full_confirm = st.checkbox("Confirm FULL run (all remaining variants)")
    if st.button("▶▶ Continue validation with resume (full)",
                 disabled=not (real_allowed and full_confirm),
                 use_container_width=True):
        run_real(None, "full validation with resume")

st.divider()

# ---------------------------------------------------------------------------
# Section 3: outputs & maintenance
# ---------------------------------------------------------------------------

st.subheader("3 · Outputs and maintenance")
m1, m2, m3, m4 = st.columns(4)

if m1.button("Push current output checkpoint", use_container_width=True):
    if not cfg.github_token_present:
        st.error("GitHub token missing — cannot push.")
    else:
        prog_now = progress_state()
        n_done = len(engine.completed_ids(prog_now))
        msg = (f"validation complete: processed {TOTAL}/{TOTAL} variants"
               if n_done >= TOTAL else
               f"validation checkpoint: processed {n_done}/{TOTAL} variants")
        log_box = st.empty()
        lines: list[str] = []

        def push_log(s: str) -> None:
            lines.append(str(s))
            log_box.code("\n".join(lines), language="text")

        result = github_checkpoint.checkpoint(
            msg, paths.checkpoint_paths(), cfg, REPO_ROOT,
            push_failures_file=paths.push_failures, log=push_log)
        if result.get("pushed"):
            st.success(f"Pushed via {result.get('method')} "
                       f"({result.get('files_pushed', '?')} file(s)).")
        elif result.get("skipped") == "no_changes":
            st.info("Nothing to push — remote already has the current output.")
        else:
            st.error(f"Push failed (logged to `output/push_failures.jsonl`): "
                     f"{result.get('push_failure', result)}")

if m2.button("Rebuild final canonical file", use_container_width=True):
    prog_now = progress_state()
    doc = engine.rebuild_final_clean_files(
        paths, prog_now, rules,
        bool(prog_now.get("grounding_enabled")), cfg=cfg, runtime="streamlit")
    st.success(f"Rebuilt `output/{engine.FINAL_CLEAN_FILENAME}` and the "
               f"compatibility copy: {doc['total_clean_variants']} clean variants "
               f"(accepted={doc['accepted_count']}, "
               f"auto_resolved={doc['auto_resolved_count']}; rejected and failed "
               f"records are excluded).")

if m3.button("Show run summary", use_container_width=True):
    summary = read_json(paths.run_summary)
    if summary:
        st.json(summary)
    else:
        st.info("No run summary yet — nothing has been processed.")

if m4.button("Show recent rejected / failures", use_container_width=True):
    st.write("**Recent rejected_from_clean entries (audit only — these records "
             "were excluded from the clean output after all automatic attempts):**")
    rj = tail_jsonl(paths.rejected, 10)
    if rj:
        st.json([{k: r.get(k) for k in
                  ("validation_id", "attempt_count", "confidence",
                   "unresolved_reasons")}
                 for r in rj])
    else:
        st.info("rejected_from_clean.jsonl is empty.")
    st.write("**Recent failures:**")
    fl = tail_jsonl(paths.failures, 10)
    st.json(fl) if fl else st.info("failures.jsonl is empty.")
    st.write("**Recent push failures:**")
    pf = tail_jsonl(paths.push_failures, 5)
    st.json(pf) if pf else st.info("push_failures.jsonl is empty.")
