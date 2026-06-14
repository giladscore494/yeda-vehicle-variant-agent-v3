"""Streamlit validation runner for the Gemini 3.1 sampled vehicle variant engine.

Gemini 3.1 is the main grounded field-level validator. GPT-5.4 is the Stage 3
grounded Repair Adjudicator that returns a full repaired JSON row; the legacy
OpenAIGuardVerifier remains only as an opt-in backward-compatibility path and is
never presented as the repair adjudicator.

Mock and real runs are completely isolated: separate output files, separate
checkpoints, separate summaries, separate UI sections. A mock run can never
append to the real dataset and a real run can never reuse mock data.

Secrets (exact paths):
    st.secrets["github"]["token"]
    st.secrets["google"]["api_key"]
    st.secrets["google"]["gemini_validator_model_id"]   (default gemini-3.1-pro-preview)
    st.secrets["google"]["grounding_enabled"]            (default true)
    st.secrets["openai"]["api_key"]                       (repair adjudicator + legacy guard verifier)
    st.secrets["openai"]["validator_model_id"]            (default gpt-5.4)
    st.secrets["google"]["force_per_variant_validation"]  (default true)

Secret values are never printed — only presence/missing status is shown.
"""

from __future__ import annotations

import os

import streamlit as st

from scripts.config import load_shared_config
from scripts.contamination import ContaminationError
from scripts.data_loader import (
    INSTRUCTIONS_PATH,
    VARIANTS_PATH,
    files_present,
    validate_and_join,
)
from scripts.output_writer import (
    MODEL_DEFAULT,
    OutputStore,
    reset_mock_outputs,
    reset_real_outputs,
)
from scripts.run_paths import ensure_mode_dirs, resolve_run_paths
from scripts.streamlit_wiring import build_run_config_and_adjudicators
from scripts.validator_engine import GitHubSaver, RunConfig, run_validation

st.set_page_config(page_title="Gemini 3.1 Variant Validation Runner", layout="wide")


# ---------------------------------------------------------------------------
# Secret helpers (never expose values)
# ---------------------------------------------------------------------------

_SHARED_CONFIG = load_shared_config()

def get_github_token() -> str:
    return _SHARED_CONFIG.github_token

def get_gemini_api_key() -> str:
    return _SHARED_CONFIG.google_api_key

def get_model_id() -> str:
    return _SHARED_CONFIG.gemini_validator_model_id or MODEL_DEFAULT

def get_grounding_enabled() -> bool:
    return _SHARED_CONFIG.grounding_enabled

def get_openai_api_key() -> str:
    return _SHARED_CONFIG.openai_api_key

def get_guard_verifier_model_id() -> str:
    return _SHARED_CONFIG.openai_validator_model_id or "gpt-5.4"

def get_repair_adjudicator_model_id() -> str:
    return _SHARED_CONFIG.openai_validator_model_id or "gpt-5.4"

def get_repair_adjudicator_enabled_default() -> bool:
    # The grounded repair adjudicator is the real Stage 3. It is enabled by
    # default whenever an OpenAI key is present so the pipeline is honest.
    return bool(_SHARED_CONFIG.openai_api_key)

def get_guard_verifier_enabled_default() -> bool:
    # Legacy guard verifier is OFF by default; it must never masquerade as
    # the repair adjudicator.
    return False

def get_force_per_variant_default() -> bool:
    return _SHARED_CONFIG.force_per_variant_validation


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
openai_api_key = get_openai_api_key()
guard_verifier_model_default = get_guard_verifier_model_id()
guard_verifier_enabled_default = get_guard_verifier_enabled_default()
repair_adjudicator_model_default = get_repair_adjudicator_model_id()
repair_adjudicator_enabled_default = get_repair_adjudicator_enabled_default()
force_per_variant_default = get_force_per_variant_default()

MOCK_PATHS = resolve_run_paths("mock")
REAL_PATHS = resolve_run_paths("real", model=model_id)

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
    st.subheader("Secrets")
    st.write(f"Gemini API key: {presence(api_key)}")
    st.write(f"GitHub token: {presence(token)}")
    st.write(f"model id: `{model_id}`")
    st.write(f"grounding enabled: `{grounding}`")
    st.write(f"OpenAI API key: {presence(openai_api_key)}")
    st.write(f"GPT-5.4 repair adjudicator model: `{repair_adjudicator_model_default}`")
    st.write(f"legacy guard verifier model: `{guard_verifier_model_default}`")
    st.write(f"force per-variant default: `{force_per_variant_default}`")
with col_c:
    st.subheader("Output files")
    st.write(
        f"mock output: {'✅ exists' if os.path.exists(MOCK_PATHS.output_path) else '— not yet'}"
    )
    st.write(
        f"real output: {'✅ exists' if os.path.exists(REAL_PATHS.output_path) else '— not yet'}"
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
# Shared run helper
# ---------------------------------------------------------------------------


def _show_paths(run_paths) -> None:
    st.code(
        f"output     = {os.path.relpath(run_paths.output_path)}\n"
        f"checkpoint = {os.path.relpath(run_paths.checkpoint_path)}\n"
        f"summary    = {os.path.relpath(run_paths.summary_path)}\n"
        f"engine     = {run_paths.engine}\n"
        f"model      = {run_paths.model}\n"
        f"gemini     = {'enabled' if run_paths.allow_gemini_calls else 'disabled'}",
    )


def execute_run(
    run_paths,
    *,
    limit,
    force_reprocess: bool,
    start_after: str,
    checkpoint_every: int,
    push_to_github: bool,
    stop_on_github_failure: bool,
    stop_on_error: bool,
    repair_adjudicator_enabled: bool = True,
    repair_adjudicator_model_id: str = "gpt-5.4",
    repair_adjudicator_mode: str = "all_clean_candidates",
    require_gpt54_grounding_for_repair: bool = True,
    final_seal_enabled: bool = True,
    strict_clean_catalog: bool = True,
    legacy_guard_verifier_enabled: bool = False,
    legacy_guard_verifier_model_id: str = "gpt-5.4",
    force_per_variant_validation: bool = True,
) -> None:
    mode = run_paths.mode
    join = validate_and_join()
    if not join.ok:
        st.error("Cannot run: join validation failed.\n" + "\n".join(join.errors[:10]))
        return
    if mode == "real" and not api_key:
        st.error("Real mode needs a Gemini API key in st.secrets['google']['api_key'].")
        return

    ensure_mode_dirs(run_paths)
    st.session_state.logs = []

    gemini_client = None
    if mode == "real" and run_paths.allow_gemini_calls:
        from scripts.gemini_client import GeminiClient, GeminiSettings

        gemini_client = GeminiClient(
            GeminiSettings(
                api_key=api_key,
                model_id=run_paths.model,
                grounding_enabled=grounding,
            )
        )

    run_config, guard_verifier, repair_adjudicator, build_error = build_run_config_and_adjudicators(
        mode=mode,
        limit=limit,
        force_reprocess=force_reprocess,
        start_after=start_after,
        checkpoint_every=checkpoint_every,
        stop_on_github_failure=stop_on_github_failure,
        stop_on_error=stop_on_error,
        force_per_variant_validation=force_per_variant_validation,
        repair_adjudicator_enabled=repair_adjudicator_enabled,
        repair_adjudicator_model_id=repair_adjudicator_model_id,
        repair_adjudicator_mode=repair_adjudicator_mode,
        require_gpt54_grounding_for_repair=require_gpt54_grounding_for_repair,
        require_gemini_grounding=grounding,
        final_seal_enabled=final_seal_enabled,
        strict_clean_catalog=strict_clean_catalog,
        legacy_guard_verifier_enabled=legacy_guard_verifier_enabled,
        legacy_guard_verifier_model_id=legacy_guard_verifier_model_id,
        openai_api_key=openai_api_key,
    )
    if build_error:
        st.error(build_error)
        return
    if repair_adjudicator is not None:
        st.info(f"GPT-5.4 repair adjudicator enabled: `{repair_adjudicator_model_id}` (mode={repair_adjudicator_mode}).")
    if force_reprocess is False and mode == "real":
        st.warning(
            "Existing completed rows will be skipped unless Force reprocess is enabled. "
            "Repair/final-seal changes will not apply to skipped rows."
        )

    github_saver = None
    if push_to_github and run_paths.allow_github_push:
        if not token:
            st.error("GitHub auto-save requested but token is missing.")
        else:
            from scripts.github_checkpoint import (
                GitHubCheckpoint,
                resolve_config_from_streamlit,
            )

            config_gh, notes = resolve_config_from_streamlit(st.secrets)
            if config_gh is None or not config_gh.configured:
                st.error(
                    "GitHub config incomplete: " + ", ".join(notes) +
                    ". Add [github].repo and [github].branch to secrets if "
                    "detection failed."
                )
            else:
                try:
                    checkpoint = GitHubCheckpoint(config_gh)
                    github_saver = GitHubSaver(
                        checkpoint,
                        run_paths.github_paths,
                        commit_prefix=run_paths.commit_prefix,
                    )
                    st.info(f"GitHub auto-save: {config_gh.repo}@{config_gh.branch}")
                except Exception as exc:  # noqa: BLE001
                    st.error(f"GitHub auto-save disabled: {exc}")
    elif push_to_github and not run_paths.allow_github_push:
        st.warning("GitHub push is disabled for mock mode; skipping push.")

    store = OutputStore.for_paths(
        run_paths,
        total_input_variants=join.variant_count,
        total_instruction_records=join.instruction_count,
    )
    try:
        store.load_existing()
    except ContaminationError as exc:
        st.error(
            "Output file contamination detected: "
            f"{exc} Reset the {mode} output before continuing."
        )
        return

    def _on_progress(info):
        st.session_state.progress = info

    with st.spinner(f"Running {mode} validation..."):
        result = run_validation(
            join,
            run_config,
            store=store,
            gemini_client=gemini_client,
            github_saver=github_saver,
            model_id=run_paths.model,
            log=log_line,
            on_progress=_on_progress,
            flash_adjudicator=None,
            guard_verifier=guard_verifier,
            repair_adjudicator=repair_adjudicator,
        )
    st.session_state.run_result = {
        "mode": mode,
        "processed": result.processed,
        "stopped_reason": result.stopped_reason,
        "gemini_called": result.gemini_called,
        "github_attempted": result.github_attempted,
    }
    st.success(
        f"[{mode}] Done — processed {result.processed}, stopped: {result.stopped_reason}"
    )


# ---------------------------------------------------------------------------
# Section 2 · Mock validation (testing stage — never calls Gemini)
# ---------------------------------------------------------------------------

st.header("2 · 🧪 Mock validation (testing stage)")
st.caption(
    "Writes to **mock output only**. Never calls Gemini. Use this to exercise "
    "the pipeline, schema, and checkpoint logic."
)
_show_paths(MOCK_PATHS)

mc1, mc2 = st.columns(2)
with mc1:
    mock_limit_enabled = st.checkbox("Limit variants (mock)", value=True, key="mock_limit_en")
    mock_limit = (
        st.number_input("Limit (mock)", min_value=1, value=20, step=1, key="mock_limit")
        if mock_limit_enabled
        else None
    )
    mock_force = st.checkbox("Force reprocess (mock)", value=False, key="mock_force")
with mc2:
    mock_start_after = st.text_input("Start after id (mock)", value="", key="mock_start")
    mock_checkpoint_every = st.number_input(
        "Checkpoint every N (mock)", min_value=1, value=1, key="mock_cp"
    )
    mock_push = st.checkbox(
        "Push mock files to GitHub (mock-only path)", value=False, key="mock_push"
    )

mrun_col, mreset_col = st.columns(2)
mock_run_clicked = mrun_col.button("▶️ Run mock validation", type="primary", key="mock_run")
mock_reset_clicked = mreset_col.button("🗑️ Reset mock output/checkpoint", key="mock_reset")

if mock_reset_clicked:
    st.warning(
        "⚠️ Resetting MOCK runtime files only. Source files and real output are "
        "untouched."
    )
    removed = reset_mock_outputs(log=log_line)
    st.info("Mock reset removed: " + (", ".join(removed) or "nothing"))

if mock_run_clicked:
    execute_run(
        MOCK_PATHS,
        limit=mock_limit,
        force_reprocess=mock_force,
        start_after=mock_start_after,
        checkpoint_every=mock_checkpoint_every,
        push_to_github=mock_push,
        stop_on_github_failure=False,
        stop_on_error=False,
    )

# ---------------------------------------------------------------------------
# Section 3 · Real Gemini validation (clean real-only dataset)
# ---------------------------------------------------------------------------

st.header("3 · 🛰️ Real Gemini validation")
st.caption(
    "Writes to **real output only**. Calls Gemini, requires an API key (and "
    "grounding if enabled), and can push the real checkpoint to GitHub."
)
_show_paths(REAL_PATHS)
if not api_key:
    st.warning("Gemini API key missing — real validation is disabled until it is set.")

rc1, rc2 = st.columns(2)
with rc1:
    real_limit_enabled = st.checkbox("Limit variants (real)", value=True, key="real_limit_en")
    real_limit = (
        st.number_input("Limit (real)", min_value=1, value=20, step=1, key="real_limit")
        if real_limit_enabled
        else None
    )
    real_force = st.checkbox("Force reprocess (real)", value=False, key="real_force")
    real_stop_on_error = st.checkbox("Stop on first row error", value=False, key="real_soe")
    real_repair_adjudicator_enabled = st.checkbox(
        "GPT-5.4 grounded repair adjudicator (Stage 3)",
        value=repair_adjudicator_enabled_default,
        key="real_repair_adjudicator",
        help="Real Stage 3. Instantiates OpenAIRepairAdjudicator and returns a full repaired row. Requires OpenAI API key.",
    )
    real_require_gpt54_grounding = st.checkbox(
        "Require GPT-5.4 grounding for repair",
        value=True,
        key="real_require_gpt54_grounding",
        help="If grounded support is missing, the row fails closed to review_queue and cannot reach clean_catalog.",
    )
    real_strict_clean_catalog = st.checkbox(
        "Strict clean_catalog gate",
        value=True,
        key="real_strict_clean_catalog",
    )
    real_guard_verifier_enabled = st.checkbox(
        "Legacy GPT guard verifier (backward-compat only)",
        value=guard_verifier_enabled_default,
        key="real_guard_verifier",
        help="Legacy guard-scoped verifier. NOT the repair adjudicator. Off by default.",
    )
    real_force_per_variant = st.checkbox("Force per-variant Gemini validation", value=force_per_variant_default, key="real_force_per_variant")
with rc2:
    real_start_after = st.text_input("Start after id (real)", value="", key="real_start")
    real_checkpoint_every = st.number_input(
        "Checkpoint every N (real)", min_value=1, value=1, key="real_cp"
    )
    real_push = st.checkbox(
        "Auto-save real files to GitHub", value=bool(token), key="real_push"
    )
    real_stop_on_gh = st.checkbox("Stop on GitHub save failure", value=True, key="real_sogh")
    real_final_seal_enabled = st.checkbox("Python final seal (publication authority)", value=True, key="real_final_seal")
    real_repair_adjudicator_mode = st.selectbox(
        "Repair adjudicator trigger mode",
        options=["all_clean_candidates", "all_rows", "risk_only"],
        index=0,
        key="real_repair_adjudicator_mode",
    )
    real_repair_adjudicator_model_id = st.text_input("Repair adjudicator model id", value=repair_adjudicator_model_default, key="real_repair_adjudicator_model")
    real_guard_verifier_model_id = st.text_input("Legacy guard verifier model id", value=guard_verifier_model_default, key="real_guard_verifier_model")

if real_repair_adjudicator_enabled and not openai_api_key:
    st.error(
        "GPT-5.4 repair adjudicator is enabled but the OpenAI API key is missing. "
        "The run will refuse to start until the key is set (it will not silently "
        "fall back to the legacy guard verifier)."
    )

rrun_col, rreset_col = st.columns(2)
real_run_clicked = rrun_col.button(
    "▶️ Run real validation", type="primary", key="real_run", disabled=not api_key
)
real_reset_clicked = rreset_col.button("🗑️ Reset real output/checkpoint", key="real_reset")

if real_reset_clicked:
    st.warning(
        "⚠️ Resetting REAL runtime files only. Source files and mock output are "
        "untouched."
    )
    removed = reset_real_outputs(log=log_line)
    st.info("Real reset removed: " + (", ".join(removed) or "nothing"))

if real_run_clicked:
    execute_run(
        REAL_PATHS,
        limit=real_limit,
        force_reprocess=real_force,
        start_after=real_start_after,
        checkpoint_every=real_checkpoint_every,
        push_to_github=real_push,
        stop_on_github_failure=real_stop_on_gh,
        stop_on_error=real_stop_on_error,
        repair_adjudicator_enabled=real_repair_adjudicator_enabled,
        repair_adjudicator_model_id=real_repair_adjudicator_model_id,
        repair_adjudicator_mode=real_repair_adjudicator_mode,
        require_gpt54_grounding_for_repair=real_require_gpt54_grounding,
        final_seal_enabled=real_final_seal_enabled,
        strict_clean_catalog=real_strict_clean_catalog,
        legacy_guard_verifier_enabled=real_guard_verifier_enabled,
        legacy_guard_verifier_model_id=real_guard_verifier_model_id,
        force_per_variant_validation=real_force_per_variant,
    )

# ---------------------------------------------------------------------------
# Section 4 · Smoke checks
# ---------------------------------------------------------------------------

st.header("4 · Smoke checks")
if st.button("🧪 Run smoke checks"):
    import contextlib
    import io

    from scripts import smoke_test

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = smoke_test.main()
    st.code(buf.getvalue() or "(no output)")
    st.success("Smoke checks passed.") if code == 0 else st.error("Smoke checks failed.")

# ---------------------------------------------------------------------------
# Section 5 · Progress (per mode)
# ---------------------------------------------------------------------------

st.header("5 · Progress")


def _mode_progress(label: str, run_paths) -> None:
    st.subheader(label)
    store_view = OutputStore.for_paths(run_paths)
    try:
        store_view.load_existing()
    except ContaminationError as exc:
        st.error(f"Contamination detected in {label}: {exc}")
        return
    meta = store_view.metadata
    total_input = meta.get("total_input_variants") or 0
    completed = len(store_view.validated_by_id)

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Completed", completed)
    p2.metric("Remaining", max(0, total_input - completed) if total_input else "—")
    p3.metric("Gemini calls", meta.get("gemini_call_count", 0))
    p4.metric("GitHub checkpoints", meta.get("github_checkpoint_count", 0))

    v1, v2, v3, v4, v5 = st.columns(5)
    v1.metric("Stage 1 Pro", meta.get("stage1_pro_calls", 0))
    v2.metric("Guard flags", meta.get("stage2_guard_flags_total", 0))
    v3.metric("Stage 2.5 repair triggered", meta.get("stage25_repair_triggered_rows", 0))
    v4.metric("GPT-5.4 repair calls", meta.get("stage3_repair_adjudicator_calls", 0))
    v5.metric("Final seal blocks", meta.get("stage4_final_seal_blocks", 0))

    r1, r2, r3, r4, r5 = st.columns(5)
    r1.metric("Repair successes", meta.get("stage3_repair_adjudicator_successes", 0))
    r2.metric("Repair failures", meta.get("stage3_repair_adjudicator_failures", 0))
    r3.metric("Repair patches", meta.get("stage3_repair_adjudicator_patches", 0))
    r4.metric("Routing changes", meta.get("stage3_repair_adjudicator_routing_changes", 0))
    r5.metric("Summary rewrites", meta.get("stage3_repair_adjudicator_summary_rewrites", 0))

    if meta.get("repair_setup_failed"):
        st.error(
            "Repair adjudicator was enabled but not wired (repair_setup_failed). "
            "Rows were forced to review_queue and blocked from clean_catalog."
        )
    if meta.get("stage25_repair_triggered_rows", 0) and not meta.get("stage3_repair_adjudicator_calls", 0):
        st.warning(
            "Repair was triggered for some rows but the GPT-5.4 repair adjudicator "
            "was never actually called. Those rows cannot enter clean_catalog."
        )

    st.caption(
        "Gemini grounding missing="
        f"{meta.get('stage1_gemini_grounding_missing', 0)} · "
        "GPT-5.4 grounding missing="
        f"{meta.get('stage3_repair_adjudicator_grounding_missing', 0)} · "
        "clean_catalog blocks → final_seal="
        f"{meta.get('clean_catalog_blocks_by_final_seal', 0)}, grounding="
        f"{meta.get('clean_catalog_blocks_by_grounding', 0)}, trim="
        f"{meta.get('clean_catalog_blocks_by_unresolved_trim', 0)}, critical_field="
        f"{meta.get('clean_catalog_blocks_by_unresolved_critical_field', 0)}"
    )

    dc = meta.get("decision_counts", {})
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("clean_exact", dc.get("clean_exact", 0))
    d2.metric("clean_partial", dc.get("clean_partial", 0))
    d3.metric("split_required", dc.get("split_required", 0))
    d4.metric("reject", dc.get("reject", 0))
    st.caption(
        f"run_mode=`{meta.get('run_mode')}` · is_mock_output="
        f"`{meta.get('is_mock_output')}` · last id: {meta.get('last_validated_id')}"
    )

    latest = store_view.latest_row()
    if latest:
        with st.expander(f"Latest {label} row"):
            st.write(
                f"repair_triggered: `{latest.get('_repair_adjudicator_triggered')}` · "
                f"final_route: `{latest.get('final_route')}` · "
                f"publishable: `{latest.get('publishable_to_clean_catalog')}` · "
                f"_flags_count: `{latest.get('_flags_count')}`"
            )
            st.json({
                "preflight_risk_tags": latest.get("preflight_risk_tags"),
                "guard_flags": latest.get("guard_flags"),
                "risk_score": latest.get("risk_score"),
                "repair_triggered": latest.get("_repair_adjudicator_triggered"),
                "repair_decision": latest.get("_repair_decision"),
                "field_patches": latest.get("field_patches"),
                "grounding_status": latest.get("grounding_status"),
                "final_seal_result": latest.get("final_seal_result"),
                "final_route": latest.get("final_route"),
                "route_reason": latest.get("route_reason"),
            })
            if latest.get("adjudication_log"):
                st.json(latest.get("adjudication_log"))
            st.json(latest)
    if os.path.exists(run_paths.output_path):
        with open(run_paths.output_path, "rb") as fh:
            st.download_button(
                f"⬇️ Download {label} output JSON",
                fh.read(),
                file_name=os.path.basename(run_paths.output_path),
                mime="application/json",
                key=f"dl_{run_paths.mode}",
            )


_mode_progress("🧪 Mock", MOCK_PATHS)
_mode_progress("🛰️ Real", REAL_PATHS)

# ---------------------------------------------------------------------------
# Section 6 · Logs
# ---------------------------------------------------------------------------

st.header("6 · Logs")
st.code("\n".join(st.session_state.logs[-60:]) or "(no logs yet)")
