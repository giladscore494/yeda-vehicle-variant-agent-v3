"""Streamlit runner for the GPT-5.4 Israeli vehicle variant/catalog pipeline.

One production path only. For each make/model cluster GPT-5.4 answers a single
grounded question — what technical versions were actually sold in Israel? — and
Python validates the returned profile. GPT-5.4 is the only model.

Secrets (env vars win; same key name from Streamlit secrets next):
    OPENAI_API_KEY            required for any run
    OPENAI_VALIDATOR_MODEL_ID optional, default gpt-5.4
    GITHUB_TOKEN              optional, only for GitHub checkpoint pushes

Secret values are never printed — only presence/missing status is shown.
"""

from __future__ import annotations

import os

import streamlit as st

from scripts.catalog_builder import (
    CATALOG_OUTPUT_PATH,
    READINESS_OUTPUT_PATH,
    REVIEW_OUTPUT_PATH,
    build_catalog,
    compute_resume_state,
    load_existing_outputs,
)
from scripts.catalog_quality_scan import QUALITY_SCAN_OUTPUT_PATH, scan_quality
from scripts.catalog_repair import repair_review_models
from scripts.catalog_checkpoint import CatalogCheckpointConfig
from scripts.config import load_shared_config
from scripts.data_loader import (
    INSTRUCTIONS_PATH,
    VARIANTS_PATH,
    files_present,
    validate_and_join,
)
from scripts.openai_catalog_client import CatalogClientSettings

st.set_page_config(
    page_title="GPT-5.4 Israeli Vehicle Variant Catalog Runner", layout="wide"
)

_CONFIG = load_shared_config()


def presence(value) -> str:
    return "✅ present" if value else "❌ missing"


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "logs" not in st.session_state:
    st.session_state.logs = []


def log_line(msg: str) -> None:
    st.session_state.logs.append(msg)
    st.session_state.logs = st.session_state.logs[-400:]


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("🚗 GPT-5.4 Israeli Vehicle Variant Catalog Runner")
st.caption(
    "One grounded GPT-5.4 request per make/model cluster collects the technical "
    "versions actually sold in Israel. Python validates each profile and routes "
    "it to the website-ready catalog or to review."
)

openai_api_key = _CONFIG.openai_api_key
github_token = _CONFIG.github_token
model_id = _CONFIG.openai_validator_model_id

# Persistent progress header rendered from disk on every rerun.
def render_progress_header():
    try:
        state = compute_resume_state()
    except Exception as exc:  # noqa: BLE001
        st.warning(f"Progress header unavailable: {exc}")
        return None
    total = state["total_universe"] or 1
    st.progress(min(state["done"] / total, 1.0))
    next_label = (
        f"{state['next_make']} {state['next_model']}"
        if state.get("next_make") or state.get("next_model")
        else "START"
    )
    st.info(
        f"Processed {state['done']}/{state['total_universe']} | "
        f"ready {state['ready']} | blocked {state['blocked']} | "
        f"remaining {state['remaining']} | next: {next_label}"
    )
    if os.path.exists(QUALITY_SCAN_OUTPUT_PATH):
        try:
            import json
            with open(QUALITY_SCAN_OUTPUT_PATH, "r", encoding="utf-8") as fh:
                q = json.load(fh)
            t = q.get("totals", {})
            st.caption(
                f"Quality: {t.get('bug', 0)} bugs | {t.get('leak', 0)} source-leaks | "
                f"{t.get('normalization', 0)} normalization | {t.get('structure', 0)} structure"
            )
        except Exception:
            pass
    return state

resume_state = render_progress_header()

# ---------------------------------------------------------------------------
# Status section
# ---------------------------------------------------------------------------

st.header("1 · Status")
fp = files_present()
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.subheader("Source files (read-only)")
    st.write(f"variants: {presence(fp.get(VARIANTS_PATH))}")
    st.write(f"instructions: {presence(fp.get(INSTRUCTIONS_PATH))}")
with col_b:
    st.subheader("Secrets & model")
    st.write(f"OPENAI_API_KEY: {presence(openai_api_key)}")
    st.write(f"GITHUB_TOKEN: {presence(github_token)}")
    st.write(f"OpenAI model id: `{model_id}`")
with col_c:
    st.subheader("Output files")
    st.write(
        f"catalog: {'✅ exists' if os.path.exists(CATALOG_OUTPUT_PATH) else '— not yet'}"
    )
    st.write(
        f"readiness: {'✅ exists' if os.path.exists(READINESS_OUTPUT_PATH) else '— not yet'}"
    )
    st.write(
        f"review: {'✅ exists' if os.path.exists(REVIEW_OUTPUT_PATH) else '— not yet'}"
    )

if st.button("🔎 Validate source files & join"):
    join = validate_and_join()
    st.session_state.join_summary = join.summary()

join_summary = st.session_state.get("join_summary")
if join_summary:
    if join_summary["ok"]:
        st.success(
            f"Join OK — {join_summary['variant_count']} variants, "
            f"{join_summary['instruction_count']} instructions, "
            f"{join_summary['joined_ids']} joined ids."
        )
    else:
        st.error("Join FAILED:\n" + "\n".join(join_summary["errors"][:10]))
    for w in join_summary["warnings"]:
        st.warning(w)

# ---------------------------------------------------------------------------
# Run / repair / scan section
# ---------------------------------------------------------------------------

st.header("2 · Build, repair, and scan")
st.caption("Runs are manual only. Refresh never starts a model call; the header is recomputed from disk.")

col_run, col_repair, col_scan = st.columns(3)
with col_run:
    batch_size = st.number_input("models this batch", min_value=1, value=25, step=1, key="batch_size")
    run_clicked = st.button("▶️ Run next batch", type="primary", key="run_next_batch")
with col_repair:
    repair_batch = st.number_input("blocked models to repair", min_value=1, value=5, step=1, key="repair_batch")
    repair_clicked = st.button("🛠️ Repair blocked models", key="repair_blocked")
with col_scan:
    scan_clicked = st.button("🔬 Run quality scan", key="quality_scan")

with st.expander("Reset progress"):
    confirm = st.text_input("Type RESET to clear catalog, review, readiness, and checkpoint state", key="reset_confirm")
    if st.button("Reset progress", key="reset_progress"):
        if confirm == "RESET":
            for path in (CATALOG_OUTPUT_PATH, READINESS_OUTPUT_PATH, REVIEW_OUTPUT_PATH, QUALITY_SCAN_OUTPUT_PATH):
                if os.path.exists(path):
                    os.remove(path)
            st.session_state.logs = []
            st.success("Progress reset.")
            st.rerun()
        else:
            st.error("Type RESET exactly before clearing progress.")

progress_box = st.empty()
log_box = st.empty()

def _require_api():
    if not openai_api_key:
        st.error("OPENAI_API_KEY is missing. Set it before running.")
        st.stop()

def _settings():
    return CatalogClientSettings(api_key=openai_api_key, model_id=model_id, use_web_search=True)

def _checkpoint():
    return CatalogCheckpointConfig(
        enabled=bool(_CONFIG.github_checkpoint_enabled),
        push_every_profiles=int(_CONFIG.push_every_profiles),
        strict=bool(_CONFIG.strict_github_checkpoint),
        token=github_token,
    )

def _on_log(msg: str) -> None:
    log_line(msg)
    log_box.code("\n".join(st.session_state.logs[-40:]) or "(no logs yet)")

def _on_progress(info: dict) -> None:
    if info.get("phase") == "running":
        progress_box.info(f"[{info['index']}/{info['total']}] RUNNING — {info['make']} {info['model']} · processed={info['processed']} ready={info['ready']} blocked={info['review']}")
    elif info.get("phase") == "done":
        progress_box.success(f"[{info['index']}/{info['total']}] DONE — {info['make']} {info['model']} · ready={str(info.get('ready_profile')).lower()} · issues={info.get('issues')}")
    elif info.get("phase") == "error":
        progress_box.warning(f"[{info['index']}/{info['total']}] ERROR — {info['make']} {info['model']} routed to review")

if run_clicked:
    _require_api()
    if _CONFIG.github_checkpoint_enabled and not github_token:
        st.error("GitHub checkpointing is enabled but GITHUB_TOKEN is missing.")
        st.stop()
    st.session_state.logs = []
    state = compute_resume_state()
    try:
        with st.spinner("Running next grounded GPT-5.4 batch..."):
            result = build_catalog(limit_models=int(batch_size), start_after_key=state.get("next_key"), settings=_settings(), checkpoint=_checkpoint(), log=_on_log, on_progress=_on_progress)
        st.success(f"Batch complete — ready {result.readiness['models_ready_for_website']} | blocked {result.readiness['models_blocked']} | total {result.readiness['total_models']}.")
    except ValueError as exc:
        st.error(str(exc))
        st.stop()
    render_progress_header()

if repair_clicked:
    _require_api()
    st.session_state.logs = []
    with st.spinner("Repairing blocked models..."):
        result = repair_review_models(batch=int(repair_batch), settings=_settings(), log=_on_log)
    st.success(f"Repair complete — processed {result['processed']}, promoted {result['promoted']}, kept {result['kept']}, skipped {result['skipped']}.")
    render_progress_header()

if scan_clicked:
    catalog, _readiness, review = load_existing_outputs()
    report = scan_quality(catalog, review)
    t = report["totals"]
    st.success(f"Quality: {t.get('bug', 0)} bugs | {t.get('leak', 0)} source-leaks | {t.get('normalization', 0)} normalization | {t.get('structure', 0)} structure")
    for typ, count in sorted(report.get("counts_by_type", {}).items()):
        with st.expander(f"{typ} ({count})"):
            st.json([f for f in report["findings"] if f["type"] == typ])

# ---------------------------------------------------------------------------
# Logs
# ---------------------------------------------------------------------------

st.header("3 · Logs")
st.code("\n".join(st.session_state.logs[-60:]) or "(no logs yet)")
