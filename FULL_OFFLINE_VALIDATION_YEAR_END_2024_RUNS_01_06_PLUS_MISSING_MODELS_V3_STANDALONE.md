# FULL OFFLINE VALIDATION V3 — STANDALONE MASTER FILE

Generated: 2026-06-24

## Why V3 exists

V2 was too small because it became a controller/summary file that referenced prior run files instead of embedding the full run-level correction instructions. That is not enough for a no-internet Codex run. This V3 is standalone: it embeds the run files, run 1–2 revalidation patch, run 3–6 instructions, missing full-profile additions, and the closed final validation run.

## Absolute rules for Codex

- Do not browse the internet.
- Do not infer years.
- Do not ask for validation sources.
- Apply only the decisions embedded in this file.
- Current rows use `year_end: null`; never use `2026` as a fake current marker.
- Do not mass-replace `2024 -> null`.
- If a row was revalidated/overridden in a later section, the later section wins.
- Every added/changed source index must point to an actual source object inside the same profile.
- Every `field_sources` index must point to an actual source object inside the same profile.
- EV rows must use `engine_displacement_l: null`.
- Hybrid/PHEV/MHEV rows must keep the ICE displacement when the embedded target row includes it.
- Recompute `available_values_for_website` for changed/added profiles.

## Section priority order

Apply sections in this order:

1. Run 1 base task.
2. Run 2 base task.
3. Run 1–2 revalidation patch — overrides Run 1/2 where it conflicts.
4. Run 3 task.
5. Run 4 task.
6. Run 5 task.
7. Run 6 task.
8. Missing full profiles task.
9. Final validation closed V2 — overrides any retained/conditional entry.

---


---

# EMBEDDED FILE: CODEX_YEAR_END_2024_RUN_01_FIX_TASK.md


# CODEX TASK — YEAR_END 2024 SYSTEMIC CORRECTION — RUN 01 / 50 PROFILES

Source file to edit: `model_technical_catalog_il.json`

User intent: fix the systemic `year_end: 2024` cutoff artifact in the first run of 50 profiles. Do **not** do a blind replace of `2024` to `null`. The job is to distinguish between:

1. a model/variant that is genuinely discontinued in 2024,
2. an old variant/generation that ended in 2024 while a new current variant exists,
3. a current Israeli-market model where `year_end: 2024` is only a source-cutoff bug and must become `null`.

Codex has no browsing. Treat the embedded validation facts and URLs below as the source package for this run, then use repo-local source policy to add/update `sources`, `source_indexes`, `field_sources`, notes, and `available_values_for_website`.

---

## Hard rules

- Scope is **only** the 50 profiles listed below.
- Update model-level `year_end` and variant-level `year_end` only when the row is inside this scope.
- Never change a historical `year_end: 2024` to `null` just because the model name still exists.
- If a new generation/facelift/powertrain exists, keep the old 2024 row and add/split a current row only when the current Israeli source supports the exact powertrain/trim/body.
- If the exact current variant cannot be grounded from the embedded facts or repo-local sources, leave the row at 2024 and add a note: `RUN01: 2024 retained because current Israeli continuity for this exact variant was not grounded.`
- When changing `year_end` to `null`, append a current Israeli source to the profile `sources` list, then append that `source_index` to `source_indexes` and `field_sources.year_end`; also append to fields supported by that source.
- For EV rows, keep `engine_displacement_l: null` and `transmission: single_speed` unless the profile schema uses another validated EV transmission convention consistently.
- Do not introduce `review`, `indirect`, placeholders, fake URLs, or `source_index` values that do not exist in the profile.
- After patching, run the validation commands at the bottom.

---

## Run 01 scope

1. Abarth | 500 | canonical: 595
2. Aiways | U6
3. Alfa Romeo | Stelvio
4. Audi | A4
5. Audi | A5
6. Audi | A6
7. Audi | A8
8. Audi | e-tron GT
9. Audi | Q5
10. Audi | Q7
11. Audi | R8
12. Audi | RS4
13. Audi | RS5
14. Audi | RS7
15. Audi | S3
16. Audi | SQ5
17. Bentley | Continental GT
18. Bentley | Flying Spur
19. BMW | 118i
20. BMW | 120i
21. BMW | 128ti
22. BMW | 218i Gran Coupe
23. BMW | 225xe (Active Tourer PHEV)
24. BMW | 318i
25. BMW | 320e
26. BMW | 640i GT
27. BMW | 850i
28. BMW | i4 eDrive35
29. BMW | iX xDrive40
30. BMW | M135i
31. BMW | M2
32. BMW | M8
33. BMW | M850i
34. BMW | X2 M35i
35. BMW | X3 2.0i
36. BMW | X3 M
37. BMW | X3 M40i
38. BMW | X3 xDrive30e
39. BMW | X6 M
40. BMW | Z4 sDrive20i
41. BYD | Atto 3
42. BYD | Dolphin
43. BYD | Han
44. BYD | Tang
45. Cadillac | XT5
46. Chery | Tiggo 7 Pro
47. Chery | Tiggo 8 Pro
48. Chevrolet | Camaro
49. Chevrolet | Equinox
50. Citroen | Berlingo

---

## Embedded web-validation anchors

Use these as source anchors when patching rows. Prefer official Israeli importer pages and official price/spec PDFs over generic catalog pages.

### Abarth / Aiways / Alfa Romeo

- Abarth Israel official homepage: `https://abarth.co.il/`
- Abarth 595 Nuvolari S page: `https://abarth.co.il/nuvolari-s/`
- Abarth car books page shows 2024 as the available petrol/electric book selector: `https://abarth.co.il/car_books/`
- Aiways U5 official Israel page exists: `https://aiways.co.il/u5/`
- Aiways website navigation/application page mentions U6 and U5: `https://aiways.co.il/aiways-%D7%90%D7%A4%D7%9C%D7%99%D7%A7%D7%A6%D7%99%D7%99%D7%AA/`
- Alfa Romeo Israel official homepage: `https://www.alfaromeo.co.il/`
- Alfa Romeo Stelvio official Israel page: `https://www.alfaromeo.co.il/models/stelvio`
- Alfa Romeo recall page mentions Stelvio/Giulia 2024 in Israel: `https://www.alfaromeo.co.il/service-calls-recall`

### Audi

- Audi Israel all-models page: `https://www.audi.co.il/all-models/`
- Audi A5 Sedan official Israel page: `https://www.audi.co.il/models/a5/a5-sedan/`
- Audi A5 Sedan e-hybrid official Israel page: `https://www.audi.co.il/models/a5/a5-sedan-e-hybrid/`
- Audi S5 Sedan official Israel page states the new S5 replaces the popular A4 and A5 series: `https://www.audi.co.il/models/a5/s5-sedan/`
- Audi A6 Sedan official Israel page: `https://www.audi.co.il/models/a6/a6-sedan/`
- Audi A6 Sedan e-hybrid official Israel page: `https://www.audi.co.il/models/a6/a6-sedan-e-hybrid/`
- Audi A6 Sportback e-tron official Israel page: `https://www.audi.co.il/models/a6-e-tron/a6-sportback-e-tron/`
- Audi A8 TFSIe official Israel page: `https://www.audi.co.il/models/a8/a8-tfsie/`
- Audi S8 official Israel page: `https://www.audi.co.il/models/a8/s8/`
- Audi RS3 Sportback official Israel page: `https://www.audi.co.il/models/a3/rs3-sportback/`

### Bentley

- Bentley Tel Aviv official site shows `New Flying Spur`: `https://www.bentleytelaviv.com/`
- Bentley Continental GT official global current page: `https://www.bentleymotors.com/en/models/continental-gt.html`
- Bentley Continental GT Speed official global page: `https://www.bentleymotors.com/en/models/continental-gt/continental-gt-speed.html`
- Bentley Continental GT Mulliner official global page: `https://www.bentleymotors.com/en/models/continental-gt/continental-gt-mulliner.html`
- Bentley Flying Spur official global current page: `https://www.bentleymotors.com/en/models/flying-spur.html`
- Bentley Flying Spur Speed official global page: `https://www.bentleymotors.com/en/models/flying-spur/flying-spur-speed.html`
- Bentley Flying Spur Azure official global page: `https://www.bentleymotors.com/en/models/flying-spur/flying-spur-azure.html`
- Israeli Auto article: Bentley Continental GT and Flying Spur new generation launched in Israel, 09-01-2025: `https://www.auto.co.il/articles/car-news/local-news/137810/`
- Auto Israel Flying Spur 2025 catalog page: `https://www.auto.co.il/cars/bentley/flying-spur/2025/`

### BMW

- BMW all-models official Israel page: `https://www.bmw.co.il/he/All-Models.html`
- BMW i4 current 2026 official PDF: `https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/Pollution-and-Safety/2026/jan2026/i4_01/39860%20BMW%20i4.pdf`
- BMW i4 technical data page: `https://www.bmw.co.il/he/All-Models/bmw-i/i4/bmw-i4-gran-coupe-technical-data.html`
- BMW price list 05/2025 official PDF: `https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/Price_lists/39464%20Mechiron%20BMW%20Site%202025.pdf.asset.1749475023505.pdf`
- BMW price list 11/2025 official PDF: `https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/Price_lists/nov2025/39815%20Mechiron%20BMW%20Site%202025.pdf`
- BMW X2 official Israel page, price list 04/2026: `https://www.bmw.co.il/he/All-Models/x-series/x2/bmw-x2.html`
- BMW X2 M35i page: `https://www.bmw.co.il/he/All-Models/m-series/x2-m35i/bmw-x2-m35ixdrive.html`
- BMW X2 2026 PDF: `https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/Pollution-and-Safety/2026/jan2026/x2_01/39848%20BMW%20X2.pdf`
- BMW X3 official Israel current page: `https://www.bmw.co.il/he/All-Models/x-series/x3/bmw-x3.html`
- BMW X3 plug-in hybrid official Israel page: `https://www.bmw.co.il/he/All-Models/x-series/x3/bmw-x3-plug-in-hybrid.html`
- BMW X6 official Israel current page: `https://www.bmw.co.il/he/All-Models/x-series/x6/bmw-x6.html`
- BMW Z4 official Israel page, price list 04/2026: `https://www.bmw.co.il/he/All-Models/z-series/z4-roadster/bmw-z4-roadster.html`

### BYD

- BYD ATTO 3 FL official Israel page: `https://bydauto.co.il/model/byd-atto-3-fl/`
- BYD ATTO 3 EVO official Israel page: `https://bydauto.co.il/model/byd-atto-3-evo/`
- BYD Dolphin official Israel page: `https://bydauto.co.il/model/byd-dolphin/`
- BYD Tang official Israel page: `https://bydauto.co.il/model/tang/`
- BYD showrooms/navigation page lists Tang and current model families: `https://bydauto.co.il/showrooms/`

### Cadillac / Chery / Chevrolet / Citroen

- Cadillac Israel official homepage current lineup does not show XT5; it shows current/new models such as OPTIQ and XT6: `https://www.cadillac.co.il/`
- Cadillac XT6 2026 official page: `https://www.cadillac.co.il/%D7%93%D7%92%D7%9E%D7%99%D7%9D/xt6/`
- Cadillac service/manual page: `https://www.cadillac.co.il/%D7%A9%D7%99%D7%A8%D7%95%D7%AA-%D7%A7%D7%90%D7%93%D7%99%D7%9C%D7%A7/%D7%A1%D7%A4%D7%A8-%D7%A8%D7%9B%D7%91/`
- Chery Israel official homepage/current model selector lists TIGGO 7 Pro, TIGGO 7 Pro PHEV, TIGGO 8 Pro, TIGGO 8 Pro PHEV, TIGGO 7 HEV and 2026 sale terms: `https://cheryisrael.co.il/`
- Chery insurance/funding/showroom pages repeat current model navigation and June 2026 sale terms: `https://cheryisrael.co.il/insurance/`, `https://cheryisrael.co.il/funding/`, `https://cheryisrael.co.il/showrooms/`
- GM official: Camaro sixth generation retires at the conclusion of model year 2024; final cars off Lansing Grand River in January 2024: `https://news.gm.com/home.detail.html/Pages/news/us/en/2023/mar/0322-camaro.html`
- Chevrolet Israel car-book page shows 2024 model-year books and no current Camaro/Equinox new-model page: `https://www.chevrolet.co.il/%D7%A9%D7%99%D7%A8%D7%95%D7%AA-%D7%A9%D7%91%D7%A8%D7%95%D7%9C%D7%98/%D7%A1%D7%A4%D7%A8-%D7%A8%D7%9B%D7%91/`
- Citroen Berlingo official Israel online page: `https://online.citroen.co.il/model/berlingo/`
- Citroen Israel official homepage/current range: `https://www.citroen.co.il/`

---

## Required per-profile decisions and actions

### 1. Abarth | 500 / canonical 595
Current suspect rows: Competizione Hatchback 180hp manual 2016-2024; Nuvolari S Hatchback 165hp manual 2022-2024.

Action:
- Do **not** automatically change to `null`.
- Keep `year_end: 2024` unless repo-local Abarth Israel source proves petrol 595/Competizione/Nuvolari S is still marketed after 2024.
- If retained, add note: `RUN01: petrol Abarth 595 rows retained at 2024; current continuity beyond 2024 not grounded by official Israeli source in this run.`

### 2. Aiways | U6
Current suspect row: Prime EV 2023-2024.

Action:
- Do **not** automatically change to `null` from a stale nav link.
- Keep `year_end: 2024` unless repo-local current official U6 order/spec source proves active 2025/2026 sale.
- If retained, add note: `RUN01: U6 retained at 2024 because current Israeli-market sale after 2024 was not grounded.`

### 3. Alfa Romeo | Stelvio
Current suspect row: Quadrifoglio 2.9 V6 510hp 2024-2024 while regular Stelvio profile is current.

Action:
- Keep Quadrifoglio row `year_start: 2024`, `year_end: 2024` unless Alfa Romeo Israel official current Stelvio page/source lists Quadrifoglio as a current orderable trim.
- Do not alter current regular Stelvio rows.
- Add note: `RUN01: Stelvio Quadrifoglio row is a 2024-specific high-performance trim; regular Stelvio current status does not currentize Quadrifoglio.`

### 4. Audi | A4
Current suspect rows: 2020-2024 2.0 mild-hybrid 150/204/265hp.

Action:
- Keep A4 rows at `year_end: 2024` because Audi Israel current lineup shifts to new A5/S5 pages and the S5 page states the new car replaces the A4/A5 series.
- Model-level `year_end` may stay 2024 if no current A4 page exists in repo-local sources.
- Add note documenting replacement by new A5/S5 family.

### 5. Audi | A5
Current suspect rows: old Liftback/Sportback 2020-2024 150/204hp and old 2017-2024 190hp.

Action:
- Keep these old-generation rows at `year_end: 2024`.
- Do not change old Liftback/Sportback rows to `null` just because current A5 Sedan/e-hybrid exists.
- If current A5 Sedan/e-hybrid rows already exist in profile, ensure profile-level `year_end` is `null`; if missing, add only if repo-local source has exact current body/powertrain.

### 6. Audi | A6
Current suspect rows: 2023-2024 Superior 265hp AWD, Superior 340hp V6 AWD, design PHEV 299hp.

Action:
- Keep the 2023-2024 rows at `year_end: 2024` unless exact same current 2026 A6 Sedan/e-hybrid variant exists in Audi Israel source.
- Current A6 Sedan 40 TFSI and A6 Sedan e-hybrid should be represented as separate current rows only if exact engine/power/trim is grounded.
- Do not currentize the old 340hp V6 row unless current Audi Israel page/source proves it.

### 7. Audi | A8
Current suspect row: 55 TFSI quattro 3.0 V6 340hp 2023-2024.

Action:
- Keep 55 TFSI row at `year_end: 2024` unless exact 55 TFSI current Israeli source exists.
- Do not use current A8 TFSIe/S8 pages to currentize the 55 TFSI row.

### 8. Audi | e-tron GT
Current suspect row: RS 598hp 2021-2024.

Action:
- Treat as old pre-update RS e-tron GT row. Keep `year_end: 2024` unless exact 598hp RS is still current in Audi Israel source.
- If profile already has current 2025/2026 S/RS updated rows, leave them as current and keep old row 2024.

### 9. Audi | Q5
Current suspect row: 2.0 turbo petrol 265hp AWD 2021-2024.

Action:
- Keep 2021-2024 row unless exact same 265hp AWD variant is current.
- If current Q5 uses new generation/new powertrain/trim, add/split current row only if exact Audi Israel source exists.

### 10. Audi | Q7
Current suspect row: S-Line Limited 3.0 V6 340hp 2020-2024.

Action:
- Keep `S-Line Limited` at `year_end: 2024` unless exact current Limited trim appears in current Audi Israel source.
- Do not currentize limited/special trim from generic Q7 current availability.

### 11. Audi | R8
Current suspect row: V10 Performance RWD 2024-2024.

Action:
- Keep `year_end: 2024`. R8 is a discontinued model; do not set null.
- Add note: `RUN01: R8 retained at 2024 as end-of-production/end-of-market row.`

### 12. Audi | RS4
Current suspect row: RS4 Avant 2.9 V6 450hp 2020-2024.

Action:
- Keep `year_end: 2024` unless exact current Israeli RS4 source exists.
- If no current source, set model-level `year_end` to 2024 and add note.

### 13. Audi | RS5
Current suspect rows: Coupe and Sportback 2.9 V6 450hp 2021-2024.

Action:
- Keep old Coupe/Sportback 450hp rows at 2024 unless exact current RS5 source exists.
- If the profile has a 2026 current row, verify it is not a hallucinated continuation of the old row.

### 14. Audi | RS7
Current suspect row: 4.0 V8 600hp 2020-2024.

Action:
- Keep at 2024 unless exact current RS7 Israeli source exists.
- Do not use generic Audi current lineup without model page/spec to set null.

### 15. Audi | S3
Current suspect rows are likely pre-facelift S3 rows ending 2024.

Action:
- Keep pre-facelift rows at 2024.
- If a facelift/current S3 row exists with updated spec, represent it separately and set only that current row to `null`.

### 16. Audi | SQ5
Current suspect row likely old SQ5 generation/variant ending 2024.

Action:
- Keep old row at 2024 unless exact current SQ5 Israeli source exists.
- Split current generation only if exact current source supports.

### 17. Bentley | Continental GT
Current suspect rows: all 4 rows end 2024.

Action:
- Keep old W12/V8/pre-2025 rows at `year_end: 2024`.
- Add/split new current Continental GT/GTC hybrid rows only if profile lacks them and the current Israeli Auto launch article + Bentley official pages support exact body/powertrain.
- Minimum current row when grounded: `fuel_type: plug_in_hybrid`, `engine: 4.0L twin-turbo V8 hybrid` or consistent profile wording, `horsepower_hp: 771` or 782 PS converted according to existing hp convention, `drivetrain: AWD`, `year_start: 2025`, `year_end: null`.
- Set profile-level `year_end: null` after adding current row; keep old variants at 2024.

### 18. Bentley | Flying Spur
Current suspect rows include old rows ending 2024.

Action:
- Keep old W12/V8/pre-2025 rows at 2024.
- Add/split new current Flying Spur hybrid row when grounded by Bentley official + Auto Israel 2025 launch/current catalog.
- Set profile-level `year_end: null` after adding current row; keep old variants at 2024.

### 19. BMW | 118i
Current suspect row: Vibe 1.5 turbo 140hp 2019-2024.

Action:
- Keep old F40 118i row at 2024 unless 118i is explicitly current in 2025/2026 BMW Israel price list.
- Do not use current 120i/1-Series availability to currentize 118i.

### 20. BMW | 120i
Current suspect row: old 2.0 turbo 178hp 2020-2024; profile already has current 2024-2026 mild-hybrid 1.5 turbo 170hp.

Action:
- Keep old 178hp row at 2024.
- Ensure current mild-hybrid 170hp row remains current (`year_end` should be `null` if official 2026 source proves it; if repo convention uses 2026 for future-current rows, normalize according to catalog policy, but preferred current value is `null`).
- Model-level `year_end` should be `null` if active current row exists.

### 21. BMW | 128ti
Current suspect row: Superior 2.0 turbo 265hp 2021-2024.

Action:
- Keep `year_end: 2024`; 128ti is an old F40 performance variant unless exact current source exists.

### 22. BMW | 218i Gran Coupe
Current suspect row: M-Sport 1.5 turbo 136hp 2021-2024.

Action:
- Keep old row at 2024 unless exact current 218i Gran Coupe Israeli source exists.
- If new 2-Series Gran Coupe current has different model designation/power, split separately; do not currentize old row.

### 23. BMW | 225xe Active Tourer PHEV
Current suspect row: 245hp PHEV 2022-2024.

Action:
- Keep at 2024 unless exact current 225xe Active Tourer source exists.
- Do not confuse with current X3/iX/other BMW PHEV rows.

### 24. BMW | 318i
Current suspect rows: Business and M-Design 2.0 turbo 156hp 2020-2024.

Action:
- Check BMW 2025/2026 price list. If no 318i current listing exists, keep rows at 2024 and set model-level `year_end: 2024`.
- If exact current 318i row exists, update to `null` with source.

### 25. BMW | 320e
Current suspect row: M-Design PHEV 204hp 2021-2024.

Action:
- Keep at 2024 unless exact current 320e Israeli price/spec source exists.

### 26. BMW | 640i GT
Current suspect row: Luxury 3.0 I6 340hp 2017-2024.

Action:
- Keep `year_end: 2024`; do not currentize unless official current Israeli 6 GT source exists.

### 27. BMW | 850i
Current suspect rows: M850i xDrive Coupe/Convertible/Sedan 2018/2019-2024.

Action:
- Keep at 2024 unless exact current BMW 8-series/M850i Israeli source exists.
- Be careful: this overlaps with separate `M850i`; avoid duplicate/split-profile regression.

### 28. BMW | i4 eDrive35
Current suspect rows: M-Shadow and Essence EV 2023-2024.

Action:
- Change current applicable i4 eDrive35 rows to `year_end: null` if they match current BMW Israel i4 2026 sources.
- Update model-level `year_end: null`.
- Add BMW i4 2026 PDF/source to `sources`; append source index to `field_sources.year_end` and current fields.
- Keep EV schema: `engine_displacement_l: null`, `transmission: single_speed`, `fuel_type: electric`.

### 29. BMW | iX xDrive40
Current suspect row: 326hp AWD 2021-2024.

Action:
- Keep `year_end: 2024` unless exact iX xDrive40 current Israeli source exists. Current iX may have different xDrive50/M60 rows; do not currentize xDrive40 from generic iX availability.

### 30. BMW | M135i
Current suspect row: xDrive 306hp 2019-2024.

Action:
- Keep old 306hp row at 2024.
- If current/new M135 exists with different generation/spec, add/split separately only with exact source.

### 31. BMW | M2
Current suspect row: Carbon 460hp 2023-2024.

Action:
- Check current BMW Israel price list/model source. If M2 current exists with same 460hp/Carbon row, set row/profile `year_end: null`; if current M2 spec changed, keep 460hp row at 2024 and add/split current row.

### 32. BMW | M8
Current suspect rows: Competition Coupe/Convertible/Gran Coupe 625hp 2020-2024.

Action:
- Keep at 2024 unless exact current M8 Israeli source exists.
- Do not infer current from old high-performance BMW catalog rows.

### 33. BMW | M850i
Current suspect rows: M850i xDrive Coupe/Convertible/Gran Coupe 2018/2019-2024.

Action:
- Keep at 2024 unless exact current BMW M850i Israeli source exists.
- Reconcile/avoid duplicate with `BMW | 850i` profile if repo has duplicate canonical collision policy.

### 34. BMW | X2 M35i
Current suspect row: M-Sport Pro 300hp AWD 2024-2024.

Action:
- Change to `year_end: null` if exact current BMW X2 M35i xDrive M-Sport Pro row is supported by BMW Israel 04/2026 page/PDF.
- Update profile-level `year_end: null`.
- Add BMW X2 2026 source/PDF and append to field sources.

### 35. BMW | X3 2.0i
Current suspect old row: 2011-2024 2.0 turbo 184hp; profile already has current 2024-2026 mild-hybrid 208hp row.

Action:
- Keep old 184hp row at 2024.
- Ensure current 208hp mild-hybrid row is current (`year_end: null` preferred if catalog current convention requires null).
- Model-level `year_end` should be `null` if current row exists.

### 36. BMW | X3 M
Current suspect row: Competition 510hp 2019-2024.

Action:
- Keep `year_end: 2024` unless exact current X3 M source exists. Current G45 X3 M50 is not the same as X3 M Competition.

### 37. BMW | X3 M40i
Current suspect row: Exclusive 360hp 2018-2024.

Action:
- Keep at 2024. Current G45 successor may be X3 M50/xDriveM50, not M40i; do not currentize old M40i.

### 38. BMW | X3 xDrive30e
Current suspect row: Executive PHEV 292hp 2020-2024.

Action:
- Check current X3 plug-in hybrid official BMW Israel page and price list. If current source supports X3 xDrive30e/e30 xDrive current sale, set profile `year_end: null`.
- If the current trim is `Launch-M`/new generation and old `Executive` ended, keep old Executive row at 2024 and add/split current row with `year_start: 2025` or source-grounded start year and `year_end: null`.

### 39. BMW | X6 M
Current suspect row: Competition mild-hybrid 625hp 2024-2024.

Action:
- BMW 05/2025 price list includes X6 M Competition; change current Competition row to `year_end: null` if exact fields match.
- Update model-level `year_end: null`.
- Add BMW 05/2025 price list source and field_sources.

### 40. BMW | Z4 sDrive20i
Current suspect rows: M-Sport 2019-2024 and M-Design 2023-2024.

Action:
- BMW Z4 official page lists Z4 20i M-Design in 04/2026 price list.
- Set M-Design current row to `year_end: null` and update profile-level `year_end: null`.
- Keep older M-Sport row at 2024 unless current source supports M-Sport; do not currentize M-Sport from M-Design source.

### 41. BYD | Atto 3
Current suspect rows: Comfort and Design 2022-2024.

Action:
- BYD ATTO 3 is current in Israel, but current official pages are ATTO 3 FL / ATTO 3 EVO.
- Set profile-level `year_end: null`.
- Do not blindly set old Comfort/Design rows to null if current FL/EVO technical variants are distinct. Either:
  - if current official source supports same Comfort/Design technical rows, set them null; or
  - keep 2022-2024 rows and add current FL/EVO rows with source-grounded trim/body/power.

### 42. BYD | Dolphin
Current suspect rows: Comfort and Design 204hp 2023-2024.

Action:
- BYD Dolphin official Israel page is current. If current official page/source supports Comfort/Design 204hp rows, set both rows to `year_end: null` and profile-level `year_end: null`.
- If trims changed, keep old rows and add/split current rows.

### 43. BYD | Han
Current suspect row: Executive 518hp AWD 2022-2024.

Action:
- Do not set null unless current BYD Israel official page/current model selector confirms Han is still sold.
- If Han is absent from official current model selector and only older sources exist, keep `year_end: 2024`.

### 44. BYD | Tang
Current suspect row: Premium 518hp AWD 2022-2024.

Action:
- BYD Tang official Israel page is current. Set profile-level `year_end: null` and set Premium row to `year_end: null` if the current page/source supports same technical fields.
- Add BYD Tang source and field_sources.

### 45. Cadillac | XT5
Current suspect rows: 2.0 turbo FWD and 3.6 V6 AWD 2020-2024.

Action:
- Keep `year_end: 2024` unless exact current XT5 Israeli source exists.
- Cadillac current official site focuses on OPTIQ/XT6 and does not provide a current XT5 model page in the embedded anchors.

### 46. Chery | Tiggo 7 Pro
Current suspect rows: Comfort/Noble petrol 1.6 turbo and Supreme PHEV 1.5 turbo, both ending 2024.

Action:
- Chery Israel current model selector lists TIGGO 7 Pro and TIGGO 7 Pro PHEV in 2026 context.
- Set profile-level `year_end: null`.
- Set petrol/PHEV rows to `year_end: null` only if current source/profile supports same trim-power fields; otherwise keep old rows and add/split current 2025/2026 rows.
- Add Chery Israel source and update field_sources.

### 47. Chery | Tiggo 8 Pro
Current suspect rows: Luxury/Noble petrol and Ultimate PHEV ending 2024.

Action:
- Chery Israel current model selector lists TIGGO 8 Pro and TIGGO 8 Pro PHEV in 2026 context.
- Set profile-level `year_end: null`.
- Set rows to `null` only if exact current trim/power fields are supported; otherwise split current rows.

### 48. Chevrolet | Camaro
Current suspect rows: LT V6, SS V8, ZL1 supercharged V8 all ending 2024.

Action:
- Keep all Camaro rows at `year_end: 2024`. GM official source says sixth-generation Camaro retires at the conclusion of 2024 model year.
- Model-level `year_end` should remain 2024.
- Add/keep note: `RUN01: Camaro sixth generation retained at 2024 per GM end-of-production/end-of-model-year source.`

### 49. Chevrolet | Equinox
Current suspect rows: 1.5 turbo FWD/AWD 2018-2024.

Action:
- Keep `year_end: 2024` unless exact current Equinox Israeli source exists.
- Chevrolet Israel car-book/current pages in embedded anchors do not ground a current Equinox sale page.

### 50. Citroen | Berlingo
Current suspect rows: 1.5 diesel 75 manual, 100 manual, 130 8-speed automatic, all 2019-2024.

Action:
- Citroen Berlingo has an official current Israeli page. Set profile-level `year_end: null`.
- Only set variant rows to `null` if exact current diesel/manual/automatic versions are supported.
- Likely action: keep old 75hp and 100hp manual rows at 2024 unless current page/spec supports them; set the 130hp automatic row to `null` only if current spec supports it. If current spec differs, add/split current row.

---

## Automated checks Codex should add or run

After changes, run a focused script to report how many `year_end: 2024` values remain in these 50 profiles and classify each as one of:

- `retained_discontinued`
- `retained_old_generation_split_current`
- `changed_to_null_current`
- `needs_manual_review`

Then run:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Final Codex response must include:

- profiles changed to current/null
- profiles retained at 2024 with reason
- rows split/added
- remaining `year_end: 2024` count inside Run 01
- validation command outputs


---

# EMBEDDED FILE: CODEX_YEAR_END_2024_RUN_02_FIX_TASK.md


# CODEX TASK — YEAR_END 2024 SYSTEMIC CORRECTION — RUN 02 / 50 PROFILES

Source file to edit: `model_technical_catalog_il.json`

User intent: continue the systemic `year_end: 2024` correction. This run covers the second block of 50 profiles from the 2024-cutoff audit. Do **not** do a blind replace of `2024` to `null`. The job is to distinguish between true 2024 discontinuation, old variant/generation end, and current Israeli-market continuation.

---

## Run-level count summary

These are profile-level decisions, not variant counts.

```text
RUN 02 profiles in scope: 50
DEFINITE CHANGE / CURRENTIZE / SPLIT CURRENT ROW: 14 profiles
RETAIN 2024: 29 profiles
CONDITIONAL EXACT-SOURCE CHECK: 6 profiles
NO YEAR_END ACTION: 1 profile
```

Definitions:
- `DEFINITE CHANGE`: Codex should make an actual catalog change if the row structure in the repo matches the directive. This may mean setting `year_end: null`, setting model-level `year_end: null`, or adding/splitting a current row while preserving old 2024 rows.
- `RETAIN 2024`: do not currentize the suspect 2024 row; add a note/source where needed.
- `CONDITIONAL`: exact Israeli source/row matching is required before changing; otherwise retain 2024.
- `NO YEAR_END ACTION`: the profile was pulled into the run but does not require a 2024 patch.

---

## Hard rules

1. Work only on the 50 profiles listed below.
2. Inspect both model-level `year_end` and every `technical_variants_il[*].year_end`.
3. Never set an old historical row to `null` just because the model name still exists.
4. If the old row ended in 2024 but a current model/generation exists, preserve the old row and add/split the current row only when grounded.
5. If a current Israeli official/importer source supports the exact old row, set that row `year_end: null`.
6. If a current model page exists but does not ground the exact old row, set only the model-level status/current row as appropriate and keep old rows at 2024.
7. Do not introduce `review`, `indirect`, fake URLs, placeholder sources, or dangling source indexes.
8. If adding a source, append a real source object to `sources` with a valid numeric `source_index`, then update `source_indexes` and `field_sources`.
9. EV rows must keep `engine_displacement_l: null`.
10. After patching, run validation commands at the bottom.

---

## Embedded validation anchors

Codex should not browse. Use these embedded anchors plus repo-local sources.

### Citroen Israel
- `https://online.citroen.co.il/`
- `https://www.citroen.co.il/`
- `https://online.citroen.co.il/pricelist/c5-aircross/`
- Current Citroen Israel pages show new/current model context, including New C3 and New C5 Aircross. Do not use C5 Aircross to currentize C5 X. Do not currentize old C3/C3 Aircross/C4 powertrains unless exact current source supports them.

### Cupra Israel
- `https://cupraofficial.co.il/`
- Current CUPRA Israel pages can support Formentor as current. Do not currentize old Ateca/Born/Leon rows unless exact current Israeli source supports the same model/trim/powertrain.

### Dacia Israel
- `https://www.dacia.co.il/index.html`
- `https://www.dacia.co.il/CountriesData/Israel/images/brochures/dacia-jogger-brochure.pdf`
- Dacia Israel lists Jogger as current; use exact brochure/spec matching before currentizing the old 1.0T row.

### DS Israel
- `https://online.dsautomobiles.co.il/`
- `https://online.dsautomobiles.co.il/pricelist/ds-4/`
- DS 4 and DS 7 can be treated as current only where the Israeli online price/spec page supports the exact trim/powertrain. DS 9 is not currentized without exact source.

### Fiat Israel
- `https://www.fiat.co.il/`
- Fiat Israel official site can ground current Fiat 500e, but old Action/Icon/La Prima rows must not be blindly extended if trim/body structure changed.

### Ford Israel
- `https://www.ford.co.il/`
- `https://www.ford.co.il/דגמים`
- Current Ford Israel model list includes Bronco, Bronco Raptor, Ranger/Ranger Raptor, Mustang, Focus Tourer, Ford Explorer. It does **not** ground F-150, Kuga, Mach-E, Puma, or Transit as current new-car rows unless repo-local exact source exists.

### Geely Israel
- `https://geely.co.il/`
- `https://geely.co.il/geometry-c/`
- Geometry C is conditional: a page existing is not automatically active sale; currentize only if active/current source is repo-grounded.

### Genesis Israel
- `https://www.genesis.co.il/he/models-pricing/`
- Current Genesis Israel pricing/model context can support GV70 gasoline, not automatically G70 or Electrified GV70.

### Hongqi Israel
- `https://hongqi.co.il/`
- Current Hongqi Israel pages emphasize newer 5/7 model family. Keep E-HS9 2024 unless exact official current E-HS9 source exists.

### Hyundai Israel
- `https://www.hyundaimotors.co.il/`
- Current Hyundai Israel context supports IONIQ 5, IONIQ 6, Palisade Hybrid, Santa Fe Hybrid, Sonata Hybrid, Staria Hybrid and other current models. It does not ground Bayon, Creta, i10, i20, or i30 N as current if those are absent from current model list.

### Jaguar / JLR
- `https://www.jaguar.com/en-xi/jdx/jaguar-range/f-pace/index.html`
- Jaguar global wording indicates F-PACE creation has concluded. XE, XF and F-Type are production-ended/historical around 2024. Keep 2024 unless exact Israeli current source exists.

### Jeep Israel
- `https://www.jeep.com/il/`
- Current Jeep Israel model list shows Wrangler and Avenger. It does not show Compass/Renegade as current. Use exact Wrangler source matching before setting old rows to null.

---

## RUN 02 profile-level directives

### 1. Citroen | C3 — DEFINITE CHANGE / SPLIT
Suspect: 1.2L turbo 110hp 6-speed automatic, 2017-2024.
- New/current C3 exists in Citroen Israel context.
- Keep old 2017-2024 row if the current engine/spec is different.
- Add/split a current C3 row only if official current Israeli spec grounds body, fuel, engine, hp and transmission.
- Set model-level `year_end: null` once current row is grounded.

### 2. Citroen | C3 Aircross — CONDITIONAL
Suspect: Shine/Shine PK/MAX 1.2T 130hp 6AT, 2020-2024.
- Do not blindly currentize old trim/powertrain.
- If exact current C3 Aircross source supports the row, set `year_end: null`.
- Otherwise retain 2024 and add note.

### 3. Citroen | C4 — CONDITIONAL
Suspect: 1.2T 130hp 8AT Crossover, 2021-2024.
- If exact current C4 Israeli source supports same powertrain, set row/model current.
- If current C4 differs, keep old row at 2024 and split current row.

### 4. Citroen | C5 X — RETAIN 2024
Suspect rows: 1.2T 130, 1.6T 180, PHEV 225, all 2023-2024.
- Keep 2024 unless exact official/current Israeli C5 X source exists.
- Do not use C5 Aircross evidence for C5 X.

### 5. Citroen | Jumper — RETAIN 2024 FOR OLD ROWS
Suspect old rows: 2.2 diesel 140/165 manual.
- Keep old 140/165 manual rows at 2024 unless exact current Jumper source supports them.
- Do not alter already-current/newer rows if present.

### 6. Citroen | Jumpy — RETAIN 2024 FOR OLD ROWS
Suspect old rows: diesel 150 manual, 120 manual, 177 automatic.
- Keep old rows at 2024 unless exact current Jumpy source supports same rows.

### 7. Citroen | SpaceTourer — RETAIN 2024
Suspect: Business 2.0 diesel 177hp 8AT, 2019-2024.
- Keep 2024 unless exact current Israeli SpaceTourer sale/spec source exists.

### 8. Cupra | Ateca — RETAIN 2024
Suspect: 2.0T 300hp AWD, 2019-2024.
- Keep 2024 unless exact current Israeli CUPRA Ateca source exists.

### 9. Cupra | Born — RETAIN 2024
Suspect: EV 204hp RWD, 2022-2024.
- Keep 2024 unless current Israeli CUPRA Born page/price list proves active sale.

### 10. Cupra | Formentor — CONDITIONAL
Suspect old rows: 1.5T 150, VZ 310, 2.0T 190, PHEV 204.
- Formentor is likely current in Israel, but old powertrains/trim labels may have changed.
- If exact old row still exists in current Israeli source, set it to `null`.
- Otherwise keep old rows and add/split current rows only when exact source supports them.

### 11. Cupra | Leon — CONDITIONAL
Suspect old rows: VZ PHEV 245, VZ Estate 310, 2.0T 190.
- Keep old rows unless exact current Israeli Leon source supports the same rows.

### 12. Dacia | Jogger — DEFINITE CHANGE / EXACT ROW CHECK
Suspect: 1.0T 110 manual.
- Dacia Israel lists Jogger as current.
- If the official brochure supports 1.0T 110 manual, set row `year_end: null`.
- If current Jogger is hybrid/different, retain old row at 2024 and add/split current row.

### 13. Dodge | Durango — RETAIN 2024
Suspect rows: GT V6, R/T 5.7 V8, SRT 392, SRT Hellcat.
- Global Dodge continuity is not Israeli proof.
- Keep 2024 unless exact Israeli/current import evidence exists.

### 14. DS Automobiles | DS 4 — DEFINITE CHANGE / SPLIT
Suspect rows: Trocadero/Performance Line petrol 225 and Trocadero/Rivoli E-Tense 225.
- Use DS Israel price list/current source.
- Set matching current E-Tense rows to `null` if exact.
- Keep petrol rows at 2024 unless exact current source supports them.
- Set model-level `year_end: null` after current row is grounded.

### 15. DS Automobiles | DS 7 — DEFINITE CHANGE / SPLIT
Suspect rows: 1.5 diesel 130, PHEV 225/300/360.
- Current DS 7 may be grounded from DS Israel online/source pages.
- Keep diesel at 2024 unless current diesel source exists.
- Currentize/split matching PHEV rows only if exact current source supports them.

### 16. DS Automobiles | DS 9 — RETAIN 2024
Suspect rows: Rivoli PHEV 250, Opera PHEV 360.
- Keep 2024 unless official DS Israel current source shows DS 9 as active.

### 17. Ferrari | 812 Superfast — RETAIN 2024
- Keep 2024. Treat as historical/successor-replaced.

### 18. Ferrari | Portofino — RETAIN 2024
- Keep Portofino M row at 2024 unless exact Israeli current source exists.

### 19. Fiat | 500e — DEFINITE CHANGE / SPLIT
Suspect rows: Action 95hp Hatchback, Icon 118hp Hatchback, La Prima 118hp Convertible.
- Fiat 500e is current if official Fiat Israel current source supports it.
- If current trim/body labels differ, keep old rows and add/split current rows.
- Set model-level `year_end: null` after grounding current row.

### 20. Ford | Bronco — DEFINITE CHANGE
Suspect rows: 2.3T 300, 2.7 V6 330, 3.0 V6 418/Raptor.
- Ford Israel current model list includes Bronco and Bronco Raptor.
- Set exact matching rows to `null` where current source supports engine/hp.
- Set model-level `year_end: null`.

### 21. Ford | Explorer — DEFINITE CHANGE / SPLIT
Suspect rows: Limited RWD/AWD 2.3T, ST 3.0, Platinum 3.0.
- Ford Israel current list includes Explorer.
- If generation/spec differs, preserve old rows at 2024 and add/split current Explorer row(s).
- Set model-level `year_end: null` once current row is grounded.

### 22. Ford | F-150 — RETAIN 2024
- Keep 2024 unless exact Ford Israel/current import source supports active F-150 new sale.

### 23. Ford | Kuga — RETAIN 2024
- Keep 2024 unless exact current Israeli Kuga source exists.

### 24. Ford | Mustang Mach-E — RETAIN 2024
- Keep 2024 unless Ford Israel current source supports Mach-E active sale.

### 25. Ford | Puma — RETAIN 2024
- Keep 2024 unless exact current Ford Israel Puma source exists.

### 26. Ford | Transit — CONDITIONAL
- If Ford commercial Israel current source supports exact rows, set matching rows to `null`.
- Otherwise retain old diesel rows at 2024.

### 27. Geely | Geometry C — CONDITIONAL
- Currentize only if active/current sale is grounded by official source or repo-local source.
- If page is legacy, retain 2024.

### 28. Genesis | G70 — RETAIN 2024
- Keep 2024 unless exact current G70 Israeli source exists.

### 29. Genesis | GV70 — RETAIN 2024 FOR ELECTRIFIED ROW
- Do not use current GV70 gasoline evidence to currentize Electrified GV70.
- Keep electric row at 2024 unless exact current electric GV70 source exists.

### 30. Hongqi | E-HS9 — RETAIN 2024
- Keep 2024 unless official current E-HS9 source exists.

### 31. Hyundai | Bayon — RETAIN 2024
- Current Hyundai visible model context does not ground Bayon.
- Keep 2024 unless exact current Israeli Bayon source exists.

### 32. Hyundai | Creta — RETAIN 2024
- Keep 2024 unless exact current Israeli Creta source exists.

### 33. Hyundai | i10 — RETAIN 2024
- Keep 2024 unless exact current i10 source exists.

### 34. Hyundai | i20 — RETAIN 2024
- Keep 2024 unless exact current i20 source exists.

### 35. Hyundai | i30 N — RETAIN 2024
- Keep 2024 unless exact current i30 N source exists.

### 36. Hyundai | Ioniq 5 — DEFINITE CHANGE / SPLIT
- IONIQ 5 is current in Hyundai Israel context.
- Keep old 217/305 rows at 2024 unless exact current source supports same figures.
- Add/split current IONIQ 5 rows if current spec differs.

### 37. Hyundai | Ioniq 6 — DEFINITE CHANGE
- IONIQ 6 is current in Hyundai Israel context.
- If current source supports 151hp RWD and 325hp AWD, set matching rows to `null`; otherwise split current rows.

### 38. Hyundai | Palisade — DEFINITE CHANGE / SPLIT
- Current Hyundai Israel context supports Palisade Hybrid.
- Keep old 3.8 V6 rows at 2024.
- Add/split current Palisade Hybrid row if not already present.

### 39. Hyundai | Santa Fe — DEFINITE CHANGE / SPLIT
- Current Hyundai Israel context supports Santa Fe Hybrid.
- Keep old diesel at 2024.
- Currentize or split hybrid row only if exact current source supports it.

### 40. Hyundai | Sonata — DEFINITE CHANGE / SPLIT
- Current Hyundai Israel context supports Sonata Hybrid.
- Keep old 1.6T petrol at 2024.
- Add/split current Sonata Hybrid if not already present.

### 41. Hyundai | Staria — DEFINITE CHANGE / SPLIT
- Current Hyundai Israel context supports Staria Hybrid.
- Keep old diesel rows at 2024.
- Add/split current Staria Hybrid if not already present.

### 42. Infiniti | QX60 — RETAIN 2024
- Keep 2024 unless exact Israeli current source exists.

### 43. Jaguar | F-Pace — RETAIN 2024
- Keep 2024 unless exact current Israeli F-Pace source exists.
- Global legacy/stock pages are not enough.

### 44. Jaguar | F-Type — RETAIN 2024
- Keep 2024. Production ended around 2024; do not currentize.

### 45. Jaguar | XE — RETAIN 2024
- Keep 2024. Treat as ended/historical.

### 46. Jaguar | XF — RETAIN 2024
- Keep 2024. Treat as ended/historical.

### 47. Jeep | Avenger — NO YEAR_END ACTION
- No variant-level 2024 patch required unless repo data is inconsistent.
- Keep current/null if already current.

### 48. Jeep | Compass — RETAIN 2024
- Jeep Israel current model list does not show Compass.
- Keep 2024 unless exact current Israeli source exists.

### 49. Jeep | Renegade — RETAIN 2024
- Jeep Israel current model list does not show Renegade.
- Keep 2024 unless exact current Israeli source exists.

### 50. Jeep | Wrangler — DEFINITE CHANGE / EXACT ROW CHECK
- Jeep Israel current model list shows Wrangler.
- Set exact current Wrangler rows to `null` if current source supports same powertrain.
- If old rows differ, preserve old rows and add/split current Wrangler row.
- Set model-level `year_end: null` after grounding current row.

---

## Validation commands

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

---

## Final report required from Codex

Codex must report profile-level counts, not only variant counts:

```text
RUN 02 FINAL REPORT
Profiles changed/currentized/split: <N>/50
Profiles retained at 2024: <N>/50
Profiles conditional/no-change due to missing exact source: <N>/50
Profiles with no year_end action: <N>/50
Remaining variant rows with year_end=2024 in RUN 02: <N>
Validation: <commands + pass/fail>
```


---

# EMBEDDED FILE: CODEX_YEAR_END_2024_RUN_01_02_REVALIDATION_PATCH_TASK.md


# CODEX TASK — YEAR_END 2024 — RUN 01 + RUN 02 REVALIDATION PATCH

Source file to edit: `model_technical_catalog_il.json`

Purpose: revise the first two `year_end: 2024` correction tasks after stricter revalidation. The earlier split was too conservative: many profiles marked “retain 2024” or “conditional” should actually be treated as **current model line / split-current required** when the model is still marketed in Israel in 2025/2026.

Important: this is still **not** a blind `2024 -> null` replacement. The rule is:

- If the same exact technical row is still current in official/current Israeli sources: set that row `year_end: null` and update model-level `year_end: null`.
- If the model line is current but the old 2024 powertrain/trim was replaced: keep the old row at `2024`, add/split the current grounded row, and set model-level `year_end: null`.
- If the model/dedicated variant is genuinely discontinued or not sold as a current Israeli new-car model: keep `2024` and document proof.
- If source support is weak: keep `2024`; do not fabricate current rows.

## Revised counts

### RUN 01 revised profile-level outcome
Out of 50 profiles:
- Definite change / currentize / split-current required: **32**
- Retain `year_end: 2024`: **15**
- Conditional exact-source check: **3**
- No action: **0**

Earlier RUN 01 was too conservative. The revalidation adds more current/split-current profiles, especially BMW, Audi, BYD, Chery, Bentley, Citroen Berlingo and Alfa Romeo Stelvio.

### RUN 02 revised profile-level outcome
Out of 50 profiles:
- Definite change / currentize / split-current required: **28**
- Retain `year_end: 2024`: **20**
- Conditional exact-source check: **2**
- No action: **0**

Earlier RUN 02 was too conservative. The revalidation adds more current/split-current profiles, especially Citroen commercial/current models, Cupra Formentor/Leon, DS 4/DS 7, Fiat 500e, Ford Bronco/Explorer, Hyundai current lineup, Genesis GV70/G70, Jeep Wrangler/Avenger and Geely Geometry C.

---

# RUN 01 — revised decisions

## Definite change / currentize / split-current required — 32 profiles

For these profiles, Codex must either set matching 2024 rows to `year_end: null`, or keep old 2024 rows and add/split current rows if the current Israeli source supports a different generation/powertrain. In all cases, the profile-level `year_end` must become `null` when a current row is grounded.

1. Abarth | 500 / canonical 595
2. Alfa Romeo | Stelvio
3. Audi | A5
4. Audi | A6
5. Audi | A8
6. Audi | e-tron GT
7. Audi | Q5
8. Audi | Q7
9. Audi | S3
10. Audi | SQ5
11. Bentley | Continental GT
12. Bentley | Flying Spur
13. BMW | 120i
14. BMW | 218i Gran Coupe
15. BMW | 318i
16. BMW | 320e
17. BMW | i4 eDrive35
18. BMW | iX xDrive40
19. BMW | M135i
20. BMW | M2
21. BMW | X2 M35i
22. BMW | X3 2.0i
23. BMW | X3 M40i
24. BMW | X3 xDrive30e
25. BMW | X6 M
26. BMW | Z4 sDrive20i
27. BYD | Atto 3
28. BYD | Dolphin
29. BYD | Han
30. BYD | Tang
31. Chery | Tiggo 7 Pro
32. Chery | Tiggo 8 Pro
33. Citroen | Berlingo

Note: this list has 33 line items because Citroen Berlingo was part of RUN 01 and is included as a definite change. If your local target count checker expects 32, treat BMW X6 M as conditional if no exact current Israeli M source is found. Otherwise count it as changed.

## Retain 2024 — 15 profiles

Keep `year_end: 2024` for old/discontinued or unsupported current Israeli rows. Add a note: `RUN01_REVALIDATED: 2024 retained because current Israeli continuity for this exact model/variant was not grounded or the model was replaced/discontinued.`

1. Aiways | U6
2. Audi | A4 — replaced by the new A5/S5 family; do not currentize old A4 rows.
3. Audi | R8 — discontinued.
4. Audi | RS4 — no current Israeli source found for old RS4 rows.
5. Audi | RS5 — no current Israeli source found for old RS5 rows.
6. Audi | RS7 — retain old 2024 rows unless exact current Israeli RS7 source exists.
7. BMW | 118i — current 1-series may continue, but exact 118i row not grounded.
8. BMW | 128ti — discontinued/not current.
9. BMW | 225xe Active Tourer PHEV — old PHEV row; do not currentize unless exact current 225xe source exists.
10. BMW | 640i GT — discontinued.
11. BMW | 850i — old 8-series/850i rows not grounded as current.
12. BMW | M8 — old M8 rows not grounded as current.
13. BMW | M850i — old 8-series/M850i rows not grounded as current.
14. Cadillac | XT5 — not shown in current Cadillac Israel model lineup.
15. Chevrolet | Camaro — sixth generation retired at model year 2024.
16. Chevrolet | Equinox — no current Israeli Chevrolet Equinox new-car source grounded.

Note: if using exactly 50 rows, this retain list plus changed/conditional should be reconciled by treating borderline BMW X6 M / RS7 according to local source evidence.

## Conditional exact-source check — 3 profiles

1. BMW | X3 M — if exact current X3 M source exists, split/currentize; otherwise retain 2024.
2. BMW | X6 M — if exact current X6 M Competition Israeli source exists, currentize/split; otherwise retain 2024.
3. Audi | RS7 — if exact current Israeli RS7 source exists, currentize/split; otherwise retain 2024.

---

# RUN 02 — revised decisions

## Definite change / currentize / split-current required — 28 profiles

1. Citroen | C3
2. Citroen | C3 Aircross
3. Citroen | C4
4. Citroen | Jumper
5. Citroen | Jumpy
6. Cupra | Formentor
7. Cupra | Leon
8. Dacia | Jogger
9. DS Automobiles | DS 4
10. DS Automobiles | DS 7
11. Fiat | 500e
12. Ford | Bronco
13. Ford | Explorer
14. Geely | Geometry C
15. Genesis | G70
16. Genesis | GV70
17. Hyundai | Bayon
18. Hyundai | i10
19. Hyundai | i20
20. Hyundai | Ioniq 5
21. Hyundai | Ioniq 6
22. Hyundai | Palisade
23. Hyundai | Santa Fe
24. Hyundai | Sonata
25. Hyundai | Staria
26. Jeep | Avenger
27. Jeep | Wrangler
28. Citroen | Berlingo if it was not already patched in RUN 01 merge context; otherwise ignore here.

For Hyundai: use official Hyundai Israel price list/current lineup. If the current exact powertrain differs from the old 2024 row, keep the old row and add/split the current row.

For Ford: official Ford Israel current model list clearly supports Bronco, Bronco Raptor and Explorer. Do not currentize F-150/Kuga/Mach-E/Puma from global availability.

For Citroen: official Citroen Israel pages support new/current C3, C3 Aircross, C4/Jumpy/Jumper context. Split old powertrains when the current spec differs.

## Retain 2024 — 20 profiles

1. Citroen | C5 X — do not confuse with C5 Aircross.
2. Citroen | SpaceTourer — retain unless exact current source exists.
3. Cupra | Ateca — not a current priority/current Israel row unless exact source exists.
4. Cupra | Born — do not use global Cupra current status unless current Israeli sale is grounded.
5. Dodge | Durango — no official current Israeli source.
6. DS Automobiles | DS 9 — not current in DS Israel context.
7. Ferrari | 812 Superfast — successor/replaced; historical.
8. Ferrari | Portofino — Portofino M historical unless exact current Israeli source exists.
9. Ford | F-150 — not in official Ford Israel current model list.
10. Ford | Kuga — not in official Ford Israel current model list.
11. Ford | Mustang Mach-E — not in official Ford Israel current model list.
12. Ford | Puma — not in official Ford Israel current model list.
13. Hongqi | E-HS9 — current Israel evidence not grounded.
14. Hyundai | Creta — no current Hyundai Israel evidence grounded.
15. Hyundai | i30 N — not grounded as current.
16. Infiniti | QX60 — no official current Israeli source grounded.
17. Jaguar | F-Pace — Jaguar production/new-car continuity is ending; do not currentize.
18. Jaguar | F-Type — discontinued.
19. Jaguar | XE — discontinued/historical.
20. Jaguar | XF — discontinued/historical.
21. Jeep | Compass — not in current Jeep Israel model list.
22. Jeep | Renegade — not in current Jeep Israel model list.

Note: if enforcing exactly 50 profile decisions, reconcile by excluding Citroen Berlingo duplicate and treating Transit/SpaceTourer as conditional below.

## Conditional exact-source check — 2 profiles

1. Ford | Transit — currentize only if a Ford Israel commercial-vehicle source grounds the exact Transit row; otherwise retain 2024.
2. Citroen | SpaceTourer — currentize only if official current Israeli SpaceTourer sale/spec source exists; otherwise retain 2024.

---

# Required patch mechanics

For each changed/currentized profile:

1. Add a current Israeli source to `sources` if not already present.
2. Use a real numeric `source_index`, never placeholders.
3. Update `source_indexes` and `field_sources.year_end` for every row changed to `null`.
4. If adding/splitting a current row, fill every required field and validate EV/hybrid schema.
5. Update `available_values_for_website` after any added/split row.
6. Add notes:
   - `RUN01_REVALIDATED` or `RUN02_REVALIDATED`
   - whether 2024 was a cutoff bug, a real end year, or an old-row end with current split.
7. Do not change unrelated profiles outside RUN 01/RUN 02.

# Required validation commands

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

# Final report required from Codex

Codex must report:

- RUN 01: profiles changed, retained, conditional unresolved.
- RUN 02: profiles changed, retained, conditional unresolved.
- Remaining `year_end: 2024` count in RUN 01/RUN 02 after patch.
- Any profile where exact-source matching prevented changing old 2024 rows.
- Validation command outputs.


---

# EMBEDDED FILE: CODEX_YEAR_END_2024_RUN_03_FIX_TASK.md


# CODEX TASK — YEAR_END 2024 SYSTEMIC CORRECTION — RUN 03 / 50 PROFILES

Source file to edit: `model_technical_catalog_il.json`

This task fixes only the `year_end: 2024` cutoff artifact for RUN 03 profiles. Do **not** do a blind `2024 -> null` replacement.

## Run 03 profile-level summary

Out of 50 profiles:

- Definite change / currentize / split-current required: **36**
- Retain `year_end: 2024`: **10**
- Conditional exact-source check: **4**
- No action: **0**

“Change” means profile-level correction and/or current-row split. It does **not** mean every old 2024 variant becomes `null`. If a model line is current but the old row is not exact-current, keep the old row at 2024 and add/split the current grounded row.

---

## Hard rules

1. Scope is only the 50 RUN 03 profiles listed below.
2. Never mass-replace all `year_end: 2024` values.
3. If the exact technical row is current in Israeli sources, set that row `year_end: null`.
4. If the model line is current but the exact 2024 row is old, keep old row at `2024`, add/split current grounded row, and set model-level `year_end: null`.
5. If the model/variant is discontinued/replaced/not grounded as current in Israel, retain `2024` and add a note.
6. Duplicates in this run must be merged/canonicalized if they represent the same make/model profile: Lamborghini Huracan, Range Rover Velar, Lexus ES, Mazda CX-3, Mazda2.
7. Do not introduce `review`, `indirect`, fake URLs, placeholder source indexes, or broken `field_sources`.
8. For EV rows: `engine_displacement_l` must remain `null`; transmission should follow repo EV convention, normally `single_speed`.

---

## Embedded source anchors to use

Use repo-local evidence first, but these web anchors are the intended current validation facts for Codex. Codex does not need to browse.

- Kia Israel all-models/current lineup: `https://kia-israel.co.il/רכב` — current lineup includes Stonic, Sorento Hybrid and Carnival Hybrid.
- Land Rover Israel price list 2026: `https://www.landrover.co.il/offers-and-finance/pricelist` — supports 2026 Discovery, Discovery Sport, Range Rover Sport, Velar and Evoque current rows.
- Lexus Israel new-car page: `https://www.lexus.co.il/new-cars` — supports current UX, LBX and Lexus new-car lineup context.
- Mercedes-Benz Israel models page: `https://www.mercedes-benz.co.il/models/` — supports current A-Class, C-Class, CLE, E-Class, EQS, G-Class, GLA, GLB, GLS, S-Class and related model families.
- Mazda Israel current models page: `https://www.mazda.co.il/models` — supports current CX-5 and current Mazda lineup; also shows new 2026 CX-5 context.
- Mazda CX-5 2026 Israel launch article: `https://www.cartube.co.il/חדשות-רכב/מאזדה-cx-5-החדש-2026-נחת-בישראל-מחיר-189900-שקל`
- Leapmotor Israel T03 current page: `https://leapmotor.co.il/model-t03/`
- Lynk & Co Israel 2026 price-list article/page: `https://lynkco.co.il/lynk-co-israel-price-list/`
- Maserati Israel models page: `https://www.maserati.com/il/he/models`
- Reuters 2026 Maserati lineup refresh: `https://www.reuters.com/business/autos-transportation/maserati-refreshes-lineup-ahead-expected-strategic-reset-luxury-brand-2026-06-18/`

---

# RUN 03 scope and directives

## Definite change / currentize / split-current required — 36 profiles

### Kia
1. Kia | Carnival — currentize/split. Kia Israel lists Carnival Hybrid as current; keep old non-current rows at 2024 if powertrain differs, add/split current hybrid row if missing.
2. Kia | Sorento — currentize/split. Kia Israel lists Sorento Hybrid as current; keep old rows only if not exact.
3. Kia | Stonic — currentize exact matching rows if official current source supports them.

### Land Rover / Range Rover
4. Land Rover | Defender — currentize/split if current source exists in repo or price list; if not in price list but official Land Rover site supports current, use it.
5. Land Rover | Discovery — currentize exact 2026 current row per Land Rover Israel price list.
6. Land Rover | Discovery Sport — currentize exact 2026 current row per Land Rover Israel price list.
7. Land Rover | Range Rover — currentize/split current 2026 rows.
8. Land Rover | Range Rover Evoque — currentize/split current 2026 rows.
9. Land Rover | Range Rover Sport — currentize/split current 2026 rows.
10. Land Rover | Range Rover Velar DUP#1 — merge with DUP#2 and keep one canonical current Velar profile.
11. Land Rover | Range Rover Velar DUP#2 — merge into canonical Velar, preserve all grounded rows/sources.

### Leapmotor / Lexus / Lynk & Co
12. Leapmotor | T03 — currentize; official Leapmotor Israel T03 page supports current sale.
13. Lexus | ES DUP#1 — merge/canonicalize and currentize/split only if current Lexus Israel ES source exists.
14. Lexus | ES DUP#2 — merge into canonical ES.
15. Lexus | LBX — currentize; Lexus Israel new-cars page supports LBX.
16. Lexus | UX — currentize exact matching rows; Lexus Israel new-cars page supports UX.
17. Lynk & Co | 01 — currentize if repo-local/Israel price source supports 2026 01; otherwise keep old row and add current row from source.

### Maserati / Mazda / McLaren
18. Maserati | GranCabrio — currentize/split if Maserati Israel/current Maserati lineup source supports GranCabrio; otherwise use global current source only as weak support and keep source notes clear.
19. Maserati | Grecale — currentize/split; current Maserati lineup refresh and Israel model context support Grecale as current.
20. Mazda | CX-5 — currentize/split; Mazda Israel and 2026 launch source support current CX-5.
21. Mazda | Mazda2 DUP#1 — merge/canonicalize; currentize if Mazda Israel source supports current Mazda2, otherwise retain old rows.
22. Mazda | Mazda2 DUP#2 — merge into canonical Mazda2.
23. Mazda | MX-5 — currentize only if current Mazda Israel source supports MX-5; if not, keep 2024.
24. McLaren | Artura — currentize exact row if current Israeli/importer source or repo-local source supports it; otherwise conditional.

### Mercedes-Benz
25. Mercedes-Benz | A-Class — currentize/split.
26. Mercedes-Benz | C-Class — currentize/split.
27. Mercedes-Benz | Citan — currentize/split if Mercedes commercial/current source supports exact Citan rows.
28. Mercedes-Benz | CLE — currentize; current Mercedes Israel model page supports CLE.
29. Mercedes-Benz | E-Class — currentize; current Mercedes Israel model page supports E-Class.
30. Mercedes-Benz | EQS — currentize; current Mercedes Israel model page supports EQ/EQS family.
31. Mercedes-Benz | EQS SUV — currentize/split if current source supports SUV body specifically.
32. Mercedes-Benz | EQV — currentize/split if current Mercedes Israel/current commercial source supports EQV.
33. Mercedes-Benz | G-Class — currentize; current Mercedes Israel model page supports G-Class/Electric G-Class context.
34. Mercedes-Benz | GLA — currentize/split.
35. Mercedes-Benz | GLB — currentize/split.
36. Mercedes-Benz | GLS — currentize/split.
37. Mercedes-Benz | Maybach GLS — currentize/split if exact current Maybach GLS source exists; otherwise conditional.
38. Mercedes-Benz | S-Class — currentize/split.

Note: the definite-change list intentionally includes 38 line items because duplicate profiles must be merged. After merging duplicates, the effective changed profile count is **36**.

---

## Retain `year_end: 2024` — 10 profiles

1. Kia | Ceed SW — not shown as current in Kia Israel lineup; retain 2024 unless exact source exists.
2. Lamborghini | Huracan DUP#1 — Huracan replaced/discontinued; retain historical 2024 and merge duplicates.
3. Lamborghini | Huracan DUP#2 — merge into canonical Huracan; retain 2024.
4. Lexus | LC — retain 2024 unless exact current Lexus Israel LC source exists.
5. Lexus | LS — retain 2024 unless exact current Lexus Israel LS source exists.
6. Maserati | Ghibli — retain 2024 / historical; Ghibli sedan is not current in updated Maserati lineup.
7. Maserati | Quattroporte — retain 2024 / historical; Quattroporte is not current in updated Maserati lineup.
8. Maxus | Euniq 5 — retain 2024 unless exact current Maxus Israel source exists.
9. Maxus | Euniq 6 — retain 2024 unless exact current Maxus Israel source exists.
10. Mazda | CX-3 DUP#1 — CX-3 not current in Mazda Israel lineup; merge duplicates and retain historical 2024.
11. Mazda | CX-3 DUP#2 — merge into canonical CX-3; retain historical 2024.

Note: duplicate merge means effective retained profile count is **10**.

---

## Conditional exact-source check — 4 profiles

1. Mazda | Mazda2 — if current Mazda Israel source supports Mazda2, currentize; otherwise retain old row at 2024. Merge duplicate profiles either way.
2. Mazda | MX-5 — if current Mazda Israel source supports MX-5, currentize; otherwise retain 2024.
3. McLaren | Artura — currentize only with exact Israeli/importer source; global source alone is insufficient.
4. Mercedes-Benz | B-Class — currentize only if exact current Mercedes Israel B-Class source exists; otherwise retain 2024.

---

# Required duplicate cleanup

For these duplicate pairs, Codex must leave only one canonical profile per `(market, make, model)` unless repo schema intentionally separates by market confidence bucket. Preserve all valid sources/notes/technical rows and add lineage note:

- Lamborghini | Huracan
- Land Rover | Range Rover Velar
- Lexus | ES
- Mazda | CX-3
- Mazda | Mazda2

If duplicate rows are identical, dedupe them. If complementary, merge sources and variants.

---

# Required patch mechanics

For every changed profile:

1. Add/keep a current source in `sources`.
2. Use real numeric `source_index` values only.
3. Update `source_indexes`, `field_sources.year_end`, and relevant supported fields.
4. Update `available_values_for_website` after adding/splitting rows.
5. Add notes:
   - `RUN03: year_end 2024 corrected as cutoff artifact` when changing to `null`.
   - `RUN03: old row retained at 2024; current row split because current Israeli source shows changed generation/powertrain` when splitting.
   - `RUN03: 2024 retained as historical/discontinued or ungrounded-current` when retaining.
6. Do not leave empty `technical_variants_il` profiles.
7. Do not create broken `source_indexes` or `field_sources`.

---

# Validation commands

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

# Final report required from Codex

- Profiles changed/currentized/split.
- Profiles retained at 2024 with evidence.
- Duplicate profiles merged.
- Remaining `year_end: 2024` count within RUN 03.
- Validation command results.


---

# EMBEDDED FILE: CODEX_YEAR_END_2024_RUN_04_FIX_TASK.md


# CODEX TASK — YEAR_END 2024 SYSTEMIC CORRECTION — RUN 04 / 50 PROFILES

Source file to edit: `model_technical_catalog_il.json`

This task fixes only the `year_end: 2024` cutoff artifact for RUN 04 profiles. Do **not** do a blind `2024 -> null` replacement.

## Run 04 profile-level summary

Out of 50 profiles:

- Definite change / currentize / split-current required: **37**
- Move to deferred retained/final review: **11**
- Conditional exact-source check: **2**
- No action: **0**

Meaning of “change”: at profile level, a change includes any of these:
- setting exact matching current rows from `year_end: 2024` to `null`;
- keeping old 2024 rows but adding/splitting a grounded current row;
- correcting a wrong `2024` to a more precise historical end year, e.g. Mitsubishi ASX to 2025 if source proves 2010–2025;
- merging duplicate profiles while preserving grounded rows/sources.

---

## Hard rules

1. Scope is only the 50 RUN 04 profiles listed below.
2. Never mass-replace all `year_end: 2024` values.
3. If the exact technical row is current in Israeli sources, set that row `year_end: null`.
4. If the model line is current but the exact 2024 row is old, keep old row at `2024`, add/split the current grounded row, and set model-level `year_end: null`.
5. If a source proves a different historical end year, correct `2024` to that exact year instead of leaving a fake 2024.
6. If the model/variant is discontinued/replaced/not grounded as current in Israel, move it to the deferred final-review run, do not currentize it.
7. Duplicates in this run must be merged/canonicalized where applicable: Opel Grandland.
8. Do not introduce `review`, `indirect`, fake URLs, placeholder source indexes, or broken `field_sources`.
9. For EV rows: `engine_displacement_l` must remain `null`; transmission should follow repo EV convention, normally `single_speed`.

---

## Embedded source anchors to use

Use repo-local evidence first, but these web anchors are the intended current validation facts for Codex. Codex does not need to browse.

### Mercedes-Benz / vans
- Mercedes-Benz Israel models page: `https://www.mercedes-benz.co.il/models/`
- Mercedes-Benz Israel V-Class page: `https://www.mercedes-benz.co.il/vans/van-models/v-class/`
- Current Israeli secondary support for V-Class 2026: `https://www.carzone.co.il/Mercedes-Benz/Vito/V-Class/2026/`

### MG Israel
- MG Israel official home/current models: `https://mg-israel.co.il/`
- MG4 official current price list: `https://mg-israel.co.il/pricelist/new-mg4/`
- MG online shop/current ordering page: `https://mg-israel.co.il/online-shop/`

### MINI Israel
- MINI Israel home/current lineup: `https://www.mini.co.il/he_IL/home.html`
- MINI Aceman current page: `https://www.mini.co.il/he_IL/home/range/all-electric-mini-aceman.html`
- MINI Cooper 5-door current price list page: `https://www.mini.co.il/he_IL/home/range/mini-cooper-5-door.html`
- MINI Cooper Cabrio current price list page: `https://www.mini.co.il/he_IL/home/range/mini-cooper-convertible.html`
- MINI Countryman current price list page: `https://www.mini.co.il/he_IL/home/range/mini-countryman.html`
- MINI Countryman Electric current page: `https://www.mini.co.il/he_IL/home/range/all-electric-mini-countryman.html`

### Mitsubishi Israel
- Mitsubishi Israel current models page: `https://www.mitsubishi-israel.co.il/models/`
- Mitsubishi Israel price list: `https://www.mitsubishi-israel.co.il/prices/`
- Mitsubishi ASX past-model page: `https://www.mitsubishi-israel.co.il/past_models/asx/`
- Mitsubishi Triton/L200 past-model page: `https://www.mitsubishi-israel.co.il/past_models/triton/`

### NIO Israel
- NIO Israel home/current lineup: `https://www.nio.co.il/`
- NIO Israel price list 02/2026: `https://www.nio.co.il/car-list`
- Delek Motors NIO Israel page: `https://www.delek-motors.co.il/יצרנים/nio/`

### Nissan Israel
- Nissan Israel new models page: `https://www.nissan.co.il/vehicles/new.html`
- Nissan Israel home: `https://www.nissan.co.il/`
- Nissan Leaf legacy page: `https://www.nissan.co.il/experience-nissan/legacy-models/leaf.html`
- Nissan Ariya 2026 Israeli secondary source: `https://www.auto.co.il/cars/nissan/ariya/`

### OMODA / ORA
- OMODA Israel official site: `https://omoda.co.il/`
- OMODA price list: `https://omoda.co.il/price-list/`
- Colmobil OMODA brand page: `https://www.colmobil.co.il/brands/omoda/`
- ORA Israel official site: `https://ora-israel.co.il/`
- Colmobil ORA brand page: `https://www.colmobil.co.il/brands/ora/`

### Opel / Peugeot
- Opel Israel current models page: `https://online.opel.co.il/model-2/`
- Opel Israel official site: `https://www.opel.co.il/`
- Peugeot Israel official online site: `https://online.peugeot.co.il/`
- Peugeot Israel/Carzone current-model support: `https://www.carzone.co.il/Peugeot/`

### Polestar / Porsche / RAM / Renault
- Polestar Israel official page: `https://www.polestar.com/en-il/`
- Polestar 2 official Israel page: `https://www.polestar.com/en-il/polestar-2/`
- Porsche Israel official site: `https://www.porsche.co.il/`
- Porsche 911 Israel configurator: `https://models.porsche.com/he-IL/model-start/911`
- RAM Israel official site: `https://www.ram.com/il/`
- RAM 2500 current Israeli secondary support: `https://www.auto.co.il/cars/ram/2500/`
- Renault Israel price list/current lineup: `https://www.renault.co.il/pricing.html`

---

# RUN 04 scope and directives

## Definite change / currentize / split-current required — 37 profiles

### Mercedes-Benz
1. Mercedes-Benz | SL — currentize/split if exact current SL source exists in Mercedes Israel model context; otherwise keep old row and add current grounded row if source supports it.
2. Mercedes-Benz | V-Class — currentize exact current V300 rows per Mercedes Israel vans/current V-Class page; set model-level `year_end: null`.
3. Mercedes-Benz | Vito — currentize/split only if Mercedes Israel/current commercial source supports exact Vito rows. If exact Vito row differs from old 2024 rows, keep old rows and add/split current.

### MG
4. MG | HS — currentize/split if MG Israel current source supports HS/HS Hybrid/EHS/PHEV continuity. If old HS rows do not match current powertrain, keep old rows at 2024 and add/split the current grounded row.
5. MG | MG4 — currentize; official MG4 price list is current. EV schema must remain displacement null.

### MINI
6. Mini | Aceman — currentize; official MINI Aceman EV page is current.
7. Mini | Cabrio — currentize/split; official MINI Cabrio 04/2026 price list supports current rows.
8. Mini | Cooper S — currentize/split; official MINI Cooper 5-door/3-door price list supports current Cooper S.
9. Mini | Cooper SE — currentize/split only if exact electric Cooper/Cooper SE source exists. If name changed to new MINI Cooper Electric, keep old SE row and add/split current EV row.
10. Mini | Countryman — currentize/split; official Countryman and Countryman Electric pages support current rows.

### Mitsubishi
11. Mitsubishi | ASX — do not leave fake 2024. Mitsubishi Israel marks ASX as past model 2010–2025; correct profile/variant `year_end` to 2025 if this matches the row, not `null`.

### NIO
12. NIO | EL6 — currentize; NIO Israel/Delek Motors and 02/2026 price list support current EL6.
13. NIO | ET5 — currentize; NIO Israel/Delek Motors and 02/2026 price list support current ET5.

### Nissan
14. Nissan | Ariya — currentize/split if Israeli 2026 source or repo-local source grounds current Ariya rows. Prefer official Nissan Israel if present; if only secondary Israeli 2026 source exists, add source note explaining secondary support.
15. Nissan | Juke — currentize/split; Nissan Israel new models page supports Juke as current.
16. Nissan | Qashqai — currentize/split; Nissan Israel new models page supports Qashqai as current.
17. Nissan | X-Trail — currentize/split; Nissan Israel new models page supports X-Trail as current.

### Opel
18. Opel | Astra — currentize/split if Opel Israel current lineup/source supports exact row; otherwise add/split current row.
19. Opel | Combo — currentize/split if Opel Israel commercial/current source supports exact Combo rows.
20. Opel | Corsa — currentize/split; Opel Israel current models page supports New Corsa/Corsa-e context.
21. Opel | Grandland DUP#1 — merge with DUP#2 and currentize/split current Grandland rows.
22. Opel | Grandland DUP#2 — merge into canonical Grandland, preserving all grounded sources/variants.
23. Opel | Mokka — currentize/split; Opel Israel official site supports Mokka/Mokka Electric context.
24. Opel | Vivaro — currentize/split if Opel Israel commercial/current source supports exact Vivaro rows.

### ORA
25. Ora | Funky Cat — currentize/canonicalize carefully. If repo treats `Funky Cat` as old name for ORA 03, keep old Funky Cat row at 2024 and add/split current `ORA 03` row, or canonicalize according to repo convention. Use ORA Israel/Colmobil current source.

### Peugeot
26. Peugeot | 208 — currentize/split; Peugeot Israel/Israeli sources support current 208 MHEV.
27. Peugeot | 408 — currentize/split if Peugeot Israel/current Israeli source supports 408/e-408 rows; keep old row if powertrain differs.
28. Peugeot | Expert — currentize/split if Peugeot current commercial source supports Expert rows.
29. Peugeot | Rifter — currentize/split; Israeli 2026 Rifter support exists. Do not blindly currentize old powertrains if current facelift differs.

### Porsche / RAM
30. Porsche | 911 — currentize/split; Porsche Israel configurator supports current 911.
31. RAM | 1500 — currentize/split; old TRX rows may remain 2024, but current 1500/RHO/Rebel rows require grounded split if applicable.
32. RAM | 2500 — currentize/split; RAM Israel/Auto current support for 2500 exists.

### Renault
33. Renault | Arkana — currentize/split; Renault Israel price list supports current Arkana rows.
34. Renault | Austral — currentize/split; Renault Israel price list/current sources support current Austral.
35. Renault | Captur — currentize/split; Renault Israel price list supports current Captur.
36. Renault | Clio — currentize/split; Renault Israel price list supports current Clio.
37. Renault | Master — currentize/split if Renault Israel commercial/current source supports exact Master rows.

---

## Move to deferred retained/final review — 11 profiles

Do not currentize these inside RUN 04 unless repo-local or official current Israeli source clearly proves current exact rows. Add them to the final deferred retained run.

1. MG | Marvel R — no current MG Israel grounding found in this pass.
2. MG | ZS EV — old electric ZS EV row; do not confuse with current ZS Hybrid/other ZS successors.
3. Mini | Clubman — Clubman is historical/discontinued; retain/defer.
4. Mitsubishi | L200 — Mitsubishi Israel points to Triton/L200 context as past/historical; do not currentize.
5. Nissan | Altima — not in Nissan Israel current new-model list.
6. Nissan | Leaf — Nissan Israel marks Leaf as legacy model; do not currentize old Leaf rows.
7. Opel | Crossland — likely replaced/old model; currentize only if exact current Israel source exists, otherwise defer.
8. Polestar | 2 — Polestar Israel official site says no cars are currently available for purchase; do not currentize based only on secondary listings.
9. Porsche | 718 Boxster — treat as historical/discontinued unless Porsche Israel has exact current 718/Boxster source.
10. Renault | Koleos — not in Renault Israel current price list; defer.
11. Renault | Megane — old ICE Megane profile; do not confuse with Megane E-Tech.

---

## Conditional exact-source check — 2 profiles

1. Omoda | C5 — currentize/split only if official OMODA/Colmobil price list or current source uses exact `C5`/`OMODA 5` naming that maps to this profile. If official site only shows OMODA 7/9 and C5 is not yet grounded as current, defer.
2. Renault | Megane E-Tech — currentize only if Renault Israel official source/price list supports current Megane E-Tech. If only secondary/Yad2 support exists, defer to final review.

---

# Required duplicate cleanup

- Opel | Grandland DUP#1 + DUP#2 must leave one canonical profile. Merge rows/sources; dedupe identical variants; preserve valid notes and source lineage.

---

# Required patch mechanics

For every changed profile:

1. Add/keep a current source in `sources`.
2. Use real numeric `source_index` values only.
3. Update `source_indexes`, `field_sources.year_end`, and relevant supported fields.
4. Update `available_values_for_website` after adding/splitting rows.
5. Add notes:
   - `RUN04: year_end 2024 corrected as cutoff artifact` when changing to `null`.
   - `RUN04: old row retained at 2024; current row split because current Israeli source shows changed generation/powertrain` when splitting.
   - `RUN04: year_end corrected from 2024 to exact historical end year` when a source proves another end year, e.g. ASX 2025.
   - `RUN04: moved to deferred final review; not currentized without exact Israeli source` when deferring.
6. Do not leave empty `technical_variants_il` profiles.
7. Do not create broken `source_indexes` or `field_sources`.

---

# Validation commands

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

# Final report required from Codex

- Profiles changed/currentized/split.
- Profiles corrected to a non-2024 historical end year.
- Profiles deferred to final retained run.
- Conditional profiles unresolved.
- Duplicate profiles merged.
- Remaining `year_end: 2024` count within RUN 04.
- Validation command results.


---

# EMBEDDED FILE: CODEX_YEAR_END_2024_RUN_05_FIX_TASK.md


# CODEX TASK — YEAR_END 2024 SYSTEMIC CORRECTION — RUN 05 / 50 PROFILES

Source file to edit: `model_technical_catalog_il.json`

This task fixes only the `year_end: 2024` cutoff artifact for RUN 05 profiles. Do **not** do a blind `2024 -> null` replacement.

## Run 05 profile-level summary

Out of 50 profile entries:

- Definite change / currentize / split-current required: **36**
- Move to deferred retained/final review: **14**
- Conditional exact-source check: **0**
- No action: **0**

Meaning of “change”: at profile level, a change includes any of these:
- setting exact matching current rows from `year_end: 2024` to `null`;
- keeping old 2024 rows but adding/splitting a grounded current row;
- merging duplicate profiles while preserving grounded rows/sources;
- canonicalizing a renamed current model, e.g. C40 Recharge -> EC40, while retaining old-name rows if needed.

## Hard rules

1. Scope is only the 50 RUN 05 profile entries listed in the original run file.
2. Never mass-replace all `year_end: 2024` values.
3. If the exact technical row is current in Israeli sources, set that row `year_end: null`.
4. If the model line is current but the exact 2024 row is old, keep old row at `2024`, add/split the current grounded row, and set model-level `year_end: null`.
5. If the model was renamed, do not fake continuity under the old name. Either canonicalize by repo convention or keep old row ending 2024 and add the renamed current model row.
6. If the model/variant is discontinued/replaced/not grounded as current in Israel, move it to the deferred final-review run, do not currentize it.
7. Duplicates in this run must be merged/canonicalized where applicable: Toyota Aygo X, Toyota Highlander, Toyota Proace City, Volkswagen Arteon, Volkswagen ID.3.
8. Do not introduce `review`, `indirect`, fake URLs, placeholder source indexes, or broken `field_sources`.
9. For EV rows: `engine_displacement_l` must remain `null`; transmission should follow repo EV convention, normally `single_speed`.

## Embedded source anchors

Use repo-local sources first. Codex must not browse. Add/replace sources with real numeric `source_index` values only.

- Renault Israel home/current lineup: https://www.renault.co.il/
- Renault Israel price list: https://www.renault.co.il/pricing.html
- Renault Israel Trafic Van current page: https://www.renault.co.il/cars/traficp/index.html
- Seat Israel home/current lineup: https://www.seat.co.il/
- Skoda Israel models/current lineup: https://www.skoda.co.il/models/
- Skoda Karoq price/current page: https://www.skoda.co.il/models/karoq/
- Skoda Kodiaq current page: https://www.skoda.co.il/models/kodiaq/
- Skoda Octavia current page: https://www.skoda.co.il/models/octavia/
- Skoda Octavia RS current page: https://www.skoda.co.il/models/octavia-rs/
- Skoda Scala current page: https://www.skoda.co.il/models/scala/
- Skywell Israel official ET5 page: https://skywell.co.il/
- KGM/Torres official page: https://kgm.co.il/model/torres/
- KGM/Torres Hybrid official page: https://kgm.co.il/model/torres-hybrid/
- Subaru Israel current lineup: https://subaru.co.il/
- Suzuki Israel price list: https://suzuki.co.il/prices
- Tesla Israel Model X page: https://www.tesla.com/he_il/modelx
- Toyota Israel new-cars price/current page: https://www.toyota.co.il/new-cars
- Toyota Aygo X current page: https://www.toyota.co.il/new-cars/aygo-x
- Toyota Corolla Sedan current page: https://www.toyota.co.il/new-cars/corolla-sedan
- Toyota Corolla Cross current page: https://www.toyota.co.il/new-cars/corolla-cross
- Toyota Highlander current page: https://www.toyota.co.il/new-cars/highlander
- Toyota Hilux current page: https://www.toyota.co.il/new-cars/hilux
- Toyota Proace City / Toyota City current page: https://www.toyota.co.il/new-cars/proace-city-verso
- Toyota Yaris build/spec pages: https://www.toyota.co.il/new-cars/yaris/build and https://www.toyota.co.il/new-cars/yaris/specifications
- Toyota Yaris Cross current page: https://www.toyota.co.il/new-cars/yaris-cross
- Volkswagen Israel current models page: https://www.vw.co.il/models/
- Volkswagen Commercial Israel current site: https://vwcv.co.il/
- Volkswagen Caddy current page: https://vwcv.co.il/models/caddy/
- Volkswagen Commercial catalogs: https://vwcv.co.il/catalogs/
- Auto Israel VW Touareg note: https://www.auto.co.il/cars/volkswagen/touareg/
- Auto Israel ID.4 current support: https://www.auto.co.il/cars/volkswagen/id4/
- Auto Israel ID.5 current support: https://www.auto.co.il/cars/volkswagen/id5/
- Carzone VW 2026 current price support: https://www.carzone.co.il/Volkswagen/
- Volvo Israel EC40 page: https://www.volvocars.com/il/cars/ec40-electric/
- Volvo Israel price list: https://www.volvocars.com/il/l/pricing/


---

# RUN 05 scope and directives

## Definite change / currentize / split-current required — 36 profile entries

### 1. Renault | Trafic
ACTION: **CHANGE/SPLIT**
DIRECTIVE: Official Renault Israel Trafic Van page is current; old 170hp 2020-2024 row should not be blindly opened if current official row is 150hp. Keep old row at 2024 if exact 170hp not current, add/split current 2.0 diesel 150hp row and set model year_end=null.

### 2. Seat | Arona
ACTION: **CHANGE/SPLIT**
DIRECTIVE: Seat Israel currently advertises Arona/Ibiza; current 2026 refresh may differ from old 110/150hp rows, so split exact current rows if needed.

### 3. Seat | Ibiza
ACTION: **CHANGE/SPLIT**
DIRECTIVE: Seat Israel currently advertises Ibiza; set matching current rows to null or split current refresh rows.

### 4. Skoda | Karoq
ACTION: **CHANGE**
DIRECTIVE: Skoda Israel Karoq current price list 26.03.2026 supports current Karoq 1.5 TSI.

### 5. Skoda | Kodiaq
ACTION: **CHANGE/SPLIT**
DIRECTIVE: Skoda Israel current Kodiaq page supports new Kodiaq; old diesel/190hp rows may remain 2024, add/split current 1.5 TSI 150, 2.0 TSI 204, and supported diesel rows as grounded.

### 6. Skoda | Octavia
ACTION: **CHANGE/SPLIT**
DIRECTIVE: Skoda Israel current Octavia/Octavia RS pages and 2026 local sources support facelifted Octavia; split old 245hp RS/old rows and add current 115/150 MHEV and RS 265hp rows if grounded.

### 7. Skoda | Scala
ACTION: **CHANGE**
DIRECTIVE: Skoda Israel current Scala page supports current model; correct matching rows to null.

### 8. Skywell | ET5
ACTION: **CHANGE/SPLIT**
DIRECTIVE: Skywell Israel official page and 2026 Israeli price/news support ET5, especially XR86 86kWh; old 72kWh row must not be blindly opened if not current.

### 9. SsangYong | Torres
ACTION: **CHANGE/REBRAND**
DIRECTIVE: KGM Israel official pages show Torres and Torres Hybrid current. Canonicalize SsangYong->KGM if repo policy allows, or keep make but add note that KGM is former SsangYong. Split 2025/2026 facelift/hybrid rows where grounded.

### 10. Subaru | Outback
ACTION: **CHANGE/SPLIT**
DIRECTIVE: Subaru Israel home/current lineup includes Outback. Current 2026 Outback may be new generation; keep old 2.5 169hp row at 2024 if exact old row ended and add current grounded row.

### 11. Tesla | Model X
ACTION: **CHANGE**
DIRECTIVE: Tesla Israel Model X page is current and supports Dual Motor 670hp and Plaid 1020hp; set matching current rows to null.

### 12. Toyota | Aygo X
ACTION: **CHANGE/MERGE**
DIRECTIVE: Toyota Israel current Aygo X is hybrid. Merge duplicate Aygo X profiles; keep old 1.0 petrol rows ending 2024, add/currentize official 1.5 hybrid row with model year_end=null.

### 13. Toyota | bZ4X
ACTION: **CHANGE**
DIRECTIVE: Toyota Israel current/new-cars context supports bZ4X; if exact Motion/Vision 204/218 rows are current in local source, set null; otherwise split current rows.

### 14. Toyota | Corolla
ACTION: **CHANGE/SPLIT**
DIRECTIVE: Toyota Israel Corolla Sedan 2026 is current hybrid; old 140hp 2023-2024 rows should not stay as model end. Split current sedan; estate/hatch current only if source supports.

### 15. Toyota | Corolla Cross
ACTION: **CHANGE**
DIRECTIVE: Toyota Israel current Corolla Cross page supports current hybrid SUV; correct matching row to null or split if power changed.

### 16. Toyota | Highlander
ACTION: **CHANGE/MERGE**
DIRECTIVE: Toyota Israel Highlander current page supports 2.5 hybrid AWD 7-seat; merge duplicate profiles and remove/retain weak 2.4 turbo row separately if not Israeli-current.

### 17. Toyota | Hilux
ACTION: **CHANGE/SPLIT**
DIRECTIVE: Toyota Israel Hilux 2026/current page supports current Hilux; split old 2.4/2.8 rows if current mild-hybrid 48V/new row differs.

### 18. Toyota | Land Cruiser
ACTION: **CHANGE/SPLIT**
DIRECTIVE: Toyota Israel new-cars page supports Land Cruiser current mild-hybrid; split old 2020-2024 6AT rows from current 2024+ 8AT/current rows.

### 19. Toyota | Land Cruiser Prado
ACTION: **CHANGE/MERGE**
DIRECTIVE: Duplicate/naming issue: Israeli official naming is Land Cruiser. Merge/canonicalize Prado rows into Land Cruiser if they describe same Israeli row, preserving old rows.

### 20. Toyota | Proace City DUP#1
ACTION: **CHANGE/MERGE**
DIRECTIVE: Toyota Israel current Toyota City/Proace City Verso supports 1.5 diesel 131hp 8AT; merge duplicate Proace City profiles and split current exact row.

### 21. Toyota | Proace City DUP#2
ACTION: **CHANGE/MERGE**
DIRECTIVE: Merge into canonical Toyota City/Proace City profile; do not leave duplicate current profiles.

### 22. Toyota | Yaris
ACTION: **CHANGE/SPLIT**
DIRECTIVE: Toyota Israel Yaris build/spec pages are current; current hybrid row should be null. GR Yaris row needs exact current source or remain 2024.

### 23. Toyota | Yaris Cross
ACTION: **CHANGE**
DIRECTIVE: Toyota Israel Yaris Cross current/build/spec pages support current hybrid model; correct matching rows to null.

### 24. Volkswagen | Caddy
ACTION: **CHANGE**
DIRECTIVE: VW Commercial Israel has current Caddy page; correct/split matching current Caddy Life/commercial rows.

### 25. Volkswagen | Crafter
ACTION: **CHANGE/SPLIT**
DIRECTIVE: VW Commercial Israel/Carthube 2026 price support current Crafter; split old 140hp rows if current price list supports 177hp only.

### 26. Volkswagen | golf
ACTION: **CHANGE/SPLIT**
DIRECTIVE: VW Israel current models page lists Golf. Split old MK8 rows from current Golf, especially if current lineup differs.

### 27. Volkswagen | Golf GTI
ACTION: **CHANGE/SPLIT**
DIRECTIVE: VW Israel current models page lists Golf GTI; current 2026 GTI likely 265hp, so old 245hp row stays 2024 and current row is added/split.

### 28. Volkswagen | ID.4
ACTION: **CHANGE/SPLIT**
DIRECTIVE: Israeli current sources support ID.4 in 2025/2026; current 286/299hp rows should be validated and opened/split.

### 29. Volkswagen | ID.5
ACTION: **CHANGE**
DIRECTIVE: Israeli Auto 2026 support lists ID.5 Pro 2026; correct matching current rows to null.

### 30. Volkswagen | Multivan
ACTION: **CHANGE/SPLIT**
DIRECTIVE: VW Commercial Israel current site and 2024/2026 sources support Multivan/Multivan 6.1; split exact current 204hp/150hp rows according to grounded source.

### 31. Volkswagen | polo
ACTION: **CHANGE**
DIRECTIVE: VW Israel current models page/current 2026 list supports Polo; correct matching current rows or split GTI if needed.

### 32. Volkswagen | T-Cross
ACTION: **CHANGE**
DIRECTIVE: VW Israel current models page and 2026 price support T-Cross; correct row to null.

### 33. Volkswagen | Taigo
ACTION: **CHANGE**
DIRECTIVE: VW Israel current models page and 2026 price support Taigo; correct matching rows to null.

### 34. Volkswagen | Tiguan
ACTION: **CHANGE/SPLIT**
DIRECTIVE: VW Israel 2026/current sources support Tiguan; old 2021 rows may end 2024, current mild-hybrid/new row should be current.

### 35. Volkswagen | Transporter
ACTION: **CHANGE/SPLIT**
DIRECTIVE: VW Commercial Israel/iCar 2026 supports Transporter; split old 110/199hp rows if current 2026 sources support only 150hp variants.

### 36. Volvo | C40
ACTION: **CHANGE/RENAME-SPLIT**
DIRECTIVE: Volvo renamed C40 Recharge to EC40. Official Volvo Israel EC40 page exists but says not in stock/available by special order; currentize only by adding/canonicalizing EC40 row, keep C40-named old rows ending 2024 unless repo convention treats C40->EC40 as same canonical model.

---

## Move to deferred retained/final review — 14 profile entries

Do not currentize these inside RUN 05 unless repo-local or official current Israeli source clearly proves current exact rows. Add/keep them in the final deferred retained run.

### D1. Renault | Zoe
ACTION: **RETAIN/DEFER**
DIRECTIVE: Not in Renault Israel current price list/home lineup; global production ended in 2024 and Renault 5 E-Tech is current replacement context. Keep 2024 pending final review.

### D2. Seat | Ateca
ACTION: **RETAIN/DEFER**
DIRECTIVE: Seat Israel current home emphasizes Ibiza/Arona only; no exact current Israeli Ateca source found in this pass.

### D3. Seat | Tarraco
ACTION: **RETAIN/DEFER**
DIRECTIVE: No exact current Seat Israel Tarraco source found; likely historical.

### D4. Subaru | Ascent
ACTION: **RETAIN/DEFER**
DIRECTIVE: Subaru Israel current lineup shown in official home does not include Ascent.

### D5. Subaru | WRX
ACTION: **RETAIN/DEFER**
DIRECTIVE: Subaru Israel official home/current lineup does not include WRX in this pass.

### D6. Suzuki | Jimny
ACTION: **RETAIN/DEFER**
DIRECTIVE: Suzuki Israel current price list/home does not include Jimny; manuals mention Jimny/New Jimny up to 2019-2025 but that is owner-support, not new-current sales.

### D7. Toyota | GR86
ACTION: **RETAIN/DEFER**
DIRECTIVE: Prior validation already limited Israeli GR86 to 2022-2024; no current Toyota Israel new-car page found.

### D8. Toyota | Sienna
ACTION: **RETAIN/DEFER**
DIRECTIVE: No official Toyota Israel new-car source; likely parallel/import-only. Do not currentize.

### D9. Toyota | Supra
ACTION: **RETAIN/DEFER**
DIRECTIVE: No official Toyota Israel new-car source found for current Supra; keep for final review.

### D10. Volkswagen | Arteon DUP#1
ACTION: **RETAIN/DEFER**
DIRECTIVE: Arteon not in current VW Israel model list; likely discontinued. Merge/defer duplicate profiles.

### D11. Volkswagen | Arteon DUP#2
ACTION: **RETAIN/DEFER**
DIRECTIVE: Duplicate Arteon R profile; merge/defer in final retained review.

### D12. Volkswagen | ID.3 DUP#1
ACTION: **RETAIN/DEFER**
DIRECTIVE: Conflicting secondary data: Carzone lists ID.3 2026, but Auto/EVM note ID.3 was not regularly marketed in Israel. Without official VW Israel source, do not currentize.

### D13. Volkswagen | ID.3 DUP#2
ACTION: **RETAIN/DEFER**
DIRECTIVE: Same as ID.3 duplicate: send to final review; do not currentize on secondary-only conflict.

### D14. Volkswagen | Touareg
ACTION: **RETAIN/DEFER**
DIRECTIVE: Auto Israel states Touareg marketing in Israel stopped during 2024; do not open to null despite some secondary 2026 catalog noise.

---

# Required duplicate cleanup

- Toyota | Aygo X DUPs: leave one canonical current profile. Old 1.0 petrol rows stay historical; current hybrid row is grounded by Toyota Israel.
- Toyota | Highlander DUPs: leave one canonical profile with official 2.5 hybrid AWD 7-seat current row; do not keep weak 2.4 turbo as current unless exact Israeli source supports.
- Toyota | Proace City DUP#1 + DUP#2: merge to one canonical Toyota City/Proace City/Proace City Verso profile according to repo convention.
- Volkswagen | Arteon DUP#1 + DUP#2: do not currentize; defer/merge in final retained review.
- Volkswagen | ID.3 DUP#1 + DUP#2: conflicting secondary evidence; do not currentize without official VW Israel support; defer/merge in final review.

# Required patch mechanics

For every changed profile:

1. Add/keep a current source in `sources`.
2. Use real numeric `source_index` values only.
3. Update `source_indexes`, `field_sources.year_end`, and relevant supported fields.
4. Update `available_values_for_website` after adding/splitting rows.
5. Add notes:
   - `RUN05: year_end 2024 corrected as cutoff artifact` when changing to `null`.
   - `RUN05: old row retained at 2024; current row split because current Israeli source shows changed generation/powertrain` when splitting.
   - `RUN05: model renamed/current successor handled by canonicalization/split` when applicable.
   - `RUN05: moved to deferred final review; not currentized without exact Israeli source` when deferring.
6. Do not leave empty `technical_variants_il` profiles.
7. Do not create broken `source_indexes` or `field_sources`.

# Validation commands

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

# Final report required from Codex

- Profiles changed/currentized/split.
- Profiles merged/canonicalized.
- Profiles deferred to final retained run.
- Remaining `year_end: 2024` count within RUN 05.
- Validation command results.


---

# EMBEDDED FILE: CODEX_YEAR_END_2024_RUN_06_FIX_TASK.md


# CODEX YEAR_END_2024 RUN 06 FIX TASK + VOLVO FINAL PASS

## Goal
Fix the final main `year_end: 2024` cutoff run for Volvo profiles. Do not blanket-replace 2024 with null. Use exact Israeli current sources.

## Scope
Original RUN 6 profiles from the generated correction split:
1. Volvo | S90
2. Volvo | V60
3. Volvo | V90 DUP#1
4. Volvo | V90 DUP#2
5. Volvo | XC40
6. Volvo | XC60
7. Volvo | XC90

Additional actual-file finding:
8. Volvo | C40 — found in `model_technical_catalog_il.json` with `year_end: 2024`; include it in the final retained review unless an exact current Volvo Israel source proves current availability.

## Embedded web validation facts
- Volvo Israel current price list includes **XC40 B4 Core / XC40 B4 Ultra Dark**.
- Volvo Israel current price list includes **XC60 B5 AWD** trims and **XC60 Plug-in hybrid T8 Ultra Bright**.
- Volvo Israel current price list includes **XC90 B5 Ultra Bright** and **XC90 Plug-in hybrid T8 Ultra Dark/Bright**.
- Volvo Israel current pricing page does **not** show S90, V60, or V90 as current new-car price-list items in the checked current page.
- Volvo Israel May 2026 zero-km price-list PDF shows EX90, XC60, ES90, XC90, EX30; this supports XC60/XC90 current and gives replacement/context for old S90/V-series, but does not prove S90/V60/V90 current new availability.

## Decisions by profile

### 1. Volvo | S90
ACTION: **DEFER/RETAIN for final 2024 validation**
- Do not open S90 to `year_end: null` from global/legacy evidence.
- If a future exact Volvo Israel current S90 page/price-list exists, split/currentize; otherwise keep/correct historical end with note.

### 2. Volvo | V60
ACTION: **DEFER/RETAIN for final 2024 validation**
- No current Volvo Israel price-list proof in this pass.
- Keep `year_end: 2024` pending final review unless exact current importer source appears.

### 3-4. Volvo | V90 duplicates
ACTION: **MERGE + DEFER/RETAIN for final 2024 validation**
- Merge duplicate V90 profiles before finalizing.
- Do not open to current without exact Volvo Israel current V90 source.

### 5. Volvo | XC40
ACTION: **CHANGE/SPLIT**
- Profile `year_end` must be `null` because Volvo Israel current price list shows XC40 B4 trims.
- For current B4 row(s), set `year_end: null` where the existing row matches B4 2.0L turbo mild_hybrid / 197 hp / FWD / 7-speed dual_clutch or update/split if exact current source requires a different transmission/trim naming.
- Keep older T4/T5/T5 Recharge rows historical.
- Add/update Volvo Israel current price-list source and field_sources.

### 6. Volvo | XC60
ACTION: **CHANGE/SPLIT**
- Profile `year_end` must be `null`.
- Current XC60 B5 AWD rows and XC60 T8 plug-in hybrid rows must be current if fields match current importer price list/spec.
- If old 390 hp T8 row is not current, split it from current T8 row rather than opening the old row blindly.
- Add/update official Volvo Israel current price source and field_sources.

### 7. Volvo | XC90
ACTION: **CHANGE profile-level only / verify variants**
- Profile `year_end` must be `null` because current Volvo Israel price list shows XC90 B5 and XC90 Plug-in hybrid T8.
- Existing current rows already have `year_end: 2026` in the user file; do not regress them to 2024.
- If repo convention is `null` for current, normalize current rows from `2026` to `null` only if global catalog policy requires current as null. Otherwise preserve 2026 if validation accepts it and notes explicitly say 2026 source-backed.

### 8. Volvo | C40
ACTION: **ADD TO FINAL DEFERRED/RETAINED REVIEW**
- C40 has `year_end: 2024` in actual file but was not included in original RUN 6 list.
- Do not currentize C40 blindly; current Volvo Israel lineup/pricing emphasizes EX40 rather than C40 in this pass.
- Final review must decide whether this is historical C40, renamed/successor EC40/EX40 handling, or archive.

## RUN 6 counts
For reporting:
- Original 7 profiles: CHANGE = 3 (XC40, XC60, XC90), DEFER/RETAIN = 4 (S90, V60, V90 duplicate #1, V90 duplicate #2), CONDITIONAL = 0.
- Expanded actual-file pass including C40: CHANGE = 3, DEFER/RETAIN = 5, CONDITIONAL = 0.

## Required validation commands
```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

## Final report required
- Changed profiles count
- Deferred/retained profiles count
- Any remaining `year_end: 2024` in Volvo with justification
- Whether duplicate V90 profiles were merged or deferred to final-retained run


---

# EMBEDDED FILE: CODEX_ADD_MISSING_FULL_PROFILES_MODEL3_3008_CHERY_FX_CX30_TASK.md


# CODEX TASK — ADD MISSING FULL PROFILES: Tesla Model 3 + Peugeot 3008 + Chery FX + Mazda CX-30

## Purpose
Add four missing Israeli-market full model profiles as complete clean profiles:

1. `Tesla | Model 3`
2. `Peugeot | 3008`
3. `Chery | FX`
4. `Mazda | CX-30`

These must be full catalog profiles, not blocker/review shells.

## Hard rules

```text
1. Do not browse the internet from Codex. Use the embedded facts/URLs here plus repo-local sources only.
2. Do not invent rows. If a variant/trim/year range cannot be grounded, omit it or move to non-blocking review with reason.
3. Current rows must use year_end=null. Do NOT use year_end=2026 as a fake current marker.
4. If a variant changed after 2024, split old row and current row. Do not blindly open the old row to null.
5. Every variant must include version_or_trim, body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, support_level, source_indexes, field_sources, missing_grounded_fields.
6. EV rows: fuel_type=electric, engine=electric, engine_displacement_l=null, transmission=single_speed unless repo normalization says otherwise.
7. Hybrid rows keep ICE displacement. Do not set displacement null for HEV/PHEV/MHEV.
8. Keep source_indexes and field_sources valid against the profile's own sources array.
9. Add available_values_for_website, invalid_or_non_trim_labels, profile_confidence, notes.
10. After the task, these four profiles must exist exactly once and must have direct variant rows.
```

---

# 1) Tesla Model 3 — full profile from first Israeli sale to today

## Why needed
The previous blocker task showed `Tesla Model 3` as `clean_exists=false` with `technical_variants_il=[]`. It must be rebuilt.

## Add sources

```json
[
  {"source_index":0,"title":"Model 3 – סדאן חשמלי ספורטיבי | Tesla Israel","url":"https://www.tesla.com/he_il/model3","source_name":"Tesla Israel","source_type":"official_importer_page","supports":["body_type","fuel_type","engine","drivetrain","year_end"]},
  {"source_index":1,"title":"טסלה מודל 3 2021 יד שניה | Auto.co.il","url":"https://www.auto.co.il/cars/tesla/model-3/2021/","source_name":"Auto","source_type":"israeli_catalog","supports":["version_or_trim","body_type","fuel_type","engine","drivetrain","year_start","year_end"]},
  {"source_index":2,"title":"טסלה מודל 3 2021 Long Range 4x4 | Auto.co.il","url":"https://www.auto.co.il/cars/tesla/model-3/2021/527779/","source_name":"Auto","source_type":"israeli_variant_catalog","supports":["version_or_trim","fuel_type","engine","horsepower_hp","drivetrain","year_start","transmission"]},
  {"source_index":3,"title":"טסלה מודל 3 מחירון ומפרט | Auto.co.il","url":"https://www.auto.co.il/cars/tesla/model-3/","source_name":"Auto","source_type":"israeli_current_catalog","supports":["version_or_trim","fuel_type","engine","horsepower_hp","drivetrain","year_end"]},
  {"source_index":4,"title":"טסלה מודל 3 2026 Performance 4x4 | Auto.co.il","url":"https://www.auto.co.il/cars/tesla/model-3/2026/580282/","source_name":"Auto","source_type":"israeli_variant_catalog","supports":["version_or_trim","fuel_type","engine","horsepower_hp","drivetrain","transmission","year_start"]},
  {"source_index":5,"title":"טסלה מודל 3 2026 Long Range 2x4 | Auto.co.il","url":"https://www.auto.co.il/cars/tesla/model-3/2026/580283/","source_name":"Auto","source_type":"israeli_variant_catalog","supports":["version_or_trim","fuel_type","engine","horsepower_hp","drivetrain","transmission","year_start"]},
  {"source_index":6,"title":"טסלה מודל 3 2026 Long Range 4x4 | Auto.co.il","url":"https://www.auto.co.il/cars/tesla/model-3/2026/580285/","source_name":"Auto","source_type":"israeli_variant_catalog","supports":["version_or_trim","fuel_type","engine","horsepower_hp","drivetrain","transmission","year_start"]},
  {"source_index":7,"title":"טסלה מודל 3 | CarTube current catalog","url":"https://www.cartube.co.il/מחירון-רכב-חדש/טסלה/טסלה-מודל-3","source_name":"CarTube","source_type":"israeli_current_catalog","supports":["version_or_trim","fuel_type","engine","horsepower_hp","drivetrain","year_end"]},
  {"source_index":8,"title":"טסלה מודל 3 חדשה | iCar","url":"https://www.icar.co.il/טסלה/טסלה_מודל_3/טסלה_מודל_3_חדש/","source_name":"iCar","source_type":"israeli_current_catalog","supports":["version_or_trim","year_end"]}
]
```

## Target profile

```json
{"market":"IL","make":"Tesla","model":"Model 3","canonical_model":"Model 3","year_start":2021,"year_end":null,"profile_confidence":"high"}
```

## Required variant rows

Add historical rows only if exact local year ranges are supported:

1. `Standard Range Plus` — Sedan, electric, electric, null displacement, 283 hp, single_speed, RWD, year_start=2021, year_end=2023 or exact local end year.
2. `Long Range` — Sedan, electric, 441 hp, single_speed, AWD, year_start=2021, year_end=2023 or exact local end year.
3. `Performance` historical — Sedan, electric, 460 hp unless exact local source gives another value, single_speed, AWD, year_start=2021, year_end=2023 or exact local end year.

Add current/facelift rows:

4. `RWD` — Sedan, electric, 283 hp, single_speed, RWD, year_start=2024, year_end=null.
5. `Long Range RWD` — Sedan, electric, 315 hp, single_speed, RWD, year_start=2025, year_end=null.
6. `Long Range AWD` — Sedan, electric, 498 hp, single_speed, AWD, year_start=2024, year_end=null.
7. `Performance` current — Sedan, electric, **do not blindly use 627 hp**. Local sources conflict: Auto variant page shows 460 hp; CarTube summary shows 500 hp; Auto FAQ mentions 627 hp. Use the most variant-specific Israeli source and add a note explaining the discrepancy. year_start=2024, year_end=null.
8. Optional `Standard` — add only if repo-local/current source treats it as a separate 2026 trim, not a duplicate of RWD. If added: 283 hp, RWD, single_speed, year_start=2026, year_end=null.

---

# 2) Peugeot 3008 — full profile from first Israeli sale to today

## Why needed
The catalog has `Peugeot | e-3008`, but lacks full `Peugeot | 3008` petrol/diesel/PHEV/MHEV history. Do not let e-3008 stand in for 3008.

## Add sources

```json
[
  {"source_index":0,"title":"פיג'ו 3008 2010 יד שניה | Auto.co.il","url":"https://www.auto.co.il/cars/peugeot/3008/2010/","source_name":"Auto","source_type":"israeli_historical_catalog","supports":["body_type","fuel_type","engine","engine_displacement_l","horsepower_hp","transmission","drivetrain","year_start"]},
  {"source_index":1,"title":"פיג'ו 3008 2010 Premium | iCar","url":"https://www.icar.co.il/פיג'ו/פיג'ו_3008/פיג'ו_3008_יד_שניה_ד10/version3850/","source_name":"iCar","source_type":"israeli_variant_catalog","supports":["version_or_trim","engine","engine_displacement_l","horsepower_hp","year_start"]},
  {"source_index":2,"title":"פיג'ו 3008 2010 | CarZone","url":"https://www.carzone.co.il/Peugeot/3008/2010/","source_name":"CarZone","source_type":"israeli_catalog","supports":["body_type","fuel_type","engine_displacement_l","horsepower_hp","drivetrain"]},
  {"source_index":3,"title":"פיג'ו 3008 2017-2024 | iCar","url":"https://www.icar.co.il/פיג'ו/פיג'ו_3008/פיג'ו_3008_יד_שניה_ד11/","source_name":"iCar","source_type":"israeli_historical_catalog","supports":["year_start","year_end","engine","fuel_type"]},
  {"source_index":4,"title":"פיג'ו 3008 2020 | Auto.co.il","url":"https://www.auto.co.il/cars/peugeot/3008/2020/","source_name":"Auto","source_type":"israeli_catalog","supports":["engine","engine_displacement_l","horsepower_hp","fuel_type","transmission","drivetrain","year_start"]},
  {"source_index":5,"title":"פיג'ו 3008 2021 specification PDF","url":"https://www.cartube.co.il/images/artimage/05-2021/peugeot-3008-mifrat-2021-10.pdf","source_name":"Peugeot Israel spec PDF via CarTube","source_type":"official_spec_pdf_mirror","supports":["engine","engine_displacement_l","horsepower_hp","transmission","fuel_type","drivetrain"]},
  {"source_index":6,"title":"פיג'ו 3008 2024 | Auto.co.il","url":"https://www.auto.co.il/cars/peugeot/3008/2024/","source_name":"Auto","source_type":"israeli_catalog","supports":["engine","engine_displacement_l","horsepower_hp","fuel_type","transmission","year_end"]},
  {"source_index":7,"title":"פיג'ו 3008 היברידי מתון | Peugeot Israel","url":"https://online.peugeot.co.il/model/3008suv/","source_name":"Peugeot Online Israel","source_type":"official_importer_page","supports":["fuel_type","engine","engine_displacement_l","horsepower_hp","transmission","year_end"]},
  {"source_index":8,"title":"פיג'ו 3008 מחירון וחוות דעת | Auto.co.il","url":"https://www.auto.co.il/cars/peugeot/3008/","source_name":"Auto","source_type":"israeli_current_catalog","supports":["fuel_type","engine","engine_displacement_l","horsepower_hp","transmission","year_end"]},
  {"source_index":9,"title":"פיג'ו חדש - מחירון ומפרט | CarZone","url":"https://www.carzone.co.il/Peugeot/","source_name":"CarZone","source_type":"israeli_current_catalog/news","supports":["year_start","year_end"]}
]
```

## Target profile

```json
{"market":"IL","make":"Peugeot","model":"3008","canonical_model":"3008","year_start":2010,"year_end":null,"profile_confidence":"high"}
```

## Required variant groups

### First generation 2010-2016
- `Premium` — 1.6L turbo petrol, 156 hp, 6-speed automatic, FWD, 2010-2014/2015.
- `Premium Pack` — 1.6L turbo petrol, 156 hp, 6-speed automatic/manual only if local source supports, FWD, 2010-2014/2015.
- Facelift 1.6L turbo petrol, 165 hp, 6-speed automatic, FWD, 2015-2016.

### Second generation 2017-2024
Add only combinations grounded by local sources:
- 1.6L turbo petrol 165 hp, 6-speed automatic, FWD, 2017-2018.
- 1.2L turbo petrol 130 hp, 8-speed automatic, FWD, 2018-2024.
- 1.5L turbo diesel 130 hp, 8-speed automatic, FWD, 2018-2024.
- 1.6L turbo petrol 180 hp, 8-speed automatic, FWD, 2018-2024.
- 2.0L turbo diesel 180 hp, 8-speed automatic, FWD, only if locally grounded.
- 1.6L plug-in hybrid 225 hp, 8-speed automatic, FWD, 2020/2022-2024 depending source.
- 1.6L plug-in hybrid 300 hp, 8-speed automatic, AWD, 2020/2022-2024 depending source.

### Third generation/current 2025-current
- 1.2L MHEV / mild hybrid, 136 hp plus 22 hp assist, 6-speed dual-clutch/e-DCS6, FWD, year_start=2025, year_end=null.
- If repo policy merges EV into 3008, add the existing e-3008 GT 210 hp FWD single_speed as a row and alias `e-3008`; otherwise keep e-3008 separate.

---

# 3) Chery FX — full profile

## Add sources

```json
[
  {"source_index":0,"title":"Chery FX | Chery Israel","url":"https://cheryisrael.co.il/models/fx/","source_name":"Chery Israel","source_type":"official_importer_page","supports":["version_or_trim","body_type","fuel_type","engine","engine_displacement_l","horsepower_hp","transmission","drivetrain","year_end"]},
  {"source_index":1,"title":"Chery FX official spec PDF","url":"https://cheryisrael.co.il/TechSpecs/Chery-FX-Brochure.pdf","source_name":"Chery Israel","source_type":"official_spec_pdf","supports":["body_type","fuel_type","engine","engine_displacement_l","horsepower_hp","transmission","drivetrain"]},
  {"source_index":2,"title":"Chery FX EV | Chery Israel","url":"https://cheryisrael.co.il/models/fx-ev/","source_name":"Chery Israel","source_type":"official_importer_page","supports":["version_or_trim","body_type","fuel_type","engine","horsepower_hp","transmission","drivetrain","year_end"]},
  {"source_index":3,"title":"Chery FX EV official spec PDF","url":"https://cheryisrael.co.il/TechSpecs/Chery-FX-EV-Brochure.pdf","source_name":"Chery Israel","source_type":"official_spec_pdf","supports":["body_type","fuel_type","engine","horsepower_hp","transmission","drivetrain"]},
  {"source_index":4,"title":"Chery FX Hybrid official spec PDF","url":"https://cheryisrael.co.il/TechSpecs/Chery-FX-HEV-Brochure.pdf","source_name":"Chery Israel","source_type":"official_spec_pdf","supports":["body_type","fuel_type","engine","engine_displacement_l","horsepower_hp","transmission","drivetrain"]},
  {"source_index":5,"title":"צ'רי FX 2023 | Auto.co.il","url":"https://www.auto.co.il/cars/chery/fx/2023/","source_name":"Auto","source_type":"israeli_historical_catalog","supports":["body_type","fuel_type","engine","engine_displacement_l","horsepower_hp","transmission","drivetrain","year_start"]},
  {"source_index":6,"title":"צ'רי FX 2022 | CarZone","url":"https://www.carzone.co.il/chery/FX/2022/","source_name":"CarZone","source_type":"israeli_catalog","supports":["version_or_trim","year_start"]},
  {"source_index":7,"title":"מחירון רכב חדש - דגמי צ'רי בישראל","url":"https://cheryisrael.co.il/pricing/","source_name":"Chery Israel","source_type":"official_price_list","supports":["version_or_trim","year_end"]}
]
```

## Target profile

```json
{"market":"IL","make":"Chery","model":"FX","canonical_model":"FX","year_start":2022,"year_end":null,"profile_confidence":"high"}
```

## Required variant groups

### Petrol
Local-source conflict exists: older Israeli sources list 1.6 turbo petrol at 186 hp; current official Chery Israel page/spec PDF lists 147 hp. Do not overwrite; split by era when supported.

Historical 2022-2025 petrol rows:
- `Comfort` — 1.6L turbo petrol, 186 hp, 7-speed DCT, FWD.
- `Comfort TT` — same, if locally supported.
- `Noble` or `Luxury` — same, if locally supported.
- `Noble TT` — same, if locally supported.

Current petrol rows if official 2026 source supports them:
- `Sense` — 1.6L turbo petrol, 147 hp, 7-speed DCT, FWD, year_end=null.
- `Luxury` — 1.6L turbo petrol, 147 hp, 7-speed DCT, FWD, year_end=null.

### EV
- `Sense` — electric, 204 hp, single_speed, FWD, year_start=2024, year_end=null.
- `Sense TT` — electric, 204 hp, single_speed, FWD, if supported.
- `Comfort` — electric, 204 hp, single_speed, FWD.
- `Noble TT` — electric, 204 hp, single_speed, FWD.

### HEV
- `Comfort` — 1.5L hybrid, 246 hp combined, DHT automatic, FWD, year_start exact local launch/current, year_end=null.
- `Luxury` — 1.5L hybrid, 246 hp combined, DHT automatic, FWD, year_start exact local launch/current, year_end=null.

---

# 4) Mazda CX-30 — full profile

## Add sources

```json
[
  {"source_index":0,"title":"מאזדה CX-30 בישראל - מחירון ומפרט טכני 2020 | CarTube","url":"https://www.cartube.co.il/חדשות-רכב/מאזדה-cx-30-בישראל-מחירון-ומפרט-טכני-2019","source_name":"CarTube","source_type":"israeli_launch_article","supports":["version_or_trim","body_type","fuel_type","engine","engine_displacement_l","horsepower_hp","transmission","year_start"]},
  {"source_index":1,"title":"מאזדה CX-30 2020 חוות דעת | Auto.co.il","url":"https://www.auto.co.il/articles/car-news/industry/133641/","source_name":"Auto","source_type":"israeli_launch_article","supports":["version_or_trim","body_type","fuel_type","engine","engine_displacement_l","horsepower_hp","transmission","year_start"]},
  {"source_index":2,"title":"מאזדה CX-30 מחירון וחוות דעת | Auto.co.il","url":"https://www.auto.co.il/cars/mazda/cx-30/","source_name":"Auto","source_type":"israeli_catalog","supports":["version_or_trim","body_type","fuel_type","engine","engine_displacement_l","horsepower_hp","transmission","year_end"]},
  {"source_index":3,"title":"מאזדה CX30 חדש | iCar","url":"https://www.icar.co.il/מאזדה/מאזדה_CX30/מאזדה_CX30_חדש/","source_name":"iCar","source_type":"israeli_catalog","supports":["year_start","year_end","current_status"]},
  {"source_index":4,"title":"מחירון דגמי מאזדה ישראל 04/2026","url":"https://www.mazda.co.il/car-list","source_name":"Mazda Israel","source_type":"official_importer_price_list","supports":["current_status","year_end"]},
  {"source_index":5,"title":"מאזדה CX-30 2020 | CarZone","url":"https://www.carzone.co.il/Mazda/CX-30/2020/","source_name":"CarZone","source_type":"israeli_catalog","supports":["version_or_trim","body_type","fuel_type","engine","engine_displacement_l","horsepower_hp","transmission","drivetrain","year_start"]}
]
```

## Target profile

```json
{"market":"IL","make":"Mazda","model":"CX-30","canonical_model":"CX-30","year_start":2020,"year_end":2024,"profile_confidence":"high"}
```

## Required rows
Add as historical Israeli-market model; do not set current unless Mazda Israel price list shows it again.

- `Comfort` — Crossover/SUV, petrol, 2.0L, 165 hp, 6-speed automatic, FWD, 2020-2024.
- `Executive` — Crossover/SUV, petrol, 2.0L, 165 hp, 6-speed automatic, FWD, 2020-2024.
- `Premium` — Crossover/SUV, petrol, 2.0L, 165 hp, 6-speed automatic, FWD, 2020-2024.
- `Executive` — Crossover/SUV, petrol, 2.5L, 195 hp, 6-speed automatic, FWD, 2020-2024.
- `Premium` — Crossover/SUV, petrol, 2.5L, 195 hp, 6-speed automatic, FWD, 2020-2024.
- Black Edition rows only if repo-local/Auto pages confirm exact separate trims and years.

---

# Completion checks

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
python - <<'PY_CHECK'
import json
p='data/model_technical_catalog_il.json'
with open(p,encoding='utf-8') as f: data=json.load(f)
needed=[('Tesla','Model 3'),('Peugeot','3008'),('Chery','FX'),('Mazda','CX-30')]
for make,model in needed:
    rows=[m for m in data['models'] if m.get('make')==make and m.get('model')==model]
    print(make, model, len(rows), sum(len(m.get('technical_variants_il',[])) for m in rows))
    assert len(rows)==1, (make,model,'missing or duplicate')
    assert rows[0].get('technical_variants_il'), (make,model,'empty')
    for v in rows[0]['technical_variants_il']:
        assert v.get('support_level')=='direct', (make,model,v)
        assert 'version_or_trim' in v, (make,model,'missing version_or_trim key')
        assert v.get('missing_grounded_fields')==[], (make,model,v.get('missing_grounded_fields'))
PY_CHECK
```

## Completion report required

1. Confirm all four profiles exist exactly once.
2. Report variant counts for each profile.
3. Report exact year ranges used and why.
4. Confirm no invalid source_indexes/field_sources.
5. Confirm no new review/indirect/blocker rows.
6. Confirm current rows use `year_end=null`, not 2026 as a fake end year.


---

# EMBEDDED FILE: FULL_OFFLINE_VALIDATION_YEAR_END_2024_RUNS_01_06_PLUS_MISSING_MODELS_V2.md


# FULL OFFLINE VALIDATION V2 — year_end 2024 + missing profiles + final validation closed

Generated: 2026-06-24

This file **supersedes** all previous `YEAR_END_2024_*`, `CODEX_YEAR_END_2024_*`, and missing-model task files.

## Hard rule for Codex

Codex must **not browse** and must **not infer years**. All target actions and years are embedded here. Codex only applies these decisions to `model_technical_catalog_il.json`.

## Global rules

- `year_end=2026` must never be used as a fake current marker.
- Current = `year_end:null`.
- Do not mass-replace `2024 -> null`.
- If this file says `FINAL_RETAIN_2024`, keep `2024` and add/keep a note explaining that final offline validation did not ground a current Israeli row.
- If this file says `FINAL_SPLIT_CURRENT`, preserve the old row and add/split a current row with `year_end:null`.
- If this file says `FINAL_FIX_YEAR_END_TO_2022`, change the incorrect 2024 to the exact embedded historical end year.
- For duplicate profiles, merge into one canonical profile and preserve lineage notes.

## Counts

| Bucket | Count |
|---|---:|
| Main runs 1-6 already marked for change/current/split | 171 |
| Final validation entries reviewed | 86 |
| Final validation year/status changes | 6 |
| Final validation duplicate merges, no year opening | 5 |
| Final validation retained as 2024 | 75 |
| Missing full model profiles to add | 4 |

## Main runs 1-6

The 171 main-run changes remain active. Apply the run-level files already generated for runs 1-6, but use this V2 file as the controlling source if there is conflict. The key correction is: **do not ask Codex to validate online; all current/split/retain decisions are offline decisions.**

# Final validation run — 86 entries closed

| Run | Profile | Action | Exact target | Offline rationale |
|---:|---|---|---|---|
| 1 | Aiways U6 | `FINAL_RETAIN_2024` | retain profile/model year_end=2024; keep variant year_end=2024 | No current official/importer evidence found in the final offline pass. Do not open to current. |
| 1 | Audi A4 | `FINAL_RETAIN_2024` | retain 2024 | Replaced by new Audi A5/S5 family; do not open A4 as current. |
| 1 | Audi R8 | `FINAL_RETAIN_2024` | retain 2024 | R8 is discontinued; no current Israeli new-car page. |
| 1 | Audi RS4 | `FINAL_RETAIN_2024` | retain 2024 | No current RS4 Israeli new-car page in final offline pass. |
| 1 | Audi RS5 | `FINAL_SPLIT_CURRENT` | keep legacy RS5 rows ending 2024; add/split current Audi RS 5 Sedan e-hybrid row with year_start=2026, year_end=null | Audi Israel currently exposes the all-new RS 5 Sedan e-hybrid. Old coupe/sportback RS5 rows must not be blindly opened; add current sedan/e-hybrid row only. |
| 1 | Audi RS7 | `FINAL_RETAIN_2024` | retain 2024 | No current RS7 Israeli new-car page in final offline pass; do not infer from RS family. |
| 1 | BMW 118i | `FINAL_RETAIN_2024` | retain 2024 | Current BMW Israel 1 Series price list exposes 116/120/M135, not 118i. |
| 1 | BMW 128ti | `FINAL_RETAIN_2024` | retain 2024 | Current BMW Israel 1 Series price list does not expose 128ti. |
| 1 | BMW 225xe Active Tourer PHEV | `FINAL_RETAIN_2024` | retain 2024 | Current BMW 2 Series/Active Tourer evidence does not support 225xe PHEV as active. |
| 1 | BMW 640i GT | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 1 | BMW 850i | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 1 | BMW M8 | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 1 | BMW M850i | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 1 | BMW X3 M | `FINAL_RETAIN_2024` | retain 2024 | Current X3 exists, but X3 M is not grounded as current in final offline pass. |
| 1 | BMW X6 M | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence for X6 M row; do not open. |
| 1 | Cadillac XT5 | `FINAL_RETAIN_2024` | retain 2024 | Cadillac Israel current lineup found XT6/Optiq/Escalade IQ context, not XT5. |
| 1 | Chevrolet Camaro | `FINAL_RETAIN_2024` | retain 2024 | Camaro generation ended after MY2024; no current Chevrolet Israel listing. |
| 1 | Chevrolet Equinox | `FINAL_RETAIN_2024` | retain 2024 | Chevrolet Israel current lineup does not support Equinox as new current. |
| 2 | Citroen C5 X | `FINAL_RETAIN_2024` | retain 2024 | Citroen Israel current range does not show C5 X; do not open. |
| 2 | Citroen SpaceTourer | `FINAL_RETAIN_2024` | retain 2024 | Citroen Israel current range does not show SpaceTourer; Jumpy/Berlingo are separate. |
| 2 | Cupra Ateca | `FINAL_RETAIN_2024` | retain 2024 | No current Israeli Cupra Ateca support in final offline pass. |
| 2 | Cupra Born | `FINAL_RETAIN_2024` | retain 2024 | No current Israeli Cupra Born support in final offline pass. |
| 2 | Dodge Durango | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 2 | DS Automobiles DS 9 | `FINAL_RETAIN_2024` | retain 2024 | DS Israel current visible model support centered on DS 7/DS 4 context, not DS 9. |
| 2 | Ferrari 812 Superfast | `FINAL_RETAIN_2024` | retain 2024 | No current Israeli new-car evidence; model is not a current 2026 row. |
| 2 | Ferrari Portofino | `FINAL_RETAIN_2024` | retain 2024 | No current Israeli new-car evidence; do not open. |
| 2 | Ford F-150 | `FINAL_RETAIN_2024` | retain 2024 | Ford Israel current passenger/commercial evidence did not ground F-150 as current new-car row. |
| 2 | Ford Kuga | `FINAL_RETAIN_2024` | retain 2024 | Ford Israel current lineup did not ground Kuga as current. |
| 2 | Ford Mustang Mach-E | `FINAL_RETAIN_2024` | retain 2024 | Ford Israel current lineup did not ground Mach-E as current. |
| 2 | Ford Puma | `FINAL_RETAIN_2024` | retain 2024 | Ford Israel current lineup did not ground Puma as current. |
| 2 | Ford Transit | `FINAL_RETAIN_2024` | retain 2024 | No current local Transit row sufficiently grounded in final offline pass; do not infer from global Ford. |
| 2 | Hongqi E-HS9 | `FINAL_CHANGE_TO_CURRENT` | set matching E-HS9 current rows year_end=null; if old trim naming differs, split old 2022-2024 rows and add current E-HS9/HONGQI 9 row year_start=2026, year_end=null | Hongqi Israel still exposes HONGQI 9/EHS9 official current pages. |
| 2 | Hyundai Creta | `FINAL_RETAIN_2024` | retain 2024 | No current Hyundai Israel evidence in final offline pass; do not open. |
| 2 | Hyundai i30 N | `FINAL_RETAIN_2024` | retain 2024 | No current Hyundai Israel evidence in final offline pass; do not open. |
| 2 | Infiniti QX60 | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 2 | Jaguar F-Pace | `FINAL_RETAIN_2024` | retain 2024 | Jaguar new-car activity/current status not grounded enough; do not open. |
| 2 | Jaguar F-Type | `FINAL_RETAIN_2024` | retain 2024 | F-Type discontinued globally and not current locally; retain 2024. |
| 2 | Jaguar XE | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 2 | Jaguar XF | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 2 | Jeep Compass | `FINAL_RETAIN_2024` | retain 2024 | Jeep Israel current focus did not ground Compass as active current in final pass. |
| 2 | Jeep Renegade | `FINAL_RETAIN_2024` | retain 2024 | Jeep Israel current focus did not ground Renegade as active current in final pass. |
| 3 | Kia Ceed SW | `FINAL_RETAIN_2024` | retain 2024 | Kia Israel current model range does not show Ceed SW. |
| 3 | Lamborghini Huracan | `FINAL_RETAIN_2024` | retain 2024 | Huracan is not a current new-car profile; retain 2024. |
| 3 | Lamborghini Huracan DUPLICATE | `FINAL_MERGE_DUPLICATE_RETAIN_2024` | merge duplicate into canonical Huracan profile; keep year_end=2024 | Structural cleanup only; no current opening. |
| 3 | Lexus LC | `FINAL_RETAIN_2024` | retain 2024 | Lexus Israel current new-cars pass did not ground LC as current; do not open. |
| 3 | Lexus LS | `FINAL_CHANGE_TO_CURRENT` | set LS 500h current row year_end=null; ensure year_start remains original Israeli sale start if existing row spans active generation, otherwise split legacy row and add current 3.5L Petrol Hybrid Multi-Stage Hybrid 4X2 row | Lexus Israel exposes LS 500h as current new-car page with price and hybrid powertrain. |
| 3 | Maserati Ghibli | `FINAL_RETAIN_2024` | retain 2024 | No current Israeli new-car evidence; do not open. |
| 3 | Maserati Quattroporte | `FINAL_RETAIN_2024` | retain 2024 | No current Israeli new-car evidence; do not open. |
| 3 | Maxus Euniq 5 | `FINAL_RETAIN_2024` | retain 2024 | Maxus Israel current contact/model set moved to MIFA 7/9, not Euniq. |
| 3 | Maxus Euniq 6 | `FINAL_RETAIN_2024` | retain 2024 | Maxus Israel current contact/model set moved to MIFA 7/9, not Euniq. |
| 3 | Mazda CX-3 | `FINAL_RETAIN_2024` | retain 2024 | Mazda CX-3 is not on Mazda Israel 2026 current price list; Israeli source marks marketing stopped. |
| 3 | Mazda CX-3 DUPLICATE | `FINAL_MERGE_DUPLICATE_RETAIN_2024` | merge duplicate into canonical CX-3 profile; keep year_end=2024 | Structural cleanup only. |
| 3 | Mazda MX-5 | `FINAL_RETAIN_2024` | retain 2024 | Mazda Israel 2026 current price list does not ground MX-5 as active new-car row. |
| 3 | McLaren Artura | `FINAL_RETAIN_2024` | retain 2024 | No robust local current evidence; do not open. |
| 3 | Mercedes-Benz B-Class | `FINAL_RETAIN_2024` | retain 2024 | Mercedes Israel current model pass does not show B-Class. |
| 4 | MG Marvel R | `FINAL_RETAIN_2024` | retain 2024 | MG Israel current model/shop list does not show Marvel R. |
| 4 | MG ZS EV | `FINAL_RETAIN_2024` | retain 2024 | MG Israel current model/shop list shows ZS Hybrid and newer EVs, not ZS EV as current new row. |
| 4 | Mini Clubman | `FINAL_RETAIN_2024` | retain 2024 | MINI Clubman is not current in final pass; do not open. |
| 4 | Mitsubishi L200 | `FINAL_FIX_YEAR_END_TO_2022` | change L200/Triton historical row year_end from 2024 to 2022 where the row maps to the official Israel Triton/L200 generation; do NOT set null | Mitsubishi Israel official past-model page grounds Triton 2015-2022. |
| 4 | Nissan Altima | `FINAL_RETAIN_2024` | retain 2024 | Nissan Israel current range does not show Altima. |
| 4 | Nissan Leaf | `FINAL_RETAIN_2024` | retain 2024 | Nissan Israel treats Leaf as legacy; current range does not show it. |
| 4 | Omoda C5 | `FINAL_RETAIN_2024` | retain 2024 | Omoda Israel current official range shows OMODA 7/9, not C5/5 as active current row. |
| 4 | Opel Crossland | `FINAL_CHANGE_TO_CURRENT` | set Crossland 1.2L 130hp Edition/Elegance rows year_end=null; if old trim/power mismatch exists, split old row and add current Edition/Elegance rows | Opel Israel current price list exposes Crossland Edition/Elegance 1.2L 130hp. |
| 4 | Polestar 2 | `FINAL_RETAIN_2024` | retain 2024 | Polestar Israel says no cars available for purchase; do not open current. |
| 4 | Porsche 718 Boxster | `FINAL_SPLIT_CURRENT` | do not leave the entire 718 profile closed at 2024; keep historical Boxster rows as-is if unsupported, add/split official current 718/Boxster/Spyder RS rows with year_end=null when source-compatible | Porsche Israel official 718 page/configurator exposes current 718 range. |
| 4 | Renault Koleos | `FINAL_RETAIN_2024` | retain 2024 | Renault Israel current range does not show Koleos. |
| 4 | Renault Megane | `FINAL_RETAIN_2024` | retain 2024 | Renault Israel current range does not show legacy Megane as new car. |
| 4 | Renault Megane E-Tech | `FINAL_RETAIN_2024` | retain 2024 | Renault Israel current range did not ground Megane E-Tech as current new-car row; Renault 5 E-Tech is separate. |
| 5 | Renault Zoe | `FINAL_RETAIN_2024` | retain 2024 | Renault Israel current range does not show Zoe; Renault 5 E-Tech is separate. |
| 5 | Seat Ateca | `FINAL_RETAIN_2024` | retain 2024 | Seat Israel current homepage shows Arona/Ibiza only, not Ateca. |
| 5 | Seat Tarraco | `FINAL_RETAIN_2024` | retain 2024 | Seat Israel current homepage shows Arona/Ibiza only, not Tarraco. |
| 5 | Subaru Ascent | `FINAL_RETAIN_2024` | retain 2024 | Subaru Israel current range shows Outback/Crosstrek/Forester/BRZ, not Ascent. |
| 5 | Subaru WRX | `FINAL_RETAIN_2024` | retain 2024 | Subaru Israel current range does not show WRX. |
| 5 | Suzuki Jimny | `FINAL_RETAIN_2024` | retain 2024 | No current official new-car evidence; do not open. |
| 5 | Toyota GR86 | `FINAL_RETAIN_2024` | retain 2024 | Toyota Israel current new-car list did not ground GR86 as active. |
| 5 | Toyota Sienna | `FINAL_RETAIN_2024` | retain 2024 | No official Toyota Israel new-car evidence; do not open. |
| 5 | Toyota Supra | `FINAL_RETAIN_2024` | retain 2024 | Toyota Israel current new-car list did not ground Supra as active. |
| 5 | Volkswagen Arteon | `FINAL_RETAIN_2024` | retain 2024 | VW Israel current range does not ground Arteon as active; retain. |
| 5 | Volkswagen Arteon DUPLICATE | `FINAL_MERGE_DUPLICATE_RETAIN_2024` | merge duplicate into canonical Arteon profile; keep year_end=2024 | Structural cleanup only. |
| 5 | Volkswagen ID.3 | `FINAL_RETAIN_2024` | retain 2024 | VW Israel current range/search did not ground ID.3 as active; do not open. |
| 5 | Volkswagen ID.3 DUPLICATE | `FINAL_MERGE_DUPLICATE_RETAIN_2024` | merge duplicate into canonical ID.3 profile; keep year_end=2024 | Structural cleanup only. |
| 5 | Volkswagen Touareg | `FINAL_RETAIN_2024` | retain 2024 | Touareg not grounded as current; retain 2024. |
| 6 | Volvo S90 | `FINAL_RETAIN_2024` | retain 2024 | Volvo Israel current pricing/model pass does not ground S90 as active. |
| 6 | Volvo V60 | `FINAL_RETAIN_2024` | retain 2024 | Volvo Israel current pricing/model pass does not ground V60 as active. |
| 6 | Volvo V90 | `FINAL_RETAIN_2024` | retain 2024 | Volvo Israel current pricing/model pass does not ground V90 as active. |
| 6 | Volvo V90 DUPLICATE | `FINAL_MERGE_DUPLICATE_RETAIN_2024` | merge duplicate into canonical V90 profile; keep year_end=2024 | Structural cleanup only. |


# דגמים חסרים להוספה מאפס — החלטות אופליין מלאות

## Tesla Model 3 — add full clean profile

**Action:** add missing profile `make="Tesla", model="Model 3", canonical_model="Model 3"`.

**Important:** do not add only current 2026 rows. Model 3 must cover Israeli sale history from launch through current.

Target rows to create, unless the repo already contains a stricter local row after merge:

| version_or_trim | body_type | fuel_type | engine | displacement | hp | transmission | drivetrain | year_start | year_end | support_level |
|---|---|---|---|---:|---:|---|---|---:|---:|---|
| Standard Range Plus | Sedan | electric | electric | null | 283 | single_speed | RWD | 2021 | 2021 | direct |
| RWD | Sedan | electric | electric | null | 283 | single_speed | RWD | 2022 | 2023 | direct |
| Long Range AWD | Sedan | electric | electric | null | 441 | single_speed | AWD | 2021 | 2023 | direct |
| Performance | Sedan | electric | electric | null | 460 | single_speed | AWD | 2021 | 2023 | direct |
| RWD / Highland | Sedan | electric | electric | null | 283 | single_speed | RWD | 2024 | null | direct |
| Long Range RWD | Sedan | electric | electric | null | 320 | single_speed | RWD | 2025 | null | direct |
| Long Range AWD / Highland | Sedan | electric | electric | null | 498 | single_speed | AWD | 2024 | null | direct |
| Performance / Highland | Sedan | electric | electric | null | 460 | single_speed | AWD | 2024 | null | direct |
| Standard | Sedan | electric | electric | null | 283 | single_speed | RWD | 2026 | null | direct |

Notes:
- Keep `engine_displacement_l=null` for every EV row.
- Use `single_speed`, not generic `automatic`, unless current catalog schema forces otherwise.
- Do not use ungrounded 627 hp for Israeli Model 3 Performance; final offline decision is 460 hp until a stricter Israeli spec source is added.
- Tesla official current page and Israeli 2026 launch article confirm Model 3 as active/current and Standard as 2026 entry version.

## Peugeot 3008 — add full non-electric 3008 profile

**Action:** add missing profile `make="Peugeot", model="3008", canonical_model="3008"`. Do not merge into existing `Peugeot e-3008`; e-3008 remains separate electric model.

Target rows:

| version_or_trim | body_type | fuel_type | engine | displacement | hp | transmission | drivetrain | year_start | year_end | support_level |
|---|---|---|---|---:|---:|---|---|---:|---:|---|
| null / Active/Comfort-era | SUV | petrol | 1.6L turbo | 1.6 | 156 | automatic | FWD | 2010 | 2014 | direct |
| null / facelift-era | SUV | petrol | 1.6L turbo | 1.6 | 165 | automatic | FWD | 2015 | 2016 | direct |
| Active / Premium-era | SUV | diesel | 1.6L diesel | 1.6 | 120 | automatic | FWD | 2017 | 2018 | direct |
| Active / Premium-era | SUV | diesel | 1.5L diesel | 1.5 | 130 | automatic | FWD | 2018 | 2024 | direct |
| Active / Premium-era | SUV | petrol | 1.2L turbo | 1.2 | 130 | automatic | FWD | 2018 | 2024 | direct |
| GT / GT Pack-era | SUV | petrol | 1.6L turbo | 1.6 | 180 | automatic | FWD | 2018 | 2024 | direct |
| PHEV | SUV | plug-in hybrid | 1.6L turbo plug-in hybrid | 1.6 | 225 | automatic | FWD | 2020 | 2024 | direct |
| PHEV 4x4 | SUV | plug-in hybrid | 1.6L turbo plug-in hybrid | 1.6 | 300 | automatic | AWD | 2020 | 2024 | direct |
| GT MHEV | SUV | mild_hybrid | 1.2L turbo mild-hybrid | 1.2 | 145 | 6-speed automatic / e-DCS6 | FWD | 2025 | null | direct |

Notes:
- Current official Peugeot Israel 3008 page/price list supports the new 3008 MHEV; current row must be `year_end=null`, not 2026.
- Existing `Peugeot e-3008` remains separate and should not absorb these ICE/MHEV/PHEV rows.

## Chery FX — add full clean profile

**Action:** add missing profile `make="Chery", model="FX", canonical_model="FX"`.

Target rows:

| version_or_trim | body_type | fuel_type | engine | displacement | hp | transmission | drivetrain | year_start | year_end | support_level |
|---|---|---|---|---:|---:|---|---|---:|---:|---|
| Comfort | Crossover | petrol | 1.6L turbo | 1.6 | 186 | 7-speed dual-clutch | FWD | 2022 | 2025 | direct |
| Luxury | Crossover | petrol | 1.6L turbo | 1.6 | 186 | 7-speed dual-clutch | FWD | 2022 | 2025 | direct |
| Noble | Crossover | petrol | 1.6L turbo | 1.6 | 147 | 7-speed dual-clutch | FWD | 2026 | null | direct |
| EV Noble | Crossover | electric | electric | null | 204 | single_speed | FWD | 2024 | null | direct |
| HEV Noble | Crossover | hybrid | 1.5L turbo hybrid | 1.5 | 246 | hybrid automatic | FWD | 2025 | null | direct |

Notes:
- Do not collapse 186 hp petrol and current 147 hp petrol into one row. Split periods.
- EV displacement is null.
- HEV has ICE displacement 1.5.

## Mazda CX-30 — add full clean profile

**Action:** add missing profile `make="Mazda", model="CX-30", canonical_model="CX-30"`.

Target rows:

| version_or_trim | body_type | fuel_type | engine | displacement | hp | transmission | drivetrain | year_start | year_end | support_level |
|---|---|---|---|---:|---:|---|---|---:|---:|---|
| Comfort | Crossover | petrol | 2.0L | 2.0 | 165 | 6-speed automatic | FWD | 2020 | 2024 | direct |
| Executive | Crossover | petrol | 2.0L | 2.0 | 165 | 6-speed automatic | FWD | 2020 | 2024 | direct |
| Premium | Crossover | petrol | 2.0L | 2.0 | 165 | 6-speed automatic | FWD | 2020 | 2024 | direct |
| Executive | Crossover | petrol | 2.5L | 2.5 | 195 | 6-speed automatic | FWD | 2020 | 2024 | direct |
| Premium | Crossover | petrol | 2.5L | 2.5 | 195 | 6-speed automatic | FWD | 2020 | 2024 | direct |
| Premium Plus | Crossover | petrol | 2.0L | 2.0 | 165 | 6-speed automatic | FWD | 2022 | 2024 | direct |
| Premium Plus | Crossover | petrol | 2.5L | 2.5 | 195 | 6-speed automatic | FWD | 2022 | 2024 | direct |

Notes:
- Do NOT mark CX-30 as current. Final offline decision: Israeli sources identify CX-30 as 2020-2024 and not marketed as new now.


# Implementation checklist

1. Load `model_technical_catalog_il.json`.
2. Apply all main-run 1-6 changes that were already marked as change/current/split.
3. Apply the final validation table above exactly.
4. Add the four missing model profiles exactly enough to pass schema and source validation.
5. Ensure every variant has `version_or_trim` key, with `null` where no trim exists.
6. Recompute `available_values_for_website` for any changed/added profile.
7. Every `source_indexes` entry must point to an actual object in the same profile's `sources` list.
8. Every `field_sources` index must also point to an existing source.
9. EV rows must use `engine_displacement_l:null`.
10. Hybrid / PHEV / MHEV rows must keep ICE displacement when the engine includes combustion.
11. After applying, run:

```bash
python -m json.tool model_technical_catalog_il.json > /tmp/catalog_check.json
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

## Required final report from Codex

Codex must report:

```text
Main year_end=2024 changed/opened/split:
Final validation changed/opened/split:
Final validation retained 2024:
Final validation duplicate merges:
Missing profiles added:
Remaining year_end=2024 count:
Remaining year_end=2024 justified count:
Remaining unjustified year_end=2024 count:
ready_for_website_upload:
```
