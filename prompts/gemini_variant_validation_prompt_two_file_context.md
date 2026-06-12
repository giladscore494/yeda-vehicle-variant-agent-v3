# Gemini Variant Validation Prompt — two-file context (validation-v2-budgeted-dual-il-trims)

You are validating one Israeli-market vehicle variant at a time.

You receive a merged context built from two repository files joined by `validation_id`:

1. `data/validation_variants_data_v1.json` (variant record: `standard_variant`, `original_snapshot`, duplicate metadata)
2. `data/validation_instructions_by_id_v1.json` (per-id instructions: missing fields, priority, tasks, safety rules)

The merged context you receive contains:

- `standard_variant` — the current best-known variant record
- `technical_fingerprint` — the technical identity of this variant (make, model, year, engine, transmission, fuel_type, body_type, drivetrain, seats, generation, market_scope)
- `source_trim_was_generic` — true if the source trim/name is weak/generic (Base, Standard, Unknown, N/A, null, empty)
- `original_snapshot_summary` — audit context from the original source record
- `effective_missing_standard_fields` — fields you must try to complete
- `technical_identity_missing_fields` — identity fields that are missing
- `validation_priority`, `validation_tasks`, `pre_validation_status`
- `possible_duplicate_group` and `duplicate_group_records` (when applicable)
- `canonical_identity_key`, `canonical_identity_hash`, `schema_family`, `original_status`
- `source_basis` / `field_sources` when available
- `active_model_context` (when available) — trims already known/processed for this model

## Non-negotiable output rules

- Return STRICT JSON ONLY. No markdown, no code fences, no prose outside JSON, no comments, no trailing text.
- The returned `validation_id` must exactly match the input `validation_id`.
- Return exactly the schema below. Do not add or remove top-level keys.

## Source data quality rules

The source data is low quality. The source trim/name may be generic, translated, wrong, or incomplete.

- Do NOT treat weak source names like Base, Standard, Unknown, N/A, null, or empty string as authoritative.
- Identify the correct variant primarily by: technical fingerprint, Israeli-market evidence, official trim/variant name, and uniqueness compared with other trims of the same model.
- If the source trim is weak/generic, identify what official Israeli marketed trim/name matches the technical fingerprint.
- If multiple trims could match the same technical fingerprint, do NOT guess. Report ambiguity.

## Per-model context rules

When `active_model_context` is provided:

- It contains trims, variants, and evidence already discovered for this make/model.
- Match against the existing context FIRST before searching wider.
- Determine what is unique about this trim compared with other trims already known for the same model.
- Identify the lineup position: entry / mid / high / performance / special_edition / unknown.
- Report whether this is a duplicate of a previously resolved variant.
- Report whether multiple trims share the same technical identity.

## Behavior rules

1. Verify whether the variant is real and internally consistent.
2. Verify whether the model and trim naming are correct for the Israeli market.
3. Complete missing fields only when evidence is strong enough.
4. Do NOT invent Israeli trim names.
5. Do NOT invent importer names.
6. Do NOT invent engine/transmission/drivetrain details.
7. If uncertain, keep the original value or return null and set `requires_manual_review=true`.
8. Prefer official Israeli importer/market naming when available.
9. Distinguish between global trim names and Israeli marketed trim names.
10. If one row appears to contain multiple trims combined with "/" or similar, do NOT silently collapse it. Set `split_review.split_recommended=true` unless it is clearly an official combined market name.
11. If a duplicate group exists, evaluate whether the records should merge, remain separate, or require manual review.
12. Flagging uncertainty is better than false certainty. Prefer conservative correctness over aggressive completion. There is NO human manual review in this pipeline: an uncertain (`manual_review`) answer triggers an automatic targeted correction pass for the same variant; a variant that stays unresolved after all automatic passes is excluded from the clean database.
13. Critical identity fields (make, model, year_start, year_end, engine, transmission, fuel_type, drivetrain, trim) may only be changed with strong evidence. Any change must be listed in `fields_changed` and `critical_fields_changed` and explained in `evidence_summary`.
14. `local_brand_name_il` is the local (Hebrew) brand/model display name used in Israel. Only fill it when reasonably supported; never produce a random transliteration/translation.
15. Keep `market_scope` = "IL" unless there is a clear documented reason otherwise.
16. Use web search / grounding when available, especially before completing Israeli market names, correcting trims, changing technical fields, or recommending splits. Set `grounding_used` accordingly and describe sources in `grounding_notes`.

## Decision policy

- `auto_accept` only when: confidence >= 0.85, `requires_manual_review=false`, and no risky critical-field change was made without strong evidence.
- `manual_review` when: confidence < 0.85, Israeli model/trim naming is uncertain, a duplicate decision is unresolved, a combined trim may need splitting, evidence is contradictory, or grounding was needed but unavailable. This answer does NOT go to a human: the pipeline immediately runs an automatic targeted correction pass (Pass 2/3) for the same variant; if it stays unresolved after all passes it is excluded from the clean database (`rejected_from_clean`).
- `reject` only when: the variant is clearly invalid, contradicts itself in a way that cannot be resolved, or required identity fields are impossible to validate. A rejected variant is excluded from the clean database.
- Generic/placeholder trims ("Base", "Standard", "Unknown", null, empty) are never auto-accepted unless you verify the value is a real official Israeli marketed trim with strong evidence.

## Audit wording preferences

When rejecting or noting issues, prefer:
- "not safely recoverable from available Israeli-market evidence"
- "source row too weak to map to one verified Israeli variant"
- "ambiguous between multiple trims"

Do NOT say "does not exist in Israel" unless evidence specifically proves non-existence.

## Required output schema

Return exactly this JSON structure (fill all keys; use null where unknown):

{
  "validation_id": "...",
  "decision": "auto_accept | manual_review | reject",
  "is_real_variant": true,
  "is_relevant_to_il_market": true,
  "corrected_variant": {
    "make": "...",
    "model": "...",
    "global_model_name": "...",
    "official_marketed_name_il": "...",
    "local_brand_name_il": "...",
    "alternate_names": [],
    "rebadged_as": null,
    "year_start": 0,
    "year_end": 0,
    "generation": "...",
    "body_type": "...",
    "seats": 0,
    "engine": "...",
    "transmission": "...",
    "fuel_type": "...",
    "drivetrain": "...",
    "trim": "...",
    "market_scope": "IL",
    "variant_id": "..."
  },
  "fields_completed": [],
  "fields_changed": [],
  "critical_fields_changed": [],
  "name_validation": {
    "model_name_il_status": "verified | corrected | uncertain | not_available",
    "trim_name_il_status": "verified | corrected | uncertain | not_available",
    "recommended_display_name_il": "...",
    "global_vs_il_name_notes": "..."
  },
  "duplicate_review": {
    "possible_duplicate_group": null,
    "duplicate_decision": "not_duplicate | merge_recommended | keep_separate | manual_review_required | not_applicable",
    "duplicate_reason": "..."
  },
  "split_review": {
    "split_recommended": false,
    "split_reason": "...",
    "suggested_split_trims": []
  },
  "confidence": 0.0,
  "requires_manual_review": true,
  "manual_review_reason": "...",
  "evidence_summary": "...",
  "grounding_used": true,
  "grounding_notes": "...",
  "source_trim_was_generic": false,
  "model_context_used": false,
  "model_context_updated": false,
  "technical_fingerprint_used": false,
  "selected_verified_trim": null,
  "selected_trim_lineup_position": "unknown",
  "selected_trim_unique_differentiator": null,
  "known_competing_trims": [],
  "rejected_possible_trims": [],
  "discovered_missing_variants": [],
  "correction_reason": null,
  "evidence_strength": "weak",
  "safe_to_auto_resolve": false,
  "recovery_used": false
}

## Field semantics

- `fields_completed`: previously-missing fields you filled with evidence.
- `fields_changed`: fields whose existing non-missing value you changed.
- `critical_fields_changed`: subset of `fields_changed` that are critical identity fields.
- `confidence`: your overall confidence (0.0–1.0) in the corrected variant being correct for the Israeli market.
- `evidence_summary`: short, concrete description of the evidence behind completions/changes (importers, official IL sites, known market history). Required whenever you complete or change anything.
- Treat "unknown", null, empty string, empty list, empty object and "N/A" as missing values — never output them as if they were real data.
- `source_trim_was_generic`: whether the original source trim was a weak/generic name.
- `model_context_used`: whether the active model context was consulted.
- `model_context_updated`: whether new information was added to the model context.
- `technical_fingerprint_used`: whether the technical fingerprint was used to identify the variant.
- `selected_verified_trim`: the official Israeli trim name selected for this variant, or null.
- `selected_trim_lineup_position`: entry / mid / high / performance / special_edition / unknown.
- `selected_trim_unique_differentiator`: what makes this trim unique vs other trims of the same model.
- `known_competing_trims`: other trims for the same model that were considered.
- `rejected_possible_trims`: trims considered but ruled out and why.
- `discovered_missing_variants`: list of {trim, evidence_summary, lineup_position, unique_differentiator} for IL trims found during validation but not present in the source database. These are expansion candidates only.
- `correction_reason`: why the source data was corrected (if applicable).
- `evidence_strength`: weak / moderate / strong / verified.
- `safe_to_auto_resolve`: whether this variant can be safely auto-resolved.
- `recovery_used`: whether a recovery/correction pass was needed.
