# BATCH 24 — RUN 1 CODEX TASK

## Scope

Execute **RUN 1 only** for Batch 24.

Window baseline from the uploaded ZIP:

```text
source_cursor = 467/1124
resume_after_key = IL-confirmed|Jeep|Avenger
next_key_to_process = IL-likely|Jeep|Avenger
clean_models = 438
review_only_blocked_entries = 12
active_blocked = 12
unmatched_output_keys_count = 0
split_profile_alias_count = 17
ready_for_website_upload = false
```

RUN 1 covers these 18 clean profiles:

```text
Honda HR-V
Honda Insight
Honda Jazz
Honda Legend
Honda Prelude
Honda ZR-V
Hongqi E-HS9
Hummer h2
Hummer h3
Hyundai Atos
Hyundai Bayon
Hyundai Casper
Hyundai Coupe
Hyundai Creta
Hyundai elantra
Hyundai Excel
Hyundai getz
Hyundai grandeur
```

Important: execute RUN 1 only. Do not continue to RUN 2 or blockers/final cleanup.

Also important: `data/model_technical_catalog_il_quality_scan.json` appears stale relative to the current catalog. Always regenerate quality scan after applying RUN 1.

---

## RUN 1 correction requirements

### 1. Honda HR-V — FIX

Current rows in clean:

```text
Honda HR-V
- null trim, petrol, 1.5L, 130 hp, CVT, FWD, 2016-current, support indirect
- null trim, hybrid, 1.5L, 131 hp, automatic, FWD, 2024-current, support indirect
```

Problems:

1. The old petrol HR-V must not remain open-ended/current. The Israeli petrol generation is the earlier 2016–2021 generation.
2. Current HR-V in Israel is the e:HEV hybrid line, not the old petrol row.
3. The 2024+ hybrid row should not stay trim-null if the Israeli current sources identify `Elegance` and `Advance`.

Validated facts:

- Israeli Honda HR-V petrol 2016 was sold with 1.5L petrol, 130 hp, CVT/FWD.
- Current Israeli HR-V e:HEV is 1.5L hybrid, FWD, 1,498 cc, 107 hp gasoline engine and 131 hp electric motor output; Israeli importer/source pages list `Elegance` and `Advance` trims.

Sources embedded for Codex task:

```text
https://www.auto.co.il/cars/honda/hr-v/2016/
https://hondacars.co.il/model/hrv-hybrid-ehev/
https://www.icar.co.il/הונדה/הונדה_HR-V/הונדה_HR-V_חדש/
https://www.cartube.co.il/חדשות-רכב/הונדה-hr-v-היברידי-החדש-2024-בישראל-מחיר-204900-שקל
```

Action:

```text
FIX
- Close old petrol HR-V row to year_end=2021 unless repo-local source proves a different Israeli end year.
- Keep petrol row as 1.5L petrol, 130 hp, CVT, FWD, year_start=2016.
- Replace/split the current hybrid row into current Israeli trims if schema allows trim rows:
  - Elegance, hybrid, 1.5L/e:HEV, 131 hp, automatic or e-CVT/cvt only if schema/source supports, FWD, year_start=2024, year_end=null
  - Advance, hybrid, 1.5L/e:HEV, 131 hp, automatic or e-CVT/cvt only if schema/source supports, FWD, year_start=2024, year_end=null
- If the schema prefers one technical row when trims share identical technical data, use scalar `version_or_trim="Elegance / Advance"`, not a list.
- Do not leave the petrol row current.
```

---

### 2. Honda Insight — KEEP

Current clean row:

```text
Comfort, hatchback, hybrid, 1.3L, 88 hp, CVT, FWD, 2009–2014
```

Validated facts:

- Israeli sources support second-generation Insight with 1.3L hybrid, CVT, Comfort trim, 2009–2014.
- Conflicting marketplace references to 102 hp exist, but current retained 88 hp is supported by stronger Israeli editorial/catalog evidence in the repo.

Action:

```text
KEEP
- Keep the current single Comfort row.
- Do not add global third-generation Insight or 1.5L/151 hp rows without direct Israeli-market source evidence.
```

---

### 3. Honda Jazz — FIX

Current rows include:

```text
2015–2020 petrol 1.3L 102 hp manual/CVT
2018–2020 petrol 1.5L 130 hp CVT
2020–2023 hybrid 1.5L 109 hp CVT
2023–2024 hybrid 1.5L 122 hp CVT
```

Problem:

- Jazz Hybrid is still current on Honda Israel / Honda Cars pages and Israeli 2026 catalog pages. The latest 1.5 e:HEV 122 hp row should not be closed at 2024 if current Israeli evidence is present.

Validated facts:

- Honda Jazz Hybrid e:HEV remains on the Israeli Honda Cars website.
- Israeli 2026 sources describe Jazz Hybrid 1.5 e:HEV with combined output of 122 hp.

Sources:

```text
https://hondacars.co.il/model/jazz-2/
https://www.auto.co.il/cars/honda/jazz/
https://www.carzone.co.il/Honda/Jazz/
```

Action:

```text
FIX
- Keep historical petrol and 2020–2023 109 hp hybrid rows if their sources remain valid.
- Change latest 1.5L hybrid 122 hp row year_end from 2024 to null/current.
- If exact current trims are grounded in repo-local sources, add scalar trim context such as Elegance / Crosstar or split rows by trim; otherwise do not invent trim labels.
- model-level year_end must become null/current after this fix.
```

---

### 4. Honda Legend — KEEP

Current rows:

```text
3.5L V6 208 hp automatic FWD, 1996–2004
3.5L V6 295 hp automatic AWD, 2006–2008
3.7L V6 291 hp automatic AWD, 2009–2012
```

Action:

```text
KEEP
- Keep historical rows as clean if source_indexes and field_sources are valid.
- Do not add ungrounded global/current rows.
```

---

### 5. Honda Prelude — KEEP

Current rows:

```text
2.0L 133 hp automatic FWD, 1992–2000
2.2L 185 hp automatic FWD, 1992–2000
```

Action:

```text
KEEP
- Keep historical rows only.
- Do not add future/global Prelude references unless direct Israeli-market launch/source evidence exists.
```

---

### 6. Honda ZR-V — FIX

Current clean row:

```text
null trim, crossover, hybrid, 2.0L, 184 hp, CVT, FWD, 2023–2024
```

Problems:

1. The catalog appears to use global/European timing. Israeli-market ZR-V launch is current/new for 2026.
2. Israeli current ZR-V has named trims; do not keep one null-trim row if exact Israeli trims are available.

Validated facts:

- Honda Cars Israel current ZR-V page lists 1,993 cc and 184 hp.
- Israeli coverage in January 2026 says ZR-V launched locally with 184 hp hybrid and three trims.
- iCar 2026 ZR-V pages list `Elegance`, `Sport`, and `Advance`.

Sources:

```text
https://hondacars.co.il/model/zrv-hybrid-ehev/
https://www.auto.co.il/articles/car-news/local-news/honda-zrv-launch/
https://www.icar.co.il/הונדה/הונדה_ZR-V/הונדה_ZR-V_חדש/version30254/
```

Action:

```text
FIX
- Replace current ZR-V row timing with Israeli timing:
  year_start=2026
  year_end=null/current
- Use 2.0L hybrid/e:HEV, 184 hp, FWD.
- Split into current Israeli trims if schema permits:
  - Elegance
  - Sport
  - Advance
- If duplicate detection would reject same technical rows, use scalar `version_or_trim="Elegance / Sport / Advance"` and document identical technical basis.
- Do not leave ZR-V as 2023–2024 clean row.
```

---

### 7. Hongqi E-HS9 — FIX / ENRICH

Current rows:

```text
Premium, electric, 435 hp, AWD, 2022–2024
Luxury, electric, 551 hp, AWD, 2022–2024
```

Problems:

1. Premium 435 hp historical row appears valid through 2024.
2. From 2025 onward, Israeli sources indicate E-HS9 was offered mainly/top-version 551 hp configurations; the catalog currently closes the whole model at 2024 and is missing current 551 hp structure.
3. Current official Hongqi Israel pages still reference the EHS9/Hongqi 9 line, but exact current trim rows must not be guessed beyond source support.

Validated facts:

- 2022 Israeli launch: Premium 435 hp and higher 551 hp trims.
- Auto/iCar/price-list sources indicate 2025/2026 551 hp E-HS9 variants such as Luxury/Exclusive/Exclusive LR.
- Premium 435 hp should not be kept current if sources show 2024 only.

Sources:

```text
https://www.cartube.co.il/חדשות-רכב/הונגצ-י-מותג-יוקרה-חשמלי-חדש-ויוקרתי-בישראל-מחיר-399000-שקל
https://www.auto.co.il/cars/hongqi/e-hs9/
https://hongqi.co.il/hongqi-9-new/
https://www.icar.co.il/הונגצ'י/הונגצ'י_E-HS9/הונגצ'י_E-HS9_חדש/version24632/
```

Action:

```text
FIX / ENRICH
- Keep Premium 435 hp AWD as 2022–2024 only.
- Keep Luxury 551 hp AWD and extend only if repo-local source supports 2025/current.
- Add `Exclusive` / `Exclusive LR` 551 hp AWD rows only if source data in repo or generated sources directly supports the exact trim, seats/range/body, and year range.
- If current 551 hp trim evidence is not strong enough in repo-local sources, do not fabricate; keep the historical rows and place current uncertainty in non-blocking archive/report note.
- Do not leave model-level year_end=2024 if at least one directly grounded 551 hp current row is retained.
```

---

### 8. Hummer h2 — FIX CASING, KEEP DATA

Current model identity:

```text
Hummer h2
```

Problem:

- Model casing is wrong. Should be `H2`, not `h2`.

Action:

```text
FIX
- Rename model to `Hummer H2`.
- Add alias/lineage from `IL|Hummer|h2` to `IL|Hummer|H2`.
- Keep current technical rows if source_indexes and field_sources are valid:
  6.0L V8 325 hp SUV/Pickup 2003/2005–2007
  6.2L V8 393 hp SUV/Pickup 2008–2009
- Do not create current Hummer EV linkage here.
```

---

### 9. Hummer h3 — FIX CASING, KEEP DATA

Current model identity:

```text
Hummer h3
```

Problem:

- Model casing is wrong. Should be `H3`, not `h3`.

Action:

```text
FIX
- Rename model to `Hummer H3`.
- Add alias/lineage from `IL|Hummer|h3` to `IL|Hummer|H3`.
- Keep rows if field grounding remains valid:
  3.5L inline-5 220 hp 2006–2007
  3.7L inline-5 242 hp 2007–2010
  5.3L V8 300 hp 2008–2010
```

---

### 10. Hyundai Atos — KEEP

Current rows:

```text
GL 1.0L 55 hp manual/automatic 1998–2000
Prime 1.0L 58 hp manual/automatic 2001–2003
```

Action:

```text
KEEP
- Keep historical Atos rows.
- No current/global additions.
```

---

### 11. Hyundai Bayon — KEEP / DO NOT REOPEN

Current rows:

```text
Premium, 1.0L turbo mild hybrid, 100 hp, 7DCT, 2022–2024
Prime, 1.0L turbo mild hybrid, 100 hp, 7DCT, 2022–2024
Supreme, 1.0L turbo mild hybrid, 100 hp, 7DCT, 2022–2024
Supreme, 1.0L turbo mild hybrid, 120 hp, 7DCT, 2022–2024
```

Validated facts:

- Hyundai Israel article and iCar/Auto sources support 1.0L turbo, 100 hp and 120 hp mild-hybrid versions.
- iCar new-page/search text indicates the model is not marketed as a new car and still displays 2024 in the page content; do not reopen as 2026/current without official/importer support.

Sources:

```text
https://www.hyundaimotors.co.il/article/bayon
https://www.icar.co.il/יונדאי/יונדאי_באיון/יונדאי_באיון_יד_שניה_ד10/
https://www.icar.co.il/יונדאי/יונדאי_באיון/יונדאי_באיון_חדש/version24755/
```

Action:

```text
KEEP
- Keep Bayon as 2022–2024.
- Do not set year_end=null/current based only on used-car/listing pages.
- Ensure 100 hp vs 120 hp rows remain distinct and scalar trims are not list-valued.
```

---

### 12. Hyundai Casper — MOVE / RENAME DECISION REQUIRED

Current clean model:

```text
Hyundai Casper
- electric, 97 hp, single_speed, FWD, 2025-current
- electric, 115 hp, single_speed, FWD, 2025-current
```

Problems:

1. Israeli-market name is not `Casper`; the EV version is marketed internationally/locally as `Hyundai Inster`.
2. Current sources found for Israel are mostly preview/arrival/first-drive pages, not a strong official Israeli sales page in the current catalog sources.
3. The existing clean source metadata in the ZIP uses preview articles (`expected in Israel`, `way to Israel`) rather than confirmed official sales/price-list grounding.

Validated facts:

- Hyundai Inster is based on Casper but is the EV model name used in Israeli coverage.
- Israeli sources describe 97 hp and 115 hp electric versions, but some sources frame it as expected/estimated arrival rather than confirmed official sale.

Sources:

```text
https://www.auto.co.il/cars/hyundai/inster/
https://www.icar.co.il/test_drive/hknk2y11jyx/
https://www.cartube.co.il/חדשות-רכב/יונדאי-אינסטר-הוא-קרוסאובר-עירוני-חשמלי-עם-טווח-של-355-קילומטר
```

Action:

```text
MOVE / FIX IDENTITY
- Do not keep `Hyundai Casper` as a clean Israeli model name.
- Preferred if repo-local evidence contains an official Israeli sales/price source:
  MERGE/RENAME to `Hyundai Inster`
  Add alias/lineage from `IL|Hyundai|Casper` to `IL|Hyundai|Inster`.
  Keep 97 hp and 115 hp electric FWD rows, year_start=2025, year_end=null only if official or strong Israeli sales evidence exists.
- If no stronger source exists beyond preview/expected-arrival articles:
  MOVE `Hyundai Casper` / `Hyundai Inster` to non-blocking archive with reason `insufficient_confirmed_israeli_sales_evidence` or `expected_arrival_only`.
  Do not leave it as clean.
- In all cases, never publish `Casper` as the canonical clean Israeli EV model.
```

---

### 13. Hyundai Coupe — KEEP

Current rows cover 1996–2009 generations with 1.6L, 2.0L, and 2.7L V6 petrol manual/automatic rows.

Action:

```text
KEEP
- Keep historical rows if source and field-source references validate.
- Do not add Genesis Coupe or Tiburon global aliases unless directly supported by Israeli catalog lineage.
```

---

### 14. Hyundai Creta — KEEP WITH PARALLEL-IMPORT SCOPE / DO NOT OVERSTATE

Current rows:

```text
1.5L petrol 115 hp CVT FWD, 2020–2024
1.4L turbo petrol 140 hp 7DCT FWD, 2020–2024
```

Problem:

- Israeli evidence is mainly parallel-import/local importer evidence, not the official Hyundai/Colmobil new-car lineup.

Validated facts:

- Automax / Israeli coverage support Hyundai Creta as parallel import with 1.5L 115 hp and 1.4L turbo 140 hp configurations.

Sources:

```text
https://automax.co.il/hyundai-creta/
https://www.cartube.co.il/חדשות-רכב/יונדאי-קרטה-2021-החדש-בישראל-יבוא-מקביל-מחיר-החל-מ-134900-שקל
```

Action:

```text
KEEP WITH SCOPE OR ARCHIVE
- If the catalog allows parallel-import-only models in clean, keep Creta but add/retain note/source metadata that it is `parallel_import_only`, not official Colmobil lineup.
- Do not make it current/open-ended unless a current local importer/price source exists.
- If website clean should include only official/importer-confirmed models, move to non-blocking archive rather than deleting.
```

---

### 15. Hyundai elantra — FIX CASING + CURRENT TRIMS + MISSING ELANTRA N

Current model identity:

```text
Hyundai elantra
```

Current rows include:

```text
null trim, hybrid, 1.6L, 141 hp, dual_clutch, FWD, 2021–2025
historical petrol rows 2001–2020
```

Problems:

1. Model casing is wrong: `elantra` -> `Elantra`.
2. Current Elantra Hybrid should not stay trim-null; official current Israeli page lists trims Prime/Premium/Supreme/Luxury.
3. Current 2026 Israeli sources indicate the hybrid output is 139 hp in some catalog sources; existing 141 hp may come from older/alternate rating. Use importer/repo source as source of truth; do not silently keep an unsupported number.
4. Hyundai Elantra N is currently sold in Israel and is missing from clean. It should be a separate performance model, similar to existing conventions for `i30 N`, `Kona N`, `Civic Type R`.

Validated facts:

- Hyundai Israel current Elantra Hybrid page lists current trim levels Prime, Premium, Supreme, Luxury.
- Israeli current sources list Elantra Hybrid 2026 with 1.6 hybrid and about 139 hp; if repo-local official spec says 141, document the source conflict and use official importer value.
- Hyundai Elantra N launched/sold in Israel in 2025/current with 2.0 turbo, 280 hp, Performance manual and Performance automatic/DCT variants.

Sources:

```text
https://www.hyundaimotors.co.il/models/elantra-hybrid
https://www.auto.co.il/cars/hyundai/elantra-hybrid/
https://www.cartube.co.il/מחירון-רכב-חדש/יונדאי/יונדאי-אלנטרה/6476-יונדאי-אלנטרה-1-6-היברידי-supreme
https://www.hyundaimotors.co.il/models/elantran
https://www.cartube.co.il/חדשות-רכב/יונדאי-אלנטרה-n-נחתה-בישראל-מחיר-224900-שקל
https://www.auto.co.il/cars/hyundai/elantra-n/
```

Action:

```text
FIX / SPLIT / ADD
- Rename canonical model to `Hyundai Elantra`.
- Add alias/lineage from `IL|Hyundai|elantra` to `IL|Hyundai|Elantra`.
- Split or scalar-label current hybrid row into trims:
  Prime, Premium, Supreme, Luxury
  fuel_type=hybrid
  engine=1.6L hybrid
  transmission=6-speed dual_clutch or dual_clutch according to schema
  drivetrain=FWD
  year_start=2021 or facelift/current split if repo data supports it
  year_end=null/current
  horsepower_hp:
    - Use 139 if current 2026 Israeli sources are the strongest local source.
    - Use 141 only if importer/repo-local field source directly supports it.
    - Do not leave an unsupported hp value silently.
- Preserve historical petrol rows if valid.
- Add separate clean model `Hyundai Elantra N` if not already present:
  - Performance manual, sedan, petrol, 2.0L turbo, 280 hp, manual/6-speed manual, FWD, year_start=2025, year_end=null
  - Performance automatic, sedan, petrol, 2.0L turbo, 280 hp, 8-speed dual_clutch, FWD, year_start=2025, year_end=null
- Do not merge Elantra N into normal Elantra if the catalog convention keeps N/Type R performance lines separate.
```

---

### 16. Hyundai Excel — KEEP

Current rows:

```text
1.5L 81 hp sedan/hatchback manual/automatic, 1994–1995
```

Action:

```text
KEEP
- Keep historical Excel rows.
- Do not extend beyond Israeli-source years.
```

---

### 17. Hyundai getz — FIX CASING, KEEP DATA

Current model identity:

```text
Hyundai getz
```

Problem:

- Model casing is wrong. Should be `Getz`.

Action:

```text
FIX
- Rename canonical model to `Hyundai Getz`.
- Add alias/lineage from `IL|Hyundai|getz` to `IL|Hyundai|Getz`.
- Keep existing 1.3L/1.4L/1.6L rows if source and field-source grounding remain valid.
- Do not add 2011 tail rows unless repo-local Israeli source directly supports the exact row.
```

---

### 18. Hyundai grandeur — FIX CASING, KEEP HISTORICAL

Current model identity:

```text
Hyundai grandeur
```

Problem:

- Model casing is wrong. Should be `Grandeur`.
- Global 2023+ Grandeur information exists, but no strong official Israeli sales evidence was found in the current RUN 1 validation. Do not add current global rows.

Action:

```text
FIX
- Rename canonical model to `Hyundai Grandeur`.
- Add alias/lineage from `IL|Hyundai|grandeur` to `IL|Hyundai|Grandeur`.
- Keep historical 3.3L V6 235 hp automatic FWD, 2006–2011 if field grounding remains valid.
- Do not add 2023+ global Grandeur engines to clean without direct Israeli-market evidence.
```

---

## Required RUN 1 output state

After applying RUN 1:

```text
- RUN 1 models corrected only.
- Do not process RUN 2 models.
- Review/blocker count may remain >0 because final blockers are handled later.
- Do not create new unmatched output keys.
- Do not create duplicate technical variants.
- Regenerate catalog, readiness, review, archive, and quality scan outputs.
- Quality scan bug/normalization findings should not increase; if RUN 1 creates any bug/normalization finding, fix it before reporting success.
```

Run:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
```

Report back:

```text
RUN 1 RESULT: PASS / PASS WITH WARNINGS / FAIL
files changed
models touched
variants added/fixed/moved/archived
alias/lineage changes
readiness metrics after RUN 1
quality scan bug/leak/structure/normalization counts
unmatched output keys count/sample
tests run
commit hash if committed
remaining risks before RUN 2
```


---

# BATCH 24 — RUN 2 CODEX TASK

## Scope

Execute **RUN 2 only** for Batch 24.

Baseline from uploaded ZIP 17:

```text
source_cursor = 467/1124
resume_after_key = IL-confirmed|Jeep|Avenger
next_key_to_process = IL-likely|Jeep|Avenger
clean_models = 438
review_only_blocked_entries = 12
active_blocked = 12
unmatched_output_keys_count = 0
split_profile_alias_count = 17
ready_for_website_upload = false
quality_scan_stale = true
```

RUN 2 covers these 17 clean profiles:

```text
Hyundai H1
Hyundai i10
Hyundai i20
Hyundai i25
Hyundai i30
Hyundai i30 N
Hyundai i40
Hyundai Ioniq 5
Hyundai Ioniq 5 N
Hyundai Ioniq 6
Hyundai ix35
Hyundai Kona N
Hyundai Matrix
Hyundai Nexo
Hyundai Palisade
Hyundai Santa Fe
Hyundai Sonata
```

Important: execute RUN 2 only. Do not continue to RUN 3, RUN 4, or final blockers.

Also important: `data/model_technical_catalog_il_quality_scan.json` appears stale relative to the current catalog/review outputs. Always regenerate quality scan after RUN 2 corrections.

---

## RUN 2 correction requirements

### 1. Hyundai H1 / i800 — KEEP WITH ALIAS/NOTES

Current clean rows:

```text
Hyundai H1
- null trim, Van, diesel, 2.5L turbo, 100 hp, manual, RWD, 1998–2007
- i800, Van, diesel, 2.5L turbo, 136 hp, manual, RWD, 2008–2021
- i800, Van, diesel, 2.5L turbo, 170 hp, automatic, RWD, 2008–2021
```

Validated facts:

- Israeli sources describe the second generation as `i800` in Israel.
- Israeli H1/i800 was sold locally with 2.5L diesel, 136 hp manual and 170 hp automatic.
- Do not extend H1/i800 as current without direct Israeli evidence. Some pages show 2024/new-page placeholders but mark the model as not marketed as a new vehicle.

Sources embedded for Codex task:

```text
https://www.auto.co.il/cars/hyundai/i800/
https://www.icar.co.il/יונדאי/יונדאי_i800/יונדאי_i800_יד_שניה_ד10/
https://www.icar.co.il/יונדאי/יונדאי_i800/יונדאי_i800_חדש/version19460/
```

Action:

```text
KEEP
- Keep the historical H1/i800 rows if their source_indexes and field_sources are valid.
- Preserve/add alias/lineage from Hyundai H1 to Hyundai i800 where project convention supports it.
- Do not open year_end/current.
- Do not add global H-1/Starex petrol rows.
```

---

### 2. Hyundai i10 — FIX

Current clean rows:

```text
Hyundai i10
- null trim, petrol, 1.1L, 69 hp, manual, FWD, 2009–2013
- null trim, petrol, 1.1L, 69 hp, automatic, FWD, 2009–2013
- null trim, petrol, 1.0L, 66 hp, manual, FWD, 2014–2019
- null trim, petrol, 1.0L, 66 hp, automatic, FWD, 2014–2019
- null trim, petrol, 1.25L, 87 hp, automatic, FWD, 2014–2019
- null trim, petrol, 1.2L, 84 hp, automatic, FWD, 2020–2024
```

Problems:

1. The 2020–2024/current-generation i10 row is too coarse: local sources show 1.2L 84 hp with both manual and automatic-electronic/robotic/single-clutch automatic transmissions.
2. The row labels `automatic` without representing the single-clutch robotic nature. Use the existing schema's canonical value if it does not support a separate single-clutch enum, but preserve a note/field source.
3. Current trims such as Intense/Prime/Prime Plus/Supreme are visible in Israeli sources; do not leave the current row completely trim-null if repo-local sources can support a safe scalar label.
4. Do not open to 2026 if the actual repo/source evidence says the Israeli new-car page is only 2024 or not currently marketed as new.

Validated facts:

- Hyundai Israel's 2024 new-i10 article says all trims use the familiar 1.2L 4-cylinder 84 hp engine and mentions automatic-electronic plus manual transmission.
- Auto Israel describes the current i10 with 84 hp and a slow robotic transmission, plus manual option.
- iCar's 2024 pages list 1.2 automatic trims such as Inspire/Prime and indicate single-clutch robotic automatic.

Sources embedded:

```text
https://www.hyundaimotors.co.il/article/new-i10
https://www.auto.co.il/cars/hyundai/i10/
https://www.icar.co.il/יונדאי/יונדאי_i10/יונדאי_i10_יד_שניה_ד12/version28779/
https://www.icar.co.il/יונדאי/יונדאי_i10/יונדאי_i10_חדש/version15350/
```

Action:

```text
FIX
- Keep historical 2009–2019 rows if their source links remain valid.
- For 2020–2024 generation, add/ensure a manual 1.2L 84 hp FWD row if repo-local source support exists.
- For automatic rows, represent transmission as the project's canonical robotic/single-clutch automatic value if available; if not, keep canonical `automatic` but add note/field-source evidence that it is the automatic-electronic/single-clutch robotic gearbox.
- Add scalar trim context only if safely grounded. Example: `Intense / Prime / Prime Plus / Supreme` for shared technical automatic variants, or split exact trim rows if project convention prefers exact trims.
- Do not set year_end=null/current unless repo-local official/current evidence proves it is still marketed as a new Israeli model.
```

---

### 3. Hyundai i20 — KEEP / LIGHT FIX

Current clean rows:

```text
Hyundai i20
- Insight / Inspire, petrol, 1.2L, 85 hp, manual, FWD, 2009–2014
- Inspire / Supreme, petrol, 1.4L, 100 hp, automatic, FWD, 2009–2018
- Supreme, petrol, 1.6L, 126 hp, automatic, FWD, 2009–2012
- Prestige / Prime / Supreme, petrol, 1.0L turbo, 100 hp, dual_clutch, FWD, 2018–2024
- Performance, petrol, 1.6L turbo, 204 hp, manual, FWD, 2022–2024
```

Validated facts:

- Israeli 2024 sources show i20 with 1.0L 100 hp and the N/Performance 204 hp version.
- iCar 2024 variant pages list many trims: Intense, Prime, Prime Plus, Prestige, Supreme, Supreme Plus.
- No strong current 2025/2026 Israeli evidence was embedded for opening the row beyond 2024 in this task.

Sources:

```text
https://www.auto.co.il/cars/hyundai/i20/
https://www.icar.co.il/יונדאי/יונדאי_i20/יונדאי_i20_יד_שניה_ד12/
https://www.icar.co.il/יונדאי/יונדאי_i20/יונדאי_i20_יד_שניה_ד12/version28785/
```

Action:

```text
KEEP / LIGHT FIX
- Keep the 1.0T 100 hp DCT row through 2024.
- Keep the 1.6T 204 hp Performance row through 2024.
- If exact trim rows are already grounded in repo-local sources, split/shared-label the 1.0T row to include Intense / Prime / Prime Plus / Prestige / Supreme / Supreme Plus.
- Do not open year_end to null/current unless repo-local current-source evidence supports it.
```

---

### 4. Hyundai i25 / Accent i25 — FIX TRANSMISSION

Current clean rows:

```text
Hyundai i25
- Inspire, petrol, 1.4L, 109 hp, automatic, FWD, 2011–2014
- Premium, petrol, 1.6L, 124 hp, automatic, FWD, 2011–2014
- Inspire, petrol, 1.4L, 100 hp, cvt, FWD, 2015–2019
- Premium, petrol, 1.6L, 124 hp, cvt, FWD, 2015–2019
```

Problem:

- The 2015–2019 generation uses conventional 6-speed automatic transmission in Israeli sources, not CVT.

Validated facts:

- Auto Israel describes the newer i25/Accent with 1.4L 100 hp and 1.6L about 123/124 hp, and says the transmissions are 6-speed only, including a planetary automatic transmission.
- Yad2/Israeli marketplace evidence supports 2015 entries with 1.4 100 hp Inspire and 1.6 124 hp Premium.

Sources:

```text
https://www.auto.co.il/cars/hyundai/i25/
https://www.yad2.co.il/vehicles/cars?manufacturer=21&model=10259&year=2015-2015
```

Action:

```text
FIX
- Change the 2015–2019 1.4L 100 hp row transmission from `cvt` to `6-speed automatic` or project canonical `automatic` with 6-speed evidence.
- Change the 2015–2019 1.6L 124 hp row transmission from `cvt` to `6-speed automatic` or project canonical `automatic` with 6-speed evidence.
- Do not change 1.6 hp from 124 to 123 unless the repo's field-level source policy prefers Auto's 123 hp over Yad2/marketplace 124 hp. If uncertain, keep 124 with a source-conflict note.
- Keep trims Inspire and Premium if field_sources are valid.
```

---

### 5. Hyundai i30 — KEEP / ADD TRIM CONTEXT ONLY IF GROUNDED

Current clean rows:

```text
Hyundai i30
- null trim, 1.6L petrol, 126 hp, 4-speed automatic, 2007–2012
- null trim, 1.6L petrol, 135 hp, 6-speed automatic, 2012–2017
- null trim, 1.4L turbo petrol, 140 hp, 7-speed DCT, 2017–2021
- null trim, 1.0L turbo petrol, 120 hp, 7-speed DCT, 2021–2022
```

Validated facts:

- Israeli sources support 2018–2020/2021 i30 with 1.4L turbo 140 hp and 7-speed DCT.
- Later 1.0L turbo 120 hp existed locally but requires repo-local field evidence for exact trims and end year.

Sources:

```text
https://www.icar.co.il/יונדאי/יונדאי_i30/יונדאי_i30_יד_שניה_ד12/
https://www.auto.co.il/cars/hyundai/i30/
```

Action:

```text
KEEP / LIGHT FIX
- Keep technical rows if field_sources are valid.
- Add exact trim context only if already supported by repo-local source fields.
- Do not extend i30 as current; the regular i30 should remain closed if no current Israeli new-car source exists.
- Do not duplicate Hyundai i30 N rows inside the regular i30 profile.
```

---

### 6. Hyundai i30 N — FIX UNSUPPORTED 2023+ MANUAL ROW

Current clean rows:

```text
Hyundai i30 N
- Performance, petrol, 2.0L turbo, 275 hp, 6-speed manual, FWD, 2019–2022
- Performance, petrol, 2.0L turbo, 280 hp, 8-speed dual_clutch, FWD, 2023–2024
- Performance, petrol, 2.0L turbo, 280 hp, 6-speed manual, FWD, 2023–2024
```

Problem:

- The 2023 Israeli relaunch sources strongly support the 280 hp DCT-8 row. The 2023–2024 280 hp manual row should not remain clean unless repo-local source evidence directly supports manual Israeli marketing in that period.

Validated facts:

- Israeli 2023 i30 N relaunch articles describe 2.0L turbo 280 hp, 8-speed DCT, FWD.
- Articles also mention the previous visit had 275 hp, which aligns with the older manual row.

Sources:

```text
https://www.auto.co.il/articles/car-news/local-news/136368/
https://www.cartube.co.il/חדשות-רכב/יונדאי-i30n-החדשה-2023-בישראל-מחיר-269900-שקל
```

Action:

```text
FIX
- Keep 2019–2022 275 hp 6-speed manual Performance row if sources remain valid.
- Keep 2023–2024 280 hp 8-speed dual_clutch Performance row.
- Move/delete the 2023–2024 280 hp manual row unless repo-local Israeli evidence directly supports it.
- If moved out, archive non-blocking with reason `unsupported_transmission_for_israeli_period`.
```

---

### 7. Hyundai i40 — KEEP

Current clean rows include sedan/estate, petrol/diesel, Premium trim, 2012–2018.

Action:

```text
KEEP
- Keep i40 historical rows if source_indexes and field_sources are valid.
- Do not reopen current.
- Do not add unsupported trims beyond Premium without direct source evidence.
```

---

### 8. Hyundai Ioniq 5 — FIX REGULAR VS N CONFUSION

Current clean rows:

```text
Hyundai Ioniq 5
- electric 217 hp RWD, 2021–2024
- electric 305 hp AWD, 2021–2024
- electric 170 hp RWD, 2023–2026
- electric 229 hp RWD, 2024–2026
- electric 609 hp AWD, 2024–2026
```

Problems:

1. The 609 hp row looks like leakage from the Ioniq 5 N performance model and should not remain in regular `Ioniq 5` unless a direct source proves a non-N 609 hp Israeli variant.
2. Current/facelift Ioniq 5 in Israel is supported with 170/229 and likely AWD power outputs, but do not use N data in the regular model.
3. Trim context such as Prestige/Supreme/Elite/Limited/Luxury appears in iCar pages; add only if field-grounded.

Validated facts:

- Auto Israel describes Ioniq 5 facelift from 2024 and notes a 2026 version with improved technical specification.
- iCar 2025 pages show Ioniq 5 229 hp Limited and list Prestige/Supreme/Elite/Elite 4X4/Luxury/Luxury 4X4 family trims.
- The high-output 650 hp car is explicitly Ioniq 5 N, a separate performance model.

Sources:

```text
https://www.auto.co.il/cars/hyundai/ionic-5/
https://www.icar.co.il/יונדאי/יונדאי_איוניק_5/יונדאי_איוניק_5_יד_שניה_ד10/version30398/
https://www.cartube.co.il/חדשות-רכב/יונדאי-איוניק-5n-מחיר-439990-שקל
```

Action:

```text
FIX
- Remove/move the 609 hp AWD row from regular `Hyundai Ioniq 5` unless direct repo-local evidence proves a regular non-N Ioniq 5 609 hp Israeli row.
- Keep old 217 RWD and 305 AWD rows through 2024 if source-grounded.
- Keep/fix facelift/current 170 RWD and 229 RWD rows; add/keep 325 AWD current row only if repo-local source supports it.
- Add scalar trim context only if exact sources support it.
- Ensure `Hyundai Ioniq 5 N` is a separate clean profile, not duplicated under Ioniq 5.
```

---

### 9. Hyundai Ioniq 5 N — FIX CURRENT STATUS

Current clean row:

```text
Hyundai Ioniq 5 N
- null trim, electric, 650 hp, single_speed, AWD, 2024–2024
```

Problem:

- The 650 hp N row is valid, but closing it at 2024 is likely wrong if the model remains listed/available in current Hyundai Israel lineup or current 2025 catalog pages.

Validated facts:

- Israeli 2024 launch sources describe Ioniq 5 N with 650 hp.
- iCar says Ioniq 5 N reached Israel in September 2024 and has 2025 used/new listing context.
- Hyundai Israel current site navigation includes IONIQ-5-N.

Sources:

```text
https://www.cartube.co.il/חדשות-רכב/יונדאי-איוניק-5n-מחיר-439990-שקל
https://www.icar.co.il/יונדאי/יונדאי_איוניק_5N/יונדאי_איוניק_5N_יד_שניה_ד10/
https://www.hyundaimotors.co.il/
```

Action:

```text
FIX
- Keep Ioniq 5 N as separate clean model with 650 hp, AWD, single_speed/electric direct drive.
- Change year_end from 2024 to null/current if repo-local current evidence supports it; otherwise at least 2025 if only 2025 listing evidence exists.
- Do not duplicate this row inside regular Ioniq 5.
```

---

### 10. Hyundai Ioniq 6 — FIX CURRENT ROWS

Current clean rows:

```text
Hyundai Ioniq 6
- electric 151 hp RWD, 2023–2024
- electric 228 hp RWD, 2023–2024
- electric 325 hp AWD, 2023–2024
```

Problems:

1. Israeli current sources show Ioniq 6 still marketed in 2026, at least as 228 hp RWD Ultra/Excellence.
2. Do not keep old 151/325 rows open-current unless exact current source supports them.

Validated facts:

- iCar current/new Ioniq 6 page describes base 151 hp, intermediate 228 hp, and higher AWD output in the model family.
- Cartube 2026 price/spec page lists 2026 Ioniq 6 facelift rows Ultra and Excellence with 228 hp.
- Auto Israel says Ioniq 6 is currently offered only with single motor/RWD 228 hp.

Sources:

```text
https://www.icar.co.il/יונדאי/יונדאי_איוניק_6/יונדאי_איוניק_6_חדש/
https://www.cartube.co.il/מחירון-רכב-חדש/יונדאי/יונדאי-איוניק-6
https://www.auto.co.il/cars/hyundai/ioniq-6/
```

Action:

```text
FIX
- Keep 151 hp and 325 hp rows as 2023–2024 or close at the exact repo-supported end year.
- Add/extend a 228 hp RWD current row for 2026/current.
- If exact current trims are supported, use Ultra / Excellence as scalar/split trim rows for 228 hp RWD.
- Do not open 151/325 to current unless directly grounded.
```

---

### 11. Hyundai ix35 — KEEP

Current rows:

```text
2.0L petrol 163 hp FWD, 2010–2013
2.0L petrol 154 hp FWD, 2014–2015
2.4L petrol 177 hp 4WD, 2010–2014
2.0L diesel turbo 184 hp 4WD, 2010–2015
```

Validated facts:

- Auto Israel confirms 2.0 petrol 163 hp before facelift and 154 hp after facelift, 2.4 petrol 177 hp, and 2.0 turbo diesel 184 hp.

Sources:

```text
https://www.auto.co.il/cars/hyundai/ix35/
https://www.cartube.co.il/חדשות-רכב/יונדאי-ix35-החדש-מתיחת-פנים-בישראל-–-מחיר-החל-מ-150,900-שקל
```

Action:

```text
KEEP
- Keep ix35 rows if sources and field_sources are valid.
- Do not add Tucson rows or extend as current.
```

---

### 12. Hyundai Kona N — KEEP

Current clean row:

```text
Hyundai Kona N
- null trim, SUV, petrol, 2.0L turbo, 280 hp, 8-speed dual_clutch, FWD, 2022–2023
```

Validated facts:

- Kona N was a distinct performance version; keep separate from the regular Kona blocker/final-run profile.
- Do not merge into regular Kona if project convention keeps performance model separate.

Action:

```text
KEEP
- Keep Kona N row if field sources remain valid.
- Do not duplicate it inside the regular Hyundai Kona profile during final blocker repair.
```

---

### 13. Hyundai Matrix — KEEP / WEAK SOURCE CAUTION

Current clean row:

```text
Hyundai Matrix
- GL, MPV, petrol, 1.6L, 103 hp, automatic, FWD, 2008–2010
```

Validated facts:

- Autoboom/Gear Israel references support 2008–2010 Matrix with 1.6L petrol, 103 hp, FWD, automatic/manual availability.
- Source tier is weaker than importer/iCar/Auto. Keep only if repo-local field_sources are valid and no stronger contradictory source exists.

Sources:

```text
https://autoboom.co.il/catalog/cars/hyundai/matrix
https://www.gear.co.il/מחירון-רכב-דגם/יונדאי/מטריקס/2008/מטריקס/1.6-SSSGL-אוטומט-
```

Action:

```text
KEEP / SOURCE CHECK
- Keep the GL 1.6L 103 hp automatic row if its existing source_indexes/field_sources are valid.
- If the only support is weak and validation policy requires stronger evidence, move to non-blocking archive rather than fabricating stronger data.
- Do not open current or add ungrounded trims.
```

---

### 14. Hyundai Nexo — MOVE TO ARCHIVE UNLESS ISRAELI SALES EVIDENCE EXISTS

Current clean row:

```text
Hyundai Nexo
- null trim, SUV, hydrogen, electric, 163 hp, single_speed, FWD, 2019-current
```

Problem:

- The current clean row appears to treat Nexo as a normal Israeli-market clean model, but available sources found here are mostly foreign/first-drive/global hydrogen coverage, not clear Israeli marketing/sales/importer evidence.
- Hydrogen infrastructure and limited global availability make this high risk for false clean inclusion.

Validated facts:

- Auto Israel article is a test/first-drive context abroad and discusses European pricing, not proof of Israeli sales as a clean local model.
- Cartube 2025 Nexo article is global/Korea news, not Israeli marketing.

Sources:

```text
https://www.auto.co.il/articles/test-drives/first-drives/132776/
https://www.cartube.co.il/חדשות-רכב/מימן-משופר-יונדאי-nexo-החדש-2025-נחשף
```

Action:

```text
MOVE TO ARCHIVE unless repo-local direct Israeli sales/registration/importer evidence exists.
- If there is no strong Israeli-market source in the repo, remove Nexo from clean and archive it as non_blocking=true with reason `global_or_foreign_test_drive_only` or `insufficient_israeli_market_evidence`.
- Preserve the technical reference row in archive lineage if useful.
- Do not leave 2019-current clean based only on global/test-drive evidence.
```

---

### 15. Hyundai Palisade — FIX / ADD 2026 HYBRID GENERATION

Current clean rows:

```text
Hyundai Palisade
- null trim, SUV, petrol, 3.8L V6, 291 hp, 8-speed automatic, FWD, 2020–2024
- null trim, SUV, petrol, 3.8L V6, 291 hp, 8-speed automatic, AWD, 2020–2024
```

Problem:

- The catalog misses the new 2026 Israeli Palisade hybrid generation.

Validated facts:

- Israeli May 2026 launch coverage says the new Palisade arrived in Israel as a 7/8-seat hybrid crossover with 2.5 turbo hybrid, 329 hp.
- Trims/prices include Excellence 8 seats, Excellence 7 seats, and Calligraphy 7 seats.
- Carzone 2026 evidence also references Calligraphy 4X4 hybrid 2.5L and other hybrid 2026 trims.

Sources:

```text
https://www.cartube.co.il/חדשות-רכב/יונדאי-פליסייד-החדש-2026-נחת-בישראל-מחיר-349990-שקל
https://www.carzone.co.il/Hyundai/Palisade/
```

Action:

```text
FIX
- Keep old 3.8L V6 291 hp FWD/AWD rows closed at 2024 unless repo-local source proves 2025 overlap.
- Add 2026-current Palisade hybrid rows:
  - Excellence, 2.5L turbo hybrid, 329 hp, automatic, drivetrain per source; include 7/8-seat context only if schema supports variant notes/body_detail.
  - Calligraphy, 2.5L turbo hybrid, 329 hp, automatic, drivetrain per source.
- If source ambiguity exists between FWD/AWD/4X4 for exact trim, do not guess drivetrain; either use only directly supported rows or move uncertain trim rows to review/archive non-blocking.
- model-level year_end should become null/current after valid 2026 rows are added.
```

---

### 16. Hyundai Santa Fe — FIX / ADD 2025–2026 HYBRID GENERATION

Current clean rows:

```text
Hyundai Santa Fe
- null trim, petrol, 2.4L, 185 hp, 6-speed automatic, FWD, 2019–2020
- null trim, petrol, 2.4L, 185 hp, 6-speed automatic, AWD, 2019–2020
- null trim, diesel, 2.2L turbo, 200 hp, 8-speed automatic, AWD, 2019–2020
- null trim, diesel, 2.2L turbo, 202 hp, 8-speed dual_clutch, AWD, 2021–2024
- null trim, hybrid, 1.6L turbo, 226 hp, 6-speed automatic, AWD, 2022–2024
```

Problems:

1. The new 2025/2026 Santa Fe Hybrid generation is missing or not represented accurately.
2. Current sources show several Israeli hybrid trims and different current outputs depending source/year: 215 hp for 2025 launch reports, 238 hp in 2026 price/spec pages.
3. Do not blindly extend the old 226 hp row as current if the current generation has different output and trims.

Validated facts:

- Hyundai Israel has a current Santa Fe Hybrid page and price list.
- Israeli 2025 launch coverage lists 1.6 turbo hybrid 2X4 Elite and 4X4 Calligraphy.
- Autocom 2025 describes 1.6 turbo hybrid with combined 215 hp.
- Cartube 2026 price/spec page lists Santa Fe Hybrid 2X4 Luxury/Ultimate/Excellence at 238 hp.

Sources:

```text
https://www.hyundaimotors.co.il/models/santa-fe-hybrid
https://www.hyundaimotors.co.il/article/santa-fe-hybrid-2025
https://www.cartube.co.il/חדשות-רכב/יונדאי-סנטה-פה-החדש-2025-נחת-בישראל-מחיר-369990-שקל
https://www.cartube.co.il/מחירון-רכב-חדש/יונדאי/יונדאי-סנטה-פה
https://www.auto.co.il/cars/hyundai/santa-fe/2025/537894/
```

Action:

```text
FIX
- Keep historical 2019–2024 rows if valid.
- Do not simply open the old 226 hp hybrid row to current.
- Add a new generation row/set for 2025-current Santa Fe Hybrid only with directly supported values.
- If using 2025 launch facts, add 1.6L turbo hybrid 215 hp rows for Elite 2X4/FWD and Calligraphy 4X4/AWD, year_start=2025.
- If using 2026 price/spec facts, add/update current 1.6L turbo hybrid 238 hp rows for Luxury/Ultimate/Excellence only if those values are directly supported by repo-local sources.
- If 215 vs 238 cannot be reconciled, preserve both as separate year-split technical variants with source notes rather than overwriting silently.
- model-level year_end should become null/current once current rows are grounded.
```

---

### 17. Hyundai Sonata — FIX CURRENT ROW / REMOVE UNSUPPORTED CURRENT PETROL

Current clean rows:

```text
Hyundai Sonata
- hybrid, 2.0L, 192 hp, 6-speed automatic, FWD, 2020-current
- petrol, 1.6L turbo, 180 hp, 8-speed automatic, FWD, 2021-current
- hybrid, 2.0L, 193 hp, 6-speed automatic, FWD, 2015–2019
- petrol, 2.0L, 144 hp, 4-speed automatic, FWD, 2006–2010
- petrol, 2.4L, 161 hp, 5-speed automatic, FWD, 2006–2010
```

Problems:

1. Current Israeli Sonata appears to be hybrid-only in recent official/editorial sources.
2. The 1.6 turbo petrol row should not remain current unless direct Israeli-market source evidence supports current sale.
3. Current hybrid row should carry trim context such as Luxury if source-grounded.

Validated facts:

- Hyundai Israel current Sonata Hybrid page presents Sonata Hybrid.
- Auto Israel states the renewed Sonata is marketed in Israel only as a hybrid combining 2.0L petrol + electric for 192 hp, FWD, 6-speed automatic.
- Cartube 2026 price/spec page lists Sonata Hybrid 2.0 Luxury and says launch year 2019.

Sources:

```text
https://www.hyundaimotors.co.il/models/sonata-hybrid
https://www.auto.co.il/cars/hyundai/sonata/
https://www.cartube.co.il/מחירון-רכב-חדש/יונדאי/יונדאי-סונטה/6465-יונדאי-סונטה-היברידית-2-0-luxury
```

Action:

```text
FIX
- Keep current 2.0L hybrid 192 hp row open/current.
- Add scalar trim context `Luxury` for the 2026 current row if source-grounded, or split by trim only if exact trims are supported.
- Close the 1.6L turbo petrol 180 hp row to the last directly supported Israeli year if repo-local evidence exists; otherwise move to archive/review non-blocking.
- Do not keep 1.6T petrol as current without direct evidence.
- Keep older 2015–2019 hybrid 193 hp and 2006–2010 petrol rows if source-grounded.
```

---

## Required post-RUN 2 checks

After applying RUN 2 only:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
```

Report:

```text
RUN 2 RESULT: PASS / PASS WITH WARNINGS / FAIL
files changed
models touched
variants added/fixed/moved/archived
alias/lineage changes
readiness metrics after RUN 2
quality scan bug/leak/structure/normalization counts
unmatched output keys count/sample
tests run
commit hash if committed
remaining risks before RUN 3
```

Do not report success if:

```text
- Hyundai Ioniq 5 still contains an N/high-output row duplicated in the regular Ioniq 5 profile without direct non-N evidence.
- Hyundai Nexo remains clean without direct Israeli-market sales/importer evidence.
- Hyundai Palisade lacks the 2026 hybrid generation despite embedded source support.
- Hyundai Santa Fe old 226 hp row is blindly opened as current while newer 2025/2026 generation facts are ignored.
- Hyundai Sonata 1.6T petrol remains current without direct current Israeli evidence.
- quality scan is not regenerated.
```


---

# BATCH 24 — RUN 3 CODEX TASK

## Scope

Execute **RUN 3 only** for Batch 24.

Baseline from uploaded ZIP 17:

```text
source_cursor = 467/1124
resume_after_key = IL-confirmed|Jeep|Avenger
next_key_to_process = IL-likely|Jeep|Avenger
clean_models = 438
review_only_blocked_entries = 12
active_blocked = 12
unmatched_output_keys_count = 0
split_profile_alias_count = 17
ready_for_website_upload = false
quality_scan_stale = true
```

RUN 3 covers these 17 clean source groups:

```text
Hyundai Staria
Hyundai Terracan
Hyundai Veloster
Hyundai Venue
Infiniti G Series
Infiniti Q30
Infiniti Q50
Infiniti Q60
Infiniti Q70
Infiniti QX30
Infiniti QX50
Infiniti QX60
Infiniti QX70
Infiniti QX80
global-reference-only|Isuzu|Rodeo
IL-confirmed|Isuzu|Rodeo
IL-likely|Isuzu|Trooper
```

Important: execute RUN 3 only. Do not continue to RUN 4 or final blockers/unmatched.

Also important: `data/model_technical_catalog_il_quality_scan.json` appears stale relative to the current catalog/review outputs. Always regenerate quality scan after RUN 3 corrections.

---

## RUN 3 correction requirements

### 1. Hyundai Staria — FIX DIESEL CURRENT STATUS + SPLIT CURRENT HYBRID TRIMS

Current clean rows:

```text
Hyundai Staria
- null trim, MPV, diesel, 2.2L turbo, 177 hp, 8-speed automatic, FWD, 2021–current
- null trim, Van, diesel, 2.2L turbo, 177 hp, 8-speed automatic, FWD, 2021–current
- null trim, MPV, hybrid, 1.6L turbo, 225 hp, 6-speed automatic, FWD, 2024–current
```

Validated facts:

- Current Israeli price/spec sources show `STARIA Hybrid` as the active/new model line, with 1.6L turbo-hybrid, 225 hp.
- Current 2026 sources list at least passenger 9-seat `Premium` and `Luxury` hybrid variants; Cartube also lists a 3-seat commercial closed-van hybrid.
- iCar’s old diesel page is marked “not marketed as a new vehicle” and shows the 2.2 diesel passenger variant as model year 2024.
- Therefore diesel rows must not stay open/current unless a repo-local importer/current source explicitly supports current diesel sale.

Sources embedded for Codex task:

```text
https://www.hyundaimotors.co.il/prices
https://www.auto.co.il/cars/hyundai/staria/
https://www.cartube.co.il/מחירון-רכב-חדש/יונדאי/יונדאי-סטאריה
https://www.icar.co.il/יונדאי/יונדאי_סטאריה/יונדאי_סטאריה_חדש/version24703/
```

Action:

```text
FIX
- Close diesel 2.2L 177 hp rows to year_end=2024 unless existing repo-local official source proves current diesel sales.
- Replace/split the current hybrid row into scalar trims where supported:
  - Premium, MPV/passenger, hybrid, 1.6L turbo, 225 hp, 6-speed automatic, FWD, year_start=2024 or 2025 per repo-local source, year_end=null.
  - Luxury, MPV/passenger, hybrid, 1.6L turbo, 225 hp, 6-speed automatic, FWD, year_start=2024 or 2025 per repo-local source, year_end=null.
  - Commercial/closed Van 3-seat hybrid, Van, 1.6L turbo hybrid, 225 hp, automatic, FWD, only if source-local evidence supports it.
- Do not keep a single null-trim current hybrid row if the sources expose Premium/Luxury/Commercial trim/body splits.
```

---

### 2. Hyundai Terracan — FIX PETROL HP IF UNSUPPORTED; KEEP HISTORICAL ONLY

Current clean rows:

```text
Hyundai Terracan
- GLS, diesel, 2.9L turbo, 150 hp, automatic, 4WD, 2001–2004
- GLS, diesel, 2.9L turbo, 163 hp, automatic, 4WD, 2004–2007
- GLS, petrol, 3.5L V6, 195 hp, automatic, 4WD, 2001–2004
```

Validated facts:

- Israeli used-car sources support Terracan as historical 2003–2007.
- Gear’s Israeli price/spec page for 2005–2007 lists the 3.5L petrol at 200 hp and 2.9 turbo-diesel automatic at 150 hp.
- Current 195 hp row may be global/older leakage unless repo-local sources directly support 195 hp.

Sources embedded for Codex task:

```text
https://www.icar.co.il/יונדאי/יונדאי_טראקאן/יונדאי_טראקאן_יד_שניה_ד10/
https://www.gear.co.il/מחירון-רכב-דגם/יונדאי/טראקאן/2005/טראקאן/5-מושבים-4x4-3.5-אוטומט-
```

Action:

```text
FIX / KEEP WITH SOURCE CHECK
- Keep Terracan historical only; do not open current.
- If no strong repo-local source supports 195 hp, correct the petrol 3.5L V6 row to 200 hp and align year range with the Israeli source evidence.
- Keep diesel rows only where source-backed; do not invent trims beyond GLS if not supported.
```

---

### 3. Hyundai Veloster — KEEP HISTORICAL; DO NOT EXTEND

Current clean rows:

```text
Hyundai Veloster
- Inspire, 1.6L petrol, 140 hp, manual, 2011–2016
- Inspire / Premium / Supreme / Elite, 1.6L petrol, 140 hp, dual_clutch, 2011–2016
- Elite, 1.6L turbo, 186 hp, manual, 2013–2016
- Elite, 1.6L turbo, 186 hp, automatic, 2013–2016
```

Validated facts:

- Israeli sources support 1.6 naturally aspirated 140 hp and 1.6 turbo 186 hp.
- Auto states Veloster marketing in Israel ended in May 2016.
- The joined trim row `Inspire / Premium / Supreme / Elite` is acceptable only if those trims are the same technical variant; otherwise split only if repo-local source supports distinct technical rows.

Sources embedded for Codex task:

```text
https://www.auto.co.il/cars/hyundai/veloster/2015/
https://www.carzone.co.il/Hyundai/Veloster/2013/
```

Action:

```text
KEEP WITH QA
- Keep historical year_end=2016.
- Do not open current.
- Do not introduce extra trims without exact local evidence.
- If schema rejects slash-joined trims, split only into identical technical rows with scalar trims, or keep a single shared technical row if this is the project convention for shared trims.
```

---

### 4. Hyundai Venue — FIX CURRENT STATUS + HP

Current clean row:

```text
Hyundai Venue
- null trim, SUV, petrol, 1.6L, 123 hp, CVT, FWD, 2019–2024
```

Validated facts:

- Hyundai Israel still has an active Venue model page.
- Auto’s current 2026 Venue page states the model is marketed in Israel with one 1.6L naturally aspirated engine, 121 hp, CVT with simulated 8 steps, and a trim update in early 2026.
- iCar also describes the 1.6L/CVT powertrain, but the current clean row’s 123 hp looks like global leakage rather than the Israeli value.

Sources embedded for Codex task:

```text
https://www.hyundaimotors.co.il/models/venue
https://www.auto.co.il/cars/hyundai/venue/
https://www.icar.co.il/יונדאי/יונדאי_וניו/יונדאי_וניו_חדש/
```

Action:

```text
FIX
- Correct horsepower from 123 hp to 121 hp unless repo-local official source supports 123 hp for Israel.
- Set year_end=null/current if source evidence supports current Israeli sale.
- Add scalar trim context only if repo-local Hyundai/Auto/iCar source exposes exact 2026 trim names; otherwise null trim is acceptable with explicit no-safe-trim note.
```

---

### 5. Infiniti G Series — KEEP, BUT DO NOT OVERGENERALIZE G25/G37

Current clean rows:

```text
Infiniti G Series
- Sedan, petrol, 3.7L V6, 320 hp, 7-speed automatic, RWD, 2009–2013
- Sedan, petrol, 2.5L V6, 222 hp, 7-speed automatic, RWD, 2011–2013
- Coupe, petrol, 3.7L V6, 320 hp, 7-speed automatic, RWD, 2009–2013
- Convertible, petrol, 3.7L V6, 320 hp, 7-speed automatic, RWD, 2009–2013
```

Validated facts:

- Israeli sources support the G37 coupe/convertible/sedan family and a G25 sedan entry with 2.5L/222 hp.
- Gear and iCar pages expose G37 body splits and 320 hp in some rows; other Israeli marketplace snippets show 315 hp for some sedan/coupe rows.
- Since the project currently models this profile as `G Series`, do not split into separate `G25` / `G37` models unless the repository already uses that convention.

Sources embedded for Codex task:

```text
https://www.icar.co.il/אינפיניטי/אינפיניטי_G37_קופה/
https://www.gear.co.il/מחירון-רכב-דגם/אינפיניטי/G37/2014/G37-קבריולט/3.7-GT-V6-אוטומט--
https://www.cartube.co.il/חדשות-רכב/אינפיניטי-מציגה-את-ה-g25-גרסה-זולה-למשפחת-ה-g
```

Action:

```text
KEEP WITH SOURCE-CONFLICT NOTE
- Keep G Series as a historical clean profile if field sources are valid.
- Do not create additional unsupported rows.
- If repo-local sources specifically support 315 hp rather than 320 hp for some G37 rows, split or correct by body/year; otherwise preserve 320 hp where directly grounded.
- Add notes that G25/G37 are designation/lineage names, not necessarily separate canonical models in this catalog convention.
```

---

### 6. Infiniti Q30 — KEEP

Current clean rows:

```text
Infiniti Q30
- Hatchback, 1.6L turbo, 156 hp, 7-speed dual_clutch, FWD, 2017–2019
- Hatchback, 2.0L turbo, 211 hp, 7-speed dual_clutch, AWD, 2017–2019
```

Validated facts:

- The two Q30 technical rows are plausible and historically bounded.
- No evidence found to extend Q30 as current.

Action:

```text
KEEP
- Preserve rows if source_indexes and field_sources are valid.
- Do not open current.
- Add scalar trim names only if already grounded in repo-local evidence.
```

---

### 7. Infiniti Q50 — FIX 3.0L POWER AND TRIM

Current clean rows:

```text
Infiniti Q50
- Sedan, petrol, 2.0L turbo, 211 hp, 7-speed automatic, RWD, 2014–2019
- Sedan, hybrid, 3.5L V6, 364 hp, 7-speed automatic, RWD, 2014–2019
- Sedan, petrol, 3.0L V6 turbo, 300 hp, 7-speed automatic, RWD, 2017–2022
```

Validated facts:

- Israeli iCar/Auto/Yad2 evidence supports Q50 3.0 turbo `Sport Tech` at 405 hp, not 300 hp.
- Auto states the 3.0L twin-turbo V6 was added toward late 2016 and produced 405 hp.
- Yad2 price-list rows show `Sport Tech` 3.0 at 405 hp for 2018/2019.
- Therefore the 300 hp row is likely global leakage and should not remain clean as an Israeli row without direct Israeli support.

Sources embedded for Codex task:

```text
https://www.icar.co.il/חדשות_רכב/אינפיניטי_Q50_מקבלת_מנוע_חדש._המחיר:_399,000_שקל/
https://www.auto.co.il/cars/infiniti/q50/
https://www.yad2.co.il/price-list/sub-model/102245/2019
```

Action:

```text
FIX
- Correct the 3.0L V6 turbo row from 300 hp to 405 hp if no Israeli source supports 300 hp.
- Set version_or_trim to `Sport Tech` where grounded.
- Keep year_start around 2017 or late-2016/2017 per schema convention; do not extend beyond the strongest repo-local year_end.
- Preserve 2.0T 211 and hybrid 364 rows if sources remain valid.
```

---

### 8. Infiniti Q60 — FIX 3.0L POWER

Current clean rows:

```text
Infiniti Q60
- Coupe, petrol, 2.0L turbo, 211 hp, 7-speed automatic, RWD, 2017–2020
- Coupe, petrol, 3.0L twin-turbo V6, 400 hp, 7-speed automatic, AWD, 2017–2020
```

Validated facts:

- Israeli launch/used-car sources support Q60 3.0 twin-turbo at 405 hp and AWD.
- iCar describes two engines: 2.0L 211 hp RWD and 3.0L 405 hp AWD.
- Cartube Israeli launch article also says 3.0L twin-turbo 405 hp.

Sources embedded for Codex task:

```text
https://www.icar.co.il/אינפיניטי/אינפיניטי_Q60/אינפיניטי_Q60_יד_שניה_ד10/
https://www.cartube.co.il/חדשות-רכב/2017-אינפיניטי-q60-החדשה-בישראל-מחיר-329000-שקל
https://www.auto.co.il/cars/infiniti/q60/2017/
```

Action:

```text
FIX
- Correct 3.0L twin-turbo Q60 horsepower from 400 to 405 hp unless repo-local source specifically supports 400 for Israel.
- Preserve 2.0L 211 hp row.
- Do not open current beyond supported local years.
```

---

### 9. Infiniti Q70 — KEEP

Current clean rows:

```text
Infiniti Q70
- Sedan, petrol, 3.7L V6, 320 hp, 7-speed automatic, RWD, 2014–2018
- Sedan, hybrid, 3.5L V6, 364 hp, 7-speed automatic, RWD, 2014–2018
```

Action:

```text
KEEP
- Preserve if source and field-source grounding remain valid.
- Do not open current.
- Add trim labels only if repo-local evidence safely maps them.
```

---

### 10. Infiniti QX30 — KEEP

Current clean row:

```text
Infiniti QX30
- Luxe Tech, Crossover, petrol, 2.0L turbo, 211 hp, 7-speed dual_clutch, AWD, 2017–2019
```

Action:

```text
KEEP
- This row is plausible, scalar, and historically bounded.
- Do not open current.
```

---

### 11. Infiniti QX50 — FIX CURRENT STATUS AND CURRENT TRIMS

Current clean rows:

```text
Infiniti QX50
- GT, SUV, petrol, 3.7L V6, 320 hp, 7-speed automatic, AWD, 2014–2018
- Luxe, SUV, petrol, 2.0L turbo, 268 hp, CVT, FWD, 2019–2023
- Essential, SUV, petrol, 2.0L turbo, 268 hp, CVT, AWD, 2019–2023
```

Validated facts:

- Infiniti Israel currently lists QX50 with 2.0 VC-Turbo at 268 hp and AWD.
- Cartube current 2026 price/spec page lists QX50 `2.0 Luxe 2X4` and `2.0 Sport 4X4`, both 268 hp.
- Therefore ending QX50 at 2023 is stale if current Israeli sources are available.
- The old 3.7L GT row remains historical only.

Sources embedded for Codex task:

```text
https://www.infiniti-cars.co.il/vehicles/qx50.html
https://www.cartube.co.il/מחירון-רכב-חדש/אינפיניטי/אינפיניטי-qx50
```

Action:

```text
FIX
- Keep 3.7L GT historical 2014–2018.
- Add or extend current 2.0L VC-Turbo 268 hp rows to current/null year_end.
- Use scalar current trims where supported:
  - Luxe, 2.0L turbo, 268 hp, CVT, FWD/2X4, year_end=null.
  - Sport, 2.0L turbo, 268 hp, CVT, AWD/4X4, year_end=null.
- Do not keep `Essential` as current if current sources show `Sport`; close it historically or rename only if repo-local evidence supports the replacement.
```

---

### 12. Infiniti QX60 — FIX 2025+ CURRENT ENGINE; CLOSE OLD 3.5

Current clean rows:

```text
Infiniti QX60
- Elite, SUV, petrol, 3.5L V6, 265 hp, CVT, AWD, 2014–2021
- Sensory, SUV, petrol, 3.5L V6, 295 hp, automatic, AWD, 2022–2024
```

Validated facts:

- Israeli sources show the old/newer 3.5L 295 hp QX60 rows through 2024/2025 used-price contexts.
- Current Infiniti Israel QX60 page lists a VC-Turbo engine producing 268 hp.
- Auto explains that until 2025 QX60 used the 3.5L naturally aspirated V6, then it was replaced by a 2.0L turbo-petrol VC-Turbo producing 268 hp with a 9-speed automatic and AWD.
- Therefore the 3.5L V6 row should not remain the only/current representation after 2024/2025 if current official source supports 2.0 VC-Turbo.

Sources embedded for Codex task:

```text
https://www.infiniti-cars.co.il/vehicles/qx60.html
https://www.auto.co.il/cars/infiniti/qx60/
https://www.yad2.co.il/price-list/feed?manufacturer=3&model=10062
```

Action:

```text
FIX
- Keep the 2014–2021 3.5L/265 hp Elite row only if source-backed.
- Close the 3.5L/295 hp row at 2024 or 2025 according to the strongest repo-local source.
- Add a current 2.0L VC-Turbo 268 hp row for QX60 with automatic 9-speed and AWD, year_start=2025 or 2026 per source, year_end=null.
- Use scalar trim names such as Luxe/Sensory only if supported by repo-local current source; otherwise use null trim with explicit current-source note.
```

---

### 13. Infiniti QX70 — ADD TRIM CONTEXT; KEEP HISTORICAL

Current clean rows:

```text
Infiniti QX70
- null trim, SUV, petrol, 3.7L V6, 320 hp, 7-speed automatic, AWD, 2014–2017
- null trim, SUV, diesel, 3.0L V6 turbo, 238 hp, 7-speed automatic, AWD, 2014–2017
- null trim, SUV, petrol, 5.0L V8, 390 hp, 7-speed automatic, AWD, 2014–2017
```

Validated facts:

- Israeli sources support QX70 with 3.7L 320 hp, 3.0 diesel 238 hp, and 5.0L 390 hp.
- iCar exposes trim labels such as GT, GT Premium, and S Premium.
- Gear states all QX70 engines were paired with 7-speed automatic and AWD.

Sources embedded for Codex task:

```text
https://www.icar.co.il/אינפיניטי/אינפיניטי_QX70/אינפיניטי_QX70_יד_שניה_ד10/version13303/
https://www.gear.co.il/כתבת-רכב/2015-07-06-N01-מבצע-קרוסאובר-אינפיניטי
https://www.yad2.co.il/vehicles/cars?manufacturer=3&model=10063
```

Action:

```text
FIX / ENRICH
- Keep historical 2014–2017.
- Add scalar trims where field evidence supports them:
  - 3.7 petrol 320 hp: GT / GT Premium if both are source-backed.
  - 3.0 diesel 238 hp: GT / GT Premium if both are source-backed.
  - 5.0 petrol 390 hp: S Premium if source-backed.
- If exact trim/body mapping is not fully supported, keep technical rows but do not invent trims; add note.
```

---

### 14. Infiniti QX80 — FIX DRIVETRAIN; KEEP HISTORICAL UNLESS CURRENT ISRAELI SOURCE EXISTS

Current clean row:

```text
Infiniti QX80
- null trim, SUV, petrol, 5.6L V8, 400 hp, 7-speed automatic, RWD, 2014–2022
```

Validated facts:

- Israeli Cartube source for QX80 update says 5.6L V8, 400 hp, 7-speed automatic, and 4WD/AWD.
- The current clean row says RWD, which is inconsistent with that local source.
- New global QX80 generations may use 3.5 twin-turbo V6, but do not add a current Israeli row unless repo-local Israeli pricing/importer evidence supports it.

Sources embedded for Codex task:

```text
https://www.cartube.co.il/חדשות-רכב/אינפיניטי-מעדכנת-את-ה-qx80
https://www.infiniti-cars.co.il/
```

Action:

```text
FIX
- Correct drivetrain from RWD to AWD/4WD if local source support is present.
- Keep 5.6L V8 / 400 hp / 7-speed automatic historical row.
- Do not add new 3.5 twin-turbo QX80 current row without strong Israeli source in repo.
```

---

### 15. Isuzu Rodeo — MERGE DUPLICATE SOURCE-SCOPE PROFILES

Current clean state includes two Rodeo profiles:

```text
global-reference-only|Isuzu|Rodeo
- null trim, SUV, petrol, 3.2L V6, 205 hp, 4-speed automatic, 4WD, 1998–2004

IL-confirmed|Isuzu|Rodeo
- null trim, SUV, petrol, 3.2L V6, 205 hp, 4-speed automatic, 4WD, 2002–2004
```

Validated facts:

- Israeli Yad2/Gear price-list sources support Rodeo 3.2L 205 hp automatic 4WD in LS/LSE trims for 2002–2004.
- The 1998–2001 extension appears less strongly grounded from the fetched Israeli sources.
- There must not be two published clean profiles for the same Israeli model due to `global-reference-only` vs `IL-confirmed` source scope.

Sources embedded for Codex task:

```text
https://www.yad2.co.il/price-list/feed?manufacturer=4&model=10067
https://www.gear.co.il/מחירון-רכב-דגם/איסוזו/רודאו/2004/רודאו/3.2-4x4-LSE-גולד-אוטומט-
```

Action:

```text
MERGE / FIX
- Publish one canonical clean profile: `IL-confirmed|Isuzu|Rodeo` or canonical `IL|Isuzu|Rodeo` according to repo convention.
- Merge duplicate source-scope profile into alias/lineage; do not publish `global-reference-only|Isuzu|Rodeo` as separate clean website model.
- Preferred clean rows if supported:
  - LS, SUV, petrol, 3.2L V6, 205 hp, 4-speed automatic, 4WD, 2002–2004.
  - LSE / LSE Gold, same technical configuration, 2002–2004.
- If repo-local evidence supports 1998–2001, preserve with source note; otherwise do not keep unsupported years in clean.
```

---

### 16. Isuzu Trooper — MERGE DUPLICATE SOURCE-SCOPE PROFILES + REMOVE UNSUPPORTED FIRST-GEN ROW

Current clean state includes two Trooper profiles:

```text
IL-likely|Isuzu|Trooper
- 7 variants, including 2.8L diesel 106 hp, 1990–1992
- 3.1L diesel 114 hp, 1993–1998
- 3.2L petrol 177 hp, 1993–1998
- 3.0L diesel 159 hp, 1999–2004
- 3.5L petrol 215 hp, 1999–2004

IL-confirmed|Isuzu|Trooper
- 6 variants, duplicate of the later rows but starting 1992/1999
```

Validated facts:

- Shvilim Israeli buying guide states the first generation did not reach Israel.
- The second generation was sold in Israel in 1995–1998 with 3.1 diesel and 3.2 petrol.
- From 1999 the Trooper received 3.0 diesel 159 hp and 3.5 petrol 215 hp.
- Israeli listing/price-list sources support 3.0 diesel 159 hp manual/automatic and 3.5 petrol 215 hp automatic.
- The 2.8L 1990–1992 row is suspect and should not remain clean unless the repo contains a very strong Israeli source.

Sources embedded for Codex task:

```text
https://shvilim.co.il/isuzu-trooper/
https://www.yad2.co.il/vehicles/cars?manufacturer=4&model=10068
https://www.yad2.co.il/price-list/sub-model/122911/2001
```

Action:

```text
MERGE / FIX / ARCHIVE SUSPECT ROW
- Publish one canonical clean Trooper profile; do not keep both `IL-likely` and `IL-confirmed` as independent clean website models.
- Preserve the old source key as alias/lineage.
- Remove or archive non-blocking the 2.8L diesel 106 hp 1990–1992 row unless a strong Israeli source exists.
- Correct early second-generation year_start to 1995 if no local source supports 1992/1993 Israeli sale.
- Keep supported rows:
  - 3.1L turbo diesel, 114 hp, manual and automatic, 4WD, approx. 1995–1998.
  - 3.2L V6 petrol, 177 hp, 4-speed automatic, 4WD, approx. 1995–1998.
  - 3.0L turbo diesel, 159 hp, manual and automatic, 4WD, 1999–2004.
  - 3.5L V6 petrol, 215 hp, automatic, 4WD, 1999–2004.
- Add trim labels S/LS only if repo-local evidence safely maps them to body/seat/transmission rows.
```

---

## Required post-RUN 3 checks

After applying RUN 3 corrections only:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
```

Report:

```text
RUN 3 RESULT: PASS / PASS WITH WARNINGS / FAIL
files changed
models touched
variants added/fixed/moved/archived
alias/lineage changes
readiness metrics after RUN 3
quality scan bug/leak/structure/normalization counts
unmatched output keys count/sample
tests run
commit hash if committed
remaining risks before RUN 4
```

Do not report success if:

```text
- Rodeo or Trooper still publish duplicate clean profiles from source-scope keys.
- Q50/Q60 keep Israeli 3.0L turbo rows at 300/400 hp when embedded Israeli facts support 405 hp.
- QX50/QX60 remain stale and miss current importer-supported rows.
- Staria diesel remains open/current without current diesel support.
- Venue remains capped at 2024 despite current Hyundai/Auto source support.
- quality scan is not regenerated.
```


---

# BATCH 24 — RUN 4 CODEX TASK

## Scope

Execute **RUN 4 only** for Batch 24.

Baseline from uploaded ZIP 17:

```text
source_cursor = 467/1124
resume_after_key = IL-confirmed|Jeep|Avenger
next_key_to_process = IL-likely|Jeep|Avenger
clean_models = 438
review_only_blocked_entries = 12
active_blocked = 12
unmatched_output_keys_count = 0
split_profile_alias_count = 17
ready_for_website_upload = false
quality_scan_stale = true
```

RUN 4 covers these 17 clean source groups:

```text
IL-confirmed|Isuzu|Trooper
IL-confirmed|Jaecoo|J7
IL-likely|Jaecoo|J7
IL-likely|Jaecoo|J8
IL-confirmed|Jaguar|E-Pace
IL-confirmed|Jaguar|F-Pace
IL-confirmed|Jaguar|F-Type
IL-confirmed|Jaguar|I-Pace
IL-confirmed|Jaguar|S-Type
IL-confirmed|Jaguar|X-Type
IL-likely|Jaguar|X-Type
global-reference-only|Jaguar|X-Type
IL-confirmed|Jaguar|XE
IL-confirmed|Jaguar|XF
IL-likely|Jaguar|XJ
IL-confirmed|Jaguar|XJ
IL-confirmed|Jeep|Avenger
```

Important: execute RUN 4 only. Do **not** continue to the final blockers/review run, and do **not** process `IL-likely|Jeep|Avenger` yet; it is the next source after this window.

Also important: `data/model_technical_catalog_il_quality_scan.json` appears stale relative to the current catalog/review outputs. Always regenerate quality scan after RUN 4 corrections.

---

## RUN 4 correction requirements

### 1. Isuzu Trooper — MERGE IL-likely / IL-confirmed SOURCE-SCOPE DUPLICATES

Current clean profiles include both:

```text
IL-likely|Isuzu|Trooper
IL-confirmed|Isuzu|Trooper
```

Current issue:

- The same Israeli-market model exists as two clean profiles because of source-scope duplication.
- `IL-likely` contains an extra early 2.8L diesel row from 1990–1992.
- `IL-confirmed` contains the better grounded 3.1 / 3.2 / 3.0 / 3.5 rows.

Validated facts:

- Israeli off-road buying-guide evidence strongly supports the later Trooper rows: 3.0L diesel, 159 hp, manual/automatic; and 3.5L petrol, 215 hp, automatic.
- The earlier 3.1L / 3.2L rows are plausible and already supported by repo-local field sources.
- The 2.8L 1990–1992 row is weaker and should not be kept clean unless repo-local evidence is strong.

Sources embedded for Codex task:

```text
https://shvilim.co.il/isuzu-trooper/
https://www.yad2.co.il/price-list/feed?manufacturer=4&model=10067
```

Action:

```text
MERGE / FIX / ARCHIVE IF WEAK
- Keep one canonical clean profile: IL-confirmed|Isuzu|Trooper.
- Add alias/lineage from IL-likely|Isuzu|Trooper to IL-confirmed|Isuzu|Trooper.
- Preserve strongly grounded rows:
  - 3.1L turbo diesel, 114 hp, manual/automatic, 4WD, 1992/1993–1998 per repo-local evidence.
  - 3.2L V6 petrol, 177 hp, 4-speed automatic, 4WD, 1992/1993–1998 per repo-local evidence.
  - 3.0L turbo diesel, 159 hp, manual/automatic, 4WD, 1999–2004.
  - 3.5L V6 petrol, 215 hp, 4-speed automatic, 4WD, 1999–2004.
- Do not keep the 2.8L 1990–1992 row clean unless strong Israeli repo-local source exists; otherwise move it to non-blocking archive with reason `weak_or_insufficient_israeli_evidence`.
- Do not leave both source-scope profiles as clean models.
```

---

### 2. Jaecoo J7 — MERGE IL-confirmed / IL-likely AND ADD PHEV WITHOUT DUPLICATES

Current clean profiles include:

```text
IL-confirmed|Jaecoo|J7
- Executive, 1.6T petrol, 147 hp, 7-speed DCT, FWD, 2024-current
- Titanium, 1.6T petrol, 147 hp, 7-speed DCT, FWD, 2024-current
- Adventure, 1.6T petrol, 147 hp, 7-speed DCT, AWD, 2024-current

IL-likely|Jaecoo|J7
- null trim, 1.6T petrol, 147 hp, FWD, 2024–2025
- null trim, 1.6T petrol, 147 hp, AWD, 2024–2025
- null trim, 1.5T PHEV, 342 hp, automatic, FWD, 2025–2025
```

Current issue:

- Same model appears under `IL-confirmed` and `IL-likely`.
- Petrol rows already exist better as scalar trims in `IL-confirmed`; the `IL-likely` null-trim petrol rows are duplicates.
- PHEV/SHS row is real and current, but must be merged into the canonical J7 profile, not kept as a separate profile.

Validated facts:

- Israeli sources support J7 petrol 1.6T with 147 hp, 7-speed dual-clutch, FWD/AWD.
- Israeli sources support J7 PHEV/SHS added in November 2024: 1.5T plus electric motors, combined 342 hp, 3-speed dedicated hybrid transmission, FWD, 91 km electric range.
- Jaecoo Israel’s current website presents JAECOO 7 as a PHEV and exposes Elegance / Premium / Luxury in the PHEV consumption table.

Sources embedded for Codex task:

```text
https://www.auto.co.il/cars/jaecoo/j7/
https://www.cartube.co.il/חדשות-רכב/פלאג-אין-ג-אקו-7-phev-בישראל-מחיר-18990-שקל
https://jaecoo.co.il/models/jaecoo7/
https://jaecoo.co.il/
```

Action:

```text
MERGE / FIX
- Keep one canonical clean profile: IL-confirmed|Jaecoo|J7.
- Add alias/lineage from IL-likely|Jaecoo|J7 to IL-confirmed|Jaecoo|J7.
- Keep petrol rows as scalar trims only if source-grounded:
  - Executive, 1.6T petrol, 147 hp, 7-speed dual_clutch, FWD, 2024-current.
  - Titanium, 1.6T petrol, 147 hp, 7-speed dual_clutch, FWD, 2024-current.
  - Adventure, 1.6T petrol, 147 hp, 7-speed dual_clutch, AWD, 2024-current.
- Remove/archive duplicated null-trim petrol rows from IL-likely.
- Add/merge J7 PHEV/SHS row(s): 1.5T plug_in_hybrid, 342 hp, 3-speed automatic / dedicated hybrid transmission per schema, FWD, year_start=2024 or 2025 according to repo-local Israeli launch/date evidence, year_end=null/current.
- Use PHEV trims `Elegance`, `Premium`, `Luxury` only if official repo-local Jaecoo source/PDF supports trim-specific rows. If exact trims are not safely grounded, keep one shared PHEV technical row with explicit no-safe-trim note rather than inventing separate trims.
- Do not leave any `IL-likely|Jaecoo|J7` clean profile after merge.
```

---

### 3. Jaecoo J8 — KEEP PHEV CURRENT; ARCHIVE UNSUPPORTED PETROL ROW

Current clean profile:

```text
IL-likely|Jaecoo|J8
- null trim, SUV, petrol, 2.0L turbo, 249 hp, 7-speed dual_clutch, AWD, 2025-current
- null trim, SUV, plug_in_hybrid, 1.5L turbo, 608 hp, 3-speed automatic, AWD, 2025-current
```

Current issue:

- Israeli current evidence found for J8 is PHEV-focused.
- The 2.0T petrol 249 hp row looks like global leakage unless repo-local Israeli source supports it.
- `IL-likely` should be promoted to canonical only if it is truly Israeli-market backed; otherwise it needs alias/source-scope handling.

Validated facts:

- Jaecoo Israel presents JAECOO 8 as a 7-seat PHEV.
- Auto Israel describes J8 as marketed in Israel as a 7-seat AWD PHEV beginning around late 2025 / model year 2026.

Sources embedded for Codex task:

```text
https://jaecoo.co.il/models/jaecoo8/
https://www.auto.co.il/cars/jaecoo/j8/
https://jaecoo.co.il/
```

Action:

```text
FIX / ARCHIVE WEAK ROW
- Keep/promote canonical clean J8 only if repo-local evidence confirms Israeli sale.
- Preserve the 1.5T PHEV AWD row with 608 hp, 3-speed automatic, 7 seats, year_start=2025 or 2026 per source evidence, year_end=null/current.
- Add scalar trim such as `Luxury` only if source-supported.
- Do not keep the 2.0T petrol 249 hp row clean unless a strong Israeli source exists in the repo; otherwise move that row to non-blocking archive with reason `global_reference_only` or `weak_or_insufficient_israeli_evidence`.
- If source-scope is upgraded from `IL-likely` to `IL-confirmed`, preserve alias/lineage from the old key.
```

---

### 4. Jaguar E-Pace — KEEP CURRENT PHEV/MHEV ONLY IF LOCAL CURRENT SOURCE SUPPORTS; DO NOT OVEREXTEND OLD ROWS

Current clean profile includes historical petrol/diesel rows and 2021–2026 mild-hybrid/PHEV rows:

```text
E-Pace
- 2018–2020 petrol/diesel rows
- 2021–2026 mild_hybrid 2.0L 200 hp AWD
- 2021–2026 PHEV 1.5L 309 hp AWD
```

Validated facts:

- Jaguar Israel still has an E-PACE page and specifically refers to E-PACE Plug-in Hybrid with EV range.
- Israeli secondary sources also list 2026 E-Pace 1.5 S.
- Cartube’s facelift article supports the 2021 platform/PHEV change and 309 hp.

Sources embedded for Codex task:

```text
https://www.jaguar.co.il/jaguar-range/e-pace/overview
https://www.cartube.co.il/חדשות-רכב/מתיחת-פנים-2021-יגואר-e-pace-החדש-נחשף
https://www.cmotors.co.il/cars/jaguar/e-pace/
```

Action:

```text
KEEP / FIX SUPPORT
- Keep historical 2018–2020 rows closed.
- Keep 2021+ PHEV 1.5L 309 hp row if field sources support it; set current/open-ended only if repo-local current source supports active sale.
- Keep 2021+ MHEV/P200 row only if repo-local source supports Israeli sale; otherwise cap/archive weak current extension.
- Do not keep `year_end=2026` mechanically if project convention uses null for current; use either null/current or exact 2026 according to catalog convention and source evidence.
- If all non-empty fields are grounded, set support_level direct; do not leave false `indirect` quality bug.
```

---

### 5. Jaguar F-Pace — FIX CURRENT STATUS/TRIMS; DO NOT HIDE P250/P400e/SVR DIFFERENCES

Current clean profile includes 2016–2024 rows:

```text
F-Pace
- 2.0 diesel 180, AWD, 2016–2020
- 2.0 petrol 250, AWD, 2017–2024
- 2.0 PHEV 404, AWD, 2021–2024
- 5.0 V8 supercharged 550, AWD, 2019–2024
```

Validated facts:

- Israeli Auto source describes F-Pace after facelift as offered locally in P250 and P400e/PHEV versions, with 250 hp and 404 hp, AWD and 8-speed automatic.
- Israeli price-list evidence shows 2024 F-Pace trims such as SE / R-Dynamic / S Plus for P250 and P400e.
- Jaguar Israel has an F-PACE SVR 575 Edition page; if keeping a late SVR row, avoid leaving a stale 550 hp row as if it represents the current 575 Edition.

Sources embedded for Codex task:

```text
https://www.auto.co.il/cars/jaguar/f-pace/
https://www.yad2.co.il/price-list/feed?manufacturer=20&model=10249
https://www.jaguar.co.il/about-jaguar/special-vehicle-operations/f-pace-svr-575-edition
```

Action:

```text
FIX / KEEP WITH SOURCE CHECK
- Keep historical diesel 180 row closed to 2020.
- Keep P250 2.0 petrol 250 hp AWD and P400e/PHEV 404 hp AWD with year_end/current status based on repo-local 2024/2026 evidence.
- Add trim context such as SE / R-Dynamic / S Plus only if exact source supports it.
- If an SVR row is retained for late/current years, correct/replace 550 hp with 575 Edition only where source-supported; otherwise cap 550 hp to the years it is supported and do not mark as current.
- Do not create duplicate P400e rows that differ only by source wording.
```

---

### 6. Jaguar F-Type — KEEP 2.0 300 CURRENT-TO-2024; CAP UNSUPPORTED OLD ENGINES

Current clean profile contains several coupe/convertible variants with 2.0, 3.0 V6, and 5.0 V8 rows.

Validated facts:

- Auto Israel’s 2024 F-Type page lists the 2.0 turbo automatic coupe and convertible as the local 2024 versions and states marketing ended.
- Gear/Yad2 price-list evidence supports 2.0 turbo 300 hp in 2024.
- Older V6/V8 rows are real historically, but should not be open/current unless source-supported.

Sources embedded for Codex task:

```text
https://www.auto.co.il/cars/jaguar/f-type/
https://www.gear.co.il/מחירון-רכב-דגם/יגואר/F-TYPE/2024-חדש/F-TYPE/2.0-טורבו-300hp-פרימיום-אוטומט-
https://www.yad2.co.il/price-list/feed?manufacturer=20&model=10250
```

Action:

```text
FIX / KEEP
- Keep 2.0L turbo 300 hp, 8-speed automatic, RWD, Coupe and Convertible rows through 2024.
- Do not extend F-Type beyond 2024 unless repo-local official/current source proves sale.
- Cap 3.0 V6 and 5.0 V8 rows to the exact supported years; do not keep them as current or generic through 2024 unless source proves that exact row.
- Add scalar designation such as Coupe / Convertible body_type and, where supported, R-Dynamic / R, but do not invent trims.
```

---

### 7. Jaguar I-Pace — FIX SUPPORT LEVEL; KEEP EV400 400 HP AWD

Current clean profile:

```text
I-Pace
- EV400, SUV, electric, 400 hp, single_speed, AWD, 2018–2025, support_level=indirect
```

Validated facts:

- Jaguar Israel has an I-PACE page and warranty text for 90kWh battery.
- Auto Israel describes the facelifted I-Pace as two electric motors, 400 hp, AWD, 90 kWh battery, 425 km range.

Sources embedded for Codex task:

```text
https://www.jaguar.co.il/jaguar-range/i-pace/overview
https://www.auto.co.il/cars/jaguar/i-pace/
```

Action:

```text
KEEP / FIX SUPPORT
- Keep EV400, electric, 400 hp, single_speed, AWD.
- If all non-empty fields have field-source support, change support_level from indirect to direct and clear quality false positive.
- Keep year_end according to project convention/current source: either 2025 if only 2025 is source-backed, or null/current if official source proves active sale.
```

---

### 8. Jaguar S-Type — FIX HP ROUNDING AND ADD/KEEP R ONLY IF SOURCE-SUPPORTED

Current clean profile includes 1999–2007 rows:

```text
S-Type
- 3.0 V6, 240 hp, 1999–2002
- 4.0 V8, 281 hp, 1999–2002
- 2.5 V6, 200 hp, 2002–2007
- 3.0 V6, 240 hp, 2002–2007
- 4.2 V8, 300 hp, 2002–2007
```

Validated facts:

- Yad2 Israel price list supports S-Type 2.5 around 201 hp, 3.0 at 240 hp, 4.2 at 300 hp, and R 4.2 around 400 hp.
- Autoboom Israel also lists 2.5/200, 3.0/238, 4.2/298, 4.2/395 in its on-road data, but this is secondary and slightly rounded.

Sources embedded for Codex task:

```text
https://www.yad2.co.il/price-list/feed?manufacturer=20&model=10253
https://autoboom.co.il/en/catalog/cars/jaguar/s-type
```

Action:

```text
KEEP / FIX WITH ISRAELI SOURCE PREFERENCE
- Prefer Israeli Yad2/Gear-style rounded hp values where catalog convention uses Israeli price-list values:
  - 2.5 V6: 200/201 hp acceptable only if consistent with project convention; do not create duplicate 200 and 201 rows.
  - 3.0 V6: 240 hp.
  - 4.2 V8: 300 hp.
  - S-Type R 4.2: 400 hp only if source-grounded; add as separate row only if repo-local source supports it.
- Keep historical only; no current/open-ended rows.
- Do not keep 4.0/281 row clean unless source-local evidence supports the pre-facelift 4.0 row. If not supported, archive or cap with source note.
```

---

### 9. Jaguar X-Type — MERGE IL-confirmed / IL-likely / global-reference-only; KEEP ONLY ISRAELI-BACKED ROWS

Current clean profiles include three source scopes:

```text
IL-confirmed|Jaguar|X-Type
IL-likely|Jaguar|X-Type
global-reference-only|Jaguar|X-Type
```

Current issue:

- Same model is duplicated across source scopes.
- `global-reference-only` includes an Estate row; this should not be clean unless Israeli source supports it.
- The `IL-confirmed` profile is missing the 3.0L row that appears in the other sources and Israeli price lists.
- A 2.1L FWD row conflicts with Israeli iCar statement that versions sold in Israel had AWD; keep only if source-grounded.

Validated facts:

- Yad2/Gear Israeli sources support X-Type 2.5 V6 194 hp and 3.0 V6 231 hp, with Sport/Executive/SE trims.
- iCar’s Israeli overview states X-Type was sold in Israel 2001–2009 and says versions sold locally had AWD.

Sources embedded for Codex task:

```text
https://www.yad2.co.il/price-list/feed?manufacturer=20&model=10258
https://www.icar.co.il/יגואר/יגואר_X-TYPE/יגואר_X-TYPE_יד_שניה_ד10/
https://www.gear.co.il/דגם/יגואר/X-TYPE/2005/X-TYPE
```

Action:

```text
MERGE / FIX / ARCHIVE GLOBAL-ONLY
- Keep one canonical clean profile: IL-confirmed|Jaguar|X-Type.
- Add aliases/lineage from:
  - IL-likely|Jaguar|X-Type
  - global-reference-only|Jaguar|X-Type
- Retain source-backed Israeli rows:
  - 2.5L V6, 194 hp, automatic, AWD, 2001/2002–2009.
  - 3.0L V6, 231 hp, automatic, AWD, 2001/2002–2009.
- Add trim context such as Sport / Executive / SE only if exact source and project convention support separate trim rows; otherwise keep technical rows without unsafe trim over-splitting.
- Do not keep the Estate row clean unless repo-local Israeli evidence supports Estate sale.
- Do not keep 2.1L FWD clean unless strong repo-local source proves Israeli sale; otherwise archive as weak/global leakage.
- Do not leave multiple X-Type clean profiles.
```

---

### 10. Jaguar XE — KEEP LOCAL POWERTRAIN HISTORY; DO NOT OVEREXTEND CURRENT

Current clean profile:

```text
XE
- 2.0T 200 hp, RWD, 2015–2018
- 2.0T 240 hp, RWD, 2015–2018
- 3.0 supercharged V6 340 hp, RWD, 2015–2018
- 2.0T 250 hp, RWD, 2018–2024
```

Validated facts:

- Auto Israel states XE was marketed locally with 2.0T 200/240 hp and 3.0 supercharged V6 340 hp; after the 2019 facelift the 240 hp engine rose to 250 hp.
- XE global production ended around 2024, so do not open current unless local official source says otherwise.

Sources embedded for Codex task:

```text
https://www.auto.co.il/cars/jaguar/xe/
https://www.jaguar.co.il/jaguar-range/xe/overview
```

Action:

```text
KEEP
- Current technical rows are broadly correct.
- Keep 2015–2018 200/240/340 rows and 2018/2019–2024 250 row if source-backed.
- Add trim labels only if source-local evidence supports exact scalar labels.
- Do not add 300 hp / AWD / Project 8 or global variants unless Israeli source exists.
- Do not open current beyond 2024.
```

---

### 11. Jaguar XF — ENRICH HISTORY; KEEP/CAP CURRENT CAREFULLY

Current clean profile:

```text
XF
- 3.0 V6 238 hp, 6-speed auto, RWD, 2008–2012
- 2.0T 240 hp, 8-speed auto, RWD, 2012–2017
- Prestige diesel 2.0 180 hp, 2016–2020
- Prestige petrol 2.0 250 hp, 2018–2024
```

Validated facts:

- Israeli price-list evidence supports XF rows with 2.0T 200/240/250, 2.0 diesel 180, and S 3.0 380 around 2016–2017.
- Auto/Jaguar sources show XF as a known local model but do not justify blind current/open-ended status.

Sources embedded for Codex task:

```text
https://www.yad2.co.il/price-list/feed?manufacturer=20&model=10255
https://www.auto.co.il/cars/jaguar/xf/
https://www.gear.co.il/מחירון-רכב-דגם/יגואר/XF/2017/XF/S-3.0-V6-מגדש-על-אוטומט-
```

Action:

```text
KEEP / FIX
- Keep existing 2008–2024 rows if grounded.
- Add/correct missing 2.0T 200 hp and S 3.0 supercharged V6 380 hp rows only if repo-local source supports them.
- Keep `Prestige` trim only where exact source supports it.
- Do not open current beyond 2024 without strong local source.
- Avoid duplicates where 240/250 rows overlap due facelift transition.
```

---

### 12. Jaguar XJ — MERGE IL-likely / IL-confirmed AND FIX HP VALUES

Current clean profiles include:

```text
IL-likely|Jaguar|XJ
- 1990–1997 older inline-6 rows

IL-confirmed|Jaguar|XJ
- 1997–2019 rows, including 2.0T 240, 3.0 SC 340, 3.0 V6 238, 4.2 V8 298, 3.2 V8 237
```

Current issue:

- XJ is split across `IL-likely` and `IL-confirmed` scopes.
- Some hp values use global/raw values while Israeli price lists use rounded local values: 3.0 240, 4.2 300, R 400.
- Newer 2010–2018 XJ rows may need trim/context like Luxury / Premium Luxury / SWB / LWB if source supports them.

Validated facts:

- Yad2 Israeli price-list evidence supports XJ 3.0 at 240 hp, 4.2 at 300 hp, R 4.2 at 400 hp, and 3.5/3.6 at 262 hp for some years.
- iCar source supports 2010–2018 XJ trims such as Luxury SWB 2.0 and Premium Luxury SWB/LWB 3.0.

Sources embedded for Codex task:

```text
https://www.yad2.co.il/price-list/feed?manufacturer=20&model=10256
https://www.icar.co.il/יגואר/יגואר_XJ/יגואר_XJ_יד_שניה_ד11/
```

Action:

```text
MERGE / FIX
- Keep one canonical clean profile: IL-confirmed|Jaguar|XJ.
- Add alias/lineage from IL-likely|Jaguar|XJ.
- Preserve older 1990–1997 rows only if repo-local Israeli evidence supports them; otherwise archive weak early rows.
- Correct local hp values where project convention prefers Israeli price-list values:
  - 3.0 V6: 240 hp, not 238, when aligned to local price-list rows.
  - 4.2 V8: 300 hp, not 298, when aligned to local price-list rows.
  - R 4.2: 400 hp if source-backed.
- Preserve 2010–2018/2019 rows such as 2.0T 240 and 3.0 supercharged 340 if source-backed.
- Add SWB/LWB/Luxury/Premium Luxury trim/body-length context only if exact source supports it; do not invent.
- Do not leave both IL-likely and IL-confirmed clean profiles.
```

---

### 13. Jeep Avenger — FIX CURRENT E-HYBRID STATUS; DO NOT PROCESS NEXT `IL-likely|Jeep|Avenger`

Current clean profile:

```text
IL-confirmed|Jeep|Avenger
- Altitude, petrol, 1.2L turbo, 100 hp, 6-speed manual, FWD, 2023–2024
- Altitude, mild_hybrid, 1.2L turbo, 100 hp, 6-speed dual_clutch, FWD, 2024–2024
```

Current issue:

- Jeep Israel’s current Avenger page presents the model as now available in a mild-hybrid/e-Hybrid version.
- Existing e-Hybrid row ending in 2024 is likely too closed if repo-local current source supports active sale.
- The next unprocessed source after this window is `IL-likely|Jeep|Avenger`; do not process it in RUN 4, but make sure RUN 4 changes do not create cursor confusion.

Validated facts:

- Jeep Israel official Avenger page says Avenger is now in a mild-hybrid version and lists 1200 cc, petrol engine, 100 hp.
- Autocom Israel launch article states Avenger e-Hybrid uses a 100 hp petrol engine plus 28 hp electric motor with 6-speed e-DCT.
- EV/global electric Avenger is real globally, but do not add a clean Israeli electric row in RUN 4 unless repo-local Israeli evidence exists in this source group.

Sources embedded for Codex task:

```text
https://www.jeep.com/il/avenger.html
https://www.autocom.co.il/גיפ-avenger-e-hybrid-היברידי-חדש-בישראל/
https://www.carzone.co.il/Jeep/Avenger/
```

Action:

```text
FIX / KEEP CURRENT
- Keep historical 1.2L petrol manual row only for source-supported years; do not open it current unless source supports ongoing manual petrol sale.
- Set Avenger e-Hybrid / mild_hybrid 1.2L 100 hp, 6-speed dual_clutch/e-DCT, FWD to year_end=null/current if repo-local Jeep Israel source supports active sale.
- Keep `Altitude` only if source/PDF supports the trim; otherwise use null trim with no-safe-trim note or source-supported trim.
- Do not add the fully electric Avenger row unless this RUN 4 source group contains strong Israeli evidence. The `IL-likely|Jeep|Avenger` source is next and should be handled in a later batch/window if needed.
- Ensure cursor remains `resume_after_key = IL-confirmed|Jeep|Avenger`, `next_key_to_process = IL-likely|Jeep|Avenger` after RUN 4.
```

---

## RUN 4 non-negotiable checks

```text
- No duplicate clean profiles across IL-confirmed / IL-likely / global-reference-only for the same make/model.
- Jaecoo J7 must not remain as both IL-confirmed and IL-likely clean profiles.
- Jaguar X-Type must not remain as three clean profiles.
- Jaguar XJ must not remain as two clean profiles.
- Isuzu Trooper must not remain as two clean profiles.
- Jeep Avenger must not accidentally consume/process IL-likely|Jeep|Avenger in RUN 4.
- All archive records created in RUN 4 must have non_blocking=true, batch_id=BATCH24, reason, and lineage/canonical target where applicable.
- Regenerate readiness, review, archive, and quality scan after corrections.
- Quality scan bug and normalization findings caused by RUN 4 should be zero after regeneration.
```

## Expected status after RUN 4 only

RUN 4 does not need to clear the 12 final blockers. They are reserved for FINAL RUN.

After RUN 4 only:

```text
review_only_blocked_entries may still be 12
active_blocked may still be 12
unmatched_output_keys_count must stay 0
RUN 4 source-scope duplicates should be merged/aliased or archived non-blocking
quality_scan should be regenerated and not stale
```

Do not report full Batch 24 success yet; this is RUN 4 only.

## Required commands after applying RUN 4

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


---
---

# BATCH 24 — FINAL BLOCKERS / REVIEW / IDENTITY CODEX TASK

## Scope

Execute the **FINAL RUN only** for Batch 24.

This task handles:

```text
12 active review-only blockers
+ identity / casing / source-scope cleanup
+ archive non-blocking handling
+ final readiness / cursor safety checks
```

Baseline from uploaded ZIP 17:

```text
source_cursor = 467/1124
resume_after_key = IL-confirmed|Jeep|Avenger
next_key_to_process = IL-likely|Jeep|Avenger
clean_models = 438
review_only_blocked_entries = 12
active_blocked = 12
unmatched_output_keys_count = 0
split_profile_alias_count = 17
ready_for_website_upload = false
quality_scan_stale = true
```

Important:

- Do **not** browse the internet.
- All web validation facts and target corrections are embedded below.
- Use repo-local evidence plus this task file only.
- If a row is not backed by strong Israeli-market evidence, do **not** fabricate it. Move it to `data/model_technical_catalog_il_archive.json` as `non_blocking=true` with reason and lineage.
- Regenerate readiness, review, archive, and quality scan after applying corrections.
- Keep `unmatched_output_keys_count = 0`.
- Do not process beyond the Batch 24 window. `IL-likely|Jeep|Avenger` is the next source after the current cursor window and must remain the next source unless it is already represented only as an alias/source-scope duplicate of the already processed Avenger.

Expected final cursor after Batch 24:

```text
resume_after_key = IL-confirmed|Jeep|Avenger
next_key_to_process = IL-likely|Jeep|Avenger
```

If the cursor regresses or incorrectly advances past `IL-likely|Jeep|Avenger`, fix it before reporting success.

---

## Final blockers to resolve

Current active review-only blockers:

```text
IL|Honda|e:Ny1
IL|Honda|FR-V
IL|Honda|odyssey
IL|Honda|Stream
IL|Hyundai|i30 CW
IL|Hyundai|Ioniq
IL|Hyundai|Kona
IL|Hyundai|Trajet
IL|Hyundai|Tucson
IL|Isuzu|D-Max
global-reference-only|Isuzu|MU-X
IL-likely|Jaguar|S-Type
```

---

# FINAL correction requirements

## 1. Honda e:Ny1 — MOVE TO ARCHIVE unless repo-local official Israeli evidence exists

Current review issue:

- Review profile has one row: `Advance`, SUV, electric, 204 hp, `single_speed`, FWD, 2024–2024.
- `version_or_trim` and `transmission` are missing field-source grounding.
- Notes already say no official Israeli importer model/spec page was found; evidence is parallel import / editorial only.

Validated facts embedded for this task:

- Israeli market coverage found is parallel-import/editorial, not official importer sales evidence.
- Available technical reference supports a single electric motor, 204 hp, FWD, and 68.8 kWh battery, but not strong official Israeli trim grounding.
- Honda Cars Israel homepage alone is not a model-level technical source.

Embedded source URLs:

```text
https://wheel.co.il/יבוא-מקביל-הונדה-eny1-החשמלית-נחתה-בישראל/
https://www.auto.co.il/articles/car-news/world-news/136188/
https://autoboom.co.il/en/catalog/cars/honda/eny1
https://hondacars.co.il/
```

Action:

- Do not promote `Honda e:Ny1` to verified clean based only on parallel-import/editorial evidence.
- Move to non-blocking archive unless repo-local evidence contains an official Israeli importer model/spec page with exact trim and transmission support.
- Archive record should preserve technical reference row:

```json
{
  "make": "Honda",
  "model": "e:Ny1",
  "reason": "parallel_import_or_insufficient_official_israeli_evidence",
  "non_blocking": true,
  "batch_id": "BATCH24",
  "lineage": ["IL|Honda|e:Ny1"],
  "technical_reference": {
    "body_type": "SUV",
    "fuel_type": "electric",
    "engine": "electric",
    "horsepower_hp": 204,
    "transmission": "single_speed",
    "drivetrain": "FWD",
    "year_start": 2024,
    "year_end": 2024
  }
}
```

Action tag: `MOVE TO ARCHIVE` unless official repo-local evidence exists.

---

## 2. Honda FR-V — FIX drivetrain and move to clean

Current review issue:

- Three rows exist: `Trend`, `Comfort`, `Executive`.
- All are 1.8L petrol, 140 hp, automatic, 2007–2010.
- All are blocked only because `drivetrain` is null / missing grounded field.

Validated facts embedded for this task:

- iCar Israeli page for Honda FR-V 2007 1.8 Executive lists the Israeli trims `Trend`, `Comfort`, `Executive` and states front-wheel drive (`הנעה קדמית`).
- Honda FR-V is a compact MPV / six-seat MPV; 1.8L 140 hp automatic is consistent with Israeli-market rows.

Embedded source URLs:

```text
https://www.icar.co.il/הונדה/הונדה_FR-V/הונדה_FR-V_יד_שניה_ד10/version381/
https://autoboom.co.il/en/catalog/cars/honda/fr-v
```

Action:

- Set `drivetrain = "FWD"` for all Honda FR-V rows.
- Add field-source support for drivetrain from the iCar source.
- Keep rows:

```text
Honda FR-V | Trend     | MPV | petrol | 1.8L | 140 hp | automatic | FWD | 2007–2010
Honda FR-V | Comfort   | MPV | petrol | 1.8L | 140 hp | automatic | FWD | 2007–2010
Honda FR-V | Executive | MPV | petrol | 1.8L | 140 hp | automatic | FWD | 2007–2010
```

- Move profile from review to clean.

Action tag: `FIX / KEEP`.

---

## 3. Honda Odyssey — FIX or ARCHIVE unsupported 1999–2004 row

Current review issue:

- Profile contains multiple rows, most already grounded.
- One 1999–2004 3.5L V6 automatic FWD row has `horsepower_hp = null` and blocks readiness.

Current review rows:

```text
2018–2020 | 3.5L V6 | 280 hp | automatic | FWD
2011–2017 | 3.5L V6 | 248 hp | automatic | FWD
2005–2010 | 3.5L V6 | 244 hp | automatic | FWD
1999–2004 | 3.5L V6 | hp null | automatic | FWD
2013–2020 | 2.4L i4 | 175 hp | CVT | FWD
```

Validated facts embedded for this task:

- Global sources show 1999–2004 Odyssey 3.5L V6 around 240/243 hp, but this is not strong enough by itself for verified Israeli clean if repo-local Israeli source does not support it.
- Existing review source list includes KML pages for 1999–2004; if that page directly grounds horsepower, use the repo-local KML value.
- If no repo-local Israeli source supports horsepower for the 1999–2004 row, do not guess from global sources.

Embedded source URLs:

```text
https://www.auto.co.il/model/honda-odyssey
https://www.kml.co.il/car/honda/odyssey/1999-2004
https://www.edmunds.com/honda/odyssey/2004/minivan/st-100347230/features-specs/
https://www.auto-data.net/en/honda-odyssey-ii-3.5-i-v6-ls-243hp-12390
```

Action:

- If repo-local KML/Israeli source directly supports horsepower for the 1999–2004 row, set the exact Israeli-supported horsepower and add field source.
- If not, move only the 1999–2004 row to archive non-blocking with reason `missing_required_field_grounding`.
- Keep the other grounded Odyssey rows clean if source/field-source grounding is valid.
- Do not leave any clean row with `horsepower_hp = null`.

Action tag: `FIX IF GROUNDED / PARTIAL ARCHIVE`.

---

## 4. Honda Stream — RECOVER from empty profile using Israeli price-list evidence, or archive if repo-local evidence is absent

Current review issue:

- `technical_variants_il` is empty.

Validated facts embedded for this task:

- Israeli price-list evidence exists for Honda Stream in Israel, especially 2001–2005 rows with 2.0L petrol, 156 hp, automatic, MPV/minivan 6–7 seats.
- Yad2 Israeli price list shows sub-trims/labels including `I`, `II`, `III`, and `1A`, generally with 2.0 automatic 156 hp.
- Gear Israeli page shows `2.0 ES automatic` for 2003.

Embedded source URLs:

```text
https://www.yad2.co.il/price-list/feed?manufacturer=17&model=10195
https://www.yad2.co.il/price-list/feed?manufacturer=17&max-year=2005&min-year=2005&model=10195
https://www.gear.co.il/מחירון-רכב-דגם/הונדה/סטרים/2003/סטרים/2.0-ES-אוטומט-
```

Action:

- Recover a conservative clean profile only if repo-local sources can support source indexes/field sources.
- Minimum safe clean technical row set:

```text
Honda Stream | 2.0 I    | MPV | petrol | 2.0L | 156 hp | automatic | FWD/null only if FWD not grounded | 2001–2005
Honda Stream | 2.0 II   | MPV | petrol | 2.0L | 156 hp | automatic | FWD/null only if FWD not grounded | 2001–2004/2005 if grounded
Honda Stream | 2.0 III  | MPV | petrol | 2.0L | 156 hp | automatic | FWD/null only if FWD not grounded | 2004–2005 if grounded
Honda Stream | 2.0 1A   | MPV | petrol | 2.0L | 156 hp | automatic | FWD/null only if FWD not grounded | 2002–2005 if grounded
Honda Stream | 2.0 ES   | MPV | petrol | 2.0L | 156 hp | automatic | FWD/null only if FWD not grounded | 2003 if grounded
```

- If `drivetrain` is required and no Israeli source grounds FWD, either add a repo-local source that grounds FWD or archive rather than leaving active blocker.
- Do not fabricate 1.7/125 hp Israeli rows unless repo-local Israeli evidence supports them.
- If exact trim/year splits cannot be grounded safely, archive as non-blocking rather than publishing weak clean rows.

Action tag: `RECOVER IF GROUNDED / ARCHIVE`.

---

## 5. Hyundai i30 CW — FIX missing source_indexes / field_sources and move to clean

Current review issue:

- Three rows are technically plausible but have no `source_indexes`, despite source list containing iCar/Auto pages.

Rows:

```text
2009–2012 | Estate | petrol | 1.6L | 126 hp | 4-speed automatic | FWD
2009–2011 | Estate | petrol | 2.0L | 143 hp | 4-speed automatic | FWD
2012–2017 | Estate | petrol | 1.6L | 135 hp | 6-speed automatic | FWD
```

Validated facts embedded for this task:

- iCar and Auto source pages in the review profile are local Israeli pages for i30 CW / i30 station wagon generations.
- The blocker is structural/source-linking, not necessarily bad technical data.

Embedded source URLs from review profile:

```text
https://www.icar.co.il/יונדאי/יונדאי_i30_סטיישן_CW/
https://www.auto.co.il/model/hyundai-i30cw_g228
```

Action:

- Attach valid `source_indexes` from the existing source list to each row.
- Populate field_sources for body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, years where supported.
- Keep only rows directly supported by existing source list.
- If any row cannot be source-linked, archive that row non-blocking, but do not keep the whole model blocked.

Action tag: `FIX SOURCE REFERENCES`.

---

## 6. Hyundai Ioniq — RECOVER hybrid/electric from empty profile

Current review issue:

- `technical_variants_il` is empty.

Validated facts embedded for this task:

- Israeli sources support Hyundai Ioniq 2017–2022 hybrid: 1.6L petrol + electric, combined 141 hp, FWD, 6-speed DCT / dual-clutch automatic.
- Auto states the Ioniq hybrid was marketed in Israel, was successful in fleets, and stopped marketing during 2022.
- Auto also states facelift-era electric Ioniq had 38.3 kWh battery and 136 hp; hybrid had 141 hp and there was no plug-in version in Israel.
- iCar supports 2022 Ioniq 1.6 hybrid Premium.

Embedded source URLs:

```text
https://www.icar.co.il/יונדאי/יונדאי_איוניק/יונדאי_איוניק_יד_שניה_ד10/
https://www.auto.co.il/cars/hyundai/ioniq/
https://www.auto.co.il/articles/car-news/industry/134891/
https://www.icar.co.il/יונדאי/יונדאי_איוניק/יונדאי_איוניק_יד_שניה_ד10/version24591/
```

Action:

- Recover safe clean rows:

```text
Hyundai Ioniq | hybrid   | Sedan/Hatchback/Liftback per schema | hybrid   | 1.6L hybrid | 141 hp | 6-speed dual-clutch automatic/DCT | FWD | 2017–2022
Hyundai Ioniq | electric | Sedan/Hatchback/Liftback per schema | electric | electric    | 136 hp | single_speed/direct_drive          | FWD | 2019–2022 if repo-local evidence supports
```

- Keep trims such as Premium only if source-level support exists; otherwise use null trim with note if schema allows, or archive if trim required.
- Do **not** add Ioniq plug-in hybrid; Auto states PHEV did not reach Israel.

Action tag: `RECOVER`.

---

## 7. Hyundai Kona — RECOVER from empty profile with current/historical splits

Current review issue:

- `technical_variants_il` is empty.

Validated facts embedded for this task:

- Hyundai Israel currently sells Kona Hybrid in 2026.
- Auto says Kona Hybrid 2026 output was reduced from 141 hp to 129 hp.
- Hyundai Israel official page and Auto page support current Kona Hybrid presence.
- Kona also has historical petrol/electric lines in Israel, but exact clean rows must be repo-local grounded.

Embedded source URLs:

```text
https://www.hyundaimotors.co.il/models/kona-hybrid
https://www.auto.co.il/cars/hyundai/kona/
https://www.icar.co.il/יונדאי/יונדאי_קונה/יונדאי_קונה_חדש/
```

Action:

- Recover current Kona Hybrid as a clean profile if repo-local sources can support fields:

```text
Hyundai Kona | hybrid | SUV/Crossover | hybrid | 1.6L hybrid | 129 hp | automatic/DCT as supported | FWD | 2026–current
```

- If repo-local evidence supports earlier 141 hp hybrid years, split:

```text
Hyundai Kona | hybrid | ... | 141 hp | ... | historical years up to 2025
Hyundai Kona | hybrid | ... | 129 hp | ... | 2026–current
```

- Add petrol/electric rows only if source/field-source support exists inside repo or embedded sources.
- Do not leave empty profile active; recover grounded rows or archive uncertain rows non-blocking.

Action tag: `RECOVER`.

---

## 8. Hyundai Trajet — RECOVER from empty profile or archive weak rows

Current review issue:

- `technical_variants_il` is empty.

Validated facts embedded for this task:

- Israeli catalog/reference evidence supports Trajet in Israel with rows such as 2.0 diesel 113 hp FWD, 2.0 petrol 136 hp FWD, and 2.7 petrol 173 hp FWD.
- Global sources support that Trajet was a 7-seat MPV produced 1999–2008 with 2.0 petrol/diesel and 2.7 V6 options.

Embedded source URLs:

```text
https://autoboom.co.il/en/catalog/cars/hyundai/trajet/1-generation/compact-van/21398
https://en.wikipedia.org/wiki/Hyundai_Trajet
```

Action:

- Recover only source-backed Israeli rows, likely:

```text
Hyundai Trajet | MPV | diesel | 2.0L | 113 hp | automatic | FWD | grounded years
Hyundai Trajet | MPV | petrol | 2.0L | 136 hp | automatic/manual if grounded | FWD | grounded years
Hyundai Trajet | MPV | petrol | 2.7L V6 | 173 hp | automatic | FWD | grounded years
```

- If only Autoboom/global reference exists and no repo-local Israeli source can support exact fields, move the model to archive non-blocking with technical reference rows, not active review.

Action tag: `RECOVER IF GROUNDED / ARCHIVE`.

---

## 9. Hyundai Tucson — RECOVER from empty profile with Israeli official current hybrid line

Current review issue:

- `technical_variants_il` is empty.

Validated facts embedded for this task:

- Hyundai Israel official page currently lists Tucson Hybrid.
- Hyundai Israel 2025 hybrid guide states Tucson Hybrid uses 1.6L turbo petrol hybrid with 230 hp and 4X4.
- Hyundai current page/pricing supports active 2026 Tucson Hybrid presence.

Embedded source URLs:

```text
https://www.hyundaimotors.co.il/models/tucson-hybrid
https://www.hyundaimotors.co.il/article/hybrid-cars-2025-guide
```

Action:

- Recover at minimum the current official hybrid line:

```text
Hyundai Tucson | Pure/Prestige/etc only if source-backed | SUV | hybrid | 1.6L turbo hybrid | 230 hp or exact source-supported value | automatic | 4WD/AWD if source-supported | current/open-ended
```

- If current price list/source supports 2026 trims, split trims accordingly.
- Historical petrol/diesel/hybrid Tucson rows should be added only if exact repo-local evidence exists.
- Do not leave empty profile active.

Action tag: `RECOVER`.

---

## 10. Isuzu D-Max — FIX missing drivetrain on one historical row

Current review issue:

- D-Max profile has multiple good rows.
- One 2007–2012 3.0L turbo diesel 163 hp automatic row has missing drivetrain field-source grounding.

Validated facts embedded for this task:

- Auto / Israeli page confirms 2007 D-Max 3.0 4X4 163 hp.
- Autoboom and Auto-Data technical reference support first-generation/restyling D-Max 3.0 TD 163 hp 4WD/AWD.

Embedded source URLs:

```text
https://www.auto.co.il/cars/isuzu/dmax/2007/517431/
https://autoboom.co.il/en/catalog/cars/isuzu/d-max/1-generation-restyling/pickup-double-cab/21930
https://www.auto-data.net/en/isuzu-d-max-i-3.0-td-single-cab-163hp-4wd-15979
https://www.isuzu.co.il/
```

Action:

- Set drivetrain for the 2007–2012 3.0L 163 hp automatic row to `4WD` / canonical AWD/4WD value used by the project.
- Add field source for drivetrain from existing source list if available, or add repo-local/source metadata from embedded Israeli Auto page.
- Keep the other D-Max rows.
- Move profile to clean.

Action tag: `FIX`.

---

## 11. Isuzu MU-X — ARCHIVE global-reference-only

Current review issue:

- Source key is `global-reference-only|Isuzu|MU-X`.
- `technical_variants_il` is empty.
- Sources are world-news/editorial about Isuzu revealing MU-X, not Israeli-market sale specs.

Validated facts embedded for this task:

- Isuzu Israel official site focuses on D-Max and trucks, not MU-X passenger SUV.
- Existing source key itself is `global-reference-only`.
- No strong Israeli sales/importer evidence is embedded for MU-X.

Embedded source URLs:

```text
https://www.cartube.co.il/חדשות-רכב/איסוזו-חושפת-mu-x-חדש-מתחרה-ללנד-קרוזר
https://www.auto.co.il/article/131758-world-news
https://www.isuzu.co.il/
```

Action:

- Do not recover to clean.
- Move to archive non-blocking:

```json
{
  "make": "Isuzu",
  "model": "MU-X",
  "reason": "global_reference_only_no_israeli_market_evidence",
  "non_blocking": true,
  "batch_id": "BATCH24",
  "lineage": ["global-reference-only|Isuzu|MU-X"]
}
```

Action tag: `MOVE TO ARCHIVE`.

---

## 12. Jaguar S-Type — MERGE source-scope duplicate into confirmed clean profile or recover if absent

Current review issue:

- `IL-likely|Jaguar|S-Type` is empty / blocked.
- RUN 4 already handled `IL-confirmed|Jaguar|S-Type` clean-side correction.

Validated facts embedded for this task:

- Yad2 Israeli price list supports Jaguar S-Type rows: 3.0 240 hp, SE 3.0 240 hp, 4.2 300 hp, and R 4.2 400 hp in relevant years.
- The `IL-likely` empty profile should not remain active review if the confirmed profile already exists.

Embedded source URLs:

```text
https://www.yad2.co.il/price-list/feed?manufacturer=20&model=10253
```

Action:

- If `IL-confirmed|Jaguar|S-Type` exists in clean, merge/archive `IL-likely|Jaguar|S-Type` as a source-scope duplicate alias pointing to the confirmed profile.
- Preserve alias/lineage:

```text
IL-likely|Jaguar|S-Type -> IL-confirmed|Jaguar|S-Type
```

- Do not create a second clean S-Type profile.
- If confirmed profile is absent due to prior implementation bug, recover one canonical clean S-Type profile with source-supported rows:

```text
Jaguar S-Type | 3.0        | Sedan | petrol | 3.0L V6 | 240 hp | automatic | RWD | grounded years
Jaguar S-Type | SE 3.0     | Sedan | petrol | 3.0L V6 | 240 hp | automatic | RWD | grounded years
Jaguar S-Type | 4.2 i      | Sedan | petrol | 4.2L V8 | 300 hp | automatic | RWD | grounded years
Jaguar S-Type | R 4.2 i    | Sedan | petrol | 4.2L V8 | 400 hp | automatic | RWD | grounded years
```

Action tag: `MERGE / ALIAS / RECOVER IF NEEDED`.

---

# Identity / casing / alias cleanup for FINAL RUN

Even though `unmatched_output_keys_count = 0`, run a final identity audit across Batch 24 window.

Required checks:

```text
Honda odyssey -> Honda Odyssey if project convention uses title case
Honda e:Ny1 casing preserved exactly if archived/clean
Honda Stream casing preserved
Hyundai elantra -> Hyundai Elantra
Hyundai getz -> Hyundai Getz
Hyundai grandeur -> Hyundai Grandeur
Hummer h2 -> Hummer H2
Hummer h3 -> Hummer H3
Isuzu global/IL source-scope duplicates merged or archived
Jaguar IL-likely/global-reference-only source-scope duplicates merged or archived
Jaecoo IL-likely/IL-confirmed duplicates merged or aliased
Jeep Avenger: do not consume/process the next source `IL-likely|Jeep|Avenger` unless it is only an alias to the already processed `IL-confirmed|Jeep|Avenger`
```

Rules:

- No duplicate clean profiles for the same Israeli model.
- All source-scope duplicates should be aliases/lineage or non-blocking archive records.
- Archive entries must include `non_blocking=true`, `batch_id=BATCH24`, reason, and lineage/source key.
- Do not let non-blocking archive entries create active blockers or unmatched output keys.

---

# Final required state after applying FINAL RUN

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

Expected cursor after full Batch 24 window:

```text
resume_after_key = IL-confirmed|Jeep|Avenger
next_key_to_process = IL-likely|Jeep|Avenger
```

Quality scan:

- `bug = 0` required.
- `normalization = 0` required.
- `leak` / `structure` can remain informational only if they are not readiness blockers.

---

# Commands to run

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Also run a direct generated-file / resume-state audit using `compute_resume_state()` and assert:

```text
resume_after_key = IL-confirmed|Jeep|Avenger
next_key_to_process = IL-likely|Jeep|Avenger
active_blocked_count = 0
unmatched_output_keys_count = 0
unmatched_output_keys_sample = []
```

---

# Return format

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

If any required metric is not green, say:

```text
Do not merge yet.
```
