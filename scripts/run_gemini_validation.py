#!/usr/bin/env python3
"""Gemini-based vehicle variant validation engine.

Validates 3,712 Israeli-market vehicle variants by merging, per validation_id,
the variant record from data/validation_variants_data_v1.json with the
instruction record from data/validation_instructions_by_id_v1.json, sending a
compact merged context to Gemini (gemini-3.1-pro-preview, grounding enabled
when supported), then running deterministic QA on every response.

Outputs (under output/):
    validation_results.jsonl                    full audit log (incl. original_snapshot)
    canonical_variants_clean.jsonl              clean canonical rows
    manual_review.jsonl                         variants routed to manual review
    failures.jsonl                              malformed/failed responses
    validation_progress.json                    resume state
    validation_run_summary.json                 run summary
    validation-v2-budgeted-dual-il-trims.json   final clean database (NO original_snapshot)
    canonical_vehicle_variants_clean_v1.json    compatibility copy of the final database

The engine never validates from one input file alone, never invents data, and
prefers manual_review over false certainty.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import signal
import sys
import time
from pathlib import Path
from typing import Any

import requests

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import deterministic_qa as qa  # noqa: E402
import github_checkpoint  # noqa: E402

DATA_DIR = REPO_ROOT / "data"
CONFIG_DIR = REPO_ROOT / "config"
PROMPTS_DIR = REPO_ROOT / "prompts"
OUTPUT_DIR = REPO_ROOT / "output"

VARIANTS_FILE = DATA_DIR / "validation_variants_data_v1.json"
INSTRUCTIONS_FILE = DATA_DIR / "validation_instructions_by_id_v1.json"
FIELD_RULES_FILE = CONFIG_DIR / "field_rules.json"
SCHEMA_FILE = CONFIG_DIR / "validation_schema.json"
PROMPT_FILE = PROMPTS_DIR / "gemini_variant_validation_prompt_two_file_context.md"

RESULTS_FILE = OUTPUT_DIR / "validation_results.jsonl"
CANONICAL_JSONL = OUTPUT_DIR / "canonical_variants_clean.jsonl"
MANUAL_REVIEW_FILE = OUTPUT_DIR / "manual_review.jsonl"
FAILURES_FILE = OUTPUT_DIR / "failures.jsonl"
PROGRESS_FILE = OUTPUT_DIR / "validation_progress.json"
RUN_SUMMARY_FILE = OUTPUT_DIR / "validation_run_summary.json"
FINAL_CLEAN_FILE = OUTPUT_DIR / "validation-v2-budgeted-dual-il-trims.json"
FINAL_COMPAT_FILE = OUTPUT_DIR / "canonical_vehicle_variants_clean_v1.json"
STARTUP_FAILURE_FILE = OUTPUT_DIR / "startup_failure_report.json"

OUTPUT_PATHS_FOR_CHECKPOINT = [str(OUTPUT_DIR.relative_to(REPO_ROOT))]

MODEL_ID = "gemini-3.1-pro-preview"
GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL_ID}:generateContent"
)
SCHEMA_VERSION = "validation-v2-budgeted-dual-il-trims"
TARGET_BRANCH = os.environ.get("TARGET_BRANCH", "validation-v2-budgeted-dual-il-trims")


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def log(msg: str) -> None:
    print(f"[{utcnow()}] {msg}", flush=True)


# ---------------------------------------------------------------------------
# Startup validation
# ---------------------------------------------------------------------------

def startup_validation(rules: dict) -> tuple[dict, dict, dict]:
    """Validate both input files before any Gemini call.

    Returns (variants_doc, variants_by_id, instructions_by_id).
    On any failure: writes output/startup_failure_report.json and exits.
    """
    failures: list[str] = []
    variants_doc: dict = {}
    variants_by_id: dict = {}
    instructions_by_id: dict = {}

    for path in (VARIANTS_FILE, INSTRUCTIONS_FILE):
        if not path.exists():
            failures.append(f"required input file missing: {path.relative_to(REPO_ROOT)}")

    if not failures:
        try:
            variants_doc = json.loads(VARIANTS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            failures.append(f"variants file is not valid JSON: {e}")
        try:
            instructions_doc = json.loads(INSTRUCTIONS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            failures.append(f"instructions file is not valid JSON: {e}")

    if not failures:
        variant_list = variants_doc.get("variants")
        if not isinstance(variant_list, list):
            failures.append("variants file has no 'variants' list")
        instructions_by_id = instructions_doc.get("instructions_by_validation_id")
        if not isinstance(instructions_by_id, dict):
            failures.append("instructions file has no 'instructions_by_validation_id' object")

    if not failures:
        variant_ids = [v.get("validation_id") for v in variant_list]
        dup_in_variants = sorted({i for i in variant_ids if variant_ids.count(i) > 1}) \
            if len(set(variant_ids)) != len(variant_ids) else []
        if dup_in_variants:
            failures.append(f"duplicated validation_id in variants file: {dup_in_variants[:10]}")
        variants_by_id = {v["validation_id"]: v for v in variant_list}

        vset, iset = set(variants_by_id), set(instructions_by_id)
        expected = rules["expected_total_variants"]
        if len(vset) != expected:
            failures.append(f"expected {expected} unique validation_id values in variants file, "
                            f"found {len(vset)}")
        if len(iset) != expected:
            failures.append(f"expected {expected} unique validation_id values in instructions "
                            f"file, found {len(iset)}")
        only_v = sorted(vset - iset)
        only_i = sorted(iset - vset)
        if only_v:
            failures.append(f"validation_id only in variants file: {only_v[:10]} "
                            f"({len(only_v)} total)")
        if only_i:
            failures.append(f"validation_id only in instructions file: {only_i[:10]} "
                            f"({len(only_i)} total)")

        for vid, record in variants_by_id.items():
            if not isinstance(record.get("standard_variant"), dict):
                failures.append(f"{vid}: missing standard_variant")
            snapshot = record.get("original_snapshot")
            basis = (record.get("standard_variant") or {}).get("source_basis")
            if not snapshot and not basis:
                failures.append(f"{vid}: no audit context (original_snapshot/source_basis)")
            if len(failures) > 50:
                failures.append("... aborting check loop, too many failures")
                break

        if len(failures) <= 50:
            for vid, instr in instructions_by_id.items():
                if not instr.get("validation_priority"):
                    failures.append(f"{vid}: instruction record missing validation_priority")
                if not instr.get("validation_tasks"):
                    failures.append(f"{vid}: instruction record missing validation_tasks")
                if len(failures) > 50:
                    failures.append("... aborting check loop, too many failures")
                    break

    if failures:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report = {
            "failed_at": utcnow(),
            "stage": "startup_validation",
            "checks_failed": failures,
            "gemini_called": False,
            "message": "Startup validation failed. No Gemini calls were made and the "
                       "validation run did not start.",
        }
        STARTUP_FAILURE_FILE.write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        log(f"STARTUP VALIDATION FAILED ({len(failures)} issue(s)). "
            f"Report: {STARTUP_FAILURE_FILE}")
        for f in failures[:20]:
            log(f"  - {f}")
        sys.exit(2)

    log(f"Startup validation passed: {len(variants_by_id)} variants joined with "
        f"{len(instructions_by_id)} instruction records.")
    return variants_doc, variants_by_id, instructions_by_id


# ---------------------------------------------------------------------------
# Merged context
# ---------------------------------------------------------------------------

def summarize_original_snapshot(snapshot: Any, max_chars: int = 4000) -> Any:
    """Compact audit summary: unwrap {'value':..,'status':..} fields, drop noise."""
    if not isinstance(snapshot, dict):
        return snapshot

    def compact(value: Any) -> Any:
        if isinstance(value, dict) and "value" in value:
            keep = {"value": value.get("value")}
            for extra in ("status", "confidence", "sources_count", "reason"):
                if value.get(extra) not in (None, "", [], {}):
                    keep[extra] = value[extra]
            return keep
        if isinstance(value, list) and len(value) > 8:
            return value[:8] + [f"... +{len(value) - 8} more"]
        return value

    skip_keys = {"source_files", "candidate_raw", "created_at", "updated_at"}
    summary = {k: compact(v) for k, v in snapshot.items() if k not in skip_keys}
    if "trim_options" in snapshot:
        summary["trim_options"] = snapshot["trim_options"]
    text = json.dumps(summary, ensure_ascii=False)
    if len(text) > max_chars:
        summary = {k: summary[k] for k in list(summary)[: max(5, len(summary) // 2)]}
        summary["_truncated"] = True
    return summary


def duplicate_group_summaries(variant: dict, variants_by_id: dict) -> list[dict]:
    group = variant.get("possible_duplicate_group")
    if not group:
        return []
    members = []
    for other in variants_by_id.values():
        if other.get("possible_duplicate_group") == group \
                and other["validation_id"] != variant["validation_id"]:
            sv = other.get("standard_variant") or {}
            members.append({
                "validation_id": other["validation_id"],
                "variant_id": sv.get("variant_id"),
                "canonical_identity_hash": other.get("canonical_identity_hash"),
                "make": sv.get("make"), "model": sv.get("model"),
                "year_start": sv.get("year_start"), "year_end": sv.get("year_end"),
                "generation": sv.get("generation"), "engine": sv.get("engine"),
                "transmission": sv.get("transmission"), "fuel_type": sv.get("fuel_type"),
                "drivetrain": sv.get("drivetrain"), "trim": sv.get("trim"),
                "body_type": sv.get("body_type"),
            })
    return members


def build_merged_context(variant: dict, instruction: dict, variants_by_id: dict) -> dict:
    sv = variant.get("standard_variant") or {}
    return {
        "validation_id": variant["validation_id"],
        "standard_variant": sv,
        "original_snapshot_summary": summarize_original_snapshot(
            variant.get("original_snapshot")),
        "original_status": variant.get("original_status"),
        "original_variant_id": variant.get("original_variant_id"),
        "schema_family": variant.get("schema_family"),
        "canonical_identity_key": variant.get("canonical_identity_key"),
        "canonical_identity_hash": variant.get("canonical_identity_hash"),
        "possible_duplicate_group": variant.get("possible_duplicate_group"),
        "is_possible_duplicate_after_mapping": variant.get(
            "is_possible_duplicate_after_mapping"),
        "duplicate_group_records": duplicate_group_summaries(variant, variants_by_id),
        "effective_missing_standard_fields": instruction.get(
            "effective_missing_standard_fields", []),
        "technical_identity_missing_fields": instruction.get(
            "technical_identity_missing_fields", []),
        "standard_completeness_score": instruction.get("standard_completeness_score"),
        "technical_identity_completeness_score": instruction.get(
            "technical_identity_completeness_score"),
        "validation_priority": instruction.get("validation_priority"),
        "ai_validation_route": instruction.get("ai_validation_route"),
        "validation_tasks": instruction.get("validation_tasks", []),
        "pre_validation_status": instruction.get("pre_validation_status"),
        "focus_fields_for_gemini": instruction.get("focus_fields_for_gemini", []),
        "required_actions": instruction.get("required_actions", []),
        "source_basis": sv.get("source_basis"),
        "field_sources": sv.get("field_sources") or {},
    }


# ---------------------------------------------------------------------------
# Gemini client
# ---------------------------------------------------------------------------

class GeminiClient:
    """Minimal REST client for gemini-3.1-pro-preview with grounding fallback."""

    def __init__(self, api_key: str, system_prompt: str, rules: dict):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.rules = rules
        self.grounding_enabled = True  # optimistic; downgraded on first hard failure
        self.session = requests.Session()

    def _request_body(self, user_text: str, use_grounding: bool, strict_retry: bool) -> dict:
        body: dict = {
            "system_instruction": {"parts": [{"text": self.system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_text}]}],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 8192,
            },
        }
        if use_grounding:
            body["tools"] = [{"google_search": {}}]
        else:
            # JSON mime type is only reliable without tools.
            body["generationConfig"]["responseMimeType"] = "application/json"
        if strict_retry:
            body["generationConfig"]["temperature"] = 0.0
        return body

    def _post(self, body: dict) -> requests.Response:
        return self.session.post(
            GEMINI_ENDPOINT,
            headers={"x-goog-api-key": self.api_key,
                     "Content-Type": "application/json"},
            json=body,
            timeout=300,
        )

    @staticmethod
    def _extract_text(payload: dict) -> tuple[str, bool]:
        candidates = payload.get("candidates") or []
        if not candidates:
            raise ValueError(f"no candidates in response: "
                             f"{json.dumps(payload)[:500]}")
        cand = candidates[0]
        grounded = bool(cand.get("groundingMetadata"))
        parts = (cand.get("content") or {}).get("parts") or []
        text = "".join(p.get("text", "") for p in parts)
        if not text.strip():
            raise ValueError(f"empty text in candidate (finishReason="
                             f"{cand.get('finishReason')})")
        return text, grounded

    def generate(self, user_text: str, strict_retry: bool = False) -> tuple[str, bool]:
        """Returns (response_text, grounding_used). Handles rate limits and the
        grounding-unsupported fallback. Raises RuntimeError on hard failure."""
        max_rl = self.rules["rate_limit_max_retries"]
        base = self.rules["rate_limit_base_backoff_seconds"]
        attempt = 0
        while True:
            body = self._request_body(user_text, self.grounding_enabled, strict_retry)
            try:
                resp = self._post(body)
            except requests.RequestException as e:
                if attempt >= max_rl:
                    raise RuntimeError(f"network failure after retries: {e}") from e
                wait = base * (2 ** attempt)
                log(f"  network error ({e.__class__.__name__}); retrying in {wait}s")
                time.sleep(wait)
                attempt += 1
                continue

            if resp.status_code in (429, 500, 502, 503, 504):
                if attempt >= max_rl:
                    raise RuntimeError(
                        f"Gemini API {resp.status_code} after {max_rl} retries: "
                        f"{resp.text[:300]}")
                retry_after = resp.headers.get("retry-after")
                wait = int(retry_after) if retry_after and retry_after.isdigit() \
                    else base * (2 ** attempt)
                log(f"  Gemini API {resp.status_code}; backing off {wait}s "
                    f"(attempt {attempt + 1}/{max_rl})")
                time.sleep(wait)
                attempt += 1
                continue

            if resp.status_code == 400 and self.grounding_enabled and (
                    "tool" in resp.text.lower() or "search" in resp.text.lower()):
                log("  grounding/google_search not supported by API for this model; "
                    "disabling grounding for the rest of the run")
                self.grounding_enabled = False
                continue

            if resp.status_code != 200:
                raise RuntimeError(f"Gemini API error {resp.status_code}: "
                                   f"{resp.text[:500]}")

            payload = resp.json()
            text, grounded = self._extract_text(payload)
            return text, grounded


def build_user_prompt(merged_context: dict, strict_retry: bool) -> str:
    header = (
        "Validate the following Israeli-market vehicle variant. "
        "Follow every rule in the system instructions. "
        "Return STRICT JSON only, exactly in the required schema.\n"
    )
    if strict_retry:
        header += (
            "\nIMPORTANT: your previous answer was malformed or failed deterministic QA. "
            "Return ONLY one valid JSON object matching the required schema exactly: "
            "no markdown, no code fences, no commentary, all required keys present, "
            "validation_id copied exactly from the input.\n"
        )
    return header + "\nMERGED_CONTEXT:\n" + json.dumps(
        merged_context, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------

def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def canonical_row(merged_context: dict, response: dict | None, decision: str,
                  rules: dict) -> dict:
    """Build one clean canonical row (no original_snapshot, no legacy fields)."""
    sv = merged_context["standard_variant"]
    cv = (response or {}).get("corrected_variant") or {}

    def pick(field: str) -> Any:
        val = cv.get(field)
        if qa.is_missing_value(val, rules):
            val = sv.get(field)
        if qa.is_missing_value(val, rules):
            return None
        return val

    row = {
        "validation_id": merged_context["validation_id"],
        "variant_id": pick("variant_id"),
        "canonical_identity_hash": merged_context.get("canonical_identity_hash"),
    }
    for field in ("make", "model", "global_model_name", "official_marketed_name_il",
                  "local_brand_name_il", "alternate_names", "rebadged_as",
                  "year_start", "year_end", "generation", "body_type", "seats",
                  "engine", "transmission", "fuel_type", "drivetrain", "trim",
                  "market_scope"):
        row[field] = pick(field)
    if row["market_scope"] is None:
        row["market_scope"] = "IL"
    row.update({
        "validation_decision": decision,
        "confidence": (response or {}).get("confidence"),
        "requires_manual_review": decision != "auto_accept",
        "evidence_summary": (response or {}).get("evidence_summary"),
        "grounding_used": bool((response or {}).get("grounding_used")),
    })
    return row


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            log("WARNING: progress file corrupt; starting fresh progress state")
    return {
        "run_started_at": utcnow(),
        "last_updated_at": None,
        "last_processed_validation_id": None,
        "processed": {},  # validation_id -> decision
        "counts": {"accepted": 0, "manual_review": 0, "rejected": 0, "failed": 0},
        "grounding_enabled": None,
    }


def save_progress(progress: dict) -> None:
    progress["last_updated_at"] = utcnow()
    tmp = PROGRESS_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(PROGRESS_FILE)


def rebuild_final_clean_files(progress: dict, rules: dict, grounding_enabled: bool) -> None:
    """Rebuild the final clean database from canonical_variants_clean.jsonl
    (last record wins per validation_id). No original_snapshot inside."""
    latest: dict[str, dict] = {}
    if CANONICAL_JSONL.exists():
        with CANONICAL_JSONL.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                latest[row["validation_id"]] = row

    counts = progress["counts"]
    doc = {
        "schema_version": SCHEMA_VERSION,
        "created_at": utcnow(),
        "source_input_files": [
            "validation_variants_data_v1.json",
            "validation_instructions_by_id_v1.json",
        ],
        "validator_model": MODEL_ID,
        "target_branch": TARGET_BRANCH,
        "grounding_enabled": grounding_enabled,
        "total_input_variants": rules["expected_total_variants"],
        "accepted_count": counts["accepted"],
        "manual_review_count": counts["manual_review"],
        "rejected_count": counts["rejected"],
        "failed_count": counts["failed"],
        "variants": [latest[k] for k in sorted(latest)],
    }
    text = json.dumps(doc, ensure_ascii=False, indent=1)
    FINAL_CLEAN_FILE.write_text(text, encoding="utf-8")
    FINAL_COMPAT_FILE.write_text(text, encoding="utf-8")


def write_run_summary(progress: dict, rules: dict, grounding_enabled: bool,
                      run_info: dict) -> None:
    counts = progress["counts"]
    summary = {
        "schema_version": SCHEMA_VERSION,
        "updated_at": utcnow(),
        "validator_model": MODEL_ID,
        "target_branch": TARGET_BRANCH,
        "grounding_enabled": grounding_enabled,
        "total_input_variants": rules["expected_total_variants"],
        "processed_count": len(progress["processed"]),
        "accepted_count": counts["accepted"],
        "manual_review_count": counts["manual_review"],
        "rejected_count": counts["rejected"],
        "failed_count": counts["failed"],
        "last_processed_validation_id": progress.get("last_processed_validation_id"),
        "run_started_at": progress.get("run_started_at"),
        "run_info": run_info,
    }
    RUN_SUMMARY_FILE.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Per-variant processing
# ---------------------------------------------------------------------------

def process_variant(client: GeminiClient | None, merged_context: dict,
                    rules: dict, schema: dict, dry_run: bool) -> dict:
    """Process one variant. Returns
    {"decision", "response", "qa", "raw_text", "attempts", "error"}."""
    vid = merged_context["validation_id"]

    if dry_run:
        return {"decision": "dry_run", "response": None, "qa": None,
                "raw_text": None, "attempts": 0, "error": None}

    max_retries = rules["max_model_retries"]
    last_error = None
    last_qa = None
    raw_text = None

    for attempt in range(1, max_retries + 1):
        strict = attempt > 1
        try:
            user_prompt = build_user_prompt(merged_context, strict_retry=strict)
            raw_text, grounded = client.generate(user_prompt, strict_retry=strict)
        except RuntimeError as e:
            last_error = f"model call failed: {e}"
            log(f"  {vid} attempt {attempt}: {last_error}")
            continue

        try:
            response = qa.parse_strict_json(raw_text)
        except ValueError as e:
            last_error = f"malformed JSON: {e}"
            log(f"  {vid} attempt {attempt}: {last_error}")
            continue

        # Transport-level grounding signal overrides model claims when absent.
        if not client.grounding_enabled:
            response["grounding_used"] = False
        elif grounded:
            response["grounding_used"] = True

        qa_result = qa.run_qa(response, merged_context, rules, schema,
                              grounding_enabled=client.grounding_enabled)
        last_qa = qa_result

        if qa_result["status"] == qa.QA_RETRY:
            last_error = f"QA retry: {qa_result['issues'][:3]}"
            log(f"  {vid} attempt {attempt}: {last_error}")
            continue

        decision = {
            qa.QA_PASS: "auto_accept",
            qa.QA_MANUAL_REVIEW: "manual_review",
            qa.QA_REJECT: "reject",
        }[qa_result["status"]]
        return {"decision": decision, "response": response, "qa": qa_result,
                "raw_text": raw_text, "attempts": attempt, "error": None}

    # Retry budget exhausted: structurally-valid-but-QA-retry responses go to
    # manual review; truly malformed/failed calls go to failures.
    if last_qa is not None and last_qa["status"] == qa.QA_RETRY:
        try:
            response = qa.parse_strict_json(raw_text)
        except (ValueError, TypeError):
            response = None
        if response is not None:
            return {"decision": "manual_review", "response": response, "qa": last_qa,
                    "raw_text": raw_text, "attempts": max_retries,
                    "error": f"retry limit reached; routed to manual review: {last_error}"}
    return {"decision": "failed", "response": None, "qa": last_qa,
            "raw_text": raw_text, "attempts": max_retries, "error": last_error}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Gemini vehicle variant validation engine")
    p.add_argument("--limit", type=int, default=None,
                   help="max number of variants to process this run (default: all)")
    p.add_argument("--only-priority", choices=["high", "medium", "low", "sample_only"],
                   default=None, help="process only one priority group")
    p.add_argument("--validation-id", default=None,
                   help="process a single validation_id")
    p.add_argument("--start-after", default=None,
                   help="skip until after this validation_id in processing order")
    p.add_argument("--dry-run", action="store_true",
                   help="build contexts and ordering without calling Gemini")
    p.add_argument("--no-resume", action="store_true",
                   help="ignore existing progress file (still does not delete outputs)")
    p.add_argument("--push-every", type=int,
                   default=int(os.environ.get("PUSH_EVERY_N_VARIANTS", "25")),
                   help="checkpoint push frequency (default 25; 1 = push every variant)")
    p.add_argument("--no-push", action="store_true",
                   help="never push (local commits only)")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rules = json.loads(FIELD_RULES_FILE.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    system_prompt = PROMPT_FILE.read_text(encoding="utf-8")

    force_reprocess = os.environ.get("FORCE_REPROCESS", "false").strip().lower() == "true"

    _, variants_by_id, instructions_by_id = startup_validation(rules)

    # Processing order: priority groups, variant_sequence inside each group.
    priority_rank = {p: i for i, p in enumerate(rules["priority_order"])}
    ordered_ids = sorted(
        variants_by_id,
        key=lambda vid: (
            priority_rank.get(instructions_by_id[vid].get("validation_priority"), 99),
            variants_by_id[vid].get("variant_sequence", 0),
        ),
    )

    if args.only_priority:
        ordered_ids = [v for v in ordered_ids
                       if instructions_by_id[v].get("validation_priority") == args.only_priority]
    if args.validation_id:
        if args.validation_id not in variants_by_id:
            log(f"ERROR: unknown validation_id {args.validation_id}")
            return 2
        ordered_ids = [args.validation_id]
    if args.start_after:
        if args.start_after in ordered_ids:
            ordered_ids = ordered_ids[ordered_ids.index(args.start_after) + 1:]
        else:
            log(f"WARNING: --start-after id {args.start_after} not in selection; ignoring")

    progress = load_progress() if not args.no_resume else {
        "run_started_at": utcnow(), "last_updated_at": None,
        "last_processed_validation_id": None, "processed": {},
        "counts": {"accepted": 0, "manual_review": 0, "rejected": 0, "failed": 0},
        "grounding_enabled": None,
    }

    pending = [v for v in ordered_ids
               if force_reprocess or v not in progress["processed"]]
    if args.limit is not None:
        pending = pending[: args.limit]

    total_expected = rules["expected_total_variants"]
    log(f"Selected {len(pending)} variant(s) to process "
        f"(already completed: {len(progress['processed'])}/{total_expected}, "
        f"force_reprocess={force_reprocess}, dry_run={args.dry_run}, "
        f"push_every={args.push_every})")

    client = None
    if not args.dry_run:
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            STARTUP_FAILURE_FILE.write_text(json.dumps({
                "failed_at": utcnow(), "stage": "startup_validation",
                "checks_failed": ["GEMINI_API_KEY is not set in the environment"],
                "gemini_called": False,
            }, ensure_ascii=False, indent=2), encoding="utf-8")
            log("ERROR: GEMINI_API_KEY not set. Wrote startup failure report; exiting.")
            return 2
        client = GeminiClient(api_key, system_prompt, rules)

    grounding_enabled = client.grounding_enabled if client else False
    run_info = {
        "limit": args.limit, "only_priority": args.only_priority,
        "validation_id": args.validation_id, "dry_run": args.dry_run,
        "force_reprocess": force_reprocess, "push_every": args.push_every,
        "selected_count": len(pending),
    }

    # Save progress on SIGTERM/SIGINT so a crash/cancel never loses results.
    def _graceful_exit(signum, frame):
        log(f"received signal {signum}; saving progress and exiting")
        save_progress(progress)
        write_run_summary(progress, rules,
                          client.grounding_enabled if client else False, run_info)
        sys.exit(130)

    signal.signal(signal.SIGTERM, _graceful_exit)
    signal.signal(signal.SIGINT, _graceful_exit)

    do_push = not args.no_push
    since_checkpoint = 0

    for i, vid in enumerate(pending, 1):
        variant = variants_by_id[vid]
        instruction = instructions_by_id[vid]
        merged_context = build_merged_context(variant, instruction, variants_by_id)
        priority = instruction.get("validation_priority")
        log(f"[{i}/{len(pending)}] {vid} (priority={priority})")

        result = process_variant(client, merged_context, rules, schema, args.dry_run)

        if args.dry_run:
            log(f"  dry-run: context built "
                f"({len(json.dumps(merged_context, ensure_ascii=False))} chars), "
                f"tasks={merged_context['validation_tasks']}")
            continue

        decision = result["decision"]
        response = result["response"]
        grounding_enabled = client.grounding_enabled

        # 1) Full audit record (the ONLY place original_snapshot is kept).
        append_jsonl(RESULTS_FILE, {
            "validation_id": vid,
            "processed_at": utcnow(),
            "validation_priority": priority,
            "decision": decision,
            "attempts": result["attempts"],
            "error": result["error"],
            "qa_issues": (result["qa"] or {}).get("issues"),
            "grounding_enabled": grounding_enabled,
            "original_snapshot": variant.get("original_snapshot"),
            "original_variant_id": variant.get("original_variant_id"),
            "standard_variant_before": merged_context["standard_variant"],
            "gemini_response": response,
        })

        # 2) Clean canonical row for accepted + manual_review variants.
        if decision in ("auto_accept", "manual_review"):
            append_jsonl(CANONICAL_JSONL,
                         canonical_row(merged_context, response, decision, rules))

        # 3) Routing files.
        if decision == "manual_review":
            append_jsonl(MANUAL_REVIEW_FILE, {
                "validation_id": vid,
                "processed_at": utcnow(),
                "reasons": (result["qa"] or {}).get("issues") or [result["error"]],
                "manual_review_reason": (response or {}).get("manual_review_reason"),
                "confidence": (response or {}).get("confidence"),
                "gemini_response": response,
            })
        elif decision in ("failed", "reject"):
            append_jsonl(FAILURES_FILE, {
                "validation_id": vid,
                "processed_at": utcnow(),
                "decision": decision,
                "error": result["error"],
                "qa_issues": (result["qa"] or {}).get("issues"),
                "raw_text_excerpt": (result["raw_text"] or "")[:2000] or None,
            })

        # 4) Progress + derived final files, saved after EVERY variant.
        count_key = {"auto_accept": "accepted", "manual_review": "manual_review",
                     "reject": "rejected", "failed": "failed"}[decision]
        prev = progress["processed"].get(vid)
        if prev is not None:
            prev_key = {"auto_accept": "accepted", "manual_review": "manual_review",
                        "reject": "rejected", "failed": "failed"}.get(prev)
            if prev_key:
                progress["counts"][prev_key] = max(0, progress["counts"][prev_key] - 1)
        progress["processed"][vid] = decision
        progress["counts"][count_key] += 1
        progress["last_processed_validation_id"] = vid
        progress["grounding_enabled"] = grounding_enabled
        save_progress(progress)
        rebuild_final_clean_files(progress, rules, grounding_enabled)
        write_run_summary(progress, rules, grounding_enabled, run_info)

        log(f"  -> {decision} "
            f"(confidence={(response or {}).get('confidence')}, "
            f"attempts={result['attempts']})")

        # 5) Checkpoint commit/push.
        since_checkpoint += 1
        if since_checkpoint >= max(1, args.push_every):
            n_done = len(progress["processed"])
            github_checkpoint.checkpoint(
                f"validation checkpoint: processed {n_done}/{total_expected} variants",
                OUTPUT_PATHS_FOR_CHECKPOINT, cwd=str(REPO_ROOT), do_push=do_push)
            since_checkpoint = 0

    if args.dry_run:
        log("Dry run complete; no Gemini calls were made and no outputs were written.")
        return 0

    n_done = len(progress["processed"])
    write_run_summary(progress, rules, grounding_enabled, run_info)
    if n_done >= total_expected:
        message = f"validation complete: processed {total_expected}/{total_expected} variants"
    else:
        message = f"validation checkpoint: processed {n_done}/{total_expected} variants"
    github_checkpoint.checkpoint(message, OUTPUT_PATHS_FOR_CHECKPOINT,
                                 cwd=str(REPO_ROOT), do_push=do_push)

    counts = progress["counts"]
    log(f"Run finished: processed={n_done}/{total_expected} "
        f"accepted={counts['accepted']} manual_review={counts['manual_review']} "
        f"rejected={counts['rejected']} failed={counts['failed']} "
        f"grounding_enabled={grounding_enabled}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
