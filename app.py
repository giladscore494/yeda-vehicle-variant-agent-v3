"""Streamlit runner for selectable OpenAI/Gemini vehicle catalog validation."""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import streamlit as st

from scripts.catalog_builder import CATALOG_OUTPUT_PATH, READINESS_OUTPUT_PATH, REVIEW_OUTPUT_PATH, build_catalog, compute_resume_state, load_existing_outputs
from scripts.catalog_checkpoint import CatalogCheckpointConfig
from scripts.catalog_provider import CatalogProviderSettings
from scripts.catalog_quality_scan import QUALITY_SCAN_OUTPUT_PATH, scan_quality
from scripts.catalog_repair import repair_review_models
from scripts.config import DEFAULT_GEMINI_VALIDATOR_MODEL_ID, DEFAULT_OPENAI_VALIDATOR_MODEL_ID, SharedConfig, load_shared_config
from scripts.data_loader import INSTRUCTIONS_PATH, VARIANTS_PATH, files_present, validate_and_join
from scripts.github_checkpoint import OUTPUT_JSON_PATHS, github_autosave_enabled, manual_push_outputs
from scripts.security import sanitize_error

MODEL_OPTIONS = ["GPT-5.4", "Gemini 3.1"]



def provider_settings_for_label(label: str, config: SharedConfig) -> CatalogProviderSettings:
    if label == "Gemini 3.1":
        return CatalogProviderSettings(
            provider="google",
            display_name="Gemini 3.1",
            model_id=config.gemini_validator_model_id or DEFAULT_GEMINI_VALIDATOR_MODEL_ID,
            api_key=config.google_api_key,
            grounding_enabled=config.gemini_grounding_enabled,
        )
    return CatalogProviderSettings(
        provider="openai",
        display_name="GPT-5.4",
        model_id=config.openai_validator_model_id or DEFAULT_OPENAI_VALIDATOR_MODEL_ID,
        api_key=config.openai_api_key,
        web_search_enabled=config.openai_web_search_enabled,
    )


def can_start_provider(settings: CatalogProviderSettings) -> tuple[bool, str]:
    if settings.api_key:
        return True, ""
    if settings.provider == "openai":
        return False, "OpenAI API key is missing for the selected GPT-5.4 validation model. No fallback was used."
    return False, "Google API key is missing for the selected Gemini 3.1 validation model. No fallback was used."


def existing_output_paths(paths: Optional[List[str]] = None) -> List[str]:
    return [p for p in (paths or OUTPUT_JSON_PATHS) if os.path.exists(p)]


def load_blocked_model_options(review_path: str = REVIEW_OUTPUT_PATH) -> Dict[str, str]:
    if not os.path.exists(review_path):
        return {}
    try:
        with open(review_path, "r", encoding="utf-8") as fh:
            review = json.load(fh)
    except Exception:
        return {}
    options: Dict[str, str] = {}
    for entry in review.get("models", []) or []:
        if not isinstance(entry, dict):
            continue
        market = entry.get("market") or "IL"
        key = f"{market}|{entry.get('make', '')}|{entry.get('model', '')}"
        issues = entry.get("validation_issues") or []
        attempts = entry.get("repair_attempts", 0) or 0
        options[key] = f"{entry.get('make', '')} {entry.get('model', '')} — issues={len(issues)} — attempts={attempts}"
    return options


st.set_page_config(page_title="Vehicle Variant Catalog Runner", layout="wide")
_CONFIG = load_shared_config()

if "logs" not in st.session_state:
    st.session_state.logs = []


def presence(value: object) -> str:
    return "✅ exists" if value else "❌ missing"


def log_line(msg: str) -> None:
    st.session_state.logs.append(sanitize_error(msg))
    st.session_state.logs = st.session_state.logs[-400:]


st.title("🚗 Vehicle Variant Catalog Runner")
st.caption("Manual-only validation and repair with explicit model selection. Refresh does not start work.")

try:
    state = compute_resume_state()
    total = state["total_universe"] or 1
    st.progress(min(state["done"] / total, 1.0))
    st.info(f"Processed {state['done']}/{state['total_universe']} | ready {state['ready']} | blocked {state['blocked']} | remaining {state['remaining']} | next: {state.get('next_make') or 'START'} {state.get('next_model') or ''}")
except Exception as exc:  # noqa: BLE001
    st.warning(f"Progress unavailable: {sanitize_error(exc)}")
    state = {"next_key": None}

st.header("1 · Status")
fp = files_present()
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.subheader("Source files")
    st.write(f"variants: {presence(fp.get(VARIANTS_PATH))}")
    st.write(f"instructions: {presence(fp.get(INSTRUCTIONS_PATH))}")
with col_b:
    st.subheader("Secrets")
    st.write(f"GitHub token: {presence(_CONFIG.github_token)}")
    st.write(f"OpenAI key: {presence(_CONFIG.openai_api_key)}")
    st.write(f"Google key: {presence(_CONFIG.google_api_key)}")
with col_c:
    st.subheader("Outputs")
    for path in OUTPUT_JSON_PATHS:
        st.write(f"{path}: {presence(os.path.exists(path))}")

if st.button("🔎 Validate source files & join", key="join_button"):
    join = validate_and_join()
    st.session_state.join_summary = join.summary()
if st.session_state.get("join_summary"):
    st.json(st.session_state.join_summary)

st.header("2 · GitHub save")
st.write(f"GitHub token status: {presence(_CONFIG.github_token)}")
st.write(f"Repo full name: `{_CONFIG.github_repo_full_name or '(missing)'}`")
st.write(f"Target branch: `{_CONFIG.github_target_branch or '(missing)'}`")
st.write("Existing output files:", existing_output_paths() or "none")
autosave_default = github_autosave_enabled(token=_CONFIG.github_token, repo_full_name=_CONFIG.github_repo_full_name, target_branch=_CONFIG.github_target_branch)
autosave_enabled = st.checkbox("Autosave to GitHub after each processed vehicle model", value=autosave_default, key="autosave_enabled")
if st.button("💾 Push current outputs to GitHub", key="manual_push"):
    result = manual_push_outputs(token=_CONFIG.github_token, repo_full_name=_CONFIG.github_repo_full_name, target_branch=_CONFIG.github_target_branch, paths=OUTPUT_JSON_PATHS)
    if result.get("ok"):
        st.success(f"Pushed {len(result.get('saved', []))} file(s) to {result.get('repo_full_name')}@{result.get('target_branch')}")
    else:
        st.error(sanitize_error(result.get("error")))

st.header("3 · Build, repair, and scan")
validation_label = st.selectbox("Validation model", MODEL_OPTIONS, index=0, key="validation_model")
repair_label = st.selectbox("Blocked repair model", MODEL_OPTIONS, index=0, key="repair_model")
validation_provider = provider_settings_for_label(validation_label, _CONFIG)
repair_provider = provider_settings_for_label(repair_label, _CONFIG)

blocked_options = load_blocked_model_options()
selected_labels = st.multiselect("Blocked vehicle models to repair", options=list(blocked_options), format_func=lambda k: blocked_options[k], key="blocked_models_to_repair")
push_after_repair = st.checkbox("Push to GitHub after repair completes", value=bool(_CONFIG.github_token), key="push_after_repair")

col_run, col_repair, col_scan = st.columns(3)
with col_run:
    batch_size = st.number_input("models this batch", min_value=1, value=25, step=1, key="batch_size")
    run_clicked = st.button("▶️ Run next batch", type="primary", key="run_next_batch")
with col_repair:
    repair_batch = st.number_input("blocked models to repair", min_value=1, value=5, step=1, key="repair_batch")
    repair_clicked = st.button("🛠️ Repair blocked models", key="repair_blocked")
with col_scan:
    scan_clicked = st.button("🔬 Run quality scan", key="quality_scan")

log_box = st.empty()
progress_box = st.empty()


def _checkpoint() -> CatalogCheckpointConfig:
    return CatalogCheckpointConfig(enabled=bool(autosave_enabled), push_every_profiles=1, strict=False, token=_CONFIG.github_token, repo=_CONFIG.github_repo_full_name, branch=_CONFIG.github_target_branch)


def _on_log(msg: str) -> None:
    log_line(msg)
    log_box.code("\n".join(st.session_state.logs[-40:]) or "(no logs yet)")


def _on_progress(info: Dict[str, Any]) -> None:
    if info.get("phase") == "running":
        progress_box.info(f"[{info['index']}/{info['total']}] RUNNING — {info['make']} {info['model']}")
    elif info.get("phase") == "done":
        progress_box.success(f"[{info['index']}/{info['total']}] DONE — {info['make']} {info['model']}")
    elif info.get("phase") == "error":
        progress_box.warning(f"[{info['index']}/{info['total']}] ERROR — {info['make']} {info['model']} routed to review")

if run_clicked:
    ok, message = can_start_provider(validation_provider)
    if not ok:
        st.error(message)
        st.stop()
    st.session_state.logs = []
    try:
        with st.spinner(f"Running {validation_provider.display_name} batch..."):
            result = build_catalog(limit_models=int(batch_size), start_after_key=state.get("next_key"), provider_settings=validation_provider, checkpoint=_checkpoint(), log=_on_log, on_progress=_on_progress)
        st.success(f"Batch complete — ready {result.readiness['models_ready_for_website']} | blocked {result.readiness['models_blocked']} | total {result.readiness['total_models']}.")
    except Exception as exc:  # noqa: BLE001
        st.error(sanitize_error(exc))
        st.stop()

if repair_clicked:
    ok, message = can_start_provider(repair_provider)
    if not ok:
        st.error(message)
        st.stop()
    st.session_state.logs = []
    try:
        with st.spinner(f"Repairing with {repair_provider.display_name}..."):
            result = repair_review_models(batch=int(repair_batch), selected_keys=selected_labels or None, provider_settings=repair_provider, log=_on_log)
        st.success(f"Repair complete — processed {result['processed']}, promoted {result['promoted']}, kept {result['kept']}, skipped {result['skipped']}.")
        if push_after_repair:
            push = manual_push_outputs(token=_CONFIG.github_token, repo_full_name=_CONFIG.github_repo_full_name, target_branch=_CONFIG.github_target_branch, paths=OUTPUT_JSON_PATHS, message="catalog: Streamlit repair save")
            if push.get("ok"):
                st.success(f"Repair outputs pushed: {len(push.get('saved', []))} file(s).")
            else:
                st.error(f"Repair finished, but GitHub push failed: {sanitize_error(push.get('error'))}")
    except Exception as exc:  # noqa: BLE001
        st.error(sanitize_error(exc))
        st.stop()

if scan_clicked:
    catalog, _readiness, review = load_existing_outputs()
    report = scan_quality(catalog, review)
    totals = report["totals"]
    st.success(f"Quality: {totals.get('bug', 0)} bugs | {totals.get('leak', 0)} source-leaks | {totals.get('normalization', 0)} normalization | {totals.get('structure', 0)} structure")
    if autosave_enabled:
        push = manual_push_outputs(token=_CONFIG.github_token, repo_full_name=_CONFIG.github_repo_full_name, target_branch=_CONFIG.github_target_branch, paths=OUTPUT_JSON_PATHS, message="catalog: quality scan save")
        if not push.get("ok"):
            st.error(f"Quality scan saved locally, but GitHub push failed: {sanitize_error(push.get('error'))}")

st.header("4 · Logs")
st.code("\n".join(st.session_state.logs[-60:]) or "(no logs yet)")
