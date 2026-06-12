#!/usr/bin/env python3
"""Gemini-based vehicle variant validation engine.

Validates 3,712 Israeli-market vehicle variants by merging, per validation_id,
the variant record from data/validation_variants_data_v1.json with the
instruction record from data/validation_instructions_by_id_v1.json, sending a
compact merged context (one variant at a time, never the full dataset) to
Gemini, then running deterministic QA on every response.

Runtimes:
  - Streamlit (main, via app.py + st.secrets)  -> run_validation(...)
  - CLI / GitHub Actions (env vars)            -> python scripts/run_gemini_validation.py

Outputs (under output/; mock mode writes to output/mock/ so real progress is
never polluted):
    validation_results.jsonl                    full audit log (incl. original_snapshot)
    canonical_variants_clean.jsonl              clean canonical rows
    manual_review.jsonl                         variants routed to manual review
    failures.jsonl                              malformed/failed responses
    push_failures.jsonl                         checkpoint push failures
    validation_progress.json                    resume state
    validation_run_summary.json                 run summary
    validation-v2-budgeted-dual-il-trims.json   final clean database (NO original_snapshot)
    canonical_vehicle_variants_clean_v1.json    compatibility copy of the final database
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import deterministic_qa as qa  # noqa: E402
import github_checkpoint  # noqa: E402
import runtime_config  # noqa: E402

DATA_DIR = REPO_ROOT / "data"
CONFIG_DIR = REPO_ROOT / "config"
PROMPTS_DIR = REPO_ROOT / "prompts"
OUTPUT_DIR = REPO_ROOT / "output"

CONFIG_FILES = {
    "field_rules": CONFIG_DIR / "field_rules.json",
    "schema": CONFIG_DIR / "validation_schema.json",
    "prompt": PROMPTS_DIR / "gemini_variant_validation_prompt_two_file_context.md",
}

SCHEMA_VERSION = "validation-v2-budgeted-dual-il-trims"
FINAL_CLEAN_FILENAME = "validation-v2-budgeted-dual-il-trims.json"


def resolve_input_file(name: str) -> Path:
    """Prefer data/<name>; fall back to repository root."""
    preferred = DATA_DIR / name
    if preferred.exists():
        return preferred
    fallback = REPO_ROOT / name
    return fallback if fallback.exists() else preferred


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


@dataclasses.dataclass
class OutputPaths:
    base: Path

    @property
    def results(self) -> Path: return self.base / "validation_results.jsonl"
    @property
    def canonical_jsonl(self) -> Path: return self.base / "canonical_variants_clean.jsonl"
    @property
    def manual_review(self) -> Path: return self.base / "manual_review.jsonl"
    @property
    def failures(self) -> Path: return self.base / "failures.jsonl"
    @property
    def push_failures(self) -> Path: return self.base / "push_failures.jsonl"
    @property
    def progress(self) -> Path: return self.base / "validation_progress.json"
    @property
    def run_summary(self) -> Path: return self.base / "validation_run_summary.json"
    @property
    def final_clean(self) -> Path: return self.base / FINAL_CLEAN_FILENAME
    @property
    def final_compat(self) -> Path: return self.base / "canonical_vehicle_variants_clean_v1.json"
    @property
    def startup_failure(self) -> Path: return self.base / "startup_failure_report.json"

    def checkpoint_paths(self) -> list[str]:
        return [self.base.relative_to(REPO_ROOT).as_posix()]


REAL_PATHS = OutputPaths(OUTPUT_DIR)
MOCK_PATHS = OutputPaths(OUTPUT_DIR / "mock")


@dataclasses.dataclass
class RunOptions:
    limit: int | None = None
    only_priority: str | None = None
    validation_id: str | None = None
    start_after: str | None = None
    dry_run: bool = False
    mock_mode: bool = False
    force_reprocess: bool = False
    resume: bool = True
    push_every: int = 1
    push_enabled: bool = True


def load_rules() -> dict:
    return json.loads(CONFIG_FILES["field_rules"].read_text(encoding="utf-8"))


def load_schema() -> dict:
    return json.loads(CONFIG_FILES["schema"].read_text(encoding="utf-8"))


def load_prompt() -> str:
    return CONFIG_FILES["prompt"].read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Startup validation
# ---------------------------------------------------------------------------

def startup_checks(rules: dict) -> tuple[list[str], dict, dict]:
    """Validate both input files. Returns (failures, variants_by_id,
    instructions_by_id). Never exits, never calls Gemini."""
    failures: list[str] = []
    variants_by_id: dict = {}
    instructions_by_id: dict = {}

    variants_file = resolve_input_file("validation_variants_data_v1.json")
    instructions_file = resolve_input_file("validation_instructions_by_id_v1.json")

    for path in (variants_file, instructions_file):
        if not path.exists():
            failures.append(f"required input file missing: {path.name} "
                            f"(looked in data/ and repository root)")
    if failures:
        return failures, {}, {}

    try:
        variants_doc = json.loads(variants_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        failures.append(f"variants file is not valid JSON: {e}")
        variants_doc = {}
    try:
        instructions_doc = json.loads(instructions_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        failures.append(f"instructions file is not valid JSON: {e}")
        instructions_doc = {}
    if failures:
        return failures, {}, {}

    variant_list = variants_doc.get("variants")
    if not isinstance(variant_list, list):
        failures.append("variants file has no 'variants' list")
    instructions_by_id = instructions_doc.get("instructions_by_validation_id")
    if not isinstance(instructions_by_id, dict):
        failures.append("instructions file has no 'instructions_by_validation_id' object")
        instructions_by_id = {}
    if failures:
        return failures, {}, instructions_by_id

    variant_ids = [v.get("validation_id") for v in variant_list]
    if len(set(variant_ids)) != len(variant_ids):
        dups = sorted({i for i in variant_ids if variant_ids.count(i) > 1})
        failures.append(f"duplicated validation_id in variants file: {dups[:10]}")
    variants_by_id = {v["validation_id"]: v for v in variant_list}

    vset, iset = set(variants_by_id), set(instructions_by_id)
    expected = rules["expected_total_variants"]
    if len(vset) != expected:
        failures.append(f"expected {expected} unique validation_id values in variants "
                        f"file, found {len(vset)}")
    if len(iset) != expected:
        failures.append(f"expected {expected} unique validation_id values in "
                        f"instructions file, found {len(iset)}")
    only_v, only_i = sorted(vset - iset), sorted(iset - vset)
    if only_v:
        failures.append(f"validation_id only in variants file: {only_v[:10]} "
                        f"({len(only_v)} total)")
    if only_i:
        failures.append(f"validation_id only in instructions file: {only_i[:10]} "
                        f"({len(only_i)} total)")

    for vid, record in variants_by_id.items():
        if not isinstance(record.get("standard_variant"), dict):
            failures.append(f"{vid}: missing standard_variant")
        if not record.get("original_snapshot") and not (
                record.get("standard_variant") or {}).get("source_basis"):
            failures.append(f"{vid}: no audit context (original_snapshot/source_basis)")
        if len(failures) > 50:
            failures.append("... aborting check loop, too many failures")
            return failures, variants_by_id, instructions_by_id

    for vid, instr in instructions_by_id.items():
        if not instr.get("validation_priority"):
            failures.append(f"{vid}: instruction record missing validation_priority")
        if not instr.get("validation_tasks"):
            failures.append(f"{vid}: instruction record missing validation_tasks")
        if len(failures) > 50:
            failures.append("... aborting check loop, too many failures")
            break

    return failures, variants_by_id, instructions_by_id


def write_startup_failure(paths: OutputPaths, failures: list[str]) -> None:
    paths.base.mkdir(parents=True, exist_ok=True)
    report = {
        "failed_at": utcnow(),
        "stage": "startup_validation",
        "checks_failed": failures,
        "gemini_called": False,
        "message": "Startup validation failed. No Gemini calls were made and the "
                   "validation run did not start.",
    }
    paths.startup_failure.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Merged context (one variant + matching instruction only — never the dataset)
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
    if len(json.dumps(summary, ensure_ascii=False)) > max_chars:
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
# Gemini clients
# ---------------------------------------------------------------------------

class GeminiClient:
    """Minimal REST client for the configured Gemini model, with a
    grounding-unsupported fallback to plain JSON mode."""

    def __init__(self, api_key: str, model_id: str, system_prompt: str,
                 rules: dict, grounding_enabled: bool = True, log=print):
        import requests
        self._requests = requests
        self.api_key = api_key
        self.model_id = model_id
        self.endpoint = (f"https://generativelanguage.googleapis.com/v1beta/models/"
                         f"{model_id}:generateContent")
        self.system_prompt = system_prompt
        self.rules = rules
        self.grounding_enabled = grounding_enabled
        self.log = log
        self.session = requests.Session()

    def _request_body(self, user_text: str, use_grounding: bool, strict_retry: bool) -> dict:
        body: dict = {
            "system_instruction": {"parts": [{"text": self.system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_text}]}],
            "generationConfig": {
                "temperature": 0.0 if strict_retry else 0.1,
                "maxOutputTokens": 8192,
            },
        }
        if use_grounding:
            body["tools"] = [{"google_search": {}}]
        else:
            # JSON mime type is only reliable without tools.
            body["generationConfig"]["responseMimeType"] = "application/json"
        return body

    @staticmethod
    def _extract_text(payload: dict) -> tuple[str, bool]:
        candidates = payload.get("candidates") or []
        if not candidates:
            raise ValueError(f"no candidates in response: {json.dumps(payload)[:500]}")
        cand = candidates[0]
        grounded = bool(cand.get("groundingMetadata"))
        parts = (cand.get("content") or {}).get("parts") or []
        text = "".join(p.get("text", "") for p in parts)
        if not text.strip():
            raise ValueError(f"empty text in candidate "
                             f"(finishReason={cand.get('finishReason')})")
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
                resp = self.session.post(
                    self.endpoint,
                    headers={"x-goog-api-key": self.api_key,
                             "Content-Type": "application/json"},
                    json=body, timeout=300)
            except self._requests.RequestException as e:
                if attempt >= max_rl:
                    raise RuntimeError(
                        f"network failure after retries: {e.__class__.__name__}") from e
                wait = base * (2 ** attempt)
                self.log(f"  network error ({e.__class__.__name__}); retrying in {wait}s")
                time.sleep(wait)
                attempt += 1
                continue

            if resp.status_code in (429, 500, 502, 503, 504):
                if attempt >= max_rl:
                    raise RuntimeError(f"Gemini API {resp.status_code} after "
                                       f"{max_rl} retries: {resp.text[:300]}")
                retry_after = resp.headers.get("retry-after")
                wait = int(retry_after) if retry_after and retry_after.isdigit() \
                    else base * (2 ** attempt)
                self.log(f"  Gemini API {resp.status_code}; backing off {wait}s "
                         f"(attempt {attempt + 1}/{max_rl})")
                time.sleep(wait)
                attempt += 1
                continue

            if resp.status_code == 400 and self.grounding_enabled and (
                    "tool" in resp.text.lower() or "search" in resp.text.lower()):
                self.log("  grounding/google_search not supported by API for this "
                         "model; disabling grounding for the rest of the run")
                self.grounding_enabled = False
                continue

            if resp.status_code != 200:
                raise RuntimeError(f"Gemini API error {resp.status_code}: "
                                   f"{resp.text[:500]}")

            return self._extract_text(resp.json())


class MockGeminiClient:
    """Deterministic offline stand-in for Gemini. Used by mock mode to test the
    full pipeline (QA, outputs, progress, resume) with zero API calls/cost."""

    grounding_enabled = True

    def __init__(self, *_args, **_kwargs):
        pass

    def generate(self, user_text: str, strict_retry: bool = False) -> tuple[str, bool]:
        ctx = json.loads(user_text.split("MERGED_CONTEXT:\n", 1)[1])
        sv = ctx["standard_variant"]
        vid = ctx["validation_id"]
        # Deterministic variety: every 3rd variant simulates low confidence.
        low = int(vid.rsplit("-", 1)[-1]) % 3 == 2 if vid[-1].isdigit() else False
        conf = 0.55 if low else 0.93
        cv = {k: sv.get(k) for k in (
            "make", "model", "global_model_name", "official_marketed_name_il",
            "local_brand_name_il", "rebadged_as", "year_start", "year_end",
            "generation", "body_type", "seats", "engine", "transmission",
            "fuel_type", "drivetrain", "trim", "variant_id")}
        cv["alternate_names"] = sv.get("alternate_names") or []
        cv["market_scope"] = "IL"
        resp = {
            "validation_id": vid,
            "decision": "auto_accept" if conf >= 0.85 else "manual_review",
            "is_real_variant": True,
            "is_relevant_to_il_market": True,
            "corrected_variant": cv,
            "fields_completed": [], "fields_changed": [], "critical_fields_changed": [],
            "name_validation": {
                "model_name_il_status": "verified", "trim_name_il_status": "verified",
                "recommended_display_name_il": sv.get("global_model_name"),
                "global_vs_il_name_notes": "mock mode"},
            "duplicate_review": {
                "possible_duplicate_group": ctx.get("possible_duplicate_group"),
                "duplicate_decision": "keep_separate"
                    if ctx.get("possible_duplicate_group") else "not_applicable",
                "duplicate_reason": "mock mode"},
            "split_review": {"split_recommended": False,
                             "split_reason": "mock mode: treated as single marketed name",
                             "suggested_split_trims": []},
            "confidence": conf,
            "requires_manual_review": conf < 0.85,
            "manual_review_reason": "" if conf >= 0.85 else "mock low confidence",
            "evidence_summary": "MOCK RESPONSE - no real validation evidence; "
                                "values copied from existing record",
            "grounding_used": False,
            "grounding_notes": "mock mode, no grounding performed",
        }
        return json.dumps(resp, ensure_ascii=False), False


def build_user_prompt(merged_context: dict, strict_retry: bool) -> str:
    header = (
        "Validate the following Israeli-market vehicle variant. "
        "Follow every rule in the system instructions. "
        "Return STRICT JSON only, exactly in the required schema.\n"
    )
    if strict_retry:
        header += (
            "\nIMPORTANT: your previous answer was malformed or failed deterministic "
            "QA. Return ONLY one valid JSON object matching the required schema "
            "exactly: no markdown, no code fences, no commentary, all required keys "
            "present, validation_id copied exactly from the input.\n"
        )
    return header + "\nMERGED_CONTEXT:\n" + json.dumps(
        merged_context, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------------------
# Outputs / progress
# ---------------------------------------------------------------------------

def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def canonical_row(merged_context: dict, response: dict | None, decision: str,
                  rules: dict) -> dict:
    """One clean canonical row (no original_snapshot, no legacy fields)."""
    sv = merged_context["standard_variant"]
    cv = (response or {}).get("corrected_variant") or {}

    def pick(field: str) -> Any:
        val = cv.get(field)
        if qa.is_missing_value(val, rules):
            val = sv.get(field)
        return None if qa.is_missing_value(val, rules) else val

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


def fresh_progress() -> dict:
    return {
        "run_started_at": utcnow(),
        "last_updated_at": None,
        "last_processed_validation_id": None,
        "processed": {},  # validation_id -> decision
        "counts": {"accepted": 0, "manual_review": 0, "rejected": 0, "failed": 0},
        "grounding_enabled": None,
    }


def load_progress(paths: OutputPaths) -> dict:
    if paths.progress.exists():
        try:
            return json.loads(paths.progress.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return fresh_progress()


def save_progress(paths: OutputPaths, progress: dict) -> None:
    progress["last_updated_at"] = utcnow()
    paths.base.mkdir(parents=True, exist_ok=True)
    tmp = paths.progress.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(paths.progress)


def rebuild_final_clean_files(paths: OutputPaths, progress: dict, rules: dict,
                              grounding_enabled: bool, cfg=None,
                              runtime: str = "cli") -> dict:
    """Rebuild the final clean database from canonical_variants_clean.jsonl
    (last record wins per validation_id). No original_snapshot inside."""
    latest: dict[str, dict] = {}
    if paths.canonical_jsonl.exists():
        with paths.canonical_jsonl.open(encoding="utf-8") as f:
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
            "data/validation_variants_data_v1.json",
            "data/validation_instructions_by_id_v1.json",
        ],
        "validator_model": getattr(cfg, "model_id", runtime_config.DEFAULT_MODEL_ID),
        "runtime": runtime,
        "target_branch": getattr(cfg, "target_branch",
                                 runtime_config.DEFAULT_TARGET_BRANCH),
        "grounding_enabled": grounding_enabled,
        "total_input_variants": rules["expected_total_variants"],
        "accepted_count": counts["accepted"],
        "manual_review_count": counts["manual_review"],
        "rejected_count": counts["rejected"],
        "failed_count": counts["failed"],
        "variants": [latest[k] for k in sorted(latest)],
    }
    text = json.dumps(doc, ensure_ascii=False, indent=1)
    paths.base.mkdir(parents=True, exist_ok=True)
    paths.final_clean.write_text(text, encoding="utf-8")
    paths.final_compat.write_text(text, encoding="utf-8")
    return doc


def write_run_summary(paths: OutputPaths, progress: dict, rules: dict,
                      grounding_enabled: bool, run_info: dict, cfg=None,
                      runtime: str = "cli") -> None:
    counts = progress["counts"]
    summary = {
        "schema_version": SCHEMA_VERSION,
        "updated_at": utcnow(),
        "validator_model": getattr(cfg, "model_id", runtime_config.DEFAULT_MODEL_ID),
        "runtime": runtime,
        "target_branch": getattr(cfg, "target_branch",
                                 runtime_config.DEFAULT_TARGET_BRANCH),
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
    paths.run_summary.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Per-variant processing
# ---------------------------------------------------------------------------

def process_variant(client, merged_context: dict, rules: dict, schema: dict,
                    log=print) -> dict:
    """Process one variant. Returns
    {"decision", "response", "qa", "raw_text", "attempts", "error"}."""
    vid = merged_context["validation_id"]
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
# Main run loop (reusable from Streamlit and CLI)
# ---------------------------------------------------------------------------

def select_pending(variants_by_id: dict, instructions_by_id: dict, rules: dict,
                   options: RunOptions, progress: dict) -> list[str]:
    priority_rank = {p: i for i, p in enumerate(rules["priority_order"])}
    ordered = sorted(
        variants_by_id,
        key=lambda vid: (
            priority_rank.get(instructions_by_id[vid].get("validation_priority"), 99),
            variants_by_id[vid].get("variant_sequence", 0),
        ),
    )
    if options.only_priority:
        ordered = [v for v in ordered
                   if instructions_by_id[v].get("validation_priority") == options.only_priority]
    if options.validation_id:
        ordered = [options.validation_id] if options.validation_id in variants_by_id else []
    if options.start_after and options.start_after in ordered:
        ordered = ordered[ordered.index(options.start_after) + 1:]
    pending = [v for v in ordered
               if options.force_reprocess or v not in progress["processed"]]
    if options.limit is not None:
        pending = pending[: options.limit]
    return pending


def run_validation(options: RunOptions, cfg: runtime_config.RuntimeConfig | None = None,
                   log: Callable[[str], None] = print,
                   progress_callback: Callable[[dict], None] | None = None) -> dict:
    """Run validation. Returns a result dict; never calls Gemini in dry-run or
    mock mode. Saves all output after EVERY variant; resumable at any point."""
    cfg = cfg or runtime_config.resolve()
    runtime = cfg.runtime
    paths = MOCK_PATHS if options.mock_mode else REAL_PATHS
    paths.base.mkdir(parents=True, exist_ok=True)

    rules = load_rules()
    schema = load_schema()

    failures, variants_by_id, instructions_by_id = startup_checks(rules)
    if failures:
        write_startup_failure(paths, failures)
        log(f"STARTUP VALIDATION FAILED ({len(failures)} issue(s)); "
            f"report: {paths.startup_failure}")
        return {"status": "startup_failed", "failures": failures,
                "processed_this_run": 0}

    log(f"Startup validation passed: {len(variants_by_id)} variants joined with "
        f"{len(instructions_by_id)} instruction records.")

    progress = load_progress(paths) if options.resume else fresh_progress()
    pending = select_pending(variants_by_id, instructions_by_id, rules, options, progress)
    total_expected = rules["expected_total_variants"]
    mode = "mock" if options.mock_mode else ("dry-run" if options.dry_run else "REAL")
    log(f"Selected {len(pending)} variant(s) to process [{mode}] "
        f"(already completed: {len(progress['processed'])}/{total_expected}, "
        f"force_reprocess={options.force_reprocess}, push_every={options.push_every})")

    if options.dry_run:
        for i, vid in enumerate(pending, 1):
            merged = build_merged_context(variants_by_id[vid],
                                          instructions_by_id[vid], variants_by_id)
            log(f"[{i}/{len(pending)}] {vid} dry-run: context built "
                f"({len(json.dumps(merged, ensure_ascii=False))} chars), "
                f"priority={merged['validation_priority']}, "
                f"tasks={merged['validation_tasks']}")
        log("Dry run complete; no Gemini calls were made and no outputs were written.")
        return {"status": "dry_run_ok", "processed_this_run": len(pending)}

    if options.mock_mode:
        client = MockGeminiClient()
        log("MOCK MODE: using offline mock client; outputs go to output/mock/ "
            "so real progress is untouched. No Gemini calls, no cost.")
    else:
        if not cfg.gemini_key_present:
            failures = ["Gemini API key is not configured "
                        "(st.secrets [google].api_key or env GEMINI_API_KEY)"]
            write_startup_failure(paths, failures)
            log("ERROR: Gemini API key missing. Wrote startup failure report; "
                "real run blocked.")
            return {"status": "blocked_no_api_key", "failures": failures,
                    "processed_this_run": 0}
        client = GeminiClient(cfg.gemini_api_key, cfg.model_id, load_prompt(),
                              rules, grounding_enabled=cfg.grounding_enabled, log=log)

    run_info = {
        "runtime": runtime, "mode": mode, "limit": options.limit,
        "only_priority": options.only_priority, "validation_id": options.validation_id,
        "force_reprocess": options.force_reprocess, "push_every": options.push_every,
        "selected_count": len(pending),
    }
    push_results: list[dict] = []
    since_checkpoint = 0
    processed_this_run = 0
    grounding_enabled = client.grounding_enabled

    def do_checkpoint(final: bool = False) -> None:
        n_done = len(progress["processed"])
        if final and n_done >= total_expected:
            message = f"validation complete: processed {total_expected}/{total_expected} variants"
        else:
            message = f"validation checkpoint: processed {n_done}/{total_expected} variants"
        if not options.push_enabled:
            log(f"[checkpoint] push disabled; skipping ('{message}')")
            return
        result = github_checkpoint.checkpoint(
            message, paths.checkpoint_paths(), cfg, REPO_ROOT,
            push_failures_file=paths.push_failures, log=log)
        push_results.append(result)

    try:
        for i, vid in enumerate(pending, 1):
            variant = variants_by_id[vid]
            instruction = instructions_by_id[vid]
            merged_context = build_merged_context(variant, instruction, variants_by_id)
            priority = instruction.get("validation_priority")
            log(f"[{i}/{len(pending)}] {vid} (priority={priority})")

            result = process_variant(client, merged_context, rules, schema, log=log)
            decision = result["decision"]
            response = result["response"]
            grounding_enabled = client.grounding_enabled

            # 1) Full audit record (the ONLY place original_snapshot is kept).
            append_jsonl(paths.results, {
                "validation_id": vid,
                "processed_at": utcnow(),
                "runtime": runtime,
                "mode": mode,
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
                append_jsonl(paths.canonical_jsonl,
                             canonical_row(merged_context, response, decision, rules))

            # 3) Routing files.
            if decision == "manual_review":
                append_jsonl(paths.manual_review, {
                    "validation_id": vid,
                    "processed_at": utcnow(),
                    "reasons": (result["qa"] or {}).get("issues") or [result["error"]],
                    "manual_review_reason": (response or {}).get("manual_review_reason"),
                    "confidence": (response or {}).get("confidence"),
                    "gemini_response": response,
                })
            elif decision in ("failed", "reject"):
                append_jsonl(paths.failures, {
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
                    progress["counts"][prev_key] = max(
                        0, progress["counts"][prev_key] - 1)
            progress["processed"][vid] = decision
            progress["counts"][count_key] += 1
            progress["last_processed_validation_id"] = vid
            progress["grounding_enabled"] = grounding_enabled
            save_progress(paths, progress)
            rebuild_final_clean_files(paths, progress, rules, grounding_enabled,
                                      cfg=cfg, runtime=runtime)
            write_run_summary(paths, progress, rules, grounding_enabled, run_info,
                              cfg=cfg, runtime=runtime)
            processed_this_run += 1

            log(f"  -> {decision} (confidence={(response or {}).get('confidence')}, "
                f"attempts={result['attempts']})")
            if progress_callback:
                progress_callback({
                    "index": i, "total": len(pending), "validation_id": vid,
                    "decision": decision, "counts": dict(progress["counts"]),
                    "processed_total": len(progress["processed"]),
                })

            # 5) Checkpoint commit/push.
            since_checkpoint += 1
            if since_checkpoint >= max(1, options.push_every):
                do_checkpoint()
                since_checkpoint = 0
    except (Exception, KeyboardInterrupt) as e:
        # Progress is already saved per-variant; record the interruption safely.
        save_progress(paths, progress)
        write_run_summary(paths, progress, rules, grounding_enabled, run_info,
                          cfg=cfg, runtime=runtime)
        log(f"Run interrupted after {processed_this_run} variant(s): "
            f"{e.__class__.__name__}. Progress saved; run is resumable.")
        if not isinstance(e, KeyboardInterrupt):
            raise
        return {"status": "interrupted", "processed_this_run": processed_this_run,
                "counts": progress["counts"]}

    if since_checkpoint > 0 or processed_this_run > 0:
        do_checkpoint(final=True)

    counts = progress["counts"]
    n_done = len(progress["processed"])
    log(f"Run finished: processed={n_done}/{total_expected} "
        f"accepted={counts['accepted']} manual_review={counts['manual_review']} "
        f"rejected={counts['rejected']} failed={counts['failed']} "
        f"grounding_enabled={grounding_enabled}")
    failed_pushes = [r for r in push_results if r.get("push_failure")]
    return {
        "status": "ok",
        "processed_this_run": processed_this_run,
        "processed_total": n_done,
        "total_expected": total_expected,
        "counts": dict(counts),
        "grounding_enabled": grounding_enabled,
        "push_results": push_results,
        "push_failures": len(failed_pushes),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Gemini vehicle variant validation engine")
    p.add_argument("--limit", type=int, default=None,
                   help="max number of variants to process this run (default: all)")
    p.add_argument("--only-priority", choices=["high", "medium", "low", "sample_only"],
                   default=None)
    p.add_argument("--validation-id", default=None)
    p.add_argument("--start-after", default=None)
    p.add_argument("--dry-run", action="store_true",
                   help="build contexts and ordering without calling Gemini")
    p.add_argument("--mock", action="store_true",
                   help="offline mock validation into output/mock/ (no Gemini calls)")
    p.add_argument("--no-resume", action="store_true")
    p.add_argument("--push-every", type=int,
                   default=int(os.environ.get("PUSH_EVERY_N_VARIANTS", "25")))
    p.add_argument("--no-push", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    options = RunOptions(
        limit=args.limit,
        only_priority=args.only_priority,
        validation_id=args.validation_id,
        start_after=args.start_after,
        dry_run=args.dry_run,
        mock_mode=args.mock,
        force_reprocess=os.environ.get("FORCE_REPROCESS", "false").strip().lower() == "true",
        resume=not args.no_resume,
        push_every=args.push_every,
        push_enabled=not args.no_push,
    )
    cfg = runtime_config.resolve(runtime="cli")
    result = run_validation(options, cfg=cfg)
    if result["status"] in ("startup_failed", "blocked_no_api_key"):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
