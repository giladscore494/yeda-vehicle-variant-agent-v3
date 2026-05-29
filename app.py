"""Yeda Vehicle Variant Agent v3 — Streamlit UI.

Calls engine functions and displays progress/results.
Does NOT directly mutate canonical.
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from core.config import config_summary, CANONICAL_RESUME_PATH, get_branch_warning
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
from engine.batch import run_batch
from engine.retry_failed import retry_failed_seed as _retry_failed_seed
from engine.reset import (
    reset_validation_state,
    audit_queue_state,
    audit_specific_seed,
    remove_stale_failure,
)

st.set_page_config(page_title="Yeda v3", layout="wide")
st.title("🚗 Yeda Vehicle Variant Agent v3")

# Default seed ID for audit/stale-failure UI (known failed seed from previous run)
_DEFAULT_AUDIT_SEED_ID = "mg_(british_era)__tf__2002__2005__il"

# ---------- Sidebar: Config ----------
with st.sidebar:
    st.header("Configuration")
    cfg = config_summary()
    st.write(f"**Gemini key:** {cfg['gemini_key']}")
    st.write(f"**GitHub token:** {cfg['github_token']}")
    st.write(f"**GitHub repo:** {cfg['github_repo']}")
    st.write(f"**GitHub branch:** {cfg['github_branch']}")
    st.write(f"**Canonical:** {cfg['canonical_path']}")

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

# ---------- Tabs ----------
tab_main, tab_manual, tab_diag, tab_reset = st.tabs(
    ["Main Run", "Manual Seed", "Diagnostics / Export", "Reset / Audit"]
)

# ==================== Main Run ====================
with tab_main:
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

    batch_size = st.number_input("Batch size", min_value=1, max_value=50, value=1)
    push_enabled = st.checkbox("Push to GitHub after save", value=False)

    col_dry, col_run = st.columns(2)

    with col_dry:
        if st.button("🔍 Dry-run next"):
            with st.spinner("Running dry-run..."):
                result = run_batch(
                    batch_size=1,
                    dry_run=True,
                    push_to_github=False,
                )
                st.json(result)

    with col_run:
        if st.button(f"▶️ Run next {batch_size}"):
            with st.spinner(f"Running batch of {batch_size}..."):
                result = run_batch(
                    batch_size=batch_size,
                    dry_run=False,
                    push_to_github=push_enabled,
                )

                # Determine completion message
                failed_q = bs.get("failed_seed_ids") or []
                manual_q = bs.get("manual_review_seed_ids") or []
                batch_results = result.get("results", [])
                any_success = any(
                    r.get("action") in ("ACCEPT_VARIANTS", "CLOSE_NO_VARIANTS_PROVEN")
                    for r in batch_results
                )

                if result.get("ok"):
                    if not batch_results:
                        # No seeds ran at all
                        if failed_q or manual_q:
                            st.warning(
                                "⚠️ No normal seeds left. "
                                "Resolve failed/manual review queues."
                            )
                        else:
                            st.info("No seeds to process.")
                    elif any_success:
                        st.success("✅ Batch completed!")
                    else:
                        st.info("Batch finished — no seeds were successfully resolved.")
                else:
                    st.error(f"Batch failed: {result.get('error')}")

                # Show results
                if "results" in result:
                    st.subheader("Seed Results")
                    for r in result["results"]:
                        action = r.get("action", "?")
                        icon = {"ACCEPT_VARIANTS": "✅", "CLOSE_NO_VARIANTS_PROVEN": "📋",
                                "MANUAL_REVIEW": "⚠️", "FAIL_TRANSIENT": "❌"}.get(action, "❓")
                        st.write(f"{icon} `{r['seed_id']}` → **{action}** "
                                 f"(+{r.get('added_count', 0)} added, "
                                 f"{r.get('merged_count', 0)} merged)")

                if "tracker" in result:
                    with st.expander("Progress Details"):
                        st.json(result["tracker"])

    # Runtime progress file
    runtime_path = Path("data/runtime/current_run.json")
    if runtime_path.exists():
        with st.expander("Current Run Progress"):
            st.json(json.loads(runtime_path.read_text()))

# ==================== Manual Seed ====================
with tab_manual:
    st.subheader("Run a specific seed")

    manual_seed_id = st.text_input("Seed ID", value=bs.get("next_seed_id") or "")

    if st.button("🔍 Dry-run this seed"):
        seed = find_seed_by_id(seeds, manual_seed_id)
        if seed:
            from engine.run_seed import run_seed
            from engine.decision import decide_seed_result
            with st.spinner("Running..."):
                result = run_seed(seed, manual_seed_id, dry_run=True)
                st.json({
                    "ok": result.ok,
                    "candidates": len(result.candidate_variants),
                    "no_variants_reason": result.no_variants_reason,
                    "errors": result.errors,
                })
        else:
            st.error(f"Seed not found: {manual_seed_id}")

    # Manual review queue
    manual_seeds = bs.get("manual_review_seed_ids") or []
    if manual_seeds:
        st.subheader(f"Manual Review Queue ({len(manual_seeds)})")
        for sid in manual_seeds[:20]:
            st.write(f"- `{sid}`")

# ==================== Failed Seed Retry ====================
with tab_manual:
    st.divider()
    st.subheader("🔁 Retry Failed Seeds")

    failed_seeds = bs.get("failed_seed_ids") or []
    if failed_seeds:
        st.write(f"**Failed seeds ({len(failed_seeds)}):**")
        for fs in failed_seeds:
            st.write(f"- `{fs}`")

        selected_failed = st.selectbox(
            "Select failed seed to retry",
            options=failed_seeds,
            key="retry_failed_select",
        )

        col_retry_dry, col_retry_save = st.columns(2)

        with col_retry_dry:
            if st.button("🔍 Dry-run failed seed"):
                from engine.run_seed import run_seed
                from engine.decision import decide_seed_result

                seed = find_seed_by_id(seeds, selected_failed)
                if seed:
                    with st.spinner("Running dry-run retry..."):
                        seed_result = run_seed(seed, selected_failed, dry_run=True)
                        decision = decide_seed_result(seed_result)
                        result = _retry_failed_seed(
                            seed_id=selected_failed,
                            decision=decision,
                            canonical=canonical,
                            seeds=seeds,
                            dry_run=True,
                        )
                        st.json(result)
                else:
                    st.error(f"Seed not found in catalog: {selected_failed}")

        with col_retry_save:
            if st.button("▶️ Retry failed seed and save"):
                from engine.run_seed import run_seed
                from engine.decision import decide_seed_result

                seed = find_seed_by_id(seeds, selected_failed)
                if seed:
                    with st.spinner("Running retry..."):
                        seed_result = run_seed(seed, selected_failed, dry_run=False)
                        decision = decide_seed_result(seed_result)
                        push_enabled_retry = st.session_state.get("push_enabled", False)
                        result = _retry_failed_seed(
                            seed_id=selected_failed,
                            decision=decision,
                            canonical=canonical,
                            seeds=seeds,
                            dry_run=False,
                            push_to_github=push_enabled_retry,
                            canonical_path=CANONICAL_RESUME_PATH,
                        )
                        if result.get("ok"):
                            st.success("✅ Retry completed!")
                        else:
                            st.error(f"❌ Retry failed: {result.get('error')}")
                        st.json(result)
                else:
                    st.error(f"Seed not found in catalog: {selected_failed}")
    else:
        st.info("No failed seeds to retry.")

# ==================== Diagnostics ====================
with tab_diag:
    st.subheader("Config Source Resolution")
    diag_cfg = config_summary()
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.write(f"**Gemini key present:** {diag_cfg['gemini_key']}")
        st.write(f"**GitHub token present:** {diag_cfg['github_token']}")
        st.write(f"**GitHub repo:** {diag_cfg['github_repo']}")
        st.write(f"**GitHub branch:** {diag_cfg['github_branch']}")
    with col_d2:
        st.write(f"**Canonical path:** {diag_cfg['canonical_path']}")
        st.write(f"**Runtime path:** {diag_cfg['runtime_state_path']}")
        if diag_cfg.get("branch_warning"):
            st.warning(diag_cfg["branch_warning"])

    st.divider()

    st.subheader("True Queue Status")
    if st.button("🔎 Compute True Queue State"):
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
        value=_DEFAULT_AUDIT_SEED_ID,
        key="audit_seed_input",
    )
    if st.button("🔍 Audit This Seed"):
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

    st.subheader("Audit")
    if st.button("🔎 Run Audit"):
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

# ==================== Reset / Audit ====================
with tab_reset:
    st.subheader("🔄 Reset Validation Run State")
    st.warning(
        "This resets **only** runtime/progress state (current_run.json). "
        "Canonical data (variants, batch_state) is **not** touched."
    )

    if st.button("⚠️ Reset Validation Run State", type="primary"):
        reset_result = reset_validation_state(canonical, seeds)
        if reset_result["ok"]:
            st.success(
                f"✅ Validation state reset. New run ID: `{reset_result['new_run_id']}`"
            )
            with st.expander("Reset Details"):
                st.json(reset_result)
        else:
            st.error("Failed to reset state.")

    st.divider()

    st.subheader("🧹 Remove Stale Failure")
    st.write(
        "If a seed is in the failed queue but already properly resolved "
        "in canonical, you can remove it from the failed queue here."
    )

    stale_seed_id = st.text_input(
        "Seed ID to check/remove",
        value=_DEFAULT_AUDIT_SEED_ID,
        key="stale_seed_input",
    )

    col_audit, col_remove = st.columns(2)
    with col_audit:
        if st.button("🔍 Audit before removal"):
            result = audit_specific_seed(stale_seed_id, canonical, seeds)
            st.json(result)

    with col_remove:
        if st.button("🧹 Remove stale failure"):
            # First audit
            audit_result = audit_specific_seed(stale_seed_id, canonical, seeds)
            if audit_result["is_stale_failure"]:
                remove_result = remove_stale_failure(
                    stale_seed_id, canonical,
                    audit_note=f"Stale failure removed via UI. Resolution: {audit_result['resolution_detail']}",
                )
                if remove_result["ok"]:
                    st.success(f"✅ Removed `{stale_seed_id}` from failed queue.")
                    st.json(remove_result)
                else:
                    st.error(f"Failed: {remove_result.get('error')}")
            elif audit_result["needs_retry"]:
                st.error(
                    f"❌ Cannot remove — `{stale_seed_id}` genuinely needs retry. "
                    f"Failure cause: {audit_result['failure_cause']}"
                )
            else:
                st.info(f"`{stale_seed_id}` is not in the failed queue.")
