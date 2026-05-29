"""Yeda Vehicle Variant Agent v3 — Validation Engine UI.

Primary purpose: validation of the existing canonical database.
Does NOT directly mutate canonical.
Treats data/canonical/resume_package_canonical.json as read-only input.
All validation outputs go under data/validated_runs/.
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from core.config import (
    config_summary,
    CANONICAL_RESUME_PATH,
    VALIDATION_OUTPUT_PATH,
    GITHUB_BRANCH,
    get_branch_warning,
)
from engine.state import (
    load_canonical,
    load_canonical_with_recovery,
    load_seeds,
    get_all_variants,
    get_batch_state,
    ensure_batch_state_fields,
    find_seed_by_id,
    seed_id_from_seed,
    CanonicalCorruptionError,
)
from engine.audit import audit_canonical

st.set_page_config(page_title="Yeda v3 — Validation Engine", layout="wide")
st.title("🚗 Yeda Vehicle Variant Agent v3 — Validation Engine")

_DEFAULT_TARGET_SEED_ID = "mg_(british_era)__tf__2002__2005__il"

# ---------- Branch guard ----------
if GITHUB_BRANCH == "main":
    st.error(
        "🛑 Branch resolved to 'main'. Validation mode requires branch "
        "'validation-v2-budgeted-dual-il-trims'. Check your secrets configuration."
    )
    st.stop()

# ---------- Sidebar: Config ----------
with st.sidebar:
    st.header("Configuration")
    cfg = config_summary()

    st.subheader("Keys & Tokens")
    st.write(f"**Gemini key present:** {'✅ yes' if cfg['gemini_key'] == 'configured' else '❌ no'}")
    st.write(f"**Gemini model resolved:** `{cfg['gemini_model']}`")
    st.write(f"**OpenAI key present:** {'✅ yes' if cfg['openai_key'] == 'configured' else '❌ no'}")
    st.write(f"**OpenAI model resolved:** `{cfg['openai_model']}`")
    st.write(f"**GitHub token present:** {'✅ yes' if cfg['github_token'] == 'configured' else '❌ no'}")

    st.subheader("Repo & Branch")
    st.write(f"**GitHub repo resolved:** `{cfg['github_repo']}`")
    st.write(f"**GitHub branch resolved:** `{cfg['github_branch']}`")

    st.subheader("Validation")
    st.write(f"**Validation mode:** `{cfg['validation_mode']}`")
    st.write(f"**Validation output path:** `{cfg['validation_output_path']}`")
    st.write(f"**Dry run status:** {'🟡 enabled' if cfg['dry_run'] else '🟢 disabled'}")
    st.write(f"**Repo write status:** {'🟢 enabled' if cfg['repo_write'] else '🔴 disabled'}")

    branch_warn = get_branch_warning()
    if branch_warn:
        st.warning(branch_warn)

# ---------- Load data ----------
try:
    canonical = load_canonical_with_recovery(
        CANONICAL_RESUME_PATH,
        backup_path=cfg.get("backup_path"),
    )
    if "_recovery" in canonical:
        st.warning(
            f"⚠️ Canonical was corrupted and restored from backup: "
            f"{canonical['_recovery']['restored_from']}"
        )
        del canonical["_recovery"]
    ensure_batch_state_fields(canonical)
    bs = get_batch_state(canonical)
    all_variants = get_all_variants(canonical)
    seeds = load_seeds("data/seeds/vehicle_model_seeds_il.json")
    data_loaded = True
except CanonicalCorruptionError as exc:
    st.error(
        "🛑 Canonical JSON is corrupted. Restore from backup before running.\n\n"
        f"**Path:** `{exc.path}`\n\n"
        f"**Size:** {exc.size} bytes\n\n"
        f"**Line:** {exc.line}, **Column:** {exc.column}, **Position:** {exc.pos}"
    )
    data_loaded = False
except Exception as exc:
    st.error(f"Failed to load data: {exc}")
    data_loaded = False

if not data_loaded:
    st.stop()

# ---------- Load validation state ----------
from engine.validation.validation_state import load_validation_state

val_state = load_validation_state()

# ---------- Tabs ----------
tab_validation, tab_partial, tab_legacy = st.tabs(
    ["🔍 Validation Run", "📋 Partial Variants", "🔧 Legacy Build Diagnostics"]
)

# ==================== VALIDATION RUN ====================
with tab_validation:
    # ── Validation Status Dashboard ─────────────────────────────────────
    st.subheader("Validation Status")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Variants", len(all_variants))
    col2.metric("Verified", len(canonical.get("verified_variants") or []))
    col3.metric("Partial", len(canonical.get("partial_variants") or []))
    col4.metric("Total Seeds", len(seeds))

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Processed Seeds", len(bs.get("processed_seed_ids", [])))
    col6.metric("Failed Seeds", len(bs.get("failed_seed_ids", [])))
    col7.metric("Manual Review Seeds", len(bs.get("manual_review_seed_ids", [])))
    col8.metric("Validation Run ID", val_state.get("validation_run_id", "N/A")[:20])

    st.write(f"**Validation source canonical:** `{CANONICAL_RESUME_PATH}`")
    st.write(f"**Validation output path:** `{VALIDATION_OUTPUT_PATH}`")
    st.write(f"**Validation mode:** `{cfg['validation_mode']}`")
    st.write(f"**Current stage:** `{val_state.get('current_stage', 'READY')}`")

    completed_items = val_state.get("completed_validation_items") or []
    failed_items = val_state.get("failed_validation_items") or []
    manual_items = val_state.get("manual_review_validation_items") or []

    if completed_items:
        st.write(f"**Completed validation items:** {len(completed_items)}")
    if failed_items:
        st.write(f"**Failed validation items:** {len(failed_items)}")
    if manual_items:
        st.write(f"**Manual review items:** {len(manual_items)}")

    if val_state.get("last_error_type"):
        st.error(
            f"**Last error:** `{val_state['last_error_type']}` — "
            f"{val_state.get('last_error_message', '')}"
        )

    st.write(f"**GitHub branch resolved:** `{cfg['github_branch']}`")
    st.write(f"**Gemini key status:** {cfg['gemini_key']}")
    st.write(f"**OpenAI key status:** {cfg['openai_key']}")
    st.write(f"**GitHub token status:** {cfg['github_token']}")

    st.divider()

    # ── Actions ─────────────────────────────────────────────────────────
    st.subheader("Validation Actions")

    col_a1, col_a2 = st.columns(2)

    with col_a1:
        if st.button("🔄 Reset Validation Session", type="secondary"):
            from engine.validation.validation_state import reset_validation_session
            new_state = reset_validation_session()
            st.success(f"✅ Validation session reset. New run ID: `{new_state['validation_run_id']}`")
            st.rerun()

        if st.button("🔎 Run Deterministic Audit"):
            from engine.validation.validation_runner import run_deterministic_audit_only
            with st.spinner("Running deterministic audit over all variants..."):
                result = run_deterministic_audit_only()
                if result["ok"]:
                    summary = result["summary"]
                    st.success(
                        f"✅ Deterministic audit complete. "
                        f"**{result['total_issues']}** issues found."
                    )
                    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                    by_sev = summary.get("by_severity", {})
                    col_s1.metric("Critical", by_sev.get("critical", 0))
                    col_s2.metric("High", by_sev.get("high", 0))
                    col_s3.metric("Medium", by_sev.get("medium", 0))
                    col_s4.metric("Low", by_sev.get("low", 0))

                    with st.expander("Issue Details"):
                        st.json(result["issues"][:100])
                else:
                    st.error(f"❌ Audit failed: {result.get('error')}")

    with col_a2:
        if st.button("🎯 Run Targeted Failed Seed Validation"):
            from engine.validation.validation_runner import run_targeted_seed_validation
            with st.spinner(f"Validating targeted seed: {_DEFAULT_TARGET_SEED_ID}..."):
                result = run_targeted_seed_validation(_DEFAULT_TARGET_SEED_ID)
                if result["ok"]:
                    tr = result["result"]
                    status_icon = "✅" if tr.get("failure_was_stale_state") else "⚠️"
                    st.success(
                        f"{status_icon} Targeted seed validation complete.\n\n"
                        f"**Status:** {tr.get('validation_status')}\n\n"
                        f"**Action:** {tr.get('recommended_action')}"
                    )
                    with st.expander("Full Result"):
                        st.json(tr)
                else:
                    st.error(f"❌ Validation failed: {result.get('error')}")

        if st.button("🔍 Run Suspicious Groups Detection"):
            from engine.validation.validation_runner import run_suspicious_groups_validation
            with st.spinner("Detecting suspicious groups..."):
                result = run_suspicious_groups_validation()
                if result["ok"]:
                    summary = result["summary"]
                    st.success(
                        f"✅ Found **{result['total_groups']}** suspicious groups "
                        f"({summary.get('total_variants_in_groups', 0)} variants)."
                    )
                    by_risk = summary.get("by_risk_level", {})
                    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
                    col_r1.metric("Critical", by_risk.get("critical", 0))
                    col_r2.metric("High", by_risk.get("high", 0))
                    col_r3.metric("Medium", by_risk.get("medium", 0))
                    col_r4.metric("Low", by_risk.get("low", 0))

                    with st.expander("Suspicious Groups"):
                        st.json(result["groups"][:50])
                else:
                    st.error(f"❌ Detection failed: {result.get('error')}")

    st.divider()

    col_full, col_export = st.columns(2)

    with col_full:
        if st.button("▶️ Run Full Validation Session", type="primary"):
            from engine.validation.validation_runner import run_full_validation
            with st.spinner("Running full validation session..."):
                result = run_full_validation()
                if result["ok"]:
                    st.success(
                        f"✅ Full validation complete!\n\n"
                        f"**Run ID:** {result['validation_run_id']}\n\n"
                        f"**Variants scanned:** {result['total_variants_scanned']}\n\n"
                        f"**Seeds scanned:** {result['total_seeds_scanned']}"
                    )

                    det = result.get("deterministic_issues", {})
                    sg = result.get("suspicious_groups", {})
                    pv = result.get("partial_variants", {})

                    st.subheader("Results Summary")
                    col_r1, col_r2, col_r3 = st.columns(3)
                    col_r1.metric("Deterministic Issues", det.get("total_issues", 0))
                    col_r2.metric("Suspicious Groups", sg.get("total_suspicious_groups", 0))
                    col_r3.metric("Partial Variants", pv.get("total_partial_variants", 0))

                    st.info(
                        "ℹ️ Full Validation does NOT automatically call models. "
                        "Use **Run Model Validation on Suspicious Groups** to trigger model calls."
                    )

                    with st.expander("Full Result"):
                        st.json(result)
                else:
                    st.error(f"❌ Validation failed: {json.dumps(result.get('error', {}), indent=2)}")

    with col_export:
        if st.button("📥 Export Validation Report"):
            report_path = Path("data/validated_runs/validation_report_v2.json")
            if report_path.exists():
                report_data = report_path.read_text(encoding="utf-8")
                st.download_button(
                    "Download Validation Report",
                    data=report_data,
                    file_name="validation_report_v2.json",
                    mime="application/json",
                )
            else:
                st.info("No validation report found. Run a full validation first.")

    # ── Model Validation Section ────────────────────────────────────────
    st.divider()
    st.subheader("Model Validation")

    col_model, col_save = st.columns(2)

    with col_model:
        if st.button("🤖 Run Model Validation on Suspicious Groups", type="primary"):
            try:
                from engine.validation.validation_runner import (
                    run_model_validation_on_suspicious_groups,
                )
            except ImportError as exc:
                st.error(
                    "❌ Model validation could not be loaded. "
                    f"Check deployment dependencies. Details: {exc}"
                )
            else:
                with st.spinner("Running model validation on suspicious groups..."):
                    try:
                        model_result = run_model_validation_on_suspicious_groups()
                    except ImportError as exc:
                        st.error(
                            "❌ Model validation dependencies are unavailable. "
                            f"Details: {exc}"
                        )
                    else:
                        if model_result["ok"]:
                            if model_result.get("model_validation_ran", False):
                                st.success("✅ Model validation complete!")
                                col_m1, col_m2, col_m3 = st.columns(3)
                                col_m1.metric(
                                    "Gemini Calls",
                                    f"{model_result.get('gemini_calls_success', 0)}/{model_result.get('gemini_calls_attempted', 0)}",
                                )
                                col_m2.metric(
                                    "OpenAI Calls",
                                    f"{model_result.get('openai_calls_success', 0)}/{model_result.get('openai_calls_attempted', 0)}",
                                )
                                col_m3.metric(
                                    "Items Validated",
                                    model_result.get("model_validation_items_count", 0),
                                )

                                if model_result.get("model_validation_failed_items_count", 0) > 0:
                                    st.warning(
                                        f"⚠️ {model_result['model_validation_failed_items_count']} "
                                        f"items failed model validation."
                                    )
                                if model_result.get("last_model_validation_error"):
                                    st.error(
                                        f"Last error: {model_result['last_model_validation_error']}"
                                    )
                            else:
                                st.info(
                                    f"ℹ️ {model_result.get('reason', 'No suspicious groups found')}"
                                )
                        else:
                            st.error(
                                f"❌ Model validation failed: "
                                f"{json.dumps(model_result.get('error', {}), indent=2)}"
                            )

    with col_save:
        if st.button("💾 Save Validation Outputs to GitHub", type="secondary"):
            from engine.validation.github_save import (
                save_validation_outputs_to_github,
                get_files_to_save,
            )

            run_id = val_state.get("validation_run_id", "unknown")

            # Show what will be saved
            files_info = get_files_to_save()
            existing_files = [f for f in files_info if f["exists"]]

            if not existing_files:
                st.warning("No validation output files found to save.")
            else:
                st.write("**Files to save:**")
                for f in existing_files:
                    st.write(f"  📄 `{f['path']}` ({f['size']:,} bytes)")

                with st.spinner("Saving to GitHub..."):
                    save_result = save_validation_outputs_to_github(
                        validation_run_id=run_id,
                    )

                    if save_result["ok"]:
                        st.success(
                            f"✅ Saved to GitHub!\n\n"
                            f"**Repo:** `{save_result['repo']}`\n\n"
                            f"**Branch:** `{save_result['target_branch']}`\n\n"
                            f"**Commit SHA:** `{save_result.get('commit_sha', 'N/A')}`"
                        )
                    else:
                        st.error(
                            f"❌ Save failed: {save_result.get('error', 'Unknown error')}"
                        )

                    with st.expander("Save Details"):
                        st.json(save_result)

    # ── Model Validation Status ─────────────────────────────────────────
    st.divider()
    st.subheader("Model Validation Status")

    model_results_path = Path("data/validated_runs/model_validation_results_v2.json")
    if model_results_path.exists():
        try:
            model_data = json.loads(model_results_path.read_text(encoding="utf-8"))
            mcs = model_data.get("model_calls_summary", {})

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.write(f"**deterministic_validation_ran:** ✅")
                st.write(f"**model_validation_ran:** {'✅' if model_data.get('model_validation_ran') else '❌'}")
                st.write(f"**gemini_calls_attempted:** {mcs.get('gemini_calls_attempted', 0)}")
                st.write(f"**gemini_calls_success:** {mcs.get('gemini_calls_success', 0)}")
                st.write(f"**gemini_calls_failed:** {mcs.get('gemini_calls_failed', 0)}")
            with col_s2:
                st.write(f"**openai_calls_attempted:** {mcs.get('openai_calls_attempted', 0)}")
                st.write(f"**openai_calls_success:** {mcs.get('openai_calls_success', 0)}")
                st.write(f"**openai_calls_failed:** {mcs.get('openai_calls_failed', 0)}")
                st.write(f"**model_validation_items_count:** {model_data.get('model_validation_items_count', 0)}")
                st.write(f"**model_validation_failed_items_count:** {model_data.get('model_validation_failed_items_count', 0)}")

            st.write(f"**model_validation_output_path:** `{model_data.get('model_validation_output_path', '')}`")
            if model_data.get("last_model_validation_error"):
                st.write(f"**last_model_validation_error:** {model_data['last_model_validation_error']}")
        except Exception:
            st.warning("Could not load model validation results.")
    else:
        st.info("No model-based validation was executed; deterministic audit only.")

    # ── Show existing validation outputs ────────────────────────────────
    st.divider()
    st.subheader("Existing Validation Outputs")

    validated_runs_dir = Path("data/validated_runs")
    if validated_runs_dir.exists():
        output_files = sorted(validated_runs_dir.glob("*.json"))
        if output_files:
            for f in output_files:
                st.write(f"📄 `{f.name}` ({f.stat().st_size:,} bytes)")
        else:
            st.info("No validation output files yet.")
    else:
        st.info("data/validated_runs/ directory does not exist yet.")

    # Validation runtime state
    val_runtime_path = Path("data/runtime/current_validation_run.json")
    if val_runtime_path.exists():
        with st.expander("Current Validation Run State"):
            st.json(json.loads(val_runtime_path.read_text()))

# ==================== PARTIAL VARIANTS ====================
with tab_partial:
    st.subheader("📋 Partial Variants Analysis")

    partial_variants = canonical.get("partial_variants") or []
    st.metric("Total Partial Variants", len(partial_variants))

    if st.button("🔎 Classify Partial Variants"):
        from engine.validation.partial_variants import (
            classify_all_partial_variants,
            summarize_partial_variants,
        )
        with st.spinner("Classifying partial variants..."):
            classifications = classify_all_partial_variants(canonical)
            summary = summarize_partial_variants(classifications)

            st.subheader("Partial Variants Summary")
            col_p1, col_p2, col_p3, col_p4 = st.columns(4)
            col_p1.metric("Total", summary["total_partial_variants"])
            col_p2.metric("Valid Keep", summary.get("valid_partial_keep", 0))
            col_p3.metric("Needs Evidence", summary.get("needs_evidence", 0))
            col_p4.metric("Manual Review", summary.get("manual_review_required", 0))

            col_p5, col_p6, col_p7, col_p8 = st.columns(4)
            col_p5.metric("Merge Candidates", summary.get("merge_candidate", 0))
            col_p6.metric("Promote Candidates", summary.get("promote_to_verified_candidate", 0))
            col_p7.metric("Needs Normalization", summary.get("needs_normalization", 0))
            col_p8.metric("Reject Candidates", summary.get("reject_candidate", 0))

            st.divider()
            st.subheader("Risk Distribution")
            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
            col_r1.metric("Low Risk", summary.get("risk_low", 0))
            col_r2.metric("Medium Risk", summary.get("risk_medium", 0))
            col_r3.metric("High Risk", summary.get("risk_high", 0))
            col_r4.metric("Critical Risk", summary.get("risk_critical", 0))

            with st.expander("All Classifications"):
                st.json(classifications[:100])

# ==================== LEGACY BUILD DIAGNOSTICS (READ-ONLY) ====================
with tab_legacy:
    st.subheader("🔧 Legacy Build Diagnostics (Read-Only)")
    st.info(
        "⚠️ This section is READ-ONLY. The validation engine does NOT use the build flow. "
        "Build generation, retry, and canonical mutation actions are disabled on this branch."
    )

    _LEGACY_DISABLED_MSG = "legacy_build_action_disabled_in_validation_branch"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Variants", len(all_variants))
    col2.metric("Processed", len(bs.get("processed_seed_ids", [])))
    col3.metric("Manual Review", len(bs.get("manual_review_seed_ids", [])))
    col4.metric("Failed", len(bs.get("failed_seed_ids", [])))

    st.write(f"**Next seed:** `{bs.get('next_seed_id', 'N/A')}`")
    st.write(f"**Last completed:** `{bs.get('last_completed_seed_id', 'N/A')}`")
    if bs.get("last_failed_seed_id"):
        st.write(f"**Last failed:** `{bs['last_failed_seed_id']}` at `{bs.get('last_failed_at', 'N/A')}`")
    if bs.get("last_handled_seed_id"):
        st.write(f"**Last handled (manual/review):** `{bs['last_handled_seed_id']}`")
    st.write(f"**Total seeds:** {len(seeds)}")

    st.divider()

    st.subheader("Config Source Resolution")
    diag_cfg = config_summary()
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.write(f"**Gemini key present:** {diag_cfg['gemini_key']}")
        st.write(f"**OpenAI key present:** {diag_cfg['openai_key']}")
        st.write(f"**GitHub token present:** {diag_cfg['github_token']}")
        st.write(f"**GitHub repo:** {diag_cfg['github_repo']}")
        st.write(f"**GitHub branch:** {diag_cfg['github_branch']}")
    with col_d2:
        st.write(f"**Canonical path:** {diag_cfg['canonical_path']}")
        st.write(f"**Runtime path:** {diag_cfg['runtime_state_path']}")
        st.write(f"**Validation runtime:** {diag_cfg['validation_runtime_state_path']}")
        if diag_cfg.get("branch_warning"):
            st.warning(diag_cfg["branch_warning"])

    st.divider()

    st.subheader("True Queue Status")
    if st.button("🔎 Compute True Queue State"):
        from engine.reset import audit_queue_state
        queue_state = audit_queue_state(canonical, seeds)
        col_q1, col_q2, col_q3, col_q4, col_q5 = st.columns(5)
        col_q1.metric("Total Seeds", queue_state["total_catalog_seeds"])
        col_q2.metric("Processed", queue_state["processed_count"])
        col_q3.metric("Manual Review", queue_state["manual_review_count"])
        col_q4.metric("Failed", queue_state["failed_count"])
        col_q5.metric("Unresolved", queue_state["unresolved_count"])

        if queue_state["orphaned_count"]:
            st.warning(
                f"⚠️ {queue_state['orphaned_count']} processed IDs not in seed catalog: "
                f"{queue_state['orphaned_seed_ids'][:10]}"
            )

        with st.expander("Full Queue Details"):
            st.json(queue_state)

    st.divider()

    st.subheader("Seed Audit")
    audit_seed_id = st.text_input(
        "Audit specific seed ID",
        value=_DEFAULT_TARGET_SEED_ID,
        key="audit_seed_input",
    )
    if st.button("🔍 Audit This Seed"):
        from engine.reset import audit_specific_seed
        audit_result = audit_specific_seed(audit_seed_id, canonical, seeds)
        if audit_result["is_stale_failure"]:
            st.info(
                f"✅ **{audit_seed_id}** is a stale failure — already properly resolved. "
                f"Resolution: {audit_result['resolution_detail']}"
            )
        elif audit_result["needs_retry"]:
            cause = audit_result["failure_cause"] or "unknown"
            st.warning(
                f"⚠️ **{audit_seed_id}** needs retry. "
                f"Failure cause: **{cause}** — {audit_result['reason']}"
            )
        elif not audit_result["in_failed"]:
            st.success(f"✅ **{audit_seed_id}** is not in failed queue.")
        st.json(audit_result)

    st.divider()

    st.subheader("Legacy Audit")
    if st.button("🔎 Run Legacy Audit"):
        ok, errs = audit_canonical(canonical, seed_catalog=seeds)
        if ok:
            st.success("✅ Audit passed")
        else:
            st.error("❌ Audit failed")
            for e in errs:
                st.write(f"- {e}")

    st.divider()

    st.subheader("Counts")
    counts = canonical.get("counts") or {}
    st.json(counts)

    st.subheader("Batch State Summary")
    st.json({
        "processed": len(bs.get("processed_seed_ids", [])),
        "manual_review": len(bs.get("manual_review_seed_ids", [])),
        "failed": len(bs.get("failed_seed_ids", [])),
        "needs_retry": len(bs.get("needs_retry_seed_ids", [])),
        "next_seed_id": bs.get("next_seed_id"),
        "last_completed_seed_id": bs.get("last_completed_seed_id"),
        "last_failed_seed_id": bs.get("last_failed_seed_id"),
        "last_handled_seed_id": bs.get("last_handled_seed_id"),
    })

    st.divider()
    st.subheader("Export")
    if st.button("📥 Download Canonical"):
        st.download_button(
            "Download JSON",
            data=json.dumps(canonical, ensure_ascii=False, indent=2),
            file_name="resume_package_canonical.json",
            mime="application/json",
        )
