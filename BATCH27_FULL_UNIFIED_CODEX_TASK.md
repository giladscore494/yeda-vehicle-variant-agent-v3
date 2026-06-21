# BATCH27 FULL UNIFIED CODEX TASK

Apply RUN1 -> RUN2 -> RUN3 -> RUN4 -> RUN5 -> FINAL RUN. Do not browse the internet. Delete codex_tasks/BATCH27_*.md before final commit unless user explicitly asks to keep them.



---

# BATCH27 RUN 1 — VARIANT-LEVEL WEB VALIDATION CODEX TASK

## Operating mode

Do not browse the internet.
All web-validation facts, source decisions, field-level target values, and actions are embedded in this task file.
Use this file as the single source of truth for RUN 1 only.

Apply **BATCH27 RUN 1 only**.
Do not apply RUN 2, RUN 3, RUN 4, RUN 5, FINAL blockers, or any future unified task.

## RUN 1 scope

From `IL-confirmed|Mitsubishi|Space Star` through `global-reference-only|Nissan|Murano`.

Profiles: 20.
Technical variants in these profiles: 63.
Every variant below has a field-level decision.

## Mandatory temporary-file cleanup

Before final commit for this RUN, delete `codex_tasks/BATCH27_RUN1_*.md` unless the user explicitly asks to keep it.
Do not leave temporary task files in the repository.

## Required checks after implementation

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

If `pytest` fails because `streamlit` is missing, report it explicitly as environment/dependency failure and still run the remaining possible checks.

## Required file audit after implementation

Inspect actual generated files, not only console output:

- `data/model_technical_catalog_il.json`
- readiness report
- review file/report
- archive file/report
- quality scan output
- `compute_resume_state()`
- `unmatched_output_keys`
- active blockers
- cursor/resume state
- duplicate/split alias cleanup

## RUN 1 source pack


### Mitsubishi Space Star

- SOURCE: Cartube launch 2013 — https://www.cartube.co.il/חדשות-רכב/מיצובישי-ספייס-סטאר-בישראל-מחיר-החל-מ-69900-שקל
  FACT: Israeli launch context for 2013 Space Star.
- SOURCE: iCar Space Star 2018/2019 — https://www.icar.co.il/מיצובישי/מיצובישי_ספייס_סטאר/
  FACT: Israeli used-car technical references for 1.2 CVT generation.
- SOURCE: Auto.co.il 2021 update — https://www.auto.co.il/article/135084-local-news-mitsubishi-spacestar
  FACT: Israeli update to 1.2L 71 hp facelift/current-period row.
- SOURCE: Carzone 2021 Space Star — https://www.carzone.co.il/Mitsubishi/Space-Star/2021/
  FACT: Israeli trims/sales for 2021, Supreme/Premium/Instyle 1.2L.

### Mitsubishi Space Wagon

- SOURCE: Yad2 price-list feed — https://www.yad2.co.il/price-list/feed?manufacturer=30&model=10386
  FACT: Israeli Space Wagon sub-models: GLXI 2.0 133 hp and GLX 2.4 around 147/150 hp.
- SOURCE: Auto.co.il model pages — https://www.auto.co.il/model/mitsubishi-space-wagon_g250
  FACT: Israeli model pages for 1998-2004 generation.
- SOURCE: Autoboom Israel Space Wagon 2.4 — https://autoboom.co.il/en/catalog/cars/mitsubishi/space-wagon/3-generation/compact-van/34117
  FACT: Israel-context 2.4 AT 150 hp FWD compact van.

### NIO EL6

- SOURCE: NIO Israel car-list 02/2026 — https://www.nio.co.il/car-list
  FACT: Official Israeli price list: eL6 75 KWH, 100 KWH, and 100 KWH Comfort Pack.
- SOURCE: Official eL6 PDF — https://api.nio.co.il/Uploads/eL6/מפרט/39887%20Nio%20eL6.pdf
  FACT: Official Israeli PDF: 75/100 kWh, 489 hp, Intelligent E-AWD, WLTP 406/523 km.
- SOURCE: NIO Israel EL6 page — https://www.nio.co.il/model/5/el6
  FACT: Official Israeli model page; current eL6.

### NIO EL7

- SOURCE: iCar EL7 — https://www.icar.co.il/ניו/ניו_EL7/ניו_EL7_חדש/
  FACT: Israeli expert page: EL7 sold in Israel with two motors, 653 hp, 100 kWh.
- SOURCE: Auto.co.il EL7 — https://www.auto.co.il/cars/nio/el7/
  FACT: Israeli technical page: one 100 kWh AWD 653 hp version.
- SOURCE: Carzone EL7 2026 — https://www.carzone.co.il/NIO/eL7/
  FACT: Israeli 2026 page: 100 kWh, 653 hp, AWD, 471 km.
- SOURCE: Cartube EL7 2026 technical — https://www.cartube.co.il/מחירון-רכב-חדש/ניאו/ניאו-el7/6084-ניאו-el7-100kwh
  FACT: Israeli 2026 technical page: direct transmission, 100 kWh, 653 hp, 501 km.

### Nissan 200SX

- SOURCE: Auto.co.il 200SX 1994-1999 — https://www.auto.co.il/catalog/nissan/200sx/1994-1999
  FACT: Israeli 200SX catalog: 2.0 turbo coupe, manual/automatic.
- SOURCE: KML 200SX automatic — https://www.kml.co.il/car/nissan/200sx/1994-1999/automatic
  FACT: Israeli spec reference for automatic 2.0 turbo 200 hp.
- SOURCE: Auto-data S14 — https://www.auto-data.net/en/nissan-200-sx-s14-2.0-i-16v-turbo-200hp-380
  FACT: Global technical support only: S14 2.0 turbo 200 hp RWD.

### Nissan 370Z

- SOURCE: iCar 370Z — https://www.icar.co.il/ניסאן/ניסאן_370Z/
  FACT: Israeli 370Z pages for coupe/roadster.
- SOURCE: Auto.co.il 370Z — https://www.auto.co.il/model/nissan-370z_g196
  FACT: Israeli 370Z technical catalog.
- SOURCE: Cartube Nismo Israel — https://www.cartube.co.il/חדשות-רכב/ניסאן-370z-ניסמו-בישראל-מחיר-החל-מ-349900-שקל
  FACT: Israeli 370Z Nismo launch: supports Nismo as Israeli-market special row.
- SOURCE: Autoweek 370Z specs — https://www.autoweek.nl/auto/56877/nissan-370z/
  FACT: Global technical confirmation: 3.7L 328 hp, RWD, manual/auto.

### Nissan Almera

- SOURCE: iCar Almera 1996-2000 — https://www.icar.co.il/ניסאן/ניסאן_אלמרה/ניסאן_אלמרה_דור_1/
  FACT: Israeli first-generation Almera; use 1996 start if supported.
- SOURCE: iCar Almera 2000-2006 — https://www.icar.co.il/ניסאן/ניסאן_אלמרה/
  FACT: Israeli second-generation Almera 2000-2006, 1.5/1.8.
- SOURCE: Auto.co.il Almera generation 2 — https://www.auto.co.il/model/nissan-almera_g131
  FACT: Israeli technical support for 2000-2006.

### Nissan Altima

- SOURCE: iCar Altima — https://www.icar.co.il/ניסאן/ניסאן_אלטימה/
  FACT: Israeli Altima model/spec pages.
- SOURCE: Cartube Altima 2019 — https://www.cartube.co.il/חדשות-רכב/ניסאן-אלטימה-החדשה-בישראל-מחיר-החל-מ-164990-שקל
  FACT: Israeli 2019 Altima launch/update.
- SOURCE: Cartube Altima initial launch — https://www.cartube.co.il/חדשות-רכב/ניסאן-אלטימה-בישראל-מחיר-החל-מ-175000-שקל
  FACT: Israeli 2013 Altima launch context.
- SOURCE: Auto-data Altima VI — https://www.auto-data.net/en/nissan-altima-vi-2.5-188hp-cvt-33003
  FACT: Global technical support: 2.5 188 hp CVT for VI gen.

### Nissan Ariya

- SOURCE: Cartube Ariya Israel launch — https://www.cartube.co.il/חדשות-רכב/ניסאן-אריה-נוחת-בישראל-מחיר-החל-מ-239990-שקל
  FACT: Israeli Ariya launch with Advance/Evolve/e-4ORCE lineup.
- SOURCE: iCar Ariya — https://www.icar.co.il/ניסאן/ניסאן_אריה/
  FACT: Israeli Ariya technical pages.
- SOURCE: Nissan Israel Ariya source in repo — https://nissanisrael.co.il/models/ariya/
  FACT: Repo-local official-ish Israeli Ariya source; validate if still accessible.
- SOURCE: Yad2 Ariya 2026 Advance — https://www.yad2.co.il/price-list/sub-model/131354/2026
  FACT: Tier 3 Israeli price-list signal; not enough alone for official current clean.

### Nissan GT-R

- SOURCE: Auto.co.il GT-R — https://www.auto.co.il/model/nissan-gt-r_g80
  FACT: Israeli GT-R model page.
- SOURCE: Cartube GT-R 2017 Israel — https://www.cartube.co.il/חדשות-רכב/ניסאן-gt-r-החדשה-2017-בישראל-מחיר-החל-מ-879990-שקל
  FACT: Israeli GT-R 2017 launch/update.
- SOURCE: Auto.co.il GT-R 2011 spec — https://www.auto.co.il/cars/nissan/gt-r/2011/502612/
  FACT: Israeli spec page shows 3.8 turbo, AWD, 570 hp on listed row; check historical year mapping carefully.

### Nissan Juke

- SOURCE: Nissan Israel current Juke — https://www.nissan.co.il/vehicles/new/juke.html
  FACT: Official current Israeli page: 1.0L turbo petrol and 1.6L hybrid versions.
- SOURCE: iCar Juke 2010-2019 — https://www.icar.co.il/ניסאן/ניסאן_ג%27וק/ניסאן_ג%27וק_יד_שנייה_-_דור_1/
  FACT: Israeli first-generation rows.
- SOURCE: Cartube Juke Hybrid Israel — https://www.cartube.co.il/חדשות-רכב/ניסאן-גוק-ההיברידי-2023-בישראל-מחיר-החל-מ-147990-שקל
  FACT: Israeli launch of Juke Hybrid 2023.

### Nissan Leaf

- SOURCE: Nissan Israel Leaf legacy — https://www.nissan.co.il/experience-nissan/legacy-models/leaf.html
  FACT: Official Nissan Israel now lists Leaf as legacy, not current new model.
- SOURCE: Cartube Leaf 2018 Israel — https://www.cartube.co.il/חדשות-רכב/ניסאן-ליף-החדשה-בישראל-מחיר-החל-מ-164-990-שקל
  FACT: Israeli Leaf 40 kWh / 150 hp launch context.
- SOURCE: Gear Leaf e+ Israel — https://www.gear.co.il/חדשות_רכב/2021-06-21-ניסאן-ליף-e-plus-ישראל
  FACT: Israeli Leaf e+ 217 hp source.
- SOURCE: iCar Leaf 2013-2018 — https://www.icar.co.il/ניסאן/ניסאן_ליף/ניסאן_ליף_דגמי_2013-2018/
  FACT: Israeli first Leaf generation 109 hp.

### Nissan Maxima

- SOURCE: iCar Maxima 1995-1999 — https://www.icar.co.il/ניסאן/ניסאן_מקסימה/ניסאן_מקסימה_דור_4/
  FACT: Israeli 1995-1999 Maxima rows.
- SOURCE: iCar Maxima 2000-2003 — https://www.icar.co.il/ניסאן/ניסאן_מקסימה/ניסאן_מקסימה_דור_5/
  FACT: Israeli 2000-2003 Maxima rows.
- SOURCE: Auto.co.il Maxima 2016-2021 — https://www.auto.co.il/model/nissan-maxima_g1281
  FACT: Israeli 2016-2021 Maxima.
- SOURCE: Cartube Maxima 2016 Israel — https://www.cartube.co.il/חדשות-רכב/ניסאן-מקסימה-החדשה-2016-בישראל-מחיר-החל-מ-239-900-שקל
  FACT: Israeli 2016 launch; 3.5L V6 300 hp Xtronic CVT.

### Nissan Micra

- SOURCE: Cartube Micra 2019 Israel — https://www.cartube.co.il/חדשות-רכב/ניסאן-מיקרה-החדשה-2019-בישראל-מחיר-החל-מ-94,990-שקל
  FACT: Israeli 2019 Micra 1.0T 100 hp launch.
- SOURCE: Auto.co.il Micra 2019 — https://www.auto.co.il/cars/nissan/micra/2019/
  FACT: Israeli technical statement: 1.0 turbo 100 hp, CVT/manual.
- SOURCE: iCar Micra 2011-2018 — https://www.icar.co.il/ניסאן/ניסאן_מיקרה/ניסאן_מיקרה_יד_שנייה_12/
  FACT: Israeli 1.2 80 hp rows.
- SOURCE: Yad2 Micra feed — https://www.yad2.co.il/vehicles/cars?manufacturer=32&model=10438
  FACT: Tier 3 support for sub-models 1.2 80 hp and 1.0 100 hp.

### Nissan Murano

- SOURCE: iCar Murano 2005-2008 — https://www.icar.co.il/ניסאן/ניסאן_מוראנו/ניסאן_מוראנו_דור_1/
  FACT: Israeli first-gen Murano 3.5 CVT.
- SOURCE: Auto.co.il Murano 2008-2014 — https://www.auto.co.il/model/nissan-murano_g144
  FACT: Israeli second-gen Murano.
- SOURCE: Yad2 Murano 2008 — https://www.yad2.co.il/price-list/sub-model/106925/2008
  FACT: Tier 3 Israeli price-list/spec signal for 2008 3.5 234 hp.
- SOURCE: Carzone Murano — https://www.carzone.co.il/prices/ניסאן/מוראנו/
  FACT: Tier 3 Israeli price-list/used-market signal.


---

# Variant-level instructions


## MODEL PROFILE: `IL-confirmed|Mitsubishi|Space Star`

Profile variants: 3

### VARIANT 1/3

MODEL: Mitsubishi Space Star

PROFILE KEY: `IL-confirmed|Mitsubishi|Space Star`

CURRENT VALUE: `year_start=2013, year_end=2014, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.0, horsepower_hp=71, transmission='5-speed manual', drivetrain='FWD'`

PROBLEM: Null trim needs justification; verify engine/power/year row is Israeli, not global.

WEB-VALIDATED FACT: Israeli launch/used-car sources support Space Star 1.0 71 hp manual and 1.2 80 hp CVT historical rows.

SOURCE: See RUN 1 source pack for Mitsubishi Space Star; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP with field_sources for body/fuel/engine/hp/transmission/drivetrain/years; trim null accepted only as aggregate technical row, not as missing source.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/3

MODEL: Mitsubishi Space Star

PROFILE KEY: `IL-confirmed|Mitsubishi|Space Star`

CURRENT VALUE: `year_start=2013, year_end=2020, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.2, horsepower_hp=80, transmission='cvt', drivetrain='FWD'`

PROBLEM: Null trim needs justification; verify engine/power/year row is Israeli, not global.

WEB-VALIDATED FACT: Israeli launch/used-car sources support Space Star 1.0 71 hp manual and 1.2 80 hp CVT historical rows.

SOURCE: See RUN 1 source pack for Mitsubishi Space Star; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP with field_sources for body/fuel/engine/hp/transmission/drivetrain/years; trim null accepted only as aggregate technical row, not as missing source.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 3/3

MODEL: Mitsubishi Space Star

PROFILE KEY: `IL-confirmed|Mitsubishi|Space Star`

CURRENT VALUE: `year_start=2021, year_end=2025, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.2, horsepower_hp=71, transmission='cvt', drivetrain='FWD'`

PROBLEM: Current-period row needs explicit no-extension rule and battery fields not applicable.

WEB-VALIDATED FACT: Israeli sources support the 2021 facelift 1.2L 71 hp CVT FWD; Mitsubishi current price lists must be used before extending beyond 2025.

SOURCE: See RUN 1 source pack for Mitsubishi Space Star; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP as 2021-2025 1.2L petrol 71 hp CVT FWD; do not extend past 2025 unless repo-local official Mitsubishi 2026 source is attached. Trim may stay null only as aggregate technical row; available_values should include Supreme/Premium/Instyle if repo stores trims separately.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|Mitsubishi|Space Wagon`

Profile variants: 2

### VARIANT 1/2

MODEL: Mitsubishi Space Wagon

PROFILE KEY: `IL-confirmed|Mitsubishi|Space Wagon`

CURRENT VALUE: `version_or_trim='GLX', year_start=1992, year_end=1998, body_type='MPV', fuel_type='petrol', engine_displacement_l=2.0, horsepower_hp=133, transmission='4-speed automatic', drivetrain='FWD'`

PROBLEM: Historical row needs local-market grounding.

WEB-VALIDATED FACT: Israeli sources support Space Wagon GLXI 2.0 133 hp automatic FWD around the 1998-2001 period and model line 1992-1998.

SOURCE: See RUN 1 source pack for Mitsubishi Space Wagon; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP 2.0L petrol 133 hp 4AT FWD; do not currentize. Preserve GLX/GLXI lineage if schema supports trim aliases.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/2

MODEL: Mitsubishi Space Wagon

PROFILE KEY: `IL-confirmed|Mitsubishi|Space Wagon`

CURRENT VALUE: `version_or_trim='GLX', year_start=1998, year_end=2003, body_type='MPV', fuel_type='petrol', engine_displacement_l=2.4, horsepower_hp=150, transmission='4-speed automatic', drivetrain='FWD'`

PROBLEM: 2.4L horsepower varies between local price-list rounding 147 and technical sources 150; avoid silent contradiction.

WEB-VALIDATED FACT: Israeli/Israel-context sources support Space Wagon 2.4 automatic FWD around 147/150 hp; technical source supports 150 hp while Yad2 may show 147 hp due to PS/kW rounding.

SOURCE: See RUN 1 source pack for Mitsubishi Space Wagon; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP 2.4L 150 hp only if existing field_sources directly support 150; otherwise set horsepower_hp=147 and note local price-list rounding. Preserve 1998-2003 historical status, not current.

ACTION: KEEP/FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|NIO|EL6`

Profile variants: 2

### VARIANT 1/2

MODEL: NIO EL6

PROFILE KEY: `IL-confirmed|NIO|EL6`

CURRENT VALUE: `version_or_trim='75 kWh', year_start=2024, year_end=2024, body_type='SUV', fuel_type='electric', horsepower_hp=489, transmission='single_speed', drivetrain='AWD'`

PROBLEM: battery_kwh and range are missing; year_end=2024 wrongly closes a current Israeli model.

WEB-VALIDATED FACT: Official NIO Israel 02/2026 price list and PDF support eL6 Standard Range 75 KWH, 489 hp, Intelligent E-AWD, WLTP 406 km.

SOURCE: See RUN 1 source pack for NIO EL6; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX to version_or_trim="Standard Range 75 kWh", year_start=2024, year_end=null/current, battery_kwh=75, electric_range_km_wltp=406, electric, displacement null, 489 hp, single_speed/direct_drive, AWD.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/2

MODEL: NIO EL6

PROFILE KEY: `IL-confirmed|NIO|EL6`

CURRENT VALUE: `version_or_trim='100 kWh', year_start=2024, year_end=2024, body_type='SUV', fuel_type='electric', horsepower_hp=489, transmission='single_speed', drivetrain='AWD'`

PROBLEM: battery_kwh and range are missing; year_end=2024 wrongly closes a current Israeli model; 100 kWh Comfort Pack trim is missing if trim rows are stored.

WEB-VALIDATED FACT: Official NIO Israel 02/2026 price list supports eL6 Long Range 100 KWH and Long Range Comfort Pack 100 KWH; PDF supports 489 hp, AWD and WLTP 523 km for 100 kWh.

SOURCE: See RUN 1 source pack for NIO EL6; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX to version_or_trim="Long Range 100 kWh", year_start=2024, year_end=null/current, battery_kwh=100, electric_range_km_wltp=523, 489 hp, single_speed/direct_drive, AWD. ADD sibling trim "Long Range Comfort Pack 100 kWh" with same technical fields if schema keeps trim-level rows.

ACTION: FIX/ADD

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|NIO|EL7`

Profile variants: 2

### VARIANT 1/2

MODEL: NIO EL7

PROFILE KEY: `IL-confirmed|NIO|EL7`

CURRENT VALUE: `version_or_trim='75kWh', year_start=2023, body_type='SUV', fuel_type='electric', horsepower_hp=653, transmission='single_speed', drivetrain='AWD'`

PROBLEM: 75 kWh EL7 appears unsupported as an Israeli clean row; Israeli sources found mainly/only 100 kWh.

WEB-VALIDATED FACT: Israeli iCar/Auto/Carzone/Cartube references support EL7 100 kWh AWD 653 hp; current NIO official price list does not show EL7, and public local sources for EL7 center on 100 kWh.

SOURCE: See RUN 1 source pack for NIO EL7; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MOVE 75 kWh EL7 to non-blocking review/archive with reason="Israeli 75 kWh EL7 not grounded" unless existing repo-local source explicitly proves Israeli sale. Do not keep as clean by global reference only.

ACTION: MOVE TO REVIEW

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/2

MODEL: NIO EL7

PROFILE KEY: `IL-confirmed|NIO|EL7`

CURRENT VALUE: `version_or_trim='100kWh', year_start=2023, body_type='SUV', fuel_type='electric', horsepower_hp=653, transmission='single_speed', drivetrain='AWD'`

PROBLEM: battery_kwh/range missing and year_start/current status needs normalization.

WEB-VALIDATED FACT: Israeli sources support EL7 100 kWh, 653 hp, AWD, direct/single-speed style transmission, range around 501 km; Carzone/Cartube still list 2026 but official NIO 02/2026 price list omits EL7, so current status should be source-policy controlled.

SOURCE: See RUN 1 source pack for NIO EL7; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX to single canonical 100 kWh row: battery_kwh=100, horsepower_hp=653, drivetrain=AWD, transmission=single_speed/direct_drive, electric_range_km_wltp=501. Set year_start=2024 if repo-local launch evidence supports 2024; keep current/null only if local current price source is accepted, otherwise year_end=2025/2026 per source policy.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|Nissan|200SX`

Profile variants: 2

### VARIANT 1/2

MODEL: Nissan 200SX

PROFILE KEY: `IL-confirmed|Nissan|200SX`

CURRENT VALUE: `year_start=1994, year_end=1999, body_type='Coupe', fuel_type='petrol', engine_displacement_l=2.0, horsepower_hp=200, transmission='5-speed manual', drivetrain='RWD'`

PROBLEM: version_or_trim is null; technical row is real but should carry 2.0 Turbo lineage.

WEB-VALIDATED FACT: Israeli Auto/KML sources support Nissan 200SX 1994-1999 coupe, 2.0 turbo 200 hp, RWD, manual/automatic.

SOURCE: See RUN 1 source pack for Nissan 200SX; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX version_or_trim to "2.0 Turbo" (or equivalent trim alias) for both manual and automatic rows; keep years 1994-1999, 200 hp, RWD, coupe.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/2

MODEL: Nissan 200SX

PROFILE KEY: `IL-confirmed|Nissan|200SX`

CURRENT VALUE: `year_start=1994, year_end=1999, body_type='Coupe', fuel_type='petrol', engine_displacement_l=2.0, horsepower_hp=200, transmission='4-speed automatic', drivetrain='RWD'`

PROBLEM: version_or_trim is null; technical row is real but should carry 2.0 Turbo lineage.

WEB-VALIDATED FACT: Israeli Auto/KML sources support Nissan 200SX 1994-1999 coupe, 2.0 turbo 200 hp, RWD, manual/automatic.

SOURCE: See RUN 1 source pack for Nissan 200SX; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX version_or_trim to "2.0 Turbo" (or equivalent trim alias) for both manual and automatic rows; keep years 1994-1999, 200 hp, RWD, coupe.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `global-reference-only|Nissan|200SX`

Profile variants: 2

### VARIANT 1/2

MODEL: Nissan 200SX

PROFILE KEY: `global-reference-only|Nissan|200SX`

CURRENT VALUE: `year_start=1995, year_end=2000, body_type='Coupe', fuel_type='petrol', engine_displacement_l=2.0, horsepower_hp=200, transmission='manual', drivetrain='RWD'`

PROBLEM: Duplicate global-reference-only profile overlaps IL-confirmed Nissan 200SX.

WEB-VALIDATED FACT: Israeli IL-confirmed profile already covers the same 2.0 turbo 200 hp manual/automatic technical variants for 1994-1999.

SOURCE: See RUN 1 source pack for Nissan 200SX; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE into IL-confirmed|Nissan|200SX as source_alias_keys/lineage, then ARCHIVE NON-BLOCKING or DELETE DUPLICATE from clean. Do not keep global-reference-only as a separate clean profile.

ACTION: MERGE/ARCHIVE NON-BLOCKING

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/2

MODEL: Nissan 200SX

PROFILE KEY: `global-reference-only|Nissan|200SX`

CURRENT VALUE: `year_start=1995, year_end=2000, body_type='Coupe', fuel_type='petrol', engine_displacement_l=2.0, horsepower_hp=200, transmission='automatic', drivetrain='RWD'`

PROBLEM: Duplicate global-reference-only profile overlaps IL-confirmed Nissan 200SX.

WEB-VALIDATED FACT: Israeli IL-confirmed profile already covers the same 2.0 turbo 200 hp manual/automatic technical variants for 1994-1999.

SOURCE: See RUN 1 source pack for Nissan 200SX; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE into IL-confirmed|Nissan|200SX as source_alias_keys/lineage, then ARCHIVE NON-BLOCKING or DELETE DUPLICATE from clean. Do not keep global-reference-only as a separate clean profile.

ACTION: MERGE/ARCHIVE NON-BLOCKING

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `global-reference-only|Nissan|370Z`

Profile variants: 3

### VARIANT 1/3

MODEL: Nissan 370Z

PROFILE KEY: `global-reference-only|Nissan|370Z`

CURRENT VALUE: `year_start=2009, year_end=2020, body_type='Coupe', fuel_type='petrol', engine_displacement_l=3.7, horsepower_hp=328, transmission='6-speed manual', drivetrain='RWD'`

PROBLEM: Duplicate global/likely 370Z row overlaps IL-confirmed 370Z.

WEB-VALIDATED FACT: IL-confirmed profile already covers 3.7L V6 328 hp coupe manual/automatic; global/likely rows duplicate or extend it.

SOURCE: See RUN 1 source pack for Nissan 370Z; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE sources/aliases into IL-confirmed|Nissan|370Z and remove duplicate clean profile. Keep only one canonical coupe manual row and one coupe 7AT row.

ACTION: MERGE/DELETE DUPLICATE

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/3

MODEL: Nissan 370Z

PROFILE KEY: `global-reference-only|Nissan|370Z`

CURRENT VALUE: `year_start=2009, year_end=2020, body_type='Coupe', fuel_type='petrol', engine_displacement_l=3.7, horsepower_hp=328, transmission='7-speed automatic', drivetrain='RWD'`

PROBLEM: Duplicate global/likely 370Z row overlaps IL-confirmed 370Z.

WEB-VALIDATED FACT: IL-confirmed profile already covers 3.7L V6 328 hp coupe manual/automatic; global/likely rows duplicate or extend it.

SOURCE: See RUN 1 source pack for Nissan 370Z; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE sources/aliases into IL-confirmed|Nissan|370Z and remove duplicate clean profile. Keep only one canonical coupe manual row and one coupe 7AT row.

ACTION: MERGE/DELETE DUPLICATE

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 3/3

MODEL: Nissan 370Z

PROFILE KEY: `global-reference-only|Nissan|370Z`

CURRENT VALUE: `version_or_trim='Nismo', year_start=2015, year_end=2020, body_type='Coupe', fuel_type='petrol', engine_displacement_l=3.7, horsepower_hp=344, transmission='6-speed manual', drivetrain='RWD'`

PROBLEM: Nismo is a real Israeli-market/special row but lives under a global-reference-only duplicate profile.

WEB-VALIDATED FACT: Cartube reports 370Z Nismo in Israel; technical values are 3.7L V6, 344 hp, RWD, manual, coupe.

SOURCE: See RUN 1 source pack for Nissan 370Z; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE Nismo row into canonical IL-confirmed|Nissan|370Z with version_or_trim="Nismo", year_start=2015, year_end=2020, 3.7L petrol, 344 hp, 6-speed manual, RWD. Archive duplicate source profile non-blocking with lineage.

ACTION: MERGE

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-likely|Nissan|370Z`

Profile variants: 3

### VARIANT 1/3

MODEL: Nissan 370Z

PROFILE KEY: `IL-likely|Nissan|370Z`

CURRENT VALUE: `year_start=2010, year_end=2019, body_type='Coupe', fuel_type='petrol', engine_displacement_l=3.7, horsepower_hp=328, transmission='7-speed automatic', drivetrain='RWD'`

PROBLEM: Duplicate global/likely 370Z row overlaps IL-confirmed 370Z.

WEB-VALIDATED FACT: IL-confirmed profile already covers 3.7L V6 328 hp coupe manual/automatic; global/likely rows duplicate or extend it.

SOURCE: See RUN 1 source pack for Nissan 370Z; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE sources/aliases into IL-confirmed|Nissan|370Z and remove duplicate clean profile. Keep only one canonical coupe manual row and one coupe 7AT row.

ACTION: MERGE/DELETE DUPLICATE

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/3

MODEL: Nissan 370Z

PROFILE KEY: `IL-likely|Nissan|370Z`

CURRENT VALUE: `year_start=2010, year_end=2019, body_type='Coupe', fuel_type='petrol', engine_displacement_l=3.7, horsepower_hp=328, transmission='6-speed manual', drivetrain='RWD'`

PROBLEM: Duplicate global/likely 370Z row overlaps IL-confirmed 370Z.

WEB-VALIDATED FACT: IL-confirmed profile already covers 3.7L V6 328 hp coupe manual/automatic; global/likely rows duplicate or extend it.

SOURCE: See RUN 1 source pack for Nissan 370Z; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE sources/aliases into IL-confirmed|Nissan|370Z and remove duplicate clean profile. Keep only one canonical coupe manual row and one coupe 7AT row.

ACTION: MERGE/DELETE DUPLICATE

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 3/3

MODEL: Nissan 370Z

PROFILE KEY: `IL-likely|Nissan|370Z`

CURRENT VALUE: `year_start=2010, year_end=2015, body_type='Roadster', fuel_type='petrol', engine_displacement_l=3.7, horsepower_hp=328, transmission='7-speed automatic', drivetrain='RWD'`

PROBLEM: Roadster row is in IL-likely duplicate profile, not canonical confirmed profile.

WEB-VALIDATED FACT: iCar/Auto 370Z Israeli references include coupe/roadster generations; roadster is plausible Israeli technical row but must not remain in IL-likely split profile.

SOURCE: See RUN 1 source pack for Nissan 370Z; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE Roadster 3.7L 328 hp 7AT RWD into IL-confirmed|Nissan|370Z if repo-local iCar/Auto source supports it; otherwise move this row to non-blocking review. Archive IL-likely source profile after merge/review.

ACTION: MERGE/MOVE TO REVIEW

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|Nissan|370Z`

Profile variants: 2

### VARIANT 1/2

MODEL: Nissan 370Z

PROFILE KEY: `IL-confirmed|Nissan|370Z`

CURRENT VALUE: `year_start=2010, year_end=2020, body_type='Coupe', fuel_type='petrol', engine_displacement_l=3.7, horsepower_hp=328, transmission='6-speed manual', drivetrain='RWD'`

PROBLEM: Null trim is acceptable only if row represents base coupe; duplicate global/likely rows must not remain.

WEB-VALIDATED FACT: Israeli iCar/Auto sources support 370Z 3.7L 328 hp coupe with manual and 7AT RWD for 2010-2020.

SOURCE: See RUN 1 source pack for Nissan 370Z; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP canonical coupe rows; set version_or_trim="Coupe" or "Base Coupe" if schema requires non-null trim. Accept merged Nismo/Roadster only as separate rows with lineage/source support.

ACTION: KEEP/FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/2

MODEL: Nissan 370Z

PROFILE KEY: `IL-confirmed|Nissan|370Z`

CURRENT VALUE: `year_start=2010, year_end=2020, body_type='Coupe', fuel_type='petrol', engine_displacement_l=3.7, horsepower_hp=328, transmission='7-speed automatic', drivetrain='RWD'`

PROBLEM: Null trim is acceptable only if row represents base coupe; duplicate global/likely rows must not remain.

WEB-VALIDATED FACT: Israeli iCar/Auto sources support 370Z 3.7L 328 hp coupe with manual and 7AT RWD for 2010-2020.

SOURCE: See RUN 1 source pack for Nissan 370Z; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP canonical coupe rows; set version_or_trim="Coupe" or "Base Coupe" if schema requires non-null trim. Accept merged Nismo/Roadster only as separate rows with lineage/source support.

ACTION: KEEP/FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|Nissan|Almera`

Profile variants: 7

### VARIANT 1/7

MODEL: Nissan Almera

PROFILE KEY: `IL-confirmed|Nissan|Almera`

CURRENT VALUE: `year_start=1995, year_end=2000, body_type='Sedan', fuel_type='petrol', engine_displacement_l=1.6, horsepower_hp=99, transmission='5-speed manual', drivetrain='FWD'`

PROBLEM: year_start=1995 conflicts with Israeli source title/generation that appears 1996-2000; trim null needs aggregate justification.

WEB-VALIDATED FACT: Israeli iCar first-gen Almera source is 1996-2000; 1.6L 99 hp FWD sedan/hatchback manual/automatic variants are supported.

SOURCE: See RUN 1 source pack for Nissan Almera; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX year_start from 1995 to 1996 for first-generation 1.6L rows unless repo-local source explicitly supports 1995 Israeli sale. Keep body/transmission split and FWD.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/7

MODEL: Nissan Almera

PROFILE KEY: `IL-confirmed|Nissan|Almera`

CURRENT VALUE: `year_start=1995, year_end=2000, body_type='Sedan', fuel_type='petrol', engine_displacement_l=1.6, horsepower_hp=99, transmission='4-speed automatic', drivetrain='FWD'`

PROBLEM: year_start=1995 conflicts with Israeli source title/generation that appears 1996-2000; trim null needs aggregate justification.

WEB-VALIDATED FACT: Israeli iCar first-gen Almera source is 1996-2000; 1.6L 99 hp FWD sedan/hatchback manual/automatic variants are supported.

SOURCE: See RUN 1 source pack for Nissan Almera; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX year_start from 1995 to 1996 for first-generation 1.6L rows unless repo-local source explicitly supports 1995 Israeli sale. Keep body/transmission split and FWD.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 3/7

MODEL: Nissan Almera

PROFILE KEY: `IL-confirmed|Nissan|Almera`

CURRENT VALUE: `year_start=1995, year_end=2000, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.6, horsepower_hp=99, transmission='5-speed manual', drivetrain='FWD'`

PROBLEM: year_start=1995 conflicts with Israeli source title/generation that appears 1996-2000; trim null needs aggregate justification.

WEB-VALIDATED FACT: Israeli iCar first-gen Almera source is 1996-2000; 1.6L 99 hp FWD sedan/hatchback manual/automatic variants are supported.

SOURCE: See RUN 1 source pack for Nissan Almera; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX year_start from 1995 to 1996 for first-generation 1.6L rows unless repo-local source explicitly supports 1995 Israeli sale. Keep body/transmission split and FWD.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 4/7

MODEL: Nissan Almera

PROFILE KEY: `IL-confirmed|Nissan|Almera`

CURRENT VALUE: `year_start=1995, year_end=2000, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.6, horsepower_hp=99, transmission='4-speed automatic', drivetrain='FWD'`

PROBLEM: year_start=1995 conflicts with Israeli source title/generation that appears 1996-2000; trim null needs aggregate justification.

WEB-VALIDATED FACT: Israeli iCar first-gen Almera source is 1996-2000; 1.6L 99 hp FWD sedan/hatchback manual/automatic variants are supported.

SOURCE: See RUN 1 source pack for Nissan Almera; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX year_start from 1995 to 1996 for first-generation 1.6L rows unless repo-local source explicitly supports 1995 Israeli sale. Keep body/transmission split and FWD.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 5/7

MODEL: Nissan Almera

PROFILE KEY: `IL-confirmed|Nissan|Almera`

CURRENT VALUE: `year_start=2000, year_end=2006, body_type='Sedan', fuel_type='petrol', engine_displacement_l=1.5, horsepower_hp=90, transmission='5-speed manual', drivetrain='FWD'`

PROBLEM: Second-generation row must keep exact Perfect/engine/body split and not overextend.

WEB-VALIDATED FACT: Israeli iCar/Auto sources support Almera 2000-2006, including 1.5 90 hp manual and 1.8 114 hp Perfect automatic sedan/hatchback.

SOURCE: See RUN 1 source pack for Nissan Almera; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP 2000-2006 rows with Perfect trim where present; ensure field_sources exist for body/fuel/engine/hp/transmission/drivetrain/years.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 6/7

MODEL: Nissan Almera

PROFILE KEY: `IL-confirmed|Nissan|Almera`

CURRENT VALUE: `version_or_trim='Perfect', year_start=2000, year_end=2006, body_type='Sedan', fuel_type='petrol', engine_displacement_l=1.8, horsepower_hp=114, transmission='4-speed automatic', drivetrain='FWD'`

PROBLEM: Second-generation row must keep exact Perfect/engine/body split and not overextend.

WEB-VALIDATED FACT: Israeli iCar/Auto sources support Almera 2000-2006, including 1.5 90 hp manual and 1.8 114 hp Perfect automatic sedan/hatchback.

SOURCE: See RUN 1 source pack for Nissan Almera; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP 2000-2006 rows with Perfect trim where present; ensure field_sources exist for body/fuel/engine/hp/transmission/drivetrain/years.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 7/7

MODEL: Nissan Almera

PROFILE KEY: `IL-confirmed|Nissan|Almera`

CURRENT VALUE: `version_or_trim='Perfect', year_start=2000, year_end=2006, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.8, horsepower_hp=114, transmission='4-speed automatic', drivetrain='FWD'`

PROBLEM: Second-generation row must keep exact Perfect/engine/body split and not overextend.

WEB-VALIDATED FACT: Israeli iCar/Auto sources support Almera 2000-2006, including 1.5 90 hp manual and 1.8 114 hp Perfect automatic sedan/hatchback.

SOURCE: See RUN 1 source pack for Nissan Almera; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP 2000-2006 rows with Perfect trim where present; ensure field_sources exist for body/fuel/engine/hp/transmission/drivetrain/years.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|Nissan|Altima`

Profile variants: 2

### VARIANT 1/2

MODEL: Nissan Altima

PROFILE KEY: `IL-confirmed|Nissan|Altima`

CURRENT VALUE: `version_or_trim='SV', year_start=2013, year_end=2018, body_type='Sedan', fuel_type='petrol', engine_displacement_l=2.5, horsepower_hp=182, transmission='cvt', drivetrain='FWD'`

PROBLEM: Verify Israeli-market years and generation split; do not currentize.

WEB-VALIDATED FACT: Israeli iCar/Cartube sources support Altima 2013 launch with 2.5L CVT around 182 hp and 2019 generation with 2.5L 188 hp CVT.

SOURCE: See RUN 1 source pack for Nissan Altima; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP SV 2013-2018 2.5L 182 hp CVT FWD and SV 2019-2024 2.5L 188 hp CVT FWD; do not extend beyond 2024 without local current source.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/2

MODEL: Nissan Altima

PROFILE KEY: `IL-confirmed|Nissan|Altima`

CURRENT VALUE: `version_or_trim='SV', year_start=2019, year_end=2024, body_type='Sedan', fuel_type='petrol', engine_displacement_l=2.5, horsepower_hp=188, transmission='cvt', drivetrain='FWD'`

PROBLEM: Verify Israeli-market years and generation split; do not currentize.

WEB-VALIDATED FACT: Israeli iCar/Cartube sources support Altima 2013 launch with 2.5L CVT around 182 hp and 2019 generation with 2.5L 188 hp CVT.

SOURCE: See RUN 1 source pack for Nissan Altima; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP SV 2013-2018 2.5L 182 hp CVT FWD and SV 2019-2024 2.5L 188 hp CVT FWD; do not extend beyond 2024 without local current source.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|Nissan|Ariya`

Profile variants: 3

### VARIANT 1/3

MODEL: Nissan Ariya

PROFILE KEY: `IL-confirmed|Nissan|Ariya`

CURRENT VALUE: `version_or_trim='Advance', year_start=2023, year_end=2024, body_type='SUV', fuel_type='electric', horsepower_hp=218, transmission='single_speed', drivetrain='FWD'`

PROBLEM: battery_kwh/range missing; current status should not be inferred from global pages.

WEB-VALIDATED FACT: Israeli launch sources support Ariya Advance with 63/66 kWh class battery and 218 hp FWD; Nissan Israel current new-model page did not show Ariya in the latest public list, so do not extend beyond source-grounded years automatically.

SOURCE: See RUN 1 source pack for Nissan Ariya; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX: battery_kwh=63 (or 66 gross if repo schema uses gross; choose one consistently), electric_range_km_wltp per repo official source, transmission=single_speed, drivetrain=FWD, displacement=null. Keep year_end=2024 unless repo-local official source supports later Israeli sales.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/3

MODEL: Nissan Ariya

PROFILE KEY: `IL-confirmed|Nissan|Ariya`

CURRENT VALUE: `version_or_trim='Evolve', year_start=2023, year_end=2024, body_type='SUV', fuel_type='electric', horsepower_hp=242, transmission='single_speed', drivetrain='FWD'`

PROBLEM: battery_kwh/range missing.

WEB-VALIDATED FACT: Israeli/Yad2 and global technical sources support 87 kWh FWD Ariya at 242 hp; local clean depends on repo-local Ariya sources.

SOURCE: See RUN 1 source pack for Nissan Ariya; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX: battery_kwh=87, transmission=single_speed, drivetrain=FWD, displacement=null, range from attached Nissan/iCar source. Keep 2023-2024 unless local source supports 2025/2026.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 3/3

MODEL: Nissan Ariya

PROFILE KEY: `IL-confirmed|Nissan|Ariya`

CURRENT VALUE: `version_or_trim='Evolve e-4ORCE', year_start=2023, year_end=2024, body_type='SUV', fuel_type='electric', horsepower_hp=306, transmission='single_speed', drivetrain='AWD'`

PROBLEM: battery_kwh/range missing; e-4ORCE row needs AWD schema confirmation.

WEB-VALIDATED FACT: Ariya e-4ORCE 87 kWh is 306 hp AWD with single-speed EV drivetrain; Israeli source package supports e-4ORCE row at launch/price-list level.

SOURCE: See RUN 1 source pack for Nissan Ariya; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX: battery_kwh=87, horsepower_hp=306, drivetrain=AWD, transmission=single_speed/direct_drive, displacement=null, range from source. Keep 2023-2024 unless local source supports later years.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|Nissan|GT-R`

Profile variants: 3

### VARIANT 1/3

MODEL: Nissan GT-R

PROFILE KEY: `IL-confirmed|Nissan|GT-R`

CURRENT VALUE: `year_start=2011, year_end=2016, body_type='Coupe', fuel_type='petrol', engine_displacement_l=3.8, horsepower_hp=550, transmission='6-speed dual_clutch', drivetrain='AWD'`

PROBLEM: Historical GT-R 550 hp row should not be current and must have exact local source indexes.

WEB-VALIDATED FACT: Israeli Auto page supports GT-R 3.8 turbo AWD DCT technical identity; 550 hp row is historical pre-2016 update.

SOURCE: See RUN 1 source pack for Nissan GT-R; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP 2011-2016 3.8L turbo 550 hp AWD 6DCT only if source_indexes/field_sources support the 550 hp year range; otherwise split/update.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/3

MODEL: Nissan GT-R

PROFILE KEY: `IL-confirmed|Nissan|GT-R`

CURRENT VALUE: `version_or_trim='Premium Edition', year_start=2016, body_type='Coupe', fuel_type='petrol', engine_displacement_l=3.8, horsepower_hp=570, transmission='6-speed dual_clutch', drivetrain='AWD'`

PROBLEM: year_end=null wrongly implies current; Nissan Israel current model list does not show GT-R.

WEB-VALIDATED FACT: Israeli Auto/Cartube sources support GT-R historical/local rows, including 2017 update and 570 hp versions; no official current Israeli new-car source was found.

SOURCE: See RUN 1 source pack for Nissan GT-R; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX year_end to last repo-local source-supported Israeli marketing year; if exact year_end cannot be grounded, MOVE row to non-blocking review rather than leave current. Preserve Premium/Black Edition trims and 3.8L turbo AWD 6DCT 570 hp.

ACTION: FIX/MOVE TO REVIEW

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 3/3

MODEL: Nissan GT-R

PROFILE KEY: `IL-confirmed|Nissan|GT-R`

CURRENT VALUE: `version_or_trim='Black Edition', year_start=2016, body_type='Coupe', fuel_type='petrol', engine_displacement_l=3.8, horsepower_hp=570, transmission='6-speed dual_clutch', drivetrain='AWD'`

PROBLEM: year_end=null wrongly implies current; Nissan Israel current model list does not show GT-R.

WEB-VALIDATED FACT: Israeli Auto/Cartube sources support GT-R historical/local rows, including 2017 update and 570 hp versions; no official current Israeli new-car source was found.

SOURCE: See RUN 1 source pack for Nissan GT-R; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX year_end to last repo-local source-supported Israeli marketing year; if exact year_end cannot be grounded, MOVE row to non-blocking review rather than leave current. Preserve Premium/Black Edition trims and 3.8L turbo AWD 6DCT 570 hp.

ACTION: FIX/MOVE TO REVIEW

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|Nissan|Juke`

Profile variants: 6

### VARIANT 1/6

MODEL: Nissan Juke

PROFILE KEY: `IL-confirmed|Nissan|Juke`

CURRENT VALUE: `year_start=2010, year_end=2019, body_type='Crossover', fuel_type='petrol', engine_displacement_l=1.6, horsepower_hp=117, transmission='cvt', drivetrain='FWD'`

PROBLEM: Historical row needs no current extension; trim null accepted only as aggregate.

WEB-VALIDATED FACT: Israeli iCar source supports first-gen Juke rows: 1.6 117 hp CVT/manual, 1.2T 115 hp manual, and early second-gen 1.0T 117 hp DCT.

SOURCE: See RUN 1 source pack for Nissan Juke; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP with exact historical years and field_sources; do not currentize these old rows.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/6

MODEL: Nissan Juke

PROFILE KEY: `IL-confirmed|Nissan|Juke`

CURRENT VALUE: `year_start=2010, year_end=2019, body_type='Crossover', fuel_type='petrol', engine_displacement_l=1.6, horsepower_hp=117, transmission='manual', drivetrain='FWD'`

PROBLEM: Historical row needs no current extension; trim null accepted only as aggregate.

WEB-VALIDATED FACT: Israeli iCar source supports first-gen Juke rows: 1.6 117 hp CVT/manual, 1.2T 115 hp manual, and early second-gen 1.0T 117 hp DCT.

SOURCE: See RUN 1 source pack for Nissan Juke; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP with exact historical years and field_sources; do not currentize these old rows.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 3/6

MODEL: Nissan Juke

PROFILE KEY: `IL-confirmed|Nissan|Juke`

CURRENT VALUE: `year_start=2014, year_end=2019, body_type='Crossover', fuel_type='petrol', engine_displacement_l=1.2, horsepower_hp=115, transmission='manual', drivetrain='FWD'`

PROBLEM: Historical row needs no current extension; trim null accepted only as aggregate.

WEB-VALIDATED FACT: Israeli iCar source supports first-gen Juke rows: 1.6 117 hp CVT/manual, 1.2T 115 hp manual, and early second-gen 1.0T 117 hp DCT.

SOURCE: See RUN 1 source pack for Nissan Juke; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP with exact historical years and field_sources; do not currentize these old rows.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 4/6

MODEL: Nissan Juke

PROFILE KEY: `IL-confirmed|Nissan|Juke`

CURRENT VALUE: `year_start=2019, year_end=2021, body_type='Crossover', fuel_type='petrol', engine_displacement_l=1.0, horsepower_hp=117, transmission='dual_clutch', drivetrain='FWD'`

PROBLEM: Historical row needs no current extension; trim null accepted only as aggregate.

WEB-VALIDATED FACT: Israeli iCar source supports first-gen Juke rows: 1.6 117 hp CVT/manual, 1.2T 115 hp manual, and early second-gen 1.0T 117 hp DCT.

SOURCE: See RUN 1 source pack for Nissan Juke; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP with exact historical years and field_sources; do not currentize these old rows.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 5/6

MODEL: Nissan Juke

PROFILE KEY: `IL-confirmed|Nissan|Juke`

CURRENT VALUE: `year_start=2021, year_end=2024, body_type='Crossover', fuel_type='petrol', engine_displacement_l=1.0, horsepower_hp=114, transmission='dual_clutch', drivetrain='FWD'`

PROBLEM: current row is closed at 2024 while Nissan Israel now lists Juke as current with petrol and hybrid engines.

WEB-VALIDATED FACT: Official Nissan Israel current Juke page lists 1.0L turbo petrol and 1.6L hybrid versions; Cartube supports 2023 hybrid launch.

SOURCE: See RUN 1 source pack for Nissan Juke; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX year_end to null/current for source-supported 1.0L turbo 114 hp DCT FWD and 1.6L hybrid 143 hp FWD rows; set version_or_trim to actual current trim family such as Acenta Tech / Acenta Tech TT if schema requires trim rows. Keep old first-gen rows historical.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 6/6

MODEL: Nissan Juke

PROFILE KEY: `IL-confirmed|Nissan|Juke`

CURRENT VALUE: `year_start=2022, year_end=2024, body_type='Crossover', fuel_type='hybrid', engine_displacement_l=1.6, horsepower_hp=143, transmission='automatic', drivetrain='FWD'`

PROBLEM: current row is closed at 2024 while Nissan Israel now lists Juke as current with petrol and hybrid engines.

WEB-VALIDATED FACT: Official Nissan Israel current Juke page lists 1.0L turbo petrol and 1.6L hybrid versions; Cartube supports 2023 hybrid launch.

SOURCE: See RUN 1 source pack for Nissan Juke; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: FIX year_end to null/current for source-supported 1.0L turbo 114 hp DCT FWD and 1.6L hybrid 143 hp FWD rows; set version_or_trim to actual current trim family such as Acenta Tech / Acenta Tech TT if schema requires trim rows. Keep old first-gen rows historical.

ACTION: FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-likely|Nissan|Leaf`

Profile variants: 3

### VARIANT 1/3

MODEL: Nissan Leaf

PROFILE KEY: `IL-likely|Nissan|Leaf`

CURRENT VALUE: `year_start=2018, year_end=2024, body_type='Hatchback', fuel_type='electric', horsepower_hp=150, transmission='single_speed', drivetrain='FWD'`

PROBLEM: Clean profile is IL-likely and battery_kwh/range missing.

WEB-VALIDATED FACT: Cartube/Nissan sources support newer Leaf 40 kWh around 150 hp; Nissan Israel legacy status means do not leave current.

SOURCE: See RUN 1 source pack for Nissan Leaf; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE into IL-confirmed|Nissan|Leaf as 40 kWh 150 hp row, year_start=2018, year_end=2024 only if local source supports; otherwise cap to last official year. Add battery_kwh=40, displacement=null, transmission=single_speed, FWD.

ACTION: MERGE/FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/3

MODEL: Nissan Leaf

PROFILE KEY: `IL-likely|Nissan|Leaf`

CURRENT VALUE: `version_or_trim='e+', year_start=2021, year_end=2024, body_type='Hatchback', fuel_type='electric', horsepower_hp=217, transmission='single_speed', drivetrain='FWD'`

PROBLEM: Clean profile is IL-likely and battery_kwh/range missing.

WEB-VALIDATED FACT: Gear/Israeli sources support Leaf e+ around 217 hp; not a separate model from Leaf.

SOURCE: See RUN 1 source pack for Nissan Leaf; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE into IL-confirmed|Nissan|Leaf as version_or_trim="e+", year_start=2021, year_end=2024 only if local source supports 2024, battery_kwh=62, transmission=single_speed, FWD. Archive IL-likely profile non-blocking.

ACTION: MERGE/FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 3/3

MODEL: Nissan Leaf

PROFILE KEY: `IL-likely|Nissan|Leaf`

CURRENT VALUE: `year_start=2013, year_end=2018, body_type='Hatchback', fuel_type='electric', horsepower_hp=109, transmission='single_speed', drivetrain='FWD'`

PROBLEM: Clean profile is IL-likely while IL-confirmed Nissan Leaf exists in review/blockers; this is split-profile pollution.

WEB-VALIDATED FACT: Israeli iCar supports 2013-2018 Leaf 109 hp; Nissan Israel now lists Leaf under legacy, so not current.

SOURCE: See RUN 1 source pack for Nissan Leaf; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE this 2013-2018 109 hp row into canonical IL-confirmed|Nissan|Leaf in FINAL or now if same-run policy permits. Add battery_kwh from source if available; displacement=null, transmission single_speed, FWD. Archive IL-likely profile non-blocking.

ACTION: MERGE

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|Nissan|Maxima`

Profile variants: 4

### VARIANT 1/4

MODEL: Nissan Maxima

PROFILE KEY: `IL-confirmed|Nissan|Maxima`

CURRENT VALUE: `year_start=1995, year_end=2003, body_type='Sedan', fuel_type='petrol', engine_displacement_l=2.0, horsepower_hp=140, transmission='4-speed automatic', drivetrain='FWD'`

PROBLEM: Need preserve historical split; do not let duplicate global profile create contradictions.

WEB-VALIDATED FACT: Israeli iCar supports 1995-2003 2.0/3.0 rows; Auto/Cartube support 2016 Maxima 3.5 V6 300 hp CVT.

SOURCE: See RUN 1 source pack for Nissan Maxima; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP existing IL-confirmed rows, but prepare to merge global 2004-2008 and 2014-2015 rows only if local source support is attached. Ensure 2016 row year_end is not extended beyond source-supported local marketing period.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/4

MODEL: Nissan Maxima

PROFILE KEY: `IL-confirmed|Nissan|Maxima`

CURRENT VALUE: `year_start=1995, year_end=1999, body_type='Sedan', fuel_type='petrol', engine_displacement_l=3.0, horsepower_hp=193, transmission='4-speed automatic', drivetrain='FWD'`

PROBLEM: Need preserve historical split; do not let duplicate global profile create contradictions.

WEB-VALIDATED FACT: Israeli iCar supports 1995-2003 2.0/3.0 rows; Auto/Cartube support 2016 Maxima 3.5 V6 300 hp CVT.

SOURCE: See RUN 1 source pack for Nissan Maxima; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP existing IL-confirmed rows, but prepare to merge global 2004-2008 and 2014-2015 rows only if local source support is attached. Ensure 2016 row year_end is not extended beyond source-supported local marketing period.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 3/4

MODEL: Nissan Maxima

PROFILE KEY: `IL-confirmed|Nissan|Maxima`

CURRENT VALUE: `year_start=2000, year_end=2003, body_type='Sedan', fuel_type='petrol', engine_displacement_l=3.0, horsepower_hp=200, transmission='4-speed automatic', drivetrain='FWD'`

PROBLEM: Need preserve historical split; do not let duplicate global profile create contradictions.

WEB-VALIDATED FACT: Israeli iCar supports 1995-2003 2.0/3.0 rows; Auto/Cartube support 2016 Maxima 3.5 V6 300 hp CVT.

SOURCE: See RUN 1 source pack for Nissan Maxima; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP existing IL-confirmed rows, but prepare to merge global 2004-2008 and 2014-2015 rows only if local source support is attached. Ensure 2016 row year_end is not extended beyond source-supported local marketing period.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 4/4

MODEL: Nissan Maxima

PROFILE KEY: `IL-confirmed|Nissan|Maxima`

CURRENT VALUE: `year_start=2016, year_end=2021, body_type='Sedan', fuel_type='petrol', engine_displacement_l=3.5, horsepower_hp=300, transmission='cvt', drivetrain='FWD'`

PROBLEM: Need preserve historical split; do not let duplicate global profile create contradictions.

WEB-VALIDATED FACT: Israeli iCar supports 1995-2003 2.0/3.0 rows; Auto/Cartube support 2016 Maxima 3.5 V6 300 hp CVT.

SOURCE: See RUN 1 source pack for Nissan Maxima; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP existing IL-confirmed rows, but prepare to merge global 2004-2008 and 2014-2015 rows only if local source support is attached. Ensure 2016 row year_end is not extended beyond source-supported local marketing period.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `global-reference-only|Nissan|Maxima`

Profile variants: 3

### VARIANT 1/3

MODEL: Nissan Maxima

PROFILE KEY: `global-reference-only|Nissan|Maxima`

CURRENT VALUE: `year_start=2004, year_end=2008, body_type='Sedan', fuel_type='petrol', engine_displacement_l=3.5, horsepower_hp=265, transmission='5-speed automatic', drivetrain='FWD'`

PROBLEM: Global-reference-only row must not remain separate clean profile.

WEB-VALIDATED FACT: Israeli price/model sources are required for Maxima historical generations; global rows may represent valid imported years but belong under IL-confirmed with local source evidence.

SOURCE: See RUN 1 source pack for Nissan Maxima; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE into IL-confirmed Maxima only if source_indexes/field_sources are local; otherwise MOVE TO REVIEW/ARCHIVE NON-BLOCKING. Do not keep global-reference-only clean.

ACTION: MERGE/MOVE TO REVIEW

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/3

MODEL: Nissan Maxima

PROFILE KEY: `global-reference-only|Nissan|Maxima`

CURRENT VALUE: `year_start=2014, year_end=2015, body_type='Sedan', fuel_type='petrol', engine_displacement_l=3.5, horsepower_hp=290, transmission='cvt', drivetrain='FWD'`

PROBLEM: Global-reference-only row must not remain separate clean profile.

WEB-VALIDATED FACT: Israeli price/model sources are required for Maxima historical generations; global rows may represent valid imported years but belong under IL-confirmed with local source evidence.

SOURCE: See RUN 1 source pack for Nissan Maxima; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE into IL-confirmed Maxima only if source_indexes/field_sources are local; otherwise MOVE TO REVIEW/ARCHIVE NON-BLOCKING. Do not keep global-reference-only clean.

ACTION: MERGE/MOVE TO REVIEW

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 3/3

MODEL: Nissan Maxima

PROFILE KEY: `global-reference-only|Nissan|Maxima`

CURRENT VALUE: `year_start=2016, year_end=2022, body_type='Sedan', fuel_type='petrol', engine_displacement_l=3.5, horsepower_hp=300, transmission='cvt', drivetrain='FWD'`

PROBLEM: Duplicate global row overlaps IL-confirmed 2016 Maxima and extends to 2022 without strong Israeli current/source support.

WEB-VALIDATED FACT: Israeli Cartube/Auto support 2016 launch and 3.5 V6 300 hp CVT; local sources generally show 2016-2021/2020, not a separate global clean profile.

SOURCE: See RUN 1 source pack for Nissan Maxima; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE into IL-confirmed Maxima and set year_end to source-supported local end year, not 2022 unless repo source supports 2022. Archive global profile non-blocking.

ACTION: MERGE/FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|Nissan|Micra`

Profile variants: 7

### VARIANT 1/7

MODEL: Nissan Micra

PROFILE KEY: `IL-confirmed|Nissan|Micra`

CURRENT VALUE: `year_start=2019, year_end=2023, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.0, horsepower_hp=100, transmission='cvt', drivetrain='FWD'`

PROBLEM: Null trims need aggregate justification; current years should not extend beyond source.

WEB-VALIDATED FACT: Israeli sources support Micra 1993-2002 1.3 75 hp, 2003-2010 1.4 88 hp, 2011-2018/2019 1.2 80 hp, and 2019-2023 1.0T 100 hp manual/CVT.

SOURCE: See RUN 1 source pack for Nissan Micra; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP rows with existing year ranges and technical fields; set trim aliases/available_values to Visia/Acenta where repo supports. Do not currentize beyond 2023 because Nissan Israel current new-model list no longer lists Micra.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/7

MODEL: Nissan Micra

PROFILE KEY: `IL-confirmed|Nissan|Micra`

CURRENT VALUE: `year_start=2019, year_end=2023, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.0, horsepower_hp=100, transmission='manual', drivetrain='FWD'`

PROBLEM: Null trims need aggregate justification; current years should not extend beyond source.

WEB-VALIDATED FACT: Israeli sources support Micra 1993-2002 1.3 75 hp, 2003-2010 1.4 88 hp, 2011-2018/2019 1.2 80 hp, and 2019-2023 1.0T 100 hp manual/CVT.

SOURCE: See RUN 1 source pack for Nissan Micra; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP rows with existing year ranges and technical fields; set trim aliases/available_values to Visia/Acenta where repo supports. Do not currentize beyond 2023 because Nissan Israel current new-model list no longer lists Micra.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 3/7

MODEL: Nissan Micra

PROFILE KEY: `IL-confirmed|Nissan|Micra`

CURRENT VALUE: `year_start=2011, year_end=2018, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.2, horsepower_hp=80, transmission='cvt', drivetrain='FWD'`

PROBLEM: Null trims need aggregate justification; current years should not extend beyond source.

WEB-VALIDATED FACT: Israeli sources support Micra 1993-2002 1.3 75 hp, 2003-2010 1.4 88 hp, 2011-2018/2019 1.2 80 hp, and 2019-2023 1.0T 100 hp manual/CVT.

SOURCE: See RUN 1 source pack for Nissan Micra; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP rows with existing year ranges and technical fields; set trim aliases/available_values to Visia/Acenta where repo supports. Do not currentize beyond 2023 because Nissan Israel current new-model list no longer lists Micra.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 4/7

MODEL: Nissan Micra

PROFILE KEY: `IL-confirmed|Nissan|Micra`

CURRENT VALUE: `year_start=2011, year_end=2018, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.2, horsepower_hp=80, transmission='manual', drivetrain='FWD'`

PROBLEM: Null trims need aggregate justification; current years should not extend beyond source.

WEB-VALIDATED FACT: Israeli sources support Micra 1993-2002 1.3 75 hp, 2003-2010 1.4 88 hp, 2011-2018/2019 1.2 80 hp, and 2019-2023 1.0T 100 hp manual/CVT.

SOURCE: See RUN 1 source pack for Nissan Micra; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP rows with existing year ranges and technical fields; set trim aliases/available_values to Visia/Acenta where repo supports. Do not currentize beyond 2023 because Nissan Israel current new-model list no longer lists Micra.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 5/7

MODEL: Nissan Micra

PROFILE KEY: `IL-confirmed|Nissan|Micra`

CURRENT VALUE: `year_start=2003, year_end=2010, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.4, horsepower_hp=88, transmission='4-speed automatic', drivetrain='FWD'`

PROBLEM: Null trims need aggregate justification; current years should not extend beyond source.

WEB-VALIDATED FACT: Israeli sources support Micra 1993-2002 1.3 75 hp, 2003-2010 1.4 88 hp, 2011-2018/2019 1.2 80 hp, and 2019-2023 1.0T 100 hp manual/CVT.

SOURCE: See RUN 1 source pack for Nissan Micra; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP rows with existing year ranges and technical fields; set trim aliases/available_values to Visia/Acenta where repo supports. Do not currentize beyond 2023 because Nissan Israel current new-model list no longer lists Micra.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 6/7

MODEL: Nissan Micra

PROFILE KEY: `IL-confirmed|Nissan|Micra`

CURRENT VALUE: `year_start=1993, year_end=2002, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.3, horsepower_hp=75, transmission='cvt', drivetrain='FWD'`

PROBLEM: Null trims need aggregate justification; current years should not extend beyond source.

WEB-VALIDATED FACT: Israeli sources support Micra 1993-2002 1.3 75 hp, 2003-2010 1.4 88 hp, 2011-2018/2019 1.2 80 hp, and 2019-2023 1.0T 100 hp manual/CVT.

SOURCE: See RUN 1 source pack for Nissan Micra; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP rows with existing year ranges and technical fields; set trim aliases/available_values to Visia/Acenta where repo supports. Do not currentize beyond 2023 because Nissan Israel current new-model list no longer lists Micra.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 7/7

MODEL: Nissan Micra

PROFILE KEY: `IL-confirmed|Nissan|Micra`

CURRENT VALUE: `year_start=1993, year_end=2002, body_type='Hatchback', fuel_type='petrol', engine_displacement_l=1.3, horsepower_hp=75, transmission='manual', drivetrain='FWD'`

PROBLEM: Null trims need aggregate justification; current years should not extend beyond source.

WEB-VALIDATED FACT: Israeli sources support Micra 1993-2002 1.3 75 hp, 2003-2010 1.4 88 hp, 2011-2018/2019 1.2 80 hp, and 2019-2023 1.0T 100 hp manual/CVT.

SOURCE: See RUN 1 source pack for Nissan Micra; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP rows with existing year ranges and technical fields; set trim aliases/available_values to Visia/Acenta where repo supports. Do not currentize beyond 2023 because Nissan Israel current new-model list no longer lists Micra.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `IL-confirmed|Nissan|Murano`

Profile variants: 2

### VARIANT 1/2

MODEL: Nissan Murano

PROFILE KEY: `IL-confirmed|Nissan|Murano`

CURRENT VALUE: `year_start=2005, year_end=2008, body_type='SUV', fuel_type='petrol', engine_displacement_l=3.5, horsepower_hp=234, transmission='cvt', drivetrain='AWD'`

PROBLEM: Need protect canonical IL-confirmed values from duplicate global hp/year mismatch.

WEB-VALIDATED FACT: Israeli iCar/Auto/Yad2 support Murano 2005-2008 3.5 CVT AWD around 234/235 hp and 2008-2014 second generation; global 260 hp should not override local source if local profile supports 256.

SOURCE: See RUN 1 source pack for Nissan Murano; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP canonical IL-confirmed rows; ensure source_indexes support 234 and 256 hp. Do not currentize; do not accept global 260 hp duplicate into clean without local support.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/2

MODEL: Nissan Murano

PROFILE KEY: `IL-confirmed|Nissan|Murano`

CURRENT VALUE: `year_start=2008, year_end=2014, body_type='SUV', fuel_type='petrol', engine_displacement_l=3.5, horsepower_hp=256, transmission='cvt', drivetrain='AWD'`

PROBLEM: Need protect canonical IL-confirmed values from duplicate global hp/year mismatch.

WEB-VALIDATED FACT: Israeli iCar/Auto/Yad2 support Murano 2005-2008 3.5 CVT AWD around 234/235 hp and 2008-2014 second generation; global 260 hp should not override local source if local profile supports 256.

SOURCE: See RUN 1 source pack for Nissan Murano; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: KEEP canonical IL-confirmed rows; ensure source_indexes support 234 and 256 hp. Do not currentize; do not accept global 260 hp duplicate into clean without local support.

ACTION: KEEP

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


## MODEL PROFILE: `global-reference-only|Nissan|Murano`

Profile variants: 2

### VARIANT 1/2

MODEL: Nissan Murano

PROFILE KEY: `global-reference-only|Nissan|Murano`

CURRENT VALUE: `year_start=2008, year_end=2014, body_type='SUV', fuel_type='petrol', engine_displacement_l=3.5, horsepower_hp=260, transmission='cvt', drivetrain='AWD'`

PROBLEM: Global duplicate conflicts with IL-confirmed second-gen Murano horsepower value.

WEB-VALIDATED FACT: IL-confirmed Israeli sources support the same 2008-2014 Murano generation but use local value 256 hp; global/other sources show 260/265 depending standard/rounding.

SOURCE: See RUN 1 source pack for Nissan Murano; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE/ARCHIVE global profile; if importing this row, FIX horsepower to IL-confirmed local value 256 and preserve only one canonical Murano profile.

ACTION: MERGE/FIX

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.

### VARIANT 2/2

MODEL: Nissan Murano

PROFILE KEY: `global-reference-only|Nissan|Murano`

CURRENT VALUE: `year_start=2004, year_end=2008, body_type='SUV', fuel_type='petrol', engine_displacement_l=3.5, horsepower_hp=234, transmission='cvt', drivetrain='AWD'`

PROBLEM: Global duplicate overlaps IL-confirmed first-gen Murano.

WEB-VALIDATED FACT: IL-confirmed profile already covers 2005-2008 3.5 CVT AWD 234 hp.

SOURCE: See RUN 1 source pack for Nissan Murano; prefer Tier 1/2 local sources listed there and existing repo-local source_indexes/field_sources.

TARGET VALUE: MERGE source/alias into IL-confirmed and remove/archive global duplicate non-blocking.

ACTION: MERGE/ARCHIVE NON-BLOCKING

FIELD-LEVEL VALIDATION REQUIRED: validate market existence, trim/name, year_start/year_end, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, EV schema where applicable, source_indexes, field_sources, duplicate/alias/lineage.


---

# RUN 1 coverage assertion

Covered variant decisions: 63/63.

RUN 1 must not be marked complete unless every profile and every variant above was applied or explicitly reported as conflicting with repo-local evidence.

# Required report from Codex

When finished, report:

1. Files changed.
2. Exact before/after metrics.
3. Confirmation that all 20 profiles and all 63 variants were handled.
4. Test results.
5. Confirmation that temporary `codex_tasks/BATCH27_RUN1_*.md` files were deleted before final commit.
6. Remaining issues, if any.


---

# BATCH27 RUN 2 — VARIANT-LEVEL CODEX TASK

## Mandatory execution rules
Do not browse the internet. All web-validation facts and target corrections are embedded in this task file. Use this task file as the single source of truth. Do not apply corrections that are not instructed here. If repo-local evidence conflicts with this task file, report it instead of guessing. If a variant cannot be grounded with the embedded facts or repo-local sources, move it to non-blocking review/archive rather than fabricating data.

Temporary-file cleanup is mandatory: before final commit, delete `codex_tasks/BATCH27_RUN2_*.md` unless the user explicitly asks to keep it.

## RUN 2 scope
```text
BATCH27 RUN 2 only
Start profile: IL-confirmed|Nissan|Navara
End profile: IL-confirmed|Opel|Ampera
Profiles: 20
Technical variants: 60
Do not apply RUN 1, RUN 3, RUN 4, RUN 5, or FINAL blockers.
```

## Web / repo-local source anchors embedded in this RUN
- Nissan official Qashqai: https://www.nissan.co.il/vehicles/new/qashqai/price-specifications.html
- Nissan official X-Trail: https://www.nissan.co.il/vehicles/new/x-trail/price-specifications.html
- Nissan official Sentra: https://www.nissan.co.il/vehicles/new/sentra.html
- Nissan Israel homepage/model range: https://www.nissan.co.il/
- Omoda Israel price list: https://omoda.co.il/price-list/
- Opel Israel current range: https://online.opel.co.il/
- iCar / Auto / Cartube / Carzone / Yad2 repo-local sources: Use the exact repo-local URLs already attached in each profile sources[] array.
- Global spec fallback only: Auto-Data / manufacturer-country pages may explain horsepower/schema but do not by themselves justify Israeli clean status.

## High-risk findings to fix in RUN 2
- Invalid `source_indexes` are present in Pathfinder, Patrol global, Qashqai, Sunny, Terrano likely, X-Trail, Omoda C5/E5, and Opel Adam. These must be fixed to valid local source indexes or the rows must move to review/archive.
- Global-reference-only profiles must not remain separate clean profiles when a canonical IL-confirmed profile exists: Pathfinder, Patrol, Omoda C5.
- IL-likely profiles must not remain split from canonical profiles without explicit lineage: Nissan Terrano and Omoda E5.
- Nissan Qashqai current data must reflect the official Nissan Israel current page: 1.3T Mild Hybrid 156 hp CVT FWD and 1.5T e-POWER GEN3 with 205 hp front electric motor. Keep older 190 hp e-POWER as historical only if source-supported.
- Nissan X-Trail current data must reflect current Israeli sources: 1.5T MHEV 163 hp, e-POWER 204 hp FWD, e-POWER 213 hp AWD; preserve historical rows separately.
- Omoda C5/E5 must not be forced into verified clean based on global/preview data. The current official Omoda Israel price list found for this validation lists Omoda 7/9 PHEV, not C5/E5.
- Opel Adam robotized 1.4 87 hp must not be represented as ordinary automatic if schema supports automated_manual/robotized.

## Model-level decisions
- **IL-confirmed|Nissan|Navara** — ACTION: KEEP/FIX. Israeli iCar sources in repo support Navara D40 and NP300; make variant names explicit and preserve 2005-2022 historical range. Do not currentize beyond 2022.
- **IL-confirmed|Nissan|Note** — ACTION: KEEP/FIX. Israeli iCar/Carzone repo sources support Note 2006-2013 1.6 110 and 2014-2018 1.2 DIG-S 98 CVT. Normalize trims/tech names, no currentization.
- **IL-confirmed|Nissan|NV200** — ACTION: KEEP/FIX. Repo-local iCar/Auto sources support NV200 cargo/passenger 1.5 dCi 85/90 hp. Keep separate Van/MPV only if schema treats body_type as technical variant; otherwise lineage aliases.
- **IL-confirmed|Nissan|Pathfinder** — ACTION: FIX/MERGE. IL-confirmed Pathfinder has invalid source_indexes. Fix all source_indexes/field_sources to local profile sources. Merge fourth-gen global-reference-only Pathfinder into canonical Pathfinder only if Israeli iCar/Auto repo-local sources support 2013-2020 3.5 V6 260 CVT AWD; otherwise archive non-blocking.
- **global-reference-only|Nissan|Pathfinder** — ACTION: MERGE / ARCHIVE NON-BLOCKING. IL-confirmed Pathfinder has invalid source_indexes. Fix all source_indexes/field_sources to local profile sources. Merge fourth-gen global-reference-only Pathfinder into canonical Pathfinder only if Israeli iCar/Auto repo-local sources support 2013-2020 3.5 V6 260 CVT AWD; otherwise archive non-blocking.
- **IL-confirmed|Nissan|Patrol** — ACTION: KEEP/MERGE/ARCHIVE. Historical Y61 diesel rows are Israel-grounded. global-reference-only Patrol duplicates diesel and adds 5.6 V8 global/parallel-import type evidence; do not leave as separate clean. Merge duplicate diesel; move V8 to non-blocking review/archive unless local official/price-list evidence is attached.
- **global-reference-only|Nissan|Patrol** — ACTION: MERGE / ARCHIVE NON-BLOCKING. Historical Y61 diesel rows are Israel-grounded. global-reference-only Patrol duplicates diesel and adds 5.6 V8 global/parallel-import type evidence; do not leave as separate clean. Merge duplicate diesel; move V8 to non-blocking review/archive unless local official/price-list evidence is attached.
- **IL-confirmed|Nissan|Primera** — ACTION: KEEP/FIX. Auto/iCar repo sources support Primera 1999-2008 1.8/2.0 petrol FWD. Keep historical only and normalize P11/P12 lineage.
- **IL-confirmed|Nissan|Qashqai** — ACTION: FIX/ADD. Official Nissan Israel current page supports 1.3T Mild Hybrid 156 hp CVT FWD and 1.5T e-POWER rows. Existing source_indexes are invalid. Keep historical rows; currentize 1.3T MHEV 156 and split old e-POWER 190 from current e-POWER GEN3 205 if needed.
- **IL-confirmed|Nissan|Sentra** — ACTION: KEEP/FIX. Official Nissan Israel current Sentra page supports 2.0L petrol 149 hp CVT. Keep 1.8 2016-2020 historical; keep 2.0 2021-current only if field_sources are valid.
- **IL-confirmed|Nissan|Sunny** — ACTION: KEEP/FIX. Historical Auto Israel source supports Sunny N14; fix invalid source_indexes from [1143] to local [0].
- **IL-likely|Nissan|Terrano** — ACTION: MERGE / MOVE TO REVIEW. IL-likely first-gen Terrano must not remain separate if canonical IL-confirmed Terrano exists. Merge/alias with lineage; fix invalid source_indexes. Keep 1993-2006 confirmed rows only where local evidence supports engine/year split.
- **IL-confirmed|Nissan|Terrano** — ACTION: MERGE/FIX. IL-likely first-gen Terrano must not remain separate if canonical IL-confirmed Terrano exists. Merge/alias with lineage; fix invalid source_indexes. Keep 1993-2006 confirmed rows only where local evidence supports engine/year split.
- **IL-confirmed|Nissan|Tiida** — ACTION: KEEP/FIX. Israeli iCar/Auto sources support Tiida 2008-2012 1.6 110 hp sedan/hatchback, AT/MT. Keep historical; normalize trim strings if needed.
- **IL-confirmed|Nissan|X-Trail** — ACTION: FIX/ADD. Official Nissan Israel current X-Trail page supports current model; Auto/Cartube support 2026/2023 powertrains. Fix invalid source_indexes. Keep historical rows; currentize 1.5 MHEV 163 and e-POWER 204/213 rows if local sources attached.
- **global-reference-only|Omoda|C5** — ACTION: MERGE / ARCHIVE NON-BLOCKING. Do not keep global-reference-only C5 separate. Official Omoda Israel price list currently lists Omoda 7/9 PHEV, not C5/E5; Omoda C5 evidence may be Chery FX/older launch. Merge/alias to canonical Chery FX/Omoda C5 only with repo-local evidence; otherwise non-blocking review/archive. Fix invalid source indexes.
- **IL-confirmed|Omoda|C5** — ACTION: MERGE/REVIEW. Do not keep global-reference-only C5 separate. Official Omoda Israel price list currently lists Omoda 7/9 PHEV, not C5/E5; Omoda C5 evidence may be Chery FX/older launch. Merge/alias to canonical Chery FX/Omoda C5 only with repo-local evidence; otherwise non-blocking review/archive. Fix invalid source indexes.
- **IL-likely|Omoda|E5** — ACTION: MERGE / MOVE TO REVIEW. No strong official Israeli current price-list evidence found in Omoda Israel price list. Treat as weak/future/preview unless repo-local Israeli catalog source proves sales. EV schema is technically okay but clean status is not.
- **IL-confirmed|Opel|Adam** — ACTION: KEEP/FIX. Israeli iCar/Auto/Cartube sources support Opel Adam 2014-2019, 1.4 87 hp manual/robotized and Adam S 1.4T 150 hp manual. Fix invalid source_indexes and label robotized transmission, not generic automatic.
- **IL-confirmed|Opel|Ampera** — ACTION: KEEP/FIX. Israeli Auto/iCar sources support Ampera 2012-2015/2016 as plug-in hybrid/EREV with 1.4 generator and 150 hp electric drive. Keep historical; use repo-valid e-CVT/single-speed electric-drive schema.

## Variant-level instructions

### MODEL PROFILE 649: IL-confirmed|Nissan|Navara
PROFILE SOURCES COUNT: 2
- source[0]: ניסאן נבארה (2016-2022) - מחירון רכב, מפרט טכני — https://www.icar.co.il/%D7%A0%D7%99%D7%A1%D7%90%D7%9F/%D7%A0%D7%99%D7%A1%D7%90%D7%9F_%D7%A0%D7%91%D7%90%D7%A8%D7%94/
- source[1]: ניסאן נבארה דור 2 (2005-2015) - מפרט טכני — https://www.icar.co.il/%D7%A0%D7%99%D7%A1%D7%90%D7%9F/%D7%A0%D7%99%D7%A1%D7%90%D7%9F_%D7%A0%D7%91%D7%90%D7%A8%D7%94_%D7%93%D7%95%D7%A8_2/

#### VARIANT 1/4
MODEL: IL-confirmed|Nissan|Navara
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Pickup",
  "fuel_type": "diesel",
  "engine": "2.5L turbo",
  "engine_displacement_l": 2.5,
  "horsepower_hp": 174,
  "transmission": "5-speed automatic",
  "drivetrain": "4WD",
  "year_start": 2005,
  "year_end": 2010,
  "support_level": "direct",
  "source_indexes": [
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Israeli iCar sources in repo support Navara D40 and NP300; make variant names explicit and preserve 2005-2022 historical range. Do not currentize beyond 2022.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Navara above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 2/4
MODEL: IL-confirmed|Nissan|Navara
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Pickup",
  "fuel_type": "diesel",
  "engine": "2.5L turbo",
  "engine_displacement_l": 2.5,
  "horsepower_hp": 190,
  "transmission": "5-speed automatic",
  "drivetrain": "4WD",
  "year_start": 2010,
  "year_end": 2015,
  "support_level": "direct",
  "source_indexes": [
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Israeli iCar sources in repo support Navara D40 and NP300; make variant names explicit and preserve 2005-2022 historical range. Do not currentize beyond 2022.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Navara above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 3/4
MODEL: IL-confirmed|Nissan|Navara
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Pickup",
  "fuel_type": "diesel",
  "engine": "3.0L v6 turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 231,
  "transmission": "7-speed automatic",
  "drivetrain": "4WD",
  "year_start": 2010,
  "year_end": 2015,
  "support_level": "direct",
  "source_indexes": [
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Israeli iCar sources in repo support Navara D40 and NP300; make variant names explicit and preserve 2005-2022 historical range. Do not currentize beyond 2022.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Navara above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 4/4
MODEL: IL-confirmed|Nissan|Navara
CURRENT VALUE:
```json
{
  "version_or_trim": "Tekna",
  "body_type": "Pickup",
  "fuel_type": "diesel",
  "engine": "2.3L twin-turbo",
  "engine_displacement_l": 2.3,
  "horsepower_hp": 190,
  "transmission": "7-speed automatic",
  "drivetrain": "4WD",
  "year_start": 2016,
  "year_end": 2022,
  "support_level": "direct",
  "source_indexes": [
    0
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Israeli iCar sources in repo support Navara D40 and NP300; make variant names explicit and preserve 2005-2022 historical range. Do not currentize beyond 2022.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Navara above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

### MODEL PROFILE 650: IL-confirmed|Nissan|Note
PROFILE SOURCES COUNT: 3
- source[0]: ניסאן נוט (2006-2013) - מחירון, מפרטים, ואבזור | iCar — https://www.icar.co.il/nissan/nissan_note/nissan_note_d1/
- source[1]: ניסאן נוט (2014-2018) - מחירון, מפרטים, ואבזור | iCar — https://www.icar.co.il/nissan/nissan_note/nissan_note_d2/
- source[2]: ניסאן נוט - מפרט טכני | קארזון — https://www.carzone.co.il/nissan/note/

#### VARIANT 1/2
MODEL: IL-confirmed|Nissan|Note
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "MPV",
  "fuel_type": "petrol",
  "engine": "1.6L",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 110,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2006,
  "year_end": 2013,
  "support_level": "direct",
  "source_indexes": [
    0,
    2
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Israeli iCar/Carzone repo sources support Note 2006-2013 1.6 110 and 2014-2018 1.2 DIG-S 98 CVT. Normalize trims/tech names, no currentization.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Note above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 2/2
MODEL: IL-confirmed|Nissan|Note
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "MPV",
  "fuel_type": "petrol",
  "engine": "1.2L supercharged",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 98,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2014,
  "year_end": 2018,
  "support_level": "direct",
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Israeli iCar/Carzone repo sources support Note 2006-2013 1.6 110 and 2014-2018 1.2 DIG-S 98 CVT. Normalize trims/tech names, no currentization.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Note above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

### MODEL PROFILE 651: IL-confirmed|Nissan|NV200
PROFILE SOURCES COUNT: 2
- source[0]: ניסאן NV200 - קטלוג רכבים | iCar — https://www.icar.co.il/nissan/nissan_nv200/
- source[1]: ניסאן NV200 - מחירון, מפרטים, אמינות ועוד - אוטו — https://www.auto.co.il/model/nissan-nv200_g140

#### VARIANT 1/4
MODEL: IL-confirmed|Nissan|NV200
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Van",
  "fuel_type": "diesel",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 85,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 2011,
  "year_end": 2014,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Repo-local iCar/Auto sources support NV200 cargo/passenger 1.5 dCi 85/90 hp. Keep separate Van/MPV only if schema treats body_type as technical variant; otherwise lineage aliases.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|NV200 above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 2/4
MODEL: IL-confirmed|Nissan|NV200
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "MPV",
  "fuel_type": "diesel",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 85,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 2011,
  "year_end": 2014,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Repo-local iCar/Auto sources support NV200 cargo/passenger 1.5 dCi 85/90 hp. Keep separate Van/MPV only if schema treats body_type as technical variant; otherwise lineage aliases.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|NV200 above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 3/4
MODEL: IL-confirmed|Nissan|NV200
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Van",
  "fuel_type": "diesel",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 90,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 2015,
  "year_end": 2019,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Repo-local iCar/Auto sources support NV200 cargo/passenger 1.5 dCi 85/90 hp. Keep separate Van/MPV only if schema treats body_type as technical variant; otherwise lineage aliases.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|NV200 above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 4/4
MODEL: IL-confirmed|Nissan|NV200
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "MPV",
  "fuel_type": "diesel",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 90,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 2015,
  "year_end": 2019,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Repo-local iCar/Auto sources support NV200 cargo/passenger 1.5 dCi 85/90 hp. Keep separate Van/MPV only if schema treats body_type as technical variant; otherwise lineage aliases.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|NV200 above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

### MODEL PROFILE 652: IL-confirmed|Nissan|Pathfinder
PROFILE SOURCES COUNT: 3
- source[0]: ניסאן פאת'פיינדר 2005-2014 - מפרט טכני — https://www.icar.co.il/ניסאן/ניסאן_פאת'פיינדר/ניסאן_פאת'פיינדר_יד_שניה_דגם_1/
- source[1]: ניסאן פאת'פיינדר 2001-2004 - מפרט טכני — https://www.icar.co.il/ניסאן/ניסאן_פאת'פיינדר/ניסאן_פאת'פיינדר_יד_שניה_דגם_2/
- source[2]: מבחן דרכים: ניסאן פאת'פיינדר החדש בישראל 2010 — https://www.auto.co.il/article/roadcartest/26671-nissan-pathfinder

#### VARIANT 1/4
MODEL: IL-confirmed|Nissan|Pathfinder
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "3.5L v6",
  "engine_displacement_l": 3.5,
  "horsepower_hp": 220,
  "transmission": "4-speed automatic",
  "drivetrain": "4WD",
  "year_start": 2001,
  "year_end": 2004,
  "support_level": "direct",
  "source_indexes": [
    1123
  ]
}
```
PROBLEM: source_indexes [1123] are invalid for this profile because sources[] length is 3
WEB-VALIDATED FACT: Repo-local iCar/Auto Israeli sources support Pathfinder 2001-2014; source indexes must be normalized to local [0..2].
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Pathfinder above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Use explicit generation labels: R50 3.5 V6, R51 2.5 dCi, R51 facelift 2.5 dCi, R51 3.0 dCi V6.
ACTION: FIX

#### VARIANT 2/4
MODEL: IL-confirmed|Nissan|Pathfinder
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "2.5L turbo",
  "engine_displacement_l": 2.5,
  "horsepower_hp": 174,
  "transmission": "5-speed automatic",
  "drivetrain": "4WD",
  "year_start": 2005,
  "year_end": 2010,
  "support_level": "direct",
  "source_indexes": [
    1122
  ]
}
```
PROBLEM: source_indexes [1122] are invalid for this profile because sources[] length is 3
WEB-VALIDATED FACT: Repo-local iCar/Auto Israeli sources support Pathfinder 2001-2014; source indexes must be normalized to local [0..2].
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Pathfinder above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Use explicit generation labels: R50 3.5 V6, R51 2.5 dCi, R51 facelift 2.5 dCi, R51 3.0 dCi V6.
ACTION: FIX

#### VARIANT 3/4
MODEL: IL-confirmed|Nissan|Pathfinder
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "2.5L turbo",
  "engine_displacement_l": 2.5,
  "horsepower_hp": 190,
  "transmission": "5-speed automatic",
  "drivetrain": "4WD",
  "year_start": 2010,
  "year_end": 2014,
  "support_level": "direct",
  "source_indexes": [
    1122,
    1124
  ]
}
```
PROBLEM: source_indexes [1122, 1124] are invalid for this profile because sources[] length is 3
WEB-VALIDATED FACT: Repo-local iCar/Auto Israeli sources support Pathfinder 2001-2014; source indexes must be normalized to local [0..2].
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Pathfinder above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Use explicit generation labels: R50 3.5 V6, R51 2.5 dCi, R51 facelift 2.5 dCi, R51 3.0 dCi V6.
ACTION: FIX

#### VARIANT 4/4
MODEL: IL-confirmed|Nissan|Pathfinder
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "3.0L v6 turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 231,
  "transmission": "7-speed automatic",
  "drivetrain": "4WD",
  "year_start": 2010,
  "year_end": 2014,
  "support_level": "direct",
  "source_indexes": [
    1122,
    1124
  ]
}
```
PROBLEM: source_indexes [1122, 1124] are invalid for this profile because sources[] length is 3
WEB-VALIDATED FACT: Repo-local iCar/Auto Israeli sources support Pathfinder 2001-2014; source indexes must be normalized to local [0..2].
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Pathfinder above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Use explicit generation labels: R50 3.5 V6, R51 2.5 dCi, R51 facelift 2.5 dCi, R51 3.0 dCi V6.
ACTION: FIX

### MODEL PROFILE 653: global-reference-only|Nissan|Pathfinder
PROFILE SOURCES COUNT: 2
- source[0]: ניסאן פאת'פיינדר דור 4 (2013-2020) - מחירון, מפרט טכני וחוות דעת — https://www.icar.co.il/%D7%A0%D7%99%D7%A1%D7%90%D7%9F/%D7%A0%D7%99%D7%A1%D7%90%D7%9F_%D7%A4%D7%90%D7%AA'%D7%A4%D7%99%D7%99%D7%A0%D7%93%D7%A8/
- source[1]: ניסאן פאת'פיינדר - מפרט טכני, חדשות וסקירות — https://www.auto.co.il/model/nissan-pathfinder

#### VARIANT 1/1
MODEL: global-reference-only|Nissan|Pathfinder
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "3.5L v6",
  "engine_displacement_l": 3.5,
  "horsepower_hp": 260,
  "transmission": "cvt",
  "drivetrain": "AWD",
  "year_start": 2013,
  "year_end": 2020,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: global-reference-only profile must not remain as separate verified clean when Israeli canonical/confirmed model exists or evidence is weak.
WEB-VALIDATED FACT: Attached repo-local sources are Israeli iCar/Auto for fourth-gen Pathfinder 2013-2020, despite global-reference-only scope.
SOURCE:
- Repo-local Israeli sources[] attached to global-reference-only|Nissan|Pathfinder above.
TARGET VALUE: MERGE into IL-confirmed canonical profile with alias/lineage, or ARCHIVE NON-BLOCKING if not grounded for Israel. Move/merge this fourth-gen 3.5 V6 260 CVT AWD row into canonical IL-confirmed Pathfinder if source policy accepts iCar/Auto; otherwise archive non-blocking with lineage.
ACTION: MERGE / FIX

### MODEL PROFILE 654: IL-confirmed|Nissan|Patrol
PROFILE SOURCES COUNT: 2
- source[0]: ניסאן פטרול (1998-2010) - מפרט טכני, מידע וסקירות | אוטו — https://www.auto.co.il/model/nissan-patrol_g131
- source[1]: ניסאן פטרול יד שניה - חוות דעת, מחירון, צריכת דלק, מפרט טכני - iCar — https://www.icar.co.il/%D7%A0%D7%99%D7%A1%D7%90%D7%9F/%D7%A0%D7%99%D7%A1%D7%90%D7%9F_%D7%A4%D7%98%D7%A8%D7%95%D7%9C/%D7%A0%D7%99%D7%A1%D7%90%D7%9F_%D7%A4%D7%98%D7%A8%D7%95%D7%9C_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%933/

#### VARIANT 1/3
MODEL: IL-confirmed|Nissan|Patrol
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "2.8L turbo",
  "engine_displacement_l": 2.8,
  "horsepower_hp": 130,
  "transmission": "4-speed automatic",
  "drivetrain": "4WD",
  "year_start": 1998,
  "year_end": 2000,
  "support_level": "direct",
  "source_indexes": [
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Historical Y61 diesel rows are Israel-grounded. global-reference-only Patrol duplicates diesel and adds 5.6 V8 global/parallel-import type evidence; do not leave as separate clean. Merge duplicate diesel; move V8 to non-blocking review/archive unless local official/price-list evidence is attached.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Patrol above.
TARGET VALUE: Preserve or correct row according to embedded fact; ensure all field_sources/source_indexes are valid and no duplicate profile remains.
ACTION: KEEP/FIX

#### VARIANT 2/3
MODEL: IL-confirmed|Nissan|Patrol
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "3.0L turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 158,
  "transmission": "4-speed automatic",
  "drivetrain": "4WD",
  "year_start": 2000,
  "year_end": 2010,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Historical Y61 diesel rows are Israel-grounded. global-reference-only Patrol duplicates diesel and adds 5.6 V8 global/parallel-import type evidence; do not leave as separate clean. Merge duplicate diesel; move V8 to non-blocking review/archive unless local official/price-list evidence is attached.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Patrol above.
TARGET VALUE: Preserve or correct row according to embedded fact; ensure all field_sources/source_indexes are valid and no duplicate profile remains.
ACTION: KEEP/FIX

#### VARIANT 3/3
MODEL: IL-confirmed|Nissan|Patrol
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "3.0L turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 158,
  "transmission": "5-speed manual",
  "drivetrain": "4WD",
  "year_start": 2000,
  "year_end": 2010,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Historical Y61 diesel rows are Israel-grounded. global-reference-only Patrol duplicates diesel and adds 5.6 V8 global/parallel-import type evidence; do not leave as separate clean. Merge duplicate diesel; move V8 to non-blocking review/archive unless local official/price-list evidence is attached.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Patrol above.
TARGET VALUE: Preserve or correct row according to embedded fact; ensure all field_sources/source_indexes are valid and no duplicate profile remains.
ACTION: KEEP/FIX

### MODEL PROFILE 655: global-reference-only|Nissan|Patrol
PROFILE SOURCES COUNT: 2
- source[0]: ניסאן פטרול (1998-2010) - מחירון רכב מפרט טכני - iCar — https://www.icar.co.il/nissan/nissan_patrol/
- source[1]: ניסאן פטרול צריכת דלק, מפרט טכני - קילומטר לליטר (יבוא מקביל/אישי) — https://kml.co.il/car/nissan/patrol

#### VARIANT 1/2
MODEL: global-reference-only|Nissan|Patrol
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "3.0L turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 160,
  "transmission": "4-speed automatic",
  "drivetrain": "4WD",
  "year_start": 1998,
  "year_end": 2010,
  "support_level": "direct",
  "source_indexes": [
    1
  ]
}
```
PROBLEM: global-reference-only profile must not remain as separate verified clean when Israeli canonical/confirmed model exists or evidence is weak.
WEB-VALIDATED FACT: Historical Y61 diesel rows are Israel-grounded. global-reference-only Patrol duplicates diesel and adds 5.6 V8 global/parallel-import type evidence; do not leave as separate clean. Merge duplicate diesel; move V8 to non-blocking review/archive unless local official/price-list evidence is attached.
SOURCE:
- Repo-local Israeli sources[] attached to global-reference-only|Nissan|Patrol above.
TARGET VALUE: MERGE into IL-confirmed canonical profile with alias/lineage, or ARCHIVE NON-BLOCKING if not grounded for Israel. Merge 3.0 diesel duplicate into IL-confirmed Patrol historical row and delete duplicate clean profile.
ACTION: MERGE / DELETE DUPLICATE

#### VARIANT 2/2
MODEL: global-reference-only|Nissan|Patrol
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "5.6L v8",
  "engine_displacement_l": 5.6,
  "horsepower_hp": 400,
  "transmission": "7-speed automatic",
  "drivetrain": "4WD",
  "year_start": 2010,
  "year_end": 2020,
  "support_level": "direct",
  "source_indexes": [
    2
  ]
}
```
PROBLEM: source_indexes [2] are invalid for this profile because sources[] length is 2 global-reference-only profile must not remain as separate verified clean when Israeli canonical/confirmed model exists or evidence is weak.
WEB-VALIDATED FACT: 5.6 V8 400 hp Patrol is globally valid, but no strong official Israeli clean-market source is embedded in this RUN.
SOURCE:
- Repo-local Israeli sources[] attached to global-reference-only|Nissan|Patrol above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. MERGE into IL-confirmed canonical profile with alias/lineage, or ARCHIVE NON-BLOCKING if not grounded for Israel. Do not keep as verified clean unless repo-local evidence explicitly proves Israeli official/price-list availability; otherwise review/archive non-blocking.
ACTION: MOVE TO REVIEW / ARCHIVE NON-BLOCKING

### MODEL PROFILE 656: IL-confirmed|Nissan|Primera
PROFILE SOURCES COUNT: 4
- source[0]: ניסאן פרימרה 2002-2008 מפרט טכני — https://www.auto.co.il/model/nissan-primera_g246
- source[1]: ניסאן פרימרה 1997-2002 מפרט טכני — https://www.auto.co.il/model/nissan-primera_g245
- source[2]: ניסאן פרימרה יד שניה (2002 - 2008) — https://www.icar.co.il/%D7%A0%D7%99%D7%A1%D7%90%D7%9F/%D7%A0%D7%99%D7%A1%D7%90%D7%9F_%D7%A4%D7%A8%D7%99%D7%9E%D7%A8%D7%94/%D7%A0%D7%99%D7%A1%D7%90%D7%9F_%D7%A4%D7%A8%D7%99%D7%9E%D7%A8%D7%94_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%932/
- source[3]: ניסאן פרימרה דור 2 (1997-2002) - מפרט — https://www.icar.co.il/%D7%A0%D7%99%D7%A1%D7%90%D7%9F/%D7%A0%D7%99%D7%A1%D7%90%D7%9F_%D7%A4%D7%A8%D7%99%D7%9E%D7%A8%D7%94/%D7%A0%D7%99%D7%A1%D7%90%D7%9F_%D7%A4%D7%A8%D7%99%D7%9E%D7%A8%D7%94_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%931/

#### VARIANT 1/4
MODEL: IL-confirmed|Nissan|Primera
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "1.8L",
  "engine_displacement_l": 1.8,
  "horsepower_hp": 116,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2002,
  "year_end": 2008,
  "support_level": "direct",
  "source_indexes": [
    0,
    2
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Auto/iCar repo sources support Primera 1999-2008 1.8/2.0 petrol FWD. Keep historical only and normalize P11/P12 lineage.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Primera above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 2/4
MODEL: IL-confirmed|Nissan|Primera
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 140,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2002,
  "year_end": 2008,
  "support_level": "direct",
  "source_indexes": [
    0,
    2
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Auto/iCar repo sources support Primera 1999-2008 1.8/2.0 petrol FWD. Keep historical only and normalize P11/P12 lineage.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Primera above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 3/4
MODEL: IL-confirmed|Nissan|Primera
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "1.8L",
  "engine_displacement_l": 1.8,
  "horsepower_hp": 114,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 1999,
  "year_end": 2002,
  "support_level": "direct",
  "source_indexes": [
    1,
    3
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Auto/iCar repo sources support Primera 1999-2008 1.8/2.0 petrol FWD. Keep historical only and normalize P11/P12 lineage.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Primera above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 4/4
MODEL: IL-confirmed|Nissan|Primera
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 140,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 1999,
  "year_end": 2002,
  "support_level": "direct",
  "source_indexes": [
    1,
    3
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Auto/iCar repo sources support Primera 1999-2008 1.8/2.0 petrol FWD. Keep historical only and normalize P11/P12 lineage.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Primera above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

### MODEL PROFILE 657: IL-confirmed|Nissan|Qashqai
PROFILE SOURCES COUNT: 4
- source[0]: ניסאן קשקאי 2007-2013 יד שנייה - מפרט טכני — https://www.auto.co.il/model/nissan-qashqai_g209
- source[1]: ניסאן קשקאי (2014-2021) - מחירון רכב, מפרט טכני — https://www.icar.co.il/%D7%A0%D7%99%D7%A1%D7%90%D7%9F/%D7%A0%D7%99%D7%A1%D7%90%D7%9F_%D7%A7%D7%A9%D7%A7%D7%90%D7%99_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%99%D7%94/
- source[2]: ניסאן קשקאי החדש 2021 בישראל - מחיר החל מ- 159,900 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%A0%D7%99%D7%A1%D7%90%D7%9F-%D7%A7%D7%A9%D7%A7%D7%90%D7%99-%D7%94%D7%97%D7%93%D7%A9-2021-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-159900-%D7%A9%D7%A7%D7%9C
- source[3]: ניסאן קשקאי e-Power בישראל - מחיר החל מ-207,990 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%A0%D7%99%D7%A1%D7%90%D7%9F-%D7%A7%D7%A9%D7%A7%D7%90%D7%99-e-power-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-207990-%D7%A9%D7%A7%D7%9C

#### VARIANT 1/6
MODEL: IL-confirmed|Nissan|Qashqai
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Crossover",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 140,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2007,
  "year_end": 2013,
  "support_level": "direct",
  "source_indexes": [
    1075
  ]
}
```
PROBLEM: source_indexes [1075] are invalid for this profile because sources[] length is 4
WEB-VALIDATED FACT: Official Nissan Israel current page supports 1.3T Mild Hybrid 156 hp CVT FWD and 1.5T e-POWER rows. Existing source_indexes are invalid. Keep historical rows; currentize 1.3T MHEV 156 and split old e-POWER 190 from current e-POWER GEN3 205 if needed.
SOURCE:
- Nissan official Qashqai price/spec page: https://www.nissan.co.il/vehicles/new/qashqai/price-specifications.html
- Repo-local Qashqai sources[] attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Keep historical Qashqai row but replace invalid source indexes with proper attached Israeli sources.
ACTION: FIX / ADD

#### VARIANT 2/6
MODEL: IL-confirmed|Nissan|Qashqai
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Crossover",
  "fuel_type": "petrol",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 115,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2014,
  "year_end": 2018,
  "support_level": "direct",
  "source_indexes": [
    1076
  ]
}
```
PROBLEM: source_indexes [1076] are invalid for this profile because sources[] length is 4
WEB-VALIDATED FACT: Official Nissan Israel current page supports 1.3T Mild Hybrid 156 hp CVT FWD and 1.5T e-POWER rows. Existing source_indexes are invalid. Keep historical rows; currentize 1.3T MHEV 156 and split old e-POWER 190 from current e-POWER GEN3 205 if needed.
SOURCE:
- Nissan official Qashqai price/spec page: https://www.nissan.co.il/vehicles/new/qashqai/price-specifications.html
- Repo-local Qashqai sources[] attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Keep historical Qashqai row but replace invalid source indexes with proper attached Israeli sources.
ACTION: FIX / ADD

#### VARIANT 3/6
MODEL: IL-confirmed|Nissan|Qashqai
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Crossover",
  "fuel_type": "diesel",
  "engine": "1.6L turbo",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 130,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2014,
  "year_end": 2018,
  "support_level": "direct",
  "source_indexes": [
    1076
  ]
}
```
PROBLEM: source_indexes [1076] are invalid for this profile because sources[] length is 4
WEB-VALIDATED FACT: Official Nissan Israel current page supports 1.3T Mild Hybrid 156 hp CVT FWD and 1.5T e-POWER rows. Existing source_indexes are invalid. Keep historical rows; currentize 1.3T MHEV 156 and split old e-POWER 190 from current e-POWER GEN3 205 if needed.
SOURCE:
- Nissan official Qashqai price/spec page: https://www.nissan.co.il/vehicles/new/qashqai/price-specifications.html
- Repo-local Qashqai sources[] attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Keep historical Qashqai row but replace invalid source indexes with proper attached Israeli sources.
ACTION: FIX / ADD

#### VARIANT 4/6
MODEL: IL-confirmed|Nissan|Qashqai
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Crossover",
  "fuel_type": "petrol",
  "engine": "1.3L turbo",
  "engine_displacement_l": 1.3,
  "horsepower_hp": 160,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2019,
  "year_end": 2021,
  "support_level": "direct",
  "source_indexes": [
    1076
  ]
}
```
PROBLEM: source_indexes [1076] are invalid for this profile because sources[] length is 4
WEB-VALIDATED FACT: Official Nissan Israel current page supports 1.3T Mild Hybrid 156 hp CVT FWD and 1.5T e-POWER rows. Existing source_indexes are invalid. Keep historical rows; currentize 1.3T MHEV 156 and split old e-POWER 190 from current e-POWER GEN3 205 if needed.
SOURCE:
- Nissan official Qashqai price/spec page: https://www.nissan.co.il/vehicles/new/qashqai/price-specifications.html
- Repo-local Qashqai sources[] attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Keep historical Qashqai row but replace invalid source indexes with proper attached Israeli sources.
ACTION: FIX / ADD

#### VARIANT 5/6
MODEL: IL-confirmed|Nissan|Qashqai
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Crossover",
  "fuel_type": "mild_hybrid",
  "engine": "1.3L turbo",
  "engine_displacement_l": 1.3,
  "horsepower_hp": 156,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2021,
  "year_end": 2024,
  "support_level": "direct",
  "source_indexes": [
    1077
  ]
}
```
PROBLEM: source_indexes [1077] are invalid for this profile because sources[] length is 4
WEB-VALIDATED FACT: Nissan Israel current Qashqai page lists 1.3T Mild Hybrid 156 hp CVT FWD and 1.5T e-POWER rows; current e-POWER GEN3 front electric motor is 205 hp, while older e-POWER rows were 190 hp.
SOURCE:
- Nissan official Qashqai price/spec page: https://www.nissan.co.il/vehicles/new/qashqai/price-specifications.html
- Repo-local Qashqai sources[] attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Fix source indexes; keep/split historical 2022-2024 190 e-POWER and add/currentize 2026 e-POWER GEN3 205 if not present. 1.3T MHEV 156 may be current if official source attached.
ACTION: FIX / ADD

#### VARIANT 6/6
MODEL: IL-confirmed|Nissan|Qashqai
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Crossover",
  "fuel_type": "hybrid",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 190,
  "transmission": "single_speed",
  "drivetrain": "FWD",
  "year_start": 2022,
  "year_end": 2024,
  "support_level": "direct",
  "source_indexes": [
    1078
  ]
}
```
PROBLEM: source_indexes [1078] are invalid for this profile because sources[] length is 4
WEB-VALIDATED FACT: Nissan Israel current Qashqai page lists 1.3T Mild Hybrid 156 hp CVT FWD and 1.5T e-POWER rows; current e-POWER GEN3 front electric motor is 205 hp, while older e-POWER rows were 190 hp.
SOURCE:
- Nissan official Qashqai price/spec page: https://www.nissan.co.il/vehicles/new/qashqai/price-specifications.html
- Repo-local Qashqai sources[] attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Fix source indexes; keep/split historical 2022-2024 190 e-POWER and add/currentize 2026 e-POWER GEN3 205 if not present. 1.3T MHEV 156 may be current if official source attached.
ACTION: FIX / ADD

### MODEL PROFILE 658: IL-confirmed|Nissan|Sentra
PROFILE SOURCES COUNT: 4
- source[0]: Nissan Sentra 1.8 (2016-2020) Specifications - iCar Israel — https://www.icar.co.il/Nissan/Nissan_Sentra/Nissan_Sentra_1_Used/
- source[1]: ניסאן סנטרה נוחתת בישראל: מחיר החל מ- 130 אלף שקל — https://www.cartube.co.il/חדשות-רכב/ניסאן-סנטרה-נוחתת-בישראל-מחיר-החל-מ-130-אלף-שקל
- source[2]: Nissan Sentra 2.0 Specifications - iCar Israel — https://www.icar.co.il/Nissan/Nissan_Sentra/Nissan_Sentra_2_Used/
- source[3]: ניסאן סנטרה החדשה 2021 בישראל - מחיר החל מ- 133,990 שקלים — https://www.cartube.co.il/חדשות-רכב/ניסאן-סנטרה-החדשה-2021-בישראל-מחיר-החל-מ-133990-שקלים

#### VARIANT 1/2
MODEL: IL-confirmed|Nissan|Sentra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "1.8L",
  "engine_displacement_l": 1.8,
  "horsepower_hp": 130,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2016,
  "year_end": 2020,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Official Nissan Israel current Sentra page supports 2.0L petrol 149 hp CVT. Keep 1.8 2016-2020 historical; keep 2.0 2021-current only if field_sources are valid.
SOURCE:
- Nissan official Sentra page: https://www.nissan.co.il/vehicles/new/sentra.html
- Repo-local iCar/Cartube Sentra sources attached above.
TARGET VALUE: Keep 1.8L 130 hp CVT as 2016-2020 historical only.
ACTION: KEEP/FIX

#### VARIANT 2/2
MODEL: IL-confirmed|Nissan|Sentra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 149,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2021,
  "year_end": null,
  "support_level": "direct",
  "source_indexes": [
    2,
    3
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Nissan Israel current Sentra page states NEW SENTRA, 2.0 litre petrol, 149 hp.
SOURCE:
- Nissan official Sentra page: https://www.nissan.co.il/vehicles/new/sentra.html
- Repo-local iCar/Cartube Sentra sources attached above.
TARGET VALUE: Keep 2.0L 149 hp CVT FWD as current only with valid source_indexes/field_sources to official Nissan/iCar/Cartube sources.
ACTION: KEEP/FIX

### MODEL PROFILE 659: IL-confirmed|Nissan|Sunny
PROFILE SOURCES COUNT: 1
- source[0]: Nissan Sunny N14 (1991-1995) Technical Specs - Israel Market — https://www.auto.co.il/model/nissan-sunny_g144

#### VARIANT 1/2
MODEL: IL-confirmed|Nissan|Sunny
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "1.6L",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 90,
  "transmission": "automatic",
  "drivetrain": "FWD",
  "year_start": 1991,
  "year_end": 1995,
  "support_level": "direct",
  "source_indexes": [
    1143
  ]
}
```
PROBLEM: source_indexes [1143] are invalid for this profile because sources[] length is 1
WEB-VALIDATED FACT: Historical Auto Israel source supports Sunny N14; fix invalid source_indexes from [1143] to local [0].
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Sunny above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Keep historical N14 1.6 90 hp AT/MT, but replace invalid [1143] source index with local [0].
ACTION: FIX

#### VARIANT 2/2
MODEL: IL-confirmed|Nissan|Sunny
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "1.6L",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 90,
  "transmission": "manual",
  "drivetrain": "FWD",
  "year_start": 1991,
  "year_end": 1995,
  "support_level": "direct",
  "source_indexes": [
    1143
  ]
}
```
PROBLEM: source_indexes [1143] are invalid for this profile because sources[] length is 1
WEB-VALIDATED FACT: Historical Auto Israel source supports Sunny N14; fix invalid source_indexes from [1143] to local [0].
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Sunny above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Keep historical N14 1.6 90 hp AT/MT, but replace invalid [1143] source index with local [0].
ACTION: FIX

### MODEL PROFILE 660: IL-likely|Nissan|Terrano
PROFILE SOURCES COUNT: 2
- source[0]: מחירון רכב ניסאן טראנו 1990-1995 - לוי יצחק (Levi Yitzhak Pricing & Specs) — https://www.levi-itzhak.co.il/
- source[1]: ניסאן טראנו דור 1 - מפרט טכני וסקירה — https://www.auto.co.il/model/nissan-terrano_g210

#### VARIANT 1/1
MODEL: IL-likely|Nissan|Terrano
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.4L",
  "engine_displacement_l": 2.4,
  "horsepower_hp": 125,
  "transmission": "5-speed manual",
  "drivetrain": "4WD",
  "year_start": 1990,
  "year_end": 1995,
  "support_level": "direct",
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: source_indexes [1, 2] are invalid for this profile because sources[] length is 2 IL-likely profile should not remain separate clean when an IL-confirmed canonical profile exists or official Israeli evidence is missing.
WEB-VALIDATED FACT: IL-likely first-gen Terrano must not remain separate if canonical IL-confirmed Terrano exists. Merge/alias with lineage; fix invalid source_indexes. Keep 1993-2006 confirmed rows only where local evidence supports engine/year split.
SOURCE:
- Repo-local Israeli sources[] attached to IL-likely|Nissan|Terrano above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Promote to IL-confirmed only with repo-local Israeli evidence; otherwise merge/alias or move to non-blocking review/archive. Merge first-gen likely row into canonical Terrano lineage or archive non-blocking; do not keep separate clean profile.
ACTION: MERGE/FIX

### MODEL PROFILE 661: IL-confirmed|Nissan|Terrano
PROFILE SOURCES COUNT: 3
- source[0]: ניסאן טראנו (1996-2006) - מחירון, מפרט טכני - iCar — https://www.icar.co.il/ניסאן/ניסאן_טראנו/ניסאן_טראנו_יד_שניה_ד1/
- source[1]: ניסאן טראנו (1996-2006) - חוות דעת, מחירון, מבחני דרכים - אוטו — https://www.auto.co.il/model/nissan-terrano_g210
- source[2]: ניסאן טראנו 1993-2006 - מפרט טכני — https://kml.co.il/Car/ניסאן_טראנו

#### VARIANT 1/6
MODEL: IL-confirmed|Nissan|Terrano
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "2.7L turbo",
  "engine_displacement_l": 2.7,
  "horsepower_hp": 125,
  "transmission": "4-speed automatic",
  "drivetrain": "4WD",
  "year_start": 1996,
  "year_end": 2006,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: IL-likely first-gen Terrano must not remain separate if canonical IL-confirmed Terrano exists. Merge/alias with lineage; fix invalid source_indexes. Keep 1993-2006 confirmed rows only where local evidence supports engine/year split.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Terrano above.
TARGET VALUE: Keep confirmed Terrano rows by engine/year, fix source indexes/lineage; do not merge away 2.7/3.0 diesel split.
ACTION: FIX

#### VARIANT 2/6
MODEL: IL-confirmed|Nissan|Terrano
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "2.7L turbo",
  "engine_displacement_l": 2.7,
  "horsepower_hp": 125,
  "transmission": "5-speed manual",
  "drivetrain": "4WD",
  "year_start": 1996,
  "year_end": 2006,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: IL-likely first-gen Terrano must not remain separate if canonical IL-confirmed Terrano exists. Merge/alias with lineage; fix invalid source_indexes. Keep 1993-2006 confirmed rows only where local evidence supports engine/year split.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Terrano above.
TARGET VALUE: Keep confirmed Terrano rows by engine/year, fix source indexes/lineage; do not merge away 2.7/3.0 diesel split.
ACTION: FIX

#### VARIANT 3/6
MODEL: IL-confirmed|Nissan|Terrano
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "3.0L turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 154,
  "transmission": "4-speed automatic",
  "drivetrain": "4WD",
  "year_start": 2002,
  "year_end": 2006,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: IL-likely first-gen Terrano must not remain separate if canonical IL-confirmed Terrano exists. Merge/alias with lineage; fix invalid source_indexes. Keep 1993-2006 confirmed rows only where local evidence supports engine/year split.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Terrano above.
TARGET VALUE: Keep confirmed Terrano rows by engine/year, fix source indexes/lineage; do not merge away 2.7/3.0 diesel split.
ACTION: FIX

#### VARIANT 4/6
MODEL: IL-confirmed|Nissan|Terrano
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "3.0L turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 154,
  "transmission": "5-speed manual",
  "drivetrain": "4WD",
  "year_start": 2002,
  "year_end": 2006,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: IL-likely first-gen Terrano must not remain separate if canonical IL-confirmed Terrano exists. Merge/alias with lineage; fix invalid source_indexes. Keep 1993-2006 confirmed rows only where local evidence supports engine/year split.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Terrano above.
TARGET VALUE: Keep confirmed Terrano rows by engine/year, fix source indexes/lineage; do not merge away 2.7/3.0 diesel split.
ACTION: FIX

#### VARIANT 5/6
MODEL: IL-confirmed|Nissan|Terrano
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "2.7L turbo",
  "engine_displacement_l": 2.7,
  "horsepower_hp": 100,
  "transmission": "5-speed manual",
  "drivetrain": "4WD",
  "year_start": 1993,
  "year_end": 1996,
  "support_level": "direct",
  "source_indexes": [
    2
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: IL-likely first-gen Terrano must not remain separate if canonical IL-confirmed Terrano exists. Merge/alias with lineage; fix invalid source_indexes. Keep 1993-2006 confirmed rows only where local evidence supports engine/year split.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Terrano above.
TARGET VALUE: Keep confirmed Terrano rows by engine/year, fix source indexes/lineage; do not merge away 2.7/3.0 diesel split.
ACTION: FIX

#### VARIANT 6/6
MODEL: IL-confirmed|Nissan|Terrano
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.4L",
  "engine_displacement_l": 2.4,
  "horsepower_hp": 118,
  "transmission": "5-speed manual",
  "drivetrain": "4WD",
  "year_start": 1993,
  "year_end": 2000,
  "support_level": "direct",
  "source_indexes": [
    2
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: IL-likely first-gen Terrano must not remain separate if canonical IL-confirmed Terrano exists. Merge/alias with lineage; fix invalid source_indexes. Keep 1993-2006 confirmed rows only where local evidence supports engine/year split.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Terrano above.
TARGET VALUE: Keep confirmed Terrano rows by engine/year, fix source indexes/lineage; do not merge away 2.7/3.0 diesel split.
ACTION: FIX

### MODEL PROFILE 662: IL-confirmed|Nissan|Tiida
PROFILE SOURCES COUNT: 2
- source[0]: ניסאן טידה (2008-2012) - מחירון רכב ומפרט טכני — https://www.icar.co.il/nissan/nissan_tiida/nissan_tiida_d1/
- source[1]: ניסאן טידה 2008-2012 - חוות דעת, מחירון, מפרטים — https://www.auto.co.il/model/nissan-tiida_g281

#### VARIANT 1/4
MODEL: IL-confirmed|Nissan|Tiida
CURRENT VALUE:
```json
{
  "version_or_trim": "Visia / Acenta",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "1.6L",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 110,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2008,
  "year_end": 2012,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Israeli iCar/Auto sources support Tiida 2008-2012 1.6 110 hp sedan/hatchback, AT/MT. Keep historical; normalize trim strings if needed.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Tiida above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 2/4
MODEL: IL-confirmed|Nissan|Tiida
CURRENT VALUE:
```json
{
  "version_or_trim": "Visia",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "1.6L",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 110,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 2008,
  "year_end": 2012,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Israeli iCar/Auto sources support Tiida 2008-2012 1.6 110 hp sedan/hatchback, AT/MT. Keep historical; normalize trim strings if needed.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Tiida above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 3/4
MODEL: IL-confirmed|Nissan|Tiida
CURRENT VALUE:
```json
{
  "version_or_trim": "Visia / Acenta",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.6L",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 110,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2008,
  "year_end": 2012,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Israeli iCar/Auto sources support Tiida 2008-2012 1.6 110 hp sedan/hatchback, AT/MT. Keep historical; normalize trim strings if needed.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Tiida above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

#### VARIANT 4/4
MODEL: IL-confirmed|Nissan|Tiida
CURRENT VALUE:
```json
{
  "version_or_trim": "Visia",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.6L",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 110,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 2008,
  "year_end": 2012,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Israeli iCar/Auto sources support Tiida 2008-2012 1.6 110 hp sedan/hatchback, AT/MT. Keep historical; normalize trim strings if needed.
SOURCE:
- Repo-local Israeli sources[] attached to IL-confirmed|Nissan|Tiida above.
TARGET VALUE: Keep as historical Israeli-market technical variant, normalize version_or_trim/generation labels and ensure field_sources point to attached Israeli sources.
ACTION: KEEP/FIX

### MODEL PROFILE 663: IL-confirmed|Nissan|X-Trail
PROFILE SOURCES COUNT: 5
- source[0]: ניסאן אקס טרייל 2023 החדש בישראל - מפרט טכני ומחירון — https://www.cartube.co.il/nissan-x-trail-2023
- source[1]: ניסאן אקס-טרייל - מחירון ותת-דגמים — https://www.icar.co.il/nissan/x-trail
- source[2]: ניסאן אקס טרייל דור 3 (2014-2022) מפרט טכני — https://gear.co.il/nissan/x-trail
- source[3]: ניסאן אקס טרייל 2007-2014 יד שניה — https://www.auto.co.il/model/nissan-x-trail-2007-2014
- source[4]: ניסאן אקס-טרייל 2001-2007 (דור ראשון) — https://www.icar.co.il/nissan/x-trail-2001-2007

#### VARIANT 1/8
MODEL: IL-confirmed|Nissan|X-Trail
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "mild_hybrid",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 163,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2022,
  "year_end": 2024,
  "support_level": "direct",
  "source_indexes": [
    1082
  ]
}
```
PROBLEM: source_indexes [1082] are invalid for this profile because sources[] length is 5
WEB-VALIDATED FACT: Nissan Israel current X-Trail page and Israeli Auto/Cartube sources support current 1.5T MHEV 163 hp plus e-POWER 204 FWD / 213 AWD.
SOURCE:
- Nissan official X-Trail price/spec page: https://www.nissan.co.il/vehicles/new/x-trail/price-specifications.html
- Cartube/Auto repo-local Israeli sources attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Fix source indexes; currentize 2026 rows only for 1.5 MHEV 163 and e-POWER 204/213 where repo-local/official sources are attached. Preserve single_speed/direct schema for e-POWER.
ACTION: FIX / ADD

#### VARIANT 2/8
MODEL: IL-confirmed|Nissan|X-Trail
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "hybrid",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 204,
  "transmission": "single_speed",
  "drivetrain": "FWD",
  "year_start": 2022,
  "year_end": 2024,
  "support_level": "direct",
  "source_indexes": [
    1082
  ]
}
```
PROBLEM: source_indexes [1082] are invalid for this profile because sources[] length is 5
WEB-VALIDATED FACT: Nissan Israel current X-Trail page and Israeli Auto/Cartube sources support current 1.5T MHEV 163 hp plus e-POWER 204 FWD / 213 AWD.
SOURCE:
- Nissan official X-Trail price/spec page: https://www.nissan.co.il/vehicles/new/x-trail/price-specifications.html
- Cartube/Auto repo-local Israeli sources attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Fix source indexes; currentize 2026 rows only for 1.5 MHEV 163 and e-POWER 204/213 where repo-local/official sources are attached. Preserve single_speed/direct schema for e-POWER.
ACTION: FIX / ADD

#### VARIANT 3/8
MODEL: IL-confirmed|Nissan|X-Trail
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "hybrid",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 213,
  "transmission": "single_speed",
  "drivetrain": "AWD",
  "year_start": 2022,
  "year_end": 2024,
  "support_level": "direct",
  "source_indexes": [
    1082
  ]
}
```
PROBLEM: source_indexes [1082] are invalid for this profile because sources[] length is 5
WEB-VALIDATED FACT: Nissan Israel current X-Trail page and Israeli Auto/Cartube sources support current 1.5T MHEV 163 hp plus e-POWER 204 FWD / 213 AWD.
SOURCE:
- Nissan official X-Trail price/spec page: https://www.nissan.co.il/vehicles/new/x-trail/price-specifications.html
- Cartube/Auto repo-local Israeli sources attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Fix source indexes; currentize 2026 rows only for 1.5 MHEV 163 and e-POWER 204/213 where repo-local/official sources are attached. Preserve single_speed/direct schema for e-POWER.
ACTION: FIX / ADD

#### VARIANT 4/8
MODEL: IL-confirmed|Nissan|X-Trail
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.3L turbo",
  "engine_displacement_l": 1.3,
  "horsepower_hp": 160,
  "transmission": "dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2019,
  "year_end": 2022,
  "support_level": "direct",
  "source_indexes": [
    1083
  ]
}
```
PROBLEM: source_indexes [1083] are invalid for this profile because sources[] length is 5
WEB-VALIDATED FACT: Official Nissan Israel current X-Trail page supports current model; Auto/Cartube support 2026/2023 powertrains. Fix invalid source_indexes. Keep historical rows; currentize 1.5 MHEV 163 and e-POWER 204/213 rows if local sources attached.
SOURCE:
- Nissan official X-Trail price/spec page: https://www.nissan.co.il/vehicles/new/x-trail/price-specifications.html
- Cartube/Auto repo-local Israeli sources attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Keep historical X-Trail row but fix source_indexes to valid local sources.
ACTION: FIX / ADD

#### VARIANT 5/8
MODEL: IL-confirmed|Nissan|X-Trail
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "1.6L turbo",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 130,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2014,
  "year_end": 2019,
  "support_level": "direct",
  "source_indexes": [
    1083
  ]
}
```
PROBLEM: source_indexes [1083] are invalid for this profile because sources[] length is 5
WEB-VALIDATED FACT: Official Nissan Israel current X-Trail page supports current model; Auto/Cartube support 2026/2023 powertrains. Fix invalid source_indexes. Keep historical rows; currentize 1.5 MHEV 163 and e-POWER 204/213 rows if local sources attached.
SOURCE:
- Nissan official X-Trail price/spec page: https://www.nissan.co.il/vehicles/new/x-trail/price-specifications.html
- Cartube/Auto repo-local Israeli sources attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Keep historical X-Trail row but fix source_indexes to valid local sources.
ACTION: FIX / ADD

#### VARIANT 6/8
MODEL: IL-confirmed|Nissan|X-Trail
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 177,
  "transmission": "cvt",
  "drivetrain": "4WD",
  "year_start": 2017,
  "year_end": 2019,
  "support_level": "direct",
  "source_indexes": [
    1084
  ]
}
```
PROBLEM: source_indexes [1084] are invalid for this profile because sources[] length is 5
WEB-VALIDATED FACT: Official Nissan Israel current X-Trail page supports current model; Auto/Cartube support 2026/2023 powertrains. Fix invalid source_indexes. Keep historical rows; currentize 1.5 MHEV 163 and e-POWER 204/213 rows if local sources attached.
SOURCE:
- Nissan official X-Trail price/spec page: https://www.nissan.co.il/vehicles/new/x-trail/price-specifications.html
- Cartube/Auto repo-local Israeli sources attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Keep historical X-Trail row but fix source_indexes to valid local sources.
ACTION: FIX / ADD

#### VARIANT 7/8
MODEL: IL-confirmed|Nissan|X-Trail
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 141,
  "transmission": "cvt",
  "drivetrain": "AWD",
  "year_start": 2007,
  "year_end": 2014,
  "support_level": "direct",
  "source_indexes": [
    1085
  ]
}
```
PROBLEM: source_indexes [1085] are invalid for this profile because sources[] length is 5
WEB-VALIDATED FACT: Official Nissan Israel current X-Trail page supports current model; Auto/Cartube support 2026/2023 powertrains. Fix invalid source_indexes. Keep historical rows; currentize 1.5 MHEV 163 and e-POWER 204/213 rows if local sources attached.
SOURCE:
- Nissan official X-Trail price/spec page: https://www.nissan.co.il/vehicles/new/x-trail/price-specifications.html
- Cartube/Auto repo-local Israeli sources attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Keep historical X-Trail row but fix source_indexes to valid local sources.
ACTION: FIX / ADD

#### VARIANT 8/8
MODEL: IL-confirmed|Nissan|X-Trail
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 140,
  "transmission": "automatic",
  "drivetrain": "4WD",
  "year_start": 2001,
  "year_end": 2007,
  "support_level": "direct",
  "source_indexes": [
    1086
  ]
}
```
PROBLEM: source_indexes [1086] are invalid for this profile because sources[] length is 5
WEB-VALIDATED FACT: Official Nissan Israel current X-Trail page supports current model; Auto/Cartube support 2026/2023 powertrains. Fix invalid source_indexes. Keep historical rows; currentize 1.5 MHEV 163 and e-POWER 204/213 rows if local sources attached.
SOURCE:
- Nissan official X-Trail price/spec page: https://www.nissan.co.il/vehicles/new/x-trail/price-specifications.html
- Cartube/Auto repo-local Israeli sources attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Keep historical X-Trail row but fix source_indexes to valid local sources.
ACTION: FIX / ADD

### MODEL PROFILE 664: global-reference-only|Omoda|C5
PROFILE SOURCES COUNT: 2
- source[0]: צ'רי FX - מחירון, מפרטים וירידת ערך - iCar — https://www.icar.co.il/%D7%A6'%D7%A8%D7%99/%D7%A6'%D7%A8%D7%99_FX/
- source[1]: כלמוביל מתחילה בשיווק מותגי OMODA ו- JAECOO בישראל - cartube — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9B%D7%9C%D7%9E%D7%95%D7%91%D7%99%D7%9C-%D7%9E%D7%AA%D7%97%D7%99%D7%9C%D7%94-%D7%91%D7%A9%D7%99%D7%95%D7%95%D7%A7-%D7%9E%D7%95%D7%AA%D7%92%D7%99-omoda-%D7%95-jaecoo-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C

#### VARIANT 1/1
MODEL: global-reference-only|Omoda|C5
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Crossover",
  "fuel_type": "petrol",
  "engine": "1.6L turbo",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 186,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2022,
  "year_end": 2024,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: global-reference-only profile must not remain as separate verified clean when Israeli canonical/confirmed model exists or evidence is weak.
WEB-VALIDATED FACT: C5 1.6T 186 is technically aligned with Chery FX/Omoda C5, but current official Omoda Israel price list does not list C5; duplicate global profile must not remain clean.
SOURCE:
- Omoda Israel price list: https://omoda.co.il/price-list/
- Repo-local Omoda/Chery sources attached above.
TARGET VALUE: MERGE into IL-confirmed canonical profile with alias/lineage, or ARCHIVE NON-BLOCKING if not grounded for Israel. Merge into IL-confirmed Omoda C5 or Chery FX alias only if repo-local policy allows; otherwise archive non-blocking with lineage.
ACTION: MERGE / ARCHIVE NON-BLOCKING

### MODEL PROFILE 665: IL-confirmed|Omoda|C5
PROFILE SOURCES COUNT: 2
- source[0]: Omoda C5 / Chery FX 1.6 Turbo Specifications Israel — https://www.icar.co.il/omoda/c5/
- source[1]: Omoda C5 2023 Models and Trims - Comfort — https://www.cartube.co.il/omoda-c5-israel-launch

#### VARIANT 1/1
MODEL: IL-confirmed|Omoda|C5
CURRENT VALUE:
```json
{
  "version_or_trim": "Comfort",
  "body_type": "Crossover",
  "fuel_type": "petrol",
  "engine": "1.6L turbo",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 186,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2023,
  "year_end": null,
  "support_level": "direct",
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: source_indexes [1, 2] are invalid for this profile because sources[] length is 2
WEB-VALIDATED FACT: Official Omoda Israel current price list found in this validation lists Omoda 7/9 PHEV, not C5. Attached repo sources may support older launch/Chery FX lineage.
SOURCE:
- Omoda Israel price list: https://omoda.co.il/price-list/
- Repo-local Omoda/Chery sources attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Do not leave year_end=null/current unless repo-local Israeli evidence proves current sales. Fix invalid [1,2] source indexes to valid profile sources or move to review.
ACTION: FIX / MOVE TO REVIEW

### MODEL PROFILE 666: IL-likely|Omoda|E5
PROFILE SOURCES COUNT: 2
- source[0]: אומודה E5 החשמלי בדרך לישראל - מפרט טכני — https://www.cartube.co.il/חדשות-רכב/אומודה-e5-החשמלי-בדרך-לישראל
- source[1]: אומודה E5 - מחירון רכב, מבחני דרכים ומפרט טכני — https://www.icar.co.il/אומודה/אומודה_E5/

#### VARIANT 1/1
MODEL: IL-likely|Omoda|E5
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "electric",
  "engine": "electric",
  "engine_displacement_l": null,
  "horsepower_hp": 204,
  "transmission": "single_speed",
  "drivetrain": "FWD",
  "year_start": 2024,
  "year_end": null,
  "support_level": "direct",
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: source_indexes [1, 2] are invalid for this profile because sources[] length is 2 IL-likely profile should not remain separate clean when an IL-confirmed canonical profile exists or official Israeli evidence is missing.
WEB-VALIDATED FACT: No strong official Israeli current price-list evidence for Omoda E5 was found; EV technical fields are plausible globally but not enough for verified Israeli clean.
SOURCE:
- Omoda Israel price list: https://omoda.co.il/price-list/
- Repo-local Omoda/Chery sources attached above.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Promote to IL-confirmed only with repo-local Israeli evidence; otherwise merge/alias or move to non-blocking review/archive. Move to non-blocking review/archive unless repo-local Israeli source proves actual local marketing/sales; keep EV schema if retained.
ACTION: MOVE TO REVIEW / ARCHIVE NON-BLOCKING

### MODEL PROFILE 667: IL-confirmed|Opel|Adam
PROFILE SOURCES COUNT: 4
- source[0]: אופל אדם - מחירון, מפרטים, ואבזור | iCar — https://www.icar.co.il/אופל/אופל_אדם/
- source[1]: אופל אדם S בישראל – מחיר החל מ-119,900 שקל — https://www.cartube.co.il/חדשות-רכב/אופל-אדם-s-בישראל-מחיר-החל-מ-119,900-שקל
- source[2]: אופל אדם רובוטית בישראל – מחיר החל מ-91,990 שקל — https://www.cartube.co.il/חדשות-רכב/אופל-אדם-אוטומטית-רובוטית-בישראל-מחיר-החל-מ-91,990-שקל
- source[3]: אופל אדם בישראל – מחיר החל מ-89,990 שקל — https://www.cartube.co.il/חדשות-רכב/אופל-אדם-בישראל-מחיר-החל-מ-89,990-שקל

#### VARIANT 1/3
MODEL: IL-confirmed|Opel|Adam
CURRENT VALUE:
```json
{
  "version_or_trim": "Jam",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 87,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 2014,
  "year_end": 2019,
  "support_level": "direct",
  "source_indexes": [
    2005,
    2008
  ]
}
```
PROBLEM: source_indexes [2005, 2008] are invalid for this profile because sources[] length is 4
WEB-VALIDATED FACT: Israeli iCar/Auto/Cartube sources support Adam 2014-2019; Adam S 1.4T 150 hp from 2016 and robotized 1.4 87 hp from 2015.
SOURCE:
- iCar Opel Adam 2014-2019 page and Cartube Adam automatic/S launch sources attached above.
- Auto/Cartube Israeli validation in web task.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Fix invalid source indexes [2005..] to attached local source indexes; keep historical year_end 2019.
ACTION: FIX

#### VARIANT 2/3
MODEL: IL-confirmed|Opel|Adam
CURRENT VALUE:
```json
{
  "version_or_trim": "Unlimited",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 87,
  "transmission": "5-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2015,
  "year_end": 2019,
  "support_level": "direct",
  "source_indexes": [
    2005,
    2007
  ]
}
```
PROBLEM: source_indexes [2005, 2007] are invalid for this profile because sources[] length is 4
WEB-VALIDATED FACT: Israeli iCar/Auto/Cartube sources support Adam 2014-2019; Adam S 1.4T 150 hp from 2016 and robotized 1.4 87 hp from 2015.
SOURCE:
- iCar Opel Adam 2014-2019 page and Cartube Adam automatic/S launch sources attached above.
- Auto/Cartube Israeli validation in web task.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Change transmission to 5-speed robotized/automated_manual if schema supports; this is not conventional automatic. Fix invalid source indexes [2005..] to attached local source indexes; keep historical year_end 2019.
ACTION: FIX

#### VARIANT 3/3
MODEL: IL-confirmed|Opel|Adam
CURRENT VALUE:
```json
{
  "version_or_trim": "S",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.4L turbo",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 150,
  "transmission": "6-speed manual",
  "drivetrain": "FWD",
  "year_start": 2016,
  "year_end": 2019,
  "support_level": "direct",
  "source_indexes": [
    2005,
    2006
  ]
}
```
PROBLEM: source_indexes [2005, 2006] are invalid for this profile because sources[] length is 4
WEB-VALIDATED FACT: Israeli iCar/Auto/Cartube sources support Adam 2014-2019; Adam S 1.4T 150 hp from 2016 and robotized 1.4 87 hp from 2015.
SOURCE:
- iCar Opel Adam 2014-2019 page and Cartube Adam automatic/S launch sources attached above.
- Auto/Cartube Israeli validation in web task.
TARGET VALUE: Replace source_indexes and field_sources with valid local profile source indexes that support each field. Fix invalid source indexes [2005..] to attached local source indexes; keep historical year_end 2019.
ACTION: FIX

### MODEL PROFILE 668: IL-confirmed|Opel|Ampera
PROFILE SOURCES COUNT: 2
- source[0]: אופל אמפרה 2012-2015: מחירון, מפרטים, תמונות - אוטו — https://www.auto.co.il/model/opel-ampera_g236
- source[1]: אופל אמפרה - מחירון, מפרטים, אמינות וחוות דעת - iCar — https://www.icar.co.il/אופל/אופל_אמפרה/

#### VARIANT 1/1
MODEL: IL-confirmed|Opel|Ampera
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Hatchback",
  "fuel_type": "plug_in_hybrid",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 150,
  "transmission": "cvt",
  "drivetrain": "FWD",
  "year_start": 2012,
  "year_end": 2015,
  "support_level": "direct",
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No blocker found beyond normalization/grounding check; still requires explicit field_sources and Israeli-market grounding. Null trim is only acceptable when schema/policy allows technical-variant grouping by engine/body/year.
WEB-VALIDATED FACT: Israeli Auto/iCar sources support Opel Ampera as 2012-2015 plug-in hybrid/extended-range EV, 1.4 generator and 150 hp electric drive.
SOURCE:
- Repo-local Auto/iCar Opel Ampera sources attached above.
TARGET VALUE: Keep historical only; if schema supports EREV/single_speed/electric_drive, use that instead of generic CVT. Do not currentize.
ACTION: KEEP/FIX

## Required checks after implementation
```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

## Direct audit required
- data/model_technical_catalog_il.json
- readiness report
- review file/report
- archive file/report
- quality scan output
- compute_resume_state()
- unmatched_output_keys
- active blockers
- cursor/resume state
- duplicate/split alias cleanup

## RUN 2 completion report required from Codex
1. Files changed
2. Exact before/after metrics
3. Confirmation that all 20 profiles and all 60 variants were handled
4. Test results
5. Confirmation that temporary `codex_tasks/BATCH27_RUN2_*.md` instruction files were deleted before final commit
6. Remaining issues, conflicts, or rows moved to review/archive

---

# BATCH27 RUN 3 — Variant-level Codex task

## Non-negotiable Codex rules

Do not browse the internet. All web-validation facts and target corrections are embedded in this task file. Use this task file as the single source of truth. Do not apply corrections outside RUN 3 scope. If repo-local evidence conflicts with this task, report the conflict instead of guessing. If a variant cannot be grounded with embedded facts or repo-local sources, move it to non-blocking review/archive with `non_blocking=true`, reason, and lineage.

Temporary-file cleanup is mandatory: before final commit, delete `codex_tasks/BATCH27_RUN3_*.md` unless the user explicitly asks to keep them.

## RUN 3 scope

```text
BATCH27 RUN 3 ONLY
clean profile indices in current ZIP catalog: 669-688
scope: IL-confirmed|Opel|Astra through first IL-confirmed|Opel|Vectra profile
profiles: 20
technical variants: 73
Do not apply RUN 1, RUN 2, RUN 4, RUN 5, FINAL blockers, or any unified batch task.
```

## Embedded web-validation sources

- **Opel Astra official current price list** — Current Astra GS Line 1.2L 130hp AT8 is sold/priced by Opel Israel.  
  URL: https://online.opel.co.il/pricelist/astra/
- **Opel Astra official model page** — Astra is a current Opel Israel model; local current clean row must use official current petrol row unless repo-local PHEV evidence exists.  
  URL: https://online.opel.co.il/model/new-astra/
- **Opel Corsa official price list** — Current Corsa includes GS 1.2L 130hp AT8 and GS MHEV 145hp AT6.  
  URL: https://online.opel.co.il/pricelist/corsa/
- **Opel Combo official model page** — Current Combo Life is marketed with 1.5L turbo-diesel, 130hp, 8-speed automatic.  
  URL: https://online.opel.co.il/model/combo/
- **Opel Frontera official model page** — New Frontera current Israeli page supports 1.2L turbo MHEV with 145hp and 6-speed dual-clutch automatic, 5/7-seat configuration.  
  URL: https://online.opel.co.il/model/frontera/
- **Opel Grandland official model page** — Current Grandland page supports new 1.2L turbo mild-hybrid, combined 145hp.  
  URL: https://online.opel.co.il/model/grandland/
- **Opel Mokka official model page** — Current Mokka MHEV page supports 145hp; pricelist also lists 130hp petrol AT8.  
  URL: https://online.opel.co.il/model/MOKKA/
- **Opel Mokka price list** — Current Mokka price list includes GS Line MHEV 145hp AT6 and GS Line 1.2L 130hp AT8.  
  URL: https://online.opel.co.il/pricelist/mokka/
- **Opel Tigra Yad2/Gear local specs** — Local price/spec entry supports Tigra coupe 1.4 petrol 90hp automatic/manual; use as Tier 3 for historical rows.  
  URL: https://www.yad2.co.il/price-list/sub-model/102185/1999
- **Opel Omega Gear local specs** — Local historical spec confirms Omega MV6/Omega Israeli presence and RWD sedan lineage; use with repo-local sources.  
  URL: https://www.gear.co.il/%D7%92%D7%A8%D7%A1%D7%94/%D7%90%D7%95%D7%A4%D7%9C/%D7%90%D7%95%D7%9E%D7%92%D7%94/2001/%D7%90%D7%95%D7%9E%D7%92%D7%94/3.0-MV6-%D7%90%D7%95%D7%98%D7%95%D7%9E%D7%98
- **Opel Meriva iCar** — Local iCar page supports Meriva historical Israeli variants; keep historical only.  
  URL: https://www.icar.co.il/%D7%90%D7%95%D7%A4%D7%9C/%D7%90%D7%95%D7%A4%D7%9C_%D7%9E%D7%A8%D7%99%D7%91%D7%94/%D7%90%D7%95%D7%A4%D7%9C_%D7%9E%D7%A8%D7%99%D7%91%D7%94_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9310/version13257/
- **Opel Insignia iCar local news** — Israeli article supports 1.5T 165hp and 2.0T 260hp local Insignia rows and says 1.6T 200hp did not arrive at that time; treat 200hp row carefully with later repo-local evidence.  
  URL: https://www.icar.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA_%D7%A8%D7%9B%D7%91/%D7%90%D7%95%D7%A4%D7%9C_%D7%90%D7%99%D7%A0%D7%A1%D7%99%D7%92%D7%A0%D7%99%D7%94_%D7%9E%D7%A7%D7%91%D7%9C%D7%AA_%D7%9E%D7%A0%D7%95%D7%A2_%D7%97%D7%93%D7%A9/

## Model-level decisions

- **Opel Astra:** Keep 2010-2021 historical rows if source_indexes/field_sources remain valid. FIX current petrol GS Line 1.2T 130hp AT8 to remain current through 2026/current. MOVE TO REVIEW or close as historical the 1.6T PHEV 180hp row unless repo-local official/importer source proves Israeli current PHEV sale; official current price-list evidence found here supports petrol 130, not a current PHEV row.
- **Opel Calibra:** MERGE all duplicate Calibra profiles into one canonical Opel Calibra with alias/lineage. KEEP 2.0 115hp manual/automatic and 2.0 150hp manual/automatic only once. KEEP 2.5 V6 170hp only if local Yad2/KML/Auto source remains attached. MOVE Turbo 204hp 4WD to non-blocking review if it is supported only by forum/global evidence; keep only with clear Israeli catalog evidence.
- **Opel Combo:** KEEP historical 2001-2018 rows. FIX current Combo Life 1.5 turbo-diesel 130hp 8AT FWD from year_start 2019 to current/2026 if official Opel Israel page/source is attached; normalize body_type to MPV/van policy used by repo and trim/name to Combo Life where appropriate.
- **Opel Corsa:** FIX invalid source_indexes [4] because sources length is 4; remap to valid official/source entry or add proper source. KEEP 2020-2024 Edition Plus 100hp as historical if valid. FIX/KEEP current GS 1.2T 130hp AT8 beyond 2024. ADD or FIX current GS MHEV 145hp AT6 row if repo schema supports mild_hybrid; do not fabricate if no repo-local source can be attached.
- **Opel Crossland:** KEEP Crossland/Crossland X historical 2017-2024. Do not currentize beyond 2024; current Opel Israel lineup has Frontera/Grandland/Mokka replacing the slot, and no official current Crossland evidence was found.
- **Opel Frontera:** FIX current rows: Israeli current Frontera is 1.2L turbo MHEV 145hp, 6-speed dual-clutch automatic, FWD, SUV, 5/7 seats. Do not keep duplicate 100hp and 136hp current rows as clean Israeli rows unless repo-local official evidence proves those exact Israeli variants. KEEP historical 1999-2003 2.2 petrol/diesel 4WD rows if source valid.
- **Opel Grandland:** MERGE duplicate Grandland profiles. KEEP historical X/previous generation rows with closed year_end. FIX current new Grandland to 1.2L turbo mild_hybrid 145hp, 6-speed dual-clutch automatic, FWD. Do not keep 130hp petrol/diesel or 225/300hp PHEV as current unless repo-local current importer source proves exact Israeli sale.
- **Opel Insignia:** KEEP historical only, no current. FIX invalid source_indexes 1992-1995 by remapping them to local sources [0..3]. Verify 2020-2022 2.0T 200hp carefully: if repo-local evidence does not prove Israeli sale, move that row to review; iCar source warns 1.6T 200 did not arrive at that time and local known rows include 1.5T 165 and 2.0T 260.
- **Opel Kadett:** MERGE duplicate Kadett profiles into one historical Opel Kadett profile if repo allows; keep hatchback 1.4 75hp and convertible 2.0 115hp only as Tier-3 historical with lineage/source quality notes. Do not treat as high-confidence official clean without stronger sources.
- **Opel Meriva:** KEEP historical 2003-2017 only. Keep 1.6 105hp first generation and 1.4T 120hp 2011-2017 if local iCar/Auto/Cartube source_indexes are valid. Do not currentize.
- **Opel Mokka:** KEEP 2013-2016 1.4T 140hp historical. FIX 2021+ Mokka: current official Opel Israel supports 1.2T 130hp AT8 and MHEV 145hp AT6. Do not leave one combined trim string 'Elegance / GS Line / Ultimate' as a single current trim row if repo policy requires separate trim/lineage; split or normalize. Add/fix 145hp MHEV only with local source.
- **Opel Omega:** MERGE duplicate Omega profiles. KEEP historical RWD sedan/estate rows only if local source valid. Prefer canonical trims from profile 684 (CD/CDX/Elegance/Executive); DELETE/merge profile 685 null-trim duplicates into canonical profile, preserving body_type Estate if supported.
- **Opel Tigra:** MERGE duplicate Tigra profiles. FIX invalid source_indexes referencing source 2 when sources length is 2. Keep Coupe 1.4 90hp manual/auto and 1.6 106hp manual historical; keep TwinTop/Convertible 1.4 90hp and 1.8 125hp only if local iCar/Auto/Yad2 sources support. Normalize body_type Coupe vs Convertible and avoid duplicated identical rows.
- **Opel Vectra:** KEEP historical only. RUN 3 handles first Vectra profile; adjacent duplicate second Vectra profile is outside this RUN and must be reported/deferred if not in scope. Do not currentize. Verify 1988/1989 start with repo-local source; keep 2.0 115, 2.0 136 and 2.2 147 if sources valid.

## Variant-level decisions — 73/73 variants


### PROFILE 669: Opel Astra — 5 variants
Profile years: `2010`–`2024`. Sources in profile: `7`.

#### VARIANT 001 / profile variant 1: Opel Astra
MODEL: Opel Astra
CURRENT VALUE:
```json
{
  "version_or_trim": "Enjoy",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.4L turbo",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 140,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2010,
  "year_end": 2016,
  "source_indexes": [
    2,
    3
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

#### VARIANT 002 / profile variant 2: Opel Astra
MODEL: Opel Astra
CURRENT VALUE:
```json
{
  "version_or_trim": "Enjoy",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "1.4L turbo",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 140,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2012,
  "year_end": 2018,
  "source_indexes": [
    4
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

#### VARIANT 003 / profile variant 3: Opel Astra
MODEL: Opel Astra
CURRENT VALUE:
```json
{
  "version_or_trim": "Enjoy Plus",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.4L turbo",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 150,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2016,
  "year_end": 2021,
  "source_indexes": [
    1,
    5
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

#### VARIANT 004 / profile variant 4: Opel Astra
MODEL: Opel Astra
CURRENT VALUE:
```json
{
  "version_or_trim": "GS Line",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 130,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2022,
  "year_end": 2024,
  "source_indexes": [
    0,
    6
  ]
}
```
PROBLEM: Current petrol Astra is closed at 2024 although Opel Israel current price list supports Astra GS Line 1.2L 130hp AT8.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Set/keep GS Line 1.2T petrol 130hp AT8 FWD as current through 2026/current; keep body Hatchback.
ACTION: FIX

#### VARIANT 005 / profile variant 5: Opel Astra
MODEL: Opel Astra
CURRENT VALUE:
```json
{
  "version_or_trim": "GS Line",
  "body_type": "Hatchback",
  "fuel_type": "plug_in_hybrid",
  "engine": "1.6L turbo",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 180,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2022,
  "year_end": 2024,
  "source_indexes": [
    0,
    6
  ]
}
```
PROBLEM: PHEV row is present as 2022-2024; no current official Opel Israel price-list support found in this RUN for Astra PHEV.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep historical closed 2022-2024 only if repo-local source supports; otherwise move to non-blocking review.
ACTION: MOVE TO REVIEW

### PROFILE 670: Opel Calibra — 3 variants
Profile years: `1990`–`1997`. Sources in profile: `2`.

#### VARIANT 006 / profile variant 1: Opel Calibra
MODEL: Opel Calibra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "2.0L inline-4",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 115,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 1990,
  "year_end": 1997,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Calibra appears in three duplicate clean profiles with overlapping 2.0 rows.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge to one Opel Calibra canonical profile; keep each technical row once with local sources.
ACTION: MERGE

#### VARIANT 007 / profile variant 2: Opel Calibra
MODEL: Opel Calibra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "2.0L inline-4",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 115,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 1990,
  "year_end": 1997,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Calibra appears in three duplicate clean profiles with overlapping 2.0 rows.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge to one Opel Calibra canonical profile; keep each technical row once with local sources.
ACTION: MERGE

#### VARIANT 008 / profile variant 3: Opel Calibra
MODEL: Opel Calibra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "2.0L inline-4",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 150,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 1990,
  "year_end": 1997,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Calibra appears in three duplicate clean profiles with overlapping 2.0 rows.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge to one Opel Calibra canonical profile; keep each technical row once with local sources.
ACTION: MERGE

### PROFILE 671: Opel Calibra — 5 variants
Profile years: `1992`–`1997`. Sources in profile: `2`.

#### VARIANT 009 / profile variant 1: Opel Calibra
MODEL: Opel Calibra
CURRENT VALUE:
```json
{
  "version_or_trim": "Turbo",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 204,
  "transmission": "6-speed manual",
  "drivetrain": "4WD",
  "year_start": 1992,
  "year_end": 1997,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Turbo 204hp 4WD row is rare and may be supported by forum/global evidence rather than strong Israeli catalog source.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep only with clear local Auto/Yad2/importer evidence; otherwise non-blocking review with lineage.
ACTION: MOVE TO REVIEW

#### VARIANT 010 / profile variant 2: Opel Calibra
MODEL: Opel Calibra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 150,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 1992,
  "year_end": 1997,
  "source_indexes": [
    0
  ]
}
```
PROBLEM: Calibra appears in three duplicate clean profiles with overlapping 2.0 rows.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge to one Opel Calibra canonical profile; keep each technical row once with local sources.
ACTION: MERGE

#### VARIANT 011 / profile variant 3: Opel Calibra
MODEL: Opel Calibra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 150,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 1992,
  "year_end": 1997,
  "source_indexes": [
    0
  ]
}
```
PROBLEM: Calibra appears in three duplicate clean profiles with overlapping 2.0 rows.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge to one Opel Calibra canonical profile; keep each technical row once with local sources.
ACTION: MERGE

#### VARIANT 012 / profile variant 4: Opel Calibra
MODEL: Opel Calibra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 115,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 1992,
  "year_end": 1997,
  "source_indexes": [
    0
  ]
}
```
PROBLEM: Calibra appears in three duplicate clean profiles with overlapping 2.0 rows.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge to one Opel Calibra canonical profile; keep each technical row once with local sources.
ACTION: MERGE

#### VARIANT 013 / profile variant 5: Opel Calibra
MODEL: Opel Calibra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 115,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 1992,
  "year_end": 1997,
  "source_indexes": [
    0
  ]
}
```
PROBLEM: Calibra appears in three duplicate clean profiles with overlapping 2.0 rows.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge to one Opel Calibra canonical profile; keep each technical row once with local sources.
ACTION: MERGE

### PROFILE 672: Opel Calibra — 1 variants
Profile years: `1993`–`1997`. Sources in profile: `2`.

#### VARIANT 014 / profile variant 1: Opel Calibra
MODEL: Opel Calibra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "2.5L v6",
  "engine_displacement_l": 2.5,
  "horsepower_hp": 170,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 1993,
  "year_end": 1997,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Calibra appears in three duplicate clean profiles with overlapping 2.0 rows.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge to one Opel Calibra canonical profile; keep each technical row once with local sources.
ACTION: MERGE

### PROFILE 673: Opel Combo — 4 variants
Profile years: `2001`–`2024`. Sources in profile: `4`.

#### VARIANT 015 / profile variant 1: Opel Combo
MODEL: Opel Combo
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Van",
  "fuel_type": "petrol",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 90,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 2001,
  "year_end": 2011,
  "source_indexes": [
    3
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

#### VARIANT 016 / profile variant 2: Opel Combo
MODEL: Opel Combo
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Van",
  "fuel_type": "petrol",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 95,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 2012,
  "year_end": 2018,
  "source_indexes": [
    2
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

#### VARIANT 017 / profile variant 3: Opel Combo
MODEL: Opel Combo
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Van",
  "fuel_type": "diesel",
  "engine": "1.6L turbo",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 105,
  "transmission": "6-speed manual",
  "drivetrain": "FWD",
  "year_start": 2012,
  "year_end": 2018,
  "source_indexes": [
    2
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

#### VARIANT 018 / profile variant 4: Opel Combo
MODEL: Opel Combo
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "MPV",
  "fuel_type": "diesel",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 130,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2019,
  "year_end": 2024,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Combo Life 1.5 diesel 130hp 8AT current row is closed at 2024, but Opel Israel current page supports Combo Life 130hp diesel 8AT.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Currentize to 2026/current; normalize trim/model line to Combo Life if schema supports.
ACTION: FIX

### PROFILE 674: Opel Corsa — 4 variants
Profile years: `2010`–`2024`. Sources in profile: `4`.

#### VARIANT 019 / profile variant 1: Opel Corsa
MODEL: Opel Corsa
CURRENT VALUE:
```json
{
  "version_or_trim": "Edition Plus",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 100,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2020,
  "year_end": 2024,
  "source_indexes": [
    1,
    4
  ]
}
```
PROBLEM: 100hp Edition Plus row is historical; current price list supports 130hp/145hp, not 100hp as current.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep as 2020-2024 historical only; do not currentize.
ACTION: KEEP

#### VARIANT 020 / profile variant 2: Opel Corsa
MODEL: Opel Corsa
CURRENT VALUE:
```json
{
  "version_or_trim": "GS Line",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 130,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2020,
  "year_end": 2024,
  "source_indexes": [
    1,
    4
  ]
}
```
PROBLEM: source_indexes include [4] but profile has only 4 sources indexed 0-3. Also current Corsa GS 1.2L 130hp AT8 is still in Opel Israel price list.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Replace source_indexes with valid local/current source indexes and field_sources. Keep/currentize 130hp AT8 to 2026/current.
ACTION: FIX

#### VARIANT 021 / profile variant 3: Opel Corsa
MODEL: Opel Corsa
CURRENT VALUE:
```json
{
  "version_or_trim": "Enjoy",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.4L naturally aspirated",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 90,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2015,
  "year_end": 2019,
  "source_indexes": [
    2
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

#### VARIANT 022 / profile variant 4: Opel Corsa
MODEL: Opel Corsa
CURRENT VALUE:
```json
{
  "version_or_trim": "Enjoy",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.4L naturally aspirated",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 100,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2010,
  "year_end": 2014,
  "source_indexes": [
    3
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

### PROFILE 675: Opel Crossland — 2 variants
Profile years: `2017`–`2024`. Sources in profile: `3`.

#### VARIANT 023 / profile variant 1: Opel Crossland
MODEL: Opel Crossland
CURRENT VALUE:
```json
{
  "version_or_trim": "Enjoy",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 110,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2017,
  "year_end": 2020,
  "source_indexes": [
    0,
    2
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

#### VARIANT 024 / profile variant 2: Opel Crossland
MODEL: Opel Crossland
CURRENT VALUE:
```json
{
  "version_or_trim": "Elegance",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 130,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2020,
  "year_end": 2024,
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: Crossland is historical/current-ended; no current official Crossland evidence found.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep closed at 2024; do not currentize.
ACTION: KEEP

### PROFILE 676: Opel Frontera — 5 variants
Profile years: `1999`–`None`. Sources in profile: `2`.

#### VARIANT 025 / profile variant 1: Opel Frontera
MODEL: Opel Frontera
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "mild_hybrid",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 100,
  "transmission": "6-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2024,
  "year_end": null,
  "source_indexes": [
    0
  ]
}
```
PROBLEM: Current Israeli Frontera official page supports 1.2T MHEV 145hp, not separate 100hp/136hp rows as clean Israeli rows.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Collapse/replace current rows with one 1.2T MHEV 145hp 6-speed dual-clutch FWD SUV row, year_start 2025/2026 per repo-local official source.
ACTION: FIX

#### VARIANT 026 / profile variant 2: Opel Frontera
MODEL: Opel Frontera
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "mild_hybrid",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 136,
  "transmission": "6-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2024,
  "year_end": null,
  "source_indexes": [
    0
  ]
}
```
PROBLEM: Current Israeli Frontera official page supports 1.2T MHEV 145hp, not separate 100hp/136hp rows as clean Israeli rows.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Collapse/replace current rows with one 1.2T MHEV 145hp 6-speed dual-clutch FWD SUV row, year_start 2025/2026 per repo-local official source.
ACTION: FIX

#### VARIANT 027 / profile variant 3: Opel Frontera
MODEL: Opel Frontera
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.2L",
  "engine_displacement_l": 2.2,
  "horsepower_hp": 136,
  "transmission": "4-speed automatic",
  "drivetrain": "4WD",
  "year_start": 1999,
  "year_end": 2003,
  "source_indexes": [
    1
  ]
}
```
PROBLEM: Historical 1999-2003 Frontera row; keep only if local iCar source validates fields.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep historical 4WD petrol/diesel rows with valid sources.
ACTION: KEEP

#### VARIANT 028 / profile variant 4: Opel Frontera
MODEL: Opel Frontera
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.2L",
  "engine_displacement_l": 2.2,
  "horsepower_hp": 136,
  "transmission": "5-speed manual",
  "drivetrain": "4WD",
  "year_start": 1999,
  "year_end": 2003,
  "source_indexes": [
    1
  ]
}
```
PROBLEM: Historical 1999-2003 Frontera row; keep only if local iCar source validates fields.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep historical 4WD petrol/diesel rows with valid sources.
ACTION: KEEP

#### VARIANT 029 / profile variant 5: Opel Frontera
MODEL: Opel Frontera
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "2.2L turbo",
  "engine_displacement_l": 2.2,
  "horsepower_hp": 115,
  "transmission": "4-speed automatic",
  "drivetrain": "4WD",
  "year_start": 1999,
  "year_end": 2003,
  "source_indexes": [
    1
  ]
}
```
PROBLEM: Historical 1999-2003 Frontera row; keep only if local iCar source validates fields.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep historical 4WD petrol/diesel rows with valid sources.
ACTION: KEEP

### PROFILE 677: Opel Grandland — 6 variants
Profile years: `2018`–`2024`. Sources in profile: `4`.

#### VARIANT 030 / profile variant 1: Opel Grandland
MODEL: Opel Grandland
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 130,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2018,
  "year_end": 2019,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

#### VARIANT 031 / profile variant 2: Opel Grandland
MODEL: Opel Grandland
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 130,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2019,
  "year_end": 2024,
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: Grandland has duplicate profiles and old/current rows. Current official Opel Israel Grandland supports 1.2T MHEV 145hp.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles; keep older petrol/diesel/PHEV rows historical; fix current MHEV row to 145hp 6DCT FWD current.
ACTION: FIX

#### VARIANT 032 / profile variant 3: Opel Grandland
MODEL: Opel Grandland
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "1.6L turbo",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 120,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2018,
  "year_end": 2019,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

#### VARIANT 033 / profile variant 4: Opel Grandland
MODEL: Opel Grandland
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 130,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2019,
  "year_end": 2024,
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: Grandland has duplicate profiles and old/current rows. Current official Opel Israel Grandland supports 1.2T MHEV 145hp.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles; keep older petrol/diesel/PHEV rows historical; fix current MHEV row to 145hp 6DCT FWD current.
ACTION: FIX

#### VARIANT 034 / profile variant 5: Opel Grandland
MODEL: Opel Grandland
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "plug_in_hybrid",
  "engine": "1.6L turbo",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 225,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2021,
  "year_end": 2024,
  "source_indexes": [
    1,
    3
  ]
}
```
PROBLEM: Grandland has duplicate profiles and old/current rows. Current official Opel Israel Grandland supports 1.2T MHEV 145hp.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles; keep older petrol/diesel/PHEV rows historical; fix current MHEV row to 145hp 6DCT FWD current.
ACTION: FIX

#### VARIANT 035 / profile variant 6: Opel Grandland
MODEL: Opel Grandland
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "plug_in_hybrid",
  "engine": "1.6L turbo",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 300,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2021,
  "year_end": 2022,
  "source_indexes": [
    1,
    3
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

### PROFILE 678: Opel Grandland — 3 variants
Profile years: `2022`–`2024`. Sources in profile: `2`.

#### VARIANT 036 / profile variant 1: Opel Grandland
MODEL: Opel Grandland
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 130,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2022,
  "year_end": 2024,
  "source_indexes": [
    0
  ]
}
```
PROBLEM: Grandland has duplicate profiles and old/current rows. Current official Opel Israel Grandland supports 1.2T MHEV 145hp.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles; keep older petrol/diesel/PHEV rows historical; fix current MHEV row to 145hp 6DCT FWD current.
ACTION: FIX

#### VARIANT 037 / profile variant 2: Opel Grandland
MODEL: Opel Grandland
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "plug_in_hybrid",
  "engine": "1.6L turbo",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 225,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2022,
  "year_end": 2024,
  "source_indexes": [
    0
  ]
}
```
PROBLEM: Grandland has duplicate profiles and old/current rows. Current official Opel Israel Grandland supports 1.2T MHEV 145hp.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles; keep older petrol/diesel/PHEV rows historical; fix current MHEV row to 145hp 6DCT FWD current.
ACTION: FIX

#### VARIANT 038 / profile variant 3: Opel Grandland
MODEL: Opel Grandland
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "mild_hybrid",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 136,
  "transmission": "6-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2024,
  "year_end": 2024,
  "source_indexes": [
    1
  ]
}
```
PROBLEM: Grandland has duplicate profiles and old/current rows. Current official Opel Israel Grandland supports 1.2T MHEV 145hp.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles; keep older petrol/diesel/PHEV rows historical; fix current MHEV row to 145hp 6DCT FWD current.
ACTION: FIX

### PROFILE 679: Opel Insignia — 6 variants
Profile years: `2009`–`2022`. Sources in profile: `4`.

#### VARIANT 039 / profile variant 1: Opel Insignia
MODEL: Opel Insignia
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 220,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2009,
  "year_end": 2013,
  "source_indexes": [
    1992
  ]
}
```
PROBLEM: Invalid source_indexes use absolute legacy ids 1992-1995 rather than local source indexes 0-3.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Remap source_indexes/field_sources to actual profile sources.
ACTION: FIX

#### VARIANT 040 / profile variant 2: Opel Insignia
MODEL: Opel Insignia
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "1.6L turbo",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 170,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2014,
  "year_end": 2017,
  "source_indexes": [
    1993
  ]
}
```
PROBLEM: Invalid source_indexes use absolute legacy ids 1992-1995 rather than local source indexes 0-3.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Remap source_indexes/field_sources to actual profile sources.
ACTION: FIX

#### VARIANT 041 / profile variant 3: Opel Insignia
MODEL: Opel Insignia
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 250,
  "transmission": "6-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2014,
  "year_end": 2017,
  "source_indexes": [
    1993
  ]
}
```
PROBLEM: Invalid source_indexes use absolute legacy ids 1992-1995 rather than local source indexes 0-3.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Remap source_indexes/field_sources to actual profile sources.
ACTION: FIX

#### VARIANT 042 / profile variant 4: Opel Insignia
MODEL: Opel Insignia
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Liftback",
  "fuel_type": "petrol",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 165,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2017,
  "year_end": 2020,
  "source_indexes": [
    1994
  ]
}
```
PROBLEM: Invalid source_indexes use absolute legacy ids 1992-1995 rather than local source indexes 0-3.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Remap source_indexes/field_sources to actual profile sources.
ACTION: FIX

#### VARIANT 043 / profile variant 5: Opel Insignia
MODEL: Opel Insignia
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Liftback",
  "fuel_type": "petrol",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 260,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2017,
  "year_end": 2020,
  "source_indexes": [
    1994
  ]
}
```
PROBLEM: Invalid source_indexes use absolute legacy ids 1992-1995 rather than local source indexes 0-3.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Remap source_indexes/field_sources to actual profile sources.
ACTION: FIX

#### VARIANT 044 / profile variant 6: Opel Insignia
MODEL: Opel Insignia
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Liftback",
  "fuel_type": "petrol",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 200,
  "transmission": "9-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2020,
  "year_end": 2022,
  "source_indexes": [
    1995
  ]
}
```
PROBLEM: Invalid source_indexes use absolute legacy ids 1992-1995 rather than local source indexes 0-3. 2.0T 200hp row requires stronger local evidence; iCar source warns 1.6T 200 did not arrive at that time.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Remap source_indexes/field_sources to actual profile sources. Move to review if exact 2.0T 200hp Israeli source is not present.
ACTION: MOVE TO REVIEW

### PROFILE 680: Opel Kadett — 1 variants
Profile years: `1990`–`1991`. Sources in profile: `1`.

#### VARIANT 045 / profile variant 1: Opel Kadett
MODEL: Opel Kadett
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 75,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 1990,
  "year_end": 1991,
  "source_indexes": [
    0
  ]
}
```
PROBLEM: Kadett appears as duplicate profiles with weak historical/Tier-3 evidence.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge into one historical Kadett profile or archive non-blocking with lineage if source policy rejects weak evidence.
ACTION: MERGE

### PROFILE 681: Opel Kadett — 1 variants
Profile years: `1990`–`1993`. Sources in profile: `2`.

#### VARIANT 046 / profile variant 1: Opel Kadett
MODEL: Opel Kadett
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 115,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 1990,
  "year_end": 1993,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Kadett appears as duplicate profiles with weak historical/Tier-3 evidence.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge into one historical Kadett profile or archive non-blocking with lineage if source policy rejects weak evidence.
ACTION: MERGE

### PROFILE 682: Opel Meriva — 2 variants
Profile years: `2003`–`2017`. Sources in profile: `3`.

#### VARIANT 047 / profile variant 1: Opel Meriva
MODEL: Opel Meriva
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "MPV",
  "fuel_type": "petrol",
  "engine": "1.6L",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 105,
  "transmission": "5-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2003,
  "year_end": 2010,
  "source_indexes": [
    0
  ]
}
```
PROBLEM: Historical Meriva rows; no current status.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep 2003-2017 rows only with valid iCar/Auto sources; do not currentize.
ACTION: KEEP

#### VARIANT 048 / profile variant 2: Opel Meriva
MODEL: Opel Meriva
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "MPV",
  "fuel_type": "petrol",
  "engine": "1.4L turbo",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 120,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2011,
  "year_end": 2017,
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: Historical Meriva rows; no current status.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep 2003-2017 rows only with valid iCar/Auto sources; do not currentize.
ACTION: KEEP

### PROFILE 683: Opel Mokka — 2 variants
Profile years: `2013`–`2024`. Sources in profile: `3`.

#### VARIANT 049 / profile variant 1: Opel Mokka
MODEL: Opel Mokka
CURRENT VALUE:
```json
{
  "version_or_trim": "Enjoy",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.4L turbo",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 140,
  "transmission": "6-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2013,
  "year_end": 2016,
  "source_indexes": [
    0
  ]
}
```
PROBLEM: No field-level blocker found beyond source freshness/validity check; keep only if source_indexes/field_sources are valid.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep values as-is and ensure field_sources/source_indexes resolve to real sources.
ACTION: KEEP

#### VARIANT 050 / profile variant 2: Opel Mokka
MODEL: Opel Mokka
CURRENT VALUE:
```json
{
  "version_or_trim": "Elegance / GS Line / Ultimate",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.2L turbo",
  "engine_displacement_l": 1.2,
  "horsepower_hp": 130,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2021,
  "year_end": 2024,
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: Current Mokka row combines trims and lacks 145hp MHEV row; official Opel Israel supports Mokka 1.2T 130hp AT8 and Mokka MHEV 145hp AT6.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Split/normalize trims per schema; keep 130hp current and add/fix 145hp MHEV current if repo-local source can be attached.
ACTION: FIX

### PROFILE 684: Opel Omega — 5 variants
Profile years: `1990`–`2003`. Sources in profile: `3`.

#### VARIANT 051 / profile variant 1: Opel Omega
MODEL: Opel Omega
CURRENT VALUE:
```json
{
  "version_or_trim": "CD",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.0L inline-4",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 115,
  "transmission": "4-speed automatic",
  "drivetrain": "RWD",
  "year_start": 1990,
  "year_end": 1993,
  "source_indexes": [
    2
  ]
}
```
PROBLEM: Historical RWD Omega row with trim; keep if source-backed.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep as historical only with valid source indexes.
ACTION: KEEP

#### VARIANT 052 / profile variant 2: Opel Omega
MODEL: Opel Omega
CURRENT VALUE:
```json
{
  "version_or_trim": "CD",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.0L inline-4",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 136,
  "transmission": "4-speed automatic",
  "drivetrain": "RWD",
  "year_start": 1994,
  "year_end": 1999,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Historical RWD Omega row with trim; keep if source-backed.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep as historical only with valid source indexes.
ACTION: KEEP

#### VARIANT 053 / profile variant 3: Opel Omega
MODEL: Opel Omega
CURRENT VALUE:
```json
{
  "version_or_trim": "CDX",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.5L v6",
  "engine_displacement_l": 2.5,
  "horsepower_hp": 170,
  "transmission": "4-speed automatic",
  "drivetrain": "RWD",
  "year_start": 1994,
  "year_end": 1999,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Historical RWD Omega row with trim; keep if source-backed.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep as historical only with valid source indexes.
ACTION: KEEP

#### VARIANT 054 / profile variant 4: Opel Omega
MODEL: Opel Omega
CURRENT VALUE:
```json
{
  "version_or_trim": "Elegance",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.2L inline-4",
  "engine_displacement_l": 2.2,
  "horsepower_hp": 144,
  "transmission": "4-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2000,
  "year_end": 2003,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Historical RWD Omega row with trim; keep if source-backed.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep as historical only with valid source indexes.
ACTION: KEEP

#### VARIANT 055 / profile variant 5: Opel Omega
MODEL: Opel Omega
CURRENT VALUE:
```json
{
  "version_or_trim": "Executive",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.6L v6",
  "engine_displacement_l": 2.6,
  "horsepower_hp": 180,
  "transmission": "4-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2000,
  "year_end": 2003,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Historical RWD Omega row with trim; keep if source-backed.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep as historical only with valid source indexes.
ACTION: KEEP

### PROFILE 685: Opel Omega — 5 variants
Profile years: `1994`–`2003`. Sources in profile: `2`.

#### VARIANT 056 / profile variant 1: Opel Omega
MODEL: Opel Omega
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Estate",
  "fuel_type": "petrol",
  "engine": "2.0L inline-4",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 136,
  "transmission": "4-speed automatic",
  "drivetrain": "RWD",
  "year_start": 1994,
  "year_end": 1999,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Duplicate Omega profile with null trim rows overlaps canonical trimmed Omega profile.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge into canonical Omega profile, preserving Estate body only if source-backed; do not keep duplicate null-trim rows.
ACTION: MERGE

#### VARIANT 057 / profile variant 2: Opel Omega
MODEL: Opel Omega
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.0L inline-4",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 136,
  "transmission": "4-speed automatic",
  "drivetrain": "RWD",
  "year_start": 1994,
  "year_end": 1999,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Duplicate Omega profile with null trim rows overlaps canonical trimmed Omega profile.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge into canonical Omega profile, preserving Estate body only if source-backed; do not keep duplicate null-trim rows.
ACTION: MERGE

#### VARIANT 058 / profile variant 3: Opel Omega
MODEL: Opel Omega
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.5L v6",
  "engine_displacement_l": 2.5,
  "horsepower_hp": 170,
  "transmission": "4-speed automatic",
  "drivetrain": "RWD",
  "year_start": 1994,
  "year_end": 1999,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Duplicate Omega profile with null trim rows overlaps canonical trimmed Omega profile.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge into canonical Omega profile, preserving Estate body only if source-backed; do not keep duplicate null-trim rows.
ACTION: MERGE

#### VARIANT 059 / profile variant 4: Opel Omega
MODEL: Opel Omega
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.2L inline-4",
  "engine_displacement_l": 2.2,
  "horsepower_hp": 144,
  "transmission": "4-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2000,
  "year_end": 2003,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Duplicate Omega profile with null trim rows overlaps canonical trimmed Omega profile.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge into canonical Omega profile, preserving Estate body only if source-backed; do not keep duplicate null-trim rows.
ACTION: MERGE

#### VARIANT 060 / profile variant 5: Opel Omega
MODEL: Opel Omega
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.6L v6",
  "engine_displacement_l": 2.6,
  "horsepower_hp": 180,
  "transmission": "4-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2000,
  "year_end": 2003,
  "source_indexes": [
    0,
    1
  ]
}
```
PROBLEM: Duplicate Omega profile with null trim rows overlaps canonical trimmed Omega profile.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge into canonical Omega profile, preserving Estate body only if source-backed; do not keep duplicate null-trim rows.
ACTION: MERGE

### PROFILE 686: Opel Tigra — 5 variants
Profile years: `1994`–`2009`. Sources in profile: `2`.

#### VARIANT 061 / profile variant 1: Opel Tigra
MODEL: Opel Tigra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 90,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 1994,
  "year_end": 2000,
  "source_indexes": [
    1
  ]
}
```
PROBLEM: Historical Tigra row in duplicate profile set.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep only once in canonical Tigra profile with valid sources.
ACTION: KEEP/MERGE

#### VARIANT 062 / profile variant 2: Opel Tigra
MODEL: Opel Tigra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 90,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 1994,
  "year_end": 2000,
  "source_indexes": [
    1
  ]
}
```
PROBLEM: Historical Tigra row in duplicate profile set.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep only once in canonical Tigra profile with valid sources.
ACTION: KEEP/MERGE

#### VARIANT 063 / profile variant 3: Opel Tigra
MODEL: Opel Tigra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "1.6L",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 106,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 1994,
  "year_end": 2000,
  "source_indexes": [
    1
  ]
}
```
PROBLEM: Historical Tigra row in duplicate profile set.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep only once in canonical Tigra profile with valid sources.
ACTION: KEEP/MERGE

#### VARIANT 064 / profile variant 4: Opel Tigra
MODEL: Opel Tigra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 90,
  "transmission": "5-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2004,
  "year_end": 2009,
  "source_indexes": [
    2
  ]
}
```
PROBLEM: Duplicate Tigra profiles and invalid source index references; some variants overlap.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles, remap source_indexes, keep each Coupe/TwinTop variant once if local source-backed.
ACTION: FIX/MERGE

#### VARIANT 065 / profile variant 5: Opel Tigra
MODEL: Opel Tigra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 90,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 2004,
  "year_end": 2009,
  "source_indexes": [
    2
  ]
}
```
PROBLEM: Duplicate Tigra profiles and invalid source index references; some variants overlap.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles, remap source_indexes, keep each Coupe/TwinTop variant once if local source-backed.
ACTION: FIX/MERGE

### PROFILE 687: Opel Tigra — 5 variants
Profile years: `1995`–`2009`. Sources in profile: `2`.

#### VARIANT 066 / profile variant 1: Opel Tigra
MODEL: Opel Tigra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 90,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 1995,
  "year_end": 2000,
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: Duplicate Tigra profiles and invalid source index references; some variants overlap.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles, remap source_indexes, keep each Coupe/TwinTop variant once if local source-backed.
ACTION: FIX/MERGE

#### VARIANT 067 / profile variant 2: Opel Tigra
MODEL: Opel Tigra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 90,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 1995,
  "year_end": 2000,
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: Duplicate Tigra profiles and invalid source index references; some variants overlap.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles, remap source_indexes, keep each Coupe/TwinTop variant once if local source-backed.
ACTION: FIX/MERGE

#### VARIANT 068 / profile variant 3: Opel Tigra
MODEL: Opel Tigra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "1.6L",
  "engine_displacement_l": 1.6,
  "horsepower_hp": 106,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 1995,
  "year_end": 2000,
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: Duplicate Tigra profiles and invalid source index references; some variants overlap.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles, remap source_indexes, keep each Coupe/TwinTop variant once if local source-backed.
ACTION: FIX/MERGE

#### VARIANT 069 / profile variant 4: Opel Tigra
MODEL: Opel Tigra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "1.4L",
  "engine_displacement_l": 1.4,
  "horsepower_hp": 90,
  "transmission": "5-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2004,
  "year_end": 2009,
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: Duplicate Tigra profiles and invalid source index references; some variants overlap.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles, remap source_indexes, keep each Coupe/TwinTop variant once if local source-backed.
ACTION: FIX/MERGE

#### VARIANT 070 / profile variant 5: Opel Tigra
MODEL: Opel Tigra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "1.8L",
  "engine_displacement_l": 1.8,
  "horsepower_hp": 125,
  "transmission": "5-speed manual",
  "drivetrain": "FWD",
  "year_start": 2004,
  "year_end": 2009,
  "source_indexes": [
    1,
    2
  ]
}
```
PROBLEM: Duplicate Tigra profiles and invalid source index references; some variants overlap.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Merge duplicate profiles, remap source_indexes, keep each Coupe/TwinTop variant once if local source-backed.
ACTION: FIX/MERGE

### PROFILE 688: Opel Vectra — 3 variants
Profile years: `1988`–`2008`. Sources in profile: `3`.

#### VARIANT 071 / profile variant 1: Opel Vectra
MODEL: Opel Vectra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 115,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 1988,
  "year_end": 1995,
  "source_indexes": [
    2
  ]
}
```
PROBLEM: Historical Vectra row; adjacent second Vectra duplicate is outside RUN 3 scope.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep historical row if source-backed and report cross-run duplicate to resolve in RUN 4.
ACTION: KEEP/DEFER DUPLICATE

#### VARIANT 072 / profile variant 2: Opel Vectra
MODEL: Opel Vectra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 136,
  "transmission": "4-speed automatic",
  "drivetrain": "FWD",
  "year_start": 1996,
  "year_end": 2002,
  "source_indexes": [
    0
  ]
}
```
PROBLEM: Historical Vectra row; adjacent second Vectra duplicate is outside RUN 3 scope.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep historical row if source-backed and report cross-run duplicate to resolve in RUN 4.
ACTION: KEEP/DEFER DUPLICATE

#### VARIANT 073 / profile variant 3: Opel Vectra
MODEL: Opel Vectra
CURRENT VALUE:
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.2L",
  "engine_displacement_l": 2.2,
  "horsepower_hp": 147,
  "transmission": "5-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2003,
  "year_end": 2008,
  "source_indexes": [
    1
  ]
}
```
PROBLEM: Historical Vectra row; adjacent second Vectra duplicate is outside RUN 3 scope.
WEB-VALIDATED FACT: See embedded source facts above and repo-local sources. Current Opel Israel sources override stale 2024 closures for Astra/Corsa/Combo/Frontera/Grandland/Mokka; historical Opel models must not be currentized without exact local evidence.
SOURCE: Embedded web-validation sources in this file plus existing repo-local source_indexes/field_sources after they are made valid.
TARGET VALUE: Keep historical row if source-backed and report cross-run duplicate to resolve in RUN 4.
ACTION: KEEP/DEFER DUPLICATE

## Required checks after implementation

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

## Required direct audit

- clean catalog
- readiness
- review
- archive
- quality scan
- compute_resume_state()
- unmatched_output_keys
- active blockers
- cursor/resume state
- duplicate/split alias cleanup

## Required Codex report

1. Files changed
2. Exact before/after metrics
3. Confirmation that all 20 profiles and all 73 variants were handled
4. Test results
5. Confirmation that temporary RUN3 instruction files were deleted before final commit
6. Remaining issues/conflicts, if any


---

# BATCH27 RUN 4 — VARIANT-LEVEL CODEX TASK

## Scope

Apply **BATCH27 RUN 4 only**. Do not apply RUN 1, RUN 2, RUN 3, RUN 5, FINAL blockers/review/unmatched, or any unified batch task.

RUN 4 scope:

```text
IL-confirmed|Opel|Vectra
through
global-reference-only|Peugeot|408
```

Profiles: 20.
Technical variants: 99.

## Non-browsing rule

Do not browse the internet. All web-validation facts and target corrections for RUN 4 are embedded in this file. Use this file as the single source of truth. Do not apply corrections that are not instructed here. If repo-local evidence conflicts with this task file, report it instead of guessing. If a variant cannot be grounded with the embedded facts or repo-local sources, move it to non-blocking review/archive with reason and lineage rather than fabricating clean data.

## Mandatory cleanup rules for RUN 4

- Fix invalid source_indexes/field_sources in Opel Vectra, ORA 07, Peugeot 205, Peugeot 206, Peugeot 208, Peugeot 308 and Peugeot 408.
- Do not leave duplicate global-reference-only profiles as separate clean profiles when an IL-confirmed canonical profile exists: Peugeot 107 and Peugeot 301 must be merged; Peugeot 408 global-reference-only must merge/archive into the canonical IL Peugeot 408 profile.
- ORA 07 408 hp/AWD GT must not remain clean unless repo-local Israeli evidence proves sale; Israeli sources support 204 hp FWD rows.
- ORA Funky Cat should be aligned with current official ORA 03/Funky Cat naming and 171 hp FWD EV schema.
- Peugeot 4007 must not remain current with `year_end=null`; it is historical unless exact local evidence says otherwise.
- Current Peugeot 208/308/408 rows require current local evidence; do not extend historical rows by guessing.
- EV rows must use valid EV schema: `engine_displacement_l=null`, correct fuel_type, drivetrain, and repo-valid single_speed/direct_drive transmission.

## Variant-level instructions


---

## MODEL PROFILE: IL-confirmed|Opel|Vectra

PROFILE ACTION: FIX + MERGE/ALIAS

WEB-VALIDATED FACT: Israeli/local sources in the profile support Vectra as a historical Israeli model: 1996-2001 Vectra B 1.8/2.0 petrol and 2002-2008 Vectra C 2.2/GTS petrol. It is not current. This IL-confirmed profile overlaps the adjacent IL-likely Vectra handled in RUN3 and must be canonical.

SOURCE: Repo-local Auto.co.il Vectra 2002-2008 source index 0; repo-local iCar Vectra 1996-2002 source index 1.

TARGET VALUE / PROFILE ACTION: Keep as canonical IL-confirmed Opel Vectra historical profile; merge/archive adjacent IL-likely Vectra with alias/lineage. Replace invalid source_indexes [2011]/[2012] with valid local source indexes: 1996-2001 rows -> [1]; 2002-2008 rows -> [0].

### VARIANT 1 — Opel Vectra row 1

MODEL: IL-confirmed|Opel|Vectra

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.8L", "engine_displacement_l": 1.8, "horsepower_hp": 115, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1996, "year_end": 2001, "support_level": "direct", "source_indexes": [2012]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.8L` / `1.8` / `115` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1996-2001` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli/local sources in the profile support Vectra as a historical Israeli model: 1996-2001 Vectra B 1.8/2.0 petrol and 2002-2008 Vectra C 2.2/GTS petrol. It is not current. This IL-confirmed profile overlaps the adjacent IL-likely Vectra handled in RUN3 and must be canonical.

SOURCE:
Repo-local Auto.co.il Vectra 2002-2008 source index 0; repo-local iCar Vectra 1996-2002 source index 1.

TARGET VALUE:
Keep as canonical IL-confirmed Opel Vectra historical profile; merge/archive adjacent IL-likely Vectra with alias/lineage. Replace invalid source_indexes [2011]/[2012] with valid local source indexes: 1996-2001 rows -> [1]; 2002-2008 rows -> [0].

ACTION: FIX + MERGE/ALIAS

### VARIANT 2 — Opel Vectra row 2

MODEL: IL-confirmed|Opel|Vectra

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "2.0L", "engine_displacement_l": 2.0, "horsepower_hp": 136, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1996, "year_end": 2001, "support_level": "direct", "source_indexes": [2012]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L` / `2.0` / `136` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1996-2001` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli/local sources in the profile support Vectra as a historical Israeli model: 1996-2001 Vectra B 1.8/2.0 petrol and 2002-2008 Vectra C 2.2/GTS petrol. It is not current. This IL-confirmed profile overlaps the adjacent IL-likely Vectra handled in RUN3 and must be canonical.

SOURCE:
Repo-local Auto.co.il Vectra 2002-2008 source index 0; repo-local iCar Vectra 1996-2002 source index 1.

TARGET VALUE:
Keep as canonical IL-confirmed Opel Vectra historical profile; merge/archive adjacent IL-likely Vectra with alias/lineage. Replace invalid source_indexes [2011]/[2012] with valid local source indexes: 1996-2001 rows -> [1]; 2002-2008 rows -> [0].

ACTION: FIX + MERGE/ALIAS

### VARIANT 3 — Opel Vectra row 3

MODEL: IL-confirmed|Opel|Vectra

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "2.2L", "engine_displacement_l": 2.2, "horsepower_hp": 147, "transmission": "5-speed automatic", "drivetrain": "FWD", "year_start": 2002, "year_end": 2008, "support_level": "direct", "source_indexes": [2011]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.2L` / `2.2` / `147` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2002-2008` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli/local sources in the profile support Vectra as a historical Israeli model: 1996-2001 Vectra B 1.8/2.0 petrol and 2002-2008 Vectra C 2.2/GTS petrol. It is not current. This IL-confirmed profile overlaps the adjacent IL-likely Vectra handled in RUN3 and must be canonical.

SOURCE:
Repo-local Auto.co.il Vectra 2002-2008 source index 0; repo-local iCar Vectra 1996-2002 source index 1.

TARGET VALUE:
Keep as canonical IL-confirmed Opel Vectra historical profile; merge/archive adjacent IL-likely Vectra with alias/lineage. Replace invalid source_indexes [2011]/[2012] with valid local source indexes: 1996-2001 rows -> [1]; 2002-2008 rows -> [0].

ACTION: FIX + MERGE/ALIAS

### VARIANT 4 — Opel Vectra row 4

MODEL: IL-confirmed|Opel|Vectra

CURRENT VALUE:
```json
{"version_or_trim": "GTS", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "2.2L", "engine_displacement_l": 2.2, "horsepower_hp": 147, "transmission": "5-speed automatic", "drivetrain": "FWD", "year_start": 2003, "year_end": 2008, "support_level": "direct", "source_indexes": [2011]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `GTS` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.2L` / `2.2` / `147` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2003-2008` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli/local sources in the profile support Vectra as a historical Israeli model: 1996-2001 Vectra B 1.8/2.0 petrol and 2002-2008 Vectra C 2.2/GTS petrol. It is not current. This IL-confirmed profile overlaps the adjacent IL-likely Vectra handled in RUN3 and must be canonical.

SOURCE:
Repo-local Auto.co.il Vectra 2002-2008 source index 0; repo-local iCar Vectra 1996-2002 source index 1.

TARGET VALUE:
Keep as canonical IL-confirmed Opel Vectra historical profile; merge/archive adjacent IL-likely Vectra with alias/lineage. Replace invalid source_indexes [2011]/[2012] with valid local source indexes: 1996-2001 rows -> [1]; 2002-2008 rows -> [0].

ACTION: FIX + MERGE/ALIAS

---

## MODEL PROFILE: IL-likely|Opel|Vivaro

PROFILE ACTION: FIX / MOVE TO REVIEW IF NOT GROUNDABLE

WEB-VALIDATED FACT: Israeli Auto/iCar sources support Vivaro as a commercial van line: 2008-2014 2.0 diesel, 2015-2019 1.6 diesel, and 2020-2024 2.0 diesel; e-Vivaro is an EV van and must use EV schema. It should not be currentized beyond local evidence.

SOURCE: Repo-local Auto.co.il/iCar Vivaro sources; web check also found Auto.co.il Vivaro describes 1.6 diesel 90/115/120/140 hp and one imported version; Opel Drive specs show 2.0 diesel 145 hp but is not sufficient alone for Israeli clean current.

TARGET VALUE / PROFILE ACTION: Keep as Israeli historical/commercial profile only where source_indexes are valid. If profile remains IL-likely, promote/merge to IL-confirmed only when repo-local local source policy allows; otherwise mark profile as review/non-blocking. EV row must keep engine_displacement_l=null and single_speed/direct_drive.

### VARIANT 5 — Opel Vivaro row 1

MODEL: IL-likely|Opel|Vivaro

CURRENT VALUE:
```json
{"version_or_trim": "Edition", "body_type": "Van", "fuel_type": "diesel", "engine": "2.0L turbo", "engine_displacement_l": 2.0, "horsepower_hp": 177, "transmission": "8-speed automatic", "drivetrain": "FWD", "year_start": 2020, "year_end": 2024, "support_level": "direct", "source_indexes": [0, 1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Edition` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Van` — must match Israeli body style/source.
- fuel_type: `diesel` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L turbo` / `2.0` / `177` — must match embedded fact and repo-local source.
- transmission/drivetrain: `8-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2020-2024` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli Auto/iCar sources support Vivaro as a commercial van line: 2008-2014 2.0 diesel, 2015-2019 1.6 diesel, and 2020-2024 2.0 diesel; e-Vivaro is an EV van and must use EV schema. It should not be currentized beyond local evidence.

SOURCE:
Repo-local Auto.co.il/iCar Vivaro sources; web check also found Auto.co.il Vivaro describes 1.6 diesel 90/115/120/140 hp and one imported version; Opel Drive specs show 2.0 diesel 145 hp but is not sufficient alone for Israeli clean current.

TARGET VALUE:
Keep as Israeli historical/commercial profile only where source_indexes are valid. If profile remains IL-likely, promote/merge to IL-confirmed only when repo-local local source policy allows; otherwise mark profile as review/non-blocking. EV row must keep engine_displacement_l=null and single_speed/direct_drive.

ACTION: FIX / MOVE TO REVIEW IF NOT GROUNDABLE

### VARIANT 6 — Opel Vivaro row 2

MODEL: IL-likely|Opel|Vivaro

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Van", "fuel_type": "diesel", "engine": "2.0L turbo", "engine_displacement_l": 2.0, "horsepower_hp": 114, "transmission": "6-speed manual", "drivetrain": "FWD", "year_start": 2008, "year_end": 2014, "support_level": "direct", "source_indexes": [3, 4]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Van` — must match Israeli body style/source.
- fuel_type: `diesel` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L turbo` / `2.0` / `114` — must match embedded fact and repo-local source.
- transmission/drivetrain: `6-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2008-2014` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli Auto/iCar sources support Vivaro as a commercial van line: 2008-2014 2.0 diesel, 2015-2019 1.6 diesel, and 2020-2024 2.0 diesel; e-Vivaro is an EV van and must use EV schema. It should not be currentized beyond local evidence.

SOURCE:
Repo-local Auto.co.il/iCar Vivaro sources; web check also found Auto.co.il Vivaro describes 1.6 diesel 90/115/120/140 hp and one imported version; Opel Drive specs show 2.0 diesel 145 hp but is not sufficient alone for Israeli clean current.

TARGET VALUE:
Keep as Israeli historical/commercial profile only where source_indexes are valid. If profile remains IL-likely, promote/merge to IL-confirmed only when repo-local local source policy allows; otherwise mark profile as review/non-blocking. EV row must keep engine_displacement_l=null and single_speed/direct_drive.

ACTION: FIX / MOVE TO REVIEW IF NOT GROUNDABLE

### VARIANT 7 — Opel Vivaro row 3

MODEL: IL-likely|Opel|Vivaro

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Van", "fuel_type": "diesel", "engine": "1.6L turbo", "engine_displacement_l": 1.6, "horsepower_hp": 115, "transmission": "6-speed manual", "drivetrain": "FWD", "year_start": 2015, "year_end": 2019, "support_level": "direct", "source_indexes": [5, 6]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Van` — must match Israeli body style/source.
- fuel_type: `diesel` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L turbo` / `1.6` / `115` — must match embedded fact and repo-local source.
- transmission/drivetrain: `6-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2015-2019` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli Auto/iCar sources support Vivaro as a commercial van line: 2008-2014 2.0 diesel, 2015-2019 1.6 diesel, and 2020-2024 2.0 diesel; e-Vivaro is an EV van and must use EV schema. It should not be currentized beyond local evidence.

SOURCE:
Repo-local Auto.co.il/iCar Vivaro sources; web check also found Auto.co.il Vivaro describes 1.6 diesel 90/115/120/140 hp and one imported version; Opel Drive specs show 2.0 diesel 145 hp but is not sufficient alone for Israeli clean current.

TARGET VALUE:
Keep as Israeli historical/commercial profile only where source_indexes are valid. If profile remains IL-likely, promote/merge to IL-confirmed only when repo-local local source policy allows; otherwise mark profile as review/non-blocking. EV row must keep engine_displacement_l=null and single_speed/direct_drive.

ACTION: FIX / MOVE TO REVIEW IF NOT GROUNDABLE

### VARIANT 8 — Opel Vivaro row 4

MODEL: IL-likely|Opel|Vivaro

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Van", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 136, "transmission": "single_speed", "drivetrain": "FWD", "year_start": 2022, "year_end": 2024, "support_level": "direct", "source_indexes": [7, 8]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Van` — must match Israeli body style/source.
- fuel_type: `electric` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `electric` / `None` / `136` — must match embedded fact and repo-local source.
- transmission/drivetrain: `single_speed` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2022-2024` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli Auto/iCar sources support Vivaro as a commercial van line: 2008-2014 2.0 diesel, 2015-2019 1.6 diesel, and 2020-2024 2.0 diesel; e-Vivaro is an EV van and must use EV schema. It should not be currentized beyond local evidence.

SOURCE:
Repo-local Auto.co.il/iCar Vivaro sources; web check also found Auto.co.il Vivaro describes 1.6 diesel 90/115/120/140 hp and one imported version; Opel Drive specs show 2.0 diesel 145 hp but is not sufficient alone for Israeli clean current.

TARGET VALUE:
Keep as Israeli historical/commercial profile only where source_indexes are valid. If profile remains IL-likely, promote/merge to IL-confirmed only when repo-local local source policy allows; otherwise mark profile as review/non-blocking. EV row must keep engine_displacement_l=null and single_speed/direct_drive.

ACTION: FIX / MOVE TO REVIEW IF NOT GROUNDABLE

---

## MODEL PROFILE: IL-confirmed|Ora|07

PROFILE ACTION: FIX + MOVE TO REVIEW/ARCHIVE 408hp GT

WEB-VALIDATED FACT: Official ORA Israel page and Israeli Auto/Carzone/Cartube sources support ORA 07 in Israel with 204 hp FWD. Auto.co.il explicitly notes the dual-motor ~400 hp/AWD version is offered globally, while Israel receives one 204 hp motor; Cartube lists 2026 Pure/Pro+ 204 hp rows.

SOURCE: https://ora-israel.co.il/model/ora-07/ ; Auto.co.il ORA 07; Cartube ORA 07 price/spec page; Carzone ORA 07.

TARGET VALUE / PROFILE ACTION: Keep/FIX only 204 hp FWD Israeli rows (Pure/Pro+ if repo schema uses trim rows). Move GT/AWD/408 hp row to non-blocking review/archive unless repo-local official Israeli evidence proves sale. Fix invalid source index 2 to valid local indexes [0,1] or add valid source entry.

### VARIANT 9 — Ora 07 row 1

MODEL: IL-confirmed|Ora|07

CURRENT VALUE:
```json
{"version_or_trim": "Pure", "body_type": "Sedan", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 204, "transmission": "single_speed", "drivetrain": "FWD", "year_start": 2024, "year_end": null, "support_level": "direct", "source_indexes": [1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Pure` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `electric` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `electric` / `None` / `204` — must match embedded fact and repo-local source.
- transmission/drivetrain: `single_speed` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2024-None` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Official ORA Israel page and Israeli Auto/Carzone/Cartube sources support ORA 07 in Israel with 204 hp FWD. Auto.co.il explicitly notes the dual-motor ~400 hp/AWD version is offered globally, while Israel receives one 204 hp motor; Cartube lists 2026 Pure/Pro+ 204 hp rows.

SOURCE:
https://ora-israel.co.il/model/ora-07/ ; Auto.co.il ORA 07; Cartube ORA 07 price/spec page; Carzone ORA 07.

TARGET VALUE:
Keep/FIX only 204 hp FWD Israeli rows (Pure/Pro+ if repo schema uses trim rows). Move GT/AWD/408 hp row to non-blocking review/archive unless repo-local official Israeli evidence proves sale. Fix invalid source index 2 to valid local indexes [0,1] or add valid source entry.

ACTION: FIX + MOVE TO REVIEW/ARCHIVE 408hp GT

### VARIANT 10 — Ora 07 row 2

MODEL: IL-confirmed|Ora|07

CURRENT VALUE:
```json
{"version_or_trim": "GT", "body_type": "Sedan", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 408, "transmission": "single_speed", "drivetrain": "AWD", "year_start": 2024, "year_end": null, "support_level": "direct", "source_indexes": [1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `GT` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `electric` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `electric` / `None` / `408` — must match embedded fact and repo-local source.
- transmission/drivetrain: `single_speed` / `AWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2024-None` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Official ORA Israel page and Israeli Auto/Carzone/Cartube sources support ORA 07 in Israel with 204 hp FWD. Auto.co.il explicitly notes the dual-motor ~400 hp/AWD version is offered globally, while Israel receives one 204 hp motor; Cartube lists 2026 Pure/Pro+ 204 hp rows.

SOURCE:
https://ora-israel.co.il/model/ora-07/ ; Auto.co.il ORA 07; Cartube ORA 07 price/spec page; Carzone ORA 07.

TARGET VALUE:
Keep/FIX only 204 hp FWD Israeli rows (Pure/Pro+ if repo schema uses trim rows). Move GT/AWD/408 hp row to non-blocking review/archive unless repo-local official Israeli evidence proves sale. Fix invalid source index 2 to valid local indexes [0,1] or add valid source entry.

ACTION: FIX + MOVE TO REVIEW/ARCHIVE 408hp GT

---

## MODEL PROFILE: IL-confirmed|Ora|Funky Cat

PROFILE ACTION: FIX + ALIAS/LINEAGE

WEB-VALIDATED FACT: Official ORA Israel currently presents ORA 03 / Funky Cat with Classic, Design and +Pro trims, 63.13 kWh, 171 hp, FWD and 400 km range; Auto.co.il also supports 171 hp FWD Israeli ORA 03/Funky Cat.

SOURCE: https://ora-israel.co.il/model/ora-03/ ; Auto.co.il ORA Funky Cat; repo-local Cartube/iCar sources.

TARGET VALUE / PROFILE ACTION: Do not leave as closed 2023-2024 if official local source shows current ORA 03/Funky Cat. Canonicalize naming to ORA 03 with alias Funky Cat if project policy prefers current official name; otherwise keep Funky Cat with alias ORA 03. Add/normalize Classic/Design/+Pro trim rows if repo policy requires trim granularity. EV schema must stay displacement null/single_speed/FWD.

### VARIANT 11 — Ora Funky Cat row 1

MODEL: IL-confirmed|Ora|Funky Cat

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 171, "transmission": "single_speed", "drivetrain": "FWD", "year_start": 2023, "year_end": 2024, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `electric` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `electric` / `None` / `171` — must match embedded fact and repo-local source.
- transmission/drivetrain: `single_speed` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2023-2024` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Official ORA Israel currently presents ORA 03 / Funky Cat with Classic, Design and +Pro trims, 63.13 kWh, 171 hp, FWD and 400 km range; Auto.co.il also supports 171 hp FWD Israeli ORA 03/Funky Cat.

SOURCE:
https://ora-israel.co.il/model/ora-03/ ; Auto.co.il ORA Funky Cat; repo-local Cartube/iCar sources.

TARGET VALUE:
Do not leave as closed 2023-2024 if official local source shows current ORA 03/Funky Cat. Canonicalize naming to ORA 03 with alias Funky Cat if project policy prefers current official name; otherwise keep Funky Cat with alias ORA 03. Add/normalize Classic/Design/+Pro trim rows if repo policy requires trim granularity. EV schema must stay displacement null/single_speed/FWD.

ACTION: FIX + ALIAS/LINEAGE

---

## MODEL PROFILE: IL-confirmed|Peugeot|106

PROFILE ACTION: KEEP

WEB-VALIDATED FACT: Israeli historical price/spec sources support Peugeot 106 1993-2003 with XR/XS/Rallye/XSi/GTI variants. This is historical only.

SOURCE: Repo-local iCar/Auto sources.

TARGET VALUE / PROFILE ACTION: Keep historical rows if source indexes remain valid; do not currentize; ensure trim names and body/fuel/engine/hp/transmission/drivetrain fields remain grounded.

### VARIANT 12 — Peugeot 106 row 1

MODEL: IL-confirmed|Peugeot|106

CURRENT VALUE:
```json
{"version_or_trim": "XR", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.4L 8v", "engine_displacement_l": 1.4, "horsepower_hp": 75, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1993, "year_end": 2003, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XR` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.4L 8v` / `1.4` / `75` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1993-2003` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical price/spec sources support Peugeot 106 1993-2003 with XR/XS/Rallye/XSi/GTI variants. This is historical only.

SOURCE:
Repo-local iCar/Auto sources.

TARGET VALUE:
Keep historical rows if source indexes remain valid; do not currentize; ensure trim names and body/fuel/engine/hp/transmission/drivetrain fields remain grounded.

ACTION: KEEP

### VARIANT 13 — Peugeot 106 row 2

MODEL: IL-confirmed|Peugeot|106

CURRENT VALUE:
```json
{"version_or_trim": "XR", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.4L 8v", "engine_displacement_l": 1.4, "horsepower_hp": 75, "transmission": "3-speed automatic", "drivetrain": "FWD", "year_start": 1993, "year_end": 2003, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XR` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.4L 8v` / `1.4` / `75` — must match embedded fact and repo-local source.
- transmission/drivetrain: `3-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1993-2003` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical price/spec sources support Peugeot 106 1993-2003 with XR/XS/Rallye/XSi/GTI variants. This is historical only.

SOURCE:
Repo-local iCar/Auto sources.

TARGET VALUE:
Keep historical rows if source indexes remain valid; do not currentize; ensure trim names and body/fuel/engine/hp/transmission/drivetrain fields remain grounded.

ACTION: KEEP

### VARIANT 14 — Peugeot 106 row 3

MODEL: IL-confirmed|Peugeot|106

CURRENT VALUE:
```json
{"version_or_trim": "XS", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.4L 8v", "engine_displacement_l": 1.4, "horsepower_hp": 75, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1993, "year_end": 2003, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XS` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.4L 8v` / `1.4` / `75` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1993-2003` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical price/spec sources support Peugeot 106 1993-2003 with XR/XS/Rallye/XSi/GTI variants. This is historical only.

SOURCE:
Repo-local iCar/Auto sources.

TARGET VALUE:
Keep historical rows if source indexes remain valid; do not currentize; ensure trim names and body/fuel/engine/hp/transmission/drivetrain fields remain grounded.

ACTION: KEEP

### VARIANT 15 — Peugeot 106 row 4

MODEL: IL-confirmed|Peugeot|106

CURRENT VALUE:
```json
{"version_or_trim": "Rallye", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.3L 8v", "engine_displacement_l": 1.3, "horsepower_hp": 100, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1994, "year_end": 1996, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Rallye` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.3L 8v` / `1.3` / `100` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1994-1996` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical price/spec sources support Peugeot 106 1993-2003 with XR/XS/Rallye/XSi/GTI variants. This is historical only.

SOURCE:
Repo-local iCar/Auto sources.

TARGET VALUE:
Keep historical rows if source indexes remain valid; do not currentize; ensure trim names and body/fuel/engine/hp/transmission/drivetrain fields remain grounded.

ACTION: KEEP

### VARIANT 16 — Peugeot 106 row 5

MODEL: IL-confirmed|Peugeot|106

CURRENT VALUE:
```json
{"version_or_trim": "XSi", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L 8v", "engine_displacement_l": 1.6, "horsepower_hp": 105, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1994, "year_end": 1996, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XSi` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L 8v` / `1.6` / `105` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1994-1996` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical price/spec sources support Peugeot 106 1993-2003 with XR/XS/Rallye/XSi/GTI variants. This is historical only.

SOURCE:
Repo-local iCar/Auto sources.

TARGET VALUE:
Keep historical rows if source indexes remain valid; do not currentize; ensure trim names and body/fuel/engine/hp/transmission/drivetrain fields remain grounded.

ACTION: KEEP

### VARIANT 17 — Peugeot 106 row 6

MODEL: IL-confirmed|Peugeot|106

CURRENT VALUE:
```json
{"version_or_trim": "Rallye", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L 8v", "engine_displacement_l": 1.6, "horsepower_hp": 103, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1997, "year_end": 1999, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Rallye` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L 8v` / `1.6` / `103` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1997-1999` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical price/spec sources support Peugeot 106 1993-2003 with XR/XS/Rallye/XSi/GTI variants. This is historical only.

SOURCE:
Repo-local iCar/Auto sources.

TARGET VALUE:
Keep historical rows if source indexes remain valid; do not currentize; ensure trim names and body/fuel/engine/hp/transmission/drivetrain fields remain grounded.

ACTION: KEEP

### VARIANT 18 — Peugeot 106 row 7

MODEL: IL-confirmed|Peugeot|106

CURRENT VALUE:
```json
{"version_or_trim": "GTI", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L 16v", "engine_displacement_l": 1.6, "horsepower_hp": 120, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1997, "year_end": 2003, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `GTI` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L 16v` / `1.6` / `120` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1997-2003` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical price/spec sources support Peugeot 106 1993-2003 with XR/XS/Rallye/XSi/GTI variants. This is historical only.

SOURCE:
Repo-local iCar/Auto sources.

TARGET VALUE:
Keep historical rows if source indexes remain valid; do not currentize; ensure trim names and body/fuel/engine/hp/transmission/drivetrain fields remain grounded.

ACTION: KEEP

---

## MODEL PROFILE: global-reference-only|Peugeot|107

PROFILE ACTION: MERGE/DELETE DUPLICATE + FIX TRANSMISSION IF SCHEMA SUPPORTS

WEB-VALIDATED FACT: Israeli sources support Peugeot 107 2009-2014 1.0L 68 hp FWD. The global-reference-only and IL-confirmed profiles are duplicates. Automatic-like 107/108 transmissions are often robotic/2-Tronic, not a conventional torque-converter automatic.

SOURCE: Repo-local iCar/Auto Peugeot 107 sources.

TARGET VALUE / PROFILE ACTION: Canonical profile must be IL-confirmed Peugeot 107. Delete/merge global-reference-only duplicate with lineage. In canonical rows, keep 1.0L 68 hp, FWD, 2009-2014; set transmission to repo-valid robotized/automated_manual/5-speed robotized if schema supports, otherwise retain 5-speed automatic only with explicit note.

### VARIANT 19 — Peugeot 107 row 1

MODEL: global-reference-only|Peugeot|107

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.0L", "engine_displacement_l": 1.0, "horsepower_hp": 68, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2009, "year_end": 2014, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.0L` / `1.0` / `68` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2009-2014` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 107 2009-2014 1.0L 68 hp FWD. The global-reference-only and IL-confirmed profiles are duplicates. Automatic-like 107/108 transmissions are often robotic/2-Tronic, not a conventional torque-converter automatic.

SOURCE:
Repo-local iCar/Auto Peugeot 107 sources.

TARGET VALUE:
Canonical profile must be IL-confirmed Peugeot 107. Delete/merge global-reference-only duplicate with lineage. In canonical rows, keep 1.0L 68 hp, FWD, 2009-2014; set transmission to repo-valid robotized/automated_manual/5-speed robotized if schema supports, otherwise retain 5-speed automatic only with explicit note.

ACTION: MERGE/DELETE DUPLICATE + FIX TRANSMISSION IF SCHEMA SUPPORTS

### VARIANT 20 — Peugeot 107 row 2

MODEL: global-reference-only|Peugeot|107

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.0L", "engine_displacement_l": 1.0, "horsepower_hp": 68, "transmission": "5-speed automatic", "drivetrain": "FWD", "year_start": 2009, "year_end": 2014, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.0L` / `1.0` / `68` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2009-2014` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 107 2009-2014 1.0L 68 hp FWD. The global-reference-only and IL-confirmed profiles are duplicates. Automatic-like 107/108 transmissions are often robotic/2-Tronic, not a conventional torque-converter automatic.

SOURCE:
Repo-local iCar/Auto Peugeot 107 sources.

TARGET VALUE:
Canonical profile must be IL-confirmed Peugeot 107. Delete/merge global-reference-only duplicate with lineage. In canonical rows, keep 1.0L 68 hp, FWD, 2009-2014; set transmission to repo-valid robotized/automated_manual/5-speed robotized if schema supports, otherwise retain 5-speed automatic only with explicit note.

ACTION: MERGE/DELETE DUPLICATE + FIX TRANSMISSION IF SCHEMA SUPPORTS

---

## MODEL PROFILE: IL-confirmed|Peugeot|107

PROFILE ACTION: MERGE/DELETE DUPLICATE + FIX TRANSMISSION IF SCHEMA SUPPORTS

WEB-VALIDATED FACT: Israeli sources support Peugeot 107 2009-2014 1.0L 68 hp FWD. The global-reference-only and IL-confirmed profiles are duplicates. Automatic-like 107/108 transmissions are often robotic/2-Tronic, not a conventional torque-converter automatic.

SOURCE: Repo-local iCar/Auto Peugeot 107 sources.

TARGET VALUE / PROFILE ACTION: Canonical profile must be IL-confirmed Peugeot 107. Delete/merge global-reference-only duplicate with lineage. In canonical rows, keep 1.0L 68 hp, FWD, 2009-2014; set transmission to repo-valid robotized/automated_manual/5-speed robotized if schema supports, otherwise retain 5-speed automatic only with explicit note.

### VARIANT 21 — Peugeot 107 row 1

MODEL: IL-confirmed|Peugeot|107

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.0L", "engine_displacement_l": 1.0, "horsepower_hp": 68, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2009, "year_end": 2014, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.0L` / `1.0` / `68` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2009-2014` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 107 2009-2014 1.0L 68 hp FWD. The global-reference-only and IL-confirmed profiles are duplicates. Automatic-like 107/108 transmissions are often robotic/2-Tronic, not a conventional torque-converter automatic.

SOURCE:
Repo-local iCar/Auto Peugeot 107 sources.

TARGET VALUE:
Canonical profile must be IL-confirmed Peugeot 107. Delete/merge global-reference-only duplicate with lineage. In canonical rows, keep 1.0L 68 hp, FWD, 2009-2014; set transmission to repo-valid robotized/automated_manual/5-speed robotized if schema supports, otherwise retain 5-speed automatic only with explicit note.

ACTION: MERGE/DELETE DUPLICATE + FIX TRANSMISSION IF SCHEMA SUPPORTS

### VARIANT 22 — Peugeot 107 row 2

MODEL: IL-confirmed|Peugeot|107

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.0L", "engine_displacement_l": 1.0, "horsepower_hp": 68, "transmission": "5-speed automatic", "drivetrain": "FWD", "year_start": 2009, "year_end": 2014, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.0L` / `1.0` / `68` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2009-2014` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 107 2009-2014 1.0L 68 hp FWD. The global-reference-only and IL-confirmed profiles are duplicates. Automatic-like 107/108 transmissions are often robotic/2-Tronic, not a conventional torque-converter automatic.

SOURCE:
Repo-local iCar/Auto Peugeot 107 sources.

TARGET VALUE:
Canonical profile must be IL-confirmed Peugeot 107. Delete/merge global-reference-only duplicate with lineage. In canonical rows, keep 1.0L 68 hp, FWD, 2009-2014; set transmission to repo-valid robotized/automated_manual/5-speed robotized if schema supports, otherwise retain 5-speed automatic only with explicit note.

ACTION: MERGE/DELETE DUPLICATE + FIX TRANSMISSION IF SCHEMA SUPPORTS

---

## MODEL PROFILE: IL-confirmed|Peugeot|108

PROFILE ACTION: FIX / KEEP HISTORICAL

WEB-VALIDATED FACT: Israeli launch/update sources support Peugeot 108 2014-2021 with 1.0 69/72 hp and 1.2 82 hp rows. The automated gearbox should be represented as robotic/ETG/2-Tronic if schema supports.

SOURCE: Repo-local Cartube/iCar Peugeot 108 sources.

TARGET VALUE / PROFILE ACTION: Keep as historical; do not currentize. Fix 5-speed automatic to repo-valid robotized/automated_manual where source/policy supports.

### VARIANT 23 — Peugeot 108 row 1

MODEL: IL-confirmed|Peugeot|108

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.0L", "engine_displacement_l": 1.0, "horsepower_hp": 69, "transmission": "5-speed automatic", "drivetrain": "FWD", "year_start": 2014, "year_end": 2018, "support_level": "indirect", "source_indexes": [0, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.0L` / `1.0` / `69` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2014-2018` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli launch/update sources support Peugeot 108 2014-2021 with 1.0 69/72 hp and 1.2 82 hp rows. The automated gearbox should be represented as robotic/ETG/2-Tronic if schema supports.

SOURCE:
Repo-local Cartube/iCar Peugeot 108 sources.

TARGET VALUE:
Keep as historical; do not currentize. Fix 5-speed automatic to repo-valid robotized/automated_manual where source/policy supports.

ACTION: FIX / KEEP HISTORICAL

### VARIANT 24 — Peugeot 108 row 2

MODEL: IL-confirmed|Peugeot|108

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.2L", "engine_displacement_l": 1.2, "horsepower_hp": 82, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2014, "year_end": 2018, "support_level": "indirect", "source_indexes": [0, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L` / `1.2` / `82` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2014-2018` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli launch/update sources support Peugeot 108 2014-2021 with 1.0 69/72 hp and 1.2 82 hp rows. The automated gearbox should be represented as robotic/ETG/2-Tronic if schema supports.

SOURCE:
Repo-local Cartube/iCar Peugeot 108 sources.

TARGET VALUE:
Keep as historical; do not currentize. Fix 5-speed automatic to repo-valid robotized/automated_manual where source/policy supports.

ACTION: FIX / KEEP HISTORICAL

### VARIANT 25 — Peugeot 108 row 3

MODEL: IL-confirmed|Peugeot|108

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.0L", "engine_displacement_l": 1.0, "horsepower_hp": 72, "transmission": "5-speed automatic", "drivetrain": "FWD", "year_start": 2018, "year_end": 2021, "support_level": "indirect", "source_indexes": [1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.0L` / `1.0` / `72` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2018-2021` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli launch/update sources support Peugeot 108 2014-2021 with 1.0 69/72 hp and 1.2 82 hp rows. The automated gearbox should be represented as robotic/ETG/2-Tronic if schema supports.

SOURCE:
Repo-local Cartube/iCar Peugeot 108 sources.

TARGET VALUE:
Keep as historical; do not currentize. Fix 5-speed automatic to repo-valid robotized/automated_manual where source/policy supports.

ACTION: FIX / KEEP HISTORICAL

---

## MODEL PROFILE: IL-confirmed|Peugeot|205

PROFILE ACTION: FIX SOURCE INDEXES

WEB-VALIDATED FACT: Historical Israeli sources support Peugeot 205 variants including 1.4 Forever/CJ, GTI 1.9, and convertible CJ. Current source indexes are invalid legacy IDs.

SOURCE: Repo-local Auto/Yad2/KML/Gear sources indexes 0-3.

TARGET VALUE / PROFILE ACTION: Keep historical only. Replace invalid source_indexes [2139,2140,2141,2142] with valid source indexes from the local profile; field_sources must be rebuilt accordingly.

### VARIANT 26 — Peugeot 205 row 1

MODEL: IL-confirmed|Peugeot|205

CURRENT VALUE:
```json
{"version_or_trim": "Forever", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.4L", "engine_displacement_l": 1.4, "horsepower_hp": 75, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1990, "year_end": 1998, "support_level": "direct", "source_indexes": [2139, 2140, 2141]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Forever` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.4L` / `1.4` / `75` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1990-1998` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Historical Israeli sources support Peugeot 205 variants including 1.4 Forever/CJ, GTI 1.9, and convertible CJ. Current source indexes are invalid legacy IDs.

SOURCE:
Repo-local Auto/Yad2/KML/Gear sources indexes 0-3.

TARGET VALUE:
Keep historical only. Replace invalid source_indexes [2139,2140,2141,2142] with valid source indexes from the local profile; field_sources must be rebuilt accordingly.

ACTION: FIX SOURCE INDEXES

### VARIANT 27 — Peugeot 205 row 2

MODEL: IL-confirmed|Peugeot|205

CURRENT VALUE:
```json
{"version_or_trim": "Forever", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.4L", "engine_displacement_l": 1.4, "horsepower_hp": 75, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1990, "year_end": 1998, "support_level": "direct", "source_indexes": [2139, 2140, 2141]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Forever` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.4L` / `1.4` / `75` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1990-1998` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Historical Israeli sources support Peugeot 205 variants including 1.4 Forever/CJ, GTI 1.9, and convertible CJ. Current source indexes are invalid legacy IDs.

SOURCE:
Repo-local Auto/Yad2/KML/Gear sources indexes 0-3.

TARGET VALUE:
Keep historical only. Replace invalid source_indexes [2139,2140,2141,2142] with valid source indexes from the local profile; field_sources must be rebuilt accordingly.

ACTION: FIX SOURCE INDEXES

### VARIANT 28 — Peugeot 205 row 3

MODEL: IL-confirmed|Peugeot|205

CURRENT VALUE:
```json
{"version_or_trim": "GTI", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.9L", "engine_displacement_l": 1.9, "horsepower_hp": 122, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1990, "year_end": 1994, "support_level": "direct", "source_indexes": [2139, 2140, 2141]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `GTI` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.9L` / `1.9` / `122` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1990-1994` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Historical Israeli sources support Peugeot 205 variants including 1.4 Forever/CJ, GTI 1.9, and convertible CJ. Current source indexes are invalid legacy IDs.

SOURCE:
Repo-local Auto/Yad2/KML/Gear sources indexes 0-3.

TARGET VALUE:
Keep historical only. Replace invalid source_indexes [2139,2140,2141,2142] with valid source indexes from the local profile; field_sources must be rebuilt accordingly.

ACTION: FIX SOURCE INDEXES

### VARIANT 29 — Peugeot 205 row 4

MODEL: IL-confirmed|Peugeot|205

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 89, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1990, "year_end": 1994, "support_level": "direct", "source_indexes": [2139, 2140, 2141]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `89` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1990-1994` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Historical Israeli sources support Peugeot 205 variants including 1.4 Forever/CJ, GTI 1.9, and convertible CJ. Current source indexes are invalid legacy IDs.

SOURCE:
Repo-local Auto/Yad2/KML/Gear sources indexes 0-3.

TARGET VALUE:
Keep historical only. Replace invalid source_indexes [2139,2140,2141,2142] with valid source indexes from the local profile; field_sources must be rebuilt accordingly.

ACTION: FIX SOURCE INDEXES

### VARIANT 30 — Peugeot 205 row 5

MODEL: IL-confirmed|Peugeot|205

CURRENT VALUE:
```json
{"version_or_trim": "CJ", "body_type": "Convertible", "fuel_type": "petrol", "engine": "1.4L", "engine_displacement_l": 1.4, "horsepower_hp": 75, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1990, "year_end": 1995, "support_level": "direct", "source_indexes": [2139, 2140, 2141, 2142]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `CJ` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Convertible` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.4L` / `1.4` / `75` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1990-1995` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Historical Israeli sources support Peugeot 205 variants including 1.4 Forever/CJ, GTI 1.9, and convertible CJ. Current source indexes are invalid legacy IDs.

SOURCE:
Repo-local Auto/Yad2/KML/Gear sources indexes 0-3.

TARGET VALUE:
Keep historical only. Replace invalid source_indexes [2139,2140,2141,2142] with valid source indexes from the local profile; field_sources must be rebuilt accordingly.

ACTION: FIX SOURCE INDEXES

---

## MODEL PROFILE: IL-confirmed|Peugeot|206

PROFILE ACTION: FIX SOURCE INDEXES

WEB-VALIDATED FACT: Israeli sources support Peugeot 206, 206 CC, 206 Plus and 206 SW historical rows. Current source_indexes are invalid legacy IDs.

SOURCE: Repo-local iCar Peugeot 206/206 CC/206 Plus/206 SW sources indexes 0-3.

TARGET VALUE / PROFILE ACTION: Keep historical rows only. Replace invalid source indexes 2133/2135/2136/2137 with valid local profile source indexes: hatchback -> [0], CC -> [1], 206 Plus -> [2], SW/Estate -> [3].

### VARIANT 31 — Peugeot 206 row 1

MODEL: IL-confirmed|Peugeot|206

CURRENT VALUE:
```json
{"version_or_trim": "XR", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.4L", "engine_displacement_l": 1.4, "horsepower_hp": 75, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1999, "year_end": 2009, "support_level": "direct", "source_indexes": [2133]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XR` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.4L` / `1.4` / `75` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1999-2009` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 206, 206 CC, 206 Plus and 206 SW historical rows. Current source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar Peugeot 206/206 CC/206 Plus/206 SW sources indexes 0-3.

TARGET VALUE:
Keep historical rows only. Replace invalid source indexes 2133/2135/2136/2137 with valid local profile source indexes: hatchback -> [0], CC -> [1], 206 Plus -> [2], SW/Estate -> [3].

ACTION: FIX SOURCE INDEXES

### VARIANT 32 — Peugeot 206 row 2

MODEL: IL-confirmed|Peugeot|206

CURRENT VALUE:
```json
{"version_or_trim": "XT", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.4L", "engine_displacement_l": 1.4, "horsepower_hp": 75, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1999, "year_end": 2009, "support_level": "direct", "source_indexes": [2133]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XT` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.4L` / `1.4` / `75` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1999-2009` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 206, 206 CC, 206 Plus and 206 SW historical rows. Current source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar Peugeot 206/206 CC/206 Plus/206 SW sources indexes 0-3.

TARGET VALUE:
Keep historical rows only. Replace invalid source indexes 2133/2135/2136/2137 with valid local profile source indexes: hatchback -> [0], CC -> [1], 206 Plus -> [2], SW/Estate -> [3].

ACTION: FIX SOURCE INDEXES

### VARIANT 33 — Peugeot 206 row 3

MODEL: IL-confirmed|Peugeot|206

CURRENT VALUE:
```json
{"version_or_trim": "XT", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 90, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1999, "year_end": 2001, "support_level": "direct", "source_indexes": [2133]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XT` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `90` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1999-2001` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 206, 206 CC, 206 Plus and 206 SW historical rows. Current source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar Peugeot 206/206 CC/206 Plus/206 SW sources indexes 0-3.

TARGET VALUE:
Keep historical rows only. Replace invalid source indexes 2133/2135/2136/2137 with valid local profile source indexes: hatchback -> [0], CC -> [1], 206 Plus -> [2], SW/Estate -> [3].

ACTION: FIX SOURCE INDEXES

### VARIANT 34 — Peugeot 206 row 4

MODEL: IL-confirmed|Peugeot|206

CURRENT VALUE:
```json
{"version_or_trim": "XS", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 110, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2001, "year_end": 2008, "support_level": "direct", "source_indexes": [2133]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XS` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `110` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2001-2008` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 206, 206 CC, 206 Plus and 206 SW historical rows. Current source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar Peugeot 206/206 CC/206 Plus/206 SW sources indexes 0-3.

TARGET VALUE:
Keep historical rows only. Replace invalid source indexes 2133/2135/2136/2137 with valid local profile source indexes: hatchback -> [0], CC -> [1], 206 Plus -> [2], SW/Estate -> [3].

ACTION: FIX SOURCE INDEXES

### VARIANT 35 — Peugeot 206 row 5

MODEL: IL-confirmed|Peugeot|206

CURRENT VALUE:
```json
{"version_or_trim": "XT", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 110, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2001, "year_end": 2008, "support_level": "direct", "source_indexes": [2133]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XT` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `110` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2001-2008` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 206, 206 CC, 206 Plus and 206 SW historical rows. Current source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar Peugeot 206/206 CC/206 Plus/206 SW sources indexes 0-3.

TARGET VALUE:
Keep historical rows only. Replace invalid source indexes 2133/2135/2136/2137 with valid local profile source indexes: hatchback -> [0], CC -> [1], 206 Plus -> [2], SW/Estate -> [3].

ACTION: FIX SOURCE INDEXES

### VARIANT 36 — Peugeot 206 row 6

MODEL: IL-confirmed|Peugeot|206

CURRENT VALUE:
```json
{"version_or_trim": "GTI", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "2.0L", "engine_displacement_l": 2.0, "horsepower_hp": 136, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1999, "year_end": 2006, "support_level": "direct", "source_indexes": [2133]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `GTI` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L` / `2.0` / `136` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1999-2006` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 206, 206 CC, 206 Plus and 206 SW historical rows. Current source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar Peugeot 206/206 CC/206 Plus/206 SW sources indexes 0-3.

TARGET VALUE:
Keep historical rows only. Replace invalid source indexes 2133/2135/2136/2137 with valid local profile source indexes: hatchback -> [0], CC -> [1], 206 Plus -> [2], SW/Estate -> [3].

ACTION: FIX SOURCE INDEXES

### VARIANT 37 — Peugeot 206 row 7

MODEL: IL-confirmed|Peugeot|206

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Convertible", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 110, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2001, "year_end": 2007, "support_level": "direct", "source_indexes": [2135]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Convertible` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `110` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2001-2007` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 206, 206 CC, 206 Plus and 206 SW historical rows. Current source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar Peugeot 206/206 CC/206 Plus/206 SW sources indexes 0-3.

TARGET VALUE:
Keep historical rows only. Replace invalid source indexes 2133/2135/2136/2137 with valid local profile source indexes: hatchback -> [0], CC -> [1], 206 Plus -> [2], SW/Estate -> [3].

ACTION: FIX SOURCE INDEXES

### VARIANT 38 — Peugeot 206 row 8

MODEL: IL-confirmed|Peugeot|206

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Convertible", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 110, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2001, "year_end": 2007, "support_level": "direct", "source_indexes": [2135]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Convertible` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `110` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2001-2007` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 206, 206 CC, 206 Plus and 206 SW historical rows. Current source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar Peugeot 206/206 CC/206 Plus/206 SW sources indexes 0-3.

TARGET VALUE:
Keep historical rows only. Replace invalid source indexes 2133/2135/2136/2137 with valid local profile source indexes: hatchback -> [0], CC -> [1], 206 Plus -> [2], SW/Estate -> [3].

ACTION: FIX SOURCE INDEXES

### VARIANT 39 — Peugeot 206 row 9

MODEL: IL-confirmed|Peugeot|206

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Convertible", "fuel_type": "petrol", "engine": "2.0L", "engine_displacement_l": 2.0, "horsepower_hp": 136, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2001, "year_end": 2007, "support_level": "direct", "source_indexes": [2135]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Convertible` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L` / `2.0` / `136` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2001-2007` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 206, 206 CC, 206 Plus and 206 SW historical rows. Current source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar Peugeot 206/206 CC/206 Plus/206 SW sources indexes 0-3.

TARGET VALUE:
Keep historical rows only. Replace invalid source indexes 2133/2135/2136/2137 with valid local profile source indexes: hatchback -> [0], CC -> [1], 206 Plus -> [2], SW/Estate -> [3].

ACTION: FIX SOURCE INDEXES

### VARIANT 40 — Peugeot 206 row 10

MODEL: IL-confirmed|Peugeot|206

CURRENT VALUE:
```json
{"version_or_trim": "Urban", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.4L", "engine_displacement_l": 1.4, "horsepower_hp": 73, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2009, "year_end": 2012, "support_level": "direct", "source_indexes": [2136]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Urban` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.4L` / `1.4` / `73` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2009-2012` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 206, 206 CC, 206 Plus and 206 SW historical rows. Current source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar Peugeot 206/206 CC/206 Plus/206 SW sources indexes 0-3.

TARGET VALUE:
Keep historical rows only. Replace invalid source indexes 2133/2135/2136/2137 with valid local profile source indexes: hatchback -> [0], CC -> [1], 206 Plus -> [2], SW/Estate -> [3].

ACTION: FIX SOURCE INDEXES

### VARIANT 41 — Peugeot 206 row 11

MODEL: IL-confirmed|Peugeot|206

CURRENT VALUE:
```json
{"version_or_trim": "XT", "body_type": "Estate", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 110, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2002, "year_end": 2006, "support_level": "direct", "source_indexes": [2137]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XT` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Estate` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `110` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2002-2006` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 206, 206 CC, 206 Plus and 206 SW historical rows. Current source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar Peugeot 206/206 CC/206 Plus/206 SW sources indexes 0-3.

TARGET VALUE:
Keep historical rows only. Replace invalid source indexes 2133/2135/2136/2137 with valid local profile source indexes: hatchback -> [0], CC -> [1], 206 Plus -> [2], SW/Estate -> [3].

ACTION: FIX SOURCE INDEXES

---

## MODEL PROFILE: IL-confirmed|Peugeot|207

PROFILE ACTION: KEEP

WEB-VALIDATED FACT: Israeli sources support Peugeot 207 2007-2012 hatchback and SW/CC through about 2013; petrol FWD rows look grounded.

SOURCE: Repo-local iCar/Auto Peugeot 207 sources.

TARGET VALUE / PROFILE ACTION: Keep as historical; do not currentize. Ensure body type distinctions Hatchback/Estate/Convertible remain.

### VARIANT 42 — Peugeot 207 row 1

MODEL: IL-confirmed|Peugeot|207

CURRENT VALUE:
```json
{"version_or_trim": "Trendy", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.4L", "engine_displacement_l": 1.4, "horsepower_hp": 95, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2007, "year_end": 2012, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Trendy` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.4L` / `1.4` / `95` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2007-2012` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 207 2007-2012 hatchback and SW/CC through about 2013; petrol FWD rows look grounded.

SOURCE:
Repo-local iCar/Auto Peugeot 207 sources.

TARGET VALUE:
Keep as historical; do not currentize. Ensure body type distinctions Hatchback/Estate/Convertible remain.

ACTION: KEEP

### VARIANT 43 — Peugeot 207 row 2

MODEL: IL-confirmed|Peugeot|207

CURRENT VALUE:
```json
{"version_or_trim": "Sport", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 120, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2007, "year_end": 2012, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Sport` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `120` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2007-2012` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 207 2007-2012 hatchback and SW/CC through about 2013; petrol FWD rows look grounded.

SOURCE:
Repo-local iCar/Auto Peugeot 207 sources.

TARGET VALUE:
Keep as historical; do not currentize. Ensure body type distinctions Hatchback/Estate/Convertible remain.

ACTION: KEEP

### VARIANT 44 — Peugeot 207 row 3

MODEL: IL-confirmed|Peugeot|207

CURRENT VALUE:
```json
{"version_or_trim": "Active", "body_type": "Estate", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 120, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2008, "year_end": 2013, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Active` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Estate` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `120` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2008-2013` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 207 2007-2012 hatchback and SW/CC through about 2013; petrol FWD rows look grounded.

SOURCE:
Repo-local iCar/Auto Peugeot 207 sources.

TARGET VALUE:
Keep as historical; do not currentize. Ensure body type distinctions Hatchback/Estate/Convertible remain.

ACTION: KEEP

### VARIANT 45 — Peugeot 207 row 4

MODEL: IL-confirmed|Peugeot|207

CURRENT VALUE:
```json
{"version_or_trim": "Sport", "body_type": "Convertible", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 120, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2007, "year_end": 2013, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Sport` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Convertible` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `120` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2007-2013` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 207 2007-2012 hatchback and SW/CC through about 2013; petrol FWD rows look grounded.

SOURCE:
Repo-local iCar/Auto Peugeot 207 sources.

TARGET VALUE:
Keep as historical; do not currentize. Ensure body type distinctions Hatchback/Estate/Convertible remain.

ACTION: KEEP

---

## MODEL PROFILE: IL-confirmed|Peugeot|208

PROFILE ACTION: FIX SOURCE INDEXES + REVIEW CURRENT SPLIT

WEB-VALIDATED FACT: Israeli sources support historical 208 2012-2019 and later 1.2 turbo 130 hp AT8 rows; current 2025/2026 local information supports 208 MHEV launch and current official Peugeot Online page, so 130 hp petrol must not be blindly extended as the only current row. Existing source_indexes are invalid legacy IDs.

SOURCE: Peugeot Online Israel 208 page; Auto.co.il 208; Gear/industry item on 208 MHEV launch; repo-local iCar/Cartube/Auto sources indexes 0-2.

TARGET VALUE / PROFILE ACTION: Replace invalid source_indexes 2121/2122/2124 with valid local indexes. Keep 2012-2019 rows historical; keep 2020-2024 1.2T 130 AT8 as historical/current only through grounded years; add/split current MHEV row only if repo-local evidence supports exact hp/transmission; do not fabricate e-208 or MHEV data.

### VARIANT 46 — Peugeot 208 row 1

MODEL: IL-confirmed|Peugeot|208

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.2L", "engine_displacement_l": 1.2, "horsepower_hp": 82, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2012, "year_end": 2019, "support_level": "direct", "source_indexes": [2121]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L` / `1.2` / `82` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2012-2019` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support historical 208 2012-2019 and later 1.2 turbo 130 hp AT8 rows; current 2025/2026 local information supports 208 MHEV launch and current official Peugeot Online page, so 130 hp petrol must not be blindly extended as the only current row. Existing source_indexes are invalid legacy IDs.

SOURCE:
Peugeot Online Israel 208 page; Auto.co.il 208; Gear/industry item on 208 MHEV launch; repo-local iCar/Cartube/Auto sources indexes 0-2.

TARGET VALUE:
Replace invalid source_indexes 2121/2122/2124 with valid local indexes. Keep 2012-2019 rows historical; keep 2020-2024 1.2T 130 AT8 as historical/current only through grounded years; add/split current MHEV row only if repo-local evidence supports exact hp/transmission; do not fabricate e-208 or MHEV data.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT SPLIT

### VARIANT 47 — Peugeot 208 row 2

MODEL: IL-confirmed|Peugeot|208

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.2L", "engine_displacement_l": 1.2, "horsepower_hp": 82, "transmission": "5-speed automatic", "drivetrain": "FWD", "year_start": 2012, "year_end": 2019, "support_level": "direct", "source_indexes": [2121]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L` / `1.2` / `82` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2012-2019` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support historical 208 2012-2019 and later 1.2 turbo 130 hp AT8 rows; current 2025/2026 local information supports 208 MHEV launch and current official Peugeot Online page, so 130 hp petrol must not be blindly extended as the only current row. Existing source_indexes are invalid legacy IDs.

SOURCE:
Peugeot Online Israel 208 page; Auto.co.il 208; Gear/industry item on 208 MHEV launch; repo-local iCar/Cartube/Auto sources indexes 0-2.

TARGET VALUE:
Replace invalid source_indexes 2121/2122/2124 with valid local indexes. Keep 2012-2019 rows historical; keep 2020-2024 1.2T 130 AT8 as historical/current only through grounded years; add/split current MHEV row only if repo-local evidence supports exact hp/transmission; do not fabricate e-208 or MHEV data.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT SPLIT

### VARIANT 48 — Peugeot 208 row 3

MODEL: IL-confirmed|Peugeot|208

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 120, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2012, "year_end": 2015, "support_level": "direct", "source_indexes": [2121]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `120` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2012-2015` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support historical 208 2012-2019 and later 1.2 turbo 130 hp AT8 rows; current 2025/2026 local information supports 208 MHEV launch and current official Peugeot Online page, so 130 hp petrol must not be blindly extended as the only current row. Existing source_indexes are invalid legacy IDs.

SOURCE:
Peugeot Online Israel 208 page; Auto.co.il 208; Gear/industry item on 208 MHEV launch; repo-local iCar/Cartube/Auto sources indexes 0-2.

TARGET VALUE:
Replace invalid source_indexes 2121/2122/2124 with valid local indexes. Keep 2012-2019 rows historical; keep 2020-2024 1.2T 130 AT8 as historical/current only through grounded years; add/split current MHEV row only if repo-local evidence supports exact hp/transmission; do not fabricate e-208 or MHEV data.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT SPLIT

### VARIANT 49 — Peugeot 208 row 4

MODEL: IL-confirmed|Peugeot|208

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.2L turbo", "engine_displacement_l": 1.2, "horsepower_hp": 110, "transmission": "6-speed automatic", "drivetrain": "FWD", "year_start": 2015, "year_end": 2019, "support_level": "direct", "source_indexes": [2121]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L turbo` / `1.2` / `110` — must match embedded fact and repo-local source.
- transmission/drivetrain: `6-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2015-2019` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support historical 208 2012-2019 and later 1.2 turbo 130 hp AT8 rows; current 2025/2026 local information supports 208 MHEV launch and current official Peugeot Online page, so 130 hp petrol must not be blindly extended as the only current row. Existing source_indexes are invalid legacy IDs.

SOURCE:
Peugeot Online Israel 208 page; Auto.co.il 208; Gear/industry item on 208 MHEV launch; repo-local iCar/Cartube/Auto sources indexes 0-2.

TARGET VALUE:
Replace invalid source_indexes 2121/2122/2124 with valid local indexes. Keep 2012-2019 rows historical; keep 2020-2024 1.2T 130 AT8 as historical/current only through grounded years; add/split current MHEV row only if repo-local evidence supports exact hp/transmission; do not fabricate e-208 or MHEV data.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT SPLIT

### VARIANT 50 — Peugeot 208 row 5

MODEL: IL-confirmed|Peugeot|208

CURRENT VALUE:
```json
{"version_or_trim": "GTI", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L turbo", "engine_displacement_l": 1.6, "horsepower_hp": 200, "transmission": "6-speed manual", "drivetrain": "FWD", "year_start": 2013, "year_end": 2015, "support_level": "direct", "source_indexes": [2124]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `GTI` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L turbo` / `1.6` / `200` — must match embedded fact and repo-local source.
- transmission/drivetrain: `6-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2013-2015` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support historical 208 2012-2019 and later 1.2 turbo 130 hp AT8 rows; current 2025/2026 local information supports 208 MHEV launch and current official Peugeot Online page, so 130 hp petrol must not be blindly extended as the only current row. Existing source_indexes are invalid legacy IDs.

SOURCE:
Peugeot Online Israel 208 page; Auto.co.il 208; Gear/industry item on 208 MHEV launch; repo-local iCar/Cartube/Auto sources indexes 0-2.

TARGET VALUE:
Replace invalid source_indexes 2121/2122/2124 with valid local indexes. Keep 2012-2019 rows historical; keep 2020-2024 1.2T 130 AT8 as historical/current only through grounded years; add/split current MHEV row only if repo-local evidence supports exact hp/transmission; do not fabricate e-208 or MHEV data.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT SPLIT

### VARIANT 51 — Peugeot 208 row 6

MODEL: IL-confirmed|Peugeot|208

CURRENT VALUE:
```json
{"version_or_trim": "GTI", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L turbo", "engine_displacement_l": 1.6, "horsepower_hp": 208, "transmission": "6-speed manual", "drivetrain": "FWD", "year_start": 2015, "year_end": 2019, "support_level": "direct", "source_indexes": [2124]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `GTI` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L turbo` / `1.6` / `208` — must match embedded fact and repo-local source.
- transmission/drivetrain: `6-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2015-2019` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support historical 208 2012-2019 and later 1.2 turbo 130 hp AT8 rows; current 2025/2026 local information supports 208 MHEV launch and current official Peugeot Online page, so 130 hp petrol must not be blindly extended as the only current row. Existing source_indexes are invalid legacy IDs.

SOURCE:
Peugeot Online Israel 208 page; Auto.co.il 208; Gear/industry item on 208 MHEV launch; repo-local iCar/Cartube/Auto sources indexes 0-2.

TARGET VALUE:
Replace invalid source_indexes 2121/2122/2124 with valid local indexes. Keep 2012-2019 rows historical; keep 2020-2024 1.2T 130 AT8 as historical/current only through grounded years; add/split current MHEV row only if repo-local evidence supports exact hp/transmission; do not fabricate e-208 or MHEV data.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT SPLIT

### VARIANT 52 — Peugeot 208 row 7

MODEL: IL-confirmed|Peugeot|208

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.2L turbo", "engine_displacement_l": 1.2, "horsepower_hp": 130, "transmission": "8-speed automatic", "drivetrain": "FWD", "year_start": 2020, "year_end": 2024, "support_level": "direct", "source_indexes": [2122]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L turbo` / `1.2` / `130` — must match embedded fact and repo-local source.
- transmission/drivetrain: `8-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2020-2024` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support historical 208 2012-2019 and later 1.2 turbo 130 hp AT8 rows; current 2025/2026 local information supports 208 MHEV launch and current official Peugeot Online page, so 130 hp petrol must not be blindly extended as the only current row. Existing source_indexes are invalid legacy IDs.

SOURCE:
Peugeot Online Israel 208 page; Auto.co.il 208; Gear/industry item on 208 MHEV launch; repo-local iCar/Cartube/Auto sources indexes 0-2.

TARGET VALUE:
Replace invalid source_indexes 2121/2122/2124 with valid local indexes. Keep 2012-2019 rows historical; keep 2020-2024 1.2T 130 AT8 as historical/current only through grounded years; add/split current MHEV row only if repo-local evidence supports exact hp/transmission; do not fabricate e-208 or MHEV data.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT SPLIT

---

## MODEL PROFILE: IL-confirmed|Peugeot|301

PROFILE ACTION: MERGE + FIX CANONICAL COVERAGE

WEB-VALIDATED FACT: Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE: iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE / PROFILE ACTION: Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

### VARIANT 53 — Peugeot 301 row 1

MODEL: IL-confirmed|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.2L", "engine_displacement_l": 1.2, "horsepower_hp": 72, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2013, "year_end": 2015, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L` / `1.2` / `72` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2013-2015` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 54 — Peugeot 301 row 2

MODEL: IL-confirmed|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.2L", "engine_displacement_l": 1.2, "horsepower_hp": 72, "transmission": "5-speed automatic", "drivetrain": "FWD", "year_start": 2013, "year_end": 2015, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L` / `1.2` / `72` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2013-2015` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 55 — Peugeot 301 row 3

MODEL: IL-confirmed|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.2L", "engine_displacement_l": 1.2, "horsepower_hp": 82, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2015, "year_end": 2020, "support_level": "direct", "source_indexes": [0, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L` / `1.2` / `82` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2015-2020` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 56 — Peugeot 301 row 4

MODEL: IL-confirmed|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.2L", "engine_displacement_l": 1.2, "horsepower_hp": 82, "transmission": "5-speed automatic", "drivetrain": "FWD", "year_start": 2015, "year_end": 2020, "support_level": "direct", "source_indexes": [0, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L` / `1.2` / `82` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2015-2020` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 57 — Peugeot 301 row 5

MODEL: IL-confirmed|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 115, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2013, "year_end": 2016, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `115` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2013-2016` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 58 — Peugeot 301 row 6

MODEL: IL-confirmed|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 115, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2013, "year_end": 2016, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `115` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2013-2016` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 59 — Peugeot 301 row 7

MODEL: IL-confirmed|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 115, "transmission": "6-speed automatic", "drivetrain": "FWD", "year_start": 2016, "year_end": 2020, "support_level": "direct", "source_indexes": [0, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `115` — must match embedded fact and repo-local source.
- transmission/drivetrain: `6-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2016-2020` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

---

## MODEL PROFILE: IL-likely|Peugeot|301

PROFILE ACTION: MERGE + FIX CANONICAL COVERAGE

WEB-VALIDATED FACT: Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE: iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE / PROFILE ACTION: Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

### VARIANT 60 — Peugeot 301 row 1

MODEL: IL-likely|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.2L", "engine_displacement_l": 1.2, "horsepower_hp": 72, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2013, "year_end": 2015, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L` / `1.2` / `72` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2013-2015` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 61 — Peugeot 301 row 2

MODEL: IL-likely|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.2L", "engine_displacement_l": 1.2, "horsepower_hp": 72, "transmission": "5-speed automatic", "drivetrain": "FWD", "year_start": 2013, "year_end": 2015, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L` / `1.2` / `72` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2013-2015` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 62 — Peugeot 301 row 3

MODEL: IL-likely|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.2L", "engine_displacement_l": 1.2, "horsepower_hp": 82, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2015, "year_end": 2019, "support_level": "direct", "source_indexes": [1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L` / `1.2` / `82` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2015-2019` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 63 — Peugeot 301 row 4

MODEL: IL-likely|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.2L", "engine_displacement_l": 1.2, "horsepower_hp": 82, "transmission": "5-speed automatic", "drivetrain": "FWD", "year_start": 2015, "year_end": 2019, "support_level": "direct", "source_indexes": [1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L` / `1.2` / `82` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2015-2019` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 64 — Peugeot 301 row 5

MODEL: IL-likely|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 115, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2013, "year_end": 2016, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `115` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2013-2016` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 65 — Peugeot 301 row 6

MODEL: IL-likely|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 115, "transmission": "6-speed automatic", "drivetrain": "FWD", "year_start": 2016, "year_end": 2019, "support_level": "direct", "source_indexes": [1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `115` — must match embedded fact and repo-local source.
- transmission/drivetrain: `6-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2016-2019` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 66 — Peugeot 301 row 7

MODEL: IL-likely|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "diesel", "engine": "1.6L turbo", "engine_displacement_l": 1.6, "horsepower_hp": 92, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2013, "year_end": 2016, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `diesel` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L turbo` / `1.6` / `92` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2013-2016` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

### VARIANT 67 — Peugeot 301 row 8

MODEL: IL-likely|Peugeot|301

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "diesel", "engine": "1.6L turbo", "engine_displacement_l": 1.6, "horsepower_hp": 100, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2016, "year_end": 2019, "support_level": "direct", "source_indexes": [1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `diesel` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L turbo` / `1.6` / `100` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2016-2019` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 301 2013-2020 with 1.2 petrol 72/82 hp, 1.6 petrol 115 hp, and diesel 1.6 92/100 hp rows. IL-likely profile duplicates IL-confirmed and also contains diesel rows missing/duplicated.

SOURCE:
iCar Peugeot 301 sources; Cartube launch/update sources.

TARGET VALUE:
Merge IL-likely Peugeot 301 into IL-confirmed canonical profile. Preserve diesel rows if supported; do not leave duplicate clean profiles. Normalize year ranges 2013-2015/2016-2020 according to source evidence.

ACTION: MERGE + FIX CANONICAL COVERAGE

---

## MODEL PROFILE: IL-confirmed|Peugeot|306

PROFILE ACTION: KEEP

WEB-VALIDATED FACT: Israeli historical sources support Peugeot 306 1993-2002 variants including XN/XR/SR/GTI and convertible.

SOURCE: Repo-local Auto/Yad2/KML Peugeot 306 sources.

TARGET VALUE / PROFILE ACTION: Keep historical rows; do not currentize. If convertible trim is null, keep only if source does not provide exact trim, otherwise normalize.

### VARIANT 68 — Peugeot 306 row 1

MODEL: IL-confirmed|Peugeot|306

CURRENT VALUE:
```json
{"version_or_trim": "XN", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.4L", "engine_displacement_l": 1.4, "horsepower_hp": 75, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1993, "year_end": 2002, "support_level": "direct", "source_indexes": [0, 1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XN` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.4L` / `1.4` / `75` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1993-2002` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 306 1993-2002 variants including XN/XR/SR/GTI and convertible.

SOURCE:
Repo-local Auto/Yad2/KML Peugeot 306 sources.

TARGET VALUE:
Keep historical rows; do not currentize. If convertible trim is null, keep only if source does not provide exact trim, otherwise normalize.

ACTION: KEEP

### VARIANT 69 — Peugeot 306 row 2

MODEL: IL-confirmed|Peugeot|306

CURRENT VALUE:
```json
{"version_or_trim": "XR", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 90, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1993, "year_end": 2002, "support_level": "direct", "source_indexes": [0, 1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XR` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `90` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1993-2002` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 306 1993-2002 variants including XN/XR/SR/GTI and convertible.

SOURCE:
Repo-local Auto/Yad2/KML Peugeot 306 sources.

TARGET VALUE:
Keep historical rows; do not currentize. If convertible trim is null, keep only if source does not provide exact trim, otherwise normalize.

ACTION: KEEP

### VARIANT 70 — Peugeot 306 row 3

MODEL: IL-confirmed|Peugeot|306

CURRENT VALUE:
```json
{"version_or_trim": "XR", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 90, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1993, "year_end": 2002, "support_level": "direct", "source_indexes": [0, 1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `XR` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `90` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1993-2002` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 306 1993-2002 variants including XN/XR/SR/GTI and convertible.

SOURCE:
Repo-local Auto/Yad2/KML Peugeot 306 sources.

TARGET VALUE:
Keep historical rows; do not currentize. If convertible trim is null, keep only if source does not provide exact trim, otherwise normalize.

ACTION: KEEP

### VARIANT 71 — Peugeot 306 row 4

MODEL: IL-confirmed|Peugeot|306

CURRENT VALUE:
```json
{"version_or_trim": "SR", "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 90, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1994, "year_end": 2002, "support_level": "direct", "source_indexes": [0, 1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `SR` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `90` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1994-2002` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 306 1993-2002 variants including XN/XR/SR/GTI and convertible.

SOURCE:
Repo-local Auto/Yad2/KML Peugeot 306 sources.

TARGET VALUE:
Keep historical rows; do not currentize. If convertible trim is null, keep only if source does not provide exact trim, otherwise normalize.

ACTION: KEEP

### VARIANT 72 — Peugeot 306 row 5

MODEL: IL-confirmed|Peugeot|306

CURRENT VALUE:
```json
{"version_or_trim": "SR", "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.8L", "engine_displacement_l": 1.8, "horsepower_hp": 103, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1994, "year_end": 2001, "support_level": "direct", "source_indexes": [0, 1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `SR` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.8L` / `1.8` / `103` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1994-2001` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 306 1993-2002 variants including XN/XR/SR/GTI and convertible.

SOURCE:
Repo-local Auto/Yad2/KML Peugeot 306 sources.

TARGET VALUE:
Keep historical rows; do not currentize. If convertible trim is null, keep only if source does not provide exact trim, otherwise normalize.

ACTION: KEEP

### VARIANT 73 — Peugeot 306 row 6

MODEL: IL-confirmed|Peugeot|306

CURRENT VALUE:
```json
{"version_or_trim": "GTI", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "2.0L", "engine_displacement_l": 2.0, "horsepower_hp": 167, "transmission": "6-speed manual", "drivetrain": "FWD", "year_start": 1997, "year_end": 2001, "support_level": "direct", "source_indexes": [0, 1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `GTI` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L` / `2.0` / `167` — must match embedded fact and repo-local source.
- transmission/drivetrain: `6-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1997-2001` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 306 1993-2002 variants including XN/XR/SR/GTI and convertible.

SOURCE:
Repo-local Auto/Yad2/KML Peugeot 306 sources.

TARGET VALUE:
Keep historical rows; do not currentize. If convertible trim is null, keep only if source does not provide exact trim, otherwise normalize.

ACTION: KEEP

### VARIANT 74 — Peugeot 306 row 7

MODEL: IL-confirmed|Peugeot|306

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Convertible", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 90, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1995, "year_end": 2002, "support_level": "direct", "source_indexes": [0, 1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Convertible` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `90` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1995-2002` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 306 1993-2002 variants including XN/XR/SR/GTI and convertible.

SOURCE:
Repo-local Auto/Yad2/KML Peugeot 306 sources.

TARGET VALUE:
Keep historical rows; do not currentize. If convertible trim is null, keep only if source does not provide exact trim, otherwise normalize.

ACTION: KEEP

---

## MODEL PROFILE: IL-confirmed|Peugeot|307

PROFILE ACTION: KEEP

WEB-VALIDATED FACT: Israeli sources support Peugeot 307 2002-2008 hatchback/SW/CC rows with 1.6/2.0 petrol FWD.

SOURCE: Repo-local iCar/Auto Peugeot 307/307 CC/307 SW sources.

TARGET VALUE / PROFILE ACTION: Keep historical rows; do not currentize. Preserve body distinctions.

### VARIANT 75 — Peugeot 307 row 1

MODEL: IL-confirmed|Peugeot|307

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 110, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2002, "year_end": 2008, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `110` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2002-2008` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 307 2002-2008 hatchback/SW/CC rows with 1.6/2.0 petrol FWD.

SOURCE:
Repo-local iCar/Auto Peugeot 307/307 CC/307 SW sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve body distinctions.

ACTION: KEEP

### VARIANT 76 — Peugeot 307 row 2

MODEL: IL-confirmed|Peugeot|307

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 110, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 2002, "year_end": 2008, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `110` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2002-2008` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 307 2002-2008 hatchback/SW/CC rows with 1.6/2.0 petrol FWD.

SOURCE:
Repo-local iCar/Auto Peugeot 307/307 CC/307 SW sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve body distinctions.

ACTION: KEEP

### VARIANT 77 — Peugeot 307 row 3

MODEL: IL-confirmed|Peugeot|307

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "petrol", "engine": "2.0L", "engine_displacement_l": 2.0, "horsepower_hp": 140, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2002, "year_end": 2008, "support_level": "direct", "source_indexes": [0, 1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L` / `2.0` / `140` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2002-2008` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 307 2002-2008 hatchback/SW/CC rows with 1.6/2.0 petrol FWD.

SOURCE:
Repo-local iCar/Auto Peugeot 307/307 CC/307 SW sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve body distinctions.

ACTION: KEEP

### VARIANT 78 — Peugeot 307 row 4

MODEL: IL-confirmed|Peugeot|307

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Estate", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 110, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2002, "year_end": 2008, "support_level": "direct", "source_indexes": [3]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Estate` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `110` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2002-2008` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 307 2002-2008 hatchback/SW/CC rows with 1.6/2.0 petrol FWD.

SOURCE:
Repo-local iCar/Auto Peugeot 307/307 CC/307 SW sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve body distinctions.

ACTION: KEEP

### VARIANT 79 — Peugeot 307 row 5

MODEL: IL-confirmed|Peugeot|307

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Estate", "fuel_type": "petrol", "engine": "2.0L", "engine_displacement_l": 2.0, "horsepower_hp": 140, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2002, "year_end": 2008, "support_level": "direct", "source_indexes": [3]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Estate` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L` / `2.0` / `140` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2002-2008` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 307 2002-2008 hatchback/SW/CC rows with 1.6/2.0 petrol FWD.

SOURCE:
Repo-local iCar/Auto Peugeot 307/307 CC/307 SW sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve body distinctions.

ACTION: KEEP

### VARIANT 80 — Peugeot 307 row 6

MODEL: IL-confirmed|Peugeot|307

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Convertible", "fuel_type": "petrol", "engine": "2.0L", "engine_displacement_l": 2.0, "horsepower_hp": 140, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2004, "year_end": 2008, "support_level": "direct", "source_indexes": [2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Convertible` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L` / `2.0` / `140` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2004-2008` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support Peugeot 307 2002-2008 hatchback/SW/CC rows with 1.6/2.0 petrol FWD.

SOURCE:
Repo-local iCar/Auto Peugeot 307/307 CC/307 SW sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve body distinctions.

ACTION: KEEP

---

## MODEL PROFILE: IL-confirmed|Peugeot|308

PROFILE ACTION: FIX SOURCE INDEXES + REVIEW CURRENT COVERAGE

WEB-VALIDATED FACT: Israeli sources support 308 historical rows plus newer 308. Auto.co.il describes current-generation 1.2 turbo 130 and PHEV 180/225; Peugeot Israel source exists in profile. Existing source_indexes are invalid legacy IDs.

SOURCE: Repo-local iCar/Auto/Peugeot Israel sources indexes 0-4; Auto.co.il 308 result.

TARGET VALUE / PROFILE ACTION: Replace invalid source_indexes 2150-2154 with valid local indexes. Keep 2008-2014/2014-2021 historical rows. Keep 2019-2026 1.2T 130 and 2022-2026 PHEV 225 only if exact Peugeot Israel/local source is attached. Add PHEV 180 only if repo-local source supports exact row; otherwise report missing coverage.

### VARIANT 81 — Peugeot 308 row 1

MODEL: IL-confirmed|Peugeot|308

CURRENT VALUE:
```json
{"version_or_trim": "Active", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 120, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2008, "year_end": 2014, "support_level": "direct", "source_indexes": [2150]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Active` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `120` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2008-2014` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support 308 historical rows plus newer 308. Auto.co.il describes current-generation 1.2 turbo 130 and PHEV 180/225; Peugeot Israel source exists in profile. Existing source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar/Auto/Peugeot Israel sources indexes 0-4; Auto.co.il 308 result.

TARGET VALUE:
Replace invalid source_indexes 2150-2154 with valid local indexes. Keep 2008-2014/2014-2021 historical rows. Keep 2019-2026 1.2T 130 and 2022-2026 PHEV 225 only if exact Peugeot Israel/local source is attached. Add PHEV 180 only if repo-local source supports exact row; otherwise report missing coverage.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT COVERAGE

### VARIANT 82 — Peugeot 308 row 2

MODEL: IL-confirmed|Peugeot|308

CURRENT VALUE:
```json
{"version_or_trim": "Comfort", "body_type": "Estate", "fuel_type": "petrol", "engine": "1.6L", "engine_displacement_l": 1.6, "horsepower_hp": 120, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 2008, "year_end": 2014, "support_level": "direct", "source_indexes": [2154]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Comfort` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Estate` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L` / `1.6` / `120` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2008-2014` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support 308 historical rows plus newer 308. Auto.co.il describes current-generation 1.2 turbo 130 and PHEV 180/225; Peugeot Israel source exists in profile. Existing source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar/Auto/Peugeot Israel sources indexes 0-4; Auto.co.il 308 result.

TARGET VALUE:
Replace invalid source_indexes 2150-2154 with valid local indexes. Keep 2008-2014/2014-2021 historical rows. Keep 2019-2026 1.2T 130 and 2022-2026 PHEV 225 only if exact Peugeot Israel/local source is attached. Add PHEV 180 only if repo-local source supports exact row; otherwise report missing coverage.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT COVERAGE

### VARIANT 83 — Peugeot 308 row 3

MODEL: IL-confirmed|Peugeot|308

CURRENT VALUE:
```json
{"version_or_trim": "Premium", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.2L turbo", "engine_displacement_l": 1.2, "horsepower_hp": 130, "transmission": "6-speed automatic", "drivetrain": "FWD", "year_start": 2014, "year_end": 2018, "support_level": "direct", "source_indexes": [2151]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Premium` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L turbo` / `1.2` / `130` — must match embedded fact and repo-local source.
- transmission/drivetrain: `6-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2014-2018` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support 308 historical rows plus newer 308. Auto.co.il describes current-generation 1.2 turbo 130 and PHEV 180/225; Peugeot Israel source exists in profile. Existing source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar/Auto/Peugeot Israel sources indexes 0-4; Auto.co.il 308 result.

TARGET VALUE:
Replace invalid source_indexes 2150-2154 with valid local indexes. Keep 2008-2014/2014-2021 historical rows. Keep 2019-2026 1.2T 130 and 2022-2026 PHEV 225 only if exact Peugeot Israel/local source is attached. Add PHEV 180 only if repo-local source supports exact row; otherwise report missing coverage.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT COVERAGE

### VARIANT 84 — Peugeot 308 row 4

MODEL: IL-confirmed|Peugeot|308

CURRENT VALUE:
```json
{"version_or_trim": "Active", "body_type": "Estate", "fuel_type": "petrol", "engine": "1.2L turbo", "engine_displacement_l": 1.2, "horsepower_hp": 130, "transmission": "6-speed automatic", "drivetrain": "FWD", "year_start": 2014, "year_end": 2018, "support_level": "direct", "source_indexes": [2152]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Active` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Estate` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L turbo` / `1.2` / `130` — must match embedded fact and repo-local source.
- transmission/drivetrain: `6-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2014-2018` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support 308 historical rows plus newer 308. Auto.co.il describes current-generation 1.2 turbo 130 and PHEV 180/225; Peugeot Israel source exists in profile. Existing source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar/Auto/Peugeot Israel sources indexes 0-4; Auto.co.il 308 result.

TARGET VALUE:
Replace invalid source_indexes 2150-2154 with valid local indexes. Keep 2008-2014/2014-2021 historical rows. Keep 2019-2026 1.2T 130 and 2022-2026 PHEV 225 only if exact Peugeot Israel/local source is attached. Add PHEV 180 only if repo-local source supports exact row; otherwise report missing coverage.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT COVERAGE

### VARIANT 85 — Peugeot 308 row 5

MODEL: IL-confirmed|Peugeot|308

CURRENT VALUE:
```json
{"version_or_trim": "Allure", "body_type": "Hatchback", "fuel_type": "petrol", "engine": "1.2L turbo", "engine_displacement_l": 1.2, "horsepower_hp": 130, "transmission": "8-speed automatic", "drivetrain": "FWD", "year_start": 2019, "year_end": 2026, "support_level": "direct", "source_indexes": [2151, 2153]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Allure` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L turbo` / `1.2` / `130` — must match embedded fact and repo-local source.
- transmission/drivetrain: `8-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2019-2026` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support 308 historical rows plus newer 308. Auto.co.il describes current-generation 1.2 turbo 130 and PHEV 180/225; Peugeot Israel source exists in profile. Existing source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar/Auto/Peugeot Israel sources indexes 0-4; Auto.co.il 308 result.

TARGET VALUE:
Replace invalid source_indexes 2150-2154 with valid local indexes. Keep 2008-2014/2014-2021 historical rows. Keep 2019-2026 1.2T 130 and 2022-2026 PHEV 225 only if exact Peugeot Israel/local source is attached. Add PHEV 180 only if repo-local source supports exact row; otherwise report missing coverage.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT COVERAGE

### VARIANT 86 — Peugeot 308 row 6

MODEL: IL-confirmed|Peugeot|308

CURRENT VALUE:
```json
{"version_or_trim": "Premium", "body_type": "Estate", "fuel_type": "petrol", "engine": "1.2L turbo", "engine_displacement_l": 1.2, "horsepower_hp": 130, "transmission": "8-speed automatic", "drivetrain": "FWD", "year_start": 2019, "year_end": 2021, "support_level": "direct", "source_indexes": [2152]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Premium` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Estate` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L turbo` / `1.2` / `130` — must match embedded fact and repo-local source.
- transmission/drivetrain: `8-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2019-2021` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support 308 historical rows plus newer 308. Auto.co.il describes current-generation 1.2 turbo 130 and PHEV 180/225; Peugeot Israel source exists in profile. Existing source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar/Auto/Peugeot Israel sources indexes 0-4; Auto.co.il 308 result.

TARGET VALUE:
Replace invalid source_indexes 2150-2154 with valid local indexes. Keep 2008-2014/2014-2021 historical rows. Keep 2019-2026 1.2T 130 and 2022-2026 PHEV 225 only if exact Peugeot Israel/local source is attached. Add PHEV 180 only if repo-local source supports exact row; otherwise report missing coverage.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT COVERAGE

### VARIANT 87 — Peugeot 308 row 7

MODEL: IL-confirmed|Peugeot|308

CURRENT VALUE:
```json
{"version_or_trim": "GT", "body_type": "Hatchback", "fuel_type": "plug_in_hybrid", "engine": "1.6L turbo", "engine_displacement_l": 1.6, "horsepower_hp": 225, "transmission": "8-speed automatic", "drivetrain": "FWD", "year_start": 2022, "year_end": 2026, "support_level": "direct", "source_indexes": [2153]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `GT` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Hatchback` — must match Israeli body style/source.
- fuel_type: `plug_in_hybrid` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.6L turbo` / `1.6` / `225` — must match embedded fact and repo-local source.
- transmission/drivetrain: `8-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2022-2026` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli sources support 308 historical rows plus newer 308. Auto.co.il describes current-generation 1.2 turbo 130 and PHEV 180/225; Peugeot Israel source exists in profile. Existing source_indexes are invalid legacy IDs.

SOURCE:
Repo-local iCar/Auto/Peugeot Israel sources indexes 0-4; Auto.co.il 308 result.

TARGET VALUE:
Replace invalid source_indexes 2150-2154 with valid local indexes. Keep 2008-2014/2014-2021 historical rows. Keep 2019-2026 1.2T 130 and 2022-2026 PHEV 225 only if exact Peugeot Israel/local source is attached. Add PHEV 180 only if repo-local source supports exact row; otherwise report missing coverage.

ACTION: FIX SOURCE INDEXES + REVIEW CURRENT COVERAGE

---

## MODEL PROFILE: IL-confirmed|Peugeot|4007

PROFILE ACTION: FIX YEAR_END / MOVE TO REVIEW IF NOT GROUNDABLE

WEB-VALIDATED FACT: Peugeot 4007 is a historical SUV/crossover and not a current Israeli model; repo row has year_end null, which falsely makes it current.

SOURCE: Repo-local iCar/Walla historical Peugeot 4007 sources.

TARGET VALUE / PROFILE ACTION: Set year_end to historical end year supported by sources (likely 2012/2013; use repo-local source), or move to review if exact Israeli year_end cannot be grounded. Do not leave year_end null/current.

### VARIANT 88 — Peugeot 4007 row 1

MODEL: IL-confirmed|Peugeot|4007

CURRENT VALUE:
```json
{"version_or_trim": "Premium", "body_type": "SUV", "fuel_type": "diesel", "engine": "2.2L turbo", "engine_displacement_l": 2.2, "horsepower_hp": 156, "transmission": "manual", "drivetrain": "4WD", "year_start": 2007, "year_end": null, "support_level": "direct", "source_indexes": [0, 1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Premium` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `SUV` — must match Israeli body style/source.
- fuel_type: `diesel` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.2L turbo` / `2.2` / `156` — must match embedded fact and repo-local source.
- transmission/drivetrain: `manual` / `4WD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2007-None` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Peugeot 4007 is a historical SUV/crossover and not a current Israeli model; repo row has year_end null, which falsely makes it current.

SOURCE:
Repo-local iCar/Walla historical Peugeot 4007 sources.

TARGET VALUE:
Set year_end to historical end year supported by sources (likely 2012/2013; use repo-local source), or move to review if exact Israeli year_end cannot be grounded. Do not leave year_end null/current.

ACTION: FIX YEAR_END / MOVE TO REVIEW IF NOT GROUNDABLE

---

## MODEL PROFILE: IL-confirmed|Peugeot|406

PROFILE ACTION: KEEP

WEB-VALIDATED FACT: Israeli historical sources support Peugeot 406 sedan/estate/coupe 1995/1996-2004 with 1.8/2.0 petrol, 2.0 HDi diesel and 3.0 V6 coupe rows.

SOURCE: Repo-local Auto/Gear Peugeot 406 sources.

TARGET VALUE / PROFILE ACTION: Keep historical rows; do not currentize. Preserve coupe and estate body distinctions.

### VARIANT 89 — Peugeot 406 row 1

MODEL: IL-confirmed|Peugeot|406

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.8L", "engine_displacement_l": 1.8, "horsepower_hp": 110, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1995, "year_end": 2004, "support_level": "direct", "source_indexes": [0, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.8L` / `1.8` / `110` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1995-2004` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 406 sedan/estate/coupe 1995/1996-2004 with 1.8/2.0 petrol, 2.0 HDi diesel and 3.0 V6 coupe rows.

SOURCE:
Repo-local Auto/Gear Peugeot 406 sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve coupe and estate body distinctions.

ACTION: KEEP

### VARIANT 90 — Peugeot 406 row 2

MODEL: IL-confirmed|Peugeot|406

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "1.8L", "engine_displacement_l": 1.8, "horsepower_hp": 110, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1995, "year_end": 2004, "support_level": "direct", "source_indexes": [0, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.8L` / `1.8` / `110` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1995-2004` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 406 sedan/estate/coupe 1995/1996-2004 with 1.8/2.0 petrol, 2.0 HDi diesel and 3.0 V6 coupe rows.

SOURCE:
Repo-local Auto/Gear Peugeot 406 sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve coupe and estate body distinctions.

ACTION: KEEP

### VARIANT 91 — Peugeot 406 row 3

MODEL: IL-confirmed|Peugeot|406

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "2.0L", "engine_displacement_l": 2.0, "horsepower_hp": 132, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1995, "year_end": 1999, "support_level": "direct", "source_indexes": [0, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L` / `2.0` / `132` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1995-1999` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 406 sedan/estate/coupe 1995/1996-2004 with 1.8/2.0 petrol, 2.0 HDi diesel and 3.0 V6 coupe rows.

SOURCE:
Repo-local Auto/Gear Peugeot 406 sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve coupe and estate body distinctions.

ACTION: KEEP

### VARIANT 92 — Peugeot 406 row 4

MODEL: IL-confirmed|Peugeot|406

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "2.0L", "engine_displacement_l": 2.0, "horsepower_hp": 136, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1999, "year_end": 2004, "support_level": "direct", "source_indexes": [0, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L` / `2.0` / `136` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1999-2004` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 406 sedan/estate/coupe 1995/1996-2004 with 1.8/2.0 petrol, 2.0 HDi diesel and 3.0 V6 coupe rows.

SOURCE:
Repo-local Auto/Gear Peugeot 406 sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve coupe and estate body distinctions.

ACTION: KEEP

### VARIANT 93 — Peugeot 406 row 5

MODEL: IL-confirmed|Peugeot|406

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "diesel", "engine": "2.0L turbo", "engine_displacement_l": 2.0, "horsepower_hp": 109, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1999, "year_end": 2004, "support_level": "direct", "source_indexes": [0]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `diesel` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L turbo` / `2.0` / `109` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1999-2004` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 406 sedan/estate/coupe 1995/1996-2004 with 1.8/2.0 petrol, 2.0 HDi diesel and 3.0 V6 coupe rows.

SOURCE:
Repo-local Auto/Gear Peugeot 406 sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve coupe and estate body distinctions.

ACTION: KEEP

### VARIANT 94 — Peugeot 406 row 6

MODEL: IL-confirmed|Peugeot|406

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "diesel", "engine": "2.0L turbo", "engine_displacement_l": 2.0, "horsepower_hp": 109, "transmission": "5-speed manual", "drivetrain": "FWD", "year_start": 1999, "year_end": 2004, "support_level": "direct", "source_indexes": [0]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Sedan` — must match Israeli body style/source.
- fuel_type: `diesel` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L turbo` / `2.0` / `109` — must match embedded fact and repo-local source.
- transmission/drivetrain: `5-speed manual` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1999-2004` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 406 sedan/estate/coupe 1995/1996-2004 with 1.8/2.0 petrol, 2.0 HDi diesel and 3.0 V6 coupe rows.

SOURCE:
Repo-local Auto/Gear Peugeot 406 sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve coupe and estate body distinctions.

ACTION: KEEP

### VARIANT 95 — Peugeot 406 row 7

MODEL: IL-confirmed|Peugeot|406

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Estate", "fuel_type": "petrol", "engine": "2.0L", "engine_displacement_l": 2.0, "horsepower_hp": 136, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1999, "year_end": 2004, "support_level": "direct", "source_indexes": [0, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Estate` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L` / `2.0` / `136` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1999-2004` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 406 sedan/estate/coupe 1995/1996-2004 with 1.8/2.0 petrol, 2.0 HDi diesel and 3.0 V6 coupe rows.

SOURCE:
Repo-local Auto/Gear Peugeot 406 sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve coupe and estate body distinctions.

ACTION: KEEP

### VARIANT 96 — Peugeot 406 row 8

MODEL: IL-confirmed|Peugeot|406

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Coupe", "fuel_type": "petrol", "engine": "2.0L", "engine_displacement_l": 2.0, "horsepower_hp": 136, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1999, "year_end": 2004, "support_level": "direct", "source_indexes": [1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Coupe` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `2.0L` / `2.0` / `136` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1999-2004` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 406 sedan/estate/coupe 1995/1996-2004 with 1.8/2.0 petrol, 2.0 HDi diesel and 3.0 V6 coupe rows.

SOURCE:
Repo-local Auto/Gear Peugeot 406 sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve coupe and estate body distinctions.

ACTION: KEEP

### VARIANT 97 — Peugeot 406 row 9

MODEL: IL-confirmed|Peugeot|406

CURRENT VALUE:
```json
{"version_or_trim": null, "body_type": "Coupe", "fuel_type": "petrol", "engine": "3.0L v6", "engine_displacement_l": 3.0, "horsepower_hp": 190, "transmission": "4-speed automatic", "drivetrain": "FWD", "year_start": 1997, "year_end": 1999, "support_level": "direct", "source_indexes": [1]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `None` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Coupe` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `3.0L v6` / `3.0` / `190` — must match embedded fact and repo-local source.
- transmission/drivetrain: `4-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `1997-1999` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Israeli historical sources support Peugeot 406 sedan/estate/coupe 1995/1996-2004 with 1.8/2.0 petrol, 2.0 HDi diesel and 3.0 V6 coupe rows.

SOURCE:
Repo-local Auto/Gear Peugeot 406 sources.

TARGET VALUE:
Keep historical rows; do not currentize. Preserve coupe and estate body distinctions.

ACTION: KEEP

---

## MODEL PROFILE: global-reference-only|Peugeot|408

PROFILE ACTION: MERGE/ARCHIVE NON-BLOCKING + FIX SOURCE INDEX

WEB-VALIDATED FACT: Peugeot 408 is marketed in Israel, but this profile is global-reference-only and has invalid source index. There is an adjacent IL-likely/canonical Peugeot 408 profile in the next run; current Israeli evidence supports 1.2 turbo 130 hp Allure Pack and later 2026 updates should not be fabricated.

SOURCE: Peugeot Online Israel 408 page; Auto.co.il Peugeot 408 2026; Carzone Peugeot 408; repo-local iCar/Cartube sources.

TARGET VALUE / PROFILE ACTION: Do not keep global-reference-only Peugeot 408 as separate clean. Merge/archive non-blocking with lineage into canonical IL Peugeot 408 profile handled in RUN5, or promote only if repo policy resolves canonical in this run. Fix invalid source index [2] if retained temporarily.

### VARIANT 98 — Peugeot 408 row 1

MODEL: global-reference-only|Peugeot|408

CURRENT VALUE:
```json
{"version_or_trim": "Allure Pack", "body_type": "Liftback", "fuel_type": "petrol", "engine": "1.2L turbo", "engine_displacement_l": 1.2, "horsepower_hp": 130, "transmission": "8-speed automatic", "drivetrain": "FWD", "year_start": 2023, "year_end": null, "support_level": "direct", "source_indexes": [1, 2]}
```

PROBLEM:
- Apply the profile-specific problem above plus field-level validation below.
- Check `source_indexes` and `field_sources`; if any source index is outside the profile source array, replace it with valid repo-local indexes or move the row to review.

FIELD-LEVEL AUDIT:
- version_or_trim: `Allure Pack` — validate/normalize per model target; empty trim allowed only if source lacks real trim.
- body_type: `Liftback` — must match Israeli body style/source.
- fuel_type: `petrol` — must match local row; EV rows require displacement null.
- engine/displacement/hp: `1.2L turbo` / `1.2` / `130` — must match embedded fact and repo-local source.
- transmission/drivetrain: `8-speed automatic` / `FWD` — fix robotized/single_speed/FWD/AWD/4WD where target says so.
- years: `2023-None` — historical rows must not be currentized; current rows require local current evidence.

WEB-VALIDATED FACT:
Peugeot 408 is marketed in Israel, but this profile is global-reference-only and has invalid source index. There is an adjacent IL-likely/canonical Peugeot 408 profile in the next run; current Israeli evidence supports 1.2 turbo 130 hp Allure Pack and later 2026 updates should not be fabricated.

SOURCE:
Peugeot Online Israel 408 page; Auto.co.il Peugeot 408 2026; Carzone Peugeot 408; repo-local iCar/Cartube sources.

TARGET VALUE:
Do not keep global-reference-only Peugeot 408 as separate clean. Merge/archive non-blocking with lineage into canonical IL Peugeot 408 profile handled in RUN5, or promote only if repo policy resolves canonical in this run. Fix invalid source index [2] if retained temporarily.

ACTION: MERGE/ARCHIVE NON-BLOCKING + FIX SOURCE INDEX


## Required checks after implementation

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Audit actual generated files, not only console output:

```text
- clean catalog
- data/model_technical_catalog_il.json
- readiness report
- review file/report
- archive file/report
- quality scan output
- compute_resume_state()
- unmatched_output_keys
- active blockers
- cursor/resume state
- duplicate/split alias cleanup
```

Temporary-file cleanup is mandatory:

```text
Before final commit, delete codex_tasks/BATCH27_RUN4_*.md unless the user explicitly asks to keep them.
```

Report:

```text
1. Files changed
2. Exact before/after metrics
3. Confirmation that all 20 profiles and all 99 variants were handled
4. Test results
5. Confirmation that temporary RUN4 instruction files were deleted before final commit
6. Remaining issues, if any
```


---

# BATCH27 RUN 5 — VARIANT-LEVEL CODEX TASK ONLY

Source ZIP: `yeda-vehicle-variant-agent-v3-validation-v2-budgeted-dual-il-trims (23).zip`

Apply **RUN 5 only**. Do not apply RUN 1, RUN 2, RUN 3, RUN 4, FINAL blockers, or any unified batch task.

RUN 5 clean window: clean catalog indices 709-722.

Scope: `IL-likely|Peugeot|408` through `IL-confirmed|Porsche|718 Boxster`.

Profiles: 14.
Technical variants: 33.

## Mandatory Codex rules

Do not browse the internet.

All web-validation facts and target corrections for RUN 5 are embedded in this task file.
Use this task file as the single source of truth for RUN 5.
Do not apply corrections outside RUN 5 except reporting cross-run conflicts such as Peugeot 408 duplicates from RUN 4.
If repo-local evidence conflicts with this task file, report it instead of guessing.
If a variant cannot be grounded with embedded facts or repo-local sources, move it to non-blocking review/archive with `non_blocking=true`, reason, and lineage rather than fabricating clean data.

Temporary-file cleanup is mandatory: before final commit, delete `codex_tasks/BATCH27_RUN5_*.md` unless the user explicitly asks to keep them.

## Required checks after implementation

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Also audit actual generated files: clean catalog, readiness, review, archive, quality scan, compute_resume_state(), unmatched_output_keys, active blockers, cursor/resume state, duplicate/split alias cleanup.

## Local ZIP checks before task generation

- `python -m compileall scripts`: PASS
- `python -m scripts.catalog_validation`: PASS
- `python -m scripts.catalog_quality_scan`: PASS
- `python -m pytest -q`: FAIL due to `ModuleNotFoundError: streamlit` during test collection. Treat as environment/dependency issue unless repo test environment includes streamlit.

## RUN 5 high-risk hotspots

- Peugeot 408: merge RUN4 `global-reference-only|Peugeot|408` into canonical Israeli 408; do not extend 130 hp petrol / 225 hp PHEV as 2026 current when current Israeli fact is 145 hp MHEV GT.
- Peugeot 5008/e-5008: keep one canonical representation with alias/lineage; do not duplicate EV 210 hp under both 5008 and e-5008 clean profiles.
- Peugeot 607: merge/delete global-reference-only duplicate; weak 2.2 petrol row goes to review unless locally grounded.
- Peugeot e-308: not verified clean from one weak Autoboom-style source; move to review/archive unless official/importer evidence exists.
- Peugeot Rifter: 2026 current GT/GT Long 1.5 diesel 130 hp 8AT FWD should be represented; existing row has broken source indexes and stale year_end.
- Polestar 2/3/4: many source indexes are invalid; Polestar official Israel pages currently indicate availability limitations, so year_end/current status must be reviewed rather than assumed.
- Porsche 718 Boxster: do not extend base/S/GTS rows beyond 2024 without official Israel evidence; normalize base null trim.

---

## MODEL PROFILE: IL-likely|Peugeot|408

Profile variants: 2

WEB-VALIDATED MODEL FACT: Peugeot 408 is an Israeli-market model, but the current 2026 Israeli row is 1.2 turbo-petrol micro-hybrid 145 hp GT. The 2023 launch rows of 1.2 turbo 130 hp and PHEV 225 hp should not be silently extended as current 2026 rows. The adjacent global-reference-only 408 from RUN 4 must be merged/archived into this canonical Israeli 408 profile.

MODEL SOURCES: Peugeot Online Israel 408 page; iCar 408 2026 1.2 turbo-petrol micro-hybrid 145 hp GT; Cartube 2023 Israel launch 1.2 turbo 130 hp and PHEV 225 hp historical launch coverage.

### VARIANT 1/2

MODEL: IL-likely|Peugeot|408

CURRENT VALUE: `{"version_or_trim": "Allure", "body_type": "Liftback", "fuel_type": "petrol", "engine": "1.2L turbo", "engine_displacement_l": 1.2, "horsepower_hp": 130, "transmission": "8-speed automatic", "drivetrain": "FWD", "year_start": 2023, "year_end": 2024, "support_level": "direct", "source_indexes": [0, 1]}`

PROBLEM: Profile is IL-likely despite local official/evidence. Need canonical IL-confirmed identity, merge with global-reference-only 408, and split historical 2023-2024 rows from 2026 Hybrid 145 current row.

WEB-VALIDATED FACT: Peugeot 408 is an Israeli-market model, but the current 2026 Israeli row is 1.2 turbo-petrol micro-hybrid 145 hp GT. The 2023 launch rows of 1.2 turbo 130 hp and PHEV 225 hp should not be silently extended as current 2026 rows. The adjacent global-reference-only 408 from RUN 4 must be merged/archived into this canonical Israeli 408 profile. Field-level validation for this row: version_or_trim='Allure'; body_type='Liftback'; fuel_type='petrol'; engine='1.2L turbo'; engine_displacement_l=1.2; horsepower_hp=130; transmission='8-speed automatic'; drivetrain='FWD'; years=2023-2024.

SOURCE: Peugeot Online Israel 408 page; iCar 408 2026 1.2 turbo-petrol micro-hybrid 145 hp GT; Cartube 2023 Israel launch 1.2 turbo 130 hp and PHEV 225 hp historical launch coverage.

TARGET VALUE: Keep as historical 2023-2024 1.2 turbo 130 hp Allure if field_sources valid; do not extend to 2026. Add/split a new 2026 1.2 turbo micro-hybrid 145 hp GT row if repo-local sources support it. Canonicalize profile as IL-confirmed Peugeot 408 and merge RUN4 global-reference-only 408 into it.

ACTION: FIX

---

### VARIANT 2/2

MODEL: IL-likely|Peugeot|408

CURRENT VALUE: `{"version_or_trim": "GT", "body_type": "Liftback", "fuel_type": "plug_in_hybrid", "engine": "1.6L turbo", "engine_displacement_l": 1.6, "horsepower_hp": 225, "transmission": "8-speed automatic", "drivetrain": "FWD", "year_start": 2023, "year_end": 2024, "support_level": "direct", "source_indexes": [0, 1]}`

PROBLEM: Profile is IL-likely despite local official/evidence. Need canonical IL-confirmed identity, merge with global-reference-only 408, and split historical 2023-2024 rows from 2026 Hybrid 145 current row.

WEB-VALIDATED FACT: Peugeot 408 is an Israeli-market model, but the current 2026 Israeli row is 1.2 turbo-petrol micro-hybrid 145 hp GT. The 2023 launch rows of 1.2 turbo 130 hp and PHEV 225 hp should not be silently extended as current 2026 rows. The adjacent global-reference-only 408 from RUN 4 must be merged/archived into this canonical Israeli 408 profile. Field-level validation for this row: version_or_trim='GT'; body_type='Liftback'; fuel_type='plug_in_hybrid'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=225; transmission='8-speed automatic'; drivetrain='FWD'; years=2023-2024.

SOURCE: Peugeot Online Israel 408 page; iCar 408 2026 1.2 turbo-petrol micro-hybrid 145 hp GT; Cartube 2023 Israel launch 1.2 turbo 130 hp and PHEV 225 hp historical launch coverage.

TARGET VALUE: Keep PHEV 225 hp only for locally sourced historical 2023-2024 years; do not mark current 2026 unless a local Peugeot source proves active sale. Canonicalize profile as IL-confirmed.

ACTION: FIX

---


## MODEL PROFILE: IL-likely|Peugeot|5008

Profile variants: 2

WEB-VALIDATED MODEL FACT: Israeli current Peugeot 5008 is grounded as 1.2L mild-hybrid 136 hp FWD and E-5008 electric 210 hp FWD. E-5008 may be marketed as a line but must not duplicate the same technical EV row in two clean profiles without alias/lineage.

MODEL SOURCES: Peugeot Online Israel 5008 and E-5008 pages; Auto/iCar Israeli 5008/E-5008 pages.

### VARIANT 1/2

MODEL: IL-likely|Peugeot|5008

CURRENT VALUE: `{"version_or_trim": null, "body_type": "SUV", "fuel_type": "mild_hybrid", "engine": "1.2L turbo", "engine_displacement_l": 1.2, "horsepower_hp": 136, "transmission": "6-speed dual_clutch", "drivetrain": "FWD", "year_start": 2025, "year_end": 2026, "support_level": "indirect", "source_indexes": [0, 1, 2, 3, 4]}`

PROBLEM: Profile is IL-likely but is locally marketed; needs IL-confirmed canonical handling and merge/alias with separate e-5008 profile.

WEB-VALIDATED FACT: Israeli current Peugeot 5008 is grounded as 1.2L mild-hybrid 136 hp FWD and E-5008 electric 210 hp FWD. E-5008 may be marketed as a line but must not duplicate the same technical EV row in two clean profiles without alias/lineage. Field-level validation for this row: version_or_trim=None; body_type='SUV'; fuel_type='mild_hybrid'; engine='1.2L turbo'; engine_displacement_l=1.2; horsepower_hp=136; transmission='6-speed dual_clutch'; drivetrain='FWD'; years=2025-2026.

SOURCE: Peugeot Online Israel 5008 and E-5008 pages; Auto/iCar Israeli 5008/E-5008 pages.

TARGET VALUE: Keep/currentize as IL-confirmed Peugeot 5008 MHEV 136 hp FWD; normalize trim/lineage if local sources expose Allure/GT, otherwise keep null trim with reason.

ACTION: FIX

---

### VARIANT 2/2

MODEL: IL-likely|Peugeot|5008

CURRENT VALUE: `{"version_or_trim": "GT", "body_type": "SUV", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 210, "transmission": "single_speed", "drivetrain": "FWD", "year_start": 2025, "year_end": 2026, "support_level": "indirect", "source_indexes": [0, 1, 2, 5, 6]}`

PROBLEM: Profile is IL-likely but is locally marketed; needs IL-confirmed canonical handling and merge/alias with separate e-5008 profile.

WEB-VALIDATED FACT: Israeli current Peugeot 5008 is grounded as 1.2L mild-hybrid 136 hp FWD and E-5008 electric 210 hp FWD. E-5008 may be marketed as a line but must not duplicate the same technical EV row in two clean profiles without alias/lineage. Field-level validation for this row: version_or_trim='GT'; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=210; transmission='single_speed'; drivetrain='FWD'; years=2025-2026. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=FWD.

SOURCE: Peugeot Online Israel 5008 and E-5008 pages; Auto/iCar Israeli 5008/E-5008 pages.

TARGET VALUE: Keep this EV technical row only once, preferably under canonical Peugeot 5008 with e-5008 alias/lineage. Do not leave duplicate e-5008 profile plus 5008 EV row.

ACTION: MERGE

---


## MODEL PROFILE: IL-confirmed|Peugeot|607

Profile variants: 1

WEB-VALIDATED MODEL FACT: Israeli-market evidence supports Peugeot 607 3.0 V6 around 2001-2008 with approximately 2946 cc and 211 hp. It is historical, not current.

MODEL SOURCES: iCar Peugeot 607 Israeli pages; Autoboom Israel 607 technical listing.

### VARIANT 1/1

MODEL: IL-confirmed|Peugeot|607

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "3.0L v6", "engine_displacement_l": 2.946, "horsepower_hp": 211, "transmission": "6-speed automatic", "drivetrain": "FWD", "year_start": 2001, "year_end": 2008, "support_level": "indirect", "source_indexes": [0, 1]}`

PROBLEM: Confirmed profile is mostly correct but the null trim hides engine-line identity; adjacent global-reference-only 607 duplicates/weakly adds rows and must be resolved.

WEB-VALIDATED FACT: Israeli-market evidence supports Peugeot 607 3.0 V6 around 2001-2008 with approximately 2946 cc and 211 hp. It is historical, not current. Field-level validation for this row: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L v6'; engine_displacement_l=2.946; horsepower_hp=211; transmission='6-speed automatic'; drivetrain='FWD'; years=2001-2008.

SOURCE: iCar Peugeot 607 Israeli pages; Autoboom Israel 607 technical listing.

TARGET VALUE: Keep historical 3.0 V6 row; normalize version_or_trim from null to 3.0 V6 if schema policy allows, and keep year_end 2008.

ACTION: FIX

---


## MODEL PROFILE: global-reference-only|Peugeot|607

Profile variants: 2

WEB-VALIDATED MODEL FACT: Global/weak 607 profile must not remain a separate clean profile when an IL-confirmed 607 exists. The 3.0 V6 row duplicates the confirmed 3.0 V6 but with 210 instead of 211 hp; the 2.2 petrol row needs stronger Israeli grounding before clean.

MODEL SOURCES: Wheel nostalgia article and Israeli secondary 607 pages; compare against IL-confirmed Peugeot 607.

### VARIANT 1/2

MODEL: global-reference-only|Peugeot|607

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "2.2L", "engine_displacement_l": 2.2, "horsepower_hp": 160, "transmission": "automatic", "drivetrain": "FWD", "year_start": 2000, "year_end": 2008, "support_level": "direct", "source_indexes": [0]}`

PROBLEM: Separate global-reference-only clean profile causes duplicate/split identity and weak field grounding.

WEB-VALIDATED FACT: Global/weak 607 profile must not remain a separate clean profile when an IL-confirmed 607 exists. The 3.0 V6 row duplicates the confirmed 3.0 V6 but with 210 instead of 211 hp; the 2.2 petrol row needs stronger Israeli grounding before clean. Field-level validation for this row: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.2L'; engine_displacement_l=2.2; horsepower_hp=160; transmission='automatic'; drivetrain='FWD'; years=2000-2008.

SOURCE: Wheel nostalgia article and Israeli secondary 607 pages; compare against IL-confirmed Peugeot 607.

TARGET VALUE: Move 2.2 petrol row to non-blocking review/archive unless repo-local Israeli source proves sale and technical fields. Do not keep global-reference-only clean.

ACTION: MOVE TO REVIEW

---

### VARIANT 2/2

MODEL: global-reference-only|Peugeot|607

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Sedan", "fuel_type": "petrol", "engine": "3.0L v6", "engine_displacement_l": 3, "horsepower_hp": 210, "transmission": "automatic", "drivetrain": "FWD", "year_start": 2000, "year_end": 2008, "support_level": "direct", "source_indexes": [0]}`

PROBLEM: Separate global-reference-only clean profile causes duplicate/split identity and weak field grounding.

WEB-VALIDATED FACT: Global/weak 607 profile must not remain a separate clean profile when an IL-confirmed 607 exists. The 3.0 V6 row duplicates the confirmed 3.0 V6 but with 210 instead of 211 hp; the 2.2 petrol row needs stronger Israeli grounding before clean. Field-level validation for this row: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L v6'; engine_displacement_l=3; horsepower_hp=210; transmission='automatic'; drivetrain='FWD'; years=2000-2008.

SOURCE: Wheel nostalgia article and Israeli secondary 607 pages; compare against IL-confirmed Peugeot 607.

TARGET VALUE: Merge/delete duplicate into IL-confirmed Peugeot 607 3.0 V6; target displacement 2.946L and horsepower 211 hp, not a separate 210 hp clean row.

ACTION: MERGE

---


## MODEL PROFILE: IL-confirmed|Peugeot|Boxer

Profile variants: 4

WEB-VALIDATED MODEL FACT: Peugeot Boxer is current in Israel with 2.2 diesel rows: 140 hp manual and 180 hp automatic, with van and chassis/workbody configurations. Use repo-valid body type mapping for chassis-cab/open-bed rows if schema lacks chassis-cab.

MODEL SOURCES: Peugeot Online Israel Boxer page; iCar/Carzone/Auto 2026 Boxer pages.

### VARIANT 1/4

MODEL: IL-confirmed|Peugeot|Boxer

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Van", "fuel_type": "diesel", "engine": "2.2L turbo", "engine_displacement_l": 2.2, "horsepower_hp": 140, "transmission": "6-speed manual", "drivetrain": "FWD", "year_start": 2021, "year_end": 2026, "support_level": "direct", "source_indexes": [0, 1, 2, 3]}`

PROBLEM: Rows are directionally correct but must keep current source_indexes/field_sources and avoid unsupported body labels. Null trim may be acceptable only if dimensions/body configuration are tracked elsewhere; otherwise normalize L2H2/L3H2/single-cab/double-cab lineage.

WEB-VALIDATED FACT: Peugeot Boxer is current in Israel with 2.2 diesel rows: 140 hp manual and 180 hp automatic, with van and chassis/workbody configurations. Use repo-valid body type mapping for chassis-cab/open-bed rows if schema lacks chassis-cab. Field-level validation for this row: version_or_trim=None; body_type='Van'; fuel_type='diesel'; engine='2.2L turbo'; engine_displacement_l=2.2; horsepower_hp=140; transmission='6-speed manual'; drivetrain='FWD'; years=2021-2026.

SOURCE: Peugeot Online Israel Boxer page; iCar/Carzone/Auto 2026 Boxer pages.

TARGET VALUE: Keep Israeli current Boxer row but repair field_sources/source_indexes to include current official/2026 local sources; normalize body/trim lineage for Van vs chassis-cab/pickup rows.

ACTION: FIX

---

### VARIANT 2/4

MODEL: IL-confirmed|Peugeot|Boxer

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Van", "fuel_type": "diesel", "engine": "2.2L turbo", "engine_displacement_l": 2.2, "horsepower_hp": 180, "transmission": "8-speed automatic", "drivetrain": "FWD", "year_start": 2025, "year_end": 2026, "support_level": "direct", "source_indexes": [0, 1, 4, 5]}`

PROBLEM: Rows are directionally correct but must keep current source_indexes/field_sources and avoid unsupported body labels. Null trim may be acceptable only if dimensions/body configuration are tracked elsewhere; otherwise normalize L2H2/L3H2/single-cab/double-cab lineage.

WEB-VALIDATED FACT: Peugeot Boxer is current in Israel with 2.2 diesel rows: 140 hp manual and 180 hp automatic, with van and chassis/workbody configurations. Use repo-valid body type mapping for chassis-cab/open-bed rows if schema lacks chassis-cab. Field-level validation for this row: version_or_trim=None; body_type='Van'; fuel_type='diesel'; engine='2.2L turbo'; engine_displacement_l=2.2; horsepower_hp=180; transmission='8-speed automatic'; drivetrain='FWD'; years=2025-2026.

SOURCE: Peugeot Online Israel Boxer page; iCar/Carzone/Auto 2026 Boxer pages.

TARGET VALUE: Keep Israeli current Boxer row but repair field_sources/source_indexes to include current official/2026 local sources; normalize body/trim lineage for Van vs chassis-cab/pickup rows.

ACTION: FIX

---

### VARIANT 3/4

MODEL: IL-confirmed|Peugeot|Boxer

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Pickup", "fuel_type": "diesel", "engine": "2.2L turbo", "engine_displacement_l": 2.2, "horsepower_hp": 140, "transmission": "6-speed manual", "drivetrain": "FWD", "year_start": 2022, "year_end": 2026, "support_level": "direct", "source_indexes": [0, 1, 6, 7, 8]}`

PROBLEM: Rows are directionally correct but must keep current source_indexes/field_sources and avoid unsupported body labels. Null trim may be acceptable only if dimensions/body configuration are tracked elsewhere; otherwise normalize L2H2/L3H2/single-cab/double-cab lineage.

WEB-VALIDATED FACT: Peugeot Boxer is current in Israel with 2.2 diesel rows: 140 hp manual and 180 hp automatic, with van and chassis/workbody configurations. Use repo-valid body type mapping for chassis-cab/open-bed rows if schema lacks chassis-cab. Field-level validation for this row: version_or_trim=None; body_type='Pickup'; fuel_type='diesel'; engine='2.2L turbo'; engine_displacement_l=2.2; horsepower_hp=140; transmission='6-speed manual'; drivetrain='FWD'; years=2022-2026.

SOURCE: Peugeot Online Israel Boxer page; iCar/Carzone/Auto 2026 Boxer pages.

TARGET VALUE: Keep Israeli current Boxer row but repair field_sources/source_indexes to include current official/2026 local sources; normalize body/trim lineage for Van vs chassis-cab/pickup rows.

ACTION: FIX

---

### VARIANT 4/4

MODEL: IL-confirmed|Peugeot|Boxer

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Pickup", "fuel_type": "diesel", "engine": "2.2L turbo", "engine_displacement_l": 2.2, "horsepower_hp": 180, "transmission": "8-speed automatic", "drivetrain": "FWD", "year_start": 2025, "year_end": 2026, "support_level": "direct", "source_indexes": [0, 1, 8, 9]}`

PROBLEM: Rows are directionally correct but must keep current source_indexes/field_sources and avoid unsupported body labels. Null trim may be acceptable only if dimensions/body configuration are tracked elsewhere; otherwise normalize L2H2/L3H2/single-cab/double-cab lineage.

WEB-VALIDATED FACT: Peugeot Boxer is current in Israel with 2.2 diesel rows: 140 hp manual and 180 hp automatic, with van and chassis/workbody configurations. Use repo-valid body type mapping for chassis-cab/open-bed rows if schema lacks chassis-cab. Field-level validation for this row: version_or_trim=None; body_type='Pickup'; fuel_type='diesel'; engine='2.2L turbo'; engine_displacement_l=2.2; horsepower_hp=180; transmission='8-speed automatic'; drivetrain='FWD'; years=2025-2026.

SOURCE: Peugeot Online Israel Boxer page; iCar/Carzone/Auto 2026 Boxer pages.

TARGET VALUE: Keep Israeli current Boxer row but repair field_sources/source_indexes to include current official/2026 local sources; normalize body/trim lineage for Van vs chassis-cab/pickup rows.

ACTION: FIX

---


## MODEL PROFILE: IL-likely|Peugeot|e-308

Profile variants: 1

WEB-VALIDATED MODEL FACT: The e-308 row is not sufficiently grounded for verified-clean Israeli catalog if only Autoboom/global-style source exists. It should be review/archive non-blocking unless repo-local official/importer evidence proves Israeli sale.

MODEL SOURCES: Autoboom e-308 Israeli listing only in current repo; no strong official Peugeot Israel current sales page embedded for this row in the task context.

### VARIANT 1/1

MODEL: IL-likely|Peugeot|e-308

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Hatchback", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 156, "transmission": "single_speed", "drivetrain": "FWD", "year_start": 2021, "year_end": null, "support_level": "indirect", "source_indexes": [0]}`

PROBLEM: IL-likely clean row is supported by weak single-source evidence only.

WEB-VALIDATED FACT: The e-308 row is not sufficiently grounded for verified-clean Israeli catalog if only Autoboom/global-style source exists. It should be review/archive non-blocking unless repo-local official/importer evidence proves Israeli sale. Field-level validation for this row: version_or_trim=None; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=156; transmission='single_speed'; drivetrain='FWD'; years=2021-None. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=FWD.

SOURCE: Autoboom e-308 Israeli listing only in current repo; no strong official Peugeot Israel current sales page embedded for this row in the task context.

TARGET VALUE: Move to non-blocking review/archive unless repo-local official/importer evidence proves Israeli e-308 sale. If kept, merge/alias under Peugeot 308 electric lineage and keep EV schema valid.

ACTION: MOVE TO REVIEW

---


## MODEL PROFILE: IL-likely|Peugeot|e-5008

Profile variants: 1

WEB-VALIDATED MODEL FACT: E-5008 is Israeli-market current as electric 210 hp FWD with 73 kWh battery. But the same EV row already exists inside Peugeot 5008; keep one canonical representation with alias/lineage rather than duplicate clean profiles.

MODEL SOURCES: Peugeot Online Israel E-5008 page; Auto/iCar/Carzone Israeli E-5008 pages.

### VARIANT 1/1

MODEL: IL-likely|Peugeot|e-5008

CURRENT VALUE: `{"version_or_trim": null, "body_type": "SUV", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 210, "transmission": "single_speed", "drivetrain": "FWD", "year_start": 2025, "year_end": 2026, "support_level": "indirect", "source_indexes": [0, 1, 2, 3, 4, 5]}`

PROBLEM: Separate e-5008 clean profile duplicates the EV technical row under Peugeot 5008.

WEB-VALIDATED FACT: E-5008 is Israeli-market current as electric 210 hp FWD with 73 kWh battery. But the same EV row already exists inside Peugeot 5008; keep one canonical representation with alias/lineage rather than duplicate clean profiles. Field-level validation for this row: version_or_trim=None; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=210; transmission='single_speed'; drivetrain='FWD'; years=2025-2026. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=FWD.

SOURCE: Peugeot Online Israel E-5008 page; Auto/iCar/Carzone Israeli E-5008 pages.

TARGET VALUE: Merge into canonical Peugeot 5008 EV/e-5008 lineage; do not leave duplicate clean profile.

ACTION: MERGE

---


## MODEL PROFILE: IL-confirmed|Peugeot|Expert

Profile variants: 3

WEB-VALIDATED MODEL FACT: Israeli evidence supports historical Expert 2.0 diesel 120/163 hp 2007-2013 and e-Expert XL electric 136 hp in 2023-2024. Current 2026 diesel Expert must not be invented unless repo-local source supports it.

MODEL SOURCES: Autoboom Israel Expert generation pages; Carzone 2023 e-Expert page.

### VARIANT 1/3

MODEL: IL-confirmed|Peugeot|Expert

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Van", "fuel_type": "diesel", "engine": "2.0L turbo", "engine_displacement_l": 2, "horsepower_hp": 120, "transmission": "6-speed manual", "drivetrain": "FWD", "year_start": 2007, "year_end": 2013, "support_level": "direct", "source_indexes": [0, 1]}`

PROBLEM: One source_index combination is wrong/reversed; EV schema is directionally valid but must keep single_speed/direct_drive-style schema and displacement null.

WEB-VALIDATED FACT: Israeli evidence supports historical Expert 2.0 diesel 120/163 hp 2007-2013 and e-Expert XL electric 136 hp in 2023-2024. Current 2026 diesel Expert must not be invented unless repo-local source supports it. Field-level validation for this row: version_or_trim=None; body_type='Van'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2; horsepower_hp=120; transmission='6-speed manual'; drivetrain='FWD'; years=2007-2013.

SOURCE: Autoboom Israel Expert generation pages; Carzone 2023 e-Expert page.

TARGET VALUE: Keep row with valid historical/EV schema; for EV keep displacement null and single_speed/direct_drive style transmission. Do not currentize beyond 2024 without new local evidence.

ACTION: KEEP

---

### VARIANT 2/3

MODEL: IL-confirmed|Peugeot|Expert

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Van", "fuel_type": "diesel", "engine": "2.0L turbo", "engine_displacement_l": 2, "horsepower_hp": 163, "transmission": "6-speed manual", "drivetrain": "FWD", "year_start": 2007, "year_end": 2013, "support_level": "direct", "source_indexes": [2, 1]}`

PROBLEM: One source_index combination is wrong/reversed; EV schema is directionally valid but must keep single_speed/direct_drive-style schema and displacement null.

WEB-VALIDATED FACT: Israeli evidence supports historical Expert 2.0 diesel 120/163 hp 2007-2013 and e-Expert XL electric 136 hp in 2023-2024. Current 2026 diesel Expert must not be invented unless repo-local source supports it. Field-level validation for this row: version_or_trim=None; body_type='Van'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2; horsepower_hp=163; transmission='6-speed manual'; drivetrain='FWD'; years=2007-2013.

SOURCE: Autoboom Israel Expert generation pages; Carzone 2023 e-Expert page.

TARGET VALUE: Keep historical 2.0 diesel 163 hp but fix source_indexes/field_sources to point to the 163 hp source, not the 120 hp source.

ACTION: FIX

---

### VARIANT 3/3

MODEL: IL-confirmed|Peugeot|Expert

CURRENT VALUE: `{"version_or_trim": "XL", "body_type": "Van", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 136, "transmission": "single_speed", "drivetrain": "FWD", "year_start": 2023, "year_end": 2024, "support_level": "indirect", "source_indexes": [3, 4]}`

PROBLEM: One source_index combination is wrong/reversed; EV schema is directionally valid but must keep single_speed/direct_drive-style schema and displacement null.

WEB-VALIDATED FACT: Israeli evidence supports historical Expert 2.0 diesel 120/163 hp 2007-2013 and e-Expert XL electric 136 hp in 2023-2024. Current 2026 diesel Expert must not be invented unless repo-local source supports it. Field-level validation for this row: version_or_trim='XL'; body_type='Van'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=136; transmission='single_speed'; drivetrain='FWD'; years=2023-2024. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=FWD.

SOURCE: Autoboom Israel Expert generation pages; Carzone 2023 e-Expert page.

TARGET VALUE: Keep row with valid historical/EV schema; for EV keep displacement null and single_speed/direct_drive style transmission. Do not currentize beyond 2024 without new local evidence.

ACTION: FIX

---


## MODEL PROFILE: IL-confirmed|Peugeot|RCZ

Profile variants: 2

WEB-VALIDATED MODEL FACT: Peugeot RCZ sold in Israel historically around 2010-2015 with 1.6 turbo 156 hp automatic and 200 hp manual. It is not current. Source indexes in current row are invalid because they point beyond local sources length.

MODEL SOURCES: iCar Israel RCZ page; Auto.co.il Peugeot RCZ 2010-2015 technical page; Cartube launch article.

### VARIANT 1/2

MODEL: IL-confirmed|Peugeot|RCZ

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Coupe", "fuel_type": "petrol", "engine": "1.6L turbo", "engine_displacement_l": 1.6, "horsepower_hp": 156, "transmission": "6-speed automatic", "drivetrain": "FWD", "year_start": 2010, "year_end": 2015, "support_level": "direct", "source_indexes": [1, 2]}`

PROBLEM: Data fields are directionally correct but source_indexes/field_sources are broken and must be repaired. Additional source-index defect: source_indexes [1, 2] contain invalid ids for profile source count 2.

WEB-VALIDATED FACT: Peugeot RCZ sold in Israel historically around 2010-2015 with 1.6 turbo 156 hp automatic and 200 hp manual. It is not current. Source indexes in current row are invalid because they point beyond local sources length. Field-level validation for this row: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=156; transmission='6-speed automatic'; drivetrain='FWD'; years=2010-2015.

SOURCE: iCar Israel RCZ page; Auto.co.il Peugeot RCZ 2010-2015 technical page; Cartube launch article.

TARGET VALUE: Keep historical RCZ row but fix source_indexes/field_sources from invalid [1,2] to valid local indexes [0,1].

ACTION: FIX

---

### VARIANT 2/2

MODEL: IL-confirmed|Peugeot|RCZ

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Coupe", "fuel_type": "petrol", "engine": "1.6L turbo", "engine_displacement_l": 1.6, "horsepower_hp": 200, "transmission": "6-speed manual", "drivetrain": "FWD", "year_start": 2010, "year_end": 2015, "support_level": "direct", "source_indexes": [1, 2]}`

PROBLEM: Data fields are directionally correct but source_indexes/field_sources are broken and must be repaired. Additional source-index defect: source_indexes [1, 2] contain invalid ids for profile source count 2.

WEB-VALIDATED FACT: Peugeot RCZ sold in Israel historically around 2010-2015 with 1.6 turbo 156 hp automatic and 200 hp manual. It is not current. Source indexes in current row are invalid because they point beyond local sources length. Field-level validation for this row: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=200; transmission='6-speed manual'; drivetrain='FWD'; years=2010-2015.

SOURCE: iCar Israel RCZ page; Auto.co.il Peugeot RCZ 2010-2015 technical page; Cartube launch article.

TARGET VALUE: Keep historical RCZ row but fix source_indexes/field_sources from invalid [1,2] to valid local indexes [0,1].

ACTION: FIX

---


## MODEL PROFILE: IL-confirmed|Peugeot|Rifter

Profile variants: 1

WEB-VALIDATED MODEL FACT: Peugeot Rifter is current again in Israel for 2026 as GT / GT Long, 1.5L turbo-diesel 130 hp, 8-speed automatic, FWD, 5 or 7 seats. Existing row ending 2024 should not remain the only clean representation, and source indexes are invalid.

MODEL SOURCES: iCar/Cartube/Auto/Carzone 2026 Peugeot Rifter Israel launch and price/spec pages.

### VARIANT 1/1

MODEL: IL-confirmed|Peugeot|Rifter

CURRENT VALUE: `{"version_or_trim": null, "body_type": "MPV", "fuel_type": "diesel", "engine": "1.5L turbo", "engine_displacement_l": 1.5, "horsepower_hp": 130, "transmission": "8-speed automatic", "drivetrain": "FWD", "year_start": 2019, "year_end": 2024, "support_level": "direct", "source_indexes": [1, 2]}`

PROBLEM: Current row has broken source indexes and outdated year_end; should split/extend to 2026 GT/GT Long if schema supports trim/seat lineage. Additional source-index defect: source_indexes [1, 2] contain invalid ids for profile source count 2.

WEB-VALIDATED FACT: Peugeot Rifter is current again in Israel for 2026 as GT / GT Long, 1.5L turbo-diesel 130 hp, 8-speed automatic, FWD, 5 or 7 seats. Existing row ending 2024 should not remain the only clean representation, and source indexes are invalid. Field-level validation for this row: version_or_trim=None; body_type='MPV'; fuel_type='diesel'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=130; transmission='8-speed automatic'; drivetrain='FWD'; years=2019-2024.

SOURCE: iCar/Cartube/Auto/Carzone 2026 Peugeot Rifter Israel launch and price/spec pages.

TARGET VALUE: Fix source_indexes/field_sources and add/split 2026 GT and GT Long 1.5 diesel 130 hp 8AT FWD rows if repo schema supports trims; otherwise extend with explicit lineage/reason. Do not leave only 2019-2024 outdated row.

ACTION: FIX

---


## MODEL PROFILE: IL-confirmed|Polestar|2

Profile variants: 6

WEB-VALIDATED MODEL FACT: Polestar 2 sold in Israel historically with early FWD 231 hp rows and later RWD/AWD rows: 272 hp SRSM RWD, 299 hp LRSM RWD, 421 hp LRDM AWD, and Performance 476 hp if locally sourced. Current official Polestar Israel page indicates not available for sale, so do not leave open-ended current rows. Existing source_indexes 1660/1662 are invalid.

MODEL SOURCES: Cartube Israel Polestar 2 launch and 2024 update; iCar Polestar 2; Polestar Israel official pages currently say Polestar 2 is not available for sale in Israel.

### VARIANT 1/6

MODEL: IL-confirmed|Polestar|2

CURRENT VALUE: `{"version_or_trim": "Standard Range Single Motor", "body_type": "Liftback", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 231, "transmission": "single_speed", "drivetrain": "FWD", "year_start": 2022, "year_end": 2023, "support_level": "direct", "source_indexes": [1660, 1662]}`

PROBLEM: All six rows have broken source indexes; historical/current boundaries need caution because official Polestar site no longer lists active sale. Additional source-index defect: source_indexes [1660, 1662] contain invalid ids for profile source count 3.

WEB-VALIDATED FACT: Polestar 2 sold in Israel historically with early FWD 231 hp rows and later RWD/AWD rows: 272 hp SRSM RWD, 299 hp LRSM RWD, 421 hp LRDM AWD, and Performance 476 hp if locally sourced. Current official Polestar Israel page indicates not available for sale, so do not leave open-ended current rows. Existing source_indexes 1660/1662 are invalid. Field-level validation for this row: version_or_trim='Standard Range Single Motor'; body_type='Liftback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=231; transmission='single_speed'; drivetrain='FWD'; years=2022-2023. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=FWD.

SOURCE: Cartube Israel Polestar 2 launch and 2024 update; iCar Polestar 2; Polestar Israel official pages currently say Polestar 2 is not available for sale in Israel.

TARGET VALUE: Keep as historical Israeli Polestar 2 row but repair invalid source_indexes 1660/1662 to valid local source ids. Do not leave year_end null/current without official availability evidence.

ACTION: FIX

---

### VARIANT 2/6

MODEL: IL-confirmed|Polestar|2

CURRENT VALUE: `{"version_or_trim": "Long Range Single Motor", "body_type": "Liftback", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 231, "transmission": "single_speed", "drivetrain": "FWD", "year_start": 2022, "year_end": 2023, "support_level": "direct", "source_indexes": [1660, 1662]}`

PROBLEM: All six rows have broken source indexes; historical/current boundaries need caution because official Polestar site no longer lists active sale. Additional source-index defect: source_indexes [1660, 1662] contain invalid ids for profile source count 3.

WEB-VALIDATED FACT: Polestar 2 sold in Israel historically with early FWD 231 hp rows and later RWD/AWD rows: 272 hp SRSM RWD, 299 hp LRSM RWD, 421 hp LRDM AWD, and Performance 476 hp if locally sourced. Current official Polestar Israel page indicates not available for sale, so do not leave open-ended current rows. Existing source_indexes 1660/1662 are invalid. Field-level validation for this row: version_or_trim='Long Range Single Motor'; body_type='Liftback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=231; transmission='single_speed'; drivetrain='FWD'; years=2022-2023. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=FWD.

SOURCE: Cartube Israel Polestar 2 launch and 2024 update; iCar Polestar 2; Polestar Israel official pages currently say Polestar 2 is not available for sale in Israel.

TARGET VALUE: Keep as historical Israeli Polestar 2 row but repair invalid source_indexes 1660/1662 to valid local source ids. Do not leave year_end null/current without official availability evidence.

ACTION: FIX

---

### VARIANT 3/6

MODEL: IL-confirmed|Polestar|2

CURRENT VALUE: `{"version_or_trim": "Long Range Dual Motor", "body_type": "Liftback", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 408, "transmission": "single_speed", "drivetrain": "AWD", "year_start": 2022, "year_end": 2023, "support_level": "direct", "source_indexes": [1660, 1662]}`

PROBLEM: All six rows have broken source indexes; historical/current boundaries need caution because official Polestar site no longer lists active sale. Additional source-index defect: source_indexes [1660, 1662] contain invalid ids for profile source count 3.

WEB-VALIDATED FACT: Polestar 2 sold in Israel historically with early FWD 231 hp rows and later RWD/AWD rows: 272 hp SRSM RWD, 299 hp LRSM RWD, 421 hp LRDM AWD, and Performance 476 hp if locally sourced. Current official Polestar Israel page indicates not available for sale, so do not leave open-ended current rows. Existing source_indexes 1660/1662 are invalid. Field-level validation for this row: version_or_trim='Long Range Dual Motor'; body_type='Liftback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=408; transmission='single_speed'; drivetrain='AWD'; years=2022-2023. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=AWD.

SOURCE: Cartube Israel Polestar 2 launch and 2024 update; iCar Polestar 2; Polestar Israel official pages currently say Polestar 2 is not available for sale in Israel.

TARGET VALUE: Keep as historical Israeli Polestar 2 row but repair invalid source_indexes 1660/1662 to valid local source ids. Do not leave year_end null/current without official availability evidence.

ACTION: FIX

---

### VARIANT 4/6

MODEL: IL-confirmed|Polestar|2

CURRENT VALUE: `{"version_or_trim": "Standard Range Single Motor", "body_type": "Liftback", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 272, "transmission": "single_speed", "drivetrain": "RWD", "year_start": 2023, "year_end": 2024, "support_level": "direct", "source_indexes": [1661, 1662]}`

PROBLEM: All six rows have broken source indexes; historical/current boundaries need caution because official Polestar site no longer lists active sale. Additional source-index defect: source_indexes [1661, 1662] contain invalid ids for profile source count 3.

WEB-VALIDATED FACT: Polestar 2 sold in Israel historically with early FWD 231 hp rows and later RWD/AWD rows: 272 hp SRSM RWD, 299 hp LRSM RWD, 421 hp LRDM AWD, and Performance 476 hp if locally sourced. Current official Polestar Israel page indicates not available for sale, so do not leave open-ended current rows. Existing source_indexes 1660/1662 are invalid. Field-level validation for this row: version_or_trim='Standard Range Single Motor'; body_type='Liftback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=272; transmission='single_speed'; drivetrain='RWD'; years=2023-2024. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=RWD.

SOURCE: Cartube Israel Polestar 2 launch and 2024 update; iCar Polestar 2; Polestar Israel official pages currently say Polestar 2 is not available for sale in Israel.

TARGET VALUE: Keep as historical Israeli Polestar 2 row but repair invalid source_indexes 1660/1662 to valid local source ids. Do not leave year_end null/current without official availability evidence.

ACTION: FIX

---

### VARIANT 5/6

MODEL: IL-confirmed|Polestar|2

CURRENT VALUE: `{"version_or_trim": "Long Range Single Motor", "body_type": "Liftback", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 299, "transmission": "single_speed", "drivetrain": "RWD", "year_start": 2023, "year_end": 2024, "support_level": "direct", "source_indexes": [1661, 1662]}`

PROBLEM: All six rows have broken source indexes; historical/current boundaries need caution because official Polestar site no longer lists active sale. Additional source-index defect: source_indexes [1661, 1662] contain invalid ids for profile source count 3.

WEB-VALIDATED FACT: Polestar 2 sold in Israel historically with early FWD 231 hp rows and later RWD/AWD rows: 272 hp SRSM RWD, 299 hp LRSM RWD, 421 hp LRDM AWD, and Performance 476 hp if locally sourced. Current official Polestar Israel page indicates not available for sale, so do not leave open-ended current rows. Existing source_indexes 1660/1662 are invalid. Field-level validation for this row: version_or_trim='Long Range Single Motor'; body_type='Liftback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=299; transmission='single_speed'; drivetrain='RWD'; years=2023-2024. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=RWD.

SOURCE: Cartube Israel Polestar 2 launch and 2024 update; iCar Polestar 2; Polestar Israel official pages currently say Polestar 2 is not available for sale in Israel.

TARGET VALUE: Keep as historical Israeli Polestar 2 row but repair invalid source_indexes 1660/1662 to valid local source ids. Do not leave year_end null/current without official availability evidence.

ACTION: FIX

---

### VARIANT 6/6

MODEL: IL-confirmed|Polestar|2

CURRENT VALUE: `{"version_or_trim": "Long Range Dual Motor", "body_type": "Liftback", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 421, "transmission": "single_speed", "drivetrain": "AWD", "year_start": 2023, "year_end": 2024, "support_level": "direct", "source_indexes": [1661, 1662]}`

PROBLEM: All six rows have broken source indexes; historical/current boundaries need caution because official Polestar site no longer lists active sale. Additional source-index defect: source_indexes [1661, 1662] contain invalid ids for profile source count 3.

WEB-VALIDATED FACT: Polestar 2 sold in Israel historically with early FWD 231 hp rows and later RWD/AWD rows: 272 hp SRSM RWD, 299 hp LRSM RWD, 421 hp LRDM AWD, and Performance 476 hp if locally sourced. Current official Polestar Israel page indicates not available for sale, so do not leave open-ended current rows. Existing source_indexes 1660/1662 are invalid. Field-level validation for this row: version_or_trim='Long Range Dual Motor'; body_type='Liftback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=421; transmission='single_speed'; drivetrain='AWD'; years=2023-2024. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=AWD.

SOURCE: Cartube Israel Polestar 2 launch and 2024 update; iCar Polestar 2; Polestar Israel official pages currently say Polestar 2 is not available for sale in Israel.

TARGET VALUE: Keep as historical Israeli Polestar 2 row but repair invalid source_indexes 1660/1662 to valid local source ids. Do not leave year_end null/current without official availability evidence.

ACTION: FIX

---


## MODEL PROFILE: IL-confirmed|Polestar|3

Profile variants: 2

WEB-VALIDATED MODEL FACT: Polestar 3 launched in Israel with Long Range Dual Motor 489 hp and Performance 517 hp AWD. If official local availability now says not available, year_end=null/current must be reviewed rather than assumed current 2026.

MODEL SOURCES: Cartube Israel Polestar 3 launch; Auto.co.il Polestar 3; Polestar global/Israel official technical pages; Polestar Israel current availability note.

### VARIANT 1/2

MODEL: IL-confirmed|Polestar|3

CURRENT VALUE: `{"version_or_trim": "Long Range Dual Motor", "body_type": "SUV", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 489, "transmission": "single_speed", "drivetrain": "AWD", "year_start": 2024, "year_end": null, "support_level": "direct", "source_indexes": [0, 1]}`

PROBLEM: Fields are plausible but open-ended year_end is not safe without active local sale evidence.

WEB-VALIDATED FACT: Polestar 3 launched in Israel with Long Range Dual Motor 489 hp and Performance 517 hp AWD. If official local availability now says not available, year_end=null/current must be reviewed rather than assumed current 2026. Field-level validation for this row: version_or_trim='Long Range Dual Motor'; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=489; transmission='single_speed'; drivetrain='AWD'; years=2024-None. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=AWD.

SOURCE: Cartube Israel Polestar 3 launch; Auto.co.il Polestar 3; Polestar global/Israel official technical pages; Polestar Israel current availability note.

TARGET VALUE: Keep Israeli launch rows but set/review year_end/current status according to repo-local evidence; open-ended null year_end is not safe if official Polestar Israel says not available.

ACTION: FIX

---

### VARIANT 2/2

MODEL: IL-confirmed|Polestar|3

CURRENT VALUE: `{"version_or_trim": "Long Range Dual Motor Performance", "body_type": "SUV", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 517, "transmission": "single_speed", "drivetrain": "AWD", "year_start": 2024, "year_end": null, "support_level": "direct", "source_indexes": [0, 1]}`

PROBLEM: Fields are plausible but open-ended year_end is not safe without active local sale evidence.

WEB-VALIDATED FACT: Polestar 3 launched in Israel with Long Range Dual Motor 489 hp and Performance 517 hp AWD. If official local availability now says not available, year_end=null/current must be reviewed rather than assumed current 2026. Field-level validation for this row: version_or_trim='Long Range Dual Motor Performance'; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=517; transmission='single_speed'; drivetrain='AWD'; years=2024-None. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=AWD.

SOURCE: Cartube Israel Polestar 3 launch; Auto.co.il Polestar 3; Polestar global/Israel official technical pages; Polestar Israel current availability note.

TARGET VALUE: Keep Israeli launch rows but set/review year_end/current status according to repo-local evidence; open-ended null year_end is not safe if official Polestar Israel says not available.

ACTION: FIX

---


## MODEL PROFILE: IL-confirmed|Polestar|4

Profile variants: 2

WEB-VALIDATED MODEL FACT: Polestar 4 launch evidence supports Long Range Single Motor 272 hp RWD and Long Range Dual Motor 544 hp AWD. Existing source_indexes [1,2] are invalid for a profile with two sources; active/current availability must be checked against repo-local source.

MODEL SOURCES: Cartube Israel Polestar 4 launch; Polestar official specifications; Polestar Israel current availability note.

### VARIANT 1/2

MODEL: IL-confirmed|Polestar|4

CURRENT VALUE: `{"version_or_trim": "Long Range Single Motor", "body_type": "SUV", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 272, "transmission": "single_speed", "drivetrain": "RWD", "year_start": 2024, "year_end": null, "support_level": "indirect", "source_indexes": [1, 2]}`

PROBLEM: Technical rows are plausible but source indexes are broken and current year_end=null needs policy decision. Additional source-index defect: source_indexes [1, 2] contain invalid ids for profile source count 2.

WEB-VALIDATED FACT: Polestar 4 launch evidence supports Long Range Single Motor 272 hp RWD and Long Range Dual Motor 544 hp AWD. Existing source_indexes [1,2] are invalid for a profile with two sources; active/current availability must be checked against repo-local source. Field-level validation for this row: version_or_trim='Long Range Single Motor'; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=272; transmission='single_speed'; drivetrain='RWD'; years=2024-None. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=RWD.

SOURCE: Cartube Israel Polestar 4 launch; Polestar official specifications; Polestar Israel current availability note.

TARGET VALUE: Keep launch rows only if local evidence supports sale; repair source_indexes [1,2] to valid [0,1] and review year_end/current status.

ACTION: FIX

---

### VARIANT 2/2

MODEL: IL-confirmed|Polestar|4

CURRENT VALUE: `{"version_or_trim": "Long Range Dual Motor", "body_type": "SUV", "fuel_type": "electric", "engine": "electric", "engine_displacement_l": null, "horsepower_hp": 544, "transmission": "single_speed", "drivetrain": "AWD", "year_start": 2024, "year_end": null, "support_level": "indirect", "source_indexes": [1, 2]}`

PROBLEM: Technical rows are plausible but source indexes are broken and current year_end=null needs policy decision. Additional source-index defect: source_indexes [1, 2] contain invalid ids for profile source count 2.

WEB-VALIDATED FACT: Polestar 4 launch evidence supports Long Range Single Motor 272 hp RWD and Long Range Dual Motor 544 hp AWD. Existing source_indexes [1,2] are invalid for a profile with two sources; active/current availability must be checked against repo-local source. Field-level validation for this row: version_or_trim='Long Range Dual Motor'; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=544; transmission='single_speed'; drivetrain='AWD'; years=2024-None. EV schema check: displacement_null=True; transmission=single_speed; drivetrain=AWD.

SOURCE: Cartube Israel Polestar 4 launch; Polestar official specifications; Polestar Israel current availability note.

TARGET VALUE: Keep launch rows only if local evidence supports sale; repair source_indexes [1,2] to valid [0,1] and review year_end/current status.

ACTION: FIX

---


## MODEL PROFILE: IL-confirmed|Porsche|718 Boxster

Profile variants: 4

WEB-VALIDATED MODEL FACT: Israeli evidence supports 718 Boxster/Boxster S/GTS/GTS 4.0 historical/current through the 982 era. Porsche Israel currently highlights 718 family/RS models, but do not extend base Boxster/S/GTS to 2026 unless an official Israel source in repo supports those exact rows. Base null trim should be normalized to Boxster/Base.

MODEL SOURCES: Porsche Israel 718 family pages; Porsche official 718 Boxster model pages; Cartube/iCar Israeli 718 Boxster/GTS coverage.

### VARIANT 1/4

MODEL: IL-confirmed|Porsche|718 Boxster

CURRENT VALUE: `{"version_or_trim": null, "body_type": "Roadster", "fuel_type": "petrol", "engine": "2.0L turbo flat-4", "engine_displacement_l": 2.0, "horsepower_hp": 300, "transmission": "7-speed dual_clutch", "drivetrain": "RWD", "year_start": 2016, "year_end": 2024, "support_level": "direct", "source_indexes": [0, 1, 3]}`

PROBLEM: Rows are mostly technically correct; base row has null trim and current extension beyond 2024 should not be inferred.

WEB-VALIDATED FACT: Israeli evidence supports 718 Boxster/Boxster S/GTS/GTS 4.0 historical/current through the 982 era. Porsche Israel currently highlights 718 family/RS models, but do not extend base Boxster/S/GTS to 2026 unless an official Israel source in repo supports those exact rows. Base null trim should be normalized to Boxster/Base. Field-level validation for this row: version_or_trim=None; body_type='Roadster'; fuel_type='petrol'; engine='2.0L turbo flat-4'; engine_displacement_l=2.0; horsepower_hp=300; transmission='7-speed dual_clutch'; drivetrain='RWD'; years=2016-2024.

SOURCE: Porsche Israel 718 family pages; Porsche official 718 Boxster model pages; Cartube/iCar Israeli 718 Boxster/GTS coverage.

TARGET VALUE: Normalize null trim to Boxster/Base; keep 2016-2024 unless official Israel source proves current sale beyond 2024.

ACTION: FIX

---

### VARIANT 2/4

MODEL: IL-confirmed|Porsche|718 Boxster

CURRENT VALUE: `{"version_or_trim": "S", "body_type": "Roadster", "fuel_type": "petrol", "engine": "2.5L turbo flat-4", "engine_displacement_l": 2.5, "horsepower_hp": 350, "transmission": "7-speed dual_clutch", "drivetrain": "RWD", "year_start": 2016, "year_end": 2024, "support_level": "direct", "source_indexes": [0, 1, 3]}`

PROBLEM: Rows are mostly technically correct; base row has null trim and current extension beyond 2024 should not be inferred.

WEB-VALIDATED FACT: Israeli evidence supports 718 Boxster/Boxster S/GTS/GTS 4.0 historical/current through the 982 era. Porsche Israel currently highlights 718 family/RS models, but do not extend base Boxster/S/GTS to 2026 unless an official Israel source in repo supports those exact rows. Base null trim should be normalized to Boxster/Base. Field-level validation for this row: version_or_trim='S'; body_type='Roadster'; fuel_type='petrol'; engine='2.5L turbo flat-4'; engine_displacement_l=2.5; horsepower_hp=350; transmission='7-speed dual_clutch'; drivetrain='RWD'; years=2016-2024.

SOURCE: Porsche Israel 718 family pages; Porsche official 718 Boxster model pages; Cartube/iCar Israeli 718 Boxster/GTS coverage.

TARGET VALUE: Keep technical row and year range as sourced; do not extend beyond 2024 without official Israel evidence.

ACTION: KEEP

---

### VARIANT 3/4

MODEL: IL-confirmed|Porsche|718 Boxster

CURRENT VALUE: `{"version_or_trim": "GTS", "body_type": "Roadster", "fuel_type": "petrol", "engine": "2.5L turbo flat-4", "engine_displacement_l": 2.5, "horsepower_hp": 365, "transmission": "7-speed dual_clutch", "drivetrain": "RWD", "year_start": 2018, "year_end": 2020, "support_level": "direct", "source_indexes": [0, 2, 3]}`

PROBLEM: Rows are mostly technically correct; base row has null trim and current extension beyond 2024 should not be inferred.

WEB-VALIDATED FACT: Israeli evidence supports 718 Boxster/Boxster S/GTS/GTS 4.0 historical/current through the 982 era. Porsche Israel currently highlights 718 family/RS models, but do not extend base Boxster/S/GTS to 2026 unless an official Israel source in repo supports those exact rows. Base null trim should be normalized to Boxster/Base. Field-level validation for this row: version_or_trim='GTS'; body_type='Roadster'; fuel_type='petrol'; engine='2.5L turbo flat-4'; engine_displacement_l=2.5; horsepower_hp=365; transmission='7-speed dual_clutch'; drivetrain='RWD'; years=2018-2020.

SOURCE: Porsche Israel 718 family pages; Porsche official 718 Boxster model pages; Cartube/iCar Israeli 718 Boxster/GTS coverage.

TARGET VALUE: Keep technical row and year range as sourced; do not extend beyond 2024 without official Israel evidence.

ACTION: KEEP

---

### VARIANT 4/4

MODEL: IL-confirmed|Porsche|718 Boxster

CURRENT VALUE: `{"version_or_trim": "GTS 4.0", "body_type": "Roadster", "fuel_type": "petrol", "engine": "4.0L naturally aspirated flat-6", "engine_displacement_l": 4.0, "horsepower_hp": 400, "transmission": "7-speed dual_clutch", "drivetrain": "RWD", "year_start": 2020, "year_end": 2024, "support_level": "direct", "source_indexes": [0, 3, 4]}`

PROBLEM: Rows are mostly technically correct; base row has null trim and current extension beyond 2024 should not be inferred.

WEB-VALIDATED FACT: Israeli evidence supports 718 Boxster/Boxster S/GTS/GTS 4.0 historical/current through the 982 era. Porsche Israel currently highlights 718 family/RS models, but do not extend base Boxster/S/GTS to 2026 unless an official Israel source in repo supports those exact rows. Base null trim should be normalized to Boxster/Base. Field-level validation for this row: version_or_trim='GTS 4.0'; body_type='Roadster'; fuel_type='petrol'; engine='4.0L naturally aspirated flat-6'; engine_displacement_l=4.0; horsepower_hp=400; transmission='7-speed dual_clutch'; drivetrain='RWD'; years=2020-2024.

SOURCE: Porsche Israel 718 family pages; Porsche official 718 Boxster model pages; Cartube/iCar Israeli 718 Boxster/GTS coverage.

TARGET VALUE: Keep technical row and year range as sourced; do not extend beyond 2024 without official Israel evidence.

ACTION: KEEP

---



---


# BATCH27 FINAL RUN — BLOCKERS / REVIEW / UNMATCHED / ARCHIVE CLEANUP

## Scope and single-source-of-truth rules

Do not browse the internet.

All web-validation facts, source decisions, target values, variant-level corrections, split/merge/archive decisions, aliases, and blocker cleanup instructions are embedded in this file.

Apply **BATCH27 FINAL RUN only** if using this file alone. If using the unified file, apply RUN 1 -> RUN 2 -> RUN 3 -> RUN 4 -> RUN 5 -> FINAL RUN in that exact order.

If repo-local evidence conflicts with this task file, report the conflict instead of guessing.
If a variant cannot be grounded with embedded facts or repo-local sources, move it to **non-blocking review/archive** with `non_blocking=true`, clear reason, and lineage rather than fabricating clean data.

Temporary-file cleanup is mandatory:

```text
Before final commit, delete codex_tasks/BATCH27_*.md from the repo unless the user explicitly asks to keep them.
```

## ZIP state before FINAL RUN

```text
source cursor = 839/1124
resume_after_key = IL-confirmed|Porsche|718 Boxster
next_key_to_process = IL-confirmed|Porsche|718 Cayman
clean_models = 724
review_entries = 21
active_blocked = 21
unmatched_output_keys_count = 0
ready_for_website_upload = false
```

Readiness blockers to clear:

```text
models_blocked = 21
review_only_blocked_entries = 21
technical_variants_missing_required_grounding = 3
technical_variants_without_sources = 4
technical_variants_missing_grounded_fields = 36
unknown_support_values = 24
ready_for_website_upload = false
```

## FINAL RUN target state

```text
models_blocked = 0
review_only_blocked_entries = 0
invalid_source_references = 0
unknown_support_values = 0
duplicate_technical_variants = 0
unmatched_output_keys_count = 0
unmatched_output_keys_sample = []
active blocked = 0
quality bug findings = 0
quality normalization findings = 0
ready_for_website_upload = true
```

If a model is archived/reviewed as non-blocking, it must include:

```text
non_blocking=true
reason
lineage/source_profile_key
canonical target when relevant
```

---

# FINAL RUN — 21 REVIEW/BLOCKER MODELS

## 1. MODEL: NIO ET5

CURRENT VALUE:
- Review-only model with 4 variants: ET5 sedan 75 kWh, ET5 sedan 100 kWh, ET5 Touring 75 kWh, ET5 Touring 100 kWh.
- All 4 variants have `source_indexes=null` and `support_level=direct` without direct source refs.

PROBLEM:
- Good Israeli-market evidence exists, but the profile is blocked because all variants lack `source_indexes` and field-level grounding.
- HP is represented as 490 while Israeli sources commonly state 489/490 hp depending on rounding. Do not create duplicate rows for 489 vs 490.

WEB-VALIDATED FACT:
- Israeli sources support NIO ET5 sale in Israel with 75 kWh and 100 kWh battery options, AWD, about 489/490 hp, and ET5 Touring/Station wagon sale in Israel.
- NIO ET5 is not a global-only profile; it can be clean if source refs are repaired.

SOURCE:
- Repo source 0: Cartube ET5 Israel launch/pricing.
- Repo source 1: iCar NIO ET5 price/spec page.
- Repo source 2: Cartube ET5 Touring Israel launch/pricing.
- Additional embedded source: https://www.auto.co.il/cars/nio/et5/
- Additional embedded source: https://www.carzone.co.il/NIO/eT5/2024/

TARGET VALUE:
- MOVE FROM REVIEW TO CLEAN after repairing sources.
- Keep 4 rows only if repo policy treats sedan and Touring as body_type variants under the same ET5 model:
  - ET5 75 kWh Sedan, 2023-current/2026 if repo-local current source attached, otherwise 2023-2024, electric, displacement null, hp 489/490, single_speed, AWD.
  - ET5 100 kWh Sedan, same fields.
  - ET5 Touring 75 kWh Estate, 2024-current/2026 if repo-local current source attached, otherwise 2024, electric, displacement null, hp 489/490, single_speed, AWD.
  - ET5 Touring 100 kWh Estate, same fields.
- `source_indexes` must point to existing local sources: sedan rows to Cartube/iCar ET5, Touring rows to Cartube ET5 Touring; field_sources must cover body_type, fuel_type, displacement, horsepower, transmission, drivetrain, year_start/year_end.

ACTION: FIX / MOVE FROM REVIEW TO CLEAN

---

## 2. MODEL: Nissan Kicks

CURRENT VALUE:
- Review-only empty profile with `technical_variants_il=[]`.

PROBLEM:
- No verified Israeli-market clean technical variants in repo.
- Kicks is not in Nissan Israel current model list; Israeli Autoboom explicitly marks it not available in Israel, while some news/spec articles are preview/global/rumor-level.

WEB-VALIDATED FACT:
- Nissan Israel current lineup lists Qashqai, X-Trail, Juke, Sentra and does not list Kicks as a current sold model.
- Autoboom page says Nissan Kicks is not available in Israel.

SOURCE:
- Nissan Israel current lineup: https://www.nissan.co.il/vehicles/new.html
- Autoboom Kicks Israel page: https://autoboom.co.il/catalog/cars/nissan/kicks
- Optional weak/global context only: Auto Israel article asking whether new Kicks will come to Israel.

TARGET VALUE:
- Do not fabricate technical variants.
- Move to non-blocking archive/review with reason: `no verified Israeli-market sale; official local lineup does not include Kicks`.
- Preserve raw lineage and any preview/global notes.

ACTION: ARCHIVE NON-BLOCKING

---

## 3. MODEL: Nissan Leaf

CURRENT VALUE:
- Review-only empty profile due to malformed model response.
- Clean catalog already contains Nissan Leaf with 3 variants.

PROBLEM:
- Duplicate/split between review-only Leaf and clean Leaf.
- Review blocker must be cleared without deleting the existing clean Leaf evidence.

WEB-VALIDATED FACT:
- Nissan Israel marks Leaf as legacy 2010-2024 and identifies ZE1 with 40 kWh / 62 kWh; LEAF e+ 62 kWh has 214 hp.
- Existing clean profile has 150 hp standard Leaf and e+ 217 hp; 214 vs 217 hp is a source discrepancy/metric difference. Do not create duplicate rows solely for 214/217; normalize according to existing repo policy or source priority.

SOURCE:
- Nissan Israel Leaf legacy page: https://www.nissan.co.il/experience-nissan/legacy-models/leaf.html
- Existing clean Nissan Leaf repo sources: Cartube, Gear, iCar, Nissan Israel.

TARGET VALUE:
- MERGE review-only Leaf into existing clean Leaf.
- Ensure year_end=2024 for Leaf current/legacy rows; do not leave year_end=null.
- Ensure EV schema: fuel_type=electric, displacement=null, transmission=single_speed/direct_drive according to schema, drivetrain=FWD.
- Remove the review blocker after lineage is preserved.

ACTION: MERGE / ALIAS-LINEAGE / CLEAR REVIEW BLOCKER

---

## 4. MODEL: Opel Agila

CURRENT VALUE:
- Review-only empty profile.

PROBLEM:
- No repo-local Israeli sources attached.
- Global technical facts exist, but weak Israeli-market evidence means it should not be forced into verified clean.

WEB-VALIDATED FACT:
- Agila is a historical Opel city car, global production 2000-2014; second generation 1.2 94 hp FWD automatic/manual exists globally.
- Israeli-specific evidence is weak in current repo; not enough for clean without local source attachment.

SOURCE:
- Global technical reference: https://www.auto-data.net/en/opel-agila-ii-1.2-94hp-automatic-19698
- Weak model context only: iCar Opel model hub.

TARGET VALUE:
- Move to non-blocking archive/review unless repo-local Israeli evidence exists.
- If a local source is added later, expected row would likely be historical Hatchback, petrol, 1.2, 86/94 hp depending year, FWD, manual/4AT — but do not add now without local evidence.

ACTION: ARCHIVE NON-BLOCKING

---

## 5. MODEL: Opel Kadett

CURRENT VALUE:
- Review-only model with one variant: 1990-1991 Sedan petrol 1.6, 3-speed automatic, FWD, horsepower null, source_indexes=[1] while only one source appears indexed 0.

PROBLEM:
- Source index invalid and horsepower missing.
- Evidence is Tier 3 historical only.

WEB-VALIDATED FACT:
- Opel Kadett 1985-1991 existed in Israeli used-car/catalog sources; exact 1.6 automatic horsepower must be grounded before clean.

SOURCE:
- Repo source: KML Opel Kadett 1985-1991.

TARGET VALUE:
- If repo source supports horsepower, fix `source_indexes` to [0], fill hp exactly, and move to clean historical with support_level not stronger than source supports.
- If hp cannot be grounded, move to non-blocking review/archive with reason `missing required horsepower grounding`.
- Do not leave active blocker.

ACTION: FIX OR ARCHIVE NON-BLOCKING

---

## 6. MODEL: Opel Movano

CURRENT VALUE:
- Review-only empty profile from model output error.

PROBLEM:
- No variants, no sources, parsing error.
- Current Opel Israel official model pages do not list Movano as a current passenger/commercial model in the available page set.

WEB-VALIDATED FACT:
- Movano is an Opel commercial van globally, but this repo has no usable local variants/sources in this batch.

SOURCE:
- Opel Israel official site current model context: https://www.opel.co.il/

TARGET VALUE:
- Archive non-blocking unless repo-local Israeli commercial source exists.
- Do not fabricate van variants from global specs.

ACTION: ARCHIVE NON-BLOCKING

---

## 7. MODEL: Opel Vivaro

CURRENT VALUE:
- Review-only empty profile from malformed model output.

PROBLEM:
- No variants, no sources, parsing error.
- No local grounded technical rows in repo.

WEB-VALIDATED FACT:
- Vivaro exists globally/commercially, but current local Opel site context does not provide enough attached variant evidence here.

SOURCE:
- Opel Israel official site current model context: https://www.opel.co.il/

TARGET VALUE:
- Archive non-blocking unless repo-local Israeli source exists.
- Do not fabricate.

ACTION: ARCHIVE NON-BLOCKING

---

## 8. MODEL: Opel Zafira

CURRENT VALUE:
- Review-only empty profile from malformed model output.

PROBLEM:
- No variants, no sources.

WEB-VALIDATED FACT:
- Historical Opel Zafira exists globally and was likely present in Israeli used market, but no current source grounding exists in this repo entry.

SOURCE:
- Opel/iCar model context only; no sufficient local source embedded in this review profile.

TARGET VALUE:
- Move to non-blocking review/archive pending local source attachment.

ACTION: ARCHIVE NON-BLOCKING

---

## 9. MODEL: Peugeot 2008

CURRENT VALUE:
- Review-only model with 6 variants.
- Some variants are missing drivetrain; e-2008 variant has drivetrain null; current/2026 handling is incomplete.

PROBLEM:
- Required website field `drivetrain` missing in several rows.
- New current 2008 MHEV exists in Israel and should not be confused with old 130 hp petrol or old e-2008 136 hp.

WEB-VALIDATED FACT:
- Peugeot Israel current 2008 page supports MHEV 145 hp current.
- Historical Israeli sources support earlier 1.6 petrol 120 hp, 1.2T 110/130 hp, 1.5 diesel 130 hp, e-2008 136 hp.

SOURCE:
- Peugeot Israel 2008 current: https://online.peugeot.co.il/model/new2008suv/
- Repo sources 0-17 already attached for historical 2008/e-2008 rows.

TARGET VALUE:
- Fix drivetrain for all combustion 2008 rows to FWD if source/context supports FWD; otherwise move missing-grounding rows to non-blocking review rather than clean.
- e-2008 EV schema: fuel_type=electric, displacement=null, transmission=single_speed/direct_drive, drivetrain=FWD if grounded; do not leave drivetrain null.
- Add or fix current 2026 row only as MHEV 145 hp if local source attached; do not extend old 130 hp as current.

ACTION: FIX / MOVE FROM REVIEW TO CLEAN WHERE FULLY GROUNDED

---

## 10. MODEL: Peugeot 3008

CURRENT VALUE:
- Review-only model with 10 variants.
- Multiple historical rows have null transmission/drivetrain; E-3008 row has null transmission.

PROBLEM:
- Required fields missing; current 3008/e-3008 rows must align with current Peugeot Israel MHEV/BEV facts.
- Do not mix unsupported global BEV/PHEV variants into clean.

WEB-VALIDATED FACT:
- Peugeot Israel 3008 price list supports 3008 GT BEV 210 hp AT and current 3008 MHEV. E-3008 page supports 210 hp, 73 kWh, up to 499 km.

SOURCE:
- Peugeot Israel E-3008: https://online.peugeot.co.il/model/new-e-3008/
- Peugeot Israel 3008 pricelist: https://online.peugeot.co.il/pricelist/3008/
- Repo historical Peugeot 3008 sources.

TARGET VALUE:
- Fill historical drivetrain/transmission only when local source supports; otherwise move incomplete historical rows to non-blocking review.
- EV row: GT BEV 210 hp, SUV, electric, displacement=null, drivetrain=FWD, transmission=single_speed/direct_drive according to schema, year_start=2024 or 2026 according to attached source coverage.
- Do not add unsupported 230/320 hp EV rows.

ACTION: FIX / REVIEW INCOMPLETE ROWS

---

## 11. MODEL: Peugeot 4008

CURRENT VALUE:
- Review-only single row: 2012-current/null-end, SUV petrol 2.0 150, manual, drivetrain null; source supports are weak/preview.

PROBLEM:
- year_end=null implies current, which is false/unsupported.
- Missing drivetrain; weak local evidence.

WEB-VALIDATED FACT:
- Israeli sources describe 4008 arrival/launch plan around 2012, but broad verified Israeli sale and current status are not established.

SOURCE:
- Repo source Autocom 2012 models.
- Repo source Auto article on 4008 coming to Israel.

TARGET VALUE:
- Do not move to clean unless repo-local evidence proves actual Israeli sale and all fields.
- If retained at all, archive/review non-blocking as weak historical/preview with year_start=2012 and year_end bounded to 2012/unknown, not current.

ACTION: ARCHIVE NON-BLOCKING / MOVE TO REVIEW NON-BLOCKING

---

## 12. MODEL: Peugeot 407

CURRENT VALUE:
- Review-only empty profile due to model output error.

PROBLEM:
- Empty output despite strong Israeli historical evidence.

WEB-VALIDATED FACT:
- iCar supports Peugeot 407 2006 Israeli variants including 2.0, 2.2, 3.0, sedan, FWD, automatic. Example 2.2 Executive has 2230 cc, 163 hp, 4-speed automatic, FWD.

SOURCE:
- iCar 407 2006 2.2 Executive: https://www.icar.co.il/פיג'ו/פיג'ו_407/פיג'ו_407_יד_שניה_ד10/version3577/
- iCar Peugeot model hub lists 407 under previous models.

TARGET VALUE:
- Rebuild clean historical profile if enough local variants are attached:
  - 2.0 petrol automatic, FWD, hp per source.
  - 2.2 petrol automatic, FWD, 163 hp.
  - 3.0 petrol automatic, FWD, hp per source.
- If only the 2.2 source is embedded, add only the 2.2 row and archive the rest as pending.
- Do not leave empty blocker.

ACTION: FIX / REBUILD HISTORICAL CLEAN OR ARCHIVE NON-BLOCKING

---

## 13. MODEL: Peugeot 408

CURRENT VALUE:
- Review-only empty profile from malformed model output.
- Clean catalog already has Peugeot 408 split profiles handled in RUN4/RUN5.

PROBLEM:
- Duplicate review blocker overlaps with RUN4/RUN5 408 split cleanup.

WEB-VALIDATED FACT:
- Peugeot Israel current 408 exists; current 2026 row should be MHEV 145 hp. Historical 2023-2024 rows may include 1.2T 130 and PHEV 225 only if local sources are attached.

SOURCE:
- Peugeot Israel 408: https://online.peugeot.co.il/model/408/
- RUN4/RUN5 task files.

TARGET VALUE:
- Merge review-only 408 into canonical Peugeot 408 handled by RUN5.
- Clear blocker; preserve lineage.
- Do not create a third 408 clean/review profile.

ACTION: MERGE / CLEAR REVIEW BLOCKER

---

## 14. MODEL: Peugeot 5008

CURRENT VALUE:
- Review-only model with 12 variants and many null drivetrain fields.
- Clean/RUN5 also handles 5008/e-5008 split.

PROBLEM:
- Missing drivetrain across many rows; current 5008/e-5008 must align with official current 5008 MHEV/e-5008.
- Duplicate/electric split risk.

WEB-VALIDATED FACT:
- Peugeot Israel current 5008 MHEV supports 145 hp AT6; E-5008 supports 210 hp, 73 kWh, FWD/electric.
- Historical 5008 rows include MPV petrol and second-generation diesel/petrol sources.

SOURCE:
- Peugeot Israel 5008 MHEV: https://online.peugeot.co.il/model/peugeot-5008-suv/
- Peugeot Israel E-5008: https://online.peugeot.co.il/model/new-e-5008/
- Peugeot 5008 pricelist: https://online.peugeot.co.il/pricelist/5008/
- Repo historical 5008 sources.

TARGET VALUE:
- Fill drivetrain=FWD only where local source/context supports; otherwise move incomplete historical rows to non-blocking review.
- Canonicalize e-5008 electric row: 210 hp, 73 kWh, electric, displacement=null, single_speed/direct_drive, FWD, not duplicate under both `5008` and `e-5008`.
- Current MHEV row: 145 hp AT6 only if local source attached.

ACTION: FIX / MERGE / REVIEW INCOMPLETE ROWS

---

## 15. MODEL: Peugeot 508

CURRENT VALUE:
- Review-only 5 variants with drivetrain null in every row.

PROBLEM:
- Missing required drivetrain. Current status not established after 2020 in this run.

WEB-VALIDATED FACT:
- Israeli sources support historical 508 first-generation and second-generation rows, but current Peugeot Israel active lineup does not list 508 as a 2026 new model.

SOURCE:
- Repo sources: Yad2/Auto/iCar historical 508 sources.
- Peugeot model hub/current lineup context.

TARGET VALUE:
- For each historical 508 row, set drivetrain=FWD only if supported by attached local sources; if not, move to non-blocking review rather than keeping missing fields.
- Keep year_end bounded to 2020 unless later local evidence attached.
- Do not currentize.

ACTION: FIX OR MOVE TO REVIEW NON-BLOCKING

---

## 16. MODEL: Peugeot Boxer

CURRENT VALUE:
- Review-only 4 variants. Diesel rows mostly grounded; electric Boxer row has horsepower null and year_end null.

PROBLEM:
- Electric Boxer row lacks required horsepower and should not be clean.
- Diesel rows can likely be clean after field-source verification.

WEB-VALIDATED FACT:
- Peugeot Israel Boxer page and iCar support current 2.2 diesel 140 manual and 180 automatic variants. Electric Boxer evidence is weaker/incomplete in this profile.

SOURCE:
- Peugeot Israel Boxer: https://online.peugeot.co.il/model/boxer/
- iCar Boxer 2026 2.2 180 automatic pickup: repo source.

TARGET VALUE:
- Move diesel Boxer rows to clean if field_sources cover body_type/fuel/displacement/hp/transmission/drivetrain/year.
- Electric Boxer row: move to non-blocking review/archive unless hp and all required EV fields are locally grounded.
- EV schema if later retained: displacement=null, electric, single_speed/direct_drive, FWD if grounded.

ACTION: FIX DIESEL / ARCHIVE OR REVIEW ELECTRIC

---

## 17. MODEL: Peugeot e-2008

CURRENT VALUE:
- Review-only 1 variant: Premium 2020-2024, 136 hp, electric, automatic, drivetrain null.

PROBLEM:
- Missing drivetrain; transmission as `automatic` is too generic for EV if schema supports single_speed/direct_drive.

WEB-VALIDATED FACT:
- Israeli sources support e-2008 136 hp sold in Israel; no sufficient source here for separate 156 hp current Israeli row.

SOURCE:
- Repo sources: Peugeot 02/2024 price list, Auto e-2008 test/news, Peugeot article.
- Peugeot 2008 current page for current MHEV context.

TARGET VALUE:
- Clean only if fixed to EV schema:
  - fuel_type=electric
  - displacement=null
  - horsepower_hp=136
  - transmission=single_speed/direct_drive according to schema
  - drivetrain=FWD if source/context supports
  - year_end=2024 unless exact current e-2008 source attached.
- Otherwise move non-blocking review.

ACTION: FIX / MOVE TO CLEAN OR REVIEW

---

## 18. MODEL: Peugeot e-208

CURRENT VALUE:
- Review-only 2 variants: 2020-2024 Premium S 136 hp cleanable; 2026 Premium S with hp/transmission/drivetrain null.

PROBLEM:
- 2026 row lacks required fields. Do not keep clean row with null hp/transmission/drivetrain.

WEB-VALIDATED FACT:
- Historical/current local sources support e-208 Premium S 136 hp through 2024; 2026 listing in iCar exists but does not ground enough technical fields in this profile.

SOURCE:
- Repo sources: Auto e-208 2020/2024, static brochure, iCar 2026 listing.

TARGET VALUE:
- Keep/fix 2020-2024 Premium S 136 hp with EV schema and FWD.
- Move 2026 row to non-blocking review unless all missing fields are grounded in repo-local source.
- Do not infer 156 hp from global update.

ACTION: FIX / SPLIT / REVIEW INCOMPLETE CURRENT ROW

---

## 19. MODEL: Peugeot e-3008

CURRENT VALUE:
- Review-only 1 variant: GT 2024-2026, 210 hp, electric, displacement null, transmission null, FWD.

PROBLEM:
- Missing EV transmission. Otherwise local evidence is strong.

WEB-VALIDATED FACT:
- Peugeot Israel E-3008 supports 210 hp and 73 kWh. Price list supports GT BEV 210hp AT.

SOURCE:
- Peugeot Israel E-3008: https://online.peugeot.co.il/model/new-e-3008/
- Peugeot Israel 3008 pricelist: https://online.peugeot.co.il/pricelist/3008/

TARGET VALUE:
- Move to clean after fixing EV transmission to schema-valid `single_speed`/`direct_drive` equivalent.
- Keep no 230/320 hp rows unless local source attached.

ACTION: FIX / MOVE FROM REVIEW TO CLEAN

---

## 20. MODEL: Peugeot Partner

CURRENT VALUE:
- Review-only empty profile due to malformed model output.

PROBLEM:
- Empty blocker. Partner is a real Israeli Peugeot commercial/historical model but no variants are attached here.

WEB-VALIDATED FACT:
- iCar Peugeot model hub lists Partner as a previous model. However current 2026 Peugeot active lineup is 208/2008/3008/408/5008/Rifter/Boxer and not Partner.

SOURCE:
- iCar Peugeot hub: https://www.icar.co.il/פיג'ו/

TARGET VALUE:
- Do not rebuild from memory/global specs.
- If repo-local Partner sources exist elsewhere, rebuild historical clean with exact rows.
- Otherwise archive non-blocking with reason `empty malformed output; no attached local source in review profile`.

ACTION: ARCHIVE NON-BLOCKING OR REBUILD ONLY WITH REPO-LOCAL SOURCE

---

## 21. MODEL: Peugeot Traveller

CURRENT VALUE:
- Review-only empty profile due to model output error.

PROBLEM:
- Empty blocker and no sources in review profile.

WEB-VALIDATED FACT:
- Traveller existed as a Peugeot MPV/van in markets, but current Peugeot Israel active new model hub does not provide enough attached detail here.

SOURCE:
- iCar Peugeot hub for model context only.

TARGET VALUE:
- Archive non-blocking unless repo-local Israeli source exists.
- Do not fabricate trims/engine rows.

ACTION: ARCHIVE NON-BLOCKING

---

# CROSS-CUTTING FINAL RUN FIXES

## A. Unknown support values

CURRENT VALUE:
- readiness reports `unknown_support_values = 24`.

PROBLEM:
- Website-ready catalog cannot contain unsupported/unknown support labels.

TARGET VALUE:
- Normalize support levels to allowed enum values used by schema.
- If exact support strength cannot be justified, use non-blocking review/archive; do not leave unknown support values.

ACTION: CODE / REPORTING FIX + DATA FIX

## B. Technical variants missing required grounding

CURRENT VALUE:
- readiness reports `technical_variants_missing_required_grounding = 3`, `technical_variants_without_sources = 4`, `technical_variants_missing_grounded_fields = 36`.

PROBLEM:
- These are active blockers for website readiness.

TARGET VALUE:
- For every remaining review variant: either repair `source_indexes` + `field_sources` for every required field, or move the row/model to non-blocking review/archive.

ACTION: FIX / MOVE TO REVIEW / ARCHIVE NON-BLOCKING

## C. Unmatched / split aliases

CURRENT VALUE:
- `unmatched_output_keys_count = 0`, but previous clean RUNs created/handled split alias risks.

TARGET VALUE:
- Keep `unmatched_output_keys_count = 0` and `unmatched_output_keys_sample=[]`.
- Do not create new split-profile keys for Nissan Leaf, Peugeot 408, Peugeot 5008/e-5008, or duplicate global-reference-only/IL-likely entries.

ACTION: ALIAS / LINEAGE / DELETE DUPLICATE

---

# REQUIRED CHECKS AFTER FINAL RUN

Run:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Then audit actual generated files, not only console output:

```text
- data/model_technical_catalog_il.json
- data/model_technical_catalog_il_readiness.json
- data/model_technical_catalog_il_review.json
- data/model_technical_catalog_il_archive.json
- data/model_technical_catalog_il_quality_scan.json
- compute_resume_state()
- unmatched_output_keys
- active blockers
- cursor/resume state
- duplicate/split alias cleanup
```

If tests fail because `streamlit` is missing, report it explicitly as an environment/dependency issue. Do not hide it. Still run every validation that can run.

Report:

```text
1. Files changed
2. Exact metrics before/after
3. Confirmation that all 21 FINAL blockers were resolved or explicitly moved to non-blocking archive/review
4. Confirmation that RUN1-RUN5 corrections remain intact
5. Test results
6. Confirmation that temporary Batch 27 instruction files were deleted before final commit
7. Remaining issues, if any
```

---

# APPENDIX — Actual review/blocker snapshot from uploaded ZIP

## NIO ET5
- validation_issues:
  - variant[0] has no source_indexes
  - variant[0] support_level=direct but no source directly supports it
  - variant[1] has no source_indexes
  - variant[1] support_level=direct but no source directly supports it
  - variant[2] has no source_indexes
  - variant[2] support_level=direct but no source directly supports it
  - variant[3] has no source_indexes
  - variant[3] support_level=direct but no source directly supports it
- technical_variants_il:
  - variant[0]: trim='75 kWh', years=2023-2024, body=Sedan, fuel=electric, displacement=None, hp=490, transmission=single_speed, drivetrain=AWD, source_indexes=None
  - variant[1]: trim='100 kWh', years=2023-2024, body=Sedan, fuel=electric, displacement=None, hp=490, transmission=single_speed, drivetrain=AWD, source_indexes=None
  - variant[2]: trim='75 kWh', years=2024-2024, body=Estate, fuel=electric, displacement=None, hp=490, transmission=single_speed, drivetrain=AWD, source_indexes=None
  - variant[3]: trim='100 kWh', years=2024-2024, body=Estate, fuel=electric, displacement=None, hp=490, transmission=single_speed, drivetrain=AWD, source_indexes=None

## Nissan Kicks
- validation_issues:
  - technical_variants_il is empty
- technical_variants_il: []

## Nissan Leaf
- model_error: `Expecting ',' delimiter: line 198 column 1 (char 4465)`
- validation_issues:
  - technical_variants_il is empty
- technical_variants_il: []

## Opel Agila
- validation_issues:
  - technical_variants_il is empty
- technical_variants_il: []

## Opel Kadett
- validation_issues:
  - variant[0] required website field 'horsepower_hp' is null/empty
  - variant[0] required field 'horsepower_hp' listed in missing_grounded_fields
- technical_variants_il:
  - variant[0]: trim=None, years=1990-1991, body=Sedan, fuel=petrol, displacement=1.6, hp=None, transmission=3-speed automatic, drivetrain=FWD, source_indexes=[1]

## Opel Movano
- model_error: `Gemini catalog client returned non-object JSON`
- validation_issues:
  - technical_variants_il is empty
- technical_variants_il: []

## Opel Vivaro
- model_error: `Expecting ',' delimiter: line 22 column 12 (char 377)`
- validation_issues:
  - technical_variants_il is empty
- technical_variants_il: []

## Opel Zafira
- model_error: `Extra data: line 208 column 1 (char 5050)`
- validation_issues:
  - technical_variants_il is empty
- technical_variants_il: []

## Peugeot 2008
- notes: ['Only Israeli-market sources were used.', 'Rows are merged across years only when sourced technical fields remain the same.', 'Drivetrain is left null where no Israeli-market source directly or contextually grounded it.']
- validation_issues:
  - variant[0] required website field 'drivetrain' is null/empty
  - variant[0] required field 'drivetrain' listed in missing_grounded_fields
  - variant[1] required website field 'drivetrain' is null/empty
  - variant[1] required field 'drivetrain' listed in missing_grounded_fields
  - variant[4] required website field 'drivetrain' is null/empty
  - variant[4] required field 'drivetrain' listed in missing_grounded_fields
- technical_variants_il:
  - variant[0]: trim=None, years=2013-2015, body=SUV, fuel=petrol, displacement=1.6, hp=120, transmission=4-speed automatic, drivetrain=None, source_indexes=[0, 1, 2, 3]
  - variant[1]: trim=None, years=2016-2019, body=SUV, fuel=petrol, displacement=1.2, hp=110, transmission=6-speed automatic, drivetrain=None, source_indexes=[4]
  - variant[2]: trim=None, years=2018-2023, body=SUV, fuel=diesel, displacement=1.5, hp=130, transmission=8-speed automatic, drivetrain=FWD, source_indexes=[5, 6, 7]
  - variant[3]: trim=None, years=2020-2024, body=SUV, fuel=petrol, displacement=1.2, hp=130, transmission=8-speed automatic, drivetrain=FWD, source_indexes=[8, 9, 10, 11]
  - variant[4]: trim=None, years=2023-2024, body=SUV, fuel=electric, displacement=None, hp=136, transmission=single_speed, drivetrain=None, source_indexes=[12, 13]
  - variant[5]: trim=None, years=2025-2026, body=SUV, fuel=mild_hybrid, displacement=1.2, hp=145, transmission=6-speed dual_clutch, drivetrain=FWD, source_indexes=[14, 15, 16, 17]

## Peugeot 3008
- notes: ['Included only Israeli-market configurations found in Israeli sources.', 'Electric E-3008 treated as a separate technical version under 3008 family because user raw data included electric for model 3008; canonical_model kept as 3008 but EV fields are grounded separately.', 'Some older variants lack grounded transmission/drivetrain in accessible Israeli sources, so those fields are null.', 'Year_end values reflect latest grounded evidence found, not inferred continuation.', 'GT 300hp PHEV engine displacement was not directly stated in the cited Israeli source excerpt, so left null despite likely known globally.']
- validation_issues:
  - variant[0] required website field 'transmission' is null/empty
  - variant[0] required website field 'drivetrain' is null/empty
  - variant[0] required field 'transmission' listed in missing_grounded_fields
  - variant[0] required field 'drivetrain' listed in missing_grounded_fields
  - variant[1] required website field 'transmission' is null/empty
  - variant[1] required website field 'drivetrain' is null/empty
  - variant[1] required field 'transmission' listed in missing_grounded_fields
  - variant[1] required field 'drivetrain' listed in missing_grounded_fields
  - variant[2] required website field 'transmission' is null/empty
  - variant[2] required website field 'drivetrain' is null/empty
  - variant[2] required field 'transmission' listed in missing_grounded_fields
  - variant[2] required field 'drivetrain' listed in missing_grounded_fields
  - variant[3] required website field 'drivetrain' is null/empty
  - variant[3] required field 'drivetrain' listed in missing_grounded_fields
  - variant[4] required website field 'drivetrain' is null/empty
  - variant[4] required field 'drivetrain' listed in missing_grounded_fields
  - variant[5] required website field 'drivetrain' is null/empty
  - variant[5] required field 'drivetrain' listed in missing_grounded_fields
  - variant[6] required website field 'transmission' is null/empty
  - variant[6] required field 'transmission' listed in missing_grounded_fields
  - ... 7 more issues
- technical_variants_il:
  - variant[0]: trim=None, years=2016-2018, body=SUV, fuel=diesel, displacement=1.6, hp=120, transmission=None, drivetrain=None, source_indexes=[0]
  - variant[1]: trim=None, years=2016-2018, body=SUV, fuel=petrol, displacement=1.6, hp=165, transmission=None, drivetrain=None, source_indexes=[0]
  - variant[2]: trim='GT', years=2016-2018, body=SUV, fuel=diesel, displacement=2, hp=180, transmission=None, drivetrain=None, source_indexes=[0]
  - variant[3]: trim=None, years=2018-2024, body=SUV, fuel=diesel, displacement=1.5, hp=130, transmission=8-speed automatic, drivetrain=None, source_indexes=[1, 2, 3]
  - variant[4]: trim=None, years=2018-2024, body=SUV, fuel=petrol, displacement=1.2, hp=130, transmission=8-speed automatic, drivetrain=None, source_indexes=[1, 2, 3]
  - variant[5]: trim=None, years=2018-2021, body=SUV, fuel=petrol, displacement=1.6, hp=180, transmission=8-speed automatic, drivetrain=None, source_indexes=[1, 2]
  - variant[6]: trim='Premium', years=2021-2024, body=SUV, fuel=plug_in_hybrid, displacement=1.6, hp=225, transmission=None, drivetrain=FWD, source_indexes=[3, 4]
  - variant[7]: trim='GT', years=2021-2021, body=SUV, fuel=plug_in_hybrid, displacement=1.6, hp=300, transmission=None, drivetrain=AWD, source_indexes=[3]
  - variant[8]: trim=None, years=2024-2026, body=SUV, fuel=mild_hybrid, displacement=1.2, hp=136, transmission=6-speed dual_clutch, drivetrain=FWD, source_indexes=[4, 5]
  - variant[9]: trim='GT', years=2024-2026, body=SUV, fuel=electric, displacement=None, hp=210, transmission=None, drivetrain=FWD, source_indexes=[5, 6]

## Peugeot 4008
- notes: ['Israeli-market sources found evidence of intended/announced Israeli sale for a 2.0L 150 hp manual configuration starting in 2012.', 'Could not ground drivetrain, body_type, fuel_type, trim, or end year from Israeli-market sources located.', "Found conflicting market-context signals about whether the 4008 was ultimately marketed broadly in Israel; however Israeli sources did describe a local offering/launch plan for the manual 2.0L version, so one technical row is retained with support_level='unknown'."]
- validation_issues:
  - variant[0] non-null field 'body_type' has no field_sources entry
  - variant[0] non-null field 'fuel_type' has no field_sources entry
  - variant[0] required website field 'drivetrain' is null/empty
  - variant[0] required field 'body_type' listed in missing_grounded_fields
  - variant[0] required field 'fuel_type' listed in missing_grounded_fields
  - variant[0] required field 'drivetrain' listed in missing_grounded_fields
- technical_variants_il:
  - variant[0]: trim=None, years=2012-None, body=SUV, fuel=petrol, displacement=2.0, hp=150, transmission=manual, drivetrain=None, source_indexes=[0, 1]

## Peugeot 407
- model_error: `Gemini catalog client returned non-object JSON`
- validation_issues:
  - technical_variants_il is empty
- technical_variants_il: []

## Peugeot 408
- model_error: `Extra data: line 133 column 1 (char 2638)`
- validation_issues:
  - technical_variants_il is empty
- technical_variants_il: []

## Peugeot 5008
- notes: ['Israeli sources clearly support first-generation petrol MPV 1.6T 156hp automatic and second-generation SUV petrol/diesel configurations. No Israeli-grounded drivetrain statement was found in the consulted sources, so drivetrain is null in all rows.', 'For 2017-2018 second-generation launch, Wheel and Autocom support 1.6 diesel 120hp, 1.6 petrol 165hp, and 2.0 diesel 180hp with 6-speed automatic. GT row trim is sourced from Wheel; Premium petrol/diesel rows are separately supported by Autocom test/spec pages.', 'For 2019 update, iCar reports the switch to 1.5 diesel 130hp / 1.6 petrol 180hp and 8-speed automatic, while official Peugeot Israel 2022 PDF confirms Active Pack and Premium offerings for those powertrains. No official 2019 price list was found in the consulted set, so 2019-2022 span is grounded by combined sources.', 'For 2021-2024, official Peugeot Israel sources support 1.2 petrol 130hp in Active Pack and later Premium. The consulted 2024 official price list only showed petrol 1.2 130hp variants; no diesel 5008 entries appeared there.', "Transmission granularity is normalized as 'automatic' for 1.2 rows because the consulted official sources name the gearbox only as אוטומטי without a speed count on those specific rows, while other rows have sourced 6-speed or 8-speed detail.", 'No separate row was created for exact pre-facelift/facelift cosmetic changes because technical fields in the required split key were unchanged within the grounded evidence.']
- validation_issues:
  - variant[0] required website field 'drivetrain' is null/empty
  - variant[0] required field 'drivetrain' listed in missing_grounded_fields
  - variant[1] required website field 'drivetrain' is null/empty
  - variant[1] required field 'drivetrain' listed in missing_grounded_fields
  - variant[2] required website field 'drivetrain' is null/empty
  - variant[2] required field 'drivetrain' listed in missing_grounded_fields
  - variant[3] required website field 'drivetrain' is null/empty
  - variant[3] required field 'drivetrain' listed in missing_grounded_fields
  - variant[4] required website field 'drivetrain' is null/empty
  - variant[4] required field 'drivetrain' listed in missing_grounded_fields
  - variant[5] required website field 'drivetrain' is null/empty
  - variant[5] required field 'drivetrain' listed in missing_grounded_fields
  - variant[6] required website field 'drivetrain' is null/empty
  - variant[6] required field 'drivetrain' listed in missing_grounded_fields
  - variant[7] required website field 'drivetrain' is null/empty
  - variant[7] required field 'drivetrain' listed in missing_grounded_fields
  - variant[8] required website field 'drivetrain' is null/empty
  - variant[8] required field 'drivetrain' listed in missing_grounded_fields
  - variant[9] required website field 'drivetrain' is null/empty
  - variant[9] required field 'drivetrain' listed in missing_grounded_fields
  - ... 4 more issues
- technical_variants_il:
  - variant[0]: trim=None, years=2010-2015, body=MPV, fuel=petrol, displacement=1.6, hp=156, transmission=6-speed automatic, drivetrain=None, source_indexes=[0]
  - variant[1]: trim='Active', years=2017-2018, body=SUV, fuel=diesel, displacement=1.6, hp=120, transmission=6-speed automatic, drivetrain=None, source_indexes=[1]
  - variant[2]: trim='Premium', years=2017-2018, body=SUV, fuel=diesel, displacement=1.6, hp=120, transmission=6-speed automatic, drivetrain=None, source_indexes=[2, 1]
  - variant[3]: trim='Active', years=2017-2018, body=SUV, fuel=petrol, displacement=1.6, hp=165, transmission=6-speed automatic, drivetrain=None, source_indexes=[1]
  - variant[4]: trim='Premium', years=2017-2018, body=SUV, fuel=petrol, displacement=1.6, hp=165, transmission=6-speed automatic, drivetrain=None, source_indexes=[3, 1]
  - variant[5]: trim='GT', years=2017-2018, body=SUV, fuel=diesel, displacement=2.0, hp=180, transmission=6-speed automatic, drivetrain=None, source_indexes=[1]
  - variant[6]: trim='Active Pack', years=2019-2022, body=SUV, fuel=diesel, displacement=1.5, hp=130, transmission=8-speed automatic, drivetrain=None, source_indexes=[4, 5]
  - variant[7]: trim='Premium', years=2019-2022, body=SUV, fuel=diesel, displacement=1.5, hp=130, transmission=8-speed automatic, drivetrain=None, source_indexes=[4, 5]
  - variant[8]: trim='Active Pack', years=2019-2022, body=SUV, fuel=petrol, displacement=1.6, hp=180, transmission=8-speed automatic, drivetrain=None, source_indexes=[4, 5]
  - variant[9]: trim='Premium', years=2019-2022, body=SUV, fuel=petrol, displacement=1.6, hp=180, transmission=8-speed automatic, drivetrain=None, source_indexes=[4, 5]
  - variant[10]: trim='Active Pack', years=2021-2024, body=SUV, fuel=petrol, displacement=1.2, hp=130, transmission=automatic, drivetrain=None, source_indexes=[6, 7, 8]
  - variant[11]: trim='Premium', years=2024-2024, body=SUV, fuel=petrol, displacement=1.2, hp=130, transmission=automatic, drivetrain=None, source_indexes=[8]

## Peugeot 508
- notes: ['Israeli sources found for first-generation petrol sedan 1.6 turbo 156hp automatic and facelift 165hp automatic, plus second-generation Fastback 180hp, 225hp petrol, and 225hp plug-in hybrid.', 'Drivetrain was not directly grounded from Israeli-market sources located, so set to null for all rows.', "Second-generation body style normalized to Liftback from Israeli source label 'FASTBACK' / hatchback-style listings.", 'PHEV trim name was not reliably grounded from the located Israeli sources, so version_or_trim is null.', 'Year ranges are bounded only by sourced evidence; absence after 2020 is not treated as proof of non-sale, but no later grounded Israeli technical source was established in this run.']
- validation_issues:
  - variant[0] required website field 'drivetrain' is null/empty
  - variant[0] required field 'drivetrain' listed in missing_grounded_fields
  - variant[1] required website field 'drivetrain' is null/empty
  - variant[1] required field 'drivetrain' listed in missing_grounded_fields
  - variant[2] required website field 'drivetrain' is null/empty
  - variant[2] required field 'drivetrain' listed in missing_grounded_fields
  - variant[3] required website field 'drivetrain' is null/empty
  - variant[3] required field 'drivetrain' listed in missing_grounded_fields
  - variant[4] required website field 'drivetrain' is null/empty
  - variant[4] required field 'drivetrain' listed in missing_grounded_fields
- technical_variants_il:
  - variant[0]: trim='Active', years=2011-2015, body=Sedan, fuel=petrol, displacement=1.6, hp=156, transmission=6-speed automatic, drivetrain=None, source_indexes=[0, 1, 2, 3]
  - variant[1]: trim='Active', years=2015-2016, body=Sedan, fuel=petrol, displacement=1.6, hp=165, transmission=automatic, drivetrain=None, source_indexes=[4, 5, 6]
  - variant[2]: trim='Premium', years=2018-2020, body=Liftback, fuel=petrol, displacement=1.6, hp=180, transmission=8-speed automatic, drivetrain=None, source_indexes=[7, 8, 9]
  - variant[3]: trim='GT', years=2018-2020, body=Liftback, fuel=petrol, displacement=1.6, hp=225, transmission=8-speed automatic, drivetrain=None, source_indexes=[7, 8, 9]
  - variant[4]: trim=None, years=2020-2020, body=Liftback, fuel=plug_in_hybrid, displacement=1.6, hp=225, transmission=8-speed automatic, drivetrain=None, source_indexes=[8, 9]

## Peugeot Boxer
- notes: ['Only Israeli-market grounded technical fields were populated; unsupported fields were set to null.', 'Diesel Boxer rows are merged across 2024-2026 because sourced technical fields are identical across the observed Israeli listings.', 'Electric Boxer evidence in Israel is weaker and partly indirect; sale/arrival is supported, but horsepower and explicit year_end were not grounded from Israeli sources.', "Drivetrain for diesel/pickup rows is treated as indirect because explicit Israeli-source statement was limited; row kept with support_level='indirect' per instructions."]
- validation_issues:
  - variant[3] required website field 'horsepower_hp' is null/empty
  - variant[3] required field 'horsepower_hp' listed in missing_grounded_fields
- technical_variants_il:
  - variant[0]: trim=None, years=2024-2026, body=Van, fuel=diesel, displacement=2.2, hp=140, transmission=6-speed manual, drivetrain=FWD, source_indexes=[0, 1, 2]
  - variant[1]: trim=None, years=2024-2026, body=Van, fuel=diesel, displacement=2.2, hp=180, transmission=8-speed automatic, drivetrain=FWD, source_indexes=[0, 1, 2]
  - variant[2]: trim=None, years=2024-2026, body=Pickup, fuel=diesel, displacement=2.2, hp=180, transmission=8-speed automatic, drivetrain=FWD, source_indexes=[0, 1, 2, 3]
  - variant[3]: trim=None, years=2020-None, body=Van, fuel=electric, displacement=None, hp=None, transmission=single_speed, drivetrain=FWD, source_indexes=[4, 5, 6]

## Peugeot e-2008
- notes: ['Israeli-market grounding found for one sold e-2008 configuration: Premium 136hp electric.', 'No Israeli-market source was found confirming a separate 156hp/54kWh e-2008 technical version actually sold in Israel, so it is not included.', 'Engine displacement is not applicable to this EV and is left null.', 'Drivetrain was present in raw hints but not grounded from Israeli-market sources, so it is left null.', "Transmission was normalized to 'automatic' because the grounded Israeli pricelist/brochure describe it only as אוטומטי / automatic, not explicitly single_speed."]
- validation_issues:
  - variant[0] required website field 'drivetrain' is null/empty
  - variant[0] required field 'drivetrain' listed in missing_grounded_fields
- technical_variants_il:
  - variant[0]: trim='Premium', years=2020-2024, body=Crossover, fuel=electric, displacement=None, hp=136, transmission=automatic, drivetrain=None, source_indexes=[0, 1, 2, 3, 4]

## Peugeot e-208
- notes: ['Israeli-market grounding found clearly for a 136 hp electric e-208 Premium S sold from launch in 2020 and still listed in 2024 sources.', 'A 2026 Israeli listing for e-208 Premium S was found, but the accessible source snippet did not ground horsepower/transmission/drivetrain/body type directly enough to populate them under the task rules.', 'No Israeli-grounded source was found in this run for a separate 156 hp e-208 version actually sold in Israel; global/update articles mention the powertrain update, but they do not by themselves ground an Israeli-market sold technical row.']
- validation_issues:
  - variant[1] non-null field 'body_type' has no field_sources entry
  - variant[1] required website field 'horsepower_hp' is null/empty
  - variant[1] required website field 'transmission' is null/empty
  - variant[1] required website field 'drivetrain' is null/empty
  - variant[1] required field 'body_type' listed in missing_grounded_fields
  - variant[1] required field 'horsepower_hp' listed in missing_grounded_fields
  - variant[1] required field 'transmission' listed in missing_grounded_fields
  - variant[1] required field 'drivetrain' listed in missing_grounded_fields
- technical_variants_il:
  - variant[0]: trim='Premium S', years=2020-2024, body=Hatchback, fuel=electric, displacement=None, hp=136, transmission=single_speed, drivetrain=FWD, source_indexes=[0, 1, 2]
  - variant[1]: trim='Premium S', years=2026-2026, body=Hatchback, fuel=electric, displacement=None, hp=None, transmission=None, drivetrain=None, source_indexes=[3]

## Peugeot e-3008
- notes: ['Israeli-market web sources found clear evidence for one sold e-3008 technical configuration in Israel: a single-motor 210 hp front-wheel-drive electric SUV.', 'Raw database hints for 230 hp long-range and 320 hp dual-motor AWD variants were not grounded as actually sold in Israel from the located Israeli-market sources, so they were not returned as technical_variants_il.', 'Official importer page was search-grounded but direct page opening returned 403 in tool fetch; support was limited to searchable snippet evidence for the 210 hp electric configuration.', 'Transmission was not stated in the located Israeli-market sources used here, so it is left null.', 'Engine displacement is not applicable to an EV and is left null per schema.']
- validation_issues:
  - variant[0] required website field 'transmission' is null/empty
  - variant[0] required field 'transmission' listed in missing_grounded_fields
- technical_variants_il:
  - variant[0]: trim='GT', years=2024-2026, body=SUV, fuel=electric, displacement=None, hp=210, transmission=None, drivetrain=FWD, source_indexes=[0, 1, 2, 3, 4]

## Peugeot Partner
- model_error: `Extra data: line 444 column 1 (char 10231)`
- validation_issues:
  - technical_variants_il is empty
- technical_variants_il: []

## Peugeot Traveller
- model_error: `Gemini catalog client returned non-object JSON`
- validation_issues:
  - technical_variants_il is empty
- technical_variants_il: []
