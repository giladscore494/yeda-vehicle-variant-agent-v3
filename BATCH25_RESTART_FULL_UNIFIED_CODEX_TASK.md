# BATCH25 RESTART — RUN1 + RUN2 CUMULATIVE CODEX TASK

This cumulative file is for traceability only if you want Codex to apply RUN 1 and RUN 2 together. Prefer applying RUNs separately unless you intentionally want a combined run. Do not browse the internet. Embedded facts are the source of truth.


---


# BATCH25 RESTART — RUN 1 VARIANT-LEVEL CODEX TASK

## Non-negotiable execution rules

Do not browse the internet. All web-validation facts and target corrections are embedded in this task file. Use this task file as the single source of truth. Do not apply corrections that are not instructed here. If repo-local evidence conflicts with this task file, report it instead of guessing. If a variant cannot be grounded with the embedded facts or repo-local sources, move it to non-blocking archive/review rather than fabricating data.

This RUN covers only RUN 1 clean profiles. Do not implement RUN 2, RUN 3, or FINAL blockers yet, except to avoid regressions caused by RUN 1 corrections.

## RUN 1 scope

RUN 1 starts after `IL-confirmed|Kia|Shuma` and contains 25 clean model profiles / 96 technical variants:
1. `IL-confirmed|Kia|Sorento` — 11 variants
2. `IL-confirmed|Kia|Soul` — 3 variants
3. `global-reference-only|Kia|Soul` — 7 variants
4. `IL-confirmed|Kia|Sportage` — 12 variants
5. `IL-confirmed|Kia|Stinger` — 2 variants
6. `IL-confirmed|Kia|Stonic` — 4 variants
7. `IL-confirmed|Kia|Venga` — 2 variants
8. `global-reference-only|Kia|Venga` — 2 variants
9. `IL-likely|Lamborghini|Aventador` — 3 variants
10. `IL-confirmed|Lamborghini|Aventador` — 2 variants
11. `global-reference-only|Lamborghini|Aventador` — 1 variants
12. `global-reference-only|Lamborghini|Gallardo` — 5 variants
13. `IL-likely|Lamborghini|Huracan` — 3 variants
14. `IL-confirmed|Lamborghini|Huracan` — 7 variants
15. `IL-confirmed|Lamborghini|Urus` — 1 variants
16. `IL-likely|Lamborghini|Urus` — 3 variants
17. `global-reference-only|Lamborghini|Urus` — 4 variants
18. `IL-confirmed|Lancia|Delta` — 3 variants
19. `global-reference-only|Lancia|Kappa` — 5 variants
20. `global-reference-only|Lancia|Lybra` — 4 variants
21. `IL-confirmed|Lancia|Lybra` — 1 variants
22. `IL-confirmed|Lancia|Thema` — 3 variants
23. `IL-likely|Lancia|Thema` — 1 variants
24. `global-reference-only|Lancia|Thesis` — 3 variants
25. `IL-confirmed|Lancia|Y` — 4 variants

## Required implementation approach

- Every variant below has an explicit KEEP/FIX/ADD/MERGE/MOVE action. Apply these exact actions.
- For every KEEP, still verify repo-local `source_indexes` and `field_sources` are valid. KEEP does not mean skip source integrity.
- `global-reference-only` profiles must not remain in clean merely because a global spec exists. Convert to IL-likely/IL-confirmed only with embedded/repo-local Israeli source support; otherwise move to non-blocking review/archive.
- For Lamborghini, do not call it official Israeli importer clean. Treat supported rows as Israeli import/listing/special-order/parallel-import unless repo-local evidence proves a stronger route.
- Preserve lineage/aliases when merging or moving profiles.

## Embedded web-validation source summary

### 1. IL-confirmed|Kia|Sorento
WEB-VALIDATED FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
SOURCES:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל

### 2. IL-confirmed|Kia|Soul
WEB-VALIDATED FACT: Israeli sources support Kia Soul sales in Israel across 2009-2019, including 1.6 petrol configurations; later turbo/diesel rows require exact Israeli support before merging from global scope.
SOURCES:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Soul 2014 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סול-החדשה-2014-בישראל-מחירון-החל-מ-119-900-שקל

### 3. global-reference-only|Kia|Soul
WEB-VALIDATED FACT: This profile is a duplicate/split-profile candidate against IL-confirmed Kia Soul. Some rows match confirmed Israeli configurations, while manual/diesel/turbo rows need exact Israeli source support before entering clean.
SOURCES:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Kia Soul 1.6 turbo 204 hp in Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סול-1-6-טורבו-204-כ-ס-בישראל

### 4. IL-confirmed|Kia|Sportage
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCES:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל

### 5. IL-confirmed|Kia|Stinger
WEB-VALIDATED FACT: Israeli sources support Stinger GT-Line 2.0 turbo 245 hp and GT 3.3 twin-turbo 370 hp with 8-speed automatic; verify drivetrain as RWD/AWD per exact Israeli catalog rows.
SOURCES:
- Cartube Stinger Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סטינגר-בישראל-מחיר-החל-מ-279-900-שקל
- iCar Stinger spec page: https://www.icar.co.il/קיה/קיה_סטינגר/

### 6. IL-confirmed|Kia|Stonic
WEB-VALIDATED FACT: Kia Israel currently markets Stonic 2026 with 1.0 turbo EX and GT-LINE, 100 hp and prices from 129,900 NIS. Existing 2021-2024 mild-hybrid rows should not be extended blindly unless repo-local official specs prove the current 2026 model is MHEV.
SOURCES:
- Kia Israel Stonic 2026 official page: https://kia-israel.co.il/רכב/סטוניק
- iCar Stonic page: https://www.icar.co.il/קיה/קיה_סטוניק/
- Cartube Stonic 2021 facelift Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סטוניק-2021-החדש-בישראל-מחיר-החל-מ-104900-שקל

### 7. IL-confirmed|Kia|Venga
WEB-VALIDATED FACT: Israeli iCar/Cartube sources support Venga 1.6 petrol automatic, including facelift from 2015 with a 6-speed automatic replacing earlier 4-speed automatic.
SOURCES:
- iCar Kia Venga page: https://www.icar.co.il/קיה/קיה_ונגה/
- Cartube Venga 2015 Israel: https://www.cartube.co.il/חדשות-רכב/קיה-ונגה-החדשה-2015-בישראל-מחיר-מ-110,000-שקל

### 8. global-reference-only|Kia|Venga
WEB-VALIDATED FACT: This is a split/duplicate candidate against IL-confirmed Venga. EX 1.6 automatic overlaps the confirmed profile. LX 1.4 manual requires exact Israeli support; do not keep global-only in clean without it.
SOURCES:
- iCar Kia Venga page: https://www.icar.co.il/קיה/קיה_ונגה/
- Auto Kia Venga page: https://www.auto.co.il/model/kia-venga_g210

### 9. IL-likely|Lamborghini|Aventador
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCES:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

### 10. IL-confirmed|Lamborghini|Aventador
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCES:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

### 11. global-reference-only|Lamborghini|Aventador
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCES:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

### 12. global-reference-only|Lamborghini|Gallardo
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCES:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

### 13. IL-likely|Lamborghini|Huracan
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCES:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

### 14. IL-confirmed|Lamborghini|Huracan
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCES:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

### 15. IL-confirmed|Lamborghini|Urus
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCES:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

### 16. IL-likely|Lamborghini|Urus
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCES:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

### 17. global-reference-only|Lamborghini|Urus
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCES:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

### 18. IL-confirmed|Lancia|Delta
WEB-VALIDATED FACT: Israeli iCar source states Lancia returned to the Israeli market with Delta and explicitly mentions the 1.8 turbo 200 hp. Existing 1.4 turbo 120 hp manual/automatic rows should stay only if repo-local iCar/Auto variant tables ground them exactly.
SOURCES:
- iCar Lancia Delta page: https://www.icar.co.il/לנצ'יה/לנצ'יה_דלתא/
- Auto Lancia Delta page: https://www.auto.co.il/model/lancia-delta_g264

### 19. global-reference-only|Lancia|Kappa
WEB-VALIDATED FACT: Kappa is a historical Lancia model. Israeli Auto/iCar catalog pages may support local price-list/spec existence, but global-reference-only profiles must be converted to IL-likely with exact source backing or moved to non-blocking review/archive.
SOURCES:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Kappa source in repo: https://www.auto.co.il/model/lancia-kappa_g1116
- iCar Kappa source in repo: https://www.icar.co.il/lancia/lancia_kappa/

### 20. global-reference-only|Lancia|Lybra
WEB-VALIDATED FACT: Lybra was manufactured globally 1998-2005 and appears in Israeli catalog sources, but global-reference-only rows for diesel/estate/body splits need exact Israeli support before clean.
SOURCES:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Lybra source in repo: https://www.auto.co.il/model/lancia-lybra_g196
- iCar Lybra source in repo: https://www.icar.co.il/לנצ'יה/לנצ'יה_ליברה/לנצ'יה_ליברה_יד_שניה/

### 21. IL-confirmed|Lancia|Lybra
WEB-VALIDATED FACT: IL-confirmed Lybra LX 2.0 automatic sedan is plausible if exact iCar/Auto source rows support it; avoid keeping duplicate global Lybra rows beside this confirmed row.
SOURCES:
- iCar Lybra source in repo: https://www.icar.co.il/lancia/lancia_lybra/
- Auto Lybra source in repo: https://www.auto.co.il/model/lancia-lybra_g1061

### 22. IL-confirmed|Lancia|Thema
WEB-VALIDATED FACT: Cartube reports the newer Lancia Thema in Israel; Auto sources cover the 2011-2014 Thema and older 1985-1994 Thema. The 2011-2014 3.6 V6 286 hp row is credible; older 1988-1994 rows must remain only if exact Auto source supports them.
SOURCES:
- Cartube Thema Israel: https://www.cartube.co.il/חדשות-רכב/לנצ-יה-תמא-thema-החדשה-בישראל
- Auto Thema 2011-2014 source in repo: https://www.auto.co.il/model/lancia-thema_g190
- Auto Thema 1985-1994 source in repo: https://www.auto.co.il/model/lancia-thema_g189

### 23. IL-likely|Lancia|Thema
WEB-VALIDATED FACT: Turbo 16V LS is only IL-likely and appears to rely on weaker/forum-type local evidence. Do not keep as clean without exact Israeli source; move to non-blocking review if source strength remains below Tier 2/3 catalog.
SOURCES:
- Auto Thema source in repo: https://www.auto.co.il/model/lancia-thema
- CarsForum weak local discussion source in repo: https://carsforum.co.il/topic/lancia-thema-turbo-israel

### 24. global-reference-only|Lancia|Thesis
WEB-VALIDATED FACT: Lancia Thesis appears in Auto/iCar Israeli catalog sources, but the current profile is global-reference-only. Keep only exact locally supported trims; otherwise move to non-blocking review/archive.
SOURCES:
- Auto Thesis source in repo: https://www.auto.co.il/model/lancia-thesis_g400
- iCar Thesis source in repo: https://www.icar.co.il/lancia/thesis/

### 25. IL-confirmed|Lancia|Y
WEB-VALIDATED FACT: Lancia Y is historical/used-market supported by Israeli price-list/catalog sources. Because sources are weaker (Yad2/Carzone/iCar used), keep only if field_sources are valid; mark source tier carefully and avoid claiming official import.
SOURCES:
- Yad2 Lancia Y price list: https://www.yad2.co.il/vehicles/prices/lancia/y/1996-2000
- iCar Lancia Y used page: https://www.icar.co.il/לנצ'יה/לנצ'יה_Y_יד_שניה/
- Carzone Lancia Y: https://carzone.co.il/vehicles/lancia/y

---

## Variant-level decisions

# MODEL 1: IL-confirmed|Kia|Sorento
MODEL CURRENT VALUE: model year_start=2015, year_end=2024, profile_confidence=medium, variants=11
WEB-VALIDATED MODEL FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
MODEL SOURCE SET:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל

## VARIANT 1
MODEL: IL-confirmed|Kia|Sorento
CURRENT VALUE: trim=None; years=2021-2024; body=SUV; fuel=petrol; engine=2.5L; displacement=2.5; hp=180; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction required beyond adding/retaining source grounding.
WEB-VALIDATED FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
SOURCE:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל
TARGET VALUE: Keep row as historical Israeli Sorento technical variant; ensure source_indexes/field_sources remain valid.
ACTION: KEEP

## VARIANT 2
MODEL: IL-confirmed|Kia|Sorento
CURRENT VALUE: trim=None; years=2021-2024; body=SUV; fuel=diesel; engine=2.2L turbo; displacement=2.2; hp=202; transmission=8-speed dual_clutch; drivetrain=FWD; support=direct
PROBLEM: No correction required beyond adding/retaining source grounding.
WEB-VALIDATED FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
SOURCE:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל
TARGET VALUE: Keep row as historical Israeli Sorento technical variant; ensure source_indexes/field_sources remain valid.
ACTION: KEEP

## VARIANT 3
MODEL: IL-confirmed|Kia|Sorento
CURRENT VALUE: trim=None; years=2021-2024; body=SUV; fuel=diesel; engine=2.2L turbo; displacement=2.2; hp=202; transmission=8-speed dual_clutch; drivetrain=AWD; support=direct
PROBLEM: No correction required beyond adding/retaining source grounding.
WEB-VALIDATED FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
SOURCE:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל
TARGET VALUE: Keep row as historical Israeli Sorento technical variant; ensure source_indexes/field_sources remain valid.
ACTION: KEEP

## VARIANT 4
MODEL: IL-confirmed|Kia|Sorento
CURRENT VALUE: trim=None; years=2021-2024; body=SUV; fuel=hybrid; engine=1.6L turbo; displacement=1.6; hp=230; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: Current Sorento Hybrid is still sold in Israel; row is closed at 2024.
WEB-VALIDATED FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
SOURCE:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל
TARGET VALUE: Set variant year_end to 2026 or current-policy value; set model year_end to 2026; add Kia Israel official current source. Keep technical fields: 1.6L turbo hybrid, 230 hp, 6-speed automatic, FWD unless repo-local official specs prove AWD/trim-specific split.
ACTION: FIX

## VARIANT 5
MODEL: IL-confirmed|Kia|Sorento
CURRENT VALUE: trim=None; years=2021-2024; body=SUV; fuel=plug_in_hybrid; engine=1.6L turbo; displacement=1.6; hp=265; transmission=6-speed automatic; drivetrain=AWD; support=direct
PROBLEM: No correction required beyond adding/retaining source grounding.
WEB-VALIDATED FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
SOURCE:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל
TARGET VALUE: Keep row as historical Israeli Sorento technical variant; ensure source_indexes/field_sources remain valid.
ACTION: KEEP

## VARIANT 6
MODEL: IL-confirmed|Kia|Sorento
CURRENT VALUE: trim=None; years=2015-2020; body=SUV; fuel=petrol; engine=2.4L; displacement=2.4; hp=188; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction required beyond adding/retaining source grounding.
WEB-VALIDATED FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
SOURCE:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל
TARGET VALUE: Keep row as historical Israeli Sorento technical variant; ensure source_indexes/field_sources remain valid.
ACTION: KEEP

## VARIANT 7
MODEL: IL-confirmed|Kia|Sorento
CURRENT VALUE: trim=None; years=2015-2020; body=SUV; fuel=petrol; engine=2.4L; displacement=2.4; hp=188; transmission=6-speed automatic; drivetrain=AWD; support=direct
PROBLEM: No correction required beyond adding/retaining source grounding.
WEB-VALIDATED FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
SOURCE:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל
TARGET VALUE: Keep row as historical Israeli Sorento technical variant; ensure source_indexes/field_sources remain valid.
ACTION: KEEP

## VARIANT 8
MODEL: IL-confirmed|Kia|Sorento
CURRENT VALUE: trim=None; years=2015-2018; body=SUV; fuel=diesel; engine=2.2L turbo; displacement=2.2; hp=200; transmission=6-speed automatic; drivetrain=AWD; support=direct
PROBLEM: No correction required beyond adding/retaining source grounding.
WEB-VALIDATED FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
SOURCE:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל
TARGET VALUE: Keep row as historical Israeli Sorento technical variant; ensure source_indexes/field_sources remain valid.
ACTION: KEEP

## VARIANT 9
MODEL: IL-confirmed|Kia|Sorento
CURRENT VALUE: trim=None; years=2018-2020; body=SUV; fuel=diesel; engine=2.2L turbo; displacement=2.2; hp=200; transmission=8-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction required beyond adding/retaining source grounding.
WEB-VALIDATED FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
SOURCE:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל
TARGET VALUE: Keep row as historical Israeli Sorento technical variant; ensure source_indexes/field_sources remain valid.
ACTION: KEEP

## VARIANT 10
MODEL: IL-confirmed|Kia|Sorento
CURRENT VALUE: trim=None; years=2018-2020; body=SUV; fuel=diesel; engine=2.2L turbo; displacement=2.2; hp=200; transmission=8-speed automatic; drivetrain=AWD; support=direct
PROBLEM: No correction required beyond adding/retaining source grounding.
WEB-VALIDATED FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
SOURCE:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל
TARGET VALUE: Keep row as historical Israeli Sorento technical variant; ensure source_indexes/field_sources remain valid.
ACTION: KEEP

## VARIANT 11
MODEL: IL-confirmed|Kia|Sorento
CURRENT VALUE: trim=None; years=2018-2020; body=SUV; fuel=petrol; engine=3.5L v6; displacement=3.5; hp=277; transmission=8-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction required beyond adding/retaining source grounding.
WEB-VALIDATED FACT: Israeli 2021 launch sources support Sorento 2.5 petrol 180 hp 6AT, 2.2 diesel 202 hp 8DCT, and 1.6 turbo hybrid 230 hp 6AT. Kia Israel currently markets Sorento Hybrid 2026 with 1.6 turbo petrol plus electric motor and 230 hp, so the hybrid line must not remain closed at 2024.
SOURCE:
- Kia Israel Sorento 2026 official page: https://kia-israel.co.il/רכב/קיה-סורנטו
- iCar Sorento 2021 Israel launch/specs: https://www.icar.co.il/חדשות_רכב/קיה_סורנטו_החדש_בישראל:_מ-234,900_שקלים/
- Cartube Sorento 2021 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סורנטו-החדש-2021-בישראל-מחיר-החל-מ-234,900-שקל
TARGET VALUE: Keep row as historical Israeli Sorento technical variant; ensure source_indexes/field_sources remain valid.
ACTION: KEEP

# MODEL 2: IL-confirmed|Kia|Soul
MODEL CURRENT VALUE: model year_start=2009, year_end=2019, profile_confidence=medium, variants=3
WEB-VALIDATED MODEL FACT: Israeli sources support Kia Soul sales in Israel across 2009-2019, including 1.6 petrol configurations; later turbo/diesel rows require exact Israeli support before merging from global scope.
MODEL SOURCE SET:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Soul 2014 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סול-החדשה-2014-בישראל-מחירון-החל-מ-119-900-שקל

## VARIANT 1
MODEL: IL-confirmed|Kia|Soul
CURRENT VALUE: trim=None; years=2009-2011; body=Crossover; fuel=petrol; engine=1.6L; displacement=1.6; hp=126; transmission=4-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction found in embedded validation pass.
WEB-VALIDATED FACT: Israeli sources support Kia Soul sales in Israel across 2009-2019, including 1.6 petrol configurations; later turbo/diesel rows require exact Israeli support before merging from global scope.
SOURCE:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Soul 2014 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סול-החדשה-2014-בישראל-מחירון-החל-מ-119-900-שקל
TARGET VALUE: Keep if all source_indexes and field_sources are valid; no specific correction found in RUN1.
ACTION: KEEP

## VARIANT 2
MODEL: IL-confirmed|Kia|Soul
CURRENT VALUE: trim=None; years=2012-2013; body=Crossover; fuel=petrol; engine=1.6L gdi; displacement=1.6; hp=140; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction found in embedded validation pass.
WEB-VALIDATED FACT: Israeli sources support Kia Soul sales in Israel across 2009-2019, including 1.6 petrol configurations; later turbo/diesel rows require exact Israeli support before merging from global scope.
SOURCE:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Soul 2014 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סול-החדשה-2014-בישראל-מחירון-החל-מ-119-900-שקל
TARGET VALUE: Keep if all source_indexes and field_sources are valid; no specific correction found in RUN1.
ACTION: KEEP

## VARIANT 3
MODEL: IL-confirmed|Kia|Soul
CURRENT VALUE: trim=None; years=2014-2019; body=Crossover; fuel=petrol; engine=1.6L gdi; displacement=1.6; hp=132; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction found in embedded validation pass.
WEB-VALIDATED FACT: Israeli sources support Kia Soul sales in Israel across 2009-2019, including 1.6 petrol configurations; later turbo/diesel rows require exact Israeli support before merging from global scope.
SOURCE:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Soul 2014 Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סול-החדשה-2014-בישראל-מחירון-החל-מ-119-900-שקל
TARGET VALUE: Keep if all source_indexes and field_sources are valid; no specific correction found in RUN1.
ACTION: KEEP

# MODEL 3: global-reference-only|Kia|Soul
MODEL CURRENT VALUE: model year_start=2010, year_end=2019, profile_confidence=medium, variants=7
WEB-VALIDATED MODEL FACT: This profile is a duplicate/split-profile candidate against IL-confirmed Kia Soul. Some rows match confirmed Israeli configurations, while manual/diesel/turbo rows need exact Israeli source support before entering clean.
MODEL SOURCE SET:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Kia Soul 1.6 turbo 204 hp in Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סול-1-6-טורבו-204-כ-ס-בישראל

## VARIANT 1
MODEL: global-reference-only|Kia|Soul
CURRENT VALUE: trim=None; years=2010-2011; body=Crossover; fuel=petrol; engine=1.6L; displacement=1.6; hp=126; transmission=automatic; drivetrain=FWD; support=direct
PROBLEM: Duplicate/split-profile clean entry duplicates IL-confirmed Soul.
WEB-VALIDATED FACT: This profile is a duplicate/split-profile candidate against IL-confirmed Kia Soul. Some rows match confirmed Israeli configurations, while manual/diesel/turbo rows need exact Israeli source support before entering clean.
SOURCE:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Kia Soul 1.6 turbo 204 hp in Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סול-1-6-טורבו-204-כ-ס-בישראל
TARGET VALUE: Merge into IL-confirmed Kia Soul equivalent row or delete as duplicate if all fields overlap; do not keep a separate global-reference-only clean model.
ACTION: MERGE / DELETE DUPLICATE

## VARIANT 2
MODEL: global-reference-only|Kia|Soul
CURRENT VALUE: trim=None; years=2010-2011; body=Crossover; fuel=petrol; engine=1.6L; displacement=1.6; hp=126; transmission=manual; drivetrain=FWD; support=direct
PROBLEM: Manual rows are not grounded strongly enough in embedded facts for clean.
WEB-VALIDATED FACT: This profile is a duplicate/split-profile candidate against IL-confirmed Kia Soul. Some rows match confirmed Israeli configurations, while manual/diesel/turbo rows need exact Israeli source support before entering clean.
SOURCE:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Kia Soul 1.6 turbo 204 hp in Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סול-1-6-טורבו-204-כ-ס-בישראל
TARGET VALUE: Keep out of clean unless exact Israeli iCar/Auto source proves manual transmission was sold locally for that year range; if proved, merge into IL-confirmed Soul and normalize transmission to 6-speed manual where applicable.
ACTION: MOVE TO REVIEW

## VARIANT 3
MODEL: global-reference-only|Kia|Soul
CURRENT VALUE: trim=None; years=2012-2013; body=Crossover; fuel=petrol; engine=1.6L; displacement=1.6; hp=140; transmission=automatic; drivetrain=FWD; support=direct
PROBLEM: Duplicate/split-profile clean entry duplicates IL-confirmed Soul.
WEB-VALIDATED FACT: This profile is a duplicate/split-profile candidate against IL-confirmed Kia Soul. Some rows match confirmed Israeli configurations, while manual/diesel/turbo rows need exact Israeli source support before entering clean.
SOURCE:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Kia Soul 1.6 turbo 204 hp in Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סול-1-6-טורבו-204-כ-ס-בישראל
TARGET VALUE: Merge into IL-confirmed Kia Soul equivalent row or delete as duplicate if all fields overlap; do not keep a separate global-reference-only clean model.
ACTION: MERGE / DELETE DUPLICATE

## VARIANT 4
MODEL: global-reference-only|Kia|Soul
CURRENT VALUE: trim=None; years=2012-2013; body=Crossover; fuel=petrol; engine=1.6L; displacement=1.6; hp=140; transmission=manual; drivetrain=FWD; support=direct
PROBLEM: Manual rows are not grounded strongly enough in embedded facts for clean.
WEB-VALIDATED FACT: This profile is a duplicate/split-profile candidate against IL-confirmed Kia Soul. Some rows match confirmed Israeli configurations, while manual/diesel/turbo rows need exact Israeli source support before entering clean.
SOURCE:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Kia Soul 1.6 turbo 204 hp in Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סול-1-6-טורבו-204-כ-ס-בישראל
TARGET VALUE: Keep out of clean unless exact Israeli iCar/Auto source proves manual transmission was sold locally for that year range; if proved, merge into IL-confirmed Soul and normalize transmission to 6-speed manual where applicable.
ACTION: MOVE TO REVIEW

## VARIANT 5
MODEL: global-reference-only|Kia|Soul
CURRENT VALUE: trim=None; years=2014-2019; body=Crossover; fuel=petrol; engine=1.6L; displacement=1.6; hp=132; transmission=automatic; drivetrain=FWD; support=direct
PROBLEM: Duplicate/split-profile clean entry duplicates IL-confirmed Soul.
WEB-VALIDATED FACT: This profile is a duplicate/split-profile candidate against IL-confirmed Kia Soul. Some rows match confirmed Israeli configurations, while manual/diesel/turbo rows need exact Israeli source support before entering clean.
SOURCE:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Kia Soul 1.6 turbo 204 hp in Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סול-1-6-טורבו-204-כ-ס-בישראל
TARGET VALUE: Merge into IL-confirmed Kia Soul equivalent row or delete as duplicate if all fields overlap; do not keep a separate global-reference-only clean model.
ACTION: MERGE / DELETE DUPLICATE

## VARIANT 6
MODEL: global-reference-only|Kia|Soul
CURRENT VALUE: trim=None; years=2016-2019; body=Crossover; fuel=diesel; engine=1.6L; displacement=1.6; hp=136; transmission=dual_clutch; drivetrain=FWD; support=direct
PROBLEM: Potential legitimate Israeli later variants are trapped in global-reference-only profile.
WEB-VALIDATED FACT: This profile is a duplicate/split-profile candidate against IL-confirmed Kia Soul. Some rows match confirmed Israeli configurations, while manual/diesel/turbo rows need exact Israeli source support before entering clean.
SOURCE:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Kia Soul 1.6 turbo 204 hp in Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סול-1-6-טורבו-204-כ-ס-בישראל
TARGET VALUE: If repo-local Israeli source explicitly supports diesel 136 hp or 1.6 turbo 204 hp, move into IL-confirmed Kia Soul with normalized transmission 7-speed dual_clutch for turbo/DCT where applicable; otherwise move to non-blocking review.
ACTION: SPLIT / MERGE

## VARIANT 7
MODEL: global-reference-only|Kia|Soul
CURRENT VALUE: trim=None; years=2017-2019; body=Crossover; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=204; transmission=dual_clutch; drivetrain=FWD; support=direct
PROBLEM: Potential legitimate Israeli later variants are trapped in global-reference-only profile.
WEB-VALIDATED FACT: This profile is a duplicate/split-profile candidate against IL-confirmed Kia Soul. Some rows match confirmed Israeli configurations, while manual/diesel/turbo rows need exact Israeli source support before entering clean.
SOURCE:
- iCar Kia Soul page: https://www.icar.co.il/קיה/קיה_סול/
- Cartube Kia Soul 1.6 turbo 204 hp in Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סול-1-6-טורבו-204-כ-ס-בישראל
TARGET VALUE: If repo-local Israeli source explicitly supports diesel 136 hp or 1.6 turbo 204 hp, move into IL-confirmed Kia Soul with normalized transmission 7-speed dual_clutch for turbo/DCT where applicable; otherwise move to non-blocking review.
ACTION: SPLIT / MERGE

# MODEL 4: IL-confirmed|Kia|Sportage
MODEL CURRENT VALUE: model year_start=2010, year_end=2026, profile_confidence=medium, variants=12
WEB-VALIDATED MODEL FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
MODEL SOURCE SET:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל

## VARIANT 1
MODEL: IL-confirmed|Kia|Sportage
CURRENT VALUE: trim=None; years=2010-2015; body=SUV; fuel=petrol; engine=2.0L; displacement=2.0; hp=163; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction required beyond source audit.
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCE:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל
TARGET VALUE: Keep as historical Sportage row if field_sources valid.
ACTION: KEEP

## VARIANT 2
MODEL: IL-confirmed|Kia|Sportage
CURRENT VALUE: trim=None; years=2010-2015; body=SUV; fuel=petrol; engine=2.0L; displacement=2.0; hp=166; transmission=6-speed automatic; drivetrain=AWD; support=direct
PROBLEM: No correction required beyond source audit.
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCE:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל
TARGET VALUE: Keep as historical Sportage row if field_sources valid.
ACTION: KEEP

## VARIANT 3
MODEL: IL-confirmed|Kia|Sportage
CURRENT VALUE: trim=None; years=2015-2016; body=SUV; fuel=petrol; engine=1.6L gdi; displacement=1.6; hp=135; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction required beyond source audit.
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCE:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל
TARGET VALUE: Keep as historical Sportage row if field_sources valid.
ACTION: KEEP

## VARIANT 4
MODEL: IL-confirmed|Kia|Sportage
CURRENT VALUE: trim=None; years=2016-2021; body=SUV; fuel=petrol; engine=1.6L gdi; displacement=1.6; hp=132; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction required beyond source audit.
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCE:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל
TARGET VALUE: Keep as historical Sportage row if field_sources valid.
ACTION: KEEP

## VARIANT 5
MODEL: IL-confirmed|Kia|Sportage
CURRENT VALUE: trim=None; years=2016-2021; body=SUV; fuel=petrol; engine=2.0L mpi; displacement=2.0; hp=155; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction required beyond source audit.
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCE:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל
TARGET VALUE: Keep as historical Sportage row if field_sources valid.
ACTION: KEEP

## VARIANT 6
MODEL: IL-confirmed|Kia|Sportage
CURRENT VALUE: trim=None; years=2016-2021; body=SUV; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=177; transmission=7-speed dual_clutch; drivetrain=FWD; support=direct
PROBLEM: No correction required beyond source audit.
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCE:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל
TARGET VALUE: Keep as historical Sportage row if field_sources valid.
ACTION: KEEP

## VARIANT 7
MODEL: IL-confirmed|Kia|Sportage
CURRENT VALUE: trim=None; years=2022-2023; body=SUV; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=150; transmission=7-speed dual_clutch; drivetrain=FWD; support=direct
PROBLEM: No correction required beyond source audit.
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCE:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל
TARGET VALUE: Keep as historical Sportage row if field_sources valid.
ACTION: KEEP

## VARIANT 8
MODEL: IL-confirmed|Kia|Sportage
CURRENT VALUE: trim=None; years=2024-2026; body=SUV; fuel=mild_hybrid; engine=1.6L turbo; displacement=1.6; hp=160; transmission=7-speed dual_clutch; drivetrain=FWD; support=direct
PROBLEM: Current status needs official 2026 grounding attached.
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCE:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל
TARGET VALUE: Keep current 2024-2026/2022-2026 row; ensure Kia Israel 2026 official/current source is attached. For hybrid 230 hp, attach Hybrid Long official/current source.
ACTION: KEEP / VERIFY CURRENT

## VARIANT 9
MODEL: IL-confirmed|Kia|Sportage
CURRENT VALUE: trim=None; years=2022-2023; body=SUV; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=180; transmission=7-speed dual_clutch; drivetrain=FWD; support=direct
PROBLEM: No correction required beyond source audit.
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCE:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל
TARGET VALUE: Keep as historical Sportage row if field_sources valid.
ACTION: KEEP

## VARIANT 10
MODEL: IL-confirmed|Kia|Sportage
CURRENT VALUE: trim=None; years=2022-2026; body=SUV; fuel=petrol; engine=2.0L; displacement=2.0; hp=156; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: Current status needs official 2026 grounding attached.
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCE:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל
TARGET VALUE: Keep current 2024-2026/2022-2026 row; ensure Kia Israel 2026 official/current source is attached. For hybrid 230 hp, attach Hybrid Long official/current source.
ACTION: KEEP / VERIFY CURRENT

## VARIANT 11
MODEL: IL-confirmed|Kia|Sportage
CURRENT VALUE: trim=None; years=2022-2026; body=SUV; fuel=hybrid; engine=1.6L turbo; displacement=1.6; hp=230; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: Current status needs official 2026 grounding attached.
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCE:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל
TARGET VALUE: Keep current 2024-2026/2022-2026 row; ensure Kia Israel 2026 official/current source is attached. For hybrid 230 hp, attach Hybrid Long official/current source.
ACTION: KEEP / VERIFY CURRENT

## VARIANT 12
MODEL: IL-confirmed|Kia|Sportage
CURRENT VALUE: trim=None; years=2023-2026; body=SUV; fuel=plug_in_hybrid; engine=1.6L turbo; displacement=1.6; hp=265; transmission=6-speed automatic; drivetrain=AWD; support=direct
PROBLEM: PHEV row may be over-opened to 2026.
WEB-VALIDATED FACT: Israeli sources support Sportage historical ICE variants and current 2026 presence. Kia Israel currently lists Sportage 2026, and Kia Israel/Cartube support 2026 Hybrid Long 1.6T hybrid 230 hp. 2022-on PHEV was reported in Israel, but current official page does not prove PHEV remains current in 2026.
SOURCE:
- Kia Israel Sportage 2026 official page: https://kia-israel.co.il/רכב/ספורטאז
- Kia Israel Sportage Hybrid Long PDF/news: https://kia-israel.co.il/catalog/mifrat_sportage_Hybrid%20LONG.pdf
- Kia Israel / Cartube Sportage 2026 Hybrid Long news: https://kia-israel.co.il/חדשות/קיה-ספורטאז-החדש-2026-בישראל-בגרסת-הייברי
- Gear Sportage PHEV Israel: https://www.gear.co.il/כתבות_רכב/2023-01-23-N01-קיה-ספורטאז-פלאג-אין-בישראל
TARGET VALUE: Keep 2023-2026 only if repo-local official/current source proves PHEV is still marketed in 2026; otherwise set year_end to last locally supported year and keep non-current.
ACTION: KEEP HISTORICAL OR FIX YEAR_END

# MODEL 5: IL-confirmed|Kia|Stinger
MODEL CURRENT VALUE: model year_start=2018, year_end=2023, profile_confidence=medium, variants=2
WEB-VALIDATED MODEL FACT: Israeli sources support Stinger GT-Line 2.0 turbo 245 hp and GT 3.3 twin-turbo 370 hp with 8-speed automatic; verify drivetrain as RWD/AWD per exact Israeli catalog rows.
MODEL SOURCE SET:
- Cartube Stinger Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סטינגר-בישראל-מחיר-החל-מ-279-900-שקל
- iCar Stinger spec page: https://www.icar.co.il/קיה/קיה_סטינגר/

## VARIANT 1
MODEL: IL-confirmed|Kia|Stinger
CURRENT VALUE: trim='GT-Line'; years=2018-2023; body=Liftback; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=245; transmission=8-speed automatic; drivetrain=RWD; support=direct
PROBLEM: Stinger drivetrain can differ by market and must be source-grounded.
WEB-VALIDATED FACT: Israeli sources support Stinger GT-Line 2.0 turbo 245 hp and GT 3.3 twin-turbo 370 hp with 8-speed automatic; verify drivetrain as RWD/AWD per exact Israeli catalog rows.
SOURCE:
- Cartube Stinger Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סטינגר-בישראל-מחיר-החל-מ-279-900-שקל
- iCar Stinger spec page: https://www.icar.co.il/קיה/קיה_סטינגר/
TARGET VALUE: Keep variant, but verify drivetrain against exact Israeli source. If iCar/Cartube proves GT 3.3 is RWD rather than AWD for Israel, fix drivetrain; otherwise retain AWD only with explicit source.
ACTION: KEEP / VERIFY DRIVETRAIN

## VARIANT 2
MODEL: IL-confirmed|Kia|Stinger
CURRENT VALUE: trim='GT'; years=2018-2020; body=Liftback; fuel=petrol; engine=3.3L v6 twin-turbo; displacement=3.3; hp=370; transmission=8-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Stinger drivetrain can differ by market and must be source-grounded.
WEB-VALIDATED FACT: Israeli sources support Stinger GT-Line 2.0 turbo 245 hp and GT 3.3 twin-turbo 370 hp with 8-speed automatic; verify drivetrain as RWD/AWD per exact Israeli catalog rows.
SOURCE:
- Cartube Stinger Israel launch: https://www.cartube.co.il/חדשות-רכב/קיה-סטינגר-בישראל-מחיר-החל-מ-279-900-שקל
- iCar Stinger spec page: https://www.icar.co.il/קיה/קיה_סטינגר/
TARGET VALUE: Keep variant, but verify drivetrain against exact Israeli source. If iCar/Cartube proves GT 3.3 is RWD rather than AWD for Israel, fix drivetrain; otherwise retain AWD only with explicit source.
ACTION: KEEP / VERIFY DRIVETRAIN

# MODEL 6: IL-confirmed|Kia|Stonic
MODEL CURRENT VALUE: model year_start=2018, year_end=2024, profile_confidence=medium, variants=4
WEB-VALIDATED MODEL FACT: Kia Israel currently markets Stonic 2026 with 1.0 turbo EX and GT-LINE, 100 hp and prices from 129,900 NIS. Existing 2021-2024 mild-hybrid rows should not be extended blindly unless repo-local official specs prove the current 2026 model is MHEV.
MODEL SOURCE SET:
- Kia Israel Stonic 2026 official page: https://kia-israel.co.il/רכב/סטוניק
- iCar Stonic page: https://www.icar.co.il/קיה/קיה_סטוניק/
- Cartube Stonic 2021 facelift Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סטוניק-2021-החדש-בישראל-מחיר-החל-מ-104900-שקל

## VARIANT 1
MODEL: IL-confirmed|Kia|Stonic
CURRENT VALUE: trim=None; years=2018-2024; body=Crossover; fuel=petrol; engine=1.4L; displacement=1.4; hp=100; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No current-extension correction for this historical row.
WEB-VALIDATED FACT: Kia Israel currently markets Stonic 2026 with 1.0 turbo EX and GT-LINE, 100 hp and prices from 129,900 NIS. Existing 2021-2024 mild-hybrid rows should not be extended blindly unless repo-local official specs prove the current 2026 model is MHEV.
SOURCE:
- Kia Israel Stonic 2026 official page: https://kia-israel.co.il/רכב/סטוניק
- iCar Stonic page: https://www.icar.co.il/קיה/קיה_סטוניק/
- Cartube Stonic 2021 facelift Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סטוניק-2021-החדש-בישראל-מחיר-החל-מ-104900-שקל
TARGET VALUE: Keep as historical Stonic row; preserve 2018-2024/2021 ranges if field sources are valid.
ACTION: KEEP

## VARIANT 2
MODEL: IL-confirmed|Kia|Stonic
CURRENT VALUE: trim=None; years=2018-2021; body=Crossover; fuel=petrol; engine=1.0L turbo; displacement=1.0; hp=120; transmission=7-speed dual_clutch; drivetrain=FWD; support=direct
PROBLEM: No current-extension correction for this historical row.
WEB-VALIDATED FACT: Kia Israel currently markets Stonic 2026 with 1.0 turbo EX and GT-LINE, 100 hp and prices from 129,900 NIS. Existing 2021-2024 mild-hybrid rows should not be extended blindly unless repo-local official specs prove the current 2026 model is MHEV.
SOURCE:
- Kia Israel Stonic 2026 official page: https://kia-israel.co.il/רכב/סטוניק
- iCar Stonic page: https://www.icar.co.il/קיה/קיה_סטוניק/
- Cartube Stonic 2021 facelift Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סטוניק-2021-החדש-בישראל-מחיר-החל-מ-104900-שקל
TARGET VALUE: Keep as historical Stonic row; preserve 2018-2024/2021 ranges if field sources are valid.
ACTION: KEEP

## VARIANT 3
MODEL: IL-confirmed|Kia|Stonic
CURRENT VALUE: trim=None; years=2021-2024; body=Crossover; fuel=mild_hybrid; engine=1.0L turbo; displacement=1.0; hp=100; transmission=7-speed dual_clutch; drivetrain=FWD; support=direct
PROBLEM: Model is incorrectly closed at 2024; current 2026 source shows 1.0 turbo 100 hp EX/GT-LINE.
WEB-VALIDATED FACT: Kia Israel currently markets Stonic 2026 with 1.0 turbo EX and GT-LINE, 100 hp and prices from 129,900 NIS. Existing 2021-2024 mild-hybrid rows should not be extended blindly unless repo-local official specs prove the current 2026 model is MHEV.
SOURCE:
- Kia Israel Stonic 2026 official page: https://kia-israel.co.il/רכב/סטוניק
- iCar Stonic page: https://www.icar.co.il/קיה/קיה_סטוניק/
- Cartube Stonic 2021 facelift Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סטוניק-2021-החדש-בישראל-מחיר-החל-מ-104900-שקל
TARGET VALUE: Keep 2021-2024 mild-hybrid rows as historical only. Add/fix current 2026 Stonic 1.0 turbo 100 hp EX and GT-LINE rows from Kia Israel; do not extend 120 hp MHEV to 2026 without source. Set model year_end to 2026.
ACTION: KEEP + ADD CURRENT FIX

## VARIANT 4
MODEL: IL-confirmed|Kia|Stonic
CURRENT VALUE: trim=None; years=2021-2024; body=Crossover; fuel=mild_hybrid; engine=1.0L turbo; displacement=1.0; hp=120; transmission=7-speed dual_clutch; drivetrain=FWD; support=direct
PROBLEM: Model is incorrectly closed at 2024; current 2026 source shows 1.0 turbo 100 hp EX/GT-LINE.
WEB-VALIDATED FACT: Kia Israel currently markets Stonic 2026 with 1.0 turbo EX and GT-LINE, 100 hp and prices from 129,900 NIS. Existing 2021-2024 mild-hybrid rows should not be extended blindly unless repo-local official specs prove the current 2026 model is MHEV.
SOURCE:
- Kia Israel Stonic 2026 official page: https://kia-israel.co.il/רכב/סטוניק
- iCar Stonic page: https://www.icar.co.il/קיה/קיה_סטוניק/
- Cartube Stonic 2021 facelift Israel: https://www.cartube.co.il/חדשות-רכב/קיה-סטוניק-2021-החדש-בישראל-מחיר-החל-מ-104900-שקל
TARGET VALUE: Keep 2021-2024 mild-hybrid rows as historical only. Add/fix current 2026 Stonic 1.0 turbo 100 hp EX and GT-LINE rows from Kia Israel; do not extend 120 hp MHEV to 2026 without source. Set model year_end to 2026.
ACTION: KEEP + ADD CURRENT FIX

# MODEL 7: IL-confirmed|Kia|Venga
MODEL CURRENT VALUE: model year_start=2010, year_end=2019, profile_confidence=medium, variants=2
WEB-VALIDATED MODEL FACT: Israeli iCar/Cartube sources support Venga 1.6 petrol automatic, including facelift from 2015 with a 6-speed automatic replacing earlier 4-speed automatic.
MODEL SOURCE SET:
- iCar Kia Venga page: https://www.icar.co.il/קיה/קיה_ונגה/
- Cartube Venga 2015 Israel: https://www.cartube.co.il/חדשות-רכב/קיה-ונגה-החדשה-2015-בישראל-מחיר-מ-110,000-שקל

## VARIANT 1
MODEL: IL-confirmed|Kia|Venga
CURRENT VALUE: trim=None; years=2010-2014; body=MPV; fuel=petrol; engine=1.6L; displacement=1.6; hp=125; transmission=4-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction required if source references are valid.
WEB-VALIDATED FACT: Israeli iCar/Cartube sources support Venga 1.6 petrol automatic, including facelift from 2015 with a 6-speed automatic replacing earlier 4-speed automatic.
SOURCE:
- iCar Kia Venga page: https://www.icar.co.il/קיה/קיה_ונגה/
- Cartube Venga 2015 Israel: https://www.cartube.co.il/חדשות-רכב/קיה-ונגה-החדשה-2015-בישראל-מחיר-מ-110,000-שקל
TARGET VALUE: Keep confirmed 1.6 petrol automatic Venga row; ensure pre/post-2015 gearbox split remains 4AT then 6AT.
ACTION: KEEP

## VARIANT 2
MODEL: IL-confirmed|Kia|Venga
CURRENT VALUE: trim=None; years=2015-2019; body=MPV; fuel=petrol; engine=1.6L; displacement=1.6; hp=125; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: No correction required if source references are valid.
WEB-VALIDATED FACT: Israeli iCar/Cartube sources support Venga 1.6 petrol automatic, including facelift from 2015 with a 6-speed automatic replacing earlier 4-speed automatic.
SOURCE:
- iCar Kia Venga page: https://www.icar.co.il/קיה/קיה_ונגה/
- Cartube Venga 2015 Israel: https://www.cartube.co.il/חדשות-רכב/קיה-ונגה-החדשה-2015-בישראל-מחיר-מ-110,000-שקל
TARGET VALUE: Keep confirmed 1.6 petrol automatic Venga row; ensure pre/post-2015 gearbox split remains 4AT then 6AT.
ACTION: KEEP

# MODEL 8: global-reference-only|Kia|Venga
MODEL CURRENT VALUE: model year_start=2010, year_end=2015, profile_confidence=medium, variants=2
WEB-VALIDATED MODEL FACT: This is a split/duplicate candidate against IL-confirmed Venga. EX 1.6 automatic overlaps the confirmed profile. LX 1.4 manual requires exact Israeli support; do not keep global-only in clean without it.
MODEL SOURCE SET:
- iCar Kia Venga page: https://www.icar.co.il/קיה/קיה_ונגה/
- Auto Kia Venga page: https://www.auto.co.il/model/kia-venga_g210

## VARIANT 1
MODEL: global-reference-only|Kia|Venga
CURRENT VALUE: trim='EX'; years=2010-2015; body=MPV; fuel=petrol; engine=1.6L; displacement=1.6; hp=125; transmission=4-speed automatic; drivetrain=FWD; support=direct
PROBLEM: Duplicate/split-profile of confirmed Venga.
WEB-VALIDATED FACT: This is a split/duplicate candidate against IL-confirmed Venga. EX 1.6 automatic overlaps the confirmed profile. LX 1.4 manual requires exact Israeli support; do not keep global-only in clean without it.
SOURCE:
- iCar Kia Venga page: https://www.icar.co.il/קיה/קיה_ונגה/
- Auto Kia Venga page: https://www.auto.co.il/model/kia-venga_g210
TARGET VALUE: Merge with IL-confirmed Kia Venga 1.6 automatic row; do not keep separate global-reference-only EX duplicate.
ACTION: MERGE / DELETE DUPLICATE

## VARIANT 2
MODEL: global-reference-only|Kia|Venga
CURRENT VALUE: trim='LX'; years=2010-2015; body=MPV; fuel=petrol; engine=1.4L; displacement=1.4; hp=90; transmission=5-speed manual; drivetrain=FWD; support=direct
PROBLEM: 1.4 manual is not grounded strongly enough in embedded facts.
WEB-VALIDATED FACT: This is a split/duplicate candidate against IL-confirmed Venga. EX 1.6 automatic overlaps the confirmed profile. LX 1.4 manual requires exact Israeli support; do not keep global-only in clean without it.
SOURCE:
- iCar Kia Venga page: https://www.icar.co.il/קיה/קיה_ונגה/
- Auto Kia Venga page: https://www.auto.co.il/model/kia-venga_g210
TARGET VALUE: Keep 1.4 LX manual out of clean unless exact Israeli source proves local sale; if proved, merge into IL-confirmed Venga as separate 1.4 manual variant.
ACTION: MOVE TO REVIEW

# MODEL 9: IL-likely|Lamborghini|Aventador
MODEL CURRENT VALUE: model year_start=2011, year_end=2017, profile_confidence=medium, variants=3
WEB-VALIDATED MODEL FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
MODEL SOURCE SET:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

## VARIANT 1
MODEL: IL-likely|Lamborghini|Aventador
CURRENT VALUE: trim='LP 700-4'; years=2011-2016; body=Coupe; fuel=petrol; engine=6.5L v12; displacement=6.5; hp=700; transmission=7-speed automatic; drivetrain=AWD; support=direct
PROBLEM: IL-likely exotic rows are not official-importer clean by default.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep only if exact Auto/Israeli catalog supports this exact LP trim/body/year. Otherwise move to non-blocking review. If kept, mark import_route as special_order/parallel, not official.
ACTION: MOVE TO REVIEW OR FIX SOURCE_SCOPE

## VARIANT 2
MODEL: IL-likely|Lamborghini|Aventador
CURRENT VALUE: trim='SV LP 750-4'; years=2015-2017; body=Coupe; fuel=petrol; engine=6.5L v12; displacement=6.5; hp=750; transmission=7-speed automatic; drivetrain=AWD; support=direct
PROBLEM: IL-likely exotic rows are not official-importer clean by default.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep only if exact Auto/Israeli catalog supports this exact LP trim/body/year. Otherwise move to non-blocking review. If kept, mark import_route as special_order/parallel, not official.
ACTION: MOVE TO REVIEW OR FIX SOURCE_SCOPE

## VARIANT 3
MODEL: IL-likely|Lamborghini|Aventador
CURRENT VALUE: trim='LP 700-4'; years=2013-2016; body=Roadster; fuel=petrol; engine=6.5L v12; displacement=6.5; hp=700; transmission=7-speed automatic; drivetrain=AWD; support=direct
PROBLEM: IL-likely exotic rows are not official-importer clean by default.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep only if exact Auto/Israeli catalog supports this exact LP trim/body/year. Otherwise move to non-blocking review. If kept, mark import_route as special_order/parallel, not official.
ACTION: MOVE TO REVIEW OR FIX SOURCE_SCOPE

# MODEL 10: IL-confirmed|Lamborghini|Aventador
MODEL CURRENT VALUE: model year_start=2017, year_end=2021, profile_confidence=medium, variants=2
WEB-VALIDATED MODEL FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
MODEL SOURCE SET:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

## VARIANT 1
MODEL: IL-confirmed|Lamborghini|Aventador
CURRENT VALUE: trim='S LP 740-4'; years=2017-2021; body=Coupe; fuel=petrol; engine=6.5L v12; displacement=6.5; hp=740; transmission=7-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Israeli evidence supports presence/listing but not normal official importer sales.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep only with exact Israeli Auto/Cartube support; set/import-note as special_order/parallel/import listing, not official importer.
ACTION: KEEP WITH SOURCE_SCOPE FIX

## VARIANT 2
MODEL: IL-confirmed|Lamborghini|Aventador
CURRENT VALUE: trim='SVJ LP 770-4'; years=2018-2021; body=Coupe; fuel=petrol; engine=6.5L v12; displacement=6.5; hp=770; transmission=7-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Israeli evidence supports presence/listing but not normal official importer sales.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep only with exact Israeli Auto/Cartube support; set/import-note as special_order/parallel/import listing, not official importer.
ACTION: KEEP WITH SOURCE_SCOPE FIX

# MODEL 11: global-reference-only|Lamborghini|Aventador
MODEL CURRENT VALUE: model year_start=2021, year_end=2022, profile_confidence=medium, variants=1
WEB-VALIDATED MODEL FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
MODEL SOURCE SET:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

## VARIANT 1
MODEL: global-reference-only|Lamborghini|Aventador
CURRENT VALUE: trim='Ultimae LP 780-4'; years=2021-2022; body=Coupe; fuel=petrol; engine=6.5L v12; displacement=6.5; hp=780; transmission=7-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Ultimae row is global-reference-only.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Do not clean as Israeli without exact local import/listing source; global launch article alone is insufficient.
ACTION: MOVE TO REVIEW

# MODEL 12: global-reference-only|Lamborghini|Gallardo
MODEL CURRENT VALUE: model year_start=2006, year_end=2013, profile_confidence=medium, variants=5
WEB-VALIDATED MODEL FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
MODEL SOURCE SET:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

## VARIANT 1
MODEL: global-reference-only|Lamborghini|Gallardo
CURRENT VALUE: trim='LP560-4'; years=2008-2013; body=Coupe; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=560; transmission=6-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Historical exotic trim-level evidence is weaker than required for clean global-reference-only rows.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep only if Auto/Gear Israeli catalog supports this exact Gallardo variant. If source only proves generic model, move variant to non-blocking review.
ACTION: MOVE TO REVIEW OR FIX TO IL-LIKELY

## VARIANT 2
MODEL: global-reference-only|Lamborghini|Gallardo
CURRENT VALUE: trim='LP560-4'; years=2008-2013; body=Convertible; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=560; transmission=6-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Historical exotic trim-level evidence is weaker than required for clean global-reference-only rows.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep only if Auto/Gear Israeli catalog supports this exact Gallardo variant. If source only proves generic model, move variant to non-blocking review.
ACTION: MOVE TO REVIEW OR FIX TO IL-LIKELY

## VARIANT 3
MODEL: global-reference-only|Lamborghini|Gallardo
CURRENT VALUE: trim='LP550-2'; years=2009-2013; body=Coupe; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=550; transmission=6-speed automatic; drivetrain=RWD; support=direct
PROBLEM: Historical exotic trim-level evidence is weaker than required for clean global-reference-only rows.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep only if Auto/Gear Israeli catalog supports this exact Gallardo variant. If source only proves generic model, move variant to non-blocking review.
ACTION: MOVE TO REVIEW OR FIX TO IL-LIKELY

## VARIANT 4
MODEL: global-reference-only|Lamborghini|Gallardo
CURRENT VALUE: trim='LP570-4 Superleggera'; years=2010-2013; body=Coupe; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=570; transmission=6-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Historical exotic trim-level evidence is weaker than required for clean global-reference-only rows.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep only if Auto/Gear Israeli catalog supports this exact Gallardo variant. If source only proves generic model, move variant to non-blocking review.
ACTION: MOVE TO REVIEW OR FIX TO IL-LIKELY

## VARIANT 5
MODEL: global-reference-only|Lamborghini|Gallardo
CURRENT VALUE: trim=None; years=2006-2008; body=Coupe; fuel=petrol; engine=5.0L v10; displacement=5.0; hp=520; transmission=6-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Historical exotic trim-level evidence is weaker than required for clean global-reference-only rows.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep only if Auto/Gear Israeli catalog supports this exact Gallardo variant. If source only proves generic model, move variant to non-blocking review.
ACTION: MOVE TO REVIEW OR FIX TO IL-LIKELY

# MODEL 13: IL-likely|Lamborghini|Huracan
MODEL CURRENT VALUE: model year_start=2014, year_end=2024, profile_confidence=medium, variants=3
WEB-VALIDATED MODEL FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
MODEL SOURCE SET:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

## VARIANT 1
MODEL: IL-likely|Lamborghini|Huracan
CURRENT VALUE: trim='LP610-4'; years=2014-2019; body=Coupe; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=610; transmission=7-speed dual_clutch; drivetrain=AWD; support=direct
PROBLEM: Israeli model presence is supported, but official-importer status is not.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep if exact Israeli Cartube/iCar source supports this trim; set/import-note as special_order/parallel/import listing, not official importer.
ACTION: KEEP WITH SOURCE_SCOPE FIX

## VARIANT 2
MODEL: IL-likely|Lamborghini|Huracan
CURRENT VALUE: trim='Performante'; years=2017-2019; body=Coupe; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=640; transmission=7-speed dual_clutch; drivetrain=AWD; support=direct
PROBLEM: Israeli model presence is supported, but official-importer status is not.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep if exact Israeli Cartube/iCar source supports this trim; set/import-note as special_order/parallel/import listing, not official importer.
ACTION: KEEP WITH SOURCE_SCOPE FIX

## VARIANT 3
MODEL: IL-likely|Lamborghini|Huracan
CURRENT VALUE: trim='Evo'; years=2019-2024; body=Coupe; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=640; transmission=7-speed dual_clutch; drivetrain=AWD; support=direct
PROBLEM: Israeli model presence is supported, but official-importer status is not.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep if exact Israeli Cartube/iCar source supports this trim; set/import-note as special_order/parallel/import listing, not official importer.
ACTION: KEEP WITH SOURCE_SCOPE FIX

# MODEL 14: IL-confirmed|Lamborghini|Huracan
MODEL CURRENT VALUE: model year_start=2019, year_end=2024, profile_confidence=medium, variants=7
WEB-VALIDATED MODEL FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
MODEL SOURCE SET:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

## VARIANT 1
MODEL: IL-confirmed|Lamborghini|Huracan
CURRENT VALUE: trim='Evo'; years=2019-2024; body=Coupe; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=640; transmission=7-speed dual_clutch; drivetrain=AWD; support=direct
PROBLEM: Israeli model presence is supported, but official-importer status is not.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep if exact Israeli Cartube/iCar source supports this trim; set/import-note as special_order/parallel/import listing, not official importer.
ACTION: KEEP WITH SOURCE_SCOPE FIX

## VARIANT 2
MODEL: IL-confirmed|Lamborghini|Huracan
CURRENT VALUE: trim='Evo Spyder'; years=2019-2024; body=Convertible; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=640; transmission=7-speed dual_clutch; drivetrain=AWD; support=direct
PROBLEM: Israeli model presence is supported, but official-importer status is not.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep if exact Israeli Cartube/iCar source supports this trim; set/import-note as special_order/parallel/import listing, not official importer.
ACTION: KEEP WITH SOURCE_SCOPE FIX

## VARIANT 3
MODEL: IL-confirmed|Lamborghini|Huracan
CURRENT VALUE: trim='Evo RWD'; years=2020-2024; body=Coupe; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=610; transmission=7-speed dual_clutch; drivetrain=RWD; support=direct
PROBLEM: Israeli model presence is supported, but official-importer status is not.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep if exact Israeli Cartube/iCar source supports this trim; set/import-note as special_order/parallel/import listing, not official importer.
ACTION: KEEP WITH SOURCE_SCOPE FIX

## VARIANT 4
MODEL: IL-confirmed|Lamborghini|Huracan
CURRENT VALUE: trim='Evo RWD Spyder'; years=2020-2024; body=Convertible; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=610; transmission=7-speed dual_clutch; drivetrain=RWD; support=direct
PROBLEM: Israeli model presence is supported, but official-importer status is not.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep if exact Israeli Cartube/iCar source supports this trim; set/import-note as special_order/parallel/import listing, not official importer.
ACTION: KEEP WITH SOURCE_SCOPE FIX

## VARIANT 5
MODEL: IL-confirmed|Lamborghini|Huracan
CURRENT VALUE: trim='STO'; years=2021-2024; body=Coupe; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=640; transmission=7-speed dual_clutch; drivetrain=RWD; support=direct
PROBLEM: Israeli model presence is supported, but official-importer status is not.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep if exact Israeli Cartube/iCar source supports this trim; set/import-note as special_order/parallel/import listing, not official importer.
ACTION: KEEP WITH SOURCE_SCOPE FIX

## VARIANT 6
MODEL: IL-confirmed|Lamborghini|Huracan
CURRENT VALUE: trim='Tecnica'; years=2022-2024; body=Coupe; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=640; transmission=7-speed dual_clutch; drivetrain=RWD; support=direct
PROBLEM: Israeli model presence is supported, but official-importer status is not.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep if exact Israeli Cartube/iCar source supports this trim; set/import-note as special_order/parallel/import listing, not official importer.
ACTION: KEEP WITH SOURCE_SCOPE FIX

## VARIANT 7
MODEL: IL-confirmed|Lamborghini|Huracan
CURRENT VALUE: trim='Sterrato'; years=2023-2024; body=Coupe; fuel=petrol; engine=5.2L v10; displacement=5.2; hp=610; transmission=7-speed dual_clutch; drivetrain=AWD; support=direct
PROBLEM: Israeli model presence is supported, but official-importer status is not.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep if exact Israeli Cartube/iCar source supports this trim; set/import-note as special_order/parallel/import listing, not official importer.
ACTION: KEEP WITH SOURCE_SCOPE FIX

# MODEL 15: IL-confirmed|Lamborghini|Urus
MODEL CURRENT VALUE: model year_start=2018, year_end=2022, profile_confidence=medium, variants=1
WEB-VALIDATED MODEL FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
MODEL SOURCE SET:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

## VARIANT 1
MODEL: IL-confirmed|Lamborghini|Urus
CURRENT VALUE: trim=None; years=2018-2022; body=SUV; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=650; transmission=8-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Urus appears in duplicate IL-confirmed/IL-likely/global profiles and must not remain split.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Merge duplicate Urus profiles into one Israeli import/special-order profile. Keep exact supported Urus/S/Performante rows; close/route unsupported rows to review.
ACTION: MERGE / SOURCE_SCOPE FIX

# MODEL 16: IL-likely|Lamborghini|Urus
MODEL CURRENT VALUE: model year_start=2018, year_end=None, profile_confidence=medium, variants=3
WEB-VALIDATED MODEL FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
MODEL SOURCE SET:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

## VARIANT 1
MODEL: IL-likely|Lamborghini|Urus
CURRENT VALUE: trim=None; years=2018-None; body=SUV; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=650; transmission=8-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Urus appears in duplicate IL-confirmed/IL-likely/global profiles and must not remain split.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Merge duplicate Urus profiles into one Israeli import/special-order profile. Keep exact supported Urus/S/Performante rows; close/route unsupported rows to review.
ACTION: MERGE / SOURCE_SCOPE FIX

## VARIANT 2
MODEL: IL-likely|Lamborghini|Urus
CURRENT VALUE: trim='S'; years=2023-None; body=SUV; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=666; transmission=8-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Urus appears in duplicate IL-confirmed/IL-likely/global profiles and must not remain split.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Merge duplicate Urus profiles into one Israeli import/special-order profile. Keep exact supported Urus/S/Performante rows; close/route unsupported rows to review.
ACTION: MERGE / SOURCE_SCOPE FIX

## VARIANT 3
MODEL: IL-likely|Lamborghini|Urus
CURRENT VALUE: trim='Performante'; years=2022-None; body=SUV; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=666; transmission=8-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Urus appears in duplicate IL-confirmed/IL-likely/global profiles and must not remain split.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Merge duplicate Urus profiles into one Israeli import/special-order profile. Keep exact supported Urus/S/Performante rows; close/route unsupported rows to review.
ACTION: MERGE / SOURCE_SCOPE FIX

# MODEL 17: global-reference-only|Lamborghini|Urus
MODEL CURRENT VALUE: model year_start=2018, year_end=2024, profile_confidence=medium, variants=4
WEB-VALIDATED MODEL FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
MODEL SOURCE SET:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63

## VARIANT 1
MODEL: global-reference-only|Lamborghini|Urus
CURRENT VALUE: trim=None; years=2018-2023; body=SUV; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=650; transmission=8-speed automatic; drivetrain=AWD; support=direct
PROBLEM: No correction found in embedded validation pass.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Keep if all source_indexes and field_sources are valid; no specific correction found in RUN1.
ACTION: KEEP

## VARIANT 2
MODEL: global-reference-only|Lamborghini|Urus
CURRENT VALUE: trim='Performante'; years=2022-2024; body=SUV; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=666; transmission=8-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Duplicate global profile for a likely Israeli-imported trim.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Merge into Israeli Urus import/special-order profile if exact Israeli source supports trim; otherwise review.
ACTION: MERGE / SOURCE_SCOPE FIX

## VARIANT 3
MODEL: global-reference-only|Lamborghini|Urus
CURRENT VALUE: trim='S'; years=2023-2024; body=SUV; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=666; transmission=8-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Duplicate global profile for a likely Israeli-imported trim.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Merge into Israeli Urus import/special-order profile if exact Israeli source supports trim; otherwise review.
ACTION: MERGE / SOURCE_SCOPE FIX

## VARIANT 4
MODEL: global-reference-only|Lamborghini|Urus
CURRENT VALUE: trim='SE'; years=2024-2024; body=SUV; fuel=plug_in_hybrid; engine=4.0L v8 twin-turbo; displacement=4.0; hp=800; transmission=8-speed automatic; drivetrain=AWD; support=direct
PROBLEM: Urus SE is global/new PHEV with no embedded Israeli clean proof.
WEB-VALIDATED FACT: Israeli sources support the physical presence/listing/import of selected Lamborghini models and variants, but evidence points to special-order/personal/parallel import rather than a normal official Israeli importer clean line. Do not label as official importer. Keep only variants with exact Israeli article/catalog/price-list support; move global-only trims to non-blocking review/archive.
SOURCE:
- Cartube Lamborghini Israel / model launch articles in repo
- Auto/iCar Lamborghini Israeli catalog pages in repo
- Calcalist 2023/2025 import-registration coverage: https://www.calcalist.co.il/local_news/car/article/bji113pu63 and https://www.calcalist.co.il/local_news/car/article/hkdeecwtxe
- Yad2 Lamborghini price-list example: https://www.yad2.co.il/price-list/feed?manufacturer=63
TARGET VALUE: Do not clean as Israeli 2024 SE unless exact Israeli source supports local import/price/listing; global article alone is insufficient.
ACTION: MOVE TO REVIEW

# MODEL 18: IL-confirmed|Lancia|Delta
MODEL CURRENT VALUE: model year_start=2010, year_end=2014, profile_confidence=medium, variants=3
WEB-VALIDATED MODEL FACT: Israeli iCar source states Lancia returned to the Israeli market with Delta and explicitly mentions the 1.8 turbo 200 hp. Existing 1.4 turbo 120 hp manual/automatic rows should stay only if repo-local iCar/Auto variant tables ground them exactly.
MODEL SOURCE SET:
- iCar Lancia Delta page: https://www.icar.co.il/לנצ'יה/לנצ'יה_דלתא/
- Auto Lancia Delta page: https://www.auto.co.il/model/lancia-delta_g264

## VARIANT 1
MODEL: IL-confirmed|Lancia|Delta
CURRENT VALUE: trim=None; years=2010-2014; body=Hatchback; fuel=petrol; engine=1.4L turbo; displacement=1.4; hp=120; transmission=6-speed manual; drivetrain=FWD; support=direct
PROBLEM: 1.4 variants are plausible but need exact field-level local source.
WEB-VALIDATED FACT: Israeli iCar source states Lancia returned to the Israeli market with Delta and explicitly mentions the 1.8 turbo 200 hp. Existing 1.4 turbo 120 hp manual/automatic rows should stay only if repo-local iCar/Auto variant tables ground them exactly.
SOURCE:
- iCar Lancia Delta page: https://www.icar.co.il/לנצ'יה/לנצ'יה_דלתא/
- Auto Lancia Delta page: https://www.auto.co.il/model/lancia-delta_g264
TARGET VALUE: Keep 1.4 turbo 120 hp row only if exact iCar/Auto variant table supports transmission. If exact source missing, move just this row to review, not entire model.
ACTION: KEEP / VERIFY EXACT TRIM

## VARIANT 2
MODEL: IL-confirmed|Lancia|Delta
CURRENT VALUE: trim=None; years=2010-2014; body=Hatchback; fuel=petrol; engine=1.4L turbo; displacement=1.4; hp=120; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: 1.4 variants are plausible but need exact field-level local source.
WEB-VALIDATED FACT: Israeli iCar source states Lancia returned to the Israeli market with Delta and explicitly mentions the 1.8 turbo 200 hp. Existing 1.4 turbo 120 hp manual/automatic rows should stay only if repo-local iCar/Auto variant tables ground them exactly.
SOURCE:
- iCar Lancia Delta page: https://www.icar.co.il/לנצ'יה/לנצ'יה_דלתא/
- Auto Lancia Delta page: https://www.auto.co.il/model/lancia-delta_g264
TARGET VALUE: Keep 1.4 turbo 120 hp row only if exact iCar/Auto variant table supports transmission. If exact source missing, move just this row to review, not entire model.
ACTION: KEEP / VERIFY EXACT TRIM

## VARIANT 3
MODEL: IL-confirmed|Lancia|Delta
CURRENT VALUE: trim=None; years=2010-2014; body=Hatchback; fuel=petrol; engine=1.8L turbo; displacement=1.8; hp=200; transmission=6-speed automatic; drivetrain=FWD; support=direct
PROBLEM: Supported Israeli Delta variant.
WEB-VALIDATED FACT: Israeli iCar source states Lancia returned to the Israeli market with Delta and explicitly mentions the 1.8 turbo 200 hp. Existing 1.4 turbo 120 hp manual/automatic rows should stay only if repo-local iCar/Auto variant tables ground them exactly.
SOURCE:
- iCar Lancia Delta page: https://www.icar.co.il/לנצ'יה/לנצ'יה_דלתא/
- Auto Lancia Delta page: https://www.auto.co.il/model/lancia-delta_g264
TARGET VALUE: Keep 1.8 turbo 200 hp Delta row; iCar explicitly describes 1.8 turbo 200 hp in Israeli context.
ACTION: KEEP

# MODEL 19: global-reference-only|Lancia|Kappa
MODEL CURRENT VALUE: model year_start=1995, year_end=2001, profile_confidence=medium, variants=5
WEB-VALIDATED MODEL FACT: Kappa is a historical Lancia model. Israeli Auto/iCar catalog pages may support local price-list/spec existence, but global-reference-only profiles must be converted to IL-likely with exact source backing or moved to non-blocking review/archive.
MODEL SOURCE SET:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Kappa source in repo: https://www.auto.co.il/model/lancia-kappa_g1116
- iCar Kappa source in repo: https://www.icar.co.il/lancia/lancia_kappa/

## VARIANT 1
MODEL: global-reference-only|Lancia|Kappa
CURRENT VALUE: trim='LS'; years=1995-2001; body=Sedan; fuel=petrol; engine=2.4L inline-5; displacement=2.4; hp=175; transmission=4-speed automatic; drivetrain=FWD; support=direct
PROBLEM: Global-reference-only historical Lancia rows are not clean Israeli variants without exact local catalog support.
WEB-VALIDATED FACT: Kappa is a historical Lancia model. Israeli Auto/iCar catalog pages may support local price-list/spec existence, but global-reference-only profiles must be converted to IL-likely with exact source backing or moved to non-blocking review/archive.
SOURCE:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Kappa source in repo: https://www.auto.co.il/model/lancia-kappa_g1116
- iCar Kappa source in repo: https://www.icar.co.il/lancia/lancia_kappa/
TARGET VALUE: Do not keep as global-reference-only clean. If Auto/iCar exact Israeli catalog row supports this exact body/engine/transmission, convert profile to IL-likely historical and keep; otherwise move row to non-blocking review/archive.
ACTION: MOVE TO REVIEW OR FIX TO IL-LIKELY

## VARIANT 2
MODEL: global-reference-only|Lancia|Kappa
CURRENT VALUE: trim=None; years=1995-1998; body=Sedan; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=205; transmission=5-speed manual; drivetrain=FWD; support=direct
PROBLEM: Global-reference-only historical Lancia rows are not clean Israeli variants without exact local catalog support.
WEB-VALIDATED FACT: Kappa is a historical Lancia model. Israeli Auto/iCar catalog pages may support local price-list/spec existence, but global-reference-only profiles must be converted to IL-likely with exact source backing or moved to non-blocking review/archive.
SOURCE:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Kappa source in repo: https://www.auto.co.il/model/lancia-kappa_g1116
- iCar Kappa source in repo: https://www.icar.co.il/lancia/lancia_kappa/
TARGET VALUE: Do not keep as global-reference-only clean. If Auto/iCar exact Israeli catalog row supports this exact body/engine/transmission, convert profile to IL-likely historical and keep; otherwise move row to non-blocking review/archive.
ACTION: MOVE TO REVIEW OR FIX TO IL-LIKELY

## VARIANT 3
MODEL: global-reference-only|Lancia|Kappa
CURRENT VALUE: trim=None; years=1998-2001; body=Sedan; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=220; transmission=5-speed manual; drivetrain=FWD; support=direct
PROBLEM: Global-reference-only historical Lancia rows are not clean Israeli variants without exact local catalog support.
WEB-VALIDATED FACT: Kappa is a historical Lancia model. Israeli Auto/iCar catalog pages may support local price-list/spec existence, but global-reference-only profiles must be converted to IL-likely with exact source backing or moved to non-blocking review/archive.
SOURCE:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Kappa source in repo: https://www.auto.co.il/model/lancia-kappa_g1116
- iCar Kappa source in repo: https://www.icar.co.il/lancia/lancia_kappa/
TARGET VALUE: Do not keep as global-reference-only clean. If Auto/iCar exact Israeli catalog row supports this exact body/engine/transmission, convert profile to IL-likely historical and keep; otherwise move row to non-blocking review/archive.
ACTION: MOVE TO REVIEW OR FIX TO IL-LIKELY

## VARIANT 4
MODEL: global-reference-only|Lancia|Kappa
CURRENT VALUE: trim=None; years=1997-2000; body=Coupe; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=220; transmission=5-speed manual; drivetrain=FWD; support=direct
PROBLEM: Global-reference-only historical Lancia rows are not clean Israeli variants without exact local catalog support.
WEB-VALIDATED FACT: Kappa is a historical Lancia model. Israeli Auto/iCar catalog pages may support local price-list/spec existence, but global-reference-only profiles must be converted to IL-likely with exact source backing or moved to non-blocking review/archive.
SOURCE:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Kappa source in repo: https://www.auto.co.il/model/lancia-kappa_g1116
- iCar Kappa source in repo: https://www.icar.co.il/lancia/lancia_kappa/
TARGET VALUE: Do not keep as global-reference-only clean. If Auto/iCar exact Israeli catalog row supports this exact body/engine/transmission, convert profile to IL-likely historical and keep; otherwise move row to non-blocking review/archive.
ACTION: MOVE TO REVIEW OR FIX TO IL-LIKELY

## VARIANT 5
MODEL: global-reference-only|Lancia|Kappa
CURRENT VALUE: trim='LS'; years=1996-2000; body=Estate; fuel=petrol; engine=2.4L inline-5; displacement=2.4; hp=175; transmission=4-speed automatic; drivetrain=FWD; support=direct
PROBLEM: Global-reference-only historical Lancia rows are not clean Israeli variants without exact local catalog support.
WEB-VALIDATED FACT: Kappa is a historical Lancia model. Israeli Auto/iCar catalog pages may support local price-list/spec existence, but global-reference-only profiles must be converted to IL-likely with exact source backing or moved to non-blocking review/archive.
SOURCE:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Kappa source in repo: https://www.auto.co.il/model/lancia-kappa_g1116
- iCar Kappa source in repo: https://www.icar.co.il/lancia/lancia_kappa/
TARGET VALUE: Do not keep as global-reference-only clean. If Auto/iCar exact Israeli catalog row supports this exact body/engine/transmission, convert profile to IL-likely historical and keep; otherwise move row to non-blocking review/archive.
ACTION: MOVE TO REVIEW OR FIX TO IL-LIKELY

# MODEL 20: global-reference-only|Lancia|Lybra
MODEL CURRENT VALUE: model year_start=1999, year_end=2005, profile_confidence=medium, variants=4
WEB-VALIDATED MODEL FACT: Lybra was manufactured globally 1998-2005 and appears in Israeli catalog sources, but global-reference-only rows for diesel/estate/body splits need exact Israeli support before clean.
MODEL SOURCE SET:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Lybra source in repo: https://www.auto.co.il/model/lancia-lybra_g196
- iCar Lybra source in repo: https://www.icar.co.il/לנצ'יה/לנצ'יה_ליברה/לנצ'יה_ליברה_יד_שניה/

## VARIANT 1
MODEL: global-reference-only|Lancia|Lybra
CURRENT VALUE: trim=None; years=1999-2005; body=Sedan; fuel=petrol; engine=2.0L inline-5; displacement=2.0; hp=154; transmission=4-speed automatic; drivetrain=FWD; support=direct
PROBLEM: Global-reference-only Lybra split profile overlaps IL-confirmed Lybra and includes unsupported body/fuel splits.
WEB-VALIDATED FACT: Lybra was manufactured globally 1998-2005 and appears in Israeli catalog sources, but global-reference-only rows for diesel/estate/body splits need exact Israeli support before clean.
SOURCE:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Lybra source in repo: https://www.auto.co.il/model/lancia-lybra_g196
- iCar Lybra source in repo: https://www.icar.co.il/לנצ'יה/לנצ'יה_ליברה/לנצ'יה_ליברה_יד_שניה/
TARGET VALUE: Merge any exact duplicate of IL-confirmed Lybra into the confirmed model. Diesel/estate/body variants require exact Israeli catalog support; otherwise move to non-blocking review.
ACTION: MOVE TO REVIEW OR MERGE

## VARIANT 2
MODEL: global-reference-only|Lancia|Lybra
CURRENT VALUE: trim=None; years=1999-2005; body=Estate; fuel=petrol; engine=2.0L inline-5; displacement=2.0; hp=154; transmission=4-speed automatic; drivetrain=FWD; support=direct
PROBLEM: Global-reference-only Lybra split profile overlaps IL-confirmed Lybra and includes unsupported body/fuel splits.
WEB-VALIDATED FACT: Lybra was manufactured globally 1998-2005 and appears in Israeli catalog sources, but global-reference-only rows for diesel/estate/body splits need exact Israeli support before clean.
SOURCE:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Lybra source in repo: https://www.auto.co.il/model/lancia-lybra_g196
- iCar Lybra source in repo: https://www.icar.co.il/לנצ'יה/לנצ'יה_ליברה/לנצ'יה_ליברה_יד_שניה/
TARGET VALUE: Merge any exact duplicate of IL-confirmed Lybra into the confirmed model. Diesel/estate/body variants require exact Israeli catalog support; otherwise move to non-blocking review.
ACTION: MOVE TO REVIEW OR MERGE

## VARIANT 3
MODEL: global-reference-only|Lancia|Lybra
CURRENT VALUE: trim=None; years=2000-2004; body=Sedan; fuel=diesel; engine=1.9L turbo; displacement=1.9; hp=115; transmission=5-speed manual; drivetrain=FWD; support=direct
PROBLEM: Global-reference-only Lybra split profile overlaps IL-confirmed Lybra and includes unsupported body/fuel splits.
WEB-VALIDATED FACT: Lybra was manufactured globally 1998-2005 and appears in Israeli catalog sources, but global-reference-only rows for diesel/estate/body splits need exact Israeli support before clean.
SOURCE:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Lybra source in repo: https://www.auto.co.il/model/lancia-lybra_g196
- iCar Lybra source in repo: https://www.icar.co.il/לנצ'יה/לנצ'יה_ליברה/לנצ'יה_ליברה_יד_שניה/
TARGET VALUE: Merge any exact duplicate of IL-confirmed Lybra into the confirmed model. Diesel/estate/body variants require exact Israeli catalog support; otherwise move to non-blocking review.
ACTION: MOVE TO REVIEW OR MERGE

## VARIANT 4
MODEL: global-reference-only|Lancia|Lybra
CURRENT VALUE: trim=None; years=2000-2004; body=Estate; fuel=diesel; engine=1.9L turbo; displacement=1.9; hp=115; transmission=5-speed manual; drivetrain=FWD; support=direct
PROBLEM: Global-reference-only Lybra split profile overlaps IL-confirmed Lybra and includes unsupported body/fuel splits.
WEB-VALIDATED FACT: Lybra was manufactured globally 1998-2005 and appears in Israeli catalog sources, but global-reference-only rows for diesel/estate/body splits need exact Israeli support before clean.
SOURCE:
- Auto Lancia brand/catalog page: https://www.auto.co.il/cars/lancia/
- Auto Lybra source in repo: https://www.auto.co.il/model/lancia-lybra_g196
- iCar Lybra source in repo: https://www.icar.co.il/לנצ'יה/לנצ'יה_ליברה/לנצ'יה_ליברה_יד_שניה/
TARGET VALUE: Merge any exact duplicate of IL-confirmed Lybra into the confirmed model. Diesel/estate/body variants require exact Israeli catalog support; otherwise move to non-blocking review.
ACTION: MOVE TO REVIEW OR MERGE

# MODEL 21: IL-confirmed|Lancia|Lybra
MODEL CURRENT VALUE: model year_start=1999, year_end=2005, profile_confidence=medium, variants=1
WEB-VALIDATED MODEL FACT: IL-confirmed Lybra LX 2.0 automatic sedan is plausible if exact iCar/Auto source rows support it; avoid keeping duplicate global Lybra rows beside this confirmed row.
MODEL SOURCE SET:
- iCar Lybra source in repo: https://www.icar.co.il/lancia/lancia_lybra/
- Auto Lybra source in repo: https://www.auto.co.il/model/lancia-lybra_g1061

## VARIANT 1
MODEL: IL-confirmed|Lancia|Lybra
CURRENT VALUE: trim='LX'; years=1999-2005; body=Sedan; fuel=petrol; engine=2.0L inline-5; displacement=2.0; hp=154; transmission=4-speed automatic; drivetrain=FWD; support=direct
PROBLEM: Confirmed row is the clean anchor for Lybra.
WEB-VALIDATED FACT: IL-confirmed Lybra LX 2.0 automatic sedan is plausible if exact iCar/Auto source rows support it; avoid keeping duplicate global Lybra rows beside this confirmed row.
SOURCE:
- iCar Lybra source in repo: https://www.icar.co.il/lancia/lancia_lybra/
- Auto Lybra source in repo: https://www.auto.co.il/model/lancia-lybra_g1061
TARGET VALUE: Keep only this exact LX 2.0 automatic sedan if source-backed; remove duplicate global overlap.
ACTION: KEEP

# MODEL 22: IL-confirmed|Lancia|Thema
MODEL CURRENT VALUE: model year_start=1988, year_end=2014, profile_confidence=medium, variants=3
WEB-VALIDATED MODEL FACT: Cartube reports the newer Lancia Thema in Israel; Auto sources cover the 2011-2014 Thema and older 1985-1994 Thema. The 2011-2014 3.6 V6 286 hp row is credible; older 1988-1994 rows must remain only if exact Auto source supports them.
MODEL SOURCE SET:
- Cartube Thema Israel: https://www.cartube.co.il/חדשות-רכב/לנצ-יה-תמא-thema-החדשה-בישראל
- Auto Thema 2011-2014 source in repo: https://www.auto.co.il/model/lancia-thema_g190
- Auto Thema 1985-1994 source in repo: https://www.auto.co.il/model/lancia-thema_g189

## VARIANT 1
MODEL: IL-confirmed|Lancia|Thema
CURRENT VALUE: trim=None; years=1988-1992; body=Sedan; fuel=petrol; engine=2.0L inline-4; displacement=2.0; hp=147; transmission=4-speed automatic; drivetrain=FWD; support=direct
PROBLEM: Older Thema rows are historical and need exact local catalog support.
WEB-VALIDATED FACT: Cartube reports the newer Lancia Thema in Israel; Auto sources cover the 2011-2014 Thema and older 1985-1994 Thema. The 2011-2014 3.6 V6 286 hp row is credible; older 1988-1994 rows must remain only if exact Auto source supports them.
SOURCE:
- Cartube Thema Israel: https://www.cartube.co.il/חדשות-רכב/לנצ-יה-תמא-thema-החדשה-בישראל
- Auto Thema 2011-2014 source in repo: https://www.auto.co.il/model/lancia-thema_g190
- Auto Thema 1985-1994 source in repo: https://www.auto.co.il/model/lancia-thema_g189
TARGET VALUE: Keep older Thema rows only if Auto source exactly supports 1988-1994 Israeli/local catalog. Otherwise move weak rows to non-blocking review.
ACTION: KEEP / VERIFY HISTORICAL

## VARIANT 2
MODEL: IL-confirmed|Lancia|Thema
CURRENT VALUE: trim='LS'; years=1992-1994; body=Sedan; fuel=petrol; engine=2.0L inline-4; displacement=2.0; hp=152; transmission=4-speed automatic; drivetrain=FWD; support=direct
PROBLEM: Older Thema rows are historical and need exact local catalog support.
WEB-VALIDATED FACT: Cartube reports the newer Lancia Thema in Israel; Auto sources cover the 2011-2014 Thema and older 1985-1994 Thema. The 2011-2014 3.6 V6 286 hp row is credible; older 1988-1994 rows must remain only if exact Auto source supports them.
SOURCE:
- Cartube Thema Israel: https://www.cartube.co.il/חדשות-רכב/לנצ-יה-תמא-thema-החדשה-בישראל
- Auto Thema 2011-2014 source in repo: https://www.auto.co.il/model/lancia-thema_g190
- Auto Thema 1985-1994 source in repo: https://www.auto.co.il/model/lancia-thema_g189
TARGET VALUE: Keep older Thema rows only if Auto source exactly supports 1988-1994 Israeli/local catalog. Otherwise move weak rows to non-blocking review.
ACTION: KEEP / VERIFY HISTORICAL

## VARIANT 3
MODEL: IL-confirmed|Lancia|Thema
CURRENT VALUE: trim='Executive'; years=2011-2014; body=Sedan; fuel=petrol; engine=3.6L v6; displacement=3.6; hp=286; transmission=8-speed automatic; drivetrain=RWD; support=direct
PROBLEM: Newer Thema Israel row has strong local article/catalog support.
WEB-VALIDATED FACT: Cartube reports the newer Lancia Thema in Israel; Auto sources cover the 2011-2014 Thema and older 1985-1994 Thema. The 2011-2014 3.6 V6 286 hp row is credible; older 1988-1994 rows must remain only if exact Auto source supports them.
SOURCE:
- Cartube Thema Israel: https://www.cartube.co.il/חדשות-רכב/לנצ-יה-תמא-thema-החדשה-בישראל
- Auto Thema 2011-2014 source in repo: https://www.auto.co.il/model/lancia-thema_g190
- Auto Thema 1985-1994 source in repo: https://www.auto.co.il/model/lancia-thema_g189
TARGET VALUE: Keep 2011-2014 Thema Executive 3.6 V6 286 hp RWD 8AT if Cartube/Auto sources remain attached.
ACTION: KEEP

# MODEL 23: IL-likely|Lancia|Thema
MODEL CURRENT VALUE: model year_start=1992, year_end=1994, profile_confidence=medium, variants=1
WEB-VALIDATED MODEL FACT: Turbo 16V LS is only IL-likely and appears to rely on weaker/forum-type local evidence. Do not keep as clean without exact Israeli source; move to non-blocking review if source strength remains below Tier 2/3 catalog.
MODEL SOURCE SET:
- Auto Thema source in repo: https://www.auto.co.il/model/lancia-thema
- CarsForum weak local discussion source in repo: https://carsforum.co.il/topic/lancia-thema-turbo-israel

## VARIANT 1
MODEL: IL-likely|Lancia|Thema
CURRENT VALUE: trim='Turbo 16V LS'; years=1992-1994; body=Sedan; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=201; transmission=5-speed manual; drivetrain=FWD; support=direct
PROBLEM: Weak IL-likely/forum-supported row.
WEB-VALIDATED FACT: Turbo 16V LS is only IL-likely and appears to rely on weaker/forum-type local evidence. Do not keep as clean without exact Israeli source; move to non-blocking review if source strength remains below Tier 2/3 catalog.
SOURCE:
- Auto Thema source in repo: https://www.auto.co.il/model/lancia-thema
- CarsForum weak local discussion source in repo: https://carsforum.co.il/topic/lancia-thema-turbo-israel
TARGET VALUE: Move Turbo 16V LS row to non-blocking review unless repo-local Auto source supports exact Israeli variant; forum evidence is insufficient for clean.
ACTION: MOVE TO REVIEW

# MODEL 24: global-reference-only|Lancia|Thesis
MODEL CURRENT VALUE: model year_start=2002, year_end=2009, profile_confidence=medium, variants=3
WEB-VALIDATED MODEL FACT: Lancia Thesis appears in Auto/iCar Israeli catalog sources, but the current profile is global-reference-only. Keep only exact locally supported trims; otherwise move to non-blocking review/archive.
MODEL SOURCE SET:
- Auto Thesis source in repo: https://www.auto.co.il/model/lancia-thesis_g400
- iCar Thesis source in repo: https://www.icar.co.il/lancia/thesis/

## VARIANT 1
MODEL: global-reference-only|Lancia|Thesis
CURRENT VALUE: trim='Emblema'; years=2002-2007; body=Sedan; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=185; transmission=manual; drivetrain=FWD; support=direct
PROBLEM: Global-reference-only Thesis row lacks enough embedded Israeli proof.
WEB-VALIDATED FACT: Lancia Thesis appears in Auto/iCar Israeli catalog sources, but the current profile is global-reference-only. Keep only exact locally supported trims; otherwise move to non-blocking review/archive.
SOURCE:
- Auto Thesis source in repo: https://www.auto.co.il/model/lancia-thesis_g400
- iCar Thesis source in repo: https://www.icar.co.il/lancia/thesis/
TARGET VALUE: Move to non-blocking review unless exact Israeli catalog source supports this trim/body/engine/transmission.
ACTION: MOVE TO REVIEW

## VARIANT 2
MODEL: global-reference-only|Lancia|Thesis
CURRENT VALUE: trim='Executive'; years=2003-2009; body=Sedan; fuel=petrol; engine=3.2L v6; displacement=3.2; hp=230; transmission=automatic; drivetrain=FWD; support=direct
PROBLEM: Best-supported Thesis row but still global-reference-only.
WEB-VALIDATED FACT: Lancia Thesis appears in Auto/iCar Israeli catalog sources, but the current profile is global-reference-only. Keep only exact locally supported trims; otherwise move to non-blocking review/archive.
SOURCE:
- Auto Thesis source in repo: https://www.auto.co.il/model/lancia-thesis_g400
- iCar Thesis source in repo: https://www.icar.co.il/lancia/thesis/
TARGET VALUE: Keep 3.2 V6 Executive only if exact Israeli iCar/Auto source supports it; otherwise review.
ACTION: KEEP ONLY IF EXACT ICAR/AUTO SUPPORT ELSE REVIEW

## VARIANT 3
MODEL: global-reference-only|Lancia|Thesis
CURRENT VALUE: trim=None; years=2003-2009; body=Sedan; fuel=diesel; engine=2.4L turbo; displacement=2.4; hp=175; transmission=automatic; drivetrain=FWD; support=indirect
PROBLEM: Global-reference-only Thesis row lacks enough embedded Israeli proof.
WEB-VALIDATED FACT: Lancia Thesis appears in Auto/iCar Israeli catalog sources, but the current profile is global-reference-only. Keep only exact locally supported trims; otherwise move to non-blocking review/archive.
SOURCE:
- Auto Thesis source in repo: https://www.auto.co.il/model/lancia-thesis_g400
- iCar Thesis source in repo: https://www.icar.co.il/lancia/thesis/
TARGET VALUE: Move to non-blocking review unless exact Israeli catalog source supports this trim/body/engine/transmission.
ACTION: MOVE TO REVIEW

# MODEL 25: IL-confirmed|Lancia|Y
MODEL CURRENT VALUE: model year_start=1996, year_end=2003, profile_confidence=medium, variants=4
WEB-VALIDATED MODEL FACT: Lancia Y is historical/used-market supported by Israeli price-list/catalog sources. Because sources are weaker (Yad2/Carzone/iCar used), keep only if field_sources are valid; mark source tier carefully and avoid claiming official import.
MODEL SOURCE SET:
- Yad2 Lancia Y price list: https://www.yad2.co.il/vehicles/prices/lancia/y/1996-2000
- iCar Lancia Y used page: https://www.icar.co.il/לנצ'יה/לנצ'יה_Y_יד_שניה/
- Carzone Lancia Y: https://carzone.co.il/vehicles/lancia/y

## VARIANT 1
MODEL: IL-confirmed|Lancia|Y
CURRENT VALUE: trim='LS'; years=1996-2000; body=Hatchback; fuel=petrol; engine=1.2L; displacement=1.2; hp=60; transmission=5-speed manual; drivetrain=FWD; support=direct
PROBLEM: Clean row is supported by weaker historical/used-market sources and must not be overstated.
WEB-VALIDATED FACT: Lancia Y is historical/used-market supported by Israeli price-list/catalog sources. Because sources are weaker (Yad2/Carzone/iCar used), keep only if field_sources are valid; mark source tier carefully and avoid claiming official import.
SOURCE:
- Yad2 Lancia Y price list: https://www.yad2.co.il/vehicles/prices/lancia/y/1996-2000
- iCar Lancia Y used page: https://www.icar.co.il/לנצ'יה/לנצ'יה_Y_יד_שניה/
- Carzone Lancia Y: https://carzone.co.il/vehicles/lancia/y
TARGET VALUE: Keep only if source references are valid; tag as historical/used-market/Tier-3 supported, not official importer.
ACTION: KEEP WITH SOURCE-TIER WARNING

## VARIANT 2
MODEL: IL-confirmed|Lancia|Y
CURRENT VALUE: trim='LS'; years=1997-2000; body=Hatchback; fuel=petrol; engine=1.2L; displacement=1.2; hp=60; transmission=cvt; drivetrain=FWD; support=direct
PROBLEM: Clean row is supported by weaker historical/used-market sources and must not be overstated.
WEB-VALIDATED FACT: Lancia Y is historical/used-market supported by Israeli price-list/catalog sources. Because sources are weaker (Yad2/Carzone/iCar used), keep only if field_sources are valid; mark source tier carefully and avoid claiming official import.
SOURCE:
- Yad2 Lancia Y price list: https://www.yad2.co.il/vehicles/prices/lancia/y/1996-2000
- iCar Lancia Y used page: https://www.icar.co.il/לנצ'יה/לנצ'יה_Y_יד_שניה/
- Carzone Lancia Y: https://carzone.co.il/vehicles/lancia/y
TARGET VALUE: Keep only if source references are valid; tag as historical/used-market/Tier-3 supported, not official importer.
ACTION: KEEP WITH SOURCE-TIER WARNING

## VARIANT 3
MODEL: IL-confirmed|Lancia|Y
CURRENT VALUE: trim='LS'; years=2001-2003; body=Hatchback; fuel=petrol; engine=1.2L; displacement=1.2; hp=80; transmission=5-speed manual; drivetrain=FWD; support=direct
PROBLEM: Clean row is supported by weaker historical/used-market sources and must not be overstated.
WEB-VALIDATED FACT: Lancia Y is historical/used-market supported by Israeli price-list/catalog sources. Because sources are weaker (Yad2/Carzone/iCar used), keep only if field_sources are valid; mark source tier carefully and avoid claiming official import.
SOURCE:
- Yad2 Lancia Y price list: https://www.yad2.co.il/vehicles/prices/lancia/y/1996-2000
- iCar Lancia Y used page: https://www.icar.co.il/לנצ'יה/לנצ'יה_Y_יד_שניה/
- Carzone Lancia Y: https://carzone.co.il/vehicles/lancia/y
TARGET VALUE: Keep only if source references are valid; tag as historical/used-market/Tier-3 supported, not official importer.
ACTION: KEEP WITH SOURCE-TIER WARNING

## VARIANT 4
MODEL: IL-confirmed|Lancia|Y
CURRENT VALUE: trim='LS'; years=2001-2003; body=Hatchback; fuel=petrol; engine=1.2L; displacement=1.2; hp=80; transmission=cvt; drivetrain=FWD; support=direct
PROBLEM: Clean row is supported by weaker historical/used-market sources and must not be overstated.
WEB-VALIDATED FACT: Lancia Y is historical/used-market supported by Israeli price-list/catalog sources. Because sources are weaker (Yad2/Carzone/iCar used), keep only if field_sources are valid; mark source tier carefully and avoid claiming official import.
SOURCE:
- Yad2 Lancia Y price list: https://www.yad2.co.il/vehicles/prices/lancia/y/1996-2000
- iCar Lancia Y used page: https://www.icar.co.il/לנצ'יה/לנצ'יה_Y_יד_שניה/
- Carzone Lancia Y: https://carzone.co.il/vehicles/lancia/y
TARGET VALUE: Keep only if source references are valid; tag as historical/used-market/Tier-3 supported, not official importer.
ACTION: KEEP WITH SOURCE-TIER WARNING

## Required post-change checks

Run all of the following in the real repo:
```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Also directly audit readiness, review, archive, quality scan, compute_resume_state(), unmatched_output_keys, active blockers, cursor, split aliases, and duplicates. RUN 1 must not move the cursor backward or forward beyond the RUN 1 implementation boundary unless the project design requires cursor to reflect already completed source groups. Report any ambiguity.

---


# BATCH25 RESTART — RUN 2 VARIANT-LEVEL CODEX TASK

## Non-negotiable execution rules

Do not browse the internet. All web-validation facts and target corrections are embedded in this task file. Use this task file as the single source of truth. Do not apply corrections that are not instructed here. If repo-local evidence conflicts with this task file, report it instead of guessing. If a variant cannot be grounded with the embedded facts or repo-local sources, move it to non-blocking archive/review rather than fabricating data.

This RUN covers only RUN 2 clean profiles. Do not implement RUN 3 or FINAL blockers yet, except to avoid regressions caused by RUN 2 corrections. RUN 1 was handled in `BATCH25_RESTART_RUN1_VARIANT_LEVEL_CODEX_TASK.md`.

## RUN 2 scope

RUN 2 starts after `IL-confirmed|Lancia|Y` and contains 25 clean model profiles / 97 technical variants:

1. `IL-confirmed|Lancia|Ypsilon` — 4 variants
2. `IL-confirmed|Land Rover|Defender` — 10 variants
3. `IL-confirmed|Land Rover|Discovery` — 6 variants
4. `IL-confirmed|Land Rover|Discovery Sport` — 5 variants
5. `IL-confirmed|Land Rover|Freelander` — 7 variants
6. `IL-confirmed|Land Rover|Freelander 2` — 5 variants
7. `IL-confirmed|Land Rover|Range Rover` — 7 variants
8. `IL-confirmed|Land Rover|Range Rover Evoque` — 4 variants
9. `IL-likely|Land Rover|Range Rover Evoque` — 6 variants
10. `IL-confirmed|Land Rover|Range Rover Sport` — 6 variants
11. `IL-confirmed|Land Rover|Range Rover Velar` — 7 variants
12. `IL-likely|Land Rover|Range Rover Velar` — 4 variants
13. `global-reference-only|Leapmotor|C10` — 1 variants
14. `IL-confirmed|Leapmotor|C10` — 1 variants
15. `IL-confirmed|Leapmotor|T03` — 1 variants
16. `IL-confirmed|Lexus|CT 200h` — 1 variants
17. `global-reference-only|Lexus|ES` — 1 variants
18. `IL-confirmed|Lexus|ES` — 1 variants
19. `IL-confirmed|Lexus|GS` — 6 variants
20. `global-reference-only|Lexus|GX` — 2 variants
21. `IL-confirmed|Lexus|IS` — 5 variants
22. `IL-confirmed|Lexus|LBX` — 1 variants
23. `IL-confirmed|Lexus|LC` — 4 variants
24. `global-reference-only|Lexus|LM` — 1 variants
25. `IL-confirmed|Lexus|LM` — 1 variants

## Local audit/test baseline from uploaded ZIP

- `python -m compileall scripts` — PASS
- `python -m scripts.catalog_validation` — PASS
- `python -m scripts.catalog_quality_scan` — PASS
- `python -m pytest -q` — FAIL in this sandbox because `streamlit` is missing while collecting `tests/test_selectable_provider_and_github.py`; in a real repo environment install requirements or report dependency/test-environment failure, do not hide it.
- `git diff --check` — run in the real git repo after changes; the uploaded ZIP extraction here is not a git checkout.

## Required post-implementation checks

Run all of these after applying RUN 2 only:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Then directly inspect readiness, review, archive, quality scan, `compute_resume_state()`, unmatched_output_keys, active blockers, and cursor. Do not approve by console output alone.

## Embedded web-validation sources used for RUN 2

### Lancia Ypsilon
- iCar Lancia Ypsilon 2011-2015: https://www.icar.co.il/לנצ%27יה/לנצ%27יה_אפסילון/לנצ%27יה_אפסילון_יד_שניה_ד10/
- Auto.co.il Lancia Ypsilon: https://www.auto.co.il/cars/lancia/ypsilon/
- Carzone Ypsilon 2011: https://www.carzone.co.il/Lancia/Ypsilon/2011/
- Yad2 Ypsilon price-list: https://www.yad2.co.il/price-list/feed?manufacturer=25&model=10316

### Land Rover 2026 official pricelist
- Land Rover Israel 2026 official price list: https://www.landrover.co.il/offers-and-finance/pricelist

### Defender
- iCar Defender 2020 technical page: https://www.icar.co.il/לנד_רובר/לנד_רובר_דיפנדר_חדש/מפרט_טכני/
- Cartube Defender 2020 Israel launch: https://www.cartube.co.il/חדשות-רכב/לנד-רובר-דיפנדר-החדש-2020-בישראל-מחיר-החל-מ-425,000-שקל
- iCar Defender 2007-2016: https://www.icar.co.il/לנד_רובר/לנד_רובר_דיפנדר_דור_1/

### Discovery
- Auto.co.il Discovery 5 2017: https://www.auto.co.il/cars/land-rover/discovery-5/2017/
- Carzone Discovery 2017: https://www.carzone.co.il/Land-Rover/Discovery/2017/
- Land Rover Israel Discovery overview: https://www.landrover.co.il/discovery/discovery/overview

### Discovery Sport
- iCar Discovery Sport 2020 technical rows: https://www.icar.co.il/לנדרובר/לנדרובר_דיסקברי_ספורט/לנדרובר_דיסקברי_ספורט_יד_שניה_ד10/version22106/
- Carzone Discovery Sport 2020: https://www.carzone.co.il/Land-Rover/Discovery-Sport/2020/
- Auto.co.il Discovery Sport 2020: https://www.auto.co.il/cars/land-rover/discovery-sport/2020/

### Freelander
- iCar Freelander until 2006: https://www.icar.co.il/לנד_רובר/לנד_רובר_פרילנדר_עד_2006/
- iCar Freelander / Freelander 2: https://www.icar.co.il/לנד_רובר/לנד_רובר_פרילנדר/
- Auto.co.il Freelander: https://www.auto.co.il/model/land-rover-freelander_g350

### Range Rover family
- Land Rover Israel 2026 official price list: https://www.landrover.co.il/offers-and-finance/pricelist

### Leapmotor
- Leapmotor Israel official site: https://leapmotor.co.il/
- Carzone Leapmotor C10 2024: https://www.carzone.co.il/leapmotor/C10/2024/
- Yad2 Leapmotor price list: https://www.yad2.co.il/price-list/feed?manufacturer=320
- Auto.co.il Leapmotor C10: https://www.auto.co.il/cars/leap-motor/c10/
- Carzone Leapmotor T03 2022: https://www.carzone.co.il/leapmotor/T03/2022/
- Auto.co.il Leapmotor T03: https://www.auto.co.il/cars/leap-motor/t03/

### Lexus official/current
- Lexus Israel new cars: https://www.lexus.co.il/new-cars
- Lexus Israel LBX: https://www.lexus.co.il/new-cars/lbx
- Lexus Israel LBX specifications: https://www.lexus.co.il/new-cars/lbx/specifications
- Lexus Israel LM: https://www.lexus.co.il/new-cars/lm
- Lexus Israel trade-in model price snippets: https://www.lexus.co.il/lease/trade-in

### Lexus historical
- iCar Lexus CT200h 2011-2020: https://www.icar.co.il/לקסוס/לקסוס_CT200h/לקסוס_CT200h_יד_שניה_ד10/
- Auto.co.il Lexus CT200h 2018: https://www.auto.co.il/cars/lexus/ct200h/2018/
- iCar Lexus ES: https://www.icar.co.il/לקסוס/לקסוס_ES/לקסוס_ES_חדש/
- Carzone Lexus ES 2018: https://www.carzone.co.il/Lexus/ES/2018/
- Auto.co.il Lexus ES: https://www.auto.co.il/cars/lexus/es/
- iCar Lexus GS250 2012: https://www.icar.co.il/לקסוס/לקסוס_GS250/לקסוס_GS250_יד_שניה_ד10/version9936/
- Auto.co.il Lexus GS450h Israel: https://www.auto.co.il/articles/car-news/115307/
- iCar Lexus GS450h review: https://www.icar.co.il/מבחני_רכב/לקסוס_GS450h_-_מבחן_רכב/
- iCar Lexus IS300h: https://www.icar.co.il/לקסוס/לקסוס_IS300h/לקסוס_IS300h_יד_שניה_ד10/
- iCar Lexus IS250: https://www.icar.co.il/לקסוס/לקסוס_IS250/
- Cartube Lexus LC Israel launch: https://www.cartube.co.il/חדשות-רכב/לקסוס-lc-נחתה-בישראל-מחיר-החל-מ-725,000-שקל
- Auto.co.il Lexus LC: https://www.auto.co.il/cars/lexus/lc/

### Lexus GX
- Cartube Lexus GX revealed / coming to Israel: https://www.cartube.co.il/חדשות-רכב/לקסוס-gx-החדש-2024-נחשף-מגיע-לישראל
- Auto.co.il Lexus GX world news / Israel expectation: https://www.auto.co.il/article/135967-world-news-lexus-gx
- Yad2 Lexus GX marketplace/pricelist: https://www.yad2.co.il/vehicles/lexus/gx

## Variant-level decisions


### MODEL: `IL-confirmed|Lancia|Ypsilon`
CURRENT VALUE: clean profile index 486; model years 2007-2015; variants=4
WEB-VALIDATED FACT: Israeli sources support Ypsilon 2011-2015 with 1.2L 69 hp manual and 0.9L TwinAir turbo 85 hp; Auto/iCar describe the 0.9 as robotized/automated rather than a conventional automatic. Carzone/Yad2 also show 0.9 manual sub-models in some years. The older 2007-2011 1.4L 95 hp rows depend mainly on repo-local Auto source and should not be promoted without valid source integrity.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2011-2015 / body=Hatchback / fuel=petrol / engine=1.2L / hp=69 / trans=5-speed manual / drive=FWD | Supported 2011-2015 1.2L 69 hp manual row. | Keep; ensure source_refs/field_sources valid. | KEEP |
| V2 | trim=None / years=2011-2015 / body=Hatchback / fuel=petrol / engine=0.9L turbo / hp=85 / trans=5-speed automatic / drive=FWD | Transmission stored as conventional 5-speed automatic, but Israeli sources describe the 0.9 TwinAir 85 hp as robotized/automated; manual 0.9 rows also appear in price-list sources. | Change transmission to 5-speed automated manual / robotized per schema; add separate 0.9L 85 hp manual row only if repo-local/embedded Carzone-Yad2 source can be attached; otherwise report as review-only missing-candidate. | FIX |
| V3 | trim=None / years=2007-2011 / body=Hatchback / fuel=petrol / engine=1.4L / hp=95 / trans=5-speed manual / drive=FWD | Older 2007-2011 1.4L 95 hp rows are weakly grounded compared with stronger 2011-2015 Israeli Ypsilon evidence. | Keep only if repo-local Auto source is valid and field-level grounded; otherwise move these two rows to non-blocking review with lineage. | MOVE TO REVIEW |
| V4 | trim=None / years=2007-2011 / body=Hatchback / fuel=petrol / engine=1.4L / hp=95 / trans=5-speed automatic / drive=FWD | Older 2007-2011 1.4L 95 hp rows are weakly grounded compared with stronger 2011-2015 Israeli Ypsilon evidence. | Keep only if repo-local Auto source is valid and field-level grounded; otherwise move these two rows to non-blocking review with lineage. | MOVE TO REVIEW |

### MODEL: `IL-confirmed|Land Rover|Defender`
CURRENT VALUE: clean profile index 487; model years 2007-2024; variants=10
WEB-VALIDATED FACT: Israeli historical sources support Defender 2007-2016 2.4/2.2 turbodiesel 122 hp manual 4WD. Israeli 2020+ sources support D200/D240/P400/PHEV rows, and the official Land Rover Israel 2026 price list confirms current Defender 90/110/130 D200/D250/D350, Defender 110 PHEV, and OCTA 4.4 V8 635. Normalize new Defender drivetrain as 4WD, not generic AWD.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2007-2012 / body=SUV / fuel=diesel / engine=2.4L turbodiesel / hp=122 / trans=6-speed manual / drive=4WD | Historical 2007-2016 Defender 2.4/2.2 turbodiesel 122 hp manual 4WD is supported. | Keep; ensure SUV/Pickup body split has valid field_sources. | KEEP |
| V2 | trim=None / years=2012-2016 / body=SUV / fuel=diesel / engine=2.2L turbodiesel / hp=122 / trans=6-speed manual / drive=4WD | Historical 2007-2016 Defender 2.4/2.2 turbodiesel 122 hp manual 4WD is supported. | Keep; ensure SUV/Pickup body split has valid field_sources. | KEEP |
| V3 | trim=None / years=2007-2012 / body=Pickup / fuel=diesel / engine=2.4L turbodiesel / hp=122 / trans=6-speed manual / drive=4WD | Historical 2007-2016 Defender 2.4/2.2 turbodiesel 122 hp manual 4WD is supported. | Keep; ensure SUV/Pickup body split has valid field_sources. | KEEP |
| V4 | trim=None / years=2012-2016 / body=Pickup / fuel=diesel / engine=2.2L turbodiesel / hp=122 / trans=6-speed manual / drive=4WD | Historical 2007-2016 Defender 2.4/2.2 turbodiesel 122 hp manual 4WD is supported. | Keep; ensure SUV/Pickup body split has valid field_sources. | KEEP |
| V5 | trim=None / years=2020-2021 / body=SUV / fuel=diesel / engine=2.0L turbo / hp=200 / trans=8-speed automatic / drive=AWD | New Defender is a 4WD/off-road drivetrain model; current row uses AWD normalization. | Change drivetrain to 4WD; keep years 2020-2021 and D200/D240 diesel values if source_refs valid. | FIX |
| V6 | trim=None / years=2020-2021 / body=SUV / fuel=diesel / engine=2.0L twin-turbo / hp=240 / trans=8-speed automatic / drive=AWD | New Defender is a 4WD/off-road drivetrain model; current row uses AWD normalization. | Change drivetrain to 4WD; keep years 2020-2021 and D200/D240 diesel values if source_refs valid. | FIX |
| V7 | trim=None / years=2020-2024 / body=SUV / fuel=mild_hybrid / engine=3.0L turbo inline-6 / hp=400 / trans=8-speed automatic / drive=AWD | P400 is petrol MHEV 3.0 inline-6; engine text currently lacks petrol/MHEV clarity and drivetrain should be 4WD. | Set engine to 3.0L petrol turbo inline-6 MHEV; fuel_type mild_hybrid; drivetrain 4WD; keep 2020-2024 unless repo-local 2026 official source extends it. | FIX |
| V8 | trim=None / years=2021-2024 / body=SUV / fuel=mild_hybrid / engine=3.0L turbo inline-6 / hp=200 / trans=8-speed automatic / drive=AWD | D200/D250 rows should be diesel MHEV 3.0 inline-6 and 4WD; official 2026 price list still supports D200/D250 Defender. | Set engine to 3.0L turbodiesel inline-6 MHEV; drivetrain 4WD; extend year_end to null/current for D200/D250 if source refs include 2026 official price list. | FIX |
| V9 | trim=None / years=2021-2024 / body=SUV / fuel=mild_hybrid / engine=3.0L turbo inline-6 / hp=250 / trans=8-speed automatic / drive=AWD | D200/D250 rows should be diesel MHEV 3.0 inline-6 and 4WD; official 2026 price list still supports D200/D250 Defender. | Set engine to 3.0L turbodiesel inline-6 MHEV; drivetrain 4WD; extend year_end to null/current for D200/D250 if source refs include 2026 official price list. | FIX |
| V10 | trim=None / years=2021-2024 / body=SUV / fuel=plug_in_hybrid / engine=2.0L turbo / hp=404 / trans=8-speed automatic / drive=AWD | Official 2026 price list supports Defender 110 PHEV, so this PHEV should not necessarily close at 2024; drivetrain should be 4WD. | Set drivetrain 4WD and extend current if linked to 2026 official price list; keep 404 hp unless repo-local source proves new hp value. | FIX |

Additional profile-level actions:
- ACTION: ADD — PROBLEM: Missing current official 2026 Defender D350 3.0D row. — TARGET VALUE: Add Defender 110 X-DYNAMIC HSE 3.0D 350: diesel/mild_hybrid as schema permits, 3.0L, 350 hp, 8-speed automatic, 4WD, year_start 2026/current, source=Land Rover Israel 2026 official price list.
- ACTION: ADD — PROBLEM: Missing current official 2026 Defender OCTA 4.4 V8 635 row. — TARGET VALUE: Add Defender OCTA/OCTA BLACK technical row: petrol, 4.4L V8, 635 hp, 8-speed automatic, 4WD, year_start 2026/current, source=Land Rover Israel 2026 official price list.

### MODEL: `IL-confirmed|Land Rover|Discovery`
CURRENT VALUE: clean profile index 488; model years 1990-2024; variants=6
WEB-VALIDATED FACT: Israeli sources support Discovery historical diesel rows including Discovery 5 2017 3.0D 258 and earlier generations. The official 2026 price list confirms current Discovery Dynamic SE 3.0D 250; existing D300 2021-2024 should not be the only current row.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=1990-1998 / body=SUV / fuel=diesel / engine=2.5L turbo / hp=111 / trans=4-speed automatic / drive=4WD | Historical Discovery row supported by Israeli catalog/editorial sources. | Keep closed historical years; verify sources. | KEEP |
| V2 | trim=None / years=1998-2004 / body=SUV / fuel=diesel / engine=2.5L turbo / hp=136 / trans=4-speed automatic / drive=4WD | Historical Discovery row supported by Israeli catalog/editorial sources. | Keep closed historical years; verify sources. | KEEP |
| V3 | trim=None / years=2004-2009 / body=SUV / fuel=diesel / engine=2.7L v6 turbo / hp=190 / trans=6-speed automatic / drive=4WD | Historical Discovery row supported by Israeli catalog/editorial sources. | Keep closed historical years; verify sources. | KEEP |
| V4 | trim=None / years=2012-2016 / body=SUV / fuel=diesel / engine=3.0L v6 turbo / hp=256 / trans=8-speed automatic / drive=4WD | Historical Discovery row supported by Israeli catalog/editorial sources. | Keep closed historical years; verify sources. | KEEP |
| V5 | trim=None / years=2017-2020 / body=SUV / fuel=diesel / engine=3.0L v6 turbo / hp=258 / trans=8-speed automatic / drive=4WD | Historical Discovery row supported by Israeli catalog/editorial sources. | Keep closed historical years; verify sources. | KEEP |
| V6 | trim=None / years=2021-2024 / body=SUV / fuel=mild_hybrid / engine=3.0L inline-6 turbo / hp=300 / trans=8-speed automatic / drive=4WD | D300 MHEV 2021-2024 row is supported historically, but official 2026 price list points to D250 as current. | Keep 2021-2024; do not use this as the only current Discovery row. Add current D250 row separately. | KEEP |

Additional profile-level actions:
- ACTION: ADD — PROBLEM: Missing current official Discovery 3.0D 250 row. — TARGET VALUE: Add Discovery Dynamic SE 3.0D 250: diesel/mild_hybrid as schema permits, 3.0L, 250 hp, 8-speed automatic, 4WD/AWD per schema, year_start 2026/current, source=Land Rover Israel 2026 official price list.

### MODEL: `IL-confirmed|Land Rover|Discovery Sport`
CURRENT VALUE: clean profile index 489; model years 2015-2024; variants=5
WEB-VALIDATED FACT: Israeli sources support Discovery Sport 2015-2019 petrol/diesel, 2020 petrol 200/249 hp, and P300e 1.5 PHEV 309 hp. The official 2026 price list confirms current Discovery Sport 2.0D 204; do not keep only old petrol/PHEV rows as current.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2015-2019 / body=SUV / fuel=petrol / engine=2.0L turbo / hp=240 / trans=9-speed automatic / drive=AWD | 2015-2019 petrol/diesel rows supported. | Keep; verify sources. | KEEP |
| V2 | trim=None / years=2016-2019 / body=SUV / fuel=diesel / engine=2.0L turbo / hp=180 / trans=9-speed automatic / drive=AWD | 2015-2019 petrol/diesel rows supported. | Keep; verify sources. | KEEP |
| V3 | trim=None / years=2020-2024 / body=SUV / fuel=mild_hybrid / engine=2.0L turbo / hp=200 / trans=9-speed automatic / drive=AWD | Israeli sources describe 2020 Discovery Sport 2.0 turbo petrol 200/249 hp; fuel_type mild_hybrid may be over-normalized if not explicitly sourced. | Set fuel_type to petrol unless repo-local official source explicitly says MHEV; keep 9-speed automatic AWD. | FIX |
| V4 | trim=None / years=2020-2024 / body=SUV / fuel=mild_hybrid / engine=2.0L turbo / hp=249 / trans=9-speed automatic / drive=AWD | Israeli sources describe 2020 Discovery Sport 2.0 turbo petrol 200/249 hp; fuel_type mild_hybrid may be over-normalized if not explicitly sourced. | Set fuel_type to petrol unless repo-local official source explicitly says MHEV; keep 9-speed automatic AWD. | FIX |
| V5 | trim=None / years=2021-2024 / body=SUV / fuel=plug_in_hybrid / engine=1.5L turbo / hp=309 / trans=8-speed automatic / drive=AWD | P300e 1.5 PHEV 309 hp row supported for 2021-2024. | Keep closed 2021-2024 unless official 2026 source proves current. | KEEP |

Additional profile-level actions:
- ACTION: ADD — PROBLEM: Missing current official Discovery Sport 2.0D 204 row. — TARGET VALUE: Add Discovery Sport 2.0D 204: diesel, 2.0L, 204 hp, automatic, AWD, year_start 2026/current, source=Land Rover Israel 2026 official price list.

### MODEL: `IL-confirmed|Land Rover|Freelander`
CURRENT VALUE: clean profile index 490; model years 1998-2014; variants=7
WEB-VALIDATED FACT: Freelander gen 1 and gen 2 are Israeli-market vehicles, but the clean catalog currently duplicates gen-2 technical rows between `Freelander` and `Freelander 2`. Keep one canonical clean profile and preserve `Freelander 2` as alias/lineage, not duplicate clean technical variants.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=1998-2006 / body=SUV / fuel=petrol / engine=1.8L / hp=120 / trans=5-speed manual / drive=AWD | Freelander generation 1 row supported. | Keep in canonical Freelander profile. | KEEP |
| V2 | trim=None / years=2001-2006 / body=SUV / fuel=diesel / engine=2.0L turbo / hp=112 / trans=5-speed automatic / drive=AWD | Freelander generation 1 row supported. | Keep in canonical Freelander profile. | KEEP |
| V3 | trim=None / years=2001-2006 / body=SUV / fuel=petrol / engine=2.5L v6 / hp=177 / trans=5-speed automatic / drive=AWD | Freelander generation 1 row supported. | Keep in canonical Freelander profile. | KEEP |
| V4 | trim=None / years=2007-2012 / body=SUV / fuel=petrol / engine=3.2L / hp=233 / trans=6-speed automatic / drive=AWD | Freelander generation 2 row can stay in canonical Freelander if duplicate `Freelander 2` profile is removed. | Keep here as canonical; merge any unique `Freelander 2` variants into this profile and add alias/lineage `Freelander 2`. | KEEP |
| V5 | trim=None / years=2007-2010 / body=SUV / fuel=diesel / engine=2.2L turbo / hp=160 / trans=6-speed automatic / drive=AWD | Freelander generation 2 row can stay in canonical Freelander if duplicate `Freelander 2` profile is removed. | Keep here as canonical; merge any unique `Freelander 2` variants into this profile and add alias/lineage `Freelander 2`. | KEEP |
| V6 | trim=None / years=2011-2014 / body=SUV / fuel=diesel / engine=2.2L turbo / hp=190 / trans=6-speed automatic / drive=AWD | Freelander generation 2 row can stay in canonical Freelander if duplicate `Freelander 2` profile is removed. | Keep here as canonical; merge any unique `Freelander 2` variants into this profile and add alias/lineage `Freelander 2`. | KEEP |
| V7 | trim=None / years=2013-2014 / body=SUV / fuel=petrol / engine=2.0L turbo / hp=240 / trans=6-speed automatic / drive=AWD | Freelander generation 2 row can stay in canonical Freelander if duplicate `Freelander 2` profile is removed. | Keep here as canonical; merge any unique `Freelander 2` variants into this profile and add alias/lineage `Freelander 2`. | KEEP |

### MODEL: `IL-confirmed|Land Rover|Freelander 2`
CURRENT VALUE: clean profile index 491; model years 2007-2014; variants=5
WEB-VALIDATED FACT: This profile overlaps `IL-confirmed|Land Rover|Freelander` for 2007-2014. Merge unique gen-2 rows into the canonical Freelander profile and remove the duplicate profile from clean, preserving lineage alias `Freelander 2`.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2007-2012 / body=SUV / fuel=petrol / engine=3.2L i6 / hp=233 / trans=6-speed automatic / drive=AWD | Duplicate generation profile overlaps `IL-confirmed/Land Rover/Freelander` 2007-2014. | Merge unique rows into canonical `Land Rover Freelander`, add alias/lineage `Freelander 2`, then remove this duplicate clean profile. | MERGE |
| V2 | trim=None / years=2012-2014 / body=SUV / fuel=petrol / engine=2.0L turbo / hp=240 / trans=6-speed automatic / drive=AWD | Duplicate generation profile overlaps `IL-confirmed/Land Rover/Freelander` 2007-2014. | Merge unique rows into canonical `Land Rover Freelander`, add alias/lineage `Freelander 2`, then remove this duplicate clean profile. | MERGE |
| V3 | trim=None / years=2007-2011 / body=SUV / fuel=diesel / engine=2.2L turbo / hp=160 / trans=6-speed automatic / drive=AWD | Duplicate generation profile overlaps `IL-confirmed/Land Rover/Freelander` 2007-2014. | Merge unique rows into canonical `Land Rover Freelander`, add alias/lineage `Freelander 2`, then remove this duplicate clean profile. | MERGE |
| V4 | trim=None / years=2011-2014 / body=SUV / fuel=diesel / engine=2.2L turbo / hp=150 / trans=6-speed automatic / drive=AWD | Duplicate generation profile overlaps `IL-confirmed/Land Rover/Freelander` 2007-2014. | Merge unique rows into canonical `Land Rover Freelander`, add alias/lineage `Freelander 2`, then remove this duplicate clean profile. | MERGE |
| V5 | trim=None / years=2011-2014 / body=SUV / fuel=diesel / engine=2.2L turbo / hp=190 / trans=6-speed automatic / drive=AWD | Duplicate generation profile overlaps `IL-confirmed/Land Rover/Freelander` 2007-2014. | Merge unique rows into canonical `Land Rover Freelander`, add alias/lineage `Freelander 2`, then remove this duplicate clean profile. | MERGE |

### MODEL: `IL-confirmed|Land Rover|Range Rover`
CURRENT VALUE: clean profile index 492; model years 2007-2024; variants=7
WEB-VALIDATED FACT: Official 2026 price list confirms current Range Rover 3.0D 350, PHEV 460, PHEV 550, 4.4P 530, and SV 4.4P 615. Old P510 PHEV should not be treated as the current official 2026 PHEV; keep older row closed and add current P460/P550.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2022-2024 / body=SUV / fuel=diesel / engine=3.0L turbo / hp=350 / trans=8-speed automatic / drive=AWD | Official 2026 price list still supports 3.0D 350 and 4.4P 530 Range Rover current rows. | Extend current/year_end null or 2026 with 2026 official source_refs; keep 8-speed AWD. | FIX |
| V2 | trim=None / years=2022-2024 / body=SUV / fuel=petrol / engine=4.4L v8 turbo / hp=530 / trans=8-speed automatic / drive=AWD | Official 2026 price list still supports 3.0D 350 and 4.4P 530 Range Rover current rows. | Extend current/year_end null or 2026 with 2026 official source_refs; keep 8-speed AWD. | FIX |
| V3 | trim=None / years=2022-2024 / body=SUV / fuel=plug_in_hybrid / engine=3.0L turbo / hp=510 / trans=8-speed automatic / drive=AWD | PHEV 510 is old current row; 2026 official price list shows PHEV 460 and PHEV 550 instead. | Close PHEV 510 at last supported year; add PHEV 460 and PHEV 550 current rows with 3.0L PHEV, 8AT, AWD. | FIX |
| V4 | trim=None / years=2018-2021 / body=SUV / fuel=plug_in_hybrid / engine=2.0L turbo / hp=404 / trans=8-speed automatic / drive=AWD | Historical Range Rover row supported. | Keep closed historical years; verify source refs. | KEEP |
| V5 | trim=None / years=2013-2018 / body=SUV / fuel=diesel / engine=3.0L v6 turbo / hp=258 / trans=8-speed automatic / drive=AWD | Historical Range Rover row supported. | Keep closed historical years; verify source refs. | KEEP |
| V6 | trim=None / years=2013-2021 / body=SUV / fuel=diesel / engine=4.4L v8 turbo / hp=339 / trans=8-speed automatic / drive=AWD | Historical Range Rover row supported. | Keep closed historical years; verify source refs. | KEEP |
| V7 | trim=None / years=2007-2010 / body=SUV / fuel=diesel / engine=3.6L v8 turbo / hp=272 / trans=6-speed automatic / drive=AWD | Historical Range Rover row supported. | Keep closed historical years; verify source refs. | KEEP |

Additional profile-level actions:
- ACTION: ADD — PROBLEM: Missing official current PHEV 460 and PHEV 550 rows. — TARGET VALUE: Add Range Rover PHEV 460 and PHEV 550: 3.0L PHEV, 8-speed automatic, AWD, current; source=Land Rover Israel 2026 official price list.
- ACTION: ADD — PROBLEM: Missing official current SV 4.4P 615 row. — TARGET VALUE: Add Range Rover SV 4.4P 615: petrol, 4.4L, 615 hp, 8-speed automatic, AWD, current; source=Land Rover Israel 2026 official price list.

### MODEL: `IL-confirmed|Land Rover|Range Rover Evoque`
CURRENT VALUE: clean profile index 493; model years 2011-2026; variants=4
WEB-VALIDATED FACT: Official 2026 price list confirms Evoque S 2.0P 250 and Evoque PHEV 269 1.5P. Historical 2011-2018 P240 is supported. Current P200/P249/P300e 309 rows need correction/closure or replacement with official 2026 P250/PHEV269.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2011-2018 / body=SUV / fuel=petrol / engine=2.0L turbo / hp=240 / trans=automatic / drive=AWD | 2011-2018 P240 petrol row supported. | Keep closed historical row. | KEEP |
| V2 | trim=None / years=2019-2026 / body=SUV / fuel=mild_hybrid / engine=2.0L turbo / hp=200 / trans=automatic / drive=AWD | Official 2026 price list does not list P200; current official row is P250 and PHEV269. | Close P200 at last supported year or move to review if only global. Do not leave open to 2026 without exact source. | FIX |
| V3 | trim=None / years=2019-2026 / body=SUV / fuel=mild_hybrid / engine=2.0L turbo / hp=249 / trans=automatic / drive=AWD | Official 2026 price list lists 2.0P 250; row says 249 hp and no trim. | Normalize to 250 hp if using official 2026 row; add/attach trim S if schema supports trim; keep current. | FIX |
| V4 | trim=None / years=2021-2026 / body=SUV / fuel=plug_in_hybrid / engine=1.5L turbo / hp=309 / trans=automatic / drive=AWD | Official 2026 price list lists Evoque PHEV 269 1.5P, while row is older P300e/309 hp. | Close 309 hp PHEV at last supported year and add current PHEV 269 row, or update only if repo-local source proves 309 remains current. | FIX |

Additional profile-level actions:
- ACTION: ADD — PROBLEM: Missing official current Evoque PHEV 269 row. — TARGET VALUE: Add Evoque S 1.5P PHEV 269 current row; close older 309 hp PHEV if no current source supports it.

### MODEL: `IL-likely|Land Rover|Range Rover Evoque`
CURRENT VALUE: clean profile index 494; model years 2011-2024; variants=6
WEB-VALIDATED FACT: This is a split/duplicate candidate against IL-confirmed Evoque. Convertible 2016-2018 may be a unique legitimate body row; other P240/P200/P250/PHEV rows overlap confirmed profile and must be merged or deleted.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2016-2018 / body=Convertible / fuel=petrol / engine=2.0L turbo / hp=240 / trans=9-speed automatic / drive=AWD | Convertible body row may be unique, but should not live in separate IL-likely duplicate profile. | Merge into IL-confirmed Evoque as 2016-2018 Convertible P240 9AT AWD if source valid; remove IL-likely profile. | MERGE |
| V2 | trim=None / years=2011-2013 / body=SUV / fuel=petrol / engine=2.0L turbo / hp=240 / trans=6-speed automatic / drive=AWD | Duplicate/overlap with IL-confirmed Evoque. | Merge source support into IL-confirmed row or delete duplicate after preserving lineage. | MERGE |
| V3 | trim=None / years=2014-2018 / body=SUV / fuel=petrol / engine=2.0L turbo / hp=240 / trans=9-speed automatic / drive=AWD | Duplicate/overlap with IL-confirmed Evoque. | Merge source support into IL-confirmed row or delete duplicate after preserving lineage. | MERGE |
| V4 | trim=None / years=2019-2024 / body=SUV / fuel=petrol / engine=2.0L turbo / hp=200 / trans=9-speed automatic / drive=AWD | Duplicate/overlap with IL-confirmed Evoque. | Merge source support into IL-confirmed row or delete duplicate after preserving lineage. | MERGE |
| V5 | trim=None / years=2019-2024 / body=SUV / fuel=petrol / engine=2.0L turbo / hp=250 / trans=9-speed automatic / drive=AWD | Duplicate/overlap with IL-confirmed Evoque. | Merge source support into IL-confirmed row or delete duplicate after preserving lineage. | MERGE |
| V6 | trim=None / years=2020-2024 / body=SUV / fuel=plug_in_hybrid / engine=1.5L turbo / hp=309 / trans=8-speed automatic / drive=AWD | Duplicate/overlap with IL-confirmed Evoque. | Merge source support into IL-confirmed row or delete duplicate after preserving lineage. | MERGE |

### MODEL: `IL-confirmed|Land Rover|Range Rover Sport`
CURRENT VALUE: clean profile index 495; model years 2013-2024; variants=6
WEB-VALIDATED FACT: Official 2026 price list confirms current Range Rover Sport D250, P400, D300, D350, P530, SV 4.4 635, and PHEV 460. Historical 2013-2022 diesel/PHEV/SVR rows are supported, but PHEV 510 is not the official 2026 current PHEV.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2013-2022 / body=SUV / fuel=diesel / engine=3.0L v6 twin-turbo / hp=306 / trans=8-speed automatic / drive=4WD | Historical Range Rover Sport row supported. | Keep closed historical row. | KEEP |
| V2 | trim=None / years=2018-2022 / body=SUV / fuel=plug_in_hybrid / engine=2.0L turbo / hp=404 / trans=8-speed automatic / drive=4WD | Historical Range Rover Sport row supported. | Keep closed historical row. | KEEP |
| V3 | trim=None / years=2018-2022 / body=SUV / fuel=petrol / engine=5.0L v8 supercharged / hp=575 / trans=8-speed automatic / drive=4WD | Historical Range Rover Sport row supported. | Keep closed historical row. | KEEP |
| V4 | trim=None / years=2022-2024 / body=SUV / fuel=mild_hybrid / engine=3.0L inline-6 twin-turbo / hp=300 / trans=8-speed automatic / drive=4WD | Official 2026 price list supports D300 current and also D250/D350 rows. | Extend D300 current if source attached; add D250 and D350 current rows. | FIX |
| V5 | trim=None / years=2022-2024 / body=SUV / fuel=plug_in_hybrid / engine=3.0L inline-6 turbo / hp=460 / trans=8-speed automatic / drive=4WD | Official 2026 price list supports PHEV 460 current. | Keep/extend PHEV 460 current with official source. | FIX |
| V6 | trim=None / years=2022-2024 / body=SUV / fuel=plug_in_hybrid / engine=3.0L inline-6 turbo / hp=510 / trans=8-speed automatic / drive=4WD | PHEV 510 is not the official 2026 PHEV row; official current is PHEV 460. | Close PHEV 510 at last supported year; do not treat as current. | FIX |

Additional profile-level actions:
- ACTION: ADD — PROBLEM: Missing official current Range Rover Sport rows from 2026 price list. — TARGET VALUE: Add D250, P400, D350, P530 and SV 4.4 635 current technical rows; keep PHEV460 current; close PHEV510 unless exact support exists.

### MODEL: `IL-confirmed|Land Rover|Range Rover Velar`
CURRENT VALUE: clean profile index 496; model years 2017-2024; variants=7
WEB-VALIDATED FACT: Official 2026 price list confirms current Velar SE R-Dynamic 3.0P 400. Historical Velar 2017-2024 P250, P380, D180/D240/D300, PHEV404/D204 rows are supported by repo-local sources, but current clean should include the official P400 row.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2017-2024 / body=SUV / fuel=petrol / engine=2.0L turbo / hp=250 / trans=8-speed automatic / drive=AWD | Historical Velar row supported. | Keep closed/historical as-is after source integrity check. | KEEP |
| V2 | trim=None / years=2017-2020 / body=SUV / fuel=petrol / engine=3.0L v6 supercharged / hp=380 / trans=8-speed automatic / drive=AWD | Historical Velar row supported. | Keep closed/historical as-is after source integrity check. | KEEP |
| V3 | trim=None / years=2017-2020 / body=SUV / fuel=diesel / engine=2.0L turbo / hp=180 / trans=8-speed automatic / drive=AWD | Historical Velar row supported. | Keep closed/historical as-is after source integrity check. | KEEP |
| V4 | trim=None / years=2017-2020 / body=SUV / fuel=diesel / engine=2.0L turbo / hp=240 / trans=8-speed automatic / drive=AWD | Historical Velar row supported. | Keep closed/historical as-is after source integrity check. | KEEP |
| V5 | trim=None / years=2017-2020 / body=SUV / fuel=diesel / engine=3.0L v6 turbo / hp=300 / trans=8-speed automatic / drive=AWD | Historical Velar row supported. | Keep closed/historical as-is after source integrity check. | KEEP |
| V6 | trim=None / years=2021-2024 / body=SUV / fuel=plug_in_hybrid / engine=2.0L turbo / hp=404 / trans=8-speed automatic / drive=AWD | 2021-2024 PHEV404/D204 rows supported historically. | Keep closed at 2024 unless repo-local official source proves current. | KEEP |
| V7 | trim=None / years=2021-2024 / body=SUV / fuel=mild_hybrid / engine=2.0L turbo / hp=204 / trans=8-speed automatic / drive=AWD | 2021-2024 PHEV404/D204 rows supported historically. | Keep closed at 2024 unless repo-local official source proves current. | KEEP |

Additional profile-level actions:
- ACTION: ADD/MERGE — PROBLEM: Missing official current Velar 3.0P 400 in confirmed profile. — TARGET VALUE: Merge from IL-likely Velar V1 or add to IL-confirmed as SE R-Dynamic 3.0P 400, petrol/mild_hybrid as schema permits, 8-speed automatic AWD, current.

### MODEL: `IL-likely|Land Rover|Range Rover Velar`
CURRENT VALUE: clean profile index 497; model years 2017-2024; variants=4
WEB-VALIDATED FACT: This profile overlaps IL-confirmed Velar. Dynamic HSE 3.0P 400 is the only row that should be promoted/merged as official current technical row; the others duplicate P250/PHEV404/D180 rows already represented.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=Dynamic HSE / years=2021-2024 / body=SUV / fuel=mild_hybrid / engine=3.0L turbo / hp=400 / trans=8-speed automatic / drive=AWD | Official 2026 price list supports Velar SE R-Dynamic 3.0P 400; this is legitimate but should merge into IL-confirmed Velar. | Merge/promote into IL-confirmed Velar as current 3.0P 400 row with trim SE R-Dynamic; remove IL-likely duplicate profile. | MERGE |
| V2 | trim=S / years=2017-2024 / body=SUV / fuel=petrol / engine=2.0L turbo / hp=250 / trans=8-speed automatic / drive=AWD | Duplicate/overlap with IL-confirmed Velar rows. | Merge source support or delete duplicate from IL-likely after preserving lineage. | MERGE |
| V3 | trim=Dynamic SE / years=2021-2024 / body=SUV / fuel=plug_in_hybrid / engine=2.0L turbo / hp=404 / trans=8-speed automatic / drive=AWD | Duplicate/overlap with IL-confirmed Velar rows. | Merge source support or delete duplicate from IL-likely after preserving lineage. | MERGE |
| V4 | trim=S / years=2017-2020 / body=SUV / fuel=diesel / engine=2.0L turbo / hp=180 / trans=8-speed automatic / drive=AWD | Duplicate/overlap with IL-confirmed Velar rows. | Merge source support or delete duplicate from IL-likely after preserving lineage. | MERGE |

### MODEL: `global-reference-only|Leapmotor|C10`
CURRENT VALUE: clean profile index 498; model years 2024-None; variants=1
WEB-VALIDATED FACT: Israeli sources confirm C10 is marketed in Israel. The current global-reference-only row is duplicate/split against IL-confirmed C10 and must not remain a separate clean profile.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2024-None / body=SUV / fuel=electric / engine=electric / hp=218 / trans=single_speed / drive=RWD | Duplicate global-reference-only clean profile while Israeli C10 profile exists. | Merge/delete into IL-confirmed Leapmotor C10; do not keep separate global clean row. | MERGE |

### MODEL: `IL-confirmed|Leapmotor|C10`
CURRENT VALUE: clean profile index 499; model years 2024-None; variants=1
WEB-VALIDATED FACT: Leapmotor Israel, Carzone, Auto and Yad2 support C10 BEV in Israel with 215 hp RWD, not 218 hp. 2026 Israeli price sources add C10 PHEV 1.5 with 215 hp and Long Range / higher-output BEV variants. EV displacement must remain null and transmission single_speed/direct_drive per schema.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2024-None / body=SUV / fuel=electric / engine=electric / hp=218 / trans=single_speed / drive=RWD | Israeli sources list C10 BEV at 215 hp, not 218 hp; 2026 sources add PHEV and Long Range variants. | Set BEV hp to 215, keep EV displacement null and single_speed RWD; add 2026 PHEV 1.5 215 and Long Range/Performance BEV rows only with embedded source_refs. | FIX |

Additional profile-level actions:
- ACTION: ADD — PROBLEM: Missing 2026 C10 PHEV and higher-output BEV variants from Israeli price sources. — TARGET VALUE: Add C10 PHEV 1.5 215 hp and C10 Long Range/Performance BEV rows only with embedded Carzone/Yad2/Cartube source refs; EV rows keep displacement null and single_speed/direct_drive.

### MODEL: `IL-confirmed|Leapmotor|T03`
CURRENT VALUE: clean profile index 500; model years 2022-2024; variants=1
WEB-VALIDATED FACT: Israeli sources support T03 2022 with 108 hp EV. Later Israeli sources mention an updated 95 hp version; do not simply extend the 108 hp row through 2026 if current data is 95 hp.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2022-2024 / body=Hatchback / fuel=electric / engine=electric / hp=108 / trans=single_speed / drive=FWD | 2022 row 108 hp is supported; later/current Israeli sources mention updated 95 hp. Current row closing at 2024 may be too early, but extending 108 hp to 2026 would be wrong. | Keep 108 hp for 2022-2024; add/replace current 95 hp row for 2025/2026 if repo-local Auto/Gear/Yad2 source can be attached. | FIX |

### MODEL: `IL-confirmed|Lexus|CT 200h`
CURRENT VALUE: clean profile index 501; model years 2011-2020; variants=1
WEB-VALIDATED FACT: Israeli sources support CT200h 2011-2020 with 1.8 hybrid 136 hp, CVT, FWD hatchback.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2011-2020 / body=Hatchback / fuel=hybrid / engine=1.8L / hp=136 / trans=cvt / drive=FWD | CT200h 1.8 hybrid 136 hp CVT FWD 2011-2020 supported. | Keep historical row. | KEEP |

### MODEL: `global-reference-only|Lexus|ES`
CURRENT VALUE: clean profile index 502; model years 2018-2024; variants=1
WEB-VALIDATED FACT: Duplicate/split against IL-confirmed ES. Israeli sources support ES 300h 2.5 hybrid 218 hp. Merge into IL-confirmed, do not keep global-reference-only clean duplicate.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=300h / years=2018-2024 / body=Sedan / fuel=hybrid / engine=2.5L inline-4 / hp=218 / trans=cvt / drive=FWD | Duplicate global profile for Israeli-supported ES 300h. | Merge into IL-confirmed ES and delete global clean duplicate. | MERGE |

### MODEL: `IL-confirmed|Lexus|ES`
CURRENT VALUE: clean profile index 503; model years 2018-2024; variants=1
WEB-VALIDATED FACT: Israeli sources and current Lexus Israel model list support ES Hybrid / ES 300h. Set trim to 300h rather than null, and keep current if Lexus Israel repo/local sources show 2026 model presence.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2018-2024 / body=Sedan / fuel=hybrid / engine=2.5L inline-4 / hp=218 / trans=cvt / drive=FWD | Trim is null although Israeli model is ES 300h; Lexus Israel current list supports ES Hybrid. | Set version_or_trim to 300h; extend current/year_end null or 2026 if Lexus Israel source_refs valid. | FIX |

### MODEL: `IL-confirmed|Lexus|GS`
CURRENT VALUE: clean profile index 504; model years 2006-2020; variants=6
WEB-VALIDATED FACT: Israeli sources support GS 2006-2020 including GS250 2.5 209 hp, GS450h 3.5 hybrid 345 hp, and GS F 5.0 V8 477 hp. Keep as historical; do not mark current.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2006-2011 / body=Sedan / fuel=petrol / engine=3.0L v6 / hp=249 / trans=6-speed automatic / drive=RWD | GS technical row supported historically by Israeli sources. | Keep historical row; do not mark current. | KEEP |
| V2 | trim=None / years=2012-2016 / body=Sedan / fuel=petrol / engine=2.5L v6 / hp=209 / trans=6-speed automatic / drive=RWD | GS technical row supported historically by Israeli sources. | Keep historical row; do not mark current. | KEEP |
| V3 | trim=None / years=2014-2020 / body=Sedan / fuel=hybrid / engine=2.5L i4 / hp=223 / trans=cvt / drive=RWD | GS technical row supported historically by Israeli sources. | Keep historical row; do not mark current. | KEEP |
| V4 | trim=None / years=2012-2020 / body=Sedan / fuel=hybrid / engine=3.5L v6 / hp=345 / trans=cvt / drive=RWD | GS technical row supported historically by Israeli sources. | Keep historical row; do not mark current. | KEEP |
| V5 | trim=None / years=2016-2020 / body=Sedan / fuel=petrol / engine=2.0L turbo / hp=245 / trans=8-speed automatic / drive=RWD | GS technical row supported historically by Israeli sources. | Keep historical row; do not mark current. | KEEP |
| V6 | trim=None / years=2016-2020 / body=Sedan / fuel=petrol / engine=5.0L v8 / hp=477 / trans=8-speed automatic / drive=RWD | GS technical row supported historically by Israeli sources. | Keep historical row; do not mark current. | KEEP |

### MODEL: `global-reference-only|Lexus|GX`
CURRENT VALUE: clean profile index 505; model years 2010-None; variants=2
WEB-VALIDATED FACT: Sources are preview/coming-to-Israel and marketplace-level, while Lexus Israel current new-car list does not show GX as a confirmed official clean model. Keep lineage, but move to non-blocking review/archive unless repo-local official sales evidence exists.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2010-2023 / body=SUV / fuel=petrol / engine=4.6L v8 / hp=301 / trans=6-speed automatic / drive=4WD | GX has preview/coming-to-Israel/marketplace evidence but no strong official Lexus Israel clean sales page in embedded sources. | Move to non-blocking review/archive with reason `weak_israeli_sales_grounding`; keep lineage and source links. | MOVE TO REVIEW |
| V2 | trim=None / years=2024-None / body=SUV / fuel=petrol / engine=3.4L v6 twin-turbo / hp=354 / trans=10-speed automatic / drive=4WD | GX has preview/coming-to-Israel/marketplace evidence but no strong official Lexus Israel clean sales page in embedded sources. | Move to non-blocking review/archive with reason `weak_israeli_sales_grounding`; keep lineage and source links. | MOVE TO REVIEW |

### MODEL: `IL-confirmed|Lexus|IS`
CURRENT VALUE: clean profile index 506; model years 2006-2021; variants=5
WEB-VALIDATED FACT: Israeli sources support IS250, IS-F, IS250C, IS300h, and IS200t. Later iCar references indicate IS 2021-2025 with turbo petrol; add/extend only if repo-local source supports exact current row.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2006-2013 / body=Sedan / fuel=petrol / engine=2.5L v6 / hp=208 / trans=6-speed automatic / drive=RWD | IS row supported historically; later current IS requires separate exact source before adding. | Keep as historical; do not add 2021-2025 turbo row unless repo-local exact source is present. | KEEP |
| V2 | trim=None / years=2008-2012 / body=Sedan / fuel=petrol / engine=5.0L v8 / hp=423 / trans=8-speed automatic / drive=RWD | IS row supported historically; later current IS requires separate exact source before adding. | Keep as historical; do not add 2021-2025 turbo row unless repo-local exact source is present. | KEEP |
| V3 | trim=None / years=2009-2013 / body=Convertible / fuel=petrol / engine=2.5L v6 / hp=208 / trans=6-speed automatic / drive=RWD | IS row supported historically; later current IS requires separate exact source before adding. | Keep as historical; do not add 2021-2025 turbo row unless repo-local exact source is present. | KEEP |
| V4 | trim=None / years=2013-2021 / body=Sedan / fuel=hybrid / engine=2.5L / hp=223 / trans=cvt / drive=RWD | IS row supported historically; later current IS requires separate exact source before adding. | Keep as historical; do not add 2021-2025 turbo row unless repo-local exact source is present. | KEEP |
| V5 | trim=None / years=2015-2018 / body=Sedan / fuel=petrol / engine=2.0L turbo / hp=245 / trans=8-speed automatic / drive=RWD | IS row supported historically; later current IS requires separate exact source before adding. | Keep as historical; do not add 2021-2025 turbo row unless repo-local exact source is present. | KEEP |

### MODEL: `IL-confirmed|Lexus|LBX`
CURRENT VALUE: clean profile index 507; model years 2024-2024; variants=1
WEB-VALIDATED FACT: Lexus Israel officially markets LBX with trims ELEGANT, ELEGANT+, EMOTION, RELAX and COOL. The current row incorrectly stores all trims as a comma-joined string and year_end 2024 despite active official model presence. Split/normalize trims and keep current.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=Elegant, Elegant Plus, Emotion, Relax, Cool / years=2024-2024 / body=Crossover / fuel=hybrid / engine=1.5L 3-cylinder / hp=136 / trans=cvt / drive=FWD | Five trims are stored as one comma-joined string and year_end is 2024 despite active Lexus Israel model page. | Split/normalize trims `Elegant`, `Elegant Plus`, `Emotion`, `Relax`, `Cool` into schema-supported trim representation; keep same 1.5 hybrid 136 hp CVT FWD tech; set current/year_end null or 2026. | SPLIT/FIX |

Additional profile-level actions:
- ACTION: CODE/REPORTING FIX — PROBLEM: available_values_for_website must not expose a single combined trim string. — TARGET VALUE: Regenerate website values so LBX trims are separate selectable values: Elegant, Elegant Plus, Emotion, Relax, Cool.

### MODEL: `IL-confirmed|Lexus|LC`
CURRENT VALUE: clean profile index 508; model years 2017-2024; variants=4
WEB-VALIDATED FACT: Israeli sources support LC500h 3.5 hybrid 359 hp coupe and LC500 5.0 V8 coupe/convertible; iCar/Cartube support 477 hp at launch and later 464 hp rows. Keep historical/current-through-2024 rows only if source refs are valid.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=None / years=2017-2024 / body=Coupe / fuel=hybrid / engine=3.5L v6 / hp=359 / trans=cvt / drive=RWD | LC row supported by Israeli sources; 477 hp launch and later 464 hp rows appear as separate technical periods. | Keep if source refs valid; do not extend beyond 2024 without current Lexus Israel support. | KEEP |
| V2 | trim=None / years=2017-2020 / body=Coupe / fuel=petrol / engine=5.0L v8 / hp=477 / trans=10-speed automatic / drive=RWD | LC row supported by Israeli sources; 477 hp launch and later 464 hp rows appear as separate technical periods. | Keep if source refs valid; do not extend beyond 2024 without current Lexus Israel support. | KEEP |
| V3 | trim=None / years=2020-2024 / body=Coupe / fuel=petrol / engine=5.0L v8 / hp=464 / trans=10-speed automatic / drive=RWD | LC row supported by Israeli sources; 477 hp launch and later 464 hp rows appear as separate technical periods. | Keep if source refs valid; do not extend beyond 2024 without current Lexus Israel support. | KEEP |
| V4 | trim=None / years=2020-2024 / body=Convertible / fuel=petrol / engine=5.0L v8 / hp=464 / trans=10-speed automatic / drive=RWD | LC row supported by Israeli sources; 477 hp launch and later 464 hp rows appear as separate technical periods. | Keep if source refs valid; do not extend beyond 2024 without current Lexus Israel support. | KEEP |

### MODEL: `global-reference-only|Lexus|LM`
CURRENT VALUE: clean profile index 509; model years 2023-None; variants=1
WEB-VALIDATED FACT: Duplicate/split against IL-confirmed LM. Lexus Israel officially markets LM Hybrid and Cartube/iCar sources support 350h; merge into IL-confirmed and remove duplicate global profile.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=350h / years=2023-None / body=MPV / fuel=hybrid / engine=2.5L inline-4 / hp=250 / trans=cvt / drive=AWD | Duplicate global profile for official Israeli LM 350h. | Merge into IL-confirmed LM and delete global clean duplicate. | MERGE |

### MODEL: `IL-confirmed|Lexus|LM`
CURRENT VALUE: clean profile index 510; model years 2023-None; variants=1
WEB-VALIDATED FACT: Lexus Israel officially markets LM Hybrid. Keep LM 350h MPV hybrid 2.5, CVT, AWD as current, with trim 350h and lineage from duplicate global profile.
SOURCE: see embedded sources above and repo-local source_indexes/field_sources attached to this profile.

| VARIANT | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---|---|---|---|---|
| V1 | trim=350h / years=2023-None / body=MPV / fuel=hybrid / engine=2.5L inline-4 / hp=250 / trans=cvt / drive=AWD | Lexus Israel officially markets LM Hybrid / 350h; technical fields are plausible. | Keep current; ensure trim 350h and official source_refs. | KEEP |

## Cross-profile cleanup required in RUN 2

- MERGE/ALIAS: `IL-confirmed|Land Rover|Freelander 2` into `IL-confirmed|Land Rover|Freelander`; preserve alias/lineage `Freelander 2`; remove duplicate clean profile.
- MERGE/ALIAS: `IL-likely|Land Rover|Range Rover Evoque` into `IL-confirmed|Land Rover|Range Rover Evoque`; keep unique Convertible row if grounded; remove duplicate IL-likely profile.
- MERGE/ALIAS: `IL-likely|Land Rover|Range Rover Velar` into `IL-confirmed|Land Rover|Range Rover Velar`; promote only the official/current P400 row and delete duplicate rows.
- MERGE/ALIAS: `global-reference-only|Leapmotor|C10` into `IL-confirmed|Leapmotor|C10`; fix 218 hp to 215 hp for Israeli BEV row.
- MERGE/ALIAS: `global-reference-only|Lexus|ES` into `IL-confirmed|Lexus|ES`; set trim 300h.
- MOVE TO REVIEW: `global-reference-only|Lexus|GX` unless repo-local official Israeli sales evidence proves clean status.
- MERGE/ALIAS: `global-reference-only|Lexus|LM` into `IL-confirmed|Lexus|LM`; delete duplicate global clean profile.
- NORMALIZATION: LBX trims must not remain a single comma-joined string in `version_or_trim` or website values.
- CURRENT YEAR LOGIC: current 2026 official Land Rover/Lexus/Leapmotor rows should be `year_end: null` or the project’s current marker, not stale 2024, only where embedded official/current source supports it.
- ARCHIVE/REVIEW: Any row that cannot attach valid field_sources after these instructions must move to non-blocking review/archive with reason and lineage, not be silently deleted.

## Expected RUN 2 success criteria

- All 25 RUN 2 profiles and 97 variants above are explicitly handled.
- No duplicate clean profiles remain for Freelander/Freelander 2, Evoque IL-confirmed/IL-likely, Velar IL-confirmed/IL-likely, Leapmotor C10 global/IL, Lexus ES global/IL, or Lexus LM global/IL.
- LBX trims are normalized into separate selectable values or schema-supported trim representation.
- Land Rover 2026 official current variants are added/updated only from the embedded official price list, with valid source refs.
- Leapmotor C10 BEV hp is corrected to Israeli 215 hp; EV schema remains displacement null + single_speed/direct_drive.
- GX is not kept in clean unless official Israeli sales evidence exists in repo-local sources; otherwise non-blocking review/archive.
- The cursor must not move backward and must not skip beyond RUN 2 scope as a side effect.


---

# BATCH25 RESTART — RUN 3 VARIANT-LEVEL CODEX TASK

## Non-negotiable execution rules

Do not browse the internet. All web-validation facts and target corrections are embedded in this task file. Use this task file as the single source of truth. Do not apply corrections that are not instructed here. If repo-local evidence conflicts with this task file, report it instead of guessing. If a variant cannot be grounded with the embedded facts or repo-local sources, move it to non-blocking archive/review rather than fabricating data.

This RUN covers only RUN 3 clean profiles. Do not implement FINAL blockers/review/unmatched yet, except to avoid regressions caused by RUN 3 corrections. RUN 1 and RUN 2 were handled in their own task files.

## RUN 3 scope

RUN 3 starts after `IL-confirmed|Lexus|LM` and contains 4 clean model profiles / 17 technical variants:

1. `IL-confirmed|Lexus|LS` — 4 variants
2. `IL-confirmed|Lexus|LX` — 3 variants
3. `IL-confirmed|Lexus|NX` — 7 variants
4. `IL-confirmed|Lexus|RC` — 3 variants

## Local audit/test baseline from uploaded ZIP

- `python -m compileall scripts` — PASS
- `python -m scripts.catalog_validation` — PASS
- `python -m scripts.catalog_quality_scan` — PASS
- `python -m pytest -q` — FAIL in this sandbox because `streamlit` is missing while collecting `tests/test_selectable_provider_and_github.py`; in a real repo environment install requirements or report dependency/test-environment failure, do not hide it.
- `git diff --check` — run in the real git repo after changes; the uploaded ZIP extraction here is not a git checkout.

## Required post-implementation checks

Run all of these after applying RUN 3 only:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Then directly inspect readiness, review, archive, quality scan, `compute_resume_state()`, unmatched_output_keys, active blockers, and cursor. Do not approve by console output alone.

## Embedded web-validation sources used for RUN 3

### Lexus official/current
- Lexus Israel new cars index (current 2026 model menu; lists LS, NX but not LX in new-car menu): https://www.lexus.co.il/new-cars
- Lexus Israel homepage/current model menu (shows LBX/UX/RZ/NX/RX/LM/LS/IS; LX appears under history rather than new-cars): https://www.lexus.co.il/
- Lexus Israel LS current page: https://www.lexus.co.il/new-cars/ls
- Lexus Israel LS prices/costs page: https://www.lexus.co.il/new-cars/ls/prices-and-costs
- Lexus Israel NX current page: https://www.lexus.co.il/new-cars/nx
- Lexus Israel NX specifications: https://www.lexus.co.il/new-cars/nx/specifications
- Lexus Israel NX build/current PHEV data: https://www.lexus.co.il/new-cars/nx/build

### Lexus LS historical/current support
- iCar Lexus LS / LS460 2006-2017 pages: https://www.icar.co.il/לקסוס/לקסוס_LS/לקסוס_LS_יד_שניה_דגם_2006/ and https://www.icar.co.il/לקסוס/לקסוס_LS460/לקסוס_LS460_יד_שניה_ד11/
- Cartube Lexus LS 2018 Israel launch: https://www.cartube.co.il/חדשות-רכב/לקסוס-ls-החדשה-2018-בישראל-מחיר-החל-מ-795000-שקל
- Lexus Israel 2024 price list PDF stored/referenced by repo: https://www.lexus.co.il/content/dam/lexus/israel/prices/Lexus-Price-List-2024.pdf

### Lexus LX support
- Lexus Israel LX history page: https://www.lexus.co.il/car-history/lx
- Auto.co.il Lexus LX600 Israel launch 2022: https://www.auto.co.il/articles/car-news/local-news/135622/
- Cartube Lexus LX price/model page: https://www.cartube.co.il/מחירון-רכב-חדש/לקסוס/לקסוס-lx
- Cartube Lexus LX600 Takumi 2023 technical page: https://www.cartube.co.il/מחירון-רכב-חדש/לקסוס/לקסוס-lx/2020-לקסוס-lx600-takumi
- Cartube Lexus LX600 Takumi VIP 2024 technical page: https://www.cartube.co.il/מחירון-רכב-חדש/לקסוס/לקסוס-lx/3163-לקסוס-lx600-takumi-vip
- Carzone Lexus LX 2024: https://www.carzone.co.il/Lexus/LX/2024/
- Carzone Lexus LX 2026: https://www.carzone.co.il/Lexus/LX/2026/
- Yad2 Lexus LX price list: https://www.yad2.co.il/price-list/feed?manufacturer=26&model=10324

### Lexus NX support
- Cartube Lexus NX Israel 2014 launch: https://www.cartube.co.il/חדשות-רכב/לקסוס-nx-בישראל-מחיר-החל-מ-296000-שקל
- iCar Lexus NX 2015-2021: https://www.icar.co.il/לקסוס/לקסוס_NX/לקסוס_NX_יד_שניה_ד10/
- iCar Lexus NX 2020 NX300 Premium 4x4: https://www.icar.co.il/לקסוס/לקסוס_NX/לקסוס_NX_יד_שניה_ד10/version22144/
- Cartube Lexus NX 2018 facelift Israel: https://www.cartube.co.il/חדשות-רכב/לקסוס-nx-2018-החדש-בישראל-מחיר-275000-שקל
- Cartube 2022 Lexus NX Israel launch with PHEV: https://www.cartube.co.il/חדשות-רכב/כולל-דגם-פלאג-אין-2022-לקסוס-nx-החדש-בישראל-מחיר-289900-שקל
- iCar Lexus NX new/current: https://www.icar.co.il/לקסוס/לקסוס_NX/לקסוס_NX_חדש/

### Lexus RC support
- iCar Lexus RC main page: https://www.icar.co.il/לקסוס/לקסוס_RC/
- iCar Lexus RC 2017 200t F-Sport: https://www.icar.co.il/לקסוס/לקסוס_RC/לקסוס_RC_יד_שניה_ד10/version17685/
- Cartube Lexus RC 200t Israel launch: https://www.cartube.co.il/חדשות-רכב/לקסוס-rc-200t-בישראל-מחיר-החל-מ-325-000-שקל
- TheCar Lexus RC F Israel launch: https://thecar.co.il/לקסוס-rc-f-בישראל/
- Cartube Lexus RC 2019 Israel facelift: https://www.cartube.co.il/חדשות-רכב/לקסוס-rc-החדשה-2019-נחתה-בישראל

## RUN 3 actual variant inventory from uploaded ZIP

### IL-confirmed|Lexus|LS — model_years=2006..2024
- V1: version_or_trim=null; body_type='Sedan'; fuel_type='petrol'; engine='4.6L v8 naturally aspirated'; engine_displacement_l=4.6; horsepower_hp=380; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2006; year_end=2017; support_level='direct'; source_indexes=[1024]
- V2: version_or_trim=null; body_type='Sedan'; fuel_type='hybrid'; engine='5.0L v8 hybrid'; engine_displacement_l=5.0; horsepower_hp=438; transmission='cvt'; drivetrain='AWD'; year_start=2007; year_end=2017; support_level='direct'; source_indexes=[1024]
- V3: version_or_trim=null; body_type='Sedan'; fuel_type='petrol'; engine='3.5L v6 twin-turbo'; engine_displacement_l=3.5; horsepower_hp=417; transmission='10-speed automatic'; drivetrain='RWD'; year_start=2018; year_end=2021; support_level='direct'; source_indexes=[1025, 1026]
- V4: version_or_trim=null; body_type='Sedan'; fuel_type='hybrid'; engine='3.5L v6 hybrid'; engine_displacement_l=3.5; horsepower_hp=359; transmission='10-speed automatic'; drivetrain='RWD'; year_start=2018; year_end=2024; support_level='direct'; source_indexes=[1025, 1027]

### IL-confirmed|Lexus|LX — model_years=2008..2026
- V1: version_or_trim=null; body_type='SUV'; fuel_type='petrol'; engine='5.7L v8'; engine_displacement_l=5.7; horsepower_hp=367; transmission='6-speed automatic'; drivetrain='4WD'; year_start=2008; year_end=2015; support_level='direct'; source_indexes=[2, 3]
- V2: version_or_trim=null; body_type='SUV'; fuel_type='petrol'; engine='5.7L v8'; engine_displacement_l=5.7; horsepower_hp=367; transmission='8-speed automatic'; drivetrain='4WD'; year_start=2016; year_end=2021; support_level='direct'; source_indexes=[2, 3]
- V3: version_or_trim=null; body_type='SUV'; fuel_type='petrol'; engine='3.5L twin-turbo v6'; engine_displacement_l=3.5; horsepower_hp=409; transmission='10-speed automatic'; drivetrain='4WD'; year_start=2022; year_end=2026; support_level='direct'; source_indexes=[1, 3]

### IL-confirmed|Lexus|NX — model_years=2014..None
- V1: version_or_trim=null; body_type='SUV'; fuel_type='hybrid'; engine='2.5L'; engine_displacement_l=2.5; horsepower_hp=197; transmission='cvt'; drivetrain='FWD'; year_start=2014; year_end=2021; support_level='direct'; source_indexes=[0, 3]
- V2: version_or_trim=null; body_type='SUV'; fuel_type='hybrid'; engine='2.5L'; engine_displacement_l=2.5; horsepower_hp=197; transmission='cvt'; drivetrain='AWD'; year_start=2014; year_end=2021; support_level='direct'; source_indexes=[0, 3]
- V3: version_or_trim=null; body_type='SUV'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=238; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2015; year_end=2021; support_level='direct'; source_indexes=[1, 3]
- V4: version_or_trim=null; body_type='SUV'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=238; transmission='6-speed automatic'; drivetrain='AWD'; year_start=2015; year_end=2021; support_level='direct'; source_indexes=[1, 3]
- V5: version_or_trim=null; body_type='SUV'; fuel_type='hybrid'; engine='2.5L'; engine_displacement_l=2.5; horsepower_hp=244; transmission='cvt'; drivetrain='FWD'; year_start=2021; year_end=null; support_level='direct'; source_indexes=[2, 3]
- V6: version_or_trim=null; body_type='SUV'; fuel_type='hybrid'; engine='2.5L'; engine_displacement_l=2.5; horsepower_hp=244; transmission='cvt'; drivetrain='AWD'; year_start=2021; year_end=null; support_level='direct'; source_indexes=[2, 3]
- V7: version_or_trim=null; body_type='SUV'; fuel_type='plug_in_hybrid'; engine='2.5L'; engine_displacement_l=2.5; horsepower_hp=309; transmission='cvt'; drivetrain='AWD'; year_start=2021; year_end=null; support_level='direct'; source_indexes=[2, 3]

### IL-confirmed|Lexus|RC — model_years=2015..2021
- V1: version_or_trim='200t F-Sport'; body_type='Coupe'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=245; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2015; year_end=2018; support_level='direct'; source_indexes=[0, 1]
- V2: version_or_trim='300h F-Sport'; body_type='Coupe'; fuel_type='hybrid'; engine='2.5L inline-4'; engine_displacement_l=2.5; horsepower_hp=223; transmission='cvt'; drivetrain='RWD'; year_start=2019; year_end=2021; support_level='direct'; source_indexes=[0, 3]
- V3: version_or_trim='F'; body_type='Coupe'; fuel_type='petrol'; engine='5.0L v8'; engine_displacement_l=5.0; horsepower_hp=477; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2015; year_end=2021; support_level='direct'; source_indexes=[0, 2]

## RUN 3 required variant-level decisions

### MODEL: `IL-confirmed|Lexus|LS`

#### LS V1
CURRENT VALUE: `version_or_trim=null`; petrol 4.6L V8, 380 hp, 8-speed automatic, RWD, Sedan, 2006-2017.
PROBLEM: Technical fields are grounded, but `version_or_trim=null` hides the Israeli marketed variant family; Israeli sources present this generation as LS460/LS 460, not as a blank trim.
WEB-VALIDATED FACT: iCar has LS/LS460 2006-2017 pages and version listings for LS460 4.6 Luxury/Premium/F-Sport. The 4.6 V8 + 8-speed/RWD technical identity is consistent with the LS460 family.
SOURCE: iCar LS / LS460 pages listed above; repo source index 1024.
TARGET VALUE: Keep technical fields; set/normalize `version_or_trim` to `LS 460` unless the repo schema intentionally keeps model-designation variants outside the trim field. If separate trim aliases exist, preserve Luxury/Premium/F-Sport as aliases/available-values, not as duplicate technical variants.
ACTION: FIX / ALIAS-LINEAGE

#### LS V2
CURRENT VALUE: `version_or_trim=null`; hybrid 5.0L V8, 438 hp, CVT, AWD, Sedan, 2007-2017.
PROBLEM: Technical row is grounded, but null version loses the marketed LS600h/LS 600h identity.
WEB-VALIDATED FACT: iCar LS pages distinguish LS460 and LS600h families; the repo source grounds the 5.0L V8 hybrid 438 hp AWD configuration as the hybrid flagship of the 2006-2017 generation.
SOURCE: iCar LS / LS460 pages listed above; repo source index 1024.
TARGET VALUE: Keep technical fields; set/normalize `version_or_trim` to `LS 600h`. Do not create equipment-trim duplicates unless the schema has a non-technical trim-alias field.
ACTION: FIX / ALIAS-LINEAGE

#### LS V3
CURRENT VALUE: `version_or_trim=null`; petrol 3.5L V6 twin-turbo, 417 hp, 10-speed automatic, RWD, Sedan, 2018-2021.
PROBLEM: Null version hides LS500 identity. This is a historical petrol row, not the current 2026 official LS hybrid.
WEB-VALIDATED FACT: Cartube documents the 2018 LS launch in Israel; the official Lexus Israel current LS pages now show LS as hybrid/Multi-Stage Hybrid, so the petrol LS500 row should remain historical and should not be extended to current years without repo-local official evidence.
SOURCE: Cartube LS 2018 launch; Lexus Israel current LS page/prices pages listed above.
TARGET VALUE: Keep technical fields and `year_end=2021`; set/normalize `version_or_trim` to `LS 500`.
ACTION: FIX

#### LS V4
CURRENT VALUE: `version_or_trim=null`; hybrid 3.5L V6, 359 hp, 10-speed automatic, RWD, Sedan, 2018-2024.
PROBLEM: Current official Lexus Israel LS pages still show LS as an active new-car model, so `year_end=2024` is likely stale. Null version also loses LS500h identity.
WEB-VALIDATED FACT: Lexus Israel current LS page/prices page lists active LS Takumi / LS Takumi High Wood, Sedan 4 Doors (LWB), hybrid, Multi-Stage Hybrid | 4X2, with active 2026 website pricing. Therefore the clean catalog must not close the hybrid LS at 2024.
SOURCE: Lexus Israel LS page and LS prices/costs page.
TARGET VALUE: Set/normalize `version_or_trim` to `LS 500h` or `LS 500h Takumi` depending on repo naming convention; set `year_end=null` for current active model. Keep 3.5L V6 hybrid, 359 hp, RWD/4X2, 10-speed/multi-stage automatic unless repo-local official PDF gives a newer field value.
ACTION: FIX

### MODEL: `IL-confirmed|Lexus|LX`

#### LX V1
CURRENT VALUE: `version_or_trim=null`; petrol 5.7L V8, 367 hp, 6-speed automatic, 4WD, SUV, 2008-2015.
PROBLEM: Technical row is grounded, but null version hides LX570/LX 570 marketed identity.
WEB-VALIDATED FACT: Israeli used-car/catalog sources support LX historical rows; the 5.7L V8 + 6-speed pre-facelift technical identity corresponds to LX570.
SOURCE: iCar/Auto LX sources already in repo; Lexus LX history page confirms LX lineage, not exact early fields.
TARGET VALUE: Keep technical fields; set/normalize `version_or_trim` to `LX 570`. Keep `year_end=2015`.
ACTION: FIX / ALIAS-LINEAGE

#### LX V2
CURRENT VALUE: `version_or_trim=null`; petrol 5.7L V8, 367 hp, 8-speed automatic, 4WD, SUV, 2016-2021.
PROBLEM: Null version hides LX570 identity; this is the facelift/update technical row and must stay separate from the 6-speed row.
WEB-VALIDATED FACT: Israeli catalog/price sources distinguish later LX570 years; the change from 6-speed to 8-speed is a real technical split, so it should not be merged with V1.
SOURCE: iCar/Auto LX sources already in repo; Lexus LX history page confirms broader LX lineage.
TARGET VALUE: Keep technical fields; set/normalize `version_or_trim` to `LX 570`. Keep `year_start=2016`, `year_end=2021`.
ACTION: FIX / KEEP

#### LX V3
CURRENT VALUE: `version_or_trim=null`; petrol 3.5L twin-turbo V6, 409 hp, 10-speed automatic, 4WD, SUV, 2022-2026.
PROBLEM: Current row is probably valid as LX600, but source coverage must be made explicit and the null version must be fixed. Also avoid treating Lexus Israel history page as proof of active new-car listing; the Lexus current new-car menu does not clearly list LX, while Carzone/Yad2 show 2026 price-list rows.
WEB-VALIDATED FACT: Lexus Israel history page says LX600 was launched in Israel in 2022. Auto.co.il reports the LX600 landed in Israel in 2022. Cartube and Carzone list 2023/2024 LX600 technical/price rows, and Carzone/Yad2 show 2026 LX rows. However, 2026 support is Tier 3 unless repo-local official Lexus price list exists.
SOURCE: Lexus LX history page; Auto.co.il LX600 2022 launch; Cartube LX page; Carzone LX 2024/2026; Yad2 LX price list.
TARGET VALUE: Set/normalize `version_or_trim` to `LX 600`. Keep 3.5L/3.4L twin-turbo V6, 409 hp, 10-speed automatic, 4WD. Keep `year_start=2022`. Keep `year_end=2026` only if the catalog accepts Carzone/Yad2 Tier 3 current price-list support; otherwise cap at `year_end=2024` and add a non-blocking review note for 2025/2026 continuation. Do not add LX700h to clean from Tier 3 alone; add it only to non-blocking review candidate unless official Israeli evidence exists in repo.
ACTION: FIX / POSSIBLE MOVE-TO-REVIEW FOR 2026-CURRENT EDGE

### MODEL: `IL-confirmed|Lexus|NX`

#### NX V1
CURRENT VALUE: `version_or_trim=null`; hybrid 2.5L, 197 hp, CVT, FWD, SUV, 2014-2021.
PROBLEM: Null version hides NX300h identity.
WEB-VALIDATED FACT: Cartube documents the 2014 Israel launch with NX300h, and iCar documents the 2015-2021 NX generation with 2.5 hybrid alongside 2.0 turbo. The 197 hp outgoing hybrid is explicitly referenced in 2022 launch coverage as the previous-generation output.
SOURCE: Cartube NX 2014 launch; iCar NX 2015-2021; Cartube NX 2022 launch.
TARGET VALUE: Keep technical fields; set/normalize `version_or_trim` to `NX 300h`. Keep `year_end=2021`.
ACTION: FIX / KEEP

#### NX V2
CURRENT VALUE: `version_or_trim=null`; hybrid 2.5L, 197 hp, CVT, AWD, SUV, 2014-2021.
PROBLEM: Null version hides NX300h identity; AWD split is valid and must not be merged into FWD.
WEB-VALIDATED FACT: Cartube launch coverage and iCar used-car rows support NX300h with trim/drivetrain variants; AWD/Premium/F-Sport variants existed as separate marketed forms but this row is the correct technical AWD grouping.
SOURCE: Cartube NX 2014 launch; iCar NX 2015-2021.
TARGET VALUE: Keep technical fields; set/normalize `version_or_trim` to `NX 300h 4x4` or `NX 300h AWD` according to repo naming convention. Keep `year_end=2021`.
ACTION: FIX / KEEP

#### NX V3
CURRENT VALUE: `version_or_trim=null`; petrol 2.0L turbo, 238 hp, 6-speed automatic, FWD, SUV, 2015-2021.
PROBLEM: The technical engine is grounded, but the marketed name changed during the generation: early rows are NX200t; facelift rows are NX300. A single null-version row from 2015-2021 loses that lineage.
WEB-VALIDATED FACT: Cartube 2014/2015 launch uses NX200t for 2.0 turbo 238 hp. iCar and Cartube 2018 facelift sources list NX300 2.0 turbo 238 hp. The engine/transmission/drivetrain remain technically similar, but the marketed variant identity changed.
SOURCE: Cartube NX 2014 launch; iCar NX 2020 NX300 page; Cartube NX 2018 facelift; iCar NX 2015-2021.
TARGET VALUE: Split or rename with lineage. Preferred: split into `NX 200t` FWD for 2015-2017 and `NX 300` FWD for 2018-2021 if exact repo evidence supports FWD for both periods. If the repo does not support precise split, use `version_or_trim="NX 200t / NX 300"` with lineage note; do not leave null.
ACTION: FIX / SPLIT / ALIAS-LINEAGE

#### NX V4
CURRENT VALUE: `version_or_trim=null`; petrol 2.0L turbo, 238 hp, 6-speed automatic, AWD, SUV, 2015-2021.
PROBLEM: Same marketed-name lineage issue as V3; AWD technical split is valid.
WEB-VALIDATED FACT: iCar 2020 NX300 Premium 4x4 and Cartube 2018 facelift support NX300 2.0 turbo 238 hp 4x4, while earlier launch sources support NX200t Premium/F-Sport 4x4.
SOURCE: iCar NX 2020 NX300 Premium 4x4; Cartube NX 2018 facelift; Cartube NX 2014 launch.
TARGET VALUE: Preferred split into `NX 200t AWD` 2015-2017 and `NX 300 AWD` 2018-2021. If exact split cannot be implemented safely, use `version_or_trim="NX 200t / NX 300 AWD"` with lineage note. Do not leave null.
ACTION: FIX / SPLIT / ALIAS-LINEAGE

#### NX V5
CURRENT VALUE: `version_or_trim=null`; hybrid 2.5L, 244 hp, CVT, FWD, SUV, 2021-current.
PROBLEM: Null version hides current NX350h identity.
WEB-VALIDATED FACT: Lexus Israel current NX page presents NX 350h self-charging hybrid and NX 450h+ plug-in hybrid. Cartube 2022 launch states NX350h replaced NX300h and produces 244 hp, with FWD and AWD forms.
SOURCE: Lexus Israel NX current page/specifications/build; Cartube NX 2022 launch.
TARGET VALUE: Set/normalize `version_or_trim` to `NX 350h`. Keep 2.5L hybrid, 244 hp, CVT, FWD, `year_end=null`.
ACTION: FIX / KEEP

#### NX V6
CURRENT VALUE: `version_or_trim=null`; hybrid 2.5L, 244 hp, CVT, AWD, SUV, 2021-current.
PROBLEM: Null version hides current NX350h AWD identity.
WEB-VALIDATED FACT: Lexus Israel current NX page presents NX 350h, and Cartube 2022 launch explicitly supports 244 hp and AWD availability for the 350h.
SOURCE: Lexus Israel NX current page/specifications/build; Cartube NX 2022 launch.
TARGET VALUE: Set/normalize `version_or_trim` to `NX 350h AWD` or `NX 350h 4x4` according to repo convention. Keep `year_end=null`.
ACTION: FIX / KEEP

#### NX V7
CURRENT VALUE: `version_or_trim=null`; plug-in hybrid 2.5L, 309 hp, CVT, AWD, SUV, 2021-current.
PROBLEM: Null version hides current NX450h+ identity.
WEB-VALIDATED FACT: Lexus Israel current NX pages present the plug-in hybrid NX 450h+. Cartube 2022 launch states the NX450h+ PHEV uses a 2.5L petrol engine plus two electric motors, AWD, and 309 hp.
SOURCE: Lexus Israel NX current page/specifications/build; Cartube NX 2022 launch.
TARGET VALUE: Set/normalize `version_or_trim` to `NX 450h+`. Keep plug_in_hybrid fuel_type, 2.5L displacement, 309 hp, CVT, AWD, `year_end=null`.
ACTION: FIX / KEEP

### MODEL: `IL-confirmed|Lexus|RC`

#### RC V1
CURRENT VALUE: `version_or_trim='200t F-Sport'`; petrol 2.0L turbo, 245 hp, 8-speed automatic, RWD, Coupe, 2015-2018.
PROBLEM: Israeli iCar rows show both Luxury and F-Sport for RC 200t; storing only F-Sport can falsely imply the technical row excludes Luxury. Since Luxury and F-Sport share core technical data, do not create duplicate technical variants just to represent equipment trims.
WEB-VALIDATED FACT: iCar 2017 RC page lists 2.0 200t Luxury and 2.0 200t F-Sport variants. Cartube documents RC 200t launch in Israel. The 2.0 turbo 8-speed RWD technical identity is valid.
SOURCE: iCar RC 2017 200t F-Sport; Cartube RC 200t Israel launch.
TARGET VALUE: Preferred: set `version_or_trim` to `200t` and preserve `Luxury` / `F-Sport` in available trim aliases if schema supports it. If schema requires one label, use `200t F-Sport` only when repo-local sources prove F-Sport is the intended representative; otherwise add lineage note and avoid duplicate technical rows.
ACTION: FIX / ALIAS-LINEAGE

#### RC V2
CURRENT VALUE: `version_or_trim='300h F-Sport'`; hybrid 2.5L inline-4, 223 hp, CVT, RWD, Coupe, 2019-2021.
PROBLEM: Row appears technically valid, but the same trim-representation caution applies: do not duplicate identical technical rows solely for equipment levels unless schema expects trim-level granularity.
WEB-VALIDATED FACT: iCar and Cartube 2019 facelift sources support the RC 300h hybrid row for Israel. Existing year range 2019-2021 is consistent with a historical, not current, row.
SOURCE: iCar RC main page; Cartube RC 2019 facelift.
TARGET VALUE: Keep technical fields. Keep `version_or_trim='300h F-Sport'` if source-indexed to F-Sport; otherwise normalize to `300h` with F-Sport as alias/trim note. Keep `year_end=2021`.
ACTION: KEEP / POSSIBLE ALIAS-LINEAGE FIX

#### RC V3
CURRENT VALUE: `version_or_trim='F'`; petrol 5.0L V8, 477 hp, 8-speed automatic, RWD, Coupe, 2015-2021.
PROBLEM: Technical row is strongly grounded; only naming should be normalized to the marketed `RC F` identity if repo convention allows full marketed version names.
WEB-VALIDATED FACT: TheCar reports the RC F Israel launch in 2015, by Union Motors, with 5.0L V8, 477 hp, 8-speed automatic, RWD. iCar/price sources support later historical rows.
SOURCE: TheCar RC F Israel launch; iCar RC main page; Cartube RC F/RC 2019 sources.
TARGET VALUE: Keep technical fields; normalize `version_or_trim` from `F` to `RC F` or `F` according to repo convention, but ensure website output displays `RC F` clearly.
ACTION: KEEP / FIX DISPLAY-NAME

## RUN 3 implementation boundaries

- Apply only RUN 3 corrections.
- Do not touch FINAL blockers/review/unmatched yet, except if a RUN 3 correction directly creates or resolves a duplicate/split profile.
- Do not add LX700h to clean unless repo-local official Israeli evidence exists; Tier 3 price-list support alone should create a non-blocking review candidate, not a verified-clean variant.
- For RC and NX equipment-trim aliases, do not create duplicate technical variants if engine/transmission/drivetrain/body/fuel/year are identical and the only difference is equipment trim. Prefer aliases/lineage/available-values or a single normalized technical variant.
- For all current Lexus models, prefer `year_end=null` when an official Lexus Israel current new-car page supports the model/version; use a finite year when only historical/Tier 2/Tier 3 sources support it.

## Completion criteria for RUN 3

- All 17 RUN 3 variants have either KEEP/FIX/SPLIT/MOVE-TO-REVIEW decisions implemented or explicitly reported if repo-local evidence conflicts.
- No duplicate technical variants introduced.
- No source indexes left broken after source edits.
- Website available values regenerated for LS/LX/NX/RC.
- Readiness/review/archive/quality scan and cursor audited after this run.


---

# BATCH25 RESTART — FINAL RUN VARIANT-LEVEL CODEX TASK

## Non-negotiable execution rules

Do not browse the internet. All web-validation facts and target corrections are embedded in this task file. Use this task file as the single source of truth. Do not apply corrections that are not instructed here. If repo-local evidence conflicts with this task file, report it instead of guessing. If a variant cannot be grounded with the embedded facts or repo-local sources, move it to non-blocking archive/review rather than fabricating data.

This FINAL RUN covers blockers/review-only/unmatched/split aliases/casing/archive/reporting only. RUN 1, RUN 2, and RUN 3 have separate variant-level task files. Do not rework clean models outside FINAL scope except to prevent duplicate/split regressions caused by FINAL fixes.

## Actual ZIP audit baseline

```text
source cursor = 568/1124
resume_after_key = IL-confirmed|Lexus|RC
next_key_to_process = IL-confirmed|Lexus|RX
clean_models = 515
review_entries = 24
active_blocked = 24
unmatched_output_keys_count = 0
ready_for_website_upload = false
invalid_source_references = 12
unknown_support_values = 9
technical_variants_missing_required_grounding = 8
technical_variants_missing_grounded_fields = 24
quality_findings_total = 597
quality_counts_by_type = {'grounding_completeness': 438, 'year_split_duplicates': 36, 'source_tier_inversion': 116, 'source_domain': 7}
```

## FINAL RUN scope — 24/24 active blockers

1. `IL-confirmed|Jeep|Gladiator` — 1 current variants; issues: ['variant[0] has no source_indexes', 'variant[0] support_level=direct but no source directly supports it']
2. `IL-confirmed|KGM|Tivoli` — 1 current variants; issues: ['variant[0] has no source_indexes', 'variant[0] support_level=direct but no source directly supports it']
3. `IL-confirmed|Kia|Carens` — 0 current variants; issues: ['technical_variants_il is empty']
4. `IL-confirmed|Kia|EV9` — 3 current variants; issues: ["variant[0] required website field 'transmission' is null/empty", "variant[0] required field 'transmission' listed in missing_grounded_fields", "variant[1] required website field 'transmission' is null/empty", "variant[1] required field 'transmission' listed in missing_grounded_fields", "variant[2] required website field 'transmission' is null/empty", "variant[2] required field 'transmission' listed in missing_grounded_fields"]
5. `IL-confirmed|Kia|Mohave` — 2 current variants; issues: ["variant[1] required website field 'horsepower_hp' is null/empty", "variant[1] required website field 'transmission' is null/empty", "variant[1] required field 'horsepower_hp' listed in missing_grounded_fields", "variant[1] required field 'transmission' listed in missing_grounded_fields"]
6. `global-reference-only|Kia|Mohave` — 0 current variants; issues: ['technical_variants_il is empty']
7. `IL-confirmed|Kia|Niro` — 4 current variants; issues: ["variant[1] required website field 'drivetrain' is null/empty", "variant[1] required field 'drivetrain' listed in missing_grounded_fields", "variant[3] required website field 'drivetrain' is null/empty", "variant[3] required field 'drivetrain' listed in missing_grounded_fields"]
8. `IL-confirmed|Kia|Niro Plus` — 3 current variants; issues: ["variant[2] required website field 'transmission' is null/empty", "variant[2] required website field 'drivetrain' is null/empty", "variant[2] required field 'transmission' listed in missing_grounded_fields", "variant[2] required field 'drivetrain' listed in missing_grounded_fields"]
9. `IL-confirmed|Kia|Picanto` — 1 current variants; issues: ['variant[0] field_sources/source_indexes reference 12 unknown source(s)', "variant[0] required website field 'drivetrain' is null/empty", 'variant[1] is not an object']
10. `IL-confirmed|Kia|Pride` — 2 current variants; issues: ["variant[0] required website field 'drivetrain' is null/empty", "variant[0] required field 'drivetrain' listed in missing_grounded_fields", "variant[1] required website field 'drivetrain' is null/empty", "variant[1] required field 'drivetrain' listed in missing_grounded_fields"]
11. `IL-confirmed|Kia|ProCeed` — 3 current variants; issues: ["variant[0] non-null field 'fuel_type' has no field_sources entry", "variant[0] required website field 'transmission' is null/empty", "variant[0] required website field 'drivetrain' is null/empty", "variant[0] required field 'fuel_type' listed in missing_grounded_fields", "variant[0] required field 'transmission' listed in missing_grounded_fields", "variant[0] required field 'drivetrain' listed in missing_grounded_fields", "variant[1] required website field 'drivetrain' is null/empty", "variant[1] required field 'drivetrain' listed in missing_grounded_fields", "variant[2] required website field 'drivetrain' is null/empty", "variant[2] required field 'drivetrain' listed in missing_grounded_fields"]
12. `global-reference-only|Kia|ProCeed` — 2 current variants; issues: ["variant[0] non-null field 'fuel_type' has no field_sources entry", "variant[0] required website field 'horsepower_hp' is null/empty", "variant[0] required website field 'drivetrain' is null/empty", "variant[0] required field 'fuel_type' listed in missing_grounded_fields", "variant[0] required field 'horsepower_hp' listed in missing_grounded_fields", "variant[0] required field 'drivetrain' listed in missing_grounded_fields", "variant[1] required website field 'drivetrain' is null/empty", "variant[1] required field 'drivetrain' listed in missing_grounded_fields"]
13. `IL-confirmed|Kia|Rio` — 9 current variants; issues: ["variant[0] required website field 'horsepower_hp' is null/empty", "variant[0] required field 'horsepower_hp' listed in missing_grounded_fields", "variant[6] required website field 'horsepower_hp' is null/empty", "variant[6] required field 'horsepower_hp' listed in missing_grounded_fields"]
14. `IL-confirmed|Kia|Sephia` — 8 current variants; issues: ["variant[0] required website field 'drivetrain' is null/empty", "variant[0] required field 'drivetrain' listed in missing_grounded_fields", "variant[1] required website field 'drivetrain' is null/empty", "variant[1] required field 'drivetrain' listed in missing_grounded_fields", "variant[2] non-null field 'body_type' has no field_sources entry", "variant[2] required website field 'drivetrain' is null/empty", "variant[2] required field 'body_type' listed in missing_grounded_fields", "variant[2] required field 'drivetrain' listed in missing_grounded_fields", "variant[3] non-null field 'body_type' has no field_sources entry", "variant[3] required website field 'drivetrain' is null/empty", "variant[3] required field 'body_type' listed in missing_grounded_fields", "variant[3] required field 'drivetrain' listed in missing_grounded_fields", "variant[4] non-null field 'body_type' has no field_sources entry", "variant[4] required website field 'drivetrain' is null/empty", "variant[4] required field 'body_type' listed in missing_grounded_fields", "variant[4] required field 'drivetrain' listed in missing_grounded_fields", "variant[5] non-null field 'body_type' has no field_sources entry", "variant[5] non-null field 'fuel_type' has no field_sources entry", "variant[5] non-null field 'transmission' has no field_sources entry", "variant[5] required website field 'drivetrain' is null/empty", "variant[5] required field 'body_type' listed in missing_grounded_fields", "variant[5] required field 'fuel_type' listed in missing_grounded_fields", "variant[5] required field 'transmission' listed in missing_grounded_fields", "variant[5] required field 'drivetrain' listed in missing_grounded_fields", "variant[6] non-null field 'body_type' has no field_sources entry", "variant[6] required website field 'drivetrain' is null/empty", "variant[6] required field 'body_type' listed in missing_grounded_fields", "variant[6] required field 'drivetrain' listed in missing_grounded_fields", "variant[7] non-null field 'body_type' has no field_sources entry", "variant[7] required website field 'drivetrain' is null/empty", "variant[7] required field 'body_type' listed in missing_grounded_fields", "variant[7] required field 'drivetrain' listed in missing_grounded_fields"]
15. `IL-confirmed|Kia|XCeed` — 0 current variants; issues: ['technical_variants_il is empty']
16. `IL-confirmed|Lamborghini|Revuelto` — 0 current variants; issues: ['technical_variants_il is empty']
17. `IL-confirmed|Lancia|Dedra` — 0 current variants; issues: ['technical_variants_il is empty']
18. `IL-likely|Lancia|Delta` — 0 current variants; issues: ['technical_variants_il is empty']
19. `IL-confirmed|Lancia|Kappa` — 0 current variants; issues: ['technical_variants_il is empty']
20. `IL-likely|Lancia|Lybra` — 0 current variants; issues: ['technical_variants_il is empty']
21. `global-reference-only|Lancia|Musa` — 0 current variants; issues: ['technical_variants_il is empty']
22. `global-reference-only|Lancia|Phedra` — 0 current variants; issues: ['technical_variants_il is empty']
23. `global-reference-only|Lancia|Thema` — 2 current variants; issues: ['variant[0] has no source_indexes', 'variant[0] support_level=direct but no source directly supports it', 'variant[1] has no source_indexes', 'variant[1] support_level=direct but no source directly supports it']
24. `global-reference-only|Lexus|LX` — 0 current variants; issues: ['technical_variants_il is empty']

## Required commands

Run all before reporting PASS:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Also directly audit generated files, not only stdout:

- `data/model_technical_catalog_il.json`
- `data/model_technical_catalog_il_readiness.json`
- `data/model_technical_catalog_il_review.json`
- `data/model_technical_catalog_il_archive.json`
- `data/model_technical_catalog_il_quality_scan.json`
- `compute_resume_state()`
- unmatched output keys / split profile aliases
- active blockers / review-only blockers
- cursor / resume_after_key / next_key_to_process

If `pytest` fails only because `streamlit` is missing in the execution environment, report it as environment/dependency failure and still run all non-Streamlit tests possible. Do not mark full PASS unless dependency issue is fixed or CI environment has it installed.

## End-state targets

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
quality scan fresh = true
```

Cursor rules:
- Do not move cursor backward.
- Do not skip beyond this window.
- `resume_after_key` must stay `IL-confirmed|Lexus|RC` for this completed window unless repo-local source cursor computation proves a later key was actually processed.
- `next_key_to_process` should stay `IL-confirmed|Lexus|RX` unless repo-local cursor computation proves otherwise.
- Non-blocking archive entries may count as completed only if `non_blocking=true` and reason/lineage are valid.

## Current blocker snapshots from actual ZIP


### CURRENT SNAPSHOT 1: `IL-confirmed|Jeep|Gladiator`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Jeep",
  "model": "Gladiator",
  "canonical_model": "Gladiator",
  "year_start": 2020,
  "year_end": null,
  "profile_confidence": "medium",
  "validation_issues": [
    "variant[0] has no source_indexes",
    "variant[0] support_level=direct but no source directly supports it"
  ]
}
```

CURRENT SOURCES:
- [0] iCar | Jeep Gladiator Rubicon - iCar | https://www.icar.co.il/%D7%92'%D7%99%D7%A4/%D7%92'%D7%99%D7%A4_%D7%92%D7%9C%D7%93%D7%99%D7%90%D7%98%D7%95%D7%A8/ | supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'version_or_trim']
- [1] Cartube | ג'יפ גלדיאטור בישראל - מחיר החל מ- 419,000 שקלים | https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%92-%D7%99%D7%A4-%D7%92%D7%9C%D7%93%D7%99%D7%90%D7%98%D7%95%D7%A8-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-419000-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D | supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'version_or_trim']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "version_or_trim": "Rubicon",
    "body_type": "Pickup",
    "fuel_type": "petrol",
    "engine": "3.6L v6",
    "engine_displacement_l": 3.6,
    "horsepower_hp": 280,
    "transmission": "8-speed automatic",
    "drivetrain": "4WD",
    "year_start": 2020,
    "year_end": null,
    "support_level": "direct",
    "invalid_or_non_trim_labels": [],
    "missing_grounded_fields": [],
    "field_sources": {
      "version_or_trim": [
        0,
        1
      ],
      "body_type": [
        0,
        1
      ],
      "fuel_type": [
        0,
        1
      ],
      "engine": [
        0,
        1
      ],
      "engine_displacement_l": [
        0,
        1
      ],
      "horsepower_hp": [
        0,
        1
      ],
      "transmission": [
        0,
        1
      ],
      "drivetrain": [
        0,
        1
      ],
      "year_start": [
        0,
        1
      ],
      "year_end": []
    }
  }
]
```


### CURRENT SNAPSHOT 2: `IL-confirmed|KGM|Tivoli`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "KGM",
  "model": "Tivoli",
  "canonical_model": "Tivoli",
  "year_start": 2024,
  "year_end": null,
  "profile_confidence": "medium",
  "validation_issues": [
    "variant[0] has no source_indexes",
    "variant[0] support_level=direct but no source directly supports it"
  ]
}
```

CURRENT SOURCES:
- [0] Cartube | 2024 ק.ג.מ (סאנגיונג) טיבולי החדש בישראל | https://www.cartube.co.il/חדשות-רכב/2024-ק-ג-מ-סאנגיונג-טיבולי-החדש-בישראל-מחיר-החל-מ-138900-שקל | supports=['year_start', 'make', 'model', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'body_type', 'fuel_type']
- [1] iCar | KGM טיבולי - מפרט טכני | https://www.icar.co.il/KGM/KGM_%D7%98%D7%99%D7%91%D7%95%D7%9C%D7%99/ | supports=['year_start', 'make', 'model', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'body_type', 'fuel_type']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "version_or_trim": null,
    "body_type": "Crossover",
    "fuel_type": "petrol",
    "engine": "1.5L turbo",
    "engine_displacement_l": 1.5,
    "horsepower_hp": 163,
    "transmission": "6-speed automatic",
    "drivetrain": "FWD",
    "year_start": 2024,
    "year_end": null,
    "support_level": "direct",
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        0,
        1
      ],
      "fuel_type": [
        0,
        1
      ],
      "engine": [
        0,
        1
      ],
      "engine_displacement_l": [
        0,
        1
      ],
      "horsepower_hp": [
        0,
        1
      ],
      "transmission": [
        0,
        1
      ],
      "drivetrain": [
        0,
        1
      ],
      "year_start": [
        0,
        1
      ],
      "year_end": []
    },
    "missing_grounded_fields": []
  }
]
```


### CURRENT SNAPSHOT 3: `IL-confirmed|Kia|Carens`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Kia",
  "model": "Carens",
  "canonical_model": "Carens",
  "year_start": null,
  "year_end": null,
  "profile_confidence": null,
  "validation_issues": [
    "technical_variants_il is empty"
  ],
  "error": "Gemini catalog client returned non-object JSON"
}
```

CURRENT SOURCES:
- none in current review profile

CURRENT VARIANTS / RAW PAYLOAD:
```json
{
  "years_seen": [
    2000,
    2006,
    2007,
    2012,
    2013,
    2016,
    2019
  ],
  "trims_seen": [],
  "engines_seen": [
    "1.7L CRDi Diesel (141 hp)",
    "1.8L Petrol",
    "2.0L CRDi (140 hp)",
    "2.0L GDI Petrol (166 hp)",
    "2.0L Petrol (144 hp)"
  ],
  "horsepower_seen": [],
  "transmissions_seen": [
    "4-speed automatic",
    "6-speed automatic",
    "7-speed DCT"
  ],
  "body_types_seen": [
    "MPV"
  ],
  "fuel_types_seen": [
    "Diesel",
    "Petrol"
  ],
  "drivetrains_seen": [
    "FWD"
  ]
}
```


### CURRENT SNAPSHOT 4: `IL-confirmed|Kia|EV9`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Kia",
  "model": "EV9",
  "canonical_model": "EV9",
  "year_start": 2024,
  "year_end": null,
  "profile_confidence": "medium",
  "validation_issues": [
    "variant[0] required website field 'transmission' is null/empty",
    "variant[0] required field 'transmission' listed in missing_grounded_fields",
    "variant[1] required website field 'transmission' is null/empty",
    "variant[1] required field 'transmission' listed in missing_grounded_fields",
    "variant[2] required website field 'transmission' is null/empty",
    "variant[2] required field 'transmission' listed in missing_grounded_fields"
  ]
}
```

CURRENT SOURCES:
- [0] Kia Israel | השקה: קיה EV9 החשמלית עם 7 המקומות בישראל – החל מ-429 אלף ש"ח | https://kia-israel.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA/%D7%94%D7%A9%D7%A7%D7%94-%D7%A7%D7%99%D7%94-ev9-%D7%94%D7%97%D7%A9%D7%9E%D7%9C%D7%99%D7%AA-%D7%A2%D7%9D-7-%D7%94%D7%9E%D7%A7%D7%95%D7%9E%D7%95%D7%AA-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C | supports=['version_or_trim', 'fuel_type', 'engine', 'horsepower_hp', 'drivetrain']
- [1] iCar | קיה EV9 - אתר iCar | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_EV9/%D7%A7%D7%99%D7%94_EV9_%D7%97%D7%93%D7%A9/ | supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'horsepower_hp', 'drivetrain', 'year_start']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "version_or_trim": "Executive",
    "body_type": "SUV",
    "fuel_type": "electric",
    "engine": "electric",
    "engine_displacement_l": null,
    "horsepower_hp": 203,
    "transmission": null,
    "drivetrain": "RWD",
    "year_start": 2024,
    "year_end": null,
    "support_level": "unknown",
    "source_indexes": [
      0,
      1
    ],
    "field_sources": {
      "version_or_trim": [
        1
      ],
      "body_type": [
        1
      ],
      "fuel_type": [
        0,
        1
      ],
      "engine": [
        0,
        1
      ],
      "engine_displacement_l": [],
      "horsepower_hp": [
        0,
        1
      ],
      "transmission": [],
      "drivetrain": [
        0,
        1
      ],
      "year_start": [
        1
      ],
      "year_end": []
    },
    "missing_grounded_fields": [
      "transmission"
    ]
  },
  {
    "version_or_trim": "Premium",
    "body_type": "SUV",
    "fuel_type": "electric",
    "engine": "electric",
    "engine_displacement_l": null,
    "horsepower_hp": 384,
    "transmission": null,
    "drivetrain": "AWD",
    "year_start": 2024,
    "year_end": null,
    "support_level": "unknown",
    "source_indexes": [
      0,
      1
    ],
    "field_sources": {
      "version_or_trim": [
        0,
        1
      ],
      "body_type": [
        1
      ],
      "fuel_type": [
        0,
        1
      ],
      "engine": [
        0,
        1
      ],
      "engine_displacement_l": [],
      "horsepower_hp": [
        0,
        1
      ],
      "transmission": [],
      "drivetrain": [
        0,
        1
      ],
      "year_start": [
        1
      ],
      "year_end": []
    },
    "missing_grounded_fields": [
      "transmission"
    ]
  },
  {
    "version_or_trim": "GT-Line",
    "body_type": "SUV",
    "fuel_type": "electric",
    "engine": "electric",
    "engine_displacement_l": null,
    "horsepower_hp": 384,
    "transmission": null,
    "drivetrain": "AWD",
    "year_start": 2024,
    "year_end": null,
    "support_level": "unknown",
    "source_indexes": [
      0,
      1
    ],
    "field_sources": {
      "version_or_trim": [
        0,
        1
      ],
      "body_type": [
        1
      ],
      "fuel_type": [
        0,
        1
      ],
      "engine": [
        0,
        1
      ],
      "engine_displacement_l": [],
      "horsepower_hp": [
        0,
        1
      ],
      "transmission": [],
      "drivetrain": [
        0,
        1
      ],
      "year_start": [
        1
      ],
      "year_end": []
    },
    "missing_grounded_fields": [
      "transmission"
    ]
  }
]
```


### CURRENT SNAPSHOT 5: `IL-confirmed|Kia|Mohave`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Kia",
  "model": "Mohave",
  "canonical_model": "Mohave",
  "year_start": 2009,
  "year_end": 2011,
  "profile_confidence": "low",
  "validation_issues": [
    "variant[1] required website field 'horsepower_hp' is null/empty",
    "variant[1] required website field 'transmission' is null/empty",
    "variant[1] required field 'horsepower_hp' listed in missing_grounded_fields",
    "variant[1] required field 'transmission' listed in missing_grounded_fields"
  ]
}
```

CURRENT SOURCES:
- [0] Autoboom Israel | קיה מוהאבי בישראל 2014 - אוטובום | https://autoboom.co.il/en/catalog/cars/kia/mohave/2014 | supports=['body_type', 'year_start', 'year_end']
- [1] Autoboom Israel | Kia Mohave 2019 - diesel, gasoline - AUTOBOOM | https://autoboom.co.il/en/catalog/cars/kia/mohave/2019 | supports=['fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp']
- [2] Autoboom Israel | Kia Mohave in Israel in Israel – Review, Prices, Comparisons and Rating on Autoboom | https://autoboom.co.il/en/catalog/cars/kia/mohave/2014 | supports=['fuel_type', 'engine', 'engine_displacement_l', 'transmission', 'drivetrain']
- [3] Wikipedia (Portuguese) | Kia Borrego | https://pt.wikipedia.org/wiki/Kia_Borrego | supports=['fuel_type', 'engine', 'engine_displacement_l', 'drivetrain']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "version_or_trim": null,
    "body_type": "SUV",
    "fuel_type": "diesel",
    "engine": "3.0L turbo v6",
    "engine_displacement_l": 3.0,
    "horsepower_hp": 250.0,
    "transmission": "automatic",
    "drivetrain": "4WD",
    "year_start": 2009,
    "year_end": 2011,
    "support_level": "direct",
    "source_indexes": [
      0,
      1,
      2
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        0
      ],
      "fuel_type": [
        1,
        2
      ],
      "engine": [
        1,
        2
      ],
      "engine_displacement_l": [
        1,
        2
      ],
      "horsepower_hp": [
        1
      ],
      "transmission": [
        2
      ],
      "drivetrain": [
        2
      ],
      "year_start": [
        0
      ],
      "year_end": [
        0
      ]
    },
    "missing_grounded_fields": []
  },
  {
    "version_or_trim": null,
    "body_type": "SUV",
    "fuel_type": "petrol",
    "engine": "3.8L v6",
    "engine_displacement_l": 3.8,
    "horsepower_hp": null,
    "transmission": null,
    "drivetrain": "4WD",
    "year_start": 2009,
    "year_end": 2011,
    "support_level": "indirect",
    "source_indexes": [
      0,
      3
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        0
      ],
      "fuel_type": [
        3
      ],
      "engine": [
        3
      ],
      "engine_displacement_l": [
        3
      ],
      "horsepower_hp": [],
      "transmission": [],
      "drivetrain": [
        3
      ],
      "year_start": [
        0
      ],
      "year_end": [
        0
      ]
    },
    "missing_grounded_fields": [
      "horsepower_hp",
      "transmission"
    ]
  }
]
```


### CURRENT SNAPSHOT 6: `global-reference-only|Kia|Mohave`

CURRENT VALUE:
```json
{
  "market": "global-reference-only",
  "make": "Kia",
  "model": "Mohave",
  "canonical_model": "Mohave",
  "year_start": null,
  "year_end": null,
  "profile_confidence": "high",
  "validation_issues": [
    "technical_variants_il is empty"
  ]
}
```

CURRENT SOURCES:
- [0] Kia Israel | קיה ישראל - כל דגמי קיה | KIA ISRAEL | https://kia-israel.co.il/ | supports=['model_not_listed_current_range']
- [1] Kia Israel | אמות מידה למרכז שירות | https://kia-israel.co.il/wp-content/uploads/2019/09/%D7%90%D7%9E%D7%95%D7%AA_%D7%9E%D7%99%D7%93%D7%94_%D7%A7%D7%99%D7%94_08.2019-1.pdf | supports=['model_name_only']
- [2] auto.co.il | קיה מוהאבי חוזר ומביא חבר | https://www.auto.co.il/articles/car-news/world-news/131979/ | supports=['not_confirmed_for_israel_2019']
- [3] auto.co.il | עוד פנאי ענקי: קיה מוהאבי | https://www.auto.co.il/articles/car-news/world-news/132563/ | supports=['not_expected_in_israel']
- [4] cartube.co.il | קיה מוהאבי החדש נחשף במלוא הדרו | https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%A7%D7%99%D7%94-%D7%9E%D7%95%D7%94%D7%90%D7%91%D7%99-%D7%94%D7%97%D7%93%D7%A9-%D7%A0%D7%97%D7%A9%D7%A3-%D7%91%D7%9E%D7%9C%D7%95%D7%90-%D7%94%D7%93%D7%A8%D7%95 | supports=['not_clear_if_marketed_outside_korea']
- [5] cartube.co.il | קרוסאובר עירוני חדש וזול לקיה: גרסת ייצור בהמשך 2019 | https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%A7%D7%99%D7%94-%D7%97%D7%95%D7%A9%D7%A4%D7%AA-%D7%A7%D7%A8%D7%95%D7%A1%D7%90%D7%95%D7%91%D7%A8-%D7%A2%D7%99%D7%A8%D7%95%D7%A0%D7%99-%D7%97%D7%93%D7%A9-%D7%95%D7%A8%D7%9B%D7%91-%D7%A4%D7%A0%D7%90%D7%99-%D7%92%D7%93%D7%95%D7%9C-2019 | supports=['not_sold_in_israel_context']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[]
```


### CURRENT SNAPSHOT 7: `IL-confirmed|Kia|Niro`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Kia",
  "model": "Niro",
  "canonical_model": "Niro",
  "year_start": 2016,
  "year_end": 2026,
  "profile_confidence": "medium",
  "validation_issues": [
    "variant[1] required website field 'drivetrain' is null/empty",
    "variant[1] required field 'drivetrain' listed in missing_grounded_fields",
    "variant[3] required website field 'drivetrain' is null/empty",
    "variant[3] required field 'drivetrain' listed in missing_grounded_fields"
  ]
}
```

CURRENT SOURCES:
- [0] autocom | ארכיון נירו - autocom | https://www.autocom.co.il/brands/%D7%A0%D7%99%D7%A8%D7%95/ | supports=['fuel_type', 'year_start', 'year_end']
- [1] Kia Israel | The new Niro Hybrid crossover | https://kia-israel.co.il/wp-content/uploads/2018/05/%D7%9E%D7%A4%D7%A8%D7%98-%D7%98%D7%9B%D7%A0%D7%99-%D7%A0%D7%99%D7%A8%D7%95-%D7%A0%D7%92%D7%99%D7%A9.pdf | supports=['engine', 'engine_displacement_l', 'horsepower_hp', 'transmission']
- [2] Kia Israel | The new Niro Hybrid crossover | https://kia-israel.co.il/wp-content/uploads/2018/05/%D7%9E%D7%A4%D7%A8%D7%98-%D7%98%D7%9B%D7%A0%D7%99-%D7%A0%D7%99%D7%A8%D7%95-%D7%A0%D7%92%D7%99%D7%A9.pdf | supports=['body_type', 'drivetrain']
- [3] Kia Israel | KIA*9920 :לפרטיםמערכות הבטיחות הינם אמצעי עזר וסיוע בלבד, הפעולות תחת תנאים ומגבלות שונים והן אינן מהוות תחליף לשמירה על כללי הנהיגה, זהירות ולהערנות | https://kia-israel.co.il/catalog/mifrat_niro-hybrid.pdf | supports=['fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start']
- [4] Kia Israel | קיה נירו 2026 - NIRO - קיה ישראל | Kia Israel | https://kia-israel.co.il/%D7%A8%D7%9B%D7%91/%D7%A0%D7%99%D7%A8%D7%95-%D7%94%D7%97%D7%93%D7%A9 | supports=['body_type', 'year_end']
- [5] Kia Israel | www.kia.com | https://kia-israel.co.il/catalog/mifrat-niro-plugin.pdf | supports=['body_type', 'fuel_type', 'drivetrain', 'year_start', 'year_end']
- [6] Kia Israel | www.kia.com | https://kia-israel.co.il/catalog/mifrat-niro-plugin.pdf | supports=['engine', 'engine_displacement_l', 'horsepower_hp']
- [7] Kia Israel | www.kia.com | https://kia-israel.co.il/catalog/mifrat-niro-plugin.pdf | supports=['transmission']
- [8] autocom | ארכיון נירו - autocom | https://www.autocom.co.il/brands/%D7%A0%D7%99%D7%A8%D7%95/ | supports=['year_start']
- [9] Kia Israel | KIAniro Hybrid. Plug-in. Electric.www.kia.com*9920 | https://kia-israel.co.il/catalog/NiroEV.pdf | supports=['body_type', 'fuel_type', 'engine', 'horsepower_hp']
- [10] autocom | קיה נירו EV 2024 - autocom | https://www.autocom.co.il/%D7%A7%D7%99%D7%94-%D7%A0%D7%99%D7%A8%D7%95-ev-2024/ | supports=['body_type', 'engine', 'horsepower_hp', 'transmission', 'year_end']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "version_or_trim": null,
    "body_type": "Crossover",
    "fuel_type": "hybrid",
    "engine": "1.6L",
    "engine_displacement_l": 1.6,
    "horsepower_hp": 141,
    "transmission": "6-speed dual_clutch",
    "drivetrain": "FWD",
    "year_start": 2016,
    "year_end": 2019,
    "support_level": "direct",
    "source_indexes": [
      0,
      1,
      2
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        2
      ],
      "fuel_type": [
        0
      ],
      "engine": [
        0,
        1
      ],
      "engine_displacement_l": [
        0,
        1
      ],
      "horsepower_hp": [
        1
      ],
      "transmission": [
        1
      ],
      "drivetrain": [
        2
      ],
      "year_start": [
        0
      ],
      "year_end": [
        0
      ]
    },
    "missing_grounded_fields": []
  },
  {
    "version_or_trim": null,
    "body_type": "Crossover",
    "fuel_type": "hybrid",
    "engine": "1.6L gdi",
    "engine_displacement_l": 1.6,
    "horsepower_hp": 129,
    "transmission": "6-speed dual_clutch",
    "drivetrain": null,
    "year_start": 2025,
    "year_end": 2026,
    "support_level": "direct",
    "source_indexes": [
      3,
      4
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        4
      ],
      "fuel_type": [
        3
      ],
      "engine": [
        3
      ],
      "engine_displacement_l": [
        3
      ],
      "horsepower_hp": [
        3
      ],
      "transmission": [
        3
      ],
      "drivetrain": [],
      "year_start": [
        3
      ],
      "year_end": [
        4
      ]
    },
    "missing_grounded_fields": [
      "drivetrain"
    ]
  },
  {
    "version_or_trim": null,
    "body_type": "Crossover",
    "fuel_type": "plug_in_hybrid",
    "engine": "1.6L gdi",
    "engine_displacement_l": 1.6,
    "horsepower_hp": 141,
    "transmission": "6-speed dual_clutch",
    "drivetrain": "FWD",
    "year_start": 2020,
    "year_end": 2023,
    "support_level": "direct",
    "source_indexes": [
      5,
      6,
      7
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        5
      ],
      "fuel_type": [
        5
      ],
      "engine": [
        6
      ],
      "engine_displacement_l": [
        6
      ],
      "horsepower_hp": [
        6
      ],
      "transmission": [
        7
      ],
      "drivetrain": [
        5
      ],
      "year_start": [
        5
      ],
      "year_end": [
        5
      ]
    },
    "missing_grounded_fields": []
  },
  {
    "version_or_trim": null,
    "body_type": "Crossover",
    "fuel_type": "electric",
    "engine": "electric",
    "engine_displacement_l": null,
    "horsepower_hp": 204,
    "transmission": "single_speed",
    "drivetrain": null,
    "year_start": 2021,
    "year_end": 2024,
    "support_level": "direct",
    "source_indexes": [
      8,
      9,
      10
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        8,
        10
      ],
      "fuel_type": [
        9
      ],
      "engine": [
        9,
        10
      ],
      "engine_displacement_l": [],
      "horsepower_hp": [
        9,
        10
      ],
      "transmission": [
        10
      ],
      "drivetrain": [],
      "year_start": [
        8
      ],
      "year_end": [
        10
      ]
    },
    "missing_grounded_fields": [
      "drivetrain"
    ]
  }
]
```


### CURRENT SNAPSHOT 8: `IL-confirmed|Kia|Niro Plus`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Kia",
  "model": "Niro Plus",
  "canonical_model": "Niro Plus",
  "year_start": 2022,
  "year_end": 2025,
  "profile_confidence": "medium",
  "validation_issues": [
    "variant[2] required website field 'transmission' is null/empty",
    "variant[2] required website field 'drivetrain' is null/empty",
    "variant[2] required field 'transmission' listed in missing_grounded_fields",
    "variant[2] required field 'drivetrain' listed in missing_grounded_fields"
  ]
}
```

CURRENT SOURCES:
- [0] Kia Israel | Kia Niro Plus Plug-in Hybrid Crossover specification PDF | https://kia-israel.co.il/catalog/mifrat-niro-plugin.pdf | supports=['version_or_trim', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission']
- [1] Kia Israel | Kia Niro Plus EV specification PDF | https://kia-israel.co.il/catalog/mifrat-niro-plus.pdf | supports=['fuel_type']
- [2] Kia Israel | Niro Plus HEV/PHEV owner manual PDF | https://cdnmedia.kia-israel.co.il/www/cars-book/Niro-Plus-HEV-PHEV-OM-2022.pdf | supports=['engine_displacement_l', 'horsepower_hp', 'drivetrain', 'transmission']
- [3] Auto | קיה נירו פלוס - מבחן דרכים (חשמלי) | https://www.auto.co.il/articles/test-drives/road-tests/135875/ | supports=['horsepower_hp']
- [4] Auto | קיה נירו פלוס - אוטו | https://www.auto.co.il/cars/kia/niro-plus/ | supports=['year_end', 'horsepower_hp', 'engine']
- [5] Auto | קיה נירו פלוס 2022 יד שניה - אוטו | https://www.auto.co.il/cars/kia/niro-plus/2022/ | supports=['version_or_trim', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain']
- [6] Auto | קיה נירו פלוס 2023 יד שניה - אוטו | https://www.auto.co.il/cars/kia/niro-plus/2023/ | supports=['body_type', 'year_start', 'year_end', 'horsepower_hp', 'transmission']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "version_or_trim": "GX",
    "body_type": "Crossover",
    "fuel_type": "hybrid",
    "engine": "1.6L",
    "engine_displacement_l": 1.6,
    "horsepower_hp": 141,
    "transmission": "6-speed dual_clutch",
    "drivetrain": "FWD",
    "year_start": 2022,
    "year_end": 2024,
    "support_level": "direct",
    "source_indexes": [
      2,
      5,
      6
    ],
    "field_sources": {
      "version_or_trim": [
        5
      ],
      "body_type": [
        6
      ],
      "fuel_type": [
        5
      ],
      "engine": [
        5
      ],
      "engine_displacement_l": [
        5
      ],
      "horsepower_hp": [
        5
      ],
      "transmission": [
        5
      ],
      "drivetrain": [
        5
      ],
      "year_start": [
        6
      ],
      "year_end": [
        6
      ]
    },
    "missing_grounded_fields": []
  },
  {
    "version_or_trim": "LX/EX",
    "body_type": "Crossover",
    "fuel_type": "plug_in_hybrid",
    "engine": "1.6L",
    "engine_displacement_l": 1.6,
    "horsepower_hp": 141,
    "transmission": "6-speed dual_clutch",
    "drivetrain": "FWD",
    "year_start": 2022,
    "year_end": 2024,
    "support_level": "direct",
    "source_indexes": [
      0,
      2,
      5,
      6
    ],
    "field_sources": {
      "version_or_trim": [
        0,
        5
      ],
      "body_type": [
        6
      ],
      "fuel_type": [
        0,
        5
      ],
      "engine": [
        0,
        2
      ],
      "engine_displacement_l": [
        0,
        2
      ],
      "horsepower_hp": [
        0,
        2,
        5
      ],
      "transmission": [
        0,
        2,
        5
      ],
      "drivetrain": [
        2,
        5
      ],
      "year_start": [
        6
      ],
      "year_end": [
        6
      ]
    },
    "missing_grounded_fields": []
  },
  {
    "version_or_trim": "EX",
    "body_type": "Crossover",
    "fuel_type": "electric",
    "engine": "electric",
    "engine_displacement_l": null,
    "horsepower_hp": 204,
    "transmission": null,
    "drivetrain": null,
    "year_start": 2022,
    "year_end": 2025,
    "support_level": "unknown",
    "source_indexes": [
      1,
      3,
      4,
      6
    ],
    "field_sources": {
      "version_or_trim": [
        5
      ],
      "body_type": [
        6
      ],
      "fuel_type": [
        1
      ],
      "engine": [
        4
      ],
      "engine_displacement_l": [],
      "horsepower_hp": [
        3,
        5
      ],
      "transmission": [],
      "drivetrain": [],
      "year_start": [
        6
      ],
      "year_end": [
        4
      ]
    },
    "missing_grounded_fields": [
      "transmission",
      "drivetrain"
    ]
  }
]
```


### CURRENT SNAPSHOT 9: `IL-confirmed|Kia|Picanto`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Kia",
  "model": "Picanto",
  "canonical_model": "Picanto",
  "year_start": 2011,
  "year_end": 2016,
  "profile_confidence": "medium",
  "validation_issues": [
    "variant[0] field_sources/source_indexes reference 12 unknown source(s)",
    "variant[0] required website field 'drivetrain' is null/empty",
    "variant[1] is not an object"
  ]
}
```

CURRENT SOURCES:
- none in current review profile

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "version_or_trim": "EX",
    "body_type": "Hatchback",
    "fuel_type": "petrol",
    "engine": "1.25L",
    "engine_displacement_l": 1.25,
    "horsepower_hp": 85,
    "transmission": "automatic",
    "drivetrain": null,
    "year_start": 2011,
    "year_end": 2016,
    "support_level": "direct",
    "source_indexes": [
      0,
      1
    ],
    "field_sources": {
      "version_or_trim": [
        1
      ],
      "body_type": [
        0,
        1
      ],
      "fuel_type": [
        0
      ],
      "engine": [
        0
      ],
      "engine_displacement_l": [
        0
      ],
      "horsepower_hp": [
        0
      ],
      "transmission": [
        0
      ],
      "drivetrain": [],
      "year_start": [
        1
      ],
      "year_end": [
        0
      ]
    },
    "missing_grounded_fields": []
  }
]
```


### CURRENT SNAPSHOT 10: `IL-confirmed|Kia|Pride`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Kia",
  "model": "Pride",
  "canonical_model": "Pride",
  "year_start": 1996,
  "year_end": 2000,
  "profile_confidence": "medium",
  "validation_issues": [
    "variant[0] required website field 'drivetrain' is null/empty",
    "variant[0] required field 'drivetrain' listed in missing_grounded_fields",
    "variant[1] required website field 'drivetrain' is null/empty",
    "variant[1] required field 'drivetrain' listed in missing_grounded_fields"
  ]
}
```

CURRENT SOURCES:
- [0] Wheel | נוסטלגיה לשבת: קיה פרייד (קאיה פרייד ליתר דיוק, באותם ימים...) | https://wheel.co.il/%D7%A0%D7%95%D7%A1%D7%98%D7%9C%D7%92%D7%99%D7%94-%D7%9C%D7%A9%D7%91%D7%AA-%D7%A7%D7%99%D7%94-%D7%A4%D7%A8%D7%99%D7%99%D7%93-%D7%A7%D7%90%D7%99%D7%94-%D7%A4%D7%A8%D7%99%D7%99%D7%93-%D7%9C%D7%99%D7%AA/ | supports=['engine', 'engine_displacement_l', 'horsepower_hp', 'transmission']
- [1] Yad2 | קיה פרייד 1997 DLX אוט׳ 1.3 (75 כ״ס) | מחירון יד2 | https://www.yad2.co.il/price-list/sub-model/110440/1997 | supports=['version_or_trim', 'body_type', 'fuel_type', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start']
- [2] Yad2 | מחירון רכבים קטנים של קיה | מחירון יד2 | https://www.yad2.co.il/price-list/feed?carFamilyType=1&manufacturer=48&page=3 | supports=['version_or_trim', 'fuel_type', 'horsepower_hp', 'transmission', 'year_end']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "version_or_trim": "DLX",
    "body_type": "Hatchback",
    "fuel_type": "petrol",
    "engine": "1.3L",
    "engine_displacement_l": 1.3,
    "horsepower_hp": 75,
    "transmission": "5-speed manual",
    "drivetrain": null,
    "year_start": 1996,
    "year_end": 1998,
    "support_level": "direct",
    "source_indexes": [
      0,
      1
    ],
    "field_sources": {
      "version_or_trim": [
        1
      ],
      "body_type": [
        1
      ],
      "fuel_type": [
        1
      ],
      "engine": [
        1
      ],
      "engine_displacement_l": [
        1
      ],
      "horsepower_hp": [
        1
      ],
      "transmission": [
        0,
        1
      ],
      "drivetrain": [],
      "year_start": [
        1
      ],
      "year_end": [
        1
      ]
    },
    "missing_grounded_fields": [
      "drivetrain"
    ]
  },
  {
    "version_or_trim": "DLX",
    "body_type": "Hatchback",
    "fuel_type": "petrol",
    "engine": "1.3L",
    "engine_displacement_l": 1.3,
    "horsepower_hp": 75,
    "transmission": "automatic",
    "drivetrain": null,
    "year_start": 1996,
    "year_end": 2000,
    "support_level": "direct",
    "source_indexes": [
      0,
      1,
      2
    ],
    "field_sources": {
      "version_or_trim": [
        1,
        2
      ],
      "body_type": [
        1
      ],
      "fuel_type": [
        1,
        2
      ],
      "engine": [
        1
      ],
      "engine_displacement_l": [
        1
      ],
      "horsepower_hp": [
        1,
        2
      ],
      "transmission": [
        0,
        1,
        2
      ],
      "drivetrain": [],
      "year_start": [
        1
      ],
      "year_end": [
        2
      ]
    },
    "missing_grounded_fields": [
      "drivetrain"
    ]
  }
]
```


### CURRENT SNAPSHOT 11: `IL-confirmed|Kia|ProCeed`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Kia",
  "model": "ProCeed",
  "canonical_model": "ProCeed",
  "year_start": 2008,
  "year_end": 2019,
  "profile_confidence": "medium",
  "validation_issues": [
    "variant[0] non-null field 'fuel_type' has no field_sources entry",
    "variant[0] required website field 'transmission' is null/empty",
    "variant[0] required website field 'drivetrain' is null/empty",
    "variant[0] required field 'fuel_type' listed in missing_grounded_fields",
    "variant[0] required field 'transmission' listed in missing_grounded_fields",
    "variant[0] required field 'drivetrain' listed in missing_grounded_fields",
    "variant[1] required website field 'drivetrain' is null/empty",
    "variant[1] required field 'drivetrain' listed in missing_grounded_fields",
    "variant[2] required website field 'drivetrain' is null/empty",
    "variant[2] required field 'drivetrain' listed in missing_grounded_fields"
  ]
}
```

CURRENT SOURCES:
- [0] auto.co.il | קיה פרו-סיד; קוסמת | https://www.auto.co.il/articles/test-drives/120550/ | supports=['body_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'year_start', 'year_end']
- [1] iCar | קיה פרוסיד יד שניה - iCar | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_%D7%A4%D7%A8%D7%95%D7%A1%D7%99%D7%93/%D7%A7%D7%99%D7%94_%D7%A4%D7%A8%D7%95%D7%A1%D7%99%D7%93_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9311/ | supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'year_start', 'year_end']
- [2] iCar | מבחני רכב - קיה פרוסיד - מבחן רכב | https://www.icar.co.il/%D7%9E%D7%91%D7%97%D7%A0%D7%99_%D7%A8%D7%9B%D7%91/%D7%A7%D7%99%D7%94_%D7%A4%D7%A8%D7%95%D7%A1%D7%99%D7%93_-_%D7%9E%D7%91%D7%97%D7%9F_%D7%A8%D7%9B%D7%91/ | supports=['engine', 'engine_displacement_l', 'horsepower_hp', 'transmission']
- [3] iCar | קיה פרוסיד 2016 1.6 - יד שניה | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_%D7%A4%D7%A8%D7%95%D7%A1%D7%99%D7%93/%D7%A7%D7%99%D7%94_%D7%A4%D7%A8%D7%95%D7%A1%D7%99%D7%93_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9311/version15618/ | supports=['engine', 'engine_displacement_l']
- [4] auto.co.il | קיה אקסיד - החל מ-138 אלף שקל | https://www.auto.co.il/article/133099-local-news-kia-xceed | supports=['version_or_trim', 'body_type', 'year_start', 'year_end']
- [5] iCar | חדשות רכב - קיה פרוסיד נחשפת: שילוב בין סטיישן לקופה | https://www.icar.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA_%D7%A8%D7%9B%D7%91/%D7%A7%D7%99%D7%94_%D7%A4%D7%A8%D7%95%D7%A1%D7%99%D7%93_%D7%A0%D7%97%D7%A9%D7%A4%D7%AA%3A_%D7%A9%D7%99%D7%9C%D7%95%D7%91_%D7%91%D7%99%D7%9F_%D7%A1%D7%98%D7%99%D7%99%D7%A9%D7%9F_%D7%9C%D7%A7%D7%95%D7%A4%D7%94/ | supports=['fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp']
- [6] auto.co.il | קיה פרו-סיד - מחירון, חוות דעת ומידע טכני | https://www.auto.co.il/cars/kia/pro-ceed/ | supports=['engine', 'engine_displacement_l', 'transmission']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "version_or_trim": null,
    "body_type": "Coupe",
    "fuel_type": "petrol",
    "engine": "2.0L",
    "engine_displacement_l": 2,
    "horsepower_hp": 143,
    "transmission": null,
    "drivetrain": null,
    "year_start": 2008,
    "year_end": 2008,
    "support_level": "unknown",
    "source_indexes": [
      0
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        0
      ],
      "fuel_type": [],
      "engine": [
        0
      ],
      "engine_displacement_l": [
        0
      ],
      "horsepower_hp": [
        0
      ],
      "transmission": [],
      "drivetrain": [],
      "year_start": [
        0
      ],
      "year_end": [
        0
      ]
    },
    "missing_grounded_fields": [
      "fuel_type",
      "transmission",
      "drivetrain"
    ]
  },
  {
    "version_or_trim": null,
    "body_type": "Coupe",
    "fuel_type": "petrol",
    "engine": "1.6L",
    "engine_displacement_l": 1.6,
    "horsepower_hp": 135,
    "transmission": "dual_clutch",
    "drivetrain": null,
    "year_start": 2013,
    "year_end": 2017,
    "support_level": "unknown",
    "source_indexes": [
      1,
      2,
      3
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        1
      ],
      "fuel_type": [
        1
      ],
      "engine": [
        1,
        2
      ],
      "engine_displacement_l": [
        1,
        2
      ],
      "horsepower_hp": [
        2
      ],
      "transmission": [
        2
      ],
      "drivetrain": [],
      "year_start": [
        1
      ],
      "year_end": [
        1
      ]
    },
    "missing_grounded_fields": [
      "drivetrain"
    ]
  },
  {
    "version_or_trim": "GT",
    "body_type": "Estate",
    "fuel_type": "petrol",
    "engine": "1.6L turbo",
    "engine_displacement_l": 1.6,
    "horsepower_hp": 204,
    "transmission": "6-speed dual_clutch",
    "drivetrain": null,
    "year_start": 2019,
    "year_end": 2019,
    "support_level": "unknown",
    "source_indexes": [
      4,
      5,
      6
    ],
    "field_sources": {
      "version_or_trim": [
        4
      ],
      "body_type": [
        4
      ],
      "fuel_type": [
        5
      ],
      "engine": [
        5
      ],
      "engine_displacement_l": [
        5
      ],
      "horsepower_hp": [
        5
      ],
      "transmission": [
        6
      ],
      "drivetrain": [],
      "year_start": [
        4
      ],
      "year_end": [
        4
      ]
    },
    "missing_grounded_fields": [
      "drivetrain"
    ]
  }
]
```


### CURRENT SNAPSHOT 12: `global-reference-only|Kia|ProCeed`

CURRENT VALUE:
```json
{
  "market": "global-reference-only",
  "make": "Kia",
  "model": "ProCeed",
  "canonical_model": "ProCeed",
  "year_start": 2008,
  "year_end": 2017,
  "profile_confidence": "medium",
  "validation_issues": [
    "variant[0] non-null field 'fuel_type' has no field_sources entry",
    "variant[0] required website field 'horsepower_hp' is null/empty",
    "variant[0] required website field 'drivetrain' is null/empty",
    "variant[0] required field 'fuel_type' listed in missing_grounded_fields",
    "variant[0] required field 'horsepower_hp' listed in missing_grounded_fields",
    "variant[0] required field 'drivetrain' listed in missing_grounded_fields",
    "variant[1] required website field 'drivetrain' is null/empty",
    "variant[1] required field 'drivetrain' listed in missing_grounded_fields"
  ]
}
```

CURRENT SOURCES:
- [0] iCar | קיה פרוסיד - כל המידע והדגמים | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_%D7%A4%D7%A8%D7%95%D7%A1%D7%99%D7%93/ | supports=['year_start', 'year_end', 'model generations sold in Israel']
- [1] iCar | קיה פרו סיד בישראל: 135,900 שקל | https://www.icar.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA_%D7%A8%D7%9B%D7%91/%D7%A7%D7%99%D7%94_%D7%A4%D7%A8%D7%95_%D7%A1%D7%99%D7%93_%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C%3A_135%2C900_%D7%A9%D7%A7%D7%9C/ | supports=['2008-2012 engine context sold in Israel', '2008-2012 transmission context sold in Israel', '2013 launch year', '2013-2017 fuel_type', '2013-2017 engine', '2013-2017 engine_displacement_l', '2013-2017 horsepower_hp', '2013-2017 transmission']
- [2] Auto | ועכשיו, קיה פרו-סיד | https://www.auto.co.il/articles/car-news/114019/ | supports=['2013-2017 body_type', '2013-2017 year_start', '2013-2017 fuel_type', '2013-2017 engine', '2013-2017 engine_displacement_l', '2013-2017 horsepower_hp', '2013-2017 transmission']
- [3] Auto | קיה פרו-סיד - מחירון, חוות דעת ומידע טכני | https://www.auto.co.il/cars/kia/pro-ceed/ | supports=['2013-2017 engine', '2013-2017 engine_displacement_l', '2013-2017 horsepower_hp', '2013-2017 transmission', '2013-2017 year_end']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "version_or_trim": null,
    "body_type": "Coupe",
    "fuel_type": "petrol",
    "engine": "2.0L",
    "engine_displacement_l": 2,
    "horsepower_hp": null,
    "transmission": "manual",
    "drivetrain": null,
    "year_start": 2008,
    "year_end": 2012,
    "support_level": "unknown",
    "source_indexes": [
      0,
      1,
      2
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        0
      ],
      "fuel_type": [],
      "engine": [
        1
      ],
      "engine_displacement_l": [
        1
      ],
      "horsepower_hp": [],
      "transmission": [
        1
      ],
      "drivetrain": [],
      "year_start": [
        0
      ],
      "year_end": [
        0
      ]
    },
    "missing_grounded_fields": [
      "fuel_type",
      "horsepower_hp",
      "drivetrain"
    ]
  },
  {
    "version_or_trim": null,
    "body_type": "Coupe",
    "fuel_type": "petrol",
    "engine": "1.6L",
    "engine_displacement_l": 1.6,
    "horsepower_hp": 135,
    "transmission": "6-speed dual_clutch",
    "drivetrain": null,
    "year_start": 2013,
    "year_end": 2017,
    "support_level": "unknown",
    "source_indexes": [
      0,
      2,
      3
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        2
      ],
      "fuel_type": [
        2
      ],
      "engine": [
        2,
        3
      ],
      "engine_displacement_l": [
        2,
        3
      ],
      "horsepower_hp": [
        2,
        3
      ],
      "transmission": [
        2,
        3
      ],
      "drivetrain": [],
      "year_start": [
        0,
        2,
        3
      ],
      "year_end": [
        0
      ]
    },
    "missing_grounded_fields": [
      "drivetrain"
    ]
  }
]
```


### CURRENT SNAPSHOT 13: `IL-confirmed|Kia|Rio`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Kia",
  "model": "Rio",
  "canonical_model": "Rio",
  "year_start": 2012,
  "year_end": 2019,
  "profile_confidence": "medium",
  "validation_issues": [
    "variant[0] required website field 'horsepower_hp' is null/empty",
    "variant[0] required field 'horsepower_hp' listed in missing_grounded_fields",
    "variant[6] required website field 'horsepower_hp' is null/empty",
    "variant[6] required field 'horsepower_hp' listed in missing_grounded_fields"
  ]
}
```

CURRENT SOURCES:
- [0] iCar | קיה ריו 2014 1.2 בנזין ידני 5 דל' LX - יד שניה | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9311/version11766/ | supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'transmission', 'year_start']
- [1] iCar | קיה ריו 2015 1.4 בנזין אוטומט 5 דל' LX - יד שניה | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9311/version13650/ | supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'transmission', 'year_start']
- [2] iCar | מידע מקיף ומקצועי על קיה ריו 2012-2016 - אתר iCar | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9311/ | supports=['year_end', 'year_start', 'version_or_trim', 'engine']
- [3] Autoboom | בדיקת רכב לפני קניה, מספר רכב 39-685-52, קיה ריו 2013 – AUTOBOOM.co.il | https://autoboom.co.il/check-car/3968552 | supports=['fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start']
- [4] iCar | קיה ריו 2016 1.4 בנזין אוטומט 5 דל' EX - יד שניה | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9311/version15593/ | supports=['drivetrain', 'transmission']
- [5] iCar | קיה ריו 2015 1.4 בנזין אוטומט 4 דלתות LX - יד שניה | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9311/version13652/ | supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'transmission', 'year_start', 'year_end']
- [6] iCar | קיה ריו 2015 1.4 בנזין אוטומט 4 דלתות EX - יד שניה | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9311/version13651/ | supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'transmission', 'year_start', 'year_end']
- [7] iCar | קיה ריו 2014 1.4 בנזין ידני 4 דלתות - יד שניה | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9311/version11772/ | supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'transmission', 'year_start', 'year_end']
- [8] Autoboom | בדיקת רכב לפני קניה, מספר רכב 90-358-11, קיה ריו 2013 – AUTOBOOM.co.il | https://autoboom.co.il/check-car/9035811 | supports=['fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start']
- [9] iCar | קיה ריו 2012 1.4 טורבו דיזל ידני 5 דל' LX - יד שניה | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9311/version10395/ | supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'transmission', 'year_start']
- [10] Kia Israel | חדש בארץ: קיה ריו טורבו 1.0 ליטר | קיה ישראל | https://kia-israel.co.il/%D7%9B%D7%AA%D7%91%D7%95%D7%AA-%D7%95%D7%9E%D7%91%D7%97%D7%A0%D7%99-%D7%A8%D7%9B%D7%91/%D7%97%D7%93%D7%A9-%D7%91%D7%90%D7%A8%D7%A5-%D7%A7%D7%99%D7%94-%D7%A8%D7%99%D7%95-%D7%98%D7%95%D7%A8%D7%91%D7%95-1-0-%D7%9C%D7%99%D7%98%D7%A8 | supports=['fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start', 'year_end']
- [11] iCar | מבחני רכב - קיה ריו (1.0 טורבו) - מבחן רכב | https://www.icar.co.il/%D7%9E%D7%91%D7%97%D7%A0%D7%99_%D7%A8%D7%9B%D7%91/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95_%281.0_%D7%98%D7%95%D7%A8%D7%91%D7%95%29_-_%D7%9E%D7%91%D7%97%D7%9F_%D7%A8%D7%9B%D7%91/ | supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start', 'drivetrain', 'year_end']
- [12] iCar | מבחני רכב - קיה ריו סדאן (2018) – מבחן רכב | https://www.icar.co.il/%D7%9E%D7%91%D7%97%D7%A0%D7%99_%D7%A8%D7%9B%D7%91/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95_%D7%A1%D7%93%D7%90%D7%9F_%282018%29_%E2%80%93_%D7%9E%D7%91%D7%97%D7%9F_%D7%A8%D7%9B%D7%91/ | supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start', 'year_end']
- [13] iCar | קיה ריו 2016 1.4 בנזין אוטומט 5 דל' EX - יד שניה | https://www.icar.co.il/%D7%A7%D7%99%D7%94/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95/%D7%A7%D7%99%D7%94_%D7%A8%D7%99%D7%95_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9311/version15593/ | supports=['drivetrain']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "version_or_trim": "LX",
    "body_type": "Hatchback",
    "fuel_type": "petrol",
    "engine": "1.2L",
    "engine_displacement_l": 1.2,
    "horsepower_hp": null,
    "transmission": "manual",
    "drivetrain": "FWD",
    "year_start": 2014,
    "year_end": 2016,
    "support_level": "indirect",
    "source_indexes": [
      0,
      1,
      2
    ],
    "field_sources": {
      "version_or_trim": [
        0
      ],
      "body_type": [
        0
      ],
      "fuel_type": [
        0
      ],
      "engine": [
        0
      ],
      "engine_displacement_l": [
        0
      ],
      "horsepower_hp": [],
      "transmission": [
        0
      ],
      "drivetrain": [
        2
      ],
      "year_start": [
        0,
        1
      ],
      "year_end": [
        1
      ]
    },
    "missing_grounded_fields": [
      "horsepower_hp"
    ]
  },
  {
    "version_or_trim": "LX",
    "body_type": "Hatchback",
    "fuel_type": "petrol",
    "engine": "1.4L",
    "engine_displacement_l": 1.4,
    "horsepower_hp": 109,
    "transmission": "automatic",
    "drivetrain": "FWD",
    "year_start": 2012,
    "year_end": 2016,
    "support_level": "direct",
    "source_indexes": [
      1,
      2,
      3
    ],
    "field_sources": {
      "version_or_trim": [
        1
      ],
      "body_type": [
        1
      ],
      "fuel_type": [
        1,
        3
      ],
      "engine": [
        1,
        3
      ],
      "engine_displacement_l": [
        1,
        3
      ],
      "horsepower_hp": [
        3
      ],
      "transmission": [
        1,
        3
      ],
      "drivetrain": [
        2
      ],
      "year_start": [
        1,
        2
      ],
      "year_end": [
        2
      ]
    },
    "missing_grounded_fields": []
  },
  {
    "version_or_trim": "EX",
    "body_type": "Hatchback",
    "fuel_type": "petrol",
    "engine": "1.4L",
    "engine_displacement_l": 1.4,
    "horsepower_hp": 109,
    "transmission": "automatic",
    "drivetrain": "FWD",
    "year_start": 2012,
    "year_end": 2016,
    "support_level": "direct",
    "source_indexes": [
      2,
      3,
      4
    ],
    "field_sources": {
      "version_or_trim": [
        2
      ],
      "body_type": [
        2
      ],
      "fuel_type": [
        2,
        3
      ],
      "engine": [
        2,
        3
      ],
      "engine_displacement_l": [
        2,
        3
      ],
      "horsepower_hp": [
        3
      ],
      "transmission": [
        2,
        3
      ],
      "drivetrain": [
        4
      ],
      "year_start": [
        2
      ],
      "year_end": [
        2
      ]
    },
    "missing_grounded_fields": []
  },
  {
    "version_or_trim": "LX",
    "body_type": "Sedan",
    "fuel_type": "petrol",
    "engine": "1.4L",
    "engine_displacement_l": 1.4,
    "horsepower_hp": 109,
    "transmission": "automatic",
    "drivetrain": "FWD",
    "year_start": 2012,
    "year_end": 2016,
    "support_level": "direct",
    "source_indexes": [
      5,
      3,
      4
    ],
    "field_sources": {
      "version_or_trim": [
        5
      ],
      "body_type": [
        5
      ],
      "fuel_type": [
        5,
        3
      ],
      "engine": [
        5,
        3
      ],
      "engine_displacement_l": [
        5,
        3
      ],
      "horsepower_hp": [
        3
      ],
      "transmission": [
        5,
        3
      ],
      "drivetrain": [
        4
      ],
      "year_start": [
        5
      ],
      "year_end": [
        5
      ]
    },
    "missing_grounded_fields": []
  },
  {
    "version_or_trim": "EX",
    "body_type": "Sedan",
    "fuel_type": "petrol",
    "engine": "1.4L",
    "engine_displacement_l": 1.4,
    "horsepower_hp": 109,
    "transmission": "automatic",
    "drivetrain": "FWD",
    "year_start": 2012,
    "year_end": 2016,
    "support_level": "direct",
    "source_indexes": [
      6,
      3,
      4
    ],
    "field_sources": {
      "version_or_trim": [
        6
      ],
      "body_type": [
        6
      ],
      "fuel_type": [
        6,
        3
      ],
      "engine": [
        6,
        3
      ],
      "engine_displacement_l": [
        6,
        3
      ],
      "horsepower_hp": [
        3
      ],
      "transmission": [
        6,
        3
      ],
      "drivetrain": [
        4
      ],
      "year_start": [
        6
      ],
      "year_end": [
        6
      ]
    },
    "missing_grounded_fields": []
  },
  {
    "version_or_trim": null,
    "body_type": "Sedan",
    "fuel_type": "petrol",
    "engine": "1.4L",
    "engine_displacement_l": 1.4,
    "horsepower_hp": 109,
    "transmission": "manual",
    "drivetrain": "FWD",
    "year_start": 2013,
    "year_end": 2014,
    "support_level": "indirect",
    "source_indexes": [
      7,
      8,
      4
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        7
      ],
      "fuel_type": [
        7,
        8
      ],
      "engine": [
        7,
        8
      ],
      "engine_displacement_l": [
        7,
        8
      ],
      "horsepower_hp": [
        8
      ],
      "transmission": [
        7,
        8
      ],
      "drivetrain": [
        4
      ],
      "year_start": [
        7,
        8
      ],
      "year_end": [
        7
      ]
    },
    "missing_grounded_fields": []
  },
  {
    "version_or_trim": "LX",
    "body_type": "Hatchback",
    "fuel_type": "diesel",
    "engine": "1.4L turbo",
    "engine_displacement_l": 1.4,
    "horsepower_hp": null,
    "transmission": "manual",
    "drivetrain": "FWD",
    "year_start": 2012,
    "year_end": 2016,
    "support_level": "indirect",
    "source_indexes": [
      9,
      4,
      2
    ],
    "field_sources": {
      "version_or_trim": [
        9
      ],
      "body_type": [
        9
      ],
      "fuel_type": [
        9
      ],
      "engine": [
        9
      ],
      "engine_displacement_l": [
        9
      ],
      "horsepower_hp": [],
      "transmission": [
        9
      ],
      "drivetrain": [
        4
      ],
      "year_start": [
        9,
        2
      ],
      "year_end": [
        2
      ]
    },
    "missing_grounded_fields": [
      "horsepower_hp"
    ]
  },
  {
    "version_or_trim": null,
    "body_type": "Hatchback",
    "fuel_type": "petrol",
    "engine": "1.0L turbo",
    "engine_displacement_l": 1,
    "horsepower_hp": 120,
    "transmission": "dual_clutch",
    "drivetrain": "FWD",
    "year_start": 2019,
    "year_end": 2019,
    "support_level": "indirect",
    "source_indexes": [
      10,
      11
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        10
      ],
      "fuel_type": [
        10,
        11
      ],
      "engine": [
        10,
        11
      ],
      "engine_displacement_l": [
        10,
        11
      ],
      "horsepower_hp": [
        10,
        11
      ],
      "transmission": [
        10,
        11
      ],
      "drivetrain": [
        11
      ],
      "year_start": [
        10,
        11
      ],
      "year_end": [
        10,
        11
      ]
    },
    "missing_grounded_fields": []
  },
  {
    "version_or_trim": null,
    "body_type": "Sedan",
    "fuel_type": "petrol",
    "engine": "1.4L",
    "engine_displacement_l": 1.4,
    "horsepower_hp": 100,
    "transmission": "automatic",
    "drivetrain": "FWD",
    "year_start": 2018,
    "year_end": 2018,
    "support_level": "indirect",
    "source_indexes": [
      12,
      13
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        12
      ],
      "fuel_type": [
        12
      ],
      "engine": [
        12
      ],
      "engine_displacement_l": [
        12
      ],
      "horsepower_hp": [
        12
      ],
      "transmission": [
        12
      ],
      "drivetrain": [
        13
      ],
      "year_start": [
        12
      ],
      "year_end": [
        12
      ]
    },
    "missing_grounded_fields": []
  }
]
```


### CURRENT SNAPSHOT 14: `IL-confirmed|Kia|Sephia`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Kia",
  "model": "Sephia",
  "canonical_model": "Sephia",
  "year_start": 1996,
  "year_end": 2001,
  "profile_confidence": "low",
  "validation_issues": [
    "variant[0] required website field 'drivetrain' is null/empty",
    "variant[0] required field 'drivetrain' listed in missing_grounded_fields",
    "variant[1] required website field 'drivetrain' is null/empty",
    "variant[1] required field 'drivetrain' listed in missing_grounded_fields",
    "variant[2] non-null field 'body_type' has no field_sources entry",
    "variant[2] required website field 'drivetrain' is null/empty",
    "variant[2] required field 'body_type' listed in missing_grounded_fields",
    "variant[2] required field 'drivetrain' listed in missing_grounded_fields",
    "variant[3] non-null field 'body_type' has no field_sources entry",
    "variant[3] required website field 'drivetrain' is null/empty",
    "variant[3] required field 'body_type' listed in missing_grounded_fields",
    "variant[3] required field 'drivetrain' listed in missing_grounded_fields",
    "variant[4] non-null field 'body_type' has no field_sources entry",
    "variant[4] required website field 'drivetrain' is null/empty",
    "variant[4] required field 'body_type' listed in missing_grounded_fields",
    "variant[4] required field 'drivetrain' listed in missing_grounded_fields",
    "variant[5] non-null field 'body_type' has no field_sources entry",
    "variant[5] non-null field 'fuel_type' has no field_sources entry",
    "variant[5] non-null field 'transmission' has no field_sources entry",
    "variant[5] required website field 'drivetrain' is null/empty",
    "variant[5] required field 'body_type' listed in missing_grounded_fields",
    "variant[5] required field 'fuel_type' listed in missing_grounded_fields",
    "variant[5] required field 'transmission' listed in missing_grounded_fields",
    "variant[5] required field 'drivetrain' listed in missing_grounded_fields",
    "variant[6] non-null field 'body_type' has no field_sources entry",
    "variant[6] required website field 'drivetrain' is null/empty",
    "variant[6] required field 'body_type' listed in missing_grounded_fields",
    "variant[6] required field 'drivetrain' listed in missing_grounded_fields",
    "variant[7] non-null field 'body_type' has no field_sources entry",
    "variant[7] required website field 'drivetrain' is null/empty",
    "variant[7] required field 'body_type' listed in missing_grounded_fields",
    "variant[7] required field 'drivetrain' listed in missing_grounded_fields"
  ]
}
```

CURRENT SOURCES:
- [0] יד2 | קיה ספיה 1998 ידני 1.5 (105 כ״ס) | מחירון יד2 | https://www.yad2.co.il/price-list/sub-model/110475/1998 | supports=['body_type', 'fuel_type', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_end']
- [1] יד2 | מחירון של קיה ספיה | מחירון יד2 | https://www.yad2.co.il/price-list/feed?manufacturer=48&model=10716 | supports=['version_or_trim', 'fuel_type', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start', 'year_end']
- [2] יד2 | קיה ספיה 1998 GLX אוט׳ 1.5 (90 כ״ס) | מחירון יד2 | https://www.yad2.co.il/price-list/sub-model/110473/1998 | supports=['version_or_trim', 'body_type', 'fuel_type', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_end']
- [3] יד2 | קיה ספיה 1997 ידני 1.8 (112 כ״ס) | מחירון יד2 | https://www.yad2.co.il/price-list/sub-model/110479/1997 | supports=['engine_displacement_l', 'horsepower_hp', 'year_start', 'year_end']
- [4] יד2 | מחירון של קיה שנתון 2000 | מחירון יד2 | https://www.yad2.co.il/price-list/feed?manufacturer=48&max-year=2000&min-year=2000 | supports=['version_or_trim', 'fuel_type', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "version_or_trim": null,
    "body_type": "Sedan",
    "fuel_type": "petrol",
    "engine": "1.5L",
    "engine_displacement_l": 1.5,
    "horsepower_hp": 105,
    "transmission": "manual",
    "drivetrain": null,
    "year_start": 1996,
    "year_end": 1998,
    "support_level": "indirect",
    "source_indexes": [
      0,
      1
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [
        0
      ],
      "fuel_type": [
        0
      ],
      "engine": [
        0
      ],
      "engine_displacement_l": [
        0
      ],
      "horsepower_hp": [
        0,
        1
      ],
      "transmission": [
        0
      ],
      "drivetrain": [],
      "year_start": [
        1
      ],
      "year_end": [
        0
      ]
    },
    "missing_grounded_fields": [
      "drivetrain"
    ]
  },
  {
    "version_or_trim": "GLX",
    "body_type": "Sedan",
    "fuel_type": "petrol",
    "engine": "1.5L",
    "engine_displacement_l": 1.5,
    "horsepower_hp": 90,
    "transmission": "automatic",
    "drivetrain": null,
    "year_start": 1997,
    "year_end": 1998,
    "support_level": "indirect",
    "source_indexes": [
      2,
      1
    ],
    "field_sources": {
      "version_or_trim": [
        2,
        1
      ],
      "body_type": [
        2
      ],
      "fuel_type": [
        2
      ],
      "engine": [
        2
      ],
      "engine_displacement_l": [
        2
      ],
      "horsepower_hp": [
        2,
        1
      ],
      "transmission": [
        2
      ],
      "drivetrain": [],
      "year_start": [
        1
      ],
      "year_end": [
        2
      ]
    },
    "missing_grounded_fields": [
      "drivetrain"
    ]
  },
  {
    "version_or_trim": null,
    "body_type": "Sedan",
    "fuel_type": "petrol",
    "engine": "1.5L",
    "engine_displacement_l": 1.5,
    "horsepower_hp": 105,
    "transmission": "automatic",
    "drivetrain": null,
    "year_start": 1997,
    "year_end": 1998,
    "support_level": "indirect",
    "source_indexes": [
      1
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [],
      "fuel_type": [
        1
      ],
      "engine": [
        1
      ],
      "engine_displacement_l": [
        1
      ],
      "horsepower_hp": [
        1
      ],
      "transmission": [
        1
      ],
      "drivetrain": [],
      "year_start": [
        1
      ],
      "year_end": [
        1
      ]
    },
    "missing_grounded_fields": [
      "body_type",
      "drivetrain"
    ]
  },
  {
    "version_or_trim": null,
    "body_type": "Sedan",
    "fuel_type": "petrol",
    "engine": "1.6L",
    "engine_displacement_l": 1.6,
    "horsepower_hp": 80,
    "transmission": "manual",
    "drivetrain": null,
    "year_start": 1996,
    "year_end": 1997,
    "support_level": "indirect",
    "source_indexes": [
      1
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [],
      "fuel_type": [
        1
      ],
      "engine": [
        1
      ],
      "engine_displacement_l": [
        1
      ],
      "horsepower_hp": [
        1
      ],
      "transmission": [
        1
      ],
      "drivetrain": [],
      "year_start": [
        1
      ],
      "year_end": [
        1
      ]
    },
    "missing_grounded_fields": [
      "body_type",
      "drivetrain"
    ]
  },
  {
    "version_or_trim": null,
    "body_type": "Sedan",
    "fuel_type": "petrol",
    "engine": "1.6L",
    "engine_displacement_l": 1.6,
    "horsepower_hp": 80,
    "transmission": "automatic",
    "drivetrain": null,
    "year_start": 1996,
    "year_end": 1997,
    "support_level": "indirect",
    "source_indexes": [
      1
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [],
      "fuel_type": [
        1
      ],
      "engine": [
        1
      ],
      "engine_displacement_l": [
        1
      ],
      "horsepower_hp": [
        1
      ],
      "transmission": [
        1
      ],
      "drivetrain": [],
      "year_start": [
        1
      ],
      "year_end": [
        1
      ]
    },
    "missing_grounded_fields": [
      "body_type",
      "drivetrain"
    ]
  },
  {
    "version_or_trim": null,
    "body_type": "Sedan",
    "fuel_type": "petrol",
    "engine": "1.8L",
    "engine_displacement_l": 1.8,
    "horsepower_hp": 112,
    "transmission": "manual",
    "drivetrain": null,
    "year_start": 1997,
    "year_end": 1997,
    "support_level": "indirect",
    "source_indexes": [
      3,
      1
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [],
      "fuel_type": [],
      "engine": [
        3
      ],
      "engine_displacement_l": [
        3
      ],
      "horsepower_hp": [
        3,
        1
      ],
      "transmission": [],
      "drivetrain": [],
      "year_start": [
        3,
        1
      ],
      "year_end": [
        3,
        1
      ]
    },
    "missing_grounded_fields": [
      "body_type",
      "fuel_type",
      "transmission",
      "drivetrain"
    ]
  },
  {
    "version_or_trim": null,
    "body_type": "Sedan",
    "fuel_type": "petrol",
    "engine": "1.8L",
    "engine_displacement_l": 1.8,
    "horsepower_hp": 112,
    "transmission": "automatic",
    "drivetrain": null,
    "year_start": 1997,
    "year_end": 1997,
    "support_level": "indirect",
    "source_indexes": [
      1
    ],
    "field_sources": {
      "version_or_trim": [],
      "body_type": [],
      "fuel_type": [
        1
      ],
      "engine": [
        1
      ],
      "engine_displacement_l": [
        1
      ],
      "horsepower_hp": [
        1
      ],
      "transmission": [
        1
      ],
      "drivetrain": [],
      "year_start": [
        1
      ],
      "year_end": [
        1
      ]
    },
    "missing_grounded_fields": [
      "body_type",
      "drivetrain"
    ]
  },
  {
    "version_or_trim": "LS",
    "body_type": "Sedan",
    "fuel_type": "petrol",
    "engine": "1.5L",
    "engine_displacement_l": 1.5,
    "horsepower_hp": 88,
    "transmission": "manual",
    "drivetrain": null,
    "year_start": 2000,
    "year_end": 2001,
    "support_level": "indirect",
    "source_indexes": [
      1,
      4
    ],
    "field_sources": {
      "version_or_trim": [
        1,
        4
      ],
      "body_type": [],
      "fuel_type": [
        1,
        4
      ],
      "engine": [
        1,
        4
      ],
      "engine_displacement_l": [
        1,
        4
      ],
      "horsepower_hp": [
        1,
        4
      ],
      "transmission": [
        1,
        4
      ],
      "drivetrain": [],
      "year_start": [
        4
      ],
      "year_end": [
        1,
        4
      ]
    },
    "missing_grounded_fields": [
      "body_type",
      "drivetrain"
    ]
  }
]
```


### CURRENT SNAPSHOT 15: `IL-confirmed|Kia|XCeed`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Kia",
  "model": "XCeed",
  "canonical_model": "XCeed",
  "year_start": null,
  "year_end": null,
  "profile_confidence": null,
  "validation_issues": [
    "technical_variants_il is empty"
  ],
  "error": "Gemini catalog client returned non-object JSON"
}
```

CURRENT SOURCES:
- none in current review profile

CURRENT VARIANTS / RAW PAYLOAD:
```json
{
  "years_seen": [
    2019,
    2021,
    2026
  ],
  "trims_seen": [
    "Premium"
  ],
  "engines_seen": [
    "1.4L T-GDI petrol, 140 hp",
    "1.5L T-GDI petrol, 160 hp",
    "1.6L GDI PHEV, 141 hp"
  ],
  "horsepower_seen": [],
  "transmissions_seen": [
    "6-speed DCT",
    "7-speed DCT"
  ],
  "body_types_seen": [
    "Crossover"
  ],
  "fuel_types_seen": [
    "Mild Hybrid",
    "Petrol",
    "Plug-in Hybrid"
  ],
  "drivetrains_seen": [
    "FWD"
  ]
}
```


### CURRENT SNAPSHOT 16: `IL-confirmed|Lamborghini|Revuelto`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Lamborghini",
  "model": "Revuelto",
  "canonical_model": "Revuelto",
  "year_start": null,
  "year_end": null,
  "profile_confidence": null,
  "validation_issues": [
    "technical_variants_il is empty"
  ],
  "error": "Extra data: line 120 column 1 (char 2514)"
}
```

CURRENT SOURCES:
- none in current review profile

CURRENT VARIANTS / RAW PAYLOAD:
```json
{
  "years_seen": [
    2023,
    2026
  ],
  "trims_seen": [],
  "engines_seen": [
    "6.5L V12 Plug-in Hybrid, 1015 hp"
  ],
  "horsepower_seen": [],
  "transmissions_seen": [
    "8-speed DCT"
  ],
  "body_types_seen": [
    "Coupe"
  ],
  "fuel_types_seen": [
    "Plug-in Hybrid"
  ],
  "drivetrains_seen": [
    "AWD"
  ]
}
```


### CURRENT SNAPSHOT 17: `IL-confirmed|Lancia|Dedra`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Lancia",
  "model": "Dedra",
  "canonical_model": "Dedra",
  "year_start": null,
  "year_end": null,
  "profile_confidence": null,
  "validation_issues": [
    "technical_variants_il is empty"
  ],
  "error": "Extra data: line 136 column 1 (char 3500)"
}
```

CURRENT SOURCES:
- none in current review profile

CURRENT VARIANTS / RAW PAYLOAD:
```json
{
  "years_seen": [
    1990,
    1999
  ],
  "trims_seen": [
    "1.6 i.e.",
    "1.8 i.e.",
    "2.0 i.e."
  ],
  "engines_seen": [
    "1.6L inline-4 petrol",
    "1.8L inline-4 petrol",
    "2.0L inline-4 petrol"
  ],
  "horsepower_seen": [],
  "transmissions_seen": [
    "4-speed automatic",
    "5-speed manual"
  ],
  "body_types_seen": [
    "Sedan"
  ],
  "fuel_types_seen": [
    "Petrol"
  ],
  "drivetrains_seen": [
    "FWD"
  ]
}
```


### CURRENT SNAPSHOT 18: `IL-likely|Lancia|Delta`

CURRENT VALUE:
```json
{
  "market": "IL-likely",
  "make": "Lancia",
  "model": "Delta",
  "canonical_model": "Delta",
  "year_start": null,
  "year_end": null,
  "profile_confidence": null,
  "validation_issues": [
    "technical_variants_il is empty"
  ],
  "error": "Gemini catalog client returned non-object JSON"
}
```

CURRENT SOURCES:
- none in current review profile

CURRENT VARIANTS / RAW PAYLOAD:
```json
{
  "years_seen": [
    1993,
    1999
  ],
  "trims_seen": [],
  "engines_seen": [
    "1.6L petrol"
  ],
  "horsepower_seen": [],
  "transmissions_seen": [
    "5-speed manual"
  ],
  "body_types_seen": [
    "Hatchback"
  ],
  "fuel_types_seen": [
    "Petrol"
  ],
  "drivetrains_seen": [
    "FWD"
  ]
}
```


### CURRENT SNAPSHOT 19: `IL-confirmed|Lancia|Kappa`

CURRENT VALUE:
```json
{
  "market": "IL-confirmed",
  "make": "Lancia",
  "model": "Kappa",
  "canonical_model": "Kappa",
  "year_start": null,
  "year_end": null,
  "profile_confidence": null,
  "validation_issues": [
    "technical_variants_il is empty"
  ],
  "error": "Gemini catalog client returned non-object JSON"
}
```

CURRENT SOURCES:
- none in current review profile

CURRENT VARIANTS / RAW PAYLOAD:
```json
{
  "years_seen": [
    1994,
    2001
  ],
  "trims_seen": [
    "LS",
    "LX"
  ],
  "engines_seen": [
    "2.0L 20V inline-5 petrol, 145-155 hp",
    "2.4L 20V inline-5 petrol, 175 hp"
  ],
  "horsepower_seen": [],
  "transmissions_seen": [
    "4-speed automatic",
    "5-speed manual"
  ],
  "body_types_seen": [
    "Sedan"
  ],
  "fuel_types_seen": [
    "Petrol"
  ],
  "drivetrains_seen": [
    "FWD"
  ]
}
```


### CURRENT SNAPSHOT 20: `IL-likely|Lancia|Lybra`

CURRENT VALUE:
```json
{
  "market": "IL-likely",
  "make": "Lancia",
  "model": "Lybra",
  "canonical_model": "Lybra",
  "year_start": null,
  "year_end": null,
  "profile_confidence": null,
  "validation_issues": [
    "technical_variants_il is empty"
  ],
  "error": "Expecting ',' delimiter: line 91 column 3 (char 2196)"
}
```

CURRENT SOURCES:
- none in current review profile

CURRENT VARIANTS / RAW PAYLOAD:
```json
{
  "years_seen": [
    1999,
    2005
  ],
  "trims_seen": [],
  "engines_seen": [
    "1.8L inline-4 petrol, 131 hp"
  ],
  "horsepower_seen": [],
  "transmissions_seen": [
    "5-speed manual"
  ],
  "body_types_seen": [
    "Sedan"
  ],
  "fuel_types_seen": [
    "Petrol"
  ],
  "drivetrains_seen": [
    "FWD"
  ]
}
```


### CURRENT SNAPSHOT 21: `global-reference-only|Lancia|Musa`

CURRENT VALUE:
```json
{
  "market": "global-reference-only",
  "make": "Lancia",
  "model": "Musa",
  "canonical_model": "Musa",
  "year_start": null,
  "year_end": null,
  "profile_confidence": "medium",
  "validation_issues": [
    "technical_variants_il is empty"
  ]
}
```

CURRENT SOURCES:
- none in current review profile

CURRENT VARIANTS / RAW PAYLOAD:
```json
[]
```


### CURRENT SNAPSHOT 22: `global-reference-only|Lancia|Phedra`

CURRENT VALUE:
```json
{
  "market": "global-reference-only",
  "make": "Lancia",
  "model": "Phedra",
  "canonical_model": "Phedra",
  "year_start": null,
  "year_end": null,
  "profile_confidence": null,
  "validation_issues": [
    "technical_variants_il is empty"
  ],
  "error": "Extra data: line 13 column 1 (char 236)"
}
```

CURRENT SOURCES:
- none in current review profile

CURRENT VARIANTS / RAW PAYLOAD:
```json
{
  "years_seen": [
    2002,
    2010
  ],
  "trims_seen": [],
  "engines_seen": [
    "2.0L 16V Petrol, 136 hp",
    "2.2L JTD Turbo Diesel, 128 hp",
    "3.0L V6 24V Petrol, 204 hp"
  ],
  "horsepower_seen": [],
  "transmissions_seen": [
    "4-speed automatic",
    "5-speed manual"
  ],
  "body_types_seen": [
    "Minivan"
  ],
  "fuel_types_seen": [
    "Diesel",
    "Petrol"
  ],
  "drivetrains_seen": [
    "FWD"
  ]
}
```


### CURRENT SNAPSHOT 23: `global-reference-only|Lancia|Thema`

CURRENT VALUE:
```json
{
  "market": "global-reference-only",
  "make": "Lancia",
  "model": "Thema",
  "canonical_model": "Thema",
  "year_start": 2011,
  "year_end": 2014,
  "profile_confidence": "medium",
  "validation_issues": [
    "variant[0] has no source_indexes",
    "variant[0] support_level=direct but no source directly supports it",
    "variant[1] has no source_indexes",
    "variant[1] support_level=direct but no source directly supports it"
  ]
}
```

CURRENT SOURCES:
- [1] Autoboom Israel | לנצ'יה תמא 2011 - 2014, דור 2, סדאן – מפרט טכני | https://autoboom.co.il/he/catalog/cars/lancia/thema/2-generation/sedan | supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

CURRENT VARIANTS / RAW PAYLOAD:
```json
[
  {
    "body_type": "Sedan",
    "fuel_type": "diesel",
    "engine": "3.0L v6 turbo",
    "engine_displacement_l": 3.0,
    "horsepower_hp": 190,
    "transmission": "5-speed automatic",
    "drivetrain": "RWD",
    "year_start": 2011,
    "year_end": 2014,
    "version_or_trim": null,
    "support_level": "direct",
    "missing_grounded_fields": [],
    "field_sources": {
      "body_type": [
        1
      ],
      "fuel_type": [
        1
      ],
      "engine": [
        1
      ],
      "engine_displacement_l": [
        1
      ],
      "horsepower_hp": [
        1
      ],
      "transmission": [
        1
      ],
      "drivetrain": [
        1
      ],
      "year_start": [
        1
      ],
      "year_end": [
        1
      ],
      "version_or_trim": []
    }
  },
  {
    "body_type": "Sedan",
    "fuel_type": "diesel",
    "engine": "3.0L v6 turbo",
    "engine_displacement_l": 3.0,
    "horsepower_hp": 239,
    "transmission": "5-speed automatic",
    "drivetrain": "RWD",
    "year_start": 2011,
    "year_end": 2014,
    "version_or_trim": null,
    "support_level": "direct",
    "missing_grounded_fields": [],
    "field_sources": {
      "body_type": [
        1
      ],
      "fuel_type": [
        1
      ],
      "engine": [
        1
      ],
      "engine_displacement_l": [
        1
      ],
      "horsepower_hp": [
        1
      ],
      "transmission": [
        1
      ],
      "drivetrain": [
        1
      ],
      "year_start": [
        1
      ],
      "year_end": [
        1
      ],
      "version_or_trim": []
    }
  }
]
```


### CURRENT SNAPSHOT 24: `global-reference-only|Lexus|LX`

CURRENT VALUE:
```json
{
  "market": "global-reference-only",
  "make": "Lexus",
  "model": "LX",
  "canonical_model": "LX",
  "year_start": null,
  "year_end": null,
  "profile_confidence": "medium",
  "validation_issues": [
    "technical_variants_il is empty"
  ]
}
```

CURRENT SOURCES:
- [0] WinWin / Yitzhak Levi | לקסוס LX - מחירון רכב, מבחני דרכים וחוות דעת - יצחק לוי | https://www.winwin.co.il/cars/catalog/lexus/lx | supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain']
- [1] Lexus Israel | Lexus LX Israel Website (None found/Available) | https://www.lexus.co.il/ | supports=[]
- [2] Auto.co.il | לקסוס משיקה את רכב השטח LX בישראל | https://www.auto.co.il/article/111059-local-news-lexus-lx | supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [3] iCar | לקסוס LX - קטלוג רכבים חדשים - iCar | https://www.icar.co.il/lexus/lexus_lx | supports=[]

CURRENT VARIANTS / RAW PAYLOAD:
```json
[]
```



## FINAL RUN DECISION BLOCKS — EVERY ACTIVE BLOCKER

### 1. Jeep Gladiator
MODEL: Jeep Gladiator
CURRENT VALUE: `IL-confirmed|Jeep|Gladiator` has one Rubicon row but no row-level `source_indexes`.
PROBLEM: Source/indexing blocker only; the Israeli-market model/variant is grounded.
WEB-VALIDATED FACT: Israeli sources support Jeep Gladiator Rubicon in Israel with 3.6L V6 petrol, 280 hp, 8-speed automatic and 4WD/Rubicon configuration.
SOURCE:
- Repo-local: iCar Jeep Gladiator Rubicon; Cartube Gladiator Israel launch/spec PDF.
- Web cross-check: Cartube Gladiator PDF (`jeep-gladiator-mifrat-2023.pdf`) and Israeli listings support 3.6L petrol automatic Gladiator/Rubicon.
TARGET VALUE:
- Move from review to clean.
- Keep exactly one technical row unless repo-local sources distinguish multiple Israeli trims:
  - `version_or_trim=Rubicon`
  - `body_type=Pickup`
  - `fuel_type=petrol`
  - `engine=3.6L V6`
  - `engine_displacement_l=3.6`
  - `horsepower_hp=280`
  - `transmission=8-speed automatic`
  - `drivetrain=4WD`
  - `year_start=2020` only if existing repo-local source already grounds 2020; otherwise use `year_start=2021`; `year_end=null` if current/local listing/source support remains valid.
- Add valid `source_indexes` and `field_sources` for every non-null field.
ACTION: FIX / KEEP

### 2. KGM Tivoli
MODEL: KGM Tivoli
CURRENT VALUE: `IL-confirmed|KGM|Tivoli` has one 1.5T 163 hp row but no row-level `source_indexes`.
PROBLEM: Source/indexing blocker; also brand lineage must not confuse KGM Tivoli with older SsangYong Tivoli.
WEB-VALIDATED FACT: Israeli KGM/Tivoli sources support current KGM Tivoli with 1.5L turbo petrol, 163 hp, automatic transmission; the current profile row already has the right technical fingerprint.
SOURCE:
- Repo-local: Cartube 2024/2025 KGM Tivoli Israel; iCar KGM Tivoli specs.
TARGET VALUE:
- Move to clean with one grounded current KGM row:
  - `version_or_trim=null` unless repo-local source gives real Israeli trim names.
  - `body_type=Crossover`, `fuel_type=petrol`, `engine=1.5L turbo`, `engine_displacement_l=1.5`, `horsepower_hp=163`, `transmission=6-speed automatic`, `drivetrain=FWD`.
  - `year_start=2024` if current repo-local source supports 2024; otherwise use `year_start=2025`; `year_end=null`.
- Add `source_indexes` and `field_sources`.
- Preserve alias/lineage from SsangYong Tivoli only if repo already has a brand-lineage mechanism; do not duplicate the same current car under both brands.
ACTION: FIX / ALIAS / LINEAGE

### 3. Kia Carens
MODEL: Kia Carens
CURRENT VALUE: Empty `technical_variants_il` due model-output failure.
PROBLEM: Real Israeli historical model, but current profile is empty and blocking.
WEB-VALIDATED FACT: Israeli sources support Kia Carens as a 7-seat MPV in Israel around 2013-2019; relevant Israeli/raw fingerprints include 2.0 GDI petrol 166 hp and 1.7 CRDi diesel 141 hp. Global-only older 1.8/2.0 CRDi rows are not enough for clean without local source.
SOURCE:
- Repo/raw payload values.
- iCar Kia Carens page/version evidence in repo-local profile references if available.
TARGET VALUE:
- Rebuild only locally grounded rows. Minimum acceptable clean rows:
  1. Petrol row: `body_type=MPV`, `fuel_type=petrol`, `engine=2.0L GDI`, `engine_displacement_l=2.0`, `horsepower_hp=166`, `transmission=6-speed automatic` if source supports it, `drivetrain=FWD`, `year_start=2013`, `year_end=2019` or narrower if source requires.
  2. Diesel row: `body_type=MPV`, `fuel_type=diesel`, `engine=1.7L CRDi`, `engine_displacement_l=1.7`, `horsepower_hp=141`, `transmission=7-speed dual_clutch` if source supports it, `drivetrain=FWD`, `year_start=2016/2018` according to source, `year_end=2019`.
- Do not add 2000/2006/2007/1.8/2.0 CRDi rows unless exact Israeli source support exists.
- If exact local sources are insufficient, move weak rows to non-blocking archive/review and leave only grounded rows clean.
ACTION: ADD / FIX / MOVE WEAK ROW TO REVIEW

### 4. Kia EV9
MODEL: Kia EV9
CURRENT VALUE: Three current EV rows Executive / Premium / GT-Line; `transmission=null`.
PROBLEM: EV schema failure; all EV rows need canonical EV transmission value.
WEB-VALIDATED FACT: Kia Israel EV9 official page and PDF support Executive RWD, Premium AWD, GT-Line AWD; RWD is about 149.5 kW / 203 hp and AWD rows are 384 hp in the existing repo facts.
SOURCE:
- `https://kia-israel.co.il/רכב/ev9`
- `https://kia-israel.co.il/catalog/mifrat_EV9.pdf`
TARGET VALUE:
- Keep all three rows clean.
- Set `transmission=single_speed` or repo canonical EV value `direct_drive` consistently with schema.
- Keep `engine=electric`, `engine_displacement_l=null`, `fuel_type=electric`.
- Keep `drivetrain=RWD` for Executive; `AWD` for Premium and GT-Line.
- Set support level from `unknown` to direct/official if repo-local official source indexes support each row.
- Add field_sources for `transmission` and remove it from `missing_grounded_fields`.
ACTION: FIX

### 5. Kia Mohave + global Kia Mohave
MODEL: Kia Mohave
CURRENT VALUE: `IL-confirmed|Kia|Mohave` has a good diesel row plus a weak petrol row missing hp/transmission; `global-reference-only|Kia|Mohave` has zero variants.
PROBLEM: Mixed local historical support and global/reference duplicate.
WEB-VALIDATED FACT: Existing Israeli evidence supports historical Mohave mostly as a weak/Tier 3 local catalog. Later 2019 global Mohave sources state not confirmed/not expected for Israel.
SOURCE:
- Repo-local Autoboom/Kia/Auto/Cartube sources already in profile.
TARGET VALUE:
- Keep only the diesel 3.0L V6 row if all source indexes validate: `body_type=SUV`, `fuel_type=diesel`, `engine=3.0L turbo V6`, `engine_displacement_l=3.0`, `horsepower_hp=250`, `transmission=automatic`, `drivetrain=4WD`, `year_start=2009`, `year_end=2011`.
- Move petrol 3.8L V6 row to non-blocking archive/review unless exact Israeli hp and transmission are grounded.
- Archive `global-reference-only|Kia|Mohave` as non-blocking duplicate/reference-only with lineage to `IL-confirmed|Kia|Mohave`.
ACTION: FIX / MOVE TO REVIEW / ARCHIVE NON-BLOCKING / ALIAS

### 6. Kia Niro
MODEL: Kia Niro
CURRENT VALUE: Four rows; current hybrid has `drivetrain=null`, EV has `drivetrain=null`.
PROBLEM: Missing drivetrain fields; current/historical split must stay because outputs differ.
WEB-VALIDATED FACT: Kia Israel official current Niro Hybrid page/PDF supports 1.6 GDI hybrid 129 hp and 6-speed DCT; older Niro hybrid/PHEV and Niro EV are Israeli-grounded in repo-local PDFs/catalog sources. Niro/Niro EV powertrains are FWD in this class.
SOURCE:
- `https://kia-israel.co.il/רכב/נירו-החדש`
- `https://kia-israel.co.il/catalog/mifrat_niro-hybrid.pdf`
TARGET VALUE:
- Keep row 0 older hybrid 2016-2019 as is if sources validate.
- FIX row 1 current hybrid: set `drivetrain=FWD`; keep `horsepower_hp=129`, `transmission=6-speed dual_clutch`, `year_end=2026/null-current` according to schema convention, with official Kia Israel current source.
- Keep row 2 PHEV 2020-2023 if source indexes validate.
- FIX row 3 EV: set `drivetrain=FWD`; keep `transmission=single_speed`, `horsepower_hp=204`; do not keep `year_end=2024` as current unless source supports; if no current official Niro EV page, close EV at the last grounded year.
ACTION: FIX / KEEP

### 7. Kia Niro Plus
MODEL: Kia Niro Plus
CURRENT VALUE: HEV/PHEV rows valid; EV row missing `transmission` and `drivetrain`.
PROBLEM: EV schema and drivetrain missing.
WEB-VALIDATED FACT: Kia Israel Niro Plus EV PDF supports 150 kW / 204 hp EV. The EV is a FWD single-motor/single-speed type; schema needs explicit transmission/drivetrain.
SOURCE:
- `https://kia-israel.co.il/catalog/mifrat-niro-plus.pdf`
- Repo-local Auto/iCar sources already in profile.
TARGET VALUE:
- Keep GX HEV and LX/EX PHEV if sources validate.
- FIX EV EX row: `transmission=single_speed` or canonical `direct_drive`, `drivetrain=FWD`, `engine=electric`, `engine_displacement_l=null`, `horsepower_hp=204`, `year_start=2022`; set `year_end` to last grounded Israeli year, not blindly current.
ACTION: FIX / KEEP

### 8. Kia Picanto
MODEL: Kia Picanto
CURRENT VALUE: One 2011-2016 EX 1.25 automatic row, no source array, invalid source refs, `drivetrain=null`, and `variant[1] is not an object`.
PROBLEM: Broken source/reference structure plus malformed variant object.
WEB-VALIDATED FACT: Israeli used-car/catalog sources support 2011-2016 Picanto 1.2/1.25 petrol automatic around 85 hp; drivetrain for Picanto is FWD.
SOURCE:
- Existing repo-local Picanto references if present in source files.
- Cross-check: Israeli listings/catalogs show 2012-2016 Picanto 1.2/1.25 85 hp automatic.
TARGET VALUE:
- Repair sources list and valid `source_indexes`/`field_sources`.
- Set row: `version_or_trim=EX`, `body_type=Hatchback`, `fuel_type=petrol`, `engine=1.25L`, `engine_displacement_l=1.25`, `horsepower_hp=85`, `transmission=automatic`, `drivetrain=FWD`, `year_start=2011`, `year_end=2016`.
- Delete/repair malformed `variant[1]` so every variant is an object.
ACTION: FIX / DELETE MALFORMED DUPLICATE

### 9. Kia Pride
MODEL: Kia Pride
CURRENT VALUE: Two DLX 1.3 75 hp rows; `drivetrain=null`.
PROBLEM: Missing drivetrain only; historical support is Tier 3 but coherent.
WEB-VALIDATED FACT: Yad2 price list supports 1997/1998 Kia Pride DLX manual/automatic 1.3 75 hp petrol. Pride is FWD.
SOURCE:
- `https://www.yad2.co.il/price-list/feed?manufacturer=48&model=10713`
TARGET VALUE:
- Keep both manual and automatic DLX rows as historical Tier 3 if sources validate.
- Set `drivetrain=FWD` for both rows and add field_sources/source indexes.
- Keep `body_type=Hatchback`, `fuel_type=petrol`, `engine=1.3L`, `horsepower_hp=75`.
ACTION: FIX / KEEP

### 10. Kia ProCeed + global Kia ProCeed
MODEL: Kia ProCeed
CURRENT VALUE: `IL-confirmed|Kia|ProCeed` has 3 rows and `global-reference-only|Kia|ProCeed` has 2 overlapping rows; several missing `fuel_type`, `transmission`, `horsepower_hp`, `drivetrain`.
PROBLEM: Duplicate scope plus weak early rows.
WEB-VALIDATED FACT: Israeli sources support Kia ProCeed/ProCeed GT as an Israeli marketed line. Front-wheel-drive is the drivetrain. 2019 ProCeed GT is 1.6 turbo 204 hp with dual-clutch; 2013-2017 1.6 GDI 135 hp DCT is plausible if repo-local sources support it. Early 2008 2.0 coupe rows are weak and missing required fields.
SOURCE:
- Repo-local iCar/Auto ProCeed sources.
TARGET VALUE:
- Merge `global-reference-only|Kia|ProCeed` into `IL-confirmed|Kia|ProCeed` or archive the global duplicate non-blocking.
- Set `drivetrain=FWD` for grounded 1.6 GDI and GT rows.
- For 2019 GT row: keep `version_or_trim=GT`, `body_type=Estate` or repo canonical shooting-brake/estate, `fuel_type=petrol`, `engine=1.6L turbo`, `horsepower_hp=204`, `transmission=6-speed dual_clutch`, `drivetrain=FWD`, `year_start=2019`, `year_end=2019` unless wider Israeli source exists.
- For 2013-2017 1.6 GDI row: keep only if source supports; set `drivetrain=FWD`.
- Move 2008/2012 2.0 coupe rows to non-blocking archive/review unless exact Israeli source fills all missing fields including transmission/drivetrain/hp.
ACTION: MERGE / FIX / ARCHIVE WEAK ROWS NON-BLOCKING

### 11. Kia Rio
MODEL: Kia Rio
CURRENT VALUE: Nine rows; rows 0 and 6 missing `horsepower_hp`.
PROBLEM: Missing hp fields block readiness; otherwise most rows are coherent.
WEB-VALIDATED FACT: Israeli/used-car sources support 2012-2016 Rio 1.4 petrol automatic 109 hp and 1.4 diesel/manual around 90 hp; global/European data supports 1.25/1.2 petrol manual around 85-86 hp. Rio is FWD.
SOURCE:
- Repo-local iCar/Yad2/Autoboom sources.
- Cross-check: Israeli listings show 1.4 109 hp petrol; global data supports 1.4 CRDi 90 hp and 1.25/1.2 85 hp.
TARGET VALUE:
- FIX variant 0 (`LX`, hatchback, 1.2L petrol manual, 2014-2016): set `horsepower_hp=85` only if repo-local source supports 1.25/1.2 85 hp; otherwise move this row to non-blocking review.
- Keep variants 1-5 if source indexes validate.
- FIX variant 6 (`LX`, hatchback, 1.4L turbo diesel manual): set `horsepower_hp=90` only if repo-local/local source supports; otherwise move this row to non-blocking review.
- Keep variants 7-8 if source indexes validate.
- Ensure all rows have `drivetrain=FWD` and valid field_sources.
ACTION: FIX / MOVE WEAK ROW TO REVIEW

### 12. Kia Sephia
MODEL: Kia Sephia
CURRENT VALUE: Eight rows; many missing `drivetrain`, some missing `body_type`/`fuel_type`/`transmission` field_sources.
PROBLEM: Historical Tier 3 catalog rows need source normalization and drivetrain/body field repair.
WEB-VALIDATED FACT: Yad2 price list supports Sephia 1997-1998 rows including GLX automatic 1.5 90 hp, 1.5 manual/automatic 105 hp, 1.6 80 hp, 1.8 112 hp; body is sedan and drivetrain is FWD.
SOURCE:
- `https://www.yad2.co.il/price-list/feed?manufacturer=48&model=10716`
TARGET VALUE:
- Keep as historical/Tier 3 if source policy allows Yad2 price list for old Israeli models.
- Set `body_type=Sedan` and `drivetrain=FWD` for all rows.
- Ensure `fuel_type=petrol` and `transmission=manual/automatic` field_sources exist for every non-null value.
- If a row lacks exact source support for the trim/engine/hp combination, move only that row to non-blocking review/archive.
ACTION: FIX / KEEP / MOVE WEAK ROW TO REVIEW

### 13. Kia XCeed
MODEL: Kia XCeed
CURRENT VALUE: Empty profile; raw payload includes 2019/2021/2026, Premium, 1.4T 140, 1.5T 160, 1.6 PHEV 141, DCT, FWD.
PROBLEM: Empty blocker caused by model-output failure; 2026 raw value appears wrong for Israel.
WEB-VALIDATED FACT: Israeli sources say XCeed was marketed in Israel between 2019 and 2023; Cartube explicitly says that after facelift it did not return to Israel. Israeli sources support 2019 1.4 T-GDI 140 hp 7DCT and 2021 1.5 turbo mild-hybrid 160 hp. Current 2026 Israel clean must not be added without official/local source.
SOURCE:
- `https://www.cartube.co.il/חדשות-רכב/קיה-אקסיד-בישראל-מחיר-137900-שקל`
- `https://www.icar.co.il/מבחני_רכב/קיה_אקסיד_-_מבחן_רכב/`
- `https://www.cartube.co.il/חדשות-רכב/חדש-בישראל-2021-קיה-אקסיד-1-5-טורבו-160`
- `https://www.cartube.co.il/חדשות-רכב/2026-קיה-אקסיד-החדש-נחשף-מתיחת-פנים-מקיפה-לדגם`
TARGET VALUE:
- Rebuild XCeed clean with grounded historical rows only:
  1. `year_start=2019`, `year_end=2020/2021 according to source`, `body_type=Crossover`, `fuel_type=petrol`, `engine=1.4L T-GDI`, `engine_displacement_l=1.4`, `horsepower_hp=140`, `transmission=7-speed dual_clutch`, `drivetrain=FWD`, trim `LX/EX/Premium` only if repo-local source differentiates; otherwise do not split by equipment trim.
  2. `year_start=2021`, `year_end=2023`, `body_type=Crossover`, `fuel_type=mild_hybrid` or schema canonical petrol-mild-hybrid, `engine=1.5L T-GDI`, `engine_displacement_l=1.5`, `horsepower_hp=160`, `transmission=7-speed dual_clutch`, `drivetrain=FWD`.
- Do not add `year_end=2026` for Israeli clean.
- Add 1.6 PHEV 141 only if repo-local Israeli source proves it was marketed in Israel; otherwise archive it non-blocking.
ACTION: ADD / FIX / ARCHIVE UNSUPPORTED 2026/PHEV ROWS

### 14. Lamborghini Revuelto
MODEL: Lamborghini Revuelto
CURRENT VALUE: Empty `IL-confirmed|Lamborghini|Revuelto` profile; raw says 2023/2026, 6.5 V12 PHEV 1015 hp, 8DCT, AWD.
PROBLEM: No strong official Israeli importer clean source. Israeli evidence is special/private/parallel import or vehicle registration/news, not normal official-market clean.
WEB-VALIDATED FACT: Revuelto exists globally and Israeli press has covered imported/registered examples, but this does not prove regular official Israeli-market trim catalog. For this project, global/exotic import-only evidence is not enough to add a normal clean Israeli catalog variant.
SOURCE:
- Israeli press/register/listing evidence only; no official Lamborghini Israel importer source found in repo/task.
TARGET VALUE:
- Do not keep as `IL-confirmed` clean unless repo-local source proves official Israeli sales/catalog.
- Move to non-blocking archive/review with `reason=special_import_or_registration_only_no_official_il_catalog_grounding`.
- Preserve raw fingerprint in archive lineage: `6.5L V12 plug-in hybrid`, `1015 hp`, `8-speed DCT`, `AWD`, `Coupe`, `2023+ global`.
ACTION: ARCHIVE NON-BLOCKING / MOVE TO REVIEW

### 15. Lancia Dedra
MODEL: Lancia Dedra
CURRENT VALUE: Empty profile; raw values are 1990/1999 1.6/1.8/2.0 petrol FWD sedan.
PROBLEM: No strong Israeli source embedded; model output failed.
WEB-VALIDATED FACT: Available evidence in this task is not strong enough to rebuild verified clean Israeli technical rows. For a verified clean catalog, do not fabricate old Lancia variants from raw/global values alone.
SOURCE:
- Raw payload only; no Tier 1/2 Israeli source embedded.
TARGET VALUE:
- Move to non-blocking archive/review unless repo-local sources ground exact Israeli rows.
- Archive raw fingerprints with lineage, `non_blocking=true`, reason `legacy_lancia_insufficient_israeli_field_grounding`.
ACTION: ARCHIVE NON-BLOCKING / MOVE TO REVIEW

### 16. Lancia Delta `IL-likely`
MODEL: Lancia Delta
CURRENT VALUE: Empty `IL-likely|Lancia|Delta`; raw historical 1993/1999 1.6 petrol FWD hatchback.
PROBLEM: Duplicate/weak likely profile; RUN 1 already handled `IL-confirmed|Lancia|Delta`.
WEB-VALIDATED FACT: Modern/reintroduced Delta evidence belongs to `IL-confirmed|Lancia|Delta` task from RUN 1. This `IL-likely` profile is a weak historical/global duplicate unless local source proves exact separate rows.
SOURCE:
- RUN 1 cumulative task for `IL-confirmed|Lancia|Delta`.
TARGET VALUE:
- Do not create duplicate clean profile.
- Merge into `IL-confirmed|Lancia|Delta` only if exact row is locally grounded and not duplicate.
- Otherwise archive non-blocking with lineage `duplicate_or_weak_lancia_delta_likely_profile`.
ACTION: MERGE / ARCHIVE NON-BLOCKING / ALIAS

### 17. Lancia Kappa
MODEL: Lancia Kappa
CURRENT VALUE: Empty `IL-confirmed|Lancia|Kappa`; raw values 1994/2001 LS/LX, 2.0 145-155, 2.4 175.
PROBLEM: Empty blocker; legacy evidence is weak/mixed. Yad2 has some Kappa rows but not necessarily matching raw exactly.
WEB-VALIDATED FACT: Israeli listing/price-list evidence confirms Lancia Kappa presence and supports at least 2.4 175 hp and 2.0 variants, but sources are Tier 3 and not enough to fabricate full clean rows where trim/hp conflict exists.
SOURCE:
- `https://www.yad2.co.il/price-list/feed?manufacturer=25`
- Israeli listing cross-checks for Lancia Kappa.
TARGET VALUE:
- If repo-local Yad2/price-list source gives exact submodels, rebuild only exact rows. Candidate: `Distinctive` 2.4 175 hp automatic; possible 2.0 row only if exact hp and transmission source are present.
- Do not add raw LS/LX 2.0 145-155 hp rows without exact Israeli source.
- If no exact field-level local source exists, archive non-blocking with raw fingerprints.
ACTION: ADD IF EXACT / ARCHIVE NON-BLOCKING

### 18. Lancia Lybra `IL-likely`
MODEL: Lancia Lybra
CURRENT VALUE: Empty `IL-likely|Lancia|Lybra`; raw says 1999/2005 1.8 131 manual sedan FWD.
PROBLEM: Weak likely profile; RUN 1 already has `IL-confirmed|Lancia|Lybra` row.
WEB-VALIDATED FACT: Do not create duplicate clean profiles for same model/scope. Exact Israeli source for this likely profile is not embedded.
SOURCE:
- RUN 1 cumulative task / repo-local sources if any.
TARGET VALUE:
- Merge into `IL-confirmed|Lancia|Lybra` only if exact local source supports and not duplicate.
- Otherwise archive this likely profile non-blocking with lineage to confirmed Lybra.
ACTION: MERGE / ARCHIVE NON-BLOCKING / ALIAS

### 19. Lancia Musa
MODEL: Lancia Musa
CURRENT VALUE: Empty `global-reference-only|Lancia|Musa`.
PROBLEM: Global-reference-only with no Israeli technical rows.
WEB-VALIDATED FACT: No embedded Israeli source supports a clean Israeli Musa row.
SOURCE: none sufficient.
TARGET VALUE:
- Archive non-blocking with `reason=global_reference_only_no_israeli_market_grounding`.
ACTION: ARCHIVE NON-BLOCKING

### 20. Lancia Phedra
MODEL: Lancia Phedra
CURRENT VALUE: Empty `global-reference-only|Lancia|Phedra`; raw values include 2.0 petrol, 2.2 JTD, 3.0 V6.
PROBLEM: Global-reference-only minivan with no embedded Israeli market support.
WEB-VALIDATED FACT: No sufficient Israeli source is embedded for clean Israeli Phedra technical rows.
SOURCE: raw/global payload only.
TARGET VALUE:
- Archive non-blocking with raw fingerprints and reason `global_reference_only_no_israeli_market_grounding`.
ACTION: ARCHIVE NON-BLOCKING

### 21. Lancia Thema `global-reference-only`
MODEL: Lancia Thema
CURRENT VALUE: `global-reference-only|Lancia|Thema` has two 3.0 V6 diesel RWD rows 190 hp / 239 hp but no `source_indexes`.
PROBLEM: Source/indexing blocker plus wrong scope: global-reference-only should not be clean. The rows may be local catalog but not official importer.
WEB-VALIDATED FACT: Autoboom Israel supports Thema 2011-2014 3.0 diesel variants. Global sources also support 190 hp and 239 hp 3.0 V6 diesel/RWD/automatic. But this is not strong enough to keep as regular `global-reference-only` clean; use IL-likely/historical or archive non-blocking.
SOURCE:
- Repo-local Autoboom Israel Thema source.
- Global cross-check for 3.0 V6 diesel 190/239 hp.
TARGET VALUE:
- If repo policy allows Autoboom as Tier 3 historical Israeli catalog, move rows to `IL-likely|Lancia|Thema` or merge into existing `IL-confirmed|Lancia|Thema` lineage as non-blocking historical rows with source indexes.
- Otherwise archive non-blocking.
- If keeping rows, add `source_indexes=[1]`, field_sources for all non-null fields, and `support_level=indirect`/Tier 3, not direct official.
ACTION: MOVE TO REVIEW / FIX SOURCE INDEXES / ARCHIVE NON-BLOCKING

### 22. Lexus LX `global-reference-only`
MODEL: Lexus LX
CURRENT VALUE: Empty `global-reference-only|Lexus|LX`; duplicate/weak review profile while RUN 3 already covers `IL-confirmed|Lexus|LX`.
PROBLEM: Duplicate global scope. Must not leave a separate global LX blocker.
WEB-VALIDATED FACT: Lexus Israel states LX 600 launched in Israel in 2022. Auto.co.il and Israeli price-list sources support LX600 3.4/3.5 V6 twin-turbo 409 hp, 10-speed automatic, 4WD, and Yad2/Carzone list 2026 LX600 plus LX700h, but Lexus Israel places LX under car-history rather than current new-cars page.
SOURCE:
- `https://www.lexus.co.il/car-history/lx`
- `https://www.auto.co.il/articles/test-drives/road-tests/135974/`
- `https://www.yad2.co.il/price-list/feed?manufacturer=26&model=10324`
- `https://www.carzone.co.il/Lexus/LX/2026/`
TARGET VALUE:
- Do not keep separate `global-reference-only|Lexus|LX` as active review/blocker.
- Merge/alias it into `IL-confirmed|Lexus|LX` from RUN 3 or archive non-blocking duplicate.
- If RUN 3 clean LX exists, ensure it contains/keeps grounded LX 570 historical and LX 600 local launch rows only; add LX700h only if repo-local Israeli 2026 source is allowed and fields fully sourced.
ACTION: MERGE / ALIAS / ARCHIVE NON-BLOCKING

## FINAL alias/unmatched/casing/reporting cleanup
MODEL: batch-level reporting
CURRENT VALUE: `unmatched_output_keys_count=0`; split aliases exist in clean file; quality scan stale/has findings; readiness not ready.
PROBLEM: Final state must be computed from generated files after fixes, not stale reports.
WEB-VALIDATED FACT: Not applicable — repo-local consistency task.
SOURCE: actual uploaded ZIP/readiness/quality/review/archive files.
TARGET VALUE:
- Rebuild/refresh readiness, review, archive, and quality scan after applying fixes.
- Confirm `unmatched_output_keys_count=0` and sample empty.
- Do not regress cursor from `IL-confirmed|Lexus|RC`; next key must remain `IL-confirmed|Lexus|RX` unless the repo's actual source window logic proves otherwise.
- Ensure no model remains both clean and archive unless archive entry is explicitly non-blocking lineage/duplicate alias.
- All archive/review records created by this task must have `non_blocking=true`, `reason`, and lineage/source key.
ACTION: CODE / REPORTING FIX

