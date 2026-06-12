#!/usr/bin/env python3
"""Gemini-based vehicle variant validation engine.

Validates 3,712 Israeli-market vehicle variants by merging, per validation_id,
the variant record from data/validation_variants_data_v1.json with the
instruction record from data/validation_instructions_by_id_v1.json, sending a
compact merged context (one variant at a time, never the full dataset) to
Gemini, then running deterministic QA on every response.

There is NO human manual review. Every validation_id stays in the active
processing loop until it reaches exactly one final machine decision:

    auto_accept          Pass 1 passed deterministic QA + confidence threshold
    auto_resolved        a correction pass (Pass 2..max_attempts) resolved it
    rejected_from_clean  could not be safely resolved after max_attempts
    failed               API/runtime failure after retries

Pass 2/3 do NOT repeat the full generic prompt: they receive a compact
targeted correction context (previous response + deterministic QA failures +
exact unresolved reasons). Deterministic QA always overrides Gemini
confidence.

Runtimes:
  - Streamlit (main, via app.py + st.secrets)  -> run_validation(...)
  - CLI / GitHub Actions (env vars)            -> python scripts/run_gemini_validation.py

Outputs (under output/; mock mode writes to output/mock/ so real progress is
never polluted):
    validation_results.jsonl                    full audit log, one record per
                                                attempt (incl. original_snapshot
                                                on attempt 1)
    canonical_variants_clean.jsonl              clean canonical rows
                                                (auto_accept / auto_resolved only)
    rejected_from_clean.jsonl                   audit-only: why a record was
                                                excluded from the clean database
    failures.jsonl                              API/runtime failures
    push_failures.jsonl                         checkpoint push failures
    validation_progress.json                    resume state + per-id attempts
    validation_run_summary.json                 run summary
    validation-v2-budgeted-dual-il-trims.json   final clean database
                                                (auto_accept/auto_resolved ONLY,
                                                NO original_snapshot)
    canonical_vehicle_variants_clean_v1.json    identical compatibility copy

output/manual_review.jsonl is a deprecated legacy file: nothing writes to it
and no logic depends on it.
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
import evidence_normalizer as enorm  # noqa: E402
import github_checkpoint  # noqa: E402
import identity  # noqa: E402
import model_context as mctx  # noqa: E402
import openai_adjudicator as adjudicator  # noqa: E402
import runtime_config  # noqa: E402

DATA_DIR = REPO_ROOT / "data"
CONFIG_DIR = REPO_ROOT / "config"
PROMPTS_DIR = REPO_ROOT / "prompts"
OUTPUT_DIR = REPO_ROOT / "output"

CONFIG_FILES = {
    "field_rules": CONFIG_DIR / "field_rules.json",
    "schema": CONFIG_DIR / "validation_schema.json",
    "prompt": PROMPTS_DIR / "gemini_variant_validation_prompt_two_file_context.md",
    "research_prompt": PROMPTS_DIR / "gemini_research_prompt.md",
}

SCHEMA_VERSION = "validation-v2-budgeted-dual-il-trims"
FINAL_CLEAN_FILENAME = "validation-v2-budgeted-dual-il-trims.json"

# The only allowed final machine decisions.
FINAL_DECISIONS = ("auto_accept", "auto_resolved", "rejected_from_clean",
                   "split_required", "failed")
CLEAN_DECISIONS = ("auto_accept", "auto_resolved")
DECISION_COUNT_KEY = {
    "auto_accept": "accepted",
    "auto_resolved": "auto_resolved",
    "rejected_from_clean": "rejected_from_clean",
    "split_required": "split_required",
    "failed": "failed",
}

PROGRESS_FORMAT_VERSION = 2


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
    def rejected(self) -> Path: return self.base / "rejected_from_clean.jsonl"
    @property
    def manual_review(self) -> Path:
        # Deprecated legacy file: kept only so old runs remain readable.
        return self.base / "manual_review.jsonl"
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
    @property
    def active_model_context(self) -> Path: return self.base / "active_model_context.json"
    @property
    def discovered_missing(self) -> Path: return self.base / "discovered_missing_variants.jsonl"
    @property
    def split_required(self) -> Path: return self.base / "split_required.jsonl"
    @property
    def model_runs(self) -> Path: return self.base / "model_runs"

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
    max_attempts: int = 3


def load_rules() -> dict:
    return json.loads(CONFIG_FILES["field_rules"].read_text(encoding="utf-8"))


def load_schema() -> dict:
    return json.loads(CONFIG_FILES["schema"].read_text(encoding="utf-8"))


def load_prompt() -> str:
    return CONFIG_FILES["prompt"].read_text(encoding="utf-8")


def load_research_prompt() -> str:
    return CONFIG_FILES["research_prompt"].read_text(encoding="utf-8")


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


def build_merged_context(variant: dict, instruction: dict, variants_by_id: dict,
                         active_model_ctx: dict | None = None) -> dict:
    sv = variant.get("standard_variant") or {}
    fingerprint = mctx.build_technical_fingerprint(sv)
    source_trim_weak = mctx.is_weak_source_name(sv.get("trim"))
    ctx = {
        "validation_id": variant["validation_id"],
        "standard_variant": sv,
        "technical_fingerprint": fingerprint,
        "source_trim_was_generic": source_trim_weak,
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
    if active_model_ctx is not None:
        ctx["active_model_context"] = mctx.context_summary_for_prompt(active_model_ctx)
    return ctx


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
    full multi-pass pipeline (QA, correction passes, outputs, progress, resume)
    with zero API calls/cost.

    Deterministic behavior by the numeric part of validation_id:
      idx % 3 == 2  -> Pass 1 simulates low confidence (goes to Pass 2)
      idx % 9 == 8  -> correction passes also stay low (ends rejected_from_clean)
      otherwise     -> Pass 2 resolves it (ends auto_resolved)
    """

    grounding_enabled = True

    def __init__(self, *_args, **_kwargs):
        pass

    @staticmethod
    def _vid_index(vid: str) -> int:
        digits = "".join(c for c in vid if c.isdigit())
        return int(digits) if digits else 0

    @staticmethod
    def _extract_marker_json(user_text: str, marker: str) -> dict | None:
        """Return JSON after a prompt marker, or None when the marker is absent.

        Mock mode supports multiple prompt shapes (full validation, correction,
        and research). Missing markers should be handled explicitly instead of
        crashing with IndexError from split(...)[1].
        """
        prefix = f"{marker}:\n"
        if prefix not in user_text:
            return None
        return json.loads(user_text.split(prefix, 1)[1])

    def _response(self, vid: str, sv: dict, confidence: float,
                  resolved_note: str = "") -> str:
        accept = confidence >= 0.85
        cv = {k: sv.get(k) for k in (
            "make", "model", "global_model_name", "official_marketed_name_il",
            "local_brand_name_il", "rebadged_as", "year_start", "year_end",
            "generation", "body_type", "seats", "engine", "transmission",
            "fuel_type", "drivetrain", "trim", "variant_id")}
        cv["alternate_names"] = sv.get("alternate_names") or []
        cv["market_scope"] = "IL"
        resp = {
            "validation_id": vid,
            "decision": "auto_accept" if accept else "manual_review",
            "is_real_variant": True,
            "is_relevant_to_il_market": True,
            "corrected_variant": cv,
            "fields_completed": [], "fields_changed": [], "critical_fields_changed": [],
            "name_validation": {
                "model_name_il_status": "verified", "trim_name_il_status": "verified",
                "recommended_display_name_il": sv.get("global_model_name"),
                "global_vs_il_name_notes": "mock mode"},
            "duplicate_review": {
                "possible_duplicate_group": None,
                "duplicate_decision": "keep_separate",
                "duplicate_reason": "mock mode"},
            "split_review": {"split_recommended": False,
                             "split_reason": "mock mode: treated as single marketed name",
                             "suggested_split_trims": []},
            "confidence": confidence,
            "requires_manual_review": not accept,
            "manual_review_reason": "" if accept else "mock low confidence",
            "evidence_summary": ("MOCK RESPONSE - no real validation evidence; "
                                 "values copied from existing record. " + resolved_note),
            "grounding_used": False,
            "grounding_notes": "mock mode, no grounding performed",
            "source_trim_was_generic": False,
            "model_context_used": False,
            "model_context_updated": False,
            "technical_fingerprint_used": True,
            "selected_verified_trim": sv.get("trim"),
            "selected_trim_lineup_position": "unknown",
            "selected_trim_unique_differentiator": None,
            "known_competing_trims": [],
            "rejected_possible_trims": [],
            "discovered_missing_variants": [],
            "correction_reason": None,
            "evidence_strength": "weak",
            "safe_to_auto_resolve": accept,
            "recovery_used": bool(resolved_note),
        }
        return json.dumps(resp, ensure_ascii=False)

    def _research_response(self, ctx: dict) -> str:
        vid = ctx.get("validation_id") or "MOCK-RESEARCH"
        trim = ctx.get("trim") or ctx.get("official_marketed_name_il")
        evidence_summary = (
            "mock research: no external calls; values copied from research context")
        if trim:
            evidence_summary += f" for trim {trim}"
        resp = {
            "validation_id": vid,
            "research_status": "complete",
            "research_summary": evidence_summary,
            "queries_used": [
                "mock mode research",
                "Israeli-market vehicle variant validation",
            ],
            "source_ladder_coverage": {
                "official_importer_checked": False,
                "price_list_or_brochure_checked": False,
                "israeli_auto_sites_checked": False,
                "used_listings_checked_as_weak_support": False,
                "non_israeli_sources_checked_for_technical_only": False,
            },
            "evidence_items": [],
            "possible_israeli_trims_found": [],
            "model_family_findings": {
                "is_model_family": False,
                "family_name": None,
                "reason": "mock mode did not perform model-family research",
            },
            "technical_fingerprint_findings": {
                "engine": ctx.get("engine"),
                "transmission": ctx.get("transmission"),
                "fuel_type": ctx.get("fuel_type"),
                "drivetrain": ctx.get("drivetrain"),
                "body_type": ctx.get("body_type"),
                "year_range": f"{ctx.get('year_start')}-{ctx.get('year_end')}",
                "supported_by_sources": [],
            },
            "split_indicators": {
                "split_likely": False,
                "reason": "mock mode found no split indicators",
                "candidate_child_variants": [],
            },
            "unique_mapping_candidate": {
                "exists": bool(trim),
                "trim_name": trim,
                "official_marketed_name": ctx.get("official_marketed_name_il"),
                "confidence": 0.5 if trim else 0.0,
                "supporting_sources": [],
                "reason": "mock mode only reflects supplied research context",
            },
            "conflicts": [],
            "missing_information": [],
            "researcher_recommended_next_action": "send_to_adjudicator",
        }
        return json.dumps(resp, ensure_ascii=False)

    def generate(self, user_text: str, strict_retry: bool = False) -> tuple[str, bool]:
        correction_ctx = self._extract_marker_json(user_text, "CORRECTION_CONTEXT")
        if correction_ctx is not None:
            vid = correction_ctx["validation_id"]
            sv = correction_ctx["original_standard_variant"]
            idx = self._vid_index(vid)
            if idx % 9 == 8:
                return self._response(vid, sv, 0.6,
                                      "mock: still unresolvable on purpose"), False
            return self._response(vid, sv, 0.92,
                                  "mock: correction pass resolved the issue"), False

        research_ctx = self._extract_marker_json(user_text, "RESEARCH_CONTEXT")
        if research_ctx is not None:
            return self._research_response(research_ctx), False

        ctx = self._extract_marker_json(user_text, "MERGED_CONTEXT")
        if ctx is None:
            raise ValueError(
                "mock Gemini prompt missing one of CORRECTION_CONTEXT, "
                "RESEARCH_CONTEXT, or MERGED_CONTEXT")

        vid = ctx["validation_id"]
        sv = ctx["standard_variant"]
        idx = self._vid_index(vid)
        low = idx % 3 == 2
        resp = self._response(vid, sv, 0.55 if low else 0.93)
        if not low and ctx.get("possible_duplicate_group"):
            parsed = json.loads(resp)
            parsed["duplicate_review"]["possible_duplicate_group"] = \
                ctx["possible_duplicate_group"]
            resp = json.dumps(parsed, ensure_ascii=False)
        return resp, False


# ---------------------------------------------------------------------------
# Prompts (Pass 1 = full validation; Pass 2/3 = compact targeted correction)
# ---------------------------------------------------------------------------

def build_user_prompt(merged_context: dict, strict_retry: bool = False) -> str:
    header = (
        "Validate the following Israeli-market vehicle variant. "
        "Follow every rule in the system instructions. "
        "Return STRICT JSON only, exactly in the required schema.\n"
    )
    if merged_context.get("source_trim_was_generic"):
        header += (
            "\nIMPORTANT: The source trim/name for this variant is WEAK or GENERIC. "
            "Do NOT treat the source trim as authoritative. "
            "Identify the correct official Israeli marketed trim/variant by matching "
            "the technical fingerprint (engine, transmission, fuel_type, drivetrain, "
            "body_type, year range) to known Israeli-market trims for this model. "
            "If exactly one official Israeli trim matches, replace the weak source "
            "trim with the official name. If multiple trims could match, report "
            "ambiguity — do NOT guess.\n"
        )
    if merged_context.get("active_model_context"):
        header += (
            "\nACTIVE MODEL CONTEXT (trims already known/processed for this model):\n"
            + json.dumps(merged_context["active_model_context"],
                         ensure_ascii=False, separators=(",", ":"))
            + "\nMatch against this context first before searching wider.\n"
        )
    header += (
        "\nIn your response, also include these metadata fields at the top level:\n"
        "  source_trim_was_generic: true/false\n"
        "  model_context_used: true/false\n"
        "  model_context_updated: true/false\n"
        "  technical_fingerprint_used: true/false\n"
        "  selected_verified_trim: string or null\n"
        "  selected_trim_lineup_position: entry/mid/high/performance/special_edition/unknown\n"
        "  selected_trim_unique_differentiator: string or null\n"
        "  known_competing_trims: [] list of other trims for the same model\n"
        "  rejected_possible_trims: [] list of trims considered but rejected\n"
        "  discovered_missing_variants: [] list of {trim, evidence_summary, "
        "lineup_position, unique_differentiator} for IL trims found but not in source\n"
        "  correction_reason: string or null\n"
        "  evidence_strength: weak/moderate/strong/verified\n"
        "  safe_to_auto_resolve: true/false\n"
        "  recovery_used: true/false\n"
    )
    return header + "\nMERGED_CONTEXT:\n" + json.dumps(
        merged_context, ensure_ascii=False, separators=(",", ":"))


def build_research_prompt(merged_context: dict, gaps: list[str] | None = None) -> str:
    """Build a user prompt for Gemini research-only pass (two-model mode).

    When *gaps* is provided, this is a targeted follow-up research pass
    focused only on the listed missing items.
    """
    sv = merged_context.get("standard_variant") or {}
    research_ctx = {
        "validation_id": merged_context["validation_id"],
        "make": sv.get("make"),
        "model": sv.get("model"),
        "trim": sv.get("trim"),
        "official_marketed_name_il": sv.get("official_marketed_name_il"),
        "year_start": sv.get("year_start"),
        "year_end": sv.get("year_end"),
        "engine": sv.get("engine"),
        "transmission": sv.get("transmission"),
        "fuel_type": sv.get("fuel_type"),
        "drivetrain": sv.get("drivetrain"),
        "body_type": sv.get("body_type"),
        "generation": sv.get("generation"),
        "seats": sv.get("seats"),
        "source_trim_was_generic": merged_context.get("source_trim_was_generic", False),
        "technical_fingerprint": merged_context.get("technical_fingerprint"),
    }
    if merged_context.get("active_model_context"):
        research_ctx["active_model_context"] = merged_context["active_model_context"]

    header = (
        "Research the following Israeli-market vehicle variant. "
        "Follow every rule in the system instructions. "
        "Return STRICT JSON only, in the research output schema.\n"
    )
    if gaps:
        header += (
            "\nThis is a TARGETED follow-up research pass. "
            "Focus ONLY on these gaps:\n"
            + json.dumps(gaps, ensure_ascii=False)
            + "\nDo not repeat previously successful research.\n"
        )
    return header + "\nRESEARCH_CONTEXT:\n" + json.dumps(
        research_ctx, ensure_ascii=False, separators=(",", ":"))

def build_correction_prompt(merged_context: dict, previous: dict,
                            attempt_number: int, max_attempts: int) -> str:
    """Compact targeted prompt for Pass 2/3. Sends only this variant's
    context + the previous output + the exact deterministic QA failures —
    never the full dataset, never the full generic validation prompt."""
    prev_response = previous.get("response")
    prev_qa = previous.get("qa") or {}
    unresolved = list(prev_qa.get("issues") or [])
    if previous.get("error"):
        unresolved.append(previous["error"])

    correction_context = {
        "validation_id": merged_context["validation_id"],
        "attempt_number": attempt_number,
        "max_attempts": max_attempts,
        "original_standard_variant": merged_context["standard_variant"],
        "original_variant_id": merged_context.get("original_variant_id"),
        "original_canonical_identity_hash": merged_context.get("canonical_identity_hash"),
        "possible_duplicate_group": merged_context.get("possible_duplicate_group"),
        "duplicate_group_records": merged_context.get("duplicate_group_records") or [],
        "technical_fingerprint": merged_context.get("technical_fingerprint"),
        "source_trim_was_generic": merged_context.get("source_trim_was_generic", False),
        "previous_model_response": prev_response,
        "previous_raw_excerpt": None if prev_response is not None
        else (previous.get("raw_text") or "")[:1500] or None,
        "deterministic_qa_status": prev_qa.get("status"),
        "deterministic_qa_failures": unresolved,
        "unresolved_reasons": unresolved,
        "fields_that_must_be_fixed": sorted({
            f for f in ("trim", "year_start", "year_end", "engine", "transmission",
                        "fuel_type", "drivetrain", "body_type", "seats", "generation",
                        "official_marketed_name_il", "local_brand_name_il",
                        "alternate_names", "market_scope")
            if any(f in reason for reason in unresolved)
        }),
    }
    if merged_context.get("active_model_context"):
        correction_context["active_model_context"] = merged_context["active_model_context"]

    strictness = ""
    if attempt_number >= 3:
        strictness = (
            "THIS IS A FINAL STRICT CORRECTION PASS. Be maximally conservative: "
            "if you cannot verify a safe correction with clear evidence, return "
            "decision \"reject\" so the record is excluded from the clean "
            "database. Do NOT guess. Do NOT invent Israeli names or trims.\n"
        )
    header = (
        f"CORRECTION PASS {attempt_number}/{max_attempts} for one Israeli-market "
        f"vehicle variant that FAILED deterministic QA.\n"
        f"{strictness}"
        "Focus ONLY on the unresolved reasons listed in "
        "deterministic_qa_failures below. Do not re-validate fields that "
        "already passed.\n"
        "You must answer with exactly ONE of these outcomes:\n"
        "  1. resolved: return decision \"auto_accept\" with a safe "
        "corrected_variant that fixes every listed issue (with evidence in "
        "evidence_summary);\n"
        "  2. keep original and accept: return decision \"auto_accept\" with "
        "the original values ONLY if you can justify that they are safe and "
        "the QA concerns do not apply (explain why in evidence_summary);\n"
        "  3. not safely resolvable: return decision \"reject\".\n"
        "NEVER return decision \"manual_review\" — there is no human review in "
        "this pipeline. An unresolved record will be excluded from the clean "
        "database.\n"
        "Return STRICT JSON only, in exactly the same response schema as the "
        "system instructions (all required keys present, validation_id copied "
        "exactly).\n"
    )
    if merged_context.get("source_trim_was_generic"):
        header += (
            "\nThe source trim is WEAK/GENERIC. Identify the correct official "
            "Israeli marketed trim by technical fingerprint matching. "
            "Do NOT accept a generic trim without strong evidence.\n"
        )
    header += (
        "\nAlso include metadata: source_trim_was_generic, model_context_used, "
        "model_context_updated, technical_fingerprint_used, selected_verified_trim, "
        "selected_trim_lineup_position, selected_trim_unique_differentiator, "
        "known_competing_trims, rejected_possible_trims, discovered_missing_variants, "
        "correction_reason, evidence_strength, safe_to_auto_resolve, recovery_used.\n"
    )
    return header + "\nCORRECTION_CONTEXT:\n" + json.dumps(
        correction_context, ensure_ascii=False, separators=(",", ":"))


def prompt_type_for_attempt(attempt_number: int) -> str:
    if attempt_number == 1:
        return "pass1_full_validation"
    if attempt_number == 2:
        return "pass2_targeted_correction"
    return f"pass{attempt_number}_strict_correction"


# ---------------------------------------------------------------------------
# Outputs / progress
# ---------------------------------------------------------------------------

def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def canonical_row(merged_context: dict, response: dict | None, decision: str,
                  rules: dict) -> dict:
    """One clean canonical row (no original_snapshot, no legacy fields).
    Only called for auto_accept / auto_resolved decisions."""
    sv = merged_context["standard_variant"]
    cv = (response or {}).get("corrected_variant") or {}

    def pick(field: str) -> Any:
        val = cv.get(field)
        if qa.is_missing_value(val, rules):
            val = sv.get(field)
        return None if qa.is_missing_value(val, rules) else val

    original_variant_id = merged_context.get("original_variant_id") or sv.get("variant_id")
    row = {
        "validation_id": merged_context["validation_id"],
        # variant_id stays the original/source ID for traceability.
        "variant_id": sv.get("variant_id") or original_variant_id,
        "original_variant_id": original_variant_id,
        "original_canonical_identity_hash": merged_context.get("canonical_identity_hash"),
    }
    for field in ("make", "model", "global_model_name", "official_marketed_name_il",
                  "local_brand_name_il", "alternate_names", "rebadged_as",
                  "year_start", "year_end", "generation", "body_type", "seats",
                  "engine", "transmission", "fuel_type", "drivetrain", "trim",
                  "market_scope"):
        row[field] = pick(field)
    if row["market_scope"] is None:
        row["market_scope"] = "IL"
    # alternate_names must always be a list ([] instead of null).
    alt = cv.get("alternate_names")
    if not isinstance(alt, list):
        alt = sv.get("alternate_names")
    row["alternate_names"] = alt if isinstance(alt, list) else []

    # Identity: preserve the original hash, generate the validated hash from
    # the validated fields (so corrected identities get a different hash).
    row["validated_identity_hash"] = identity.identity_hash(row)
    identity_changed = any(
        qa.values_differ(sv.get(f), row.get(f), rules)
        for f in identity.CRITICAL_IDENTITY_FIELDS
    ) or row["validated_identity_hash"] != row["original_canonical_identity_hash"]
    row["validated_variant_id"] = (
        identity.build_validated_variant_id(row) if identity_changed
        else (row["variant_id"] or identity.build_validated_variant_id(row))
    )

    row.update({
        "validation_decision": decision,
        "confidence": (response or {}).get("confidence"),
        "requires_manual_review": False,
        "evidence_summary": (response or {}).get("evidence_summary"),
        "grounding_used": bool((response or {}).get("grounding_used")),
    })
    # Stable field order per config.
    ordered = {f: row.get(f) for f in rules["canonical_output_fields"]}
    return ordered


def fresh_progress() -> dict:
    return {
        "progress_format_version": PROGRESS_FORMAT_VERSION,
        "run_started_at": utcnow(),
        "last_updated_at": None,
        "last_processed_validation_id": None,
        "max_attempts": None,
        # validation_id -> {status, attempt_count, last_attempt_at, last_error,
        #                   last_decision, unresolved_reasons, final_decision}
        "records": {},
        "counts": {"accepted": 0, "auto_resolved": 0,
                   "rejected_from_clean": 0, "split_required": 0, "failed": 0},
        "grounding_enabled": None,
    }


def recompute_counts(progress: dict) -> None:
    counts = {"accepted": 0, "auto_resolved": 0, "rejected_from_clean": 0,
              "split_required": 0, "failed": 0}
    for rec in progress["records"].values():
        key = DECISION_COUNT_KEY.get(rec.get("final_decision"))
        if key:
            counts[key] += 1
    progress["counts"] = counts


def migrate_progress(progress: dict) -> dict:
    """Upgrade a v1 progress file (processed/{vid: decision} + manual_review
    counts) to the v2 format. manual_review and any other non-final legacy
    decision is NOT final: those ids go back into the active processing loop."""
    if progress.get("progress_format_version") == PROGRESS_FORMAT_VERSION \
            and isinstance(progress.get("records"), dict):
        return progress

    legacy_map = {
        "auto_accept": "auto_accept",
        "auto_resolved": "auto_resolved",
        "reject": "rejected_from_clean",
        "rejected": "rejected_from_clean",
        "rejected_from_clean": "rejected_from_clean",
        "failed": "failed",
    }
    new = fresh_progress()
    new["run_started_at"] = progress.get("run_started_at") or new["run_started_at"]
    new["last_processed_validation_id"] = progress.get("last_processed_validation_id")
    new["grounding_enabled"] = progress.get("grounding_enabled")
    for vid, old_decision in (progress.get("processed") or {}).items():
        final = legacy_map.get(old_decision)
        new["records"][vid] = {
            "status": "final" if final else "pending_retry",
            "attempt_count": 1,
            "last_attempt_at": progress.get("last_updated_at"),
            "last_error": None,
            "last_decision": old_decision,
            "unresolved_reasons": [] if final else [
                f"legacy decision '{old_decision}' is no longer a final state; "
                f"will be reprocessed by the automatic multi-pass flow"],
            "final_decision": final,
        }
    recompute_counts(new)
    return new


def completed_ids(progress: dict) -> set[str]:
    return {vid for vid, rec in progress["records"].items()
            if rec.get("final_decision") in FINAL_DECISIONS}


def final_decisions(progress: dict) -> dict[str, str]:
    return {vid: rec["final_decision"] for vid, rec in progress["records"].items()
            if rec.get("final_decision") in FINAL_DECISIONS}


def load_progress(paths: OutputPaths) -> dict:
    if paths.progress.exists():
        try:
            return migrate_progress(
                json.loads(paths.progress.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            pass
    return fresh_progress()


def save_progress(paths: OutputPaths, progress: dict) -> None:
    progress["last_updated_at"] = utcnow()
    recompute_counts(progress)
    paths.base.mkdir(parents=True, exist_ok=True)
    tmp = paths.progress.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(paths.progress)


def rebuild_final_clean_files(paths: OutputPaths, progress: dict, rules: dict,
                              grounding_enabled: bool, cfg=None,
                              runtime: str = "cli") -> dict:
    """Rebuild the final clean database from canonical_variants_clean.jsonl
    (last record wins per validation_id). ONLY auto_accept / auto_resolved
    variants are included — never manual_review, unresolved_auto,
    rejected_from_clean, failed, or original_snapshot."""
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

    finals = final_decisions(progress)
    clean_rows = []
    for vid in sorted(latest):
        row = latest[vid]
        if row.get("validation_decision") not in CLEAN_DECISIONS:
            continue  # legacy manual_review/unresolved rows are never clean
        if vid in progress["records"] and finals.get(vid) not in CLEAN_DECISIONS:
            continue  # superseded by a later non-clean final decision
        clean_rows.append(row)

    accepted = sum(1 for r in clean_rows if r["validation_decision"] == "auto_accept")
    auto_resolved = sum(1 for r in clean_rows
                        if r["validation_decision"] == "auto_resolved")
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
        "total_input_variants": rules["expected_total_variants"],
        "total_clean_variants": len(clean_rows),
        "accepted_count": accepted,
        "auto_resolved_count": auto_resolved,
        "rejected_from_clean_count": counts["rejected_from_clean"],
        "failed_count": counts["failed"],
        "deprecated_manual_review_count": 0,
        "variants": clean_rows,
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
        "max_attempts": progress.get("max_attempts"),
        "total_input_variants": rules["expected_total_variants"],
        "processed_count": len(completed_ids(progress)),
        "accepted_count": counts["accepted"],
        "auto_resolved_count": counts["auto_resolved"],
        "rejected_from_clean_count": counts["rejected_from_clean"],
        "split_required_count": counts.get("split_required", 0),
        "failed_count": counts["failed"],
        "total_clean_variants": counts["accepted"] + counts["auto_resolved"],
        "deprecated_manual_review_count": 0,
        "last_processed_validation_id": progress.get("last_processed_validation_id"),
        "run_started_at": progress.get("run_started_at"),
        "run_info": run_info,
    }
    paths.run_summary.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Per-variant multi-pass processing
# ---------------------------------------------------------------------------

def _needs_adjudication(
    merged_context: dict, response: dict | None, qa_result: dict | None,
    scope: str,
) -> bool:
    """Determine whether this variant needs GPT-5.4 adjudication based on
    the configured scope."""
    if scope == "off":
        return False
    if scope == "all":
        return True
    # "all_non_trivial" (default): skip only low-risk deterministic auto_accept
    if qa_result and qa_result["status"] == qa.QA_PASS:
        # Already passed QA with no issues -> trivial accept, skip adjudication
        sv = merged_context.get("standard_variant") or {}
        trim = sv.get("trim")
        if not mctx.is_weak_source_name(trim):
            il_name = sv.get("official_marketed_name_il")
            if not mctx.is_weak_source_name(il_name):
                return False
    return True


def _run_gemini_research(
    client, merged_context: dict, gaps: list[str] | None = None,
    log=print,
) -> tuple[dict | None, str | None]:
    """Run a single Gemini research pass. Returns (pack, error)."""
    prompt = build_research_prompt(merged_context, gaps)
    try:
        raw_text, _grounded = client.generate(prompt)
        try:
            pack = qa.parse_strict_json(raw_text)
            return pack, None
        except ValueError as e:
            return None, f"Gemini research malformed JSON: {e}"
    except (RuntimeError, ValueError) as e:
        return None, f"Gemini research call failed: {e}"


def process_variant_two_model(
    gemini_client, adjudicator_client,
    merged_context: dict, rules: dict, schema: dict,
    max_attempts: int, adjudication_scope: str = "all_non_trivial",
    log=print, on_attempt: Callable[[dict], None] | None = None,
) -> dict:
    """Two-model validation flow for ONE validation_id.

    Phase 1: Gemini research pass
    Phase 2: Deterministic evidence normalization
    Phase 3: GPT-5.4 final adjudication
    Phase 4: Deterministic QA + routing

    Falls back to single-model (Gemini-only) flow when:
      - adjudication_scope is "off"
      - adjudicator_client is None
      - GPT-5.4 call fails (graceful degradation)
    """
    vid = merged_context["validation_id"]
    attempts: list[dict] = []
    last_error: str | None = None
    final_decision: str | None = None
    final_response: dict | None = None
    final_qa: dict | None = None

    # Try single-model first (Pass 1) to handle trivial accepts
    if adjudication_scope in ("off",) or adjudicator_client is None:
        return process_variant(gemini_client, merged_context, rules, schema,
                               max_attempts, log=log, on_attempt=on_attempt)

    # --- Phase 1: Gemini research pass (Pass 1 full validation first) ---
    user_prompt = build_user_prompt(merged_context)
    error: str | None = None
    response: dict | None = None
    qa_result: dict | None = None
    raw_text: str | None = None

    try:
        raw_text, grounded = gemini_client.generate(user_prompt)
        try:
            response = qa.parse_strict_json(raw_text)
        except ValueError as e:
            error = f"malformed JSON: {e}"
    except (RuntimeError, ValueError) as e:
        error = f"model call failed: {e}"
        grounded = False

    if response is not None:
        if not gemini_client.grounding_enabled:
            response["grounding_used"] = False
        elif grounded:
            response["grounding_used"] = True
        qa_result = qa.run_qa(response, merged_context, rules, schema,
                              grounding_enabled=gemini_client.grounding_enabled)

    # Check if this is a trivial accept that can skip adjudication
    if qa_result and qa_result["status"] == qa.QA_PASS:
        if not _needs_adjudication(merged_context, response, qa_result,
                                   adjudication_scope):
            final_decision = "auto_accept"
            attempt_record = {
                "validation_id": vid,
                "attempt_number": 1,
                "max_attempts": max_attempts,
                "prompt_type": "pass1_full_validation",
                "model_response": response,
                "raw_text_excerpt": None,
                "deterministic_qa_result": qa_result,
                "decision_before_retry": "auto_accept",
                "unresolved_reasons": [],
                "error": None,
                "final_decision": "auto_accept",
                "timestamp": utcnow(),
            }
            attempts.append(attempt_record)
            if on_attempt:
                on_attempt(attempt_record)
            return {
                "final_decision": "auto_accept",
                "response": response,
                "qa": qa_result,
                "attempts": attempts,
                "attempt_count": 1,
                "error": None,
            }

    # --- Run Gemini research for non-trivial cases ---
    research_pack, research_error = _run_gemini_research(
        gemini_client, merged_context, log=log)

    if research_error or research_pack is None:
        log(f"  {vid}: Gemini research failed ({research_error}); "
            f"falling back to single-model flow")
        return process_variant(gemini_client, merged_context, rules, schema,
                               max_attempts, log=log, on_attempt=on_attempt)

    # --- Phase 2: Deterministic evidence normalization ---
    research_pack = enorm.normalize_research_pack(research_pack)
    qa_warnings = enorm.generate_qa_warnings(research_pack)

    # Collect unresolved reasons from initial QA pass
    unresolved = list((qa_result or {}).get("issues") or [])
    if error:
        unresolved.append(error)

    # --- Phase 3 & 4: GPT-5.4 adjudication + deterministic routing ---
    for attempt_number in range(1, max_attempts + 1):
        try:
            adj_result = adjudicator_client.adjudicate(
                merged_context, research_pack, qa_warnings, unresolved,
                attempt_number, max_attempts,
            )
        except (RuntimeError, ValueError) as e:
            adj_error = f"adjudicator call failed: {e}"
            log(f"  {vid}: GPT-5.4 adjudication failed ({adj_error}); "
                f"falling back to single-model flow")
            return process_variant(gemini_client, merged_context, rules, schema,
                                   max_attempts, log=log, on_attempt=on_attempt)

        adj_decision = adj_result.get("final_decision")

        # Handle needs_more_grounding
        if adj_decision == "needs_more_grounding" and attempt_number < max_attempts:
            gaps = (adj_result.get("grounding_attempts") or {}).get(
                "no_source_found_for") or []
            missing = adj_result.get("adjudicator_notes", {}).get(
                "gemini_research_limitations") or []
            all_gaps = gaps + missing

            log(f"  {vid} attempt {attempt_number}/{max_attempts}: "
                f"needs_more_grounding -> running targeted Gemini research")

            new_pack, new_err = _run_gemini_research(
                gemini_client, merged_context, gaps=all_gaps or None, log=log)
            if new_pack and not new_err:
                research_pack = enorm.normalize_research_pack(new_pack)
                qa_warnings = enorm.generate_qa_warnings(research_pack)

            attempt_record = {
                "validation_id": vid,
                "attempt_number": attempt_number,
                "max_attempts": max_attempts,
                "prompt_type": f"two_model_attempt_{attempt_number}",
                "model_response": response,
                "raw_text_excerpt": None,
                "deterministic_qa_result": qa_result,
                "adjudicator_result": adj_result,
                "decision_before_retry": "needs_more_grounding",
                "unresolved_reasons": all_gaps,
                "error": None,
                "final_decision": None,
                "timestamp": utcnow(),
            }
            attempts.append(attempt_record)
            if on_attempt:
                on_attempt(attempt_record)
            continue

        # Map to final engine decision
        if adj_decision == "needs_more_grounding":
            # Attempts exhausted
            final_decision = "rejected_from_clean"
            last_error = "grounding_exhausted"
        elif adj_decision in ("auto_resolved", "split_required",
                              "rejected_from_clean"):
            final_decision = adj_decision
        else:
            final_decision = "rejected_from_clean"

        attempt_record = {
            "validation_id": vid,
            "attempt_number": attempt_number,
            "max_attempts": max_attempts,
            "prompt_type": f"two_model_attempt_{attempt_number}",
            "model_response": response,
            "raw_text_excerpt": None,
            "deterministic_qa_result": qa_result,
            "adjudicator_result": adj_result,
            "decision_before_retry": adj_decision,
            "unresolved_reasons": (
                list((adj_result.get("grounding_attempts") or {}).get(
                    "no_source_found_for") or [])
            ),
            "error": last_error,
            "final_decision": final_decision,
            "timestamp": utcnow(),
        }
        attempts.append(attempt_record)
        if on_attempt:
            on_attempt(attempt_record)
        final_response = response
        final_qa = qa_result
        break

    if final_decision is None:
        final_decision = "failed"
        last_error = "no final decision reached"

    return {
        "final_decision": final_decision,
        "response": final_response,
        "qa": final_qa,
        "attempts": attempts,
        "attempt_count": len(attempts),
        "error": last_error,
        "adjudicator_result": (
            attempts[-1].get("adjudicator_result") if attempts else None
        ),
    }


def process_variant(client, merged_context: dict, rules: dict, schema: dict,
                    max_attempts: int, log=print,
                    on_attempt: Callable[[dict], None] | None = None) -> dict:
    """Run the full automatic multi-pass flow for ONE validation_id until it
    reaches a final machine decision. Returns
    {"final_decision", "response", "qa", "attempts", "attempt_count", "error"}.

    Pass 1 uses the full validation prompt. Any unresolved / QA-failed /
    low-confidence outcome immediately triggers the next correction pass
    (compact targeted prompt) for the same validation_id — there is no
    manual-review queue and no backlog.
    """
    vid = merged_context["validation_id"]
    attempts: list[dict] = []
    previous: dict = {}
    had_qa_evaluated_response = False
    last_error: str | None = None
    final_decision: str | None = None
    final_response: dict | None = None
    final_qa: dict | None = None

    for attempt_number in range(1, max_attempts + 1):
        prompt_type = prompt_type_for_attempt(attempt_number)
        if attempt_number == 1:
            user_prompt = build_user_prompt(merged_context)
        else:
            user_prompt = build_correction_prompt(merged_context, previous,
                                                  attempt_number, max_attempts)

        error: str | None = None
        response: dict | None = None
        qa_result: dict | None = None
        raw_text: str | None = None
        try:
            raw_text, grounded = client.generate(user_prompt,
                                                 strict_retry=attempt_number > 1)
            try:
                response = qa.parse_strict_json(raw_text)
            except ValueError as e:
                error = f"malformed JSON: {e}"
        except (RuntimeError, ValueError) as e:
            error = f"model call failed: {e}"
            grounded = False

        if response is not None:
            # Transport-level grounding signal overrides model claims when absent.
            if not client.grounding_enabled:
                response["grounding_used"] = False
            elif grounded:
                response["grounding_used"] = True
            qa_result = qa.run_qa(response, merged_context, rules, schema,
                                  grounding_enabled=client.grounding_enabled)
            if qa_result["status"] in (qa.QA_PASS, qa.QA_UNRESOLVED, qa.QA_REJECT):
                had_qa_evaluated_response = True

        if qa_result is not None and qa_result["status"] == qa.QA_PASS:
            final_decision = "auto_accept" if attempt_number == 1 else "auto_resolved"
        elif qa_result is not None and qa_result["status"] == qa.QA_REJECT:
            final_decision = "rejected_from_clean"

        unresolved_reasons = list((qa_result or {}).get("issues") or [])
        if error:
            unresolved_reasons.append(error)
        if error:
            decision_before_retry = "error"
        elif final_decision:
            decision_before_retry = final_decision
        elif qa_result and qa_result["status"] == qa.QA_RETRY:
            decision_before_retry = "schema_invalid_retry"
        else:
            decision_before_retry = "unresolved"

        # Last allowed attempt and still no safe resolution: finalize NOW so
        # the audit record carries the final decision. API/runtime failure on
        # the last attempt -> failed; QA-evaluated but unsafe -> rejected.
        if final_decision is None and attempt_number == max_attempts:
            if error and error.startswith("model call failed"):
                final_decision = "failed"
            elif had_qa_evaluated_response:
                final_decision = "rejected_from_clean"
            else:
                final_decision = "failed"

        attempt_record = {
            "validation_id": vid,
            "attempt_number": attempt_number,
            "max_attempts": max_attempts,
            "prompt_type": prompt_type,
            "model_response": response,
            "raw_text_excerpt": None if response is not None
            else (raw_text or "")[:2000] or None,
            "deterministic_qa_result": qa_result,
            "decision_before_retry": decision_before_retry,
            "unresolved_reasons": unresolved_reasons,
            "error": error,
            "final_decision": final_decision,
            "timestamp": utcnow(),
        }
        attempts.append(attempt_record)
        if on_attempt:
            on_attempt(attempt_record)

        if final_decision:
            final_response, final_qa = response, qa_result
            if final_decision in ("rejected_from_clean", "failed"):
                last_error = error or (f"not safely resolvable after "
                                       f"{attempt_number} attempt(s): "
                                       f"{unresolved_reasons[:3]}")
            break

        last_error = error or (f"unresolved after {prompt_type}: "
                               f"{unresolved_reasons[:3]}")
        log(f"  {vid} attempt {attempt_number}/{max_attempts} "
            f"({prompt_type}): {decision_before_retry} -> "
            f"{'next correction pass' if attempt_number < max_attempts else 'attempts exhausted'}"
            + (f" | {unresolved_reasons[:2]}" if unresolved_reasons else ""))
        previous = {"response": response, "raw_text": raw_text,
                    "qa": qa_result, "error": error}

    return {
        "final_decision": final_decision,
        "response": final_response,
        "qa": final_qa,
        "attempts": attempts,
        "attempt_count": len(attempts),
        "error": last_error if final_decision in ("rejected_from_clean", "failed")
        else None,
    }


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
    done = completed_ids(progress)
    pending = [v for v in ordered if options.force_reprocess or v not in done]
    if options.limit is not None:
        pending = pending[: options.limit]
    return pending


def select_pending_by_model(
    variants_by_id: dict,
    instructions_by_id: dict,
    rules: dict,
    options: RunOptions,
    progress: dict,
) -> list[tuple[tuple[str, str], list[str]]]:
    """Group pending variants by (make, model) while preserving priority order.

    Returns [(make_model_key, [vid, ...]), ...] in priority-then-model order.
    """
    pending = select_pending(variants_by_id, instructions_by_id, rules, options, progress)
    # Group by make/model preserving the original priority order
    groups: dict[tuple[str, str], list[str]] = {}
    for vid in pending:
        sv = (variants_by_id[vid].get("standard_variant") or {})
        key = ((sv.get("make") or "").strip(), (sv.get("model") or "").strip())
        groups.setdefault(key, []).append(vid)
    # Return in the order of first-seen model
    seen: list[tuple[str, str]] = []
    for vid in pending:
        sv = (variants_by_id[vid].get("standard_variant") or {})
        key = ((sv.get("make") or "").strip(), (sv.get("model") or "").strip())
        if key not in seen:
            seen.append(key)
    return [(key, groups[key]) for key in seen]


def _write_model_run_summary(run_dir: Path, make: str, model: str,
                              model_ctx: dict, model_stats: dict) -> None:
    """Write model_run_summary.json for a completed model."""
    run_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "make": make,
        "model": model,
        "completed_at": model_ctx.get("completed_at"),
        "total_variants": model_ctx["processed_model_variants_count"],
        "resolved_count": len(model_ctx["already_resolved_variants"]),
        "rejected_count": len(model_ctx["already_rejected_variants"]),
        "known_trims": model_ctx["known_or_candidate_israeli_trims"],
        "official_marketed_names": model_ctx["official_marketed_names_found"],
        "source_quality_warnings_count": len(model_ctx["source_quality_warnings"]),
        "ambiguous_fingerprints_count": len(model_ctx["ambiguous_fingerprints"]),
        **model_stats,
    }
    (run_dir / "model_run_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def run_validation(options: RunOptions, cfg: runtime_config.RuntimeConfig | None = None,
                   log: Callable[[str], None] = print,
                   progress_callback: Callable[[dict], None] | None = None) -> dict:
    """Run validation with per-model context. Returns a result dict; never
    calls Gemini in dry-run or mock mode. Saves all output after EVERY
    variant; resumable at any point.

    Processing order: variants are grouped by (make, model). For each model
    a temporary active context is maintained, finalized to audit, and then
    cleared before the next model starts.
    """
    cfg = cfg or runtime_config.resolve()
    runtime = cfg.runtime
    paths = MOCK_PATHS if options.mock_mode else REAL_PATHS
    paths.base.mkdir(parents=True, exist_ok=True)

    rules = load_rules()
    schema = load_schema()
    max_attempts = max(1, int(options.max_attempts
                              or rules["max_validation_attempts_default"]))

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
    progress["max_attempts"] = max_attempts

    # Group pending variants by model
    model_groups = select_pending_by_model(
        variants_by_id, instructions_by_id, rules, options, progress)
    pending_flat = [vid for _, vids in model_groups for vid in vids]
    total_pending = len(pending_flat)
    total_expected = rules["expected_total_variants"]
    mode = "mock" if options.mock_mode else ("dry-run" if options.dry_run else "REAL")
    n_models = len(model_groups)
    log(f"Selected {total_pending} variant(s) across {n_models} model(s) [{mode}] "
        f"(already completed: {len(completed_ids(progress))}/{total_expected}, "
        f"force_reprocess={options.force_reprocess}, push_every={options.push_every}, "
        f"max_attempts={max_attempts})")

    if options.dry_run:
        global_idx = 0
        for (make, model_name), model_vids in model_groups:
            log(f"[model] {make} {model_name} — {len(model_vids)} variant(s)")
            for vid in model_vids:
                global_idx += 1
                merged = build_merged_context(variants_by_id[vid],
                                              instructions_by_id[vid], variants_by_id)
                log(f"  [{global_idx}/{total_pending}] {vid} dry-run: context built "
                    f"({len(json.dumps(merged, ensure_ascii=False))} chars), "
                    f"priority={merged['validation_priority']}, "
                    f"tasks={merged['validation_tasks']}")
        log("Dry run complete; no Gemini calls were made and no outputs were written.")
        return {"status": "dry_run_ok", "processed_this_run": total_pending}

    if options.mock_mode:
        client = MockGeminiClient()
        adj_client = adjudicator.MockAdjudicatorClient()
        log("MOCK MODE: using offline mock clients; outputs go to output/mock/ "
            "so real progress is untouched. No API calls, no cost.")
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
        # Create adjudicator client if OpenAI key is present
        if cfg.openai_key_present and cfg.adjudication_scope != "off":
            adj_client = adjudicator.OpenAIAdjudicatorClient(
                cfg.openai_api_key, cfg.openai_model_id, log=log)
            log(f"Two-model mode: Gemini researcher + GPT-5.4 adjudicator "
                f"(scope={cfg.adjudication_scope})")
        else:
            adj_client = None
            if cfg.adjudication_scope != "off":
                log("OpenAI API key missing; falling back to Gemini-only mode")
            else:
                log("Adjudication scope=off; using Gemini-only mode")

    run_info = {
        "runtime": runtime, "mode": mode, "limit": options.limit,
        "only_priority": options.only_priority, "validation_id": options.validation_id,
        "force_reprocess": options.force_reprocess, "push_every": options.push_every,
        "max_attempts": max_attempts, "selected_count": total_pending,
        "model_count": n_models,
        "two_model_enabled": adj_client is not None,
        "adjudication_scope": cfg.adjudication_scope,
    }
    push_results: list[dict] = []
    since_checkpoint = 0
    processed_this_run = 0
    grounding_enabled = client.grounding_enabled
    mctx.reset_discovery_counter()

    def do_checkpoint(final: bool = False) -> None:
        n_done = len(completed_ids(progress))
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

    global_idx = 0

    try:
        for model_idx, ((make, model_name), model_vids) in enumerate(model_groups, 1):
            # ── Start model context ──────────────────────────────────
            sv0 = (variants_by_id[model_vids[0]].get("standard_variant") or {})
            active_ctx = mctx.fresh_context(
                make, model_name,
                global_model_name=sv0.get("global_model_name"))
            mctx.save_active_context(active_ctx, paths.base)
            run_dir = mctx.model_run_dir(paths.base, make, model_name)
            run_dir.mkdir(parents=True, exist_ok=True)
            model_stats = {"clean_count": 0, "rejected_count": 0, "failed_count": 0}

            log(f"\n{'='*60}")
            log(f"[MODEL {model_idx}/{n_models}] {make} {model_name} — "
                f"{len(model_vids)} variant(s)")
            log(f"{'='*60}")

            for local_idx, vid in enumerate(model_vids, 1):
                global_idx += 1
                variant = variants_by_id[vid]
                instruction = instructions_by_id[vid]
                merged_context = build_merged_context(
                    variant, instruction, variants_by_id,
                    active_model_ctx=active_ctx)
                priority = instruction.get("validation_priority")
                log(f"[{global_idx}/{total_pending}] {vid} "
                    f"(model {local_idx}/{len(model_vids)}, priority={priority})")

                def on_attempt(attempt_record: dict,
                               _vid=vid, _variant=variant, _mc=merged_context,
                               _priority=priority, _gi=global_idx) -> None:
                    audit = {
                        "validation_id": _vid,
                        "processed_at": attempt_record["timestamp"],
                        "runtime": runtime,
                        "mode": mode,
                        "validation_priority": _priority,
                        **{k: attempt_record[k] for k in (
                            "attempt_number", "max_attempts", "prompt_type",
                            "model_response", "raw_text_excerpt",
                            "deterministic_qa_result", "decision_before_retry",
                            "unresolved_reasons", "error", "final_decision",
                            "timestamp")},
                        "grounding_enabled": client.grounding_enabled,
                    }
                    if attempt_record["attempt_number"] == 1:
                        audit["original_snapshot"] = _variant.get("original_snapshot")
                        audit["original_variant_id"] = _variant.get("original_variant_id")
                        audit["standard_variant_before"] = _mc["standard_variant"]
                    append_jsonl(paths.results, audit)
                    rec = progress["records"].setdefault(_vid, {})
                    rec.update({
                        "status": "final" if attempt_record["final_decision"]
                        else "in_progress",
                        "attempt_count": attempt_record["attempt_number"],
                        "last_attempt_at": attempt_record["timestamp"],
                        "last_error": attempt_record["error"],
                        "last_decision": attempt_record["decision_before_retry"],
                        "unresolved_reasons": attempt_record["unresolved_reasons"],
                        "final_decision": attempt_record["final_decision"],
                    })
                    if progress_callback:
                        progress_callback({
                            "index": _gi, "total": total_pending,
                            "validation_id": _vid,
                            "attempt": attempt_record["attempt_number"],
                            "max_attempts": max_attempts,
                            "decision": attempt_record["decision_before_retry"],
                            "counts": dict(progress["counts"]),
                        })

                result = process_variant_two_model(
                    client, adj_client, merged_context, rules, schema,
                    max_attempts, adjudication_scope=cfg.adjudication_scope,
                    log=log, on_attempt=on_attempt)
                decision = result["final_decision"]
                response = result["response"]
                grounding_enabled = client.grounding_enabled

                # ── Update model context ─────────────────────────────
                fingerprint = merged_context.get("technical_fingerprint") or {}
                mctx.update_context_after_variant(
                    active_ctx, vid,
                    merged_context["standard_variant"],
                    decision, response, fingerprint)

                # ── Extract discovered missing variants from response ─
                if response:
                    discovered = response.get("discovered_missing_variants") or []
                    for disc in discovered:
                        if isinstance(disc, dict) and disc.get("trim"):
                            rec = mctx.build_discovered_missing_variant(
                                make, model_name,
                                sv0.get("global_model_name"),
                                disc["trim"],
                                disc,
                                vid,
                            )
                            model_disc_path = run_dir / "discovered_missing_variants.jsonl"
                            mctx.append_discovered_missing(
                                rec, paths.discovered_missing, model_disc_path)

                # ── Routing files ─────────────────────────────────────
                if decision in CLEAN_DECISIONS:
                    crow = canonical_row(merged_context, response, decision, rules)
                    append_jsonl(paths.canonical_jsonl, crow)
                    # Also write to model-level clean
                    append_jsonl(run_dir / "clean_variants.jsonl", crow)
                    model_stats["clean_count"] += 1
                elif decision == "rejected_from_clean":
                    rej_record = {
                        "validation_id": vid,
                        "processed_at": utcnow(),
                        "final_decision": decision,
                        "attempt_count": result["attempt_count"],
                        "max_attempts": max_attempts,
                        "unresolved_reasons": (result["qa"] or {}).get("issues")
                        or result["attempts"][-1]["unresolved_reasons"],
                        "confidence": (response or {}).get("confidence"),
                        "note": "audit only: explains why this record was excluded "
                                "from the clean database after all automatic attempts",
                    }
                    append_jsonl(paths.rejected, rej_record)
                    append_jsonl(run_dir / "final_rejected_after_recovery.jsonl", rej_record)
                    model_stats["rejected_count"] += 1
                elif decision == "split_required":
                    adj_res = result.get("adjudicator_result") or {}
                    split_record = {
                        "validation_id": vid,
                        "processed_at": utcnow(),
                        "final_decision": decision,
                        "attempt_count": result["attempt_count"],
                        "max_attempts": max_attempts,
                        "make": (merged_context.get("standard_variant") or {}).get("make"),
                        "model": (merged_context.get("standard_variant") or {}).get("model"),
                        "raw_trim_name": (merged_context.get("standard_variant") or {}).get("trim"),
                        "raw_official_marketed_name_il": (
                            merged_context.get("standard_variant") or {}
                        ).get("official_marketed_name_il"),
                        "candidate_child_variants": (
                            (adj_res.get("split_review") or {}).get(
                                "candidate_child_variants") or []
                        ),
                        "possible_israeli_trims_found": (
                            adj_res.get("possible_israeli_trims_found") or []
                        ),
                        "evidence_items": adj_res.get("evidence_items") or [],
                        "final_reason": adj_res.get("final_reason") or "",
                        "final_confidence": adj_res.get("final_confidence") or 0.0,
                        "adjudicator_notes": adj_res.get("adjudicator_notes") or {},
                        "confidence": (response or {}).get("confidence"),
                    }
                    append_jsonl(paths.split_required, split_record)
                    append_jsonl(run_dir / "split_required.jsonl", split_record)
                    model_stats.setdefault("split_count", 0)
                    model_stats["split_count"] += 1
                elif decision == "failed":
                    fail_record = {
                        "validation_id": vid,
                        "processed_at": utcnow(),
                        "final_decision": decision,
                        "attempt_count": result["attempt_count"],
                        "error": result["error"],
                        "qa_issues": (result["qa"] or {}).get("issues"),
                    }
                    append_jsonl(paths.failures, fail_record)
                    model_stats["failed_count"] += 1

                # ── Progress + derived final files ────────────────────
                progress["records"][vid]["status"] = "final"
                progress["records"][vid]["final_decision"] = decision
                progress["last_processed_validation_id"] = vid
                progress["grounding_enabled"] = grounding_enabled
                save_progress(paths, progress)
                rebuild_final_clean_files(paths, progress, rules, grounding_enabled,
                                          cfg=cfg, runtime=runtime)
                write_run_summary(paths, progress, rules, grounding_enabled, run_info,
                                  cfg=cfg, runtime=runtime)
                mctx.save_active_context(active_ctx, paths.base)
                processed_this_run += 1

                log(f"  -> FINAL {decision} (confidence="
                    f"{(response or {}).get('confidence')}, "
                    f"attempts={result['attempt_count']}/{max_attempts})")
                if progress_callback:
                    progress_callback({
                        "index": global_idx, "total": total_pending,
                        "validation_id": vid, "decision": decision,
                        "counts": dict(progress["counts"]),
                        "processed_total": len(completed_ids(progress)),
                    })

                since_checkpoint += 1
                if since_checkpoint >= max(1, options.push_every):
                    do_checkpoint()
                    since_checkpoint = 0

            # ── Finalize model context ────────────────────────────────
            try:
                final_ctx = mctx.finalize_context(active_ctx)
                mctx.save_final_model_context(final_ctx, run_dir)
                _write_model_run_summary(run_dir, make, model_name,
                                         final_ctx, model_stats)
            finally:
                mctx.clear_active_context(paths.base)
            log(f"[MODEL DONE] {make} {model_name}: "
                f"clean={model_stats['clean_count']} "
                f"rejected={model_stats['rejected_count']} "
                f"split={model_stats.get('split_count', 0)} "
                f"failed={model_stats['failed_count']} — context reset")

    except (Exception, KeyboardInterrupt) as e:
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
    n_done = len(completed_ids(progress))
    log(f"Run finished: processed={n_done}/{total_expected} "
        f"accepted={counts['accepted']} auto_resolved={counts['auto_resolved']} "
        f"rejected_from_clean={counts['rejected_from_clean']} "
        f"split_required={counts.get('split_required', 0)} "
        f"failed={counts['failed']} grounding_enabled={grounding_enabled}")
    failed_pushes = [r for r in push_results if r.get("push_failure")]
    return {
        "status": "ok",
        "processed_this_run": processed_this_run,
        "processed_total": n_done,
        "total_expected": total_expected,
        "counts": dict(counts),
        "max_attempts": max_attempts,
        "grounding_enabled": grounding_enabled,
        "push_results": push_results,
        "push_failures": len(failed_pushes),
        "models_processed": n_models,
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
    p.add_argument("--max-attempts", type=int, choices=[1, 2, 3, 4, 5], default=3,
                   help="max automatic validation passes per variant (default 3)")
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
        max_attempts=args.max_attempts,
    )
    cfg = runtime_config.resolve(runtime="cli")
    result = run_validation(options, cfg=cfg)
    if result["status"] in ("startup_failed", "blocked_no_api_key"):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
