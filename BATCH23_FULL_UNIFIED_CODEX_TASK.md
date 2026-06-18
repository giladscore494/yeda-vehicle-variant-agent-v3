# BATCH 23 — RUN 1 CODEX TASK

Scope: RUN 1 only. Do **not** process RUN 2 / RUN 3 / RUN 4 / final blockers yet.

Task file is the source of truth for Codex. Do **not** browse the internet. All validation facts and target corrections are embedded here.

---

## Current ZIP state verified before RUN 1

Cursor window:

```text
previous baseline: IL|Dodge|Nitro
current resume_after_key: IL|Honda|CR-Z
current next_key_to_process: IL|Honda|e:Ny1
actual source groups in this cursor window: 88
clean groups in this cursor window: 59
review/blocker groups in this cursor window: 29
unmatched_output_keys_count: 0
split_profile_alias_count: 10
ready_for_website_upload: false
models_blocked: 29
review_only_blocked_entries: 29
unknown_support_values: 3  # in review, not clean
quality bug: 0
quality normalization: 0
quality leak: 111
quality structure: 330
```

Why the last-88 list is not clean enough:

1. The window contains 59 clean profiles and 29 review/blocker profiles, so the batch is mixed by construction.
2. Several source groups are duplicated or identity-split: DS/DS Crossback, DS Automobiles casing, GAC/Aion, global-reference-only vs IL-confirmed keys.
3. Some clean profiles are schema-green but data-quality weak: null trims where Israeli trim names are known, wrong casing, old model rows mixed with facelift/current rows, current models closed at 2024/2025, and weak/indirect support values.
4. The clean gate detects structural blockers but does not prove full Israeli-market coverage. Example: a model may be green while missing a current EV/PHEV row, or while using a broad model row instead of real Israeli trim rows.
5. Several blockers are parse/non-object JSON failures, not necessarily true lack of data. They must be recovered in the final blockers run, not ignored.

---

## RUN 1 clean-model scope

Validate and correct only these 15 clean source groups:

```text
1. IL|Dodge|Ram
2. IL|Dongfeng|Box
3. IL|DS Automobiles|DS 3
4. IL|DS Automobiles|DS 4
5. IL|DS Automobiles|DS 7
6. IL|Ds Automobiles|ds 9
7. IL|Ferrari|296 GTB
8. IL|Ferrari|458 Italia
9. IL|Ferrari|488 GTB
10. IL|Ferrari|812 Superfast
11. IL|Ferrari|California
12. IL|Ferrari|GTC4Lusso
13. IL|Ferrari|Portofino
14. IL|Ferrari|Purosangue
15. IL|Ferrari|Roma
```

Do not resolve the 29 blockers in this RUN 1 file, except where a RUN 1 clean profile must be split/lineaged to avoid duplicating a blocker later. Keep blockers for the final blockers run.

---

## General RUN 1 rules

- If a value is already correct and grounded, KEEP it.
- If an Israeli source proves a more exact trim/body/powertrain/year, FIX it.
- If the profile is really an alias/split of another Israeli profile, add alias/lineage and prevent unmatched output keys.
- Do not invent a variant from global data only.
- Do not keep a weak or unsupported variant in clean just to satisfy readiness. Move uncertain rows to non-blocking review/archive if required.
- `engine_displacement_l = null` is valid for EVs.
- `year_end = null` is valid for current/open-ended Israeli models.
- `version_or_trim = null` is only valid when Israeli evidence does not expose a marketed trim. If Israeli trims are known, use scalar trim names; do not store lists.
- After changes, rebuild catalog outputs and run validation, quality scan, and tests.

---

# RUN 1 corrections and audit instructions

## 1. Dodge Ram — KEEP historic Dodge profile, but do not lose current RAM lineage

Current clean profile:

```text
make=Dodge, model=Ram
rows:
- null trim, Pickup, diesel, 5.9L turbo, 235 hp, automatic, 4WD, 1994-2002
- SLT, Pickup, diesel, 5.9L turbo, 325 hp, automatic, 4WD, 2003-2007
- SLT, Pickup, diesel, 6.7L turbo, 350 hp, automatic, 4WD, 2007-2009
```

Validation facts:

- Auto.co.il’s Dodge Ram page supports later heavy-duty Ram rows and shows 6.7L diesel SLT configurations; it also indicates 2011+ rows under the legacy Dodge Ram page.
- Ram Israel currently markets RAM under the RAM brand, not necessarily `Dodge` as make.
- iCar’s current RAM 2500/3500 pages list 2025/2026 RAM rows such as 6.7 Laramie/Limited variants, so current RAM vehicles must not be silently lost or incorrectly forced under `Dodge|Ram`.

Sources:

```text
https://www.auto.co.il/cars/dodge/ram/
https://www.icar.co.il/ראם/ראם_2500/ראם_2500_חדש/version21605/
https://www.ram.com/il/
https://www.ram.com/il/ram-2500.html
```

Action:

```text
KEEP the three existing historic Dodge Ram rows if their source_indexes/field_sources remain valid.
DO NOT extend current 2025/2026 RAM 2500/3500 under make=Dodge unless the project has no separate RAM/Ram make convention.
If source data includes 2011+ or current Ram rows under Dodge Ram, add alias/lineage so those can be represented under make=Ram / model=2500 or 3500 in a future/current RAM profile, not as a wrong Dodge clean row.
```

No immediate blocker if the current catalog intentionally only covers historic `Dodge Ram`; but add a note/lineage guard so the next cursor batch does not regress or duplicate RAM.

---

## 2. Dongfeng Box — FIX current/open-ended year range

Current clean profile:

```text
make=Dongfeng, model=Box
year_start=2024, year_end=2025
variant: electric hatchback, 95 hp, single_speed, FWD
```

Validation facts:

- Dongfeng Israel has an active official Box page.
- Cartube reports the Israeli launch in December 2024 as a 2025 price/model context, 95 hp, 310 km range.
- Auto.co.il and Carzone list Box technical values with 95 hp and FWD; Carzone has 2026 data.

Sources:

```text
https://dongfeng.co.il/models/box/
https://www.cartube.co.il/חדשות-רכב/דונגפנג-בוקס-החשמלית-בישראל-מחיר-113900-שקל
https://www.auto.co.il/cars/dongfeng/box/
https://www.carzone.co.il/Dongfeng/Box/
```

Action:

```text
FIX year_start to 2025 unless internal source explicitly proves Israeli registration/marketing in 2024.
FIX year_end to null/current; do not close this current model at 2025.
KEEP: body_type=Hatchback, fuel_type=electric, engine=electric, engine_displacement_l=null, horsepower_hp=95, transmission=single_speed, drivetrain=FWD.
```

---

## 3. DS Automobiles DS 3 — SPLIT legacy hatchback, DS 3 Crossback, and facelift/current DS 3

Current clean profile is mixed:

```text
make=DS Automobiles, model=DS 3
rows:
- So Chic hatchback 1.2 turbo 110 hp 6AT 2015-2019
- Sport Chic hatchback 1.6 turbo 165 hp 6MT 2015-2019
- Rivoli crossover 1.2 turbo 130 hp 8AT 2019-2024
- Grand Chic crossover 1.2 turbo 155 hp 8AT 2019-2021
```

Problem:

The profile mixes the legacy DS 3 hatchback with DS 3 Crossback / later DS 3 crossover. This is why the list is not clean: the engine passes readiness, but the identity/lineage is wrong and can duplicate the `IL|DS Automobiles|DS 3 Crossback` blocker that is waiting for the final run.

Validation facts:

- DS 3 Crossback in Israel launched in 2019 as a crossover/SUV with 1.2 turbo 130 hp and 155 hp, 8-speed automatic.
- Israeli sources list DS 3 Crossback E-Tense electric 136 hp from 2021/2023 context.
- In 2023 the facelift/current model is marketed as DS 3, with DS 3 E-TENSE 156 hp Rivoli and 54 kWh/395 km WLTP source facts.
- The old DS 3 hatchback 2015-2019 is a different body/line from the Crossback/crossover line.

Sources:

```text
https://www.cartube.co.il/חדשות-רכב/ds3-קרוסבק-בישראל-מחיר-178990-שקל
https://www.auto.co.il/cars/ds/ds3-crossback/
https://www.icar.co.il/DS/DS_3_קרוסבק/DS_3_קרוסבק_יד_שניה_ד10/version24866/
https://www.icar.co.il/רכב_חשמלי/DS3_קרוסבק_החשמלי_בישראל:_199,000_שקלים/
https://www.cartube.co.il/חדשות-רכב/ds3-e-tense-החשמלי-החדש-2023-בישראל-מחיר-214990-שקל
https://www.auto.co.il/cars/ds/ds3/2023/535950/
```

Action:

```text
SPLIT / FIX identity:

A. Keep under `DS Automobiles|DS 3` only the legacy hatchback rows:
   - So Chic, Hatchback, petrol, 1.2L turbo, 110 hp, 6-speed automatic, FWD, 2015-2019.
   - Sport Chic, Hatchback, petrol, 1.6L turbo, 165 hp, 6-speed manual, FWD, 2015-2019.

B. Move the 2019-2022 crossover rows to `DS Automobiles|DS 3 Crossback` lineage:
   - So Chic / Performance Line, Crossover/SUV, petrol, 1.2L turbo, 130 hp, 8-speed automatic, FWD, 2019-2022/2023.
   - Grand Chic / Rivoli, Crossover/SUV, petrol, 1.2L turbo, 155 hp, 8-speed automatic, FWD, 2019-2022/2023.
   - E-Tense / Grand Chic / Rivoli, Crossover/SUV, electric, 136 hp, single_speed, FWD, 2021-2023.

C. For facelift/current `DS 3` 2023+:
   - Ensure `DS 3 E-TENSE Rivoli`, Crossover/SUV, electric, 156 hp, single_speed, FWD, year_start=2023, year_end=null/current if the project convention treats facelift as DS 3 rather than DS 3 Crossback.

D. Add alias/lineage:
   - `IL|DS Automobiles|DS 3 Crossback` -> relevant Crossback/crossover profile.
   - `DS3 Crossback`, `DS 3 Crossback`, `DS3`, `DS 3` must not create unmatched output keys.
```

If RUN 1 cannot safely repair the blocker profile yet, at minimum prevent DS 3 clean from continuing to mix hatchback and Crossback rows without lineage. The final blockers run will fully recover `DS 3 Crossback`.

---

## 4. DS Automobiles DS 4 — FIX null trim rows into Israeli trim rows

Current clean profile:

```text
make=DS Automobiles, model=DS 4
rows:
- null trim, petrol 1.6 turbo 225 hp, 8AT, FWD, 2022-2024
- null trim, PHEV 1.6 turbo 225 hp, 8AT, FWD, 2022-2024
```

Problem:

Israeli sources expose real trim names. Null trim is not justified here.

Validation facts:

- Cartube’s Israeli launch article lists DS4 1.6 turbo 225 hp Trocadero and Performance Line.
- It also lists DS4 E-TENSE PHEV 225 hp Trocadero and Rivoli.
- iCar and Auto confirm 1.6 turbo 225 hp petrol and PHEV with 8-speed automatic and FWD.

Sources:

```text
https://www.cartube.co.il/חדשות-רכב/ds4-החדשה-2022-בישראל-מחיר-218990-שקל
https://www.icar.co.il/DS/DS_4/DS_4_חדש/
https://www.auto.co.il/cars/ds/ds4/
https://online.dsautomobiles.co.il/article_cat/ds-4/
```

Action:

```text
SPLIT/FIX into scalar trim rows:

- Trocadero, Hatchback, petrol, 1.6L turbo, 225 hp, 8-speed automatic, FWD, 2022-2024.
- Performance Line, Hatchback, petrol, 1.6L turbo, 225 hp, 8-speed automatic, FWD, 2022-2024.
- Trocadero, Hatchback, plug_in_hybrid, 1.6L turbo, 225 hp, 8-speed automatic, FWD, 2022-2024.
- Rivoli, Hatchback, plug_in_hybrid, 1.6L turbo, 225 hp, 8-speed automatic, FWD, 2022-2024.

Do not keep broad null-trim DS 4 rows if the trim-specific rows are added.
```

---

## 5. DS Automobiles DS 7 — ADD/FIX trim context; do not leave current PHEV rows broad/null if exact trim is known

Current clean profile has six rows, all `version_or_trim=null`, covering diesel, petrol, PHEV 225/300/360.

Validation facts:

- iCar states that after the facelift DS7 is marketed with PHEV powertrains from 225 to 360 hp, all based on 1.6 turbo.
- Cartube’s 2023 DS7 Israel article supports E-TENSE 225, E-TENSE 300 4x4, and E-TENSE 360 4x4; the DS official online page supports 360 hp 4X4.
- Auto.co.il/iCar expose trim names like Rivoli, Grand Chic Inspiration Opera, Performance Line etc.

Sources:

```text
https://www.icar.co.il/DS/DS_7/DS_7_יד_שניה_ד10/
https://www.cartube.co.il/חדשות-רכב/2023-ds7-החדש-בישראל-מחיר-339990-שקל
https://www.cartube.co.il/מחירון-רכב-חדש/ds/ds7/911-ds-7-קרוסבק-1-6-טורבו-פלאג-אין-300-כ-ס-4x4-rivoli
https://online.dsautomobiles.co.il/model/ds-7-e-tense/
https://www.auto.co.il/cars/ds/ds7-crossback/2023/
```

Action:

```text
KEEP the technical powertrain coverage if valid:
- diesel 1.5 130 FWD 8AT historical.
- diesel 2.0 180 FWD 8AT historical.
- petrol 1.6 225 FWD 8AT historical.
- PHEV 225 FWD 8AT.
- PHEV 300 AWD 8AT.
- PHEV 360 AWD 8AT.

FIX trim/context where source supports it:
- At least facelift/current PHEV 225/300/360 rows should carry `Rivoli` or the exact Israeli trim from source where available.
- Do not leave all rows with null trim if source-specific trim data exists.
- DS official current page supports 360 hp 4X4; if keeping 360 as current, set year_end=null/current only if source state is current. Otherwise leave year_end as source-backed 2024 and do not guess.
```

---

## 6. Ds Automobiles ds 9 — FIX casing and keep DS 9 powertrain split

Current clean key/profile casing:

```text
make=Ds Automobiles
model=ds 9
canonical_model=ds 9
```

Problem:

This is a casing/identity defect in clean. It should not pass to website as `Ds Automobiles|ds 9`.

Validation facts:

- Israeli/DS source naming is `DS 9` under `DS Automobiles`/`DS`.
- iCar launch and Auto explain DS 9 powertrain range: 1.6 turbo petrol 225, PHEV 225/250, and E-TENSE 4x4 360. Cartube/iCar support Rivoli/Opera trim context.

Sources:

```text
https://www.icar.co.il/חדשות_רכב/DS_9:_מכונית_יוקרה_חדשה/
https://www.auto.co.il/articles/test-drives/first-drives/135032/
https://www.icar.co.il/DS/די_אס_9/
```

Action:

```text
FIX make/model casing:
- make: `DS Automobiles`
- model: `DS 9`
- canonical_model: `DS 9`

Add alias/lineage from old key:
- `IL|Ds Automobiles|ds 9` -> `IL|DS Automobiles|DS 9`

KEEP powertrain rows if field sources remain valid:
- Rivoli petrol 1.6 turbo 225 hp FWD 8AT 2021-2022.
- Rivoli PHEV 225 hp FWD 8AT 2021-2022.
- Rivoli PHEV 250 hp FWD 8AT 2022-2024.
- Opera PHEV 360 hp AWD 8AT 2022-2024.

If the sources prove different trim/year cutoffs, adjust year ranges; do not leave casing defect.
```

---

## 7. Ferrari 296 GTB — FIX current/open-ended year and avoid losing 2026 GTB

Current clean profile:

```text
Ferrari 296 GTB
one row: Coupe, PHEV, 3.0L V6 turbo, 830 hp, 8-speed dual_clutch, RWD, 2022-2024
```

Validation facts:

- Israeli Auto/Cartube/iCar support 296 GTB with 3.0 V6 PHEV, 830 hp, 8-speed dual-clutch, RWD, launched/sold in Israel from 2022.
- iCar and Cartube have 2026 Ferrari 296 GTB pages, so the GTB should not be capped at 2024.
- Carzone also shows Ferrari 296 2026 with GTB/GTS variants; do not add GTS under GTB unless the model convention is `Ferrari 296` instead of `296 GTB`.

Sources:

```text
https://www.auto.co.il/articles/car-news/local-news/135112/
https://www.icar.co.il/פרארי/פרארי_296/פרארי_296_חדש/version24649/
https://www.cartube.co.il/מחירון-רכב-חדש/פרארי/פרארי-gtb-296
https://www.carzone.co.il/Ferrari/296/
```

Action:

```text
FIX year_end from 2024 to null/current or 2026-current according to project convention.
KEEP technical values: Coupe, plug_in_hybrid, 3.0L v6 turbo, 830 hp, 8-speed dual_clutch, RWD, year_start=2022.
DO NOT add 296 GTS under `296 GTB`; if the project later creates `Ferrari 296`, split GTB/GTS there with alias/lineage.
```

---

## 8. Ferrari 458 Italia — KEEP, but verify Speciale row is grounded and not overextended

Current clean profile:

```text
- base Coupe, 4.5L V8, 570 hp, 7-speed dual_clutch, RWD, 2011-2015.
- Spider, Convertible, 4.5L V8, 570 hp, 7-speed dual_clutch, RWD, 2012-2015.
- Speciale, Coupe, 4.5L V8, 605 hp, 7-speed dual_clutch, RWD, 2014-2015.
```

Validation facts:

- Israeli/technical sources support 458 Italia 570 hp and Speciale 605 hp.
- Spider was offered in Israel; the current row is plausible.

Sources:

```text
https://www.auto.co.il/model/ferrari-458_g375
https://cars.walla.co.il/item/2723725
https://www.auto.co.il/articles/car-news/113686/
```

Action:

```text
KEEP if all source_indexes/field_sources remain valid.
Do not add Speciale A unless Israeli source exists and it is intentionally within this source group.
Do not extend beyond 2015.
```

---

## 9. Ferrari 488 GTB — KEEP

Current clean profile:

```text
Coupe, petrol, 3.9L V8 twin-turbo, 670 hp, 7-speed dual_clutch, RWD, 2015-2019.
```

Validation facts:

- Israeli/technical sources support 488 GTB with V8 turbo and 670 hp.
- 488 GTB replaced 458 and was later replaced by F8; 2015-2019 range is plausible.

Sources:

```text
https://www.cartube.co.il/חדשות-רכב/פרארי-מציגה-488-gtb-–-מחליפת-ה-458-איטליה
https://www.ynet.co.il/articles/0,7340,L-4622490,00.html
https://www.auto.co.il/model/ferrari-488_g1281
```

Action:

```text
KEEP if field sources are valid.
No GTS/Spider rows should be created under `488 GTB` unless the source group explicitly requires them.
```

---

## 10. Ferrari 812 Superfast — KEEP closed historical/current-to-2024 row

Current clean profile:

```text
Coupe, petrol, 6.5L V12, 800 hp, 7-speed dual_clutch, RWD, 2018-2024.
```

Validation facts:

- Israeli sources list Ferrari 812 Superfast 2018-2024 and 800 hp/6.5 V12.
- No correction required in RUN 1 unless source references are broken.

Sources:

```text
https://www.icar.co.il/פרארי/פרארי_812_סופרפאסט/פרארי_812_סופרפאסט_יד_שניה_ד10/
https://www.auto.co.il/model/ferrari-812-superfast_g1323
```

Action:

```text
KEEP.
Do not reopen year_end unless an Israeli 2025/2026 812 Superfast source is present.
```

---

## 11. Ferrari California — KEEP, but normalize California T displacement carefully

Current clean profile:

```text
- base California, Convertible, petrol, 4.3L V8, 490 hp, 7-speed dual_clutch, RWD, 2012-2014.
- California T, Convertible, petrol, 3.9L V8 twin-turbo, 560 hp, 7-speed dual_clutch, RWD, 2014-2017.
```

Validation facts:

- Israeli sources support California T arriving in Israel in 2014, 560 hp, V8 turbo, 7-speed dual clutch.
- Some Israeli articles state 3.8L/3.9L depending on rounding. Existing canonical 3.9L is acceptable if the project rounds 3855 cc to 3.9L.

Sources:

```text
https://www.auto.co.il/articles/car-news/112525/
https://www.icar.co.il/חדשות_רכב/פרארי_קליפורניה_T:_מנוע_טורבו_וגג_נפתח_ב-1,850,000_שקל/
https://www.cartube.co.il/חדשות-רכב/פרארי-קליפורניה-t-בישראל-–-החל-מ-1-85-מיליון-שקל
```

Action:

```text
KEEP both rows if field sources are valid.
If strict displacement normalization prefers exact 3855 cc, keep display engine as `3.9L v8 twin-turbo`; do not create conflict between 3.8 and 3.9 rows.
```

---

## 12. Ferrari GTC4Lusso — KEEP with source consistency check

Current clean profile:

```text
- V12 row: Coupe, petrol, 6.3L V12, 690 hp, 7-speed dual_clutch, AWD, 2016-2020.
- T row: Coupe, petrol, 3.9L V8 turbo, 610 hp, 7-speed dual_clutch, RWD, 2017-2020.
```

Validation facts:

- Israeli sources support GTC4Lusso V12 690 hp and GTC4Lusso T 3.9 turbo 610 hp.
- iCar may display the V12 row as 6.2L while technical displacement is approximately 6.3L / 6262 cc; avoid duplicating 6.2 and 6.3 as separate variants.

Sources:

```text
https://www.icar.co.il/פרארי/פרארי_GTC4Lusso/פרארי_GTC4Lusso_יד_שניה_ד10/version22811/
https://www.cartube.co.il/חדשות-רכב/2-65-מיליון-שקל-והיא-שלכם-פרארי-gtc4-lusso-בישראל-2016
https://www.auto.co.il/articles/car-news/127844/
```

Action:

```text
KEEP both rows.
Do not create a duplicate 6.2L row. Use the project’s canonical displacement rounding consistently.
```

---

## 13. Ferrari Portofino — KEEP

Current clean profile:

```text
- Portofino, Convertible, petrol, 3.9L V8 twin-turbo, 600 hp, 7-speed dual_clutch, RWD, 2018-2021.
- Portofino M, Convertible, petrol, 3.9L V8 twin-turbo, 620 hp, 8-speed dual_clutch, RWD, 2021-2024.
```

Validation facts:

- Israeli sources support Portofino launch and Portofino M with 620 hp and 8-speed dual-clutch.
- No need to reopen year_end without current Israeli new-car evidence.

Sources:

```text
https://www.icar.co.il/חדשות_רכב/פרארי_פורטופינו_נחתה_בישראל/
https://www.cartube.co.il/חדשות-רכב/פרארי-פורטופינו-m-בישראל-מחיר-החל-מ-1650000-שקל
https://www.cartube.co.il/חדשות-רכב/פרארי-חושפת-את-הפורטופינו-m-מתיחת-פנים
```

Action:

```text
KEEP if source references are valid.
```

---

## 14. Ferrari Purosangue — FIX support_level and current year range

Current clean profile:

```text
Ferrari Purosangue
variant: SUV, petrol, 6.5L V12, 725 hp, 8-speed dual_clutch, AWD, 2023-2024, support_level=indirect
```

Problems:

- Israeli current sources support 2025/2026 Purosangue, so the row should not be capped at 2024.
- Field evidence appears direct: Israeli sources support 6.5 V12, 725 hp, AWD, price/current pages. If every non-null field is source-grounded, `support_level=indirect` is a quality bug-like weakness and should become direct.

Sources:

```text
https://www.icar.co.il/פרארי/פרארי_פורוסאנגווה/פרארי_פורוסאנגווה_חדש/version26376/
https://www.icar.co.il/חדשות_רכב/נחתה_ונחטפה_בישראל:_הפרארי_שעולה_כמעט_5_מיליון_שקלים/
https://www.auto.co.il/articles/car-news/local-news/136613/
https://www.carzone.co.il/Ferrari/Purosangue/2025/
```

Action:

```text
FIX year_end from 2024 to null/current or 2026-current according to project convention.
FIX support_level from indirect to direct only if all non-null fields have direct source support.
KEEP technical values: SUV, petrol, 6.5L V12, 725 hp, 8-speed dual_clutch, AWD, year_start=2023.
```

---

## 15. Ferrari Roma — FIX current/open-ended year range and distinguish Coupe vs Spider

Current clean profile:

```text
- Coupe, petrol, 3.9L V8 turbo, 620 hp, 8-speed dual_clutch, RWD, 2020-2024.
- Convertible, petrol, 3.9L V8 turbo, 620 hp, 8-speed dual_clutch, RWD, 2023-2024.
```

Validation facts:

- Roma Coupe and Roma Spider share 3.9L V8 twin-turbo, 620 hp, 8-speed dual-clutch, RWD.
- Carzone/Israeli sources have 2025 Roma/Spider data, so the profile should not be capped at 2024 without a discontinuation source.
- `version_or_trim` is null on both rows. Since the convertible body is actually `Roma Spider`, use `Spider` as trim/designation or ensure body_type distinguishes clearly and website values do not collapse coupe/convertible.

Sources:

```text
https://www.cartube.co.il/חדשות-רכב/פרארי-רומא-בישראל-מחיר-החל-מ-1-75-מיליון-שקל
https://www.cartube.co.il/חדשות-רכב/פרארי-רומא-ספיידר-נוחתת-בישראל
https://www.cartube.co.il/חדשות-רכב/פרארי-רומא-ספיידר-נחשפת-פרארי-רומא-עם-גג-נפתח
https://www.carzone.co.il/Ferrari/Roma/2025/
```

Action:

```text
FIX year_end for both Roma rows from 2024 to null/current or 2025-current according to project convention.
KEEP Coupe row technical values.
For convertible row, set version_or_trim=`Spider` if schema allows; otherwise keep version_or_trim=null but ensure body_type=Convertible and lineage/note identifies Roma Spider.
```

---

# RUN 1 expected output from Codex

After applying RUN 1 only:

```text
- Rebuild catalog outputs.
- Regenerate readiness and quality scan.
- Run:
  python -m compileall scripts
  python -m scripts.catalog_validation
  python -m scripts.catalog_quality_scan
  python -m pytest -q
```

Return:

```text
RUN 1 RESULT: PASS / PASS WITH WARNINGS / FAIL
1. Files changed
2. Models touched
3. Variants added/fixed/moved/archived
4. Alias/lineage changes
5. Readiness metrics
6. Quality scan counts: bug/leak/structure/normalization
7. Unmatched output keys count/sample
8. Tests run
9. Commit hash if committed
10. Remaining risks before RUN 2
```

Do not delete mapping files or future RUN task files unless explicitly asked.


---

# BATCH 23 — RUN 2 CODEX TASK

Scope: RUN 2 only. Do **not** process RUN 3 / RUN 4 / final blockers yet.

Task file is the source of truth for Codex. Do **not** browse the internet. All validation facts and target corrections are embedded here.

---

## Current ZIP state carried from Batch 23 mapping

```text
previous baseline: IL|Dodge|Nitro
current resume_after_key in uploaded ZIP: IL|Honda|CR-Z
current next_key_to_process in uploaded ZIP: IL|Honda|e:Ny1
actual source groups in this cursor window: 88
clean groups in this cursor window: 59
review/blocker groups in this cursor window: 29
unmatched_output_keys_count: 0
split_profile_alias_count: 10
ready_for_website_upload before fixes: false
models_blocked before fixes: 29
review_only_blocked_entries before fixes: 29
quality bug before fixes: 0
quality normalization before fixes: 0
```

RUN 1 has its own task file. This file adds RUN 2 instructions only.

---

## RUN 2 clean-model scope

Validate and correct only these 15 clean source groups:

```text
1. IL|Ferrari|SF90 Stradale
2. IL|Fiat|500
3. IL|Fiat|500L
4. IL|Fiat|600e
5. IL|Fiat|Bravo
6. IL|Fiat|Croma
7. IL|Fiat|Doblo
8. IL|Fiat|Ducato
9. IL|Fiat|Fiorino
10. global-reference-only|Fiat|Freemont
11. IL-confirmed|Fiat|Freemont
12. IL|Fiat|linea
13. IL|Fiat|Marea
14. IL|Fiat|Panda
15. IL|Fiat|Punto
```

Do not resolve final-run blockers such as Fiat 500e, Fiat 500X, Fiat Fullback, Multipla, Scudo, Stilo, Tempra, or Ulysse in this RUN 2 file. They remain for the final blockers/non-matching run unless a RUN 2 clean profile must be merged/aliased to avoid duplication.

---

## General RUN 2 rules

- If a value is already correct and grounded, KEEP it.
- If an Israeli source proves a more exact trim/body/powertrain/year, FIX it.
- If a profile is duplicated by `global-reference-only` and `IL-confirmed`, keep one Israeli clean profile and add alias/lineage; do not publish duplicate website models.
- Do not invent Israeli-market variants from global data only.
- If Israeli evidence is weak, move the uncertain row/profile to non-blocking archive/review, not active blocker and not clean.
- `engine_displacement_l = null` is valid for EVs.
- `year_end = null` is valid for current/open-ended Israeli models.
- `version_or_trim = null` is only valid when Israeli evidence does not expose a marketed trim. If Israeli trims are known, use scalar trim names; do not store lists.
- Avoid whole-catalog reordering. Make the smallest data/code changes needed.
- After changes, rebuild catalog outputs and run validation, quality scan, and tests.

---

# RUN 2 corrections and audit instructions

## 1. Ferrari SF90 Stradale — KEEP; ensure current/open-ended rows remain valid

Current clean rows:

```text
- null trim, Coupe, plug_in_hybrid, 4.0L twin-turbo v8, 1000 hp, 8-speed dual_clutch, AWD, 2020-current
- Assetto Fiorano, Coupe, same technical basis, 2020-current
- Spider, Convertible, same technical basis, 2021-current
- Spider Assetto Fiorano, Convertible, same technical basis, 2021-current
```

Validation facts:

- Israeli launch sources support SF90 Stradale as a PHEV with 4.0L twin-turbo V8 + three electric motors, 1000 hp combined, AWD, and 8-speed dual-clutch.
- Auto/Cartube Israeli sources confirm the model was marketed in Israel from 2021, and Spider was also marketed in Israel.
- `year_end = null` is acceptable if the project treats exotic Ferrari catalog rows as still purchasable/new-order or current-price-list rows; do not close it without a source proving Israeli discontinuation.

Sources embedded/validated:

```text
https://www.auto.co.il/articles/car-news/local-news/134456/
https://www.cartube.co.il/חדשות-רכב/סמלת-משיקה-אולמות-תצוגה-חדשים-ויוקרתיים-לפרארי-ומזראטי-ואת-פרארי-sf90-סטרדלה
https://www.cartube.co.il/חדשות-רכב/פרארי-היברידית-פלאג-אין-sp90-סטרדלה-נחשפת
```

Action:

```text
KEEP the four SF90 rows if source_indexes and field_sources are valid.
Do not mark EV/PHEV displacement or open year_end as missing.
If a support-level invariant exists because all populated fields are grounded but support_level is indirect, set support_level to direct only for the grounded rows.
```

---

## 2. Fiat 500 — FIX undercoverage and wrong/null trim handling

Current clean profile has only 5 rows:

```text
- Pop, Hatchback, petrol, 1.2L, 69 hp, manual, FWD, 2009-2021
- Lounge, Hatchback, petrol, 1.2L, 69 hp, automatic, FWD, 2009-2021
- null trim, Convertible, petrol, 1.2L, 69 hp, automatic, FWD, 2010-2021
- Lounge, Hatchback, petrol, 1.4L, 100 hp, manual, FWD, 2009-2013
- Lounge, Hatchback, petrol, 1.4L, 100 hp, automatic, FWD, 2009-2013
```

What is wrong:

- The five rows are too coarse for Israeli-market Fiat 500.
- Israeli sources expose marketed trims/versions; `Convertible` must not remain one null-trim row.
- iCar lists multiple Israeli 2009-2020 Fiat 500 versions including 1.2 Pop/Lounge/Pop Star/Cult/Star, 1.4 Pop/Lounge/500S/Gucci, and 0.9 turbo manual Sport/Style/500S rows.
- iCar’s Fiat 500 Cabriolet page lists 500 Cabriolet / 500C versions such as 1.2 robotic Lounge and 1.2 manual Pop. Therefore the convertible row should be split into scalar trim rows or handled as a `Fiat 500 Cabriolet` alias/lineage, not kept as one null trim.
- The Israeli sources describe the automated Fiat 500 gearbox as robotic/single-clutch. If the schema only allows canonical `automatic`, keep the canonical value but add a note that it represents Fiat Dualogic/robotic automatic.

Sources embedded/validated:

```text
https://www.icar.co.il/פיאט/פיאט_500/פיאט_500_יד_שניה_ד10/
https://www.icar.co.il/פיאט/פיאט_500_קבריולה/פיאט_500_קבריולה_יד_שניה_ד10/
https://www.auto.co.il/cars/fiat/500/2015/
https://www.icar.co.il/פיאט/פיאט_500/פיאט_500_יד_שניה_ד10/version7667/
```

Action:

```text
FIX/SPLIT Fiat 500 into scalar trim rows. At minimum:
1. Replace the current single null-trim Convertible row with grounded convertible rows:
   - Pop, Convertible, petrol, 1.2L, 69 hp, manual, FWD, 2010-2020
   - Lounge, Convertible, petrol, 1.2L, 69 hp, automatic/canonical robotic, FWD, 2010-2020
   If a direct source supports 1.4 Cabriolet automatic/robotic, add it; otherwise do not invent it.
2. Keep 1.2 Hatchback Pop manual and Pop automatic/robotic, and 1.2 Lounge automatic/robotic where sourced.
3. Add or preserve scalar 1.2 Pop Star / Cult / Star rows only where year-specific Israeli source metadata supports them.
4. Keep/restore 1.4 100 hp rows, but include Pop / Lounge / 500S / Gucci only where Israeli source metadata supports those trims.
5. Add 0.9 turbo manual rows only if the embedded iCar/Auto/Gear source metadata supports them; do not add global-only TwinAir rows.
6. Do not store any `version_or_trim` arrays. Every trim must be a scalar string.
```

If exact year bounds cannot be reconstructed from the embedded sources, use conservative year ranges from the source generation pages and move uncertain extra trim rows to non-blocking archive/review rather than overfitting them into clean.

---

## 3. Fiat 500L — FIX diesel trim and add missing diesel/manual row

Current clean rows:

```text
- Pop Star, MPV, petrol, 1.4L, 95 hp, 6-speed manual, FWD, 2013-2017
- Lounge, MPV, diesel, 1.3L turbo, 85 hp, 5-speed automatic, FWD, 2013-2017
```

What is wrong:

- Israeli sources list 500L versions as 1.4 petrol manual Pop Star and Lounge, plus 1.3 diesel manual Pop Star and 1.3 diesel robotic Pop Star.
- The current diesel row uses `Lounge`, but iCar/Auto support `Pop Star` for the 1.3 diesel manual/robotic rows.
- The profile is missing the 1.3 diesel manual Pop Star row.
- 0.9 TwinAir 105 hp was discussed as future/possible in launch articles and appears in global/aggregator contexts, but it is not strongly proven as an Israeli clean row in the sources checked here. Do not add 0.9 TwinAir unless a direct Israeli source in the repo supports it.

Sources embedded/validated:

```text
https://www.icar.co.il/פיאט/פיאט_500L/פיאט_500L_יד_שניה_ד10/version13724/
https://www.icar.co.il/פיאט/פיאט_500L/פיאט_500L_יד_שניה_ד10/version11987/
https://www.icar.co.il/פיאט/פיאט_500L/פיאט_500L_יד_שניה_ד10/version11270/
https://www.auto.co.il/cars/fiat/500l/2017/505543/
https://www.auto.co.il/cars/fiat/500l/
```

Action:

```text
FIX Fiat 500L rows to:
- Pop Star, MPV, petrol, 1.4L, 95 hp, 6-speed manual, FWD, 2013-2017
- Lounge, MPV, petrol, 1.4L, 95 hp, 6-speed manual, FWD, 2013-2017
- Pop Star, MPV, diesel, 1.3L turbo, 85 hp, 5-speed manual, FWD, 2013-2017
- Pop Star, MPV, diesel, 1.3L turbo, 85 hp, 5-speed automatic/canonical robotic, FWD, 2013-2017
DELETE/FIX the current `Lounge` diesel row; it should not stay clean as Lounge unless a direct source supports that exact diesel Lounge trim.
Do not add 0.9 TwinAir 105 hp to clean without direct Israeli support.
```

---

## 4. Fiat 600e — FIX Israeli year start if needed; KEEP only grounded electric row

Current clean row:

```text
- La Prima, Crossover, electric, 156 hp, single_speed, FWD, 2023-current
```

Validation facts:

- Embedded catalog sources include Israeli launch pages titled `פיאט 600e החשמלי בישראל - מחיר החל מ-169,990 שקל` and `פיאט 600 החדש בישראל: 156 כ"ס ב-170 אלף שקל`.
- Public Israeli coverage confirms the 600e technical package: electric 156 hp, 54 kWh battery / about 409 km WLTP, FWD.
- 2023 is the global reveal/start, not necessarily the Israeli sales start. The Israeli clean catalog must use Israeli launch/start year.

Sources embedded/validated:

```text
https://www.cartube.co.il/חדשות-רכב/פיאט-600e-החשמלי-בישראל
https://www.icar.co.il/חדשות_רכב/פיאט_600_החדש_בישראל:_156_כס_ב-170_אלף_שקל/
https://www.icar.co.il/מבחני_רכב/פיאט_600_(נהיגה_ראשונה)_–_חוזרת_לימי_הזוהר/
```

Action:

```text
KEEP Fiat 600e La Prima only if source_indexes/field_sources are valid.
FIX year_start from 2023 to the Israeli launch year documented by the embedded Israeli launch source metadata:
- use 2025 if the launch article/date in the repo is 2025;
- use 2024 only if the embedded source metadata proves actual Israeli sale/start in 2024.
Do not leave year_start=2023 unless a direct Israeli source proves 2023 Israeli sales.
Do not add the 1.2 hybrid Fiat 600 row unless a direct Israeli source proves it was marketed in Israel.
```

---

## 5. Fiat Bravo — ADD missing 1.4 90 hp row and fix 150 hp trim if source supports

Current clean rows include:

```text
1996-2001 old Bravo:
- SX, 1.6L 103 hp manual/automatic
- HGT, 2.0L 147 hp manual

2009-2012 new Bravo:
- Dynamic, 1.4L turbo 120 hp manual
- Dynamic, 1.4L turbo 120 hp automatic
- Sensation, 1.4L turbo 120 hp automatic
- null trim, 1.4L turbo 150 hp manual
```

Validation facts:

- Israeli Cartube source confirms the 2009-2012 Bravo lineup had 1.4 90 hp manual, 1.4 T-Jet 120 hp, and 1.4 T-Jet 150 hp.
- A 1.4 90 hp manual row is missing from the clean profile.
- The 150 hp row should not remain null trim if the embedded source supports a marketed trim such as Sport. If no Israeli source exposes the trim, keep null only with a note that the technical row is grounded but trim was not exposed.
- Existing old-generation 1996-2001 SX/HGT rows can be kept if source indexes remain valid.

Sources embedded/validated:

```text
https://www.cartube.co.il/מבחני-רכב/פיאט-מבחני-רכב/פיאט-בראבו-מבחן-דרכים-–-bravo-לפיאט
https://www.cartube.co.il/מבצעי-רכב?start=920
https://www.auto.co.il/model/fiat-bravo_g195
https://www.auto.co.il/model/fiat-bravo_g196
```

Action:

```text
ADD/FIX:
- 2009-2012 Bravo, Hatchback, petrol, 1.4L, 90 hp, manual, FWD; trim scalar if source exposes it, otherwise null with explicit trim-not-exposed note.
KEEP:
- 1.4L turbo 120 hp Dynamic/Sensation rows if field_sources are valid.
FIX:
- 1.4L turbo 150 hp manual row: set version_or_trim to the Israeli trim if embedded sources support it; otherwise keep null but ensure all technical fields are directly supported.
Do not create unsupported 1.6/1.9/2.0 diesel rows from global Bravo data.
```

---

## 6. Fiat Croma — KEEP if source grounding remains valid

Current clean row:

```text
- Dynamic, Estate, petrol, 2.2L, 147 hp, automatic, FWD, 2009-2011
```

Validation facts:

- Embedded iCar/Auto sources support Fiat Croma 2008/2009-2011 in Israel with 2.2 petrol automatic Dynamic.
- No additional Israeli-market Croma technical row was strongly identified in this RUN 2 audit.

Sources embedded:

```text
https://www.icar.co.il/fiat/fiat_croma/
https://www.auto.co.il/model/fiat-croma_g302
```

Action:

```text
KEEP the current Croma row if all field_sources and source_indexes are valid.
Do not add global-only diesel or manual variants.
```

---

## 7. Fiat Doblo — FIX current rows; add missing electric Doblo; remove unsupported 100 hp current diesel if not grounded

Current clean rows:

```text
- null, Van, diesel, 1.5L turbo, 130 hp, 8-speed automatic, FWD, 2023-2024
- null, Van, diesel, 1.5L turbo, 100 hp, 6-speed manual, FWD, 2023-2024
- null, Van, diesel, 1.6L turbo, 105 hp, 6-speed manual, FWD, 2010-2022
- null, Van, diesel, 1.3L turbo, 90 hp, 5-speed manual, FWD, 2010-2022
- null, Van, diesel, 1.9L turbo, 105 hp, 5-speed manual, FWD, 2001-2010
```

What is wrong:

- Fiat Israel’s current official site still lists Doblo as a current Fiat Professional model.
- iCar/Cartube Israeli sources support the new 2023+ Doblo with 1.5 turbo-diesel 130 hp, 8-speed automatic, and an electric version with 136 hp / 50 kWh / about 270 km.
- The clean profile is missing the electric Doblo row.
- The 2023+ 130 hp diesel row should not be closed at 2024 if it is current.
- The 2023+ 100 hp manual diesel row was not supported by the Israeli sources checked here for the new Doblo. Move it to archive/review unless a direct embedded source supports it.

Sources embedded/validated:

```text
https://www.fiat.co.il/
https://www.icar.co.il/פיאט/פיאט_דובלו/פיאט_דובלו_חדש/
https://www.icar.co.il/פיאט/פיאט_דובלו/פיאט_דובלו_יד_שניה_ד12/
https://www.cartube.co.il/חדשות-רכב/פיאט-דובלו-החדש-2023-בישראל-מחיר-172990-שקל
```

Action:

```text
FIX current Doblo rows to include:
- null or source-exposed body/config trim, Van/MPV per existing convention, diesel, 1.5L turbo, 130 hp, 8-speed automatic, FWD, 2023-current
- null or source-exposed body/config trim, Van/MPV per existing convention, electric, electric, engine_displacement_l=null, 136 hp, single_speed, FWD, 2023-current
MOVE TO REVIEW/ARCHIVE:
- 2023+ 1.5L turbo 100 hp 6-speed manual row unless the embedded Israeli source directly supports it.
KEEP historic 1.9/1.3/1.6 diesel rows if field_sources remain valid.
```

---

## 8. Fiat Ducato — FIX current/open-ended status for 2.2L current rows

Current clean rows:

```text
- 2.2L turbo diesel 140 hp, 6-speed manual, 2022-2024
- 2.2L turbo diesel 140 hp, 9-speed automatic, 2022-2024
- 2.2L turbo diesel 180 hp, 9-speed automatic, 2022-2024
- 2.3L turbo diesel 140 hp, 9-speed automatic, 2020-2021
- 2.3L turbo diesel 130 hp, 6-speed manual, 2014-2019
```

Validation facts:

- Fiat Israel’s current official site lists Ducato as a current 2026 Fiat Professional model.
- iCar current Ducato page supports 2.2L turbo-diesel 140 or 180 hp, 6-speed manual or 9-speed automatic.
- Therefore the 2.2L 2022+ rows should be open/current, not closed at 2024.

Sources embedded/validated:

```text
https://www.fiat.co.il/
https://www.icar.co.il/פיאט/פיאט_דוקאטו/פיאט_דוקאטו_חדש/
https://www.cartube.co.il/חדשות-רכב/פיאט-דוקאטו-החדש-2022-בישראל-מחיר-החל-מ-255,000-שקלים
```

Action:

```text
FIX year_end=null/current for the 2022+ 2.2L rows:
- 140 hp manual
- 140 hp 9-speed automatic
- 180 hp 9-speed automatic
KEEP historic 2.3L rows with closed years if valid.
Do not explode Ducato into every length/height/wheelbase body configuration unless the catalog convention requires body-configuration trims; the technical powertrain rows are sufficient for this technical catalog if grounded.
```

---

## 9. Fiat Fiorino — KEEP historical rows; do not reopen as current

Current clean rows:

```text
- 1.4L petrol 73 hp manual, 2008-2018
- 1.3L diesel 75 hp manual, 2008-2016
- 1.3L diesel 75 hp automatic/canonical robotic, 2008-2016
- 1.3L diesel 80 hp manual, 2016-2022
- 1.3L diesel 80 hp automatic/canonical robotic, 2016-2022
```

Validation facts:

- Embedded iCar/Auto/Gear sources support Fiorino historical Israeli rows.
- Current Fiat Israel official site lists Doblo/Scudo/Ducato, not Fiorino, so do not set Fiorino current/open-ended.

Sources embedded:

```text
https://www.icar.co.il/פיאט/פיאט_פיורינו/
https://www.auto.co.il/model/fiat-fiorino_g248
https://gear.co.il/דגמי_רכב/פיאט-פיורינו
```

Action:

```text
KEEP the current Fiorino rows if source_indexes/field_sources remain valid.
Do not extend year_end beyond 2022 unless an Israeli source in the repo proves later marketing.
```

---

## 10. Fiat Freemont — MERGE duplicate global/IL profiles; keep only one Israeli clean profile

Current clean profiles are duplicated:

```text
global-reference-only|Fiat|Freemont:
- null, SUV, petrol, 2.4L, 170 hp, 6-speed automatic, FWD, 2012-2016

IL-confirmed|Fiat|Freemont:
- null, SUV, petrol, 2.4L, 170 hp, 6-speed automatic, FWD, 2012-2016
```

What is wrong:

- The same technical variant is published twice under two source-scope keys.
- Israeli launch/catalog sources support Fiat Freemont in Israel; the clean website catalog should keep one canonical Israeli profile, not both `global-reference-only` and `IL-confirmed` as separate clean models.
- Body type is questionable as `SUV`: Israeli coverage often presents Freemont as a 7-seat MPV/minivan/crossover based on Dodge Journey. Use the project’s canonical convention, but do not blindly keep SUV if sources classify it as MPV.
- Israeli launch appears to be around 2014. Do not use a global 2012 start unless the Israeli source directly supports 2012 Israeli availability.

Sources embedded/validated:

```text
https://www.cartube.co.il/חדשות-רכב/פיאט-פרימונט-בישראל-–-מחיר-החל-מ-169,990-שקל
https://www.icar.co.il/פיאט/פיאט_פרימונט/
https://www.auto.co.il/articles/car-news/113359/
https://www.auto.co.il/model/fiat-freemont_g302
```

Action:

```text
MERGE/DEDUPE:
- Keep one canonical clean profile: preferably `IL-confirmed|Fiat|Freemont` or canonical market key `IL|Fiat|Freemont` according to existing project conventions.
- Add alias/lineage from `global-reference-only|Fiat|Freemont` to the canonical Israeli profile.
- Remove/archive the duplicate global-reference-only clean profile so it does not count as a separate website model.
FIX body_type:
- Use MPV if the project normalizes 7-seat minivan/crossover to MPV; otherwise use the project’s accepted crossover/SUV value, but be consistent and note the source classification.
FIX year_start:
- Use the Israeli launch/start year from embedded Cartube/iCar source metadata. If the Israeli launch source is 2014, set year_start=2014; do not keep 2012 if that is global-only.
```

---

## 11. Fiat Linea — FIX casing and do not keep weak/global-only multi-row profile

Current clean profile key/casing:

```text
IL|Fiat|linea
```

Current rows:

```text
- Dynamic, Sedan, petrol, 1.4L, 77 hp, manual, 2008-2011
- Dynamic, Sedan, petrol, 1.4L, 77 hp, automatic, 2008-2011
- Dynamic, Sedan, petrol, 1.4L turbo, 120 hp, manual, 2008-2011
- Dynamic, Sedan, diesel, 1.3L turbo, 90 hp, manual, 2008-2011
- Dynamic, Sedan, diesel, 1.3L turbo, 90 hp, automatic, 2008-2011
```

What is wrong:

- Casing is wrong: model should be `Linea`, not `linea`.
- There is conflicting Israeli evidence. iCar/Auto news around 2008-2010 says Linea was expected/considered but ultimately likely did not officially arrive; Auto explicitly reports it probably would not come to Israel.
- Yad2 has a weak marketplace/price-list row for a 2008 Fiat Linea Dynamic automatic 90 hp diesel, but marketplace-only evidence is not enough to keep a five-row clean profile.
- The current five technical rows look like a global/forecast set, not a strongly verified Israeli clean profile.

Sources embedded/validated:

```text
https://www.icar.co.il/חדשות_רכב/פיאט-אלפא_פותחים_את_2010/
https://www.auto.co.il/articles/local-news/121128/
https://www.yad2.co.il/price-list/feed?manufacturer=45&model=10638
https://www.auto.co.il/model/fiat-linea_g239
```

Action:

```text
FIX casing if any Linea profile remains:
- model=`Linea`
- add alias from old `IL|Fiat|linea` to `IL|Fiat|Linea`

QUALITY DECISION:
- Do not keep the current five-row Linea profile as verified clean unless embedded Israeli catalog sources directly support each row.
- If only Yad2/marketplace supports a single 2008 Dynamic 90 hp diesel row, move the Linea profile to non-blocking archive/review instead of clean.
- If a direct iCar/Auto catalog source in the repo truly supports Israeli-market Linea rows, reduce clean to only those exact supported rows and delete/archive the unsupported forecast/global rows.

Preferred safe outcome if direct support is weak:
MOVE TO NON-BLOCKING ARCHIVE with reason `weak/marketplace-only or contradicted Israeli launch evidence`; do not leave as active blocker.
```

---

## 12. Fiat Marea — KEEP, but fix diesel trim label if needed

Current clean rows:

```text
- ELX, Sedan, petrol, 1.6L, 103 hp, automatic/manual, 1996-2002
- ELX, Estate, petrol, 1.6L, 103 hp, automatic/manual, 1996-2002
- null, Sedan, diesel, 1.9L turbo, 105 hp, manual, 1999-2002
```

Validation facts:

- Embedded Auto/iCar/KML sources support Marea/Marea Weekend and the 1.9 diesel JTD sedan row.
- The diesel row’s `version_or_trim=null` may be acceptable if the source only exposes engine designation and not a marketed trim. If the source exposes `JTD` as the marketed designation/trim, use scalar `JTD`; otherwise keep null with note.

Sources embedded:

```text
https://www.auto.co.il/model/fiat-marea_g261
https://www.icar.co.il/פיאט/פיאט_מריאה_וויקאנד/פיאט_מריאה_וויקאנד_יד_שניה_ד1/
https://kml.co.il/car/פיאט_מריאה_1-9_דיזל_JTD_ידני_2002-1999
```

Action:

```text
KEEP current Marea rows if source references are valid.
FIX diesel version_or_trim to `JTD` only if the embedded source treats JTD as a marketed variant label; otherwise keep null and record `trim not exposed by Israeli source`.
```

---

## 13. Fiat Panda — KEEP but ensure robotic gearbox is canonicalized with note

Current clean rows:

```text
- Dynamic, 1.2L petrol 60 hp manual/automatic, 2004-2010
- null, 1.2L petrol 69 hp manual, 2011-2020
- Dynamic, 1.2L petrol 69 hp automatic, 2011-2012
- null, 0.9L turbo petrol 85 hp manual/automatic, 2012-2016
```

Validation facts:

- Embedded Auto/iCar sources support Panda historical rows across 2004-2012 and 2012-2020.
- Fiat Israel current official site no longer lists Panda as a current model, so year_end=2020 is acceptable if source-supported.
- Fiat robotic/Dualogic rows may be normalized as `automatic` by schema; do not mark this as a bug if the underlying note/source indicates robotic automatic.

Sources embedded:

```text
https://www.auto.co.il/model/fiat-panda_g127
https://www.auto.co.il/model/fiat-panda_g128
https://www.icar.co.il/fiat/fiat_panda
```

Action:

```text
KEEP Panda rows if field grounding remains valid.
Do not reopen Panda as current.
Do not add global-only 4x4/Cross/Natural Power rows unless direct Israeli source exists.
If schema uses canonical automatic, preserve a note for Dualogic/robotic automatic rows.
```

---

## 14. Fiat Punto — FIX trim/designation quality, especially Punto Evo/Grande rows

Current clean profile has 11 broad technical rows, many with `version_or_trim=null`, including:

```text
1993-2006 1.2L 60/80 hp manual/CVT rows
1993-2000 1.4L turbo 133 hp manual row
2006-2010 1.2L 65 hp manual row
2006-2018 1.4L 77 hp manual/automatic rows
2010-2012 1.4L 105 hp manual row
2010-2012 1.4L turbo 135 hp manual row
2012-2018 1.2L 69 hp manual row
```

What is wrong / risk:

- Israeli iCar/Auto sources expose trim names for later Punto generations: Active, Dynamic, Lounge, Milano, Multiair, and possibly Grande Punto / Punto Evo generation distinctions.
- The 2010 Punto Evo Israeli source explicitly lists 1.4 77 hp, 105 hp, and 135 hp versions. Therefore the 2010-2012 rows should not remain all null if trims/designations are present.
- The 2006+ Grande Punto 1.4 77 hp robotic row is documented by iCar; the schema may normalize robotic to automatic, but the note should preserve that it is robotic/single-clutch.
- The 1.4 turbo 133 hp 1993-2000 row likely represents a Punto GT-style performance row. Do not leave it as a null trim if the source exposes GT; otherwise move it to review/archive if the Israeli source is weak.

Sources embedded/validated:

```text
https://www.auto.co.il/model/fiat-punto_g281
https://www.auto.co.il/model/fiat-grande-punto_g158
https://www.auto.co.il/model/fiat-punto-evo_g802
https://www.auto.co.il/model/fiat-punto_g280
https://www.auto.co.il/model/fiat-punto_g279
https://www.icar.co.il/חדשות_רכב/פיאט-אלפא_פותחים_את_2010/
https://www.icar.co.il/מבחני_רכב/פיאט_גרנדה_פונטו_-_מבחן_רכב/
https://www.icar.co.il/פיאט/פיאט_פונטו_איבו/פיאט_פונטו_איבו_יד_שניה_ד10/version149/
```

Action:

```text
FIX Punto rows to use scalar trim/designation labels where Israeli sources expose them:
- Grande Punto 1.4 77 hp robotic/canonical automatic should include Active/Dynamic if supported by the source version list; do not leave null if source exposes trim.
- Punto Evo 2010-2012 rows should carry source-exposed designations such as Active/Dynamic/Lounge/Milano/Multiair where supported.
- 1.4 turbo 135 hp 2010-2012 should be tied to Multiair/Dynamic if the embedded iCar/Auto source supports that designation.
- 1.4 turbo 133 hp 1993-2000 should become `GT` only if supported by Israeli source metadata; otherwise move to non-blocking archive/review rather than a null clean performance row.
KEEP older 1.2 60/80 hp Punto rows if source references are valid and no trim source is exposed.
Do not add unsupported global Punto diesel/convertible rows.
```

---

# RUN 2 rebuild / validation requirements

After applying RUN 2 only:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
```

Return:

```text
RUN 2 RESULT: PASS / PASS WITH WARNINGS / FAIL
files changed
models touched
variants added/fixed/moved/archived
alias/lineage changes
readiness metrics
quality scan bug/leak/structure/normalization counts
unmatched output keys count/sample
tests run
commit hash if committed
remaining risks before RUN 3
```

Do not continue to RUN 3 or RUN 4 from this file.

---

# BATCH 23 — RUN 3 CODEX TASK

Scope: RUN 3 only from the Batch 23 last-88 mapping.

Do **not** browse the internet. All relevant validation facts collected outside Codex are embedded here.

Execute RUN 3 only. Do not continue to RUN 4 or final blockers/unmatched unless a change is directly required to keep RUN 3 outputs consistent.

## Current Batch 23 context

Previous confirmed cursor baseline after Batch 22:

```text
resume_after_key = IL|Dodge|Nitro
next_key_to_process = IL|Dodge|Ram
```

Batch 23 mapped source window:

```text
start = IL|Dodge|Ram
end = IL|Honda|CR-Z
next = IL|Honda|e:Ny1
mapped source groups = 88
clean source groups in window = 59
review/blocker groups in window = 29
unmatched_output_keys_count = 0
```

RUN 1 covered:

```text
Dodge Ram -> Ferrari Roma
```

RUN 2 covered:

```text
Ferrari SF90 Stradale -> Fiat Punto
```

RUN 3 covers these 15 clean profiles:

```text
IL|Fiat|Qubo
IL|Fiat|Tipo
IL|Fiat|Topolino
IL|Fiat|Uno
IL|Ford|Bronco
IL|Ford|Explorer
IL|Ford|F-150
IL|Ford|Focus
IL|Ford|Galaxy
IL|Ford|Kuga
IL|Ford|Maverick
IL|Ford|Mondeo
IL|Ford|Mustang Mach-E
IL|Ford|Puma
IL|Ford|Ranger
```

## Global RUN 3 rules

1. Do not aim only for green readiness. Fix data quality where the current clean row is weak, incomplete, mis-scoped, or clearly contradicted by Israeli-market sources.
2. If a row is only supported by global/non-Israeli facts and no strong Israeli evidence exists in the repository, move it to non-blocking archive/review rather than keeping it as verified clean.
3. Do not invent trims. Add trim names only when Israeli sources or the embedded/source evidence clearly support them.
4. If a model is active/current in Israel, use `year_end = null`, not a stale closed year.
5. If a model is not currently sold and the latest reliable Israeli source only supports past sale years, do not keep it open/current.
6. EVs may have `engine_displacement_l = null`.
7. `version_or_trim` must be scalar string/null, never an array.
8. After fixes, rebuild outputs and run validation/quality/tests.

---

# RUN 3 corrections

## 1. Fiat Qubo

### Current catalog problem

Current clean profile has 6 variants but leaves `version_or_trim = null` for all rows:

```text
2009-2016 petrol 1.4 73 hp manual
2009-2016 diesel 1.3 turbo 75 hp manual
2009-2016 diesel 1.3 turbo 75 hp automated/automatic
2016-2019 petrol 1.4 77 hp manual
2016-2019 diesel 1.3 turbo 80 hp manual
2016-2019 diesel 1.3 turbo 80 hp automated/automatic
```

### Validation facts

Israeli sources support Qubo as a passenger/family version of Fiorino. iCar launch coverage confirms the early 1.4L petrol with 73 hp. Later Israeli listing/spec pages show 2016 `Active`/`Dynamic` trim naming and 1.3 diesel manual/robotic plus 1.4 petrol rows.

Useful source facts embedded:

- iCar launch article: Qubo launched in Israel with 1.4L petrol, 73 hp, manual.
- iCar 2016 spec page: versions include `1.3 diesel manual Active`, `1.3 diesel robotic Active`, `1.4 petrol manual Active`, `1.4 petrol manual Dynamic`, `1.3 diesel robotic Dynamic`.
- Yad2/Carzone 2016 listings/spec support 80 hp diesel and 77 hp petrol in later years.

### Required action

**FIX / SPLIT TRIM LABELS**

Do not keep all Qubo variants with `version_or_trim = null` if the local evidence supports trim names.

Target:

```text
Early 2009-2015/2016 rows:
- keep only if supported by existing sources; trim may remain null or Active if the source supports Active.

Later 2016-2019 rows:
- petrol 1.4 77 hp manual -> Active and/or Dynamic if both are grounded.
- diesel 1.3 80 hp manual -> Active if grounded.
- diesel 1.3 80 hp robotic/automatic -> Active and/or Dynamic if grounded.
```

If the project canonical enum does not support `robotic`, use the current canonical automatic/dual-clutch normalization, but add a note/source support explaining it was marketed as robotic/automated.

Do not add ungrounded trim rows. If exact trim split is not fully source-supported, keep a conservative single technical row and document the trim uncertainty in notes.

---

## 2. Fiat Tipo

### Current catalog state

Current profile mixes:

```text
1990-1995 legacy Tipo hatchback 1.4 71 hp / 1.6 83 hp
2016-2020 Tipo sedan/hatch/estate 1.4 95, 1.6 110, 1.4T 120, 1.6 diesel 120
2021-2023 Tipo Cross 1.0 turbo 100
```

### Validation facts

Auto Israel states Tipo arrived in Israel in March 2016 first as sedan with 1.4/1.6 petrol, then April 2017 added hatchback and wagon/estate, including 1.4 turbo and 1.6 diesel dual-clutch variants. This supports the modern split by body/powertrain. The 1990s legacy Tipo exists separately but is old and may rely on weaker price-list evidence.

### Required action

**KEEP WITH TARGETED CLEANUP**

- Keep modern 2016+ technical splits if sources are valid.
- Ensure `year_start` for modern Israeli Tipo is 2016 for sedan and 2017 for hatchback/estate where the sources support that difference.
- Keep `Tipo Cross` only for the 2021-2023 1.0 turbo 100 hp row if Israeli evidence supports it.
- Do not force trim names where only body/powertrain are grounded.
- If the 1990-1995 legacy rows rely only on weak/global evidence and lack Israeli source support inside the repository, move them to non-blocking archive rather than keeping them as verified clean.

---

## 3. Fiat Topolino

### Current catalog problem

Current clean profile contains:

```text
Fiat Topolino
- null trim, electric, 8 hp, Coupe, 2023-current, support_level=indirect
- Dolcevita, electric, 8 hp, Convertible, 2023-current, support_level=indirect
```

### Validation facts

Israeli coverage describes the new Topolino as a European quadricycle/L-category vehicle and notes the category is not used/marketed the same way in Israel. No strong Israeli-market sales/import source was found validating Topolino as a clean Israeli passenger-car model. iCar/Auto coverage supports the technical facts globally: 8 hp, 45 km/h, 5.5 kWh, about 70 km range, but this is not enough for verified Israeli clean.

### Required action

**MOVE TO REVIEW/ARCHIVE NON-BLOCKING** unless the repository already contains a strong Israeli import/sales source for Fiat Topolino.

Preferred:

```text
Action = MOVE TO ARCHIVE
reason = global/reference-only quadricycle coverage; no strong Israeli-market clean support
non_blocking = true
preserve facts = 8 hp electric, Topolino/Dolcevita, 2023 global launch/reference
```

Do not keep Topolino as a verified clean Israeli model based only on global or local-news global coverage.

If a strong Israeli official/importer source exists inside the repo that I missed, keep it but change `support_level` to direct only where every non-empty field is directly supported.

---

## 4. Fiat Uno

### Current catalog state

Current clean profile has:

```text
45S 1.0 45 hp manual 1990-1995
60S 1.1 57 hp manual 1990-1995
70S 1.4 71 hp manual 1990-1995
Selecta 1.4 71 hp CVT 1990-1995
Turbo i.e. 1.4 turbo 118 hp manual 1990-1993
```

### Validation facts

Israeli/legacy sources support the Uno naming family: 45S, 60S, 70S, Selecta, Turbo i.e. A local nostalgic article supports 60S = 1.1L 57 hp, 70 = roughly 71/72 hp, and Turbo i.e. = 1.4L 118 hp. Yad2 price-list evidence shows at least a 1996 1.4 `S` 71 hp row, suggesting the model year range may extend to 1996 for at least the 1.4 S/70-type row.

### Required action

**KEEP / SMALL FIX**

- Keep 45S/60S/70S/Selecta/Turbo i.e. if source references are valid.
- Normalize 70S horsepower to the project convention already used for Israeli price lists: 71 hp or 72 hp, but do not duplicate both.
- Check if model/variant `year_end` should be 1996 for the 1.4 S/70S family based on source evidence. If only weak Yad2 evidence supports 1996, either extend only the relevant 1.4 row or document as weak/archive; do not extend all rows blindly.
- Do not add South America/new Uno rows.

---

## 5. Ford Bronco

### Current catalog problem

Current clean profile is closed at 2024 and has generic/null trims:

```text
2.3 turbo 300 hp 4WD 2021-2024
2.7 V6 turbo 330 hp 4WD 2021-2024
3.0 V6 turbo 418 hp Raptor 2022-2024
```

### Validation facts

Ford Israel currently lists Ford Bronco and Bronco Raptor. Israeli Auto/Yad2/official pages show current/2026 Israeli availability and price ranges, including Big Bend 2.3L, Outer Banks 2.3L, Badlands/Wildtrak 2.7L, and Raptor 3.0L. Ford Israel Bronco Raptor page confirms Bronco Raptor current pricing; Yad2/Auto show 3.0 418 hp rows and 2.3/2.7 rows.

### Required action

**FIX CURRENT STATUS + TRIM SPLIT**

- Do not keep Ford Bronco closed at 2024.
- Set current Israeli rows to `year_end = null` where currently sold.
- Replace/null-trim generic rows with trim-specific rows only where supported:
  - Big Bend / Outer Banks / Badlands etc. for 2.3L turbo rows if grounded.
  - Badlands / Wildtrak / Luxury or similar 2.7L rows only if Israeli sources support exact trim names.
  - Raptor 3.0L V6 turbo 418 hp as a direct current row.
- If older 2.3L rows use 270/275 hp while current rows use 300 hp, split by year/source; do not merge conflicting hp values into one row.
- Keep `Bronco Raptor` as trim/line under Ford Bronco unless the catalog convention requires a split model. If split, add alias/lineage so it does not become unmatched.

---

## 6. Ford Explorer

### Current catalog problem

Current clean profile closes at 2024:

```text
Limited 2.3L 300 hp RWD 2020-2024
Limited 2.3L 300 hp AWD 2020-2024
ST 3.0L 400 hp AWD 2020-2024
Platinum 3.0L 365 hp AWD 2021-2024
```

### Validation facts

Ford Israel currently lists Explorer. The Ford Israel page exposes current Explorer trims/prices and indicates 2.3L EcoBoost 300 hp for Platinum/RWD-like rows and a 400 hp EcoBoost row for AWD/performance configuration. This supports not closing the profile at 2024 if the model is still marketed.

### Required action

**FIX CURRENT STATUS + VERIFY TRIMS**

- Do not close current Explorer rows at 2024 if Ford Israel current page/source exists in repository.
- Set current supported rows to `year_end = null`.
- Verify the 365 hp `Platinum` row. If it is historical only, close it to the supported years; if current Israeli sources no longer support 365 hp, do not keep it open.
- Keep 2.3L 300 hp and 3.0L 400 hp rows if direct source support exists.
- Use exact Ford Israel trim names if present; otherwise retain conservative Limited/ST/Platinum names only where sourced.

---

## 7. Ford F-150

### Current catalog problem

Current profile ends at 2024 and may be missing/incorrectly representing current 2025/2026 rows and Lightning rows:

```text
Raptor 3.5 V6 turbo 450 hp 2017-2024
Hybrid 3.5 V6 turbo 430 hp 2021-2024, trim null
Lariat 3.5 V6 turbo 400 hp 2021-2024
Legacy 3.7 V6 302 hp 2013-2014
```

### Validation facts

Israeli Yad2/Carzone price-list evidence shows 2023-2026 F-150 rows including Lariat 3.5 430 hp, Tech 450 hp, Raptor 450 hp, Raptor R 700 hp, and Lightning electric XLT/Lariat/Platinum rows. This indicates the current clean profile should not be closed at 2024 if the repository has strong enough source support. However, price-list-only evidence may be weaker than official importer evidence, and F-150/Lightning may be parallel/importer-specific.

### Required action

**FIX / REVIEW SCOPE CAREFULLY**

- Do not blindly add every Yad2 price-list row to clean.
- If existing repository sources include strong Israeli support for current F-150 rows, extend supported current rows to `year_end = null`.
- Fix Lariat 430 hp: if the row is PowerBoost hybrid, keep `fuel_type=hybrid`; if the Israeli source lists it as petrol only, document the conflict and do not downgrade fuel type unless supported by strong source.
- Add/keep `Tech` 450 hp only if source support is strong enough.
- Handle F-150 Lightning as either:
  - separate model `Ford F-150 Lightning` with alias/lineage from `F-150`, or
  - electric variants under `Ford F-150`,
  according to project convention. Do not leave Lightning rows unmatched or mixed without lineage.
- Raptor R 700 hp should not enter clean unless a strong Israeli source supports it as an Israeli-market variant; otherwise archive/review non-blocking.

---

## 8. Ford Focus

### Current catalog state

Current profile contains 14 variants including:

```text
2005-2011 1.6 100 hp hatch/sedan/estate
2011-2015 1.6 125 hp hatch/sedan/estate
2015-2018 1.5T 150 hp hatch/sedan/estate
2018-2021 1.5T 150 hp hatch/sedan/estate, 8-speed auto
2021-2025 1.0 mild-hybrid 155 hp hatch/estate, 7-speed dual-clutch
```

### Validation facts

iCar and Auto Israel support current/new Focus with 1.0 turbo mild-hybrid 155 hp and 7-speed dual-clutch. Gear/iCar support 2025 Tourer/Active/Titanium context. The current technical values appear plausible, but the profile lacks trim/body trim context.

### Required action

**KEEP / ADD TRIM CONTEXT WHERE GROUNDED**

- Keep the current 1.0 mild-hybrid 155 hp hatchback and estate/tourer rows.
- If sources support `Titanium`, `ST-Line`, `Active`, `Active X Tourer`, or `Titanium Tourer`, add trim/context to `version_or_trim`; otherwise keep trim null with notes rather than guessing.
- Do not close current 2025-supported rows to 2024.
- Check whether `year_end=2025` should remain closed or become `null/current`. If Ford Israel still markets Focus/Focus Tourer at the current source snapshot, set `year_end=null`; if 2025 is only a price-list/model-year record and not current importer availability, keep 2025.

---

## 9. Ford Galaxy

### Current catalog state

```text
Trend/Ghia/Titanium 2.3 petrol 161 hp 2007-2010
Trend/Titanium 2.0 turbo petrol 203 hp 2011-2015
Trend 2.0 diesel 140 hp 2007-2010
```

### Validation facts

iCar/Auto/Yad2 Israeli evidence supports Galaxy 2.3 petrol Ghia/Titanium around 2011, 2.0 turbo petrol Trend/Titanium around 2011-2015, and diesel variants around 140/163 hp depending year/trim. Current catalog may under-cover trim/body years but the broad technical rows are plausible.

### Required action

**KEEP WITH YEAR/TRIM REVIEW**

- Verify 2.3 petrol row should possibly extend to 2011, not stop at 2010, if Israeli source supports 2011 Ghia/Titanium.
- Verify diesel 140 hp year span and whether a 163 hp diesel row exists in Israeli price/spec sources. If 163 hp is only listing noise, do not add.
- Keep `Trend / Ghia / Titanium` joined only if it truly represents one shared technical row. If trims differ by engine/year, split rows.
- Do not mark current/open-ended; Galaxy is historical in Israel.

---

## 10. Ford Kuga

### Current catalog state

Current profile closes at 2024 and includes:

```text
2008-2013 2.5T 200 hp AWD
2013-2015 1.6T 180 hp AWD/FWD
2015-2019 1.5T 182 hp AWD + 1.5T 150 hp FWD
2020-2024 1.5T 150 hp FWD
2021-2024 PHEV 2.5 225 hp FWD
```

### Validation facts

Auto Israel supports Kuga technical values. Cartube notes the 2024 European facelift was not imported to Israel, so do not assume a new 2024+ facelift/current row without Israeli importer evidence.

### Required action

**KEEP / DO NOT OVER-EXTEND**

- Keep `year_end=2024` unless repository sources prove current Israeli sale after 2024.
- Do not add facelift rows from global/European sources.
- Add trim names such as Trend/Titanium/Titanium X only if source-supported by the existing Israeli source indexes.
- Validate PHEV row 225 hp and keep only if direct support exists.

---

## 11. Ford Maverick

### Current catalog problem

Current clean profile has:

```text
Lariat 2.0 turbo 250 hp AWD 2022-current
Lariat hybrid 2.5 191 hp FWD 2022-current
```

### Validation facts

Only weak/price-list Israeli evidence was found for Ford Maverick. No strong official Ford Israel or importer source was found in the external validation pass. Maverick may be parallel/grey import rather than a verified Israeli-market official model.

### Required action

**MOVE TO REVIEW/ARCHIVE NON-BLOCKING unless strong Israeli source exists in repo**

- If the only support is Yad2/marketplace/price-list style evidence, do not keep Maverick as verified clean.
- Preserve as non-blocking archive with technical facts if needed:
  - Lariat 2.0 turbo 250 hp AWD
  - Lariat Hybrid 2.5 191 hp FWD
- If strong Israeli source evidence exists in repository, keep clean but add notes/field_sources explaining official/local support.

---

## 12. Ford Mondeo

### Current catalog problem

Current profile has many technically plausible rows but almost all `version_or_trim = null` even where Israeli sources expose Trend/Titanium/Trend-X names.

### Validation facts

iCar/Auto Israeli sources support Mondeo engine families and trims: 2.3 petrol Trend/Titanium, 2.0 diesel Trend-X, 2.0 turbo petrol 203 hp Trend, 2.0 turbo petrol 240 hp Titanium, and later 1.5 turbo 160 hp rows. Auto Israel also supports the 2015 generation with 1.5 160 and 2.0 203/240.

### Required action

**FIX TRIM CONTEXT / KEEP TECHNICAL ROWS**

- Keep broad year/powertrain/body split if source references are valid.
- Add `Trend`, `Titanium`, `Trend-X` to `version_or_trim` where the source directly supports those trim/body/powertrain combinations.
- For 2.0 turbo 203 hp rows, use `Trend` where supported.
- For 2.0 turbo 240 hp rows, use `Titanium` where supported.
- For 2.0 diesel rows, use `Trend-X` where supported.
- Do not add unsupported estate/hatch rows if only sedan/5-door source exists. Split by body only where supported.

---

## 13. Ford Mustang Mach-E

### Current catalog problem

Current clean profile is 2024-only:

```text
Select 269 hp RWD
Premium 294 hp RWD
Premium 351 hp AWD
GT 487 hp AWD
```

### Validation facts

Israeli Yad2/Carzone price-list evidence shows Mustang Mach-E 2024 rows with multiple naming conventions: Select/Techno/Mach/Premium, RWD/AWD, outputs around 269/294/301/351/371/480/487 depending source/market unit conventions. This indicates source conflict and possible importer/parallel naming mismatch.

### Required action

**VERIFY / DO NOT MASK SOURCE CONFLICT**

- Keep current clean rows only if the repository has direct source support for exact horsepower and trim names.
- Do not silently change 487 to 480 or 351 to 371 based only on weaker price-list evidence; instead split or move conflicting rows to archive/review if source conflict cannot be resolved.
- If strong Israeli source supports `Techno`, `Select`, `Premium`, `GT`, `Mach` naming, normalize trims accordingly.
- If Mustang Mach-E is current in Ford Israel/official source beyond 2024, set `year_end=null`; otherwise keep 2024.
- Ensure EV null displacement remains valid and not missing-grounding.

---

## 14. Ford Puma

### Current catalog problem

Current profile closes at 2024 and has one null trim plus ST rows:

```text
1.0 mild-hybrid 125 hp DCT 2021-2024 trim null
ST 1.5T 200 hp manual 2021-2024
ST Powershift 1.0 mild-hybrid 170 hp DCT 2023-2024
```

### Validation facts

Auto/iCar Israeli sources support the 1.0 125 hp Puma with 7-speed dual-clutch, and 2024 trim names like Titanium/ST-Line/ST-Line X. Gear notes the 2024 facelift/global update replacing the 1.5 ST manual with ST Powershift 170 hp; verify local support before extending.

### Required action

**FIX TRIMS / CURRENT STATUS CAREFULLY**

- Replace null trim for 1.0 125 hp row with supported trims if source-grounded: `Titanium`, `ST-Line`, `ST-Line X`.
- If multiple trims share the same technical variant, joining as `Titanium / ST-Line / ST-Line X` is allowed only if project convention permits and all trims share exact technical values; otherwise split rows.
- Verify ST 1.5 200 hp end year. If it was discontinued/replaced by ST Powershift, close it to supported years.
- Keep ST Powershift 170 hp only if Israeli sources support local sale; otherwise review/archive.
- Do not set Puma current/open-ended unless Ford Israel/current source supports it.

---

## 15. Ford Ranger

### Current catalog state

Current profile includes:

```text
Raptor 3.0 V6 turbo 292 hp 2023-current
Tremor 2.0 bi-turbo diesel 205 hp 2023-current
XLT 2.0 turbo diesel 170 hp 2023-current
Legacy 2.5 turbo diesel 110 hp manual 1998-2006 trim null
```

### Validation facts

Ford Israel commercial price list, iCar, Auto and Cartube support current Ranger XLT 2.0 diesel 170 hp, Tremor 2.0 diesel 205 hp, and Raptor 3.0 petrol 292 hp, with current pricing. The current rows are well-supported. Legacy 2.5 diesel 110 hp is plausible but should only remain clean if source references are direct.

### Required action

**KEEP / SOURCE-CLEAN LEGACY ROW**

- Keep current XLT/Tremor/Raptor rows as direct/current with `year_end=null`.
- Ensure official Ford Israel/commercial price list source indexes support current rows.
- For the legacy 2.5 diesel 110 hp row: keep only if direct Israeli source support exists; otherwise move to archive non-blocking or add source/field grounding from existing evidence.
- Do not add global Ranger Raptor output variants not sold/grounded in Israel.

---

# Required rebuild and tests

After applying RUN 3 corrections:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
```

Also compute/inspect final interim metrics after RUN 3:

```text
models_blocked
review_only_blocked_entries
duplicate_technical_variants
invalid_source_references
unknown_support_values
ready_for_website_upload
unmatched_output_keys_count
unmatched_output_keys_sample
active_blocked_count
quality_scan bug/leak/structure/normalization counts
```

For RUN 3 only, it is acceptable that final blockers from the FINAL RUN remain unresolved until the blockers/unmatched phase. Do not claim final Batch 23 readiness unless all final blockers are actually resolved.

# Codex return format

Return:

```text
RUN 3 RESULT: PASS / PASS WITH WARNINGS / FAIL

1. Files changed
2. Models touched
3. Variants added/fixed/moved/archived
4. Alias/lineage changes
5. Readiness metrics after RUN 3
6. Quality scan counts
7. Unmatched output keys count/sample
8. Tests run
9. Commit hash if committed
10. Remaining risks before RUN 4
```


---

# BATCH 23 — RUN 4 CODEX TASK

Scope: RUN 4 only from the Batch 23 last-88 mapping.

Do **not** browse the internet. All relevant validation facts collected outside Codex are embedded here.

Execute RUN 4 only. Do not continue to the final blockers/unmatched run unless a change is directly required to keep RUN 4 outputs consistent.

## Current Batch 23 context

Previous confirmed cursor baseline after Batch 22:

```text
resume_after_key = IL|Dodge|Nitro
next_key_to_process = IL|Dodge|Ram
```

Batch 23 mapped source window:

```text
start = IL|Dodge|Ram
end = IL|Honda|CR-Z
next = IL|Honda|e:Ny1
mapped source groups = 88
clean source groups in window = 59
review/blocker groups in window = 29
unmatched_output_keys_count = 0
```

RUN 1 covered:

```text
Dodge Ram -> Ferrari Roma
```

RUN 2 covered:

```text
Ferrari SF90 Stradale -> Fiat Punto
```

RUN 3 covered:

```text
Fiat Qubo -> Ford Ranger
```

RUN 4 covers these 14 clean profiles:

```text
IL|Ford|S-MAX
IL|Ford|Tourneo Connect
IL|Ford|Transit
IL|Ford|Transit Custom
global-reference-only|GAC|Aion V
IL|GAC / Aion|Aion V
IL-confirmed|GAC / Aion|Aion Y
IL|GAC / Aion|Aion Y
IL|Geely|Geometry C
IL|Geely|monjaro
IL|Genesis|G70
IL|Haval|h6
IL|Honda|Civic Type R
IL|Honda|CR-Z
```

## Global RUN 4 rules

1. Do not aim only for green readiness. Fix data quality where the current clean row is weak, incomplete, duplicated, mis-scoped, or contradicted by Israeli-market sources.
2. If a row is only supported by global/non-Israeli facts and no strong Israeli evidence exists in the repository, move it to non-blocking archive/review rather than keeping it as verified clean.
3. Do not invent trims. Add trim names only when Israeli sources or embedded/source evidence clearly support them.
4. If a model is active/current in Israel, use `year_end = null`; if only used-price/catalog history is available, do not force `null`.
5. EVs may have `engine_displacement_l = null`.
6. `version_or_trim` must be scalar string/null, never an array.
7. Identity/casing issues are data-quality bugs even when readiness is green. Fix casing and add aliases/lineage so source keys do not become unmatched.
8. After fixes, rebuild outputs and run validation/quality/tests.

---

# RUN 4 corrections

## 1. Ford S-MAX

### Current catalog snapshot

Current profile has 5 rows, all with `version_or_trim = null`:

```text
2007-2010 petrol 2.3L 161 hp automatic FWD
2010-2015 petrol 2.0L turbo 203 hp dual_clutch FWD
2011-2015 petrol 2.0L turbo 240 hp dual_clutch FWD
2010-2015 diesel 2.0L turbo 140 hp dual_clutch FWD
2010-2015 diesel 2.0L turbo 163 hp dual_clutch FWD
```

### Validation facts

Israeli sources support the main technical split. iCar road test confirms the 2.0 turbo 203 hp row and says the Titanium version used the stronger 240 hp tune. Auto.co.il supports the 2.0 petrol 203/240 hp range and diesel engines in the local S-MAX context.

Useful source URLs:

```text
https://www.icar.co.il/מבחני_רכב/פורד_S-MAX_-_מבחן_רכב/
https://www.auto.co.il/cars/ford/s-max/
```

### Required action

**KEEP / FIX TRIM CONTEXT WHERE GROUNDED**

- Keep the five technical rows if source indexes and field_sources are valid.
- Add `version_or_trim = Titanium` to the 240 hp petrol row only if existing sources clearly support it.
- Keep other trims null if the repo-local evidence does not support exact trim names.
- Do not reopen this model as current; the Israeli clean profile should remain historical unless a strong Israeli current-sale source exists.

---

## 2. Ford Tourneo Connect

### Current catalog snapshot

Current profile has 4 rows:

```text
2003-2013 diesel 1.8L 90 hp manual
2016-2018 Trend diesel 1.5L 120 hp dual_clutch
2019-2021 Trend diesel 1.5L 120 hp automatic
2022-2026 Active diesel 2.0L 122 hp dual_clutch
```

### Validation facts

The 2022 Tourneo Connect generation is supported by Israeli/local automotive sources as a diesel 2.0L family, with 102/122 hp mentioned in launch/global-local coverage. The current catalog’s 122 hp Active row is plausible, but `year_end = 2026` should not be used as a fake current marker if the project convention expects active models to be `null`.

Useful source URLs:

```text
https://www.cartube.co.il/חדשות-רכב/פורד-חושפת-את-הטרונאו-קונקט-2022-החדש
https://www.icar.co.il/פורד/פורד_טורנאו_קונקט/
```

### Required action

**KEEP / FIX CURRENT YEAR CONVENTION**

- Keep the legacy rows if existing source/field-source support is valid.
- For the 2022+ 2.0 diesel 122 hp row, set `year_end = null` only if the current repo-local source/price catalog establishes it as currently offered.
- If the only evidence is a 2026 used/price listing and not active sale/current catalog, keep `year_end = 2026` or the grounded final year, but do not mark current incorrectly.
- Do not add AWD/PHEV rows unless Israeli sources in the repo directly support them.

---

## 3. Ford Transit

### Current catalog problem

Current profile closes at 2024 and misses/under-represents current Transit/E-Transit evidence:

```text
year_end = 2024 at model level
2017-2024 2.0 diesel 130 hp manual/automatic
2020-2024 2.0 diesel 170 hp 10-speed automatic RWD
```

### Validation facts

Israeli sources show 2025/2026 Transit entries and a current Cartube price/spec page listing Ford Transit 2.0 diesel automatic 170 hp rows, plus an electric E-Transit row. Carzone also supports 2024 Transit with 2.0L 130 hp automatic and 170 hp manual/automatic. Auto road-test material supports the 2.0 EcoBlue family with 130/170/185 hp and 10-speed automatic in the Israeli Transit context.

Useful source URLs:

```text
https://www.cartube.co.il/מחירון-רכב-חדש/פורד/פורד-טרנזיט
https://www.carzone.co.il/Ford/Transit/2024/
https://www.auto.co.il/articles/test-drives/road-tests/134569/
```

### Required action

**FIX CURRENT COVERAGE / ADD OR SPLIT ELECTRIC ONLY IF CONVENTION SUPPORTS**

- Do not keep Transit artificially closed at 2024 if the current Israeli source in the repo supports 2025/2026/current sale.
- Extend current 2.0 diesel 170 hp automatic rows to `year_end = null` if active/current is supported; otherwise to the latest directly supported year.
- Keep 130 hp manual/automatic rows only where directly grounded.
- If the repository supports separate electric model aliases, add/split `Ford E-Transit` or `Transit electric` with alias/lineage from `Ford Transit`; EV displacement null is valid.
- If E-Transit is only visible in price list but the project has no convention for electric submodel, add a non-blocking review/archive note rather than fabricating a weak clean row.

---

## 4. Ford Transit Custom

### Current catalog problem

Current profile includes a current 2024+ `Trend` row with:

```text
2.0L diesel, 136 hp, 8-speed automatic, FWD, year_end = null
```

But Israeli launch sources for the 2024 new Transit Custom also support a 170 hp diesel with 8-speed automatic, while Carzone supports a 136 hp Kombi/Custom row.

### Validation facts

Cartube launch coverage says the 2024 Transit Custom is marketed with 2.0L turbo diesel, 170 hp, 8-speed automatic. Auto says the new generation launched locally in 2024 and later body styles/electric versions were expected. Carzone supports a 2025 Kombi row with 136 hp.

Useful source URLs:

```text
https://www.cartube.co.il/חדשות-רכב/פורד-טרנזיט-קאסטום-החדש-2024-בישראל-מחיר-282000-שקל
https://www.auto.co.il/articles/car-news/local-news/136943/
https://www.carzone.co.il/Ford/Transit-Custom/Kombi/2025/
```

### Required action

**FIX / ADD CURRENT POWERTRAIN SPLIT**

- Do not replace 136 hp blindly if it is grounded as Kombi/Custom 2025.
- Add a separate 170 hp 2.0 diesel 8-speed automatic FWD current row if current source evidence exists in the repo.
- If the current source supports only van body for 170 hp and Kombi body for 136 hp, keep them as separate technical variants with body/trim notes.
- Keep `year_end = null` only for rows currently offered.
- Do not add electric Transit Custom unless local source evidence exists and project convention supports that electric line.

---

## 5. GAC / Aion V identity cleanup

### Current catalog problem

There are duplicate/competing clean profiles for the same Israeli-market model:

```text
global-reference-only|GAC|Aion V
IL|GAC / Aion|Aion V
```

Both represent the same basic EV SUV technical row:

```text
204 hp, electric, single-speed, FWD
```

### Validation facts

Official AION by GAC Israel page supports AION V as a 204 hp SUV with up to 510 km range. iCar local launch coverage also supports AION V with a front motor of 204 hp, 75.3 kWh battery, and 510 km theoretical range. Therefore this is a real Israeli-market model, but it must not appear twice under two makes/scopes.

Useful source URLs:

```text
https://aionauto.co.il/aion-v/
https://www.icar.co.il/news/rkdooplcxx/
```

### Required action

**MERGE / ALIAS / DELETE DUPLICATE CLEAN PROFILE**

- Canonical profile should be one clean model, preferably:

```text
IL|GAC / Aion|Aion V
```

- Merge `global-reference-only|GAC|Aion V` into the canonical profile as alias/lineage only.
- Do not keep both profiles as clean website models.
- The canonical row should remain:

```text
body_type = SUV
fuel_type = electric
engine = electric
engine_displacement_l = null
horsepower_hp = 204
transmission = single_speed
drivetrain = FWD
year_start = 2024 or 2025 according to strongest Israeli launch/source evidence in repo
year_end = null if current
support_level = direct
```

- Ensure alias matching prevents this from becoming an unmatched output key.

---

## 6. GAC / Aion Y identity cleanup

### Current catalog problem

There are duplicate/competing clean profiles:

```text
IL-confirmed|GAC / Aion|Aion Y
IL|GAC / Aion|Aion Y
```

One row has trim `Sense`; the other has `version_or_trim = null` and body_type `Crossover`.

### Validation facts

Official AION by GAC Israel page supports AION Y as an electric SUV/crossover with range up to 410 km. Cartube launch coverage and iCar launch coverage support GAC AION Y / Y Plus in Israel with 204 hp. Therefore this is a real Israeli-market model, but duplicated profiles should be merged.

Useful source URLs:

```text
https://aionauto.co.il/aion-y/
https://www.cartube.co.il/חדשות-רכב/דגמי-gac-aion-החשמליים-נחתו-בישראל-מחיר-142990-שקל
https://www.icar.co.il/news/rkdooplcxx/
```

### Required action

**MERGE / NORMALIZE BODY / ALIAS**

- Keep one canonical clean profile, preferably:

```text
IL|GAC / Aion|Aion Y
```

- Merge `IL-confirmed|GAC / Aion|Aion Y` into alias/lineage.
- Use one canonical body type, preferably `SUV` or project-standard crossover/SUV mapping, not two duplicate profiles solely because one says `Crossover`.
- Preserve `Sense` trim only if repo-local evidence directly supports it. If not, keep trim null rather than inventing.
- Do not publish both Aion Y profiles as separate clean website models.
- Ensure source aliases cover `Gac - Aion`, `GAC`, `Aion Y Plus`, and casing variants if present in the source/review/archive files.

---

## 7. Geely Geometry C

### Current catalog problem

Current catalog has one generic row:

```text
version_or_trim = null
2021-2024 electric 204 hp single_speed FWD
```

This is too coarse and may be incorrectly closed at 2024.

### Validation facts

Israeli sources support Geometry C with 204 hp electric FWD and multiple battery/range/trim configurations such as 350/360/460/480 and Pure/Pro. Auto.co.il 2024 source confirms the motor remains 204 hp. Carzone/Yad2 show 2024/2025 Israeli listing/spec evidence, while the current official Geely Israel homepage no longer prominently shows Geometry C as a current model and instead emphasizes newer EX5/STARRAY.

Useful source URLs:

```text
https://www.auto.co.il/cars/geely/geometry-c/2024/
https://www.carzone.co.il/Geely/Geometry-C/2025/
https://geely.co.il/
```

### Required action

**FIX COVERAGE / DO NOT OVER-OPEN CURRENT**

- Keep the 204 hp electric FWD technical basis.
- Split or label variants by grounded local trims/battery-range groups if the repo sources support them, e.g. Pure/Pro and 350/360/460/480 groups.
- Do not leave a single null-trim row if source evidence supports the real marketed Israeli variants.
- If strong source evidence supports 2025 Israeli sale/listing but not official current availability, set `year_end = 2025`, not `null`.
- Use `year_end = null` only if an official/current Israeli source in the repo confirms current sale.

---

## 8. Geely monjaro

### Current catalog problem

The model casing is wrong:

```text
IL|Geely|monjaro
```

Current rows are also suspicious for Israeli timing:

```text
2021-current 2.0 turbo 218 hp 7-speed dual_clutch FWD
2021-current 2.0 turbo 238 hp 8-speed automatic AWD
```

### Validation facts

Israeli/local 2025 Auto.co.il first-drive coverage supports Geely Monjaro with 2.0L turbo, 238 hp, 8-speed Aisin automatic and AWD. It does not support a 2021 Israeli start for a clean Israeli Monjaro row, and the 218 hp FWD row looks like global/non-Israeli leakage unless a repo-local Israeli source directly supports it.

Useful source URL:

```text
https://www.auto.co.il/articles/test-drives/first-drives/138154/
```

### Required action

**FIX CASING / FIX ISRAELI SCOPE / MOVE WEAK ROW**

- Canonical model should be:

```text
IL|Geely|Monjaro
```

- Add alias/lineage from:

```text
IL|Geely|monjaro
```

- Preferred clean Israeli row:

```text
year_start = 2025
year_end = null only if current/source supports current sale
body_type = SUV
fuel_type = petrol
engine = 2.0L turbo
engine_displacement_l = 2.0
horsepower_hp = 238
transmission = 8-speed automatic
drivetrain = AWD
support_level = direct
```

- Move/delete/archive the 218 hp FWD row unless a strong Israeli source in the repo directly supports that row.
- Do not keep 2021-current for Israel unless an Israeli source supports 2021 import/sale.

---

## 9. Genesis G70

### Current catalog problem

Current profile has two open-ended rows with null trim:

```text
2021-current Sedan 2.0 turbo 245 hp 8AT RWD
2021-current Estate 2.0 turbo 245 hp 8AT RWD
```

### Validation facts

Israeli sources support G70 in Israel from 2021 with 2.0 turbo 245 hp, 8-speed automatic, RWD. Carzone/Gear-style Israeli catalog pages support 2024 G70 with Luxury/Sport trim names and G70 Shooting Brake from 2023-2024. Auto.co.il says the Israeli G70 used the 2.0 turbo 245 hp engine, and notes the 2.5 update as a global/future update not necessarily Israeli-clean yet.

Useful source URLs:

```text
https://www.cartube.co.il/חדשות-רכב/ג-נסיס-g70-נוחתת-בישראל-מחיר-החל-מ-298-000-שקל
https://www.icar.co.il/ג'נסיס/ג'נסיס_G70/
https://www.carzone.co.il/Genesis/G70/2024/
https://www.auto.co.il/articles/car-news/world-news/136211/
```

### Required action

**FIX YEAR END / ADD TRIM CONTEXT WHERE GROUNDED**

- Do not keep G70 rows open-ended unless current official Israeli sale is supported.
- If current repo evidence only supports 2021-2024, set:

```text
year_end = 2024
```

- Add trim context `Luxury` and/or `Sport` if the repo-local sources support them for the sedan.
- Keep Shooting Brake/Estate row only where local evidence supports it, likely 2023-2024.
- Do not add 2.5L 304 hp unless there is direct Israeli-market source support; the Auto article describes the global update but says Israeli imported version had been 2.0 245 hp.

---

## 10. Haval h6

### Current catalog problem

The casing is wrong:

```text
IL|Haval|h6
```

Current clean rows are based heavily on Autoboom-style sources and include:

```text
2014-2020 2.0 diesel 156 hp manual FWD/AWD
2021-2025 2.0 petrol 224 hp dual_clutch FWD/AWD
```

### Validation facts

Autoboom Israel pages support Haval H6 listings/specs, but source strength is weaker than an official importer or major Israeli catalog. The model name casing should be fixed to `H6` at minimum. If only Autoboom/global-style sources support a row, it may be acceptable as legacy/reference but should not be promoted as verified clean beyond what those sources support.

Useful source URLs:

```text
https://autoboom.co.il/catalog/cars/haval/h6/1-generation/suv-5-doors/18057
https://autoboom.co.il/en/catalog/cars/haval/h6/2023
```

### Required action

**FIX CASING / VERIFY SOURCE STRENGTH**

- Canonical model should be:

```text
IL|Haval|H6
```

- Add alias/lineage from:

```text
IL|Haval|h6
```

- Keep rows only if source indexes and field_sources are valid.
- Do not set `year_end = null`; current catalog already ends 2025, which is safer if no official current Israeli source exists.
- If validation rules classify Autoboom-only rows as too weak for verified clean, move weak rows to non-blocking archive/review rather than keeping them as clean.

---

## 11. Honda Civic Type R

### Current catalog snapshot

Current profile has:

```text
2016-2022 Type R 2.0 turbo 319 hp 6MT FWD
2023-current Type R 2.0 turbo 329 hp 6MT FWD
```

### Validation facts

Israeli/local sources confirm the 2023 Civic Type R launch with 2.0 turbo 329 hp and 6-speed manual. Earlier FK-generation Israeli sources support Type R with a 2.0 turbo manual around 319/320 hp depending on metric/rounding conventions.

Useful source URLs:

```text
https://www.cartube.co.il/חדשות-רכב/הונדה-סיוויק-טייפ-r-החדשה-2023-בישראל-מחיר-314000-שקל
https://www.auto.co.il/article/129428-car-news-honda-civic-regular
https://www.icar.co.il/הונדה/הונדה_סיוויק_TYPE-R/הונדה_סיוויק_TYPE-R_חדש/
```

### Required action

**KEEP / VERIFY CURRENT YEAR END**

- Keep the 2023+ 329 hp row if source/field grounding is valid.
- `year_end = null` is acceptable only if current-sale/current-catalog evidence exists in the repo; otherwise cap to the latest supported local year.
- Keep earlier Type R row if 319/320 hp source support is valid; do not “fix” 319 to 320 unless the project uses Israeli catalog hp value rather than metric PS conversion.
- Ensure `version_or_trim = Type R` remains scalar.

---

## 12. Honda CR-Z

### Current catalog snapshot

Current profile has one row:

```text
2010-2013 hybrid 1.5L 124 hp 6-speed manual FWD Coupe
```

### Validation facts

Israeli/local sources support CR-Z as a 1.5 hybrid manual with 124 hp, sold around 2010-2013. Autoboom/Autocom/iCar/Wheel sources all broadly align on the hybrid manual technical fingerprint.

Useful source URLs:

```text
https://www.icar.co.il/הונדה/הונדה_CRZ/הונדה_CRZ_יד_שניה_דור_1/version8174/
https://www.autocom.co.il/הונדה-crz-2010/
https://autoboom.co.il/en/catalog/cars/honda/cr-z
```

### Required action

**KEEP**

- Keep the row if source_indexes and field_sources are valid.
- Do not add automatic/CVT rows unless Israeli evidence in the repo supports them.
- Do not extend past 2013 unless local evidence supports later Israeli sale.

---

# RUN 4 post-application requirements

After applying RUN 4 only:

1. Rebuild catalog outputs.
2. Regenerate readiness.
3. Regenerate quality scan.
4. Run:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
```

Return:

```text
RUN 4 RESULT: PASS / PASS WITH WARNINGS / FAIL
files changed
models touched
variants added/fixed/moved/archived
alias/lineage changes
readiness metrics after RUN 4
quality scan bug/leak/structure/normalization counts
unmatched output keys count/sample
tests run
commit hash if committed
remaining risks before FINAL blockers/unmatched run
```

Expected after RUN 4:

- RUN 4 clean-profile quality corrections applied.
- GAC/Aion duplicates merged or explicitly aliased.
- Geely/Haval casing fixed.
- No new unmatched output keys.
- Do **not** require final readiness green yet, because the final blockers/review-only run is still pending.


---

# BATCH 23 — FINAL RUN / BLOCKERS + UNMATCHED + IDENTITY CLEANUP CODEX TASK

## Execution scope

Execute this file as the **FINAL RUN only** for Batch 23.

This run covers:

1. The 29 active review/blocker source groups from the Batch 23 cursor window.
2. All non-matching / identity / casing / alias / split-profile cleanup discovered during the 88-source-group mapping.
3. Archive handling for weak Israeli-market evidence.
4. Final rebuild and readiness verification after RUN 1 + RUN 2 + RUN 3 + RUN 4 have been applied.

Do **not** browse the internet. All web-validation findings and target decisions are embedded here. Use only:

- this task file,
- existing repo-local sources/evidence,
- current generated catalog/review/readiness/quality files.

If a row cannot be strongly grounded from embedded facts or repo-local evidence, do **not** invent data. Move it to a non-blocking archive/review bucket and report it.

---

## Required final state after this FINAL RUN

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
quality bug findings = 0
quality normalization findings = 0
```

Expected cursor after the full Batch 23 window is completed:

```text
resume_after_key = IL|Honda|CR-Z
next_key_to_process = IL|Honda|e:Ny1
```

Do not let the cursor regress to a previously handled clean model or an archived blocker. Non-blocking archive entries may count as completed only when they are explicitly marked `non_blocking=true` and preserve source-key lineage.

---

# PART A — FINAL RUN source groups

The 29 active blockers / review-only groups from the uploaded ZIP were:

```text
IL|DS Automobiles|DS 3 Crossback
IL|Ferrari|F8 Tributo
IL|Fiat|500e
IL|Fiat|500X
IL|Fiat|Fullback
IL|Fiat|Multipla
IL|Fiat|Scudo
IL|Fiat|Stilo
IL|Fiat|Tempra
IL|Fiat|Ulysse
IL-confirmed|Ford|EcoSport
IL|Ford|Fiesta
IL|Ford|Mustang
IL|Ford|Transit Connect
IL-confirmed|Gac - Aion|aion v
IL-confirmed|Gac - Aion|aion y
IL|Geely|Starray
IL|Genesis|G80
IL|Genesis|G90
IL|Genesis|GV60
IL|Genesis|GV70
IL|Genesis|GV80
IL|GMC|Hummer EV
IL|GMC|Sierra
IL|GMC|Yukon
IL|Haval|jolion
IL|Honda|Accord
IL|Honda|Civic
IL|Honda|CR-V
```

---

# PART B — exact blocker instructions

## 1. DS Automobiles — DS 3 Crossback

Current review state:

```text
source_key: IL|DS Automobiles|DS 3 Crossback
technical_variants_il: empty
block reason: Extra data / parse failure
```

Problem:

This is not a missing-data model. It is a recoverable parse/output failure. Israeli sources support DS 3 Crossback as a real Israeli-market model before the later DS 3 naming.

Embedded validation facts:

- DS 3 Crossback reached Israel in 2019.
- Petrol engine: 1.2 turbo, 130 hp or 155 hp.
- Transmission: 8-speed automatic.
- Electric E-Tense version: 136 hp, 50 kWh class battery, around 317–330 km WLTP in early Israeli publications.
- Trims/naming seen in Israeli sources include So Chic, Grand Chic, Performance Line, Rivoli / Grand Chic Rivoli depending year/source.

Action:

`FIX / SPLIT / ALIAS`

Instructions:

1. Recover DS 3 Crossback into clean if repo-local sources support field-level grounding.
2. Add/keep lineage so DS 3 Crossback maps correctly to DS 3 if the catalog convention groups the facelift/new naming under `DS 3`.
3. Do not leave this as a blocker.
4. Suggested target rows, if supported by repo-local sources:

```json
[
  {
    "version_or_trim": "So Chic / Performance Line",
    "body_type": "SUV",
    "fuel_type": "petrol",
    "engine": "1.2L turbo",
    "engine_displacement_l": 1.2,
    "horsepower_hp": 130,
    "transmission": "8-speed automatic",
    "drivetrain": "FWD",
    "year_start": 2019,
    "year_end": 2022
  },
  {
    "version_or_trim": "Grand Chic / Rivoli",
    "body_type": "SUV",
    "fuel_type": "petrol",
    "engine": "1.2L turbo",
    "engine_displacement_l": 1.2,
    "horsepower_hp": 155,
    "transmission": "8-speed automatic",
    "drivetrain": "FWD",
    "year_start": 2019,
    "year_end": 2022
  },
  {
    "version_or_trim": "E-Tense / Rivoli",
    "body_type": "SUV",
    "fuel_type": "electric",
    "engine": "electric",
    "engine_displacement_l": null,
    "horsepower_hp": 136,
    "transmission": "single_speed",
    "drivetrain": "FWD",
    "year_start": 2021,
    "year_end": 2023
  }
]
```

If exact trims are not fully grounded, use safer trim labels like `130 hp`, `155 hp`, and `E-Tense`, but do not fabricate unsupported trims.

---

## 2. Ferrari — F8 Tributo

Current review state:

```text
source_key: IL|Ferrari|F8 Tributo
one technical variant exists
source_indexes missing
```

Current row:

```text
Coupe, petrol, 3.9L twin-turbo V8, 720 hp, 7-speed dual clutch, RWD, 2019–2023, direct, source_indexes=null
```

Problem:

The technical row is structurally correct enough, but it is blocked because `source_indexes` / `field_sources` are missing. Israeli Ferrari/F8 sources support the model and the 3.9 V8 twin-turbo with 7-speed DCT; hp may appear as 720 hp or 711 metric/local rounding depending source.

Action:

`FIX / KEEP`

Instructions:

1. Attach valid source_indexes and field_sources from repo-local Ferrari F8/F8 Tributo sources.
2. If repo-local source uses 711 hp instead of 720 hp, either:
   - keep 720 only when a direct source supports it, or
   - normalize to the local verified value and add a source note.
3. Do not leave in review solely due to missing source indexes.
4. If the model already exists as `Ferrari F8`, add alias/lineage from `F8 Tributo` to `F8` without creating duplicates.

---

## 3. Fiat — 500e

Current review state:

```text
source_key: IL|Fiat|500e
3 variants exist but source_indexes missing
```

Current rows:

```text
Action hatchback EV 95 hp, single_speed, FWD, 2021–2024
Icon hatchback EV 118 hp, 42kWh-class, single_speed, FWD, 2021–2024
La Prima convertible EV 118 hp, single_speed, FWD, 2021–2024
```

Problem:

500e is real in Israel. The blocker is mainly source linkage and possible overlap with `Fiat 500` / new-generation electric 500. Israeli sources support Action 95 hp and higher 118 hp trims such as Icon/Passion/La Prima/Cabrio/3+1 depending year.

Action:

`FIX / ALIAS / MERGE IF NEEDED`

Instructions:

1. Attach source_indexes and field_sources for the existing EV rows.
2. If the catalog convention groups electric 500 under `Fiat 500`, merge with alias `500e -> 500` and preserve lineage.
3. If the convention keeps `500e` as a separate model, keep it as `Fiat 500e` with clear alias to `Fiat 500 electric`.
4. Do not close at 2024 if current Fiat Israel/source files prove the electric 500 is still active; otherwise keep the 2021–2024 cap.
5. Do not leave `source_indexes=null`.

---

## 4. Fiat — 500X

Current review state:

```text
source_key: IL|Fiat|500X
technical_variants_il: empty
block reason: Extra data / parse failure
```

Problem:

500X is recoverable; the blocker is parser/output failure. Israeli sources support 500X in several trims and engines.

Embedded validation facts:

- Israeli 500X launch/used-data sources support 1.6 petrol manual Pop/Pop Star.
- Israeli sources support 1.4 turbo automatic variants such as Pop, Pop Star, Lounge, Cross.
- Do not invent later/current rows if no direct local source supports them.

Action:

`FIX`

Instructions:

Recover 500X into clean with field-level source grounding. Suggested target rows if supported:

```text
1.6 petrol, manual, FWD, Pop
1.6 petrol, manual, FWD, Pop Star
1.4 turbo petrol, automatic, FWD, Pop
1.4 turbo petrol, automatic, FWD, Pop Star
1.4 turbo petrol, automatic, FWD, Lounge
1.4 turbo petrol, automatic, FWD, Cross
```

Set years according to repo-local Israeli source coverage. If exact hp differs by source, use the value directly grounded by the repo source, not global memory.

---

## 5. Fiat — Fullback

Current review state:

```text
source_key: IL|Fiat|Fullback
3 variants exist but source_indexes missing / row coverage incomplete
```

Problem:

The row list is close but not exact. Israeli launch/spec evidence supports a more precise split.

Embedded validation facts:

- Fullback was sold in Israel around 2016–2019.
- 2.4 turbo diesel, 154 hp in Comfort versions.
- 2.4 turbo diesel, 181 hp in Style/Premium versions.
- Comfort existed as 4x2 manual and 4x4 automatic in some source material.
- Style/Premium 181 hp automatic 4x4 are supported by local spec evidence.

Action:

`FIX`

Target structure, if repo-local sources confirm:

```text
Comfort 4x2 — 2.4L turbo diesel, 154 hp, 6-speed manual, RWD/4x2, 2016–2019
Comfort 4x4 — 2.4L turbo diesel, 154 hp, automatic, 4WD, 2016–2019
Style — 2.4L turbo diesel, 181 hp, automatic, 4WD, 2016–2019
Premium — 2.4L turbo diesel, 181 hp, automatic, 4WD, 2016–2019
```

Do not keep only a partial three-row version if the source supports four distinct configurations.

---

## 6. Fiat — Multipla

Current review state:

```text
source_key: IL|Fiat|Multipla
technical_variants_il: empty
block reason: Extra data / parse failure
```

Problem:

Multipla is a legacy/low-volume model. Israeli used-car sources support it, but some technical fields may be weak.

Embedded validation facts:

- Israeli sources show Fiat Multipla 2000–2009.
- Common Israeli versions include 1.6 petrol manual and 1.9 diesel manual.

Action:

`FIX IF GROUNDED / ARCHIVE IF WEAK`

Instructions:

1. Recover minimal clean rows only if repo-local sources directly support the required website fields.
2. Suggested rows:
   - 1.6 petrol manual
   - 1.9 diesel manual
3. If horsepower, years, or transmission cannot be field-grounded, move uncertain rows/model to non-blocking archive.
4. Do not leave this as active review/blocker.

---

## 7. Fiat — Scudo

Current review state:

```text
source_key: IL|Fiat|Scudo
technical_variants_il: empty
block reason: non-object JSON
```

Problem:

This is recoverable. Israeli 2024 Scudo launch sources support a clear commercial van configuration.

Embedded validation facts:

- Fiat Scudo relaunched in Israel in 2024.
- Body: commercial closed van.
- Engine: 2.0 turbo diesel.
- Horsepower: 177 hp.
- Transmission: 8-speed automatic.
- Versions: medium and long / short and long body depending source wording.

Action:

`FIX`

Target rows:

```text
Medium / Short — Van, diesel, 2.0L turbo, 177 hp, 8-speed automatic, FWD, 2024-current if source supports current
Long — Van, diesel, 2.0L turbo, 177 hp, 8-speed automatic, FWD, 2024-current if source supports current
```

Do not add old Scudo or e-Scudo unless repo-local Israeli sources directly support them.

---

## 8. Fiat — Stilo

Current review state:

```text
source_key: IL|Fiat|Stilo
technical_variants_il: empty
block reason: JSON delimiter/parse failure
```

Problem:

Legacy Fiat Stilo rows should not be fabricated. This blocker is recoverable only if local repo sources support exact variants.

Action:

`FIX IF GROUNDED / ARCHIVE IF WEAK`

Instructions:

1. Search repo-local sources for Stilo variants and exact fields.
2. Potentially recover rows only when field-level grounding exists, e.g. 1.6 / 1.8 / Abarth if local sources prove they were Israeli-market variants.
3. If exact trim, hp, transmission, and year fields are not grounded, move to archive with `non_blocking=true`.
4. Do not leave active review.

---

## 9. Fiat — Tempra

Current review state:

```text
source_key: IL|Fiat|Tempra
4 variants exist
horsepower_hp = null on all rows
support_level = indirect
```

Problem:

These rows cannot go to clean with null hp if horsepower is a required website field. Do not guess exact horsepower from global memory.

Action:

`FIX IF LOCAL SOURCE SUPPORTS / ARCHIVE`

Instructions:

1. For each Tempra row, fill horsepower only if a repo-local Israeli source directly supports it.
2. Current rows are:
   - 1.4 manual sedan
   - 1.6 manual sedan
   - 1.6 Selecta/CVT sedan
   - Weekend 1.6 manual
3. If horsepower remains ungrounded, move Tempra to non-blocking archive.
4. Do not mark `support_level=direct` unless all non-empty fields are field-grounded.

---

## 10. Fiat — Ulysse

Current review state:

```text
source_key: IL|Fiat|Ulysse
2 variants exist but source_indexes missing
```

Current rows:

```text
JTD 2.0 diesel 109 hp automatic, FWD, 2004–2007
3.0 V6 petrol 204 hp automatic, FWD, 2004–2007
```

Problem:

The legacy Ulysse rows need field-level source grounding. There is also modern E-Ulysse information in Israeli sources, but do not mix the old Ulysse profile with E-Ulysse unless the catalog convention supports it.

Action:

`FIX IF GROUNDED / ARCHIVE IF WEAK`

Instructions:

1. If repo-local sources directly support the two legacy rows, attach source_indexes and field_sources.
2. If not, archive the legacy Ulysse rows as non-blocking.
3. Do not create `E-Ulysse` clean rows unless repo-local sources explicitly support Israeli market, body, hp, transmission, and years.
4. Preserve alias/lineage if `E-Ulysse` is handled separately.

---

## 11. Ford — EcoSport

Current review state:

```text
source_key: IL-confirmed|Ford|EcoSport
technical_variants_il: empty
block reason: Extra data / parse failure
```

Problem:

The `IL-confirmed` scope is non-standard, and the profile is parse-failed. This can only be restored if local evidence is strong enough.

Action:

`FIX IF GROUNDED / ARCHIVE + ALIAS`

Instructions:

1. Canonicalize source scope to `IL|Ford|EcoSport` if retained.
2. Add alias from `IL-confirmed|Ford|EcoSport`.
3. Reconstruct only variants directly grounded by repo-local Israeli sources.
4. If local evidence is not strong, archive non-blocking.
5. Do not keep `IL-confirmed` as a website-clean scope.

---

## 12. Ford — Fiesta

Current review state:

```text
source_key: IL|Ford|Fiesta
technical_variants_il: empty
block reason: JSON parse failure
```

Problem:

Fiesta is a real Israeli-market model, but this is a large legacy model and exact variant coverage is risky. Do not guess.

Action:

`FIX IF GROUNDED / PARTIAL CLEAN + ARCHIVE WEAK ROWS`

Instructions:

1. Reconstruct only rows whose trim/engine/hp/trans/year values are field-grounded in repo-local sources.
2. Prefer a partial, strongly grounded clean profile over a large invented profile.
3. Archive unsupported historical rows non-blocking.
4. Do not leave active review.

---

## 13. Ford — Mustang

Current review state:

```text
source_key: IL|Ford|Mustang
12 variants exist, but source_indexes missing
```

Problem:

The current review rows mix official/current Israeli Mustang evidence with older personal/parallel-import type evidence. This is a high-risk model. Do not publish historical/parallel variants as verified-clean unless repo-local sources strongly support them.

Embedded validation facts:

- The official/current Israeli Mustang appears mainly around 2024+.
- Stronger local evidence supports V8 GT current configurations; older EcoBoost/GT rows may be parallel/personal import or lower-confidence price-list data.
- Existing review rows include 2015–2023 EcoBoost and GT rows plus 2024–2026 EcoBoost/GT rows. This must not be accepted blindly.

Action:

`PARTIAL KEEP / ARCHIVE WEAK ROWS`

Instructions:

1. Keep clean only official/strongly grounded Israeli Mustang rows.
2. Prefer 2024+ V8 GT rows if sources support field-level values.
3. Do not keep 2015–2023 EcoBoost/GT rows in clean if the only basis is weak price-list/parallel-import evidence.
4. If older rows are not strongly grounded, move to non-blocking archive with a note: `parallel/personal-import evidence not sufficient for verified clean`.
5. Attach source_indexes and field_sources to all retained rows.
6. Avoid duplicate Mustang vs Mustang Mach-E; Mach-E is a separate EV profile already handled in RUN 3.

---

## 14. Ford — Transit Connect

Current review state:

```text
source_key: IL|Ford|Transit Connect
6 variants exist
last 2.0 diesel current row has hp/transmission null
```

Problem:

Transit Connect must not use Transit or Transit Custom sources. The 2023+ 2.0 row cannot be clean with missing hp/transmission.

Action:

`FIX / DELETE OR ARCHIVE BAD CURRENT ROW`

Instructions:

1. Keep the historical 1.8 / 1.6 / 1.5 diesel rows only if sources are valid and direct.
2. For the 2.0 diesel 2023-current row:
   - fill horsepower and transmission only if a repo-local Transit Connect source directly supports them,
   - otherwise move that row to archive or delete from clean/review.
3. Do not ground Transit Connect using Transit/Transit Custom source pages.
4. Final active review must be 0.

---

## 15. GAC / Aion — Aion V malformed source key

Current review state:

```text
source_key: IL-confirmed|Gac - Aion|aion v
technical_variants_il: empty
block reason: Extra data / parse failure
```

Problem:

This is not a new model. It is a duplicate/malformed key for Aion V, already represented in the clean window under GAC / Aion.

Action:

`MERGE / ALIAS / ARCHIVE SOURCE KEY`

Instructions:

1. Canonical clean model must be:

```text
IL|GAC / Aion|Aion V
```

2. Merge/archive aliases:

```text
global-reference-only|GAC|Aion V
IL-confirmed|Gac - Aion|aion v
```

3. Preserve source-key lineage so resume/unmatched counts remain 0.
4. Do not publish multiple clean Aion V profiles.
5. Target technical basis from RUN 4: Aion V electric SUV/crossover, 204 hp, FWD, with trims/range only if repo-local sources support them.

---

## 16. GAC / Aion — Aion Y malformed source key

Current review state:

```text
source_key: IL-confirmed|Gac - Aion|aion y
technical_variants_il: empty
block reason: non-object JSON
```

Problem:

Duplicate/malformed key for Aion Y.

Action:

`MERGE / ALIAS / ARCHIVE SOURCE KEY`

Instructions:

1. Canonical clean model must be:

```text
IL|GAC / Aion|Aion Y
```

2. Merge/archive aliases:

```text
IL-confirmed|GAC / Aion|Aion Y
IL-confirmed|Gac - Aion|aion y
```

3. Do not publish duplicate Aion Y profiles.
4. Preserve alias/lineage and keep unmatched output keys at 0.
5. Keep `Sense` or other trim names only if source-grounded.

---

## 17. Geely — Starray

Current review state:

```text
source_key: IL|Geely|Starray
one PHEV variant exists
horsepower_hp = null
support_level = indirect
```

Problem:

Starray is a real/current Israeli-market Geely PHEV, but hp is missing. Official/current Israeli Geely material supports 214 hp and Pro/Tech trims.

Embedded validation facts:

- Model: Geely Starray EM-i.
- Fuel: plug-in hybrid.
- Engine: 1.5L plug-in hybrid / hybrid powertrain.
- Combined output: 214 hp.
- Electric range: about 83 km according to local launch/spec material.
- Trims: Pro and Tech.
- Year: 2025/current or 2026 model year depending source, but Israeli launch is late 2025. Use `year_start=2025`, `year_end=null` if current source exists.

Action:

`FIX / SPLIT`

Target rows:

```text
Pro — SUV, plug_in_hybrid, 1.5L plug-in hybrid, 214 hp, automatic/direct_drive per schema, FWD, 2025-current
Tech — SUV, plug_in_hybrid, 1.5L plug-in hybrid, 214 hp, automatic/direct_drive per schema, FWD, 2025-current
```

Attach direct source_indexes and field_sources. Do not leave hp null.

---

## 18. Genesis — G80

Current review state:

```text
source_key: IL|Genesis|G80
technical_variants_il: empty
block reason: non-object JSON
```

Problem:

Recoverable output failure. Genesis Israel official/current sources support G80 and downloadable specs.

Embedded validation facts:

- Current G80 exists in Genesis Israel lineup.
- 2.5 turbo petrol, about 304 hp, 8-speed automatic, AWD is the expected local technical base.
- Official trims/pricing include names such as Exclusive / Luxury depending model year.
- Electrified G80 may also exist, but only include if repo-local sources directly support the EV row.

Action:

`FIX`

Instructions:

1. Reconstruct G80 from repo-local Genesis sources.
2. Minimum current clean rows if supported:
   - Exclusive — 2.5L turbo petrol, 304 hp, 8-speed automatic, AWD
   - Luxury — 2.5L turbo petrol, 304 hp, 8-speed automatic, AWD
3. Add Electrified G80 only if source-grounded; do not mix speculative EV data.
4. Use official Genesis Israel sources preferentially over marketplace/price-list sources.

---

## 19. Genesis — G90

Current review state:

```text
source_key: IL|Genesis|G90
technical_variants_il: empty
block reason: non-object JSON
```

Problem:

Recoverable output failure.

Embedded validation facts:

- Genesis Israel has G90 official/current pages/price information.
- Trims/names include Legendary, Executive, Black depending source.
- Technical basis: 3.5L V6 turbo / mild-hybrid/e-supercharged, 8-speed automatic, AWD.
- Horsepower in local sources may appear as 415 hp or similar depending exact powertrain. Use source-grounded value only.

Action:

`FIX`

Instructions:

1. Rebuild clean G90 rows only if official/repo-local sources provide direct field evidence.
2. Candidate rows:
   - Legendary
   - Executive
   - Black
3. Use `year_start=2025` or `2026` based on source; use `year_end=null` if current.
4. Do not guess horsepower. If the source supports 415 hp, use 415. If only another local source supports a different value, use the backed value with source note.

---

## 20. Genesis — GV60

Current review state:

```text
source_key: IL|Genesis|GV60
6 variants exist
transmission = null on EV rows
```

Problem:

GV60 is real/current, but EV transmission cannot be null in website clean rows. EV displacement null is valid; EV transmission null is not valid if schema expects a value.

Embedded validation facts:

- GV60 has RWD 228 hp.
- GV60 has AWD 318 hp.
- Performance/Ultimate variant has up to 489 hp with boost.
- EV transmission should be `single_speed` / `direct_drive` according to schema convention.

Action:

`FIX / KEEP`

Instructions:

1. Set EV transmission to `single_speed` or canonical project value for EV direct drive.
2. Keep rows such as:
   - 228 hp RWD Elegant/Premium/Luxury if source-backed
   - 318 hp AWD Premium/Luxury if source-backed
   - 489 hp AWD Ultimate/Performance if source-backed
3. Keep `engine_displacement_l=null` for EV.
4. `year_end=null` if current source supports current sale; otherwise use supported last year.
5. Attach/repair field_sources.

---

## 21. Genesis — GV70

Current review state:

```text
source_key: IL|Genesis|GV70
4 variants exist
EV rows have transmission=null
potential 3.5 hp local/global conflict
```

Problem:

GV70 rows are close but need field-source/transmission repair. Also be careful with 375 vs 380 hp for 3.5L because Israeli and global values may differ.

Embedded validation facts:

- 2.5 turbo petrol: 304 hp, 8-speed automatic, AWD.
- 3.5 turbo Sport: Israeli/global sources may show 375 or 380 hp; use repo-local Israeli source value.
- Electrified GV70: EV AWD, around 489 hp, EV transmission should not be null.

Action:

`FIX / KEEP`

Instructions:

1. Set EV transmission to single_speed/direct_drive.
2. Keep 2.5 petrol row if source-grounded.
3. For 3.5 row, do not override 375/380 blindly. Pick the value supported by repo-local Israeli source and document conflict if needed.
4. Set source_indexes/field_sources for all non-empty fields.
5. If Electrified GV70 is included, ensure alias/lineage does not create duplicate EV profile.

---

## 22. Genesis — GV80

Current review state:

```text
source_key: IL|Genesis|GV80
5 variants exist
some rows missing field_sources for body/fuel/year/etc.
```

Problem:

Rows are largely recoverable. Need field_sources and careful hp/value handling.

Embedded validation facts:

- Diesel 3.0 turbo 278 hp rows existed around 2020–2022.
- Current GV80 3.5L V6 turbo petrol produces 375 hp according to Genesis Israel page text.
- Official/current trims include Exclusive/Elegant/Luxury depending price/spec source.

Action:

`FIX / KEEP`

Instructions:

1. Repair field_sources for all required fields.
2. Keep diesel 278 rows only for years directly supported.
3. Keep current 3.5 V6 rows with 375 hp if Genesis Israel/repo source supports it.
4. Do not force 380 hp if official Israeli source says 375.
5. Ensure support_level reflects actual direct grounding.

---

## 23. GMC — Hummer EV

Current review state:

```text
source_key: IL|GMC|Hummer EV
3 variants exist
transmission=null
year_start/year_end null
support_level=indirect
```

Problem:

Current evidence appears global/weak or import-marketplace, not strong verified Israeli market. Do not publish Hummer EV as clean if only global reveal or weak dealer listings are available.

Action:

`ARCHIVE UNLESS STRONG IL SOURCE EXISTS`

Instructions:

1. If repo contains official/strong Israeli source for Hummer EV, repair rows with EV transmission single_speed/direct_drive and exact years/trims.
2. If not, move to non-blocking archive with reason:

```text
weak_or_global_only_evidence_not_enough_for_verified_clean
```

3. Do not leave active review.
4. Do not delete silently; preserve source-key and uncertainty trail.

---

## 24. GMC — Sierra / Sierra EV

Current review state:

```text
source_key: IL|GMC|Sierra
canonical_model: Sierra EV
horsepower_hp=null
transmission=null
drivetrain=null
support_level=unknown
```

Problem:

The current row is incomplete and weak. Some Israeli articles/dealer sources mention Sierra EV, but this may be import/dealer rather than official clean-market evidence. The row cannot be website clean with null hp/trans/drivetrain.

Action:

`FIX IF STRONG / ARCHIVE`

Instructions:

1. If repo-local sources directly support Sierra EV Denali/Max Range with hp/drivetrain/transmission, repair as EV pickup with single_speed/direct_drive and AWD.
2. If evidence is only dealer/parallel/global and fields remain incomplete, archive non-blocking.
3. Do not leave unknown support values.
4. Do not use Silverado EV or Hummer EV data as a substitute.

---

## 25. GMC — Yukon

Current review state:

```text
source_key: IL|GMC|Yukon
Denali 6.2 V8 420 hp 4WD 2020–2024
transmission=null
support_level=unknown
```

Problem:

Yukon may exist in Israel via niche/import channels, but the row is incomplete and weak. Do not use Chevrolet Tahoe/Cadillac Escalade sources to ground GMC Yukon.

Action:

`FIX IF DIRECT / ARCHIVE`

Instructions:

1. Fill transmission only if a repo-local GMC Yukon source directly supports it.
2. If only weak marketplace/import evidence exists, move to non-blocking archive.
3. Do not keep `support_level=unknown` in clean.
4. Final review must be 0.

---

## 26. Haval — Jolion

Current review state:

```text
source_key: IL|Haval|jolion
technical_variants_il empty
```

Problem:

Casing is wrong and Israeli evidence appears weak. Do not fabricate.

Action:

`CASING FIX + ARCHIVE IF WEAK`

Instructions:

1. Normalize identity to:

```text
IL|Haval|Jolion
```

2. Add alias from `IL|Haval|jolion`.
3. If no strong Israeli source exists in repo, archive non-blocking.
4. Do not publish a clean Jolion profile from Autoboom/global data alone.

---

## 27. Honda — Accord

Current review state:

```text
source_key: IL|Honda|Accord
8 variants exist
some rows have missing field_sources/support unknown
```

Problem:

Many Accord rows are probably recoverable, but a few need field-source repair or archival if unsupported.

Action:

`FIX / PARTIAL KEEP`

Instructions:

1. Repair field_sources for rows that are fully grounded.
2. The 2.0 petrol 155/156 hp rows should keep exact hp only if repo-local source supports it.
3. If the `Premium 2.0 156 hp` row is unsupported, merge/archive it rather than leaving `unknown` support.
4. Accord hybrid row must remain clean only if engine/hp/transmission/year are field-grounded.
5. Do not leave any `unknown_support_values`.

---

## 28. Honda — Civic

Current review state:

```text
source_key: IL|Honda|Civic
7 variants exist
2017–2021 turbo rows have drivetrain null
current hybrid row has transmission null / indirect support
Type R row may duplicate Honda Civic Type R profile
```

Problem:

Civic is real and mostly recoverable, but it must be normalized carefully.

Embedded validation facts:

- New Civic e:HEV in Israel is hybrid, around 183/184 hp depending source/rounding, with CVT/e-CVT style transmission and FWD.
- Civic Type R is already handled as a separate clean model in RUN 4 with 329 hp; avoid duplicate Type R rows inside Civic unless catalog convention requires both with alias.

Action:

`FIX / DEDUPE / ALIAS`

Instructions:

1. Set drivetrain to FWD on Civic petrol/turbo rows only if source-supported.
2. For current e:HEV row:
   - use hp value supported by Israeli source/repo source, likely 183/184 hp,
   - set transmission to CVT/e-CVT/canonical automatic according to schema,
   - set drivetrain FWD,
   - set support_level direct only when all fields are grounded.
3. If Type R exists in `Honda Civic Type R`, remove/alias the Type R row from the generic Civic profile to avoid duplicate website variants.
4. If keeping Type R under Civic, align hp with the separate Type R profile and add lineage; do not create duplicate technical variant signatures.

---

## 29. Honda — CR-V

Current review state:

```text
source_key: IL|Honda|CR-V
4 variants exist
first old 2.0 petrol row has transmission=null
some rows are indirect
```

Problem:

CR-V is a real Israeli-market model, but rows with null transmission/indirect support cannot enter verified clean without repair.

Action:

`FIX / PARTIAL KEEP / ARCHIVE UNSUPPORTED ROWS`

Instructions:

1. For old 2.0 petrol 155 hp AWD row, fill transmission only if repo-local Honda CR-V source directly supports it.
2. For modern rows, keep only if field-grounded:
   - 1.5 turbo petrol around 193 hp, CVT, AWD/FWD as sourced.
   - e:HEV 2.0 hybrid around 183/184 hp, CVT/e-CVT, AWD/FWD as sourced.
3. Do not infer transmission from global CR-V specs if local source is missing.
4. Archive unsupported rows non-blocking.
5. Final profile must not have null required fields.

---

# PART C — identity / alias / casing cleanup required in FINAL RUN

These identity issues must be handled even if `unmatched_output_keys_count` is currently 0.

## GAC / Aion canonicalization

Canonical keys:

```text
IL|GAC / Aion|Aion V
IL|GAC / Aion|Aion Y
```

Aliases/source keys to merge or mark completed non-blocking:

```text
global-reference-only|GAC|Aion V
IL-confirmed|Gac - Aion|aion v
IL-confirmed|GAC / Aion|Aion Y
IL-confirmed|Gac - Aion|aion y
```

Rules:

- Do not publish duplicate clean profiles.
- Preserve lineage/aliases.
- Archived aliases may advance resume only if explicitly `non_blocking=true`.

## DS casing

```text
IL|Ds Automobiles|ds 9 -> IL|DS Automobiles|DS 9
```

Add alias from the old key.

## Fiat Linea casing and source strength

```text
IL|Fiat|linea -> IL|Fiat|Linea
```

But do not keep unsupported multiple Linea variants in clean. If evidence is weak, archive weak rows and keep only field-grounded rows.

## Geely Monjaro casing

```text
IL|Geely|monjaro -> IL|Geely|Monjaro
```

Use RUN 4 instruction: Israeli Monjaro should not keep global 2021-current / 218 hp FWD row if local source supports 2025, 2.0 turbo, 238 hp, 8-speed automatic, AWD.

## Haval casing

```text
IL|Haval|h6 -> IL|Haval|H6
IL|Haval|jolion -> IL|Haval|Jolion
```

If H6/Jolion source strength is weak, archive non-blocking rather than inventing clean rows.

## Global/reference-only profiles

`global-reference-only` and `IL-confirmed` are not website-clean market scopes. They must either:

1. merge into canonical `IL|...` clean profile with lineage, or
2. move to non-blocking archive with source-key completion metadata.

Do not leave them as independent clean models for website upload.

---

# PART D — archive handling rules

Use a non-blocking archive for models/rows that are not strongly Israeli-market verified but should not remain active blockers.

Each archived item must include at minimum:

```json
{
  "source_key": "...",
  "canonical_make": "...",
  "canonical_model": "...",
  "reason": "weak_or_insufficient_israeli_evidence | duplicate_alias_source_key | global_reference_only | parallel_import_only | missing_required_field_grounding",
  "non_blocking": true,
  "batch_id": "BATCH23",
  "lineage_target": "IL|...|... or null"
}
```

Do not allow arbitrary/malformed archive rows to count as completed source groups. Only explicit `non_blocking=true` archive records should be counted as completed by resume-state logic.

---

# PART E — code/reporting fixes required if needed

Implement only if current code cannot support the final required state safely:

1. Resume-state must count explicitly non-blocking archived source groups as completed so cursor does not regress.
2. Resume-state must not count arbitrary archived/malformed entries unless `non_blocking=true` is explicit.
3. Alias matching must support old casing/source-scope aliases.
4. Quality scan must not report false `bug` findings for archived non-blocking rows.
5. Readiness must remain strict for clean catalog rows.

Do not weaken validation to force green. Green must come from actual clean/repair/archive decisions.

---

# PART F — rebuild + tests

After applying this FINAL RUN:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
```

Also run a direct generated-file audit with `compute_resume_state()` and inspect:

```text
data/model_technical_catalog_il.json
data/model_technical_catalog_il_readiness.json
data/model_technical_catalog_il_review.json
data/model_technical_catalog_il_quality_scan.json
archive/non-blocking archive file if present
alias/split-profile metadata files if present
```

Required reported values:

```text
clean model count
technical variant count
models_blocked
review_only_blocked_entries
duplicate_technical_variants
invalid_source_references
unknown_support_values
ready_for_website_upload
unmatched_output_keys_count
unmatched_output_keys_sample
active_blocked_count
split_profile_alias_count
resume_after_key
next_key_to_process
quality bug/leak/structure/normalization counts
```

Expected cursor after final run:

```text
resume_after_key = IL|Honda|CR-Z
next_key_to_process = IL|Honda|e:Ny1
```

If the cursor regresses to any already-handled source key, treat it as FAIL and fix before reporting success.

---

# PART G — required Codex response format

Return:

```text
FINAL RUN RESULT: PASS / PASS WITH WARNINGS / FAIL

1. Files changed
2. Models restored to clean
3. Models/rows archived non-blocking
4. Models merged/aliased
5. Variants added/fixed/moved/archived
6. Final readiness metrics
7. Quality scan counts
8. Resume/cursor audit
9. Unmatched/split/casing audit
10. Tests run
11. Commit hash if committed
12. Remaining risks before merge
```

If anything required remains blocked, say:

```text
Do not merge yet.
```

If the final state is green but relies on archive decisions, report the archive decisions explicitly.
