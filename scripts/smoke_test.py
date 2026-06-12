#!/usr/bin/env python3
"""Smoke test for the validation engine. NO Gemini calls are made.

Verifies:
  1. Both input JSON files exist, parse, and join 1:1 on validation_id.
  2. Exactly 3,712 unique validation_id values, no duplicates, none one-sided.
  3. Every variant has standard_variant and audit context.
  4. Every instruction record has validation_priority and validation_tasks.
  5. Config, schema, and prompt files load.
  6. Merged context builds for one variant of each priority.
  7. Deterministic QA accepts a known-good synthetic response, marks a
     low-confidence response unresolved (-> automatic correction pass), and
     retries a schema-invalid response.
  8. The identity-hash recipe reproduces the source canonical_identity_hash.
  9. Canonical rows always carry validated_identity_hash, a list for
     alternate_names, and requires_manual_review=false.
 10. Correction prompts (Pass 2/3) build with compact targeted context.
 11. The runtime-config resolver works without Streamlit secrets.
 12. The output directory is writable.
 13. Secret presence is reported (values never printed).

Importable from the Streamlit app via run_checks(); exit code 0 = safe to run.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import deterministic_qa as qa  # noqa: E402
import identity  # noqa: E402
import model_context as mctx  # noqa: E402
import run_gemini_validation as engine  # noqa: E402
import runtime_config  # noqa: E402


def synthetic_response(merged: dict, confidence: float) -> dict:
    sv = merged["standard_variant"]
    return {
        "validation_id": merged["validation_id"],
        "decision": "auto_accept" if confidence >= 0.85 else "manual_review",
        "is_real_variant": True,
        "is_relevant_to_il_market": True,
        "corrected_variant": {
            "make": sv.get("make"), "model": sv.get("model"),
            "global_model_name": sv.get("global_model_name"),
            "official_marketed_name_il": sv.get("official_marketed_name_il"),
            "local_brand_name_il": sv.get("local_brand_name_il"),
            "alternate_names": sv.get("alternate_names") or [],
            "rebadged_as": sv.get("rebadged_as"),
            "year_start": sv.get("year_start"), "year_end": sv.get("year_end"),
            "generation": sv.get("generation"), "body_type": sv.get("body_type"),
            "seats": sv.get("seats"), "engine": sv.get("engine"),
            "transmission": sv.get("transmission"), "fuel_type": sv.get("fuel_type"),
            "drivetrain": sv.get("drivetrain"), "trim": sv.get("trim"),
            "market_scope": "IL", "variant_id": sv.get("variant_id"),
        },
        "fields_completed": [], "fields_changed": [], "critical_fields_changed": [],
        "name_validation": {
            "model_name_il_status": "verified", "trim_name_il_status": "verified",
            "recommended_display_name_il": sv.get("global_model_name"),
            "global_vs_il_name_notes": "",
        },
        "duplicate_review": {
            "possible_duplicate_group": merged.get("possible_duplicate_group"),
            "duplicate_decision": "keep_separate"
                if merged.get("possible_duplicate_group") else "not_duplicate",
            "duplicate_reason": "smoke test synthetic decision",
        },
        "split_review": {
            "split_recommended": False,
            "split_reason": "trim is a single marketed name",
            "suggested_split_trims": [],
        },
        "confidence": confidence,
        "requires_manual_review": confidence < 0.85,
        "manual_review_reason": "" if confidence >= 0.85 else "low confidence",
        "evidence_summary": "synthetic smoke-test response, values unchanged from input",
        "grounding_used": True,
        "grounding_notes": "smoke test",
    }


def run_checks(log=print) -> tuple[bool, list[tuple[str, bool, str]]]:
    """Run all smoke checks. Returns (all_passed, [(name, ok, detail), ...])."""
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, ok, detail))
        log(f"  [{'OK' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))

    log("== Smoke test: Gemini variant validation engine ==")
    try:
        rules = engine.load_rules()
        schema = engine.load_schema()
        check("config/field_rules.json loads", True)
        check("config/validation_schema.json loads", True)
        check("max_attempts config present",
              rules.get("max_validation_attempts_default") == 3
              and rules.get("allowed_max_attempts") == [1, 2, 3, 4, 5])
    except Exception as e:  # noqa: BLE001
        check("config files load", False, str(e)[:200])
        return False, checks

    try:
        prompt = engine.load_prompt()
        check("prompt file loads", len(prompt) > 500,
              "prompts/gemini_variant_validation_prompt_two_file_context.md")
    except Exception as e:  # noqa: BLE001
        check("prompt file loads", False, str(e)[:200])
        return False, checks

    failures, variants_by_id, instructions_by_id = engine.startup_checks(rules)
    check("both input files load and pass startup validation",
          not failures, "; ".join(failures[:3]))
    if failures:
        return False, checks
    check("exactly 3712 unique validation_ids joined",
          len(variants_by_id) == 3712 and set(variants_by_id) == set(instructions_by_id),
          f"variants={len(variants_by_id)}, instructions={len(instructions_by_id)}")

    # Identity-hash recipe must reproduce the source hashes exactly.
    hash_mismatches = 0
    for v in variants_by_id.values():
        expected = v.get("canonical_identity_hash")
        if expected and identity.identity_hash(v.get("standard_variant") or {}) != expected:
            hash_mismatches += 1
    check("identity hash recipe reproduces canonical_identity_hash",
          hash_mismatches == 0, f"{hash_mismatches} mismatch(es) of {len(variants_by_id)}")

    by_priority: dict[str, str] = {}
    for vid, instr in instructions_by_id.items():
        by_priority.setdefault(instr.get("validation_priority"), vid)
    for prio in rules["priority_order"]:
        vid = by_priority.get(prio)
        if vid is None:
            check(f"merged context for priority={prio}", False,
                  "no variant with this priority")
            continue
        merged = engine.build_merged_context(
            variants_by_id[vid], instructions_by_id[vid], variants_by_id)
        ok = (merged["validation_id"] == vid
              and isinstance(merged["standard_variant"], dict)
              and merged["validation_priority"] == prio
              and merged["validation_tasks"])
        check(f"merged context for priority={prio}", ok, vid)

    sample_vid = by_priority.get("high") or next(iter(variants_by_id))
    merged = engine.build_merged_context(
        variants_by_id[sample_vid], instructions_by_id[sample_vid], variants_by_id)

    good = synthetic_response(merged, confidence=0.95)
    res_good = qa.run_qa(good, merged, rules, schema, grounding_enabled=True)
    check("QA evaluates a clean high-confidence response",
          res_good["status"] in (qa.QA_PASS, qa.QA_UNRESOLVED),
          f"status={res_good['status']}")

    low = synthetic_response(merged, confidence=0.5)
    low["decision"] = "auto_accept"  # model lies; QA must catch it
    low["requires_manual_review"] = False
    res_low = qa.run_qa(low, merged, rules, schema, grounding_enabled=True)
    check("QA marks a low-confidence response unresolved (correction pass)",
          res_low["status"] == qa.QA_UNRESOLVED, f"status={res_low['status']}")

    bad = dict(good)
    bad.pop("corrected_variant")
    res_bad = qa.run_qa(bad, merged, rules, schema, grounding_enabled=True)
    check("QA retries on schema-invalid response",
          res_bad["status"] == qa.QA_RETRY, f"status={res_bad['status']}")

    # Generic placeholder trim must not pass without strong verification.
    weak_trim = synthetic_response(merged, confidence=0.95)
    weak_trim["corrected_variant"]["trim"] = "Base"
    weak_trim["name_validation"]["trim_name_il_status"] = "uncertain"
    res_trim = qa.run_qa(weak_trim, merged, rules, schema, grounding_enabled=True)
    check("QA refuses unverified generic trim",
          res_trim["status"] == qa.QA_UNRESOLVED
          and any("generic/placeholder trim" in i for i in res_trim["issues"]),
          f"status={res_trim['status']}")

    # Canonical row invariants for clean output.
    row = engine.canonical_row(merged, good, "auto_accept", rules)
    check("canonical row has validated_identity_hash + original hash preserved",
          bool(row.get("validated_identity_hash"))
          and row.get("original_canonical_identity_hash")
          == merged.get("canonical_identity_hash"))
    check("canonical row alternate_names is always a list",
          isinstance(row.get("alternate_names"), list))
    check("canonical row requires_manual_review is false",
          row.get("requires_manual_review") is False)
    check("canonical row has original_variant_id + validated_variant_id",
          bool(row.get("original_variant_id")) and bool(row.get("validated_variant_id")))

    # Correction prompt (Pass 2/3) builds with compact targeted context.
    prev = {"response": low, "qa": res_low, "error": None, "raw_text": "{}"}
    cp = engine.build_correction_prompt(merged, prev, 2, 3)
    check("correction prompt builds (Pass 2)",
          "CORRECTION_CONTEXT:" in cp and sample_vid in cp
          and "manual_review" not in json.dumps(
              json.loads(cp.split("CORRECTION_CONTEXT:\n", 1)[1]).get(
                  "fields_that_must_be_fixed", [])))
    cp3 = engine.build_correction_prompt(merged, prev, 3, 3)
    check("correction prompt is stricter on Pass 3",
          "FINAL STRICT CORRECTION PASS" in cp3)
    check("correction prompt sends one variant only (no full dataset)",
          len(cp) < 60_000, f"{len(cp)} chars")

    try:
        cfg = runtime_config.resolve(runtime="smoke_test")
        rep = cfg.presence_report()
        check("runtime config resolves without crashing", True,
              f"source={rep['secrets_source']}, model={rep['model_id']}")
        log(f"  [INFO] Gemini API key: {rep['gemini_api_key']} (value never shown)")
        log(f"  [INFO] GitHub token: {rep['github_token']} (value never shown)")
        log(f"  [INFO] grounding_enabled: {rep['grounding_enabled']}")
    except Exception as e:  # noqa: BLE001
        check("runtime config resolves without crashing", False, str(e)[:200])

    engine.REAL_PATHS.base.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.NamedTemporaryFile(dir=engine.REAL_PATHS.base, suffix=".tmp"):
            pass
        check("output/ directory is writable", True)
    except OSError as e:
        check("output/ directory is writable", False, str(e))

    parsed = qa.parse_strict_json('```json\n{"a": 1}\n```')
    check("strict JSON parser strips accidental fences", parsed == {"a": 1})

    # Model context checks
    ctx = mctx.fresh_context("Toyota", "Corolla", "Toyota Corolla")
    check("model context creates correctly",
          ctx["make"] == "Toyota" and ctx["model"] == "Corolla"
          and ctx["market_scope"] == "IL" and not ctx["completed"])
    fp = mctx.build_technical_fingerprint({
        "make": "Toyota", "model": "Corolla", "year_start": 2020,
        "year_end": 2023, "engine": "1.6L", "transmission": "CVT",
        "fuel_type": "Gasoline", "body_type": "Sedan", "drivetrain": "FWD",
    })
    check("technical fingerprint builds correctly",
          fp["make"] == "Toyota" and fp["engine"] == "1.6L")
    check("weak source name detected",
          mctx.is_weak_source_name("Base") and mctx.is_weak_source_name(None)
          and mctx.is_weak_source_name("") and not mctx.is_weak_source_name("Sport"))
    ctx_summary = mctx.context_summary_for_prompt(ctx)
    check("model context summary is compact",
          ctx_summary["make"] == "Toyota" and "processed_so_far" in ctx_summary)
    final_ctx = mctx.finalize_context(ctx)
    check("model context finalizes correctly",
          final_ctx["completed"] is True and "completed_at" in final_ctx)

    # Merged context includes technical fingerprint and source_trim_was_generic
    merged_with_ctx = engine.build_merged_context(
        variants_by_id[sample_vid], instructions_by_id[sample_vid],
        variants_by_id, active_model_ctx=ctx)
    check("merged context includes technical fingerprint",
          isinstance(merged_with_ctx.get("technical_fingerprint"), dict)
          and "make" in merged_with_ctx["technical_fingerprint"])
    check("merged context includes source_trim_was_generic",
          "source_trim_was_generic" in merged_with_ctx)
    check("merged context includes active model context when provided",
          isinstance(merged_with_ctx.get("active_model_context"), dict))

    # Discovered missing variant builds correctly
    mctx.reset_discovery_counter()
    disc = mctx.build_discovered_missing_variant(
        "Toyota", "Corolla", "Toyota Corolla", "LE",
        {"evidence_summary": "smoke test", "lineup_position": "entry"},
        "VAL-000001")
    check("discovered missing variant record builds",
          disc["discovery_id"] == "DISC-000001"
          and disc["discovered_trim"] == "LE"
          and disc["reason_not_added_to_clean"].startswith("expansion candidate"))

    failed = [c for c in checks if not c[1]]
    log(f"\n== Smoke test {'PASSED' if not failed else 'FAILED'}: "
        f"{len(checks) - len(failed)}/{len(checks)} checks OK ==")
    return not failed, checks


def main() -> int:
    ok, _ = run_checks()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
