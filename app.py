"""Simplified Streamlit UI for the validation pipeline.

Primary purpose: operate validation safely from the source canonical through the
review queue. The source canonical is read-only, and the final clean database is
reserved for the explicit final export step.
"""
from __future__ import annotations

import streamlit as st

from core.config import GITHUB_BRANCH, get_branch_warning
from engine.validation import streamlit_helpers as ui

st.set_page_config(page_title="Yeda v3 — Validation", layout="wide")
st.title("🚗 Yeda Vehicle Variant Validation")

# ---------- Branch guard ----------
if GITHUB_BRANCH == "main":
    st.error(
        "🛑 Branch resolved to 'main'. Validation mode requires branch "
        "'validation-v2-budgeted-dual-il-trims'. Check your secrets configuration."
    )
    st.stop()

branch_warn = get_branch_warning()
if branch_warn:
    st.warning(branch_warn)

status = ui.load_status_payload()
source = status["source"]
summary = status["validation_summary"]
banner = status["final_banner"]

# ---------- 1. Final Status Banner ----------
if banner["state"] == "missing":
    st.info(banner["message"])
elif banner["state"] == "stale":
    st.warning(banner["message"])
else:
    st.success(banner["message"])

st.caption(
    "Source canonical is read-only. Final clean database is generated only by "
    "Export Final Clean Database. AI review only runs on problematic queue items."
)

# ---------- 2. Database Source ----------
st.header("SOURCE OF TRUTH")
st.subheader("Database Source")
source_cols = st.columns(5)
source_cols[0].write(f"**Source file path**  \n`{source['source_path']}`")
source_cols[1].metric("Source variants", source["source_variant_count"])
source_cols[2].metric("Verified", source["source_verified_count"])
source_cols[3].metric("Partial", source["source_partial_count"])
if source.get("seed_count") is not None:
    source_cols[4].metric("Seed count", source["seed_count"])
else:
    source_cols[4].write("**Seed count**  \nNot available")

if source.get("stale_root_is_stale"):
    st.warning(
        "⚠️ Stale root warning: root `resume_package_canonical.json` exists and has fewer variants "
        "than `data/canonical/resume_package_canonical.json`. Use the data/canonical source of truth."
    )
elif source.get("stale_root_exists"):
    st.caption("Root `resume_package_canonical.json` exists; source of truth remains `data/canonical/`.")

# ---------- 3. Validation Summary ----------
st.subheader("Validation Summary")
row1 = st.columns(4)
row1[0].metric("issues_total", summary["issues_total"])
row1[1].metric("critical", summary["critical"])
row1[2].metric("high", summary["high"])
row1[3].metric("medium", summary["medium"])
row2 = st.columns(4)
row2[0].metric("low", summary["low"])
row2[1].metric("model_review_items_available", summary["model_review_items_available"])
row2[2].metric("manual_review_items_available", summary["manual_review_items_available"])
row2[3].write(f"**last run time**  \n`{summary['last_run_time'] or 'not run yet'}`")

# ---------- 6. Actions ----------
st.subheader("Actions")
action_cols = st.columns(4)
with action_cols[0]:
    if st.button("Refresh Status", use_container_width=True):
        st.rerun()
with action_cols[1]:
    if st.button("Run Full Audit", use_container_width=True):
        with st.spinner("Running deterministic audit..."):
            result = ui.run_audit_and_refresh_queue()
        st.success(f"Audit complete: {result['issues_total']} issues found.")
        st.rerun()
with action_cols[2]:
    if st.button("Build/Refresh Review Queue", use_container_width=True):
        with st.spinner("Building review queue from deterministic audit..."):
            result = ui.run_audit_and_refresh_queue()
        st.success(f"Review queue refreshed: {result['issues_total']} items.")
        st.rerun()
with action_cols[3]:
    if st.button("Export Final Clean Database", use_container_width=True):
        with st.spinner("Exporting final clean database..."):
            export_summary = ui.export_final_clean_database()
        st.success(f"Final clean database exported: `{export_summary['path']}`")
        summary_cols = st.columns(5)
        summary_cols[0].metric("Input variants", export_summary["total_input_variants"])
        summary_cols[1].metric("Output variants", export_summary["total_output_variants"])
        summary_cols[2].metric("Safe applied", export_summary["safe_decisions_applied"])
        summary_cols[3].metric("Manual remaining", export_summary["manual_review_remaining_count"])
        summary_cols[4].write(f"**created_at**  \n`{export_summary['created_at']}`")

# ---------- 4. Review Queue Preview ----------
st.subheader("Review Queue Preview")
queue_preview = ui.load_queue_preview(max_rows=ui.DEFAULT_QUEUE_PREVIEW_LIMIT)
st.caption(f"Showing up to {queue_preview['max_rows']} of {queue_preview['total_items']} queue rows.")
st.dataframe(queue_preview["rows"], use_container_width=True, hide_index=True, column_order=queue_preview["columns"])

# ---------- 5. AI Review Controls ----------
st.subheader("AI Review Controls")
st.caption("AI review is routed by backend helpers and only considers queue items marked `requires_model_review=true`.")
options = ui.load_queue_filter_options()
control_cols = st.columns(4)
with control_cols[0]:
    max_items = st.number_input("max items to run", min_value=1, max_value=10, value=1, step=1)
with control_cols[1]:
    risk_levels = st.multiselect("risk levels", options=options["risk_levels"], default=options["risk_levels"])
with control_cols[2]:
    issue_types = st.multiselect("issue types", options=options["issue_types"], default=[])
with control_cols[3]:
    seed_id_filter = st.text_input("optional seed_id filter", value="")

ai_cols = st.columns(2)
preview_clicked = ai_cols[0].button("Preview AI Review", type="secondary", use_container_width=True)
run_clicked = ai_cols[1].button("Run AI Review", type="primary", use_container_width=True)

if preview_clicked or run_clicked:
    selected_issue_types = issue_types or None
    selected_seed = seed_id_filter.strip() or None
    if preview_clicked:
        preview = ui.load_ai_preview(
            max_items=int(max_items),
            risk_levels=risk_levels or None,
            issue_types=selected_issue_types,
            seed_id_filter=selected_seed,
            max_rows=ui.DEFAULT_AI_PREVIEW_LIMIT,
        )
        metric_cols = st.columns(4)
        metric_cols[0].metric("planned Gemini calls", preview.get("planned_gemini_calls", 0))
        metric_cols[1].metric("planned OpenAI calls", preview.get("planned_openai_calls", 0))
        metric_cols[2].metric("planned total calls", preview.get("planned_total_calls", 0))
        metric_cols[3].metric("estimated cost", f"${preview.get('estimated_cost_usd', 0):.4f}")
        st.caption(f"Showing up to {preview['max_rows']} of {preview.get('selected_items', 0)} routed items.")
        st.dataframe(preview["rows"], use_container_width=True, hide_index=True, column_order=preview["columns"])
        if preview.get("ok") is False:
            st.error(f"Preview blocked: {preview.get('error')} — {', '.join(preview.get('reasons', []))}")
    if run_clicked:
        with st.spinner("Running backend AI review..."):
            result = ui.run_ai_review(
                max_items=int(max_items),
                risk_levels=risk_levels or None,
                issue_types=selected_issue_types,
                seed_id_filter=selected_seed,
            )
        if result.get("ok") is False:
            st.error(f"AI review blocked: {result.get('error')} — {', '.join(result.get('reasons', []))}")
        else:
            st.success(f"AI review complete. Decisions written: {result.get('decisions_written', 0)}")

# ---------- Advanced Debug ----------
with st.expander("Advanced Debug / Raw Files"):
    st.caption("Compact snippets only. Full raw dumps stay out of the main UI.")
    for item in ui.load_debug_snippets():
        st.write(f"**{item['path']}** — {'exists' if item['exists'] else 'missing'} ({item['size_bytes']} bytes)")
        if item.get("snippet"):
            st.code(item["snippet"] + ("\n… truncated" if item.get("truncated") else ""), language="json")
