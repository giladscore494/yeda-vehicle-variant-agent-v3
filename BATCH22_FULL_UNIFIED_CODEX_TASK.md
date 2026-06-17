# BATCH 22 — FULL UNIFIED CODEX TASK

This unified task combines RUN 1, RUN 2, and RUN 3. Execute in order and do not browse the internet.

---

# BATCH 22 — RUN 1 CODEX TASK

## Scope and execution rule

This is RUN 1 only. Do not proceed to RUN 2 models unless the user explicitly approves.

Do not browse the internet. All web-validated facts and target corrections are embedded here.

Repo state from uploaded ZIP `yeda-vehicle-variant-agent-v3-validation-v2-budgeted-dual-il-trims (15).zip`:

```text
clean_models = 293
technical_variants = 993
review_entries = 7
models_blocked = 7
review_only_blocked_entries = 7
invalid_source_references = 0
unknown_support_values = 0
duplicate_technical_variants = 0
ready_for_website_upload = false
resume_after_key = IL|Dodge|Nitro
next_key_to_process = IL|Dodge|Ram
unmatched_output_keys_count = 0
split_profile_alias_count = 8
```

Fresh `scan_quality()` over the current catalog/review reports:

```text
quality_scan_stale = false after regeneration
quality bug = 4
quality leak = 111
quality structure = 325
normalization = 0
```

The 4 fresh quality bugs are:

```text
Citroen SpaceTourer: variant[0] is indirect but all non-null fields are grounded
Citroen ë-C3: variant[0] is indirect but all non-null fields are grounded
Daihatsu Charade: candidate designation wrongly rejected: Charade84hp
Daihatsu Charade: candidate designation wrongly rejected: Charade90hp
```

RUN 1 model window selected from the first 20 clean models after the previous Batch 21 cursor `IL|Citroen|C6`:

```text
1.  IL|Citroen|C8
2.  IL|Citroen|DS3
3.  IL|Citroen|DS5
4.  IL|Citroen|Grand C4 Picasso
5.  IL|Citroen|Jumper
6.  IL|Citroen|Jumpy
7.  IL|Citroen|Saxo
8.  IL|Citroen|SpaceTourer
9.  IL|Citroen|Xsara
10. IL|Citroen|Xsara Picasso
11. IL|Citroen|ZX
12. IL|Citroen|ë-Berlingo
13. IL|Citroen|ë-C3
14. IL|Cupra|Ateca
15. IL|Cupra|Born
16. IL|Cupra|Formentor
17. IL|Cupra|Leon
18. IL|Cupra|Tavascan
19. IL|Dacia|Bigster
20. IL|Dacia|Dokker
```

Also apply the mandatory carry-forward fix from the previous post-merge audit:

```text
Chery Tiggo 4 HEV must not be lost. Preferred convention: separate model `Chery Tiggo 4 HEV`, not merely under `Tiggo 4 Pro`, because Chery Israel presents TIGGO 4 HEV as a separate model/line alongside TIGGO 4 Pro. Target basis: 1.5L hybrid, 163 hp combined, DHT automatic, FWD, year_start=2025, year_end=null/current. Trims Comfort/Luxury/Noble only if grounded by Israeli source/PDF; otherwise preserve as review/archive non-blocking rather than dropping.
```

---

## Sources already validated by ChatGPT for this RUN

Use these sources as field-level grounding; do not browse.

### Citroen / DS

- Citroen Jumpy 2024 Israeli launch: 2.0 turbo diesel, 177 hp, 8-speed automatic, medium/large and passenger/commercial bodies. Source: Cartube, `https://www.cartube.co.il/חדשות-רכב/סיטרואן-ג-מפי-2024-החדש-בישראל-מחיר-266990-שקל`
- Citroen Jumpy 2026 direct spec: 2.0 diesel automatic 177 hp, M1 Medium, 8 seats, FWD, 8-speed automatic, 1,997 cc. Source: Cartube, `https://www.cartube.co.il/מחירון-רכב-חדש/סיטרואן/סיטרואן-ג-מפי/6522-סיטרואן-ג-מפי-2-0-דיזל-אוטו-177-כ-ס-8-מושבים-m1-medium`
- Citroen Jumpy 2026 market evidence also shows updated 2.2L/180 hp N1 rows and 2.0L/177 hp M1 passenger rows; if this conflicts with existing sources, keep only directly grounded rows in clean and put uncertain 2.2/180 details into non-blocking review/archive. Sources: Carzone/Cmotors, `https://www.carzone.co.il/Citroen/Jumpy/`, `https://www.cmotors.co.il/cars/citroen/jumpy/`
- Citroen ë-C3: electric 113 hp, 44 kWh LFP, FWD/single-speed, 2024/2025 Israeli launch context. Sources: iCar and Cartube, `https://www.icar.co.il/test_drive/b14rrujs0/`, `https://www.cartube.co.il/חדשות-רכב/רכישת-רכב-חשמלי-אלו-הדגמים-החשובים-בדרך-לישראל-2024-2025`
- Citroen DS5 iCar page confirms DS5 model years 2012-2015; Cartube launch confirms Israeli DS5 with 1.6 turbo basis. Sources: `https://www.icar.co.il/סיטרואן/סיטרואן_DS5/`, `https://www.cartube.co.il/חדשות-רכב/סיטרואן-ds5-בישראל-מחיר-החל-מ-163-000-שקל`

### Cupra

- Cupra Leon official current Israeli price list lists `LEON PA 1.5e 150HP` and `LEON PA 2.0 VZ 300HP`. Source: Cupra Israel, `https://cupraofficial.co.il/cars/cupra-leon/`
- Cupra Leon 2024 facelift launch confirms only two current Israeli powertrains: 1.5L eTSI 150 hp with 7-speed DSG, FWD; and 2.0L turbo VZ 300 hp with 7-speed DSG, FWD. Source: Cartube, `https://www.cartube.co.il/חדשות-רכב/קופרה-לאון-החדשה-2024-נחתה-בישראל-מחיר-179900-שקל`
- Cartube price-list page shows 2023/2024 pre-facelift Leon included 1.5 150 hp, 2.0 190 hp, and 2.0 300 hp VZ. Source: `https://www.cartube.co.il/מחירון-רכב-חדש/קופרה/קופרה-לאון`
- Cupra Formentor 2024 facelift launch confirms 1.5 turbo 48V and VZ 333 hp from 2024. Source: Cartube, `https://www.cartube.co.il/חדשות-רכב/קופרה-פורמנטור-החדש-2024-בישראל-מחיר-189900-שקל`
- Cupra Formentor 2025 update confirms 2.0 turbo 204 hp 4X4 added between 1.5 150 hp and VZ 333 hp; 7-speed DSG and AWD for 204 hp row; 2025 price list has 1.5 turbo, 2.0 turbo 4X4, 2.0 turbo VZ 4X4. Source: Cartube, `https://www.cartube.co.il/חדשות-רכב/חדש-בישראל-2025-קופרה-פורמנטור-2-0-טורבו-4x4-מחיר-229900-שקל`
- Cupra Tavascan has 286 hp RWD and 340 hp AWD/VZ powertrains. Source: Cartube, `https://www.cartube.co.il/חדשות-רכב/קופרה-טווסקאן-הקרוסאובר-החשמלי-הראשון-של-קופרה-יוצא-לדרך`

### Dacia

- Dacia Bigster official Israel overview says only two Israeli engine types: mild hybrid manual 130 hp with 4X4, and full hybrid 155 hp automatic. It explicitly does not support a 140 hp FWD mild-hybrid row. Source: Dacia Israel, `https://www.dacia.co.il/cars/bigster/overview.html`
- Dacia Bigster official trims: Expression and Expression Plus can be configured with mild hybrid 4X4 or full hybrid; Journey is full hybrid only. Source: Dacia Israel overview/spec page, `https://www.dacia.co.il/cars/bigster/overview.html`, `https://www.dacia.co.il/cars/bigster/specifications.html`
- Dacia Dokker launch and iCar version page support 1.2 turbo petrol 115 hp and 1.5 turbo-diesel 90 hp; iCar version listings include Ambiance petrol, Ambiance diesel, and Laureate diesel. Sources: `https://www.icar.co.il/חדשות_רכב/דאצ'יה_מגיעה_לישראל:_המחירים_נמוכים,_הרכבים_ידניים_בלבד/`, `https://www.icar.co.il/דאצ'יה/דאצ'יה_דוקר/דאצ'יה_דוקר_יד_שניה_ד10/version20871/`

---

## RUN 1 corrections and decisions

### 0. Mandatory carry-forward correction: Chery Tiggo 4 HEV

Action: **FIX / ADD OR NON-BLOCKING REVIEW**

Current issue:

- After Batch 21 merge, `Chery Tiggo 4 HEV` was not present in clean or review, even though the source universe had a hybrid Tiggo 4 source row and Chery Israel presents a separate `TIGGO 4 HEV` line.

Target:

- Add separate model/profile `IL|Chery|Tiggo 4 HEV`, not just `Tiggo 4 Pro`, unless the repository convention has a documented rule to merge it under `Tiggo 4 Pro`.
- Preferred clean technical row basis:
  - `make = Chery`
  - `model = Tiggo 4 HEV`
  - `fuel_type = hybrid`
  - `engine = 1.5L hybrid`
  - `engine_displacement_l = 1.5`
  - `horsepower_hp = 163`
  - `transmission = DHT automatic`
  - `drivetrain = FWD`
  - `year_start = 2025`
  - `year_end = null`
  - `version_or_trim = Comfort / Luxury / Noble only if directly grounded by Israeli source/PDF`
- If exact trims are not sufficiently grounded in available repo sources, preserve the model/line in non-blocking review/archive with the above technical basis, and do not drop it silently.

---

### 1. Citroen C8

Action: **KEEP**

Current data:

- 3 rows: 2.0 petrol 138 hp automatic, 2.0 petrol 143 hp automatic, 3.0 V6 petrol 208 hp automatic, all FWD, years 2003-2008.

Validation:

- Existing Israeli iCar/Auto sources in the profile are acceptable for this old model. No exact RUN 1 correction required.

Codex instruction:

- Keep rows as-is unless local source indexes are broken.
- Ensure `source_indexes` and `field_sources` remain valid.

---

### 2. Citroen DS3

Action: **KEEP**

Current data:

- Chic 1.6 120 hp 4AT 2010-2015.
- Sport Chic 1.6 turbo 156 hp manual 2010-2015.
- So Chic 1.2 turbo 110 hp 6AT 2015-2019.

Validation:

- Israeli iCar/Cartube/Auto sources support the DS3 lines and 1.2 turbo 110 hp automatic update.

Codex instruction:

- Keep as-is.

---

### 3. Citroen DS5

Action: **KEEP**

Current data:

- Sport Chic 1.6 turbo 156 hp 6AT 2012-2015.
- Sport Chic 1.6 turbo 165 hp 6AT 2015-2018.

Validation:

- Israeli DS5 iCar/Cartube sources support the model and 1.6 turbo Israeli basis.

Codex instruction:

- Keep these rows unless local source indexes are invalid.
- Do not add diesel/hybrid rows without strong Israeli-market source support in repo sources.

---

### 4. Citroen Grand C4 Picasso

Action: **KEEP**

Current data:

- 7 technical rows across 2007-2018, split by powertrain: 1.2 turbo 130, 1.6 turbo 165, 1.6 diesel 120, 2.0 diesel 150, older 1.6 turbo 156, 2.0 petrol 143, 1.6 diesel 112.

Validation:

- Existing iCar/Auto profile sources support the two generations and powertrain splits. `version_or_trim=null` is acceptable here as technical-powertrain rows rather than official trim rows.

Codex instruction:

- Keep as-is.
- Do not create blockers for null trim on these technical rows.

---

### 5. Citroen Jumper

Action: **KEEP WITH GUARDRAIL / VERIFY LOCAL SOURCE CONSISTENCY**

Current data:

- 9 diesel van rows from 1994-2026.
- Latest row: 2.2L diesel 140 hp automatic FWD 2024-2026.

Validation:

- Existing profile includes official Citroen/Jumper and iCar/Auto/Gear-era sources. No direct contradiction was strong enough in RUN 1 to force a change.

Codex instruction:

- Keep current rows if all local `source_indexes` and `field_sources` are valid.
- Do not change `year_end` to null unless a current official Israeli Jumper page/price-list already exists in repo sources.
- If latest 2024-2026 row is only supported by weak/lease/marketplace sources, move that latest row to non-blocking review/archive rather than guessing.

---

### 6. Citroen Jumpy

Action: **FIX CURRENT COVERAGE / SOURCE GROUNDING**

Current data:

- Catalog ends the latest 2.0 turbo diesel 177 hp 8AT row at `year_end=2024`.
- It does not fully represent the 2026 current Israeli Jumpy evidence.

What is wrong:

- Israeli current sources show Jumpy still active in 2026.
- Cartube 2024 launch states 2.0 turbo diesel 177 hp with 8-speed automatic.
- Cartube 2026 direct spec confirms 2.0 diesel automatic 177 hp, M1 Medium, FWD, 1,997 cc, 8-speed automatic.
- Carzone/Cmotors also show 2026 updated Jumpy variants, including 2.2L/180 hp N1 rows. This is potentially a new current commercial split but should not be guessed if local sources conflict.

Target correction:

- Ensure at minimum this clean current row exists and is grounded:
  - `model = Jumpy`
  - `version_or_trim = M1 Medium` or `Medium M1` if the catalog uses body/seat trim naming; otherwise null with note is acceptable
  - `body_type = Van`
  - `fuel_type = diesel`
  - `engine = 2.0L turbo`
  - `engine_displacement_l = 2.0`
  - `horsepower_hp = 177`
  - `transmission = 8-speed automatic`
  - `drivetrain = FWD`
  - `year_start = 2024` if representing facelift/current row, or extend existing 2019 row to current only if source mapping says it is the same generation row
  - `year_end = null`
  - `support_level = direct`
- Preserve historical 2016-2019/2019-2024 rows if they represent pre-facelift row splits.
- For possible 2026 2.2L/180 hp N1 rows: add to clean only if the current repo already contains direct Israeli source refs supporting engine, hp, transmission and body. Otherwise create non-blocking review/archive item, not a blocker.

---

### 7. Citroen Saxo

Action: **KEEP**

Current data:

- 6 rows: 1.1, 1.4 automatic/manual, 1.5 diesel, VTR 1.6 90, VTS 1.6 120, 1996-2003.

Validation:

- Existing iCar/Auto sources are acceptable for this old model.

Codex instruction:

- Keep as-is.

---

### 8. Citroen SpaceTourer

Action: **FIX SUPPORT LEVEL BUG**

Current data:

- `variant[0]`: null trim, Van, diesel, 2.0L turbo, 150 hp, 6-speed automatic, FWD, 2017-2019, `support_level=indirect`.
- `variant[1]`: Business, Van, diesel, 2.0L turbo, 177 hp, 8-speed automatic, FWD, 2019-2024, `support_level=direct`.

What is wrong:

- Fresh quality scan says `variant[0] is indirect but all non-null fields are grounded`.

Target correction:

- Set `variant[0].support_level = direct` if all non-null fields have source refs and no missing grounded fields.
- Keep both rows otherwise unchanged.
- Re-run quality scan and ensure the SpaceTourer `support_level_invariant` bug is gone.

---

### 9. Citroen Xsara

Action: **KEEP**

Current data:

- 7 hatchback/estate petrol/diesel rows, 1998-2006.

Validation:

- Existing iCar/Auto sources support this old model’s technical splits.

Codex instruction:

- Keep as-is unless local source refs are invalid.

---

### 10. Citroen Xsara Picasso

Action: **KEEP**

Current data:

- 5 MPV rows: 2.0 petrol auto, 1.8 petrol manual, 2.0 diesel manual, 1.6 diesel manual, 1.6 petrol manual, years 2000-2007.

Validation:

- Existing iCar/Auto sources support the model and powertrain splits.

Codex instruction:

- Keep as-is.

---

### 11. Citroen ZX

Action: **KEEP WITH SOURCE-STRENGTH GUARDRAIL**

Current data:

- 10 hatchback/estate rows, 1992-1998.

Validation:

- The profile uses a mix of Israeli and non-Israeli/marketplace sources. This is acceptable for a legacy model only where Israeli sources support existence/year/trim and technical values are not contradicted.

Codex instruction:

- Keep current rows if all source indexes are valid.
- Do not allow non-Israeli Auto-Data alone to be the only support for Israel-specific trim/year existence.
- If any ZX row is only grounded by non-Israeli/marketplace source without Israeli corroboration, move that row to non-blocking review/archive.

---

### 12. Citroen ë-Berlingo

Action: **KEEP**

Current data:

- Shine Pack, Van, electric, 136 hp, single-speed, FWD, 2022-current.

Validation:

- Israeli Cartube/iCar sources support e-Berlingo as a legitimate electric model/line.

Codex instruction:

- Keep as-is.
- `engine_displacement_l = null` is valid for EV and must not create a missing-grounding blocker.

---

### 13. Citroen ë-C3

Action: **FIX SUPPORT LEVEL BUG / KEEP EV ROW**

Current data:

- MAX, Hatchback, electric, 113 hp, single-speed, FWD, 2024-current, `support_level=indirect`.

What is wrong:

- Fresh quality scan says `variant[0] is indirect but all non-null fields are grounded`.
- Search validation confirms 113 hp electric basis and 44 kWh LFP context for the ë-C3.

Target correction:

- Set `support_level = direct` if all non-null field refs are present.
- Keep:
  - `version_or_trim = MAX`
  - `body_type = Hatchback`
  - `fuel_type = electric`
  - `engine = electric`
  - `engine_displacement_l = null`
  - `horsepower_hp = 113`
  - `transmission = single_speed`
  - `drivetrain = FWD`
  - `year_start = 2024`
  - `year_end = null`
- Ensure EV null displacement is not treated as missing grounding.

---

### 14. Cupra Ateca

Action: **KEEP**

Current data:

- SUV petrol 2.0L turbo, 300 hp, 7-speed dual-clutch, AWD, 2019-2024.

Validation:

- Israeli Cartube/iCar/Cupra sources support Cupra Ateca 300 hp AWD.

Codex instruction:

- Keep row as-is unless local sources show it is still marketed current. Do not extend `year_end` to null without current Israeli source.

---

### 15. Cupra Born

Action: **KEEP WITH REVIEW OF CURRENT STATUS ONLY**

Current data:

- One electric 204 hp RWD row, 2022-2024.

Validation:

- Existing Israeli sources support Born 204 hp entry row.
- Later 2025/2026 price-list evidence from marketplace-like sources exists, but current official Cupra Israel homepage evidence is not strong enough in this RUN to force a clean extension.

Codex instruction:

- Keep current 2022-2024 row.
- Do not add 231 hp / VZ / facelift rows without strong Israeli source already in repo sources.
- If source universe contains direct Israeli official/current Born rows, add them; otherwise leave for non-blocking review/archive, not blocker.

---

### 16. Cupra Formentor

Action: **FIX FACELIFT/CURRENT COVERAGE**

Current data:

- 1.5 turbo 150 FWD, 2021-2024.
- VZ 2.0 turbo 310 AWD, 2021-2024.
- 2.0 turbo 190 AWD, 2021-2024.
- 1.4 PHEV 204 FWD, 2022-2024.

What is wrong:

- Catalog stops at 2024 and misses/does not reflect current Israeli facelift rows.
- Cartube 2024 Israeli launch confirms facelift current rows: 1.5 turbo 48V and VZ 333 hp.
- Cartube 2025 update confirms the added 2.0 turbo 204 hp 4X4 row and current 2025 price list with 1.5 turbo, 2.0 turbo 4X4, 2.0 turbo VZ 4X4.

Target correction:

- Keep historical 2021-2024 rows where directly supported.
- Add current/facelift rows:
  1. `version_or_trim = null` or `1.5` per catalog convention
     - `body_type = SUV`
     - `fuel_type = mild_hybrid` if source supports 48V; otherwise petrol with note. Preferred: `mild_hybrid` for 2024 facelift 1.5 48V.
     - `engine = 1.5L turbo`
     - `engine_displacement_l = 1.5`
     - `horsepower_hp = 150`
     - `transmission = 7-speed dual_clutch`
     - `drivetrain = FWD`
     - `year_start = 2024`
     - `year_end = null`
  2. `version_or_trim = null` or `2.0 4X4`
     - `body_type = SUV`
     - `fuel_type = petrol`
     - `engine = 2.0L turbo`
     - `engine_displacement_l = 2.0`
     - `horsepower_hp = 204`
     - `transmission = 7-speed dual_clutch`
     - `drivetrain = AWD`
     - `year_start = 2025`
     - `year_end = null`
  3. `version_or_trim = VZ`
     - `body_type = SUV`
     - `fuel_type = petrol`
     - `engine = 2.0L turbo`
     - `engine_displacement_l = 2.0`
     - `horsepower_hp = 333`
     - `transmission = 7-speed dual_clutch`
     - `drivetrain = AWD`
     - `year_start = 2024`
     - `year_end = null`
- Do not extend old 310 hp VZ beyond 2024; the facelift VZ target is 333 hp.
- PHEV 204 should remain historical through 2024 unless current Israeli source exists.

---

### 17. Cupra Leon

Action: **FIX CURRENT STATUS / REMOVE UNSUPPORTED CURRENT ROWS / ADD MISSING HISTORICAL 190 IF GROUNDED**

Current data:

- 1.5 mild-hybrid 150 FWD, 2023-current.
- VZ PHEV 1.4 turbo 245 FWD, 2021-current.
- VZ petrol 2.0 turbo 300 FWD, 2021-current.
- VZ Estate petrol 2.0 turbo 310 AWD, 2021-current.

What is wrong:

- Current official Cupra Israel and Cartube 2024 launch support only current Leon PA 1.5e 150 hp and Leon PA 2.0 VZ 300 hp in Israel.
- The PHEV 245 and Estate 310 rows should not remain open/current unless directly grounded by Israeli current sources.
- Cartube price-list evidence shows 2023/2024 pre-facelift Leon had a 2.0 190 hp row, which is missing from the catalog if source refs support it.

Target correction:

1. Keep/update current rows:
   - `1.5e / 1.5 mild_hybrid`, Hatchback, 1.5L turbo, 150 hp, 7-speed dual_clutch, FWD, `year_start=2024` or keep `2023` if source supports pre-facelift continuity, `year_end=null`.
   - `VZ`, Hatchback, petrol, 2.0L turbo, 300 hp, 7-speed dual_clutch, FWD, `year_start=2021`, `year_end=null` if continuity is accepted; otherwise split pre/post facelift but same technical values.
2. Set unsupported current rows to historical or remove from clean:
   - `VZ PHEV 245` must not remain `year_end=null` unless direct Israeli current source exists. If source support is only foreign/general, move to non-blocking review/archive or cap at the verified Israeli historical year.
   - `VZ Estate 310 AWD` must not remain `year_end=null` unless direct Israeli source exists. If source support is foreign/general, move to non-blocking review/archive or cap at verified historical years.
3. Add missing historical row if grounded by local sources:
   - `version_or_trim = null` or `2.0 190` per convention
   - `body_type = Hatchback`
   - `fuel_type = petrol`
   - `engine = 2.0L turbo`
   - `engine_displacement_l = 2.0`
   - `horsepower_hp = 190`
   - `transmission = 7-speed dual_clutch`
   - `drivetrain = FWD`
   - `year_start = 2023`
   - `year_end = 2024`
- Do not leave foreign-market Estate/PHEV rows in verified clean without Israeli proof.

---

### 18. Cupra Tavascan

Action: **KEEP**

Current data:

- Immersive, electric 286 hp, single-speed, RWD, 2024-current.
- VZ Adrenaline, electric 340 hp, single-speed, AWD, 2024-current.

Validation:

- Cartube supports Tavascan 286 hp RWD and VZ 340 hp AWD powertrains.

Codex instruction:

- Keep rows as-is.
- EV null displacement is valid and should not block.

---

### 19. Dacia Bigster

Action: **FIX — REMOVE UNSUPPORTED 140 FWD ROW AND ADD REAL ISRAELI TRIM/POWERTRAIN SPLITS**

Current data:

- null trim, hybrid, 1.8L, 155 hp, automatic, FWD, 2025-current.
- null trim, mild_hybrid, 1.2L turbo, 140 hp, manual, FWD, 2025-current.
- null trim, mild_hybrid, 1.2L turbo, 130 hp, manual, 4WD, 2025-current.

What is wrong:

- Dacia Israel official overview says Bigster is available in Israel with only two engine types:
  - mild hybrid manual 130 hp with 4X4
  - full hybrid 155 hp automatic
- It does not support the catalog’s `1.2 mild_hybrid 140 hp FWD` clean row.
- Official trim section shows:
  - Expression: mild hybrid 4X4 + full hybrid
  - Expression Plus: mild hybrid 4X4 + full hybrid
  - Journey: full hybrid only

Target correction:

- Delete or move to non-blocking review/archive:
  - `mild_hybrid 1.2L turbo 140 hp manual FWD`
- Replace null-trim technical rows with grounded trim/powertrain rows:
  1. `Expression`, SUV, mild_hybrid, `1.2L turbo`, 1.2, 130 hp, `6-speed manual` or `manual`, `4WD`, `year_start=2025`, `year_end=null`.
  2. `Expression Plus`, SUV, mild_hybrid, `1.2L turbo`, 1.2, 130 hp, `6-speed manual` or `manual`, `4WD`, `year_start=2025`, `year_end=null`.
  3. `Expression`, SUV, hybrid, `1.8L`, 1.8, 155 hp, `automatic` / multi-mode automatic, `FWD`, `year_start=2025`, `year_end=null`.
  4. `Expression Plus`, SUV, hybrid, `1.8L`, 1.8, 155 hp, `automatic` / multi-mode automatic, `FWD`, `year_start=2025`, `year_end=null`.
  5. `Journey`, SUV, hybrid, `1.8L`, 1.8, 155 hp, `automatic` / multi-mode automatic, `FWD`, `year_start=2025`, `year_end=null`.
- Update `available_values_for_website` and model-level years after variants.

---

### 20. Dacia Dokker

Action: **FIX TRIMS / ADD MISSING AMBIANCE ROWS**

Current data:

- Laureate, Van, petrol, 1.2L turbo, 115 hp, 5-speed manual, FWD, 2015-2019.
- Laureate, Van, diesel, 1.5L turbo, 90 hp, 5-speed manual, FWD, 2015-2021.

What is wrong:

- Israeli launch/iCar sources support Dokker with 1.2 turbo petrol 115 hp and 1.5 diesel 90 hp, but iCar version lists include `Ambiance` petrol, `Ambiance` diesel and `Laureate` diesel. The current clean catalog appears to over-label the petrol row as `Laureate` and misses Ambiance rows.

Target correction:

- Add or correct rows so clean contains only source-grounded trims:
  1. `Ambiance`, Van, petrol, `1.2L turbo`, 1.2, 115 hp, manual, FWD, `year_start=2015`, `year_end=2019` if this end is source-supported.
  2. `Ambiance`, Van, diesel, `1.5L turbo`, 1.5, 90 hp, manual, FWD, `year_start=2015`, `year_end=2021` if this end is source-supported.
  3. `Laureate`, Van, diesel, `1.5L turbo`, 1.5, 90 hp, manual, FWD, `year_start=2015`, `year_end=2021`.
- Keep `Laureate` petrol only if a direct Israeli source in the repo supports petrol Laureate. If not, change the current petrol Laureate row to `Ambiance` or move the Laureate petrol row to non-blocking review/archive.
- Regenerate `available_values_for_website`.

---

## Blockers observed now, but do not fully repair until RUN 3 unless needed by this RUN

Current review-only blocked entries:

```text
Citroen DS4 — parse error / technical_variants_il empty
Citroen ë-C4 — parse error / technical_variants_il empty
Dacia Jogger — parse error / technical_variants_il empty
Daewoo Cielo — parse error / technical_variants_il empty
Daihatsu Move — technical_variants_il empty
Dodge Charger — non-object JSON / technical_variants_il empty
Dodge Journey — variants present but missing source_indexes despite field_sources
```

Do not ignore these. They are RUN 3 scope unless Codex needs to touch validation code now. Ensure RUN 1 changes do not increase blocker count.

---

## Required code/reporting fixes for RUN 1

1. Regenerate quality scan after catalog changes. The ZIP had stale scan metadata before explicit regeneration. Final quality scan should reflect all 300 current models, not the previous 247-model baseline.
2. Clear RUN 1 quality bugs:
   - SpaceTourer `support_level_invariant`
   - ë-C3 `support_level_invariant`
3. Do not weaken validation to hide bugs. The fixes must be actual row/support-level or source-grounding corrections.
4. Preserve alias matching:
   - no new unmatched output keys
   - existing split aliases remain matched
5. Preserve valid optional null rules:
   - EV `engine_displacement_l=null` is valid
   - current `year_end=null` is valid
   - null trim is valid only when justified by technical-row convention/source structure
6. Rebuild catalog outputs and run:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python - <<'PY'
import json
from scripts.catalog_quality_scan import scan_quality
cat=json.load(open('data/model_technical_catalog_il.json',encoding='utf-8'))
rev=json.load(open('data/model_technical_catalog_il_review.json',encoding='utf-8'))
report=scan_quality(cat, rev)
print(report['totals'])
PY
python -m pytest -q
```

If `pytest` cannot run due missing optional local dependencies, report exactly which dependency import failed. Do not claim tests passed unless they actually did.

---

## RUN 1 required final report back to user

Return a concise report with:

```text
RUN 1 RESULT: PASS / PASS WITH WARNINGS / FAIL
Commit hash if committed
Files changed
Models touched
Variants added
Variants fixed
Variants moved to review/archive
Quality scan bug count after regeneration
Readiness metrics after rebuild
Remaining blockers count
Unmatched output keys count
Tests run and exact results
```

Stop after RUN 1. Do not start RUN 2 without user approval.


---

# BATCH 22 — RUN 2 CODEX TASK

## Scope and execution rule

This is RUN 2 only. Do not proceed to RUN 3 blockers / tail models unless the user explicitly approves.

Do not browse the internet. All web-validated facts and target corrections are embedded here.

Input ZIP audited by ChatGPT:

```text
yeda-vehicle-variant-agent-v3-validation-v2-budgeted-dual-il-trims (15).zip
```

Repo state observed from the uploaded ZIP:

```text
clean_models = 293
technical_variants = 993
review_entries = 7
models_blocked = 7
review_only_blocked_entries = 7
invalid_source_references = 0
unknown_support_values = 0
duplicate_technical_variants = 0
ready_for_website_upload = false
resume_after_key = IL|Dodge|Nitro
next_key_to_process = IL|Dodge|Ram
unmatched_output_keys_count = 0
split_profile_alias_count = 8
```

RUN 2 model window = the next 20 clean models after RUN 1:

```text
21. IL|Dacia|Duster
22. IL|Dacia|Lodgy
23. IL|Dacia|Logan
24. IL|Dacia|Sandero
25. IL|Dacia|Spring
26. IL|Daewoo|Espero
27. IL|Daewoo|Kalos
28. IL|Daewoo|Lacetti
29. IL|Daewoo|Lanos
30. IL|Daewoo|Leganza
31. IL|Daewoo|Matiz
32. IL|Daewoo|Nubira
33. IL|Daewoo|Tacuma
34. IL|Daewoo|Tico
35. IL|Daihatsu|Charade
36. IL|Daihatsu|Copen
37. IL|Daihatsu|Cuore
38. IL|Daihatsu|Gran Move
39. IL|Daihatsu|Materia
40. IL|Daihatsu|Sirion
```

Important: there are still clean tail models after RUN 2 (`Daihatsu Terios`, `Daihatsu YRV`, `Dodge Caliber`, `Dodge Challenger`, `Dodge Durango`, `Dodge Nitro`) and 7 review blockers. They belong to RUN 3 and must not be forgotten.

Current active blockers reserved for RUN 3:

```text
Citroen DS4
Citroen ë-C4
Dacia Jogger
Daewoo Cielo
Daihatsu Move
Dodge Charger
Dodge Journey
```

Carry-forward correction that remains mandatory in this Batch even if readiness becomes green:

```text
Chery Tiggo 4 HEV must not be lost. Preferred convention: separate model `Chery Tiggo 4 HEV`, not merely under `Tiggo 4 Pro`, because Chery Israel presents TIGGO 4 HEV as a separate model/line alongside TIGGO 4 Pro. Target basis: 1.5L hybrid, 163 hp combined, DHT automatic, FWD, year_start=2025, year_end=null/current. Trims Comfort/Luxury/Noble only if grounded by Israeli source/PDF; otherwise preserve as review/archive non-blocking rather than dropping.
```

---

## Sources validated by ChatGPT for RUN 2

Use these as embedded evidence; do not browse.

### Dacia

1. Dacia Israel official Duster page
   - URL: `https://www.dacia.co.il/cars/duster/overview.html`
   - Verified facts: current Israeli Duster is available with 1.2 turbo 130 hp manual 4X4 and a hybrid powertrain with 155 hp combined output. The page explicitly describes two engine types: petrol/manual 130 hp 4X4 and dynamic hybrid 155 hp.

2. iCar Dacia Duster new page
   - URL: `https://www.icar.co.il/דאצ'יה/דאצ'יה_דאסטר/דאצ'יה_דאסטר_חדש/`
   - Verified facts: current Duster has 1.2 turbo petrol 130 hp, manual only, FWD or 4X4; hybrid automatic FWD is also present.

3. Cartube 2025 Dacia Duster launch/price list
   - URL: `https://www.cartube.co.il/חדשות-רכב/דאצ-יה-דאסטר-החדש-2025-בישראל-מחיר-139990-שקל`
   - Verified facts: Israeli 2025 price list includes TCe 130 2X4 Expression, TCe 130 4X4 Expression, TCe 130 4X4 Extreme, Hybrid 140 Expression, Hybrid 140 Journey, Hybrid 140 Extreme. This source confirms the hybrid line exists in Israel, but the Dacia official page is preferred for current 155 hp technical output.

4. iCar Dacia Lodgy 2019 page
   - URL: `https://www.icar.co.il/דאצ'יה/דאצ'יה_לודג'י/דאצ'יה_לודג'י_יד_שניה_ד9310/version20870/`
   - Verified facts: Lodgy 2019 has 1.5 turbo-diesel 7-seat Laureate; iCar lists Lodgy variants as Laureate, including 1.2 turbo petrol, 1.5 diesel, and 1.3 turbo petrol entries.

5. iCar Dacia Lodgy overview 2015-2022
   - URL: `https://www.icar.co.il/דאצ'יה/דאצ'יה_לודג'י/דאצ'יה_לודג'י_יד_שניה_ד9310/`
   - Verified facts: Lodgy sold in Israel with 1.2 turbo petrol and 1.5 turbo diesel manual; from 2022 it was offered with the newer 1.3-litre Renault-Nissan engine.

6. Dacia Israel official Logan page
   - URL: `https://www.dacia.co.il/cars/logan/overview.html`
   - Verified facts: current Logan has 1.0 turbo petrol, 91 hp, automatic CVT.

7. iCar Dacia Logan MCV 2018 page
   - URL: `https://www.icar.co.il/דאצ'יה/דאצ'יה_לוגאן_MCV/דאצ'יה_לוגאן_MCV_יד_שניה_ד9310/version19172/`
   - Verified facts: Logan MCV 2016-2021 had 0.9 turbo petrol robotic, 1.5 turbo diesel manual and 1.5 turbo diesel robotic entries.

8. iCar Dacia Sandero Stepway 2025 page
   - URL: `https://www.icar.co.il/דאצ'יה/דאצ'יה_סנדרו_Stepway/דאצ'יה_סנדרו_Stepway_יד_שניה_ד9311/version30810/`
   - Verified facts: Sandero Stepway 2025 1.0 Expression has 999 cc, 91 hp, FWD, current-generation Israeli listing.

9. iCar Dacia Sandero Stepway 2016 robotic page
   - URL: `https://www.icar.co.il/דאצ'יה/דאצ'יה_סנדרו_Stepway/דאצ'יה_סנדרו_Stepway_יד_שניה_ד9310/version15451/`
   - Verified facts: 2016 Sandero Stepway 0.9 turbo petrol Laureate used a single-clutch robotic automatic transmission, not a conventional automatic.

10. Auto Dacia Sandero 2016 article
    - URL: `https://www.auto.co.il/cars/dacia/sandero/2016/`
    - Verified facts: base Sandero joined the Israeli offer in early 2016 with 1.2 litre, 75 hp, manual 5-speed.

11. iCar/Auto/Cartube Dacia Spring sources
    - URLs:
      - `https://www.icar.co.il/מבחני_רכב/נהיגה_ראשונה_-_דאצ'יה_ספרינג/`
      - `https://www.auto.co.il/articles/car-news/world-news/135776/`
      - `https://www.cartube.co.il/חדשות-רכב/דאצ-יה-ספרינג-אקסטרים-2023-נחשפת-תוספת-כוח`
    - Verified facts: Spring base power is about 44/45 hp; Spring Extreme introduced Electric 65 / 65 hp. Current catalog `Essential` 45 and `Extreme` 65 is broadly aligned, but direct Israeli import/current-status grounding is weaker than importer pages.

### Daewoo

12. Autoboom Daewoo Espero 1.8 MT page
    - URL: `https://autoboom.co.il/catalog/cars/daewoo/espero/1-generation/sedan/11043`
    - Verified facts: Daewoo Espero 1.8 MT, 95 hp appears in Autoboom, with 2.0 AT 105 hp listed as another version.

13. Yad2 Daewoo Espero price feed
    - URL: `https://www.yad2.co.il/price-list/feed?manufacturer=60&model=10833`
    - Verified facts: 1996/1997 Daewoo Espero sub-models include 2.0 automatic 105 hp, 1.8 automatic 95 hp, and 1.8 manual 90 hp. This conflicts with the catalog's 1.8 manual 95 hp and does not support 2.0 manual.

14. Autoboom Daewoo Lanos 1.6 MT page
    - URL: `https://autoboom.co.il/catalog/cars/daewoo/lanos/1-generation/micro/11139`
    - Verified facts: Lanos 1.6 MT 106 hp exists; alternatives include 1.5 MT 86 hp and 1.5 AT 86 hp.

15. Yad2 Daewoo price feed
    - URL: `https://www.yad2.co.il/price-list/feed?manufacturer=60`
    - Verified facts: Lanos Israeli price feed strongly shows 1.5 86 hp S/SE rows and an SX 1.6 106 hp row. It does not strongly support a 1.4 75 hp clean Israeli Lanos row.

16. iCar Chevrolet Optra page
    - URL: `https://www.icar.co.il/שברולט/שברולט_אופטרה/`
    - Verified facts: Israeli-market Optra was sold as Chevrolet Optra; it came from Daewoo factories, but wore Chevrolet branding in Israel.

17. Autoboom Chevrolet Optra page
    - URL: `https://autoboom.co.il/catalog/cars/chevrolet/optra`
    - Verified facts: Chevrolet Optra Israeli catalog has sedan/hatchback, 1.6/1.8 petrol, automatic/manual, FWD.

18. Autoboom Daewoo Nubira 2.0 AT page
    - URL: `https://autoboom.co.il/catalog/cars/daewoo/nubira/2-generation/sedan/11245`
    - Verified facts: Daewoo Nubira 2.0 AT 133 hp FWD exists; alternatives include 1.6 MT 106 and 1.6 AT 106.

19. Yad2 Daewoo Nubira price feed
    - URL: `https://www.yad2.co.il/price-list/feed?manufacturer=60&model=10840`
    - Verified facts: Nubira has many Israeli sub-models including S/SX/SXL 1.6 106 hp manual/automatic across sedan/hatchback/station, and 2.0 133 automatic hatchback entries.

20. Autoboom Daewoo Tico page
    - URL: `https://autoboom.co.il/catalog/cars/daewoo/tico/1-generation`
    - Verified facts: Daewoo Tico generation shown 1996-2004 in Autoboom, with 41 hp variants. Other global sources list 41 hp as the normal 0.8 output.

21. Yad2 / Carbar Daewoo Tico / Espero feeds
    - URLs:
      - `https://www.yad2.co.il/price-list/feed?manufacturer=60`
      - `https://carbar.nmmsoft.com/price-list/model/10833`
    - Verified facts: Yad2/Carbar can support certain old Israeli price-list labels, but they are lower-tier sources. Use them only where no stronger source exists, and do not mark as high-confidence direct importer evidence.

### Daihatsu

22. Yad2 Daihatsu Charade price feed
    - URL: `https://www.yad2.co.il/price-list/feed?manufacturer=15&model=10171`
    - Verified facts: Charade rows include 1.3 84 hp manual/automatic and 1.5 90 hp sedan/hatchback rows. This supports the current 84/90 hp technical split and shows why labels like `Charade84hp` / `Charade90hp` are derived technical designations, not real trims.

23. iCar Daihatsu Sirion 2008 page
    - URL: `https://www.icar.co.il/דייהטסו/דייהטסו_סיריון/דייהטסו_סיריון_יד_שניה_ד9311/version5336/`
    - Verified facts: Sirion 2008 1.3 automatic exists.

24. Autoboom Daihatsu Sirion page
    - URL: `https://autoboom.co.il/catalog/cars/daihatsu/sirion`
    - Verified facts: second-generation Sirion in Israel had 1.3 litre, 87 hp, 4-speed automatic.

25. Yad2 Daihatsu Sirion 2001 CZ price-list page
    - URL: `https://www.yad2.co.il/price-list/sub-model/103521/2001`
    - Verified facts: first-generation Sirion CZ automatic 1.3 102 hp exists in Israel.

26. Wheel Daihatsu Sirion nostalgia article
    - URL: `https://wheel.co.il/נוסטלגיה-לשבת-דייהטסו-סיריון-דור-1-האו/`
    - Verified facts: in summer 2000 the importer began marketing Sirion CZ with a 1.3-litre 16-valve engine producing 102 hp.

27. Yad2 Daihatsu Sirion 2001 feed
    - URL: `https://www.yad2.co.il/price-list/feed?manufacturer=15&max-year=2001&min-year=2001`
    - Verified facts: Sirion 2001 entries include CL/CX 1.0 55 hp manual/automatic and CZ 1.3 102 hp automatic.

28. Gear Daihatsu Materia 2008 page
    - URL: `https://www.gear.co.il/גרסה/דייהטסו/מאטריה/2008/מאטריה/1.5-CX-אוטומט`
    - Verified facts: Materia 1.5 CX automatic is 105 hp, not 103 hp.

29. Gear / iCar Daihatsu Copen sources
    - URLs already present in catalog source list, including Ynet launch and iCar/Auto catalog references.
    - Verified facts: Copen 1.3 manual, 87 hp, 2006-2008 is plausible and can be kept if current source indexes are valid.

30. Daihatsu Cuore / Gran Move sources
    - Existing catalog sources are mostly Auto/KML/Autoboom style historical listings. They are acceptable as low/medium-confidence historical sources if field-level support is valid, but do not overstate them as importer-grade.

---

# RUN 2 required corrections

## 21. IL|Dacia|Duster — FIX / ADD MISSING CURRENT HYBRID

Current issue:

```text
Current catalog has 10 Duster rows and covers historical 2015-2023 powertrains plus current 2024-2026 1.2 mild-hybrid 130 manual FWD/4WD.
It does not include the current Israeli Duster hybrid row.
The current rows also use year_end=2026 even though the model is current; project convention normally uses year_end=null for active/current rows.
```

Verified evidence:

```text
Dacia Israel official page says Duster has two engine types: petrol/manual 130 hp 4X4 and hybrid 155 hp combined.
iCar confirms current Duster has 1.2 turbo 130 manual FWD/4X4 and hybrid automatic FWD.
Cartube 2025 price list confirms a Hybrid Duster line exists in Israel, although it uses 140 hp in that older launch article. Prefer Dacia official current page for 155 hp if adding current 2026 technical data.
```

Codex action:

```text
KEEP the historical 2015-2023 rows if their existing source indexes are valid.
FIX current 2024+ Duster rows:
- 1.2L turbo / mild_hybrid / 130 hp / manual / FWD / SUV / year_start=2024 or 2025 / year_end=null if treated as current.
- 1.2L turbo / mild_hybrid / 130 hp / manual / 4WD / SUV / year_start=2024 or 2025 / year_end=null if treated as current.

ADD missing current hybrid technical variant:
- version_or_trim: "Hybrid" or "Hybrid 155" unless exact Israeli trim split is explicitly grounded in existing embedded sources.
- body_type: SUV
- fuel_type: hybrid
- engine: 1.6L hybrid or hybrid powertrain, only if the source already supports exact displacement; otherwise use "hybrid".
- engine_displacement_l: 1.6 only if grounded; otherwise null/review non-blocking.
- horsepower_hp: 155
- transmission: automatic / multi-mode automatic according to canonical values
- drivetrain: FWD
- year_start: 2025 or current-model launch year according to source support
- year_end: null
- support_level: direct

Do not leave the current Duster without a hybrid row.
If Codex cannot fit exact hybrid trim names from embedded sources, add one technical variant rather than inventing trims.
```

Expected action tag: `FIX + ADD`.

---

## 22. IL|Dacia|Lodgy — FIX UNSUPPORTED `Laureate / Stepway` AND YEAR RANGE

Current issue:

```text
Current rows include:
- 2019-2022 1.3L turbo 130 manual FWD, version_or_trim="Laureate / Stepway"
- 2019-2022 1.5L turbo diesel 116 manual FWD, version_or_trim="Laureate / Stepway"

The Israeli sources found during audit support Lodgy `Laureate` strongly. They do not strongly support `Stepway` as a separate Israeli clean trim in these technical rows.
iCar overview says the 1.3-litre engine was offered from 2022, so a 2019 start for the 1.3 row is probably too early unless an embedded source proves otherwise.
```

Verified evidence:

```text
iCar 2019 Lodgy page lists 1.5 turbo-diesel 7 seats Laureate and shows Lodgy variants as Laureate.
iCar overview 2015-2022 says Lodgy sold with 1.2 turbo petrol and 1.5 turbo diesel manual, and from 2022 with the newer 1.3-litre Renault-Nissan engine.
Yad2 current listing snippets also show 1.3 petrol 2022 as Laureate.
```

Codex action:

```text
FIX current `Laureate / Stepway` rows:
- Replace `version_or_trim="Laureate / Stepway"` with `version_or_trim="Laureate"` unless there is an existing source inside the repo that directly supports Stepway for the Israeli Lodgy.

FIX 1.3L turbo row:
- Current value: year_start=2019, year_end=2022.
- Target: year_start=2022, year_end=2022 unless repo source proves 2021/2019 Israeli sale.
- engine: 1.3L turbo
- horsepower_hp: 130 or 131 according to normalized source; keep 130 if project convention rounds/specs to 130 and source supports.
- transmission: manual
- drivetrain: FWD
- body_type: MPV

KEEP older rows:
- 2015-2018 1.2 turbo 115 manual Laureate
- 2015-2018 1.5 diesel 110 manual Laureate
- 2019-2022 1.5 diesel 116 manual Laureate if source-supported.

Do not keep `Stepway` in clean without direct field-level Israeli source support.
```

Expected action tag: `FIX`.

---

## 23. IL|Dacia|Logan — FIX CURRENT HP/YEAR_END; WATCH MCV VS SEDAN LINEAGE

Current issue:

```text
Current catalog row:
Expression Plus / 2022-2024 / petrol / 1.0L turbo / 90 hp / CVT / Sedan.

Dacia Israel official current page says current Logan has 1.0 turbo petrol, 91 hp, CVT. Therefore horsepower and current/open-ended status need correction.
```

Verified evidence:

```text
Dacia Israel official Logan page: 91 hp, 1.0 turbo 3-cylinder petrol, CVT automatic.
Carzone/iCar support the 2022+ Logan sedan and Expression Plus trim, with trim options including Expression / Expression Plus / Journey in lower-tier listings.
iCar Logan MCV 2018 page confirms older MCV estate variants: 0.9 turbo petrol robotic and 1.5 diesel manual/robotic.
```

Codex action:

```text
FIX current 2022+ Logan sedan row:
- horsepower_hp: 91, not 90.
- transmission: cvt.
- year_start: 2022.
- year_end: null if the official Dacia Israel page still represents it as current in the dataset.
- body_type: Sedan.
- trim: keep `Expression Plus` if existing source supports it. Do not add Expression/Journey without direct field-level support.

KEEP older Logan MCV estate rows if source-supported:
- 0.9L turbo 90 manual/robotic if catalog has them accurately.
- 1.5L turbo-diesel 90 manual/robotic if source-supported.

Lineage note:
If the catalog convention separates `Logan` and `Logan MCV`, do not hide estate rows under sedan without alias/lineage. If current structure keeps both under `Logan`, ensure body_type and source notes make the distinction explicit.
```

Expected action tag: `FIX`.

---

## 24. IL|Dacia|Sandero — FIX CURRENT YEAR_END; FIX ROBOTIC TRANSMISSION LABEL

Current issue:

```text
Current catalog has:
- 2015-2018 base 1.2L 75 manual.
- 2015-2020 Stepway 0.9L turbo 90 manual.
- 2016-2020 Stepway 0.9L turbo 90 automatic.
- 2021-2024 Stepway Expression 1.0L turbo 91 CVT.

The 2016 Stepway automatic was a single-clutch robotic automatic, not a conventional automatic.
The current 1.0 CVT Stepway is still represented by 2025 Israeli listings and should not close at 2024 if current.
```

Verified evidence:

```text
iCar 2016 Stepway page: transmission is "automatic - single-clutch robotic".
Cartube/iCar 2016 launch articles confirm 0.9 turbo 90 hp robotic automatic.
iCar 2025 Stepway page: 999 cc, 91 hp, current-generation 1.0 Expression.
Auto 2016 article: base Sandero 1.2 75 hp manual joined Israeli offer in early 2016.
```

Codex action:

```text
FIX 2016-2020 Stepway automatic row:
- Current transmission: automatic.
- Target transmission: robotic automatic / single_clutch_robotic according to canonical vocabulary.
- Keep 0.9L turbo, 90 hp, FWD, Hatchback, years 2016-2020.

FIX current 1.0 CVT row:
- year_end: null if the model is still current.
- year_start remains 2021 if source supports third-gen Israeli launch; otherwise keep existing but don't close at 2024.
- horsepower_hp: 91.
- transmission: cvt.
- version_or_trim: keep `Stepway Expression` or normalize to the project's convention, but do not lose the Stepway line.

KEEP base 1.2 75 manual 2016-2018 if sourced.
```

Expected action tag: `FIX`.

---

## 25. IL|Dacia|Spring — KEEP WITH SOURCE CAUTION

Current issue:

```text
Current catalog:
- Essential / electric / 45 hp / single_speed / FWD / 2023-current.
- Extreme / electric / 65 hp / single_speed / FWD / 2023-current.
```

Verified evidence:

```text
Auto/Cartube/Dacia media sources support base Spring around 44/45 hp and Extreme/Electric 65 at 65 hp.
Carzone 2025 listing shows Spring 65 hp. Yad2 has mixed 49/45 hp lower-tier listings, so do not change hp based only on Yad2.
```

Codex action:

```text
KEEP Essential 45 and Extreme 65 if existing sources in the repo are valid.
Do not change Essential to 49 hp based only on Yad2.
If no Israeli active/current source supports `year_end=null`, either:
- keep current if source exists in repo; or
- set a justified finite year_end / move uncertain current status to non-blocking review/archive.

EV displacement null is valid and must not create a blocker.
```

Expected action tag: `KEEP / VERIFY SOURCE STRENGTH`.

---

## 26. IL|Daewoo|Espero — FIX MANUAL 1.8 HP; REMOVE UNSUPPORTED 2.0 MANUAL IF NO SOURCE

Current issue:

```text
Current catalog has four rows:
- 1.8L 95 automatic
- 1.8L 95 manual
- 2.0L 105 automatic
- 2.0L 105 manual

Yad2/Carbar Israeli price-list evidence supports:
- 1.8 automatic 95 hp
- 1.8 manual 90 hp
- 2.0 automatic 105 hp
It does not support 2.0 manual as a clean Israeli row.
```

Verified evidence:

```text
Autoboom shows 1.8 MT 95 and 2.0 AT 105, but Yad2/Carbar Israeli price feeds show 1.8 manual 90 hp and do not show 2.0 manual.
For Israeli-market catalog purposes, prefer Israeli price-list evidence where old historical sources conflict.
```

Codex action:

```text
FIX:
- 1.8L automatic: keep 95 hp.
- 1.8L manual: change horsepower_hp from 95 to 90 if the row is retained.
- 2.0L automatic: keep 105 hp.
- 2.0L manual: move to review/archive or delete if no embedded source directly supports Israeli 2.0 manual.

Keep body_type=Sedan, fuel_type=petrol, drivetrain=FWD.
Do not leave conflicting field_sources that claim Yad2/Carbar supports 1.8 manual 95; it supports 90.
```

Expected action tag: `FIX + MOVE/DELETE UNSUPPORTED`.

---

## 27. IL|Daewoo|Kalos — KEEP, BUT DO NOT OVERSTATE TRIMLESS ROWS

Current state:

```text
Current catalog has 1.4L 94 hp in automatic/manual and hatchback/sedan body variants, 2002-2004.
```

Verified evidence:

```text
Kalos was sold as Daewoo Kalos before the Chevrolet Aveo naming transition. Existing repo sources are Auto/iCar style pages. No major correction was proven in this RUN.
```

Codex action:

```text
KEEP if existing field_sources are valid.
If trim names are unknown, null trim is acceptable only with a note/justification that the row is a technical body/transmission split and no reliable Israeli trim name is available.
Do not duplicate Kalos with Chevrolet Aveo unless alias/lineage is explicitly handled in the catalog.
```

Expected action tag: `KEEP`.

---

## 28. IL|Daewoo|Lacetti — HIGH-RISK BRAND/MODEL IDENTITY FIX

Current issue:

```text
Current catalog keeps `Daewoo Lacetti` with 2004-2010 rows, but its own sources are actually Chevrolet Optra / Daewoo Lacetti platform sources.
Israeli-market sources indicate the model was marketed here as Chevrolet Optra, not cleanly as Daewoo Lacetti.
```

Verified evidence:

```text
iCar Chevrolet Optra page says the Optra was marketed successfully in Israel as Chevrolet Optra, even though it came from Daewoo factories.
Autoboom Chevrolet Optra page represents the Israeli catalog under Chevrolet Optra with 1.6/1.8 petrol, sedan/hatchback, automatic/manual.
```

Codex action:

```text
Do not keep `IL|Daewoo|Lacetti` as a clean standalone Israeli model if all supporting Israeli sources are actually `Chevrolet Optra`.

Preferred correction:
- Rename/MOVE this profile to `IL|Chevrolet|Optra` if that model does not already exist, preserving the technical variants and sources.
- Add alias/lineage: `IL|Daewoo|Lacetti` -> `IL|Chevrolet|Optra`.
- If adding/renaming would collide with existing Chevrolet Optra data, merge carefully by technical signature.

If Codex cannot safely rename in this RUN:
- Move `Daewoo Lacetti` to review/archive non-blocking, with reason: Israeli marketed name is Chevrolet Optra; Daewoo Lacetti is platform/foreign name.

Do not leave Daewoo Lacetti clean using Chevrolet Optra sources without alias/lineage.
```

Expected action tag: `MOVE / MERGE / ALIAS`, not simple KEEP.

---

## 29. IL|Daewoo|Lanos — FIX UNSUPPORTED 1.4; ADD/RETAIN TRIM CONTEXT WHERE GROUNDED

Current issue:

```text
Current catalog has:
- 1.5L 86 automatic/manual across Sedan/Hatchback.
- 1.4L 75 manual hatchback.
- 1.6L 106 automatic sedan.

Israeli price-list evidence strongly supports 1.5 86 hp S/SE rows and 1.6 106 hp SX row. The 1.4 75 row was not strongly supported by the Israeli sources found in this audit.
```

Verified evidence:

```text
Autoboom: Lanos 1.6 106 hp exists and alternatives include 1.5 MT/AT 86 hp.
Yad2 Daewoo feed: Lanos shows S/SE 1.5 86 hp rows and SX 1.6 106 hp row. No strong 1.4 75 Israeli clean support in the validated search.
```

Codex action:

```text
KEEP 1.5L 86 hp manual/automatic technical rows if existing sources are valid.
If possible, add version_or_trim context S/SE only if exact body/transmission mapping is supported; otherwise keep trim null with explicit technical-split justification.

FIX 1.6L 106 row:
- Set version_or_trim to `SX` if source supports.
- Preserve automatic/manual only if field-level source supports the transmission.

MOVE TO REVIEW/ARCHIVE or DELETE 1.4L 75 manual row unless an embedded Israeli source directly supports Lanos 1.4 75 in Israel.
```

Expected action tag: `FIX + MOVE/DELETE UNSUPPORTED`.

---

## 30. IL|Daewoo|Leganza — KEEP

Current state:

```text
Current catalog has one CDX 2.0L 133 hp 4-speed automatic FWD Sedan row, 1997-2002.
```

Verified evidence:

```text
Existing iCar/Auto/Gear/Yad2 style sources support Daewoo Leganza / Laganza 2.0 automatic around 133 hp. No correction was proven in this RUN.
```

Codex action:

```text
KEEP the CDX 2.0 133 hp automatic row if source indexes and field_sources are valid.
Ensure Hebrew/English naming convention stays canonical as `Leganza`.
```

Expected action tag: `KEEP`.

---

## 31. IL|Daewoo|Matiz — KEEP / YEAR CHECK

Current state:

```text
Current catalog has 0.8L 51 hp manual FWD Hatchback, 1998-2001.
```

Verified evidence:

```text
Yad2/Gear Israeli old-car sources support Daewoo Matiz 0.8 SE manual around 51 hp and 2000-2002 listings. The current 1998-2001 year range may be plausible but should be grounded by field sources.
```

Codex action:

```text
KEEP if source support is valid.
If existing sources only support 2000-2002, adjust year_start/year_end or move older uncertain years to review/archive.
Do not create blocker for null trim if the row is a technical engine/transmission split and source lacks trim.
```

Expected action tag: `KEEP / VERIFY YEAR RANGE`.

---

## 32. IL|Daewoo|Nubira — FIX/VERIFY BODY + TRIM GRANULARITY

Current issue:

```text
Current catalog has 1.6 106 rows for Sedan/Hatchback/Estate and one 2.0 133 automatic Sedan row, with S/SX/null trims.
Israeli sources show rich S/SX/SXL/body/transmission combinations. The current profile is broadly plausible but may be under-specified and contains null trim on the 2.0 row.
```

Verified evidence:

```text
Autoboom supports Nubira 2.0 AT 133 hp and alternatives 1.6 MT/AT 106 hp.
Yad2 feed supports S/SX/SXL 1.6 106 hp manual/automatic rows across sedan/hatchback/station, and 2.0 133 automatic hatchback entries.
Gear supports 2.0 CDX automatic 133 hp and 1.6 SX rows.
```

Codex action:

```text
KEEP the 1.6 106 technical rows if source-supported.
For trim fields, prefer source-supported S/SX/SXL where exact mapping is clear; otherwise keep null with a technical-split justification.

FIX 2.0 133 row if needed:
- Current version_or_trim is null.
- Source evidence suggests 2.0 may be CDX/SX depending year/body source.
- Do not invent trim; set to CDX/SX only if embedded source directly supports exact mapping.
- Body type may need Hatchback or Sedan depending source. Current catalog uses Sedan. Yad2 has 2.0 hatchback, Autoboom has 2.0 sedan and hatchback variants. If both are supported and project models body splits, add both; otherwise keep only source-supported body.
```

Expected action tag: `FIX/VERIFY`.

---

## 33. IL|Daewoo|Tacuma — KEEP

Current state:

```text
Current catalog has CDX 2.0L 121 hp automatic and manual FWD MPV rows, 2001-2004.
```

Verified evidence:

```text
Existing iCar/Auto historical Israeli sources support Tacuma 2.0 CDX around 121 hp with automatic/manual variants. No correction was proven in this RUN.
```

Codex action:

```text
KEEP if source indexes are valid.
Ensure support_level remains direct only if field_sources truly support all non-null fields.
```

Expected action tag: `KEEP`.

---

## 34. IL|Daewoo|Tico — RESOLVE 48 HP VS 41 HP CONFLICT

Current issue:

```text
Current catalog has:
- 1995-1996 0.8L 48 hp manual.
- 2001-2001 0.8L 41 hp manual.

This split is suspicious. Multiple global/Autoboom sources support 41 hp for the 0.8 Tico, while lower-tier Israeli price snippets can show 48 hp for 1996. The current 1995-1996 row appears to rely on weak/forum-style source support.
```

Verified evidence:

```text
Autoboom Tico generation page: variants from 41 hp.
Wikipedia/global technical references: 0.8 S-TEC around 41 hp, with some references to 49 hp variants.
Yad2 can show 1996 .8 48 hp, but that is a low-tier price-list/marketplace source and conflicts with better technical references.
```

Codex action:

```text
Do not keep both 48 hp and 41 hp rows as high-confidence direct clean rows unless both are directly source-supported for Israel.

Preferred safe correction:
- Keep one 0.8L manual FWD Hatchback technical row with horsepower_hp=41 if the best available source support is technical/global/Autoboom.
- If preserving 48 hp due to Israeli price-list support, mark support_level weaker or move to review/archive non-blocking, not clean direct.

At minimum:
- Remove any field_sources that overstate weak forum/marketplace support as direct.
- Resolve year range coherently, e.g. 1996-2001 or source-supported range, instead of arbitrary 1995-1996 + 2001-only split.
```

Expected action tag: `FIX / MOVE UNCERTAIN TO REVIEW`.

---

## 35. IL|Daihatsu|Charade — CLEAR QUALITY BUG; KEEP TECHNICAL ROWS IF SOURCE-SUPPORTED

Current issue:

```text
Fresh quality scan from RUN 1 found two quality bugs:
- Daihatsu Charade: candidate designation wrongly rejected: Charade84hp
- Daihatsu Charade: candidate designation wrongly rejected: Charade90hp

Current profile has 1.3L 84 hp hatchback manual/automatic and 1.5L 90 hp sedan manual/automatic rows.
The invalid labels list contains engine/hp tokens such as `84hp` and `90hp`, but the quality scan sees `Charade84hp` / `Charade90hp` as wrongly rejected.
```

Verified evidence:

```text
Yad2 Charade price feed supports 1.3 84 hp manual/automatic and 1.5 90 hp rows.
```

Codex action:

```text
KEEP the 1.3 84 hp and 1.5 90 hp technical rows if field_sources are valid.
FIX quality-scan/normalization logic so derived technical labels like `Charade84hp` / `Charade90hp` do not become bug findings when the actual numeric horsepower is already represented as a technical variant and not a trim.

Do not add `Charade84hp` or `Charade90hp` as trim names.
Do not mark valid horsepower-only non-trim labels as blockers.
```

Expected action tag: `FIX CODE/QUALITY REPORTING + KEEP DATA`.

---

## 36. IL|Daihatsu|Copen — KEEP

Current state:

```text
Current catalog has Copen 1.3L 87 hp 5-speed manual FWD Roadster, 2006-2008.
```

Verified evidence:

```text
Existing Israeli launch/review/catalog sources support Daihatsu Copen being sold in Israel with 1.3L around 87 hp and manual transmission.
```

Codex action:

```text
KEEP if source indexes are valid.
Do not create missing trim blocker for null trim if the model had no distinct Israeli trim name in the source.
```

Expected action tag: `KEEP`.

---

## 37. IL|Daihatsu|Cuore — KEEP WITH LOW/MEDIUM HISTORICAL CONFIDENCE

Current state:

```text
Current catalog has:
- 1990-1998 0.9L/0.85L 42 hp manual/automatic.
- 1999-2003 1.0L/0.99L 56 hp manual/automatic.
```

Verified evidence:

```text
Existing Auto/KML/Autoboom style historical sources support Cuore small petrol engine generations, manual/automatic, FWD. No strong correction was proven.
```

Codex action:

```text
KEEP if source indexes and field_sources are valid.
If engine label says 0.9L while engine_displacement_l is 0.85, this is acceptable as rounded label + precise displacement only if source supports; otherwise normalize consistently.
```

Expected action tag: `KEEP`.

---

## 38. IL|Daihatsu|Gran Move — KEEP / VERIFY YEAR SPLIT

Current state:

```text
Current catalog has:
- 1996-1999 1.5L 90 hp automatic/manual.
- 1999-2002 1.6L 91 hp automatic/manual.
```

Verified evidence:

```text
Existing Auto/KML historical sources broadly support Gran Move 1996-2002 and the 1.5/1.6 engine split. No correction was proven.
```

Codex action:

```text
KEEP if source support is valid.
If both 1.5 and 1.6 rows overlap in 1999, keep overlap only if the sources show transition year; otherwise split 1996-1998 and 1999-2002 or whichever source-supported range is correct.
```

Expected action tag: `KEEP / VERIFY YEAR SPLIT`.

---

## 39. IL|Daihatsu|Materia — FIX HORSEPOWER

Current issue:

```text
Current catalog has:
- CX / 1.5L / 103 hp / 4-speed automatic / FWD / MPV / 2007-2010.

Gear Israeli source shows Daihatsu Materia 1.5 CX automatic as 105 hp.
```

Verified evidence:

```text
Gear page: `דייהטסו מאטריה 1.5 CX אוטומט, 105 כ״ס`.
```

Codex action:

```text
FIX horsepower_hp from 103 to 105.
Keep:
- version_or_trim: CX
- engine: 1.5L
- transmission: 4-speed automatic
- drivetrain: FWD
- body_type: MPV
- year_start: 2007
- year_end: 2010

Update field_sources so horsepower points to the source supporting 105 hp.
```

Expected action tag: `FIX`.

---

## 40. IL|Daihatsu|Sirion — FIX/ADD TRIM CONTEXT; VERIFY FIRST-GEN AND SECOND-GEN SPLITS

Current issue:

```text
Current catalog has:
- CX / 2006-2011 / 1.3L / 87 hp / automatic.
- null / 2001-2005 / 1.3L / 102 hp / automatic.
- null / 1998-2004 / 1.0L / 55 hp / automatic.

The second-gen 1.3 87 CX row is good.
The first-gen 1.3 102 hp row should be CZ, not null, if source-supported.
The first-gen 1.0 55 hp row may need CL/CX trim context and should include manual + automatic if the catalog models transmission variants and source supports them.
```

Verified evidence:

```text
iCar/Autoboom support second-gen Sirion 1.3 87 hp automatic.
Yad2 and Gear support first-gen Sirion CZ 1.3 102 hp automatic in 2001.
Wheel article says in summer 2000 the importer started marketing Sirion CZ with 1.3L 16V 102 hp.
Yad2 2001 feed supports CL/CX 1.0 55 hp manual/automatic and CZ 1.3 102 hp automatic.
```

Codex action:

```text
KEEP second-gen:
- version_or_trim: CX or CX One where source-supported
- 1.3L, 87 hp, automatic, FWD, Hatchback, 2006-2011.

FIX first-gen 1.3 row:
- version_or_trim: CZ
- engine: 1.3L
- horsepower_hp: 102
- transmission: automatic
- year_start: 2000 or 2001 depending source support; year_end=2005 if source-supported.

FIX first-gen 1.0 row:
- engine: 1.0L
- horsepower_hp: 55 or 56 according to source convention; current 55 is supported by Yad2/iCar 2001.
- transmission: automatic currently exists. Add manual variant if the project already models manual/automatic and source supports CL/CX manual.
- version_or_trim: CL/CX only if exact trim mapping is source-supported; otherwise keep null with explicit technical-split note.

Do not leave the 1.3 102 row as null trim if CZ is source-supported.
```

Expected action tag: `FIX + OPTIONAL ADD`.

---

# Cross-cutting RUN 2 code/data requirements

## A. Support-level invariant bug must remain fixed

From the current quality-scan behavior, rows marked `indirect` but with every non-null field grounded should be corrected to `direct` only when truly field-supported. Do not weaken the validator globally.

## B. Optional null rules remain valid

Do not reintroduce old false blockers:

```text
EV engine_displacement_l = null is valid.
year_end = null for current/open-ended models is valid.
version_or_trim = null is valid only when source lacks a real Israeli trim and row is a technical engine/body/transmission split with justification.
```

## C. Do not collapse distinct trims into one string unless it is truly one technical variant

If a future list-valued `version_or_trim` appears:

```text
- If list items are separate real trims with same technical data, either split rows or use a deliberate shared technical row only when the project convention permits.
- If list was a schema artifact, normalize safely.
- Never leave list-valued `version_or_trim` in clean JSON.
```

## D. Brand/model identity is a blocker-quality issue

The `Daewoo Lacetti` → `Chevrolet Optra` issue is not just naming. It affects Israeli-market model identity. It must be handled with rename/alias/lineage or non-blocking review/archive.

## E. RUN 3 reminder

After RUN 2 is applied and verified, RUN 3 must still handle:

```text
Clean tail models after RUN 2:
- Daihatsu Terios
- Daihatsu YRV
- Dodge Caliber
- Dodge Challenger
- Dodge Durango
- Dodge Nitro

Active blockers:
- Citroen DS4
- Citroen ë-C4
- Dacia Jogger
- Daewoo Cielo
- Daihatsu Move
- Dodge Charger
- Dodge Journey

Carry-forward:
- Chery Tiggo 4 HEV
- unmatched/split/casing/duplicates/code reporting
```

---

# Required commands after RUN 2

After applying only RUN 2 corrections, run:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
```

If the local environment lacks optional app dependencies such as Streamlit/OpenAI, report import-only failures separately and still run all available data/catalog tests.

---

# Expected return from Codex after RUN 2

Return a clear report:

```text
RUN 2 RESULT: PASS / PASS WITH WARNINGS / FAIL

1. Files changed
2. Models touched
3. Variants added
4. Variants fixed
5. Variants moved to review/archive/deleted
6. Alias/lineage changes
7. Readiness metrics
8. Quality scan: bug/leak/structure/normalization counts
9. unmatched_output_keys_count
10. Tests run and results
11. Any warnings before RUN 3
12. Commit hash if committed
```

Do not claim the whole Batch is ready until RUN 3 is completed and verified.


---

# BATCH 22 — RUN 3 / BLOCKERS + TAIL MODELS + CARRY-FORWARD CODEX TASK

## Scope and execution rule

This is RUN 3. It is the final Batch 22 correction task.

Do not browse the internet. All web-validated facts and target corrections are embedded here.

Input ZIP audited by ChatGPT:

```text
yeda-vehicle-variant-agent-v3-validation-v2-budgeted-dual-il-trims (15).zip
```

Repo state observed from the uploaded ZIP before RUN 3:

```text
clean_models = 293
technical_variants = 993
review_entries = 7
models_blocked = 7
review_only_blocked_entries = 7
invalid_source_references = 0
unknown_support_values = 0
duplicate_technical_variants = 0
ready_for_website_upload = false
resume_after_key = IL|Dodge|Nitro
next_key_to_process = IL|Dodge|Ram
unmatched_output_keys_count = 0
unmatched_output_keys_sample = []
active_blocked_count = 7
split_profile_alias_count = 8
```

Fresh validation/quality checks before this task:

```text
python -m scripts.catalog_validation = PASS
python -m scripts.catalog_quality_scan = PASS
quality counts:
- grounding_completeness = 247
- year_split_duplicates = 31
- source_tier_inversion = 106
- source_domain = 4
```

Important: `source_tier_inversion` / `source_domain` are non-blocking leak/structure findings today, but do not worsen them when applying this task.

---

## RUN 3 coverage

### Remaining clean tail models after RUN 1 + RUN 2

```text
41. IL|Daihatsu|Terios
42. IL|Daihatsu|YRV
43. IL|Dodge|Caliber
44. IL|Dodge|Challenger
45. IL|Dodge|Durango
46. IL|Dodge|Nitro
```

The current Batch actually added 46 clean models after the previous Batch 21 cursor, not 50. RUN 1 covered 20, RUN 2 covered 20, so these 6 are the remaining clean tail models.

### Active blockers / review-only models to resolve now

```text
Citroen DS4
Citroen ë-C4
Dacia Jogger
Daewoo Cielo
Daihatsu Move
Dodge Charger
Dodge Journey
```

### Mandatory carry-forward fix from Batch 21 post-merge audit

```text
Chery Tiggo 4 HEV
```

This must be handled even if Batch 22 readiness becomes green through other fixes.

---

## Embedded web evidence for RUN 3

Use these facts as source of truth. Do not browse.

### Chery Tiggo 4 HEV — official Israeli source

Source: Chery Israel official `TIGGO 4 HEV` page

URL:

```text
https://cheryisrael.co.il/models/tiggo4-hev/
```

Verified facts:

```text
Chery Israel presents TIGGO 4 HEV as a separate model/line alongside TIGGO 4 Pro.
The site model list includes both TIGGO 4 HEV and TIGGO 4 Pro.
Safety/trim table lists:
- TIGGO 4 HEV COMFORT
- TIGGO 4 HEV LUXURY
- TIGGO 4 HEV NOBLE
Fuel consumption table lists TIGGO 4 HEV.
Engine displacement = 1.5 liter.
Gasoline engine output = 95 hp.
Electric motor output = 204 hp.
Combined system output = 163 hp.
Transmission = DHT automatic.
Fuel type = hybrid.
Current marketing page active in Israel.
```

### Dacia Jogger — official Israeli source + Israeli launch/update sources

Sources:

```text
https://www.dacia.co.il/cars/jogger/overview.html
https://www.dacia.co.il/pricing.html
https://www.dacia.co.il/cars/jogger/specifications.html
https://www.icar.co.il/דאצ'יה/דאצ'יה_ג'וגר/דאצ'יה_ג'וגר_חדש/
https://www.auto.co.il/cars/dacia/jogger/
https://www.cartube.co.il/חדשות-רכב/דאצ-יה-ג-וגר-2022-בישראל-מחיר-104990-שקל
https://www.cartube.co.il/חדשות-רכב/דאצ-יה-ג-וגר-7-מושבים-היברידית-חזרה-לישראל-מחיר-174990-שקל
```

Verified facts:

```text
Dacia Israel official current Jogger page: Jogger is a 7-seat hybrid crossover/family vehicle, price from 174,990 ILS.
Dacia Israel official pricing page: Jogger 1.6 hybrid automatic Expression is current.
iCar: first generation Jogger was revealed in 2021 and reached Israel in June 2022; it replaces Lodgy and Logan MCV.
Auto.co.il / Cartube: initial Israeli launch had 1.0L turbo petrol 110 hp manual, 7 seats.
Cartube 2022: Jogger launched in Israel with 1.0 turbo 110 hp, manual gearbox, three trim levels, prices from about 105k to 120k ILS.
Cartube 2025: Jogger Hybrid returned to Israel in Hybrid 140 form, 7 seats, Expression trim, price 174,990 ILS. The official current Dacia pricing page is preferred for current trim naming.
```

### Citroen ë-C4 / e-C4 — Israeli sources

Sources:

```text
https://online.citroen.co.il/model/e-c4/?ref=
https://www.cartube.co.il/חדשות-רכב/סיטרואן-c4-החדשה-2021-בישראל-מחיר-138990-שקל
https://www.icar.co.il/מבחני_רכב/סיטרואן_C4_(חשמלית)_-_מבחן_וידאו/
```

Verified facts:

```text
Citroen/Lubinski current online page exists for e-C4, but fetch may be blocked; use it as current official existence evidence if already present in repo sources.
Cartube 2021 launch: C4 launched in Israel with 1.2 petrol 130 hp, 1.5 diesel 130 hp, and e-C4 electric.
Cartube 2021: e-C4 electric uses a front electric motor with 136 hp, 50 kWh battery, about 350 km range, automatic EV drivetrain, FWD by platform.
Cartube 2021 price list: e-C4 Shine electric was marketed in Israel.
iCar electric C4 review: third-generation C4 was marketed in one trim, Shine, identical across the petrol/diesel/electric powertrains; electric output is 136 hp.
```

### Citroen DS4 — internal legacy evidence + external technical sanity check

Internal source from `data/validation_variants_data_v1.json`:

```text
Citroen DS4 has two legacy high-confidence Israeli-market migrated rows:
1. 2012-2015 Sport Chic, Hatchback, petrol, 1.6L turbo, 163 hp, 6-speed automatic, FWD.
2. 2012-2015 Sport Chic, Hatchback, petrol, 1.6L turbo, 200 hp, 6-speed manual, FWD.
Both rows have legacy_status=verified, confidence=high, field-level source_ids, and sources_count=19/20.
The current review blocker exists only because Gemini returned malformed/non-object JSON and `technical_variants_il` is empty.
```

External technical sanity sources used by ChatGPT:

```text
Auto-data / European technical references confirm Citroen DS4 1.6 THP 163 automatic and 1.6 THP 200 manual technical configurations existed in this generation.
These are not Israeli-market sources by themselves. Use them only as sanity checks, not as primary Israeli grounding.
Primary grounding must come from the existing repo legacy source_ids / field_sources already present in validation_variants_data_v1.json.
```

### Daewoo Cielo — internal legacy evidence

Internal source from `data/validation_variants_data_v1.json`:

```text
Daewoo Cielo has four migrated high-confidence Israeli-market rows, all 1995-1998, generation 1, 1.5L petrol, FWD:
1. GLX, Hatchback, automatic
2. GLX, Sedan, automatic
3. GL, Hatchback, manual
4. GL, Sedan, manual
Each has legacy_status=verified, confidence=high, source_ids src_1/src_3, and field-level evidence for body_type, engine, transmission, fuel_type, drivetrain, trim.
The current review blocker exists because the catalog client returned malformed/non-object JSON and `technical_variants_il` is empty.
No reliable Israeli source found by ChatGPT for horsepower. Do not guess horsepower. If horsepower is not grounded, leave `horsepower_hp = null` only if allowed by current schema/website rules; otherwise move the affected row to non-blocking archive, not active review blocker.
```

### Daihatsu Move — evidence is insufficient for verified clean

Sources checked:

```text
https://www.icar.co.il/דייהטסו/
https://www.auto.co.il/catalog/brands/daihatsu
https://autoboom.co.il/catalog/cars/daihatsu/move
```

Verified facts:

```text
Current review blocker has no technical variants and only generic Daihatsu brand/catalog pages.
ChatGPT did not find strong Israeli-market technical support for a Daihatsu Move clean profile.
Autoboom page says the model is not available in Israel; this is not enough to build clean variants.
Do not fabricate a Move technical row. Resolve as non-blocking archive/rejected-uncertain, not clean and not active blocker.
```

### Dodge Journey — existing review row has variants but missing `source_indexes`

Existing review row already contains sources:

```text
0. Auto.co.il Dodge Journey 2008-2016 technical page
1. Cartube 2012 Dodge Journey launch in Israel
2. iCar Dodge Journey used-car page
```

Existing review row already has two plausible variants:

```text
1. SXT, SUV, petrol, 2.4L, 170 hp, 4-speed automatic, FWD, year_start=2008, year_end=2016.
2. R/T, SUV, petrol, 3.6L V6, 283 hp, 6-speed automatic, AWD, year_start=2012, year_end=2016.
```

Current blocking issue is structural, not factual:

```text
variant[0] has no source_indexes
variant[0] support_level=direct but no source directly supports it
variant[1] has no source_indexes
variant[1] support_level=direct but no source directly supports it
```

Repair by adding `source_indexes` consistent with `field_sources`, not by changing the technical facts unless field-level evidence contradicts them.

### Dodge Charger — weak/price-list-only Israeli evidence

Source checked:

```text
https://www.yad2.co.il/price-list/feed?manufacturer=13&model=10162
```

Verified facts:

```text
Yad2 price list has Dodge Charger entries in Israel, including GT 3.6 300 hp, Scat Pack 6.4 485 hp, Hellcat 6.2 707/717 hp depending year/door/body listing, and older SXT 3.6 292 hp rows.
This is a low-tier marketplace/price-list source, not a strong importer/editorial technical source.
Do not put Dodge Charger into verified clean using Yad2 alone unless the repository already has stronger field-level sources in the original source_ids.
If no stronger Israeli source exists inside the repo, resolve the blocker by moving Dodge Charger to a non-blocking archive/rejected-uncertain bucket with reason `insufficient strong Israeli source`, not by fabricating clean variants.
```

### Dodge Challenger — clean tail audit

Sources checked:

```text
https://www.icar.co.il/dodge/challenger/
https://www.yad2.co.il/price-list/feed?manufacturer=13&model=10161
https://www.carzone.co.il/Dodge/Challenger/2024/
```

Verified facts:

```text
Current clean rows are SXT 3.6 V6, R/T 5.7 V8, R/T Scat Pack 6.4 V8, SRT Hellcat 6.2 supercharged.
Israeli price-list sources show Challenger SXT/GT/R/T/Scat Pack/Hellcat rows across years.
Be careful with Hellcat horsepower: some Israeli price-list rows show 707 hp, not 717 hp. Do not keep 717 hp unless the row's own source directly supports 717 for that exact Israeli listing/year/body. If 717 is not directly supported, correct Hellcat to 707 hp or move the 717 hp row to non-blocking archive.
Do not add weak GT rows unless source support is strong enough and field-level grounded.
```

---

## Required corrections / actions

### A. Tail clean models

#### 1. Daihatsu Terios — KEEP, audit only

Current clean catalog has three technical rows:

```text
1997-2006 1.3L petrol 86 hp, 4-speed automatic, 4WD
1997-2006 1.3L petrol 86 hp, 5-speed manual, 4WD
2006-2012 1.5L petrol 104 hp, 4-speed automatic, 4WD
```

Action:

```text
KEEP unless tests reveal broken field_sources.
Do not add trims just to fill null `version_or_trim`; null trim is acceptable where the sources are technical/generation rows and no precise Israeli trim is fully grounded.
Verify `field_sources` and `source_indexes` are valid.
```

#### 2. Daihatsu YRV — KEEP, audit only

Current clean catalog has:

```text
CX, MPV, petrol, 1.3L i4, 87 hp, 4-speed automatic, FWD, 2001-2005
```

Action:

```text
KEEP.
No new variants unless an in-repo Israeli source directly supports additional trims/gearboxes.
```

#### 3. Dodge Caliber — KEEP with one normalization check

Current clean catalog has:

```text
SXT, Hatchback, petrol, 2.0L, 156 hp, CVT, FWD, 2006-2012
SRT4, Hatchback, petrol, 2.4L turbo, 295 hp, manual, FWD, 2008-2009
```

Action:

```text
KEEP if existing source_indexes/field_sources are valid.
Normalize trim display to `SRT-4` if current catalog conventions prefer hyphenated Dodge naming and the source title uses SRT-4; otherwise leave as `SRT4` only if existing conventions already use it.
Do not add weak rows.
```

#### 4. Dodge Challenger — FIX/AUDIT Hellcat horsepower support

Current clean catalog has:

```text
SXT — 3.6L V6, 305 hp, 8-speed automatic, RWD, 2015-2023
R/T — 5.7L V8, 372 hp, 8-speed automatic, RWD, 2015-2023
R/T Scat Pack — 6.4L V8, 485 hp, 8-speed automatic, RWD, 2015-2023
SRT Hellcat — 6.2L supercharged V8, 717 hp, 8-speed automatic, RWD, 2015-2023
```

Action:

```text
KEEP SXT/R/T/Scat Pack if field_sources are valid.
For SRT Hellcat, do not keep 717 hp unless the row source directly supports 717 hp for the Israeli Challenger listing.
If only the available Israeli price-list support shows 707 hp for Hellcat, FIX SRT Hellcat horsepower_hp to 707.
If the repo has a strong source for a 717 hp Redeye/Widebody row, then split it as a separate exact trim; otherwise do not infer it.
Do not use generic Levi Yitzhak homepage as field-level evidence unless the actual row/source has specific field support.
```

#### 5. Dodge Durango — KEEP, audit source tiers

Current clean catalog has:

```text
GT — 3.6L V6, 295 hp, 8-speed automatic, AWD, 2011-2024
R/T — 5.7L V8, 360 hp, 8-speed automatic, AWD, 2011-2024
SRT 392 — 6.4L V8, 475 hp, 8-speed automatic, AWD, 2018-2024
SRT Hellcat — 6.2L supercharged V8, 710 hp, 8-speed automatic, AWD, 2021-2024
```

Action:

```text
KEEP if source_indexes and field_sources are valid.
Do not extend to 2026/current from non-Israeli sources. This catalog is Israeli-market; current global Durango news is not Israeli grounding.
If `SRT Hellcat` is backed only by a weak/import listing, keep only if current project allows low-volume import/price-list evidence in clean; otherwise move that specific row to non-blocking archive.
```

#### 6. Dodge Nitro — KEEP

Current clean catalog has:

```text
SXT — SUV, petrol, 3.7L V6, 205 hp, 4-speed automatic, 4WD, 2007-2011
```

Action:

```text
KEEP if source_indexes and field_sources are valid.
No need to add 4.0L/R/T or diesel rows unless Israeli sources directly support them.
```

---

### B. Active blockers / review-only models

#### 7. Citroen DS4 — RESTORE FROM INTERNAL LEGACY EVIDENCE

Current state:

```text
review-only blocker
technical_variants_il = []
error = Extra data / malformed JSON
```

Action:

```text
FIX / RESTORE.
Build a clean Citroen DS4 profile from the two high-confidence rows already present in `data/validation_variants_data_v1.json`.
```

Target rows:

```text
Citroen DS4
variant 1:
- version_or_trim: Sport Chic
- body_type: Hatchback
- fuel_type: petrol
- engine: 1.6L turbo
- engine_displacement_l: 1.6
- horsepower_hp: 163
- transmission: 6-speed automatic
- drivetrain: FWD
- year_start: 2012
- year_end: 2015
- support_level: direct
- source_indexes / field_sources: map from the original legacy source_ids for this row, not guessed

variant 2:
- version_or_trim: Sport Chic
- body_type: Hatchback
- fuel_type: petrol
- engine: 1.6L turbo
- engine_displacement_l: 1.6
- horsepower_hp: 200
- transmission: 6-speed manual
- drivetrain: FWD
- year_start: 2012
- year_end: 2015
- support_level: direct
- source_indexes / field_sources: map from the original legacy source_ids for this row, not guessed
```

Do not leave DS4 as active blocker.

If source-id mapping cannot be reconstructed safely from the repo, move DS4 rows to non-blocking archive with the embedded legacy evidence; do not keep in active review blocker.

#### 8. Citroen ë-C4 — RESTORE ELECTRIC PROFILE

Current state:

```text
review-only blocker
technical_variants_il = []
error = malformed JSON
```

Action:

```text
FIX / RESTORE.
Prefer a separate model `Citroen ë-C4`, consistent with existing separate Citroen ë-Berlingo and ë-C3 convention.
```

Target minimum clean row if sources can be mapped:

```text
Citroen ë-C4
- version_or_trim: Shine
- body_type: Hatchback
- fuel_type: electric
- engine: electric motor
- engine_displacement_l: null
- horsepower_hp: 136
- transmission: automatic
- drivetrain: FWD
- year_start: 2021
- year_end: null only if current official e-C4 source in repo is accepted; otherwise year_end=2024/2025 according to source support
- support_level: direct
```

Important trim rule:

```text
The raw candidate had `Fine`. Cartube/iCar 2021 evidence supports `Shine`.
Only keep `Fine` if an in-repo current Citroen/Lubinski source directly supports Fine as Israeli trim.
Do not keep Fine just because the malformed model output produced it.
```

Do not duplicate with `Citroen C4 X` electric. `C4 X` and `ë-C4` are different body/model lines.

#### 9. Dacia Jogger — RESTORE OFFICIAL CURRENT + HISTORICAL LAUNCH VARIANTS

Current state:

```text
review-only blocker
technical_variants_il = []
error = malformed JSON
```

Action:

```text
FIX / RESTORE.
Dacia Jogger is a legitimate Israeli-market model and must not remain blocked.
```

Target rows:

```text
Dacia Jogger — historical launch gasoline row(s):
- version_or_trim: Essential / Expression / Expression Plus only if exact trims are directly supported in repo sources; otherwise use null trim or a single technical row with invalid_or_non_trim_labels documenting uncertain trims
- body_type: MPV or Crossover/MPV according to existing canonical enum
- fuel_type: petrol
- engine: 1.0L turbo
- engine_displacement_l: 1.0
- horsepower_hp: 110
- transmission: 6-speed manual
- drivetrain: FWD
- seats: 7 if schema supports seats
- year_start: 2022
- year_end: 2024 or 2025 depending source support; do not keep open-ended if current official page says only hybrid

Dacia Jogger — current hybrid row:
- version_or_trim: Expression
- body_type: MPV or Crossover/MPV according to current enum
- fuel_type: hybrid
- engine: 1.6L hybrid
- engine_displacement_l: 1.6
- horsepower_hp: 140 if using Cartube 2025 Hybrid 140; do not overwrite with 155 unless official Israeli source directly supports 155 for Jogger
- transmission: automatic
- drivetrain: FWD
- seats: 7 if schema supports seats
- year_start: 2024 or 2025 according to source support
- year_end: null/current
```

Use Dacia Israel official current page/pricing as highest-tier source for current existence, trim `Expression`, price/current status, and 1.6 hybrid automatic. Use Cartube/iCar/Auto for historical launch and horsepower if official source does not expose horsepower in parsed HTML.

#### 10. Daewoo Cielo — RESTORE FROM INTERNAL LEGACY EVIDENCE WITHOUT GUESSING HP

Current state:

```text
review-only blocker
technical_variants_il = []
error = malformed JSON
```

Action:

```text
FIX / RESTORE if schema allows horsepower_hp=null; otherwise ARCHIVE non-blocking.
Use internal legacy rows from validation_variants_data_v1.json. Do not invent horsepower.
```

Target rows:

```text
Daewoo Cielo
1. GLX, Hatchback, petrol, 1.5L, automatic, FWD, 1995-1998, horsepower_hp=null unless source-grounded
2. GLX, Sedan, petrol, 1.5L, automatic, FWD, 1995-1998, horsepower_hp=null unless source-grounded
3. GL, Hatchback, petrol, 1.5L, manual, FWD, 1995-1998, horsepower_hp=null unless source-grounded
4. GL, Sedan, petrol, 1.5L, manual, FWD, 1995-1998, horsepower_hp=null unless source-grounded
```

If `horsepower_hp` is required by current clean gate and no strong Israeli source supports the exact value, do not guess. Move these four rows to non-blocking archive/rejected-uncertain and remove the active review blocker.

#### 11. Daihatsu Move — DO NOT FABRICATE; ARCHIVE NON-BLOCKING

Current state:

```text
review-only blocker
technical_variants_il = []
only generic Daihatsu brand sources
```

Action:

```text
MOVE TO ARCHIVE / REJECTED-UNCERTAIN, not clean.
Reason: insufficient Israeli-market technical evidence.
Do not leave as active review-only blocker.
Do not create fake variants.
```

If the project has no archive sidecar yet, create a minimal non-blocking sidecar such as:

```text
data/model_technical_catalog_il_archive.json
```

or implement the equivalent existing convention. The archive must not count toward `review_only_blocked_entries` or `models_blocked`.

#### 12. Dodge Charger — DO NOT CLEAN ON YAD2 ALONE; ARCHIVE OR RESTORE ONLY WITH STRONG IN-REPO SOURCES

Current state:

```text
review-only blocker
technical_variants_il = []
error = non-object JSON
raw_database_values list trims/engines but no horsepower
```

Action:

```text
Prefer MOVE TO ARCHIVE / REJECTED-UNCERTAIN unless the repo already contains stronger direct Israeli field-level sources than Yad2.
Do not fabricate clean rows from raw trims/engines alone.
Do not use global 2026 Dodge sources for Israeli clean.
```

If, and only if, existing in-repo Israeli sources directly support exact variants, then restore only those exact rows. Potential Israeli price-list evidence exists for:

```text
GT 3.6 300 hp
Scat Pack 6.4 485 hp
Hellcat 6.2 707/717 hp depending exact year/listing
older SXT 3.6 292 hp
```

But Yad2 is a low-tier marketplace/price-list source. It may support archive documentation or low-confidence rows if your policy permits, but it is not enough for verified clean by itself.

#### 13. Dodge Journey — STRUCTURAL FIX: ADD SOURCE_INDEXES

Current state:

```text
review-only blocker has two valid-looking variants but each variant lacks `source_indexes`.
```

Action:

```text
FIX / MOVE TO CLEAN.
Do not rewrite the whole profile. Add valid `source_indexes` arrays consistent with existing `field_sources`.
```

Target rows:

```text
variant 1:
- version_or_trim: SXT
- body_type: SUV
- fuel_type: petrol
- engine: 2.4L
- engine_displacement_l: 2.4
- horsepower_hp: 170
- transmission: 4-speed automatic
- drivetrain: FWD
- year_start: 2008
- year_end: 2016
- source_indexes: include all source indexes used by field_sources, at minimum [0, 2], and include [1] only for fields it directly supports

variant 2:
- version_or_trim: R/T
- body_type: SUV
- fuel_type: petrol
- engine: 3.6L v6
- engine_displacement_l: 3.6
- horsepower_hp: 283
- transmission: 6-speed automatic
- drivetrain: AWD only if source 0/1 directly supports AWD; otherwise use FWD or archive uncertainty according to the source
- year_start: 2012
- year_end: 2016
- source_indexes: include all source indexes used by field_sources, at minimum [0, 1, 2]
```

Important:

```text
The blocker is caused by missing source_indexes / direct-support validation, not by missing model existence.
After repair, no Journey entry should remain in review.
```

---

### C. Mandatory Chery Tiggo 4 HEV carry-forward fix

Current state:

```text
Chery Tiggo 4 Pro exists in clean with two petrol rows:
- Noble, 1.5L petrol, 95 hp, CVT, 2024-2025
- Comfort, 1.5L petrol, 95 hp, CVT, 2025-current
Chery Tiggo 4 HEV is missing from clean and review.
```

Action:

```text
ADD / RESTORE Chery Tiggo 4 HEV as a separate clean model.
Do not merge it silently into Tiggo 4 Pro unless the project explicitly forbids separate HEV lines. The preferred convention is separate model `Chery Tiggo 4 HEV`, because Chery Israel presents TIGGO 4 HEV as a separate model/line alongside TIGGO 4 Pro.
```

Target model:

```text
make: Chery
model: Tiggo 4 HEV
canonical_model: Tiggo 4 HEV
market: IL
year_start: 2025
year_end: null
profile_confidence: high
sources: Chery Israel official TIGGO 4 HEV page
```

Target rows:

```text
Chery Tiggo 4 HEV Comfort
- body_type: SUV
- fuel_type: hybrid
- engine: 1.5L hybrid
- engine_displacement_l: 1.5
- horsepower_hp: 163
- transmission: DHT automatic
- drivetrain: FWD
- year_start: 2025
- year_end: null
- support_level: direct

Chery Tiggo 4 HEV Luxury
- same technical data

Chery Tiggo 4 HEV Noble
- same technical data
```

Why three rows are allowed:

```text
The official Chery Israel page lists TIGGO 4 HEV COMFORT, TIGGO 4 HEV LUXURY, and TIGGO 4 HEV NOBLE in the safety/trim table.
The same official page provides the shared technical basis: 1.5 liter, 95 hp gasoline engine, 204 hp electric motor, combined 163 hp, DHT automatic transmission.
```

Alias/lineage to add:

```text
IL|Chery|Tiggo 4 Hybrid -> IL|Chery|Tiggo 4 HEV
IL|Chery|TIGGO 4 HEV -> IL|Chery|Tiggo 4 HEV
IL|Chery|Tiggo4 HEV -> IL|Chery|Tiggo 4 HEV
```

Do not leave Chery Tiggo 4 HEV as unmatched, deleted, or missing.

---

## Split / unmatched / casing / duplicate checks

Current resume state before RUN 3:

```text
unmatched_output_keys_count = 0
unmatched_output_keys_sample = []
split_profile_alias_count = 8
```

Action:

```text
Keep unmatched_output_keys_count at 0.
Do not break existing split aliases.
Add Chery Tiggo 4 HEV aliases above without creating unmatched source/output keys.
Verify no make casing leftovers such as `Bmw` are introduced.
Verify no list-valued `version_or_trim` remains after applying repairs.
Verify duplicate_technical_variants remains 0.
```

Existing split aliases that must remain matched:

```text
Junior Elettrica -> Junior
M850i -> 850i
X5 xDrive30d -> X5 3.0d
Atto 3 EVO -> Atto 3
Escalade IQ -> Escalade
Tiggo 9 Pro PHEV -> Tiggo 9
Seal U / Song Plus aliasing must not regress
```

---

## Code/reporting requirements

1. If a model is intentionally moved out of active review due to insufficient Israeli source support, preserve an audit trail in a non-blocking archive/rejected sidecar or migration script.

2. Active review blockers must represent items still requiring repair. They must not be used as a permanent uncertainty archive if the final upload target requires:

```text
review_only_blocked_entries = 0
models_blocked = 0
active_blocked = 0
```

3. Do not weaken validator logic just to get green metrics.

4. If schema/normalization changes are needed, they must be deterministic and covered by tests.

5. Keep optional-null rules from Batch 21 intact:

```text
EV engine_displacement_l = null is valid.
year_end = null is valid for current/open-ended rows.
version_or_trim = null is valid only when there is no grounded trim or the row is intentionally technical/generic.
```

6. Do not collapse separate trims into a joined string unless they are truly one shared technical variant. If different trims are separate market variants, split them.

---

## Required final state after RUN 3

```text
models_blocked = 0
review_only_blocked_entries = 0
duplicate_technical_variants = 0
invalid_source_references = 0
unknown_support_values = 0
technical_variants_missing_required_grounding = 0
technical_variants_missing_grounded_fields = 0
ready_for_website_upload = true
unmatched_output_keys_count = 0
unmatched_output_keys_sample = []
active_blocked_count = 0
quality bug/normalization findings = 0
```

Non-blocking leak/structure findings may remain, but do not introduce new ones unnecessarily.

---

## Required commands/tests

Run at minimum:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
```

If full pytest fails because optional local dependencies are missing in the execution environment, report the exact import error and still run all data/catalog tests that can run. Do not claim success if tests were not run.

Also run a direct programmatic final-metrics audit from generated files and `compute_resume_state()`.

---

## Expected Codex response after execution

Return:

```text
1. Commit hash if committed
2. Files changed
3. Models touched
4. Variants added/fixed/moved/archived/deleted
5. Chery Tiggo 4 HEV exact result
6. Blockers resolved one by one
7. Alias/unmatched result
8. Quality scan counts
9. Readiness metrics
10. Tests run
11. Remaining risks before merge
```
