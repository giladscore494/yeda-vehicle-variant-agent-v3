# BATCH 21 — FULL UNIFIED CODEX TASK

Temporary task file path in repo:

```text
codex_tasks/BATCH21_FULL_UNIFIED_CODEX_TASK.md
```

## Single source-of-truth operating rules

1. Read this file as the complete source of truth for Batch 21.
2. Do **not** browse the internet. All web validation was performed outside Codex; use the facts and URLs embedded here.
3. Execute in order: RUN 1, then RUN 2, then RUN 3, then rebuild/tests.
4. Apply exact data-quality corrections, not only blocker clearing.
5. Never force an unsupported Israeli-market variant into clean. Move weak/unsupported rows to non-blocking archive/review.
6. Preserve legitimate split profiles and alias/lineage so `unmatched_output_keys_count` remains 0.
7. After success, delete the temporary task files under `codex_tasks/`.

Final required state:

```text
models_blocked = 0
review_only_blocked_entries = 0
duplicate_technical_variants = 0
invalid_source_references = 0
unknown_support_values = 0
ready_for_website_upload = true
unmatched_output_keys_count = 0
unmatched_output_keys_sample = []
active blocked = 0
```

---

# PART A — RUN 1

# BATCH 21 — RUN 1 Codex Task

Repository branch/context: `validation-v2-budgeted-dual-il-trims`

This task is generated after offline inspection of the uploaded ZIP and external web validation performed outside Codex. **Do not browse the internet.** Treat this file as the source-of-truth instruction bundle for RUN 1 only.

## Batch state found in ZIP

Files inspected:

- `data/model_technical_catalog_il.json`
- `data/model_technical_catalog_il_readiness.json`
- `data/model_technical_catalog_il_review.json`
- `data/model_technical_catalog_il_quality_scan.json`
- `data/validated_vehicle_variants_full_gemini31_v1.checkpoint.json`
- `data/validation_run_summary_gemini31.json`

Actual state:

```text
clean_models = 241
models_blocked = 9
review_entries = 9
review_only_blocked_entries = 9
ready_for_website_upload = false
technical_variants_total = 801
technical_variants_with_sources = 801
technical_variants_with_field_sources = 801
technical_variants_missing_required_grounding = 4
technical_variants_missing_grounded_fields = 104
duplicate_technical_variants = 0
invalid_source_references = 0
unknown_support_values = 0
last_checkpointed_profile_id = IL::Citroen::C6
resume_after_key = IL|Citroen|C6
next_key_to_process = IL|Citroen|C8
unmatched_output_keys_count = 0
split_profile_alias_count = 5
```

Known split aliases currently active and legitimate unless later contradicted:

```text
IL|Alfa Romeo|Junior Elettrica -> IL|Alfa Romeo|Junior
IL|BMW|M850i -> IL|BMW|850i
IL|BMW|X5 xDrive30d -> IL|BMW|X5 3.0d
IL|BYD|Atto 3 EVO -> IL|BYD|Atto 3
IL|Cadillac|Escalade IQ -> IL|Cadillac|Escalade
```

Do not delete legitimate split aliases. Preserve/update `source_alias_keys` / lineage so they do not become unmatched.

## RUN 1 scope

This RUN covers the first 20 profiles from the latest 50 clean profiles according to the clean catalog order:

1. `IL|BYD|Dolphin`
2. `IL|BYD|Han`
3. `IL|BYD|Seal`
4. `IL|BYD|Seal U`
5. `IL|BYD|Sealion 7`
6. `IL|BYD|Song Plus`
7. `IL|BYD|Tang`
8. `IL|Cadillac|ATS`
9. `IL|Cadillac|CTS`
10. `IL|Cadillac|Escalade`
11. `IL|Cadillac|Escalade IQ`
12. `IL|Cadillac|Lyriq`
13. `IL|Cadillac|SRX`
14. `IL|Cadillac|XT4`
15. `IL|Cadillac|XT5`
16. `IL|Cadillac|XT6`
17. `IL|Chery|Arrizo 8`
18. `IL|Chery|Tiggo 7 Pro`
19. `IL|Chery|Tiggo 8 Pro`
20. `IL|Chevrolet|Aveo`

Apply only the changes in this RUN 1 file. Do not process RUN 2 or blockers yet.

---

# A. Global deterministic quality fixes required by RUN 1

## A1. Fix top-level profile year range being null

**Current issue:** In the 20 RUN 1 profiles, top-level profile fields `year_start` / `year_end` are absent/null even when `technical_variants_il[*].year_start/year_end` are grounded.

**Action: FIX code + rebuild.**

Add deterministic derivation during catalog build/repair/normalization, after `technical_variants_il` has been finalized:

```python
variant_starts = [v.get("year_start") for v in variants if isinstance(v.get("year_start"), int)]
variant_ends = [v.get("year_end") for v in variants if isinstance(v.get("year_end"), int)]
has_open_end = any(v.get("year_end") is None for v in variants)
profile["year_start"] = min(variant_starts) if variant_starts else None
profile["year_end"] = None if has_open_end else (max(variant_ends) if variant_ends else None)
```

Do not invent years. Derive only from the profile's variant rows. Re-run catalog build/readiness so top-level years are populated.

Expected top-level year ranges for RUN 1 after this task:

```text
BYD Dolphin: 2023-2024
BYD Han: 2022-2024
BYD Seal: 2024-null
BYD Seal U: 2024-2026
BYD Sealion 7: 2025-null or 2025-2026 if all active 2026 rows are stored with concrete 2026 end
BYD Tang: 2022-2024
Cadillac ATS: 2013-2019
Cadillac CTS: 2003-2019
Cadillac Escalade: 2022-2026
Cadillac Escalade IQ: 2025-null or 2025-2026 depending active-row convention, but not top-level null/null
Cadillac Lyriq: 2025-2026
Cadillac SRX: 2004-2016
Cadillac XT4: 2019-2025
Cadillac XT5: 2016-2024
Cadillac XT6: 2020-2026
Chery Arrizo 8: 2024-2026 after added rows below
Chery Tiggo 7 Pro: 2022-2024
Chery Tiggo 8 Pro: 2022-2024 unless current official-source refresh is applied with exact 2026 support
Chevrolet Aveo: 2004-2011
```

## A2. Do not count optional null technical fields as missing grounded fields

**Current issue:** many valid rows are counted in `technical_variants_missing_grounded_fields` only because optional fields are null by nature:

- EV rows have `engine_displacement_l = null` and `missing_grounded_fields = ["engine_displacement_l"]`.
- active/open rows have `year_end = null` and `missing_grounded_fields = ["year_end"]`.
- old models with no real trim can have `version_or_trim = null` and `missing_grounded_fields = ["version_or_trim"]`.

These are not actual quality problems if the technical row is otherwise directly sourced and website-required fields are populated.

**Action: FIX code + rebuild.**

In validation/statistics/repair logic, normalize `missing_grounded_fields` as follows:

- If field value is `None`/empty and the field is optional, remove it from `missing_grounded_fields`.
- Optional-null fields include at minimum: `engine_displacement_l`, `year_end`, `version_or_trim`.
- Never create fake displacement for EVs.
- Never force active model `year_end` when the source only proves current/ongoing sale.
- Keep blocking behavior for required website fields only when actually null/empty.

Relevant files to patch:

- `scripts/catalog_validation.py` — `has_missing_grounded_fields` should not be true just because optional-null fields are listed.
- `scripts/catalog_repair.py` — `derive_repair_targets()` should not ask the model to reground optional-null fields.
- `scripts/catalog_quality_scan.py` — do not report optional-null fields as missing grounded cells.
- `scripts/catalog_normalization.py` if merge logic preserves optional-null missing fields.

Expected impact: valid EV rows like Dolphin/Han/Seal/Tang/Sealion 7 and old no-trim Aveo rows stop inflating missing-grounded stats.

## A3. Enforce scalar type for `version_or_trim`

**Current issue:** `Chery Tiggo 8 Pro` stores `version_or_trim` as arrays:

```json
["Luxury", "Noble"]
["Ultimate"]
```

Schema expects a scalar string or null, not a list.

**Action: FIX code + data.**

- Add validation that `version_or_trim` must be a string or null.
- If it is a list of strings representing the same technical variant, normalize to a scalar using `" / "`, e.g. `"Luxury / Noble"`.
- If it is a single-element list, normalize to the only item, e.g. `"Ultimate"`.
- If the list contains separate technical variants, split only when a technical field differs and is sourced.

---

# B. Per-model RUN 1 data instructions

## 1. BYD Dolphin — KEEP + cleanup optional-null missing fields

Current rows:

```text
Comfort | Hatchback | electric | engine=electric | displacement=null | 204 hp | single_speed | FWD | 2023-2024
Design  | Hatchback | electric | engine=electric | displacement=null | 204 hp | single_speed | FWD | 2023-2024
```

External validation: Israeli BYD/Cartube/iCar sources support Dolphin sold in Israel in Comfort/Design with 204 hp FWD electric layout.

Action: **KEEP** both rows.

Exact fixes:

- Remove `engine_displacement_l` from `missing_grounded_fields` because EV displacement is legitimately null.
- Keep `engine_displacement_l = null`.
- Populate top-level `year_start=2023`, `year_end=2024` through A1.

## 2. BYD Han — KEEP + cleanup optional-null missing fields

Current row:

```text
Executive | Sedan | electric | engine=electric | displacement=null | 518 hp | single_speed | AWD | 2022-2024
```

External validation: Israeli iCar/Auto/Cartube sources support Han Executive AWD with 518 hp.

Action: **KEEP** row.

Exact fixes:

- Remove `engine_displacement_l` from `missing_grounded_fields`.
- Keep `engine_displacement_l = null`.
- Populate top-level `year_start=2022`, `year_end=2024` through A1.

## 3. BYD Seal — KEEP but official-source horsepower cleanup

Current rows:

```text
Design     | Sedan | electric | 313 hp | single_speed | RWD | 2024-null | missing engine_displacement_l/year_end
Excellence | Sedan | electric | 530 hp | single_speed | AWD | 2024-null | missing engine_displacement_l/year_end
```

External validation:

- BYD Israel official source lists Seal Design with 313 hp and Seal Excellence with 531 hp.
- Israeli iCar/Cartube style sources often round/report Excellence as 530 hp.

Action: **FIX** using importer-official value as source of truth.

Exact fixes:

- Keep `Design` as `313 hp`, RWD, single_speed, 2024-null.
- Change `Excellence.horsepower_hp` from `530` to `531` if using the official BYD importer source as the direct source. If the project intentionally normalizes to rounded catalog values, document that choice and keep 530 only when the source index is iCar/Cartube, not official BYD.
- Remove `engine_displacement_l` and `year_end` from `missing_grounded_fields`; both are legitimate nulls for EV/open-ended rows.
- Add/ensure a direct BYD official source entry for Seal if not present; current profile sources only show Cartube and iCar.
- Populate top-level `year_start=2024`, `year_end=null` through A1.

## 4. BYD Seal U — FIX incomplete variant set and missing EV trim

Current rows:

```text
null    | SUV | electric       | electric          | null | 218 hp | single_speed | FWD | 2024-2026
Comfort | SUV | plug_in_hybrid | 1.5L plug-in hybrid | 1.5 | 218 hp | automatic | FWD | 2024-2026
Design  | SUV | plug_in_hybrid | 1.5L plug-in hybrid | 1.5 | 324 hp | automatic | AWD | 2024-2026
```

Problems:

- EV row has `version_or_trim = null`; Israeli sources identify EV trims as `Comfort` and `Design`.
- PHEV/DM-i lineup is incomplete: `Boost` is missing.
- Current profile source list is too thin and includes a single mixed Cartube/BYD source.

External validation:

- BYD Israel DM-i source supports `Boost` and `Comfort` with 218 hp FWD and `Design` with 324 hp AWD.
- iCar current Israeli catalog lists five Seal U variants: EV `Comfort`, EV `Design`, PHEV/DM-i `Boost`, PHEV/DM-i `Comfort`, PHEV/DM-i `Design`.
- BYD Israel EV source supports the electric Seal U line.

Action: **FIX / SPLIT rows**.

Exact target rows:

```text
Comfort | SUV | electric       | electric              | null | 218 hp | single_speed | FWD | 2024-2026
Design  | SUV | electric       | electric              | null | 218 hp | single_speed | FWD | 2024-2026
Boost   | SUV | plug_in_hybrid | 1.5L plug-in hybrid   | 1.5  | 218 hp | automatic    | FWD | 2024-2026
Comfort | SUV | plug_in_hybrid | 1.5L plug-in hybrid   | 1.5  | 218 hp | automatic    | FWD | 2024-2026
Design  | SUV | plug_in_hybrid | 1.5L plug-in hybrid   | 1.5  | 324 hp | automatic    | AWD | 2024-2026
```

Notes:

- The duplicate-looking `Comfort` trim is legitimate because EV Comfort and PHEV Comfort have different fuel_type/engine/transmission profile.
- Do not merge EV Comfort with PHEV Comfort.
- Add/ensure field_sources for every non-null field from official/importer/iCar/Cartube sources.
- Remove optional-null `engine_displacement_l` from EV rows' `missing_grounded_fields`.
- Populate top-level `year_start=2024`, `year_end=2026` through A1.

## 5. BYD Sealion 7 — FIX missing Comfort and official horsepower

Current rows:

```text
Boost      | SUV | electric | 231 hp | RWD | 2025-null
Design     | SUV | electric | 313 hp | RWD | 2025-null
Excellence | SUV | electric | 530 hp | AWD | 2025-null
```

Problems:

- `Comfort` trim is missing.
- Official BYD Israel source lists Excellence as 531 hp, not 530.
- EV displacement/open year missing fields should not count as quality issues.

External validation:

- BYD Israel official page lists Sealion 7: `Boost` 231 hp RWD, `Comfort` 313 hp RWD, `Design` 313 hp RWD, `Excellence` 531 hp AWD.

Action: **FIX**.

Exact target rows:

```text
Boost      | SUV | electric | electric | null | 231 hp | single_speed | RWD | 2025-null
Comfort    | SUV | electric | electric | null | 313 hp | single_speed | RWD | 2025-null
Design     | SUV | electric | electric | null | 313 hp | single_speed | RWD | 2025-null
Excellence | SUV | electric | electric | null | 531 hp | single_speed | AWD | 2025-null
```

- Add the missing `Comfort` row.
- Change `Excellence.horsepower_hp` from `530` to `531` using official BYD as direct source.
- Remove `engine_displacement_l` and `year_end` from missing fields.
- Populate top-level `year_start=2025`, `year_end=null` through A1.

## 6. BYD Song Plus — MERGE/DELETE standalone clean profile into Seal U alias

Current row:

```text
make=BYD | model=Song Plus | version_or_trim=null | SUV | electric | 204 hp | FWD | 2024-null
source url = local_review_source
```

Problem:

- This is not strong Israeli-market clean catalog evidence. It is using a non-URL/local review placeholder source and should not be a standalone clean Israeli marketed model.
- Israeli sources describe `Song Plus` as the Chinese/source name or basis of the model marketed locally as `BYD Seal U`, not as a strong standalone Israeli clean model.

External validation:

- Israeli sources state BYD Seal U is based on / known in China as Song Plus.
- The Israeli marketed model name is Seal U.

Action: **MERGE / DELETE standalone clean profile**.

Exact fixes:

- Remove `IL|BYD|Song Plus` as a standalone clean website model.
- Add/keep alias lineage on `IL|BYD|Seal U`:

```json
"source_alias_keys": ["IL|BYD|Song Plus"]
```

- Preserve matched-output behavior so `IL|BYD|Song Plus` is not reported as unmatched.
- Do not move this into active blockers; if any raw source row still references Song Plus, route it as an alias/mapping to Seal U or review/archive non-blocking.

## 7. BYD Tang — KEEP + cleanup optional-null missing fields

Current row:

```text
Premium | SUV | electric | 518 hp | single_speed | AWD | 2022-2024
```

External validation: Israeli BYD/iCar/Cartube/Gear sources support Tang Premium AWD with 518 hp.

Action: **KEEP**.

Exact fixes:

- Remove `engine_displacement_l` from `missing_grounded_fields`.
- Keep `engine_displacement_l = null`.
- Populate top-level `year_start=2022`, `year_end=2024` through A1.

## 8. Cadillac ATS — KEEP + top-level years

Current rows are coherent Israeli CTS/ATS-era rows:

```text
Luxury/Premium Sedan 2.0L turbo 272 hp 6AT RWD 2013-2015
Luxury/Premium Sedan 2.0L turbo 272 hp 8AT RWD 2016-2019
Premium Coupe 2.0L turbo 272 hp 6AT RWD 2015-2015
Premium Coupe 2.0L turbo 272 hp 8AT RWD 2016-2019
```

Action: **KEEP**.

Exact fixes:

- No row-level data correction found in RUN 1.
- Populate top-level `year_start=2013`, `year_end=2019` through A1.

## 9. Cadillac CTS — KEEP + top-level years

Current rows cover CTS historical engine/gearbox phases including CTS-V:

```text
3.2 V6 220 hp 5AT 2003-2004
2.8 V6 215 hp 5AT 2005-2007
3.6 V6 255 hp 5AT 2005-2007
3.0 V6 270 hp 6AT 2010-2013
3.6 V6 311 hp 6AT 2008-2013
CTS-V 6.2 supercharged 556 hp 6AT 2009-2013
2.0T 272 hp 6AT 2014-2015
2.0T 272 hp 8AT 2016-2019
CTS-V 6.2 supercharged 640 hp 8AT 2016-2019
```

External validation: Israeli Auto/iCar/Cartube/Gear sources support the 2014+ 2.0T 272 hp phase and CTS-V import; current rows are plausible and sourced.

Action: **KEEP**.

Exact fixes:

- No row-level data correction found in RUN 1.
- Populate top-level `year_start=2003`, `year_end=2019` through A1.

## 10. Cadillac Escalade — KEEP + preserve split lineage to Escalade IQ

Current row:

```text
Luxury Sport | SUV | petrol | 6.2L V8 | 420 hp | 10AT | 4WD | 2022-2026
```

Action: **KEEP**.

Exact fixes:

- Keep row as-is.
- Ensure `IL|Cadillac|Escalade IQ` split alias remains connected to `IL|Cadillac|Escalade` for unmatched-output purposes, but do not merge the IQ EV row into the petrol Escalade technical variant.
- Populate top-level `year_start=2022`, `year_end=2026` through A1.

## 11. Cadillac Escalade IQ — FIX missing trims / split rows

Current row:

```text
version_or_trim=null | SUV | electric | 750 hp | single_speed | AWD | 2025-null
```

Problems:

- `version_or_trim = null` is wrong for current Israeli official offering.
- Official Israeli Cadillac page lists two trims: `Luxury Sport` and `Premium Luxury`.
- Both trims are visible in the official pollution/trim table.

External validation:

- Cadillac Israel official page shows Escalade IQ 2026, available through UMI, and performance up to 750 hp.
- Same official page lists trims `Luxury Sport` and `Premium Luxury`.
- Same official pollution table lists `ESCALADE IQ Luxury Sport` and `ESCALADE IQ Premium Luxury`.

Action: **SPLIT / FIX**.

Exact target rows:

```text
Luxury Sport   | SUV | electric | electric | null | 750 hp | single_speed | AWD | 2025-null or 2025-2026 by active-row convention
Premium Luxury | SUV | electric | electric | null | 750 hp | single_speed | AWD | 2025-null or 2025-2026 by active-row convention
```

Exact fixes:

- Replace the single null-trim row with the two sourced trim rows above.
- Add official Cadillac Israel source `https://www.cadillac.co.il/ESCALADE-IQ/` to profile sources if not already present.
- Use official source for `version_or_trim`, `fuel_type`, `engine`, `horsepower_hp`, `drivetrain`, `year_start/current model evidence` where supported.
- Keep source alias lineage:

```json
"source_alias_keys": ["IL|Cadillac|Escalade"]
```

- Do not merge IQ with petrol Escalade; it is a legitimate split profile.

## 12. Cadillac Lyriq — KEEP + cleanup optional-null missing fields if present

Current row:

```text
Luxury AWD | SUV | electric | 515 hp | single_speed | AWD | 2025-2026
```

External validation: Cadillac Israel technical page supports Lyriq Luxury AWD with 515 hp, AWD, electric SUV configuration.

Action: **KEEP**.

Exact fixes:

- Keep row.
- If `engine_displacement_l` appears in missing fields in any regenerated output, remove it as optional-null EV displacement.
- Populate top-level `year_start=2025`, `year_end=2026` through A1.

## 13. Cadillac SRX — KEEP + top-level years

Current rows:

```text
3.6 V6 255 hp 5AT AWD 2004-2009
3.0 V6 265 hp 6AT FWD 2010-2011
3.0 V6 265 hp 6AT AWD 2010-2011
3.6 V6 314 hp 6AT FWD 2012-2016
3.6 V6 314 hp 6AT AWD 2012-2016
```

External validation: Israeli Auto/iCar/Cartube sources support the SRX Israel generations and the 3.0/3.6 V6 variants. Some sources differ between 308/314 hp on specific FWD listings; current catalog has 314 for both 3.6 FWD/AWD. Do not alter horsepower unless a stronger Israeli source in repo directly maps the FWD row to 308.

Action: **KEEP** with no unsupported speculation.

Exact fixes:

- Keep current rows.
- Populate top-level `year_start=2004`, `year_end=2016` through A1.

## 14. Cadillac XT4 — KEEP + top-level years

Current rows:

```text
Premium Luxury | SUV | petrol | 2.0L turbo | 237 hp | 9AT | FWD | 2019-2025
Sport          | SUV | petrol | 2.0L turbo | 237 hp | 9AT | AWD | 2019-2025
```

Action: **KEEP**.

Exact fixes:

- No row-level data correction found in RUN 1.
- Populate top-level `year_start=2019`, `year_end=2025` through A1.

## 15. Cadillac XT5 — KEEP + top-level years

Current rows:

```text
3.6 V6 310 hp 8AT FWD 2016-2019
3.6 V6 310 hp 8AT AWD 2016-2019
2.0T 237 hp 9AT FWD 2020-2024
3.6 V6 310 hp 9AT AWD 2020-2024
```

External validation: Israeli Auto/Cartube sources support the 2020 facelift split into 2.0T 237 hp and 3.6 V6 310 hp with 9-speed automatic; older 3.6 V6 310 hp with 8-speed is consistent with launch rows.

Action: **KEEP**.

Exact fixes:

- No row-level data correction found in RUN 1.
- Populate top-level `year_start=2016`, `year_end=2024` through A1.

## 16. Cadillac XT6 — FIX stale year_end to 2026

Current rows:

```text
Premium Luxury | SUV | petrol | 3.6L V6 | 310 hp | 9AT | AWD | 2020-2024
Sport          | SUV | petrol | 3.6L V6 | 310 hp | 9AT | AWD | 2020-2024
```

Problem:

- `year_end=2024` is stale. Current official and Israeli catalog sources show XT6 2026 in Israel.

External validation:

- Cadillac Israel official XT6 page is active for 2026 and states a 3.6L V6, about 310 hp, 9-speed automatic.
- Cartube current new-car page lists 2026 XT6 `3.6 Premium Luxury` and `3.6 Sport`, both 310 hp.
- Auto.co.il lists Cadillac XT6 2026 with 3.6L V6, 310 hp, 9-speed automatic, AWD.

Action: **FIX**.

Exact target rows:

```text
Premium Luxury | SUV | petrol | 3.6L V6 | 3.6 | 310 hp | 9-speed automatic | AWD | 2020-2026
Sport          | SUV | petrol | 3.6L V6 | 3.6 | 310 hp | 9-speed automatic | AWD | 2020-2026
```

Exact fixes:

- Change `year_end` from `2024` to `2026` on both rows.
- Add/ensure current official Cadillac Israel XT6 source URL: `https://www.cadillac.co.il/דגמים/xt6/`.
- Add/ensure current Cartube/Auto sources for 2026 trims if needed.
- Populate top-level `year_start=2020`, `year_end=2026` through A1.

## 17. Chery Arrizo 8 — FIX incomplete trims and stale year_end

Current row:

```text
Noble | Sedan | plug_in_hybrid | 1.5L turbo | 347 hp | automatic | FWD | 2024-2024
```

Problems:

- Israeli launch/current sources show at least `Comfort` and `Noble`; current catalog only has `Noble`.
- 2024-2024 is stale/incomplete for an active/current model.
- A 2026 `Sense` trim is mentioned in at least one Israeli source, but do not add it to clean unless exact technical details and source support are present in source list.

External validation:

- Israeli sources describe Arrizo 8 PHEV with 1.5 turbo plug-in-hybrid system, combined 347 hp, FWD.
- Launch/current Israeli sources list `Comfort` and `Noble` trims.
- Auto.co.il mentions a cheaper `Sense` trim added in January 2026, but if the source bundle does not explicitly provide full technical fields for Sense, keep Sense out of clean and do not block the model for it.

Action: **FIX / SPLIT**.

Exact target rows:

```text
Comfort | Sedan | plug_in_hybrid | 1.5L turbo plug-in hybrid | 1.5 | 347 hp | automatic | FWD | 2024-2026
Noble   | Sedan | plug_in_hybrid | 1.5L turbo plug-in hybrid | 1.5 | 347 hp | automatic | FWD | 2024-2026
```

Optional non-blocking note:

```text
Sense | route to review/archive only unless exact Israeli source support exists for all required technical fields.
```

Exact fixes:

- Add missing `Comfort` row with same grounded technical config as Noble.
- Extend `Noble.year_end` from `2024` to `2026` if sourced by current Israeli catalog source.
- Ensure field_sources cite exact source indexes for trim, fuel type, engine, displacement, hp, transmission, drivetrain, years.
- Populate top-level `year_start=2024`, `year_end=2026` through A1.

## 18. Chery Tiggo 7 Pro — KEEP + top-level years

Current rows:

```text
Comfort / Noble | SUV | petrol         | 1.6L turbo | 186 hp | 7DCT | FWD | 2022-2024
Supreme          | SUV | plug_in_hybrid | 1.5L turbo | 320 hp | 3-speed automatic | FWD | 2024-2024
```

External validation: Israeli Chery/Cartube/iCar sources support Tiggo 7 Pro petrol Comfort/Noble and PHEV Supreme with these broad technical fingerprints.

Action: **KEEP**.

Exact fixes:

- No row-level data correction found in RUN 1.
- Populate top-level `year_start=2022`, `year_end=2024` through A1.

## 19. Chery Tiggo 8 Pro — FIX list-valued trims

Current rows:

```json
{"version_or_trim": ["Luxury", "Noble"], "fuel_type": "petrol", "engine": "1.6L turbo", "horsepower_hp": 186, ...}
{"version_or_trim": ["Ultimate"], "fuel_type": "plug_in_hybrid", "engine": "1.5L turbo", "horsepower_hp": 318, ...}
```

Problem:

- `version_or_trim` is list-valued; this is invalid for website-ready JSON and likely creates downstream bugs.

External validation:

- Israeli Chery/Cartube/iCar sources support Tiggo 8 Pro petrol `Luxury`/`Noble` with 1.6 turbo 186 hp.
- Israeli Chery/Cartube/iCar sources support Tiggo 8 Pro PHEV `Ultimate` with 1.5 turbo PHEV around 318 hp.

Action: **FIX**.

Exact target rows:

```text
Luxury / Noble | SUV | petrol         | 1.6L turbo | 1.6 | 186 hp | 7-speed dual_clutch | FWD | 2022-2024
Ultimate       | SUV | plug_in_hybrid | 1.5L turbo | 1.5 | 318 hp | 3-speed automatic  | FWD | 2023-2024
```

Exact fixes:

- Change `version_or_trim` from `["Luxury", "Noble"]` to scalar string `"Luxury / Noble"`.
- Change `version_or_trim` from `["Ultimate"]` to scalar string `"Ultimate"`.
- Add code-level guard from A3 so this cannot regress.
- Populate top-level `year_start=2022`, `year_end=2024` through A1 unless current official 2026 source is added with full field support.

## 20. Chevrolet Aveo — KEEP + cleanup optional-null trim missing fields

Current rows:

```text
null | Sedan     | petrol | 1.4L | 94 hp  | 4AT | FWD | 2004-2008 | missing version_or_trim
null | Hatchback | petrol | 1.4L | 94 hp  | 4AT | FWD | 2004-2008 | missing version_or_trim
null | Sedan     | petrol | 1.4L | 101 hp | 4AT | FWD | 2008-2011 | missing version_or_trim
null | Hatchback | petrol | 1.4L | 101 hp | 4AT | FWD | 2008-2011 | missing version_or_trim
```

Problem:

- `version_or_trim = null` is acceptable for old Israeli Aveo technical rows if the technical configuration is directly sourced. Do not count `version_or_trim` as a missing grounded field.

Action: **KEEP**.

Exact fixes:

- Remove `version_or_trim` from `missing_grounded_fields` in all four Aveo rows.
- Keep `version_or_trim = null`.
- Populate top-level `year_start=2004`, `year_end=2011` through A1.

---

# C. Source facts used for this RUN 1 task

Codex must not browse. These are the web facts already gathered externally:

- BYD Seal: official BYD Israel page supports Design 313 hp and Excellence 531 hp; Israeli catalog pages may round Excellence to 530 hp. Prefer official importer value when official source is attached.
- BYD Seal U: official BYD Israel DM-i source supports Boost/Comfort 218 hp FWD and Design 324 hp AWD; Israeli iCar lists EV Comfort, EV Design, PHEV Boost, PHEV Comfort, PHEV Design.
- BYD Sealion 7: official BYD Israel page supports Boost 231 hp RWD, Comfort 313 hp RWD, Design 313 hp RWD, Excellence 531 hp AWD.
- BYD Song Plus: Israeli sources describe Song Plus as the Chinese/source name/basis of Seal U; Israeli market clean model should be Seal U. Standalone Song Plus with `local_review_source` is not clean-quality evidence.
- Cadillac Escalade IQ: official Cadillac Israel page shows Escalade IQ 2026 available through UMI, up to 750 hp, with trims Luxury Sport and Premium Luxury; official table lists both trim names.
- Cadillac XT6: official Cadillac Israel page and current Israeli catalog pages show XT6 2026, 3.6L V6, 310 hp, 9-speed automatic, AWD, trims Premium Luxury and Sport.
- Chery Arrizo 8: Israeli sources support Arrizo 8 PHEV 1.5 turbo plug-in hybrid, 347 hp, FWD, Comfort and Noble trims. Sense appears in a 2026 mention but must stay review/archive unless exact full technical field support exists.
- Chery Tiggo 8 Pro: Israeli sources support petrol Luxury/Noble 1.6 turbo 186 hp and PHEV Ultimate 1.5 turbo 318 hp. The issue is schema/type, not deletion.

---

# D. Rebuild and tests

After applying RUN 1 fixes:

1. Run the catalog build/rebuild command used by this repo for `model_technical_catalog_il.json` and related readiness/review outputs.
2. Run available tests/checks. At minimum:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
```

If exact module entrypoints differ, use the repo's documented test/build commands, but do not skip validation/readiness regeneration.

3. Confirm these RUN 1 expectations:

```text
- No list/dict value remains in version_or_trim.
- BYD Seal U has five technical rows: EV Comfort, EV Design, PHEV Boost, PHEV Comfort, PHEV Design.
- BYD Sealion 7 has four technical rows: Boost, Comfort, Design, Excellence.
- BYD Song Plus is not a standalone clean model; it is mapped as alias/lineage to Seal U and does not become unmatched.
- Cadillac Escalade IQ has two trim rows: Luxury Sport and Premium Luxury.
- Cadillac XT6 rows end in 2026.
- Chery Arrizo 8 has Comfort and Noble rows, not only Noble.
- Chevrolet Aveo no longer reports missing version_or_trim.
- EV rows no longer report engine_displacement_l missing when displacement is null by nature.
- Active/open-ended rows no longer report year_end missing when year_end is intentionally null.
- Top-level profile year_start/year_end are derived from variant rows.
- No new blockers are created from RUN 1 changes.
- unmatched_output_keys_count remains 0.
```

4. Stop after RUN 1. Do not proceed to RUN 2/blockers until user approves.



---

# PART B — RUN 2

# BATCH21 RUN 2 — Codex data-quality correction task

Temporary task file path in repo:

```text
codex_tasks/BATCH21_RUN2_CODEX_TASK.md
```

## Operating rules for Codex

1. Treat this file as the source of truth for RUN 2.
2. Do **not** browse the internet. The web validation has already been done and the verified facts/URLs are written here.
3. Apply the actions exactly in order.
4. Preserve Israeli-market grounding. If a variant is not backed by a strong Israeli source, move it to review/archive as non-blocking, not into clean.
5. After changes, rebuild the catalog/readiness/quality scan and run tests.
6. Delete this temporary task file only after a successful rebuild + test run.

## Batch state observed before RUN 2

Current uploaded ZIP state:

```text
models_ready_for_website / clean_models = 241
models_blocked = 9
review_entries = 9
ready_for_website_upload = false
last_checkpointed_profile_id = IL::Citroen::C6
unmatched_output_keys_count = 0
active split alias examples already present: Junior Elettrica, M850i, Atto 3 EVO, Escalade IQ
```

RUN 1 already covered the first 20 models in the selected recent-clean window: `BYD Dolphin` through `Chevrolet Aveo`.

RUN 2 covers the next 20 models, index window 211-230 in `data/model_technical_catalog_il.json`:

```text
Chevrolet Blazer EV
Chevrolet Bolt EV
Chevrolet Corvette
Chevrolet Cruze
Chevrolet Equinox
Chevrolet Equinox EV
Chevrolet Malibu
Chevrolet Orlando
Chevrolet Silverado
Chevrolet Spark
Chevrolet Trax
Chevrolet Volt
Chrysler 300C
Chrysler Crossfire
Chrysler Pacifica
Chrysler PT Cruiser
Chrysler Sebring
Chrysler Voyager
Citroen Ami
Citroen Berlingo
```

---

# A. Required code/reporting fixes found again in RUN 2

## A1 — FIX: derive model-level year_start/year_end from variant rows

Current value/problem:

All 20 RUN 2 clean model profiles currently have:

```json
"year_start": null,
"year_end": null
```

while their `technical_variants_il[*].year_start/year_end` contain real grounded years.

Why wrong:

The model-level range must be derived from the actual variant rows. This is a catalog quality issue, not a source issue. Leaving model-level years null makes website filters and readiness reporting less reliable.

Exact fix:

In the catalog build/repair/validation layer, after final cleaned variants are known, derive:

```python
profile["year_start"] = min(v["year_start"] for v in variants if v.get("year_start") is not None)
profile["year_end"] = max(v["year_end"] for v in variants if v.get("year_end") is not None) if any(v.get("year_end") is not None for v in variants) else None
```

Use `None` for model-level `year_end` only if at least one active/current variant legitimately has `year_end=None` and the model is still marketed/current, otherwise use the latest grounded closed year.

Action: `FIX`.

## A2 — FIX: EV engine_displacement_l must not be counted as missing grounding

Current value/problem:

EV rows such as `Chevrolet Blazer EV`, `Chevrolet Bolt EV`, `Chevrolet Equinox EV`, and `Citroen Ami` have:

```json
"engine_displacement_l": null
"missing_grounded_fields": ["engine_displacement_l", ...]
```

Why wrong:

Pure EVs do not have combustion engine displacement. `engine_displacement_l=null` is correct and should not count as a missing grounded field when `fuel_type="electric"` and `engine="electric"`.

Exact fix:

Update readiness/validation logic so `engine_displacement_l` is not required for pure EV variants. Remove `engine_displacement_l` from `missing_grounded_fields` for pure EV rows.

Action: `FIX`.

## A3 — FIX: open-ended current Israeli-market rows must not fail readiness solely because year_end is null

Current value/problem:

Current marketed rows like `Blazer EV`, `Silverado 2024+`, `Trax 2023+`, and `Citroen Ami` have `year_end=null` and are counted as missing grounded fields.

Why wrong:

For current/open-ended models, null `year_end` is the correct representation. Do not force fake current-year values.

Exact fix:

If a current Israeli source confirms current marketing/price/spec page, allow:

```json
"year_end": null
```

and remove `year_end` from `missing_grounded_fields`. Add a note: `year_end intentionally null because Israeli source shows current marketed model and no end date is published`.

Action: `FIX`.

## A4 — FIX: `version_or_trim` must always be string or null, never array/list

Current recurring schema bug:

`Chevrolet Spark` has values like:

```json
"version_or_trim": ["LT", "LTZ"]
"version_or_trim": ["LT+", "LTZ", "Premier"]
```

Why wrong:

`version_or_trim` must be a scalar string or null. Lists break website values and duplicate detection.

Exact fix:

Where a source confirms multiple real trims with the same technical powertrain, split into one row per trim, each with the same technical fields but a scalar `version_or_trim`.

Action: `FIX`.

---

# B. RUN 2 model-by-model correction instructions

## 1. Chevrolet Blazer EV

Current row:

```json
{
  "version_or_trim": "RS",
  "body_type": "SUV",
  "fuel_type": "electric",
  "engine": "electric",
  "engine_displacement_l": null,
  "horsepower_hp": 288,
  "transmission": "single_speed",
  "drivetrain": "AWD",
  "year_start": 2024,
  "year_end": null,
  "missing_grounded_fields": ["engine_displacement_l", "year_end"]
}
```

Verified Israeli sources:

- Chevrolet Israel official Blazer EV page: `https://www.chevrolet.co.il/דגמים/blazer-ev/` — RS, 455 km range, 300 hp.
- Chevrolet Israel homepage also shows BLAZER EV 2026 and 300 hp: `https://www.chevrolet.co.il/`.
- iCar article dated 2026-01-11: Blazer EV landed in Israel, 300 hp, expected price 390,000 NIS: `https://www.icar.co.il/news/ryjwfe11bzg/`.
- Cartube article dated 2026-02-07: Blazer EV RS in Israel, two electric motors, 300 hp, 455 km EPA: `https://www.cartube.co.il/חדשות-רכב/במחיר-של-389990-שקל-שברולט-בלייזר-ev-השבוע-בישראל`.
- Auto.co.il page says Blazer EV landed in Israel in February 2026: `https://www.auto.co.il/cars/chevrolet/blazer-ev/`.

What is wrong:

- `horsepower_hp=288` is not supported by the current Israeli/UMI page; Israeli sources support 300 hp.
- `year_start=2024` is not the Israeli market launch/start in the verified current sources. Israel launch/arrival is 2026.
- `engine_displacement_l=null` is correct for EV and must not be a missing field.
- `year_end=null` is correct for current marketed model and must not be a missing field.

Exact correction:

```json
{
  "version_or_trim": "RS",
  "body_type": "SUV",
  "fuel_type": "electric",
  "engine": "electric",
  "engine_displacement_l": null,
  "horsepower_hp": 300,
  "transmission": "single_speed",
  "drivetrain": "AWD",
  "year_start": 2026,
  "year_end": null,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```

Action: `FIX`.

## 2. Chevrolet Bolt EV

Current row:

```json
Premier Plus | Hatchback | electric | 204 hp | single_speed | FWD | 2021-2023
```

Verified Israeli sources already present in profile:

- Cartube: Bolt EV/EUV launched in Israel, 204 hp: `https://www.cartube.co.il/חדשות-רכב/שברולט-בולט-ev-ו-euv-בישראל-מחיר-החל-מ-134990-שקלים`
- iCar catalog page: `https://www.icar.co.il/שברולט/שברולט_בולט_EV/שברולט_בולט_EV_חדש/`

What is wrong:

- No data correction needed in the technical row.
- `engine_displacement_l=null` is correct for EV and must not be counted as missing.

Exact correction:

Keep row as-is, remove only EV false missing-grounded flags if present.

Action: `KEEP` plus reporting `FIX` for EV displacement logic.

## 3. Chevrolet Corvette

Current rows:

```json
Coupe | petrol | 6.2L v8 | 495 hp | 8-speed dual_clutch | RWD | 2022-2024 | trim null
Convertible | petrol | 6.2L v8 | 495 hp | 8-speed dual_clutch | RWD | 2022-2024 | trim null
```

Verified Israeli sources:

- Chevrolet Israel official Corvette page: `https://www.chevrolet.co.il/corvette/` — current official Corvette page, 2025, 6.2L LT2 V8.
- iCar 2026 new-car page: `https://www.icar.co.il/שברולט/שברולט_קורבט/שברולט_קורבט_חדש/version26269/` — 2026 `6.2 סטינגריי קופה 2LT`; page also lists `6.2 סטינגריי קבריולה 2LT`.
- iCar overview: official Israeli marketing began in 2023; C8 Stingray, 6.2L V8, 490 hp, 8-speed dual-clutch, RWD: `https://www.icar.co.il/שברולט/שברולט_קורבט/שברולט_קורבט_יד_שניה_ד10/`.
- Cartube launch article dated 2023-06-18: first official import, C8 Stingray, 490 hp, Z51 package, Coupe and Convertible: `https://www.cartube.co.il/חדשות-רכב/שברולט-קורבט-c8-החדשה-2023-בישראל-מחיר-779000-שקל`.
- Auto.co.il launch article dated 2023-06-18: regular import to Israel, Coupe and Convertible, V8, 490 hp: `https://www.auto.co.il/articles/car-news/local-news/136299/`.
- Auto.co.il 2026 model page: 6.2 V8, RWD, 490 hp: `https://www.auto.co.il/cars/chevrolet/corvette/2026/580122/`.

What is wrong:

- `horsepower_hp=495` is not the regular Israeli official source value; Israeli iCar/Cartube/Auto support 490 hp.
- `year_start=2022` is not the official Israeli import start; Israeli official import began in 2023.
- `year_end=2024` is stale; official/current sources show 2025/2026 availability.
- `version_or_trim=null` is too weak because Israeli sources identify the marketed trim as `Stingray 2LT` for both Coupe and Convertible.

Exact correction:

Replace the two rows with:

```json
{
  "version_or_trim": "Stingray 2LT",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "6.2L V8",
  "engine_displacement_l": 6.2,
  "horsepower_hp": 490,
  "transmission": "8-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2023,
  "year_end": null,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```

```json
{
  "version_or_trim": "Stingray 2LT",
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "6.2L V8",
  "engine_displacement_l": 6.2,
  "horsepower_hp": 490,
  "transmission": "8-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2023,
  "year_end": null,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```

Action: `FIX`.

## 4. Chevrolet Cruze

Current rows:

10 technical rows covering Sedan/Hatchback/Estate, 1.6/1.8/1.4T petrol, 6-speed automatic, FWD, 2009-2019.

Verified Israeli sources:

- iCar 2009-2016 Cruze page: `https://www.icar.co.il/שברולט/שברולט_קרוז/שברולט_קרוז_יד_שניה_ד10/` — 6-speed tiptronic/automatic and earlier engine generation.
- iCar 2016 LT 1.4 turbo page: `https://www.icar.co.il/שברולט/שברולט_קרוז/שברולט_קרוז_יד_שניה_ד10/version5462/`.
- iCar 2016-2020 overview: `https://www.icar.co.il/שברולט/שברולט_קרוז/`.

What is wrong:

- The final-generation Cruze rows in the current catalog end at 2019, while the Israeli iCar overview labels the generation as 2016-2020.

Exact correction:

Update only the final-generation 1.4L turbo 153 hp rows:

```text
Sedan 1.4L turbo 153 hp 6-speed automatic FWD: year_end 2019 -> 2020
Hatchback 1.4L turbo 153 hp 6-speed automatic FWD: year_end 2019 -> 2020
```

Keep the earlier 2009-2016 and Estate 2013-2015 rows as currently represented unless tests show a local source conflict.

Action: `FIX` for final-generation year_end; `KEEP` for all other Cruze rows.

## 5. Chevrolet Equinox

Current rows:

```json
2.4L petrol 182 hp 6AT FWD 2016-2017 trim null
1.5L turbo petrol 170 hp 6AT FWD 2018-2024 trim null
```

Verified Israeli sources:

- iCar 2016-2017 page: `https://www.icar.co.il/שברולט/שברולט_אקווינוקס/שברולט_אקווינוקס_יד_שניה_ד10/`.
- iCar 2018-2024 page: `https://www.icar.co.il/שברולט/שברולט_אקווינוקס/שברולט_אקווינוקס_יד_שניה_ד11/` — 1.5L 170 hp, 6-speed automatic.
- iCar 2022 RS page lists Israeli versions including `1.5 LT+ 4X4`, `1.5 RS`, and `1.5 RS 4X4`: `https://www.icar.co.il/שברולט/שברולט_אקווינוקס/שברולט_אקווינוקס_יד_שניה_ד11/version25657/`.
- Chevrolet Israel page: `https://www.chevrolet.co.il/equinox/`.

What is wrong:

- The 1.5L 2018-2024 generation is missing an AWD/4X4 technical variant even though Israeli iCar version pages list `LT+ 4X4` and `RS 4X4`.
- `version_or_trim=null` is acceptable only if this catalog groups by technical powertrain; do not invent a single trim for all rows.

Exact correction:

Keep existing rows and add the missing AWD technical row:

```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 170,
  "transmission": "6-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2018,
  "year_end": 2024,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```

Add note: `Israeli iCar pages list 4X4 trims for the 1.5L generation; catalog stores this as a separate technical drivetrain variant rather than a marketing-trim split.`

Action: `FIX`.

## 6. Chevrolet Equinox EV

Current rows:

```json
RS | Crossover | electric | 210 hp | single_speed | FWD | 2024-2025
RS | Crossover | electric | 290 hp | single_speed | AWD | 2024-2025
```

Verified Israeli sources:

- iCar Equinox EV page: `https://www.icar.co.il/Chevrolet/Chevrolet_Equinox_EV/`.
- Cartube exposure article: FWD 210 hp and AWD 290 hp: `https://www.cartube.co.il/חדשות-רכב/שברולט-אקווינוקס-ev-החשמלי-2023-נחשף`.
- Chevrolet Israel/UMI PDF already present in profile: `https://chevrolet.co.il/wp-content/uploads/Equinox-EV-Spec-IL.pdf`.

What is wrong:

- No technical row correction needed.
- `engine_displacement_l=null` must not be counted as missing for EVs.

Exact correction:

Keep both RS FWD/AWD rows. Remove EV false missing-grounded flags only.

Action: `KEEP` plus reporting `FIX`.

## 7. Chevrolet Malibu

Current rows:

6 technical rows covering 2008-2023: 3.5 V6 LTZ, 2.4 LT, 2.0T LTZ, 1.5T LT, 2.0T LTZ, 1.5T LT CVT.

Verified Israeli sources:

- Auto.co.il 2008-2012: `https://www.auto.co.il/model/chevrolet-malibu_g264`.
- Cartube 2016 launch article: 1.5T 160 hp, 6AT; outgoing 2.0T 259 hp: `https://www.cartube.co.il/חדשות-רכב/שברולט-מאליבו-החדשה-2016-בישראל`.
- iCar 2016-2023 page: `https://www.icar.co.il/שברולט/שברולט_מאליבו/שברולט_מאליבו_דור_9/`.
- Gear 2019 update: `https://www.gear.co.il/חדשות_רכב/2019-03-25-שברולט-מאליבו-2019-החדשה-בישראל`.

What is wrong:

- No confirmed correction required from RUN 2 review.

Exact correction:

Keep all Malibu rows as-is, but ensure model-level year range derives to 2008-2023.

Action: `KEEP`.

## 8. Chevrolet Orlando

Current rows:

```json
LT | MPV | diesel | 2.0L turbo | 163 hp | 6AT | FWD | 2012-2018
LT Plus | MPV | petrol | 1.4L turbo | 140 hp | 6AT | FWD | 2014-2018
```

Verified Israeli sources:

- iCar 2014 1.4 turbo petrol LT page: `https://www.icar.co.il/שברולט/שברולט_אורלנדו/שברולט_אורלנדו_יד_שניה_ד10/version11882/` — 140 hp.
- Auto.co.il 2014 page: `https://www.auto.co.il/cars/chevrolet/orlando/2014/` — 2.0 turbo-diesel 163 hp, 6AT.
- Gear 2014 page lists 2.0 turbo-diesel LT automatic 163 hp, 1.4 turbo LS automatic 140 hp, and 1.4 turbo LT automatic 140 hp: `https://www.gear.co.il/גרסה/שברולט/אורלנדו/2014/אורלנדו/2.0-טורבו-דיזל-LT-אוטומט`.
- Cartube 1.4 turbo launch article already in profile: `https://www.cartube.co.il/חדשות-רכב/שברולט-אורלנדו-1-4-טורבו-בישראל-מחיר-החל-מ-162-900-שקל`.

What is wrong:

- `LT Plus` is not supported by the verified 1.4T Israeli pages I found. The sources support `LT` and also `LS` for the petrol 1.4T. Do not keep an unsupported `LT Plus` trim in clean.

Exact correction:

Replace current petrol row:

```json
"version_or_trim": "LT Plus"
```

with two scalar rows:

```json
{
  "version_or_trim": "LS",
  "body_type": "MPV",
  "fuel_type": "petrol",
  "engine": "1.4L turbo",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 140,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2014,
  "year_end": 2018,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```

```json
{
  "version_or_trim": "LT",
  "body_type": "MPV",
  "fuel_type": "petrol",
  "engine": "1.4L turbo",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 140,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2014,
  "year_end": 2018,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```

Keep the diesel LT 2.0 row.

Action: `FIX`.

## 9. Chevrolet Silverado

Current rows:

4 diesel 6.6L V8 turbo rows covering 2014-current: 397 hp 6AT, 445 hp 6AT, 445 hp 10AT, 470 hp 10AT.

Verified Israeli sources:

- Chevrolet Israel official Silverado page: `https://www.chevrolet.co.il/silverado/` — 2026 Silverado, 6.6L Duramax V8 turbo diesel, 470 hp, 10-speed transmission.
- Carzone 2026 price/spec page: `https://www.carzone.co.il/Chevrolet/Silverado/`.
- iCar new Silverado page: `https://www.icar.co.il/שברולט/שברולט_סילברדו/שברולט_סילברדו_חדש/`.
- Queen of the Road 2023/24 facelift article: 6.6L V8 turbo-diesel, 470 hp, 10-speed Allison: `https://www.queenoftheroad.co.il/שברולט-סילברדו-2023-24-מתיחת-פנים-החל-מ-245000-שקל/`.

What is wrong:

- No row correction needed for technical values.
- `year_end=null` on the latest 470 hp row is correct current/open-ended and must not be counted as missing.

Exact correction:

Keep all Silverado rows. Ensure latest row has `missing_grounded_fields=[]` and note `current official page confirms 470 hp current marketed Silverado`.

Action: `KEEP` plus reporting `FIX` for current year_end logic.

## 10. Chevrolet Spark

Current rows have illegal list values:

```json
["LS"] | 1.0L 68 hp manual | 2011-2015
["LT", "LTZ"] | 1.2L 82 hp manual | 2011-2015
["LT"] | 1.0L 74 hp manual | 2016-2018
["LT+", "LTZ", "Premier"] | 1.4L 98 hp CVT | 2016-2022
```

Verified Israeli sources:

- iCar 2011-2015 Spark page: `https://www.icar.co.il/שברולט/שברולט_ספארק_עד_2015/`.
- iCar 2016-2022 Spark page: `https://www.icar.co.il/שברולט/שברולט_ספארק/` — 1.4L petrol/CVT.
- Cartube 2016 launch article: `https://www.cartube.co.il/חדשות-רכב/שברולט-ספארק-החדשה-2016-בישראל-מחיר-החל-מ-60900-שקל`.
- Auto.co.il Spark page states current used-market trims include `LT+` and `Premier`, and 2023 was last year marketed in Israel: `https://www.auto.co.il/cars/chevrolet/spark/`.

What is wrong:

- `version_or_trim` is a list, violating schema.
- Final row year_end 2022 is probably stale because Auto.co.il states 2023 was the last year of Israeli marketing.

Exact correction:

Split to scalar trim rows:

```text
LS | Hatchback | petrol | 1.0L | 68 hp | manual | FWD | 2011-2015
LT | Hatchback | petrol | 1.2L | 82 hp | manual | FWD | 2011-2015
LTZ | Hatchback | petrol | 1.2L | 82 hp | manual | FWD | 2011-2015
LT | Hatchback | petrol | 1.0L | 74 hp | manual | FWD | 2016-2018
LT+ | Hatchback | petrol | 1.4L | 98 hp | cvt | FWD | 2016-2023
LTZ | Hatchback | petrol | 1.4L | 98 hp | cvt | FWD | 2016-2023
Premier | Hatchback | petrol | 1.4L | 98 hp | cvt | FWD | 2016-2023
```

Important:

- Every row must use a string `version_or_trim`, not a list.
- Rebuild `available_values_for_website.version_or_trim` from scalar rows.
- Do not leave any Spark row with `version_or_trim` as array.

Action: `FIX`.

## 11. Chevrolet Trax

Current rows:

```json
null | SUV | petrol | 1.8L i4 | 140 hp | 6AT | FWD | 2013-2016
null | SUV | petrol | 1.4L turbo i4 | 140 hp | 6AT | FWD | 2013-2020
null | SUV | petrol | 1.2L turbo i3 | 139 hp | 6AT | FWD | 2023-null
```

Verified Israeli sources:

- Chevrolet Israel official Trax page: `https://www.chevrolet.co.il/trax/` — 2026 Trax, 1.2L three-cylinder turbo, 139 hp, 6-speed automatic; trims `1RS` and `2RS`.
- Cartube 2023 launch article: `https://www.cartube.co.il/חדשות-רכב/שברולט-טראקס-החדש-2023-בישראל-מחיר-החל-מ-130990-שקלים` — 1.2 turbo, 139 hp, 6AT, FWD.
- iCar old Trax page: `https://www.icar.co.il/שברולט/שברולט_טראקס_ישן/מפרט/`.

What is wrong:

- Current 2023+ Trax row has `version_or_trim=null` even though the official current Israeli page clearly lists `1RS` and `2RS`.
- `year_end=null` is correct for current marketed model and must not be counted as missing.

Exact correction:

Keep the old 1.8L and 1.4T rows as technical engine rows. Replace the current 2023+ null-trim row with two rows:

```json
{
  "version_or_trim": "1RS",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.2L turbo i3",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 139,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2023,
  "year_end": null,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```

```json
{
  "version_or_trim": "2RS",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.2L turbo i3",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 139,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2023,
  "year_end": null,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```

Action: `FIX`.

## 12. Chevrolet Volt

Current row:

```json
Hatchback | plug_in_hybrid | 1.4L | 150 hp | automatic | FWD | 2011-2012 | trim null
```

Verified Israeli sources:

- iCar Volt page: `https://www.icar.co.il/שברולט/שברולט_וולט/`.
- Auto.co.il Volt 2011-2012 page: `https://www.auto.co.il/model/chevrolet-volt_g157`.

What is wrong:

- No confirmed correction required.

Exact correction:

Keep row as-is. Ensure model-level year range derives to 2011-2012.

Action: `KEEP`.

## 13. Chrysler 300C

Current rows:

```json
null | Sedan | petrol | 3.5L V6 | 249 hp | automatic | RWD | 2005-2011
null | Sedan | petrol | 3.6L V6 | 282 hp | automatic | RWD | 2012-2023
SRT8 | Sedan | petrol | 6.4L V8 | 470 hp | automatic | RWD | 2012-2015
```

Verified Israeli sources:

- iCar 2012-2016 300/300C overview says the second generation is already called Chrysler 300, not 300C: `https://www.icar.co.il/קרייזלר/קרייזלר_300C/קרייזלר_300C_יד_שניה_ד11/`.
- iCar 2016 page lists `3.6 Limited`, `3.6 Luxury`, and `3.6`: `https://www.icar.co.il/קרייזלר/קרייזלר_300C/קרייזלר_300C_יד_שניה_ד11/version15422/`.
- Carzone 2016 page states 3.6 Limited, 282 hp, 3604 cc, RWD: `https://www.carzone.co.il/Chrysler/300/2016/`.

What is wrong:

- The 2012+ 3.6 row has `version_or_trim=null`, but Israeli sources verify at least `Limited` for the 3.6 row.
- Model naming is mixed in Israeli sources (`300C` URL / `300` content). Do not create a blocker; keep current model label for now unless a larger split/alias task handles Chrysler 300 vs 300C.

Exact correction:

Change the 2012+ 3.6 V6 row:

```json
"version_or_trim": null
```

to:

```json
"version_or_trim": "Limited"
```

Keep SRT8. Keep 2005-2011 3.5 row with trim null unless a direct Israeli source confirms a scalar trim.

Action: `FIX` for 2012+ trim; `KEEP` otherwise.

## 14. Chrysler Crossfire

Current rows:

```json
Limited | Coupe | petrol | 3.2L V6 | 215 hp | automatic | RWD | 2004-2008
Limited | Roadster | petrol | 3.2L V6 | 215 hp | automatic | RWD | 2005-2008
```

Verified Israeli sources:

- iCar 2005 3.2 page: `https://www.icar.co.il/קרייזלר/קרייזלר_קרוספייר/קרייזלר_קרוספייר_יד_שניה_ד10/version484/`.
- Gear 2005 Crossfire coupe 3.2 V6 Limited automatic page: `https://www.gear.co.il/מחירון-רכב-דגם/קרייזלר/קרוספייר/2005/קרוספייר-קופה/3.2-V6-לימיטד-אוטומט-`.
- iCar general Crossfire page already in profile: `https://www.icar.co.il/קרייזלר/קרייזלר_קרוספייר/`.

What is wrong:

- No confirmed correction required.

Exact correction:

Keep both rows.

Action: `KEEP`.

## 15. Chrysler Pacifica

Current rows:

```json
Limited | MPV | petrol | 3.6L V6 | 280 hp | 9AT | FWD | 2018-2024
Hybrid Limited | MPV | plug_in_hybrid | 3.6L V6 | 260 hp | CVT | FWD | 2019-2024
```

Verified Israeli sources:

- iCar overview: 2018-2022 Pacifica, 3.6L V6, 280 hp, 9-speed automatic: `https://www.icar.co.il/קרייזלר/קרייזלר_פסיפיקה/קרייזלר_פסיפיקה_יד_שניה_ד10/`.
- iCar 2022 page lists `Touring L 3.6` and `Limited 3.6`: `https://www.icar.co.il/קרייזלר/קרייזלר_פסיפיקה/קרייזלר_פסיפיקה_יד_שניה_ד10/version24993/`.
- Auto.co.il 2019 page states two trims, `Touring L` and `Limited`: `https://www.auto.co.il/cars/chrysler/pacifica/2019/`.
- iCar 2018 launch article: marketed in Israel with `Touring L` and `Limited`: `https://www.icar.co.il/חדשות_רכב/קרייזלר_פסיפיקה_בישראל:_מ-290,000_שקל/`.
- Carzone 2022/2025 pages list Touring L variants: `https://www.carzone.co.il/Chrysler/Pacifica/2022/`, `https://www.carzone.co.il/Chrysler/Pacifica/2025/`.
- iCar 2026 news says Pacifica was marketed in Israel before and it is unclear whether import will resume; not a confirmation of current new official marketing: `https://www.icar.co.il/news/rytn7bnj11l/`.

What is wrong:

- The clean catalog is missing `Touring L 3.6` even though Israeli sources verify it alongside Limited.
- The `Hybrid Limited` PHEV row is not backed by a sufficiently strong Israeli catalog/editorial source in my RUN 2 web validation. I found weak/local listing evidence only, not enough to keep it in clean under the user's rule.
- `year_end=2024` is weak/stale for clean unless strongly grounded. iCar overview covers 2018-2022; later Carzone listings may include later marketplace/import entries. Do not use a weak current listing to force clean.

Exact correction:

Add missing petrol trim row:

```json
{
  "version_or_trim": "Touring L",
  "body_type": "MPV",
  "fuel_type": "petrol",
  "engine": "3.6L V6",
  "engine_displacement_l": 3.6,
  "horsepower_hp": 280,
  "transmission": "9-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2018,
  "year_end": 2022,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```

Update Limited petrol row year range to the strongly grounded iCar/Auto clean range unless additional existing source in the file directly proves 2024:

```text
Limited petrol 3.6: year_start 2018, year_end 2022
```

Move this row out of clean to review/archive as non-blocking unless Codex finds an already-present strong Israeli source in the repo data that explicitly supports it:

```json
Hybrid Limited | plug_in_hybrid | 3.6L V6 | 260 hp | CVT | FWD | 2019-2024
```

Review reason:

```text
Insufficient strong Israeli-market source found in RUN 2 for Pacifica PHEV/Hybrid Limited technical row. Do not delete history; move to non-blocking review/archive.
```

Action: `FIX` + `MOVE TO REVIEW` for Hybrid Limited unless already-present source proves it strongly.

## 16. Chrysler PT Cruiser

Current rows:

```json
null | Hatchback | petrol | 2.0L | 141 hp | automatic | FWD | 2000-2004
null | Hatchback | petrol | 2.4L | 143 hp | automatic | FWD | 2004-2010
```

Verified Israeli sources:

- iCar 2004 2.0 page: `https://www.icar.co.il/קרייזלר/קרייזלר_PT_קרוזר/קרייזלר_PT_קרוזר_יד_שניה_ד10/version7067/`.
- iCar general PT Cruiser page already in profile: `https://www.icar.co.il/Chrysler/Chrysler_PT_Cruiser/Chrysler_PT_Cruiser_yad_shniya/`.
- Auto.co.il general page already in profile: `https://www.auto.co.il/model/chrysler-pt-cruiser_g196`.

What is wrong:

- No confirmed correction required. Null trim is acceptable here because the Israeli sources primarily identify engine/body years, not a robust scalar marketed trim for all years.

Exact correction:

Keep both rows.

Action: `KEEP`.

## 17. Chrysler Sebring

Current rows:

```json
Limited | Sedan | 2.7L V6 | 203 hp | 4AT | FWD | 2001-2006
Limited | Convertible | 2.7L V6 | 203 hp | 4AT | FWD | 2001-2006
Touring | Sedan | 2.4L | 170 hp | 4AT | FWD | 2007-2011
Limited | Convertible | 2.7L V6 | 186 hp | 6AT | FWD | 2007-2011
```

Verified Israeli sources:

- iCar 2008-2009 Sebring page: `https://www.icar.co.il/קרייזלר/קרייזלר_סברינג/קרייזלר_סברינג_יד_שניה_ד10/` — 2.7L V6, about 188 hp, Israeli marketing began January 2008 for that generation.
- Auto.co.il 2007-2011 page already in profile: `https://www.auto.co.il/model/chrysler-sebring_g174`.
- Auto.co.il 2001-2006 page already in profile: `https://www.auto.co.il/model/chrysler-sebring_g175`.
- iCar general page already in profile: `https://www.icar.co.il/קרייזלר/קרייזלר_סברינג/`.

What is wrong:

- The current 2007-2011 Limited Convertible row says 186 hp, while iCar summary says 188 hp. This can be rounding/source convention. Do not change unless one of the already indexed field-level sources explicitly supports 188 over 186.

Exact correction:

Keep all rows as-is for now. If the indexed source field for horsepower is weak or missing, prefer 188 hp for the 2007-2011 2.7 V6 row; otherwise keep current 186 hp.

Action: `KEEP`, with optional source-consistency check only against already stored source data.

## 18. Chrysler Voyager

Current rows:

```json
LE | MPV | 3.3L V6 | 158 hp | 4AT | FWD | 1996-2000
LX | MPV | 3.3L V6 | 174 hp | 4AT | FWD | 2001-2007
Touring | MPV | 3.8L V6 | 193 hp | 6AT | FWD | 2008-2011
Touring | MPV | 3.6L V6 | 283 hp | 6AT | FWD | 2011-2015
```

Verified Israeli sources:

- iCar 2015 Grand Voyager page lists 3.8 LX/Touring and 3.6 Touring levels: `https://www.icar.co.il/קרייזלר/קרייזלר_גרנד_וויאג'ר/קרייזלר_גרנד_וויאג'ר_יד_שניה_ד10/version13642/`.
- Auto.co.il Grand Voyager page states facelift arrived to Israel in June 2011 and improved powertrain: `https://www.auto.co.il/cars/chrysler/grand-vayoger/`.
- Yad2/Levi listing shows LX 3.3 174, LX 3.8 193, Limited 3.6 279, Touring 3.6 279/283 style entries: `https://www.yad2.co.il/vehicles/cars?manufacturer=49&model=10729`.

What is wrong:

- The profile/model name is `Voyager` while sources are overwhelmingly `Grand Voyager` for the Israeli model. This may be a canonical naming/alias issue, not a technical-row error.

Exact correction:

Do not delete rows. Add model alias/lineage:

```json
"canonical_model": "Grand Voyager"
```

or, if the project convention keeps model key stable, add an alias mapping:

```text
Chrysler Voyager -> Chrysler Grand Voyager
```

Keep technical rows.

Action: `FIX` alias/canonical naming, `KEEP` technical rows.

## 19. Citroen Ami

Current row:

```json
null | Hatchback | electric | electric | 8 hp | single_speed | FWD | 2024-null
missing_grounded_fields: ["engine_displacement_l", "year_end"]
```

Verified sources:

- Auto.co.il Ami Buggy / Ami technical article states 8 hp, 50 km/h, 5.5 kWh battery, 75 km range: `https://www.auto.co.il/articles/test-drives/first-drives/136674/`.
- iCar Citroen Ami page in profile: `https://www.icar.co.il/סיטרואן/סיטרואן_אמי/`.
- Cartube Ami Israel page in profile: `https://www.cartube.co.il/חדשות-רכב/סיטרואן-אמי-החשמלית-בישראל`.

What is wrong:

- `engine_displacement_l=null` is correct EV behavior and must not be missing.
- `year_end=null` is correct if represented as current/open-ended.
- Body type `Hatchback` is acceptable for the website schema if no microcar/quadricycle body type is supported, but add a note that this is a micro-EV/quadricycle normalized to Hatchback.

Exact correction:

Keep technical row and set:

```json
"missing_grounded_fields": []
```

Add note:

```text
Citroen Ami is a micro-EV/quadricycle; body_type normalized to Hatchback for current schema.
```

Action: `KEEP` plus reporting `FIX`.

## 20. Citroen Berlingo

Current rows:

8 diesel van rows covering 1996-2024, including 1.5L turbo-diesel 75/100 manual and 130 automatic for 2018-2024.

Verified Israeli sources:

- iCar current/new Berlingo page: `https://www.icar.co.il/סיטרואן/סיטרואן_ברלינגו/סיטרואן_ברלינגו_חדש/` — current generation arrived in Israel in 2019; 1.5L diesel 100 manual and 130 hp 8-speed automatic; also electric 136 hp.
- iCar 2019-2025 used/current generation page: `https://www.icar.co.il/סיטרואן/סיטרואן_ברלינגו/סיטרואן_ברלינגו_יד_שניה_ד12/` — 75/100/130 hp diesel, 130 hp with 8-speed automatic.
- Cartube 2019 launch: 1.5 BlueHDi 75/100/130, 130 hp with 8-speed AISIN automatic: `https://www.cartube.co.il/חדשות-רכב/סיטרואן-ברלינגו-shine-החדש-2019-בישראל-מחיר-145990-שקל`.
- Auto.co.il 2019 launch: 1.5 diesel 75/100/130, manual for lower two and 8-speed automatic for 130; also mentions petrol options: `https://www.auto.co.il/articles/car-news/local-news/132220/`.

What is wrong:

- Current catalog lacks the current electric Berlingo/e-Berlingo row even though iCar current/new page confirms an electric version with 136 hp and 269 km range.
- The 1.5L diesel rows start at 2018, while Israeli sources say the new generation arrived in Israel in 2019. Do not use 2018 unless there is a direct Israeli source inside the repo supporting local 2018 availability.

Exact correction:

Update the three 1.5L diesel rows:

```text
1.5L turbo diesel 75 hp manual: year_start 2018 -> 2019
1.5L turbo diesel 100 hp manual: year_start 2018 -> 2019
1.5L turbo diesel 130 hp automatic: transmission automatic -> 8-speed automatic, year_start 2018 -> 2019
```

Add current electric Berlingo technical row if the project schema allows current passenger/commercial van EV rows:

```json
{
  "version_or_trim": null,
  "body_type": "Van",
  "fuel_type": "electric",
  "engine": "electric",
  "engine_displacement_l": null,
  "horsepower_hp": 136,
  "transmission": "single_speed",
  "drivetrain": "FWD",
  "year_start": 2024,
  "year_end": null,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```

If the schema separates e-Berlingo as a separate model/profile, then action is `SPLIT` into `Citroen e-Berlingo` / alias lineage from `Berlingo electric`, not delete.

Action: `FIX` + possible `SPLIT` for electric Berlingo depending on existing model convention.

---

# C. Required rebuild and tests

After applying RUN 2:

```bash
python -m scripts.run_model_catalog
python -m scripts.catalog_quality_scan
pytest -q
```

Also run or inspect whichever command currently generates:

```text
data/model_technical_catalog_il_readiness.json
data/model_technical_catalog_il_quality_scan.json
data/model_technical_catalog_il_review.json
```

Expected RUN 2 local improvements:

```text
No RUN 2 row has version_or_trim as list/array.
Pure EV rows no longer count engine_displacement_l=null as missing grounded field.
Current open-ended rows no longer count year_end=null as missing when current Israeli source is present.
RUN 2 model-level year_start/year_end are derived from variants.
Chevrolet Blazer EV = RS, 300 hp, Israeli year_start 2026.
Chevrolet Corvette = Stingray 2LT, 490 hp, Israeli year_start 2023, current/open-ended.
Chevrolet Spark scalar trim rows only.
Chevrolet Trax current rows split into 1RS and 2RS.
Chevrolet Equinox includes missing AWD technical variant.
Chevrolet Orlando petrol 1.4T uses supported LS/LT, not unsupported LT Plus.
Chrysler Pacifica includes Touring L; unsupported PHEV is moved to non-blocking review unless strong existing source proves it.
Citroen Berlingo 2019+ diesel start corrected and e-Berlingo handled via add/split.
```

Final target remains:

```text
models_blocked = 0
review_only_blocked_entries = 0
duplicate_technical_variants = 0
invalid_source_references = 0
unknown_support_values = 0
ready_for_website_upload = true
unmatched_output_keys_count = 0
unmatched_output_keys_sample = []
active blocked = 0
```


---

# PART C — RUN 3

# BATCH 21 — RUN 3 Codex Task

Temporary task file path in repo:

```text
codex_tasks/BATCH21_RUN3_CODEX_TASK.md
```

## Operating rules for Codex

1. Treat this file as the source of truth for RUN 3.
2. Do **not** browse the internet. The web validation has already been performed outside Codex; the verified facts and source URLs are written below.
3. RUN 3 scope is: active blockers, review-only blockers, split aliases/unmatched output keys, duplicate/split leftovers, casing leftovers, and code/reporting fixes needed so the final readiness metrics are not falsely red.
4. Apply the actions exactly in order. Do not invent unsupported Israeli-market variants.
5. If a variant does not have enough Israeli-market grounding, move it to a non-blocking archive/review bucket; do **not** keep it as an active blocker and do **not** force it into clean.
6. After changes, rebuild catalog/readiness/review/quality scan and run tests.
7. Delete this temporary file only after successful rebuild + tests.

---

# 0. Batch state observed in uploaded ZIP

Files inspected:

```text
data/model_technical_catalog_il.json
data/model_technical_catalog_il_readiness.json
data/model_technical_catalog_il_review.json
data/model_technical_catalog_il_quality_scan.json
data/validated_vehicle_variants_full_gemini31_v1.checkpoint.json
data/validation_run_summary_gemini31.json
scripts/catalog_builder.py
app.py
```

Actual state from the ZIP:

```text
clean_models = 241
models_blocked = 9
review_entries = 9
review_only_blocked_entries = 9
ready_for_website_upload = false
technical_variants_total = 801
technical_variants_with_sources = 801
technical_variants_with_field_sources = 801
technical_variants_missing_required_grounding = 4
technical_variants_missing_grounded_fields = 104
invalid_source_references = 0
unknown_support_values = 0
duplicate_technical_variants = 0
last_checkpointed_profile_id = IL::Citroen::C6
resume_after_key = IL|Citroen|C6
next_key_to_process = IL|Citroen|C8
unmatched_output_keys_count = 0
unmatched_output_keys_sample = []
split_profile_alias_count = 5
quality_scan_stale = true
```

Active review-only blockers in `data/model_technical_catalog_il_review.json`:

```text
Chery Tiggo 4 Pro
Chery Tiggo 9
Chevrolet Camaro
Chevrolet Captiva
Chevrolet Tahoe
Chevrolet Traverse
Citroen C3 Picasso
Citroen C4 X
Citroen C5 Aircross
```

Known split aliases already present and legitimate; preserve them:

```text
IL|Alfa Romeo|Junior Elettrica -> IL|Alfa Romeo|Junior
IL|BMW|M850i -> IL|BMW|850i
IL|BMW|X5 xDrive30d -> IL|BMW|X5 3.0d
IL|BYD|Atto 3 EVO -> IL|BYD|Atto 3
IL|Cadillac|Escalade IQ -> IL|Cadillac|Escalade
```

---

# 1. Required code/reporting fixes before data fixes

## 1.1 FIX: distinguish non-blocking archive/review from active blockers

Current problem:

`model_technical_catalog_il_review.json` is currently counted as active blocking output. This is wrong for entries that are intentionally moved out of clean because Israeli grounding is insufficient.

Exact fix:

- Add a clear non-blocking state, for example:

```json
"publication_state": "archive_non_blocking"
```

or

```json
"blocking_status": "non_blocking_review"
```

- `compute_resume_state()` and readiness generation must count as active blockers **only** entries whose `blocking_status` is unresolved/blocking.
- Entries moved to archive/non-blocking review must not increment:

```text
models_blocked
review_only_blocked_entries
active_blocked_count
```

- They may remain in a separate audit file or audit section, but the final readiness target must allow:

```text
models_blocked = 0
review_only_blocked_entries = 0
active blocked = 0
ready_for_website_upload = true
```

Rule: do not delete historical uncertainty. Preserve it as non-blocking audit/archive.

## 1.2 FIX: `year_end = null` for currently sold models must not be a missing grounded field

Current problem:

Rows such as current EVs/current models get `missing_grounded_fields: ["year_end"]`, causing false red warnings.

Exact fix:

- If Israeli source says the model is currently offered / appears in current official importer catalog / current price list, keep `year_end: null` and do **not** include `year_end` in `missing_grounded_fields`.
- Add field-source semantics such as:

```json
"field_sources": { "year_end": [] },
"open_ended_current_model": true
```

or do not require `field_sources.year_end` when `year_end` is intentionally null.

## 1.3 FIX: `engine_displacement_l = null` for EV must not be missing

Current problem:

EV rows are flagged as missing displacement.

Exact fix:

- For `fuel_type = electric` and `engine = electric`, keep:

```json
"engine_displacement_l": null
```

- Do not list `engine_displacement_l` in `missing_grounded_fields`.

## 1.4 FIX: model-level years must be derived from variants

Current problem:

Some model profiles have top-level:

```json
"year_start": null,
"year_end": null
```

while `technical_variants_il[*].year_start/year_end` are populated.

Exact fix:

- `model.year_start = min(non-null variant.year_start)`.
- `model.year_end = null` if any current/open-ended variant has `year_end = null`; otherwise `max(non-null variant.year_end)`.
- Apply to all clean profiles and repaired blockers.

## 1.5 FIX: normalize BMW casing globally

Current problem found in clean catalog:

```text
make = "Bmw"
model = "850i"
make = "Bmw"
model = "z4 sdrive20i"
```

There are already proper `BMW` entries, so `Bmw` is a casing leak and can also create duplicate/unmatched identity problems.

Exact fix:

- Convert every `make: "Bmw"` to `make: "BMW"`.
- Convert `model: "z4 sdrive20i"` to canonical model casing `Z4 sDrive20i` **only if the project uses engine-grade model splits**; otherwise merge/alias it under `Z4` with `version_or_trim = "sDrive20i"`.
- Remove duplicate clean profile `Bmw 850i` if it duplicates `BMW M850i` split profile. Do not keep both `Bmw 850i` and `BMW M850i` with the same 2018-2024 M850i xDrive variants.
- Preserve historical `BMW 850i` 1990-1994 V12 row separately; it is not the same as modern `M850i`.

---

# 2. RUN 3 blocker data fixes

## 2.1 Chery Tiggo 4 Pro — FIX + SPLIT

Current value/problem in review:

- Top-level `technical_variants_il` is empty, so the profile is active-blocked.
- A nested `model_catalog.technical_variants_il` exists but contains stale/wrong data:

```json
"engine": "1.5L turbo",
"horsepower_hp": 147,
"version_or_trim": null,
"year_start": 2024,
"year_end": 2025
```

Why wrong:

Israeli current/launch sources do **not** support the 147 hp turbo row for Israeli Tiggo 4 Pro. Israeli official/current sources support Tiggo 4 Pro petrol with 1.5L, 95 hp, CVT, FWD, plus a separate Tiggo 4 HEV lineup.

Validated Israeli sources:

- Chery Israel official Tiggo 4 Pro page: 1.5L, 95 hp, automatic CVT.
  URL: `https://cheryisrael.co.il/models/tiggo4pro/`
- Chery Israel official price list: `TIGGO 4 Pro Comfort`; separate `TIGGO 4 HEV Comfort`, `Luxury`, `Noble`.
  URL: `https://cheryisrael.co.il/pricing/`
- Cartube launch article 24 Dec 2024: Tiggo 4 Pro launched in Israel with one `Noble` trim, 1.5L 95 hp, CVT.
  URL: `https://www.cartube.co.il/חדשות-רכב/צ-רי-טיגו-4-פרו-נחת-בישראל-מחיר-120990-שקל`
- iCar current catalog: petrol 1.5 95 hp CVT FWD and current versions include petrol Comfort plus Tiggo 4 HEV Comfort/Luxury/Noble.
  URL: `https://www.icar.co.il/צ'רי/צ'רי_טיגו_4_פרו/צ'רי_טיגו_4_פרו_חדש/`

Exact action:

- Action: `FIX + SPLIT`
- Do **not** promote the stale nested 147 hp turbo row.
- Replace it with current Israeli-backed rows:

```json
{
  "version_or_trim": "Comfort",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.5L petrol",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 95,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2025,
  "year_end": null,
  "support_level": "direct"
}
```

- Optional historical row only if preserving launch configuration:

```json
{
  "version_or_trim": "Noble",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.5L petrol",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 95,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2024,
  "year_end": 2025,
  "support_level": "direct"
}
```

- Add separate hybrid rows under the same model only if the catalog treats `Tiggo 4 HEV` as part of `Tiggo 4 Pro`; otherwise split to `Tiggo 4 HEV` with alias from `IL|Chery|Tiggo 4 Pro`. Use trims `Comfort`, `Luxury`, `Noble` from the official price list. If horsepower for HEV is not already available in local source records, put HEV in non-blocking archive/review until fully grounded.
- Clear this active blocker.

## 2.2 Chery Tiggo 9 — FIX model name + horsepower + trims

Current value/problem:

```json
"model": "Tiggo 9",
"version_or_trim": null,
"horsepower_hp": null,
"fuel_type": "plug_in_hybrid",
"engine": "1.5L turbo",
"drivetrain": "AWD",
"year_start": 2025
```

Why wrong:

Israeli sources identify it as `Tiggo 9 Pro PHEV` / `TIGGO 9 Pro PHEV`, not generic `Tiggo 9`, and the current Israeli price list has trims `Luxury` and `Noble`. Power is not null; Israeli reviews/editorial grounding support 428 hp combined.

Validated Israeli sources:

- Chery Israel official Tiggo 9 PHEV page: PHEV, 7 seats, turbo petrol + electric, combined range over 1,100 km.
  URL: `https://cheryisrael.co.il/models/tiggo-9-phev/`
- Chery Israel official price list: `TIGGO 9 Pro PHEV Luxury` and `TIGGO 9 Pro PHEV Noble`.
  URL: `https://cheryisrael.co.il/pricing/`
- Cartube Oct 2025 launch: Tiggo 9 Pro PHEV launched in Israel; 7 seats, AWD, 148 km electric range; at launch one trim `Noble` at 244,990 NIS.
  URL: `https://www.cartube.co.il/חדשות-רכב/צ-רי-טיגו-9-פרו-פלאג-אין-בישראל-מחיר-244990-שקל`
- Over-Drive Israeli test: combined output 428 hp; 1.5L turbo petrol 143 hp plus electric motors.
  URL: `https://over-drive.co.il/צרי-טיגו-9-מבחן-דרכים-הכל-בגדול/`

Exact action:

- Action: `FIX + SPLIT`
- Canonical model should be `Tiggo 9 Pro PHEV` if the project allows canonical marketed model names. If source group key remains `IL|Chery|Tiggo 9`, add:

```json
"source_alias_keys": ["IL|Chery|Tiggo 9"],
"split_from_source_group_key": "IL|Chery|Tiggo 9"
```

- Replace null-trim row with:

```json
{
  "version_or_trim": "Luxury",
  "body_type": "SUV",
  "fuel_type": "plug_in_hybrid",
  "engine": "1.5L turbo plug-in hybrid",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 428,
  "transmission": "automatic",
  "drivetrain": "AWD",
  "year_start": 2026,
  "year_end": null,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "Noble",
  "body_type": "SUV",
  "fuel_type": "plug_in_hybrid",
  "engine": "1.5L turbo plug-in hybrid",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 428,
  "transmission": "automatic",
  "drivetrain": "AWD",
  "year_start": 2025,
  "year_end": null,
  "support_level": "direct"
}
```

- If exact transmission subtype is not grounded in local source records, keep `transmission = "automatic"` rather than guessing DHT/3-speed.
- Clear blocker.

## 2.3 Chevrolet Camaro — FIX parse-error blocker by rebuilding exact rows

Current value/problem:

- Review entry is an API/parse error:

```text
error = Extra data: line 319 column 1
technical_variants_il = []
```

Raw values seen:

```text
LT, SS, ZL1
3.6L V6, 6.2L V8, 6.2L V8 Supercharged
Coupe, Convertible
RWD
automatic
```

Validated Israeli source:

- iCar article 27 Jan 2021: UMI started marketing Camaro SS and ZL1 in Israel; LT was already marketed. LT = 3.6L V6 335 hp; SS = 6.2L V8 455 hp; ZL1 = 6.2L supercharged V8 650 hp; all with 10-speed automatic.
  URL: `https://www.icar.co.il/חדשות_רכב/שברולט_קמארו_SS_ו-ZL1_בישראל/`

Exact action:

- Action: `FIX`
- Replace parse-error empty profile with clean technical rows:

```json
{
  "version_or_trim": "LT",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.6L V6",
  "engine_displacement_l": 3.6,
  "horsepower_hp": 335,
  "transmission": "10-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2016,
  "year_end": 2024,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "SS",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "6.2L V8",
  "engine_displacement_l": 6.2,
  "horsepower_hp": 455,
  "transmission": "10-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2021,
  "year_end": 2024,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "ZL1",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "6.2L V8 supercharged",
  "engine_displacement_l": 6.2,
  "horsepower_hp": 650,
  "transmission": "10-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2021,
  "year_end": 2024,
  "support_level": "direct"
}
```

- Add Convertible rows only if existing source records in the repo support them at exact trim level. Otherwise do not guess.
- Clear blocker.

## 2.4 Chevrolet Captiva — FIX parse-error blocker; keep only strongly grounded rows

Current value/problem:

- Review entry is a parse error:

```text
error = Extra data: line 273 column 1
technical_variants_il = []
```

Raw values seen:

```text
LS, LT, LTZ
2.0L Turbo Diesel, 2.2L Turbo Diesel, 2.4L, 3.0L V6, 3.2L V6
diesel/petrol
AWD/FWD
automatic
```

Validated Israeli sources:

- iCar Captiva 2017 page lists Israeli versions including 2.0 diesel LT, 2.2 diesel LT, 2.4 petrol LT, 3.0 petrol LTZ, 3.2 petrol LTZ, LS/LT.
  URL: `https://www.icar.co.il/שברולט/שברולט_קפטיבה/שברולט_קפטיבה_יד_שניה_ד10/version17103/`
- Same iCar page gives 2.0 diesel 2017 LT: 1956cc, 167 hp, automatic.
- Carzone Captiva 2017 summary supports 2.4 petrol 167 hp and 3.0 V6 petrol 258 hp.
  URL: `https://www.carzone.co.il/Chevrolet/Captiva/2017/`

Exact action:

- Action: `FIX PARTIAL + ARCHIVE WEAK ROWS`
- Build only rows backed by existing source data. Minimum clean rows:

```json
{
  "version_or_trim": "LT",
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "2.0L turbo diesel",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 167,
  "transmission": "automatic",
  "drivetrain": "AWD",
  "year_start": 2007,
  "year_end": 2017,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "LT",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.4L petrol",
  "engine_displacement_l": 2.4,
  "horsepower_hp": 167,
  "transmission": "automatic",
  "drivetrain": "FWD",
  "year_start": 2011,
  "year_end": 2018,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "LTZ",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "3.0L V6",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 258,
  "transmission": "automatic",
  "drivetrain": "AWD",
  "year_start": 2011,
  "year_end": 2018,
  "support_level": "direct"
}
```

- The 2.2 diesel and 3.2 V6 rows may be kept only if the repo already has exact horsepower/drivetrain grounding. Otherwise move them to non-blocking archive/review.
- Clear blocker.

## 2.5 Chevrolet Tahoe — FIX missing field_sources + split unsupported historical row

Current value/problem:

- Variant 0 has non-null `version_or_trim = High Country` but no `field_sources.version_or_trim`.
- Variant 3 has `horsepower_hp = null` for historical 2000-2006 5.3L V8 row.
- Current rows mix official/current, parallel import and historical data.

Validated Israeli sources:

- Chevrolet Israel official current Tahoe page: 2026 High Country, 6.2L V8, 420 hp, 4X4.
  URL: `https://www.chevrolet.co.il/tahoe/`
- Carzone 2023 Tahoe page supports 5.3L 355 hp 4X4.
  URL: `https://www.carzone.co.il/Chevrolet/Tahoe/2023/`
- Auto 2019 article for new Tahoe/Suburban tech supports 5.3L V8 355 hp and 6.2L V8 420 hp with 10-speed automatic.
  URL: `https://www.auto.co.il/articles/car-news/world-news/133057/`

Exact action:

- Action: `FIX + MOVE WEAK HISTORICAL ROW TO NON-BLOCKING ARCHIVE`
- Keep/fix current official row:

```json
{
  "version_or_trim": "High Country",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "6.2L V8",
  "engine_displacement_l": 6.2,
  "horsepower_hp": 420,
  "transmission": "10-speed automatic",
  "drivetrain": "4WD",
  "year_start": 2025,
  "year_end": null,
  "support_level": "direct"
}
```

- Keep 5.3L 355 hp row only if `source_indexes` point to source supporting 5.3L/355 hp/10AT/4WD. Add proper `field_sources`.
- Do **not** keep the 2000-2006 5.3L row with `horsepower_hp = null` in clean. Move it to non-blocking archive/review unless exact Israeli horsepower source is already present in repo. Missing horsepower cannot remain in clean.
- Clear blocker.

## 2.6 Chevrolet Traverse — FIX parse-error blocker by rebuilding generation rows

Current value/problem:

- Review entry is a parse error:

```text
error = Expecting ',' delimiter: line 251 column 1
technical_variants_il = []
```

Raw values seen:

```text
2009, 2017, 2018, 2024, 2026
LTZ, Premier, RS
3.6L V6, 2.5L Turbo I4
AWD
automatic
```

Validated Israeli sources:

- Chevrolet Israel current Traverse page: 2.5L turbo, 328 hp, FWD or AWD, 8-speed automatic.
  URL: `https://www.chevrolet.co.il/traverse/`
- Queen of the Road launch summary: 2024/2025 Traverse in Israel, 2.5L turbo, 328 hp, 45 kgm, 8-speed automatic, 7/8 seats, four trims.
  URL: `https://www.queenoftheroad.co.il/שברולט-טרווורס-2024-בישראל-7-8-מושבים-מ-339990₪/`
- Auto.co.il current Traverse page also supports 328 hp and 45 kgm.
  URL: `https://www.auto.co.il/cars/chevrolet/traverse/`

Exact action:

- Action: `FIX`
- Build current generation rows:

```json
{
  "version_or_trim": "LT Luxury",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.5L turbo I4",
  "engine_displacement_l": 2.5,
  "horsepower_hp": 328,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2024,
  "year_end": null,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "LT Midnight",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.5L turbo I4",
  "engine_displacement_l": 2.5,
  "horsepower_hp": 328,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2024,
  "year_end": null,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "Z71",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.5L turbo I4",
  "engine_displacement_l": 2.5,
  "horsepower_hp": 328,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2024,
  "year_end": null,
  "support_level": "direct"
}
```

- For older 3.6L V6 Premier/RS/LTZ rows, keep only if exact Israeli source records already exist in repo. Otherwise move historical older rows to non-blocking archive/review, not active blocker.
- Clear blocker.

## 2.7 Citroen C3 Picasso — FIX parse-error blocker; keep only grounded rows

Current value/problem:

- Review entry returned non-object JSON:

```text
technical_variants_il = []
```

Raw values seen:

```text
Comfort
1.4L 95 hp
1.6L 92 hp diesel
1.6L 115/120 hp petrol
1.2L PureTech 110 hp
manual/automatic/unknown
Compact Van
FWD
```

Validated Israeli source:

- iCar C3 Picasso page lists Israeli versions: 1.4 petrol Comfort, 1.6 diesel Comfort, 1.6 petrol robotic Comfort, 1.6 diesel robotic Comfort; 2012 diesel robotic Comfort has 1560cc and 92 hp.
  URL: `https://www.icar.co.il/סיטרואן/סיטרואן_C3_פיקאסו/סיטרואן_C3_פיקאסו_יד_שניה_ד10/version9162/`

Exact action:

- Action: `FIX PARTIAL + ARCHIVE WEAK ROWS`
- Minimum clean rows from strong Israeli source:

```json
{
  "version_or_trim": "Comfort",
  "body_type": "Compact Van",
  "fuel_type": "diesel",
  "engine": "1.6L HDi diesel",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 92,
  "transmission": "robotic automatic",
  "drivetrain": "FWD",
  "year_start": 2010,
  "year_end": 2017,
  "support_level": "direct"
}
```

- Add 1.4 petrol 95 hp and 1.6 petrol 115/120 hp rows only if the existing repo source records contain exact horsepower/transmission grounding. Do not infer.
- Do not keep `transmission = unknown` in clean.
- Clear blocker.

## 2.8 Citroen C4 X — FIX field_sources only; keep variants

Current value/problem:

- Variants are technically valid but `version_or_trim = Shine` has no `field_sources` entry.
- Current rows:
  - 1.2 turbo petrol 130 hp, 8-speed automatic, FWD, Shine.
  - 1.5 turbo diesel 130 hp, 8-speed automatic, FWD, Shine.
  - electric 136 hp, single-speed, FWD, Shine.

Validated Israeli sources:

- iCar C4 X page: three powertrains in Israel: 1.2 petrol 130 hp, 1.5 diesel 130 hp, electric 136 hp.
  URL: `https://www.icar.co.il/סיטרואן/סיטרואן_C4_X/סיטרואן_C4_X_יד_שניה_ד10/`
- iCar version list includes `1.2 טורבו-בנזין Shine`, `1.5 טורבו-דיזל Shine`, `חשמלית Shine`, and later `Max`.
- Auto C4 X page confirms same engine families and 8-speed automatic for petrol/diesel.
  URL: `https://www.auto.co.il/cars/citroen/c4x/2023/`

Exact action:

- Action: `FIX`
- Keep all three current rows.
- Add `field_sources.version_or_trim` for each non-null `version_or_trim`.
- Remove `year_end` from `missing_grounded_fields` if current/open-ended.
- Remove `engine_displacement_l` from `missing_grounded_fields` for the electric row.
- If a current `Max` trim exists in source records, add it only as equipment trim if technically identical; do not duplicate rows unless project wants equipment-level rows.
- Clear blocker.

## 2.9 Citroen C5 Aircross — FIX parse-error blocker by rebuilding grounded technical rows

Current value/problem:

- Review entry returned non-object JSON:

```text
technical_variants_il = []
```

Raw values seen:

```text
Feel / Shine
Shine Pack
Shine Pack / Max
You / Max
1.2L MHEV
1.2L Turbo
1.5L BlueHDi Turbo
1.6L PHEV
1.6L Turbo
diesel, mild_hybrid, petrol, plug_in_hybrid
automatic, dual_clutch
FWD
```

Validated Israeli sources:

- Cartube 2022 facelift article: 1.6L turbo petrol 180 hp; 1.5L BlueHDi diesel 130 hp.
  URL: `https://www.cartube.co.il/חדשות-רכב/סיטרואן-c5-איירקרוס-החדש-2022-בישראל-מחיר-168990-שקל`
- iCar PHEV test: C5 Aircross PHEV, 1.6L turbo, 225 hp.
  URL: `https://www.icar.co.il/מבחני_רכב/סיטרואן_C5_איירקרוס_(פלאג-אין)_-_מבחן_רכב/`
- Auto current C5 Aircross page: current Israel C5 Aircross uses 1.2L mild-hybrid Stellantis unit, 145 hp combined, 6-speed dual-clutch.
  URL: `https://www.auto.co.il/cars/citroen/c5-aircross/`
- Citroen Israel/online price list result supports `C5 AIRCROSS MAX MHEV 145hp AT`.
  URL: `https://online.citroen.co.il/pricelist/c5-aircross/`

Exact action:

- Action: `FIX`
- Rebuild clean rows with at least these grounded technical rows:

```json
{
  "version_or_trim": "Feel",
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "1.5L BlueHDi turbo diesel",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 130,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2019,
  "year_end": 2022,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "Shine Pack",
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "1.5L BlueHDi turbo diesel",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 130,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2019,
  "year_end": 2025,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "Shine Pack",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.6L turbo petrol",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 180,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2019,
  "year_end": 2022,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "Shine Pack",
  "body_type": "SUV",
  "fuel_type": "plug_in_hybrid",
  "engine": "1.6L turbo plug-in hybrid",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 225,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2021,
  "year_end": 2022,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "Max",
  "body_type": "SUV",
  "fuel_type": "mild_hybrid",
  "engine": "1.2L turbo mild-hybrid",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 145,
  "transmission": "6-speed dual-clutch",
  "drivetrain": "FWD",
  "year_start": 2026,
  "year_end": null,
  "support_level": "direct"
}
```

- If the repo has exact source data for `You` trim, add it. If not, do not guess.
- Clear blocker.

---

# 3. Split alias and unmatched-output fixes

## 3.1 KEEP: Junior Elettrica split profile

Current value:

```text
output_key = IL|Alfa Romeo|Junior Elettrica
split_from_source_group_key = IL|Alfa Romeo|Junior
source_alias_keys = [IL|Alfa Romeo|Junior]
```

Current variants:

```text
electric 156 hp, FWD, year_start 2024, open-ended
Veloce electric 280 hp, FWD, year_start 2025, open-ended
```

Action: `KEEP`

- Do not merge into `Junior` and do not delete.
- Preserve alias/lineage so it does not become unmatched.
- Remove false `year_end` and `engine_displacement_l` missing flags for current EV rows.

## 3.2 FIX: BMW M850i / 850i duplicate and casing

Current issue:

There are two modern M850i profiles:

```text
Bmw 850i — contains modern M850i xDrive 2018-2024 variants
BMW M850i — contains the same modern M850i xDrive 2018-2024 variants and correct alias to IL|BMW|850i
```

There is also a separate historical row:

```text
BMW 850i — 1990-1994 5.0L V12 300 hp RWD
```

Action: `FIX + MERGE`

- Keep historical `BMW 850i` 1990-1994 V12 row.
- Keep split profile `BMW M850i` with:

```json
"split_from_source_group_key": "IL|BMW|850i",
"source_alias_keys": ["IL|BMW|850i"]
```

- Delete/merge duplicate `Bmw 850i` modern profile into `BMW M850i`.
- Normalize all `Bmw` to `BMW`.
- Ensure `M850i` variants remain:
  - Coupe, 2018-2024, 4.4L V8 turbo, 530 hp, 8AT, AWD.
  - Convertible, 2019-2024, same technicals.
  - Gran Coupe, 2019-2024, same technicals.

## 3.3 KEEP: BMW X5 xDrive30d split profile

Current value:

```text
output_key = IL|BMW|X5 xDrive30d
split_from_source_group_key = IL|BMW|X5 3.0d
source_alias_keys = [IL|BMW|X5 3.0d]
```

Action: `KEEP + REPORTING FIX`

- Preserve the split profile and alias.
- Derive top-level `year_start = 2014`, `year_end = 2026` or `null` if current.
- Add additional source indexes if available; current one-source grounding is acceptable only if the source is direct enough. If not direct enough, move weak subrows to non-blocking review but do not make the profile unmatched.

## 3.4 KEEP: BYD Atto 3 EVO split profile

Current value:

```text
output_key = IL|BYD|Atto 3 EVO
split_from_source_group_key = IL|BYD|Atto 3
source_alias_keys = [IL|BYD|Atto 3]
```

Validated sources:

- BYD Israel official page/price list: `BYD ATTO 3 EVO Design` and `BYD ATTO 3 EVO Excellence`.
  URL: `https://bydauto.co.il/model/byd-atto-3-evo/`
- iCar current catalog: BYD Atto 3 Design 2x4 and Excellence 4x4.
  URL: `https://www.icar.co.il/BYD/BYD_אטו_3/BYD_אטו_3_חדש/`
- International BYD/European specs support Design 313 hp RWD and Excellence 449 hp AWD; local price/source supports the trims.

Action: `KEEP`

- Preserve `Atto 3 EVO` as a legitimate split profile.
- Keep rows:
  - Design, electric, 313 hp, RWD, 2026-current.
  - Excellence, electric, 449 hp, AWD, 2026-current.
- Preserve alias to `IL|BYD|Atto 3` so unmatched remains 0.
- Do not merge away the EVO profile.

## 3.5 FIX: Cadillac Escalade IQ split profile

Current value/problem:

```text
output_key = IL|Cadillac|Escalade IQ
split_from_source_group_key = IL|Cadillac|Escalade
source_alias_keys = [IL|Cadillac|Escalade]
version_or_trim = null
horsepower_hp = 750
year_start = 2025
```

Validated sources:

- Cadillac Israel official Escalade IQ page: Escalade IQ 2026, up to 724 km range, fast charging, current Israeli model page.
  URL: `https://www.cadillac.co.il/ESCALADE-IQ/`
- Cadillac global official page: Escalade IQ has Premium Luxury and Luxury/Sport family and 750 hp in Velocity Max.
  URL: `https://www.cadillac.com/electric/escalade-iq`

Action: `FIX + SPLIT`

- Preserve split alias to `IL|Cadillac|Escalade`.
- Do not keep `version_or_trim = null` if the clean catalog needs trim values.
- Split into locally supported trims only if Israeli source records in repo contain the trims. If not, keep one technical row with `version_or_trim = null` only if null trims are allowed for technical-only EV profile, but remove it from blockers by marking `trim_not_required_for_technical_row = true`.
- Preferred clean rows if trim support exists:

```json
{
  "version_or_trim": "Luxury Sport",
  "body_type": "SUV",
  "fuel_type": "electric",
  "engine": "electric",
  "engine_displacement_l": null,
  "horsepower_hp": 750,
  "transmission": "single_speed",
  "drivetrain": "AWD",
  "year_start": 2026,
  "year_end": null,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "Premium Luxury",
  "body_type": "SUV",
  "fuel_type": "electric",
  "engine": "electric",
  "engine_displacement_l": null,
  "horsepower_hp": 750,
  "transmission": "single_speed",
  "drivetrain": "AWD",
  "year_start": 2026,
  "year_end": null,
  "support_level": "direct"
}
```

- If Israeli trim support cannot be attached from repo sources, use one non-trim technical row and explicitly mark it as a valid technical-only split profile so it does not remain blocked.

---

# 4. Rebuild/test requirements

After all RUN 3 changes:

1. Rebuild:

```bash
python -m scripts.catalog_builder
python -m scripts.catalog_quality_scan
```

or the project’s existing equivalent build command.

2. Run tests:

```bash
python -m pytest -q
```

3. Verify final readiness target:

```text
models_blocked = 0
review_only_blocked_entries = 0
duplicate_technical_variants = 0
invalid_source_references = 0
unknown_support_values = 0
ready_for_website_upload = true
unmatched_output_keys_count = 0
unmatched_output_keys_sample = []
active blocked = 0
```

4. Verify quality scan no longer falsely treats:

```text
current year_end null
EV engine_displacement_l null
open-ended current models
non-blocking archive entries
```

as active blockers.

5. Delete this temporary file only after successful rebuild + tests.

