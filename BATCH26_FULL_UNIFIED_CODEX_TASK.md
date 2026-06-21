# BATCH26 FULL UNIFIED CODEX TASK — RUN1-RUN7 + FINAL

TEMPORARY FILE RULE: This is a temporary instruction file. After applying and verifying Batch 26, delete `codex_tasks/BATCH26_*.md` from the repo before final commit unless the user explicitly asks to keep audit docs.

DO NOT BROWSE THE INTERNET.
All web-validation facts, target values, source decisions, split/merge/archive decisions, and variant-level corrections are embedded in this task file and repo-local sources. Use this task file as the single source of truth.

## Execution order

```text
RUN 1 -> RUN 2 -> RUN 3 -> RUN 4 -> RUN 5 -> RUN 6 -> RUN 7 -> FINAL RUN
```

## Known ZIP state before implementation

```text
source cursor = 723/1124
resume_after_key = global-reference-only|Mitsubishi|Pajero Sport
next_key_to_process = IL-confirmed|Mitsubishi|Space Star
clean profiles in Batch 26 window = 124
review/blockers = 31
unmatched_output_keys_count = 0
```

## Required final goals

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

## Mandatory checks

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

## Mandatory direct audit

Audit actual generated files, not only console output:
- clean catalog
- data/model_technical_catalog_il.json
- readiness report
- review report/file
- archive report/file
- quality scan output
- compute_resume_state()
- unmatched_output_keys
- active blockers
- cursor/resume state
- duplicate/split alias cleanup

---


# ==============================
# RUN1
# source: BATCH26_RUN1_VARIANT_LEVEL_CODEX_TASK.md
# ==============================

# BATCH26 RUN 1 ONLY — VARIANT-LEVEL CODEX TASK

Generated for user request: start with the initial run only. Do not apply RUN 2 or FINAL RUN here.

## Hard constraints

- Do not browse the internet.
- All web-validation facts and target corrections required for RUN 1 are embedded in this task file.
- Use this task file as the single source of truth for RUN 1 only.
- Do not apply corrections that are not explicitly instructed here.
- If repo-local evidence conflicts with this task file, report the conflict instead of guessing.
- If a variant cannot be grounded with embedded facts or repo-local sources, move it to non-blocking archive/review rather than fabricating clean data.
- Temporary-file cleanup is mandatory: before final commit, delete this file and any `codex_tasks/BATCH26_RUN1_*.md` temporary instruction files unless the user explicitly asks to keep them.

## ZIP audit baseline

- Source catalog path inspected: `data/model_technical_catalog_il.json`
- Current clean catalog models: 630
- Readiness clean_models: 630
- Readiness review_entries: 31
- Readiness models_blocked: 31
- Readiness ready_for_website_upload: False
- Quality scan findings: 734
- RUN 1 starts after previous stop `IL-confirmed|Lexus|RC`.
- RUN 1 profile window: `IL-confirmed|Lexus|RX` through `IL-confirmed|Maserati|Quattroporte`.
- RUN 1 profiles: 20.
- RUN 1 technical variants: 73.

## RUN 1 model list
1. `IL-confirmed|Lexus|RX` — 8 variants
2. `IL-confirmed|Lexus|SC 430` — 1 variants
3. `IL-confirmed|Lexus|UX` — 3 variants
4. `global-reference-only|Lincoln|MKC` — 4 variants
5. `IL-likely|Lincoln|MKX` — 3 variants
6. `IL-likely|Lincoln|Navigator` — 3 variants
7. `global-reference-only|Lotus|Elise` — 2 variants
8. `IL-confirmed|Lotus|Elise` — 1 variants
9. `IL-likely|Lotus|Elise` — 2 variants
10. `IL-confirmed|Lotus|Emira` — 3 variants
11. `global-reference-only|Lotus|Evora` — 4 variants
12. `IL-confirmed|Lynk & Co|01` — 1 variants
13. `IL-confirmed|Maserati|Ghibli` — 9 variants
14. `IL-confirmed|Maserati|GranCabrio` — 2 variants
15. `IL-likely|Maserati|GranCabrio` — 3 variants
16. `IL-confirmed|Maserati|GranTurismo` — 4 variants
17. `IL-confirmed|Maserati|Grecale` — 3 variants
18. `IL-confirmed|Maserati|MC20` — 2 variants
19. `IL-likely|Maserati|Quattroporte` — 8 variants
20. `IL-confirmed|Maserati|Quattroporte` — 7 variants

## Embedded web-validation source ledger

- **LEXUS_RX_OFFICIAL:** Lexus Israel official RX page/catalog: confirms current RX 350h, RX 450h+ and RX 500h trims; RX catalog PDF lists trim columns RX350h/RX450h+/RX500h and technical spec section.
- **LEXUS_UX_OFFICIAL:** Lexus Israel official UX page/catalog: confirms current UX 300h; UX300h catalog PDF is Israeli official Lexus source.
- **LEXUS_SC_ICAR:** iCar Israel SC430 page/version supports 2007-2009 SC430 4.3 petrol, automatic Tiptronic, RWD; use as Tier 2/3 historical support only.
- **LINCOLN_AYALON:** Ayalon Motors is an Israeli licensed parallel importer; Auto/Cartube sources support Lincoln MKX marketing/arrival in Israel; Carzone/Yad2 are weaker for MKC/Navigator.
- **LINCOLN_MKC_CARZONE:** Carzone Israel MKC 2015 page supports MKC 2015 Israeli sales, Select 2.0 and Reserve 4X4 2.3; source is Tier 3 and does not prove broad official clean coverage.
- **LINCOLN_NAVIGATOR_YAD2:** Yad2 price-list page supports Navigator 2020 3.5 450hp automatic; Autoboom supports 3.5 456hp/10AT/AWD. These are weak Tier 3/Autoboom sources, not enough for clean current 2026 without stronger local evidence.
- **LOTUS_EMIRA_ICAR:** iCar Israel first drive Emira supports V6 3.5 supercharged, 405hp, 6-speed manual, RWD, estimated Israeli context around 700k NIS.
- **LOTUS_EMIRA_CARZONE:** Carzone Israel 2026 Emira page lists First Edition 2.0 and SE V6 3.5 manual price entries. Use cautiously as Tier 3 price-list support.
- **LYNKCO_01_PDF:** Lynk & Co Israel brochure PDF supports 01 PHEV: 1.5L turbo, combined 261hp, 7-speed DCT, FWD, 75km electric range.
- **MASERATI_GHIBLI_CARTUBE:** Cartube Israel Maserati Ghibli tag confirms 2021 Ghibli Hybrid 2.0 turbo 330hp and Ghibli/Quattroporte Trofeo V8 580hp.
- **MASERATI_GRANTURISMO_CARTUBE:** Cartube Israel 2024 GranTurismo launch confirms Modena 490hp and Trofeo 550hp V6 versions in Israel; note the source snippet contains a likely title/body typo that says Trofeo 490 in one line, so do not downgrade Trofeo from 550 unless repo-local source proves.
- **MASERATI_GRANCABRIO_CARTUBE:** Cartube Israel 2024 GranCabrio launch confirms Trofeo 3.0 V6 twin-turbo 550hp, 8AT, AWD, 2.05M NIS. Folgore appears in related Israeli articles but requires direct local source before clean current.
- **MASERATI_GRECALE_CARTUBE:** Cartube Israel 2022/2026 Grecale price/spec supports GT 2.0 300hp, Modena 2.0 330hp, Trofeo 3.0 530hp; 2026 price-list page indicates the model remains current in Israel.
- **MASERATI_QUATTROPORTE_CARTUBE:** Cartube Israel supports Quattroporte Trofeo V8 580hp and earlier launch data; Auto/Cartube source set supports 2013+ Quattroporte S Q4/GTS/diesel/base variants.
- **GLOBAL_ONLY_CAUTION:** Global manufacturer or generic global spec sources may be used only as secondary technical confirmation, never as the sole clean Israeli-market grounding.

## Required corrections and decisions by model/profile


### RUN1-01 — IL-confirmed|Lexus|RX

MODEL: IL-confirmed|Lexus|RX

CURRENT VALUE: clean/profile entry with 8 variants; year_start=2006; year_end=None; profile_confidence=medium.

PROBLEM: FIX source_indexes and field_sources. Keep all 8 variants. Correct RX 2006-2009 variant source_indexes from out-of-range [4] to the repo source that supports 2006-2009 RX (current local source index 3). Correct 2009-2015 to local source index 2, 2015-2022 to index 1, and 2022-current RX 350h/450h+/500h to official Lexus Israel RX page/catalog + repo Cartube source. Do not close current RX hybrid/PHEV variants.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Lexus RX.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Cartube — לקסוס RX 2023 החדש בישראל - מחיר החל מ-399,990 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9C%D7%A7%D7%A1%D7%95%D7%A1-rx-2023-%D7%94%D7%97%D7%93%D7%A9-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-399-990-%D7%A9%D7%A7%D7%9C
- repo_source[1]: Auto.co.il — לקסוס RX דור 4 (2015-2022) — https://www.auto.co.il/model/lexus-rx_g1174
- repo_source[2]: iCar — לקסוס RX דור 3 (2009-2015) — https://www.icar.co.il/%D7%9C%D7%A7%D7%A1%D7%95%D7%A1/%D7%9C%D7%A7%D7%A1%D7%95%D7%A1_RX_%D7%93%D7%95%D7%A8_3/
- repo_source[3]: iCar — לקסוס RX דור 2 (2006-2009) — https://www.icar.co.il/%D7%9C%D7%A7%D7%A1%D7%95%D7%A1/%D7%9C%D7%A7%D7%A1%D7%95%D7%A1_RX_%D7%93%D7%95%D7%A8_2/

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: FIX source_indexes and field_sources. Keep all 8 variants. Correct RX 2006-2009 variant source_indexes from out-of-range [4] to the repo source that supports 2006-2009 RX (current local source index 3). Correct 2009-2015 to local source index 2, 2015-2022 to index 1, and 2022-current RX 350h/450h+/500h to official Lexus Israel RX page/catalog + repo Cartube source. Do not close current RX hybrid/PHEV variants.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim='RX 350'; year_start=2006; year_end=2009; body_type='SUV'; fuel_type='petrol'; engine='3.5L v6'; engine_displacement_l=3.5; horsepower_hp=276; transmission='5-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[4]
  - PROBLEM: invalid source_indexes [4] for profile source count 4
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Use valid generation-specific source index: 2006-2009 -> repo_source[3], 2009-2015 -> repo_source[2], 2015-2022 -> repo_source[1], current -> official Lexus/Cartube source.
  - ACTION: FIX
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='RX 400h'; year_start=2006; year_end=2009; body_type='SUV'; fuel_type='hybrid'; engine='3.3L v6'; engine_displacement_l=3.3; horsepower_hp=272; transmission='cvt'; drivetrain='AWD'; support_level='direct'; source_indexes=[4]
  - PROBLEM: invalid source_indexes [4] for profile source count 4
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Use valid generation-specific source index: 2006-2009 -> repo_source[3], 2009-2015 -> repo_source[2], 2015-2022 -> repo_source[1], current -> official Lexus/Cartube source.
  - ACTION: FIX
- VARIANT 3:
  - CURRENT VALUE: version_or_trim='RX 350'; year_start=2009; year_end=2015; body_type='SUV'; fuel_type='petrol'; engine='3.5L v6'; engine_displacement_l=3.5; horsepower_hp=277; transmission='6-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[3]
  - PROBLEM: source index likely shifted by one after source list normalization
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Use valid generation-specific source index: 2006-2009 -> repo_source[3], 2009-2015 -> repo_source[2], 2015-2022 -> repo_source[1], current -> official Lexus/Cartube source.
  - ACTION: FIX
- VARIANT 4:
  - CURRENT VALUE: version_or_trim='RX 450h'; year_start=2009; year_end=2015; body_type='SUV'; fuel_type='hybrid'; engine='3.5L v6'; engine_displacement_l=3.5; horsepower_hp=299; transmission='cvt'; drivetrain='AWD'; support_level='direct'; source_indexes=[3]
  - PROBLEM: source index likely shifted by one after source list normalization
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Use valid generation-specific source index: 2006-2009 -> repo_source[3], 2009-2015 -> repo_source[2], 2015-2022 -> repo_source[1], current -> official Lexus/Cartube source.
  - ACTION: FIX
- VARIANT 5:
  - CURRENT VALUE: version_or_trim='RX 450h'; year_start=2015; year_end=2022; body_type='SUV'; fuel_type='hybrid'; engine='3.5L v6'; engine_displacement_l=3.5; horsepower_hp=313; transmission='cvt'; drivetrain='AWD'; support_level='direct'; source_indexes=[2]
  - PROBLEM: source index likely shifted by one after source list normalization
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Use valid generation-specific source index: 2006-2009 -> repo_source[3], 2009-2015 -> repo_source[2], 2015-2022 -> repo_source[1], current -> official Lexus/Cartube source.
  - ACTION: FIX
- VARIANT 6:
  - CURRENT VALUE: version_or_trim='RX 350h'; year_start=2022; year_end=None; body_type='SUV'; fuel_type='hybrid'; engine='2.5L'; engine_displacement_l=2.5; horsepower_hp=250; transmission='cvt'; drivetrain='AWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 7:
  - CURRENT VALUE: version_or_trim='RX 450h+'; year_start=2022; year_end=None; body_type='SUV'; fuel_type='plug_in_hybrid'; engine='2.5L'; engine_displacement_l=2.5; horsepower_hp=309; transmission='cvt'; drivetrain='AWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 8:
  - CURRENT VALUE: version_or_trim='RX 500h'; year_start=2022; year_end=None; body_type='SUV'; fuel_type='hybrid'; engine='2.4L turbo'; engine_displacement_l=2.4; horsepower_hp=371; transmission='6-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP

### RUN1-02 — IL-confirmed|Lexus|SC 430

MODEL: IL-confirmed|Lexus|SC 430

CURRENT VALUE: clean/profile entry with 1 variants; year_start=2006; year_end=2010; profile_confidence=medium.

PROBLEM: KEEP as historical Israeli-market SC430. Empty trim is acceptable because model name itself is SC 430; ensure source_indexes/field_sources point to iCar/Auto local sources only.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Lexus SC 430.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: iCar — לקסוס SC430 - חוות דעת, מחירון, מפרט טכני | iCar — https://www.icar.co.il/%D7%9C%D7%A7%D7%A1%D7%95%D7%A1/%D7%9C%D7%A7%D7%A1%D7%95%D7%A1_SC430/
- repo_source[1]: Auto.co.il — לקסוס SC - מפרט טכני, מידות, מחירון | אוטו — https://www.auto.co.il/model/lexus-sc_g162

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: KEEP as historical Israeli-market SC430. Empty trim is acceptable because model name itself is SC 430; ensure source_indexes/field_sources point to iCar/Auto local sources only.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=2006; year_end=2010; body_type='Convertible'; fuel_type='petrol'; engine='4.3L v8'; engine_displacement_l=4.3; horsepower_hp=286; transmission='6-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 1]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP

### RUN1-03 — IL-confirmed|Lexus|UX

MODEL: IL-confirmed|Lexus|UX

CURRENT VALUE: clean/profile entry with 3 variants; year_start=2019; year_end=None; profile_confidence=medium.

PROBLEM: KEEP with UX 300h current. Use Lexus Israel UX official page/PDF as Tier 1 support for current UX 300h. UX 250h must remain closed at 2024; do not extend 250h after UX 300h replaced it.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Lexus UX.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: iCar.co.il — מחירון רכב לקסוס UX - מפרט טכני — https://www.icar.co.il/lexus/lexus_ux/
- repo_source[1]: Cartube.co.il — לקסוס UX 300h החדש 2024 בישראל — https://www.cartube.co.il/חדשות-רכב/לקסוס-ux-300h-החדש-2024-בישראל
- repo_source[2]: Cartube.co.il — לקסוס UX בישראל - מחיר החל מ- 205,000 שקל — https://www.cartube.co.il/חדשות-רכב/לקסוס-ux-בישראל
- repo_source[3]: Lexus Israel Official — Lexus UX 300h - לקסוס ישראל — https://www.lexus.co.il/new-cars/ux

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: KEEP with UX 300h current. Use Lexus Israel UX official page/PDF as Tier 1 support for current UX 300h. UX 250h must remain closed at 2024; do not extend 250h after UX 300h replaced it.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim='UX 200'; year_start=2019; year_end=2022; body_type='Crossover'; fuel_type='petrol'; engine='2.0L naturally aspirated'; engine_displacement_l=2.0; horsepower_hp=173; transmission='cvt'; drivetrain='FWD'; support_level='direct'; source_indexes=[0, 2]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='UX 250h'; year_start=2019; year_end=2024; body_type='Crossover'; fuel_type='hybrid'; engine='2.0L hybrid'; engine_displacement_l=2.0; horsepower_hp=184; transmission='cvt'; drivetrain='FWD'; support_level='direct'; source_indexes=[0, 1, 2]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 3:
  - CURRENT VALUE: version_or_trim='UX 300h'; year_start=2024; year_end=None; body_type='Crossover'; fuel_type='hybrid'; engine='2.0L hybrid'; engine_displacement_l=2.0; horsepower_hp=199; transmission='cvt'; drivetrain='FWD'; support_level='direct'; source_indexes=[0, 1, 3]
  - PROBLEM: current source should include official Lexus UX300h page/PDF
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Keep UX300h current and add/ensure official Lexus Israel UX300h source/field_sources.
  - ACTION: KEEP/FIX

### RUN1-04 — global-reference-only|Lincoln|MKC

MODEL: global-reference-only|Lincoln|MKC

CURRENT VALUE: clean/profile entry with 4 variants; year_start=2014; year_end=2019; profile_confidence=medium.

PROBLEM: MOVE TO REVIEW or ARCHIVE NON-BLOCKING unless repo policy explicitly allows Tier 3 Carzone/Yad2-only models in clean. It is not a verified clean Israeli official/parallel importer profile. If retained outside clean, preserve lineage and note weak Israeli sales evidence. Also fix invalid source indexes if preserved.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Lincoln MKC.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Carzone — לינקולן MKC | קארזון - מחירון רכב, צריכת דלק וחוות דעת — https://www.carzone.co.il/lincoln/mkc/
- repo_source[1]: Yad2 — לינקולן MKC (2014-2019) - רכבים פרטיים - מחירון ולוח רכב - יד2 — https://www.yad2.co.il/vehicles/private-cars?make=168&model=1481

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: MOVE TO REVIEW or ARCHIVE NON-BLOCKING unless repo policy explicitly allows Tier 3 Carzone/Yad2-only models in clean. It is not a verified clean Israeli official/parallel importer profile. If retained outside clean, preserve lineage and note weak Israeli sales evidence. Also fix invalid source indexes if preserved.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim='Select'; year_start=2014; year_end=2019; body_type='SUV'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=240; transmission='6-speed automatic'; drivetrain='FWD'; support_level='direct'; source_indexes=[1, 2]
  - PROBLEM: invalid source_indexes [2] for profile source count 2; insufficient strong Israeli-market grounding for verified clean
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Move this variant/profile to non-blocking review/archive with reason and lineage; do not keep as verified clean unless repo-local Tier1/Tier2 evidence is found.
  - ACTION: MOVE TO REVIEW
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='Reserve'; year_start=2014; year_end=2019; body_type='SUV'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=240; transmission='6-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[1, 2]
  - PROBLEM: invalid source_indexes [2] for profile source count 2; insufficient strong Israeli-market grounding for verified clean
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Move this variant/profile to non-blocking review/archive with reason and lineage; do not keep as verified clean unless repo-local Tier1/Tier2 evidence is found.
  - ACTION: MOVE TO REVIEW
- VARIANT 3:
  - CURRENT VALUE: version_or_trim='Reserve'; year_start=2015; year_end=2019; body_type='SUV'; fuel_type='petrol'; engine='2.3L turbo'; engine_displacement_l=2.3; horsepower_hp=285; transmission='6-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[1, 2]
  - PROBLEM: invalid source_indexes [2] for profile source count 2; insufficient strong Israeli-market grounding for verified clean
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Move this variant/profile to non-blocking review/archive with reason and lineage; do not keep as verified clean unless repo-local Tier1/Tier2 evidence is found.
  - ACTION: MOVE TO REVIEW
- VARIANT 4:
  - CURRENT VALUE: version_or_trim='Black Label'; year_start=2015; year_end=2019; body_type='SUV'; fuel_type='petrol'; engine='2.3L turbo'; engine_displacement_l=2.3; horsepower_hp=285; transmission='6-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: insufficient strong Israeli-market grounding for verified clean
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Move this variant/profile to non-blocking review/archive with reason and lineage; do not keep as verified clean unless repo-local Tier1/Tier2 evidence is found.
  - ACTION: MOVE TO REVIEW

### RUN1-05 — IL-likely|Lincoln|MKX

MODEL: IL-likely|Lincoln|MKX

CURRENT VALUE: clean/profile entry with 3 variants; year_start=2007; year_end=2018; profile_confidence=medium.

PROBLEM: KEEP/FIX as Israeli parallel-import market model. Ayalon Motors/Auto/Cartube support MKX Israeli marketing. Upgrade evidence classification to import_parallel/IL-confirmed if schema supports without breaking cursor; otherwise keep IL-likely but make notes explicit. Do not treat as official importer.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Lincoln MKX.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: iCar — לינקולן MKX - מחירון, מפרטים, אמינות — https://www.icar.co.il/Lincoln/Lincoln_MKX/
- repo_source[1]: Auto.co.il — איילון מוטורס מתחילה בשיווק מותג היוקרה לינקולן — https://www.auto.co.il/article/110903-local-news
- repo_source[2]: Cartube.co.il — לינקולן MKX החדש 2016 בישראל — https://www.cartube.co.il/חדשות-רכב/לינקולן-mkx-החדש-נחת-בישראל
- repo_source[3]: Yad2 — לינקולן MKX יד שניה מפרט — https://www.yad2.co.il/vehicles/cars?manufacturer=104&model=949

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: KEEP/FIX as Israeli parallel-import market model. Ayalon Motors/Auto/Cartube support MKX Israeli marketing. Upgrade evidence classification to import_parallel/IL-confirmed if schema supports without breaking cursor; otherwise keep IL-likely but make notes explicit. Do not treat as official importer.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=2007; year_end=2010; body_type='SUV'; fuel_type='petrol'; engine='3.5L v6'; engine_displacement_l=3.5; horsepower_hp=265; transmission='6-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[0, 3]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='Select'; year_start=2011; year_end=2015; body_type='SUV'; fuel_type='petrol'; engine='3.7L v6'; engine_displacement_l=3.7; horsepower_hp=305; transmission='6-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[0, 1, 3]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 3:
  - CURRENT VALUE: version_or_trim='Reserve'; year_start=2016; year_end=2018; body_type='SUV'; fuel_type='petrol'; engine='2.7L v6 turbo'; engine_displacement_l=2.7; horsepower_hp=335; transmission='6-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[0, 2, 3]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP

### RUN1-06 — IL-likely|Lincoln|Navigator

MODEL: IL-likely|Lincoln|Navigator

CURRENT VALUE: clean/profile entry with 3 variants; year_start=2003; year_end=2026; profile_confidence=medium.

PROBLEM: MOVE TO REVIEW NON-BLOCKING. Current 2018-2026 clean entry is too weak: only Autoboom/Yad2/secondary pages support Israel and not strong enough for verified clean. Preserve historical/marketplace evidence and set reason='weak_tier3_only_current_clean_not_verified'.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Lincoln Navigator.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Autoboom Israel — Lincoln Navigator - Catalog Autoboom Israel — https://autoboom.co.il/he/catalog/cars/lincoln/navigator
- repo_source[1]: Autoboom Israel — Lincoln Navigator 2nd Generation (2003-2006) - Catalog Autoboom Israel — https://autoboom.co.il/he/catalog/cars/lincoln/navigator/2-generation

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: MOVE TO REVIEW NON-BLOCKING. Current 2018-2026 clean entry is too weak: only Autoboom/Yad2/secondary pages support Israel and not strong enough for verified clean. Preserve historical/marketplace evidence and set reason='weak_tier3_only_current_clean_not_verified'.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=2018; year_end=2026; body_type='SUV'; fuel_type='petrol'; engine='3.5L v6 turbo'; engine_displacement_l=3.5; horsepower_hp=450; transmission='10-speed automatic'; drivetrain='4WD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: insufficient strong Israeli-market grounding for verified clean
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Move this variant/profile to non-blocking review/archive with reason and lineage; do not keep as verified clean unless repo-local Tier1/Tier2 evidence is found.
  - ACTION: MOVE TO REVIEW
- VARIANT 2:
  - CURRENT VALUE: version_or_trim=None; year_start=2005; year_end=2006; body_type='SUV'; fuel_type='petrol'; engine='5.4L v8'; engine_displacement_l=5.4; horsepower_hp=300; transmission='6-speed automatic'; drivetrain='4WD'; support_level='direct'; source_indexes=[2]
  - PROBLEM: invalid source_indexes [2] for profile source count 2; insufficient strong Israeli-market grounding for verified clean
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Move this variant/profile to non-blocking review/archive with reason and lineage; do not keep as verified clean unless repo-local Tier1/Tier2 evidence is found.
  - ACTION: MOVE TO REVIEW
- VARIANT 3:
  - CURRENT VALUE: version_or_trim=None; year_start=2003; year_end=2004; body_type='SUV'; fuel_type='petrol'; engine='5.4L v8'; engine_displacement_l=5.4; horsepower_hp=300; transmission='4-speed automatic'; drivetrain='4WD'; support_level='direct'; source_indexes=[2]
  - PROBLEM: invalid source_indexes [2] for profile source count 2; insufficient strong Israeli-market grounding for verified clean
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Move this variant/profile to non-blocking review/archive with reason and lineage; do not keep as verified clean unless repo-local Tier1/Tier2 evidence is found.
  - ACTION: MOVE TO REVIEW

### RUN1-07 — global-reference-only|Lotus|Elise

MODEL: global-reference-only|Lotus|Elise

CURRENT VALUE: clean/profile entry with 2 variants; year_start=1996; year_end=2011; profile_confidence=medium.

PROBLEM: MERGE into a single Lotus Elise lineage profile; do not keep global-reference-only duplicate clean profile.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Lotus Elise.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Auto.co.il — לוטוס אליז (1996-2000) - מפרט טכני — https://www.auto.co.il/model/lotus-elise
- repo_source[1]: iCar — לוטוס אליז 111R יבוא אישי לישראל — https://www.icar.co.il/lotus/elise/

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: MERGE into a single Lotus Elise lineage profile; do not keep global-reference-only duplicate clean profile.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=1996; year_end=2000; body_type='Roadster'; fuel_type='petrol'; engine='1.8L'; engine_displacement_l=1.8; horsepower_hp=118; transmission='5-speed manual'; drivetrain='RWD'; support_level='direct'; source_indexes=[0]
  - PROBLEM: Lotus Elise split across global/IL-confirmed/IL-likely profiles
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one clean Lotus Elise lineage profile only if all variants remain locally grounded; otherwise move weak variants to review non-blocking.
  - ACTION: MERGE/FIX
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='111R'; year_start=2004; year_end=2011; body_type='Roadster'; fuel_type='petrol'; engine='1.8L'; engine_displacement_l=1.8; horsepower_hp=192; transmission='6-speed manual'; drivetrain='RWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: Lotus Elise split across global/IL-confirmed/IL-likely profiles
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one clean Lotus Elise lineage profile only if all variants remain locally grounded; otherwise move weak variants to review non-blocking.
  - ACTION: MERGE/FIX

### RUN1-08 — IL-confirmed|Lotus|Elise

MODEL: IL-confirmed|Lotus|Elise

CURRENT VALUE: clean/profile entry with 1 variants; year_start=None; year_end=None; profile_confidence=medium.

PROBLEM: MERGE/FIX into single Lotus Elise profile with the 1.6 136hp variant years fixed from null-null to 2012-2021 if supported by Auto/iCar local source. Fix invalid source index [1] when only one source exists.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Lotus Elise.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Auto.co.il — לוטוס אליז - קטלוג רכבים ומפרט טכני — https://www.auto.co.il/model/lotus-elise

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: MERGE/FIX into single Lotus Elise profile with the 1.6 136hp variant years fixed from null-null to 2012-2021 if supported by Auto/iCar local source. Fix invalid source index [1] when only one source exists.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=None; year_end=None; body_type='Roadster'; fuel_type='petrol'; engine='1.6L naturally aspirated'; engine_displacement_l=1.6; horsepower_hp=136; transmission='6-speed manual'; drivetrain='RWD'; support_level='indirect'; source_indexes=[1]
  - PROBLEM: invalid source_indexes [1] for profile source count 1; Lotus Elise split across global/IL-confirmed/IL-likely profiles
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one clean Lotus Elise lineage profile only if all variants remain locally grounded; otherwise move weak variants to review non-blocking.
  - ACTION: MERGE/FIX

### RUN1-09 — IL-likely|Lotus|Elise

MODEL: IL-likely|Lotus|Elise

CURRENT VALUE: clean/profile entry with 2 variants; year_start=2012; year_end=2021; profile_confidence=medium.

PROBLEM: MERGE into the same Lotus Elise profile. Preserve 1.6 136hp and Elise S 1.8 supercharged 220hp as historical variants if local Auto/iCar support exists. Delete duplicate split profile after alias/lineage.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Lotus Elise.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Auto.co.il — לוטוס אליז - מחירון, מפרטים, אבזור ועוד — https://www.auto.co.il/model/lotus-elise_g1281
- repo_source[1]: Cartube.co.il — לוטוס בישראל: רכבי הספורט של לוטוס נחתו בישראל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9C%D7%95%D7%98%D7%95%D7%A1-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%A8%D7%9B%D7%91%D7%99-%D7%94%D7%A1%D7%A4%D7%95%D7%A8%D7%98-%D7%A9%D7%9C-%D7%9C%D7%95%D7%98%D7%95%D7%A1-%D7%A0%D7%97%D7%AA%D7%95-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: MERGE into the same Lotus Elise profile. Preserve 1.6 136hp and Elise S 1.8 supercharged 220hp as historical variants if local Auto/iCar support exists. Delete duplicate split profile after alias/lineage.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=2012; year_end=2021; body_type='Roadster'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=136; transmission='6-speed manual'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 1]
  - PROBLEM: Lotus Elise split across global/IL-confirmed/IL-likely profiles
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one clean Lotus Elise lineage profile only if all variants remain locally grounded; otherwise move weak variants to review non-blocking.
  - ACTION: MERGE/FIX
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='S'; year_start=2012; year_end=2021; body_type='Roadster'; fuel_type='petrol'; engine='1.8L supercharged'; engine_displacement_l=1.8; horsepower_hp=220; transmission='6-speed manual'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 1]
  - PROBLEM: Lotus Elise split across global/IL-confirmed/IL-likely profiles
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one clean Lotus Elise lineage profile only if all variants remain locally grounded; otherwise move weak variants to review non-blocking.
  - ACTION: MERGE/FIX

### RUN1-10 — IL-confirmed|Lotus|Emira

MODEL: IL-confirmed|Lotus|Emira

CURRENT VALUE: clean/profile entry with 3 variants; year_start=2024; year_end=None; profile_confidence=medium.

PROBLEM: FIX invalid source_indexes [2566,2567] to repo-local source indexes. Keep Emira only with local Israeli source support. Normalize V6 output to 405hp if using iCar Israel as primary; if preserving 400hp due repo-local source conflict, report conflict explicitly. Do not leave invalid source refs.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Lotus Emira.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Cartube — לוטוס אמירה נחתה בישראל - מחירים החל מ-869,900 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9C%D7%95%D7%98%D7%95%D7%A1-%D7%90%D7%9E%D7%99%D7%A8%D7%94-%D7%A0%D7%97%D7%AA%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D-%D7%94%D7%97%D7%9C-%D7%9E-869900-%D7%A9%D7%A7%D7%9C
- repo_source[1]: Auto.co.il — לוטוס אמירה (Emira) החדשה בישראל – מחירון ומפרט טכני — https://www.auto.co.il/article/135974-new-models-lotus-emira

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: FIX invalid source_indexes [2566,2567] to repo-local source indexes. Keep Emira only with local Israeli source support. Normalize V6 output to 405hp if using iCar Israel as primary; if preserving 400hp due repo-local source conflict, report conflict explicitly. Do not leave invalid source refs.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim='First Edition'; year_start=2024; year_end=None; body_type='Coupe'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=360; transmission='8-speed dual_clutch'; drivetrain='RWD'; support_level='direct'; source_indexes=[2566, 2567]
  - PROBLEM: invalid source_indexes [2566, 2567] for profile source count 2; source indexes invalid and V6 hp may conflict 400 vs 405
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Fix source indexes to local sources; set V6 horsepower to 405hp if iCar Israel is primary, or report conflict if preserving 400hp.
  - ACTION: FIX
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='First Edition'; year_start=2024; year_end=None; body_type='Coupe'; fuel_type='petrol'; engine='3.5L v6 supercharged'; engine_displacement_l=3.5; horsepower_hp=400; transmission='6-speed manual'; drivetrain='RWD'; support_level='direct'; source_indexes=[2566, 2567]
  - PROBLEM: invalid source_indexes [2566, 2567] for profile source count 2; source indexes invalid and V6 hp may conflict 400 vs 405
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Fix source indexes to local sources; set V6 horsepower to 405hp if iCar Israel is primary, or report conflict if preserving 400hp.
  - ACTION: FIX
- VARIANT 3:
  - CURRENT VALUE: version_or_trim='First Edition'; year_start=2024; year_end=None; body_type='Coupe'; fuel_type='petrol'; engine='3.5L v6 supercharged'; engine_displacement_l=3.5; horsepower_hp=400; transmission='6-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[2566, 2567]
  - PROBLEM: invalid source_indexes [2566, 2567] for profile source count 2; source indexes invalid and V6 hp may conflict 400 vs 405
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Fix source indexes to local sources; set V6 horsepower to 405hp if iCar Israel is primary, or report conflict if preserving 400hp.
  - ACTION: FIX

### RUN1-11 — global-reference-only|Lotus|Evora

MODEL: global-reference-only|Lotus|Evora

CURRENT VALUE: clean/profile entry with 4 variants; year_start=2010; year_end=2014; profile_confidence=medium.

PROBLEM: MOVE TO REVIEW or MERGE into IL-likely Lotus Evora if local Auto/iCar source coverage is strong enough. Do not leave global-reference-only clean profile. Preserve 3.5 V6 276hp and S 345hp historical variants with lineage.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Lotus Evora.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Auto.co.il Catalog — לוטוס אבורה (2009-2014) - מפרט טכני וקטלוג רכב — https://www.auto.co.il/model/lotus-evora_g535
- repo_source[1]: Cartube.co.il — אוטו-חן משיקה את לוטוס בישראל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9C%D7%95%D7%98%D7%95%D7%A1-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%99%D7%95%D7%A6%D7%90%D7%99%D7%9D-%D7%9C%D7%93%D7%A8%D7%9A
- repo_source[2]: Auto.co.il News — לוטוס אבורה IPS נוחתת בארץ — https://www.auto.co.il/article/roadcartest/28340-local-news-lotus-evora

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: MOVE TO REVIEW or MERGE into IL-likely Lotus Evora if local Auto/iCar source coverage is strong enough. Do not leave global-reference-only clean profile. Preserve 3.5 V6 276hp and S 345hp historical variants with lineage.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=2010; year_end=2014; body_type='Coupe'; fuel_type='petrol'; engine='3.5L v6'; engine_displacement_l=3.5; horsepower_hp=276; transmission='6-speed manual'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 1]
  - PROBLEM: global-reference-only clean profile not acceptable as verified clean
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Do not leave as global-reference-only clean; either convert/merge with local evidence or move to review non-blocking.
  - ACTION: MOVE TO REVIEW/MERGE
- VARIANT 2:
  - CURRENT VALUE: version_or_trim=None; year_start=2011; year_end=2014; body_type='Coupe'; fuel_type='petrol'; engine='3.5L v6'; engine_displacement_l=3.5; horsepower_hp=276; transmission='6-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 2]
  - PROBLEM: global-reference-only clean profile not acceptable as verified clean
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Do not leave as global-reference-only clean; either convert/merge with local evidence or move to review non-blocking.
  - ACTION: MOVE TO REVIEW/MERGE
- VARIANT 3:
  - CURRENT VALUE: version_or_trim='S'; year_start=2011; year_end=2014; body_type='Coupe'; fuel_type='petrol'; engine='3.5L v6 supercharged'; engine_displacement_l=3.5; horsepower_hp=345; transmission='6-speed manual'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 2]
  - PROBLEM: global-reference-only clean profile not acceptable as verified clean
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Do not leave as global-reference-only clean; either convert/merge with local evidence or move to review non-blocking.
  - ACTION: MOVE TO REVIEW/MERGE
- VARIANT 4:
  - CURRENT VALUE: version_or_trim='S'; year_start=2011; year_end=2014; body_type='Coupe'; fuel_type='petrol'; engine='3.5L v6 supercharged'; engine_displacement_l=3.5; horsepower_hp=345; transmission='6-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 2]
  - PROBLEM: global-reference-only clean profile not acceptable as verified clean
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Do not leave as global-reference-only clean; either convert/merge with local evidence or move to review non-blocking.
  - ACTION: MOVE TO REVIEW/MERGE

### RUN1-12 — IL-confirmed|Lynk & Co|01

MODEL: IL-confirmed|Lynk & Co|01

CURRENT VALUE: clean/profile entry with 1 variants; year_start=2023; year_end=2024; profile_confidence=medium.

PROBLEM: KEEP. Israeli Lynk & Co brochure supports 01 PHEV 1.5 turbo, 261hp combined, 7DCT, FWD. Keep 2023-2024 unless repo-local current source extends it; do not fabricate 2026.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Lynk & Co 01.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Cartube — לינק אנד קו 01 בישראל - מחיר החל מ-229,900 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%95%D7%AA%D7%92-%D7%A4%D7%A8%D7%99%D7%9E%D7%99%D7%95%D7%9D-%D7%97%D7%93%D7%A9-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9C%D7%99%D7%A0%D7%A7-%D7%90%D7%A0%D7%93-%D7%A7%D7%95-01-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-229-900-%D7%A9%D7%A7%D7%9C
- repo_source[1]: Auto.co.il — לינק & קו 01 - מחירון, מפרטים, אמינות ועוד | אוטו — https://www.auto.co.il/model/lynk-and-co-01_g1483

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: KEEP. Israeli Lynk & Co brochure supports 01 PHEV 1.5 turbo, 261hp combined, 7DCT, FWD. Keep 2023-2024 unless repo-local current source extends it; do not fabricate 2026.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=2023; year_end=2024; body_type='SUV'; fuel_type='plug_in_hybrid'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=261; transmission='7-speed dual_clutch'; drivetrain='FWD'; support_level='direct'; source_indexes=[0, 1]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP

### RUN1-13 — IL-confirmed|Maserati|Ghibli

MODEL: IL-confirmed|Maserati|Ghibli

CURRENT VALUE: clean/profile entry with 9 variants; year_start=2014; year_end=2024; profile_confidence=medium.

PROBLEM: KEEP. Confirmed Israeli history through 2024; keep 2024 closed/not current. Verify Ghibli Hybrid 2.0 330hp and Trofeo 3.8 V8 580hp with Cartube. Do not extend after model ended.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Maserati Ghibli.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Cartube — מזראטי גיבלי בישראל – מחירון ורמות גימור (2014) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%96%D7%A8%D7%90%D7%98%D7%99-%D7%92%D7%99%D7%91%D7%9C%D7%99-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8%D7%95%D7%9F-%D7%95%D7%A8%D7%9E%D7%95%D7%AA-%D7%92%D7%99%D7%9E%D7%95%D7%A8
- repo_source[1]: Cartube — מזראטי גיבלי הייבריד בישראל - מחיר החל מ- 550,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%96%D7%A8%D7%90%D7%98%D7%99-%D7%92%D7%99%D7%91%D7%9C%D7%99-%D7%94%D7%99%D7%99%D7%91%D7%A8%D7%99%D7%93-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-550000-%D7%A9%D7%A7%D7%9C
- repo_source[2]: Auto.co.il — מזראטי משלימה את משפחת הטרופאו (2020) — https://www.auto.co.il/article/133519-world-news
- repo_source[3]: iCar — מזראטי גיבלי מפרט טכני — https://www.icar.co.il/%D7%9E%D7%96%D7%A8%D7%90%D7%98%D7%99/%D7%9E%D7%96%D7%A8%D7%90%D7%98%D7%99_%D7%92%D7%99%D7%91%D7%9C%D7%99/

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: KEEP. Confirmed Israeli history through 2024; keep 2024 closed/not current. Verify Ghibli Hybrid 2.0 330hp and Trofeo 3.8 V8 580hp with Cartube. Do not extend after model ended.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=2014; year_end=2017; body_type='Sedan'; fuel_type='petrol'; engine='3.0L v6 twin-turbo'; engine_displacement_l=3.0; horsepower_hp=330; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 3]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='S'; year_start=2014; year_end=2017; body_type='Sedan'; fuel_type='petrol'; engine='3.0L v6 twin-turbo'; engine_displacement_l=3.0; horsepower_hp=410; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 3]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 3:
  - CURRENT VALUE: version_or_trim='S'; year_start=2014; year_end=2017; body_type='Sedan'; fuel_type='petrol'; engine='3.0L v6 twin-turbo'; engine_displacement_l=3.0; horsepower_hp=410; transmission='8-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[0, 3]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 4:
  - CURRENT VALUE: version_or_trim=None; year_start=2014; year_end=2018; body_type='Sedan'; fuel_type='diesel'; engine='3.0L v6 turbo'; engine_displacement_l=3.0; horsepower_hp=275; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 3]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 5:
  - CURRENT VALUE: version_or_trim=None; year_start=2017; year_end=2023; body_type='Sedan'; fuel_type='petrol'; engine='3.0L v6 twin-turbo'; engine_displacement_l=3.0; horsepower_hp=350; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[3]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 6:
  - CURRENT VALUE: version_or_trim='S'; year_start=2017; year_end=2023; body_type='Sedan'; fuel_type='petrol'; engine='3.0L v6 twin-turbo'; engine_displacement_l=3.0; horsepower_hp=430; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[3]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 7:
  - CURRENT VALUE: version_or_trim='S'; year_start=2017; year_end=2023; body_type='Sedan'; fuel_type='petrol'; engine='3.0L v6 twin-turbo'; engine_displacement_l=3.0; horsepower_hp=430; transmission='8-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[3]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 8:
  - CURRENT VALUE: version_or_trim=None; year_start=2021; year_end=2024; body_type='Sedan'; fuel_type='mild_hybrid'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=330; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[1, 3]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 9:
  - CURRENT VALUE: version_or_trim='Trofeo'; year_start=2021; year_end=2024; body_type='Sedan'; fuel_type='petrol'; engine='3.8L v8 twin-turbo'; engine_displacement_l=3.8; horsepower_hp=580; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[2, 3]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP

### RUN1-14 — IL-confirmed|Maserati|GranCabrio

MODEL: IL-confirmed|Maserati|GranCabrio

CURRENT VALUE: clean/profile entry with 2 variants; year_start=2010; year_end=2019; profile_confidence=medium.

PROBLEM: MERGE with IL-likely GranCabrio. Preserve old 4.7 V8 440/460hp historical variants and absorb 2024 Trofeo/Folgore only if source-grounded. Do not leave two clean GranCabrio profiles.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Maserati GranCabrio.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Auto.co.il — מזראטי גראן-קבריו (2010-2019) מחירון רכב חדש ומפרט רכב - קטלוג אוטו — https://www.auto.co.il/model/maserati-grancabrio_g128
- repo_source[1]: iCar — מזראטי גראן קבריו - מחירון, חוות דעת, ומפרט טכני - iCar — https://www.icar.co.il/Maserati/Maserati_GranCabrio/

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: MERGE with IL-likely GranCabrio. Preserve old 4.7 V8 440/460hp historical variants and absorb 2024 Trofeo/Folgore only if source-grounded. Do not leave two clean GranCabrio profiles.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=2010; year_end=2013; body_type='Convertible'; fuel_type='petrol'; engine='4.7L v8'; engine_displacement_l=4.7; horsepower_hp=440; transmission='6-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 1]
  - PROBLEM: duplicate GranCabrio profiles
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into a single IL-confirmed GranCabrio profile; preserve historical and 2024 variants if grounded.
  - ACTION: MERGE/FIX
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='Sport / MC'; year_start=2012; year_end=2019; body_type='Convertible'; fuel_type='petrol'; engine='4.7L v8'; engine_displacement_l=4.7; horsepower_hp=460; transmission='6-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 1]
  - PROBLEM: duplicate GranCabrio profiles
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into a single IL-confirmed GranCabrio profile; preserve historical and 2024 variants if grounded.
  - ACTION: MERGE/FIX

### RUN1-15 — IL-likely|Maserati|GranCabrio

MODEL: IL-likely|Maserati|GranCabrio

CURRENT VALUE: clean/profile entry with 3 variants; year_start=2011; year_end=2024; profile_confidence=medium.

PROBLEM: MERGE into IL-confirmed GranCabrio. Trofeo 2024 is confirmed by Cartube Israel. Folgore must be kept only if a direct Israeli source in repo supports it; otherwise move Folgore to review non-blocking.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Maserati GranCabrio.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Auto.co.il — Maserati GranCabrio - Auto Israel — https://www.auto.co.il/model/maserati-grancabrio_g181
- repo_source[1]: Cartube.co.il — Maserati GranCabrio Trofeo / Folgore in Israel — https://www.cartube.co.il/חדשות-רכב/מזראטי-גראנקבריו-החדשה-נחשפת-בגרסת-הטרופאו
- repo_source[2]: Gear.co.il — Maserati GranCabrio 2011-2019 Specs — https://www.gear.co.il/מזראטי_גראן-קבריו

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: MERGE into IL-confirmed GranCabrio. Trofeo 2024 is confirmed by Cartube Israel. Folgore must be kept only if a direct Israeli source in repo supports it; otherwise move Folgore to review non-blocking.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim='Sport'; year_start=2011; year_end=2019; body_type='Convertible'; fuel_type='petrol'; engine='4.7L v8'; engine_displacement_l=4.7; horsepower_hp=460; transmission='6-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0, 2]
  - PROBLEM: duplicate GranCabrio profiles
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into a single IL-confirmed GranCabrio profile; preserve historical and 2024 variants if grounded.
  - ACTION: MERGE/FIX
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='Trofeo'; year_start=2024; year_end=2024; body_type='Convertible'; fuel_type='petrol'; engine='3.0L twin-turbo'; engine_displacement_l=3.0; horsepower_hp=550; transmission='8-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: duplicate GranCabrio profiles
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into a single IL-confirmed GranCabrio profile; preserve historical and 2024 variants if grounded.
  - ACTION: MERGE/FIX
- VARIANT 3:
  - CURRENT VALUE: version_or_trim='Folgore'; year_start=2024; year_end=2024; body_type='Convertible'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=761; transmission='single_speed'; drivetrain='AWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: duplicate GranCabrio profiles
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into a single IL-confirmed GranCabrio profile; preserve historical and 2024 variants if grounded. Folgore may remain clean only with direct Israeli source; otherwise move Folgore to review non-blocking.
  - ACTION: MERGE/FIX

### RUN1-16 — IL-confirmed|Maserati|GranTurismo

MODEL: IL-confirmed|Maserati|GranTurismo

CURRENT VALUE: clean/profile entry with 4 variants; year_start=2012; year_end=None; profile_confidence=medium.

PROBLEM: KEEP/FIX. Historical 4.2/4.7 variants and 2024 Modena/Trofeo are Israeli-grounded. Add/reconcile Folgore only if repo-local source supports Israeli availability; do not infer from global source alone. Check Trofeo horsepower remains 550hp, not 490hp.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Maserati GranTurismo.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Auto.co.il — מזראטי גרנטוריסמו דור 1 (2007-2019) - מפרט טכני — https://www.auto.co.il/model/maserati-granturismo_g1113
- repo_source[1]: Cartube.co.il — מזראטי משיקה בישראל את הגרנטוריסמו החדשה 2024 — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%96%D7%A8%D7%90%D7%98%D7%99-%D7%9E%D7%A9%D7%99%D7%A7%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%90%D7%AA-%D7%94%D7%92%D7%A8%D7%A0%D7%98%D7%95%D7%A8%D7%99%D7%A1%D7%9E%D7%95-%D7%94%D7%97%D7%93%D7%A9%D7%94-2024-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1-85-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: KEEP/FIX. Historical 4.2/4.7 variants and 2024 Modena/Trofeo are Israeli-grounded. Add/reconcile Folgore only if repo-local source supports Israeli availability; do not infer from global source alone. Check Trofeo horsepower remains 550hp, not 490hp.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=2012; year_end=2019; body_type='Coupe'; fuel_type='petrol'; engine='4.2L v8'; engine_displacement_l=4.2; horsepower_hp=405; transmission='6-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='Sport'; year_start=2012; year_end=2019; body_type='Coupe'; fuel_type='petrol'; engine='4.7L v8'; engine_displacement_l=4.7; horsepower_hp=460; transmission='6-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 3:
  - CURRENT VALUE: version_or_trim='Modena'; year_start=2024; year_end=None; body_type='Coupe'; fuel_type='petrol'; engine='3.0L v6 twin-turbo'; engine_displacement_l=3.0; horsepower_hp=490; transmission='8-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 4:
  - CURRENT VALUE: version_or_trim='Trofeo'; year_start=2024; year_end=None; body_type='Coupe'; fuel_type='petrol'; engine='3.0L v6 twin-turbo'; engine_displacement_l=3.0; horsepower_hp=550; transmission='8-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: Cartube source snippet title may typo Trofeo 490; technical fact is Trofeo 550hp
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Keep Trofeo at 550hp if source validates; do not downgrade to 490 based on typo.
  - ACTION: KEEP/FIX

### RUN1-17 — IL-confirmed|Maserati|Grecale

MODEL: IL-confirmed|Maserati|Grecale

CURRENT VALUE: clean/profile entry with 3 variants; year_start=2022; year_end=2024; profile_confidence=medium.

PROBLEM: FIX year_end for GT/Modena/Trofeo: 2026 Israeli price/spec source supports current Grecale, so do not close at 2024. Set year_end=None/current according to repo convention. Fix invalid source indexes [2] where only two sources exist.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Maserati Grecale.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Cartube — מזראטי גרקאלה (Grecale) בישראל - מחיר החל מ-570,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%96%D7%A8%D7%90%D7%98%D7%99-%D7%92%D7%A8%D7%A7%D7%90%D7%9C%D7%94-grecale-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-570,000-%D7%A9%D7%A7%D7%9C
- repo_source[1]: iCar — מזראטי גרקאלה - מחירון וקטלוג רכב — https://www.icar.co.il/%D7%9E%D7%96%D7%A8%D7%90%D7%98%D7%99/%D7%9E%D7%96%D7%A8%D7%90%D7%98%D7%99_%D7%92%D7%A8%D7%A7%D7%90%D7%9C%D7%94/

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: FIX year_end for GT/Modena/Trofeo: 2026 Israeli price/spec source supports current Grecale, so do not close at 2024. Set year_end=None/current according to repo convention. Fix invalid source indexes [2] where only two sources exist.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim='GT'; year_start=2022; year_end=2024; body_type='SUV'; fuel_type='mild_hybrid'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=300; transmission='8-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[1, 2]
  - PROBLEM: invalid source_indexes [2] for profile source count 2; year_end=2024 is stale; 2026 Israeli price/spec source supports current Grecale
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Set year_end=None/current for GT/Modena/Trofeo according to repo convention; fix invalid source refs.
  - ACTION: FIX
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='Modena'; year_start=2022; year_end=2024; body_type='SUV'; fuel_type='mild_hybrid'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=330; transmission='8-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[1, 2]
  - PROBLEM: invalid source_indexes [2] for profile source count 2; year_end=2024 is stale; 2026 Israeli price/spec source supports current Grecale
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Set year_end=None/current for GT/Modena/Trofeo according to repo convention; fix invalid source refs.
  - ACTION: FIX
- VARIANT 3:
  - CURRENT VALUE: version_or_trim='Trofeo'; year_start=2022; year_end=2024; body_type='SUV'; fuel_type='petrol'; engine='3.0L v6 twin-turbo'; engine_displacement_l=3.0; horsepower_hp=530; transmission='8-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[1, 2]
  - PROBLEM: invalid source_indexes [2] for profile source count 2; year_end=2024 is stale; 2026 Israeli price/spec source supports current Grecale
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Set year_end=None/current for GT/Modena/Trofeo according to repo convention; fix invalid source refs.
  - ACTION: FIX

### RUN1-18 — IL-confirmed|Maserati|MC20

MODEL: IL-confirmed|Maserati|MC20

CURRENT VALUE: clean/profile entry with 2 variants; year_start=2021; year_end=None; profile_confidence=medium.

PROBLEM: KEEP. MC20 and MC20 Cielo are Israeli-context models with 3.0 V6 twin-turbo 630hp, 8DCT, RWD. Keep support_level indirect/direct according to repo policy; ensure source grounding is not missing.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Maserati MC20.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Cartube.co.il — מזראטי MC20 נוחתת בישראל - מחיר החל מ-1.99 מיליון שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%96%D7%A8%D7%90%D7%98%D7%99-mc20-%D7%A0%D7%95%D7%97%D7%AA%D7%AA-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1-99-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C
- repo_source[1]: iCar.co.il — מזראטי MC20 Cielo: גרסת הגג הפתוח בישראל — https://www.icar.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA_%D7%A8%D7%9B%D7%91/%D7%9E%D7%96%D7%A8%D7%90%D7%98%D7%99_MC20_%D7%A1%D7%99%D7%99%D7%9C%D7%95_%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C/

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: KEEP. MC20 and MC20 Cielo are Israeli-context models with 3.0 V6 twin-turbo 630hp, 8DCT, RWD. Keep support_level indirect/direct according to repo policy; ensure source grounding is not missing.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=2021; year_end=None; body_type='Coupe'; fuel_type='petrol'; engine='3.0L v6 twin-turbo'; engine_displacement_l=3.0; horsepower_hp=630; transmission='8-speed dual_clutch'; drivetrain='RWD'; support_level='indirect'; source_indexes=[0]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='Cielo'; year_start=2022; year_end=None; body_type='Convertible'; fuel_type='petrol'; engine='3.0L v6 twin-turbo'; engine_displacement_l=3.0; horsepower_hp=630; transmission='8-speed dual_clutch'; drivetrain='RWD'; support_level='indirect'; source_indexes=[1]
  - PROBLEM: No blocking technical problem found in this RUN1 audit; still require valid source_indexes and field_sources.
  - WEB-VALIDATED FACT: Repo-local Israeli source plus embedded web ledger supports KEEP if source refs are valid.
  - TARGET VALUE: Keep technical values if source_indexes and field_sources are valid and consistent.
  - ACTION: KEEP

### RUN1-19 — IL-likely|Maserati|Quattroporte

MODEL: IL-likely|Maserati|Quattroporte

CURRENT VALUE: clean/profile entry with 8 variants; year_start=2004; year_end=2023; profile_confidence=medium.

PROBLEM: MERGE into IL-confirmed Quattroporte; do not keep duplicate IL-likely profile. Preserve older 2004-2012 variants and 2013-2023 variants with lineage.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Maserati Quattroporte.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: iCar — מזראטי קוואטרופורטה - מפרט טכני, גרסאות ומחירים — https://www.icar.co.il/%D7%9E%D7%96%D7%A8%D7%90%D7%98%D7%99/%D7%9E%D7%96%D7%A8%D7%90%D7%98%D7%99_%D7%A7%D7%95%D7%95%D7%90%D7%98%D7%A8%D7%95%D7%A4%D7%95%D7%A8%D7%98%D7%94/
- repo_source[1]: Auto.co.il — מזראטי קוואטרופורטה 2004-2012 - מפרט טכני — https://www.auto.co.il/model/maserati-quattroporte_g144

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: MERGE into IL-confirmed Quattroporte; do not keep duplicate IL-likely profile. Preserve older 2004-2012 variants and 2013-2023 variants with lineage.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim=None; year_start=2004; year_end=2012; body_type='Sedan'; fuel_type='petrol'; engine='4.2L v8'; engine_displacement_l=4.2; horsepower_hp=400; transmission='6-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='S'; year_start=2008; year_end=2012; body_type='Sedan'; fuel_type='petrol'; engine='4.7L v8'; engine_displacement_l=4.7; horsepower_hp=430; transmission='6-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 3:
  - CURRENT VALUE: version_or_trim='Sport GT S'; year_start=2009; year_end=2012; body_type='Sedan'; fuel_type='petrol'; engine='4.7L v8'; engine_displacement_l=4.7; horsepower_hp=440; transmission='6-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 4:
  - CURRENT VALUE: version_or_trim=None; year_start=2016; year_end=2023; body_type='Sedan'; fuel_type='petrol'; engine='3.0L twin-turbo v6'; engine_displacement_l=3.0; horsepower_hp=350; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 5:
  - CURRENT VALUE: version_or_trim='S'; year_start=2013; year_end=2017; body_type='Sedan'; fuel_type='petrol'; engine='3.0L twin-turbo v6'; engine_displacement_l=3.0; horsepower_hp=410; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 6:
  - CURRENT VALUE: version_or_trim='S'; year_start=2017; year_end=2023; body_type='Sedan'; fuel_type='petrol'; engine='3.0L twin-turbo v6'; engine_displacement_l=3.0; horsepower_hp=430; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 7:
  - CURRENT VALUE: version_or_trim='GTS'; year_start=2013; year_end=2023; body_type='Sedan'; fuel_type='petrol'; engine='3.8L twin-turbo v8'; engine_displacement_l=3.8; horsepower_hp=530; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 8:
  - CURRENT VALUE: version_or_trim='Trofeo'; year_start=2021; year_end=2023; body_type='Sedan'; fuel_type='petrol'; engine='3.8L twin-turbo v8'; engine_displacement_l=3.8; horsepower_hp=580; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX

### RUN1-20 — IL-confirmed|Maserati|Quattroporte

MODEL: IL-confirmed|Maserati|Quattroporte

CURRENT VALUE: clean/profile entry with 7 variants; year_start=2013; year_end=2024; profile_confidence=medium.

PROBLEM: MERGE/FIX target clean profile. Absorb all valid older and newer Quattroporte variants. Keep Trofeo 2021-2024 at 580hp; keep S Q4 AWD 410/430hp; preserve diesel 275hp and base 330/350hp if grounded. Delete duplicate after merge.

WEB-VALIDATED FACT: See source ledger above and per-variant table below. Israeli-market clean is allowed only when supported by official importer/Israeli Tier 2 sources or an explicitly justified Tier 3 historical/parallel-import policy.

SOURCE: repo-local sources for this profile plus embedded source ledger entries relevant to Maserati Quattroporte.

Repo-local sources to preserve/fix field_sources against:
- repo_source[0]: Cartube — מזראטי קוואטרופורטה החדשה בישראל – מחיר החל מ- 900 אלף שקל — https://www.cartube.co.il/חדשות-רכב/מזראטי-קוואטרופורטה-החדשה-בישראל-מחיר-החל-מ-900-אלף-שקל
- repo_source[1]: Auto.co.il — מזראטי קוואטרופורטה דיזל בישראל — https://www.auto.co.il/article/111005-local-news-maserati-quattroporte
- repo_source[2]: Auto.co.il — מזראטי מציגה גרסת כניסה חדשה לקוואטרופורטה בישראל — https://www.auto.co.il/article/111666-local-news-maserati-quattroporte
- repo_source[3]: Cartube — מזראטי קוואטרופורטה 2016 החדשה בישראל - מחיר החל מ- 989,000 שקל — https://www.cartube.co.il/חדשות-רכב/מזראטי-קוואטרופורטה-2016-החדשה-בישראל-מחיר-החל-מ-989000-שקל
- repo_source[4]: Cartube — מזראטי קוואטרופורטה טרופאו V8 בישראל - מחיר החל מ-1,350,000 שקל — https://www.cartube.co.il/חדשות-רכב/מזראטי-קוואטרופורטה-טרופאו-v8-בישראל-מחיר-החל-מ-1350000-שקל

TARGET VALUE: Apply model-level action plus variant-level decisions below.

ACTION: MERGE/FIX target clean profile. Absorb all valid older and newer Quattroporte variants. Keep Trofeo 2021-2024 at 580hp; keep S Q4 AWD 410/430hp; preserve diesel 275hp and base 330/350hp if grounded. Delete duplicate after merge.

#### Variant-level table

- VARIANT 1:
  - CURRENT VALUE: version_or_trim='GTS'; year_start=2013; year_end=2020; body_type='Sedan'; fuel_type='petrol'; engine='3.8L turbo v8'; engine_displacement_l=3.8; horsepower_hp=530; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[0]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 2:
  - CURRENT VALUE: version_or_trim='S Q4'; year_start=2013; year_end=2016; body_type='Sedan'; fuel_type='petrol'; engine='3.0L turbo v6'; engine_displacement_l=3.0; horsepower_hp=410; transmission='8-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[0]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 3:
  - CURRENT VALUE: version_or_trim=None; year_start=2014; year_end=2018; body_type='Sedan'; fuel_type='diesel'; engine='3.0L turbo v6'; engine_displacement_l=3.0; horsepower_hp=275; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[1]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 4:
  - CURRENT VALUE: version_or_trim=None; year_start=2014; year_end=2016; body_type='Sedan'; fuel_type='petrol'; engine='3.0L turbo v6'; engine_displacement_l=3.0; horsepower_hp=330; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[2]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 5:
  - CURRENT VALUE: version_or_trim='S Q4'; year_start=2016; year_end=2023; body_type='Sedan'; fuel_type='petrol'; engine='3.0L turbo v6'; engine_displacement_l=3.0; horsepower_hp=430; transmission='8-speed automatic'; drivetrain='AWD'; support_level='direct'; source_indexes=[3]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 6:
  - CURRENT VALUE: version_or_trim=None; year_start=2016; year_end=2023; body_type='Sedan'; fuel_type='petrol'; engine='3.0L turbo v6'; engine_displacement_l=3.0; horsepower_hp=350; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[3]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX
- VARIANT 7:
  - CURRENT VALUE: version_or_trim='Trofeo'; year_start=2021; year_end=2024; body_type='Sedan'; fuel_type='petrol'; engine='3.8L turbo v8'; engine_displacement_l=3.8; horsepower_hp=580; transmission='8-speed automatic'; drivetrain='RWD'; support_level='direct'; source_indexes=[4]
  - PROBLEM: duplicate Quattroporte profiles / overlapping technical variants
  - WEB-VALIDATED FACT: Use model-level web fact and repo-local source list; global-only evidence is not sufficient for clean.
  - TARGET VALUE: Merge into one IL-confirmed Quattroporte profile with lineage and delete duplicate profile.
  - ACTION: MERGE/FIX

## Required post-implementation checks for RUN 1 only

Run:

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Then inspect actual generated files, not only console output:

- `data/model_technical_catalog_il.json`
- `data/model_technical_catalog_il_readiness.json`
- `data/model_technical_catalog_il_review.json`
- `data/model_technical_catalog_il_archive.json`
- `data/model_technical_catalog_il_quality_scan.json`
- `compute_resume_state()` output if available in repo
- unmatched/split aliases state
- active blockers and review-only entries touched by RUN 1

Known local test environment issue from this extracted ZIP: `pytest -q` failed because `streamlit` was not installed while importing `app.py` in `tests/test_selectable_provider_and_github.py`. In the real repo/Codex environment, install dependencies or report this explicitly as a dependency issue; do not hide it.

## Completion report required from Codex

Report only for RUN 1:

1. Files changed.
2. Exact before/after counts for models/variants touched by RUN 1.
3. Confirmation that all 20 RUN 1 profiles and all 73 RUN 1 variants were applied, merged, moved to review/archive, or explicitly reported as conflicting.
4. Test results.
5. Confirmation that temporary `codex_tasks/BATCH26_RUN1_*.md` files were deleted before final commit.
6. Remaining issues, if any.


# ==============================
# RUN2
# source: BATCH26_RUN2_VARIANT_LEVEL_CODEX_TASK.md
# ==============================

# BATCH26 RUN 2 ONLY — variant-level web-validated Codex task

TEMPORARY FILE RULE: This is a temporary instruction file. After RUN 2 is fully applied and verified, delete `codex_tasks/BATCH26_RUN2_*.md` from the repo before final commit unless the user explicitly requests keeping it.

DO NOT BROWSE THE INTERNET.
All web-validation facts and target corrections for RUN 2 are embedded here. Use this file as the single source of truth for this run only.
Do not apply RUN 1, RUN 3, later clean runs, FINAL blockers, or any unified batch task.
Do not apply corrections that are not instructed here. If repo-local evidence conflicts with this task file, report the conflict instead of guessing.
If a variant cannot be grounded with the embedded facts or repo-local sources, move it to non-blocking archive/review with clear reason and lineage rather than fabricating data.

## Scope

```text
BATCH26 RUN 2 ONLY
from: IL-confirmed|Maxus|Euniq 5
to: IL-confirmed|Mazda|Mazda2
profiles: 20
technical variants covered: 57/57
source catalog indices: 526-545 inclusive
```

## Required execution checks

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Also audit actual generated files, not only console output:

```text
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

## Local pre-check result from uploaded ZIP

```text
python -m compileall scripts                  PASS
python -m scripts.catalog_validation          PASS
python -m scripts.catalog_quality_scan        PASS
python -m pytest -q                           FAIL in this environment only because streamlit is missing
```

If pytest fails because `streamlit` is missing, report it explicitly as dependency/test-environment issue. Do not hide it.

## Web-validation source package — RUN 2 only

Use these web-validation facts as embedded internet grounding. Do not browse.

### Maxus grounding
- Maxus Israel / iCar local pages confirm Maxus Israel presence and Euniq models; EV rows must use electric schema: `engine_displacement_l=null`, `fuel_type=electric`, valid single-speed/direct-drive transmission, and drivetrain must not be blank.
- Euniq 6 Israel: Auto/iCar/Cartube Israeli sources support a single electric crossover/SUV row around 174–175 hp, single-speed transmission and FWD; keep repo 174 hp if local repo sources use 174, do not invent extra trims.
- T90 is not safe as a 177 hp clean current Israeli row: several Israel-specific 2024 launch reports say the T90 EV marketed for Israel has 150 kW / 201 hp and RWD, while 177 hp is a global/European 130 kW spec. Prefer Israel-specific sources over global specs. If implementation cannot reconcile this with repo-local evidence, move T90 to non-blocking review rather than leaving a wrong clean row.
- SOURCE URL: https://maxusofficial.co.il/
- SOURCE URL: https://www.icar.co.il/מקסוס/
- SOURCE URL: https://www.auto.co.il/cars/maxus/euniq-6/
- SOURCE URL: https://www.cartube.co.il/חדשות-רכב/מקסוס-איוניק-6-החשמלי-בישראל-מחיר-171000-שקל
- SOURCE URL: https://www.autocom.co.il/טנדרים-pick-up-חשמליים-מתוצרת-מקסוס-בדרכם-ל/
- SOURCE URL: https://www.israelhayom.co.il/auto/article/15608743

### Mazda grounding
- Mazda Israel official 2026 price/model pages support current Mazda2, Mazda3, CX-5, CX-90 and other current models. Historical Mazda rows must rely on iCar/Auto/Carzone/KML as Tier 2/3 Israeli catalog sources.
- Mazda CX-5: Mazda Israel 03/2026 price list confirms current CX-5 with 2.5L grades including Comfort/Executive/Pure Black Turbo; do not leave current CX-5 artificially closed at 2024 if repo fields can be grounded. Official 2.5L PDF confirms current technical document and distinguishes 2.5 naturally aspirated and 2.5 turbo rows. Do not invent unsupported trim detail beyond source support.
- Mazda CX-50: Israeli sources in this run are global/preview/editorial only; no confirmed Israeli-market clean profile. Keep out of clean; archive/review non-blocking.
- Mazda CX-60: official/repo sources support CX-60 PHEV 327 hp in Israel; global-reference-only duplicate must not remain a separate clean profile when IL-confirmed CX-60 exists. The 3.3 mild-hybrid 284 hp row requires strong Israeli official local evidence before clean; otherwise move that row to review under CX-60, not separate global clean.
- Mazda CX-80: Israeli evidence in this ZIP is indirect/preview. Do not keep as verified clean unless repo-local evidence proves Israeli marketing/sales; otherwise move to non-blocking review.
- Mazda CX-90: Mazda Israel official current page now lists the Israeli CX-90 as 3.3L e-Skyactiv-G / 345 hp, and 2026 local articles confirm 3.3L AWD grades. The existing global-reference-only 2.5 PHEV 327 hp row is not supported as the current official Israeli CX-90 clean row. Move it to review/archive or replace with correct IL-confirmed 3.3L 345 hp row only if repo schema/source policy allows adding from embedded official facts.
- Mazda2: Israeli Auto/Carzone sources support 1.5L 116 hp automatic FWD current hatchback; do not keep mild_hybrid unless a local source explicitly supports mild-hybrid designation. If the source says petrol atmospheric, normalize fuel_type to petrol rather than mild_hybrid.
- SOURCE URL: https://www.mazda.co.il/car-list
- SOURCE URL: https://www.mazda.co.il/model/12/mazda-cx-5
- SOURCE URL: https://api.mazda.co.il/Uploads/New/CX-5/מפרט/39875%20Mazda%20CX-5%202500.pdf
- SOURCE URL: https://www.mazda.co.il/model/1001/mazda-cx-90
- SOURCE URL: https://www.auto.co.il/articles/car-news/local-news/mazda-cx-90-new-prices/
- SOURCE URL: https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- SOURCE URL: https://www.auto.co.il/cars/mazda/2/
- SOURCE URL: https://www.carzone.co.il/Mazda/2/2025/
- SOURCE URL: https://www.icar.co.il/מאזדה/
- SOURCE URL: https://www.auto.co.il/catalog/mazda

## Model and variant decisions

---

## MODEL: IL-confirmed|Maxus|Euniq 5

CATALOG INDEX: 526

CURRENT VALUE: clean profile with 1 technical variants; profile years=2021-2024; confidence=medium.

PROBLEM: Israeli Maxus/iCar/Cartube sources ground Euniq 5 as an electric MPV. Keep EV schema; do not extend beyond 2024 unless repo-local current source exists.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [1] Cartube Israel / editorial: מקסוס איוניק 5 בישראל - מחיר החל מ- 198,194 שקלים — https://www.cartube.co.il/%חדשות-רכב/מקסוס-איוניק-5-בישראל-מחיר-החל-מ-198194-שקלים
- repo source [2] iCar Israel / catalog: מקסוס Euniq 5 - מחירון רכב, מבחני דרכים ומפרטים טכניים — https://www.icar.co.il/%D7%9E%D7%A7%D7%A1%D7%95%D7%A1/%D7%9E%D7%A7%D7%A1%D7%95%D7%A1_Euniq_5/%D7%9E%D7%A7%D7%A1%D7%95%D7%A1_Euniq_5_%D7%97%D7%93%D7%A9/
- repo source [3] Maxus Israel (China Motors) / official_importer: Maxus Euniq 5 - Official Page — https://www.maxus.co.il/models/euniq-5/

TARGET VALUE: KEEP. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: KEEP

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2021-2024; body=MPV; fuel=electric; engine=electric; displacement=null; hp=177; trans=single_speed; drive=FWD; support=direct; source_indexes=[1, 2, 3] | Israeli Maxus/iCar/Cartube sources ground Euniq 5 as an electric MPV. Keep EV schema; do not extend beyond 2024 unless repo-local current source exists. | Israeli Maxus/iCar/Cartube sources ground Euniq 5 as an electric MPV. Keep EV schema; do not extend beyond 2024 unless repo-local current source exists. | trim=null; years=2021-2024; body=MPV; fuel=electric; engine=electric; displacement=null; hp=177; trans=single_speed; drive=FWD; support=direct; source_indexes=[1, 2, 3] | KEEP |

---

## MODEL: IL-confirmed|Maxus|Euniq 6

CATALOG INDEX: 527

CURRENT VALUE: clean profile with 1 technical variants; profile years=2022-2024; confidence=medium.

PROBLEM: Israeli Auto/iCar/Cartube sources ground Euniq 6 as one electric SUV/crossover row around 174-175 hp. Keep repo 174 hp if field_sources support it.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] Cartube IL / editorial: מקסוס EUNIQ 6 החשמלי בישראל - מחיר החל מ-171,000 שקלים — https://www.cartube.co.il/חדשות-רכב/מקסוס-euniq-6-החשמלי-בישראל-מחיר-החל-מ-171000-שקלים
- repo source [1] iCar IL / catalog: מקסוס Euniq 6 - מחירון, מפרטים, אמינות וחוות דעת — https://www.icar.co.il/מקסוס/מקסוס_אי-יוניק_6/

TARGET VALUE: KEEP. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: KEEP

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2022-2024; body=SUV; fuel=electric; engine=electric; displacement=null; hp=174; trans=single_speed; drive=FWD; support=direct; source_indexes=[0, 1] | Israeli Auto/iCar/Cartube sources ground Euniq 6 as one electric SUV/crossover row around 174-175 hp. Keep repo 174 hp if field_sources support it. | Israeli Auto/iCar/Cartube sources ground Euniq 6 as one electric SUV/crossover row around 174-175 hp. Keep repo 174 hp if field_sources support it. | trim=null; years=2022-2024; body=SUV; fuel=electric; engine=electric; displacement=null; hp=174; trans=single_speed; drive=FWD; support=direct; source_indexes=[0, 1] | KEEP |

---

## MODEL: IL-confirmed|Maxus|T90

CATALOG INDEX: 528

CURRENT VALUE: clean profile with 1 technical variants; profile years=2023-None; confidence=medium.

PROBLEM: Existing 177 hp row conflicts with Israel-specific 2024 launch sources for T90 EV at 150 kW / 201 hp RWD. Fix to Israeli T90 EV 201 hp if repo policy accepts embedded sources; otherwise move non-blocking review.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] Cartube Israel / editorial: טנדר חשמלי ראשון בישראל: מקסוס T90 EV - מחיר החל מ- 269,000 שקל — https://www.cartube.co.il/חדשות-רכב/טנדר-חשמלי-ראשון-בישראל-מקסוס-t90-ev-החל-מ-269-000-שקל
- repo source [1] Auto.co.il / catalog: מקסוס T90 EV - מחירון, מפרטים, אמינות ועוד — https://www.auto.co.il/model/maxus-t90-ev_g1445

TARGET VALUE: FIX OR MOVE TO REVIEW. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: FIX OR MOVE TO REVIEW

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2023-null; body=Pickup; fuel=electric; engine=electric; displacement=null; hp=177; trans=single_speed; drive=RWD; support=direct; source_indexes=[0, 1] | Existing 177 hp row conflicts with Israel-specific 2024 launch sources for T90 EV at 150 kW / 201 hp RWD. Fix to Israeli T90 EV 201 hp if repo policy accepts embedded sources; otherwise move non-blocking review. | Existing 177 hp row conflicts with Israel-specific 2024 launch sources for T90 EV at 150 kW / 201 hp RWD. Fix to Israeli T90 EV 201 hp if repo policy accepts embedded sources; otherwise move non-blocking review. | Target clean row should be Maxus T90 EV / alias T90; year_start=2024; body=Pickup; fuel=electric; engine=electric; displacement=null; hp=201; transmission=single_speed/direct_drive per schema; drivetrain=RWD. If repo-local policy cannot accept embedded Israeli sources, move this row to non-blocking review with conflict reason. | FIX / MOVE TO REVIEW |

---

## MODEL: IL-confirmed|Mazda|121

CATALOG INDEX: 529

CURRENT VALUE: clean profile with 2 technical variants; profile years=1993-1997; confidence=medium.

PROBLEM: Use IL-confirmed historical profile as primary; global-reference-only 121 is duplicate and must not remain separate clean.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] iCar Israel / catalog: מאזדה 121 (1993-1997) מחירון רכב, מפרט טכני וחוות דעת - iCar — https://www.icar.co.il/mazda/mazda_121/
- repo source [1] Auto.co.il / catalog: מאזדה 121 - קטלוג רכבים מקיף - אוטו — https://www.auto.co.il/catalog/mazda/121

TARGET VALUE: KEEP PRIMARY + MERGE DUPLICATE. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: KEEP PRIMARY + MERGE DUPLICATE

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=1993-1997; body=Sedan; fuel=petrol; engine=1.3L; displacement=1.3; hp=72; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[0, 1] | Use IL-confirmed historical profile as primary; global-reference-only 121 is duplicate and must not remain separate clean. | Use IL-confirmed historical profile as primary; global-reference-only 121 is duplicate and must not remain separate clean. | trim=null; years=1993-1997; body=Sedan; fuel=petrol; engine=1.3L; displacement=1.3; hp=72; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[0, 1] | KEEP PRIMARY + MERGE DUPLICATE |
| 2 | trim=null; years=1993-1997; body=Sedan; fuel=petrol; engine=1.3L; displacement=1.3; hp=72; trans=5-speed manual; drive=FWD; support=direct; source_indexes=[0, 1] | Use IL-confirmed historical profile as primary; global-reference-only 121 is duplicate and must not remain separate clean. | Use IL-confirmed historical profile as primary; global-reference-only 121 is duplicate and must not remain separate clean. | trim=null; years=1993-1997; body=Sedan; fuel=petrol; engine=1.3L; displacement=1.3; hp=72; trans=5-speed manual; drive=FWD; support=direct; source_indexes=[0, 1] | KEEP PRIMARY + MERGE DUPLICATE |

---

## MODEL: global-reference-only|Mazda|121

CATALOG INDEX: 530

CURRENT VALUE: clean profile with 2 technical variants; profile years=1993-1997; confidence=medium.

PROBLEM: Duplicate of IL-confirmed Mazda 121; preserve lineage/alias and archive/delete duplicate clean profile.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [1] Auto.co.il / editorial: מאזדה 121 (1993-1997) - מפרט טכני, מחירון | אוטו — https://www.auto.co.il/model/mazda-121_g117
- repo source [2] KML / catalog: מחירון רכב מאזדה 121 - קמ"ל — https://kml.co.il/car/mazda/121

TARGET VALUE: MERGE / ARCHIVE NON-BLOCKING. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: MERGE / ARCHIVE NON-BLOCKING

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=1993-1997; body=Sedan; fuel=petrol; engine=1.3L; displacement=1.3; hp=72; trans=5-speed manual; drive=FWD; support=direct; source_indexes=[1, 2] | Duplicate of IL-confirmed Mazda 121; preserve lineage/alias and archive/delete duplicate clean profile. | Duplicate of IL-confirmed Mazda 121; preserve lineage/alias and archive/delete duplicate clean profile. | Remove from clean as separate profile; merge into IL-confirmed sibling or archive non-blocking with alias/lineage. | MERGE / ARCHIVE NON-BLOCKING |
| 2 | trim=null; years=1993-1997; body=Sedan; fuel=petrol; engine=1.3L; displacement=1.3; hp=72; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1, 2] | Duplicate of IL-confirmed Mazda 121; preserve lineage/alias and archive/delete duplicate clean profile. | Duplicate of IL-confirmed Mazda 121; preserve lineage/alias and archive/delete duplicate clean profile. | Remove from clean as separate profile; merge into IL-confirmed sibling or archive non-blocking with alias/lineage. | MERGE / ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mazda|323

CATALOG INDEX: 531

CURRENT VALUE: clean profile with 9 technical variants; profile years=1990-2004; confidence=medium.

PROBLEM: Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] iCar / Israeli Catalog: מאזדה 323 לאנטיס (1998-2004) מפרט טכני — https://www.icar.co.il/מאזדה/מאזדה_323_לאנטיס/מאזדה_323_לאנטיס_יד_שניה_דגם_1/
- repo source [1] Auto.co.il / Israeli Catalog: מאזדה 323 / לאנטיס 1995 - 1998 מפרט — https://www.auto.co.il/model/mazda-323_g210
- repo source [2] Auto.co.il / Israeli Catalog: מאזדה 323 1990 - 1995 מפרט — https://www.auto.co.il/model/mazda-323_g209

TARGET VALUE: KEEP. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: KEEP

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=1990-1995; body=Sedan; fuel=petrol; engine=1.6L; displacement=1.6; hp=88; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[2] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=null; years=1990-1995; body=Sedan; fuel=petrol; engine=1.6L; displacement=1.6; hp=88; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[2] | KEEP |
| 2 | trim=null; years=1995-1998; body=Sedan; fuel=petrol; engine=1.6L; displacement=1.6; hp=90; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=null; years=1995-1998; body=Sedan; fuel=petrol; engine=1.6L; displacement=1.6; hp=90; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1] | KEEP |
| 3 | trim=null; years=1995-1998; body=Sedan; fuel=petrol; engine=1.8L; displacement=1.8; hp=114; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=null; years=1995-1998; body=Sedan; fuel=petrol; engine=1.8L; displacement=1.8; hp=114; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1] | KEEP |
| 4 | trim=null; years=1995-1998; body=Hatchback; fuel=petrol; engine=1.6L; displacement=1.6; hp=90; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=null; years=1995-1998; body=Hatchback; fuel=petrol; engine=1.6L; displacement=1.6; hp=90; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1] | KEEP |
| 5 | trim=null; years=1995-1998; body=Hatchback; fuel=petrol; engine=1.8L; displacement=1.8; hp=114; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=null; years=1995-1998; body=Hatchback; fuel=petrol; engine=1.8L; displacement=1.8; hp=114; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1] | KEEP |
| 6 | trim=null; years=1998-2004; body=Sedan; fuel=petrol; engine=1.6L; displacement=1.6; hp=105; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[0] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=null; years=1998-2004; body=Sedan; fuel=petrol; engine=1.6L; displacement=1.6; hp=105; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[0] | KEEP |
| 7 | trim=null; years=1998-2004; body=Hatchback; fuel=petrol; engine=1.6L; displacement=1.6; hp=105; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[0] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=null; years=1998-2004; body=Hatchback; fuel=petrol; engine=1.6L; displacement=1.6; hp=105; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[0] | KEEP |
| 8 | trim=null; years=1998-2001; body=Sedan; fuel=petrol; engine=1.8L; displacement=1.8; hp=114; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[0] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=null; years=1998-2001; body=Sedan; fuel=petrol; engine=1.8L; displacement=1.8; hp=114; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[0] | KEEP |
| 9 | trim=null; years=2001-2004; body=Sedan; fuel=petrol; engine=2.0L; displacement=2.0; hp=131; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[0] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=null; years=2001-2004; body=Sedan; fuel=petrol; engine=2.0L; displacement=2.0; hp=131; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[0] | KEEP |

---

## MODEL: IL-confirmed|Mazda|626

CATALOG INDEX: 532

CURRENT VALUE: clean profile with 5 technical variants; profile years=1992-2002; confidence=medium.

PROBLEM: Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [1186] Auto.co.il / editorial: מאזדה 626 (1998-2002) - מפרט טכני — https://www.auto.co.il/model/mazda-626_g172
- repo source [1187] iCar.co.il / catalog: מאזדה 626 דור 4 (1992-1997) - מפרט טכני — https://www.icar.co.il/mazda/626/1992/
- repo source [1188] KML / catalog: מאזדה 626 סטיישן 1998-2002 2.0 GLX מפרט טכני — https://kml.co.il/car/mazda_626_1998-2002

TARGET VALUE: KEEP. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: KEEP

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=GLX; years=1992-1997; body=Sedan; fuel=petrol; engine=2.0L; displacement=2.0; hp=115; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1187] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=GLX; years=1992-1997; body=Sedan; fuel=petrol; engine=2.0L; displacement=2.0; hp=115; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1187] | KEEP |
| 2 | trim=GLX; years=1992-1997; body=Hatchback; fuel=petrol; engine=2.0L; displacement=2.0; hp=115; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1187] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=GLX; years=1992-1997; body=Hatchback; fuel=petrol; engine=2.0L; displacement=2.0; hp=115; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1187] | KEEP |
| 3 | trim=GLX; years=1997-2002; body=Sedan; fuel=petrol; engine=2.0L; displacement=2.0; hp=136; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1186] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=GLX; years=1997-2002; body=Sedan; fuel=petrol; engine=2.0L; displacement=2.0; hp=136; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1186] | KEEP |
| 4 | trim=GLX; years=1997-2002; body=Hatchback; fuel=petrol; engine=2.0L; displacement=2.0; hp=136; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1186] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=GLX; years=1997-2002; body=Hatchback; fuel=petrol; engine=2.0L; displacement=2.0; hp=136; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1186] | KEEP |
| 5 | trim=GLX; years=1998-2002; body=Estate; fuel=petrol; engine=2.0L; displacement=2.0; hp=136; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1186, 1188] | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | Historical Israeli catalog sources support rows; preserve as historical clean if field_sources/source_indexes valid. | trim=GLX; years=1998-2002; body=Estate; fuel=petrol; engine=2.0L; displacement=2.0; hp=136; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1186, 1188] | KEEP |

---

## MODEL: IL-confirmed|Mazda|BT-50

CATALOG INDEX: 533

CURRENT VALUE: clean profile with 4 technical variants; profile years=2007-2011; confidence=medium.

PROBLEM: Use IL-confirmed profile as primary; global-reference-only BT-50 is duplicate and must not remain separate clean.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] Auto.co.il / israeli_editorial_and_catalog: מאזדה BT-50 (2007-2011) - מחירון, מפרט טכני וחוות דעת — https://www.auto.co.il/model/mazda-bt-50_g197
- repo source [1] iCar / israeli_editorial_and_catalog: מאזדה BT50 2007-2011 - מחירון ומידע — https://www.icar.co.il/Mazda/Mazda_BT-50/

TARGET VALUE: KEEP PRIMARY + MERGE DUPLICATE. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: KEEP PRIMARY + MERGE DUPLICATE

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2007-2011; body=Pickup; fuel=diesel; engine=2.5L turbo; displacement=2.5; hp=143; trans=5-speed manual; drive=RWD; support=direct; source_indexes=[0, 1] | Use IL-confirmed profile as primary; global-reference-only BT-50 is duplicate and must not remain separate clean. | Use IL-confirmed profile as primary; global-reference-only BT-50 is duplicate and must not remain separate clean. | trim=null; years=2007-2011; body=Pickup; fuel=diesel; engine=2.5L turbo; displacement=2.5; hp=143; trans=5-speed manual; drive=RWD; support=direct; source_indexes=[0, 1] | KEEP PRIMARY + MERGE DUPLICATE |
| 2 | trim=null; years=2007-2011; body=Pickup; fuel=diesel; engine=2.5L turbo; displacement=2.5; hp=143; trans=5-speed automatic; drive=RWD; support=direct; source_indexes=[0, 1] | Use IL-confirmed profile as primary; global-reference-only BT-50 is duplicate and must not remain separate clean. | Use IL-confirmed profile as primary; global-reference-only BT-50 is duplicate and must not remain separate clean. | trim=null; years=2007-2011; body=Pickup; fuel=diesel; engine=2.5L turbo; displacement=2.5; hp=143; trans=5-speed automatic; drive=RWD; support=direct; source_indexes=[0, 1] | KEEP PRIMARY + MERGE DUPLICATE |
| 3 | trim=null; years=2007-2011; body=Pickup; fuel=diesel; engine=2.5L turbo; displacement=2.5; hp=143; trans=5-speed manual; drive=4WD; support=direct; source_indexes=[0, 1] | Use IL-confirmed profile as primary; global-reference-only BT-50 is duplicate and must not remain separate clean. | Use IL-confirmed profile as primary; global-reference-only BT-50 is duplicate and must not remain separate clean. | trim=null; years=2007-2011; body=Pickup; fuel=diesel; engine=2.5L turbo; displacement=2.5; hp=143; trans=5-speed manual; drive=4WD; support=direct; source_indexes=[0, 1] | KEEP PRIMARY + MERGE DUPLICATE |
| 4 | trim=null; years=2007-2011; body=Pickup; fuel=diesel; engine=2.5L turbo; displacement=2.5; hp=143; trans=5-speed automatic; drive=4WD; support=direct; source_indexes=[0, 1] | Use IL-confirmed profile as primary; global-reference-only BT-50 is duplicate and must not remain separate clean. | Use IL-confirmed profile as primary; global-reference-only BT-50 is duplicate and must not remain separate clean. | trim=null; years=2007-2011; body=Pickup; fuel=diesel; engine=2.5L turbo; displacement=2.5; hp=143; trans=5-speed automatic; drive=4WD; support=direct; source_indexes=[0, 1] | KEEP PRIMARY + MERGE DUPLICATE |

---

## MODEL: global-reference-only|Mazda|BT-50

CATALOG INDEX: 534

CURRENT VALUE: clean profile with 4 technical variants; profile years=2007-2011; confidence=medium.

PROBLEM: Duplicate of IL-confirmed Mazda BT-50; preserve lineage/alias and archive/delete duplicate clean profile.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [1] iCar / specs_catalog: מאזדה BT50 (2007-2011) - מחירון, מפרטים, ואבזור — https://www.icar.co.il/%D7%9E%D7%90%D7%96%D7%93%D7%94/%D7%9E%D7%90%D7%96%D7%93%D7%94_BT50/%D7%9E%D7%90%D7%96%D7%93%D7%94_BT50_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%931/
- repo source [2] Auto.co.il / specs_catalog: מאזדה BT-50 (2007-2011) - חוות דעת, מחירון ומפרט טכני — https://www.auto.co.il/model/mazda-bt-50_g162
- repo source [3] Cartube.co.il / editorial_article: ה- BT-50 הנוכחי שהוצג ב-2011 מעולם לא שווק בישראל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%90%D7%96%D7%93%D7%94-bt-50-%D7%94%D7%97%D7%93%D7%A9-%D7%9E%D7%AA%D7%99%D7%97%D7%AA-%D7%A4%D7%A0%D7%99%D7%9D-%D7%99%D7%92%D7%99%D7%A2-%D7%90%D7%9C%D7%99%D7%A0%D7%95

TARGET VALUE: MERGE / ARCHIVE NON-BLOCKING. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: MERGE / ARCHIVE NON-BLOCKING

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2007-2011; body=Pickup; fuel=diesel; engine=2.5L turbo; displacement=2.5; hp=143; trans=5-speed manual; drive=RWD; support=direct; source_indexes=[1, 2, 3] | Duplicate of IL-confirmed Mazda BT-50; preserve lineage/alias and archive/delete duplicate clean profile. | Duplicate of IL-confirmed Mazda BT-50; preserve lineage/alias and archive/delete duplicate clean profile. | Remove from clean as separate profile; merge into IL-confirmed sibling or archive non-blocking with alias/lineage. | MERGE / ARCHIVE NON-BLOCKING |
| 2 | trim=null; years=2007-2011; body=Pickup; fuel=diesel; engine=2.5L turbo; displacement=2.5; hp=143; trans=5-speed manual; drive=4WD; support=direct; source_indexes=[1, 2, 3] | Duplicate of IL-confirmed Mazda BT-50; preserve lineage/alias and archive/delete duplicate clean profile. | Duplicate of IL-confirmed Mazda BT-50; preserve lineage/alias and archive/delete duplicate clean profile. | Remove from clean as separate profile; merge into IL-confirmed sibling or archive non-blocking with alias/lineage. | MERGE / ARCHIVE NON-BLOCKING |
| 3 | trim=null; years=2007-2011; body=Pickup; fuel=diesel; engine=2.5L turbo; displacement=2.5; hp=143; trans=5-speed automatic; drive=RWD; support=direct; source_indexes=[1, 2, 3] | Duplicate of IL-confirmed Mazda BT-50; preserve lineage/alias and archive/delete duplicate clean profile. | Duplicate of IL-confirmed Mazda BT-50; preserve lineage/alias and archive/delete duplicate clean profile. | Remove from clean as separate profile; merge into IL-confirmed sibling or archive non-blocking with alias/lineage. | MERGE / ARCHIVE NON-BLOCKING |
| 4 | trim=null; years=2007-2011; body=Pickup; fuel=diesel; engine=2.5L turbo; displacement=2.5; hp=143; trans=5-speed automatic; drive=4WD; support=direct; source_indexes=[1, 2, 3] | Duplicate of IL-confirmed Mazda BT-50; preserve lineage/alias and archive/delete duplicate clean profile. | Duplicate of IL-confirmed Mazda BT-50; preserve lineage/alias and archive/delete duplicate clean profile. | Remove from clean as separate profile; merge into IL-confirmed sibling or archive non-blocking with alias/lineage. | MERGE / ARCHIVE NON-BLOCKING |

---

## MODEL: global-reference-only|Mazda|CX-3

CATALOG INDEX: 535

CURRENT VALUE: clean profile with 2 technical variants; profile years=2017-2024; confidence=medium.

PROBLEM: Duplicate of IL-confirmed Mazda CX-3; do not keep global-reference-only clean profile.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] Cartube / editorial: מאזדה CX-3 החדש 2020 בישראל - מנוע 1.5 ליטר ומחיר זול מבעבר — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%90%D7%96%D7%93%D7%94-cx-3-%D7%94%D7%97%D7%93%D7%A9-2020-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%A0%D7%95%D7%A2-1-5-%D7%9C%D7%99%D7%98%D7%A8-%D7%95%D7%9E%D7%97%D7%99%D7%A8-%D7%96%D7%95%D7%9C-%D7%9E%D7%91%D7%A2%D7%91%D7%A8
- repo source [1] iCar / catalog: מאזדה CX-3 - מחירון, מפרטים, אמינות וחוות דעת — https://www.icar.co.il/Mazda/Mazda_CX-3/Mazda_CX-3_d1/

TARGET VALUE: MERGE / ARCHIVE NON-BLOCKING. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: MERGE / ARCHIVE NON-BLOCKING

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2017-2024; body=SUV; fuel=petrol; engine=2.0L; displacement=2.0; hp=156; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[1] | Duplicate of IL-confirmed Mazda CX-3; do not keep global-reference-only clean profile. | Duplicate of IL-confirmed Mazda CX-3; do not keep global-reference-only clean profile. | Remove from clean as separate profile; merge into IL-confirmed sibling or archive non-blocking with alias/lineage. | MERGE / ARCHIVE NON-BLOCKING |
| 2 | trim=null; years=2020-2024; body=SUV; fuel=petrol; engine=1.5L; displacement=1.5; hp=116; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[0, 1] | Duplicate of IL-confirmed Mazda CX-3; do not keep global-reference-only clean profile. | Duplicate of IL-confirmed Mazda CX-3; do not keep global-reference-only clean profile. | Remove from clean as separate profile; merge into IL-confirmed sibling or archive non-blocking with alias/lineage. | MERGE / ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mazda|CX-3

CATALOG INDEX: 536

CURRENT VALUE: clean profile with 2 technical variants; profile years=2017-2024; confidence=medium.

PROBLEM: Use IL-confirmed historical/current-to-2024 profile as primary; no evidence here to extend to 2026.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] iCar Israel / catalog: מאזדה CX-3 - מפרט טכני — https://www.icar.co.il/Mazda/Mazda_CX-3/
- repo source [1] Cartube IL / editorial: מאזדה CX-3 החדש 2021 בישראל - מחירון ומפרט טכני — https://www.cartube.co.il/חדשות-רכב/מאזדה-cx-3-החדש-2021-בישראל-מחירון-ומפרט-טכני

TARGET VALUE: KEEP PRIMARY. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: KEEP PRIMARY

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2017-2024; body=SUV; fuel=petrol; engine=2.0L naturally-aspirated; displacement=2.0; hp=156; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[0] | Use IL-confirmed historical/current-to-2024 profile as primary; no evidence here to extend to 2026. | Use IL-confirmed historical/current-to-2024 profile as primary; no evidence here to extend to 2026. | trim=null; years=2017-2024; body=SUV; fuel=petrol; engine=2.0L naturally-aspirated; displacement=2.0; hp=156; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[0] | KEEP PRIMARY |
| 2 | trim=null; years=2021-2024; body=SUV; fuel=petrol; engine=1.5L naturally-aspirated; displacement=1.5; hp=116; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[0, 1] | Use IL-confirmed historical/current-to-2024 profile as primary; no evidence here to extend to 2026. | Use IL-confirmed historical/current-to-2024 profile as primary; no evidence here to extend to 2026. | trim=null; years=2021-2024; body=SUV; fuel=petrol; engine=1.5L naturally-aspirated; displacement=1.5; hp=116; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[0, 1] | KEEP PRIMARY |

---

## MODEL: IL-confirmed|Mazda|CX-5

CATALOG INDEX: 537

CURRENT VALUE: clean profile with 5 technical variants; profile years=2012-2024; confidence=medium.

PROBLEM: Mazda Israel official 2026 car-list and CX-5 page support current CX-5; do not leave current 2.5 rows closed at 2024 if fields can be grounded. Keep historical rows as-is.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] iCar / specs: מאזדה CX-5 מפרט טכני - iCar — https://www.icar.co.il/%D7%9E%D7%90%D7%96%D7%93%D7%94/%D7%9E%D7%90%D7%96%D7%93%D7%94_CX-5/
- repo source [1] Cartube / editorial: מאזדה CX-5 החדש 2022 בישראל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%90%D7%96%D7%93%D7%94-cx-5-%D7%94%D7%97%D7%93%D7%A9-2022-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-170900-%D7%A9%D7%A7%D7%9C
- repo source [2] Cartube / editorial: מאזדה CX-5 בישראל – מחירים ומפרט טכני (2012) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%90%D7%96%D7%93%D7%94-CX-5-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%E2%80%93-%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D-%D7%95%D7%9E%D7%A4%D7%A8%D7%98-%D7%98%D7%9B%D7%A0%D7%99
- repo source [3] Cartube / editorial: מאזדה CX-5 החדש 2017 בישראל - מחיר החל מ- 167,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%90%D7%96%D7%93%D7%94-cx-5-%D7%94%D7%97%D7%93%D7%A9-2017-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-167-000-%D7%A9%D7%A7%D7%9C

TARGET VALUE: FIX CURRENT YEARS / KEEP HISTORICAL. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: FIX CURRENT YEARS / KEEP HISTORICAL

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2012-2015; body=SUV; fuel=petrol; engine=2.0L; displacement=2.0; hp=155; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[0, 2] | Mazda Israel official 2026 car-list and CX-5 page support current CX-5; do not leave current 2.5 rows closed at 2024 if fields can be grounded. Keep historical rows as-is. | Mazda Israel official 2026 car-list and CX-5 page support current CX-5; do not leave current 2.5 rows closed at 2024 if fields can be grounded. Keep historical rows as-is. | trim=null; years=2012-2015; body=SUV; fuel=petrol; engine=2.0L; displacement=2.0; hp=155; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[0, 2] | FIX CURRENT YEARS / KEEP HISTORICAL |
| 2 | trim=null; years=2015-2024; body=SUV; fuel=petrol; engine=2.0L; displacement=2.0; hp=165; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[0, 1, 3] | Mazda Israel official 2026 car-list and CX-5 page support current CX-5; do not leave current 2.5 rows closed at 2024 if fields can be grounded. Keep historical rows as-is. | Mazda Israel official 2026 car-list and CX-5 page support current CX-5; do not leave current 2.5 rows closed at 2024 if fields can be grounded. Keep historical rows as-is. | trim=null; years=2015-2024; body=SUV; fuel=petrol; engine=2.0L; displacement=2.0; hp=165; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[0, 1, 3] | FIX CURRENT YEARS / KEEP HISTORICAL |
| 3 | trim=null; years=2013-2017; body=SUV; fuel=petrol; engine=2.5L; displacement=2.5; hp=192; trans=6-speed automatic; drive=AWD; support=direct; source_indexes=[0] | Mazda Israel official 2026 car-list and CX-5 page support current CX-5; do not leave current 2.5 rows closed at 2024 if fields can be grounded. Keep historical rows as-is. | Mazda Israel official 2026 car-list and CX-5 page support current CX-5; do not leave current 2.5 rows closed at 2024 if fields can be grounded. Keep historical rows as-is. | trim=null; years=2013-2017; body=SUV; fuel=petrol; engine=2.5L; displacement=2.5; hp=192; trans=6-speed automatic; drive=AWD; support=direct; source_indexes=[0] | FIX CURRENT YEARS / KEEP HISTORICAL |
| 4 | trim=null; years=2017-2024; body=SUV; fuel=petrol; engine=2.5L; displacement=2.5; hp=195; trans=6-speed automatic; drive=AWD; support=direct; source_indexes=[0, 1, 3] | Mazda Israel official 2026 car-list and CX-5 page support current CX-5; do not leave current 2.5 rows closed at 2024 if fields can be grounded. Keep historical rows as-is. | Mazda Israel official 2026 car-list and CX-5 page support current CX-5; do not leave current 2.5 rows closed at 2024 if fields can be grounded. Keep historical rows as-is. | Keep historical split, but add/fix current CX-5 2.5L rows through 2026 if field_sources can be grounded from Mazda Israel 2026 price list/spec PDF. Do not invent unsupported trims. | FIX CURRENT YEARS IF GROUNDED |
| 5 | trim=null; years=2021-2024; body=SUV; fuel=petrol; engine=2.5L; displacement=2.5; hp=195; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[0, 1] | Mazda Israel official 2026 car-list and CX-5 page support current CX-5; do not leave current 2.5 rows closed at 2024 if fields can be grounded. Keep historical rows as-is. | Mazda Israel official 2026 car-list and CX-5 page support current CX-5; do not leave current 2.5 rows closed at 2024 if fields can be grounded. Keep historical rows as-is. | Keep historical split, but add/fix current CX-5 2.5L rows through 2026 if field_sources can be grounded from Mazda Israel 2026 price list/spec PDF. Do not invent unsupported trims. | FIX CURRENT YEARS IF GROUNDED |

---

## MODEL: global-reference-only|Mazda|CX-50

CATALOG INDEX: 538

CURRENT VALUE: clean profile with 3 technical variants; profile years=None-None; confidence=medium.

PROBLEM: Only global/preview/editorial sources; no confirmed Israeli-market clean support. Archive/review non-blocking.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [1] Cartube.co.il / editorial: מאזדה CX-50 נחשף - רכב פנאי לשטח לשוק האמריקאי — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%90%D7%96%D7%93%D7%94-cx-50-%D7%A0%D7%97%D7%A9%D7%A3-%D7%A8%D7%9B%D7%91-%D7%A4%D7%A0%D7%90%D7%99-%D7%9C%D7%A9%D7%98%D7%97-%D7%90%D7%9E%D7%99%D7%AA%D7%99
- repo source [2] Cartube.co.il / editorial: מאזדה CX-50 מקבל מערכת הנעה היברידית של טויוטה — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%90%D7%96%D7%93%D7%94-cx-50-%D7%9E%D7%A7%D7%91%D7%9C-%D7%9E%D7%A2%D7%A8%D7%9B%D7%AA-%D7%94%D7%A0%D7%A2%D7%94-%D7%94%D7%99%D7%91%D7%A8%D7%99%D7%93%D7%99%D7%AA-%D7%A9%D7%9C-%D7%98%D7%95%D7%99%D7%95%D7%98%D7%94

TARGET VALUE: ARCHIVE NON-BLOCKING. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: ARCHIVE NON-BLOCKING

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=null-null; body=SUV; fuel=petrol; engine=2.5L 4-cylinder; displacement=2.5; hp=187; trans=6-speed automatic; drive=AWD; support=unknown; source_indexes=[1] | Only global/preview/editorial sources; no confirmed Israeli-market clean support. Archive/review non-blocking. | Only global/preview/editorial sources; no confirmed Israeli-market clean support. Archive/review non-blocking. | Move to non-blocking archive/review; no Israeli clean support. | ARCHIVE NON-BLOCKING |
| 2 | trim=null; years=null-null; body=SUV; fuel=petrol; engine=2.5L turbo 4-cylinder; displacement=2.5; hp=250; trans=6-speed automatic; drive=AWD; support=unknown; source_indexes=[1] | Only global/preview/editorial sources; no confirmed Israeli-market clean support. Archive/review non-blocking. | Only global/preview/editorial sources; no confirmed Israeli-market clean support. Archive/review non-blocking. | Move to non-blocking archive/review; no Israeli clean support. | ARCHIVE NON-BLOCKING |
| 3 | trim=null; years=null-null; body=SUV; fuel=hybrid; engine=2.5L 4-cylinder; displacement=2.5; hp=219; trans=cvt; drive=AWD; support=unknown; source_indexes=[2] | Only global/preview/editorial sources; no confirmed Israeli-market clean support. Archive/review non-blocking. | Only global/preview/editorial sources; no confirmed Israeli-market clean support. Archive/review non-blocking. | Move to non-blocking archive/review; no Israeli clean support. | ARCHIVE NON-BLOCKING |

---

## MODEL: global-reference-only|Mazda|CX-60

CATALOG INDEX: 539

CURRENT VALUE: clean profile with 2 technical variants; profile years=2023-None; confidence=medium.

PROBLEM: PHEV 327 hp belongs under IL-confirmed CX-60 if source-supported. 3.3 mild-hybrid 284 hp needs Israeli official local evidence before clean; otherwise move that row to review.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [1] Mazda Israel / official_importer: מאזדה CX-60 - מפרט טכני — https://www.mazda.co.il/uploads/cx-60-specs.pdf
- repo source [2] iCar / catalog: מאזדה CX-60 - מחירון רכב, מבחני דרכים ומפרטים טכניים — https://www.icar.co.il/מאזדה/מאזדה_CX-60/מאזדה_CX-60_חדש/

TARGET VALUE: MERGE / PARTIAL REVIEW. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: MERGE / PARTIAL REVIEW

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2023-null; body=SUV; fuel=plug_in_hybrid; engine=2.5L; displacement=2.5; hp=327; trans=8-speed automatic; drive=AWD; support=direct; source_indexes=[1, 2] | PHEV 327 hp belongs under IL-confirmed CX-60 if source-supported. 3.3 mild-hybrid 284 hp needs Israeli official local evidence before clean; otherwise move that row to review. | PHEV 327 hp belongs under IL-confirmed CX-60 if source-supported. 3.3 mild-hybrid 284 hp needs Israeli official local evidence before clean; otherwise move that row to review. | Merge PHEV 327 hp duplicate into IL-confirmed Mazda CX-60; remove global-reference-only clean duplicate. | MERGE / PARTIAL REVIEW |
| 2 | trim=null; years=2023-null; body=SUV; fuel=mild_hybrid; engine=3.3L turbo; displacement=3.3; hp=284; trans=8-speed automatic; drive=AWD; support=direct; source_indexes=[1, 2] | PHEV 327 hp belongs under IL-confirmed CX-60 if source-supported. 3.3 mild-hybrid 284 hp needs Israeli official local evidence before clean; otherwise move that row to review. | PHEV 327 hp belongs under IL-confirmed CX-60 if source-supported. 3.3 mild-hybrid 284 hp needs Israeli official local evidence before clean; otherwise move that row to review. | Move 3.3 mild-hybrid 284 hp row to review unless repo-local official Israeli source grounds it; do not keep under global-reference-only clean. | MERGE / PARTIAL REVIEW |

---

## MODEL: IL-confirmed|Mazda|CX-60

CATALOG INDEX: 540

CURRENT VALUE: clean profile with 1 technical variants; profile years=2024-None; confidence=medium.

PROBLEM: IL-confirmed CX-60 PHEV 327 hp is primary; fold the global duplicate PHEV row into this profile.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] Auto.co.il / editorial: מאזדה CX-60 - מחירון, מפרט טכני וקטלוג רכב | Auto.co.il — https://www.auto.co.il/model/mazda-cx-60_g1483
- repo source [1] Cartube.co.il / editorial: מאזדה CX-60 החדש 2024 בישראל - מחיר החל מ- 295,900 שקלים | Cartube — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%90%D7%96%D7%93%D7%94-cx-60-%D7%94%D7%97%D7%93%D7%A9-2024-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-295900-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D

TARGET VALUE: KEEP PRIMARY / MERGE PHEV DUPLICATE. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: KEEP PRIMARY / MERGE PHEV DUPLICATE

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2024-null; body=SUV; fuel=plug_in_hybrid; engine=2.5L; displacement=2.5; hp=327; trans=8-speed automatic; drive=AWD; support=direct; source_indexes=[0, 1] | IL-confirmed CX-60 PHEV 327 hp is primary; fold the global duplicate PHEV row into this profile. | IL-confirmed CX-60 PHEV 327 hp is primary; fold the global duplicate PHEV row into this profile. | trim=null; years=2024-null; body=SUV; fuel=plug_in_hybrid; engine=2.5L; displacement=2.5; hp=327; trans=8-speed automatic; drive=AWD; support=direct; source_indexes=[0, 1] | KEEP PRIMARY / MERGE PHEV DUPLICATE |

---

## MODEL: IL-confirmed|Mazda|CX-7

CATALOG INDEX: 541

CURRENT VALUE: clean profile with 2 technical variants; profile years=2007-2012; confidence=medium.

PROBLEM: Historical Israeli sources support CX-7 rows; preserve as historical clean.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] iCar / catalog/spec: מאזדה CX-7 - מחירון רכב, מפרט טכני - iCar — https://www.icar.co.il/%D7%9E%D7%90%D7%96%D7%93%D7%94/%D7%9E%D7%90%D7%96%D7%93%D7%94_CX-7/%D7%9E%D7%90%D7%96%D7%93%D7%94_CX-7_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%93%D7%95%D7%A8_1/
- repo source [1] Auto.co.il / editorial/spec: מאזדה CX-7 יד שניה - אוטו — https://www.auto.co.il/model/mazda-cx-7_g164

TARGET VALUE: KEEP. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: KEEP

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2007-2012; body=SUV; fuel=petrol; engine=2.3L turbo; displacement=2.3; hp=238; trans=6-speed automatic; drive=AWD; support=direct; source_indexes=[0, 1] | Historical Israeli sources support CX-7 rows; preserve as historical clean. | Historical Israeli sources support CX-7 rows; preserve as historical clean. | trim=null; years=2007-2012; body=SUV; fuel=petrol; engine=2.3L turbo; displacement=2.3; hp=238; trans=6-speed automatic; drive=AWD; support=direct; source_indexes=[0, 1] | KEEP |
| 2 | trim=null; years=2010-2012; body=SUV; fuel=petrol; engine=2.5L; displacement=2.5; hp=163; trans=5-speed automatic; drive=FWD; support=direct; source_indexes=[0, 1] | Historical Israeli sources support CX-7 rows; preserve as historical clean. | Historical Israeli sources support CX-7 rows; preserve as historical clean. | trim=null; years=2010-2012; body=SUV; fuel=petrol; engine=2.5L; displacement=2.5; hp=163; trans=5-speed automatic; drive=FWD; support=direct; source_indexes=[0, 1] | KEEP |

---

## MODEL: IL-likely|Mazda|CX-80

CATALOG INDEX: 542

CURRENT VALUE: clean profile with 2 technical variants; profile years=2024-None; confidence=medium.

PROBLEM: Evidence is indirect/preview; no confirmed Israeli sales/official current source in this run. Do not keep as verified clean.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] Cartube.co.il / editorial: מאזדה CX-80 החדש 2024 נחשף - 7 מושבים - קארטיוב — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%90%D7%96%D7%93%D7%94-cx-80-%D7%94%D7%97%D7%93%D7%A9-2024-%D7%A0%D7%97%D7%A9%D7%A3
- repo source [1] iCar.co.il / catalog: מאזדה CX-80 מפרט טכני וחדשות - iCar — https://www.icar.co.il/%D7%9E%D7%90%D7%96%D7%93%D7%94/%D7%9E%D7%90%D7%96%D7%93%D7%94_CX-80/

TARGET VALUE: MOVE TO REVIEW. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: MOVE TO REVIEW

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2024-null; body=SUV; fuel=plug_in_hybrid; engine=2.5L; displacement=2.5; hp=327; trans=8-speed automatic; drive=AWD; support=indirect; source_indexes=[0, 1] | Evidence is indirect/preview; no confirmed Israeli sales/official current source in this run. Do not keep as verified clean. | Evidence is indirect/preview; no confirmed Israeli sales/official current source in this run. Do not keep as verified clean. | Move to non-blocking review/archive unless repo-local official Israeli sales source exists; indirect preview is not verified clean. | MOVE TO REVIEW |
| 2 | trim=null; years=2024-null; body=SUV; fuel=mild_hybrid; engine=3.3L turbo; displacement=3.3; hp=254; trans=8-speed automatic; drive=AWD; support=indirect; source_indexes=[0, 1] | Evidence is indirect/preview; no confirmed Israeli sales/official current source in this run. Do not keep as verified clean. | Evidence is indirect/preview; no confirmed Israeli sales/official current source in this run. Do not keep as verified clean. | Move to non-blocking review/archive unless repo-local official Israeli sales source exists; indirect preview is not verified clean. | MOVE TO REVIEW |

---

## MODEL: IL-confirmed|Mazda|CX-9

CATALOG INDEX: 543

CURRENT VALUE: clean profile with 2 technical variants; profile years=2008-2023; confidence=medium.

PROBLEM: CX-9 historical Israeli rows supported; CX-90 now replaces it. Do not extend beyond 2023 without official local source.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] iCar Israel / catalog: מאזדה CX-9 (2008-2015) - מפרט טכני — https://www.icar.co.il/מאזדה/מאזדה_CX-9_דור_1/מפרט_טכני/
- repo source [1] Cartube Israel / editorial: מאזדה CX-9 החדש בישראל 2021 - מחיר מ-315,000 שקל — https://www.cartube.co.il/חדשות-רכב/מאזדה-cx-9-החדש-בישראל-2021-מחיר-מ-315000-שקל
- repo source [2] Mazda Israel Official Importer / official_importer: מפרט טכני CX-9 — https://www.mazda.co.il/models/cx-9/specs

TARGET VALUE: KEEP HISTORICAL / CLOSE. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: KEEP HISTORICAL / CLOSE

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2008-2015; body=SUV; fuel=petrol; engine=3.7L v6; displacement=3.7; hp=273; trans=6-speed automatic; drive=AWD; support=direct; source_indexes=[0] | CX-9 historical Israeli rows supported; CX-90 now replaces it. Do not extend beyond 2023 without official local source. | CX-9 historical Israeli rows supported; CX-90 now replaces it. Do not extend beyond 2023 without official local source. | trim=null; years=2008-2015; body=SUV; fuel=petrol; engine=3.7L v6; displacement=3.7; hp=273; trans=6-speed automatic; drive=AWD; support=direct; source_indexes=[0] | KEEP HISTORICAL / CLOSE |
| 2 | trim=null; years=2021-2023; body=SUV; fuel=petrol; engine=2.5L turbo; displacement=2.5; hp=231; trans=6-speed automatic; drive=AWD; support=direct; source_indexes=[1, 2] | CX-9 historical Israeli rows supported; CX-90 now replaces it. Do not extend beyond 2023 without official local source. | CX-9 historical Israeli rows supported; CX-90 now replaces it. Do not extend beyond 2023 without official local source. | trim=null; years=2021-2023; body=SUV; fuel=petrol; engine=2.5L turbo; displacement=2.5; hp=231; trans=6-speed automatic; drive=AWD; support=direct; source_indexes=[1, 2] | KEEP HISTORICAL / CLOSE |

---

## MODEL: global-reference-only|Mazda|CX-90

CATALOG INDEX: 544

CURRENT VALUE: clean profile with 1 technical variants; profile years=2023-None; confidence=medium.

PROBLEM: Current official Mazda Israel CX-90 page supports 3.3L 345 hp, not the existing global 2.5 PHEV 327 row as clean. Add correct IL row if policy allows; otherwise move PHEV row to review/archive.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] iCar / editorial: מאזדה CX-90 החדש בישראל - מחירון ומפרט טכני — https://www.icar.co.il/Mazda/Mazda_CX-90/
- repo source [1] Cartube / editorial: מאזדה CX-90 פלאג-אין בישראל: מפרט מלא — https://www.cartube.co.il/חדשות-רכב/מאזדה-cx-90-פלאג-אין-327-כ-ס-בישראל

TARGET VALUE: FIX TO IL-CONFIRMED 3.3 345 OR MOVE PHEV TO REVIEW. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: FIX TO IL-CONFIRMED 3.3 345 OR MOVE PHEV TO REVIEW

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2023-null; body=SUV; fuel=plug_in_hybrid; engine=2.5L inline-4; displacement=2.5; hp=327; trans=8-speed automatic; drive=AWD; support=direct; source_indexes=[0, 1] | Current official Mazda Israel CX-90 page supports 3.3L 345 hp, not the existing global 2.5 PHEV 327 row as clean. Add correct IL row if policy allows; otherwise move PHEV row to review/archive. | Current official Mazda Israel CX-90 page supports 3.3L 345 hp, not the existing global 2.5 PHEV 327 row as clean. Add correct IL row if policy allows; otherwise move PHEV row to review/archive. | Do not keep this 2.5 PHEV 327 hp global-reference-only row as clean. Replace/add IL-confirmed CX-90 3.3L turbo/e-Skyactiv-G 345 hp AWD 8-speed automatic only if source policy allows; otherwise move PHEV row to non-blocking review/archive with reason. | MOVE TO REVIEW / ADD CORRECT IL ROW IF ALLOWED |

---

## MODEL: IL-confirmed|Mazda|Mazda2

CATALOG INDEX: 545

CURRENT VALUE: clean profile with 6 technical variants; profile years=2007-2024; confidence=medium.

PROBLEM: Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support.

WEB-VALIDATED FACT: See RUN 2 source package above plus repo-local sources below. Israeli-market sources take priority over global sources. Global-reference-only profiles cannot remain separate clean profiles when an IL-confirmed sibling exists.

SOURCE:
- repo source [0] iCar / editorial: מאזדה 2 (2007-2015) - מחירון רכב, מפרט טכני — https://www.icar.co.il/מאזדה/מאזדה_2_דגם_2007/
- repo source [1] iCar / editorial: מאזדה 2 סדאן (2011-2015) - מפרט טכני — https://www.icar.co.il/מאזדה/מאזדה_2_סדאן_דגם_2011/
- repo source [2] iCar / editorial: מאזדה 2 (2015-2024) - מחירון רכב, מפרט טכני — https://www.icar.co.il/מאזדה/מאזדה_2_דגם_2015/
- repo source [3] iCar / editorial: מאזדה 2 סדאן / דמיו (2015-2024) - מפרט טכני — https://www.icar.co.il/מאזדה/מאזדה_2_סדאן_דמיו/

TARGET VALUE: FIX CURRENT FUEL/YEAR IF NEEDED. Apply variant-level targets below. Preserve valid source_indexes/field_sources for KEEP rows. Preserve alias/lineage when merging, splitting, reviewing, or archiving.

ACTION: FIX CURRENT FUEL/YEAR IF NEEDED

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=null; years=2007-2015; body=Hatchback; fuel=petrol; engine=1.5L; displacement=1.5; hp=103; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[0] | Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support. | Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support. | trim=null; years=2007-2015; body=Hatchback; fuel=petrol; engine=1.5L; displacement=1.5; hp=103; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[0] | FIX CURRENT FUEL/YEAR IF NEEDED |
| 2 | trim=null; years=2011-2015; body=Sedan; fuel=petrol; engine=1.5L; displacement=1.5; hp=103; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1] | Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support. | Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support. | trim=null; years=2011-2015; body=Sedan; fuel=petrol; engine=1.5L; displacement=1.5; hp=103; trans=4-speed automatic; drive=FWD; support=direct; source_indexes=[1] | FIX CURRENT FUEL/YEAR IF NEEDED |
| 3 | trim=null; years=2015-2020; body=Hatchback; fuel=petrol; engine=1.5L; displacement=1.5; hp=111; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[2] | Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support. | Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support. | trim=null; years=2015-2020; body=Hatchback; fuel=petrol; engine=1.5L; displacement=1.5; hp=111; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[2] | FIX CURRENT FUEL/YEAR IF NEEDED |
| 4 | trim=null; years=2015-2020; body=Sedan; fuel=petrol; engine=1.5L; displacement=1.5; hp=111; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[3] | Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support. | Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support. | trim=null; years=2015-2020; body=Sedan; fuel=petrol; engine=1.5L; displacement=1.5; hp=111; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[3] | FIX CURRENT FUEL/YEAR IF NEEDED |
| 5 | trim=null; years=2020-2024; body=Hatchback; fuel=mild_hybrid; engine=1.5L; displacement=1.5; hp=116; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[2] | Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support. | Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support. | Verify fuel_type from local source. If current Israeli sources describe 1.5 petrol atmospheric rather than mild-hybrid, change fuel_type to petrol for the 116 hp current rows and keep source/lineage; do not invent mild_hybrid. | FIX IF NEEDED |
| 6 | trim=null; years=2020-2024; body=Sedan; fuel=mild_hybrid; engine=1.5L; displacement=1.5; hp=116; trans=6-speed automatic; drive=FWD; support=direct; source_indexes=[3] | Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support. | Current Israeli sources support 1.5L 116 hp automatic FWD Mazda2. If source says petrol atmospheric, do not label mild_hybrid unless explicitly sourced. Extend current hatchback year only with source support. | Verify fuel_type from local source. If current Israeli sources describe 1.5 petrol atmospheric rather than mild-hybrid, change fuel_type to petrol for the 116 hp current rows and keep source/lineage; do not invent mild_hybrid. | FIX IF NEEDED |


## RUN 2 completion requirements

Before reporting success, verify:

```text
- All 20 profiles above were handled.
- All 57 technical variants above have explicit KEEP/FIX/MERGE/MOVE TO REVIEW/ARCHIVE outcome.
- No global-reference-only duplicate profile remains as separate clean when an IL-confirmed sibling exists.
- Maxus T90 conflict was fixed or moved to non-blocking review; it must not remain a wrong 177 hp verified-clean Israeli T90 EV row.
- Mazda CX-90 2.5 PHEV global row was not kept as the current official clean Israeli CX-90 row; official Israeli 3.3L 345 hp evidence was handled according to repo policy.
- Mazda CX-80 was not kept as verified clean without official Israeli local evidence.
- Temporary files `codex_tasks/BATCH26_RUN2_*.md` were deleted before final commit unless the user explicitly asked to keep them.
```

Report at the end:

```text
1. Files changed
2. Exact before/after metrics for RUN 2 scope
3. Confirmation that all 20 profiles and 57 variants were handled
4. Test results
5. Confirmation that temporary RUN2 instruction files were deleted before final commit
6. Remaining conflicts/issues, if any
```


# ==============================
# RUN3
# source: BATCH26_RUN3_VARIANT_LEVEL_CODEX_TASK.md
# ==============================

# BATCH26 RUN 3 — variant-level web-validated Codex task

TEMPORARY FILE RULE: This is a temporary instruction file. After this run is fully applied and verified, delete `codex_tasks/BATCH26_RUN3_*.md` from the repo before final commit unless the user explicitly requests keeping it.

DO NOT BROWSE THE INTERNET.
All web-validation facts and target corrections are embedded here and in repo-local sources. Use this file as the single source of truth for this run.
Do not apply corrections that are not instructed here. If repo-local evidence conflicts with this task file, report it instead of guessing.
If a variant cannot be grounded with the embedded facts or repo-local sources, move it to non-blocking archive/review with clear reason and lineage rather than fabricating data.

## Scope

```text
RUN 3: 20 clean model profiles
technical_variants covered: 71/71
from: global-reference-only|Mazda|Mazda2
to: IL-confirmed|Mercedes-Benz|B-Class
```

## Web-validation source package for this run


## RUN 3 strengthened re-validation notes (2026-06-21)

These instructions override any older/generic KEEP target in the tables below when there is a conflict.

### Mazda3 current correction — mandatory
- WEB-VALIDATED FACT: Mazda Israel official 2026 price list lists current MAZDA3 Sedan as 2.5L Comfort, 2.5L Spirit, 2.5L Spirit Turbo, and 2.5L Premium Turbo; MAZDA3 Hatchback as 2.5L Spirit and 2.5L Premium Turbo. Current Israeli source material therefore no longer supports keeping `2.0L mild_hybrid 165 hp` as open-ended 2026 current.
- SOURCE URL: https://www.mazda.co.il/car-list
- SOURCE URL: https://www.mazda.co.il/model/3/mazda3-sedan
- SOURCE URL: https://www.mazda.co.il/model/2/mazda3-hatchback
- SOURCE URL: https://www.auto.co.il/cars/mazda/3/
- TARGET:
  - Set existing Mazda3 2.0L mild_hybrid 165 hp Sedan/Hatchback rows to a closed historical period, preferably `year_end=2025` if repo-local/source lineage supports that transition, otherwise `MOVE TO REVIEW` for year boundary only.
  - Add/ensure current 2026 Mazda3 technical rows:
    1. Sedan, petrol, 2.5L naturally aspirated, 191 hp, 6-speed automatic, FWD, trims Comfort/Spirit.
    2. Hatchback, petrol, 2.5L naturally aspirated, 191 hp, 6-speed automatic, FWD, trim Spirit.
    3. Sedan, petrol, 2.5L turbo, 227 hp on 95 octane Israeli-market reporting, 6-speed automatic, AWD, trims Spirit Turbo/Premium Turbo.
    4. Hatchback, petrol, 2.5L turbo, 227 hp on 95 octane Israeli-market reporting, 6-speed automatic, AWD, trim Premium Turbo.
  - Preserve older 2003-2020 Mazda3 rows if their repo-local Israeli sources remain valid.
- ACTION: FIX / ADD.

### Mazda MX-30 caution — mandatory
- WEB-VALIDATED FACT: Israeli sources describe MX-30 as arriving in Israel through parallel import with about 145-146 hp electric FWD and a 35.5 kWh battery. This is not official regular-importer current clean evidence.
- SOURCE URL: https://www.auto.co.il/articles/car-news/local-news/134633/
- SOURCE URL: https://wheel.co.il/מאזדה-mx-30-החשמלית-בישראל-יבוא-מקביל/
- TARGET: Keep only if support policy allows parallel-import clean rows; otherwise move to non-blocking review/archive with lineage. EV schema must be displacement null, fuel_type electric, transmission single_speed/direct_drive, drivetrain FWD.
- ACTION: KEEP WITH PARALLEL-IMPORT NOTE / MOVE TO REVIEW.

### Mazda MX-5 current correction — mandatory
- WEB-VALIDATED FACT: Israeli/price-list sources support MX-5 2026 variants and post-2019 2.0L engine around 183-184 hp. Current 2026 availability should not be incorrectly closed at 2024 if local price-list evidence is accepted.
- SOURCE URL: https://www.carzone.co.il/Mazda/MX-5/2026/
- SOURCE URL: https://www.cartube.co.il/מחירון-רכב-חדש/מאזדה/מאזדה-mx-5
- TARGET: If current Mazda MX-5 policy accepts Carzone/price-list support, extend/add current MX-5 2026 rows; otherwise keep 2019-2024 official-importer row and move 2025-2026 continuation to review. Do not fabricate trims.
- ACTION: FIX YEAR_END / ADD CURRENT ROWS OR MOVE TO REVIEW.

### McLaren GT / GTS duplicate handling — mandatory
- WEB-VALIDATED FACT: Israeli/automotive sources support McLaren GT 4.0L V8 twin-turbo 620 hp, 7-speed dual-clutch, RWD. GTS 2024 is primarily a global successor/announcement unless repo-local Israeli evidence exists.
- SOURCE URL: https://www.cartube.co.il/חדשות-רכב/מהירה-ונוחה-מקלארן-gt-החדשה-נחשפת
- SOURCE URL: https://www.auto.co.il/articles/car-news/world-news/132164/
- TARGET: Merge `IL-confirmed|McLaren|GT` and `IL-likely|McLaren|GT`; keep GT 620 hp as Israeli-supported if source policy accepts niche import evidence. Move GTS 635 hp to non-blocking review unless local Israeli support exists.
- ACTION: MERGE / MOVE TO REVIEW.

### Mercedes-Benz current caution — mandatory
- WEB-VALIDATED FACT: Mercedes-Benz Israel official model pages support current A-Class and AMG GT pages, but current availability by exact body/trim must be grounded. Do not extend every historical A-Class/B-Class row to 2026 merely because a model page exists.
- SOURCE URL: https://www.mercedes-benz.co.il/models/a-class/
- SOURCE URL: https://www.mercedes-benz.co.il/models/amg-gt-coupe/
- SOURCE URL: https://www.mercedes-benz.co.il/models/
- TARGET:
  - AMG GT 63 4MATIC+ Coupe 2024-2026 585 hp is supported by official/current page + Israeli coverage; keep/fix sources.
  - A 250 e 218 hp may be extended only where official current page/repo-local source supports the exact body; otherwise keep 2020-2024.
  - B-Class rows should remain historical/2024 unless there is exact current official local support in repo-local files.
- ACTION: KEEP / FIX YEAR_END ONLY WHEN GROUNDED / MOVE TO REVIEW.



### Mazda
- Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.
- SOURCE URL: https://www.mazda.co.il/car-list
- SOURCE URL: https://www.mazda.co.il/models
- SOURCE URL: https://www.icar.co.il/מאזדה/
- SOURCE URL: https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד

### McLaren
- McLaren profiles rely on niche Israeli import/market evidence. Keep only if repo-local Israeli source supports the model; otherwise archive/review non-blocking rather than treating global specs as clean Israeli data.
- SOURCE URL: https://www.icar.co.il/

### Mercedes-Benz
- Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.
- SOURCE URL: https://www.mercedes-benz.co.il/models/
- SOURCE URL: https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- SOURCE URL: https://www.mercedes-benz.co.il/models/glc-suv/
- SOURCE URL: https://www.mercedes-benz.co.il/models/eqa-fl/
- SOURCE URL: https://www.icar.co.il/מרצדס/

## Model and variant decisions


---

## MODEL: global-reference-only|Mazda|Mazda2

CURRENT VALUE: clean profile with 2 technical variants.

PROBLEM: Global-reference-only profile has local sibling(s): ['IL-confirmed|Mazda|Mazda2']. Do not keep as separate clean Israeli profile.

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- repo source: [0] מאזדה 2 - מפרט טכני (official_importer) — https://www.mazda.co.il/models/mazda2
- repo source: [1] מאזדה 2 מחירון רכב, מפרט טכני (catalog) — https://www.icar.co.il/mazda/mazda2/
- repo source: [2] מאזדה 2 דמיו (סדאן) מחירון ומפרט (catalog) — https://www.icar.co.il/mazda/mazda2-demio/

TARGET VALUE: MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2015-2024; body=Hatchback; fuel=petrol; engine=1.5L; displacement=1.5; hp=116; trans=6-speed automatic; drive=FWD | Global-reference-only profile has local sibling(s): ['IL-confirmed/Mazda/Mazda2']. Do not keep as separate clean Israeli profile. | Sources [0, 1]; Mazda source package above. | Do not keep this row as independent clean under global-reference-only|Mazda|Mazda2; merge/archive/review with lineage per model action. | MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING |
| 2 | trim=None; years=2016-2021; body=Sedan; fuel=petrol; engine=1.5L; displacement=1.5; hp=116; trans=6-speed automatic; drive=FWD | Global-reference-only profile has local sibling(s): ['IL-confirmed/Mazda/Mazda2']. Do not keep as separate clean Israeli profile. | Sources [1, 2]; Mazda source package above. | Do not keep this row as independent clean under global-reference-only|Mazda|Mazda2; merge/archive/review with lineage per model action. | MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mazda|Mazda3

CURRENT VALUE: clean profile with 10 technical variants.

PROBLEM: IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- repo source: [1162] iCar Israel - Mazda 3 Gen 1 & Gen 2 (2003-2013) Specifications (editorial_catalog) — https://www.icar.co.il/mazda/mazda3/gen1-2
- repo source: [1163] Cartube Israel - Mazda 3 Gen 3 (2013-2019) Review and Specs (editorial_catalog) — https://www.cartube.co.il/mazda/mazda3/gen3
- repo source: [1164] Gear.co.il - Mazda 3 Gen 4 Skyactiv-G Launch (2019-2020) (editorial_catalog) — https://gear.co.il/mazda/mazda3/gen4
- repo source: [1165] Mazda Israel - Official Mazda3 e-Skyactiv MHEV Catalog (official_importer) — https://www.mazda.co.il/models/mazda3

TARGET VALUE: KEEP / FIX FIELDS IF INSTRUCTED. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP / FIX FIELDS IF INSTRUCTED

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2003-2013; body=Sedan; fuel=petrol; engine=1.6L naturally aspirated; displacement=1.6; hp=105; trans=4-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1162]; Mazda source package above. | trim=None; years=2003-2013; body=Sedan; fuel=petrol; engine=1.6L naturally aspirated; displacement=1.6; hp=105; trans=4-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 2 | trim=None; years=2003-2013; body=Hatchback; fuel=petrol; engine=1.6L naturally aspirated; displacement=1.6; hp=105; trans=4-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1162]; Mazda source package above. | trim=None; years=2003-2013; body=Hatchback; fuel=petrol; engine=1.6L naturally aspirated; displacement=1.6; hp=105; trans=4-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 3 | trim=None; years=2009-2013; body=Sedan; fuel=petrol; engine=2.0L naturally aspirated; displacement=2.0; hp=150; trans=5-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1162]; Mazda source package above. | trim=None; years=2009-2013; body=Sedan; fuel=petrol; engine=2.0L naturally aspirated; displacement=2.0; hp=150; trans=5-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 4 | trim=None; years=2009-2013; body=Hatchback; fuel=petrol; engine=2.0L naturally aspirated; displacement=2.0; hp=150; trans=5-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1162]; Mazda source package above. | trim=None; years=2009-2013; body=Hatchback; fuel=petrol; engine=2.0L naturally aspirated; displacement=2.0; hp=150; trans=5-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 5 | trim=None; years=2013-2019; body=Sedan; fuel=petrol; engine=1.5L naturally aspirated; displacement=1.5; hp=120; trans=6-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1163]; Mazda source package above. | trim=None; years=2013-2019; body=Sedan; fuel=petrol; engine=1.5L naturally aspirated; displacement=1.5; hp=120; trans=6-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 6 | trim=None; years=2013-2019; body=Hatchback; fuel=petrol; engine=1.5L naturally aspirated; displacement=1.5; hp=120; trans=6-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1163]; Mazda source package above. | trim=None; years=2013-2019; body=Hatchback; fuel=petrol; engine=1.5L naturally aspirated; displacement=1.5; hp=120; trans=6-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 7 | trim=None; years=2013-2020; body=Sedan; fuel=petrol; engine=2.0L naturally aspirated; displacement=2.0; hp=165; trans=6-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1163, 1164]; Mazda source package above. | trim=None; years=2013-2020; body=Sedan; fuel=petrol; engine=2.0L naturally aspirated; displacement=2.0; hp=165; trans=6-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 8 | trim=None; years=2013-2020; body=Hatchback; fuel=petrol; engine=2.0L naturally aspirated; displacement=2.0; hp=165; trans=6-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1163, 1164]; Mazda source package above. | trim=None; years=2013-2020; body=Hatchback; fuel=petrol; engine=2.0L naturally aspirated; displacement=2.0; hp=165; trans=6-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 9 | trim=None; years=2021-2026; body=Sedan; fuel=mild_hybrid; engine=2.0L naturally aspirated; displacement=2.0; hp=165; trans=6-speed automatic; drive=FWD | Current official Mazda Israel 2026 price/model pages no longer support this as open-ended current; 2026 Mazda3 is 2.5L petrol / 2.5L turbo. | Mazda Israel 2026 price list + Auto Israel support current 2.5L 191 hp and 2.5L turbo 227 hp Israeli lineup. | Close this 2.0L mild_hybrid row at 2025 if repo-local transition evidence supports it; otherwise move the year boundary to review. Add 2026 Sedan 2.5L NA 191 FWD and 2.5L turbo 227 AWD rows with correct trims. | FIX / ADD |
| 10 | trim=None; years=2021-2026; body=Hatchback; fuel=mild_hybrid; engine=2.0L naturally aspirated; displacement=2.0; hp=165; trans=6-speed automatic; drive=FWD | Current official Mazda Israel 2026 price/model pages no longer support this as open-ended current; 2026 Mazda3 Hatchback is 2.5L petrol / 2.5L turbo. | Mazda Israel 2026 price list + Auto Israel support current 2.5L 191 hp and 2.5L turbo 227 hp Israeli lineup; Mazda hatch page specifically mentions 227 hp 2.5L Turbo. | Close this 2.0L mild_hybrid row at 2025 if repo-local transition evidence supports it; otherwise move the year boundary to review. Add 2026 Hatchback 2.5L NA 191 FWD and 2.5L turbo 227 AWD rows with correct trims. | FIX / ADD |

---

## MODEL: IL-confirmed|Mazda|Mazda5

CURRENT VALUE: clean profile with 3 technical variants.

PROBLEM: IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- repo source: [0] מאזדה 5 (2005 - 2010) - מחירון, מפרטים, אמינות וחוות דעת - iCar (israeli_catalog) — https://www.icar.co.il/%D7%9E%D7%90%D7%96%D7%93%D7%94/%D7%9E%D7%90%D7%96%D7%93%D7%94_5/%D7%9E%D7%90%D7%96%D7%93%D7%94_5_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%93%D7%95%D7%A8_1/
- repo source: [1] מאזדה 5 (2010 - 2016) - מחירון, מפרטים, אמינות וחוות דעת - iCar (israeli_catalog) — https://www.icar.co.il/%D7%9E%D7%90%D7%96%D7%93%D7%94/%D7%9E%D7%90%D7%96%D7%93%D7%94_5/%D7%9E%D7%90%D7%96%D7%93%D7%94_5_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%93%D7%95%D7%A8_2/
- repo source: [2] מאזדה 5 - מחירון רכב, מפרט טכני, וחוות דעת - קארזון (israeli_catalog) — https://www.carzone.co.il/prices/mazda/mazda5/

TARGET VALUE: KEEP / FIX FIELDS IF INSTRUCTED. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP / FIX FIELDS IF INSTRUCTED

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2005-2008; body=MPV; fuel=petrol; engine=2.0L; displacement=2.0; hp=145; trans=4-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [0]; Mazda source package above. | trim=None; years=2005-2008; body=MPV; fuel=petrol; engine=2.0L; displacement=2.0; hp=145; trans=4-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 2 | trim=None; years=2008-2010; body=MPV; fuel=petrol; engine=2.0L; displacement=2.0; hp=145; trans=5-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [0]; Mazda source package above. | trim=None; years=2008-2010; body=MPV; fuel=petrol; engine=2.0L; displacement=2.0; hp=145; trans=5-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 3 | trim=None; years=2010-2016; body=MPV; fuel=petrol; engine=2.0L; displacement=2.0; hp=144; trans=5-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1, 2]; Mazda source package above. | trim=None; years=2010-2016; body=MPV; fuel=petrol; engine=2.0L; displacement=2.0; hp=144; trans=5-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |

---

## MODEL: IL-confirmed|Mazda|MPV

CURRENT VALUE: clean profile with 3 technical variants.

PROBLEM: Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only|Mazda|MPV'].

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- repo source: [0] מאזדה MPV (1999-2006) - מחירון רכב, מפרט טכני (specs_catalog) — https://www.icar.co.il/Mazda/Mazda_MPV/Mazda_MPV_1/
- repo source: [1] מאזדה MPV דור 1 (1994-1999) - מפרט טכני (specs_catalog) — https://www.auto.co.il/model/mazda-mpv_g132

TARGET VALUE: KEEP PRIMARY + ALIAS / MERGE DUPLICATES. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP PRIMARY + ALIAS / MERGE DUPLICATES

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=1993-1999; body=MPV; fuel=petrol; engine=3.0L v6; displacement=3.0; hp=154; trans=4-speed automatic; drive=RWD | Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only/Mazda/MPV']. | Sources [1]; Mazda source package above. | Do not keep this row as independent clean under IL-confirmed|Mazda|MPV; merge/archive/review with lineage per model action. | KEEP PRIMARY + ALIAS / MERGE DUPLICATES |
| 2 | trim='GLX'; years=1999-2002; body=MPV; fuel=petrol; engine=2.5L v6; displacement=2.5; hp=170; trans=4-speed automatic; drive=FWD | Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only/Mazda/MPV']. | Sources [0]; Mazda source package above. | Do not keep this row as independent clean under IL-confirmed|Mazda|MPV; merge/archive/review with lineage per model action. | KEEP PRIMARY + ALIAS / MERGE DUPLICATES |
| 3 | trim='GLX'; years=2002-2006; body=MPV; fuel=petrol; engine=3.0L v6; displacement=3.0; hp=200; trans=5-speed automatic; drive=FWD | Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only/Mazda/MPV']. | Sources [0]; Mazda source package above. | Do not keep this row as independent clean under IL-confirmed|Mazda|MPV; merge/archive/review with lineage per model action. | KEEP PRIMARY + ALIAS / MERGE DUPLICATES |

---

## MODEL: global-reference-only|Mazda|MPV

CURRENT VALUE: clean profile with 3 technical variants.

PROBLEM: Global-reference-only profile has local sibling(s): ['IL-confirmed|Mazda|MPV']. Do not keep as separate clean Israeli profile.

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- repo source: [0] מאזדה MPV (1996-1999) יד שניה - מחירון, מפרט טכני, אמינות ועוד - iCar (israeli_editorial) — https://www.icar.co.il/%D7%9E%D7%90%D7%96%D7%93%D7%94/%D7%9E%D7%90%D7%96%D7%93%D7%94_MPV/%D7%9E%D7%90%D7%96%D7%93%D7%94_MPV_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%931/
- repo source: [1] מאזדה MPV (2000-2006) יד שניה - מחירון, מפרט טכני, אמינות ועוד - iCar (israeli_editorial) — https://www.icar.co.il/%D7%9E%D7%90%D7%96%D7%93%D7%94/%D7%9E%D7%90%D7%96%D7%93%D7%94_MPV/%D7%9E%D7%90%D7%96%D7%93%D7%94_MPV_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%932/

TARGET VALUE: MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=1996-1999; body=MPV; fuel=petrol; engine=3.0L v6; displacement=3.0; hp=150; trans=4-speed automatic; drive=RWD | Global-reference-only profile has local sibling(s): ['IL-confirmed/Mazda/MPV']. Do not keep as separate clean Israeli profile. | Sources [0]; Mazda source package above. | Do not keep this row as independent clean under global-reference-only|Mazda|MPV; merge/archive/review with lineage per model action. | MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING |
| 2 | trim=None; years=2000-2001; body=MPV; fuel=petrol; engine=2.5L v6; displacement=2.5; hp=170; trans=4-speed automatic; drive=FWD | Global-reference-only profile has local sibling(s): ['IL-confirmed/Mazda/MPV']. Do not keep as separate clean Israeli profile. | Sources [1]; Mazda source package above. | Do not keep this row as independent clean under global-reference-only|Mazda|MPV; merge/archive/review with lineage per model action. | MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING |
| 3 | trim=None; years=2002-2006; body=MPV; fuel=petrol; engine=3.0L v6; displacement=3.0; hp=200; trans=5-speed automatic; drive=FWD | Global-reference-only profile has local sibling(s): ['IL-confirmed/Mazda/MPV']. Do not keep as separate clean Israeli profile. | Sources [1]; Mazda source package above. | Do not keep this row as independent clean under global-reference-only|Mazda|MPV; merge/archive/review with lineage per model action. | MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mazda|MX-30

CURRENT VALUE: clean profile with 1 technical variants.

PROBLEM: Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only|Mazda|MX-30'].

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- repo source: [0] מאזדה MX-30 החשמלי נוחת בישראל בייבוא מקביל (editorial) — https://www.cartube.co.il/חדשות-רכב/מאזדה-mx-30-החשמלי-נוחת-בישראל-בייבוא-מקביל
- repo source: [1] מאזדה MX-30 - מפרט טכני, ממדים (catalog) — https://www.auto.co.il/catalog/mazda/mx-30

TARGET VALUE: KEEP PRIMARY + ALIAS / MERGE DUPLICATES. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP PRIMARY + ALIAS / MERGE DUPLICATES

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2022-None; body=SUV; fuel=electric; engine=electric; displacement=None; hp=145; trans=single_speed; drive=FWD | Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only/Mazda/MX-30']. | Sources [0, 1]; Mazda source package above. | Do not keep this row as independent clean under IL-confirmed|Mazda|MX-30; merge/archive/review with lineage per model action. | KEEP PRIMARY + ALIAS / MERGE DUPLICATES |

---

## MODEL: IL-confirmed|Mazda|MX-5

CURRENT VALUE: clean profile with 7 technical variants.

PROBLEM: IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- repo source: [1223] מאזדה MX-5 (1998-2005) - מפרט טכני, מחירון (israeli_editorial_catalog) — https://www.icar.co.il/מאזדה/מאזדה_MX-5/מאזדה_MX-5_דור_2_דגמי_1998-2005/
- repo source: [1224] מאזדה MX-5 (2006-2015) - מפרט טכני (israeli_editorial_catalog) — https://www.icar.co.il/מאזדה/מאזדה_MX-5/מאזדה_MX-5_דור_3_דגמי_2006-2015/
- repo source: [1225] מאזדה MX-5 דור 4 (2015-2018) מפרט ומחירון (israeli_editorial_catalog) — https://www.icar.co.il/מאזדה/מאזדה_MX-5/מאזדה_MX-5_חדשה/
- repo source: [1226] מפרט טכני מאזדה MX-5 החדשה רשמי (official_importer_page) — https://www.mazda.co.il/models/mx-5

TARGET VALUE: KEEP / FIX FIELDS IF INSTRUCTED. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP / FIX FIELDS IF INSTRUCTED

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=1998-2005; body=Roadster; fuel=petrol; engine=1.8L; displacement=1.8; hp=146; trans=6-speed manual; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1223]; Mazda source package above. | trim=None; years=1998-2005; body=Roadster; fuel=petrol; engine=1.8L; displacement=1.8; hp=146; trans=6-speed manual; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 2 | trim=None; years=2006-2015; body=Roadster; fuel=petrol; engine=2.0L; displacement=2.0; hp=160; trans=6-speed manual; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1224]; Mazda source package above. | trim=None; years=2006-2015; body=Roadster; fuel=petrol; engine=2.0L; displacement=2.0; hp=160; trans=6-speed manual; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 3 | trim=None; years=2006-2015; body=Roadster; fuel=petrol; engine=2.0L; displacement=2.0; hp=160; trans=6-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1224]; Mazda source package above. | trim=None; years=2006-2015; body=Roadster; fuel=petrol; engine=2.0L; displacement=2.0; hp=160; trans=6-speed automatic; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 4 | trim='Luxury'; years=2015-2018; body=Roadster; fuel=petrol; engine=2.0L; displacement=2.0; hp=160; trans=6-speed manual; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1225]; Mazda source package above. | trim='Luxury'; years=2015-2018; body=Roadster; fuel=petrol; engine=2.0L; displacement=2.0; hp=160; trans=6-speed manual; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 5 | trim='Luxury'; years=2015-2018; body=Roadster; fuel=petrol; engine=2.0L; displacement=2.0; hp=160; trans=6-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1225]; Mazda source package above. | trim='Luxury'; years=2015-2018; body=Roadster; fuel=petrol; engine=2.0L; displacement=2.0; hp=160; trans=6-speed automatic; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 6 | trim='Special Edition'; years=2019-2024; body=Roadster; fuel=petrol; engine=2.0L; displacement=2.0; hp=184; trans=6-speed manual; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1226]; Mazda source package above. | trim='Special Edition'; years=2019-2024; body=Roadster; fuel=petrol; engine=2.0L; displacement=2.0; hp=184; trans=6-speed manual; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 7 | trim='Luxury'; years=2019-2024; body=Roadster; fuel=petrol; engine=2.0L; displacement=2.0; hp=184; trans=6-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1226]; Mazda source package above. | trim='Luxury'; years=2019-2024; body=Roadster; fuel=petrol; engine=2.0L; displacement=2.0; hp=184; trans=6-speed automatic; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |

---

## MODEL: IL-confirmed|Mazda|Premacy

CURRENT VALUE: clean profile with 2 technical variants.

PROBLEM: IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- repo source: [1] מאזדה פרמאסי (1999-2005) - מחירון, מפרטים, אמינות ועוד | אוטו (editorial) — https://www.auto.co.il/catalog/mazda/premacy
- repo source: [2] מאזדה פרמאסי - חוות דעת, מחירון, מבחני דרכים - iCar (editorial) — https://www.icar.co.il/%D7%9E%D7%90%D7%96%D7%93%D7%94/%D7%9E%D7%90%D7%96%D7%93%D7%94_%D7%A4%D7%A8%D7%9E%D7%90%D7%A1%D7%99/

TARGET VALUE: KEEP / FIX FIELDS IF INSTRUCTED. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP / FIX FIELDS IF INSTRUCTED

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=1999-2005; body=MPV; fuel=petrol; engine=1.8L; displacement=1.8; hp=114; trans=4-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1, 2]; Mazda source package above. | trim=None; years=1999-2005; body=MPV; fuel=petrol; engine=1.8L; displacement=1.8; hp=114; trans=4-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 2 | trim=None; years=2002-2005; body=MPV; fuel=petrol; engine=2.0L; displacement=2.0; hp=131; trans=4-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1, 2]; Mazda source package above. | trim=None; years=2002-2005; body=MPV; fuel=petrol; engine=2.0L; displacement=2.0; hp=131; trans=4-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |

---

## MODEL: IL-confirmed|Mazda|RX-8

CURRENT VALUE: clean profile with 2 technical variants.

PROBLEM: Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only|Mazda|RX-8'].

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- repo source: [0] מאזדה RX-8 (2003-2008) - מחירון רכב, מפרט טכני, חוות דעת (editorial) — https://www.auto.co.il/model/mazda-rx-8_g128
- repo source: [1] מאזדה RX-8 קופה - מפרט טכני (editorial) — https://www.icar.co.il/mazda/mazda_rx_8/

TARGET VALUE: KEEP PRIMARY + ALIAS / MERGE DUPLICATES. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP PRIMARY + ALIAS / MERGE DUPLICATES

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2003-2008; body=Coupe; fuel=petrol; engine=1.3L rotary; displacement=1.3; hp=192; trans=5-speed manual; drive=RWD | Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only/Mazda/RX-8']. | Sources [0, 1]; Mazda source package above. | Do not keep this row as independent clean under IL-confirmed|Mazda|RX-8; merge/archive/review with lineage per model action. | KEEP PRIMARY + ALIAS / MERGE DUPLICATES |
| 2 | trim=None; years=2003-2008; body=Coupe; fuel=petrol; engine=1.3L rotary; displacement=1.3; hp=231; trans=6-speed manual; drive=RWD | Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only/Mazda/RX-8']. | Sources [0, 1]; Mazda source package above. | Do not keep this row as independent clean under IL-confirmed|Mazda|RX-8; merge/archive/review with lineage per model action. | KEEP PRIMARY + ALIAS / MERGE DUPLICATES |

---

## MODEL: global-reference-only|Mazda|RX-8

CURRENT VALUE: clean profile with 1 technical variants.

PROBLEM: Global-reference-only profile has local sibling(s): ['IL-confirmed|Mazda|RX-8']. Do not keep as separate clean Israeli profile.

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- repo source: [0] מאזדה RX-8 יד שניה - מחירון, חוות דעת, צריכת דלק ועוד - iCar (israeli_catalog) — https://www.icar.co.il/%D7%9E%D7%90%D7%96%D7%93%D7%94/%D7%9E%D7%90%D7%96%D7%93%D7%94_RX-8/%D7%9E%D7%90%D7%96%D7%93%D7%94_RX-8_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%99%D7%94/
- repo source: [1] מאזדה RX-8 - מחירון, מפרטים, אמינות - אוטו (israeli_catalog) — https://www.auto.co.il/model/mazda-rx-8_g212

TARGET VALUE: MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='High Power'; years=2004-2008; body=Coupe; fuel=petrol; engine=1.3L rotary; displacement=1.3; hp=231; trans=6-speed manual; drive=RWD | Global-reference-only profile has local sibling(s): ['IL-confirmed/Mazda/RX-8']. Do not keep as separate clean Israeli profile. | Sources [0, 1]; Mazda source package above. | Do not keep this row as independent clean under global-reference-only|Mazda|RX-8; merge/archive/review with lineage per model action. | MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|Mazda|Tribute

CURRENT VALUE: clean profile with 3 technical variants.

PROBLEM: Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only|Mazda|Tribute'].

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- repo source: [1] מאזדה טריביוט (2001-2006) מפרט טכני - iCar (Israeli automotive portal) — https://www.icar.co.il/%D7%9E%D7%90%D7%96%D7%93%D7%94/%D7%9E%D7%90%D7%96%D7%93%D7%94_%D7%98%D7%A8%D7%99%D7%91%D7%99%D7%95%D7%98_%D7%99%D7%A9%D7%9F/%D7%9E%D7%90%D7%96%D7%93%D7%94_%D7%98%D7%A8%D7%99%D7%91%D7%99%D7%95%D7%98_%D7%99%D7%A9%D7%9F_%D7%93%D7%95%D7%A8_1/
- repo source: [2] מאזדה טריביוט - אוטו (Israeli automotive portal) — https://www.auto.co.il/model/mazda-tribute_g144

TARGET VALUE: KEEP PRIMARY + ALIAS / MERGE DUPLICATES. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP PRIMARY + ALIAS / MERGE DUPLICATES

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2001-2004; body=SUV; fuel=petrol; engine=2.0L; displacement=2.0; hp=124; trans=4-speed automatic; drive=4WD | Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only/Mazda/Tribute']. | Sources [1, 2]; Mazda source package above. | Do not keep this row as independent clean under IL-confirmed|Mazda|Tribute; merge/archive/review with lineage per model action. | KEEP PRIMARY + ALIAS / MERGE DUPLICATES |
| 2 | trim=None; years=2001-2006; body=SUV; fuel=petrol; engine=3.0L v6; displacement=3.0; hp=197; trans=4-speed automatic; drive=4WD | Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only/Mazda/Tribute']. | Sources [1, 2]; Mazda source package above. | Do not keep this row as independent clean under IL-confirmed|Mazda|Tribute; merge/archive/review with lineage per model action. | KEEP PRIMARY + ALIAS / MERGE DUPLICATES |
| 3 | trim=None; years=2004-2006; body=SUV; fuel=petrol; engine=2.3L; displacement=2.3; hp=150; trans=4-speed automatic; drive=4WD | Use this as primary Israeli profile and fold duplicate sibling(s): ['global-reference-only/Mazda/Tribute']. | Sources [1, 2]; Mazda source package above. | Do not keep this row as independent clean under IL-confirmed|Mazda|Tribute; merge/archive/review with lineage per model action. | KEEP PRIMARY + ALIAS / MERGE DUPLICATES |

---

## MODEL: global-reference-only|Mazda|Tribute

CURRENT VALUE: clean profile with 1 technical variants.

PROBLEM: Global-reference-only profile has local sibling(s): ['IL-confirmed|Mazda|Tribute']. Do not keep as separate clean Israeli profile.

WEB-VALIDATED FACT: Mazda Israel official 2026 price/model pages support Mazda2, Mazda3, CX-5, CX-30, CX-90 and MX-5 current listings; iCar/Auto/Cartube support historical 121/323/626/BT-50/CX-3/CX-7/CX-9/MPV/RX-8/Tribute. Global-reference-only duplicates must be merged or archived non-blocking.

SOURCE:
- https://www.mazda.co.il/car-list
- https://www.mazda.co.il/models
- https://www.icar.co.il/מאזדה/
- https://www.cartube.co.il/חדשות-רכב/משפר-עמדות-2026-מאזדה-cx-90-עכשיו-במחיר-249900-שקל-בלבד
- repo source: [0] Mazda Tribute 2 generation SUV 5-doors 2.5 AT 4WD (2008 - 2011) - Specifications (israeli_catalog) — https://autoboom.co.il/en/catalog/cars/mazda/tribute/2-generation/suv-5-doors/2.5-at-4wd-171

TARGET VALUE: MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2008-2011; body=SUV; fuel=petrol; engine=2.5L; displacement=2.5; hp=171; trans=6-speed automatic; drive=4WD | Global-reference-only profile has local sibling(s): ['IL-confirmed/Mazda/Tribute']. Do not keep as separate clean Israeli profile. | Sources [0]; Mazda source package above. | Do not keep this row as independent clean under global-reference-only|Mazda|Tribute; merge/archive/review with lineage per model action. | MERGE / DELETE DUPLICATE / ARCHIVE NON-BLOCKING |

---

## MODEL: global-reference-only|McLaren|540C

CURRENT VALUE: clean profile with 1 technical variants.

PROBLEM: Global-reference-only profile is insufficient for verified Israeli clean without Israeli evidence.

WEB-VALIDATED FACT: McLaren profiles rely on niche Israeli import/market evidence. Keep only if repo-local Israeli source supports the model; otherwise archive/review non-blocking rather than treating global specs as clean Israeli data.

SOURCE:
- https://www.icar.co.il/
- repo source: [1] מקלארן 540C קופה נחשפת - מקלארן להמונים (editorial) — https://www.cartube.co.il/חדשות-רכב/מקלארן-540c-קופה-נחשפת-מקלארן-להמונים
- repo source: [2] מקלארן 540C מידע כללי מחירון ומפרטים (catalog) — https://www.auto.co.il/model/mclaren-540c

TARGET VALUE: MOVE TO REVIEW or ARCHIVE NON-BLOCKING. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: MOVE TO REVIEW or ARCHIVE NON-BLOCKING

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2015-2021; body=Coupe; fuel=petrol; engine=3.8L twin-turbo v8; displacement=3.8; hp=540; trans=7-speed dual_clutch; drive=RWD | Global-reference-only profile is insufficient for verified Israeli clean without Israeli evidence. | Sources [1, 2]; McLaren source package above. | Do not keep this row as independent clean under global-reference-only|McLaren|540C; merge/archive/review with lineage per model action. | MOVE TO REVIEW or ARCHIVE NON-BLOCKING |

---

## MODEL: IL-confirmed|McLaren|Artura

CURRENT VALUE: clean profile with 3 technical variants.

PROBLEM: IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: McLaren profiles rely on niche Israeli import/market evidence. Keep only if repo-local Israeli source supports the model; otherwise archive/review non-blocking rather than treating global specs as clean Israeli data.

SOURCE:
- https://www.icar.co.il/
- repo source: [1] מקלארן ארטורה בישראל - מחיר החל מ- 1.9 מיליון שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A7%D7%9C%D7%90%D7%A8%D7%9F-%D7%90%D7%A8%D7%98%D7%95%D7%A8%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1-9-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C
- repo source: [2] מקלארן ארטורה ספיידר 2024 נחשפת - עם 700 כ"ס (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A7%D7%9C%D7%90%D7%A8%D7%9F-%D7%90%D7%A8%D7%98%D7%95%D7%A8%D7%94-%D7%A1%D7%A4%D7%99%D7%99%D7%93%D7%A8-2024-%D7%A0%D7%97%D7%A9%D7%A4%D7%AA-%D7%A2%D7%9D-700-%D7%9B-%D7%A1

TARGET VALUE: KEEP / FIX FIELDS IF INSTRUCTED. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP / FIX FIELDS IF INSTRUCTED

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2022-2024; body=Coupe; fuel=plug_in_hybrid; engine=3.0L twin-turbo v6; displacement=3.0; hp=680; trans=8-speed dual_clutch; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1]; McLaren source package above. | trim=None; years=2022-2024; body=Coupe; fuel=plug_in_hybrid; engine=3.0L twin-turbo v6; displacement=3.0; hp=680; trans=8-speed dual_clutch; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 2 | trim=None; years=2024-2025; body=Coupe; fuel=plug_in_hybrid; engine=3.0L twin-turbo v6; displacement=3.0; hp=700; trans=8-speed dual_clutch; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [2]; McLaren source package above. | trim=None; years=2024-2025; body=Coupe; fuel=plug_in_hybrid; engine=3.0L twin-turbo v6; displacement=3.0; hp=700; trans=8-speed dual_clutch; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 3 | trim=None; years=2024-2025; body=Convertible; fuel=plug_in_hybrid; engine=3.0L twin-turbo v6; displacement=3.0; hp=700; trans=8-speed dual_clutch; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [2]; McLaren source package above. | trim=None; years=2024-2025; body=Convertible; fuel=plug_in_hybrid; engine=3.0L twin-turbo v6; displacement=3.0; hp=700; trans=8-speed dual_clutch; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |

---

## MODEL: IL-confirmed|McLaren|GT

CURRENT VALUE: clean profile with 1 technical variants.

PROBLEM: Use this as primary Israeli profile and fold duplicate sibling(s): ['IL-likely|McLaren|GT'].

WEB-VALIDATED FACT: McLaren profiles rely on niche Israeli import/market evidence. Keep only if repo-local Israeli source supports the model; otherwise archive/review non-blocking rather than treating global specs as clean Israeli data.

SOURCE:
- https://www.icar.co.il/
- repo source: [1] מקלארן GT החדשה בישראל - מחיר החל מ- 1.6 מיליון שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A7%D7%9C%D7%90%D7%A8%D7%9F-gt-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1-6-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C
- repo source: [2] מקלארן GT - מחירון, קטלוג רכב, מפרט טכני, מבחני דרכים (catalog) — https://www.auto.co.il/model/mclaren-gt_g1369

TARGET VALUE: KEEP PRIMARY + ALIAS / MERGE DUPLICATES. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP PRIMARY + ALIAS / MERGE DUPLICATES

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2020-2023; body=Coupe; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=620; trans=7-speed dual_clutch; drive=RWD | Use this as primary Israeli profile and fold duplicate sibling(s): ['IL-likely/McLaren/GT']. | Sources [1, 2]; McLaren source package above. | Do not keep this row as independent clean under IL-confirmed|McLaren|GT; merge/archive/review with lineage per model action. | KEEP PRIMARY + ALIAS / MERGE DUPLICATES |

---

## MODEL: IL-likely|McLaren|GT

CURRENT VALUE: clean profile with 2 technical variants.

PROBLEM: IL-likely duplicate has IL-confirmed sibling(s): ['IL-confirmed|McLaren|GT']. Merge into confirmed profile with alias/lineage.

WEB-VALIDATED FACT: McLaren profiles rely on niche Israeli import/market evidence. Keep only if repo-local Israeli source supports the model; otherwise archive/review non-blocking rather than treating global specs as clean Israeli data.

SOURCE:
- https://www.icar.co.il/
- repo source: [0] מקלארן GT - מחירון, צריכת דלק, חוות דעת ועוד - iCar (israeli_catalog) — https://www.icar.co.il/%D7%9E%D7%A7%D7%9C%D7%90%D7%A8%D7%9F/%D7%9E%D7%A7%D7%9C%D7%90%D7%A8%D7%9F_GT/
- repo source: [1] מקלארן GTS החדשה 2024 - מחליפת מקלארן GT (israeli_editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A7%D7%9C%D7%90%D7%A8%D7%9F-gts-%D7%94%D7%97%D7%93%D7%A9%D7%94-2024-%D7%9E%D7%97%D7%9C%D7%99%D7%A4%D7%AA-%D7%9E%D7%A7%D7%9C%D7%90%D7%A8%D7%9F-gt

TARGET VALUE: MERGE / ALIAS / DELETE DUPLICATE. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: MERGE / ALIAS / DELETE DUPLICATE

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2019-2023; body=Coupe; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=620; trans=7-speed dual_clutch; drive=RWD | IL-likely duplicate has IL-confirmed sibling(s): ['IL-confirmed/McLaren/GT']. Merge into confirmed profile with alias/lineage. | Sources [0, 1]; McLaren source package above. | Do not keep this row as independent clean under IL-likely|McLaren|GT; merge/archive/review with lineage per model action. | MERGE / ALIAS / DELETE DUPLICATE |
| 2 | trim='GTS'; years=2024-None; body=Coupe; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=635; trans=7-speed dual_clutch; drive=RWD | IL-likely duplicate has IL-confirmed sibling(s): ['IL-confirmed/McLaren/GT']. Merge into confirmed profile with alias/lineage. | Sources [1]; McLaren source package above. | Do not keep this row as independent clean under IL-likely|McLaren|GT; merge/archive/review with lineage per model action. | MERGE / ALIAS / DELETE DUPLICATE |

---

## MODEL: IL-confirmed|Mercedes-Benz|190 (W201)

CURRENT VALUE: clean profile with 4 technical variants.

PROBLEM: IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/
- repo source: [0] מרצדס 190 חוגגת 40 שנה (W201) - היסטוריה ישראלית (editorial) — https://wheel.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-190-%D7%97%D7%95%D7%92%D7%92%D7%AA-40/
- repo source: [1] מרצדס 190 מפרטים טכניים - קטלוג רכבים משומשים (catalog) — https://www.auto.co.il/model/mercedes-benz-190_g368

TARGET VALUE: KEEP / FIX FIELDS IF INSTRUCTED. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP / FIX FIELDS IF INSTRUCTED

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=1990-1993; body=Sedan; fuel=petrol; engine=1.8L i4; displacement=1.8; hp=109; trans=4-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [0, 1]; Mercedes-Benz source package above. | trim=None; years=1990-1993; body=Sedan; fuel=petrol; engine=1.8L i4; displacement=1.8; hp=109; trans=4-speed automatic; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 2 | trim=None; years=1982-1993; body=Sedan; fuel=petrol; engine=2.0L i4; displacement=2.0; hp=118; trans=4-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [0, 1]; Mercedes-Benz source package above. | trim=None; years=1982-1993; body=Sedan; fuel=petrol; engine=2.0L i4; displacement=2.0; hp=118; trans=4-speed automatic; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 3 | trim=None; years=1983-1993; body=Sedan; fuel=diesel; engine=2.0L i4; displacement=2.0; hp=75; trans=5-speed manual; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [0, 1]; Mercedes-Benz source package above. | trim=None; years=1983-1993; body=Sedan; fuel=diesel; engine=2.0L i4; displacement=2.0; hp=75; trans=5-speed manual; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 4 | trim=None; years=1985-1993; body=Sedan; fuel=diesel; engine=2.5L i5; displacement=2.5; hp=94; trans=5-speed manual; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [0, 1]; Mercedes-Benz source package above. | trim=None; years=1985-1993; body=Sedan; fuel=diesel; engine=2.5L i5; displacement=2.5; hp=94; trans=5-speed manual; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |

---

## MODEL: IL-confirmed|Mercedes-Benz|A-Class

CURRENT VALUE: clean profile with 11 technical variants.

PROBLEM: IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/
- repo source: [1724] מרצדס A קלאס החדשה 2018 בישראל - מחיר החל מ-229,900 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-a-%D7%A7%D7%9C%D7%90%D7%A1-%D7%94%D7%97%D7%93%D7%A9%D7%94-2018-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C
- repo source: [1725] מרצדס A קלאס יד שניה (catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_A_%D7%A7%D7%9C%D7%90%D7%A1/%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94/
- repo source: [1726] מפרט טכני מרצדס A-Class Plug-in Hybrid (official_importer) — https://mercedes-benz.co.il/wp-content/uploads/2021/08/A_Class_PHEV_Spec.pdf
- repo source: [1727] מרצדס A קלאס סדאן (catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_A_%D7%A7%D7%9C%D7%90%D7%A1_%D7%A1%D7%93%D7%90%D7%9F/%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94/

TARGET VALUE: KEEP / FIX FIELDS IF INSTRUCTED. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP / FIX FIELDS IF INSTRUCTED

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='A 160'; years=1998-2004; body=Hatchback; fuel=petrol; engine=1.6L; displacement=1.6; hp=102; trans=5-speed automatic; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1725]; Mercedes-Benz source package above. | trim='A 160'; years=1998-2004; body=Hatchback; fuel=petrol; engine=1.6L; displacement=1.6; hp=102; trans=5-speed automatic; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 2 | trim='A 150'; years=2004-2012; body=Hatchback; fuel=petrol; engine=1.5L; displacement=1.5; hp=95; trans=cvt; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1725]; Mercedes-Benz source package above. | trim='A 150'; years=2004-2012; body=Hatchback; fuel=petrol; engine=1.5L; displacement=1.5; hp=95; trans=cvt; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 3 | trim='A 180'; years=2012-2018; body=Hatchback; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=122; trans=7-speed dual_clutch; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1725]; Mercedes-Benz source package above. | trim='A 180'; years=2012-2018; body=Hatchback; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=122; trans=7-speed dual_clutch; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 4 | trim='A 45 AMG'; years=2013-2018; body=Hatchback; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=360; trans=7-speed dual_clutch; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1725]; Mercedes-Benz source package above. | trim='A 45 AMG'; years=2013-2018; body=Hatchback; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=360; trans=7-speed dual_clutch; drive=AWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 5 | trim='A 180'; years=2018-2024; body=Hatchback; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=136; trans=7-speed dual_clutch; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1724, 1725]; Mercedes-Benz source package above. | trim='A 180'; years=2018-2024; body=Hatchback; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=136; trans=7-speed dual_clutch; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 6 | trim='A 200'; years=2018-2024; body=Hatchback; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=163; trans=7-speed dual_clutch; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1724, 1725]; Mercedes-Benz source package above. | trim='A 200'; years=2018-2024; body=Hatchback; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=163; trans=7-speed dual_clutch; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 7 | trim='A 180'; years=2019-2024; body=Sedan; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=136; trans=7-speed dual_clutch; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1727]; Mercedes-Benz source package above. | trim='A 180'; years=2019-2024; body=Sedan; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=136; trans=7-speed dual_clutch; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 8 | trim='A 200'; years=2019-2024; body=Sedan; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=163; trans=7-speed dual_clutch; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1727]; Mercedes-Benz source package above. | trim='A 200'; years=2019-2024; body=Sedan; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=163; trans=7-speed dual_clutch; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 9 | trim='A 250 e'; years=2020-2024; body=Hatchback; fuel=plug_in_hybrid; engine=1.3L turbo; displacement=1.3; hp=218; trans=8-speed dual_clutch; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1725, 1726]; Mercedes-Benz source package above. | trim='A 250 e'; years=2020-2024; body=Hatchback; fuel=plug_in_hybrid; engine=1.3L turbo; displacement=1.3; hp=218; trans=8-speed dual_clutch; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 10 | trim='A 250 e'; years=2020-2024; body=Sedan; fuel=plug_in_hybrid; engine=1.3L turbo; displacement=1.3; hp=218; trans=8-speed dual_clutch; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1726, 1727]; Mercedes-Benz source package above. | trim='A 250 e'; years=2020-2024; body=Sedan; fuel=plug_in_hybrid; engine=1.3L turbo; displacement=1.3; hp=218; trans=8-speed dual_clutch; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 11 | trim='A 35 AMG'; years=2019-2024; body=Sedan; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=306; trans=7-speed dual_clutch; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1727]; Mercedes-Benz source package above. | trim='A 35 AMG'; years=2019-2024; body=Sedan; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=306; trans=7-speed dual_clutch; drive=AWD | KEEP / FIX FIELDS IF INSTRUCTED |

---

## MODEL: IL-confirmed|Mercedes-Benz|AMG GT

CURRENT VALUE: clean profile with 7 technical variants.

PROBLEM: IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/
- repo source: [0] מרצדס AMG GT קופה החדשה 2024 בישראל - מחיר החל מ-1,350,000 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-amg-gt-%D7%A7%D7%95%D7%A4%D7%94-%D7%94%D7%97%D7%93%D7%A9%D7%94-2024-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1,350,000-%D7%A9%D7%A7%D7%9C
- repo source: [1] מרצדס AMG GT 4 דלתות - מעתה גם בישראל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-amg-gt-4-%D7%93%D7%9C%D7%AA%D7%95%D7%AA-%D7%9E%D7%A2%D7%AA%D7%94-%D7%92%D7%9D-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C
- repo source: [2] מרצדס AMG GT רודסטר בישראל - מחירים החל מ- 1.35 מיליון שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-amg-gt-%D7%A8%D7%95%D7%93%D7%A1%D7%98%D7%A8-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D-%D7%94%D7%97%D7%9C-%D7%9E-1-35-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C
- repo source: [3] מרצדס AMG GT קופה - מחירון, מפרטים ורמות גימור (catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_AMG_GT/
- repo source: [4] מרצדס AMG GT 4 דלתות - מחירון, מפרטים ורמות גימור (catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_AMG_GT_4_%D7%93%D7%9C%D7%AA%D7%95%D7%AA/

TARGET VALUE: KEEP / FIX FIELDS IF INSTRUCTED. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP / FIX FIELDS IF INSTRUCTED

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='GT'; years=2015-2021; body=Coupe; fuel=petrol; engine=4.0L v8 biturbo; displacement=4.0; hp=476; trans=7-speed dual_clutch; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [3]; Mercedes-Benz source package above. | trim='GT'; years=2015-2021; body=Coupe; fuel=petrol; engine=4.0L v8 biturbo; displacement=4.0; hp=476; trans=7-speed dual_clutch; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 2 | trim='GT S'; years=2015-2021; body=Coupe; fuel=petrol; engine=4.0L v8 biturbo; displacement=4.0; hp=522; trans=7-speed dual_clutch; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [3]; Mercedes-Benz source package above. | trim='GT S'; years=2015-2021; body=Coupe; fuel=petrol; engine=4.0L v8 biturbo; displacement=4.0; hp=522; trans=7-speed dual_clutch; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 3 | trim='GT C'; years=2017-2021; body=Roadster; fuel=petrol; engine=4.0L v8 biturbo; displacement=4.0; hp=557; trans=7-speed dual_clutch; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [2, 3]; Mercedes-Benz source package above. | trim='GT C'; years=2017-2021; body=Roadster; fuel=petrol; engine=4.0L v8 biturbo; displacement=4.0; hp=557; trans=7-speed dual_clutch; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 4 | trim='GT 43'; years=2019-2023; body=Liftback; fuel=mild_hybrid; engine=3.0L i6 turbo; displacement=3.0; hp=367; trans=9-speed automatic; drive=RWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1, 4]; Mercedes-Benz source package above. | trim='GT 43'; years=2019-2023; body=Liftback; fuel=mild_hybrid; engine=3.0L i6 turbo; displacement=3.0; hp=367; trans=9-speed automatic; drive=RWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 5 | trim='GT 53 4MATIC+'; years=2019-2023; body=Liftback; fuel=mild_hybrid; engine=3.0L i6 turbo; displacement=3.0; hp=435; trans=9-speed automatic; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1, 4]; Mercedes-Benz source package above. | trim='GT 53 4MATIC+'; years=2019-2023; body=Liftback; fuel=mild_hybrid; engine=3.0L i6 turbo; displacement=3.0; hp=435; trans=9-speed automatic; drive=AWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 6 | trim='GT 63 S 4MATIC+'; years=2019-2023; body=Liftback; fuel=petrol; engine=4.0L v8 biturbo; displacement=4.0; hp=639; trans=9-speed automatic; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1, 4]; Mercedes-Benz source package above. | trim='GT 63 S 4MATIC+'; years=2019-2023; body=Liftback; fuel=petrol; engine=4.0L v8 biturbo; displacement=4.0; hp=639; trans=9-speed automatic; drive=AWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 7 | trim='GT 63 4MATIC+'; years=2024-2026; body=Coupe; fuel=petrol; engine=4.0L v8 biturbo; displacement=4.0; hp=585; trans=9-speed automatic; drive=AWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [0]; Mercedes-Benz source package above. | trim='GT 63 4MATIC+'; years=2024-2026; body=Coupe; fuel=petrol; engine=4.0L v8 biturbo; displacement=4.0; hp=585; trans=9-speed automatic; drive=AWD | KEEP / FIX FIELDS IF INSTRUCTED |

---

## MODEL: IL-confirmed|Mercedes-Benz|B-Class

CURRENT VALUE: clean profile with 4 technical variants.

PROBLEM: IL-confirmed profile; validate all variant fields against embedded/repo-local sources.

WEB-VALIDATED FACT: Mercedes-Benz Israel official pages support current 2026 lineup and prices for GLA/GLB/GLC/GLE/GLS/CLA/CLE/AMG GT and electric EQA/EQE/EQE SUV/EQS/EQS SUV; iCar/Cartube support historical C/E/A/B/SL/SLK/GLK/R-Class/CLS etc. Global-only duplicates such as EQA/EQB must merge into IL-confirmed or review blocker profiles. EV rows must have displacement null and single-speed/direct-drive schema.

SOURCE:
- https://www.mercedes-benz.co.il/models/
- https://www.mercedes-benz.co.il/our-brands/mercedes-electric-vehicles/
- https://www.mercedes-benz.co.il/models/glc-suv/
- https://www.mercedes-benz.co.il/models/eqa-fl/
- https://www.icar.co.il/מרצדס/
- repo source: [0] מרצדס B קלאס החדשה בישראל - מחיר החל מ- 207,900 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-b-%D7%A7%D7%9C%D7%90%D7%A1-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-207900-%D7%A9%D7%A7%D7%9C
- repo source: [1] מרצדס B-קלאס - קטלוג רכבים חדשים - אוטו (catalog) — https://www.auto.co.il/model/mercedes-benz-b-class_g1362
- repo source: [2] מרצדס B-קלאס (2012-2018) יד שניה - אוטו (editorial) — https://www.auto.co.il/model/mercedes-benz-b-class_g144
- repo source: [3] מרצדס B קלאס (2006-2012) יד שניה - אוטו (editorial) — https://www.auto.co.il/model/mercedes-benz-b-class_g144_old
- repo source: [4] מרצדס A250e ו-B250e פלאג-אין בישראל - מחיר החל מ-244,900 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-a250e-%D7%95-b250e-%D7%A4%D7%9C%D7%90%D7%92-%D7%90%D7%99%D7%9F-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-244900-%D7%A9%D7%A7%D7%9C

TARGET VALUE: KEEP / FIX FIELDS IF INSTRUCTED. Preserve field_sources/source_indexes for all kept rows. Preserve alias/lineage when merging or archiving.

ACTION: KEEP / FIX FIELDS IF INSTRUCTED

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='B 200'; years=2006-2012; body=MPV; fuel=petrol; engine=2.0L; displacement=2.0; hp=136; trans=cvt; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [3]; Mercedes-Benz source package above. | trim='B 200'; years=2006-2012; body=MPV; fuel=petrol; engine=2.0L; displacement=2.0; hp=136; trans=cvt; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 2 | trim='B 180'; years=2012-2018; body=MPV; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=122; trans=7-speed dual_clutch; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [2]; Mercedes-Benz source package above. | trim='B 180'; years=2012-2018; body=MPV; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=122; trans=7-speed dual_clutch; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 3 | trim='B 200'; years=2019-2024; body=MPV; fuel=petrol; engine=1.33L turbo; displacement=1.33; hp=163; trans=7-speed dual_clutch; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [0, 1]; Mercedes-Benz source package above. | trim='B 200'; years=2019-2024; body=MPV; fuel=petrol; engine=1.33L turbo; displacement=1.33; hp=163; trans=7-speed dual_clutch; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |
| 4 | trim='B 250 e'; years=2020-2024; body=MPV; fuel=plug_in_hybrid; engine=1.33L turbo; displacement=1.33; hp=218; trans=8-speed dual_clutch; drive=FWD | IL-confirmed profile; validate all variant fields against embedded/repo-local sources. | Sources [1, 4]; Mercedes-Benz source package above. | trim='B 250 e'; years=2020-2024; body=MPV; fuel=plug_in_hybrid; engine=1.33L turbo; displacement=1.33; hp=218; trans=8-speed dual_clutch; drive=FWD | KEEP / FIX FIELDS IF INSTRUCTED |


## Required checks after RUN implementation

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Also audit actual generated files: clean catalog, readiness, review, archive, quality scan, compute_resume_state(), unmatched_output_keys, active blockers, cursor/resume state, split aliases.

Do not claim PASS unless actual files and metrics prove this run was applied.


## Required Codex checks for RUN 3

Run after implementation:

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
- readiness
- review
- archive
- quality scan
- compute_resume_state()
- unmatched_output_keys
- active blockers
- cursor/resume state
- duplicate/split alias cleanup
```

Temporary-file cleanup is mandatory:

```text
Before final commit, delete codex_tasks/BATCH26_RUN3_*.md unless the user explicitly asks to keep them.
```

Report exact before/after metrics, all changed files, test results, and any conflicts.


# ==============================
# RUN4
# source: BATCH26_RUN4_VARIANT_LEVEL_CODEX_TASK.md
# ==============================

# BATCH26 RUN 4 ONLY — variant-level web-validated Codex task
TEMPORARY FILE RULE: This is a temporary instruction file. After RUN 4 is fully applied and verified, delete `codex_tasks/BATCH26_RUN4_*.md` from the repo before final commit unless the user explicitly requests keeping it.
DO NOT BROWSE THE INTERNET. All web-validation facts and target corrections are embedded here and in repo-local sources. Use this file as the single source of truth for RUN 4 only. Do not apply RUN 1, RUN 2, RUN 3, RUN 5, later runs, FINAL blockers, or any unified batch task.
If repo-local evidence conflicts with this task file, report it instead of guessing. If a variant cannot be grounded with embedded facts or repo-local sources, move it to non-blocking review/archive with clear reason and lineage rather than fabricating clean data.
## Scope

```text
RUN 4 only
from: IL-confirmed|Mercedes-Benz|C-Class
to: IL-confirmed|Mercedes-Benz|Maybach GLS
profiles: 20
technical_variants covered: 92/92
```

## Web-validation source package for RUN 4

Use these embedded web facts as the external validation layer. Codex must not browse.

### Mercedes-Benz Israel / Israeli-market anchors
- Mercedes-Benz Israel official C-Class page lists current C 180, C 300, C 300 e, AMG C 43 and AMG C 63 S E Performance trims, so the C-Class profile must not remain a 2024-closed profile when current rows are supported.
  SOURCE: https://www.mercedes-benz.co.il/models/c-class/
- Auto / Cartube Israeli specs support current C-Class technical values: C180 1.5L 170 hp, C300 2.0L 258 hp, C300e 2.0 PHEV 313 hp, C43 about 408 hp; use only values that can be grounded by embedded source/repo-local source.
  SOURCE: https://www.auto.co.il/articles/test-drives/road-tests/136733/
  SOURCE: https://www.cartube.co.il/מחירון-רכב-חדש/מרצדס/מרצדס-c-קלאס
- Mercedes-Benz Israel official models page lists current E-Class, EQA, EQB, EQS SUV, G-Class, GLA, GLC, GLC Coupé, GLS and GLS Maybach, and current CLA/CLE categories. Do not close those current official models at 2024 unless the specific variant was replaced.
  SOURCE: https://www.mercedes-benz.co.il/models/
- Mercedes-Benz Israel official E-Class page lists current E 200, E 300 e and E 450 4Matic variants. The profile must not remain closed at 2024 where current E200/E300e rows are supported.
  SOURCE: https://www.mercedes-benz.co.il/models/e-class/
- Mercedes-Benz Israel official GLC SUV page lists GLC 200 4Matic, GLC 300 4Matic, GLC 300 e 4Matic and AMG GLC 53; official GLC Coupé page lists GLC Coupé 300e trims. Null trims in current GLC rows must be replaced by marketed names where the row is kept.
  SOURCE: https://www.mercedes-benz.co.il/models/glc-suv/
  SOURCE: https://www.mercedes-benz.co.il/models/glc-coupe/
- Mercedes-Benz Israel official G-Class page lists current G 450 d, G 500 and AMG G 63. Existing G 350 d should not be extended beyond its supported historical period; current diesel should be G 450 d if added/updated.
  SOURCE: https://www.mercedes-benz.co.il/models/g-class/
- Mercedes-Benz Israel official EQS SUV page lists current EQS SUV 450 and EQS SUV 580 trims, so SUV rows must live under EQS SUV, not mixed into a generic/sedan EQS profile.
  SOURCE: https://www.mercedes-benz.co.il/models/eqs/
- Mercedes-Benz Israel vans official EQV page lists current EQV electric; Israeli sources support 204 hp FWD. EV schema must use displacement null and a valid EV transmission convention (single_speed/direct_drive), not a generic automatic unless the repo schema explicitly maps EV automatic.
  SOURCE: https://www.mercedes-benz.co.il/vans/van-models/eqv/
  SOURCE: https://www.icar.co.il/מרצדס/מרצדס_EQV/מרצדס_EQV_יד_שניה_ד10/
- iCar/Auto/Cartube historical Israeli-market sources support older Citan/CLS/GLK/GLS/C-Class/E-Class rows, but historical rows must not be extended to current merely because the model name still exists.
  SOURCE: https://www.icar.co.il/מרצדס/

## Required implementation outcomes for RUN 4

```text
- Every listed variant receives KEEP/FIX/MERGE/MOVE/REVIEW/ARCHIVE handling.
- Do not leave duplicate Citan clean profiles.
- Do not leave EQS SUV variants duplicated under both EQS and EQS SUV.
- EV schema: engine_displacement_l=null and valid EV transmission convention.
- Current official Mercedes models must not be closed at 2024 when exact current rows are grounded.
- Historical rows must not be extended simply because the model name still exists.
- Preserve source_indexes/field_sources for every KEEP row; repair or report invalid/local/global source indexes.
```

---

## MODEL: IL-confirmed|Mercedes-Benz|C-Class
CURRENT VALUE: clean profile with 7 technical variants; profile years=2014-2024.

PROBLEM: Official Israel page proves current C-Class; fix profile year_end/current coverage. Existing C180 2021-2024 and C300e 2021-2024 should not stay closed at 2024 if current values are grounded. Existing C200 2021-2024 is not the current official C300, so do not relabel it silently; keep as historical or add a separate C300 row. Add missing current C300/AMG rows only with exact embedded/repo-local specs.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס C קלאס החדשה 2021 בישראל - מחיר החל מ-329,900 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-c-%D7%A7%D7%9C%D7%90%D7%A1-%D7%94%D7%97%D7%93%D7%A9%D7%94-2021-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-329-900-%D7%A9%D7%A7%D7%9C
- repo source [1] מרצדס C קלאס החדשה (W205) בישראל – מחיר החל מ-295,900 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-c-%D7%A7%D7%9C%D7%90%D7%A1-%D7%94%D7%97%D7%93%D7%A9%D7%94-w205-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-295-900-%D7%A9%D7%A7%D7%9C
- repo source [2] מרצדס C-קלאס - מפרט טכני (catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_C-%D7%A7%D7%9C%D7%90%D7%A1/

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='C 180'; years=2014-2018; body=Sedan; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=156; trans=7-speed automatic; drive=RWD; sources=[1, 2] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='C 180'; years=2014-2018; body=Sedan; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=156; trans=7-speed automatic; drive=RWD; sources=[1, 2] | KEEP |
| 2 | trim='C 200'; years=2014-2018; body=Sedan; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=184; trans=7-speed automatic; drive=RWD; sources=[1, 2] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='C 200'; years=2014-2018; body=Sedan; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=184; trans=7-speed automatic; drive=RWD; sources=[1, 2] | KEEP |
| 3 | trim='C 350 e'; years=2015-2018; body=Sedan; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=279; trans=7-speed automatic; drive=RWD; sources=[2] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='C 350 e'; years=2015-2018; body=Sedan; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=279; trans=7-speed automatic; drive=RWD; sources=[2] | KEEP |
| 4 | trim='C 200'; years=2018-2021; body=Sedan; fuel=mild_hybrid; engine=1.5L turbo; displacement=1.5; hp=184; trans=9-speed automatic; drive=RWD; sources=[2] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='C 200'; years=2018-2021; body=Sedan; fuel=mild_hybrid; engine=1.5L turbo; displacement=1.5; hp=184; trans=9-speed automatic; drive=RWD; sources=[2] | KEEP |
| 5 | trim='C 180'; years=2021-2024; body=Sedan; fuel=mild_hybrid; engine=1.5L turbo; displacement=1.5; hp=170; trans=9-speed automatic; drive=RWD; sources=[0, 2] | Current C-Class row is closed at 2024 despite official current Israeli C-Class lineup. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='C 180'; years=2021-2026; body=Sedan; fuel=mild_hybrid; engine=1.5L turbo; displacement=1.5; hp=170; trans=9-speed automatic; drive=RWD; sources=[0, 2] | FIX |
| 6 | trim='C 200'; years=2021-2024; body=Sedan; fuel=mild_hybrid; engine=1.5L turbo; displacement=1.5; hp=204; trans=9-speed automatic; drive=RWD; sources=[0, 2] | C 200 is historical/previous current row; official current lineup uses C 300, not C 200. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='C 200'; years=2021-2024; body=Sedan; fuel=mild_hybrid; engine=1.5L turbo; displacement=1.5; hp=204; trans=9-speed automatic; drive=RWD; sources=[0, 2] | KEEP / DO NOT EXTEND |
| 7 | trim='C 300 e'; years=2021-2024; body=Sedan; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=313; trans=9-speed automatic; drive=RWD; sources=[0, 2] | Current C-Class row is closed at 2024 despite official current Israeli C-Class lineup. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='C 300 e'; years=2021-2026; body=Sedan; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=313; trans=9-speed automatic; drive=RWD; sources=[0, 2] | FIX |

MODEL-LEVEL ADD/FIX: Add missing current C 300 row (2.0L turbo mild_hybrid, 258 hp, 9-speed automatic, RWD/AWD according to repo-local source) and AMG C 43/C63 rows only if exact embedded/repo-local source supports all required fields; otherwise create non-blocking review entries for missing current variants rather than fabricating.

---

## MODEL: IL-confirmed|Mercedes-Benz|Citan
CURRENT VALUE: clean profile with 5 technical variants; profile years=2013-2024.

PROBLEM: There are two Citan clean profiles in this window. Use IL-confirmed Citan as primary; merge IL-likely Citan into it with alias/lineage. Empty trims in duplicate profile are not acceptable if marketed names such as 109 CDI/110 CDI/111 CDI or current 110/112 CDI can be grounded. Do not keep duplicate clean Citan profiles.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס סיטאן - מחירון, מפרט טכני, חוות דעת - iCar (auto_catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_%D7%A1%D7%99%D7%98%D7%90%D7%9F/
- repo source [1] מרצדס סיטאן החדש 2022 בישראל - מחיר החל מ-175,000 שקל - cartube (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-%D7%A1%D7%99%D7%98%D7%90%D7%9F-%D7%94%D7%97%D7%93%D7%A9-2022-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-175000-%D7%A9%D7%A7%D7%9C

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='109 CDI'; years=2013-2021; body=Van; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=90; trans=5-speed manual; drive=FWD; sources=[0] | Primary profile; must absorb duplicate IL-likely Citan and avoid duplicate clean profile. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='109 CDI'; years=2013-2021; body=Van; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=90; trans=5-speed manual; drive=FWD; sources=[0] | KEEP / MERGE SIBLING |
| 2 | trim='109 CDI'; years=2013-2021; body=MPV; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=90; trans=5-speed manual; drive=FWD; sources=[0] | Primary profile; must absorb duplicate IL-likely Citan and avoid duplicate clean profile. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='109 CDI'; years=2013-2021; body=MPV; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=90; trans=5-speed manual; drive=FWD; sources=[0] | KEEP / MERGE SIBLING |
| 3 | trim='111 CDI'; years=2013-2021; body=Van; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=110; trans=6-speed manual; drive=FWD; sources=[0] | Primary profile; must absorb duplicate IL-likely Citan and avoid duplicate clean profile. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='111 CDI'; years=2013-2021; body=Van; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=110; trans=6-speed manual; drive=FWD; sources=[0] | KEEP / MERGE SIBLING |
| 4 | trim='110 CDI'; years=2022-2024; body=Van; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=95; trans=7-speed dual_clutch; drive=FWD; sources=[1] | Primary profile; must absorb duplicate IL-likely Citan and avoid duplicate clean profile. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='110 CDI'; years=2022-2024; body=Van; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=95; trans=7-speed dual_clutch; drive=FWD; sources=[1] | KEEP / MERGE SIBLING |
| 5 | trim='110 CDI'; years=2022-2024; body=MPV; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=95; trans=7-speed dual_clutch; drive=FWD; sources=[1] | Primary profile; must absorb duplicate IL-likely Citan and avoid duplicate clean profile. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='110 CDI'; years=2022-2024; body=MPV; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=95; trans=7-speed dual_clutch; drive=FWD; sources=[1] | KEEP / MERGE SIBLING |

---

## MODEL: IL-likely|Mercedes-Benz|Citan
CURRENT VALUE: clean profile with 5 technical variants; profile years=2013-None.

PROBLEM: There are two Citan clean profiles in this window. Use IL-confirmed Citan as primary; merge IL-likely Citan into it with alias/lineage. Empty trims in duplicate profile are not acceptable if marketed names such as 109 CDI/110 CDI/111 CDI or current 110/112 CDI can be grounded. Do not keep duplicate clean Citan profiles.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס סיטאן החדש 2023 בישראל - מחיר החל מ- 167,000 שקלים (automotive_news) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-%D7%A1%D7%99%D7%98%D7%90%D7%9F-%D7%94%D7%97%D7%93%D7%A9-2023-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-167-000-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D
- repo source [1] מרצדס סיטאן - מחירון רכב, מפרט טכני (automotive_database) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_%D7%A1%D7%99%D7%98%D7%90%D7%9F/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_%D7%A1%D7%99%D7%98%D7%90%D7%9F_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%931/

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2023-None; body=Van; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=95; trans=6-speed manual; drive=FWD; sources=[1] | Duplicate Citan clean profile with empty trims and overlapping years. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | Merge into IL-confirmed/Mercedes-Benz/Citan; preserve unique current 2023+ 95/116 hp rows with marketed trims if grounded; archive duplicate profile non-blocking with lineage. | MERGE |
| 2 | trim=None; years=2023-None; body=Van; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=95; trans=7-speed dual_clutch; drive=FWD; sources=[1] | Duplicate Citan clean profile with empty trims and overlapping years. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | Merge into IL-confirmed/Mercedes-Benz/Citan; preserve unique current 2023+ 95/116 hp rows with marketed trims if grounded; archive duplicate profile non-blocking with lineage. | MERGE |
| 3 | trim=None; years=2023-None; body=Van; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=116; trans=7-speed dual_clutch; drive=FWD; sources=[1] | Duplicate Citan clean profile with empty trims and overlapping years. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | Merge into IL-confirmed/Mercedes-Benz/Citan; preserve unique current 2023+ 95/116 hp rows with marketed trims if grounded; archive duplicate profile non-blocking with lineage. | MERGE |
| 4 | trim=None; years=2013-2021; body=Van; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=90; trans=5-speed manual; drive=FWD; sources=[2] | Duplicate Citan clean profile with empty trims and overlapping years. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | Merge into IL-confirmed/Mercedes-Benz/Citan; preserve unique current 2023+ 95/116 hp rows with marketed trims if grounded; archive duplicate profile non-blocking with lineage. | MERGE |
| 5 | trim=None; years=2013-2021; body=Van; fuel=diesel; engine=1.5L turbo; displacement=1.5; hp=110; trans=6-speed manual; drive=FWD; sources=[2] | Duplicate Citan clean profile with empty trims and overlapping years. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | Merge into IL-confirmed/Mercedes-Benz/Citan; preserve unique current 2023+ 95/116 hp rows with marketed trims if grounded; archive duplicate profile non-blocking with lineage. | MERGE |

---

## MODEL: IL-confirmed|Mercedes-Benz|CLA
CURRENT VALUE: clean profile with 8 technical variants; profile years=2013-2026.

PROBLEM: Repair source indexes if they are repo-global indexes rather than local model source indexes. Do not mix the new CLA Electric/CLA EQ into the ICE/PHEV CLA profile unless a separate clean electric profile is explicitly created with lineage. Confirm 2019-2026 ICE/PHEV rows against local current source before leaving them open-ended.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס CLA דור 1 (2013-2019) - מפרט טכני (editorial) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_CLA/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_CLA_%D7%93%D7%95%D7%A8_1/
- repo source [1] מרצדס CLA החדשה 2019 בישראל - מחיר החל מ- 252,900 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-cla-%D7%94%D7%97%D7%93%D7%A9%D7%94-2019-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-252-900-%D7%A9%D7%A7%D7%9C
- repo source [2] מרצדס פלאג-אין A250e ו- CLA 250e בישראל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-%D7%A4%D7%9C%D7%90%D7%92-%D7%90%D7%99%D7%9F-a250e-%D7%95-cla-250e-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-229-900-%D7%A9%D7%A7%D7%9C

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2013-2019; body=Coupe; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=122; trans=7-speed dual_clutch; drive=FWD; sources=[1760] | Some source_indexes look repo-global rather than model-local; current years must be grounded. Do not mix CLA EQ into ICE/PHEV CLA. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2013-2019; body=Coupe; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=122; trans=7-speed dual_clutch; drive=FWD; sources=[1760] | FIX SOURCE INDEXES / KEEP IF GROUNDED |
| 2 | trim=None; years=2013-2019; body=Coupe; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=156; trans=7-speed dual_clutch; drive=FWD; sources=[1760] | Some source_indexes look repo-global rather than model-local; current years must be grounded. Do not mix CLA EQ into ICE/PHEV CLA. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2013-2019; body=Coupe; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=156; trans=7-speed dual_clutch; drive=FWD; sources=[1760] | FIX SOURCE INDEXES / KEEP IF GROUNDED |
| 3 | trim=None; years=2013-2015; body=Coupe; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=360; trans=7-speed dual_clutch; drive=AWD; sources=[1760] | Some source_indexes look repo-global rather than model-local; current years must be grounded. Do not mix CLA EQ into ICE/PHEV CLA. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2013-2015; body=Coupe; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=360; trans=7-speed dual_clutch; drive=AWD; sources=[1760] | FIX SOURCE INDEXES / KEEP IF GROUNDED |
| 4 | trim=None; years=2016-2019; body=Coupe; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=381; trans=7-speed dual_clutch; drive=AWD; sources=[1760] | Some source_indexes look repo-global rather than model-local; current years must be grounded. Do not mix CLA EQ into ICE/PHEV CLA. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2016-2019; body=Coupe; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=381; trans=7-speed dual_clutch; drive=AWD; sources=[1760] | FIX SOURCE INDEXES / KEEP IF GROUNDED |
| 5 | trim=None; years=2019-2026; body=Coupe; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=136; trans=7-speed dual_clutch; drive=FWD; sources=[1761] | Some source_indexes look repo-global rather than model-local; current years must be grounded. Do not mix CLA EQ into ICE/PHEV CLA. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2019-2026; body=Coupe; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=136; trans=7-speed dual_clutch; drive=FWD; sources=[1761] | FIX SOURCE INDEXES / KEEP IF GROUNDED |
| 6 | trim=None; years=2019-2026; body=Coupe; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=163; trans=7-speed dual_clutch; drive=FWD; sources=[1761] | Some source_indexes look repo-global rather than model-local; current years must be grounded. Do not mix CLA EQ into ICE/PHEV CLA. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2019-2026; body=Coupe; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=163; trans=7-speed dual_clutch; drive=FWD; sources=[1761] | FIX SOURCE INDEXES / KEEP IF GROUNDED |
| 7 | trim=None; years=2019-2026; body=Coupe; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=306; trans=7-speed dual_clutch; drive=AWD; sources=[1761] | Some source_indexes look repo-global rather than model-local; current years must be grounded. Do not mix CLA EQ into ICE/PHEV CLA. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2019-2026; body=Coupe; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=306; trans=7-speed dual_clutch; drive=AWD; sources=[1761] | FIX SOURCE INDEXES / KEEP IF GROUNDED |
| 8 | trim=None; years=2020-2026; body=Coupe; fuel=plug_in_hybrid; engine=1.3L turbo; displacement=1.3; hp=218; trans=8-speed dual_clutch; drive=FWD; sources=[1762] | Some source_indexes look repo-global rather than model-local; current years must be grounded. Do not mix CLA EQ into ICE/PHEV CLA. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2020-2026; body=Coupe; fuel=plug_in_hybrid; engine=1.3L turbo; displacement=1.3; hp=218; trans=8-speed dual_clutch; drive=FWD; sources=[1762] | FIX SOURCE INDEXES / KEEP IF GROUNDED |

---

## MODEL: IL-confirmed|Mercedes-Benz|CLE
CURRENT VALUE: clean profile with 4 technical variants; profile years=2024-2024.

PROBLEM: Official current CLE Coupé/Cabriolet pages support CLE current beyond 2024. Current rows should not remain year_end=2024 where the model is still listed. Null trims should be normalized to marketed variant names: CLE 200 / CLE 300 4MATIC and body Coupe/Cabriolet where supported.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס CLE קופה נוחתת בישראל - מחיר החל מ-505,000 שקל (editorial) — https://www.cartube.co.il/חדשות-רכב/מרצדס-cle-קופה-בישראל-מחיר-החל-מ-505000-שקל
- repo source [1] מרצדס CLE קבריולה - מחירון, מפרטים, אבזור ועוד (catalog) — https://www.icar.co.il/מרצדס/מרצדס_CLE_קבריולה/
- repo source [2] קטלוג מפרטים מרצדס CLE קופה החדשה (official) — https://www.mercedes-benz.co.il/models/cle-coupe/

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2024-2024; body=Coupe; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=204; trans=9-speed automatic; drive=RWD; sources=[0, 2] | Current CLE rows are closed at 2024 and have null trim despite official current CLE pages. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2024-2026; body=Coupe; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=204; trans=9-speed automatic; drive=RWD; sources=[0, 2]; set version_or_trim to CLE 200/CLE 300 4MATIC matching hp/body. | FIX |
| 2 | trim=None; years=2024-2024; body=Coupe; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=258; trans=9-speed automatic; drive=AWD; sources=[0, 2] | Current CLE rows are closed at 2024 and have null trim despite official current CLE pages. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2024-2026; body=Coupe; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=258; trans=9-speed automatic; drive=AWD; sources=[0, 2]; set version_or_trim to CLE 200/CLE 300 4MATIC matching hp/body. | FIX |
| 3 | trim=None; years=2024-2024; body=Convertible; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=204; trans=9-speed automatic; drive=RWD; sources=[1] | Current CLE rows are closed at 2024 and have null trim despite official current CLE pages. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2024-2026; body=Convertible; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=204; trans=9-speed automatic; drive=RWD; sources=[1]; set version_or_trim to CLE 200/CLE 300 4MATIC matching hp/body. | FIX |
| 4 | trim=None; years=2024-2024; body=Convertible; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=258; trans=9-speed automatic; drive=AWD; sources=[1] | Current CLE rows are closed at 2024 and have null trim despite official current CLE pages. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2024-2026; body=Convertible; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=258; trans=9-speed automatic; drive=AWD; sources=[1]; set version_or_trim to CLE 200/CLE 300 4MATIC matching hp/body. | FIX |

---

## MODEL: IL-confirmed|Mercedes-Benz|CLS
CURRENT VALUE: clean profile with 6 technical variants; profile years=2005-2023.

PROBLEM: CLS is historical/discontinued in this catalog window. Keep rows historical through 2023; do not extend to 2026 just because Mercedes still has coupe categories.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס CLS דור 1 (2005-2010) - מפרט טכני | iCar (catalog) — https://www.icar.co.il/מרצדס/מרצדס_CLS/מרצדס_CLS_דור_1_יד_שניה/
- repo source [1] מרצדס CLS דור 2 (2011-2018) - מפרט טכני | iCar (catalog) — https://www.icar.co.il/מרצדס/מרצדס_CLS/מרצדס_CLS_דור_2_יד_שניה/
- repo source [2] מרצדס CLS החדשה 2018 בישראל - מחיר החל מ- 720,000 שקל | Cartube (editorial) — https://www.cartube.co.il/חדשות-רכב/מרצדס-cls-החדשה-2018-בישראל-מחיר-החל-מ-720-000-שקל
- repo source [3] מרצדס CLS 350 החדשה בישראל - מחיר החל מ- 669,000 שקל | Cartube (editorial) — https://www.cartube.co.il/חדשות-רכב/מרצדס-cls-350-החדשה-בישראל-מחיר-החל-מ-669-000-שקל
- repo source [4] מרצדס CLS חדשה בישראל - Gear.co.il (editorial) — https://www.gear.co.il/חדשות_רכב/מרצדס-cls-חדשה-בישראל

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2005-2010; body=Coupe; fuel=petrol; engine=3.5L v6; displacement=3.5; hp=272; trans=7-speed automatic; drive=RWD; sources=[1770] | Historical CLS rows; keep closed through 2023. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2005-2010; body=Coupe; fuel=petrol; engine=3.5L v6; displacement=3.5; hp=272; trans=7-speed automatic; drive=RWD; sources=[1770] | KEEP HISTORICAL |
| 2 | trim=None; years=2011-2014; body=Coupe; fuel=petrol; engine=3.5L v6; displacement=3.5; hp=306; trans=7-speed automatic; drive=RWD; sources=[1771] | Historical CLS rows; keep closed through 2023. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2011-2014; body=Coupe; fuel=petrol; engine=3.5L v6; displacement=3.5; hp=306; trans=7-speed automatic; drive=RWD; sources=[1771] | KEEP HISTORICAL |
| 3 | trim=None; years=2014-2018; body=Coupe; fuel=petrol; engine=3.0L v6 twin-turbo; displacement=3.0; hp=333; trans=9-speed automatic; drive=RWD; sources=[1771] | Historical CLS rows; keep closed through 2023. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2014-2018; body=Coupe; fuel=petrol; engine=3.0L v6 twin-turbo; displacement=3.0; hp=333; trans=9-speed automatic; drive=RWD; sources=[1771] | KEEP HISTORICAL |
| 4 | trim=None; years=2019-2023; body=Coupe; fuel=mild_hybrid; engine=2.0L inline-4 turbo; displacement=2.0; hp=299; trans=9-speed automatic; drive=RWD; sources=[1773] | Historical CLS rows; keep closed through 2023. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2019-2023; body=Coupe; fuel=mild_hybrid; engine=2.0L inline-4 turbo; displacement=2.0; hp=299; trans=9-speed automatic; drive=RWD; sources=[1773] | KEEP HISTORICAL |
| 5 | trim=None; years=2018-2023; body=Coupe; fuel=mild_hybrid; engine=3.0L inline-6 turbo; displacement=3.0; hp=367; trans=9-speed automatic; drive=AWD; sources=[1772] | Historical CLS rows; keep closed through 2023. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2018-2023; body=Coupe; fuel=mild_hybrid; engine=3.0L inline-6 turbo; displacement=3.0; hp=367; trans=9-speed automatic; drive=AWD; sources=[1772] | KEEP HISTORICAL |
| 6 | trim=None; years=2018-2023; body=Coupe; fuel=mild_hybrid; engine=3.0L inline-6 twin-turbo; displacement=3.0; hp=435; trans=9-speed automatic; drive=AWD; sources=[1774] | Historical CLS rows; keep closed through 2023. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2018-2023; body=Coupe; fuel=mild_hybrid; engine=3.0L inline-6 twin-turbo; displacement=3.0; hp=435; trans=9-speed automatic; drive=AWD; sources=[1774] | KEEP HISTORICAL |

---

## MODEL: IL-confirmed|Mercedes-Benz|E-Class
CURRENT VALUE: clean profile with 8 technical variants; profile years=2009-2024.

PROBLEM: Official Israel page supports current E 200, E 300 e and E 450. Existing 2024 E200/E300e rows should be extended/currentized only if exact technical fields are grounded. Add E450 only with embedded/repo-local exact fields. Historical E200/E220d/E300 rows should remain closed.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס E קלאס החדשה 2024 בישראל - מחיר החל מ-539,900 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-e-%D7%A7%D7%9C%D7%90%D7%A1-%D7%94%D7%97%D7%93%D7%A9%D7%94-2024-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-539900-%D7%A9%D7%A7%D7%9C
- repo source [1] מרצדס E קלאס החדשה (מתיחת פנים) בישראל - מחיר החל מ-509,900 שקלים (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-e-%D7%A7%D7%9C%D7%90%D7%A1-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%9E%D7%AA%D7%99%D7%97%D7%AA-%D7%A4%D7%A0%D7%99%D7%9D-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-509900-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D
- repo source [2] מרצדס E קלאס החדשה 2016 בישראל - מחיר החל מ-465,000 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-e-%D7%A7%D7%9C%D7%90%D7%A1-%D7%94%D7%97%D7%93%D7%A9%D7%94-2016-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-465000-%D7%A9%D7%A7%D7%9C
- repo source [3] מרצדס E קלאס קופה החדשה בישראל - מחיר החל מ-505,000 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-e-%D7%A7%D7%9C%D7%90%D7%A1-%D7%A7%D7%95%D7%A4%D7%94-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-505000-%D7%A9%D7%A7%D7%9C
- repo source [4] מרצדס E קלאס (2009-2016) מפרט טכני (specs) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_E_%D7%A7%D7%9C%D7%90%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_E_%D7%A7%D7%9C%D7%90%D7%A1_%D7%97%D7%93%D7%A9%D7%94_2009/
- repo source [5] מרצדס E קלאס חדשה - מחירון רכב, מבחן דרכים ומפרט טכני (specs) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_E_%D7%A7%D7%9C%D7%90%D7%A1/

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='E 200'; years=2024-2024; body=Sedan; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=204; trans=9-speed automatic; drive=RWD; sources=[1744, 1749] | Current E-Class rows closed at 2024; official current E-Class page lists E200/E300e/E450. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='E 200'; years=2024-2026; body=Sedan; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=204; trans=9-speed automatic; drive=RWD; sources=[1744, 1749] | FIX |
| 2 | trim='E 300 e'; years=2024-2024; body=Sedan; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=313; trans=9-speed automatic; drive=RWD; sources=[1744, 1749] | Current E-Class rows closed at 2024; official current E-Class page lists E200/E300e/E450. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='E 300 e'; years=2024-2026; body=Sedan; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=313; trans=9-speed automatic; drive=RWD; sources=[1744, 1749] | FIX |
| 3 | trim='E 200'; years=2020-2023; body=Sedan; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=197; trans=9-speed automatic; drive=RWD; sources=[1745, 1749] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='E 200'; years=2020-2023; body=Sedan; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=197; trans=9-speed automatic; drive=RWD; sources=[1745, 1749] | KEEP HISTORICAL |
| 4 | trim='E 300 e'; years=2020-2023; body=Sedan; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=320; trans=9-speed automatic; drive=RWD; sources=[1745, 1749] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='E 300 e'; years=2020-2023; body=Sedan; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=320; trans=9-speed automatic; drive=RWD; sources=[1745, 1749] | KEEP HISTORICAL |
| 5 | trim='E 200'; years=2016-2020; body=Sedan; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=184; trans=9-speed automatic; drive=RWD; sources=[1746, 1749] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='E 200'; years=2016-2020; body=Sedan; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=184; trans=9-speed automatic; drive=RWD; sources=[1746, 1749] | KEEP HISTORICAL |
| 6 | trim='E 220 d'; years=2016-2020; body=Sedan; fuel=diesel; engine=2.0L turbo; displacement=2.0; hp=194; trans=9-speed automatic; drive=RWD; sources=[1746, 1749] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='E 220 d'; years=2016-2020; body=Sedan; fuel=diesel; engine=2.0L turbo; displacement=2.0; hp=194; trans=9-speed automatic; drive=RWD; sources=[1746, 1749] | KEEP HISTORICAL |
| 7 | trim='E 300'; years=2017-2020; body=Coupe; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=245; trans=9-speed automatic; drive=RWD; sources=[1747, 1749] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='E 300'; years=2017-2020; body=Coupe; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=245; trans=9-speed automatic; drive=RWD; sources=[1747, 1749] | KEEP HISTORICAL |
| 8 | trim='E 200 CGI'; years=2009-2016; body=Sedan; fuel=petrol; engine=1.8L turbo; displacement=1.8; hp=184; trans=7-speed automatic; drive=RWD; sources=[1748, 1749] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='E 200 CGI'; years=2009-2016; body=Sedan; fuel=petrol; engine=1.8L turbo; displacement=1.8; hp=184; trans=7-speed automatic; drive=RWD; sources=[1748, 1749] | KEEP HISTORICAL |

MODEL-LEVEL ADD/FIX: Add/keep current E 450 4Matic only if all required fields are grounded by embedded/repo-local source; otherwise note missing current E450 in non-blocking review.

---

## MODEL: IL-confirmed|Mercedes-Benz|EQA
CURRENT VALUE: clean profile with 2 technical variants; profile years=2021-2025.

PROBLEM: Official current EQA FL supports EQA 250 Plus. Existing EQA 250/250+ should be currentized to 2026 if supported; EQA 350 4MATIC should not be extended beyond supported years if it is not listed in current official source. EV schema is already close: displacement null and single_speed/FWD or AWD.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס EQA בישראל - מחיר החל מ-289,900 שקלים (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-eqa-%D7%94%D7%97%D7%A9%D7%9E%D7%9C%D7%99-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-289,900-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D
- repo source [1] 2024 מרצדס EQA ו- EQB מתוחי פנים בישראל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/2024-%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-eqa-%D7%95-eqb-%D7%94%D7%97%D7%93%D7%A9%D7%99%D7%9D-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-319,900-%D7%A9%D7%A7%D7%9C
- repo source [2] מרצדס EQA - מחירון, מפרט טכני (catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_EQA/

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='250 / 250+'; years=2021-2025; body=SUV; fuel=electric; engine=electric; displacement=None; hp=190; trans=single_speed; drive=FWD; sources=[0, 1, 2] | EQA 250 Plus FL current; row currently ends 2025. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='250 / 250+'; years=2021-2026; body=SUV; fuel=electric; engine=electric; displacement=None; hp=190; trans=single_speed; drive=FWD; sources=[0, 1, 2] | FIX |
| 2 | trim='350 4MATIC'; years=2022-2025; body=SUV; fuel=electric; engine=electric; displacement=None; hp=292; trans=single_speed; drive=AWD; sources=[1, 2] | EQA 350 4MATIC not proven as current official line; do not extend beyond supported years without repo-local evidence. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='350 4MATIC'; years=2022-2025; body=SUV; fuel=electric; engine=electric; displacement=None; hp=292; trans=single_speed; drive=AWD; sources=[1, 2] | KEEP / REVIEW CURRENT |

---

## MODEL: IL-confirmed|Mercedes-Benz|EQB
CURRENT VALUE: clean profile with 2 technical variants; profile years=2022-2026.

PROBLEM: Official models page supports current EQB. Existing rows must keep valid EV schema. Because local sources disagree on EQB hp/naming, do not fabricate; keep only exact rows supported by repo-local/embedded sources and move ambiguous horsepower/trim rows to non-blocking review.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס EQB 2024 החדש - מחירון, מפרט, תמונות | iCar (specs_database) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_EQB/
- repo source [1] מרצדס EQB החשמלי בישראל - מחיר החל מ- 349,900 שקל - cartube (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-eqb-%D7%94%D7%97%D7%A9%D7%9E%D7%9C%D7%99-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-349,900-%D7%A9%D7%A7%D7%9C
- repo source [2] Mercedes-Benz EQB Overview (official_importer) — https://www.mercedes-benz.co.il/passengercars/models/suv/eqb/overview.html

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2022-2026; body=SUV; fuel=electric; engine=electric; displacement=None; hp=228; trans=single_speed; drive=AWD; sources=[0, 1, 2] | EQB current is supported, but local sources differ on hp/naming; keep only exactly grounded rows. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2022-2026; body=SUV; fuel=electric; engine=electric; displacement=None; hp=228; trans=single_speed; drive=AWD; sources=[0, 1, 2] | KEEP / REVIEW AMBIGUOUS HP |
| 2 | trim=None; years=2023-2026; body=SUV; fuel=electric; engine=electric; displacement=None; hp=190; trans=single_speed; drive=FWD; sources=[0, 2] | EQB current is supported, but local sources differ on hp/naming; keep only exactly grounded rows. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2023-2026; body=SUV; fuel=electric; engine=electric; displacement=None; hp=190; trans=single_speed; drive=FWD; sources=[0, 2] | KEEP / REVIEW AMBIGUOUS HP |

---

## MODEL: IL-confirmed|Mercedes-Benz|EQC
CURRENT VALUE: clean profile with 1 technical variants; profile years=2020-2023.

PROBLEM: EQC is historical in Israel and should remain closed at 2023. Do not extend to current.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס EQC - מחירון, מפרט טכני, חוות דעת - iCar (israeli_catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_EQC/
- repo source [1] מרצדס EQC בישראל – מחיר החל מ-499,900 שקל - Cartube (israeli_editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-eqc-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-499,900-%D7%A9%D7%A7%D7%9C

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='400 4MATIC'; years=2020-2023; body=SUV; fuel=electric; engine=electric; displacement=None; hp=408; trans=single_speed; drive=AWD; sources=[0, 1] | Historical EQC; keep closed at 2023. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='400 4MATIC'; years=2020-2023; body=SUV; fuel=electric; engine=electric; displacement=None; hp=408; trans=single_speed; drive=AWD; sources=[0, 1] | KEEP HISTORICAL |

---

## MODEL: IL-confirmed|Mercedes-Benz|EQS
CURRENT VALUE: clean profile with 5 technical variants; profile years=2021-2024.

PROBLEM: This profile incorrectly mixes EQS liftback/sedan rows with EQS SUV rows while a separate EQS SUV profile exists. Keep sedan/liftback EQS 450+/580/AMG rows here only; move/merge SUV rows into IL-confirmed Mercedes-Benz EQS SUV with lineage. Do not leave duplicate EQS SUV rows in both profiles.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס EQS החשמלית בישראל - מחיר החל מ- 890,000 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-eqs-%D7%94%D7%97%D7%A9%D7%9E%D7%9C%D7%99%D7%AA-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-890,000-%D7%A9%D7%A7%D7%9C
- repo source [1] מרצדס EQS 53 AMG נחתה בישראל - מחיר החל מ- 1.35 מיליון שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-eqs-53-amg-%D7%A0%D7%97%D7%AA%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1-35-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C
- repo source [2] מרצדס EQS SUV בישראל - מחיר החל מ- 990,000 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-eqs-suv-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-990,000-%D7%A9%D7%A7%D7%9C
- repo source [3] מרצדס EQS - מחירון, מפרטים, ואביזרים (catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_EQS/
- repo source [4] מרצדס EQS SUV - מחירון, מפרטים, ואביזרים (catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_EQS_SUV/

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='450+'; years=2021-2024; body=Liftback; fuel=electric; engine=electric; displacement=None; hp=333; trans=single_speed; drive=RWD; sources=[0, 3] | EQS sedan/liftback row; keep as sedan/liftback, do not mix with SUV. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='450+'; years=2021-2024; body=Liftback; fuel=electric; engine=electric; displacement=None; hp=333; trans=single_speed; drive=RWD; sources=[0, 3] | KEEP HISTORICAL |
| 2 | trim='580 4MATIC'; years=2021-2024; body=Liftback; fuel=electric; engine=electric; displacement=None; hp=523; trans=single_speed; drive=AWD; sources=[0, 3] | EQS sedan/liftback row; keep as sedan/liftback, do not mix with SUV. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='580 4MATIC'; years=2021-2024; body=Liftback; fuel=electric; engine=electric; displacement=None; hp=523; trans=single_speed; drive=AWD; sources=[0, 3] | KEEP HISTORICAL |
| 3 | trim='AMG 53 4MATIC+'; years=2022-2024; body=Liftback; fuel=electric; engine=electric; displacement=None; hp=658; trans=single_speed; drive=AWD; sources=[1, 3] | EQS sedan/liftback row; keep as sedan/liftback, do not mix with SUV. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='AMG 53 4MATIC+'; years=2022-2024; body=Liftback; fuel=electric; engine=electric; displacement=None; hp=658; trans=single_speed; drive=AWD; sources=[1, 3] | KEEP HISTORICAL |
| 4 | trim='450 4MATIC'; years=2023-2024; body=SUV; fuel=electric; engine=electric; displacement=None; hp=360; trans=single_speed; drive=AWD; sources=[2, 4] | SUV row belongs to EQS SUV profile, not generic/sedan EQS. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | Move/merge this SUV variant into IL-confirmed/Mercedes-Benz/EQS SUV with lineage; remove duplicate from EQS sedan/liftback profile. | MOVE / MERGE |
| 5 | trim='580 4MATIC'; years=2023-2024; body=SUV; fuel=electric; engine=electric; displacement=None; hp=544; trans=single_speed; drive=AWD; sources=[2, 4] | SUV row belongs to EQS SUV profile, not generic/sedan EQS. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | Move/merge this SUV variant into IL-confirmed/Mercedes-Benz/EQS SUV with lineage; remove duplicate from EQS sedan/liftback profile. | MOVE / MERGE |

---

## MODEL: IL-confirmed|Mercedes-Benz|EQS SUV
CURRENT VALUE: clean profile with 2 technical variants; profile years=2023-2024.

PROBLEM: Official Israel page supports current EQS SUV 450 and 580 trims. This profile should own the SUV rows. Extend/currentize to 2026 where supported and merge SUV variants moved out of generic EQS.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס EQS SUV בישראל - מחיר החל מ- 990,000 שקל (editorial) — https://www.cartube.co.il/%חדשות-רכב/מרצדס-eqs-suv-בישראל-מחיר-החל-מ-990-000-שקל
- repo source [1] מרצדס EQS SUV - מחירון, מפרט טכני וחוות דעת (catalog) — https://www.auto.co.il/model/mercedes-eqs-suv_g1445

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='EQS 450 4MATIC'; years=2023-2024; body=SUV; fuel=electric; engine=electric; displacement=None; hp=360; trans=single_speed; drive=AWD; sources=[0, 1] | Official current EQS SUV page supports 450/580; this profile should own all SUV variants. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='EQS 450 4MATIC'; years=2023-2026; body=SUV; fuel=electric; engine=electric; displacement=None; hp=360; trans=single_speed; drive=AWD; sources=[0, 1] | FIX / MERGE SUV ROWS |
| 2 | trim='EQS 580 4MATIC'; years=2023-2024; body=SUV; fuel=electric; engine=electric; displacement=None; hp=544; trans=single_speed; drive=AWD; sources=[0, 1] | Official current EQS SUV page supports 450/580; this profile should own all SUV variants. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='EQS 580 4MATIC'; years=2023-2026; body=SUV; fuel=electric; engine=electric; displacement=None; hp=544; trans=single_speed; drive=AWD; sources=[0, 1] | FIX / MERGE SUV ROWS |

---

## MODEL: IL-confirmed|Mercedes-Benz|EQV
CURRENT VALUE: clean profile with 1 technical variants; profile years=2021-2024.

PROBLEM: Official Mercedes-Benz vans Israel page and Israeli sources support current EQV electric 204 hp FWD. Fix EV schema: engine_displacement_l=null and transmission should be single_speed/direct_drive according to schema, not generic automatic. Do not close at 2024 if current official vans page supports it.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס EQV - מחירון, מפרט טכני (catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_EQV/
- repo source [1] מרצדס EQV החשמלי בישראל - מחיר החל מ- 600,000 שקלים (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-eqv-%D7%94%D7%97%D7%A9%D7%9E%D7%9C%D7%99-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-600000-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D
- repo source [2] MERCEDES-BENZ-EQV-300 (official_importer_pdf) — https://mercedes-benz-vans.co.il/wp-content/uploads/2022/01/MERCEDES-BENZ-EQV-300-1-6-1.pdf

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='300 Avantgarde'; years=2021-2024; body=MPV; fuel=electric; engine=electric; displacement=None; hp=204; trans=automatic; drive=FWD; sources=[0, 1, 2] | EV row uses generic automatic and is closed at 2024 despite official current EQV vans page. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='300 Avantgarde'; years=2021-2026; body=MPV; fuel=electric; engine=electric; displacement=None; hp=204; trans=single_speed; drive=FWD; sources=[0, 1, 2] | FIX |

---

## MODEL: IL-confirmed|Mercedes-Benz|G-Class
CURRENT VALUE: clean profile with 3 technical variants; profile years=2018-2024.

PROBLEM: Official current G-Class lineup is G 450 d, G 500 and AMG G 63. Keep historical G350d only through supported years; add/update current G450d if exact fields are available. Extend G500/G63 to current only if specs are grounded.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] Mercedes-Benz G-Class G 500 & G 63 AMG Specs - Colmobil Israel (official_importer) — https://mercedes-benz.co.il/models/g-class/
- repo source [1] Mercedes G-Class 350 d 2019-2023 Specifications - Cartube / Icar (editorial_catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/G_%D7%A7%D7%9C%D7%90%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_G_%D7%A7%D7%9C%D7%90%D7%A1_%D7%97%D7%93%D7%A9/
- repo source [2] Mercedes G-Class 2018 Launch in Israel (editorial_article) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-g-%D7%A7%D7%9C%D7%90%D7%A1-%D7%94%D7%97%D7%93%D7%A9-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1-18-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='G 350 d'; years=2019-2024; body=SUV; fuel=diesel; engine=3.0L turbo; displacement=2.9; hp=286; trans=9-speed automatic; drive=4WD; sources=[1] | Current official diesel is G 450 d, not G 350 d. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='G 350 d'; years=2019-2024; body=SUV; fuel=diesel; engine=3.0L turbo; displacement=2.9; hp=286; trans=9-speed automatic; drive=4WD; sources=[1] | KEEP HISTORICAL / ADD CURRENT G450d IF GROUNDED |
| 2 | trim='G 500'; years=2018-2024; body=SUV; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=422; trans=9-speed automatic; drive=4WD; sources=[0, 1, 2] | Official current G-Class supports G500 and AMG G63; do not leave current rows closed at 2024 if exact specs are grounded. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='G 500'; years=2018-2026; body=SUV; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=422; trans=9-speed automatic; drive=4WD; sources=[0, 1, 2] | FIX CURRENT YEAR IF GROUNDED |
| 3 | trim='Mercedes-AMG G 63'; years=2018-2024; body=SUV; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=585; trans=9-speed automatic; drive=4WD; sources=[0, 1, 2] | Official current G-Class supports G500 and AMG G63; do not leave current rows closed at 2024 if exact specs are grounded. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='Mercedes-AMG G 63'; years=2018-2026; body=SUV; fuel=petrol; engine=4.0L v8 twin-turbo; displacement=4.0; hp=585; trans=9-speed automatic; drive=4WD; sources=[0, 1, 2] | FIX CURRENT YEAR IF GROUNDED |

MODEL-LEVEL ADD/FIX: Add/replace current diesel as G 450 d only if exact fields are grounded. Do not relabel G350d to G450d without preserving historical lineage.

---

## MODEL: IL-confirmed|Mercedes-Benz|GLA
CURRENT VALUE: clean profile with 6 technical variants; profile years=2014-2024.

PROBLEM: Official models page supports current GLA. Null trims are weak; normalize to GLA 200/GLA 250 4MATIC/GLA 250 e or equivalent where supported by row fields/sources. Do not extend every historical row just because the model exists.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס GLA עד 2020 - מפרט טכני (specs_catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_GLA_%D7%A2%D7%93_2020/
- repo source [1] מרצדס GLA מפרט טכני (דור שני) (specs_catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_GLA/
- repo source [2] מרצדס GLA החדש 2020 בישראל - מחיר החל מ-289,900 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-gla-%D7%94%D7%97%D7%93%D7%A9-2020-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-289-900-%D7%A9%D7%A7%D7%9C
- repo source [3] מרצדס GLA 250e פלאג-אין בישראל - מחיר החל מ-324,900 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-gla-250e-%D7%A4%D7%9C%D7%90%D7%92-%D7%90%D7%99%D7%9F-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-324900-%D7%A9%D7%A7%D7%9C
- repo source [4] מרצדס GLA החדש 2024 בישראל - מחיר החל מ- 359,900 שקל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-gla-%D7%94%D7%97%D7%93%D7%A9-2024-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-359900-%D7%A9%D7%A7%D7%9C

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2014-2020; body=SUV; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=156; trans=7-speed dual_clutch; drive=FWD; sources=[1] | Null trims are weak; current GLA exists but only exact current variants should extend. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2014-2020; body=SUV; fuel=petrol; engine=1.6L turbo; displacement=1.6; hp=156; trans=7-speed dual_clutch; drive=FWD; sources=[1] | FIX TRIM / CURRENT YEAR IF GROUNDED |
| 2 | trim=None; years=2014-2020; body=SUV; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=211; trans=7-speed dual_clutch; drive=AWD; sources=[1] | Null trims are weak; current GLA exists but only exact current variants should extend. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2014-2020; body=SUV; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=211; trans=7-speed dual_clutch; drive=AWD; sources=[1] | FIX TRIM / CURRENT YEAR IF GROUNDED |
| 3 | trim=None; years=2020-2023; body=SUV; fuel=petrol; engine=1.33L turbo; displacement=1.33; hp=163; trans=7-speed dual_clutch; drive=FWD; sources=[2, 3] | Null trims are weak; current GLA exists but only exact current variants should extend. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2020-2023; body=SUV; fuel=petrol; engine=1.33L turbo; displacement=1.33; hp=163; trans=7-speed dual_clutch; drive=FWD; sources=[2, 3] | FIX TRIM / CURRENT YEAR IF GROUNDED |
| 4 | trim=None; years=2020-2023; body=SUV; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=224; trans=8-speed dual_clutch; drive=AWD; sources=[2, 3] | Null trims are weak; current GLA exists but only exact current variants should extend. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2020-2023; body=SUV; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=224; trans=8-speed dual_clutch; drive=AWD; sources=[2, 3] | FIX TRIM / CURRENT YEAR IF GROUNDED |
| 5 | trim=None; years=2020-2024; body=SUV; fuel=plug_in_hybrid; engine=1.33L turbo; displacement=1.33; hp=218; trans=8-speed dual_clutch; drive=FWD; sources=[2, 4, 5] | Null trims are weak; current GLA exists but only exact current variants should extend. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2020-2024; body=SUV; fuel=plug_in_hybrid; engine=1.33L turbo; displacement=1.33; hp=218; trans=8-speed dual_clutch; drive=FWD; sources=[2, 4, 5] | FIX TRIM / CURRENT YEAR IF GROUNDED |
| 6 | trim=None; years=2024-2024; body=SUV; fuel=mild_hybrid; engine=1.33L turbo; displacement=1.33; hp=163; trans=7-speed dual_clutch; drive=FWD; sources=[5] | Null trims are weak; current GLA exists but only exact current variants should extend. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2024-2024; body=SUV; fuel=mild_hybrid; engine=1.33L turbo; displacement=1.33; hp=163; trans=7-speed dual_clutch; drive=FWD; sources=[5] | FIX TRIM / CURRENT YEAR IF GROUNDED |

---

## MODEL: IL-confirmed|Mercedes-Benz|GLB
CURRENT VALUE: clean profile with 6 technical variants; profile years=2020-2024.

PROBLEM: Official models page supports current GLB. Current 2024 mild-hybrid rows may be extended if exact variants still listed; historical 2020-2023 petrol rows stay closed. Preserve GLB 200, GLB 250 4MATIC and AMG GLB 35 lineage.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס GLB נוחת בישראל - מחיר החל מ- 289,900 שקל - cartube (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-glb-%D7%A0%D7%95%D7%97%D7%AA-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-289,900-%D7%A9%D7%A7%D7%9C
- repo source [1] מרצדס GLB - מחירון, מפרטים, אמינות וחוות דעת - iCar (catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_GLB/
- repo source [2] דגמי 2024 המחודשים של מרצדס GLB בישראל - cartube (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%93%D7%92%D7%9E%D7%99-2024-%D7%94%D7%9E%D7%97%D7%95%D7%93%D7%A9%D7%99%D7%9D-%D7%A9%D7%9C-%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-glb-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='GLB 200'; years=2020-2023; body=SUV; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=163; trans=7-speed dual_clutch; drive=FWD; sources=[0, 1] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='GLB 200'; years=2020-2023; body=SUV; fuel=petrol; engine=1.3L turbo; displacement=1.3; hp=163; trans=7-speed dual_clutch; drive=FWD; sources=[0, 1] | KEEP HISTORICAL |
| 2 | trim='GLB 250 4MATIC'; years=2020-2023; body=SUV; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=224; trans=8-speed dual_clutch; drive=AWD; sources=[0, 1] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='GLB 250 4MATIC'; years=2020-2023; body=SUV; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=224; trans=8-speed dual_clutch; drive=AWD; sources=[0, 1] | KEEP HISTORICAL |
| 3 | trim='AMG GLB 35 4MATIC'; years=2021-2023; body=SUV; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=306; trans=8-speed dual_clutch; drive=AWD; sources=[1] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='AMG GLB 35 4MATIC'; years=2021-2023; body=SUV; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=306; trans=8-speed dual_clutch; drive=AWD; sources=[1] | KEEP HISTORICAL |
| 4 | trim='GLB 200'; years=2024-2024; body=SUV; fuel=mild_hybrid; engine=1.3L turbo; displacement=1.3; hp=163; trans=7-speed dual_clutch; drive=FWD; sources=[1, 2] | Current GLB exists; exact 2024 mild-hybrid rows may extend if supported. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='GLB 200'; years=2024-2026; body=SUV; fuel=mild_hybrid; engine=1.3L turbo; displacement=1.3; hp=163; trans=7-speed dual_clutch; drive=FWD; sources=[1, 2] | FIX CURRENT YEAR IF GROUNDED |
| 5 | trim='GLB 250 4MATIC'; years=2024-2024; body=SUV; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=224; trans=8-speed dual_clutch; drive=AWD; sources=[1, 2] | Current GLB exists; exact 2024 mild-hybrid rows may extend if supported. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='GLB 250 4MATIC'; years=2024-2026; body=SUV; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=224; trans=8-speed dual_clutch; drive=AWD; sources=[1, 2] | FIX CURRENT YEAR IF GROUNDED |
| 6 | trim='AMG GLB 35 4MATIC'; years=2024-2024; body=SUV; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=306; trans=8-speed dual_clutch; drive=AWD; sources=[1, 2] | Current GLB exists; exact 2024 mild-hybrid rows may extend if supported. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='AMG GLB 35 4MATIC'; years=2024-2026; body=SUV; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=306; trans=8-speed dual_clutch; drive=AWD; sources=[1, 2] | FIX CURRENT YEAR IF GROUNDED |

---

## MODEL: IL-confirmed|Mercedes-Benz|GLC
CURRENT VALUE: clean profile with 10 technical variants; profile years=2015-2025.

PROBLEM: Official GLC SUV/Coupé pages support current GLC 200 4Matic, GLC 300 4Matic, GLC 300 e 4Matic, AMG GLC 53 and GLC Coupé 300e. Null trim current rows are not acceptable; normalize trim names. Add/fix missing current GLC 300 row if source-grounded.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס GLC - מפרט טכני (official_importer) — https://mercedes-benz.co.il/models/glc-suv/
- repo source [1] מרצדס GLC - מחירון, מפרטים, אמינות (specs_catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_GLC/
- repo source [2] מרצדס GLC קופה החדש 2023 בישראל (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-glc-%D7%A7%D7%95%D7%A4%D7%94-%D7%94%D7%97%D7%93%D7%A9-2023-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-499,900-%D7%A9%D7%A7%D7%9C

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2015-2019; body=SUV; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=211; trans=9-speed automatic; drive=AWD; sources=[1] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2015-2019; body=SUV; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=211; trans=9-speed automatic; drive=AWD; sources=[1] | KEEP HISTORICAL |
| 2 | trim=None; years=2016-2019; body=Coupe; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=211; trans=9-speed automatic; drive=AWD; sources=[1] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2016-2019; body=Coupe; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=211; trans=9-speed automatic; drive=AWD; sources=[1] | KEEP HISTORICAL |
| 3 | trim=None; years=2016-2019; body=SUV; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=320; trans=7-speed automatic; drive=AWD; sources=[1] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2016-2019; body=SUV; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=320; trans=7-speed automatic; drive=AWD; sources=[1] | KEEP HISTORICAL |
| 4 | trim=None; years=2019-2022; body=SUV; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=320; trans=9-speed automatic; drive=AWD; sources=[1] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2019-2022; body=SUV; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=320; trans=9-speed automatic; drive=AWD; sources=[1] | KEEP HISTORICAL |
| 5 | trim=None; years=2022-2025; body=SUV; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=313; trans=9-speed automatic; drive=AWD; sources=[0, 1] | Official current GLC SUV/Coupé pages support current trims; null trims must be normalized. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2022-2026; body=SUV; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=313; trans=9-speed automatic; drive=AWD; sources=[0, 1]; set marketed version_or_trim based on hp/body/fuel (GLC 200/300/300e/AMG 53, Coupe when body=Coupe). | FIX TRIM / CURRENT YEAR |
| 6 | trim=None; years=2019-2025; body=SUV; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=258; trans=9-speed automatic; drive=AWD; sources=[0, 1] | Official current GLC SUV/Coupé pages support current trims; null trims must be normalized. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2019-2026; body=SUV; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=258; trans=9-speed automatic; drive=AWD; sources=[0, 1]; set marketed version_or_trim based on hp/body/fuel (GLC 200/300/300e/AMG 53, Coupe when body=Coupe). | FIX TRIM / CURRENT YEAR |
| 7 | trim=None; years=2019-2025; body=Coupe; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=258; trans=9-speed automatic; drive=AWD; sources=[1, 2] | Official current GLC SUV/Coupé pages support current trims; null trims must be normalized. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2019-2026; body=Coupe; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=258; trans=9-speed automatic; drive=AWD; sources=[1, 2]; set marketed version_or_trim based on hp/body/fuel (GLC 200/300/300e/AMG 53, Coupe when body=Coupe). | FIX TRIM / CURRENT YEAR |
| 8 | trim=None; years=2022-2025; body=SUV; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=204; trans=9-speed automatic; drive=AWD; sources=[0, 1] | Official current GLC SUV/Coupé pages support current trims; null trims must be normalized. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2022-2026; body=SUV; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=204; trans=9-speed automatic; drive=AWD; sources=[0, 1]; set marketed version_or_trim based on hp/body/fuel (GLC 200/300/300e/AMG 53, Coupe when body=Coupe). | FIX TRIM / CURRENT YEAR |
| 9 | trim=None; years=2023-2025; body=Coupe; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=204; trans=9-speed automatic; drive=AWD; sources=[2] | Official current GLC SUV/Coupé pages support current trims; null trims must be normalized. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2023-2026; body=Coupe; fuel=mild_hybrid; engine=2.0L turbo; displacement=2.0; hp=204; trans=9-speed automatic; drive=AWD; sources=[2]; set marketed version_or_trim based on hp/body/fuel (GLC 200/300/300e/AMG 53, Coupe when body=Coupe). | FIX TRIM / CURRENT YEAR |
| 10 | trim=None; years=2023-2025; body=Coupe; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=313; trans=9-speed automatic; drive=AWD; sources=[2] | Official current GLC SUV/Coupé pages support current trims; null trims must be normalized. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2023-2026; body=Coupe; fuel=plug_in_hybrid; engine=2.0L turbo; displacement=2.0; hp=313; trans=9-speed automatic; drive=AWD; sources=[2]; set marketed version_or_trim based on hp/body/fuel (GLC 200/300/300e/AMG 53, Coupe when body=Coupe). | FIX TRIM / CURRENT YEAR |

MODEL-LEVEL ADD/FIX: Add missing GLC 300 4Matic and AMG GLC 53 rows if exact fields are grounded by embedded/repo-local sources; otherwise create non-blocking review entries for missing current variants.

---

## MODEL: IL-confirmed|Mercedes-Benz|GLK
CURRENT VALUE: clean profile with 5 technical variants; profile years=2009-2015.

PROBLEM: GLK is historical 2009-2015; keep as historical. Do not extend to GLC or current Mercedes SUV lines.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס GLK - מחירון, מפרטים וחוות דעת | iCar (israeli_catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_GLK/
- repo source [1] מרצדס GLK (2009 - 2015) - מפרט טכני, מחירון וחוות דעת | אוטו (israeli_catalog) — https://www.auto.co.il/model/mercedes-benz-glk_g327

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='GLK 220 CDI 4MATIC'; years=2009-2015; body=SUV; fuel=diesel; engine=2.1L turbo; displacement=2.1; hp=170; trans=7-speed automatic; drive=AWD; sources=[0, 1] | Historical GLK; keep 2009-2015 only. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='GLK 220 CDI 4MATIC'; years=2009-2015; body=SUV; fuel=diesel; engine=2.1L turbo; displacement=2.1; hp=170; trans=7-speed automatic; drive=AWD; sources=[0, 1] | KEEP HISTORICAL |
| 2 | trim='GLK 300 4MATIC'; years=2009-2012; body=SUV; fuel=petrol; engine=3.0L v6; displacement=3.0; hp=231; trans=7-speed automatic; drive=AWD; sources=[0, 1] | Historical GLK; keep 2009-2015 only. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='GLK 300 4MATIC'; years=2009-2012; body=SUV; fuel=petrol; engine=3.0L v6; displacement=3.0; hp=231; trans=7-speed automatic; drive=AWD; sources=[0, 1] | KEEP HISTORICAL |
| 3 | trim='GLK 350 4MATIC'; years=2009-2012; body=SUV; fuel=petrol; engine=3.5L v6; displacement=3.5; hp=272; trans=7-speed automatic; drive=AWD; sources=[0, 1] | Historical GLK; keep 2009-2015 only. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='GLK 350 4MATIC'; years=2009-2012; body=SUV; fuel=petrol; engine=3.5L v6; displacement=3.5; hp=272; trans=7-speed automatic; drive=AWD; sources=[0, 1] | KEEP HISTORICAL |
| 4 | trim='GLK 350 4MATIC'; years=2012-2015; body=SUV; fuel=petrol; engine=3.5L v6; displacement=3.5; hp=306; trans=7-speed automatic; drive=AWD; sources=[0, 1] | Historical GLK; keep 2009-2015 only. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='GLK 350 4MATIC'; years=2012-2015; body=SUV; fuel=petrol; engine=3.5L v6; displacement=3.5; hp=306; trans=7-speed automatic; drive=AWD; sources=[0, 1] | KEEP HISTORICAL |
| 5 | trim='GLK 250 4MATIC'; years=2013-2015; body=SUV; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=211; trans=7-speed automatic; drive=AWD; sources=[0, 1] | Historical GLK; keep 2009-2015 only. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='GLK 250 4MATIC'; years=2013-2015; body=SUV; fuel=petrol; engine=2.0L turbo; displacement=2.0; hp=211; trans=7-speed automatic; drive=AWD; sources=[0, 1] | KEEP HISTORICAL |

---

## MODEL: IL-confirmed|Mercedes-Benz|GLS
CURRENT VALUE: clean profile with 5 technical variants; profile years=2016-2024.

PROBLEM: Official models page supports current GLS. Existing current rows ending 2024 should not remain closed if exact current GLS variants are grounded. Null trims should be normalized to marketed names such as GLS 350d/400/450/580/450d where supported. Do not add unsupported AMG/Maybach rows here.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] מרצדס GLS 2016-2019 - מחירון רכב, מפרט טכני (editorial_catalog) — https://www.icar.co.il/mercedes-benz/gls/2016-2019/
- repo source [1] הדור החדש: 2020 מרצדס GLS החדש בישראל - מחיר החל מ- 1,150,000 שקלים (editorial_article) — https://www.cartube.co.il/חדשות-רכב/הדור-החדש-2020-מרצדס-gls-החדש-בישראל
- repo source [2] מרצדס GLS החדש - מפרט טכני (editorial_catalog) — https://gear.co.il/mercedes_benz-gls_class
- repo source [3] מרצדס GLS - מחירון רכב, מפרט טכני (editorial_catalog) — https://www.icar.co.il/mercedes-benz/gls/new/

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim=None; years=2016-2019; body=SUV; fuel=diesel; engine=3.0L v6 turbo; displacement=3.0; hp=258; trans=9-speed automatic; drive=AWD; sources=[0] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2016-2019; body=SUV; fuel=diesel; engine=3.0L v6 turbo; displacement=3.0; hp=258; trans=9-speed automatic; drive=AWD; sources=[0] | KEEP HISTORICAL / FIX TRIM IF POSSIBLE |
| 2 | trim=None; years=2016-2019; body=SUV; fuel=petrol; engine=3.0L v6 bi-turbo; displacement=3.0; hp=333; trans=9-speed automatic; drive=AWD; sources=[0] | Validate Israeli-market row and source grounding. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2016-2019; body=SUV; fuel=petrol; engine=3.0L v6 bi-turbo; displacement=3.0; hp=333; trans=9-speed automatic; drive=AWD; sources=[0] | KEEP HISTORICAL / FIX TRIM IF POSSIBLE |
| 3 | trim=None; years=2019-2024; body=SUV; fuel=mild_hybrid; engine=3.0L i6 turbo; displacement=3.0; hp=367; trans=9-speed automatic; drive=AWD; sources=[1, 2, 3] | Official current GLS exists; current rows should not remain closed at 2024 if exact variants are grounded; null trim weak. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2019-2026; body=SUV; fuel=mild_hybrid; engine=3.0L i6 turbo; displacement=3.0; hp=367; trans=9-speed automatic; drive=AWD; sources=[1, 2, 3]; set marketed GLS trim name if repo-local source supports it. | FIX TRIM / CURRENT YEAR IF GROUNDED |
| 4 | trim=None; years=2019-2024; body=SUV; fuel=mild_hybrid; engine=4.0L v8 bi-turbo; displacement=4.0; hp=489; trans=9-speed automatic; drive=AWD; sources=[1, 2, 3] | Official current GLS exists; current rows should not remain closed at 2024 if exact variants are grounded; null trim weak. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2019-2026; body=SUV; fuel=mild_hybrid; engine=4.0L v8 bi-turbo; displacement=4.0; hp=489; trans=9-speed automatic; drive=AWD; sources=[1, 2, 3]; set marketed GLS trim name if repo-local source supports it. | FIX TRIM / CURRENT YEAR IF GROUNDED |
| 5 | trim=None; years=2019-2024; body=SUV; fuel=diesel; engine=2.9L i6 turbo; displacement=2.9; hp=330; trans=9-speed automatic; drive=AWD; sources=[2, 3] | Official current GLS exists; current rows should not remain closed at 2024 if exact variants are grounded; null trim weak. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim=None; years=2019-2026; body=SUV; fuel=diesel; engine=2.9L i6 turbo; displacement=2.9; hp=330; trans=9-speed automatic; drive=AWD; sources=[2, 3]; set marketed GLS trim name if repo-local source supports it. | FIX TRIM / CURRENT YEAR IF GROUNDED |

---

## MODEL: IL-confirmed|Mercedes-Benz|Maybach GLS
CURRENT VALUE: clean profile with 1 technical variants; profile years=2020-2024.

PROBLEM: Official models page supports current GLS Maybach. Existing GLS 600 4MATIC 557 hp should be extended/currentized only if exact fields are supported; keep separate from regular GLS profile.

WEB-VALIDATED FACT: see RUN 4 source package above plus repo-local sources below.

SOURCE:
- repo source [0] בישראל: מרצדס מייבאך GLS 600 - מחיר החל מ-1.75 מיליון שקלים (editorial) — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%A8%D7%A6%D7%93%D7%A1-%D7%9E%D7%99%D7%99%D7%91%D7%90%D7%9A-gls-600-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-175-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D
- repo source [1] מרצדס מייבאך GLS - מחירון רכב, מבחני דרכים וחוות דעת (catalog) — https://www.icar.co.il/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1/%D7%9E%D7%A8%D7%A6%D7%93%D7%A1_%D7%9E%D7%99%D7%99%D7%91%D7%90%D7%9A_GLS/

TARGET VALUE: apply exact variant-level table below; preserve aliases/lineage when merging/reviewing/archiving.

ACTION: see table.

### Variant decision table

| # | CURRENT VALUE | PROBLEM | WEB-VALIDATED FACT | TARGET VALUE | ACTION |
|---:|---|---|---|---|---|
| 1 | trim='GLS 600 4MATIC'; years=2020-2024; body=SUV; fuel=mild_hybrid; engine=4.0L v8 twin-turbo; displacement=4.0; hp=557; trans=9-speed automatic; drive=AWD; sources=[0, 1] | Official current GLS Maybach listed; row should not remain closed at 2024 if exact fields are grounded. | Grounded by embedded Mercedes-Benz Israel / Israeli-market source package and repo-local sources listed below. | trim='GLS 600 4MATIC'; years=2020-2026; body=SUV; fuel=mild_hybrid; engine=4.0L v8 twin-turbo; displacement=4.0; hp=557; trans=9-speed automatic; drive=AWD; sources=[0, 1] | FIX CURRENT YEAR |


## Required checks after RUN 4 implementation

```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

Then audit actual generated files, not only console output:

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
Before final commit, delete codex_tasks/BATCH26_RUN4_*.md unless the user explicitly asks to keep them.
```

Do not claim PASS unless actual files and metrics prove the required RUN 4 end state.


# ==============================
# RUN5
# source: BATCH26_RUN5_VARIANT_LEVEL_CODEX_TASK.md
# ==============================

# BATCH26 RUN 5 — VARIANT-LEVEL CODEX TASK

## Non-negotiable execution rules
Do not browse the internet. All web-validation facts needed for RUN 5 are embedded here. Use this task file as the single source of truth for RUN 5 only.
Apply RUN 5 only. Do not apply RUN 1, RUN 2, RUN 3, RUN 4, RUN 6, RUN 7, FINAL blockers, or any unified batch task.
If repo-local evidence conflicts with this task file, report the conflict instead of guessing. If a variant cannot be grounded, move it to non-blocking review/archive with reason and lineage rather than fabricating clean data.
Temporary-file cleanup is mandatory: before final commit, delete `codex_tasks/BATCH26_RUN5_*.md` unless the user explicitly asks to keep it.

## Scope
RUN 5 scope: `IL-confirmed|Mercedes-Benz|R-Class` through `IL-confirmed|Mini|Cabrio`.
Profiles: 20. Technical variants: 74. Coverage: 74/74 variant-level decisions.

## Web/source anchors embedded for RUN 5
- Mercedes-Benz S-Class: https://www.mercedes-benz.co.il/models/s-class-fl/
- Mercedes-Benz SL: https://www.mercedes-benz.co.il/models/sl-class/
- Mercedes-Benz Vito: https://www.mercedes-benz.co.il/vans/van-models/vito-tourer/ and https://mercedes-benz-vans.co.il/vito-panel-van/
- MG current catalog: https://mg-israel.co.il/model/ and https://www.cartube.co.il/מחירון-רכב-חדש/mg
- MG ZS Hybrid: https://mg-israel.co.il/model/zs-hybrid/
- Mini Cabrio: https://www.mini.co.il/he_IL/home/range/mini-cooper-convertible.html
- Mini Aceman: https://www.mini.co.il/he_IL/home/range/mini-aceman.html

## Model-level facts
- **Mercedes-Benz R-Class**: Israeli repo sources Auto.co.il and iCar support R-Class as a historical Israeli-market model for 2006-2013; no current official Mercedes Israel page supports reopening it.
- **Mercedes-Benz S-Class**: Mercedes-Benz Israel currently lists S-Class FL trims S 350 d 4MATIC, S 450 e, S 580 e 4MATIC, and S 580 4MATIC; the old 2021 launch sources also support S 500 4MATIC and S 580 e rows through the pre-FL period.
- **Mercedes-Benz SL**: Mercedes-Benz Israel currently lists AMG SL 43 Racing, AMG SL 55 4Matic Racing, and AMG SL 63 4Matic Racing; iCar/Cartube repo sources support the 2012-2020 historical SL rows.
- **Mercedes-Benz SLK**: Israeli iCar/Cartube sources support SLK/SLC historical 2004-2020 rows; SLK/SLC is not a current Mercedes Israel model.
- **Mercedes-Benz V-Class**: Mercedes-Benz/Colmobil Vans and repo sources support V-Class as an Israeli-market van/MPV. Current rows require exact official van spec grounding before extending beyond 2024.
- **Mercedes-Benz Vito**: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
- **MG Cyberster**: Israeli launch sources support MG Cyberster Luxury RWD 340 hp and GT AWD 510 hp from 2024; EV schema with displacement null and single_speed is correct.
- **MG HS**: MG Israel/repo sources support HS PHEV and petrol rows through the earlier generation; MG's current Israeli catalog emphasizes newer HS Hybrid/EHS PHEV lines, so old HS rows must not be silently extended without exact current specs.
- **MG Marvel R**: MG Israel and Cartube support Marvel R Luxury 180 hp RWD and Performance 288 hp AWD in Israel from 2023; current 2026 catalog support is weaker, so keep closed unless repo-local current source exists.
- **MG MG3**: Israeli sources support historical MG3 petrol and current MG3 Hybrid+/hybrid 194 hp. The same 194 hp hybrid row must not exist twice under both MG3 and MG3 Hybrid+ without alias/lineage.
- **MG MG3 Hybrid+**: MG Israel markets MG3 Hybrid+ as a current Israeli model; duplicate technical rows should be merged/aliased with canonical MG3 policy rather than duplicated.
- **MG MG4**: MG Israel/Cartube/Carzone support current MG4 2026 lineup including Luxury, X-Range/Extended Range and X-Power; older Standard/170 hp row should not be treated as current unless explicitly still sold.
- **MG MG5**: MG Israel and Cartube support MG5 electric estate in Israel; current support exists but exact trim/technical fields must remain grounded.
- **MG ZR**: Israeli Auto/iCar sources support MG ZR only as historical British-era 2002-2005; do not currentize.
- **MG ZS**: Israeli sources support historical petrol ZS and current ZS Hybrid. MG Israel states ZS Hybrid has 194 hp, so any 196 hp row must be corrected or reviewed.
- **MG ZS EV**: Israeli sources support ZS EV 2020-2024 rows; current MG catalog no longer clearly lists ZS EV as the current EV line, so do not extend beyond 2024 without local source.
- **MG (British era) ZT**: Auto/KML Israeli sources support MG ZT as historical 2001-2005; keep historical only.
- **Mini Aceman**: MINI Israel has an official Aceman page, so market_scope should be IL-confirmed and rows should be current if exact local technical fields are grounded.
- **Mini Cabrio**: MINI Israel price list dated 04/2026 lists current MINI Cooper Cabrio trims Cooper C, Cooper S and Cooper JCW; older Cooper/Cooper S rows ending 2024 must not be extended as-is.

## Required checks after implementation
```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```
Then audit actual generated files: clean catalog, readiness, review, archive, quality scan, compute_resume_state(), unmatched_output_keys, active blockers, cursor/resume state, duplicate/split alias cleanup.

## Variant-level instructions

### PROFILE 1: IL-confirmed|Mercedes-Benz|R-Class
MODEL-LEVEL FACT: Israeli repo sources Auto.co.il and iCar support R-Class as a historical Israeli-market model for 2006-2013; no current official Mercedes Israel page supports reopening it.

#### VARIANT 1 / PROFILE 1.1
MODEL: IL-confirmed|Mercedes-Benz|R-Class
CURRENT VALUE: version_or_trim='R 350 4MATIC'; body_type='MPV'; fuel_type='petrol'; engine='3.5L v6'; engine_displacement_l=3.5; horsepower_hp=272; transmission='7-speed automatic'; drivetrain='AWD'; year_start=2006; year_end=2011; support_level='direct'; source_indexes=[0, 1]
PROBLEM: No blocking issue found in this row after RUN5 review; keep only if source_indexes and field_sources are valid.
WEB-VALIDATED FACT: Israeli repo sources Auto.co.il and iCar support R-Class as a historical Israeli-market model for 2006-2013; no current official Mercedes Israel page supports reopening it.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep current row unchanged; preserve field_sources/source_indexes.
ACTION: KEEP

#### VARIANT 2 / PROFILE 1.2
MODEL: IL-confirmed|Mercedes-Benz|R-Class
CURRENT VALUE: version_or_trim='R 350 4MATIC'; body_type='MPV'; fuel_type='petrol'; engine='3.5L v6'; engine_displacement_l=3.5; horsepower_hp=306; transmission='7-speed automatic'; drivetrain='AWD'; year_start=2011; year_end=2013; support_level='direct'; source_indexes=[0, 1]
PROBLEM: No blocking issue found in this row after RUN5 review; keep only if source_indexes and field_sources are valid.
WEB-VALIDATED FACT: Israeli repo sources Auto.co.il and iCar support R-Class as a historical Israeli-market model for 2006-2013; no current official Mercedes Israel page supports reopening it.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep current row unchanged; preserve field_sources/source_indexes.
ACTION: KEEP

#### VARIANT 3 / PROFILE 1.3
MODEL: IL-confirmed|Mercedes-Benz|R-Class
CURRENT VALUE: version_or_trim='R 320 CDI 4MATIC'; body_type='MPV'; fuel_type='diesel'; engine='3.0L v6 turbo'; engine_displacement_l=3.0; horsepower_hp=224; transmission='7-speed automatic'; drivetrain='AWD'; year_start=2006; year_end=2010; support_level='direct'; source_indexes=[0, 1]
PROBLEM: No blocking issue found in this row after RUN5 review; keep only if source_indexes and field_sources are valid.
WEB-VALIDATED FACT: Israeli repo sources Auto.co.il and iCar support R-Class as a historical Israeli-market model for 2006-2013; no current official Mercedes Israel page supports reopening it.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep current row unchanged; preserve field_sources/source_indexes.
ACTION: KEEP

#### VARIANT 4 / PROFILE 1.4
MODEL: IL-confirmed|Mercedes-Benz|R-Class
CURRENT VALUE: version_or_trim='R 350 CDI 4MATIC'; body_type='MPV'; fuel_type='diesel'; engine='3.0L v6 turbo'; engine_displacement_l=3.0; horsepower_hp=265; transmission='7-speed automatic'; drivetrain='AWD'; year_start=2010; year_end=2013; support_level='direct'; source_indexes=[0, 1]
PROBLEM: No blocking issue found in this row after RUN5 review; keep only if source_indexes and field_sources are valid.
WEB-VALIDATED FACT: Israeli repo sources Auto.co.il and iCar support R-Class as a historical Israeli-market model for 2006-2013; no current official Mercedes Israel page supports reopening it.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep current row unchanged; preserve field_sources/source_indexes.
ACTION: KEEP

### PROFILE 2: IL-confirmed|Mercedes-Benz|S-Class
MODEL-LEVEL FACT: Mercedes-Benz Israel currently lists S-Class FL trims S 350 d 4MATIC, S 450 e, S 580 e 4MATIC, and S 580 4MATIC; the old 2021 launch sources also support S 500 4MATIC and S 580 e rows through the pre-FL period.

#### VARIANT 5 / PROFILE 2.1
MODEL: IL-confirmed|Mercedes-Benz|S-Class
CURRENT VALUE: version_or_trim='S 500 4MATIC'; body_type='Sedan'; fuel_type='mild_hybrid'; engine='3.0L turbo inline-6'; engine_displacement_l=3.0; horsepower_hp=435; transmission='9-speed automatic'; drivetrain='AWD'; year_start=2021; year_end=2024; support_level='direct'; source_indexes=[0]
PROBLEM: Current official S-Class FL page lists S 580 4MATIC, not S 500 4MATIC; do not extend S 500 as current.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists S-Class FL trims S 350 d 4MATIC, S 450 e, S 580 e 4MATIC, and S 580 4MATIC; the old 2021 launch sources also support S 500 4MATIC and S 580 e rows through the pre-FL period.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep S 500 4MATIC as 2021-2024 pre-FL row; do not change to S 580 unless adding a separate grounded current row.
ACTION: KEEP

#### VARIANT 6 / PROFILE 2.2
MODEL: IL-confirmed|Mercedes-Benz|S-Class
CURRENT VALUE: version_or_trim='S 580 e 4MATIC'; body_type='Sedan'; fuel_type='plug_in_hybrid'; engine='3.0L turbo inline-6'; engine_displacement_l=3.0; horsepower_hp=510; transmission='9-speed automatic'; drivetrain='AWD'; year_start=2021; year_end=2024; support_level='direct'; source_indexes=[1]
PROBLEM: Row is closed at 2024, but Mercedes-Benz Israel current S-Class FL page lists S 580 e 4MATIC as an active current trim.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists S-Class FL trims S 350 d 4MATIC, S 450 e, S 580 e 4MATIC, and S 580 4MATIC; the old 2021 launch sources also support S 500 4MATIC and S 580 e rows through the pre-FL period.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Extend/currentize only this S 580 e 4MATIC row if technical fields remain grounded; otherwise keep old row closed and add current S 580 e to review with reason.
ACTION: FIX

#### VARIANT 7 / PROFILE 2.3
MODEL: IL-confirmed|Mercedes-Benz|S-Class
CURRENT VALUE: version_or_trim='S 560 e'; body_type='Sedan'; fuel_type='plug_in_hybrid'; engine='3.0L turbo v6'; engine_displacement_l=3.0; horsepower_hp=476; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2018; year_end=2020; support_level='direct'; source_indexes=[2]
PROBLEM: Historical row; no current extension allowed.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists S-Class FL trims S 350 d 4MATIC, S 450 e, S 580 e 4MATIC, and S 580 4MATIC; the old 2021 launch sources also support S 500 4MATIC and S 580 e rows through the pre-FL period.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and technical fields if sources remain valid.
ACTION: KEEP

#### VARIANT 8 / PROFILE 2.4
MODEL: IL-confirmed|Mercedes-Benz|S-Class
CURRENT VALUE: version_or_trim='S 500'; body_type='Sedan'; fuel_type='petrol'; engine='4.7L bi-turbo v8'; engine_displacement_l=4.7; horsepower_hp=455; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2017; support_level='direct'; source_indexes=[2]
PROBLEM: Historical row; no current extension allowed.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists S-Class FL trims S 350 d 4MATIC, S 450 e, S 580 e 4MATIC, and S 580 4MATIC; the old 2021 launch sources also support S 500 4MATIC and S 580 e rows through the pre-FL period.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and technical fields if sources remain valid.
ACTION: KEEP

#### VARIANT 9 / PROFILE 2.5
MODEL: IL-confirmed|Mercedes-Benz|S-Class
CURRENT VALUE: version_or_trim='S 350'; body_type='Sedan'; fuel_type='petrol'; engine='3.5L v6'; engine_displacement_l=3.5; horsepower_hp=272; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2006; year_end=2013; support_level='direct'; source_indexes=[3]
PROBLEM: Historical row; no current extension allowed.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists S-Class FL trims S 350 d 4MATIC, S 450 e, S 580 e 4MATIC, and S 580 4MATIC; the old 2021 launch sources also support S 500 4MATIC and S 580 e rows through the pre-FL period.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and technical fields if sources remain valid.
ACTION: KEEP

#### VARIANT 10 / PROFILE 2.6
MODEL: IL-confirmed|Mercedes-Benz|S-Class
CURRENT VALUE: version_or_trim='S 320'; body_type='Sedan'; fuel_type='petrol'; engine='3.2L v6'; engine_displacement_l=3.2; horsepower_hp=224; transmission='5-speed automatic'; drivetrain='RWD'; year_start=1999; year_end=2005; support_level='direct'; source_indexes=[4]
PROBLEM: Historical row; no current extension allowed.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists S-Class FL trims S 350 d 4MATIC, S 450 e, S 580 e 4MATIC, and S 580 4MATIC; the old 2021 launch sources also support S 500 4MATIC and S 580 e rows through the pre-FL period.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and technical fields if sources remain valid.
ACTION: KEEP

### PROFILE 3: IL-confirmed|Mercedes-Benz|SL
MODEL-LEVEL FACT: Mercedes-Benz Israel currently lists AMG SL 43 Racing, AMG SL 55 4Matic Racing, and AMG SL 63 4Matic Racing; iCar/Cartube repo sources support the 2012-2020 historical SL rows.

#### VARIANT 11 / PROFILE 3.1
MODEL: IL-confirmed|Mercedes-Benz|SL
CURRENT VALUE: version_or_trim='SL 43'; body_type='Convertible'; fuel_type='mild_hybrid'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=381; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2022; year_end=2024; support_level='direct'; source_indexes=[1]
PROBLEM: AMG SL current official page still lists AMG SL 43/55/63 trims; row is closed at 2024.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists AMG SL 43 Racing, AMG SL 55 4Matic Racing, and AMG SL 63 4Matic Racing; iCar/Cartube repo sources support the 2012-2020 historical SL rows.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Extend year_end to null/current for supported AMG SL rows, and normalize trim names to AMG SL 43 Racing / AMG SL 55 4Matic Racing / AMG SL 63 4Matic Racing if repo policy stores package names.
ACTION: FIX

#### VARIANT 12 / PROFILE 3.2
MODEL: IL-confirmed|Mercedes-Benz|SL
CURRENT VALUE: version_or_trim='SL 55 4MATIC+'; body_type='Convertible'; fuel_type='petrol'; engine='4.0L v8 turbo'; engine_displacement_l=4.0; horsepower_hp=476; transmission='9-speed automatic'; drivetrain='AWD'; year_start=2022; year_end=2024; support_level='direct'; source_indexes=[1]
PROBLEM: AMG SL current official page still lists AMG SL 43/55/63 trims; row is closed at 2024.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists AMG SL 43 Racing, AMG SL 55 4Matic Racing, and AMG SL 63 4Matic Racing; iCar/Cartube repo sources support the 2012-2020 historical SL rows.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Extend year_end to null/current for supported AMG SL rows, and normalize trim names to AMG SL 43 Racing / AMG SL 55 4Matic Racing / AMG SL 63 4Matic Racing if repo policy stores package names.
ACTION: FIX

#### VARIANT 13 / PROFILE 3.3
MODEL: IL-confirmed|Mercedes-Benz|SL
CURRENT VALUE: version_or_trim='SL 63 4MATIC+'; body_type='Convertible'; fuel_type='petrol'; engine='4.0L v8 turbo'; engine_displacement_l=4.0; horsepower_hp=585; transmission='9-speed automatic'; drivetrain='AWD'; year_start=2022; year_end=2024; support_level='direct'; source_indexes=[1]
PROBLEM: AMG SL current official page still lists AMG SL 43/55/63 trims; row is closed at 2024.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists AMG SL 43 Racing, AMG SL 55 4Matic Racing, and AMG SL 63 4Matic Racing; iCar/Cartube repo sources support the 2012-2020 historical SL rows.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Extend year_end to null/current for supported AMG SL rows, and normalize trim names to AMG SL 43 Racing / AMG SL 55 4Matic Racing / AMG SL 63 4Matic Racing if repo policy stores package names.
ACTION: FIX

#### VARIANT 14 / PROFILE 3.4
MODEL: IL-confirmed|Mercedes-Benz|SL
CURRENT VALUE: version_or_trim='SL 350'; body_type='Roadster'; fuel_type='petrol'; engine='3.5L v6'; engine_displacement_l=3.5; horsepower_hp=306; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2012; year_end=2016; support_level='direct'; source_indexes=[0]
PROBLEM: Historical 2012-2020 SL row; do not currentize old SL 350/400/500.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists AMG SL 43 Racing, AMG SL 55 4Matic Racing, and AMG SL 63 4Matic Racing; iCar/Cartube repo sources support the 2012-2020 historical SL rows.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and technical fields.
ACTION: KEEP

#### VARIANT 15 / PROFILE 3.5
MODEL: IL-confirmed|Mercedes-Benz|SL
CURRENT VALUE: version_or_trim='SL 400'; body_type='Roadster'; fuel_type='petrol'; engine='3.0L v6 turbo'; engine_displacement_l=3.0; horsepower_hp=367; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2016; year_end=2020; support_level='direct'; source_indexes=[0]
PROBLEM: Historical 2012-2020 SL row; do not currentize old SL 350/400/500.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists AMG SL 43 Racing, AMG SL 55 4Matic Racing, and AMG SL 63 4Matic Racing; iCar/Cartube repo sources support the 2012-2020 historical SL rows.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and technical fields.
ACTION: KEEP

#### VARIANT 16 / PROFILE 3.6
MODEL: IL-confirmed|Mercedes-Benz|SL
CURRENT VALUE: version_or_trim='SL 500'; body_type='Roadster'; fuel_type='petrol'; engine='4.7L v8 turbo'; engine_displacement_l=4.7; horsepower_hp=435; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2012; year_end=2016; support_level='direct'; source_indexes=[0]
PROBLEM: Historical 2012-2020 SL row; do not currentize old SL 350/400/500.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists AMG SL 43 Racing, AMG SL 55 4Matic Racing, and AMG SL 63 4Matic Racing; iCar/Cartube repo sources support the 2012-2020 historical SL rows.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and technical fields.
ACTION: KEEP

#### VARIANT 17 / PROFILE 3.7
MODEL: IL-confirmed|Mercedes-Benz|SL
CURRENT VALUE: version_or_trim='SL 500'; body_type='Roadster'; fuel_type='petrol'; engine='4.7L v8 turbo'; engine_displacement_l=4.7; horsepower_hp=455; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2016; year_end=2020; support_level='direct'; source_indexes=[0]
PROBLEM: Historical 2012-2020 SL row; do not currentize old SL 350/400/500.
WEB-VALIDATED FACT: Mercedes-Benz Israel currently lists AMG SL 43 Racing, AMG SL 55 4Matic Racing, and AMG SL 63 4Matic Racing; iCar/Cartube repo sources support the 2012-2020 historical SL rows.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and technical fields.
ACTION: KEEP

### PROFILE 4: IL-confirmed|Mercedes-Benz|SLK
MODEL-LEVEL FACT: Israeli iCar/Cartube sources support SLK/SLC historical 2004-2020 rows; SLK/SLC is not a current Mercedes Israel model.

#### VARIANT 18 / PROFILE 4.1
MODEL: IL-confirmed|Mercedes-Benz|SLK
CURRENT VALUE: version_or_trim='SLK 200 Kompressor'; body_type='Roadster'; fuel_type='petrol'; engine='1.8L supercharged'; engine_displacement_l=1.8; horsepower_hp=163; transmission='5-speed automatic'; drivetrain='RWD'; year_start=2004; year_end=2008; support_level='direct'; source_indexes=[1]
PROBLEM: No blocking issue found in this row after RUN5 review; keep only if source_indexes and field_sources are valid.
WEB-VALIDATED FACT: Israeli iCar/Cartube sources support SLK/SLC historical 2004-2020 rows; SLK/SLC is not a current Mercedes Israel model.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep current row unchanged; preserve field_sources/source_indexes.
ACTION: KEEP

#### VARIANT 19 / PROFILE 4.2
MODEL: IL-confirmed|Mercedes-Benz|SLK
CURRENT VALUE: version_or_trim='SLK 200 Kompressor'; body_type='Roadster'; fuel_type='petrol'; engine='1.8L supercharged'; engine_displacement_l=1.8; horsepower_hp=184; transmission='5-speed automatic'; drivetrain='RWD'; year_start=2008; year_end=2011; support_level='direct'; source_indexes=[1]
PROBLEM: No blocking issue found in this row after RUN5 review; keep only if source_indexes and field_sources are valid.
WEB-VALIDATED FACT: Israeli iCar/Cartube sources support SLK/SLC historical 2004-2020 rows; SLK/SLC is not a current Mercedes Israel model.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep current row unchanged; preserve field_sources/source_indexes.
ACTION: KEEP

#### VARIANT 20 / PROFILE 4.3
MODEL: IL-confirmed|Mercedes-Benz|SLK
CURRENT VALUE: version_or_trim='SLK 200 BlueEFFICIENCY'; body_type='Roadster'; fuel_type='petrol'; engine='1.8L turbo'; engine_displacement_l=1.8; horsepower_hp=184; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2015; support_level='direct'; source_indexes=[0, 3]
PROBLEM: No blocking issue found in this row after RUN5 review; keep only if source_indexes and field_sources are valid.
WEB-VALIDATED FACT: Israeli iCar/Cartube sources support SLK/SLC historical 2004-2020 rows; SLK/SLC is not a current Mercedes Israel model.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep current row unchanged; preserve field_sources/source_indexes.
ACTION: KEEP

#### VARIANT 21 / PROFILE 4.4
MODEL: IL-confirmed|Mercedes-Benz|SLK
CURRENT VALUE: version_or_trim='SLK 350'; body_type='Roadster'; fuel_type='petrol'; engine='3.5L v6'; engine_displacement_l=3.5; horsepower_hp=306; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2015; support_level='direct'; source_indexes=[0, 3]
PROBLEM: No blocking issue found in this row after RUN5 review; keep only if source_indexes and field_sources are valid.
WEB-VALIDATED FACT: Israeli iCar/Cartube sources support SLK/SLC historical 2004-2020 rows; SLK/SLC is not a current Mercedes Israel model.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep current row unchanged; preserve field_sources/source_indexes.
ACTION: KEEP

#### VARIANT 22 / PROFILE 4.5
MODEL: IL-confirmed|Mercedes-Benz|SLK
CURRENT VALUE: version_or_trim='SLC 200'; body_type='Roadster'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=184; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2016; year_end=2020; support_level='direct'; source_indexes=[2]
PROBLEM: No blocking issue found in this row after RUN5 review; keep only if source_indexes and field_sources are valid.
WEB-VALIDATED FACT: Israeli iCar/Cartube sources support SLK/SLC historical 2004-2020 rows; SLK/SLC is not a current Mercedes Israel model.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep current row unchanged; preserve field_sources/source_indexes.
ACTION: KEEP

### PROFILE 5: IL-confirmed|Mercedes-Benz|V-Class
MODEL-LEVEL FACT: Mercedes-Benz/Colmobil Vans and repo sources support V-Class as an Israeli-market van/MPV. Current rows require exact official van spec grounding before extending beyond 2024.

#### VARIANT 23 / PROFILE 5.1
MODEL: IL-confirmed|Mercedes-Benz|V-Class
CURRENT VALUE: version_or_trim='V 250 d'; body_type='MPV'; fuel_type='diesel'; engine='2.1L turbo'; engine_displacement_l=2.1; horsepower_hp=190; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2019; support_level='direct'; source_indexes=[1]
PROBLEM: No blocking issue found in this row after RUN5 review; keep only if source_indexes and field_sources are valid.
WEB-VALIDATED FACT: Mercedes-Benz/Colmobil Vans and repo sources support V-Class as an Israeli-market van/MPV. Current rows require exact official van spec grounding before extending beyond 2024.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep current row unchanged; preserve field_sources/source_indexes.
ACTION: KEEP

#### VARIANT 24 / PROFILE 5.2
MODEL: IL-confirmed|Mercedes-Benz|V-Class
CURRENT VALUE: version_or_trim='V 250 d'; body_type='MPV'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=190; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2019; year_end=2024; support_level='direct'; source_indexes=[1, 2, 3]
PROBLEM: V-Class is still a Mercedes Vans line, but exact 2025/2026 Israeli technical specs for V 250 d/V 300 d need local PDF grounding before extension.
WEB-VALIDATED FACT: Mercedes-Benz/Colmobil Vans and repo sources support V-Class as an Israeli-market van/MPV. Current rows require exact official van spec grounding before extending beyond 2024.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep row historical through 2024 unless official current V-Class PDF/spec supports same trim, power, transmission and drivetrain; if not grounded, move current extension to non-blocking review.
ACTION: MOVE TO REVIEW

#### VARIANT 25 / PROFILE 5.3
MODEL: IL-confirmed|Mercedes-Benz|V-Class
CURRENT VALUE: version_or_trim='V 300 d'; body_type='MPV'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=237; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2019; year_end=2024; support_level='direct'; source_indexes=[1, 2, 3]
PROBLEM: V-Class is still a Mercedes Vans line, but exact 2025/2026 Israeli technical specs for V 250 d/V 300 d need local PDF grounding before extension.
WEB-VALIDATED FACT: Mercedes-Benz/Colmobil Vans and repo sources support V-Class as an Israeli-market van/MPV. Current rows require exact official van spec grounding before extending beyond 2024.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep row historical through 2024 unless official current V-Class PDF/spec supports same trim, power, transmission and drivetrain; if not grounded, move current extension to non-blocking review.
ACTION: MOVE TO REVIEW

### PROFILE 6: IL-confirmed|Mercedes-Benz|Vito
MODEL-LEVEL FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.

#### VARIANT 26 / PROFILE 6.1
MODEL: IL-confirmed|Mercedes-Benz|Vito
CURRENT VALUE: version_or_trim=None; body_type='Van'; fuel_type='diesel'; engine='2.1L turbo'; engine_displacement_l=2.1; horsepower_hp=136; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2021; support_level='direct'; source_indexes=[2]
PROBLEM: version_or_trim is null even though horsepower/body rows map to Vito CDI commercial/passenger variants; active Mercedes Vans pages support Vito Panel Van/Tourer.
WEB-VALIDATED FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set version_or_trim to Vito 114 CDI Panel Van; keep 2.1L/7AT rows historical 2014-2021; for 2.0L/9AT rows, extend beyond 2024 only if current official Vans spec supports the exact row.
ACTION: FIX

#### VARIANT 27 / PROFILE 6.2
MODEL: IL-confirmed|Mercedes-Benz|Vito
CURRENT VALUE: version_or_trim=None; body_type='Van'; fuel_type='diesel'; engine='2.1L turbo'; engine_displacement_l=2.1; horsepower_hp=163; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2021; support_level='direct'; source_indexes=[2]
PROBLEM: version_or_trim is null even though horsepower/body rows map to Vito CDI commercial/passenger variants; active Mercedes Vans pages support Vito Panel Van/Tourer.
WEB-VALIDATED FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set version_or_trim to Vito 116 CDI Panel Van; keep 2.1L/7AT rows historical 2014-2021; for 2.0L/9AT rows, extend beyond 2024 only if current official Vans spec supports the exact row.
ACTION: FIX

#### VARIANT 28 / PROFILE 6.3
MODEL: IL-confirmed|Mercedes-Benz|Vito
CURRENT VALUE: version_or_trim=None; body_type='Van'; fuel_type='diesel'; engine='2.1L turbo'; engine_displacement_l=2.1; horsepower_hp=190; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2021; support_level='direct'; source_indexes=[2]
PROBLEM: version_or_trim is null even though horsepower/body rows map to Vito CDI commercial/passenger variants; active Mercedes Vans pages support Vito Panel Van/Tourer.
WEB-VALIDATED FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set version_or_trim to Vito 119 CDI Panel Van; keep 2.1L/7AT rows historical 2014-2021; for 2.0L/9AT rows, extend beyond 2024 only if current official Vans spec supports the exact row.
ACTION: FIX

#### VARIANT 29 / PROFILE 6.4
MODEL: IL-confirmed|Mercedes-Benz|Vito
CURRENT VALUE: version_or_trim=None; body_type='MPV'; fuel_type='diesel'; engine='2.1L turbo'; engine_displacement_l=2.1; horsepower_hp=136; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2021; support_level='direct'; source_indexes=[2]
PROBLEM: version_or_trim is null even though horsepower/body rows map to Vito CDI commercial/passenger variants; active Mercedes Vans pages support Vito Panel Van/Tourer.
WEB-VALIDATED FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set version_or_trim to Vito 114 CDI Tourer; keep 2.1L/7AT rows historical 2014-2021; for 2.0L/9AT rows, extend beyond 2024 only if current official Vans spec supports the exact row.
ACTION: FIX

#### VARIANT 30 / PROFILE 6.5
MODEL: IL-confirmed|Mercedes-Benz|Vito
CURRENT VALUE: version_or_trim=None; body_type='MPV'; fuel_type='diesel'; engine='2.1L turbo'; engine_displacement_l=2.1; horsepower_hp=163; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2021; support_level='direct'; source_indexes=[2]
PROBLEM: version_or_trim is null even though horsepower/body rows map to Vito CDI commercial/passenger variants; active Mercedes Vans pages support Vito Panel Van/Tourer.
WEB-VALIDATED FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set version_or_trim to Vito 116 CDI Tourer; keep 2.1L/7AT rows historical 2014-2021; for 2.0L/9AT rows, extend beyond 2024 only if current official Vans spec supports the exact row.
ACTION: FIX

#### VARIANT 31 / PROFILE 6.6
MODEL: IL-confirmed|Mercedes-Benz|Vito
CURRENT VALUE: version_or_trim=None; body_type='MPV'; fuel_type='diesel'; engine='2.1L turbo'; engine_displacement_l=2.1; horsepower_hp=190; transmission='7-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2021; support_level='direct'; source_indexes=[2]
PROBLEM: version_or_trim is null even though horsepower/body rows map to Vito CDI commercial/passenger variants; active Mercedes Vans pages support Vito Panel Van/Tourer.
WEB-VALIDATED FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set version_or_trim to Vito 119 CDI Tourer; keep 2.1L/7AT rows historical 2014-2021; for 2.0L/9AT rows, extend beyond 2024 only if current official Vans spec supports the exact row.
ACTION: FIX

#### VARIANT 32 / PROFILE 6.7
MODEL: IL-confirmed|Mercedes-Benz|Vito
CURRENT VALUE: version_or_trim=None; body_type='Van'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=136; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2021; year_end=2024; support_level='direct'; source_indexes=[0, 2]
PROBLEM: version_or_trim is null even though horsepower/body rows map to Vito CDI commercial/passenger variants; active Mercedes Vans pages support Vito Panel Van/Tourer.
WEB-VALIDATED FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set version_or_trim to Vito 114 CDI Panel Van; keep 2.1L/7AT rows historical 2014-2021; for 2.0L/9AT rows, extend beyond 2024 only if current official Vans spec supports the exact row.
ACTION: FIX

#### VARIANT 33 / PROFILE 6.8
MODEL: IL-confirmed|Mercedes-Benz|Vito
CURRENT VALUE: version_or_trim=None; body_type='Van'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=163; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2021; year_end=2024; support_level='direct'; source_indexes=[0, 2]
PROBLEM: version_or_trim is null even though horsepower/body rows map to Vito CDI commercial/passenger variants; active Mercedes Vans pages support Vito Panel Van/Tourer.
WEB-VALIDATED FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set version_or_trim to Vito 116 CDI Panel Van; keep 2.1L/7AT rows historical 2014-2021; for 2.0L/9AT rows, extend beyond 2024 only if current official Vans spec supports the exact row.
ACTION: FIX

#### VARIANT 34 / PROFILE 6.9
MODEL: IL-confirmed|Mercedes-Benz|Vito
CURRENT VALUE: version_or_trim=None; body_type='Van'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=190; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2021; year_end=2024; support_level='direct'; source_indexes=[0, 2]
PROBLEM: version_or_trim is null even though horsepower/body rows map to Vito CDI commercial/passenger variants; active Mercedes Vans pages support Vito Panel Van/Tourer.
WEB-VALIDATED FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set version_or_trim to Vito 119 CDI Panel Van; keep 2.1L/7AT rows historical 2014-2021; for 2.0L/9AT rows, extend beyond 2024 only if current official Vans spec supports the exact row.
ACTION: FIX

#### VARIANT 35 / PROFILE 6.10
MODEL: IL-confirmed|Mercedes-Benz|Vito
CURRENT VALUE: version_or_trim=None; body_type='MPV'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=136; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2021; year_end=2024; support_level='direct'; source_indexes=[1, 2]
PROBLEM: version_or_trim is null even though horsepower/body rows map to Vito CDI commercial/passenger variants; active Mercedes Vans pages support Vito Panel Van/Tourer.
WEB-VALIDATED FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set version_or_trim to Vito 114 CDI Tourer; keep 2.1L/7AT rows historical 2014-2021; for 2.0L/9AT rows, extend beyond 2024 only if current official Vans spec supports the exact row.
ACTION: FIX

#### VARIANT 36 / PROFILE 6.11
MODEL: IL-confirmed|Mercedes-Benz|Vito
CURRENT VALUE: version_or_trim=None; body_type='MPV'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=163; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2021; year_end=2024; support_level='direct'; source_indexes=[1, 2]
PROBLEM: version_or_trim is null even though horsepower/body rows map to Vito CDI commercial/passenger variants; active Mercedes Vans pages support Vito Panel Van/Tourer.
WEB-VALIDATED FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set version_or_trim to Vito 116 CDI Tourer; keep 2.1L/7AT rows historical 2014-2021; for 2.0L/9AT rows, extend beyond 2024 only if current official Vans spec supports the exact row.
ACTION: FIX

#### VARIANT 37 / PROFILE 6.12
MODEL: IL-confirmed|Mercedes-Benz|Vito
CURRENT VALUE: version_or_trim=None; body_type='MPV'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=190; transmission='9-speed automatic'; drivetrain='RWD'; year_start=2021; year_end=2024; support_level='direct'; source_indexes=[1, 2]
PROBLEM: version_or_trim is null even though horsepower/body rows map to Vito CDI commercial/passenger variants; active Mercedes Vans pages support Vito Panel Van/Tourer.
WEB-VALIDATED FACT: Mercedes-Benz Vans Israel has active Vito Panel Van and Vito Tourer pages with technical-spec downloads; empty trims should be normalized to Vito 114/116/119 CDI and body/usage lineage should be explicit.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set version_or_trim to Vito 119 CDI Tourer; keep 2.1L/7AT rows historical 2014-2021; for 2.0L/9AT rows, extend beyond 2024 only if current official Vans spec supports the exact row.
ACTION: FIX

### PROFILE 7: IL-confirmed|MG|Cyberster
MODEL-LEVEL FACT: Israeli launch sources support MG Cyberster Luxury RWD 340 hp and GT AWD 510 hp from 2024; EV schema with displacement null and single_speed is correct.

#### VARIANT 38 / PROFILE 7.1
MODEL: IL-confirmed|MG|Cyberster
CURRENT VALUE: version_or_trim='Luxury'; body_type='Roadster'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=340; transmission='single_speed'; drivetrain='RWD'; year_start=2024; year_end=None; support_level='direct'; source_indexes=[0, 1]
PROBLEM: No blocking issue; Israeli launch sources support Luxury 340 hp RWD and GT 510 hp AWD.
WEB-VALIDATED FACT: Israeli launch sources support MG Cyberster Luxury RWD 340 hp and GT AWD 510 hp from 2024; EV schema with displacement null and single_speed is correct.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep EV schema: displacement null, electric fuel_type, single_speed, correct drivetrain.
ACTION: KEEP

#### VARIANT 39 / PROFILE 7.2
MODEL: IL-confirmed|MG|Cyberster
CURRENT VALUE: version_or_trim='GT'; body_type='Roadster'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=510; transmission='single_speed'; drivetrain='AWD'; year_start=2024; year_end=None; support_level='direct'; source_indexes=[0, 1]
PROBLEM: No blocking issue; Israeli launch sources support Luxury 340 hp RWD and GT 510 hp AWD.
WEB-VALIDATED FACT: Israeli launch sources support MG Cyberster Luxury RWD 340 hp and GT AWD 510 hp from 2024; EV schema with displacement null and single_speed is correct.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep EV schema: displacement null, electric fuel_type, single_speed, correct drivetrain.
ACTION: KEEP

### PROFILE 8: IL-confirmed|MG|HS
MODEL-LEVEL FACT: MG Israel/repo sources support HS PHEV and petrol rows through the earlier generation; MG's current Israeli catalog emphasizes newer HS Hybrid/EHS PHEV lines, so old HS rows must not be silently extended without exact current specs.

#### VARIANT 40 / PROFILE 8.1
MODEL: IL-confirmed|MG|HS
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='plug_in_hybrid'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=258; transmission='10-speed automatic'; drivetrain='FWD'; year_start=2021; year_end=2024; support_level='direct'; source_indexes=[0, 2]
PROBLEM: Existing HS PHEV/petrol rows are older-generation rows closed at 2024; do not silently extend to newer HS Hybrid/EHS lines.
WEB-VALIDATED FACT: MG Israel/repo sources support HS PHEV and petrol rows through the earlier generation; MG's current Israeli catalog emphasizes newer HS Hybrid/EHS PHEV lines, so old HS rows must not be silently extended without exact current specs.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep closed at 2024 unless adding separate grounded current HS Hybrid/EHS rows with exact specs.
ACTION: KEEP

#### VARIANT 41 / PROFILE 8.2
MODEL: IL-confirmed|MG|HS
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=162; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2023; year_end=2024; support_level='direct'; source_indexes=[1, 2]
PROBLEM: Existing HS PHEV/petrol rows are older-generation rows closed at 2024; do not silently extend to newer HS Hybrid/EHS lines.
WEB-VALIDATED FACT: MG Israel/repo sources support HS PHEV and petrol rows through the earlier generation; MG's current Israeli catalog emphasizes newer HS Hybrid/EHS PHEV lines, so old HS rows must not be silently extended without exact current specs.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep closed at 2024 unless adding separate grounded current HS Hybrid/EHS rows with exact specs.
ACTION: KEEP

### PROFILE 9: IL-confirmed|MG|Marvel R
MODEL-LEVEL FACT: MG Israel and Cartube support Marvel R Luxury 180 hp RWD and Performance 288 hp AWD in Israel from 2023; current 2026 catalog support is weaker, so keep closed unless repo-local current source exists.

#### VARIANT 42 / PROFILE 9.1
MODEL: IL-confirmed|MG|Marvel R
CURRENT VALUE: version_or_trim='Luxury'; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=180; transmission='2-speed automatic'; drivetrain='RWD'; year_start=2023; year_end=2024; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Marvel R rows are Israel-grounded for 2023-2024; current 2026 official catalog support is not strong enough to reopen.
WEB-VALIDATED FACT: MG Israel and Cartube support Marvel R Luxury 180 hp RWD and Performance 288 hp AWD in Israel from 2023; current 2026 catalog support is weaker, so keep closed unless repo-local current source exists.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep year_end 2024. Keep 2-speed automatic only if repo schema permits this EV transmission term; otherwise normalize to allowed EV term and document exception.
ACTION: KEEP

#### VARIANT 43 / PROFILE 9.2
MODEL: IL-confirmed|MG|Marvel R
CURRENT VALUE: version_or_trim='Performance'; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=288; transmission='2-speed automatic'; drivetrain='AWD'; year_start=2023; year_end=2024; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Marvel R rows are Israel-grounded for 2023-2024; current 2026 official catalog support is not strong enough to reopen.
WEB-VALIDATED FACT: MG Israel and Cartube support Marvel R Luxury 180 hp RWD and Performance 288 hp AWD in Israel from 2023; current 2026 catalog support is weaker, so keep closed unless repo-local current source exists.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep year_end 2024. Keep 2-speed automatic only if repo schema permits this EV transmission term; otherwise normalize to allowed EV term and document exception.
ACTION: KEEP

### PROFILE 10: IL-confirmed|MG|MG3
MODEL-LEVEL FACT: Israeli sources support historical MG3 petrol and current MG3 Hybrid+/hybrid 194 hp. The same 194 hp hybrid row must not exist twice under both MG3 and MG3 Hybrid+ without alias/lineage.

#### VARIANT 44 / PROFILE 10.1
MODEL: IL-confirmed|MG|MG3
CURRENT VALUE: version_or_trim='Classic / Comfort / Deluxe'; body_type='Hatchback'; fuel_type='petrol'; engine='1.5L inline-4'; engine_displacement_l=1.5; horsepower_hp=106; transmission='5-speed manual'; drivetrain='FWD'; year_start=2015; year_end=2018; support_level='direct'; source_indexes=[1, 2]
PROBLEM: Historical petrol MG3 row supported by Israeli sources; not current.
WEB-VALIDATED FACT: Israeli sources support historical MG3 petrol and current MG3 Hybrid+/hybrid 194 hp. The same 194 hp hybrid row must not exist twice under both MG3 and MG3 Hybrid+ without alias/lineage.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep 2015-2018 petrol row.
ACTION: KEEP

#### VARIANT 45 / PROFILE 10.2
MODEL: IL-confirmed|MG|MG3
CURRENT VALUE: version_or_trim='Comfort / Luxury'; body_type='Hatchback'; fuel_type='hybrid'; engine='1.5L inline-4'; engine_displacement_l=1.5; horsepower_hp=194; transmission='3-speed automatic'; drivetrain='FWD'; year_start=2024; year_end=None; support_level='direct'; source_indexes=[3]
PROBLEM: Hybrid row duplicates separate MG3 Hybrid+ profile and stores Comfort/Luxury as one combined trim.
WEB-VALIDATED FACT: Israeli sources support historical MG3 petrol and current MG3 Hybrid+/hybrid 194 hp. The same 194 hp hybrid row must not exist twice under both MG3 and MG3 Hybrid+ without alias/lineage.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Use one canonical representation only. Prefer canonical model MG3 with alias MG3 Hybrid+; split current hybrid into Comfort and Luxury rows if website needs trim-level options. Delete/archive duplicate MG3 Hybrid+ technical row with lineage.
ACTION: SPLIT / MERGE

### PROFILE 11: IL-confirmed|MG|MG3 Hybrid+
MODEL-LEVEL FACT: MG Israel markets MG3 Hybrid+ as a current Israeli model; duplicate technical rows should be merged/aliased with canonical MG3 policy rather than duplicated.

#### VARIANT 46 / PROFILE 11.1
MODEL: IL-confirmed|MG|MG3 Hybrid+
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='hybrid'; engine='1.5L'; engine_displacement_l=1.5; horsepower_hp=194; transmission='3-speed automatic'; drivetrain='FWD'; year_start=2024; year_end=None; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Duplicate technical profile with MG MG3 current hybrid row.
WEB-VALIDATED FACT: MG Israel markets MG3 Hybrid+ as a current Israeli model; duplicate technical rows should be merged/aliased with canonical MG3 policy rather than duplicated.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Merge into MG3 canonical profile or keep MG3 Hybrid+ as canonical only if repo line-split policy requires; in all cases do not keep duplicate 194 hp clean rows in both profiles. Preserve alias/lineage.
ACTION: MERGE

### PROFILE 12: IL-confirmed|MG|MG4
MODEL-LEVEL FACT: MG Israel/Cartube/Carzone support current MG4 2026 lineup including Luxury, X-Range/Extended Range and X-Power; older Standard/170 hp row should not be treated as current unless explicitly still sold.

#### VARIANT 47 / PROFILE 12.1
MODEL: IL-confirmed|MG|MG4
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=170; transmission='single_speed'; drivetrain='RWD'; year_start=2023; year_end=2024; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Older Standard/entry MG4 row is not clearly present in current 2026 Israeli catalog.
WEB-VALIDATED FACT: MG Israel/Cartube/Carzone support current MG4 2026 lineup including Luxury, X-Range/Extended Range and X-Power; older Standard/170 hp row should not be treated as current unless explicitly still sold.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep as 2023-2024 historical; do not extend current.
ACTION: KEEP

#### VARIANT 48 / PROFILE 12.2
MODEL: IL-confirmed|MG|MG4
CURRENT VALUE: version_or_trim='Luxury'; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=204; transmission='single_speed'; drivetrain='RWD'; year_start=2023; year_end=2024; support_level='direct'; source_indexes=[0, 1]
PROBLEM: MG4 Luxury is current in Israeli 2026 catalog; row is closed at 2024.
WEB-VALIDATED FACT: MG Israel/Cartube/Carzone support current MG4 2026 lineup including Luxury, X-Range/Extended Range and X-Power; older Standard/170 hp row should not be treated as current unless explicitly still sold.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set year_end null/current if source_indexes/field_sources support current MG4 Luxury 204 hp; otherwise add to review.
ACTION: FIX

#### VARIANT 49 / PROFILE 12.3
MODEL: IL-confirmed|MG|MG4
CURRENT VALUE: version_or_trim='Extended Range'; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=245; transmission='single_speed'; drivetrain='RWD'; year_start=2024; year_end=2024; support_level='direct'; source_indexes=[0, 2]
PROBLEM: Current Israeli catalog uses MG4 X-Range naming; row says Extended Range and closed 2024.
WEB-VALIDATED FACT: MG Israel/Cartube/Carzone support current MG4 2026 lineup including Luxury, X-Range/Extended Range and X-Power; older Standard/170 hp row should not be treated as current unless explicitly still sold.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Normalize trim to X-Range or Extended Range/X-Range alias and set year_end null/current if source supports.
ACTION: FIX

#### VARIANT 50 / PROFILE 12.4
MODEL: IL-confirmed|MG|MG4
CURRENT VALUE: version_or_trim='X-Power'; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=435; transmission='single_speed'; drivetrain='AWD'; year_start=2024; year_end=2024; support_level='direct'; source_indexes=[0, 2]
PROBLEM: MG4 X-Power appears in current Israeli catalog; row is closed at 2024.
WEB-VALIDATED FACT: MG Israel/Cartube/Carzone support current MG4 2026 lineup including Luxury, X-Range/Extended Range and X-Power; older Standard/170 hp row should not be treated as current unless explicitly still sold.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Set year_end null/current for X-Power if current source supports 435 hp AWD.
ACTION: FIX

### PROFILE 13: IL-confirmed|MG|MG5
MODEL-LEVEL FACT: MG Israel and Cartube support MG5 electric estate in Israel; current support exists but exact trim/technical fields must remain grounded.

#### VARIANT 51 / PROFILE 13.1
MODEL: IL-confirmed|MG|MG5
CURRENT VALUE: version_or_trim='Luxury'; body_type='Estate'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=156; transmission='single_speed'; drivetrain='FWD'; year_start=2023; year_end=None; support_level='direct'; source_indexes=[0, 1]
PROBLEM: No blocking issue; MG5 electric estate is Israel-grounded and current support exists.
WEB-VALIDATED FACT: MG Israel and Cartube support MG5 electric estate in Israel; current support exists but exact trim/technical fields must remain grounded.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep Luxury EV estate row; ensure EV schema remains valid.
ACTION: KEEP

### PROFILE 14: IL-confirmed|MG|ZR
MODEL-LEVEL FACT: Israeli Auto/iCar sources support MG ZR only as historical British-era 2002-2005; do not currentize.

#### VARIANT 52 / PROFILE 14.1
MODEL: IL-confirmed|MG|ZR
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.4L inline-4'; engine_displacement_l=1.4; horsepower_hp=103; transmission='5-speed manual'; drivetrain='FWD'; year_start=2002; year_end=2005; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Historical British-era MG row only; no current extension.
WEB-VALIDATED FACT: Israeli Auto/iCar sources support MG ZR only as historical British-era 2002-2005; do not currentize.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and fields; do not currentize.
ACTION: KEEP

#### VARIANT 53 / PROFILE 14.2
MODEL: IL-confirmed|MG|ZR
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.8L inline-4'; engine_displacement_l=1.8; horsepower_hp=117; transmission='cvt'; drivetrain='FWD'; year_start=2002; year_end=2005; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Historical British-era MG row only; no current extension.
WEB-VALIDATED FACT: Israeli Auto/iCar sources support MG ZR only as historical British-era 2002-2005; do not currentize.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and fields; do not currentize.
ACTION: KEEP

#### VARIANT 54 / PROFILE 14.3
MODEL: IL-confirmed|MG|ZR
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.8L vvc inline-4'; engine_displacement_l=1.8; horsepower_hp=160; transmission='5-speed manual'; drivetrain='FWD'; year_start=2002; year_end=2005; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Historical British-era MG row only; no current extension.
WEB-VALIDATED FACT: Israeli Auto/iCar sources support MG ZR only as historical British-era 2002-2005; do not currentize.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and fields; do not currentize.
ACTION: KEEP

### PROFILE 15: global-reference-only|MG|ZS
MODEL-LEVEL FACT: Israeli sources support historical petrol ZS and current ZS Hybrid. MG Israel states ZS Hybrid has 194 hp, so any 196 hp row must be corrected or reviewed.

#### VARIANT 55 / PROFILE 15.1
MODEL: global-reference-only|MG|ZS
CURRENT VALUE: version_or_trim=None; body_type='Crossover'; fuel_type='petrol'; engine='1.0L turbo'; engine_displacement_l=1.0; horsepower_hp=111; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2018; year_end=2021; support_level='direct'; source_indexes=[1, 2]
PROBLEM: Global-reference-only MG ZS duplicates Israeli ZS evidence and must not remain a separate clean profile.
WEB-VALIDATED FACT: Israeli sources support historical petrol ZS and current ZS Hybrid. MG Israel states ZS Hybrid has 194 hp, so any 196 hp row must be corrected or reviewed.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Merge petrol rows into canonical Israeli MG ZS profile or archive non-blocking with lineage to IL-likely/IL-confirmed MG ZS.
ACTION: MERGE / ARCHIVE NON-BLOCKING

#### VARIANT 56 / PROFILE 15.2
MODEL: global-reference-only|MG|ZS
CURRENT VALUE: version_or_trim=None; body_type='Crossover'; fuel_type='petrol'; engine='1.5L'; engine_displacement_l=1.5; horsepower_hp=106; transmission='4-speed automatic'; drivetrain='FWD'; year_start=2018; year_end=2020; support_level='direct'; source_indexes=[1, 2]
PROBLEM: Global-reference-only MG ZS duplicates Israeli ZS evidence and must not remain a separate clean profile.
WEB-VALIDATED FACT: Israeli sources support historical petrol ZS and current ZS Hybrid. MG Israel states ZS Hybrid has 194 hp, so any 196 hp row must be corrected or reviewed.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Merge petrol rows into canonical Israeli MG ZS profile or archive non-blocking with lineage to IL-likely/IL-confirmed MG ZS.
ACTION: MERGE / ARCHIVE NON-BLOCKING

### PROFILE 16: IL-likely|MG|ZS
MODEL-LEVEL FACT: Israeli sources support historical petrol ZS and current ZS Hybrid. MG Israel states ZS Hybrid has 194 hp, so any 196 hp row must be corrected or reviewed.

#### VARIANT 57 / PROFILE 16.1
MODEL: IL-likely|MG|ZS
CURRENT VALUE: version_or_trim='Net Up'; body_type='SUV'; fuel_type='petrol'; engine='1.0L turbo'; engine_displacement_l=1.0; horsepower_hp=111; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2018; year_end=2023; support_level='direct'; source_indexes=[1]
PROBLEM: IL-likely MG ZS should be promoted/merged to canonical IL-confirmed if Israeli sources are attached; avoid duplicate with global-reference-only profile.
WEB-VALIDATED FACT: Israeli sources support historical petrol ZS and current ZS Hybrid. MG Israel states ZS Hybrid has 194 hp, so any 196 hp row must be corrected or reviewed.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Merge with global petrol ZS rows, preserve Net Up historical row, and mark canonical scope IL-confirmed if policy allows.
ACTION: FIX

#### VARIANT 58 / PROFILE 16.2
MODEL: IL-likely|MG|ZS
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='hybrid'; engine='1.5L hybrid'; engine_displacement_l=1.5; horsepower_hp=196; transmission='3-speed automatic'; drivetrain='FWD'; year_start=2024; year_end=None; support_level='direct'; source_indexes=[2]
PROBLEM: MG Israel states current ZS Hybrid combined output is 194 hp; row has 196 hp.
WEB-VALIDATED FACT: Israeli sources support historical petrol ZS and current ZS Hybrid. MG Israel states ZS Hybrid has 194 hp, so any 196 hp row must be corrected or reviewed.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Correct horsepower_hp to 194, set market_scope/profile to IL-confirmed if official source is attached, and keep current year_end null.
ACTION: FIX

### PROFILE 17: IL-confirmed|MG|ZS EV
MODEL-LEVEL FACT: Israeli sources support ZS EV 2020-2024 rows; current MG catalog no longer clearly lists ZS EV as the current EV line, so do not extend beyond 2024 without local source.

#### VARIANT 59 / PROFILE 17.1
MODEL: IL-confirmed|MG|ZS EV
CURRENT VALUE: version_or_trim='Net Up'; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=143; transmission='single_speed'; drivetrain='FWD'; year_start=2020; year_end=2021; support_level='direct'; source_indexes=[0, 1, 2]
PROBLEM: ZS EV rows are Israel-grounded through 2024; current catalog support for ZS EV is weaker than ZS Hybrid/MGS lines.
WEB-VALIDATED FACT: Israeli sources support ZS EV 2020-2024 rows; current MG catalog no longer clearly lists ZS EV as the current EV line, so do not extend beyond 2024 without local source.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep rows closed at 2024; do not extend without official current source. EV schema is valid.
ACTION: KEEP

#### VARIANT 60 / PROFILE 17.2
MODEL: IL-confirmed|MG|ZS EV
CURRENT VALUE: version_or_trim='Net Up'; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=177; transmission='single_speed'; drivetrain='FWD'; year_start=2022; year_end=2024; support_level='direct'; source_indexes=[1, 2]
PROBLEM: ZS EV rows are Israel-grounded through 2024; current catalog support for ZS EV is weaker than ZS Hybrid/MGS lines.
WEB-VALIDATED FACT: Israeli sources support ZS EV 2020-2024 rows; current MG catalog no longer clearly lists ZS EV as the current EV line, so do not extend beyond 2024 without local source.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep rows closed at 2024; do not extend without official current source. EV schema is valid.
ACTION: KEEP

#### VARIANT 61 / PROFILE 17.3
MODEL: IL-confirmed|MG|ZS EV
CURRENT VALUE: version_or_trim='Net Up'; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=156; transmission='single_speed'; drivetrain='FWD'; year_start=2022; year_end=2024; support_level='direct'; source_indexes=[1, 2]
PROBLEM: ZS EV rows are Israel-grounded through 2024; current catalog support for ZS EV is weaker than ZS Hybrid/MGS lines.
WEB-VALIDATED FACT: Israeli sources support ZS EV 2020-2024 rows; current MG catalog no longer clearly lists ZS EV as the current EV line, so do not extend beyond 2024 without local source.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep rows closed at 2024; do not extend without official current source. EV schema is valid.
ACTION: KEEP

### PROFILE 18: IL-confirmed|MG (British era)|ZT
MODEL-LEVEL FACT: Auto/KML Israeli sources support MG ZT as historical 2001-2005; keep historical only.

#### VARIANT 62 / PROFILE 18.1
MODEL: IL-confirmed|MG (British era)|ZT
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.5L v6'; engine_displacement_l=2.5; horsepower_hp=177; transmission='5-speed automatic'; drivetrain='FWD'; year_start=2001; year_end=2005; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Historical British-era MG row only; no current extension.
WEB-VALIDATED FACT: Auto/KML Israeli sources support MG ZT as historical 2001-2005; keep historical only.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and fields; do not currentize.
ACTION: KEEP

#### VARIANT 63 / PROFILE 18.2
MODEL: IL-confirmed|MG (British era)|ZT
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.5L v6'; engine_displacement_l=2.5; horsepower_hp=190; transmission='5-speed manual'; drivetrain='FWD'; year_start=2001; year_end=2005; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Historical British-era MG row only; no current extension.
WEB-VALIDATED FACT: Auto/KML Israeli sources support MG ZT as historical 2001-2005; keep historical only.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep historical years and fields; do not currentize.
ACTION: KEEP

### PROFILE 19: IL-likely|Mini|Aceman
MODEL-LEVEL FACT: MINI Israel has an official Aceman page, so market_scope should be IL-confirmed and rows should be current if exact local technical fields are grounded.

#### VARIANT 64 / PROFILE 19.1
MODEL: IL-likely|Mini|Aceman
CURRENT VALUE: version_or_trim='E'; body_type='Crossover'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=184; transmission='single_speed'; drivetrain='FWD'; year_start=2024; year_end=2024; support_level='direct'; source_indexes=[0, 1]
PROBLEM: MINI Israel has official Aceman page; profile is only IL-likely and rows are closed at 2024.
WEB-VALIDATED FACT: MINI Israel has an official Aceman page, so market_scope should be IL-confirmed and rows should be current if exact local technical fields are grounded.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Promote to IL-confirmed if source attached; set year_end null/current for E and SE if official local specs support exact 184/218 hp. Keep EV schema.
ACTION: FIX

#### VARIANT 65 / PROFILE 19.2
MODEL: IL-likely|Mini|Aceman
CURRENT VALUE: version_or_trim='SE'; body_type='Crossover'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=218; transmission='single_speed'; drivetrain='FWD'; year_start=2024; year_end=2024; support_level='direct'; source_indexes=[0, 1]
PROBLEM: MINI Israel has official Aceman page; profile is only IL-likely and rows are closed at 2024.
WEB-VALIDATED FACT: MINI Israel has an official Aceman page, so market_scope should be IL-confirmed and rows should be current if exact local technical fields are grounded.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Promote to IL-confirmed if source attached; set year_end null/current for E and SE if official local specs support exact 184/218 hp. Keep EV schema.
ACTION: FIX

### PROFILE 20: IL-confirmed|Mini|Cabrio
MODEL-LEVEL FACT: MINI Israel price list dated 04/2026 lists current MINI Cooper Cabrio trims Cooper C, Cooper S and Cooper JCW; older Cooper/Cooper S rows ending 2024 must not be extended as-is.

#### VARIANT 66 / PROFILE 20.1
MODEL: IL-confirmed|Mini|Cabrio
CURRENT VALUE: version_or_trim='Cooper'; body_type='Convertible'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=115; transmission='cvt'; drivetrain='FWD'; year_start=2004; year_end=2008; support_level='direct'; source_indexes=[2099]
PROBLEM: Historical Mini Cabrio row with local historical sources.
WEB-VALIDATED FACT: MINI Israel price list dated 04/2026 lists current MINI Cooper Cabrio trims Cooper C, Cooper S and Cooper JCW; older Cooper/Cooper S rows ending 2024 must not be extended as-is.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep closed historical years.
ACTION: KEEP

#### VARIANT 67 / PROFILE 20.2
MODEL: IL-confirmed|Mini|Cabrio
CURRENT VALUE: version_or_trim='Cooper'; body_type='Convertible'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=122; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2009; year_end=2015; support_level='direct'; source_indexes=[2096]
PROBLEM: Historical Mini Cabrio row with local historical sources.
WEB-VALIDATED FACT: MINI Israel price list dated 04/2026 lists current MINI Cooper Cabrio trims Cooper C, Cooper S and Cooper JCW; older Cooper/Cooper S rows ending 2024 must not be extended as-is.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep closed historical years.
ACTION: KEEP

#### VARIANT 68 / PROFILE 20.3
MODEL: IL-confirmed|Mini|Cabrio
CURRENT VALUE: version_or_trim='Cooper S'; body_type='Convertible'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=184; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2009; year_end=2015; support_level='direct'; source_indexes=[2096]
PROBLEM: Historical Mini Cabrio row with local historical sources.
WEB-VALIDATED FACT: MINI Israel price list dated 04/2026 lists current MINI Cooper Cabrio trims Cooper C, Cooper S and Cooper JCW; older Cooper/Cooper S rows ending 2024 must not be extended as-is.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep closed historical years.
ACTION: KEEP

#### VARIANT 69 / PROFILE 20.4
MODEL: IL-confirmed|Mini|Cabrio
CURRENT VALUE: version_or_trim='Cooper'; body_type='Convertible'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=136; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2016; year_end=2018; support_level='direct'; source_indexes=[2095]
PROBLEM: Historical Mini Cabrio row with local historical sources.
WEB-VALIDATED FACT: MINI Israel price list dated 04/2026 lists current MINI Cooper Cabrio trims Cooper C, Cooper S and Cooper JCW; older Cooper/Cooper S rows ending 2024 must not be extended as-is.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep closed historical years.
ACTION: KEEP

#### VARIANT 70 / PROFILE 20.5
MODEL: IL-confirmed|Mini|Cabrio
CURRENT VALUE: version_or_trim='Cooper S'; body_type='Convertible'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=192; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2016; year_end=2018; support_level='direct'; source_indexes=[2095]
PROBLEM: Historical Mini Cabrio row with local historical sources.
WEB-VALIDATED FACT: MINI Israel price list dated 04/2026 lists current MINI Cooper Cabrio trims Cooper C, Cooper S and Cooper JCW; older Cooper/Cooper S rows ending 2024 must not be extended as-is.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep closed historical years.
ACTION: KEEP

#### VARIANT 71 / PROFILE 20.6
MODEL: IL-confirmed|Mini|Cabrio
CURRENT VALUE: version_or_trim='Cooper'; body_type='Convertible'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=136; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2018; year_end=2024; support_level='direct'; source_indexes=[2097]
PROBLEM: MINI Israel 04/2026 price list lists current Cooper C, Cooper S and Cooper JCW Cabrio; old Cooper/Cooper S rows ending 2024 must not be extended as-is with outdated trim naming/power.
WEB-VALIDATED FACT: MINI Israel price list dated 04/2026 lists current MINI Cooper Cabrio trims Cooper C, Cooper S and Cooper JCW; older Cooper/Cooper S rows ending 2024 must not be extended as-is.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep existing 2018-2024 rows as historical. Add or currentize 2026 Cooper C / Cooper S / Cooper JCW only if official spec/PDF or repo-local source grounds exact horsepower/transmission; otherwise move current gap to non-blocking review.
ACTION: FIX / MOVE TO REVIEW

#### VARIANT 72 / PROFILE 20.7
MODEL: IL-confirmed|Mini|Cabrio
CURRENT VALUE: version_or_trim='Cooper S'; body_type='Convertible'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=192; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2018; year_end=2021; support_level='direct'; source_indexes=[2097]
PROBLEM: MINI Israel 04/2026 price list lists current Cooper C, Cooper S and Cooper JCW Cabrio; old Cooper/Cooper S rows ending 2024 must not be extended as-is with outdated trim naming/power.
WEB-VALIDATED FACT: MINI Israel price list dated 04/2026 lists current MINI Cooper Cabrio trims Cooper C, Cooper S and Cooper JCW; older Cooper/Cooper S rows ending 2024 must not be extended as-is.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep existing 2018-2024 rows as historical. Add or currentize 2026 Cooper C / Cooper S / Cooper JCW only if official spec/PDF or repo-local source grounds exact horsepower/transmission; otherwise move current gap to non-blocking review.
ACTION: FIX / MOVE TO REVIEW

#### VARIANT 73 / PROFILE 20.8
MODEL: IL-confirmed|Mini|Cabrio
CURRENT VALUE: version_or_trim='Cooper S'; body_type='Convertible'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=178; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2021; year_end=2024; support_level='direct'; source_indexes=[2098]
PROBLEM: MINI Israel 04/2026 price list lists current Cooper C, Cooper S and Cooper JCW Cabrio; old Cooper/Cooper S rows ending 2024 must not be extended as-is with outdated trim naming/power.
WEB-VALIDATED FACT: MINI Israel price list dated 04/2026 lists current MINI Cooper Cabrio trims Cooper C, Cooper S and Cooper JCW; older Cooper/Cooper S rows ending 2024 must not be extended as-is.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep existing 2018-2024 rows as historical. Add or currentize 2026 Cooper C / Cooper S / Cooper JCW only if official spec/PDF or repo-local source grounds exact horsepower/transmission; otherwise move current gap to non-blocking review.
ACTION: FIX / MOVE TO REVIEW

#### VARIANT 74 / PROFILE 20.9
MODEL: IL-confirmed|Mini|Cabrio
CURRENT VALUE: version_or_trim='John Cooper Works'; body_type='Convertible'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=231; transmission='8-speed automatic'; drivetrain='FWD'; year_start=2019; year_end=2024; support_level='direct'; source_indexes=[2097]
PROBLEM: MINI Israel 04/2026 price list lists current Cooper C, Cooper S and Cooper JCW Cabrio; old Cooper/Cooper S rows ending 2024 must not be extended as-is with outdated trim naming/power.
WEB-VALIDATED FACT: MINI Israel price list dated 04/2026 lists current MINI Cooper Cabrio trims Cooper C, Cooper S and Cooper JCW; older Cooper/Cooper S rows ending 2024 must not be extended as-is.
SOURCE: repo-local sources listed in this profile plus RUN5 web anchors above.
TARGET VALUE: Keep existing 2018-2024 rows as historical. Add or currentize 2026 Cooper C / Cooper S / Cooper JCW only if official spec/PDF or repo-local source grounds exact horsepower/transmission; otherwise move current gap to non-blocking review.
ACTION: FIX / MOVE TO REVIEW

## Coverage assertion
RUN 5 contains 20 profiles and 74 technical variants. This task includes 74/74 explicit variant decisions.

## Report format after Codex run
Report: files changed, exact before/after metrics, confirmation all 20 profiles and 74 variants were handled, test results, confirmation temporary RUN5 instruction files were deleted before final commit, and remaining issues if any.

# ==============================
# RUN6
# source: BATCH26_RUN6_VARIANT_LEVEL_CODEX_TASK.md
# ==============================

# BATCH26 RUN 6 — VARIANT-LEVEL CODEX TASK

## Non-negotiable execution rules
Do not browse the internet. All web-validation facts needed for RUN 6 are embedded here. Use this task file as the single source of truth for RUN 6 only.
Apply RUN 6 only. Do not apply RUN 1, RUN 2, RUN 3, RUN 4, RUN 5, RUN 7, FINAL blockers, or any unified batch task.
If repo-local evidence conflicts with this task file, report the conflict instead of guessing. If a variant cannot be grounded, move it to non-blocking review/archive with reason and lineage rather than fabricating clean data.
Temporary-file cleanup is mandatory: before final commit, delete `codex_tasks/BATCH26_RUN6_*.md` unless the user explicitly asks to keep it.

## Scope
RUN 6 scope: `IL-confirmed|Mini|Clubman` through `IL-confirmed|Mitsubishi|Lancer`.
Profiles: 20. Technical variants: 78. Coverage: 78/78 variant-level decisions.

## Web/source anchors embedded for RUN 6
- MINI 04/2025 official price list: https://www.mini.co.il/content/dam/MINI/marketIL/mini_co_il/pdf/39306_Mechiron_Mini_Site_2025.pdf.asset.1743080474959.pdf
- MINI Israel official home/current models: https://www.mini.co.il/he_IL/home.html
- MINI Cooper Electric official technical PDF: https://www.mini.co.il/content/dam/MINI/marketIL/mini_co_il/technical-specs-2024/jul2024/241017%2038373%20%20MINI%20COOPER%20ELECTRIC.pdf.asset.1721550458387.pdf
- iCar Mini Cooper current price/spec listing: https://www.icar.co.il/מחירון_רכב/מחירון_מיני_קופר/
- Mitsubishi Israel current models: https://www.mitsubishi-israel.co.il/models/
- Mitsubishi Israel 2026 prices: https://www.mitsubishi-israel.co.il/prices/
- Mitsubishi Israel Eclipse Cross past model page: https://www.mitsubishi-israel.co.il/past_models/eclipse-cross/
- iCar Eclipse Cross PHEV 188 hp: https://www.icar.co.il/חדשות_רכב/מיצובישי_אקליפס_קרוס_-_עכשיו_גם_בגרסה_נטענת/
- iCar Attrage 1.2: https://www.icar.co.il/מיצובישי/מיצובישי_אטראז%27/מיצובישי_אטראז%27_יד_שניה_ד10/
- iCar L200/Triton 2.4 diesel launch: https://www.icar.co.il/חדשות_רכב/טנדר_חדש_בישראל:_מיצובישי_טרייטון,_מחליף_ההאנטר/
- iCar Lancer 1.5/1.8/1.6 context: https://www.icar.co.il/מיצובישי/מיצובישי_לאנסר/מיצובישי_לאנסר_חדש/

## Model-level facts
- **Mini Clubman**: Israeli MINI price list 04/2025 no longer lists Clubman, while older repo-local sources support Clubman 2008-2024. Treat Clubman as historical/closed; do not currentize beyond 2024.
- **Mini Cooper**: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
- **Mini Cooper S**: Cooper S is a trim/variant within MINI Cooper in the current Israeli price list, not a separate current clean model line. Historical Cooper S rows can be preserved, but duplicate current rows should be merged/aliased into canonical Mini Cooper policy.
- **Mini Cooper SE**: MINI Israel 04/2025 price list and official technical PDF support current Cooper Electric E and Cooper SE with displacement null, FWD and single-speed/direct-drive EV schema. It duplicates IL-likely Mini Cooper electric rows unless canonicalized.
- **Mini Countryman**: MINI Israel 04/2025 price list lists current Countryman C 1.5, Countryman JCW ALL4, and electric Countryman E. Existing older Cooper/Cooper S/Cooper SE ALL4 PHEV rows are historical; current rows must be explicitly named and grounded.
- **Mini Paceman**: Paceman is an old MINI Israel-market model; it is not in current MINI Israel price list. Keep historical only, do not reopen.
- **Mitsubishi 3000GT**: This profile is global-reference-only; no strong Israeli-market evidence was found for regular official local marketing. Do not keep as verified clean unless repo-local Israeli historical source proves local sale; otherwise archive non-blocking.
- **Mitsubishi ASX**: Mitsubishi Israel current 2026 price page lists ASX Intense, ASX Instyle and ASX Panoramic, so ASX is active/current in Israel. The global-reference-only ASX profile duplicates the IL-confirmed ASX profile and must merge/archive non-blocking.
- **Mitsubishi Attrage**: iCar Israeli sources support Attrage 2014-2021/2022 with 1.2 petrol, CVT and manual rows. It is not listed in Mitsubishi Israel current model/price pages, so keep historical only.
- **Mitsubishi Carisma**: Israeli historical sources support Carisma as late-1990s/early-2000s model. Keep historical only; trim null can remain only when repo policy permits old low-trim-confidence rows.
- **Mitsubishi Colt**: Israeli sources support Colt 2004-2012 1.3 Invite/Instyle rows. IL-likely Colt CZT needs merge/review; global-reference-only Colt duplicates IL rows and adds weak old 1993-2004 rows that should not remain separate clean without Israeli support.
- **Mitsubishi Eclipse Cross**: Mitsubishi Israel marks Eclipse Cross as past model 2017-2025; iCar has 2026 PHEV spec but official Mitsubishi current model/price pages emphasize Outlander/ASX. Keep through 2025; do not extend to current official clean without policy approval. PHEV row should use direct-drive/valid PHEV transmission if schema supports.
- **Mitsubishi Galant**: Israeli historical sources support Galant rows through 2008. Keep historical only; no current extension.
- **Mitsubishi i-MiEV**: Israeli historical EV support exists for i-MiEV; EV schema with displacement null and single_speed is valid. Keep historical only.
- **Mitsubishi L200**: Israeli sources support L200/Triton/Hunter historical pickup generations, including 2.4 diesel 154/181 hp and later 2.2 diesel 150 hp; it is not on Mitsubishi Israel current 2026 model/price page, so keep closed at 2024 unless repo-local current source exists.
- **Mitsubishi Lancer**: iCar Israeli sources support Lancer rows including 1.5 109 hp, 1.8 140 hp and later 1.6 117 hp. Keep historical only; no current extension.

## Required checks after implementation
```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```
Then audit actual generated files: clean catalog, readiness, review, archive, quality scan, compute_resume_state(), unmatched_output_keys, active blockers, cursor/resume state, duplicate/split alias cleanup.

## Variant-level instructions

### PROFILE 1: IL-confirmed|Mini|Clubman
MODEL-LEVEL FACT: Israeli MINI price list 04/2025 no longer lists Clubman, while older repo-local sources support Clubman 2008-2024. Treat Clubman as historical/closed; do not currentize beyond 2024.

#### VARIANT 1 / PROFILE 1.1
MODEL: IL-confirmed|Mini|Clubman
CURRENT VALUE: version_or_trim='Cooper'; body_type='Estate'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=120; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2008; year_end=2015; support_level='direct'; source_indexes=[1]
PROBLEM: Clubman is not listed in MINI Israel current 04/2025 price list; row must remain historical/closed and not be extended beyond 2024.
WEB-VALIDATED FACT: Israeli MINI price list 04/2025 no longer lists Clubman, while older repo-local sources support Clubman 2008-2024. Treat Clubman as historical/closed; do not currentize beyond 2024.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical row and year_end as-is; do not currentize Clubman. Ensure aliases/lineage are preserved for Clubman body style.
ACTION: KEEP

#### VARIANT 2 / PROFILE 1.2
MODEL: IL-confirmed|Mini|Clubman
CURRENT VALUE: version_or_trim='Cooper'; body_type='Estate'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=136; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2016; year_end=2018; support_level='direct'; source_indexes=[0]
PROBLEM: Clubman is not listed in MINI Israel current 04/2025 price list; row must remain historical/closed and not be extended beyond 2024.
WEB-VALIDATED FACT: Israeli MINI price list 04/2025 no longer lists Clubman, while older repo-local sources support Clubman 2008-2024. Treat Clubman as historical/closed; do not currentize beyond 2024.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical row and year_end as-is; do not currentize Clubman. Ensure aliases/lineage are preserved for Clubman body style.
ACTION: KEEP

#### VARIANT 3 / PROFILE 1.3
MODEL: IL-confirmed|Mini|Clubman
CURRENT VALUE: version_or_trim='Cooper'; body_type='Estate'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=136; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2019; year_end=2024; support_level='direct'; source_indexes=[0, 2]
PROBLEM: Clubman is not listed in MINI Israel current 04/2025 price list; row must remain historical/closed and not be extended beyond 2024.
WEB-VALIDATED FACT: Israeli MINI price list 04/2025 no longer lists Clubman, while older repo-local sources support Clubman 2008-2024. Treat Clubman as historical/closed; do not currentize beyond 2024.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical row and year_end as-is; do not currentize Clubman. Ensure aliases/lineage are preserved for Clubman body style.
ACTION: KEEP

#### VARIANT 4 / PROFILE 1.4
MODEL: IL-confirmed|Mini|Clubman
CURRENT VALUE: version_or_trim='Cooper S'; body_type='Estate'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=192; transmission='8-speed automatic'; drivetrain='FWD'; year_start=2016; year_end=2019; support_level='direct'; source_indexes=[0]
PROBLEM: Clubman is not listed in MINI Israel current 04/2025 price list; row must remain historical/closed and not be extended beyond 2024.
WEB-VALIDATED FACT: Israeli MINI price list 04/2025 no longer lists Clubman, while older repo-local sources support Clubman 2008-2024. Treat Clubman as historical/closed; do not currentize beyond 2024.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical row and year_end as-is; do not currentize Clubman. Ensure aliases/lineage are preserved for Clubman body style.
ACTION: KEEP

#### VARIANT 5 / PROFILE 1.5
MODEL: IL-confirmed|Mini|Clubman
CURRENT VALUE: version_or_trim='John Cooper Works'; body_type='Estate'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=306; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2020; year_end=2024; support_level='direct'; source_indexes=[0, 2]
PROBLEM: Clubman is not listed in MINI Israel current 04/2025 price list; row must remain historical/closed and not be extended beyond 2024.
WEB-VALIDATED FACT: Israeli MINI price list 04/2025 no longer lists Clubman, while older repo-local sources support Clubman 2008-2024. Treat Clubman as historical/closed; do not currentize beyond 2024.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical row and year_end as-is; do not currentize Clubman. Ensure aliases/lineage are preserved for Clubman body style.
ACTION: KEEP

### PROFILE 2: IL-confirmed|Mini|Cooper
MODEL-LEVEL FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.

#### VARIANT 6 / PROFILE 2.1
MODEL: IL-confirmed|Mini|Cooper
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L 4-cyl'; engine_displacement_l=1.6; horsepower_hp=115; transmission='cvt'; drivetrain='FWD'; year_start=2001; year_end=2006; support_level='direct'; source_indexes=[2064]
PROBLEM: Historical Cooper row has null trim even though it represents Cooper/Cooper C lineage; current catalog uses explicit Cooper C/Cooper S/JCW naming.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep years/hp/transmission as historical, but set a normalized trim/lineage label such as Cooper or Cooper C where repo policy permits. Do not reopen to current without adding separate 2024+ Cooper C row.
ACTION: FIX

#### VARIANT 7 / PROFILE 2.2
MODEL: IL-confirmed|Mini|Cooper
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L 4-cyl'; engine_displacement_l=1.6; horsepower_hp=120; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2007; year_end=2013; support_level='direct'; source_indexes=[2067]
PROBLEM: Historical Cooper row has null trim even though it represents Cooper/Cooper C lineage; current catalog uses explicit Cooper C/Cooper S/JCW naming.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep years/hp/transmission as historical, but set a normalized trim/lineage label such as Cooper or Cooper C where repo policy permits. Do not reopen to current without adding separate 2024+ Cooper C row.
ACTION: FIX

#### VARIANT 8 / PROFILE 2.3
MODEL: IL-confirmed|Mini|Cooper
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.5L 3-cyl turbo'; engine_displacement_l=1.5; horsepower_hp=136; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2014; year_end=2017; support_level='direct'; source_indexes=[2063]
PROBLEM: Historical Cooper row has null trim even though it represents Cooper/Cooper C lineage; current catalog uses explicit Cooper C/Cooper S/JCW naming.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep years/hp/transmission as historical, but set a normalized trim/lineage label such as Cooper or Cooper C where repo policy permits. Do not reopen to current without adding separate 2024+ Cooper C row.
ACTION: FIX

#### VARIANT 9 / PROFILE 2.4
MODEL: IL-confirmed|Mini|Cooper
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.5L 3-cyl turbo'; engine_displacement_l=1.5; horsepower_hp=136; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2018; year_end=2023; support_level='direct'; source_indexes=[2063]
PROBLEM: Historical Cooper row has null trim even though it represents Cooper/Cooper C lineage; current catalog uses explicit Cooper C/Cooper S/JCW naming.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep years/hp/transmission as historical, but set a normalized trim/lineage label such as Cooper or Cooper C where repo policy permits. Do not reopen to current without adding separate 2024+ Cooper C row.
ACTION: FIX

#### VARIANT 10 / PROFILE 2.5
MODEL: IL-confirmed|Mini|Cooper
CURRENT VALUE: version_or_trim='S'; body_type='Hatchback'; fuel_type='petrol'; engine='2.0L 4-cyl turbo'; engine_displacement_l=2.0; horsepower_hp=192; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2014; year_end=2017; support_level='direct'; source_indexes=[2065]
PROBLEM: S rows duplicate Mini Cooper S profile; current MINI Israel treats Cooper S as trim inside Cooper, not a separate current model.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep a single canonical representation for Cooper S rows, preferably under Mini Cooper with trim Cooper S. Merge/alias duplicate Mini Cooper S profile rows with lineage.
ACTION: MERGE / ALIAS

#### VARIANT 11 / PROFILE 2.6
MODEL: IL-confirmed|Mini|Cooper
CURRENT VALUE: version_or_trim='S'; body_type='Hatchback'; fuel_type='petrol'; engine='2.0L 4-cyl turbo'; engine_displacement_l=2.0; horsepower_hp=192; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2018; year_end=2023; support_level='direct'; source_indexes=[2065]
PROBLEM: S rows duplicate Mini Cooper S profile; current MINI Israel treats Cooper S as trim inside Cooper, not a separate current model.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep a single canonical representation for Cooper S rows, preferably under Mini Cooper with trim Cooper S. Merge/alias duplicate Mini Cooper S profile rows with lineage.
ACTION: MERGE / ALIAS

#### VARIANT 12 / PROFILE 2.7
MODEL: IL-confirmed|Mini|Cooper
CURRENT VALUE: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='1.5L 3-cyl turbo'; engine_displacement_l=1.5; horsepower_hp=136; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2018; year_end=2023; support_level='direct'; source_indexes=[2066]
PROBLEM: Convertible Cooper row is stored inside Mini Cooper even though Cabrio is a separate profile handled in RUN5; this can create duplicate model-line placement.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Move/merge this convertible row to canonical Mini Cabrio profile or add alias/lineage. Do not leave duplicate Cooper Cabrio row under both Cooper and Cabrio.
ACTION: MOVE / MERGE

### PROFILE 3: IL-likely|Mini|Cooper
MODEL-LEVEL FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.

#### VARIANT 13 / PROFILE 3.1
MODEL: IL-likely|Mini|Cooper
CURRENT VALUE: version_or_trim='SE Passion'; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=184; transmission='single_speed'; drivetrain='FWD'; year_start=2020; year_end=2023; support_level='direct'; source_indexes=[2]
PROBLEM: Current MINI Israel price list has 2024/2025 Cooper C, Cooper S and JCW rows; this profile currently mostly stops in 2023.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Add/currentize 2024+ Cooper C 1.5, Cooper S 2.0 and JCW 2.0 only if repo-local exact specs are attached; otherwise add non-blocking review for current gap.
ACTION: FIX / ADD

#### VARIANT 14 / PROFILE 3.2
MODEL: IL-likely|Mini|Cooper
CURRENT VALUE: version_or_trim='SE Legend'; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=184; transmission='single_speed'; drivetrain='FWD'; year_start=2020; year_end=2023; support_level='direct'; source_indexes=[2]
PROBLEM: Current MINI Israel price list has 2024/2025 Cooper C, Cooper S and JCW rows; this profile currently mostly stops in 2023.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Add/currentize 2024+ Cooper C 1.5, Cooper S 2.0 and JCW 2.0 only if repo-local exact specs are attached; otherwise add non-blocking review for current gap.
ACTION: FIX / ADD

#### VARIANT 15 / PROFILE 3.3
MODEL: IL-likely|Mini|Cooper
CURRENT VALUE: version_or_trim='E Classic'; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=184; transmission='single_speed'; drivetrain='FWD'; year_start=2024; year_end=None; support_level='direct'; source_indexes=[1]
PROBLEM: Current MINI Israel price list has 2024/2025 Cooper C, Cooper S and JCW rows; this profile currently mostly stops in 2023.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Add/currentize 2024+ Cooper C 1.5, Cooper S 2.0 and JCW 2.0 only if repo-local exact specs are attached; otherwise add non-blocking review for current gap.
ACTION: FIX / ADD

#### VARIANT 16 / PROFILE 3.4
MODEL: IL-likely|Mini|Cooper
CURRENT VALUE: version_or_trim='E Favoured'; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=184; transmission='single_speed'; drivetrain='FWD'; year_start=2024; year_end=None; support_level='direct'; source_indexes=[1]
PROBLEM: Current MINI Israel price list has 2024/2025 Cooper C, Cooper S and JCW rows; this profile currently mostly stops in 2023.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Add/currentize 2024+ Cooper C 1.5, Cooper S 2.0 and JCW 2.0 only if repo-local exact specs are attached; otherwise add non-blocking review for current gap.
ACTION: FIX / ADD

#### VARIANT 17 / PROFILE 3.5
MODEL: IL-likely|Mini|Cooper
CURRENT VALUE: version_or_trim='SE Favoured'; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=218; transmission='single_speed'; drivetrain='FWD'; year_start=2024; year_end=None; support_level='direct'; source_indexes=[1]
PROBLEM: Current MINI Israel price list has 2024/2025 Cooper C, Cooper S and JCW rows; this profile currently mostly stops in 2023.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Add/currentize 2024+ Cooper C 1.5, Cooper S 2.0 and JCW 2.0 only if repo-local exact specs are attached; otherwise add non-blocking review for current gap.
ACTION: FIX / ADD

#### VARIANT 18 / PROFILE 3.6
MODEL: IL-likely|Mini|Cooper
CURRENT VALUE: version_or_trim='SE JCW'; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=218; transmission='single_speed'; drivetrain='FWD'; year_start=2024; year_end=None; support_level='direct'; source_indexes=[1]
PROBLEM: Current MINI Israel price list has 2024/2025 Cooper C, Cooper S and JCW rows; this profile currently mostly stops in 2023.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Cooper 3-door/5-door: Cooper C 1.5, Cooper S 2.0, JCW 2.0, plus Cooper Electric E/SE. Old null-trim rows through 2023 should remain historical; current 2024+ rows must use Cooper C/Cooper S/JCW naming rather than null trim.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Add/currentize 2024+ Cooper C 1.5, Cooper S 2.0 and JCW 2.0 only if repo-local exact specs are attached; otherwise add non-blocking review for current gap.
ACTION: FIX / ADD

### PROFILE 4: IL-confirmed|Mini|Cooper S
MODEL-LEVEL FACT: Cooper S is a trim/variant within MINI Cooper in the current Israeli price list, not a separate current clean model line. Historical Cooper S rows can be preserved, but duplicate current rows should be merged/aliased into canonical Mini Cooper policy.

#### VARIANT 19 / PROFILE 4.1
MODEL: IL-confirmed|Mini|Cooper S
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L supercharged'; engine_displacement_l=1.6; horsepower_hp=163; transmission='6-speed manual'; drivetrain='FWD'; year_start=2002; year_end=2004; support_level='direct'; source_indexes=[0]
PROBLEM: Mini Cooper S is technically a Cooper trim/variant and duplicates S rows already present under Mini Cooper.
WEB-VALIDATED FACT: Cooper S is a trim/variant within MINI Cooper in the current Israeli price list, not a separate current clean model line. Historical Cooper S rows can be preserved, but duplicate current rows should be merged/aliased into canonical Mini Cooper policy.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Merge into canonical Mini Cooper profile as Cooper S trim or keep separate only if repo policy explicitly uses model splits; in all cases remove duplicate clean technical rows and preserve aliases/lineage.
ACTION: MERGE / ALIAS

#### VARIANT 20 / PROFILE 4.2
MODEL: IL-confirmed|Mini|Cooper S
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=175; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2007; year_end=2010; support_level='direct'; source_indexes=[1]
PROBLEM: Mini Cooper S is technically a Cooper trim/variant and duplicates S rows already present under Mini Cooper.
WEB-VALIDATED FACT: Cooper S is a trim/variant within MINI Cooper in the current Israeli price list, not a separate current clean model line. Historical Cooper S rows can be preserved, but duplicate current rows should be merged/aliased into canonical Mini Cooper policy.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Merge into canonical Mini Cooper profile as Cooper S trim or keep separate only if repo policy explicitly uses model splits; in all cases remove duplicate clean technical rows and preserve aliases/lineage.
ACTION: MERGE / ALIAS

#### VARIANT 21 / PROFILE 4.3
MODEL: IL-confirmed|Mini|Cooper S
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=184; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2010; year_end=2014; support_level='direct'; source_indexes=[1]
PROBLEM: Mini Cooper S is technically a Cooper trim/variant and duplicates S rows already present under Mini Cooper.
WEB-VALIDATED FACT: Cooper S is a trim/variant within MINI Cooper in the current Israeli price list, not a separate current clean model line. Historical Cooper S rows can be preserved, but duplicate current rows should be merged/aliased into canonical Mini Cooper policy.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Merge into canonical Mini Cooper profile as Cooper S trim or keep separate only if repo policy explicitly uses model splits; in all cases remove duplicate clean technical rows and preserve aliases/lineage.
ACTION: MERGE / ALIAS

#### VARIANT 22 / PROFILE 4.4
MODEL: IL-confirmed|Mini|Cooper S
CURRENT VALUE: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=184; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2010; year_end=2015; support_level='direct'; source_indexes=[2]
PROBLEM: Mini Cooper S is technically a Cooper trim/variant and duplicates S rows already present under Mini Cooper.
WEB-VALIDATED FACT: Cooper S is a trim/variant within MINI Cooper in the current Israeli price list, not a separate current clean model line. Historical Cooper S rows can be preserved, but duplicate current rows should be merged/aliased into canonical Mini Cooper policy.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Merge into canonical Mini Cooper profile as Cooper S trim or keep separate only if repo policy explicitly uses model splits; in all cases remove duplicate clean technical rows and preserve aliases/lineage.
ACTION: MERGE / ALIAS

#### VARIANT 23 / PROFILE 4.5
MODEL: IL-confirmed|Mini|Cooper S
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=192; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2014; year_end=2018; support_level='direct'; source_indexes=[3]
PROBLEM: Mini Cooper S is technically a Cooper trim/variant and duplicates S rows already present under Mini Cooper.
WEB-VALIDATED FACT: Cooper S is a trim/variant within MINI Cooper in the current Israeli price list, not a separate current clean model line. Historical Cooper S rows can be preserved, but duplicate current rows should be merged/aliased into canonical Mini Cooper policy.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Merge into canonical Mini Cooper profile as Cooper S trim or keep separate only if repo policy explicitly uses model splits; in all cases remove duplicate clean technical rows and preserve aliases/lineage.
ACTION: MERGE / ALIAS

#### VARIANT 24 / PROFILE 4.6
MODEL: IL-confirmed|Mini|Cooper S
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=192; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2018; year_end=2023; support_level='direct'; source_indexes=[4]
PROBLEM: Mini Cooper S is technically a Cooper trim/variant and duplicates S rows already present under Mini Cooper.
WEB-VALIDATED FACT: Cooper S is a trim/variant within MINI Cooper in the current Israeli price list, not a separate current clean model line. Historical Cooper S rows can be preserved, but duplicate current rows should be merged/aliased into canonical Mini Cooper policy.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Merge into canonical Mini Cooper profile as Cooper S trim or keep separate only if repo policy explicitly uses model splits; in all cases remove duplicate clean technical rows and preserve aliases/lineage.
ACTION: MERGE / ALIAS

#### VARIANT 25 / PROFILE 4.7
MODEL: IL-confirmed|Mini|Cooper S
CURRENT VALUE: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=192; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2018; year_end=2023; support_level='direct'; source_indexes=[4]
PROBLEM: Mini Cooper S is technically a Cooper trim/variant and duplicates S rows already present under Mini Cooper.
WEB-VALIDATED FACT: Cooper S is a trim/variant within MINI Cooper in the current Israeli price list, not a separate current clean model line. Historical Cooper S rows can be preserved, but duplicate current rows should be merged/aliased into canonical Mini Cooper policy.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Merge into canonical Mini Cooper profile as Cooper S trim or keep separate only if repo policy explicitly uses model splits; in all cases remove duplicate clean technical rows and preserve aliases/lineage.
ACTION: MERGE / ALIAS

#### VARIANT 26 / PROFILE 4.8
MODEL: IL-confirmed|Mini|Cooper S
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=204; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2024; year_end=2024; support_level='direct'; source_indexes=[5]
PROBLEM: Mini Cooper S is technically a Cooper trim/variant and duplicates S rows already present under Mini Cooper. The 2024 204 hp row is current/new-generation and should be represented as Cooper S Favorite/Cooper S, not a standalone duplicated model.
WEB-VALIDATED FACT: Cooper S is a trim/variant within MINI Cooper in the current Israeli price list, not a separate current clean model line. Historical Cooper S rows can be preserved, but duplicate current rows should be merged/aliased into canonical Mini Cooper policy.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Merge into canonical Mini Cooper profile as Cooper S trim or keep separate only if repo policy explicitly uses model splits; in all cases remove duplicate clean technical rows and preserve aliases/lineage. For current row, normalize to Cooper S Favorite if local price/spec source is attached.
ACTION: MERGE / ALIAS

### PROFILE 5: IL-confirmed|Mini|Cooper SE
MODEL-LEVEL FACT: MINI Israel 04/2025 price list and official technical PDF support current Cooper Electric E and Cooper SE with displacement null, FWD and single-speed/direct-drive EV schema. It duplicates IL-likely Mini Cooper electric rows unless canonicalized.

#### VARIANT 27 / PROFILE 5.1
MODEL: IL-confirmed|Mini|Cooper SE
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=184; transmission='single_speed'; drivetrain='FWD'; year_start=2020; year_end=2024; support_level='direct'; source_indexes=[0, 2]
PROBLEM: Cooper SE rows duplicate IL-likely Mini Cooper electric rows and current price list stores Cooper Electric E/SE under Cooper Electric/Cooper, not necessarily a separate clean model.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list and official technical PDF support current Cooper Electric E and Cooper SE with displacement null, FWD and single-speed/direct-drive EV schema. It duplicates IL-likely Mini Cooper electric rows unless canonicalized.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Choose one canonical representation for Cooper Electric E/SE. Merge old 2020-2024 184 hp SE and current 2024+ 218 hp SE with IL-likely Mini Cooper EV rows; preserve alias Cooper SE. Ensure EV schema displacement null + single_speed/direct_drive + FWD.
ACTION: MERGE / ALIAS

#### VARIANT 28 / PROFILE 5.2
MODEL: IL-confirmed|Mini|Cooper SE
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=218; transmission='single_speed'; drivetrain='FWD'; year_start=2024; year_end=None; support_level='direct'; source_indexes=[1, 2]
PROBLEM: Cooper SE rows duplicate IL-likely Mini Cooper electric rows and current price list stores Cooper Electric E/SE under Cooper Electric/Cooper, not necessarily a separate clean model.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list and official technical PDF support current Cooper Electric E and Cooper SE with displacement null, FWD and single-speed/direct-drive EV schema. It duplicates IL-likely Mini Cooper electric rows unless canonicalized.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Choose one canonical representation for Cooper Electric E/SE. Merge old 2020-2024 184 hp SE and current 2024+ 218 hp SE with IL-likely Mini Cooper EV rows; preserve alias Cooper SE. Ensure EV schema displacement null + single_speed/direct_drive + FWD.
ACTION: MERGE / ALIAS

### PROFILE 6: IL-confirmed|Mini|Countryman
MODEL-LEVEL FACT: MINI Israel 04/2025 price list lists current Countryman C 1.5, Countryman JCW ALL4, and electric Countryman E. Existing older Cooper/Cooper S/Cooper SE ALL4 PHEV rows are historical; current rows must be explicitly named and grounded.

#### VARIANT 29 / PROFILE 6.1
MODEL: IL-confirmed|Mini|Countryman
CURRENT VALUE: version_or_trim='Cooper'; body_type='SUV'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=122; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2010; year_end=2016; support_level='direct'; source_indexes=[0]
PROBLEM: Current price list also lists Countryman JCW ALL4 and electric Countryman E, but these are missing from the profile as current rows.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Countryman C 1.5, Countryman JCW ALL4, and electric Countryman E. Existing older Cooper/Cooper S/Cooper SE ALL4 PHEV rows are historical; current rows must be explicitly named and grounded.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Add non-blocking current-gap review or add grounded rows for Countryman JCW ALL4 and Countryman E if exact specs are present in repo-local sources. Do not fabricate horsepower.
ACTION: ADD / FIX

#### VARIANT 30 / PROFILE 6.2
MODEL: IL-confirmed|Mini|Countryman
CURRENT VALUE: version_or_trim='Cooper S'; body_type='SUV'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=184; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2010; year_end=2016; support_level='direct'; source_indexes=[0]
PROBLEM: Current price list also lists Countryman JCW ALL4 and electric Countryman E, but these are missing from the profile as current rows.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Countryman C 1.5, Countryman JCW ALL4, and electric Countryman E. Existing older Cooper/Cooper S/Cooper SE ALL4 PHEV rows are historical; current rows must be explicitly named and grounded.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Add non-blocking current-gap review or add grounded rows for Countryman JCW ALL4 and Countryman E if exact specs are present in repo-local sources. Do not fabricate horsepower.
ACTION: ADD / FIX

#### VARIANT 31 / PROFILE 6.3
MODEL: IL-confirmed|Mini|Countryman
CURRENT VALUE: version_or_trim='Cooper'; body_type='SUV'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=136; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2017; year_end=2023; support_level='direct'; source_indexes=[1]
PROBLEM: Older Countryman generation row; current 04/2025 price list uses Countryman C/JCW and Countryman Electric E naming, so old Cooper/Cooper S/Cooper SE PHEV rows must stay historical.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Countryman C 1.5, Countryman JCW ALL4, and electric Countryman E. Existing older Cooper/Cooper S/Cooper SE ALL4 PHEV rows are historical; current rows must be explicitly named and grounded.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep row closed at 2023; do not extend to current generation.
ACTION: KEEP

#### VARIANT 32 / PROFILE 6.4
MODEL: IL-confirmed|Mini|Countryman
CURRENT VALUE: version_or_trim='Cooper S'; body_type='SUV'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=192; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2017; year_end=2023; support_level='direct'; source_indexes=[1]
PROBLEM: Older Countryman generation row; current 04/2025 price list uses Countryman C/JCW and Countryman Electric E naming, so old Cooper/Cooper S/Cooper SE PHEV rows must stay historical.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Countryman C 1.5, Countryman JCW ALL4, and electric Countryman E. Existing older Cooper/Cooper S/Cooper SE ALL4 PHEV rows are historical; current rows must be explicitly named and grounded.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep row closed at 2023; do not extend to current generation.
ACTION: KEEP

#### VARIANT 33 / PROFILE 6.5
MODEL: IL-confirmed|Mini|Countryman
CURRENT VALUE: version_or_trim='Cooper SE ALL4'; body_type='SUV'; fuel_type='plug_in_hybrid'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=224; transmission='6-speed automatic'; drivetrain='AWD'; year_start=2017; year_end=2023; support_level='direct'; source_indexes=[1]
PROBLEM: Older Countryman generation row; current 04/2025 price list uses Countryman C/JCW and Countryman Electric E naming, so old Cooper/Cooper S/Cooper SE PHEV rows must stay historical.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Countryman C 1.5, Countryman JCW ALL4, and electric Countryman E. Existing older Cooper/Cooper S/Cooper SE ALL4 PHEV rows are historical; current rows must be explicitly named and grounded.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep row closed at 2023; do not extend to current generation.
ACTION: KEEP

#### VARIANT 34 / PROFILE 6.6
MODEL: IL-confirmed|Mini|Countryman
CURRENT VALUE: version_or_trim='Countryman C'; body_type='SUV'; fuel_type='mild_hybrid'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=170; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2024; year_end=2024; support_level='direct'; source_indexes=[2]
PROBLEM: MINI Israel 04/2025 price list lists Countryman C as current; row is closed at 2024.
WEB-VALIDATED FACT: MINI Israel 04/2025 price list lists current Countryman C 1.5, Countryman JCW ALL4, and electric Countryman E. Existing older Cooper/Cooper S/Cooper SE ALL4 PHEV rows are historical; current rows must be explicitly named and grounded.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Set year_end null/current for Countryman C only if source_indexes/field_sources attach official MINI price/spec support; keep 1.5L/170 hp mild-hybrid data only if locally grounded.
ACTION: FIX

### PROFILE 7: IL-confirmed|Mini|Paceman
MODEL-LEVEL FACT: Paceman is an old MINI Israel-market model; it is not in current MINI Israel price list. Keep historical only, do not reopen.

#### VARIANT 35 / PROFILE 7.1
MODEL: IL-confirmed|Mini|Paceman
CURRENT VALUE: version_or_trim='Cooper'; body_type='Crossover'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=122; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2013; year_end=2016; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Paceman is historical only and absent from current MINI Israel price list.
WEB-VALIDATED FACT: Paceman is an old MINI Israel-market model; it is not in current MINI Israel price list. Keep historical only, do not reopen.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep closed historical row; do not currentize.
ACTION: KEEP

#### VARIANT 36 / PROFILE 7.2
MODEL: IL-confirmed|Mini|Paceman
CURRENT VALUE: version_or_trim='Cooper S'; body_type='Crossover'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=184; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2013; year_end=2016; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Paceman is historical only and absent from current MINI Israel price list.
WEB-VALIDATED FACT: Paceman is an old MINI Israel-market model; it is not in current MINI Israel price list. Keep historical only, do not reopen.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep closed historical row; do not currentize.
ACTION: KEEP

### PROFILE 8: global-reference-only|Mitsubishi|3000GT
MODEL-LEVEL FACT: This profile is global-reference-only; no strong Israeli-market evidence was found for regular official local marketing. Do not keep as verified clean unless repo-local Israeli historical source proves local sale; otherwise archive non-blocking.

#### VARIANT 37 / PROFILE 8.1
MODEL: global-reference-only|Mitsubishi|3000GT
CURRENT VALUE: version_or_trim='VR-4'; body_type='Coupe'; fuel_type='petrol'; engine='3.0L twin turbo v6'; engine_displacement_l=3.0; horsepower_hp=300; transmission='manual'; drivetrain='AWD'; year_start=1992; year_end=1999; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Profile is global-reference-only and no strong Israeli-market official/source evidence is embedded for regular local sale.
WEB-VALIDATED FACT: This profile is global-reference-only; no strong Israeli-market evidence was found for regular official local marketing. Do not keep as verified clean unless repo-local Israeli historical source proves local sale; otherwise archive non-blocking.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Move to non-blocking archive/review with reason=global_reference_only_no_strong_il_grounding unless repo-local Israeli historical source proves local marketing. Preserve lineage.
ACTION: ARCHIVE NON-BLOCKING / MOVE TO REVIEW

#### VARIANT 38 / PROFILE 8.2
MODEL: global-reference-only|Mitsubishi|3000GT
CURRENT VALUE: version_or_trim='SL'; body_type='Coupe'; fuel_type='petrol'; engine='3.0L v6'; engine_displacement_l=3.0; horsepower_hp=225; transmission='manual'; drivetrain='FWD'; year_start=1992; year_end=1999; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Profile is global-reference-only and no strong Israeli-market official/source evidence is embedded for regular local sale.
WEB-VALIDATED FACT: This profile is global-reference-only; no strong Israeli-market evidence was found for regular official local marketing. Do not keep as verified clean unless repo-local Israeli historical source proves local sale; otherwise archive non-blocking.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Move to non-blocking archive/review with reason=global_reference_only_no_strong_il_grounding unless repo-local Israeli historical source proves local marketing. Preserve lineage.
ACTION: ARCHIVE NON-BLOCKING / MOVE TO REVIEW

### PROFILE 9: global-reference-only|Mitsubishi|ASX
MODEL-LEVEL FACT: Mitsubishi Israel current 2026 price page lists ASX Intense, ASX Instyle and ASX Panoramic, so ASX is active/current in Israel. The global-reference-only ASX profile duplicates the IL-confirmed ASX profile and must merge/archive non-blocking.

#### VARIANT 39 / PROFILE 9.1
MODEL: global-reference-only|Mitsubishi|ASX
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='2.0L'; engine_displacement_l=2.0; horsepower_hp=150; transmission='cvt'; drivetrain='FWD'; year_start=2017; year_end=2024; support_level='direct'; source_indexes=[0, 1, 2]
PROBLEM: Global-reference-only ASX duplicates IL-confirmed ASX.
WEB-VALIDATED FACT: Mitsubishi Israel current 2026 price page lists ASX Intense, ASX Instyle and ASX Panoramic, so ASX is active/current in Israel. The global-reference-only ASX profile duplicates the IL-confirmed ASX profile and must merge/archive non-blocking.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Merge into IL-confirmed Mitsubishi ASX and archive this duplicate profile non-blocking with lineage.
ACTION: MERGE / ARCHIVE NON-BLOCKING

### PROFILE 10: IL-confirmed|Mitsubishi|ASX
MODEL-LEVEL FACT: Mitsubishi Israel current 2026 price page lists ASX Intense, ASX Instyle and ASX Panoramic, so ASX is active/current in Israel. The global-reference-only ASX profile duplicates the IL-confirmed ASX profile and must merge/archive non-blocking.

#### VARIANT 40 / PROFILE 10.1
MODEL: IL-confirmed|Mitsubishi|ASX
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='2.0L'; engine_displacement_l=2.0; horsepower_hp=150; transmission='cvt'; drivetrain='FWD'; year_start=2017; year_end=2025; support_level='direct'; source_indexes=[1273, 1274]
PROBLEM: Mitsubishi Israel 2026 price page lists ASX Intense/Instyle/Panoramic as current; IL-confirmed row has trim null and year_end 2025.
WEB-VALIDATED FACT: Mitsubishi Israel current 2026 price page lists ASX Intense, ASX Instyle and ASX Panoramic, so ASX is active/current in Israel. The global-reference-only ASX profile duplicates the IL-confirmed ASX profile and must merge/archive non-blocking.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Set current/year_end null only when exact local source is attached; split/alias trim coverage to ASX Intense, ASX Instyle, ASX Panoramic if website requires trim rows. Keep 2.0L 150 hp CVT/FWD only if source supports.
ACTION: FIX

### PROFILE 11: IL-confirmed|Mitsubishi|Attrage
MODEL-LEVEL FACT: iCar Israeli sources support Attrage 2014-2021/2022 with 1.2 petrol, CVT and manual rows. It is not listed in Mitsubishi Israel current model/price pages, so keep historical only.

#### VARIANT 41 / PROFILE 11.1
MODEL: IL-confirmed|Mitsubishi|Attrage
CURRENT VALUE: version_or_trim='Instyle'; body_type='Sedan'; fuel_type='petrol'; engine='1.2L'; engine_displacement_l=1.2; horsepower_hp=80; transmission='cvt'; drivetrain='FWD'; year_start=2014; year_end=2022; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Attrage is Israeli-market historical; it is not on current Mitsubishi Israel model/price pages.
WEB-VALIDATED FACT: iCar Israeli sources support Attrage 2014-2021/2022 with 1.2 petrol, CVT and manual rows. It is not listed in Mitsubishi Israel current model/price pages, so keep historical only.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical 2014-2022 CVT/Instyle and 2014-2019 manual/Invite rows. Do not currentize.
ACTION: KEEP

#### VARIANT 42 / PROFILE 11.2
MODEL: IL-confirmed|Mitsubishi|Attrage
CURRENT VALUE: version_or_trim='Invite'; body_type='Sedan'; fuel_type='petrol'; engine='1.2L'; engine_displacement_l=1.2; horsepower_hp=80; transmission='5-speed manual'; drivetrain='FWD'; year_start=2014; year_end=2019; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Attrage is Israeli-market historical; it is not on current Mitsubishi Israel model/price pages.
WEB-VALIDATED FACT: iCar Israeli sources support Attrage 2014-2021/2022 with 1.2 petrol, CVT and manual rows. It is not listed in Mitsubishi Israel current model/price pages, so keep historical only.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical 2014-2022 CVT/Instyle and 2014-2019 manual/Invite rows. Do not currentize.
ACTION: KEEP

### PROFILE 12: IL-confirmed|Mitsubishi|Carisma
MODEL-LEVEL FACT: Israeli historical sources support Carisma as late-1990s/early-2000s model. Keep historical only; trim null can remain only when repo policy permits old low-trim-confidence rows.

#### VARIANT 43 / PROFILE 12.1
MODEL: IL-confirmed|Mitsubishi|Carisma
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=100; transmission='4-speed automatic'; drivetrain='FWD'; year_start=1998; year_end=2004; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Carisma is historical; row has trim null but this may be acceptable for older low-trim-confidence rows if source_indexes are valid.
WEB-VALIDATED FACT: Israeli historical sources support Carisma as late-1990s/early-2000s model. Keep historical only; trim null can remain only when repo policy permits old low-trim-confidence rows.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical years and fields; only add trim/lineage if repo-local source supports it. Do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 44 / PROFILE 12.2
MODEL: IL-confirmed|Mitsubishi|Carisma
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=100; transmission='4-speed automatic'; drivetrain='FWD'; year_start=1998; year_end=2004; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Carisma is historical; row has trim null but this may be acceptable for older low-trim-confidence rows if source_indexes are valid.
WEB-VALIDATED FACT: Israeli historical sources support Carisma as late-1990s/early-2000s model. Keep historical only; trim null can remain only when repo policy permits old low-trim-confidence rows.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical years and fields; only add trim/lineage if repo-local source supports it. Do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 45 / PROFILE 12.3
MODEL: IL-confirmed|Mitsubishi|Carisma
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.8L'; engine_displacement_l=1.8; horsepower_hp=125; transmission='4-speed automatic'; drivetrain='FWD'; year_start=1998; year_end=2004; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Carisma is historical; row has trim null but this may be acceptable for older low-trim-confidence rows if source_indexes are valid.
WEB-VALIDATED FACT: Israeli historical sources support Carisma as late-1990s/early-2000s model. Keep historical only; trim null can remain only when repo policy permits old low-trim-confidence rows.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical years and fields; only add trim/lineage if repo-local source supports it. Do not currentize.
ACTION: KEEP / FIX SOURCE

### PROFILE 13: IL-confirmed|Mitsubishi|Colt
MODEL-LEVEL FACT: Israeli sources support Colt 2004-2012 1.3 Invite/Instyle rows. IL-likely Colt CZT needs merge/review; global-reference-only Colt duplicates IL rows and adds weak old 1993-2004 rows that should not remain separate clean without Israeli support.

#### VARIANT 46 / PROFILE 13.1
MODEL: IL-confirmed|Mitsubishi|Colt
CURRENT VALUE: version_or_trim='Instyle'; body_type='Hatchback'; fuel_type='petrol'; engine='1.3L'; engine_displacement_l=1.3; horsepower_hp=95; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2004; year_end=2012; support_level='direct'; source_indexes=[0, 1]
PROBLEM: IL-confirmed Colt 2004-2012 Invite/Instyle rows are Israeli-grounded historical rows.
WEB-VALIDATED FACT: Israeli sources support Colt 2004-2012 1.3 Invite/Instyle rows. IL-likely Colt CZT needs merge/review; global-reference-only Colt duplicates IL rows and adds weak old 1993-2004 rows that should not remain separate clean without Israeli support.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical row; do not currentize.
ACTION: KEEP

#### VARIANT 47 / PROFILE 13.2
MODEL: IL-confirmed|Mitsubishi|Colt
CURRENT VALUE: version_or_trim='Invite'; body_type='Hatchback'; fuel_type='petrol'; engine='1.3L'; engine_displacement_l=1.3; horsepower_hp=95; transmission='5-speed manual'; drivetrain='FWD'; year_start=2004; year_end=2012; support_level='direct'; source_indexes=[0]
PROBLEM: IL-confirmed Colt 2004-2012 Invite/Instyle rows are Israeli-grounded historical rows.
WEB-VALIDATED FACT: Israeli sources support Colt 2004-2012 1.3 Invite/Instyle rows. IL-likely Colt CZT needs merge/review; global-reference-only Colt duplicates IL rows and adds weak old 1993-2004 rows that should not remain separate clean without Israeli support.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical row; do not currentize.
ACTION: KEEP

### PROFILE 14: IL-likely|Mitsubishi|Colt
MODEL-LEVEL FACT: Israeli sources support Colt 2004-2012 1.3 Invite/Instyle rows. IL-likely Colt CZT needs merge/review; global-reference-only Colt duplicates IL rows and adds weak old 1993-2004 rows that should not remain separate clean without Israeli support.

#### VARIANT 48 / PROFILE 14.1
MODEL: IL-likely|Mitsubishi|Colt
CURRENT VALUE: version_or_trim='CZT'; body_type='Hatchback'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=150; transmission='5-speed manual'; drivetrain='FWD'; year_start=2005; year_end=2008; support_level='direct'; source_indexes=[1]
PROBLEM: Colt CZT 1.5 turbo may be legitimate but remains IL-likely and should not be a separate clean profile without strong Israeli source.
WEB-VALIDATED FACT: Israeli sources support Colt 2004-2012 1.3 Invite/Instyle rows. IL-likely Colt CZT needs merge/review; global-reference-only Colt duplicates IL rows and adds weak old 1993-2004 rows that should not remain separate clean without Israeli support.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: If repo-local Israeli source supports Colt CZT, merge into canonical IL-confirmed Colt profile with trim CZT. Otherwise move to non-blocking review/archive with reason.
ACTION: MERGE / MOVE TO REVIEW

### PROFILE 15: global-reference-only|Mitsubishi|Colt
MODEL-LEVEL FACT: Israeli sources support Colt 2004-2012 1.3 Invite/Instyle rows. IL-likely Colt CZT needs merge/review; global-reference-only Colt duplicates IL rows and adds weak old 1993-2004 rows that should not remain separate clean without Israeli support.

#### VARIANT 49 / PROFILE 15.1
MODEL: global-reference-only|Mitsubishi|Colt
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.3L'; engine_displacement_l=1.3; horsepower_hp=95; transmission='6-speed automatic'; drivetrain='FWD'; year_start=2004; year_end=2012; support_level='direct'; source_indexes=[0]
PROBLEM: Global Colt 2004-2012 rows duplicate IL-confirmed Invite/Instyle rows.
WEB-VALIDATED FACT: Israeli sources support Colt 2004-2012 1.3 Invite/Instyle rows. IL-likely Colt CZT needs merge/review; global-reference-only Colt duplicates IL rows and adds weak old 1993-2004 rows that should not remain separate clean without Israeli support.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Merge into IL-confirmed Colt and archive duplicate global profile non-blocking with lineage.
ACTION: MERGE / ARCHIVE NON-BLOCKING

#### VARIANT 50 / PROFILE 15.2
MODEL: global-reference-only|Mitsubishi|Colt
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.3L'; engine_displacement_l=1.3; horsepower_hp=95; transmission='5-speed manual'; drivetrain='FWD'; year_start=2004; year_end=2012; support_level='direct'; source_indexes=[0]
PROBLEM: Global Colt 2004-2012 rows duplicate IL-confirmed Invite/Instyle rows.
WEB-VALIDATED FACT: Israeli sources support Colt 2004-2012 1.3 Invite/Instyle rows. IL-likely Colt CZT needs merge/review; global-reference-only Colt duplicates IL rows and adds weak old 1993-2004 rows that should not remain separate clean without Israeli support.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Merge into IL-confirmed Colt and archive duplicate global profile non-blocking with lineage.
ACTION: MERGE / ARCHIVE NON-BLOCKING

#### VARIANT 51 / PROFILE 15.3
MODEL: global-reference-only|Mitsubishi|Colt
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=113; transmission='4-speed automatic'; drivetrain='FWD'; year_start=1993; year_end=2004; support_level='direct'; source_indexes=[1]
PROBLEM: Older 1993-2004 Colt global rows lack strong Israeli grounding in RUN6 anchors.
WEB-VALIDATED FACT: Israeli sources support Colt 2004-2012 1.3 Invite/Instyle rows. IL-likely Colt CZT needs merge/review; global-reference-only Colt duplicates IL rows and adds weak old 1993-2004 rows that should not remain separate clean without Israeli support.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Move old global 1.6 rows to non-blocking review/archive unless repo-local Israeli source proves market presence and exact fields.
ACTION: MOVE TO REVIEW / ARCHIVE NON-BLOCKING

#### VARIANT 52 / PROFILE 15.4
MODEL: global-reference-only|Mitsubishi|Colt
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=113; transmission='5-speed manual'; drivetrain='FWD'; year_start=1993; year_end=2004; support_level='direct'; source_indexes=[1]
PROBLEM: Older 1993-2004 Colt global rows lack strong Israeli grounding in RUN6 anchors.
WEB-VALIDATED FACT: Israeli sources support Colt 2004-2012 1.3 Invite/Instyle rows. IL-likely Colt CZT needs merge/review; global-reference-only Colt duplicates IL rows and adds weak old 1993-2004 rows that should not remain separate clean without Israeli support.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Move old global 1.6 rows to non-blocking review/archive unless repo-local Israeli source proves market presence and exact fields.
ACTION: MOVE TO REVIEW / ARCHIVE NON-BLOCKING

### PROFILE 16: IL-confirmed|Mitsubishi|Eclipse Cross
MODEL-LEVEL FACT: Mitsubishi Israel marks Eclipse Cross as past model 2017-2025; iCar has 2026 PHEV spec but official Mitsubishi current model/price pages emphasize Outlander/ASX. Keep through 2025; do not extend to current official clean without policy approval. PHEV row should use direct-drive/valid PHEV transmission if schema supports.

#### VARIANT 53 / PROFILE 16.1
MODEL: IL-confirmed|Mitsubishi|Eclipse Cross
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=163; transmission='cvt'; drivetrain='FWD'; year_start=2018; year_end=2021; support_level='direct'; source_indexes=[1, 2]
PROBLEM: Eclipse Cross petrol rows are Israel-grounded and official Mitsubishi page places the model as 2017-2025 past model.
WEB-VALIDATED FACT: Mitsubishi Israel marks Eclipse Cross as past model 2017-2025; iCar has 2026 PHEV spec but official Mitsubishi current model/price pages emphasize Outlander/ASX. Keep through 2025; do not extend to current official clean without policy approval. PHEV row should use direct-drive/valid PHEV transmission if schema supports.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep petrol rows through 2025; do not extend beyond 2025 without official current source.
ACTION: KEEP

#### VARIANT 54 / PROFILE 16.2
MODEL: IL-confirmed|Mitsubishi|Eclipse Cross
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=163; transmission='cvt'; drivetrain='AWD'; year_start=2018; year_end=2021; support_level='direct'; source_indexes=[1, 2]
PROBLEM: Eclipse Cross petrol rows are Israel-grounded and official Mitsubishi page places the model as 2017-2025 past model.
WEB-VALIDATED FACT: Mitsubishi Israel marks Eclipse Cross as past model 2017-2025; iCar has 2026 PHEV spec but official Mitsubishi current model/price pages emphasize Outlander/ASX. Keep through 2025; do not extend to current official clean without policy approval. PHEV row should use direct-drive/valid PHEV transmission if schema supports.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep petrol rows through 2025; do not extend beyond 2025 without official current source.
ACTION: KEEP

#### VARIANT 55 / PROFILE 16.3
MODEL: IL-confirmed|Mitsubishi|Eclipse Cross
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=152; transmission='cvt'; drivetrain='FWD'; year_start=2021; year_end=2025; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Eclipse Cross petrol rows are Israel-grounded and official Mitsubishi page places the model as 2017-2025 past model.
WEB-VALIDATED FACT: Mitsubishi Israel marks Eclipse Cross as past model 2017-2025; iCar has 2026 PHEV spec but official Mitsubishi current model/price pages emphasize Outlander/ASX. Keep through 2025; do not extend to current official clean without policy approval. PHEV row should use direct-drive/valid PHEV transmission if schema supports.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep petrol rows through 2025; do not extend beyond 2025 without official current source.
ACTION: KEEP

#### VARIANT 56 / PROFILE 16.4
MODEL: IL-confirmed|Mitsubishi|Eclipse Cross
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='plug_in_hybrid'; engine='2.4L'; engine_displacement_l=2.4; horsepower_hp=188; transmission='cvt'; drivetrain='AWD'; year_start=2022; year_end=2025; support_level='direct'; source_indexes=[0, 1]
PROBLEM: PHEV row has transmission=cvt, while Israeli iCar PHEV spec describes direct transmission; Mitsubishi Israel marks Eclipse Cross as past model 2017-2025.
WEB-VALIDATED FACT: Mitsubishi Israel marks Eclipse Cross as past model 2017-2025; iCar has 2026 PHEV spec but official Mitsubishi current model/price pages emphasize Outlander/ASX. Keep through 2025; do not extend to current official clean without policy approval. PHEV row should use direct-drive/valid PHEV transmission if schema supports.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep year_end 2025 unless policy accepts iCar 2026 as current. Normalize PHEV transmission to direct_drive/single_speed-equivalent according to repo schema if allowed; keep 2.4L PHEV 188 hp AWD.
ACTION: FIX

### PROFILE 17: IL-confirmed|Mitsubishi|Galant
MODEL-LEVEL FACT: Israeli historical sources support Galant rows through 2008. Keep historical only; no current extension.

#### VARIANT 57 / PROFILE 17.1
MODEL: IL-confirmed|Mitsubishi|Galant
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.8L'; engine_displacement_l=1.8; horsepower_hp=126; transmission='4-speed automatic'; drivetrain='FWD'; year_start=1993; year_end=1996; support_level='direct'; source_indexes=[2]
PROBLEM: Galant is historical only; trim null may be acceptable only if old source policy permits.
WEB-VALIDATED FACT: Israeli historical sources support Galant rows through 2008. Keep historical only; no current extension.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical year ranges and fields; do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 58 / PROFILE 17.2
MODEL: IL-confirmed|Mitsubishi|Galant
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L'; engine_displacement_l=2.0; horsepower_hp=133; transmission='4-speed automatic'; drivetrain='FWD'; year_start=1997; year_end=2003; support_level='direct'; source_indexes=[0]
PROBLEM: Galant is historical only; trim null may be acceptable only if old source policy permits.
WEB-VALIDATED FACT: Israeli historical sources support Galant rows through 2008. Keep historical only; no current extension.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical year ranges and fields; do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 59 / PROFILE 17.3
MODEL: IL-confirmed|Mitsubishi|Galant
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.5L v6'; engine_displacement_l=2.5; horsepower_hp=163; transmission='4-speed automatic'; drivetrain='FWD'; year_start=1997; year_end=2003; support_level='direct'; source_indexes=[0]
PROBLEM: Galant is historical only; trim null may be acceptable only if old source policy permits.
WEB-VALIDATED FACT: Israeli historical sources support Galant rows through 2008. Keep historical only; no current extension.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical year ranges and fields; do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 60 / PROFILE 17.4
MODEL: IL-confirmed|Mitsubishi|Galant
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.4L'; engine_displacement_l=2.4; horsepower_hp=165; transmission='4-speed automatic'; drivetrain='FWD'; year_start=2004; year_end=2008; support_level='direct'; source_indexes=[1]
PROBLEM: Galant is historical only; trim null may be acceptable only if old source policy permits.
WEB-VALIDATED FACT: Israeli historical sources support Galant rows through 2008. Keep historical only; no current extension.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical year ranges and fields; do not currentize.
ACTION: KEEP / FIX SOURCE

### PROFILE 18: IL-confirmed|Mitsubishi|i-MiEV
MODEL-LEVEL FACT: Israeli historical EV support exists for i-MiEV; EV schema with displacement null and single_speed is valid. Keep historical only.

#### VARIANT 61 / PROFILE 18.1
MODEL: IL-confirmed|Mitsubishi|i-MiEV
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=64; transmission='single_speed'; drivetrain='RWD'; year_start=2011; year_end=2015; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Historical EV row; schema is valid with displacement null and single_speed.
WEB-VALIDATED FACT: Israeli historical EV support exists for i-MiEV; EV schema with displacement null and single_speed is valid. Keep historical only.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep 2011-2015 historical EV row; do not currentize.
ACTION: KEEP

### PROFILE 19: IL-confirmed|Mitsubishi|L200
MODEL-LEVEL FACT: Israeli sources support L200/Triton/Hunter historical pickup generations, including 2.4 diesel 154/181 hp and later 2.2 diesel 150 hp; it is not on Mitsubishi Israel current 2026 model/price page, so keep closed at 2024 unless repo-local current source exists.

#### VARIANT 62 / PROFILE 19.1
MODEL: IL-confirmed|Mitsubishi|L200
CURRENT VALUE: version_or_trim=None; body_type='Pickup'; fuel_type='diesel'; engine='2.5L turbo'; engine_displacement_l=2.5; horsepower_hp=100; transmission='4-speed automatic'; drivetrain='4WD'; year_start=1997; year_end=2006; support_level='direct'; source_indexes=[1293]
PROBLEM: L200/Triton/Hunter rows are historical; empty trim names hide Israeli marketing names and generation/trim distinctions.
WEB-VALIDATED FACT: Israeli sources support L200/Triton/Hunter historical pickup generations, including 2.4 diesel 154/181 hp and later 2.2 diesel 150 hp; it is not on Mitsubishi Israel current 2026 model/price page, so keep closed at 2024 unless repo-local current source exists.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows through 2024, but add lineage/alias labels L200/Hunter/Triton and Dakar/Invite/Instyle only where repo-local source supports. Do not currentize beyond 2024 unless current Mitsubishi Israel source exists.
ACTION: KEEP / FIX LINEAGE

#### VARIANT 63 / PROFILE 19.2
MODEL: IL-confirmed|Mitsubishi|L200
CURRENT VALUE: version_or_trim=None; body_type='Pickup'; fuel_type='diesel'; engine='2.5L turbo'; engine_displacement_l=2.5; horsepower_hp=100; transmission='5-speed manual'; drivetrain='4WD'; year_start=1997; year_end=2006; support_level='direct'; source_indexes=[1293]
PROBLEM: L200/Triton/Hunter rows are historical; empty trim names hide Israeli marketing names and generation/trim distinctions.
WEB-VALIDATED FACT: Israeli sources support L200/Triton/Hunter historical pickup generations, including 2.4 diesel 154/181 hp and later 2.2 diesel 150 hp; it is not on Mitsubishi Israel current 2026 model/price page, so keep closed at 2024 unless repo-local current source exists.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows through 2024, but add lineage/alias labels L200/Hunter/Triton and Dakar/Invite/Instyle only where repo-local source supports. Do not currentize beyond 2024 unless current Mitsubishi Israel source exists.
ACTION: KEEP / FIX LINEAGE

#### VARIANT 64 / PROFILE 19.3
MODEL: IL-confirmed|Mitsubishi|L200
CURRENT VALUE: version_or_trim=None; body_type='Pickup'; fuel_type='diesel'; engine='2.5L turbo'; engine_displacement_l=2.5; horsepower_hp=136; transmission='5-speed manual'; drivetrain='4WD'; year_start=2006; year_end=2015; support_level='direct'; source_indexes=[1294]
PROBLEM: L200/Triton/Hunter rows are historical; empty trim names hide Israeli marketing names and generation/trim distinctions.
WEB-VALIDATED FACT: Israeli sources support L200/Triton/Hunter historical pickup generations, including 2.4 diesel 154/181 hp and later 2.2 diesel 150 hp; it is not on Mitsubishi Israel current 2026 model/price page, so keep closed at 2024 unless repo-local current source exists.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows through 2024, but add lineage/alias labels L200/Hunter/Triton and Dakar/Invite/Instyle only where repo-local source supports. Do not currentize beyond 2024 unless current Mitsubishi Israel source exists.
ACTION: KEEP / FIX LINEAGE

#### VARIANT 65 / PROFILE 19.4
MODEL: IL-confirmed|Mitsubishi|L200
CURRENT VALUE: version_or_trim=None; body_type='Pickup'; fuel_type='diesel'; engine='2.5L turbo'; engine_displacement_l=2.5; horsepower_hp=136; transmission='4-speed automatic'; drivetrain='4WD'; year_start=2006; year_end=2015; support_level='direct'; source_indexes=[1294]
PROBLEM: L200/Triton/Hunter rows are historical; empty trim names hide Israeli marketing names and generation/trim distinctions.
WEB-VALIDATED FACT: Israeli sources support L200/Triton/Hunter historical pickup generations, including 2.4 diesel 154/181 hp and later 2.2 diesel 150 hp; it is not on Mitsubishi Israel current 2026 model/price page, so keep closed at 2024 unless repo-local current source exists.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows through 2024, but add lineage/alias labels L200/Hunter/Triton and Dakar/Invite/Instyle only where repo-local source supports. Do not currentize beyond 2024 unless current Mitsubishi Israel source exists.
ACTION: KEEP / FIX LINEAGE

#### VARIANT 66 / PROFILE 19.5
MODEL: IL-confirmed|Mitsubishi|L200
CURRENT VALUE: version_or_trim=None; body_type='Pickup'; fuel_type='diesel'; engine='2.5L turbo'; engine_displacement_l=2.5; horsepower_hp=178; transmission='5-speed automatic'; drivetrain='4WD'; year_start=2011; year_end=2015; support_level='direct'; source_indexes=[1294]
PROBLEM: L200/Triton/Hunter rows are historical; empty trim names hide Israeli marketing names and generation/trim distinctions.
WEB-VALIDATED FACT: Israeli sources support L200/Triton/Hunter historical pickup generations, including 2.4 diesel 154/181 hp and later 2.2 diesel 150 hp; it is not on Mitsubishi Israel current 2026 model/price page, so keep closed at 2024 unless repo-local current source exists.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows through 2024, but add lineage/alias labels L200/Hunter/Triton and Dakar/Invite/Instyle only where repo-local source supports. Do not currentize beyond 2024 unless current Mitsubishi Israel source exists.
ACTION: KEEP / FIX LINEAGE

#### VARIANT 67 / PROFILE 19.6
MODEL: IL-confirmed|Mitsubishi|L200
CURRENT VALUE: version_or_trim=None; body_type='Pickup'; fuel_type='diesel'; engine='2.4L turbo'; engine_displacement_l=2.4; horsepower_hp=154; transmission='6-speed manual'; drivetrain='4WD'; year_start=2015; year_end=2019; support_level='direct'; source_indexes=[1295]
PROBLEM: L200/Triton/Hunter rows are historical; empty trim names hide Israeli marketing names and generation/trim distinctions.
WEB-VALIDATED FACT: Israeli sources support L200/Triton/Hunter historical pickup generations, including 2.4 diesel 154/181 hp and later 2.2 diesel 150 hp; it is not on Mitsubishi Israel current 2026 model/price page, so keep closed at 2024 unless repo-local current source exists.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows through 2024, but add lineage/alias labels L200/Hunter/Triton and Dakar/Invite/Instyle only where repo-local source supports. Do not currentize beyond 2024 unless current Mitsubishi Israel source exists.
ACTION: KEEP / FIX LINEAGE

#### VARIANT 68 / PROFILE 19.7
MODEL: IL-confirmed|Mitsubishi|L200
CURRENT VALUE: version_or_trim=None; body_type='Pickup'; fuel_type='diesel'; engine='2.4L turbo'; engine_displacement_l=2.4; horsepower_hp=154; transmission='5-speed automatic'; drivetrain='4WD'; year_start=2015; year_end=2019; support_level='direct'; source_indexes=[1295]
PROBLEM: L200/Triton/Hunter rows are historical; empty trim names hide Israeli marketing names and generation/trim distinctions.
WEB-VALIDATED FACT: Israeli sources support L200/Triton/Hunter historical pickup generations, including 2.4 diesel 154/181 hp and later 2.2 diesel 150 hp; it is not on Mitsubishi Israel current 2026 model/price page, so keep closed at 2024 unless repo-local current source exists.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows through 2024, but add lineage/alias labels L200/Hunter/Triton and Dakar/Invite/Instyle only where repo-local source supports. Do not currentize beyond 2024 unless current Mitsubishi Israel source exists.
ACTION: KEEP / FIX LINEAGE

#### VARIANT 69 / PROFILE 19.8
MODEL: IL-confirmed|Mitsubishi|L200
CURRENT VALUE: version_or_trim=None; body_type='Pickup'; fuel_type='diesel'; engine='2.4L turbo'; engine_displacement_l=2.4; horsepower_hp=181; transmission='5-speed automatic'; drivetrain='4WD'; year_start=2015; year_end=2019; support_level='direct'; source_indexes=[1295]
PROBLEM: L200/Triton/Hunter rows are historical; empty trim names hide Israeli marketing names and generation/trim distinctions.
WEB-VALIDATED FACT: Israeli sources support L200/Triton/Hunter historical pickup generations, including 2.4 diesel 154/181 hp and later 2.2 diesel 150 hp; it is not on Mitsubishi Israel current 2026 model/price page, so keep closed at 2024 unless repo-local current source exists.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows through 2024, but add lineage/alias labels L200/Hunter/Triton and Dakar/Invite/Instyle only where repo-local source supports. Do not currentize beyond 2024 unless current Mitsubishi Israel source exists.
ACTION: KEEP / FIX LINEAGE

#### VARIANT 70 / PROFILE 19.9
MODEL: IL-confirmed|Mitsubishi|L200
CURRENT VALUE: version_or_trim=None; body_type='Pickup'; fuel_type='diesel'; engine='2.2L turbo'; engine_displacement_l=2.2; horsepower_hp=150; transmission='6-speed automatic'; drivetrain='4WD'; year_start=2019; year_end=2024; support_level='direct'; source_indexes=[1296]
PROBLEM: L200/Triton/Hunter rows are historical; empty trim names hide Israeli marketing names and generation/trim distinctions.
WEB-VALIDATED FACT: Israeli sources support L200/Triton/Hunter historical pickup generations, including 2.4 diesel 154/181 hp and later 2.2 diesel 150 hp; it is not on Mitsubishi Israel current 2026 model/price page, so keep closed at 2024 unless repo-local current source exists.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows through 2024, but add lineage/alias labels L200/Hunter/Triton and Dakar/Invite/Instyle only where repo-local source supports. Do not currentize beyond 2024 unless current Mitsubishi Israel source exists.
ACTION: KEEP / FIX LINEAGE

### PROFILE 20: IL-confirmed|Mitsubishi|Lancer
MODEL-LEVEL FACT: iCar Israeli sources support Lancer rows including 1.5 109 hp, 1.8 140 hp and later 1.6 117 hp. Keep historical only; no current extension.

#### VARIANT 71 / PROFILE 20.1
MODEL: IL-confirmed|Mitsubishi|Lancer
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=113; transmission='4-speed automatic'; drivetrain='FWD'; year_start=1993; year_end=1997; support_level='direct'; source_indexes=[0]
PROBLEM: Lancer rows are historical and supported by Israeli sources; null trims are weak but may be acceptable for engine/body-level historical rows.
WEB-VALIDATED FACT: iCar Israeli sources support Lancer rows including 1.5 109 hp, 1.8 140 hp and later 1.6 117 hp. Keep historical only; no current extension.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows and exact body splits. If repo-local source supports trim names, fill trims; otherwise keep null with reason. Do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 72 / PROFILE 20.2
MODEL: IL-confirmed|Mitsubishi|Lancer
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=98; transmission='4-speed automatic'; drivetrain='FWD'; year_start=1998; year_end=2003; support_level='direct'; source_indexes=[1]
PROBLEM: Lancer rows are historical and supported by Israeli sources; null trims are weak but may be acceptable for engine/body-level historical rows.
WEB-VALIDATED FACT: iCar Israeli sources support Lancer rows including 1.5 109 hp, 1.8 140 hp and later 1.6 117 hp. Keep historical only; no current extension.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows and exact body splits. If repo-local source supports trim names, fill trims; otherwise keep null with reason. Do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 73 / PROFILE 20.3
MODEL: IL-confirmed|Mitsubishi|Lancer
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=98; transmission='4-speed automatic'; drivetrain='FWD'; year_start=2004; year_end=2008; support_level='direct'; source_indexes=[2]
PROBLEM: Lancer rows are historical and supported by Israeli sources; null trims are weak but may be acceptable for engine/body-level historical rows.
WEB-VALIDATED FACT: iCar Israeli sources support Lancer rows including 1.5 109 hp, 1.8 140 hp and later 1.6 117 hp. Keep historical only; no current extension.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows and exact body splits. If repo-local source supports trim names, fill trims; otherwise keep null with reason. Do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 74 / PROFILE 20.4
MODEL: IL-confirmed|Mitsubishi|Lancer
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.5L'; engine_displacement_l=1.5; horsepower_hp=109; transmission='4-speed automatic'; drivetrain='FWD'; year_start=2008; year_end=2012; support_level='direct'; source_indexes=[3]
PROBLEM: Lancer rows are historical and supported by Israeli sources; null trims are weak but may be acceptable for engine/body-level historical rows.
WEB-VALIDATED FACT: iCar Israeli sources support Lancer rows including 1.5 109 hp, 1.8 140 hp and later 1.6 117 hp. Keep historical only; no current extension.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows and exact body splits. If repo-local source supports trim names, fill trims; otherwise keep null with reason. Do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 75 / PROFILE 20.5
MODEL: IL-confirmed|Mitsubishi|Lancer
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.8L'; engine_displacement_l=1.8; horsepower_hp=140; transmission='cvt'; drivetrain='FWD'; year_start=2008; year_end=2012; support_level='direct'; source_indexes=[3]
PROBLEM: Lancer rows are historical and supported by Israeli sources; null trims are weak but may be acceptable for engine/body-level historical rows.
WEB-VALIDATED FACT: iCar Israeli sources support Lancer rows including 1.5 109 hp, 1.8 140 hp and later 1.6 117 hp. Keep historical only; no current extension.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows and exact body splits. If repo-local source supports trim names, fill trims; otherwise keep null with reason. Do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 76 / PROFILE 20.6
MODEL: IL-confirmed|Mitsubishi|Lancer
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.8L'; engine_displacement_l=1.8; horsepower_hp=140; transmission='cvt'; drivetrain='FWD'; year_start=2008; year_end=2012; support_level='direct'; source_indexes=[3]
PROBLEM: Lancer rows are historical and supported by Israeli sources; null trims are weak but may be acceptable for engine/body-level historical rows.
WEB-VALIDATED FACT: iCar Israeli sources support Lancer rows including 1.5 109 hp, 1.8 140 hp and later 1.6 117 hp. Keep historical only; no current extension.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows and exact body splits. If repo-local source supports trim names, fill trims; otherwise keep null with reason. Do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 77 / PROFILE 20.7
MODEL: IL-confirmed|Mitsubishi|Lancer
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=117; transmission='4-speed automatic'; drivetrain='FWD'; year_start=2012; year_end=2017; support_level='direct'; source_indexes=[3]
PROBLEM: Lancer rows are historical and supported by Israeli sources; null trims are weak but may be acceptable for engine/body-level historical rows.
WEB-VALIDATED FACT: iCar Israeli sources support Lancer rows including 1.5 109 hp, 1.8 140 hp and later 1.6 117 hp. Keep historical only; no current extension.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows and exact body splits. If repo-local source supports trim names, fill trims; otherwise keep null with reason. Do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 78 / PROFILE 20.8
MODEL: IL-confirmed|Mitsubishi|Lancer
CURRENT VALUE: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=117; transmission='4-speed automatic'; drivetrain='FWD'; year_start=2012; year_end=2017; support_level='direct'; source_indexes=[3]
PROBLEM: Lancer rows are historical and supported by Israeli sources; null trims are weak but may be acceptable for engine/body-level historical rows.
WEB-VALIDATED FACT: iCar Israeli sources support Lancer rows including 1.5 109 hp, 1.8 140 hp and later 1.6 117 hp. Keep historical only; no current extension.
SOURCE: repo-local sources listed in this profile plus RUN6 web anchors above.
TARGET VALUE: Keep historical rows and exact body splits. If repo-local source supports trim names, fill trims; otherwise keep null with reason. Do not currentize.
ACTION: KEEP / FIX SOURCE

## Coverage assertion
RUN 6 contains 20 profiles and 78 technical variants. This task includes 78/78 explicit variant decisions.

## Report format after Codex run
Report: files changed, exact before/after metrics, confirmation all 20 profiles and 78 variants were handled, test results, confirmation temporary RUN6 instruction files were deleted before final commit, and remaining issues if any.

# ==============================
# RUN7
# source: BATCH26_RUN7_VARIANT_LEVEL_CODEX_TASK.md
# ==============================

# BATCH26 RUN 7 — VARIANT-LEVEL CODEX TASK

## Non-negotiable execution rules
Do not browse the internet. All web-validation facts needed for RUN 7 are embedded here. Use this task file as the single source of truth for RUN 7 only.
Apply RUN 7 only. Do not apply RUN 1, RUN 2, RUN 3, RUN 4, RUN 5, RUN 6, FINAL blockers, or any unified batch task.
If repo-local evidence conflicts with this task file, report the conflict instead of guessing. If a variant cannot be grounded, move it to non-blocking review/archive with reason and lineage rather than fabricating clean data.
Temporary-file cleanup is mandatory: before final commit, delete `codex_tasks/BATCH26_RUN7_*.md` unless the user explicitly asks to keep it.

## Scope
RUN 7 scope: `IL-confirmed|Mitsubishi|Lancer Evolution` through `IL-confirmed|Mitsubishi|Pajero Sport`.
Profiles: 4. Technical variants: 19. Coverage: every variant has an explicit decision.

## Web/source anchors embedded for RUN 7
- Mitsubishi Israel current models page: https://www.mitsubishi-israel.co.il/models/
- Mitsubishi Israel current prices page: https://www.mitsubishi-israel.co.il/prices/
- Mitsubishi Israel Outlander official model page: https://www.mitsubishi-israel.co.il/models/outlander/
- Auto.co.il Mitsubishi Outlander current technical page: https://www.auto.co.il/cars/mitsubishi/outlander/
- Cartube Outlander 2025 FL local price/spec: https://www.cartube.co.il/חדשות-רכב/מיצובישי-אאוטלנדר-2025-החדש-בישראל-מחיר-191990-שקל
- Auto.co.il Outlander PHEV 2019 local technical page: https://www.auto.co.il/cars/mitsubishi/outlander-phev/2019/
- iCar Outlander PHEV 2019 technical page: https://www.icar.co.il/מיצובישי/מיצובישי_אאוטלנדר_PHEV/מיצובישי_אאוטלנדר_PHEV_יד_שניה_ד10/version21226/
- Auto.co.il Mitsubishi Pajero page: https://www.auto.co.il/cars/mitsubishi/pajero/
- iCar Pajero 2008-2018 technical page: https://www.icar.co.il/מיצובישי/מיצובישי_פאג'רו/מיצובישי_פאג'רו_יד_שניה_ד11/
- iCar Pajero 2015 3.2 Desert spec: https://www.icar.co.il/מיצובישי/מיצובישי_פאג'רו/מיצובישי_פאג'רו_יד_שניה_ד11/version13629/
- Yad2 Pajero listing/price evidence: https://www.yad2.co.il/vehicles/cars?manufacturer=30&model=10382
- 4x4 Pajero Sport 3.0 petrol Israel launch: https://www.4x4.co.il/article/1461
- Auto.co.il Pajero Sport 2000-2008 model page: https://www.auto.co.il/model/mitsubishi-pajero-sport_g210
- Yad2 Lancer Evolution 2010 295 hp price/spec: https://www.yad2.co.il/price-list/sub-model/118398/2010
- Gear Lancer Evolution VIII 2005 265 hp price/spec: https://www.gear.co.il/מחירון-רכב-דגם/מיצובישי/לנסר/2005/לנסר-אבולושן-8/2.0-אלגנס-ידני-
- Autoboom Lancer Evolution Israel catalog: https://autoboom.co.il/catalog/cars/mitsubishi/lancer-evolution

## Model-level facts
- **Mitsubishi Lancer Evolution**: Israeli price/catalog evidence supports Lancer Evolution as historical Israeli-market performance model, including Evolution X 2.0 turbo 295 hp AWD/SST around 2008-2016, Evolution IX 2.0 turbo 280 hp AWD/manual around 2006-2007, and Evolution VIII 2.0 turbo 265 hp AWD/manual around 2003-2005. It is not a current Mitsubishi Israel model. Null trim is weak because the rows clearly represent Evolution VIII/IX/X generations.
- **Mitsubishi Outlander**: Mitsubishi Israel current model and price pages support Outlander as current in Israel, with 2025/2026 FL 7-seat 2.5 petrol CVT trims such as Intense, Executive, Instyle/Premium/Luxury, and Luxury 4X4/S-AWC. Israeli Auto/Cartube sources support 2.5L 181 hp CVT. Historical Israeli sources support 2013-2021 2.0 petrol 150 hp CVT/FWD/4WD rows, 2007-2012 2.4 petrol 170 hp 4WD and 2010-2012 2.0 petrol 147 hp FWD rows. Outlander PHEV local sources support 2014-2018 2.0 PHEV 203 hp and 2019-2021 2.4 PHEV 224 hp with direct/single-speed style transmission and AWD.
- **Mitsubishi Pajero**: Pajero is a historical Israeli-market SUV and is absent from current Mitsubishi Israel model/price pages. Israeli Auto/iCar/Yad2 evidence supports 3.2 diesel, 3.8 petrol and older 2.8 diesel rows, but the broad 2010-2020 3.2 diesel 200 hp row is potentially too coarse: local listings show 200 hp for some 2014-2015 Desert/Dakar rows and also 190 hp for some 2016-2017 Dakar rows. Keep historical only and split or review horsepower/year coverage when repo-local evidence distinguishes 190/200 hp.
- **Mitsubishi Pajero Sport**: Pajero Sport is a historical Israeli-market SUV, not a current Mitsubishi Israel model. Local Auto/iCar evidence supports 2000-2008 Pajero Sport GLS rows. A 4x4 Israel launch article specifically supports the 3.0L V6 petrol automatic with 170 hp in Israel; Auto/iCar repo-local sources support the 2.5 turbo-diesel automatic 115 hp row if attached. Keep historical only.

## Required checks after implementation
```bash
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```
Then audit actual generated files: clean catalog, readiness, review, archive, quality scan, compute_resume_state(), unmatched_output_keys, active blockers, cursor/resume state, duplicate/split alias cleanup.

## Variant-level instructions

### PROFILE 1: IL-confirmed|Mitsubishi|Lancer Evolution
MODEL-LEVEL FACT: Israeli price/catalog evidence supports Lancer Evolution as historical Israeli-market performance model, including Evolution X 2.0 turbo 295 hp AWD/SST around 2008-2016, Evolution IX 2.0 turbo 280 hp AWD/manual around 2006-2007, and Evolution VIII 2.0 turbo 265 hp AWD/manual around 2003-2005. It is not a current Mitsubishi Israel model. Null trim is weak because the rows clearly represent Evolution VIII/IX/X generations.

#### VARIANT 1 / PROFILE 1.1
MODEL: IL-confirmed|Mitsubishi|Lancer Evolution
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=295; transmission='6-speed dual_clutch'; drivetrain='AWD'; year_start=2008; year_end=2016; support_level='direct'; source_indexes=[0]
PROBLEM: Row is technically plausible for Evolution X, but version_or_trim is null and therefore hides the exact generation/lineage; it must remain historical and not current.
WEB-VALIDATED FACT: Israeli price/catalog evidence supports Lancer Evolution as historical Israeli-market performance model, including Evolution X 2.0 turbo 295 hp AWD/SST around 2008-2016, Evolution IX 2.0 turbo 280 hp AWD/manual around 2006-2007, and Evolution VIII 2.0 turbo 265 hp AWD/manual around 2003-2005. It is not a current Mitsubishi Israel model. Null trim is weak because the rows clearly represent Evolution VIII/IX/X generations.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Set/normalize version_or_trim to `Evolution X` or `Lancer Evolution X` according to repo convention. Keep 2008-2016, 2.0L turbo, 295 hp, AWD, 6-speed dual_clutch/SST only if repo-local Auto/Yad2/Gear source supports the full row. If manual Evolution X is separately grounded, add a separate row rather than mixing transmissions.
ACTION: FIX

#### VARIANT 2 / PROFILE 1.2
MODEL: IL-confirmed|Mitsubishi|Lancer Evolution
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=280; transmission='6-speed manual'; drivetrain='AWD'; year_start=2006; year_end=2007; support_level='direct'; source_indexes=[1]
PROBLEM: Row matches Evolution IX generation but version_or_trim is null, making it ambiguous against Evolution VIII/X rows.
WEB-VALIDATED FACT: Israeli price/catalog evidence supports Lancer Evolution as historical Israeli-market performance model, including Evolution X 2.0 turbo 295 hp AWD/SST around 2008-2016, Evolution IX 2.0 turbo 280 hp AWD/manual around 2006-2007, and Evolution VIII 2.0 turbo 265 hp AWD/manual around 2003-2005. It is not a current Mitsubishi Israel model. Null trim is weak because the rows clearly represent Evolution VIII/IX/X generations.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Set/normalize version_or_trim to `Evolution IX` or `Lancer Evolution IX`. Keep 2006-2007, 2.0L turbo, 280 hp, AWD, 6-speed manual if source support remains valid.
ACTION: FIX

#### VARIANT 3 / PROFILE 1.3
MODEL: IL-confirmed|Mitsubishi|Lancer Evolution
CURRENT VALUE: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=265; transmission='5-speed manual'; drivetrain='AWD'; year_start=2003; year_end=2005; support_level='direct'; source_indexes=[2]
PROBLEM: Row matches Evolution VIII generation but version_or_trim is null, making it ambiguous against Evolution IX/X rows.
WEB-VALIDATED FACT: Israeli price/catalog evidence supports Lancer Evolution as historical Israeli-market performance model, including Evolution X 2.0 turbo 295 hp AWD/SST around 2008-2016, Evolution IX 2.0 turbo 280 hp AWD/manual around 2006-2007, and Evolution VIII 2.0 turbo 265 hp AWD/manual around 2003-2005. It is not a current Mitsubishi Israel model. Null trim is weak because the rows clearly represent Evolution VIII/IX/X generations.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Set/normalize version_or_trim to `Evolution VIII` or `Lancer Evolution VIII`. Keep 2003-2005, 2.0L turbo, 265 hp, AWD, 5-speed manual if source support remains valid.
ACTION: FIX

### PROFILE 2: IL-confirmed|Mitsubishi|Outlander
MODEL-LEVEL FACT: Mitsubishi Israel current model and price pages support Outlander as current in Israel, with 2025/2026 FL 7-seat 2.5 petrol CVT trims such as Intense, Executive, Instyle/Premium/Luxury, and Luxury 4X4/S-AWC. Israeli Auto/Cartube sources support 2.5L 181 hp CVT. Historical Israeli sources support 2013-2021 2.0 petrol 150 hp CVT/FWD/4WD rows, 2007-2012 2.4 petrol 170 hp 4WD and 2010-2012 2.0 petrol 147 hp FWD rows. Outlander PHEV local sources support 2014-2018 2.0 PHEV 203 hp and 2019-2021 2.4 PHEV 224 hp with direct/single-speed style transmission and AWD.

#### VARIANT 4 / PROFILE 2.1
MODEL: IL-confirmed|Mitsubishi|Outlander
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='2.5L'; engine_displacement_l=2.488; horsepower_hp=181; transmission='cvt'; drivetrain='FWD'; year_start=2021; year_end=2026; support_level='direct'; source_indexes=[1275, 1277]
PROBLEM: Current 2.5L Outlander rows are Israeli-grounded, but version_or_trim is null and trim/drivetrain coverage is too coarse for 2025/2026 FL lineup. Official price page lists Intense/Executive/Instyle/Premium/Luxury 2X4 and Luxury 4X4/S-AWC style trims.
WEB-VALIDATED FACT: Mitsubishi Israel current model and price pages support Outlander as current in Israel, with 2025/2026 FL 7-seat 2.5 petrol CVT trims such as Intense, Executive, Instyle/Premium/Luxury, and Luxury 4X4/S-AWC. Israeli Auto/Cartube sources support 2.5L 181 hp CVT. Historical Israeli sources support 2013-2021 2.0 petrol 150 hp CVT/FWD/4WD rows, 2007-2012 2.4 petrol 170 hp 4WD and 2010-2012 2.0 petrol 147 hp FWD rows. Outlander PHEV local sources support 2014-2018 2.0 PHEV 203 hp and 2019-2021 2.4 PHEV 224 hp with direct/single-speed style transmission and AWD.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep/currentize 2.5L 181 hp CVT FWD/2X4 through current only with official source indexes. Add/normalize trims such as Intense FL, Executive FL, Instyle/Premium/Luxury 2X4 if website policy requires trim rows. Do not leave a single null-trim current row as the only current representation.
ACTION: FIX

#### VARIANT 5 / PROFILE 2.2
MODEL: IL-confirmed|Mitsubishi|Outlander
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='2.5L'; engine_displacement_l=2.488; horsepower_hp=181; transmission='cvt'; drivetrain='4WD'; year_start=2021; year_end=2026; support_level='direct'; source_indexes=[1275, 1277]
PROBLEM: Current 2.5L Outlander rows are Israeli-grounded, but version_or_trim is null and trim/drivetrain coverage is too coarse for 2025/2026 FL lineup. Official price page lists Intense/Executive/Instyle/Premium/Luxury 2X4 and Luxury 4X4/S-AWC style trims.
WEB-VALIDATED FACT: Mitsubishi Israel current model and price pages support Outlander as current in Israel, with 2025/2026 FL 7-seat 2.5 petrol CVT trims such as Intense, Executive, Instyle/Premium/Luxury, and Luxury 4X4/S-AWC. Israeli Auto/Cartube sources support 2.5L 181 hp CVT. Historical Israeli sources support 2013-2021 2.0 petrol 150 hp CVT/FWD/4WD rows, 2007-2012 2.4 petrol 170 hp 4WD and 2010-2012 2.0 petrol 147 hp FWD rows. Outlander PHEV local sources support 2014-2018 2.0 PHEV 203 hp and 2019-2021 2.4 PHEV 224 hp with direct/single-speed style transmission and AWD.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep/currentize 2.5L 181 hp CVT 4WD/S-AWC only for Luxury 4X4 / Luxury TTH 4X4 style trims where official/Cartube sources support it. Do not represent all Outlander current trims as 4WD.
ACTION: FIX

#### VARIANT 6 / PROFILE 2.3
MODEL: IL-confirmed|Mitsubishi|Outlander
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='2.0L'; engine_displacement_l=1.998; horsepower_hp=150; transmission='cvt'; drivetrain='FWD'; year_start=2013; year_end=2021; support_level='direct'; source_indexes=[1276, 1279]
PROBLEM: Historical Outlander petrol row appears Israeli-grounded, but version_or_trim is null; trim names may be missing while engine/body/drivetrain/year data are broadly plausible.
WEB-VALIDATED FACT: Mitsubishi Israel current model and price pages support Outlander as current in Israel, with 2025/2026 FL 7-seat 2.5 petrol CVT trims such as Intense, Executive, Instyle/Premium/Luxury, and Luxury 4X4/S-AWC. Israeli Auto/Cartube sources support 2.5L 181 hp CVT. Historical Israeli sources support 2013-2021 2.0 petrol 150 hp CVT/FWD/4WD rows, 2007-2012 2.4 petrol 170 hp 4WD and 2010-2012 2.0 petrol 147 hp FWD rows. Outlander PHEV local sources support 2014-2018 2.0 PHEV 203 hp and 2019-2021 2.4 PHEV 224 hp with direct/single-speed style transmission and AWD.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep historical row and years as-is if source_indexes/field_sources are valid. Fill trim/lineage only where repo-local source supports exact trim; otherwise preserve null trim with documented reason. Do not extend historical 2.0/2.4 rows to current.
ACTION: KEEP / FIX TRIM IF SOURCED

#### VARIANT 7 / PROFILE 2.4
MODEL: IL-confirmed|Mitsubishi|Outlander
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='2.0L'; engine_displacement_l=1.998; horsepower_hp=150; transmission='cvt'; drivetrain='4WD'; year_start=2013; year_end=2021; support_level='direct'; source_indexes=[1276, 1279]
PROBLEM: Historical Outlander petrol row appears Israeli-grounded, but version_or_trim is null; trim names may be missing while engine/body/drivetrain/year data are broadly plausible.
WEB-VALIDATED FACT: Mitsubishi Israel current model and price pages support Outlander as current in Israel, with 2025/2026 FL 7-seat 2.5 petrol CVT trims such as Intense, Executive, Instyle/Premium/Luxury, and Luxury 4X4/S-AWC. Israeli Auto/Cartube sources support 2.5L 181 hp CVT. Historical Israeli sources support 2013-2021 2.0 petrol 150 hp CVT/FWD/4WD rows, 2007-2012 2.4 petrol 170 hp 4WD and 2010-2012 2.0 petrol 147 hp FWD rows. Outlander PHEV local sources support 2014-2018 2.0 PHEV 203 hp and 2019-2021 2.4 PHEV 224 hp with direct/single-speed style transmission and AWD.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep historical row and years as-is if source_indexes/field_sources are valid. Fill trim/lineage only where repo-local source supports exact trim; otherwise preserve null trim with documented reason. Do not extend historical 2.0/2.4 rows to current.
ACTION: KEEP / FIX TRIM IF SOURCED

#### VARIANT 8 / PROFILE 2.5
MODEL: IL-confirmed|Mitsubishi|Outlander
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='plug_in_hybrid'; engine='2.4L'; engine_displacement_l=2.36; horsepower_hp=224; transmission='single_speed'; drivetrain='4WD'; year_start=2019; year_end=2021; support_level='direct'; source_indexes=[1278]
PROBLEM: 2019-2021 Outlander PHEV 2.4L 224 hp AWD is supported by Israeli Auto/iCar sources. Need to ensure transmission schema is repo-valid direct/single-speed equivalent and row remains historical.
WEB-VALIDATED FACT: Mitsubishi Israel current model and price pages support Outlander as current in Israel, with 2025/2026 FL 7-seat 2.5 petrol CVT trims such as Intense, Executive, Instyle/Premium/Luxury, and Luxury 4X4/S-AWC. Israeli Auto/Cartube sources support 2.5L 181 hp CVT. Historical Israeli sources support 2013-2021 2.0 petrol 150 hp CVT/FWD/4WD rows, 2007-2012 2.4 petrol 170 hp 4WD and 2010-2012 2.0 petrol 147 hp FWD rows. Outlander PHEV local sources support 2014-2018 2.0 PHEV 203 hp and 2019-2021 2.4 PHEV 224 hp with direct/single-speed style transmission and AWD.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep 2019-2021 2.4L PHEV 224 hp AWD historical row; keep/normalize transmission to `single_speed` or repo-valid direct-drive equivalent. Do not currentize beyond 2021 unless local current PHEV source exists.
ACTION: KEEP / FIX SCHEMA

#### VARIANT 9 / PROFILE 2.6
MODEL: IL-confirmed|Mitsubishi|Outlander
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='plug_in_hybrid'; engine='2.0L'; engine_displacement_l=1.998; horsepower_hp=203; transmission='single_speed'; drivetrain='4WD'; year_start=2014; year_end=2018; support_level='direct'; source_indexes=[1281]
PROBLEM: 2014-2018 Outlander PHEV 2.0L 203 hp AWD is supported by Israeli sources as pre-facelift PHEV; ensure direct/single-speed schema and historical year closure.
WEB-VALIDATED FACT: Mitsubishi Israel current model and price pages support Outlander as current in Israel, with 2025/2026 FL 7-seat 2.5 petrol CVT trims such as Intense, Executive, Instyle/Premium/Luxury, and Luxury 4X4/S-AWC. Israeli Auto/Cartube sources support 2.5L 181 hp CVT. Historical Israeli sources support 2013-2021 2.0 petrol 150 hp CVT/FWD/4WD rows, 2007-2012 2.4 petrol 170 hp 4WD and 2010-2012 2.0 petrol 147 hp FWD rows. Outlander PHEV local sources support 2014-2018 2.0 PHEV 203 hp and 2019-2021 2.4 PHEV 224 hp with direct/single-speed style transmission and AWD.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep 2014-2018 2.0L PHEV 203 hp AWD historical row; keep/normalize transmission to `single_speed` or repo-valid direct-drive equivalent. Do not currentize.
ACTION: KEEP / FIX SCHEMA

#### VARIANT 10 / PROFILE 2.7
MODEL: IL-confirmed|Mitsubishi|Outlander
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='2.4L'; engine_displacement_l=2.359; horsepower_hp=170; transmission='cvt'; drivetrain='4WD'; year_start=2007; year_end=2012; support_level='direct'; source_indexes=[1280]
PROBLEM: Historical Outlander petrol row appears Israeli-grounded, but version_or_trim is null; trim names may be missing while engine/body/drivetrain/year data are broadly plausible.
WEB-VALIDATED FACT: Mitsubishi Israel current model and price pages support Outlander as current in Israel, with 2025/2026 FL 7-seat 2.5 petrol CVT trims such as Intense, Executive, Instyle/Premium/Luxury, and Luxury 4X4/S-AWC. Israeli Auto/Cartube sources support 2.5L 181 hp CVT. Historical Israeli sources support 2013-2021 2.0 petrol 150 hp CVT/FWD/4WD rows, 2007-2012 2.4 petrol 170 hp 4WD and 2010-2012 2.0 petrol 147 hp FWD rows. Outlander PHEV local sources support 2014-2018 2.0 PHEV 203 hp and 2019-2021 2.4 PHEV 224 hp with direct/single-speed style transmission and AWD.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep historical row and years as-is if source_indexes/field_sources are valid. Fill trim/lineage only where repo-local source supports exact trim; otherwise preserve null trim with documented reason. Do not extend historical 2.0/2.4 rows to current.
ACTION: KEEP / FIX TRIM IF SOURCED

#### VARIANT 11 / PROFILE 2.8
MODEL: IL-confirmed|Mitsubishi|Outlander
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='2.0L'; engine_displacement_l=1.998; horsepower_hp=147; transmission='cvt'; drivetrain='FWD'; year_start=2010; year_end=2012; support_level='direct'; source_indexes=[1280]
PROBLEM: Historical Outlander petrol row appears Israeli-grounded, but version_or_trim is null; trim names may be missing while engine/body/drivetrain/year data are broadly plausible.
WEB-VALIDATED FACT: Mitsubishi Israel current model and price pages support Outlander as current in Israel, with 2025/2026 FL 7-seat 2.5 petrol CVT trims such as Intense, Executive, Instyle/Premium/Luxury, and Luxury 4X4/S-AWC. Israeli Auto/Cartube sources support 2.5L 181 hp CVT. Historical Israeli sources support 2013-2021 2.0 petrol 150 hp CVT/FWD/4WD rows, 2007-2012 2.4 petrol 170 hp 4WD and 2010-2012 2.0 petrol 147 hp FWD rows. Outlander PHEV local sources support 2014-2018 2.0 PHEV 203 hp and 2019-2021 2.4 PHEV 224 hp with direct/single-speed style transmission and AWD.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep historical row and years as-is if source_indexes/field_sources are valid. Fill trim/lineage only where repo-local source supports exact trim; otherwise preserve null trim with documented reason. Do not extend historical 2.0/2.4 rows to current.
ACTION: KEEP / FIX TRIM IF SOURCED

#### VARIANT 12 / PROFILE 2.9
MODEL: IL-confirmed|Mitsubishi|Outlander
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='2.4L'; engine_displacement_l=2.378; horsepower_hp=160; transmission='4-speed automatic'; drivetrain='4WD'; year_start=2003; year_end=2006; support_level='direct'; source_indexes=[1282]
PROBLEM: Historical Outlander petrol row appears Israeli-grounded, but version_or_trim is null; trim names may be missing while engine/body/drivetrain/year data are broadly plausible.
WEB-VALIDATED FACT: Mitsubishi Israel current model and price pages support Outlander as current in Israel, with 2025/2026 FL 7-seat 2.5 petrol CVT trims such as Intense, Executive, Instyle/Premium/Luxury, and Luxury 4X4/S-AWC. Israeli Auto/Cartube sources support 2.5L 181 hp CVT. Historical Israeli sources support 2013-2021 2.0 petrol 150 hp CVT/FWD/4WD rows, 2007-2012 2.4 petrol 170 hp 4WD and 2010-2012 2.0 petrol 147 hp FWD rows. Outlander PHEV local sources support 2014-2018 2.0 PHEV 203 hp and 2019-2021 2.4 PHEV 224 hp with direct/single-speed style transmission and AWD.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep historical row and years as-is if source_indexes/field_sources are valid. Fill trim/lineage only where repo-local source supports exact trim; otherwise preserve null trim with documented reason. Do not extend historical 2.0/2.4 rows to current.
ACTION: KEEP / FIX TRIM IF SOURCED

### PROFILE 3: IL-confirmed|Mitsubishi|Pajero
MODEL-LEVEL FACT: Pajero is a historical Israeli-market SUV and is absent from current Mitsubishi Israel model/price pages. Israeli Auto/iCar/Yad2 evidence supports 3.2 diesel, 3.8 petrol and older 2.8 diesel rows, but the broad 2010-2020 3.2 diesel 200 hp row is potentially too coarse: local listings show 200 hp for some 2014-2015 Desert/Dakar rows and also 190 hp for some 2016-2017 Dakar rows. Keep historical only and split or review horsepower/year coverage when repo-local evidence distinguishes 190/200 hp.

#### VARIANT 13 / PROFILE 3.1
MODEL: IL-confirmed|Mitsubishi|Pajero
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='diesel'; engine='3.2L turbo'; engine_displacement_l=3.2; horsepower_hp=200; transmission='5-speed automatic'; drivetrain='4WD'; year_start=2010; year_end=2020; support_level='direct'; source_indexes=[0, 2]
PROBLEM: Broad 2010-2020 3.2 diesel 200 hp row is potentially over-broad. Israeli sources support Pajero as historical, but local listings/specs may distinguish 200 hp and 190 hp during later years.
WEB-VALIDATED FACT: Pajero is a historical Israeli-market SUV and is absent from current Mitsubishi Israel model/price pages. Israeli Auto/iCar/Yad2 evidence supports 3.2 diesel, 3.8 petrol and older 2.8 diesel rows, but the broad 2010-2020 3.2 diesel 200 hp row is potentially too coarse: local listings show 200 hp for some 2014-2015 Desert/Dakar rows and also 190 hp for some 2016-2017 Dakar rows. Keep historical only and split or review horsepower/year coverage when repo-local evidence distinguishes 190/200 hp.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Do not keep a single 2010-2020 200 hp row unless repo-local source supports full coverage. Prefer split into grounded trim/year ranges (e.g., 2010-2015 200 hp where supported, 2016-2020 190 hp where supported) or move ambiguous tail years to non-blocking review. Keep historical only and do not currentize.
ACTION: FIX / SPLIT OR REVIEW

#### VARIANT 14 / PROFILE 3.2
MODEL: IL-confirmed|Mitsubishi|Pajero
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='diesel'; engine='3.2L turbo'; engine_displacement_l=3.2; horsepower_hp=170; transmission='5-speed automatic'; drivetrain='4WD'; year_start=2007; year_end=2009; support_level='direct'; source_indexes=[0, 2]
PROBLEM: 2007-2009 3.2 diesel 170 hp row is historical and Israeli-grounded, but null trim hides Dakar/Desert/Limited/GLS lineage.
WEB-VALIDATED FACT: Pajero is a historical Israeli-market SUV and is absent from current Mitsubishi Israel model/price pages. Israeli Auto/iCar/Yad2 evidence supports 3.2 diesel, 3.8 petrol and older 2.8 diesel rows, but the broad 2010-2020 3.2 diesel 200 hp row is potentially too coarse: local listings show 200 hp for some 2014-2015 Desert/Dakar rows and also 190 hp for some 2016-2017 Dakar rows. Keep historical only and split or review horsepower/year coverage when repo-local evidence distinguishes 190/200 hp.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep row if field sources are valid. Add trim/lineage only where local sources support exact trim; do not currentize.
ACTION: KEEP / FIX TRIM

#### VARIANT 15 / PROFILE 3.3
MODEL: IL-confirmed|Mitsubishi|Pajero
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='3.8L v6'; engine_displacement_l=3.8; horsepower_hp=250; transmission='5-speed automatic'; drivetrain='4WD'; year_start=2007; year_end=2010; support_level='direct'; source_indexes=[0]
PROBLEM: 2007-2010 3.8 V6 petrol 250 hp 4WD row is supported by local Pajero price/listing context, but null trim is weak.
WEB-VALIDATED FACT: Pajero is a historical Israeli-market SUV and is absent from current Mitsubishi Israel model/price pages. Israeli Auto/iCar/Yad2 evidence supports 3.2 diesel, 3.8 petrol and older 2.8 diesel rows, but the broad 2010-2020 3.2 diesel 200 hp row is potentially too coarse: local listings show 200 hp for some 2014-2015 Desert/Dakar rows and also 190 hp for some 2016-2017 Dakar rows. Keep historical only and split or review horsepower/year coverage when repo-local evidence distinguishes 190/200 hp.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep historical row; fill Dakar/Limited style trim only if source supports. Do not currentize.
ACTION: KEEP / FIX TRIM

#### VARIANT 16 / PROFILE 3.4
MODEL: IL-confirmed|Mitsubishi|Pajero
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='diesel'; engine='3.2L turbo'; engine_displacement_l=3.2; horsepower_hp=165; transmission='5-speed automatic'; drivetrain='4WD'; year_start=2001; year_end=2006; support_level='direct'; source_indexes=[1]
PROBLEM: 2001-2006 3.2 diesel 165 hp row is historical and locally plausible; source/trim quality should remain valid.
WEB-VALIDATED FACT: Pajero is a historical Israeli-market SUV and is absent from current Mitsubishi Israel model/price pages. Israeli Auto/iCar/Yad2 evidence supports 3.2 diesel, 3.8 petrol and older 2.8 diesel rows, but the broad 2010-2020 3.2 diesel 200 hp row is potentially too coarse: local listings show 200 hp for some 2014-2015 Desert/Dakar rows and also 190 hp for some 2016-2017 Dakar rows. Keep historical only and split or review horsepower/year coverage when repo-local evidence distinguishes 190/200 hp.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep historical row; ensure source_indexes/field_sources are valid and add GLX/GLS style lineage only if supported. Do not currentize.
ACTION: KEEP / FIX SOURCE

#### VARIANT 17 / PROFILE 3.5
MODEL: IL-confirmed|Mitsubishi|Pajero
CURRENT VALUE: version_or_trim=None; body_type='SUV'; fuel_type='diesel'; engine='2.8L turbo'; engine_displacement_l=2.8; horsepower_hp=125; transmission='4-speed automatic'; drivetrain='4WD'; year_start=1994; year_end=2000; support_level='direct'; source_indexes=[3]
PROBLEM: 1994-2000 2.8 diesel 125 hp row is old historical Pajero evidence; keep only if source_indexes are valid and do not use as current clean.
WEB-VALIDATED FACT: Pajero is a historical Israeli-market SUV and is absent from current Mitsubishi Israel model/price pages. Israeli Auto/iCar/Yad2 evidence supports 3.2 diesel, 3.8 petrol and older 2.8 diesel rows, but the broad 2010-2020 3.2 diesel 200 hp row is potentially too coarse: local listings show 200 hp for some 2014-2015 Desert/Dakar rows and also 190 hp for some 2016-2017 Dakar rows. Keep historical only and split or review horsepower/year coverage when repo-local evidence distinguishes 190/200 hp.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep historical row; preserve 4WD/4-speed automatic if source supports. Do not currentize.
ACTION: KEEP / FIX SOURCE

### PROFILE 4: IL-confirmed|Mitsubishi|Pajero Sport
MODEL-LEVEL FACT: Pajero Sport is a historical Israeli-market SUV, not a current Mitsubishi Israel model. Local Auto/iCar evidence supports 2000-2008 Pajero Sport GLS rows. A 4x4 Israel launch article specifically supports the 3.0L V6 petrol automatic with 170 hp in Israel; Auto/iCar repo-local sources support the 2.5 turbo-diesel automatic 115 hp row if attached. Keep historical only.

#### VARIANT 18 / PROFILE 4.1
MODEL: IL-confirmed|Mitsubishi|Pajero Sport
CURRENT VALUE: version_or_trim='GLS'; body_type='SUV'; fuel_type='diesel'; engine='2.5L turbo'; engine_displacement_l=2.5; horsepower_hp=115; transmission='4-speed automatic'; drivetrain='4WD'; year_start=2000; year_end=2008; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Pajero Sport 2.5 turbo-diesel 115 hp automatic is supported by repo-local Auto/iCar sources if attached, but should remain historical only.
WEB-VALIDATED FACT: Pajero Sport is a historical Israeli-market SUV, not a current Mitsubishi Israel model. Local Auto/iCar evidence supports 2000-2008 Pajero Sport GLS rows. A 4x4 Israel launch article specifically supports the 3.0L V6 petrol automatic with 170 hp in Israel; Auto/iCar repo-local sources support the 2.5 turbo-diesel automatic 115 hp row if attached. Keep historical only.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep 2000-2008 GLS 2.5 turbo-diesel 115 hp, 4-speed automatic, 4WD only with valid local source_indexes/field_sources. If source support is missing, move to non-blocking review rather than fabricating.
ACTION: KEEP / FIX SOURCE

#### VARIANT 19 / PROFILE 4.2
MODEL: IL-confirmed|Mitsubishi|Pajero Sport
CURRENT VALUE: version_or_trim='GLS'; body_type='SUV'; fuel_type='petrol'; engine='3.0L v6'; engine_displacement_l=3.0; horsepower_hp=170; transmission='4-speed automatic'; drivetrain='4WD'; year_start=2000; year_end=2006; support_level='direct'; source_indexes=[0, 1]
PROBLEM: Pajero Sport 3.0 V6 petrol 170 hp automatic is directly supported by Israeli 4x4 launch article and local Auto/iCar evidence; keep historical only.
WEB-VALIDATED FACT: Pajero Sport is a historical Israeli-market SUV, not a current Mitsubishi Israel model. Local Auto/iCar evidence supports 2000-2008 Pajero Sport GLS rows. A 4x4 Israel launch article specifically supports the 3.0L V6 petrol automatic with 170 hp in Israel; Auto/iCar repo-local sources support the 2.5 turbo-diesel automatic 115 hp row if attached. Keep historical only.
SOURCE: repo-local sources listed in this profile plus RUN7 web anchors above.
TARGET VALUE: Keep 2000-2006 GLS 3.0 V6 petrol 170 hp, 4-speed automatic, 4WD if field_sources are valid. Do not currentize beyond 2006/2008 without local source.
ACTION: KEEP / FIX SOURCE

## Coverage assertion
RUN 7 contains 4 profiles and 19 technical variants. This task includes 19/19 explicit variant decisions.

## Report format after Codex run
Report: files changed, exact before/after metrics, confirmation all 4 profiles and 19 variants were handled, test results, confirmation temporary RUN7 instruction files were deleted before final commit, and remaining issues if any.

# ==============================
# FINAL
# source: BATCH26_FINAL_RUN_BLOCKERS_UNMATCHED_CODEX_TASK.md
# ==============================

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
