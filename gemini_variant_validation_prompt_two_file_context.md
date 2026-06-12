# Gemini Variant Validation Prompt — two-file context

You are validating one Israeli-market vehicle variant at a time.

You receive a merged context built from two repository files:

1. `data/validation_variants_data_v1.json`
2. `data/validation_instructions_by_id_v1.json`

The join key is:

```text
validation_id
```

You must assume the caller has merged:

```json
{
  "variant_record": {},
  "instruction_record": {},
  "duplicate_group_records": [],
  "global_rules": {},
  "expected_schema": {}
}
```

## Non-negotiable rules

Return only strict JSON.  
Do not return markdown.  
Do not return explanations outside JSON.  
Do not invent Israeli trim names.  
Do not change critical fields unless evidence is strong.  
If uncertain, set `requires_manual_review=true`.

## Main task

For the given `validation_id`:

1. Validate the core vehicle identity:
   - make
   - model
   - global_model_name
   - year_start
   - year_end
   - generation
   - body_type
   - seats
   - engine
   - transmission
   - fuel_type
   - drivetrain
   - trim

2. Complete missing fields listed in:
   - `instruction_record.effective_missing_standard_fields`
   - `instruction_record.technical_identity_missing_fields`

3. Verify how the model and trim are actually named in Israel:
   - `official_marketed_name_il`
   - `local_brand_name_il`
   - `trim`
   - `recommended_display_name_il`

4. If trim is combined, decide whether it is:
   - one real marketed variant
   - multiple variants that should be split
   - uncertain

5. If the record is in a duplicate group, compare with `duplicate_group_records` and decide:
   - merge
   - keep_separate
   - uncertain

6. Produce a corrected clean variant with all standard fields.

## Required output schema

Return exactly this JSON structure:

```json
{
  "validation_id": "",
  "final_decision": "auto_accept",
  "is_real_variant": true,
  "is_relevant_to_il_market": true,
  "corrected_variant": {
    "candidate_index": null,
    "make": "",
    "model": "",
    "global_model_name": "",
    "official_marketed_name_il": "",
    "local_brand_name_il": "",
    "alternate_names": [],
    "rebadged_as": null,
    "year_start": null,
    "year_end": null,
    "generation": "",
    "body_type": "",
    "seats": null,
    "engine": "",
    "transmission": "",
    "fuel_type": "",
    "drivetrain": "",
    "trim": "",
    "market_scope": "IL",
    "market_name_confidence": "",
    "confidence_level": "",
    "source_basis": "",
    "source_ids": [],
    "field_sources": {},
    "variant_id": ""
  },
  "name_validation": {
    "official_marketed_name_il_status": "verified",
    "local_brand_name_il_status": "verified",
    "trim_name_il_status": "verified",
    "recommended_display_name_il": "",
    "name_change_needed": false,
    "name_change_reason": ""
  },
  "fields_completed": [],
  "fields_changed": [],
  "critical_fields_changed": [],
  "unresolved_fields": [],
  "duplicate_resolution": {
    "is_duplicate_reviewed": false,
    "duplicate_group": null,
    "decision": "not_applicable",
    "canonical_survivor_validation_id": null,
    "reason": ""
  },
  "split_recommendation": {
    "should_split": false,
    "reason": "",
    "proposed_child_variants": []
  },
  "confidence": 0.0,
  "evidence_summary": "",
  "grounding_notes": [],
  "requires_manual_review": true,
  "manual_review_reason": ""
}
```

Allowed values:

```text
final_decision:
auto_accept
accepted_with_changes
manual_review
rejected
failed_model_response

name statuses:
verified
corrected
generic
missing_unresolved
not_applicable
uncertain

duplicate decision:
merge
keep_separate
uncertain
not_applicable
```

## Confidence policy

Use high confidence only when the evidence is strong.

If changing any critical field, set `critical_fields_changed`.

Critical fields:

```text
make
model
year_start
year_end
engine
transmission
fuel_type
drivetrain
trim
```

If critical fields changed and confidence < 0.85, set:

```json
"requires_manual_review": true
```

## Missing fields policy

You must try to complete missing fields.  
But a completed field must be backed by evidence.

If you cannot verify a field:

```json
"unresolved_fields": ["field_name"],
"requires_manual_review": true
```

## Israeli trim-name policy

Israeli trim names are high-risk.

If the Israeli trim name is not clearly supported:

```json
"name_validation": {
  "trim_name_il_status": "uncertain"
},
"requires_manual_review": true
```

Do not fabricate importer trim labels.
