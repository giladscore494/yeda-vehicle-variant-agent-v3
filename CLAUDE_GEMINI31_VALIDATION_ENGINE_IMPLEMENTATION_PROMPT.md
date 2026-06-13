# Claude Prompt: Build Gemini 3.1 Sampled Vehicle Variant Validation Engine

You are Claude Code working in a cleaned repository. Your task, when this prompt is used later, is to implement a new Gemini 3.1-based validation engine for Israeli-market vehicle variants. Read this document as the main implementation specification. Follow it exactly and do not reintroduce behavior from the previous over-strict validation engine.

## 1. Mission

Build a new practical Israeli-market vehicle variant validation engine.

The engine must use only Gemini 3.1 as the model. There must be:

* no GPT adjudicator
* no OpenAI dependency
* no dual-model flow
* no Streamlit app
* no old deterministic QA architecture copied from the previous engine

The goal is to validate and lightly enrich a raw Israeli vehicle variants database into one full validated JSON output file.

Input files:

* `data/validation_variants_data_v1.json`
* `data/validation_instructions_by_id_v1.json`

Output file:

* `data/validated_vehicle_variants_full_gemini31_v1.json`

The engine must preserve every original `validation_id`.

## 2. Background: Why This Engine Exists

The old engine rejected too many real Israeli-market variants because it treated exact trim verification as a hard acceptance requirement.

The old failure pattern was:

* raw trim was `Base`, `Standard`, `None`, `null`, empty, or generic
* model could not strongly verify the exact Israeli trim
* deterministic QA marked it unresolved
* adjudicator rejected it
* real Israeli-market variants were excluded from the clean database

This is wrong for a practical car-knowledge product.

The new engine must separate:

* vehicle identity confidence
* trim confidence

A weak trim does not mean the vehicle identity is invalid. A vehicle can be a real, useful, Israeli-market database entry even if its exact trim label is unresolved.

## 3. Core Principle

Acceptance depends primarily on vehicle identity confidence, not trim confidence.

Vehicle identity should be strict. Trim enrichment should be flexible.

If the vehicle identity is valid, plausible, technically consistent, and Israeli-market relevant, the row should enter the clean output even if the exact trim is unresolved.

If the trim is unresolved, the correct decision is usually `clean_partial`, not `reject`.

## 4. Important Definitions

### `clean_exact`

Use when:

* core vehicle identity is valid
* exact trim or marketed variant is strongly verified
* no important ambiguity remains

### `clean_partial`

Use when:

* core vehicle identity is valid
* vehicle is relevant to the Israeli market
* exact trim / Israeli marketed name / package / edition is unresolved or weak

`clean_partial` is a success state. It means the vehicle identity is accepted into the clean database while trim-level enrichment remains incomplete.

### `split_required`

Use when:

* one source row clearly combines multiple distinct trims or marketed variants
* the row should not be collapsed into one clean row
* the engine should provide `split_candidates`

### `reject`

Use only for true identity-level problems:

* vehicle likely did not exist
* make/model combination invalid
* impossible powertrain
* wrong or unsupported market
* contradictory year range
* mixed incompatible vehicles
* missing unrecoverable identity fields
* accepting the row would pollute the database

Never reject only because trim is weak.

## 5. Identity-Critical Fields

Treat these fields as identity-critical:

* make
* model
* engine
* transmission
* fuel_type
* drivetrain
* body_type
* year_start
* year_end
* Israeli market relevance

Problems in these fields can block acceptance. If these fields are contradictory, impossible, unsupported, or unrecoverable, the result may be `reject`.

## 6. Trim / Enrichment Fields

Treat these fields as enrichment fields, not hard rejection fields:

* trim
* trim_name
* trim_name_il
* official_marketed_name_il
* local_variant_name
* alternate_names
* edition/package names
* marketing names

Weakness or uncertainty in these fields should lower `trim_confidence`, not automatically cause rejection.

## 7. Data Loading and Join Requirements

Build the engine to:

1. Load `data/validation_variants_data_v1.json`
2. Load `data/validation_instructions_by_id_v1.json`
3. Join records by `validation_id`
4. Validate that every variant has matching instructions
5. Validate that there are no duplicate `validation_id`s
6. Preserve input order unless there is a good reason not to
7. Preserve every source `validation_id` in output

Expected scale:

* approximately 3,712 variants
* approximately 3,712 instruction records

If counts do not match, fail safely before calling Gemini. Do not call Gemini on a partial or mismatched join.

## 8. Gemini 3.1 Role

Gemini 3.1 should act as a practical Israeli-market automotive validation expert.

It should not behave like an academic research agent.

Its role:

* read the raw variant fingerprint
* read the per-ID instruction
* perform a short grounded check
* determine whether the identity is valid
* identify likely Israeli-market trims under the same model/year range
* lightly enrich fields when supported
* avoid inventing exact trim names
* return strict JSON

The engine should not ask Gemini to prove every trim perfectly.

Guide Gemini to answer sharply after a short high-quality check, similar to how a knowledgeable car expert would answer in chat.

## 9. Grounding Requirement

Grounding/search is required, but bounded.

Gemini must perform a short web-quality check, not deep research for every row.

The grounding goal is to understand:

* whether the model was sold in Israel
* relevant years in Israel
* available body types
* available engines / fuels / transmissions
* known trim levels or marketed names under the same model
* whether the row is one variant, a model-level partial variant, or a split-required row

Preferred sources:

* Israeli importer pages
* Israeli car catalog/spec pages
* Israeli used-car database/catalog pages
* manufacturer pages
* reliable automotive review/spec pages
* trusted market listings when official pages are unavailable

Grounding must be useful, but cost-controlled.

Do not require perfect trim proof to accept identity-valid rows.

## 10. Sampling, Clustering, and Caching Strategy

Do not build a system that researches all 3,712 rows independently from scratch.

The engine must group similar variants into identity clusters and reuse evidence.

Cluster key should be based on normalized:

* make
* model
* generation or year range
* engine
* fuel_type
* transmission
* drivetrain
* body_type

Suggested cluster key format:

`{make}|{model}|{year_bucket}|{engine}|{fuel_type}|{transmission}|{drivetrain}|{body_type}`

The engine should:

1. Build clusters before Gemini calls
2. Ground each unique cluster once when possible
3. Cache discovered Israeli-market evidence per cluster
4. Reuse cluster evidence for similar rows
5. Only perform a new grounding call when a row introduces a meaningfully different technical fingerprint or contradiction

The output should include:

* `grounding_cluster_id`
* `evidence_reused_from`
* `grounding_summary`
* `evidence_sources`

## 11. Cost-Control Behavior

Design the engine to minimize Gemini calls.

Required cost-control principles:

* one Gemini call per cluster where possible
* reuse evidence across same make/model/engine/year/body groups
* avoid repeated searches for identical fingerprints
* avoid multi-pass correction loops unless identity is unsafe
* no GPT adjudication
* no deep research per row
* bounded grounding
* deterministic pre-checks before model calls

The engine should be practical for thousands of variants.

## 12. Deterministic Pre-Checks

Before calling Gemini, perform lightweight deterministic checks:

* required files exist
* JSON structure is valid
* validation IDs join correctly
* duplicate IDs absent
* required identity fields exist or are recoverable
* obvious impossible values detected
* `year_start <= year_end`
* empty strings normalized to null
* trim placeholders normalized

Trim placeholders include:

* `Base`
* `Standard`
* `None`
* `null`
* empty string
* `N/A`
* `Unknown`
* generic short model names

These should be treated as unresolved trim, not automatic rejection.

## 13. Gemini Prompt Template

Embed a complete Gemini prompt template in the engine. The template must instruct Gemini to validate practical vehicle identity, avoid over-research, and return strict JSON only.

Use this template as the starting point:

```text
You are validating one Israeli-market vehicle variant for a practical car-knowledge database. This is not a deep research task. Perform a short grounded check. Decide whether the vehicle identity is real, plausible, internally consistent, and relevant to Israel. Do not reject because trim is missing, generic, or unverified. If identity is valid but trim remains unresolved, return clean_partial.

You are using Gemini 3.1 as the only model in this validation pipeline. There is no GPT adjudicator and no second model. Your output must be directly usable by the engine.

INPUT VARIANT JSON:
{{VARIANT_JSON}}

PER-ID INSTRUCTION JSON:
{{INSTRUCTION_JSON}}

REUSABLE CLUSTER EVIDENCE, IF AVAILABLE:
{{CLUSTER_EVIDENCE_JSON}}

TASK:
1. Read the variant and instruction.
2. Perform a short grounded check using web-quality evidence.
3. Determine whether the core vehicle identity is valid, plausible, internally consistent, and Israeli-market relevant.
4. Separate identity confidence from trim confidence.
5. Lightly enrich canonical fields only when supported.
6. Do not invent exact trim names or official Israeli marketed names.
7. If the vehicle identity is valid but the exact trim is missing, generic, weak, or unresolved, return clean_partial.
8. Return strict JSON only, with no Markdown, comments, or explanatory text outside the JSON object.

IDENTITY-CRITICAL FIELDS:
- make
- model
- engine
- transmission
- fuel_type
- drivetrain
- body_type
- year_start
- year_end
- Israeli market relevance

TRIM / ENRICHMENT FIELDS:
- trim
- trim_name
- trim_name_il
- official_marketed_name_il
- local_variant_name
- alternate_names
- edition/package names
- marketing names

DECISION RULES:
- clean_exact: use only when core identity is valid and exact trim or marketed variant is strongly verified.
- clean_partial: use when core identity is valid and Israeli-market relevant, but trim / Israeli marketed name / package / edition is unresolved or weak. clean_partial is a success state.
- split_required: use when one source row clearly combines multiple distinct trims or marketed variants and should not be collapsed into one clean row.
- reject: use only for true identity-level problems such as non-existent vehicle, invalid make/model, impossible powertrain, unsupported market, contradictory year range, mixed incompatible vehicles, or missing unrecoverable identity fields.

MANDATORY RULES:
1. If identity is valid and trim is missing, return clean_partial, set trim_status = unresolved, and do not reject.
2. If identity is valid and trim is generic, return clean_partial, set trim_status = unresolved, do not pretend generic trim is verified, and do not reject.
3. If identity is valid and exact Israeli marketed name is unknown, leave official_marketed_name_il null unless supported and return clean_partial.
4. If multiple trims are possible but technical identity is one usable model-level variant, return clean_partial and list candidates in possible_trim_names.
5. If one row clearly combines multiple distinct trims, return split_required and provide split_candidates.
6. If there is a real contradiction in identity, return reject.
7. Never reject solely because trim is null, None, Base, Standard, generic, cannot be strongly verified, or official marketed name is incomplete.
8. Do not force trim recovery.
9. Do not invent trim names.
10. Do not over-research.

GROUNDING RULES:
- Use bounded grounding/search.
- Prefer Israeli importer pages, Israeli car catalog/spec pages, Israeli used-car database/catalog pages, manufacturer pages, reliable automotive review/spec pages, and trusted market listings when official pages are unavailable.
- The goal is to determine practical identity validity and market relevance, not to prove every trim perfectly.
- Summarize evidence briefly in grounding_summary.
- Include source URLs or source identifiers in evidence_sources.

OUTPUT SCHEMA:
Return exactly one JSON object matching this schema. Use null for unknown values. Use arrays where arrays are required.

{
  "validation_id": "VAL-000000",
  "source_validation_id": "VAL-000000",
  "source_cluster_id": null,
  "grounding_cluster_id": null,
  "evidence_reused_from": null,

  "canonical_make": null,
  "canonical_model": null,
  "canonical_series_or_generation": null,
  "canonical_trim": null,
  "official_marketed_name_il": null,

  "body_type": null,
  "fuel_type": null,
  "engine": null,
  "transmission": null,
  "drivetrain": null,
  "year_start": null,
  "year_end": null,
  "market_scope": "IL",

  "validation_decision": "clean_exact | clean_partial | split_required | reject",
  "acceptance_tier": "exact | partial | none",

  "identity_status": "verified | likely_valid | uncertain | invalid",
  "identity_confidence": 0.0,

  "trim_status": "verified | inferred | unresolved | invalid",
  "trim_confidence": 0.0,

  "grounding_summary": "",
  "evidence_sources": [],
  "possible_trim_names": [],
  "split_candidates": [],

  "blocking_identity_issues": [],
  "non_blocking_trim_issues": [],

  "fields_changed": [],
  "fields_left_unresolved": [],

  "decision_reason": ""
}

STRICT JSON ONLY. Do not wrap the JSON in Markdown. Do not include comments. Do not include text before or after the JSON.
```

The Gemini output must be strict JSON.

## 14. Required Per-Variant Output Schema

Build toward this schema:

```json
{
  "validation_id": "VAL-000000",
  "source_validation_id": "VAL-000000",
  "source_cluster_id": null,
  "grounding_cluster_id": null,
  "evidence_reused_from": null,

  "canonical_make": null,
  "canonical_model": null,
  "canonical_series_or_generation": null,
  "canonical_trim": null,
  "official_marketed_name_il": null,

  "body_type": null,
  "fuel_type": null,
  "engine": null,
  "transmission": null,
  "drivetrain": null,
  "year_start": null,
  "year_end": null,
  "market_scope": "IL",

  "validation_decision": "clean_exact | clean_partial | split_required | reject",
  "acceptance_tier": "exact | partial | none",

  "identity_status": "verified | likely_valid | uncertain | invalid",
  "identity_confidence": 0.0,

  "trim_status": "verified | inferred | unresolved | invalid",
  "trim_confidence": 0.0,

  "grounding_summary": "",
  "evidence_sources": [],
  "possible_trim_names": [],
  "split_candidates": [],

  "blocking_identity_issues": [],
  "non_blocking_trim_issues": [],

  "fields_changed": [],
  "fields_left_unresolved": [],

  "decision_reason": ""
}
```

## 15. Top-Level Output File Schema

The final output file should be:

`data/validated_vehicle_variants_full_gemini31_v1.json`

Top-level structure:

```json
{
  "metadata": {
    "engine": "gemini31_sampled_validation",
    "model": "gemini-3.1",
    "market": "IL",
    "run_timestamp_utc": null,
    "total_input_variants": 0,
    "total_instruction_records": 0,
    "total_validated_variants": 0,
    "decision_counts": {
      "clean_exact": 0,
      "clean_partial": 0,
      "split_required": 0,
      "reject": 0
    },
    "grounding_cluster_count": 0,
    "gemini_call_count": 0
  },
  "validated_variants": []
}
```

## 16. Decision Rules Claude Must Preserve

Implement the following rules exactly:

1. If identity is valid and trim is missing:

   * return `clean_partial`
   * set `trim_status = unresolved`
   * do not reject

2. If identity is valid and trim is generic:

   * return `clean_partial`
   * set `trim_status = unresolved`
   * do not pretend generic trim is verified
   * do not reject

3. If identity is valid and exact Israeli marketed name is unknown:

   * leave marketed name null unless supported
   * return `clean_partial`

4. If multiple trims are possible but technical identity is one usable model-level variant:

   * return `clean_partial`
   * list candidates in `possible_trim_names`

5. If one row clearly combines multiple distinct trims:

   * return `split_required`
   * provide `split_candidates`

6. If there is a real contradiction in identity:

   * return `reject`

7. Never reject solely because:

   * trim is null
   * trim is None
   * trim is Base
   * trim is Standard
   * trim is generic
   * trim cannot be strongly verified
   * official marketed name is incomplete

8. Do not force trim recovery.

9. Do not invent trim names.

10. Do not over-research.

## 17. Split Required Handling

If `split_required`, the row should remain in the output with the original `validation_id`, but include `split_candidates`.

Each split candidate should include:

```json
{
  "candidate_trim": null,
  "candidate_marketed_name_il": null,
  "candidate_engine": null,
  "candidate_transmission": null,
  "candidate_year_range": null,
  "reason": ""
}
```

The engine should not silently duplicate rows unless explicitly requested in a later phase.

## 18. Checkpointing and Atomic Writes

Design the engine with safe writing behavior.

Required:

* write progress incrementally to a checkpoint file
* write final output atomically
* never corrupt the source files
* be able to resume after interruption
* preserve already validated rows if rerun
* support a small limit parameter for test runs

Suggested files:

* `data/validated_vehicle_variants_full_gemini31_v1.checkpoint.json`
* `data/validated_vehicle_variants_full_gemini31_v1.json.tmp`
* `data/validated_vehicle_variants_full_gemini31_v1.json`

## 19. CLI Interface

Build a simple CLI runner, not Streamlit.

Suggested command:

```bash
python scripts/run_gemini31_sampled_validation.py --limit 20 --mock
```

Real mode:

```bash
python scripts/run_gemini31_sampled_validation.py --real --limit 20
```

Full mode:

```bash
python scripts/run_gemini31_sampled_validation.py --real
```

Suggested flags:

* `--limit`
* `--mock`
* `--real`
* `--force-reprocess`
* `--start-after-validation-id`
* `--checkpoint-every`
* `--output`
* `--dry-run`

## 20. Mock Mode

Implement mock mode first.

Mock mode should not call Gemini.

Mock mode should test:

* join works
* clustering works
* output schema works
* checkpointing works
* `clean_partial` works for weak trims
* rejects only happen for identity contradictions

Mock mode is required before real Gemini integration.

## 21. Real Gemini Integration

Real Gemini integration should be isolated in one client module.

The code should read API key from environment variable.

Suggested environment variable:

`GEMINI_API_KEY`

The client should:

* send the full prompt
* request strict JSON
* parse JSON safely
* retry only on parse failure or transient API failure
* not retry repeatedly for unresolved trim
* return structured validation result

## 22. Tests / Smoke Checks

Include tests or smoke checks for:

1. source files exist
2. variants file has expected structure
3. instructions file has expected structure
4. join count matches
5. no duplicate `validation_id`
6. cluster key generation deterministic
7. weak trim maps to `clean_partial`, not reject
8. missing trim maps to `clean_partial`, not reject
9. identity contradiction maps to `reject`
10. split-required case can be represented
11. all output rows preserve `validation_id`
12. output decision is one of allowed decisions
13. final JSON writes atomically
14. checkpoint can resume
15. no OpenAI/GPT dependency exists

## 23. Expected Sanity Distribution

The final engine should not enforce quotas, but should sanity-check the output distribution.

Expected approximate distribution:

* `clean_exact`: 25-35%
* `clean_partial`: 45-55%
* `split_required`: 5-10%
* `reject`: 10-15%

If reject rate is extremely high, especially due to trim issues, the engine is wrong.

If clean_exact rate is unrealistically high, the engine may be inventing trim names.

## 24. Explicit Anti-Regression Rules

Do not reintroduce old behavior.

Forbidden behavior:

* rejecting solely because trim is weak
* requiring exact Israeli trim proof for acceptance
* sending all unresolved trims to rejection
* using GPT as adjudicator
* building Streamlit UI
* copying old deterministic QA reject logic
* performing deep research per row
* inventing official trim names
* overwriting source files
* dropping validation IDs

## 25. Build Order Claude Should Follow Later

When implementation is requested, build in this order:

1. inspect the two source JSON files
2. create loader and join validation
3. create normalization helpers
4. create cluster key builder
5. create mock Gemini validator
6. create output schema builder
7. create checkpoint writer
8. create CLI runner
9. create smoke tests
10. run mock mode
11. only then add real Gemini client
12. run small real sample
13. inspect decision distribution
14. run full validation only after sample quality is acceptable

## 26. Final Instruction

Do not optimize for proving every trim. Optimize for preserving valid Israeli vehicle identities while clearly marking unresolved trim data.
