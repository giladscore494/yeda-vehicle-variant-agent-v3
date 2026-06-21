# BATCH26 FINAL RUN — blockers / review-only / unmatched / split-alias cleanup

TEMPORARY FILE RULE: This is a temporary instruction file. After applying and verifying Batch 26, delete `codex_tasks/BATCH26_*.md` from the repo before final commit unless the user explicitly asks to keep audit docs.

DO NOT BROWSE THE INTERNET.
All web-validation facts and target corrections are embedded here and in repo-local sources. Use this task as the single source of truth for blockers/review cleanup.

## Scope

```text
FINAL RUN blockers/review profiles: 31
unmatched_output_keys_count: 0
split_profile_alias_count: 30
quality_scan_stale: True
```

## Required global cleanup

- Clear all review-only blockers by either creating a grounded clean profile, merging into an existing clean profile, or moving to non-blocking archive/review with reason and lineage.
- Do not promote global-reference-only data to clean without Israeli evidence.
- Resolve clean/review/global duplicates from RUN 1-7.
- Rebuild readiness and quality scan so they are fresh.
- `unmatched_output_keys_count` must remain 0.
- Final goals: models_blocked=0, review_only_blocked_entries=0, duplicate_technical_variants=0, invalid_source_references=0, unknown_support_values=0, ready_for_website_upload=true, active blocked=0, quality bug findings=0, quality normalization findings=0.

## Blocker decisions


---

## MODEL: IL-confirmed|Lexus|RZ

CURRENT VALUE: review/blocker profile; variants=0; error='Extra data: line 211 column 1 (char 4666)'; raw_database_values={"years_seen": [2022, 2024, 2026], "trims_seen": ["300e", "450e"], "engines_seen": ["Dual Electric Motors, 313 hp (230 kW)", "Single Electric Motor, 204 hp (150 kW)"], "horsepower_seen": [], "transmissions_seen": ["single-speed EV"], "body_types_seen": ["SUV"], "fuel_types_seen": ["Electric"], "drivetrains_seen": ["AWD", "FWD"]}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Official Lexus Israel new-car/catalog pages support RX current 2026 with RX 350h/RX 450h+/RX 500h families, UX 2.0 HEV and RZ electric SUV. Use Lexus official pages/PDF before marketplace sources. For older SC 430/RX/UX generations, use repo-local iCar/Auto/Cartube sources; if no Israeli source exists, do not force global-only into clean.

SOURCE:
- https://www.lexus.co.il/new-cars/rx
- https://www.lexus.co.il/new-cars/rx/specifications
- https://www.lexus.co.il/new-cars/rz
- https://www.lexus.co.il/new-cars/ux/prices-and-costs
- https://www.lexus.co.il/new-cars

TARGET VALUE: Use raw_database_values plus repo-local Israeli sources and embedded source package to build a clean profile; if exact field grounding is insufficient, archive non-blocking with reason instead of fabricating.

ACTION: FIX/ADD GROUNDED CLEAN PROFILE


---

## MODEL: IL-confirmed|Lotus|Eletre

CURRENT VALUE: review/blocker profile; variants=0; error='Gemini catalog client returned non-object JSON'; raw_database_values={"years_seen": [2024, 2026], "trims_seen": ["Base", "R"], "engines_seen": ["Dual Electric Motor, 112 kWh, 603 hp", "Dual Electric Motor, 112 kWh, 905 hp"], "horsepower_seen": [], "transmissions_seen": ["2-speed EV", "Single-speed EV"], "body_types_seen": ["SUV"], "fuel_types_seen": ["Electric"], "drivetrains_seen": ["AWD"]}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Lotus Israel evidence is weak/patchy in the repo window. Eletre is in review, Emira/Elise/Evora clean profiles require Israeli support. Global-only Elise/Evora/Exige must not remain separate clean profiles if IL-confirmed/IL-likely equivalents exist or if no Israeli source supports them.

SOURCE:
- https://www.icar.co.il/

TARGET VALUE: Use raw_database_values plus repo-local Israeli sources and embedded source package to build a clean profile; if exact field grounding is insufficient, archive non-blocking with reason instead of fabricating.

ACTION: FIX/ADD GROUNDED CLEAN PROFILE


---

## MODEL: global-reference-only|Lotus|Exige

CURRENT VALUE: review/blocker profile; variants=0; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. Global-reference-only profile is insufficient for verified Israeli clean without Israeli evidence.

WEB-VALIDATED FACT: Lotus Israel evidence is weak/patchy in the repo window. Eletre is in review, Emira/Elise/Evora clean profiles require Israeli support. Global-only Elise/Evora/Exige must not remain separate clean profiles if IL-confirmed/IL-likely equivalents exist or if no Israeli source supports them.

SOURCE:
- https://www.icar.co.il/

TARGET VALUE: No grounded variant rows in review. Do not fabricate clean; archive non-blocking unless repo-local Israeli evidence fully grounds a profile.

ACTION: ARCHIVE NON-BLOCKING / KEEP REVIEW NON-BLOCKING


---

## MODEL: IL-likely|Lynk & Co|02

CURRENT VALUE: review/blocker profile; variants=1; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. IL-likely requires explicit Israeli evidence for clean; otherwise non-blocking review/archive.

WEB-VALIDATED FACT: Lynk & Co 01 is the supported Israeli-market model in this window; 02 is review/likely and should not be promoted without Israeli source support.

SOURCE:
- https://www.icar.co.il/
- repo source: [1] לינק אנד קו 02 החשמלי 2025 נחשף - בישראל בתחילת השנה (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9C%D7%99%D7%A0%D7%A7-%D7%90%D7%A0%D7%93-%D7%A7%D7%95-02-%D7%94%D7%97%D7%A9%D7%9E%D7%9C%D7%99-2025-%D7%A0%D7%97%D7%A9%D7%A3-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%91%D7%AA%D7%97%D7%99%D7%9C%D7%AA-%D7%94%D7%A9%D7%A0%D7%94

TARGET VALUE: Repair missing/invalid fields and move to clean only if grounded; otherwise non-blocking archive with lineage.

ACTION: FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING

### Existing review variant decisions

| # | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---:|---|---|---|---|
| 1 | trim=None; years=2025-None; body=Crossover; fuel=electric; engine=electric; displacement=None; hp=272; trans=None; drive=RWD | EV schema incomplete/invalid: transmission=single_speed/direct_drive | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |

---

## MODEL: global-reference-only|Mahindra|Scorpio

CURRENT VALUE: review/blocker profile; variants=0; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. Global-reference-only profile is insufficient for verified Israeli clean without Israeli evidence.

WEB-VALIDATED FACT: Israeli source support required; global-only is not enough.

SOURCE:

TARGET VALUE: No grounded variant rows in review. Do not fabricate clean; archive non-blocking unless repo-local Israeli evidence fully grounds a profile.

ACTION: ARCHIVE NON-BLOCKING / KEEP REVIEW NON-BLOCKING


---

## MODEL: global-reference-only|Mahindra|Thar

CURRENT VALUE: review/blocker profile; variants=0; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. Global-reference-only profile is insufficient for verified Israeli clean without Israeli evidence.

WEB-VALIDATED FACT: Israeli source support required; global-only is not enough.

SOURCE:

TARGET VALUE: No grounded variant rows in review. Do not fabricate clean; archive non-blocking unless repo-local Israeli evidence fully grounds a profile.

ACTION: ARCHIVE NON-BLOCKING / KEEP REVIEW NON-BLOCKING


---

## MODEL: global-reference-only|Mahindra|XUV500

CURRENT VALUE: review/blocker profile; variants=0; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. Global-reference-only profile is insufficient for verified Israeli clean without Israeli evidence.

WEB-VALIDATED FACT: Israeli source support required; global-only is not enough.

SOURCE:
- repo source: [0] Mahindra Models Catalog - Auto.co.il (editorial) — https://www.auto.co.il/catalog/brands/mahindra
- repo source: [1] Mahindra Israel Catalog - iCar (editorial) — https://www.icar.co.il/מהינדרה/

TARGET VALUE: No grounded variant rows in review. Do not fabricate clean; archive non-blocking unless repo-local Israeli evidence fully grounds a profile.

ACTION: ARCHIVE NON-BLOCKING / KEEP REVIEW NON-BLOCKING


---

## MODEL: IL-confirmed|Maserati|Levante

CURRENT VALUE: review/blocker profile; variants=5; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Maserati Israel official pages list Israeli-market models; Cartube price/spec pages list 2026 Ghibli/GranTurismo/GranCabrio/Grecale/Levante/Quattroporte/MC20. Merge IL-likely duplicates into IL-confirmed profiles and preserve aliases.

SOURCE:
- https://www.maserati.com/il/he
- https://www.maserati.com/il/he/models
- https://www.cartube.co.il/מחירון-רכב-חדש/מזראטי
- repo source: [2400] מזראטי לבנטה בישראל - מחיר החל מ-610,000 שקל (editorial) — https://www.cartube.co.il/חדשות-רכב/מזראטי-לבנטה-בישראל-מחיר-החל-מ-610,000-שקל
- repo source: [2401] מזראטי לבנטה טרופאו 580 כ"ס בישראל - מחיר החל מ-1,250,000 שקל (editorial) — https://www.cartube.co.il/חדשות-רכב/מזראטי-לבנטה-טרופאו-580-כ-ס-בישראל-מחיר-החל-מ-1,250,000-שקל
- repo source: [2402] מזראטי לבנטה הייבריד 2021 בישראל - מחיר החל מ-629,000 שקל (editorial) — https://www.cartube.co.il/חדשות-רכב/מזראטי-לבנטה-הייבריד-2021-בישראל-מחיר-החל-מ-629,000-שקל
- repo source: [2403] מזראטי לבנטה - מחירון רכב, מפרט טכני (catalog) — https://www.icar.co.il/מזראטי/מזראטי_לבנטה/מזראטי_לבנטה_חדש/

TARGET VALUE: Repair missing/invalid fields and move to clean only if grounded; otherwise non-blocking archive with lineage.

ACTION: FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING

### Existing review variant decisions

| # | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---:|---|---|---|---|
| 1 | trim='Diesel'; years=2016-2019; body=SUV; fuel=diesel; engine=3.0L v6 turbo; displacement=3.0; hp=275; trans=8-speed automatic; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 2 | trim=None; years=2016-2021; body=SUV; fuel=petrol; engine=3.0L v6 twin-turbo; displacement=3.0; hp=350; trans=8-speed automatic; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 3 | trim='S'; years=2016-2024; body=SUV; fuel=petrol; engine=3.0L v6 twin-turbo; displacement=3.0; hp=430; trans=8-speed automatic; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 4 | trim='Trofeo'; years=2019-2024; body=SUV; fuel=petrol; engine=3.8L v8 twin-turbo; displacement=3.8; hp=580; trans=8-speed automatic; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 5 | trim='Hybrid'; years=2021-2024; body=SUV; fuel=mild_hybrid; engine=2.0L i4 turbo; displacement=2.0; hp=330; trans=8-speed automatic; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mazda|CX-30

CURRENT VALUE: review/blocker profile; variants=0; error="Expecting ',' delimiter: line 26 column 40 (char 660)"; raw_database_values={"years_seen": [2019, 2021, 2026], "trims_seen": [], "engines_seen": ["2.0L Skyactiv-G, 165 hp", "2.5L Skyactiv-G, 195 hp"], "horsepower_seen": [], "transmissions_seen": ["6-speed automatic"], "body_types_seen": ["Crossover SUV"], "fuel_types_seen": ["Mild Hybrid", "Petrol"], "drivetrains_seen": ["FWD"]}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד

TARGET VALUE: Use raw_database_values plus repo-local Israeli sources and embedded source package to build a clean profile; if exact field grounding is insufficient, archive non-blocking with reason instead of fabricating.

ACTION: FIX/ADD GROUNDED CLEAN PROFILE


---

## MODEL: IL-confirmed|Mazda|CX-90

CURRENT VALUE: review/blocker profile; variants=0; error='Extra data: line 133 column 1 (char 2928)'; raw_database_values={"years_seen": [2023, 2026], "trims_seen": ["Exclusive"], "engines_seen": ["3.3L e-Skyactiv G Turbo MHEV, 345 hp"], "horsepower_seen": [], "transmissions_seen": ["8-speed automatic"], "body_types_seen": ["SUV"], "fuel_types_seen": ["Mild Hybrid"], "drivetrains_seen": ["AWD"]}

PROBLEM: Active blocker/review-only entry. Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only|Mazda|CX-90'].

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד

TARGET VALUE: Use raw_database_values plus repo-local Israeli sources and embedded source package to build a clean profile; if exact field grounding is insufficient, archive non-blocking with reason instead of fabricating.

ACTION: FIX/ADD GROUNDED CLEAN PROFILE


---

## MODEL: IL-confirmed|Mazda|Mazda6

CURRENT VALUE: review/blocker profile; variants=0; error='Gemini catalog client returned non-object JSON'; raw_database_values={"years_seen": [2002, 2007, 2008, 2012, 2013, 2024], "trims_seen": ["Executive", "Luxury", "Premium", "Signature"], "engines_seen": ["2.0L MZR Petrol", "2.0L Skyactiv-G Petrol", "2.3L MZR Petrol", "2.5L MZR Petrol", "2.5L Skyactiv-G Petrol"], "horsepower_seen": [], "transmissions_seen": ["5-speed automatic", "6-speed automatic", "Automatic"], "body_types_seen": ["Hatchback", "Sedan", "Wagon"], "fuel_types_seen": ["Petrol"], "drivetrains_seen": ["FWD"]}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד

TARGET VALUE: Use raw_database_values plus repo-local Israeli sources and embedded source package to build a clean profile; if exact field grounding is insufficient, archive non-blocking with reason instead of fabricating.

ACTION: FIX/ADD GROUNDED CLEAN PROFILE


---

## MODEL: global-reference-only|Mazda|MX-30

CURRENT VALUE: review/blocker profile; variants=0; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. Global-reference-only profile has local sibling(s): ['IL-confirmed|Mazda|MX-30']. Do not keep as separate clean Israeli profile.

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד

TARGET VALUE: No grounded variant rows in review. Do not fabricate clean; archive non-blocking unless repo-local Israeli evidence fully grounds a profile.

ACTION: ARCHIVE NON-BLOCKING / KEEP REVIEW NON-BLOCKING


---

## MODEL: IL-confirmed|McLaren|720S

CURRENT VALUE: review/blocker profile; variants=0; error='Extra data: line 162 column 1 (char 3251)'; raw_database_values={"years_seen": [2017, 2019, 2023], "trims_seen": [], "engines_seen": ["4.0L V8 Twin-Turbo, 720 PS"], "horsepower_seen": [], "transmissions_seen": ["7-speed DCT"], "body_types_seen": ["Convertible", "Coupe"], "fuel_types_seen": ["Petrol"], "drivetrains_seen": ["RWD"]}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: McLaren profiles rely on niche Israeli import/market evidence. Keep only if repo-local Israeli source supports the model; otherwise archive/review non-blocking rather than treating global specs as clean Israeli data.

SOURCE:
- https://www.icar.co.il/

TARGET VALUE: No grounded variant rows in review. Do not fabricate clean; archive non-blocking unless repo-local Israeli evidence fully grounds a profile.

ACTION: ARCHIVE NON-BLOCKING / KEEP REVIEW NON-BLOCKING


---

## MODEL: IL-confirmed|Mercedes-Benz|CLK

CURRENT VALUE: review/blocker profile; variants=20; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/
- repo source: [1] מרצדס CLK קופה (2002-2009) מפרט טכני - iCar (editorial) — https://www.icar.co.il/mercedes-benz/clk/coupe/
- repo source: [2] מרצדס CLK קבריולה (2003-2010) - מחירון ומידע טכני - iCar (editorial) — https://www.icar.co.il/mercedes-benz/clk/cabriolet/
- repo source: [3] מרצדס CLK דור 1 (1997-2002) - קטלוג רכב - אוטו (editorial) — https://www.auto.co.il/catalog/mercedes/clk/1997-2002
- repo source: [4] מחירון רכב יצחק לוי - מרצדס CLK (catalog) — https://www.winwin.co.il/Cars/Mehiron/Search.aspx?Make=מרצדס&Model=CLK

TARGET VALUE: Repair missing/invalid fields and move to clean only if grounded; otherwise non-blocking archive with lineage.

ACTION: FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING

### Existing review variant decisions

| # | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---:|---|---|---|---|
| 1 | trim='200 Kompressor'; years=1997-2000; body=Coupe; fuel=petrol; engine=2.0L supercharged; displacement=2.0; hp=192; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 2 | trim='200 Kompressor'; years=2000-2002; body=Coupe; fuel=petrol; engine=2.0L supercharged; displacement=2.0; hp=163; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 3 | trim='230 Kompressor'; years=1997-2000; body=Coupe; fuel=petrol; engine=2.3L supercharged; displacement=2.3; hp=193; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 4 | trim='230 Kompressor'; years=2000-2002; body=Coupe; fuel=petrol; engine=2.3L supercharged; displacement=2.3; hp=197; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 5 | trim='320'; years=1997-2005; body=Coupe; fuel=petrol; engine=3.2L v6; displacement=3.2; hp=218; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 6 | trim='200 Kompressor'; years=1998-2000; body=Convertible; fuel=petrol; engine=2.0L supercharged; displacement=2.0; hp=192; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 7 | trim='200 Kompressor'; years=2000-2002; body=Convertible; fuel=petrol; engine=2.0L supercharged; displacement=2.0; hp=163; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 8 | trim='230 Kompressor'; years=1998-2000; body=Convertible; fuel=petrol; engine=2.3L supercharged; displacement=2.3; hp=193; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 9 | trim='230 Kompressor'; years=2000-2002; body=Convertible; fuel=petrol; engine=2.3L supercharged; displacement=2.3; hp=197; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 10 | trim='320'; years=1998-2005; body=Convertible; fuel=petrol; engine=3.2L v6; displacement=3.2; hp=218; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 11 | trim='200 Kompressor'; years=2002-2006; body=Coupe; fuel=petrol; engine=1.8L supercharged; displacement=1.8; hp=163; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 12 | trim='200 Kompressor'; years=2007-2009; body=Coupe; fuel=petrol; engine=1.8L supercharged; displacement=1.8; hp=184; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 13 | trim='240'; years=2002-2005; body=Coupe; fuel=petrol; engine=2.6L v6; displacement=2.6; hp=170; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 14 | trim='280'; years=2006-2009; body=Coupe; fuel=petrol; engine=3.0L v6; displacement=3.0; hp=231; trans=7-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 15 | trim='350'; years=2005-2009; body=Coupe; fuel=petrol; engine=3.5L v6; displacement=3.5; hp=272; trans=7-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 16 | trim='200 Kompressor'; years=2003-2006; body=Convertible; fuel=petrol; engine=1.8L supercharged; displacement=1.8; hp=163; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 17 | trim='200 Kompressor'; years=2007-2010; body=Convertible; fuel=petrol; engine=1.8L supercharged; displacement=1.8; hp=184; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 18 | trim='240'; years=2003-2005; body=Convertible; fuel=petrol; engine=2.6L v6; displacement=2.6; hp=170; trans=5-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 19 | trim='280'; years=2006-2010; body=Convertible; fuel=petrol; engine=3.0L v6; displacement=3.0; hp=231; trans=7-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 20 | trim='350'; years=2005-2010; body=Convertible; fuel=petrol; engine=3.5L v6; displacement=3.5; hp=272; trans=7-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mercedes-Benz|EQA

CURRENT VALUE: review/blocker profile; variants=3; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only|Mercedes-Benz|EQA'].

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/
- repo source: [0] מרצדס EQA - מחירון, מפרטים, אבזור (editorial) — https://www.icar.co.il/mercedes-benz/mercedes-benz_eqa/
- repo source: [1] Mercedes-Benz EQA מפרט טכני (official_importer) — https://www.mercedes-benz.co.il/models/eqa/
- repo source: [2] מרצדס EQA החשמלי בישראל - מחיר החל מ- 289,900 שקלים (editorial) — https://www.cartube.co.il/חדשות-רכב/מרצדס-eqa-החשמלי-בישראל-מחיר-החל-מ-299900-שקלים

TARGET VALUE: Repair missing/invalid fields and move to clean only if grounded; otherwise non-blocking archive with lineage.

ACTION: FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING

### Existing review variant decisions

| # | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---:|---|---|---|---|
| 1 | trim='250'; years=2021-2024; body=SUV; fuel=electric; engine=electric; displacement=None; hp=190; trans=single_speed; drive=FWD | Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only/Mercedes-Benz/EQA']. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 2 | trim='250+'; years=2022-2024; body=SUV; fuel=electric; engine=electric; displacement=None; hp=190; trans=single_speed; drive=FWD | Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only/Mercedes-Benz/EQA']. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 3 | trim='300 4MATIC'; years=2021-2024; body=SUV; fuel=electric; engine=electric; displacement=None; hp=228; trans=single_speed; drive=AWD | Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only/Mercedes-Benz/EQA']. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |

---

## MODEL: global-reference-only|Mercedes-Benz|EQB

CURRENT VALUE: review/blocker profile; variants=3; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. Global-reference-only profile has local sibling(s): ['IL-confirmed|Mercedes-Benz|EQB']. Do not keep as separate clean Israeli profile.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/
- repo source: [1] מרצדס EQB - מחירון, מפרט טכני וחוות דעת (israeli_car_catalog) — https://www.icar.co.il/mercedes-benz/mercedes-benz_eqb/
- repo source: [2] מרצדס EQB מפרט טכני מלא - קולמוביל (official_importer) — https://www.mercedes-benz.co.il/models/eqb/

TARGET VALUE: Repair missing/invalid fields and move to clean only if grounded; otherwise non-blocking archive with lineage.

ACTION: FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING

### Existing review variant decisions

| # | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---:|---|---|---|---|
| 1 | trim=None; years=2022-2024; body=SUV; fuel=electric; engine=electric; displacement=None; hp=190; trans=single_speed; drive=FWD | Global-reference-only profile has local sibling(s): ['IL-confirmed/Mercedes-Benz/EQB']. Do not keep as separate clean Israeli profile. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 2 | trim=None; years=2022-2024; body=SUV; fuel=electric; engine=electric; displacement=None; hp=228; trans=single_speed; drive=AWD | Global-reference-only profile has local sibling(s): ['IL-confirmed/Mercedes-Benz/EQB']. Do not keep as separate clean Israeli profile. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 3 | trim=None; years=2022-2024; body=SUV; fuel=electric; engine=electric; displacement=None; hp=292; trans=single_speed; drive=AWD | Global-reference-only profile has local sibling(s): ['IL-confirmed/Mercedes-Benz/EQB']. Do not keep as separate clean Israeli profile. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mercedes-Benz|EQE

CURRENT VALUE: review/blocker profile; variants=7; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/
- repo source: [0] מרצדס EQE בישראל - מחיר החל מ- 499,900 שקל (editorial) — https://www.cartube.co.il/חדשות-רכב/מרצדס-eqe-בישראל-מחיר-החל-מ-499-900-שקל
- repo source: [1] מרצדס EQE מקבלת גרסת בסיס חדשה - EQE 300 - מחיר מ-470 אלף שקל (editorial) — https://www.cartube.co.il/חדשות-רכב/מרצדס-eqe-מקבלת-גרסת-בסיס-חדשה-eqe-300-מחיר-מ-470-אלף-שקל
- repo source: [2] מרצדס EQE SUV החדש 2023 בישראל - מחירים החל מ-869,900 שקל (editorial) — https://www.cartube.co.il/חדשות-רכב/מרצדס-eqe-suv-החדש-2023-בישראל-מחירים-החל-מ-869-900-שקל
- repo source: [3] מרצדס EQE החדשה - מחירון, מפרטים, ואביזרים (editorial) — https://www.icar.co.il/מרצדס/מרצדס_EQE/
- repo source: [4] מרצדס EQE SUV החדש - מחירון, מפרטים, ואביזרים (editorial) — https://www.icar.co.il/מרצדס/מרצדס_EQE_SUV/

TARGET VALUE: Repair missing/invalid fields and move to clean only if grounded; otherwise non-blocking archive with lineage.

ACTION: FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING

### Existing review variant decisions

| # | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---:|---|---|---|---|
| 1 | trim='300'; years=2022-None; body=Sedan; fuel=electric; engine=electric; displacement=None; hp=245; trans=single_speed; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 2 | trim='350+'; years=2022-None; body=Sedan; fuel=electric; engine=electric; displacement=None; hp=292; trans=single_speed; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 3 | trim='AMG 43 4MATIC'; years=2022-None; body=Sedan; fuel=electric; engine=electric; displacement=None; hp=476; trans=single_speed; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 4 | trim='300'; years=2023-None; body=SUV; fuel=electric; engine=electric; displacement=None; hp=245; trans=single_speed; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 5 | trim='350 4MATIC'; years=2023-None; body=SUV; fuel=electric; engine=electric; displacement=None; hp=292; trans=single_speed; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 6 | trim='500 4MATIC'; years=2023-None; body=SUV; fuel=electric; engine=electric; displacement=None; hp=408; trans=single_speed; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 7 | trim='AMG 43 4MATIC'; years=2023-None; body=SUV; fuel=electric; engine=electric; displacement=None; hp=476; trans=single_speed; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mercedes-Benz|EQE SUV

CURRENT VALUE: review/blocker profile; variants=4; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/
- repo source: [0] מרצדס EQE SUV החשמלי בישראל - מחיר החל מ- 739,900 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-eqe-suv-%D7%94%D7%97%D7%A9%D7%9E%D7%9C%D7%99-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-739900-%D7%A9%D7%A7%D7%9C
- repo source: [1] מרצדס EQE SUV - מפרט טכני (catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_EQE_SUV/

TARGET VALUE: Repair missing/invalid fields and move to clean only if grounded; otherwise non-blocking archive with lineage.

ACTION: FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING

### Existing review variant decisions

| # | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---:|---|---|---|---|
| 1 | trim='300'; years=2023-None; body=SUV; fuel=electric; engine=electric; displacement=None; hp=245; trans=single_speed; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 2 | trim='350 4MATIC'; years=2023-None; body=SUV; fuel=electric; engine=electric; displacement=None; hp=292; trans=single_speed; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 3 | trim='500 4MATIC'; years=2023-None; body=SUV; fuel=electric; engine=electric; displacement=None; hp=408; trans=single_speed; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 4 | trim='AMG 43 4MATIC'; years=2023-None; body=SUV; fuel=electric; engine=electric; displacement=None; hp=476; trans=single_speed; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mercedes-Benz|GL-Class

CURRENT VALUE: review/blocker profile; variants=5; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/
- repo source: [0] Mercedes GL-Class (2006-2012) Specifications & Trims (auto_catalog) — https://www.icar.co.il/mercedes-benz/gl-class/2006/
- repo source: [1] Mercedes GL-Class (2013-2015) Specifications & Trims (auto_catalog) — https://www.icar.co.il/mercedes-benz/gl-class/2013/
- repo source: [2] מרצדס GL החדש בישראל – מחיר החל מ- 695,000 שקל (editorial) — https://www.cartube.co.il/%d7%97%d7%93%d7%a9%d7%95%d7%aa-%d7%a8%d7%9b%d7%91/%d7%9e%d7%a8%d7%a6%d7%93%d7%a1-gl-%d7%94%d7%97%d7%93%d7%a9-%d7%91%d7%99%d7%a9%d7%a8%d7%90%d7%9c-%d7%9e%d7%97%d7%99%d7%a8-%d7%94%d7%97%d7%9c-%d7%9e-695-000-%d7%a9%d7%a7%d7%9c

TARGET VALUE: Repair missing/invalid fields and move to clean only if grounded; otherwise non-blocking archive with lineage.

ACTION: FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING

### Existing review variant decisions

| # | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---:|---|---|---|---|
| 1 | trim=None; years=2006-2009; body=SUV; fuel=diesel; engine=3.0L v6 turbo; displacement=3.0; hp=224; trans=7-speed automatic; drive=4WD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 2 | trim=None; years=2010-2012; body=SUV; fuel=diesel; engine=3.0L v6 turbo; displacement=3.0; hp=265; trans=7-speed automatic; drive=4WD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 3 | trim=None; years=2006-2012; body=SUV; fuel=petrol; engine=5.5L v8; displacement=5.5; hp=388; trans=7-speed automatic; drive=4WD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 4 | trim=None; years=2013-2015; body=SUV; fuel=diesel; engine=3.0L v6 turbo; displacement=3.0; hp=258; trans=7-speed automatic; drive=4WD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 5 | trim=None; years=2013-2015; body=SUV; fuel=petrol; engine=4.7L v8 turbo; displacement=4.7; hp=435; trans=7-speed automatic; drive=4WD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mercedes-Benz|GLE

CURRENT VALUE: review/blocker profile; variants=0; error='Gemini catalog client returned non-object JSON'; raw_database_values={"years_seen": [2015, 2019, 2020, 2026], "trims_seen": ["AMG GLE 53 4MATIC+", "AMG GLE 53 4MATIC+ Coupe", "GLE 350 d 4MATIC", "GLE 350 d 4MATIC Coupe", "GLE 350 de 4MATIC", "GLE 350 de 4MATIC Coupe", "GLE 450 4MATIC", "GLE 500 e 4MATIC"], "engines_seen": ["2.0L Inline-4 Turbo Diesel + Electric Motor (320 hp combined)", "3.0L Inline-6 Turbo Petrol MHEV (367 hp)", "3.0L Inline-6 Turbo Petrol MHEV (435 hp)", "3.0L V6 Bi-Turbo Petrol + Electric Motor (442 hp combined)", "3.0L V6 Turbo Diesel (258 hp)"], "horsepower_seen": [], "transmissions_seen": ["7-speed automatic (7G-TRONIC PLUS)", "9-speed automatic (9G-TRONIC)", "9-speed automatic (AMG SPEEDSHIFT TCT 9G)"], "body_types_seen": ["Coupe", "SUV"], "fuel_types_seen": ["Diesel", "Mild Hybrid", "Plug-in Hybrid"], "drivetrains_seen": ["AWD"]}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/

TARGET VALUE: Use raw_database_values plus repo-local Israeli sources and embedded source package to build a clean profile; if exact field grounding is insufficient, archive non-blocking with reason instead of fabricating.

ACTION: FIX/ADD GROUNDED CLEAN PROFILE


---

## MODEL: IL-confirmed|Mercedes-Benz|Maybach S-Class

CURRENT VALUE: review/blocker profile; variants=4; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/
- repo source: [0] מרצדס מייבאך S קלאס החדשה בישראל - מחיר החל מ-1.75 מיליון שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-%D7%9E%D7%99%D7%99%D7%91%D7%90%D7%9A-s-%D7%A7%D7%9C%D7%90%D7%A1-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1-75-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C
- repo source: [1] מרצדס S קלאס 2018 החדשה בישראל - מחיר החל מ- 1,050,000 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-s-%D7%A7%D7%9C%D7%90%D7%A1-2018-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1050000-%D7%A9%D7%A7%D7%9C
- repo source: [2] בישראל: מרצדס S500 מייבאך - מחיר החל מ-1.37 מיליון שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-s500-%D7%9E%D7%99%D7%99%D7%91%D7%90%D7%9A-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1-37-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C

TARGET VALUE: Repair missing/invalid fields and move to clean only if grounded; otherwise non-blocking archive with lineage.

ACTION: FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING

### Existing review variant decisions

| # | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---:|---|---|---|---|
| 1 | trim='S 500'; years=2015-2017; body=Sedan; fuel=petrol; engine=4.7L v8 twin-turbo; displacement=4.7; hp=455; trans=9-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 2 | trim='S 560'; years=2018-2020; body=Sedan; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=469; trans=9-speed automatic; drive=None | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 3 | trim='S 580 4MATIC'; years=2021-2024; body=Sedan; fuel=mild_hybrid; engine=4.0L v8 twin-turbo; displacement=4.0; hp=503; trans=9-speed automatic; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 4 | trim='S 680 4MATIC'; years=2021-2024; body=Sedan; fuel=petrol; engine=6.0L v12 twin-turbo; displacement=6.0; hp=612; trans=9-speed automatic; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mercedes-Benz|ML-Class

CURRENT VALUE: review/blocker profile; variants=0; error='Gemini catalog client returned non-object JSON'; raw_database_values={"years_seen": [1998, 1999, 2002, 2005, 2009, 2011, 2012, 2015], "trims_seen": ["ML 250 BlueTEC", "ML 270 CDI", "ML 320", "ML 320 CDI", "ML 350", "ML 350 BlueTEC", "ML 63 AMG"], "engines_seen": ["2.1L I4 Turbo Diesel", "2.7L I5 Turbo Diesel", "3.0L V6 Turbo Diesel", "3.2L V6 Petrol", "3.5L V6 Petrol", "5.5L V8 BiTurbo Petrol"], "horsepower_seen": [], "transmissions_seen": ["5-speed automatic", "7-speed automatic"], "body_types_seen": ["SUV"], "fuel_types_seen": ["Diesel", "Petrol"], "drivetrains_seen": ["4WD", "AWD"]}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/

TARGET VALUE: Use raw_database_values plus repo-local Israeli sources and embedded source package to build a clean profile; if exact field grounding is insufficient, archive non-blocking with reason instead of fabricating.

ACTION: FIX/ADD GROUNDED CLEAN PROFILE


---

## MODEL: IL-confirmed|Mercedes-Benz|S-Class Coupe

CURRENT VALUE: review/blocker profile; variants=2; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/
- repo source: [0] מרצדס S קלאס קופה בישראל – מחיר החל מ- 1.05 מיליון שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-s-%D7%A7%D7%9C%D7%90%D7%A1-%D7%A7%D7%95%D7%A4%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1-05-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C
- repo source: [1] מרצדס S-קלאס קופה 2014-2021 (catalog) — https://www.auto.co.il/model/mercedes-s-class-coupe_g1281
- repo source: [2] מרצדס S קלאס קופה וקבריולט 2018 החדשות בישראל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-s-%D7%A7%D7%9C%D7%90%D7%A1-%D7%A7%D7%95%D7%A4%D7%94-%D7%95%D7%A7%D7%91%D7%A8%D7%99%D7%95%D7%9C%D7%98-2018-%D7%94%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C

TARGET VALUE: Repair missing/invalid fields and move to clean only if grounded; otherwise non-blocking archive with lineage.

ACTION: FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING

### Existing review variant decisions

| # | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---:|---|---|---|---|
| 1 | trim='S 500'; years=2014-2018; body=Coupe; fuel=petrol; engine=4.7L v8 turbo; displacement=4.7; hp=455; trans=9-speed automatic; drive=None | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 2 | trim='S 560'; years=2018-2021; body=Coupe; fuel=petrol; engine=4.0L v8 turbo; displacement=4.0; hp=469; trans=9-speed automatic; drive=None | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mercedes-Benz|Sprinter

CURRENT VALUE: review/blocker profile; variants=0; error='Gemini catalog client returned non-object JSON'; raw_database_values={"years_seen": [2000, 2006, 2018, 2020, 2021, 2026], "trims_seen": ["313 CDI", "315 CDI", "316 CDI", "516 CDI", "519 CDI", "eSprinter"], "engines_seen": ["2.0L OM654 Turbo Diesel", "2.1L OM611 Turbo Diesel", "2.1L OM651 Turbo Diesel", "3.0L OM642 V6 Turbo Diesel", "Electric Motor"], "horsepower_seen": [], "transmissions_seen": ["5-speed manual", "6-speed manual", "7-speed automatic", "9-speed automatic", "single-speed EV"], "body_types_seen": ["Chassis Cab", "Minibus", "Panel Van"], "fuel_types_seen": ["Diesel", "Electric"], "drivetrains_seen": ["FWD", "RWD"]}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/

TARGET VALUE: Use raw_database_values plus repo-local Israeli sources and embedded source package to build a clean profile; if exact field grounding is insufficient, archive non-blocking with reason instead of fabricating.

ACTION: FIX/ADD GROUNDED CLEAN PROFILE


---

## MODEL: IL-confirmed|MG|ZS

CURRENT VALUE: review/blocker profile; variants=0; error="Expecting ',' delimiter: line 159 column 4 (char 3346)"; raw_database_values={"years_seen": [2018, 2019, 2021, 2022, 2026], "trims_seen": ["Net Up", "Net Up S"], "engines_seen": ["1.0L Turbo petrol, 111 hp", "Single electric motor, 143 hp (105 kW)", "Single electric motor, 156 hp (115 kW), Long Range (70 kWh)", "Single electric motor, 177 hp (130 kW), Standard Range (50.3 kWh)"], "horsepower_seen": [], "transmissions_seen": ["6-speed automatic", "Single-speed EV"], "body_types_seen": ["SUV"], "fuel_types_seen": ["Electric", "Petrol"], "drivetrains_seen": ["FWD"]}

PROBLEM: Active blocker/review-only entry. Use this as primary Israeli profile and fold duplicate sibling(s): ['IL-likely|MG|ZS', 'global-reference-only|MG|ZS'].

WEB-VALIDATED FACT: MG Israel official catalog supports current MG3 Hybrid+, MG4, MG5, HS, Marvel R, Cyberster, ZS Hybrid/EV families; Cartube/Carzone/iCar support prices/specs. ZS has clean global/likely duplicates plus IL-confirmed review blocker; resolve to one Israeli profile.

SOURCE:
- https://mg-israel.co.il/model/
- https://mg-israel.co.il/model/zs-hybrid/
- https://mg-israel.co.il/model/mg4-x-power/
- https://www.cartube.co.il/מחירון-רכב-חדש/mg
- https://www.icar.co.il/סאיק-MG/

TARGET VALUE: Use raw_database_values plus repo-local Israeli sources and embedded source package to build a clean profile; if exact field grounding is insufficient, archive non-blocking with reason instead of fabricating.

ACTION: FIX/ADD GROUNDED CLEAN PROFILE


---

## MODEL: IL-likely|MG (British era)|ZT

CURRENT VALUE: review/blocker profile; variants=0; error='Extra data: line 115 column 1 (char 2315)'; raw_database_values={"years_seen": [2002, 2005], "trims_seen": ["160"], "engines_seen": ["1.8L Turbo petrol, 160 PS"], "horsepower_seen": [], "transmissions_seen": ["5-speed manual"], "body_types_seen": ["Sedan"], "fuel_types_seen": ["Petrol"], "drivetrains_seen": ["FWD"]}

PROBLEM: Active blocker/review-only entry. IL-likely duplicate has IL-confirmed sibling(s): ['IL-confirmed|MG (British era)|ZT']. Merge into confirmed profile with alias/lineage.

WEB-VALIDATED FACT: British-era MG ZT is weak/historical; keep only as historical Tier 2/3 Israeli support if repo-local source confirms, otherwise review/archive non-blocking.

SOURCE:
- https://www.icar.co.il/

TARGET VALUE: No grounded variant rows in review. Do not fabricate clean; archive non-blocking unless repo-local Israeli evidence fully grounds a profile.

ACTION: ARCHIVE NON-BLOCKING / KEEP REVIEW NON-BLOCKING


---

## MODEL: IL-confirmed|Mini|Coupe

CURRENT VALUE: review/blocker profile; variants=3; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: MINI Israel official pages support current Countryman, Aceman and Cabrio; official PDFs support Cooper SE. Historical Clubman/Cooper/Countryman/Paceman/Coupe/Roadster require iCar/Auto/Tier2 support. Merge likely/global duplicates into confirmed profiles.

SOURCE:
- https://www.mini.co.il/he_IL/home.html
- https://www.mini.co.il/he_IL/home/range/mini-countryman.html
- https://www.mini.co.il/he_IL/home/range/mini-cooper-convertible.html
- https://www.mini.co.il/content/dam/MINI/marketIL/mini_co_il/Catalogues/BEV_2020/200630_27013_Mini_Electric_Cooper_SE%28split%29_9-6-2020.pdf
- repo source: [0] מיני קופה בישראל – החל מ-160,000 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%99%D7%A0%D7%99-%D7%A7%D7%95%D7%A4%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%E2%80%93-%D7%94%D7%97%D7%9C-%D7%9E-160-000-%D7%A9%D7%A7%D7%9C
- repo source: [1] מיני קופה (2011-2015) יחירון ומפרט טכני (catalog) — https://www.icar.co.il/%D7%9E%D7%99%D7%A0%D7%99/%D7%9E%D7%99%D7%A0%D7%99_%D7%A7%D7%95%D7%A4%D7%94/%D7%9E%D7%99%D7%A0%D7%99_%D7%A7%D7%95%D7%A4%D7%94_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%99%D7%94_%D7%93%D7%95%D7%A8_1/

TARGET VALUE: Repair missing/invalid fields and move to clean only if grounded; otherwise non-blocking archive with lineage.

ACTION: FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING

### Existing review variant decisions

| # | CURRENT VALUE | PROBLEM | TARGET VALUE | ACTION |
|---:|---|---|---|---|
| 1 | trim='Cooper'; years=2011-2015; body=Coupe; fuel=petrol; engine=1.6L; displacement=1.6; hp=122; trans=6-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 2 | trim='Cooper S'; years=2011-2015; body=Coupe; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=184; trans=6-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |
| 3 | trim='John Cooper Works'; years=2011-2015; body=Coupe; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=211; trans=6-speed manual; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Repair/ground or archive with lineage; do not leave active blocker. | FIX EXISTING REVIEW VARIANTS OR ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mini|Roadster

CURRENT VALUE: review/blocker profile; variants=0; error='Extra data: line 261 column 1 (char 5392)'; raw_database_values={"years_seen": [2012, 2015], "trims_seen": ["Cooper", "Cooper S"], "engines_seen": ["1.6L naturally aspirated petrol, 122 hp", "1.6L turbo petrol, 184 hp"], "horsepower_seen": [], "transmissions_seen": ["6-speed automatic"], "body_types_seen": ["Roadster"], "fuel_types_seen": ["Petrol"], "drivetrains_seen": ["FWD"]}

PROBLEM: Active blocker/review-only entry. Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only|Mini|Roadster'].

WEB-VALIDATED FACT: MINI Israel official pages support current Countryman, Aceman and Cabrio; official PDFs support Cooper SE. Historical Clubman/Cooper/Countryman/Paceman/Coupe/Roadster require iCar/Auto/Tier2 support. Merge likely/global duplicates into confirmed profiles.

SOURCE:
- https://www.mini.co.il/he_IL/home.html
- https://www.mini.co.il/he_IL/home/range/mini-countryman.html
- https://www.mini.co.il/he_IL/home/range/mini-cooper-convertible.html
- https://www.mini.co.il/content/dam/MINI/marketIL/mini_co_il/Catalogues/BEV_2020/200630_27013_Mini_Electric_Cooper_SE%28split%29_9-6-2020.pdf

TARGET VALUE: Use raw_database_values plus repo-local Israeli sources and embedded source package to build a clean profile; if exact field grounding is insufficient, archive non-blocking with reason instead of fabricating.

ACTION: FIX/ADD GROUNDED CLEAN PROFILE


---

## MODEL: global-reference-only|Mini|Roadster

CURRENT VALUE: review/blocker profile; variants=0; error='Extra data: line 252 column 1 (char 4937)'; raw_database_values={"years_seen": [2012, 2015], "trims_seen": ["John Cooper Works"], "engines_seen": ["1.6L turbo petrol, 211 hp"], "horsepower_seen": [], "transmissions_seen": ["6-speed manual"], "body_types_seen": ["Roadster"], "fuel_types_seen": ["Petrol"], "drivetrains_seen": ["FWD"]}

PROBLEM: Active blocker/review-only entry. Global-reference-only profile has local sibling(s): ['IL-confirmed|Mini|Roadster']. Do not keep as separate clean Israeli profile.

WEB-VALIDATED FACT: MINI Israel official pages support current Countryman, Aceman and Cabrio; official PDFs support Cooper SE. Historical Clubman/Cooper/Countryman/Paceman/Coupe/Roadster require iCar/Auto/Tier2 support. Merge likely/global duplicates into confirmed profiles.

SOURCE:
- https://www.mini.co.il/he_IL/home.html
- https://www.mini.co.il/he_IL/home/range/mini-countryman.html
- https://www.mini.co.il/he_IL/home/range/mini-cooper-convertible.html
- https://www.mini.co.il/content/dam/MINI/marketIL/mini_co_il/Catalogues/BEV_2020/200630_27013_Mini_Electric_Cooper_SE%28split%29_9-6-2020.pdf

TARGET VALUE: No grounded variant rows in review. Do not fabricate clean; archive non-blocking unless repo-local Israeli evidence fully grounds a profile.

ACTION: ARCHIVE NON-BLOCKING / KEEP REVIEW NON-BLOCKING


---

## MODEL: IL-confirmed|Mitsubishi|Grandis

CURRENT VALUE: review/blocker profile; variants=0; error='Gemini catalog client returned non-object JSON'; raw_database_values={"years_seen": [2004, 2011], "trims_seen": ["2.4"], "engines_seen": ["2.4L 4G69 MIVEC inline-4, 165 hp"], "horsepower_seen": [], "transmissions_seen": ["4-speed automatic"], "body_types_seen": ["MPV"], "fuel_types_seen": ["Petrol"], "drivetrains_seen": ["FWD"]}

PROBLEM: Active blocker/review-only entry. IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mitsubishi Israel official pages support current Outlander in the visible model list/pricelist; iCar/Auto support historical Pajero, L200, Lancer, Colt, Galant, Grandis, i-MiEV etc. Global-reference-only duplicates must merge/archive; Grandis review should be repaired from iCar if source support is sufficient.

SOURCE:
- https://www.mitsubishi-israel.co.il/prices/
- https://www.mitsubishi-israel.co.il/models/
- https://www.mitsubishi-israel.co.il/catalog_and_specifications/
- https://www.icar.co.il/מיצובישי/
- https://www.auto.co.il/cars/mitsubishi/outlander/

TARGET VALUE: Use raw_database_values plus repo-local Israeli sources and embedded source package to build a clean profile; if exact field grounding is insufficient, archive non-blocking with reason instead of fabricating.

ACTION: FIX/ADD GROUNDED CLEAN PROFILE


---

## MODEL: global-reference-only|Mitsubishi|Pajero Sport

CURRENT VALUE: review/blocker profile; variants=0; error=None; raw_database_values={}

PROBLEM: Active blocker/review-only entry. Global-reference-only profile has local sibling(s): ['IL-confirmed|Mitsubishi|Pajero Sport']. Do not keep as separate clean Israeli profile.

WEB-VALIDATED FACT: Mitsubishi Israel official pages support current Outlander in the visible model list/pricelist; iCar/Auto support historical Pajero, L200, Lancer, Colt, Galant, Grandis, i-MiEV etc. Global-reference-only duplicates must merge/archive; Grandis review should be repaired from iCar if source support is sufficient.

SOURCE:
- https://www.mitsubishi-israel.co.il/prices/
- https://www.mitsubishi-israel.co.il/models/
- https://www.mitsubishi-israel.co.il/catalog_and_specifications/
- https://www.icar.co.il/מיצובישי/
- https://www.auto.co.il/cars/mitsubishi/outlander/
- repo source: [1] iCar - Mitsubishi Pajero Sport Israel (editorial) — https://www.icar.co.il/%D7%9E%D7%99%D7%A6%D7%95%D7%91%D7%99%D7%A9%D7%99_%D7%A4%D7%90%D7%92'%D7%A8%D7%95_%D7%A1%D7%A4%D7%95%D7%A8%D7%98/

TARGET VALUE: No grounded variant rows in review. Do not fabricate clean; archive non-blocking unless repo-local Israeli evidence fully grounds a profile.

ACTION: ARCHIVE NON-BLOCKING / KEEP REVIEW NON-BLOCKING



## Required checks after FINAL RUN

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Directly audit actual files: clean catalog, readiness, review, archive, quality scan output, compute_resume_state(), unmatched_output_keys, active blockers, cursor, split aliases, duplicate/casing cleanup.

Delete temporary Batch 26 instruction files before final commit unless user explicitly asks to keep them.
