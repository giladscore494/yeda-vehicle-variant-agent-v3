# Validation Engine Discovery Report

> Generated during the mandatory discovery phase before implementing the validation engine.

---

## 1. Current Generator Entrypoints

| Entrypoint | File | Function |
|---|---|---|
| Batch runner | `engine/batch.py` | `run_batch()` |
| Single seed runner | `engine/run_seed.py` | `run_seed()` |
| Decision engine | `engine/decision.py` | `decide_seed_result()` |
| Mutation layer | `engine/apply.py` | `apply_decision()` |
| Audit layer | `engine/audit.py` | `audit_canonical()` |
| Save layer | `engine/save.py` | `save_canonical_atomic()` |
| Streamlit UI | `app.py` | Streamlit app (calls `run_batch()`) |
| Retry failed | `engine/retry_failed.py` | `retry_failed_seed()` |

**Processing flow:**
```
run_batch() → for each seed:
  → run_seed()           [LLM discovery]
  → decide_seed_result() [quality gate]
  → apply_decision()     [mutate canonical]
  → save_canonical_atomic() [atomic write + optional GitHub push]
  → reload canonical from disk
```

---

## 2. Current Output JSON Path

- **Primary:** `data/canonical/resume_package_canonical.json`
- **Backup:** `data/canonical/resume_package_backup_previous.json`
- **Runtime progress:** `data/runtime/current_run.json`
- **Config:** `core/config.py` — env var `CANONICAL_RESUME_PATH`

Also present at repo root: `resume_package_canonical.json` (convenience copy).

---

## 3. Current Schema Summary

### Root-level structure
```json
{
  "schema_version": "resume_package_v1",
  "created_at": "ISO-8601",
  "description": "...",
  "batch_state": { ... },
  "verified_variants": [ ... ],
  "partial_variants": [ ... ],
  "counts": { ... }
}
```

### Variant record fields
| Field | Type | Notes |
|---|---|---|
| `variant_id` | string | Deterministic slug identifier |
| `make` | string | Normalized title case |
| `model` | string | Cleaned text |
| `aliases` | array[string] | Alternative names |
| `year_start` | `{value, used_in_compare}` | |
| `year_end` | `{value, used_in_compare}` | |
| `market` | string | "IL", "EU", "US", "GLOBAL" |
| `generation` | `{value, used_in_compare}` | |
| `body_type` | VerifiedField | |
| `seats` | VerifiedField or null | |
| `engine` | VerifiedField | |
| `transmission` | VerifiedField | |
| `fuel_type` | VerifiedField | |
| `drivetrain` | VerifiedField | |
| `trim` | VerifiedField | |
| `doors` | VerifiedField or null | |
| `trim_options` | array[{value, source_ids, status, sources_count}] | |
| `official_marketed_name_il` | string or null | |
| `market_scope` | string | "IL-confirmed", "IL-likely", "global-reference-only" |
| `source_basis` | string | Evidence description |
| `source_ids` | array[string] | Real source reference IDs |
| `confidence_level` | string | "high", "medium", "low" |
| `identity_confidence` | string | "candidate_verified", "candidate_unverified", etc. |
| `verification_status` | string | "verified" or "partial" |
| `confidence` | string | "high", "medium", "low" |
| `sources_count` | integer | |
| `created_at` | ISO-8601 | |
| `updated_at` | ISO-8601 | |
| `notes` | array[string] | |
| `candidate_raw` | object | Original LLM response data |

### VerifiedField structure
```json
{
  "value": "string",
  "status": "verified|partial",
  "confidence": "high|medium|low",
  "sources_count": integer,
  "source_ids": ["..."],
  "used_in_compare": boolean,
  "reason": "verified from N source(s)"
}
```

---

## 4. Current Variant Storage Path Inside JSON

Variants are stored in two separate root-level arrays:
- `canonical["verified_variants"]` — 788 variants with `verification_status="verified"`
- `canonical["partial_variants"]` — 2,924 variants with `verification_status="partial"`

Combined access via `engine/state.py::get_all_variants()`.

Total: 3,712 variants across 94 makes and 987 models.

---

## 5. variant_id Generation Logic

**File:** `core/variant_id.py::generate_variant_id()`

**Fields used (in order):**
1. make
2. model
3. year_start
4. year_end
5. market
6. generation (default: "unknown_generation")
7. engine (default: "unknown_engine")
8. transmission (default: "unknown_transmission")
9. body_type (default: "unknown_body")
10. fuel_type (default: "unknown_fuel")

**Algorithm:**
1. Join all fields with underscore
2. NFKD unicode normalize → ASCII encode → lowercase
3. Replace non-alphanumeric with underscore
4. Collapse multiple underscores
5. Strip leading/trailing underscores

**Deterministic:** Yes — same inputs always produce the same ID.

---

## 6. GitHub Write Mechanism

**File:** `storage/github_canonical_store.py::push_canonical()`

- Uses GitHub REST API: `PUT /repos/{owner}/{repo}/contents/{path}`
- Fetches existing file SHA before update
- Base64-encodes JSON content
- Sends with commit message, branch, and SHA
- Called from `engine/save.py::save_canonical_atomic()` when `push_to_github=True`

**Auth:** `Authorization: ****** header (token from config).

---

## 7. Streamlit Secrets / Env Vars Used

| Variable | Purpose | Default |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini API key | — |
| `GEMINI_MODEL_FAST` | Fast model ID | `gemini-3.1-pro-preview` |
| `GEMINI_MODEL_STRONG` | Strong model ID | `gemini-3.1-pro-preview` |
| `GITHUB_TOKEN` | GitHub PAT | — |
| `GITHUB_REPO` | Repo full name | `giladscore494/yeda-vehicle-variant-agent-v3` |
| `GITHUB_BRANCH` | Target branch | `main` |
| `CANONICAL_RESUME_PATH` | Canonical JSON path | `data/canonical/resume_package_canonical.json` |
| `CANONICAL_BACKUP_PATH` | Backup JSON path | `data/canonical/resume_package_backup_previous.json` |
| `RUNTIME_STATE_PATH` | Runtime state path | `data/runtime/current_run.json` |

**Loading order:** env vars first → `secrets.py` fallback → defaults.

---

## 8. Fields That Must Be Preserved

All existing variant fields must be preserved in the validated output:
- `variant_id` (must not be regenerated)
- All VerifiedField objects (body_type, engine, trim, etc.)
- `source_ids`, `source_basis`, `market_scope`
- `candidate_raw` (original LLM response)
- `created_at`, `updated_at`
- `trim_options`, `official_marketed_name_il`
- `notes`, `aliases`

---

## 9. Current Normalization Behavior

**File:** `core/normalize.py`

| Field | Normalization |
|---|---|
| make | `clean_text().title()` |
| model | `clean_text()` only |
| body_type | Pattern-matched to `BodyType` enum |
| fuel_type | Pattern-matched to `FuelType` enum |
| transmission | Pattern-matched to `Transmission` enum |
| drivetrain | Pattern-matched to canonical codes (AWD/FWD/RWD/4WD) |
| trim | No centralized normalization; stored as-is |

---

## 10. Current Retry/Resume Behavior

**State:** `batch_state` inside canonical JSON with cursor-based resume.

| Field | Purpose |
|---|---|
| `processed_seed_ids` | Fully resolved seeds |
| `manual_review_seed_ids` | Require human intervention |
| `failed_seed_ids` | Transient failures waiting retry |
| `next_seed_id` | Next seed to process |
| `last_completed_seed_id` | Last completed seed |
| `seed_accounting` | Per-seed status/resolution details |

**Resume:** `run_batch()` starts from `next_seed_id`, skips already-processed seeds.
**Retry:** `retry_failed_seed()` re-runs failed seeds without advancing cursor.

---

## 11. Risks Before Implementation

1. **Trim data has no centralized normalization** — validation must handle raw trim values.
2. **3,712 variants** — model calls must be budgeted carefully via grouping.
3. **VerifiedField objects** are nested — validation metadata must wrap without breaking consumers.
4. **Existing audit.py has hard gates** — new code must not interfere with production save flow.
5. **No OpenAI dependency exists** — must add `openai` to requirements.
6. **`secrets.py` pattern** — must extend config without breaking existing loader.
7. **GitHub push targets main by default** — validation must override to target branch.

---

## 12. Validation Engine Integration Plan

### Approach
- Read existing canonical JSON as read-only input
- Build validation as a separate pipeline that does NOT modify the production save flow
- Reuse `core/variant_id.py`, `core/normalize.py`, `core/schemas.py`
- Reuse `storage/github_canonical_store.py::push_canonical()` for GitHub writes (with branch override)
- Add new `engine/config.py` for validation-specific config
- Add new `engine/validation/` package for all validation logic

### New files
- `engine/config.py` — centralized config loader (Streamlit + env + secrets.py)
- `engine/github_writer.py` — validation-specific GitHub writer
- `engine/validation/` — normalizer, group_builder, risk_scorer, cost_tracker, etc.
- `engine/validation/providers/` — gemini_validator, openai_reviewer
- `engine/normalize_validate.py` — CLI entrypoint

### Safety guards
- Assert `output_path != input_path`
- Assert output is under `data/validated_runs/`
- Assert original input file is not modified (hash check)
- Never import or call `save_canonical_atomic()` from validation code
