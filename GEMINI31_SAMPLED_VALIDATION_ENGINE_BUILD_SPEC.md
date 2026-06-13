# Gemini 3.1 Sampled Vehicle Variant Validation Engine — Build Spec

## Goal

Build a new practical Israeli-market vehicle variant validation engine using Gemini 3.1 only.

The engine should read:

- `data/validation_variants_data_v1.json`
- `data/validation_instructions_by_id_v1.json`

It should join them by `validation_id`.

It should produce a new full validated output file:

- `data/validated_vehicle_variants_full_gemini31_v1.json`

The engine should preserve every original `validation_id`.

---

## Why We Are Rebuilding

The previous engine became too strict and too expensive.

It rejected too many real variants because exact trim names were weak, generic, missing, or hard to verify.

Examples of weak trims:

- "Base"
- "Standard"
- "None"
- "null"
- empty trim
- generic Israeli marketed names
- incomplete trim names

This behavior is wrong for a practical car-knowledge database.

A weak trim does not mean the vehicle identity is invalid.

The new engine must prioritize useful, safe vehicle identity validation over perfect trim-level proof.

---

## Core Principle

**Acceptance depends mainly on identity confidence, not trim confidence.**

- Vehicle identity should be strict.
- Trim enrichment should be flexible.

A row should enter the clean output if the core vehicle identity is real, plausible, internally consistent, and relevant to the Israeli market.

The exact trim can remain unresolved.

---

## Identity-Critical Fields

The engine should treat these as core identity fields:

- `make`
- `model`
- `engine`
- `transmission`
- `fuel_type`
- `drivetrain`
- `body_type`
- `year_start`
- `year_end`
- Israeli market relevance

If these fields form a real and plausible Israeli-market vehicle identity, the variant should usually be accepted.

---

## Trim/Enrichment Fields

The engine should treat these as enrichment fields, not hard rejection fields:

- `trim`
- `trim_name`
- `trim_name_il`
- `official_marketed_name_il`
- `local_variant_name`
- `alternate_names`
- package/edition names

If these are missing or uncertain, the row can still be accepted as `clean_partial`.

---

## Decision Model

The engine should use these final decisions:

### `clean_exact`

Use when:

- core vehicle identity is valid
- exact trim or marketed variant is strongly verified
- no meaningful ambiguity remains

### `clean_partial`

Use when:

- core vehicle identity is valid
- vehicle is relevant to the Israeli market
- exact trim / Israeli marketed name / package name remains unresolved or weak

This is a **success state**, not a failure state.

### `split_required`

Use when:

- one raw row clearly combines several distinct trims or marketed variants
- the variants should not be collapsed into one clean row
- examples: multiple named trims with materially different specs or positioning

### `reject`

Use only when:

- the vehicle identity is likely invalid
- make/model combination does not exist
- powertrain is contradictory
- year range is implausible
- Israeli market relevance is not credible
- the row mixes incompatible vehicles
- required identity fields are missing beyond recovery
- accepting the row would pollute the clean database

**Do not reject solely because of weak trim.**

---

## Gemini 3.1 Role

Gemini 3.1 is the only model.

There should be no GPT adjudicator.

Gemini 3.1 should act like a practical vehicle expert doing a short but grounded check.

The model should not perform deep academic research for every row.

The model should:

- inspect the technical fingerprint
- check whether the vehicle identity exists and is plausible
- use short, high-quality grounding/search
- check what trim levels or marketed versions were sold under the same model in Israel during the relevant years
- avoid inventing exact trim names
- fill useful fields when reasonably supported
- mark uncertain trim fields as unresolved instead of rejecting the row

---

## Grounding Requirement

Grounding is required, but it should be practical and bounded.

The model should do a short web-quality check, not a long research investigation.

For each model/year group, grounding should try to understand:

- whether the model was sold in Israel
- approximate years sold
- available body/powertrain combinations
- known trim levels or marketed versions under that model
- whether the raw row is one exact trim, one model-level variant, or a mixed/split row

### Preferred grounding sources:

- Israeli importer pages
- Israeli vehicle catalog pages
- Israeli used-car listings/catalogs
- manufacturer pages
- trusted automotive databases
- reliable car review/spec pages

Avoid weak sources when better ones are available.

Do not require perfect proof of exact trim to accept the row.

---

## Sampling / Grouping Strategy

Do not research every single row from scratch.

To reduce cost, group or cache by identity cluster:

- make
- model
- generation/year range
- engine
- fuel type
- transmission
- body type
- drivetrain

For each cluster, perform a short grounding pass once, then reuse the result for similar variants.

The engine should sample intelligently:

- first validate representative rows per make/model/year/powertrain cluster
- cache discovered Israeli trims and market facts
- reuse evidence across variants with the same technical fingerprint
- only trigger additional grounding when a row introduces a new engine, body, generation, year range, or contradictory detail

The goal is practical accuracy at reasonable cost.

---

## Required Output Schema Per Variant

Each validated row should include at least:

```json
{
  "validation_id": "VAL-000000",
  "source_validation_id": "VAL-000000",
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
  "blocking_identity_issues": [],
  "non_blocking_trim_issues": [],
  "fields_changed": [],
  "fields_left_unresolved": [],
  "decision_reason": ""
}
```

---

## Important Decision Rules

1. **If identity is valid and trim is missing:**
   - return `clean_partial`
   - set `trim_status = unresolved`
   - do not reject

2. **If identity is valid and trim is generic:**
   - return `clean_partial`
   - do not pretend the generic trim is verified
   - do not reject

3. **If exact Israeli marketed name is unknown:**
   - leave it null or best-effort only if supported
   - return `clean_partial` if identity is still valid

4. **If multiple trims are possible but the row represents one technical model-level identity:**
   - return `clean_partial`
   - list possible trim names in `possible_trim_names`

5. **If the row clearly combines multiple distinct trims:**
   - return `split_required`

6. **If there is a real contradiction in identity:**
   - return `reject`

7. **Never reject only because:**
   - trim is null
   - trim is None
   - trim is Base
   - trim is Standard
   - trim is generic
   - trim cannot be strongly verified
   - Israeli marketed name is incomplete

---

## Prompt Style for Gemini

The Gemini prompt should be short and practical.

It should say:

> "You are validating one Israeli-market vehicle variant for a practical car-knowledge database. This is not a deep research task. Do a short grounded check. Decide whether the vehicle identity is real and useful. Do not reject because trim is weak. If identity is valid but trim is unresolved, return clean_partial."

---

## Final Output File

The completed engine should produce:

`data/validated_vehicle_variants_full_gemini31_v1.json`

The file should include:

- metadata
- run timestamp
- model name
- grounding mode
- total input variants
- decision counts
- validated variants array

### Suggested top-level shape:

```json
{
  "metadata": {
    "engine": "gemini31_sampled_validation",
    "model": "gemini-3.1",
    "market": "IL",
    "total_input_variants": 3712,
    "decision_counts": {
      "clean_exact": 0,
      "clean_partial": 0,
      "split_required": 0,
      "reject": 0
    }
  },
  "validated_variants": []
}
```

---

## Success Criteria

The new engine is successful if:

- it preserves all source `validation_id`s
- it joins variants and instructions correctly
- it no longer rejects valid vehicles due to weak trims
- `clean_partial` becomes a normal success path
- `reject` is reserved for true identity problems
- grounding is used but bounded
- output is useful for a practical Israeli car-knowledge product
- cost is controlled by grouping, caching, and short checks

### Expected approximate output distribution:

| Decision | Approximate % |
|---|---|
| `clean_exact` | ~25–35% |
| `clean_partial` | ~45–55% |
| `split_required` | ~5–10% |
| `reject` | ~10–15% |

These are not hard quotas. They are sanity-check expectations.

---

## Do Not Build Yet

This file is a build specification.

After creating this Markdown file and cleaning the repository, stop.

Do not implement the engine yet unless explicitly asked.
Do not run Gemini.
Do not create the final validated JSON yet.
