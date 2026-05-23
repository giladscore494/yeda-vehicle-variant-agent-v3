"""Yeda Vehicle Variant Agent v3 — Streamlit UI.

Calls engine functions and displays progress/results.
Does NOT directly mutate canonical.
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from core.config import config_summary, CANONICAL_RESUME_PATH
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

st.set_page_config(page_title="Yeda v3", layout="wide")
st.title("🚗 Yeda Vehicle Variant Agent v3")

# ---------- Sidebar: Config ----------
with st.sidebar:
    st.header("Configuration")
    cfg = config_summary()
    st.write(f"**Gemini key:** {cfg['gemini_key']}")
    st.write(f"**GitHub token:** {cfg['github_token']}")
    st.write(f"**GitHub repo:** {cfg['github_repo']}")
    st.write(f"**GitHub branch:** {cfg['github_branch']}")
    st.write(f"**Canonical:** {cfg['canonical_path']}")

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
tab_main, tab_manual, tab_diag = st.tabs(["Main Run", "Manual Seed", "Diagnostics / Export"])

# ==================== Main Run ====================
with tab_main:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Variants", len(all_variants))
    col2.metric("Processed", len(bs.get("processed_seed_ids", [])))
    col3.metric("Manual Review", len(bs.get("manual_review_seed_ids", [])))
    col4.metric("Failed", len(bs.get("failed_seed_ids", [])))

    st.write(f"**Next seed:** `{bs.get('next_seed_id', 'N/A')}`")
    st.write(f"**Last completed:** `{bs.get('last_completed_seed_id', 'N/A')}`")
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
                if result.get("ok"):
                    st.success("Batch completed!")
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
                from engine.retry_failed import retry_failed_seed as _retry_fn

                seed = find_seed_by_id(seeds, selected_failed)
                if seed:
                    with st.spinner("Running dry-run retry..."):
                        seed_result = run_seed(seed, selected_failed, dry_run=True)
                        decision = decide_seed_result(seed_result)
                        result = _retry_fn(
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
                from engine.retry_failed import retry_failed_seed as _retry_fn

                seed = find_seed_by_id(seeds, selected_failed)
                if seed:
                    with st.spinner("Running retry..."):
                        seed_result = run_seed(seed, selected_failed, dry_run=False)
                        decision = decide_seed_result(seed_result)
                        push_enabled_retry = st.session_state.get("push_enabled", False)
                        result = _retry_fn(
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
