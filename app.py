"""Streamlit validation runner for the Gemini 3.1 sampled vehicle variant engine.

Gemini-only. No OpenAI. No GPT adjudicator. No dual-model flow.

Secrets (exact paths):
    st.secrets["github"]["token"]
    st.secrets["google"]["api_key"]
    st.secrets["google"]["gemini_validator_model_id"]   (default gemini-3.1-pro-preview)
    st.secrets["google"]["grounding_enabled"]            (default true)

Secret values are never printed — only presence/missing status is shown.
"""

from __future__ import annotations

import os

import streamlit as st

from scripts.data_loader import (
    INSTRUCTIONS_PATH,
    VARIANTS_PATH,
    files_present,
    validate_and_join,
)
from scripts.output_writer import (
    CHECKPOINT_PATH,
    MODEL_DEFAULT,
    OUTPUT_PATH,
    OutputStore,
)
from scripts.validator_engine import GitHubSaver, RunConfig, run_validation

st.set_page_config(page_title="Gemini 3.1 Variant Validation Runner", layout="wide")


# ---------------------------------------------------------------------------
# Secret helpers (never expose values)
# ---------------------------------------------------------------------------


def _secret(section: str, key: str, default=None):
    try:
        return st.secrets[section][key]
    except Exception:  # noqa: BLE001 - missing secrets are expected locally
        return default


def get_github_token() -> str:
    return _secret("github", "token", "") or ""


def get_gemini_api_key() -> str:
    return _secret("google", "api_key", "") or ""


def get_model_id() -> str:
    return _secret("google", "gemini_validator_model_id", MODEL_DEFAULT) or MODEL_DEFAULT


def get_grounding_enabled() -> bool:
    val = _secret("google", "grounding_enabled", True)
    if isinstance(val, str):
        return val.strip().lower() not in {"false", "0", "no"}
    return bool(val)


def presence(value) -> str:
    return "✅ present" if value else "❌ missing"


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "logs" not in st.session_state:
    st.session_state.logs = []
if "progress" not in st.session_state:
    st.session_state.progress = {}


def log_line(msg: str) -> None:
    st.session_state.logs.append(msg)
    st.session_state.logs = st.session_state.logs[-400:]


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("🚗 Gemini 3.1 Israeli-Market Variant Validation Runner")
st.caption(
    "Identity is strict. Trim enrichment is flexible. Weak/missing trim → "
    "**clean_partial**, never reject."
)

token = get_github_token()
api_key = get_gemini_api_key()
model_id = get_model_id()
grounding = get_grounding_enabled()

# ---------------------------------------------------------------------------
# Status section
# ---------------------------------------------------------------------------

st.header("1 · Status")
fp = files_present()
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.subheader("Source files")
    st.write(f"variants: {presence(fp.get(VARIANTS_PATH))}")
    st.write(f"instructions: {presence(fp.get(INSTRUCTIONS_PATH))}")
with col_b:
    st.subheader("Secrets")
    st.write(f"Gemini API key: {presence(api_key)}")
    st.write(f"GitHub token: {presence(token)}")
    st.write(f"model id: `{model_id}`")
    st.write(f"grounding enabled: `{grounding}`")
with col_c:
    st.subheader("Output files")
    st.write(f"output: {'✅ exists' if os.path.exists(OUTPUT_PATH) else '— not yet'}")
    st.write(f"checkpoint: {'✅ exists' if os.path.exists(CHECKPOINT_PATH) else '— not yet'}")

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
# Controls section
# ---------------------------------------------------------------------------

st.header("2 · Controls")
c1, c2, c3 = st.columns(3)
with c1:
    mode = st.radio("Run mode", ["mock", "real"], horizontal=True)
    limit_enabled = st.checkbox("Limit number of variants", value=True)
    limit = st.number_input("Limit", min_value=1, value=20, step=1) if limit_enabled else None
with c2:
    force_reprocess = st.checkbox("Force reprocess (ignore checkpoint)", value=False)
    start_after = st.text_input("Start after validation_id (optional)", value="")
    checkpoint_every = st.number_input("Checkpoint every N variants", min_value=1, value=1)
with c3:
    stop_on_github_failure = st.checkbox("Stop on GitHub save failure", value=True)
    push_to_github = st.checkbox("Auto-save to GitHub after each variant", value=bool(token))
    stop_on_error = st.checkbox("Stop on first row error", value=False)

run_col, smoke_col, reset_col = st.columns(3)
run_clicked = run_col.button("▶️ Run validation", type="primary")
smoke_clicked = smoke_col.button("🧪 Run smoke checks")
reset_clicked = reset_col.button("🗑️ Reset local output/checkpoint")

if reset_clicked:
    removed = []
    for p in (OUTPUT_PATH, CHECKPOINT_PATH):
        if os.path.exists(p):
            os.remove(p)
            removed.append(os.path.basename(p))
    st.warning(
        "Local output/checkpoint reset. This does NOT touch the two source "
        "JSON files. Removed: " + (", ".join(removed) or "nothing")
    )

if smoke_clicked:
    import io
    import contextlib

    from scripts import smoke_test

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = smoke_test.main()
    st.code(buf.getvalue() or "(no output)")
    st.success("Smoke checks passed.") if code == 0 else st.error("Smoke checks failed.")

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if run_clicked:
    join = validate_and_join()
    if not join.ok:
        st.error("Cannot run: join validation failed.\n" + "\n".join(join.errors[:10]))
    elif mode == "real" and not api_key:
        st.error("Real mode needs a Gemini API key in st.secrets['google']['api_key'].")
    else:
        st.session_state.logs = []

        gemini_client = None
        if mode == "real":
            from scripts.gemini_client import GeminiClient, GeminiSettings

            gemini_client = GeminiClient(
                GeminiSettings(
                    api_key=api_key,
                    model_id=model_id,
                    grounding_enabled=grounding,
                )
            )

        github_saver = None
        if push_to_github:
            if not token:
                st.error("GitHub auto-save requested but token is missing.")
            else:
                from scripts.github_checkpoint import (
                    GitHubCheckpoint,
                    resolve_config_from_streamlit,
                )

                config, notes = resolve_config_from_streamlit(st.secrets)
                if config is None or not config.configured:
                    st.error(
                        "GitHub config incomplete: " + ", ".join(notes) +
                        ". Add [github].repo and [github].branch to secrets if "
                        "detection failed."
                    )
                else:
                    try:
                        checkpoint = GitHubCheckpoint(config)
                        github_saver = GitHubSaver(checkpoint, [OUTPUT_PATH, CHECKPOINT_PATH])
                        st.info(f"GitHub auto-save: {config.repo}@{config.branch}")
                    except Exception as exc:  # noqa: BLE001
                        st.error(f"GitHub auto-save disabled: {exc}")

        store = OutputStore(
            output_path=OUTPUT_PATH,
            checkpoint_path=CHECKPOINT_PATH,
            model=model_id,
            total_input_variants=join.variant_count,
            total_instruction_records=join.instruction_count,
        )
        store.load_existing()

        config = RunConfig(
            mode=mode,
            limit=int(limit) if limit else None,
            force_reprocess=force_reprocess,
            start_after_validation_id=start_after.strip() or None,
            checkpoint_every=int(checkpoint_every),
            stop_on_github_failure=stop_on_github_failure,
            stop_on_error=stop_on_error,
        )

        progress_box = st.empty()

        def _on_progress(info):
            st.session_state.progress = info

        with st.spinner(f"Running {mode} validation..."):
            result = run_validation(
                join,
                config,
                store=store,
                gemini_client=gemini_client,
                github_saver=github_saver,
                model_id=model_id,
                log=log_line,
                on_progress=_on_progress,
            )
        st.session_state.run_result = {
            "processed": result.processed,
            "stopped_reason": result.stopped_reason,
            "gemini_called": result.gemini_called,
            "github_attempted": result.github_attempted,
        }
        st.success(
            f"Done — processed {result.processed}, stopped: {result.stopped_reason}"
        )

# ---------------------------------------------------------------------------
# Progress section
# ---------------------------------------------------------------------------

st.header("3 · Progress")
store_view = OutputStore(output_path=OUTPUT_PATH, checkpoint_path=CHECKPOINT_PATH)
store_view.load_existing()
meta = store_view.metadata
total_input = meta.get("total_input_variants") or (join_summary or {}).get("variant_count") or 0
completed = len(store_view.validated_by_id)

p1, p2, p3, p4 = st.columns(4)
p1.metric("Completed", completed)
p2.metric("Remaining", max(0, (total_input or 0) - completed) if total_input else "—")
p3.metric("Gemini calls", meta.get("gemini_call_count", 0))
p4.metric("GitHub checkpoints", meta.get("github_checkpoint_count", 0))

dc = meta.get("decision_counts", {})
d1, d2, d3, d4 = st.columns(4)
d1.metric("clean_exact", dc.get("clean_exact", 0))
d2.metric("clean_partial", dc.get("clean_partial", 0))
d3.metric("split_required", dc.get("split_required", 0))
d4.metric("reject", dc.get("reject", 0))

prog = st.session_state.get("progress", {})
st.write(
    f"**Last validated id:** {meta.get('last_validated_id')} · "
    f"**Current cluster:** {prog.get('cluster_id', '—')} · "
    f"**Latest decision:** {prog.get('decision', '—')}"
)
if prog.get("decision_reason"):
    st.caption("Latest reason: " + prog["decision_reason"])

# ---------------------------------------------------------------------------
# Logs section
# ---------------------------------------------------------------------------

st.header("4 · Logs")
st.code("\n".join(st.session_state.logs[-60:]) or "(no logs yet)")

# ---------------------------------------------------------------------------
# Output section
# ---------------------------------------------------------------------------

st.header("5 · Output")
latest = store_view.latest_row()
if latest:
    st.subheader("Latest validated variant")
    st.json(latest)

oc1, oc2 = st.columns(2)
if os.path.exists(OUTPUT_PATH):
    with open(OUTPUT_PATH, "rb") as fh:
        oc1.download_button(
            "⬇️ Download output JSON",
            fh.read(),
            file_name=os.path.basename(OUTPUT_PATH),
            mime="application/json",
        )
if os.path.exists(CHECKPOINT_PATH):
    with open(CHECKPOINT_PATH, "rb") as fh:
        oc2.download_button(
            "⬇️ Download checkpoint JSON",
            fh.read(),
            file_name=os.path.basename(CHECKPOINT_PATH),
            mime="application/json",
        )
