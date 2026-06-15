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
)
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
# Run section
# ---------------------------------------------------------------------------

st.header("2 · Build model technical catalog")
st.caption(
    "Required secret: **OPENAI_API_KEY** (grounded GPT-5.4 with web_search). "
    "**GITHUB_TOKEN** is only needed when GitHub checkpointing is enabled. "
    "Secrets are never printed, logged, or written to output."
)

cc1, cc2 = st.columns(2)
with cc1:
    cat_make = st.text_input("Make filter (optional)", value="", key="cat_make")
    cat_model = st.text_input("Model filter (optional)", value="", key="cat_model")
with cc2:
    cat_limit = st.number_input(
        "Run count / limit (0 = all selected clusters)",
        min_value=0,
        value=1,
        step=1,
        key="cat_limit",
    )
    cat_start_after = st.text_input(
        "Start after cluster key (optional, format 'market|make|model')",
        value="",
        key="cat_start_after",
    )

cp1, cp2, cp3 = st.columns(3)
with cp1:
    cat_checkpoint = st.checkbox(
        "Push GitHub checkpoint after each profile",
        value=_CONFIG.github_checkpoint_enabled,
        key="cat_checkpoint",
        help="Needs GITHUB_TOKEN. Pushes the three output files after each "
        "completed make/model profile.",
    )
with cp2:
    cat_push_every = st.number_input(
        "Push every N completed profiles",
        min_value=1,
        value=int(_CONFIG.push_every_profiles),
        step=1,
        key="cat_push_every",
    )
with cp3:
    cat_strict_gh = st.checkbox(
        "Stop on GitHub checkpoint failure",
        value=_CONFIG.strict_github_checkpoint,
        key="cat_strict_gh",
    )

run_clicked = st.button(
    "▶️ Build model technical catalog", type="primary", key="cat_run"
)

# Live progress placeholders (updated from the build callbacks).
st.subheader("Live run progress")
progress_box = st.empty()
log_box = st.empty()

if run_clicked:
    if not openai_api_key:
        st.error(
            "OPENAI_API_KEY is missing. Set it in environment variables or "
            "secrets before running. The pipeline never runs without it."
        )
        st.stop()
    if cat_checkpoint and not github_token:
        st.error(
            "GitHub checkpointing is enabled but GITHUB_TOKEN is missing. Add "
            "the token or disable checkpointing."
        )
        st.stop()

    st.session_state.logs = []

    settings = CatalogClientSettings(
        api_key=openai_api_key,
        model_id=model_id,
        use_web_search=True,  # runs always use web_search grounding
    )
    checkpoint = CatalogCheckpointConfig(
        enabled=bool(cat_checkpoint),
        push_every_profiles=int(cat_push_every),
        strict=bool(cat_strict_gh),
        token=github_token,
    )

    def _on_log(msg: str) -> None:
        log_line(msg)
        log_box.code("\n".join(st.session_state.logs[-40:]) or "(no logs yet)")

    def _on_progress(info: dict) -> None:
        if info.get("phase") == "running":
            progress_box.info(
                f"[{info['index']}/{info['total']}] RUNNING GPT-5.4 — "
                f"{info['market_scope']} :: {info['make']} :: {info['model']} · "
                f"raw_variants={info['raw_variants']} · "
                f"sample_ids={', '.join(info.get('validation_ids') or []) or '(none)'} · "
                f"processed={info['processed']} ready={info['ready']} review={info['review']}"
            )
        elif info.get("phase") == "done":
            progress_box.success(
                f"[{info['index']}/{info['total']}] DONE — {info['make']} "
                f"{info['model']} · technical_variants={info.get('technical_variants')} · "
                f"ready={str(info.get('ready_profile')).lower()} · "
                f"issues={info.get('issues')} · processed={info['processed']} "
                f"ready={info['ready']} review={info['review']}"
            )
        elif info.get("phase") == "error":
            progress_box.warning(
                f"[{info['index']}/{info['total']}] ERROR — {info['make']} "
                f"{info['model']} routed to review."
            )

    try:
        with st.spinner("Building catalog (one grounded GPT-5.4 call per make/model)..."):
            result = build_catalog(
                make=cat_make or None,
                model=cat_model or None,
                limit_models=int(cat_limit) if cat_limit else None,
                start_after_key=cat_start_after or None,
                settings=settings,
                checkpoint=checkpoint,
                log=_on_log,
                on_progress=_on_progress,
            )
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    st.success(
        f"Built — {result.readiness['total_models']} model(s), "
        f"{result.readiness['total_technical_variants']} technical variants, "
        f"{result.readiness['models_ready_for_website']} website-ready."
    )
    st.subheader("Readiness report")
    st.json(result.readiness)
    if result.catalog["models"]:
        with st.expander("Website-ready models"):
            st.json(result.catalog["models"])
    if result.review["models"]:
        with st.expander("Review / blocked models"):
            st.json(result.review["models"])
    st.code(
        f"catalog   = {os.path.relpath(result.catalog_path)}\n"
        f"readiness = {os.path.relpath(result.readiness_path)}\n"
        f"review    = {os.path.relpath(result.review_path)}"
    )

# ---------------------------------------------------------------------------
# Logs
# ---------------------------------------------------------------------------

st.header("3 · Logs")
st.code("\n".join(st.session_state.logs[-60:]) or "(no logs yet)")
