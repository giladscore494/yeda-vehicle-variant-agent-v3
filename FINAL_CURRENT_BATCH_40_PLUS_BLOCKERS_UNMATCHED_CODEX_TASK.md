# FINAL CURRENT BATCH CODEX TASK — 40 clean models + blockers + unmatched/split profiles

Date: 2026-06-17
Input repo ZIP: `yeda-vehicle-variant-agent-v3-validation-v2-budgeted-dual-il-trims (20).zip`

Codex has no web access. Do not browse. Use only the embedded evidence below and the local repository files.

## Execution order

1. Apply RUN 1 corrections.
2. Apply RUN 2 corrections.
3. Apply RUN 3 blockers, BYD Atto 3 EVO insertion, and unmatched/split-profile reconciliation.
4. Rebuild all `data/` outputs.
5. Run tests/quality/readiness.
6. Delete this temporary task file after successful verification.

## Final required state

```json
{
  "models_blocked": 0,
  "review_only_blocked_entries": 0,
  "duplicate_technical_variants": 0,
  "invalid_source_references": 0,
  "unknown_support_values": 0,
  "ready_for_website_upload": true,
  "unmatched_output_keys_count": 0,
  "unmatched_output_keys_sample": []
}
```

---

# RUN 1 — Current batch first 20 source models deep web validation

Date: 2026-06-17  
Repository input: `yeda-vehicle-variant-agent-v3-validation-v2-budgeted-dual-il-trims (20).zip`  
Scope: source groups **159–178**, from `IL|BMW|X3 xDrive30i` through `IL|BMW|X7 xDrive40i`.

Codex has no web access. Do not browse. Use the offline evidence and URLs embedded here plus the repository's local catalog/source files.

## Global hard rules

1. Israeli market only. Do not keep a clean row based only on global launch/spec information.
2. Validate every retained technical row field-by-field: `model`, `version_or_trim`, `body_type`, `fuel_type`, `engine`, `engine_displacement_l`, `horsepower_hp`, `transmission`, `drivetrain`, `year_start`, `year_end`, `sources`, `field_sources`, `available_values_for_website`.
3. Model designations such as `xDrive30i`, `xDrive40i`, `M50i`, `xDrive30d`, `X5 M`, `X6 M` are not separate trims. If no real marketed trim exists, keep `version_or_trim=null` and do **not** add `version_or_trim` to `missing_grounded_fields`.
4. Do not put `null`, `Base`, `Standard`, engine sizes, or model designations in `available_values_for_website.version_or_trim`.
5. If a modern row belongs under a different model identity, split it and add resume/source alias metadata so progress does not report it as unmatched.
6. Review-only profiles that can be grounded using the embedded evidence should be repaired into clean. Profiles that cannot be grounded should move to a non-blocking review/archive state, not remain active blockers.
7. After edits rebuild `data/model_technical_catalog_il.json`, `data/model_technical_catalog_il_review.json`, `data/model_technical_catalog_il_readiness.json`, and `data/model_technical_catalog_il_quality_scan.json`; run `pytest -q`, `python3 -m scripts.catalog_quality_scan`, and the repo readiness rebuild command.

## External evidence used in this RUN

- Cartube: 2018 BMW X3 Israel launch: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x3-החדש-2018-בישראל-מחיר-335000-שקל
- Cartube: 2022 BMW X3/X4 facelift variants: https://www.cartube.co.il/חדשות-רכב/מתיחת-פנים-2022-ב-מ-וו-x3-x4-החדשים
- Cartube: 2014 BMW X4 Israel launch: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x4-בישראל-–-מחיר-החל-מ-340-אלף-שקל
- Cartube: 2019 BMW X4 Israel launch: https://www.cartube.co.il/חדשות-רכב/2019-ב-מ-וו-x4-החדש-בישראל-מחיר-369000-שקל
- Cartube: 2019 BMW X5 Israel launch: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x5-החדש-2019-בישראל-מחיר-600000-שקל
- Cartube: 2024 BMW X5 Israel facelift: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x5-החדש-2024-בישראל-מחיר-685900-שקל
- Cartube: BMW X5 new-car price/spec page: https://www.cartube.co.il/מחירון-רכב-חדש/ב-מ-וו/ב-מ-וו-x5
- Cartube: 2024 BMW X5 xDrive50e M-Expressive spec: https://www.cartube.co.il/מחירון-רכב-חדש/ב-מ-וו/ב-מ-וו-x5/3661-ב-מ-וו-x5-פלאג-אין-5-מושבים-xdrive50e-m-expressive
- Cartube PDF: 2024 BMW X5 technical PDF: https://www.cartube.co.il/images/mifrat/bmw/37964-BMW-X5-2024-01.pdf
- Cartube: 2020 BMW X6 Israel launch: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x6-החדש-2020-בישראל-מחיר-650000-שקל
- BMW Israel: current BMW X6 official page/price list 04/2026: https://www.bmw.co.il/he/All-Models/x-series/x6/bmw-x6.html
- Auto.co.il: BMW X6 current technical summary: https://www.auto.co.il/cars/bmw/x6/
- Cartube: 2024 BMW X6 Israel facelift: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x6-החדש-2024-בישראל-מחיר-789900-שקל
- Cartube: BMW X7 2019 Israel launch: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x7-החדש-בישראל-מחיר-890000-שקל
- BMW Israel: current BMW X7 official page: https://www.bmw.co.il/he/All-Models/x-series/x7/bmw-x7.html
- BMW Israel: current BMW X7 technical data: https://www.bmw.co.il/he/All-Models/x-series/x7/bmw-x7-technical-data.html
- Auto.co.il: BMW X7 current summary: https://www.auto.co.il/cars/bmw/x7/
- Cartube: BMW M50i for X5/X7: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-מציגה-דגמי-קצה-m50i-ל-x5-ול-x7
- iCar: BMW X6 xDrive35i old generation example: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X6/ב.מ.וו_X6_יד_שניה_ד10/version7901/

---

# 159. BMW X3 xDrive30i

Current clean row:
- `version_or_trim=null`, SUV, petrol, `2.0L turbo`, 2.0L, 252 hp, 8AT, AWD, `year_start=2018`, `year_end=2021`.

Web validation:
- Israeli 2018 X3 launch confirms X3 G01 arrived in Israel at the beginning of March 2018 with engine range 184–360 hp.
- 2022 X3/X4 facelift evidence lists `X3 xDrive30i` with 2.0 turbo and **245 hp**, plus 8AT/AWD implied across the xDrive range.

Decision:
- **KEEP + ADD/FIX**.

Codex edits:
1. Keep the current pre-facelift row as 2018–2021, 2.0 turbo petrol, 252 hp, 8AT, AWD, SUV.
2. Add a facelift row if not already present:
   - `version_or_trim=null`
   - `body_type="SUV"`
   - `fuel_type="petrol"` unless local source explicitly says mild-hybrid
   - `engine="2.0L turbo"`
   - `engine_displacement_l=2.0`
   - `horsepower_hp=245`
   - `transmission="8-speed automatic"`
   - `drivetrain="AWD"`
   - `year_start=2021` or `2022` depending how this repo defines model-year vs Israeli launch date; prefer Israeli launch evidence if local source gives date.
   - `year_end=null` unless a direct Israeli discontinuation/current source exists.
3. Do not mark `version_or_trim` missing; `xDrive30i` is the model designation.

---

# 160. BMW X4 M40i

Current clean rows:
- 2016–2018, SUV, petrol, 3.0 turbo, 360 hp, 8AT, AWD.
- 2018–2019, SUV, petrol, 3.0 turbo, 354 hp, 8AT, AWD.
- 2021–2025, SUV, mild-hybrid, 3.0 turbo, 360 hp, 8AT, AWD.

Web validation:
- 2018/2019 X4 evidence supports X4 M40i in Israel with high-output 3.0 turbo around 354–360 hp.
- 2022 X3/X4 facelift evidence explicitly lists `X4 M40i` with 3.0 turbo and 360 hp.

Decision:
- **KEEP, but verify year-end/current claim**.

Codex edits:
1. Keep all three technical eras if local sources support them.
2. `version_or_trim` may remain null; `M40i` is the model designation, not trim.
3. For the 2021+ row, do not keep `year_end=2025` unless local source or current price/used-car generation evidence supports it. If no end is grounded, set `year_end=null` and keep clean only if all other fields are grounded.
4. Ensure `available_values_for_website.version_or_trim` does not include `M40i` or null.

---

# 161. BMW X4 xDrive20i

Current state:
- Review-only active profile, no clean technical variants.

Web validation:
- 2014 Israeli X4 launch states X4 offered in Israel with `X4 xDrive20i`, 2.0 turbo petrol, 184 hp, AWD/8AT family context.
- 2022 X3/X4 facelift evidence explicitly lists `X4 xDrive20i` with 2.0 turbo and 184 hp.

Decision:
- **REPAIR INTO CLEAN**.

Codex edits:
1. Create clean profile `BMW X4 xDrive20i` with at least these grounded rows:
   - pre/early generation row:
     - `version_or_trim=null`
     - `body_type="SUV"` or repo canonical SUV-coupe label if already supported; do not use invalid free-text `SUV Coupe` unless schema supports it.
     - `fuel_type="petrol"`
     - `engine="2.0L turbo"`
     - `engine_displacement_l=2.0`
     - `horsepower_hp=184`
     - `transmission="8-speed automatic"`
     - `drivetrain="AWD"`
     - `year_start=2014`
     - `year_end=2018` if local generation source supports.
   - facelift/newer row:
     - same technical values, `year_start=2021` or `2022`; only set `fuel_type="mild_hybrid"` if a local source explicitly says 48V.
2. Remove active review-only blocker for this model after clean repair.
3. Do not mark `version_or_trim` missing; `xDrive20i` is the model designation.

---

# 162. BMW X4 xDrive30i

Current clean rows:
- `M-Sport`, SUV, petrol, 2.0 turbo, 252 hp, 8AT, AWD, 2018–2021.
- `M-Sport`, SUV, mild_hybrid, 2.0 turbo, 245 hp, 8AT, AWD, 2021–null, `missing_grounded_fields=['year_end']`.

Web validation:
- 2018/2019 X4 launch evidence supports X4 xDrive30i around 252 hp.
- 2022 facelift evidence explicitly lists X4 xDrive30i with 2.0 turbo 245 hp.

Decision:
- **KEEP + CLEANUP**.

Codex edits:
1. Keep 2018–2021 252 hp row if local source supports `M-Sport`; otherwise set trim null or move trim evidence to missing.
2. Keep 2021/2022+ 245 hp row, but only mark `fuel_type=mild_hybrid` if local evidence says 48V. Otherwise use `petrol`.
3. Do not leave `missing_grounded_fields=['year_end']` if open-ended current/unknown end is accepted by schema. If schema requires grounding, use `year_end=null` with clear field source gap but not blocker.
4. `SUV Coupe` must remain invalid/non-trim/body alias only, not a trim.

---

# 163. BMW X5 3.0d

Current review rows include many diesel eras from 2002–2026, including rows that are actually modern `X5 xDrive30d`.

Web validation:
- 2019 Israeli X5 launch explicitly uses `xDrive30d` with 3.0 turbo diesel, 265 hp, 8AT, AWD.
- 2021/2023 sources in local profile support xDrive30d 286 hp era.
- 2024 X5 evidence supports facelift X5 diesel with 298 hp mild-hybrid and current price list shows X5 xDrive30d M-Executive with 298 hp for 2026.

Decision:
- **SPLIT + REPAIR**.

Codex edits:
1. Do not keep all modern rows under model `X5 3.0d` if the Israeli marketed name is `X5 xDrive30d`.
2. Keep historical `BMW X5 3.0d` rows only for old generations where the Israeli/used-car source truly labels them `3.0d`:
   - 2002–2003: diesel, ~2.9/3.0 inline-6 turbo, 184 hp, 5AT, AWD.
   - 2004–2006: 3.0 diesel, 218 hp, 6AT, AWD.
   - 2007–2010: 3.0 diesel, 235 hp, 6AT, AWD.
   - 2010–2013: 3.0 diesel, 245 hp, 8AT, AWD.
3. Move/split 2014+ rows into a separate clean profile `BMW X5 xDrive30d`:
   - 2014–2018: 3.0 diesel, 258 hp, 8AT, AWD.
   - 2019–2020: 3.0 diesel, 265 hp, 8AT, AWD; trims Elite/Superior if local source supports.
   - 2021–2023: 3.0 diesel, 286 hp, 8AT, AWD; trim M-Executive if source supports.
   - 2024–2026: 3.0 diesel mild-hybrid, 298 hp, 8AT, AWD; trim M-Executive; source: current Cartube X5 price page / 2024 PDF.
4. Add resume/source alias metadata so the split output `IL|BMW|X5 xDrive30d` maps back to the source group if needed.
5. After split, no active blocker should remain for `X5 3.0d`.

---

# 164. BMW X5 3.0i

Current clean row:
- SUV, petrol, `3.0L inline-6`, 231 hp, automatic, AWD, 2001–2006.

Web validation:
- Local profile sources iCar/KML support X5 first generation 3.0i era.

Decision:
- **KEEP**.

Codex edits:
1. Keep row if local sources support 231 hp, petrol, automatic, AWD, 2001–2006.
2. `version_or_trim=null` is acceptable; do not mark missing.
3. Ensure `field_sources.version_or_trim` is omitted/empty and not in website values.

---

# 165. BMW X5 4.4i

Current clean rows:
- 2000–2003, SUV, petrol, 4.4 V8, 286 hp, automatic, AWD.
- 2004–2006, SUV, petrol, 4.4 V8, 320 hp, automatic, AWD.

Web validation:
- Local profile sources Auto/Carzone support first-generation X5 4.4i split by engine output.

Decision:
- **KEEP**.

Codex edits:
1. Keep two output eras only if local source supports both.
2. If transmission can be grounded more specifically, use 5AT/6AT by year; otherwise `automatic` is acceptable only if the schema allows generic historical automatic.
3. Do not mark `version_or_trim` missing.

---

# 166. BMW X5 M

Current clean rows:
- 2009–2013, 4.4 V8 twin-turbo, 555 hp, 6AT, AWD.
- 2015–2019, 4.4 V8 twin-turbo, 575 hp, 8AT, AWD.
- 2020–2023, 4.4 V8 twin-turbo, 600 hp, 8AT, AWD.
- 2020–2023 Competition, 625 hp.
- 2023–2026 Competition, mild-hybrid, 625 hp.

Web validation:
- Cartube supports X5 M/X6 M Israel launches and 2023/2024 facelift Competition with 625 hp.
- The base 600 hp row must be retained only if local Israeli source distinguishes base X5 M from Competition; otherwise base row should move to review.

Decision:
- **KEEP COMPETITION; VERIFY BASE ROWS**.

Codex edits:
1. Keep historical 555 hp and 575 hp rows if iCar/Auto local sources support them.
2. For 2020–2023, keep both base 600 and Competition 625 only if local Israeli source lists both. If not, keep Competition 625 and move base 600 to review.
3. For facelift/current Competition mild-hybrid 625:
   - `year_start=2023` or `2024` depending Israeli launch/model-year convention.
   - Do not set `year_end=2026` unless current BMW/iCar/Auto price source supports current sale; otherwise use `year_end=null`.
4. `Competition` is a real trim/package and should appear in website trim values.

---

# 167. BMW X5 M50i

Current state:
- Review profile with one technical row: `Superior`, SUV, petrol, 4.4 V8 twin-turbo, 530 hp, 8AT, AWD, 2019–2023.

Web validation:
- Cartube M50i evidence supports X5/X7 M50i with 4.4 V8 twin-turbo and 530 hp.
- 2023 facelift replaced this identity with newer M60i/M models; do not extend M50i beyond 2023 without local evidence.

Decision:
- **REPAIR INTO CLEAN**.

Codex edits:
1. Move X5 M50i from active review to clean:
   - `version_or_trim="Superior"` only if source supports; otherwise null.
   - SUV, petrol, 4.4L V8 twin-turbo, 530 hp, 8AT, AWD, `year_start=2019`, `year_end=2023`.
2. Do not merge this into `X5 M` or `X5 xDrive50i`; M50i is its own model designation.
3. Remove active review blocker after repair.

---

# 168. BMW X5 xDrive40e

Current clean rows:
- Executive and Exclusive, SUV, PHEV, 2.0 turbo, 313 hp, 8AT, AWD, 2015–2018.

Web validation:
- Local profile sources Auto/Cartube support X5 plug-in launch in Israel at 313 hp.

Decision:
- **KEEP**.

Codex edits:
1. Keep Executive/Exclusive only if local source explicitly lists those trims; otherwise move unsupported trim names to review or null.
2. Keep technical fields: SUV, PHEV, 2.0 turbo, 313 hp, 8AT, AWD, 2015–2018.
3. Make sure website values include only real trims.

---

# 169. BMW X5 xDrive40i

Current clean rows:
- 2019–2023, SUV, petrol, 3.0 turbo, 340 hp, 8AT, AWD.
- 2023–2026, SUV, mild-hybrid, 3.0 turbo, 381 hp, 8AT, AWD.

Web validation:
- 2019 Israeli X5 launch explicitly supports xDrive40i, 3.0 turbo, 340 hp, 8AT, AWD.
- 2023 facelift evidence supports xDrive40i around 380/381 hp globally/for facelift context, but current 2024–2026 Israeli X5 price page found in this package emphasizes xDrive30d and xDrive50e; it does not clearly prove X5 xDrive40i remained a current 2026 Israeli official offer.

Decision:
- **KEEP 2019–2023; REVIEW OR LIMIT 381 HP ROW**.

Codex edits:
1. Keep 2019–2023 340 hp row.
2. Do **not** keep 2023–2026 381 hp row as current clean unless local Israeli source directly lists X5 xDrive40i after facelift.
3. If only facelift/global evidence exists, either:
   - set `year_end` to the last directly grounded Israeli year, or
   - move the 381 hp mild-hybrid row to review.
4. Do not mark `version_or_trim` missing.

---

# 170. BMW X5 xDrive45e

Current clean row:
- SUV, PHEV, 3.0 inline-6 turbo, 394 hp, 8AT, AWD, 2019–2023, `missing_grounded_fields=['version_or_trim']`.

Web validation:
- Cartube tag/listed evidence supports 2019 X5 xDrive45e PHEV in Israel at 394 hp.
- 2024 facelift replacement is xDrive50e, not xDrive45e.

Decision:
- **KEEP + CLEAR FALSE MISSING TRIM**.

Codex edits:
1. Keep 2019–2023 xDrive45e row.
2. Remove `version_or_trim` from `missing_grounded_fields`; `xDrive45e` is the model designation.
3. If no separate trim is grounded, keep `version_or_trim=null` and exclude null from website trim values.

---

# 171. BMW X5 xDrive50e

Current state:
- Active review-only profile with no clean variants.

Web validation:
- 2024 X5 Israel facelift source explicitly identifies new xDrive50e PHEV with about 490 hp and over 100 km electric range.
- Cartube 2024 spec page lists `xDrive50e M-Expressive`, PHEV, 2,998 cc, 489 hp, 8AT, 4X4, Israeli launch 25.01.2024.
- Current X5 price page lists 2026 `xDrive50e M-Expressive` with 489 hp.

Decision:
- **REPAIR INTO CLEAN**.

Codex edits:
1. Create clean technical row:
   - `version_or_trim="M-Expressive"`
   - `body_type="SUV"`
   - `fuel_type="plug_in_hybrid"`
   - `engine="3.0L inline-6 turbo phev"` or repo canonical equivalent
   - `engine_displacement_l=3.0`
   - `horsepower_hp=489` (or 490 only if repo normalizes rounded source text; prefer 489 from spec page)
   - `transmission="8-speed automatic"`
   - `drivetrain="AWD"`
   - `year_start=2024`
   - `year_end=2026` if current 2026 price page is used as source.
2. Remove active review-only blocker.
3. Do not merge with xDrive45e.

---

# 172. BMW X6 M

Current clean rows:
- 2010–2014 555 hp, 6AT, AWD.
- 2015–2019 575 hp, 8AT, AWD.
- 2020–2023 600 hp base.
- 2020–2023 Competition 625 hp.
- 2024–2024 Competition mild-hybrid 625 hp.

Web validation:
- Local sources support X6M generations and 2024 Competition facelift.
- If the source only supports Competition for modern years, base 600 hp row should not be over-retained.

Decision:
- **KEEP WITH MODERN BASE CHECK**.

Codex edits:
1. Keep old generation 555 and 575 hp if iCar/Auto sources support.
2. For 2020–2023, keep base 600 only with direct Israeli evidence; otherwise move to review and keep Competition 625.
3. For 2024+ Competition mild-hybrid:
   - keep `Competition`, 4.4 V8 twin-turbo mild hybrid, 625 hp, 8AT, AWD.
   - `year_end=2024` is too narrow if current source supports later sale; otherwise leave null rather than guessing.

---

# 173. BMW X6 xDrive30d

Current clean rows include older 235/245/258/265/286 hp rows, and 2021–2026 286 hp mild-hybrid rows for M-Sport/M-Expressive.

Web validation:
- 2020 Israeli X6 launch supports xDrive30d with 265 hp.
- BMW Israel current 04/2026 page lists X6 30d at **298 hp**, 8AT, AWD, diesel 48V mild-hybrid, with M-Sport and M-Expressive price lines.
- Auto current summary also states current X6 30d is 298 hp after 2024 facelift.
- Cartube 2024 article conflicts by saying 286 hp; prefer BMW Israel official/current and Auto for current 2026 technical value.

Decision:
- **FIX CURRENT ROWS**.

Codex edits:
1. Keep historical rows only if local sources support:
   - 2008–2010 235 hp.
   - 2010–2014 245 hp.
   - 2014–2019 258 hp with Luxury/M-Sport if grounded.
   - 2019–2021 265 hp with M-Sport/M-Expressive if grounded.
   - 2021–2023 286 hp mild-hybrid if grounded.
2. Do **not** keep 286 hp through 2026.
3. Add/replace current rows for 2024–2026:
   - `version_or_trim="M-Sport"`, diesel mild-hybrid, 3.0 inline-6 turbo, 298 hp, 8AT, AWD.
   - `version_or_trim="M-Expressive"`, same technical fields.
4. Cite BMW Israel current page and Auto current summary for the 298 hp current rows.

---

# 174. BMW X6 xDrive35i

Current clean row:
- SUV, petrol, 3.0 turbo, 306 hp, automatic, AWD, 2008–2019, missing version_or_trim.

Web validation:
- iCar old-generation source supports X6 xDrive35i, 3.0 petrol, AWD, automatic.
- The 2008–2019 single row likely merges E71 and F16 generations; technical output stayed around 306 hp but transmission/year handling differs.

Decision:
- **KEEP, preferably split by generation if local sources allow**.

Codex edits:
1. Remove `version_or_trim` from missing fields; xDrive35i is model designation.
2. If local sources support transmission split, split into:
   - 2008–2014, 3.0 turbo petrol, 306 hp, 6AT, AWD.
   - 2014–2019, 3.0 turbo petrol, 306 hp, 8AT, AWD.
3. If not enough local source detail, keep one row but do not overclaim exact gearbox beyond `automatic`.

---

# 175. BMW X6 xDrive50i

Current clean rows:
- 2008–2014, petrol, 4.4 V8 twin-turbo, 407 hp, automatic, AWD.
- 2014–2019, petrol, 4.4 V8 twin-turbo, 450 hp, automatic, AWD.

Web validation:
- Local iCar/Auto old generation sources support X6 xDrive50i 4.4 V8 twin-turbo and generation split.

Decision:
- **KEEP + OPTIONALLY REFINE TRANSMISSION**.

Codex edits:
1. Keep both rows.
2. If local source supports, set first-generation transmission to 6-speed automatic and second-generation to 8-speed automatic.
3. Remove false missing trim fields if present; xDrive50i is model designation.

---

# 176. BMW X7 M50i

Current clean row:
- SUV, petrol, 4.4 V8 twin-turbo, 530 hp, 8AT, AWD, 2019–2022.

Web validation:
- Cartube M50i source supports X5/X7 M50i 4.4 V8 twin-turbo with 530 hp.
- M50i should not be extended into facelift/current years without direct evidence; later X7 performance petrol identity may differ.

Decision:
- **KEEP**.

Codex edits:
1. Keep 2019–2022 if local source supports.
2. Do not merge with X7 M50d or xDrive40i.
3. Do not extend after facelift unless direct Israeli evidence exists.

---

# 177. BMW X7 xDrive30d

Current state:
- Active review-only profile with no technical variants.

Web validation:
- 2019 Israeli X7 launch explicitly lists X7 xDrive30d with 3.0 turbo diesel, 265 hp, 8AT, xDrive/AWD, Pure Excellence.
- Current BMW Israel X7 technical page lists a diesel 48V mild-hybrid with 352 hp, but this appears tied to current X7 diesel offer that may be named X7 40d/xDrive40d in some sources; do not force it into `xDrive30d` unless local profile source explicitly labels it xDrive30d.

Decision:
- **REPAIR HISTORICAL X7 xDrive30d; DO NOT POLLUTE CURRENT DIESEL IDENTITY**.

Codex edits:
1. Create clean row:
   - `version_or_trim="Pure Excellence"` if source supports.
   - `body_type="SUV"`
   - `fuel_type="diesel"`
   - `engine="3.0L inline-6 turbo"`
   - `engine_displacement_l=3.0`
   - `horsepower_hp=265`
   - `transmission="8-speed automatic"`
   - `drivetrain="AWD"`
   - `year_start=2019`
   - `year_end=2022` unless a direct local source supports longer xDrive30d sale.
2. If current 352 hp diesel is present locally as `X7 xDrive40d` or `X7 40d`, create/split to that separate model, not under xDrive30d.
3. Remove active review-only blocker after historical row is clean.

---

# 178. BMW X7 xDrive40i

Current review rows:
- M Sport, SUV, petrol, 3.0 I6 turbo, 340 hp, 8AT, AWD, 2019–2022.
- M Sport, SUV, mild_hybrid, 3.0 I6 turbo, 381 hp, 8AT, AWD, 2023–null, missing year_end.

Web validation:
- 2019 Israeli X7 launch explicitly lists xDrive40i, 3.0 turbo, 340 hp, 8AT, xDrive/AWD, Pure Excellence.
- 2023+ X7 facelift sources and current market data support xDrive40i around 381 hp in the Israeli market, but the exact current trim set may include Pure Excellence / M-Expressive / M-Sport depending source.

Decision:
- **REPAIR INTO CLEAN + TRIM CORRECTION**.

Codex edits:
1. Move X7 xDrive40i from active review to clean.
2. Correct 2019–2022 row:
   - If 2019 source lists `Pure Excellence`, use `version_or_trim="Pure Excellence"`, not `M Sport` unless local source supports M Sport for that era.
   - SUV, petrol, 3.0 I6 turbo, 340 hp, 8AT, AWD, 2019–2022.
3. Keep/add 2023+ row only if local Israeli evidence supports:
   - petrol mild-hybrid, 3.0 I6 turbo, 381 hp, 8AT, AWD.
   - `year_start=2023`.
   - `year_end=2026` only if current price/registration source supports current sale; otherwise `year_end=null`.
4. If current trim set is not fully grounded, use only trims with source support and put uncertain trims in review.
5. Remove active review-only blocker after clean repair.

---

## RUN 1 final expected state after Codex applies this file

This RUN alone may not clear all blockers because RUN 2 + RUN 3 will follow, but for the 20 source groups in this file:

- No active review-only blocker should remain for:
  - `BMW X4 xDrive20i`
  - `BMW X5 3.0d` after split/repair
  - `BMW X5 M50i`
  - `BMW X5 xDrive50e`
  - `BMW X7 xDrive30d`
  - `BMW X7 xDrive40i`
- False `version_or_trim` missing flags must be removed from model-designation rows.
- `X5 xDrive50e` must be clean and grounded as 2024–2026 M-Expressive PHEV 489 hp.
- `X6 xDrive30d` current rows must not remain 286 hp through 2026; current 2024–2026 rows should be 298 hp if grounded by BMW Israel/Auto.
- Split profiles introduced in this run must have alias/source lineage metadata where needed.


---

# RUN 2 — Deep web-backed validation task for current batch

Scope: next 20 source groups after RUN 1, source-group indexes 179–198 from the uploaded repo state.
Generated for Codex. Codex must not browse; all web research notes and source URLs are embedded here.

## Hard execution rules

1. Work only from the local repo files plus the web evidence embedded in this file.
2. Israeli market only. Do not keep a variant in clean if it is only globally plausible.
3. For every retained variant, validate field-by-field: make, model/canonical_model, version_or_trim, body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end.
4. If the row is grounded but currently in review, repair and move it to `data/model_technical_catalog_il.json`.
5. If the row cannot be grounded or belongs to a different canonical model, move it to non-blocking review/archive instead of leaving an active blocker.
6. Rebuild `sources`, `source_indexes`, `field_sources`, `available_values_for_website`, `invalid_or_non_trim_labels`, readiness, and quality scan after editing.
7. Do not leave `Base`, `Standard`, bare displacement values, engine labels, or mixed technical descriptions as visible website trims unless the evidence proves they are official marketed trim labels.
8. Preserve distinct model/body identities: `Gran Coupe` stays `Gran Coupe`; `Escalade IQ` is not regular `Escalade`; `Z4 sDrive20i` must not exist as both `BMW|Z4 sDrive20i` and `Bmw|z4 sdrive20i`.

## Exact RUN 2 source groups

179. BMW X7 xDrive40i
180. BMW XM
181. BMW Z3 1.8
182. BMW Z3 2.8
183. BMW Z3 M Roadster
184. BMW Z4 2.0i
185. BMW Z4 sDrive20i
186. Bmw z4 sdrive20i
187. BYD Atto 3
188. BYD Dolphin
189. BYD Han
190. BYD Seal
191. BYD Seal U
192. BYD Sealion 7
193. BYD Song Plus
194. BYD Tang
195. Cadillac ATS
196. Cadillac CTS
197. Cadillac Escalade
198. Cadillac Lyriq

---

## 179. BMW X7 xDrive40i

Current state: review-only active blocker with 2 variants:
- V00: `M Sport`, SUV, petrol, 3.0L I6 turbo, 340 hp, 8AT, AWD, 2019–2022.
- V01: `M Sport`, SUV, mild_hybrid, 3.0L I6 turbo, 381 hp, 8AT, AWD, 2023–null.

Web evidence:
- Existing catalog source: Cartube Israel `ב.מ.וו X7 החדש 2023 בישראל - מחיר החל מ-890,000 שקל`, URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x7-החדש-2023-בישראל-מחיר-החל-מ-890000-שקל
- Existing catalog source: iCar X7 model page, URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X7/
- Fresh web check: Carzone 2026 X7 shows xDrive40i Pure Excellence 4x4 6 seats as a sold/price-listed 2026 X7 variant; URL: https://www.carzone.co.il/BMW/X7/
- BMW Israel current X7 page currently emphasizes xDrive40d, so do not rely only on BMW Israel for the petrol 40i current row; use iCar/Carzone if they directly support 2026 xDrive40i.

Decision: FIX + MOVE TO CLEAN.

Exact Codex edits:
1. Move BMW X7 xDrive40i from review into clean if the existing local sources and the added Carzone/iCar evidence support the rows.
2. Keep the 2019–2022 340 hp petrol row only if source-level support exists for 340 hp / 3.0 I6 / 8AT / AWD / Israeli sale.
3. For the 2023+ facelift row:
   - Keep `fuel_type = mild_hybrid` only if the local source states mild-hybrid / 48V. Otherwise use `petrol` and add `mild_hybrid` only to notes.
   - `horsepower_hp = 381` is correct for the facelift petrol xDrive40i if supported.
   - Do not set `year_end = 2026` only because of global data. Set it to 2026 only if Carzone/iCar/current local source confirms 2026 xDrive40i.
   - If the current 2026 source names the trim as `Pure Excellence`, split or rename the current row accordingly: `M Sport` 2023-only/2023–2024 if supported, `Pure Excellence` 2026 if supported. Do not force every X7 xDrive40i row to `M Sport`.
4. Rebuild website values so `version_or_trim` contains only locally grounded trims: `M Sport` and/or `Pure Excellence` as supported.
5. Final state must not leave BMW X7 xDrive40i as active review-only blocker.

---

## 180. BMW XM

Current clean variants:
- `50e Ultimate`, SUV, PHEV, 3.0L I6 turbo, 476 hp, 8AT, AWD, 2023–null.
- `Ultimate`, SUV, PHEV, 4.4L V8 twin-turbo, 653 hp, 8AT, AWD, 2023–null.
- `Label Red`, SUV, PHEV, 4.4L V8 twin-turbo, 748 hp, 8AT, AWD, 2023–null.

Web evidence:
- BMW Israel official XM page confirms XM 50e as a PHEV with 6-cylinder M TwinPower Turbo + electric motor: https://www.bmw.co.il/he/All-Models/m-series/xm/bmw-xm.html
- Cartube Israel article confirms XM Red Label / Label Red with 748 hp: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-xm-רד-לייבל-נחשף-748-סוסים-היברידיים
- Existing catalog sources: iCar XM, Cartube XM launch, BMW Israel XM official page.

Decision: KEEP with minor year grounding cleanup.

Exact Codex edits:
1. Keep all 3 XM rows if local sources support them.
2. If the current BMW Israel official page is active and local sources confirm current sale, set `year_end = 2026` for currently sold rows or preserve `null` only if the project uses null for ongoing rows. Do not list `year_end` as a missing grounded field when an active official source supports current sale.
3. Keep `50e Ultimate`, `Ultimate`, and `Label Red` as real trims only if they appear in local BMW/iCar/Cartube sources.
4. Rebuild field_sources. No active blocker should remain here.

---

## 181. BMW Z3 1.8

Current clean variant:
- null trim, Roadster, petrol, 1.8L, 115 hp, manual, RWD, 1996–2002.

Web evidence:
- Existing iCar Z3 page supports Israeli used-market Z3 data: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_Z3/ב.מ.וו_Z3_יד_שניה_1/

Decision: KEEP.

Exact Codex edits:
1. Keep the row if iCar/Auto source supports 1.8L 115 hp, Roadster, manual, RWD, 1996–2002.
2. Keep `version_or_trim = null`; `1.8` is a model/engine designation, not a website trim.
3. Ensure `invalid_or_non_trim_labels` contains `1.8` as bare engine size / model designation.
4. Do not expose null or `1.8` under `available_values_for_website.version_or_trim`.

---

## 182. BMW Z3 2.8

Current clean variants:
- null trim, Roadster, petrol, 2.8L I6, 193 hp, manual, RWD, 1997–2000.
- null trim, Roadster, petrol, 2.8L I6, 193 hp, automatic, RWD, 1997–2000.

Web evidence:
- Existing Auto/iCar/Gear sources support the Z3 2.8 as a roadster with 2.8 inline-6, 193 hp, RWD, manual/automatic.
- Existing source URLs include Auto Z3, Gear Z3, and Levi/WinWin price-list references in the profile.

Decision: KEEP.

Exact Codex edits:
1. Keep both manual and automatic rows only if both transmissions are locally sourced.
2. Keep `version_or_trim = null`; `2.8` is model/engine designation, not a trim.
3. Ensure invalid labels include `2.8`, `193hp`, `Base`, `Standard` as non-trim labels.
4. Do not show null/Base/Standard under website trims.

---

## 183. BMW Z3 M Roadster

Current clean variant:
- null trim, Roadster, petrol, 3.2L I6, 321 hp, manual, RWD, 1998–2002; `missing_grounded_fields` includes `version_or_trim`.

Web evidence:
- Existing Auto/Levi sources support Z3 M Roadster.
- General BMW Z3/M evidence supports M Roadster as model identity, not a separate trim.

Decision: FIX minor missing-field classification.

Exact Codex edits:
1. Keep the row if sources support 3.2L inline-6, 321 hp, manual, RWD, Roadster, 1998–2002.
2. Remove `version_or_trim` from `missing_grounded_fields`. Here `M Roadster` is part of the model name, not a missing trim.
3. Keep `version_or_trim = null` and classify `M` under `invalid_or_non_trim_labels` as `model_name_part`.
4. Rebuild website values with no trim value for this model.

---

## 184. BMW Z4 2.0i

Current clean variant:
- null trim, Roadster, petrol, 2.0L I4, 150 hp, manual, RWD, 2005–2008; `missing_grounded_fields` includes `version_or_trim`.

Web evidence:
- Existing iCar and Auto Z4 generation-1 sources support Z4 2.0i Roadster.

Decision: FIX minor missing-field classification.

Exact Codex edits:
1. Keep the row if the iCar/Auto generation-1 sources support 2.0i, 150 hp, manual, Roadster, RWD, 2005–2008.
2. Remove `version_or_trim` from `missing_grounded_fields`; `2.0i` is the model designation.
3. Keep `version_or_trim = null`; do not expose `2.0i` as a website trim unless the project intentionally treats engine designation as visible model name, not trim.

---

## 185 + 186. BMW Z4 sDrive20i / Bmw z4 sdrive20i

Current problem:
There are two separate clean profiles for the same model identity:
- `BMW | Z4 sDrive20i` with null trim rows, including 184 hp and 197 hp rows.
- `Bmw | z4 sdrive20i` with proper trims `Sport Line`, `M-Sport`, `M-Design`.

Web evidence:
- iCar 2026 Z4 page confirms `sDrive20i M-Design`, 2.0, 197 hp, automatic: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_Z4/ב.מ.וו_Z4_חדש/version25774/
- BMW Israel official Z4 page confirms current Z4 Roadster family: https://www.bmw.co.il/he/All-Models/z-series/z4-roadster/bmw-z4-roadster.html
- Auto current Z4 page lists `sDrive20i, 2.0 turbo, M-Design` and also separate `sDrive30i M-Sport` / `M40i M-Superior`: https://www.auto.co.il/cars/bmw/z4/

Decision: FIX by canonical merge.

Exact Codex edits:
1. Merge `Bmw | z4 sdrive20i` into canonical key `IL|BMW|Z4 sDrive20i`.
2. Delete the duplicate lowercase/incorrect-casing profile after all variants and sources are safely merged.
3. Preserve historical row:
   - null trim or model-level row, Roadster, petrol, 2.0L turbo, 184 hp, 8AT, RWD, 2011–2016.
   - Remove `version_or_trim` missing marker because `sDrive20i` is model designation.
4. For 2019+ rows, prefer grounded marketed trims:
   - `Sport Line` 2019–2023 if source supports.
   - `M-Sport` 2019–2024 only if local source supports it specifically for sDrive20i. Do not confuse with current `sDrive30i M-Sport`.
   - `M-Design` 2023/2024–2026 if iCar/Auto/BMW Israel supports current `sDrive20i M-Design` at 197 hp.
5. Remove or merge the duplicate null 197 hp row if it is covered by the trimmed 2019+ rows.
6. Final clean catalog must have only one canonical model profile for `BMW Z4 sDrive20i`.
7. `available_values_for_website.version_or_trim` should show only real trims: `Sport Line`, `M-Sport` if supported, `M-Design`.
8. There must be no `Bmw` make casing and no lower-case `z4 sdrive20i` profile.

---

## 187. BYD Atto 3

Current clean problem:
The clean catalog currently keeps only old Atto 3 Comfort/Design 204 hp rows and incorrectly classifies `Evo AWD` / `Evo RWD` as labels belonging to BYD Seal. This is wrong.

Current clean rows:
- Comfort, SUV, electric, 204 hp, single-speed, FWD, 2022–2024.
- Design, SUV, electric, 204 hp, single-speed, FWD, 2022–2024.

Web evidence:
- BYD Israel official ATTO 3 EVO page: https://bydauto.co.il/model/byd-atto-3-evo/
- iCar current Atto 3 page says the updated model replaced the old 204 hp FWD powertrain with RWD 313 hp or AWD 448 hp: https://www.icar.co.il/BYD/BYD_אטו_3/BYD_אטו_3_חדש/
- Cartube 03.06.2026 confirms BYD Atto 3 EVO launched in Israel with Design RWD 313 hp and Excellence AWD 448/449 hp, prices from 154,990 NIS: https://www.cartube.co.il/חדשות-רכב/byd-אטו-3-evo-החדש-נחת-בישראל-מחיר-154990-שקל
- Auto current Atto 3 page lists `EVO חשמלי, Design, 2x4` and `EVO חשמלי, Excellence, 4x4`: https://www.auto.co.il/cars/byd/atto-3/

Decision: FIX materially.

Exact Codex edits:
1. Remove invalid classification that says `Evo AWD` / `Evo RWD` belong to BYD Seal. They belong to BYD Atto 3 EVO.
2. Keep old Atto 3 Comfort/Design 204 hp FWD rows for 2022–2025 if local sources support 2025; otherwise keep 2022–2024. Do not extend old 204 hp rows into the EVO generation unless source supports old FL sale in 2026.
3. Add new 2026 Atto 3 EVO rows:
   - `version_or_trim = "EVO Design"` or `"Design"` with `notes/model_generation = EVO` if schema supports it.
   - body_type SUV, fuel_type electric, engine electric, horsepower_hp 313, transmission single_speed, drivetrain RWD, year_start 2026, year_end 2026/current.
   - `version_or_trim = "EVO Excellence"` or `"Excellence"` with `notes/model_generation = EVO` if schema supports it.
   - body_type SUV, fuel_type electric, engine electric, horsepower_hp 448 or 449. Prefer 448 if using iCar/Auto; 449 if using Cartube. If both exist, standardize one value and note source discrepancy; do not create duplicate rows only for 448/449.
   - transmission single_speed, drivetrain AWD, year_start 2026, year_end 2026/current.
4. Rebuild website values to include old Comfort/Design and new EVO Design/EVO Excellence, without treating EVO as BYD Seal.
5. Add source entries for Cartube 2026, iCar current, and/or BYD official.

---

## 188. BYD Dolphin

Current clean rows:
- Comfort, Hatchback, electric, 204 hp, single-speed, FWD, 2023–2024.
- Design, Hatchback, electric, 204 hp, single-speed, FWD, 2023–2024.

Web evidence:
- BYD official Dolphin page: https://bydauto.co.il/model/byd-dolphin/
- Cartube current price/spec page lists 2026 Dolphin Comfort and Design, both 204 hp: https://www.cartube.co.il/מחירון-רכב-חדש/byd/byd-דולפין
- iCar used/new Dolphin pages support 204 hp, FWD, 427 km range: https://www.icar.co.il/BYD/BYD_דולפין/
- Auto current page says Dolphin uses a single motor, FWD, 204 hp: https://www.auto.co.il/cars/byd/dolphin/

Decision: FIX year_end.

Exact Codex edits:
1. Keep Comfort and Design 204 hp rows.
2. Update `year_end` to 2026/current if local current Cartube/BYD official/iCar page supports current sale.
3. Keep `engine_displacement_l = null` and include it in missing fields only if the schema demands it; for EV rows this should usually not block readiness.
4. Rebuild website values.

---

## 189. BYD Han

Current clean row:
- Executive, Sedan, electric, 518 hp, single-speed, AWD, 2022–2024.

Web evidence:
- Cartube Han Executive technical page confirms electric, 4x4, direct transmission, 518 hp: https://www.cartube.co.il/מחירון-רכב-חדש/byd/byd-האן/3327-byd-האן-executive
- Auto launch article confirms Han in Israel from 2022 with two motors, combined 518 hp, AWD: https://www.auto.co.il/articles/car-news/local-news/135411/
- BYD Israel / iCar profile currently describes Han as electric with 518 hp: https://www.icar.co.il/BYD/BYD_האן/

Decision: KEEP + current-year check.

Exact Codex edits:
1. Keep Executive 518 hp AWD sedan row.
2. If current BYD/iCar/Cartube source supports active sale in 2026, set `year_end = 2026`; otherwise keep 2024 and do not guess.
3. Keep transmission as `single_speed` / direct drive.
4. Do not add non-official trims.

---

## 190. BYD Seal

Current clean rows:
- Design, Sedan, electric, 313 hp, single-speed, RWD, 2024–null.
- Excellence, Sedan, electric, 530 hp, single-speed, AWD, 2024–null.

Web evidence:
- BYD official Seal page lists Design/Excellence: https://bydauto.co.il/model/byd-seal/
- Cartube launch confirms BYD Seal in Israel with Design and Excellence, electric sedan, 313/530 hp, RWD/AWD: https://www.cartube.co.il/חדשות-רכב/בי-וואי-די-סיל-byd-seal-בישראל-מחיר-החל-מ-216990-שקל
- iCar/Auto current pages support the model family.

Decision: KEEP.

Exact Codex edits:
1. Keep Design 313 RWD and Excellence 530 AWD.
2. Set `year_end = 2026` only if current official/BYD/iCar/Auto page supports 2026/current sale; otherwise keep null and remove year_end from blocking missing fields.
3. Keep engine descriptions like `Dual Electric Motors` under invalid/non-trim labels, not website trims.

---

## 191. BYD Seal U

Current review-only active blocker with 3 variants:
- EV null trim, SUV, electric, 218 hp, FWD, 2024–null.
- PHEV null trim, 1.5L, 218 hp, FWD, 2024–null.
- PHEV null trim, 1.5L turbo, 324 hp, AWD, 2024–null.

Current problem:
Official marketed trims were incorrectly classified as invalid mixed labels. For BYD, `Comfort DM-i` / `Design DM-i` are marketed trim-powertrain labels and should not be discarded if official sources use them.

Web evidence:
- BYD official Seal U DM-i page states: Boost/Comfort = 218 hp, Design = 324 hp AWD: https://bydauto.co.il/model/byd-seal-u-dmi/
- BYD official Seal U EV page confirms Comfort/Design EV variants: https://bydauto.co.il/model/byd-seal-u-ev/
- Auto Seal U page confirms EV version has 218 hp and Comfort/Design battery/trim split: https://www.auto.co.il/cars/byd/seal-u/
- Cartube Dec 2024 confirms Seal U plug-in Israel: 1.5 atmospheric FWD 218 hp and 1.5 turbo AWD 324 hp: https://www.cartube.co.il/חדשות-רכב/byd-סיל-u-פלאג-אין-בישראל-מחיר-209990-שקל

Decision: FIX + MOVE TO CLEAN.

Exact Codex edits:
1. Move BYD Seal U from review into clean.
2. Build/split rows using official marketed labels:
   - `Comfort EV` or `Comfort` with fuel_type electric, engine electric, 218 hp, FWD, single_speed, year_start 2024.
   - `Design EV` or `Design` with fuel_type electric, engine electric, 218 hp, FWD, single_speed, year_start 2024, if source confirms.
   - `Comfort DM-i` and/or `Boost DM-i` with fuel_type plug_in_hybrid, engine 1.5L, combined horsepower 218, automatic, FWD, year_start 2024, only for trims supported by official source.
   - `Design DM-i` with fuel_type plug_in_hybrid, engine 1.5L turbo, combined horsepower 324, automatic, AWD, year_start 2024.
3. Do not leave all variants with `version_or_trim = null` when official trims exist.
4. Move `1.5L PHEV`, `1.5L Turbo PHEV`, `Electric` to invalid/non-trim labels as powertrain labels.
5. Remove `Comfort DM-i` and `Design DM-i` from invalid_or_non_trim_labels if they are used as official marketed trims.
6. Rebuild website values to expose real trims and both powertrains.
7. Final state must not leave BYD Seal U as active review-only blocker.

---

## 192. BYD Sealion 7

Current clean rows:
- Boost, SUV, electric, 231 hp, RWD, 2025–null.
- Design, SUV, electric, 313 hp, RWD, 2025–null.
- Excellence, SUV, electric, 530 hp, AWD, 2025–null.

Web evidence:
- BYD official Sealion 7 page: https://bydauto.co.il/model/byd-sealion-7/
- Cartube launch confirms Sealion 7 Israel from May 2025, Boost 231 hp RWD, Comfort/Design 313 hp RWD, Excellence 530 hp AWD: https://www.cartube.co.il/חדשות-רכב/byd-סיליאון-7-בישראל-מחיר-218990-שקל
- iCar current page says 231/313 hp RWD and AWD 531 hp: https://www.icar.co.il/BYD/BYD_סיליון_7/BYD_סיליון_7_חדש/

Decision: FIX possible missing Comfort row + current-year cleanup.

Exact Codex edits:
1. Keep Boost 231 RWD, Design 313 RWD, Excellence 530 AWD.
2. Check if official/BYD/Cartube local source has a `Comfort` 313 hp row. If yes, add it; if not, do not invent it.
3. Keep 530 hp or 531 hp consistently. Prefer the importer/Cartube value if direct. If sources disagree by 1 hp due to rounding, choose one normalized value and note discrepancy in notes/source supports.
4. If current source supports 2026 sale, set `year_end = 2026`; otherwise preserve null/current handling without blocking.

---

## 193. BYD Song Plus

Current review-only active blocker with 3 variants:
- `Design`, SUV, plug_in_hybrid, 1.5L turbo, 324 hp, AWD, 2024–null.
- `Comfort`, SUV, plug_in_hybrid, 1.5L, 218 hp, FWD, 2024–null.
- null trim, SUV, electric, 204 hp, FWD, 2023–null.

Current problem:
The PHEV rows are actually BYD Seal U DM-i official-market rows, not Song Plus clean rows. The EV Song Plus was a parallel-import/alternate naming case and must not be mixed with official Seal U DM-i.

Web evidence:
- Existing source says BYD Israel official page for `SEAL U DM-i` is export name for Song Plus, but the Israeli website and official marketing use `Seal U DM-i`, not `Song Plus`.
- Cartube source in the profile identifies `BYD Song Plus EV` as a parallel import launch in Israel: https://www.cartube.co.il/חדשות-רכב/בי-וו-אי-די-byd/סונג-פלוס-החשמלי-בישראל-יבוא-מקביל
- BYD Seal U DM-i official source belongs under `BYD Seal U`: https://bydauto.co.il/model/byd-seal-u-dmi/

Decision: FIX by remap / non-blocking archive.

Exact Codex edits:
1. Do not promote the PHEV `Comfort` / `Design` rows under `BYD Song Plus`. Move/remap them to `BYD Seal U` as `Comfort DM-i` / `Design DM-i` if they are not already represented there.
2. For `BYD Song Plus`, keep only the parallel-import EV 204 hp FWD row if the project allows parallel-import models in clean and the Cartube source directly supports Israeli sale. If project scope is official-importer only, move it to non-blocking review/archive.
3. If kept clean:
   - model = `Song Plus`
   - body_type = SUV
   - fuel_type = electric
   - engine = electric
   - horsepower_hp = 204
   - transmission = single_speed
   - drivetrain = FWD
   - year_start = 2023
   - year_end = null or grounded year_end if sourced.
4. Final state must not leave `BYD Song Plus` as active review-only blocker. Either clean grounded EV-only or archive non-blocking.
5. Do not let `Song Plus` pollute `Seal U`, and do not let `Seal U DM-i` pollute `Song Plus`.

---

## 194. BYD Tang

Current clean row:
- Premium, SUV, electric, 518 hp, single-speed, AWD, 2022–2024.

Web evidence:
- BYD official Tang page states 517 hp from front/rear electric motors: https://bydauto.co.il/model/tang/
- iCar 2026 Tang Premium page supports 518 hp: https://www.icar.co.il/BYD/BYD_טאנג/BYD_טאנג_חדש/version24812/
- Cartube 2026 Tang Flagship page supports 518 hp, 4x4, direct transmission, electric: https://www.cartube.co.il/מחירון-רכב-חדש/byd/byd-טאנג/5930-byd-טאנג-flagship

Decision: FIX current trim/year handling.

Exact Codex edits:
1. Keep 2022–2024/2025 Tang Premium 518 hp AWD if supported.
2. Do not leave year_end at 2024 if current local source supports Tang in 2026.
3. Check whether current 2026 trim is officially called `Premium` or `Flagship`:
   - If iCar/BYD official says Premium, keep Premium through 2026.
   - If Cartube/importer says Flagship for 2026, split into Premium historical and Flagship 2026 row.
4. Use 518 hp as normalized value if most local sources use it; if importer states 517 hp, note discrepancy but avoid duplicate 517/518 rows.
5. Keep old PHEV/engine labels in invalid_or_non_trim_labels only if present; do not create PHEV Tang rows unless Israeli source directly supports them.

---

## 195. Cadillac ATS

Current review-only active blocker with 6 strong variants:
- Sedan Luxury/Premium, 2.0 turbo 272 hp, 6AT, RWD, 2013–2015.
- Sedan Luxury/Premium, 2.0 turbo 272 hp, 8AT, RWD, 2016–2019.
- Coupe Premium, 2.0 turbo 272 hp, 6AT, RWD, 2015.
- Coupe Premium, 2.0 turbo 272 hp, 8AT, RWD, 2016–2019.

Web evidence:
- iCar ATS 2015 Premium confirms 272 hp: https://www.icar.co.il/קדילאק/קדילאק_ATS/קדילאק_ATS_יד_שניה_ד10/version13678/
- Auto ATS Coupe 2015 test confirms coupe has same 272 hp and 6-speed automatic: https://www.auto.co.il/articles/test-drives/111044/
- Cartube ATS tag page confirms 2016 refreshed ATS/CTS in Israel with 8-speed automatic: https://www.cartube.co.il/component/tags/tag/קאדילק-ats
- Auto ATS 2016 Luxury page confirms 2.0 turbo, RWD, 8 speeds: https://www.auto.co.il/cars/cadillac/ats/2016/501974/
- Gear ATS 2018 test confirms 2.0 turbo 272 hp, 8AT, RWD: https://www.gear.co.il/כתבת-רכב/2018-06-21-N03-מבחן-דרכים-קאדילק-ATS

Decision: FIX + MOVE TO CLEAN.

Exact Codex edits:
1. Move Cadillac ATS from review into clean.
2. Keep the six current rows if all fields are supported by iCar/Auto/Cartube/Gear sources.
3. Keep Luxury and Premium as real equipment/version labels for ATS if iCar/Auto source pages list them.
4. Keep `2.0L Turbo` in invalid_or_non_trim_labels as engine label, not website trim.
5. Do not add ATS-V unless it is in the source group and local sources are added; this RUN2 task validates current source group rows only.
6. Final state: Cadillac ATS must not remain active review-only blocker.

---

## 196. Cadillac CTS

Current clean rows include:
- Early CTS V6 rows: 3.2/2.8/3.6/3.0.
- CTS-V 6.2 supercharged 556 hp, 2009–2013.
- Third-gen 2.0 turbo 272 hp, 2014–2015 6AT and 2016–2019 8AT.
- CTS-V 6.2 supercharged 640 hp, 2016–2019.

Web evidence:
- Existing sources include Auto/iCar/Cartube/Gear.
- Cartube CTS 2014 local launch supports third-generation CTS in Israel.
- Gear/Cartube support 8-speed updates around 2016.
- Global GM/CTS evidence supports 2.0 turbo 272 hp and CTS-V 640 hp, but clean retention should still rely on local sources already embedded.

Decision: KEEP with website-trim cleanup check.

Exact Codex edits:
1. Keep all CTS rows only if existing local sources support the fields.
2. `Elegance`, `Luxury`, and `Premium` are currently in invalid labels. If they are actual Israeli CTS trims and appear in iCar/Auto sources, do not mark them invalid; if they do not create technical differences, keep them out of website trim values but classify as equipment packages. Be consistent with how ATS handles Luxury/Premium.
3. Keep `V` as visible trim only for CTS-V rows.
4. Verify no duplicate technical variants are created by removing equipment packages.
5. Rebuild website values and field_sources.

---

## 197. Cadillac Escalade

Current review-only active blocker is empty: no sources and no variants.

Raw source hints:
- years_seen: 2007, 2014, 2015, 2020, 2021, 2025, 2026.
- trims_seen: `Luxury Sport`, `Sport Platinum`.
- engines_seen: `6.2L V8`, `Electric`.
- fuel_types: petrol/electric.
- drivetrains: 4WD/AWD.

Web evidence for regular petrol Escalade:
- Cartube 06.09.2022 confirms new Cadillac Escalade in Israel with 6.2L V8, 420 hp, 10-speed automatic and selectable RWD/4WD: https://www.cartube.co.il/חדשות-רכב/קאדילק-אסקלייד-החדש-2022-בישראל-מחיר-899990-שקל
- Auto current Escalade page confirms 6.2L atmospheric V8, 420 hp, 10-speed automatic: https://www.auto.co.il/cars/cadillac/escalade/
- Yad2 price list confirms Israeli Escalade trims/years with 6.2 420 hp for 2018–2026 and variants such as Premium Luxury, Platinum, Sport, ESV: https://www.yad2.co.il/price-list/feed?manufacturer=47&model=10684
- Carzone 2021 Escalade confirms 6162 cc, 420 hp, AWD: https://www.carzone.co.il/Cadillac/Escalade/2021/

Web evidence for electric split model:
- Cadillac Israel official Escalade IQ page: https://www.cadillac.co.il/ESCALADE-IQ/
- Cadillac Israel technical spec page states Escalade IQ Premium Luxury / Luxury Sport, AWD, two motors, 750 hp, 205 kWh battery, 740 km range: https://www.cadillac.co.il/דגמים/escalade-iq/מפרט-טכני/
- Cartube confirms Escalade IQ launched in Israel in 2025 with AWD 750 hp and two trim/design styles: https://www.cartube.co.il/חדשות-רכב/הענק-החשמלי-נחת-בישראל-קאדילק-iq-במחיר-700000-שקל

Decision: FIX by creating clean petrol Escalade + split electric Escalade IQ.

Exact Codex edits:
1. Do not leave Cadillac Escalade as empty active review-only blocker.
2. Create/repair clean `Cadillac Escalade` petrol profile:
   - body_type: SUV
   - fuel_type: petrol
   - engine: `6.2L v8`
   - engine_displacement_l: 6.2
   - horsepower_hp: 420
   - transmission: `10-speed automatic` for 2021/2022+ row.
   - drivetrain: AWD/4WD. Use one normalized value consistently; prefer `AWD` if schema uses AWD for SUVs, but keep source support for 4WD.
   - year_start: 2021 or 2022 for the new local generation row depending on source. Cartube launch article says 2022 Israel launch; Carzone has 2021 model-year page. Use 2022 for Israeli launch if uncertain.
   - year_end: 2026 if current Auto/Yad2 supports current petrol Escalade.
   - trims: include only grounded trims such as Premium Luxury / Platinum / Sport / Luxury Sport / Sport Platinum / ESV if source pages support them. If trim evidence is weak, keep version_or_trim null and place labels in notes/review, but do not block the whole model.
3. Split electric rows out of regular `Escalade` into a separate clean model `Cadillac Escalade IQ` if the source group contains electric.
   - model: `Escalade IQ`
   - body_type: SUV
   - fuel_type: electric
   - engine: electric
   - horsepower_hp: 750
   - transmission: single_speed/direct
   - drivetrain: AWD
   - year_start: 2025 or 2026 depending on local launch/source. Cartube says launched in Israel 2025; official page is 2026 model.
   - trims: `Premium Luxury`, `Luxury Sport` if official Cadillac Israel technical page supports them.
4. Add split-profile lineage mapping if needed:
   - `IL|Cadillac|Escalade IQ` split_from_source_group_key = `IL|Cadillac|Escalade`
   - This split must not appear later as unmatched output.
5. Final state: no empty active Escalade review profile. Either clean Escalade + clean Escalade IQ split, or clean Escalade and non-blocking archive for unsupported electric rows.

---

## 198. Cadillac Lyriq

Current review-only active blocker with 1 variant:
- `Luxury AWD`, SUV, electric, 515 hp, AWD, 2025–2026; missing `engine_displacement_l` and `transmission`.

Web evidence:
- Cadillac Israel Lyriq official page confirms Luxury AWD, electric motor 515 hp, 102 kWh battery, AWD: https://www.cadillac.co.il/דגמים/lyriq/
- Cadillac Israel 2025 PDF confirms Permanent magnet electric motor, AWD two motors, 515 hp: https://www.cadillac.co.il/media/wajbd0yz/lyriq_mifrat_tech_2025_web.pdf
- Cartube Lyriq AWD Luxury technical page confirms electric, 515 hp, 4x4 and direct transmission: https://www.cartube.co.il/מחירון-רכב-חדש/קאדילק/קאדילק-ליריק/5325-קאדילק-ליריק-awd-luxury

Decision: FIX + MOVE TO CLEAN.

Exact Codex edits:
1. Move Cadillac Lyriq from review into clean.
2. Keep version_or_trim as `Luxury AWD` or `AWD Luxury`; choose one normalized visible value. Prefer the official Cadillac Israel naming if present.
3. Set:
   - body_type = SUV
   - fuel_type = electric
   - engine = electric
   - engine_displacement_l = null
   - horsepower_hp = 515
   - transmission = single_speed or direct drive / `single_speed` normalized value. Do not leave transmission null if Cartube/official source supports direct transmission.
   - drivetrain = AWD
   - year_start = 2025
   - year_end = 2026/current if official source supports.
4. For EV variants, `engine_displacement_l = null` must not block readiness. Adjust validation if needed so EV rows are not blocked for missing displacement.
5. Keep `Dual Electric Motor 515 hp` in invalid_or_non_trim_labels as non-trim technical description, but do not invalidate `Luxury AWD` if official.
6. Final state: Cadillac Lyriq must not remain active review-only blocker.

---

## RUN 2 final verification requirements

After applying this RUN 2 task:

1. Rebuild:
   - `data/model_technical_catalog_il.json`
   - `data/model_technical_catalog_il_review.json`
   - `data/model_technical_catalog_il_readiness.json`
   - `data/model_technical_catalog_il_quality_scan.json`
2. Run:
   - `pytest -q`
   - `python3 -m scripts.catalog_quality_scan`
   - the repo readiness rebuild command.
3. Report:
   - Which RUN 2 models moved from review to clean.
   - Which rows were remapped to another model, especially `Escalade IQ` and `Seal U` / `Song Plus`.
   - Whether `Bmw|z4 sdrive20i` was merged into `BMW|Z4 sDrive20i`.
   - Final readiness values for models_blocked, review_only_blocked_entries, duplicate_technical_variants, invalid_source_references, unknown_support_values, ready_for_website_upload.
4. Do not start RUN 3/blockers yet unless this is part of a larger final unified task file.


---

# RUN 3 — Current batch blockers, unmatched/split profiles, and Atto 3 EVO deep web validation

Date: 2026-06-17  
Repository input: `yeda-vehicle-variant-agent-v3-validation-v2-budgeted-dual-il-trims (20).zip`  
Scope: current active review-only blockers + current unmatched/split profiles + BYD Atto 3 EVO split-profile insertion discovered during RUN 2.

Codex has no web access. Do not browse. Use only the offline evidence and URLs embedded here plus the repository's local catalog/source files.

## Current state found in the uploaded repo

`data/model_technical_catalog_il_readiness.json` currently reports:

```json
{
  "total_models": 200,
  "models_blocked": 11,
  "review_only_blocked_entries": 11,
  "duplicate_technical_variants": 0,
  "invalid_source_references": 0,
  "unknown_support_values": 0,
  "ready_for_website_upload": false
}
```

`data/model_technical_catalog_il_review.json` has 11 active review-only blockers:

1. `IL|BMW|X4 xDrive20i`
2. `IL|BMW|X5 3.0d`
3. `IL|BMW|X5 M50i`
4. `IL|BMW|X5 xDrive50e`
5. `IL|BMW|X7 xDrive30d`
6. `IL|BMW|X7 xDrive40i`
7. `IL|BYD|Seal U`
8. `IL|BYD|Song Plus`
9. `IL|Cadillac|ATS`
10. `IL|Cadillac|Escalade`
11. `IL|Cadillac|Lyriq`

The resume state also has unmatched output/split-profile keys to reconcile:

- `IL|Alfa Romeo|Junior Elettrica`
- `IL|BMW|M850i`

RUN 2 also discovered that the new `BYD Atto 3 EVO` must be inserted as a legitimate split/new clean profile instead of being mis-scoped under `BYD Seal` or ignored as not-yet-run.

## Global rules for this RUN

1. Do not leave empty active blocked profiles in review.
2. If a review profile can be grounded with the embedded evidence, repair it into `data/model_technical_catalog_il.json`.
3. If a row cannot be grounded, move it to a non-blocking archive/review state that does not count as `review_only_blocked_entries`.
4. Rebuild `sources`, `source_indexes`, `field_sources`, `available_values_for_website`, and `invalid_or_non_trim_labels` after every profile edit.
5. For EV/PHEV profiles, do not let `engine_displacement_l=null` block readiness when `fuel_type=electric` and `engine=electric`; engine displacement is not applicable for pure EV rows.
6. For EV rows, use `transmission="single_speed"` where the catalog convention requires a visible website value and the row is a direct-drive electric vehicle. If the repo validator is changed instead, pure EV rows with null transmission must not be considered active blockers, but website values should remain consistent with the rest of the catalog.
7. Add explicit source/split lineage for legitimate output profiles that do not exist as one-to-one source keys, so `unmatched_output_keys_count` becomes 0.
8. Final required state:

```json
{
  "models_blocked": 0,
  "review_only_blocked_entries": 0,
  "duplicate_technical_variants": 0,
  "invalid_source_references": 0,
  "unknown_support_values": 0,
  "ready_for_website_upload": true,
  "unmatched_output_keys_count": 0,
  "unmatched_output_keys_sample": []
}
```

---

# Embedded external evidence for RUN 3

## BMW X4 xDrive20i

- Cartube 2014 BMW X4 details: `X4 xDrive20i` with 2.0L turbo petrol, 184 hp; all X4 versions use xDrive AWD and 8-speed automatic.
  - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x4-החדש-–-הפרטים-המלאים
- Cartube 2018 BMW X4 details: `X4 xDrive20i` with 2.0L turbo petrol, 184 hp; all versions use xDrive AWD and 8AT.
  - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-חושפת-את-ה-x4-החדש-לשנת-2018
- Cartube 2022 X3/X4 facelift: `X4 xDrive20i` appears in Israel in Executive and M-Sport trims.
  - URL: https://www.cartube.co.il/חדשות-רכב/דגמי-2022-החדשים-של-ב-מ-וו-x3-x4-נחתו-בישראל
- Cartube 2022 X3/X4 technical: `X4 xDrive20i` 2.0 turbo 184 hp.
  - URL: https://www.cartube.co.il/חדשות-רכב/מתיחת-פנים-2022-ב-מ-וו-x3-x4-החדשים

### Required Codex edit — BMW X4 xDrive20i

Current issue: active review-only blocker with empty `technical_variants_il` caused by non-object JSON output.

Repair into clean. Create a clean profile for `BMW X4 xDrive20i`:

Recommended clean rows:

1. Historical / first generation row:
   - `version_or_trim`: null unless local source directly distinguishes trim
   - `body_type`: `SUV Coupe`
   - `fuel_type`: `petrol`
   - `engine`: `2.0L turbo`
   - `engine_displacement_l`: 2.0
   - `horsepower_hp`: 184
   - `transmission`: `8-speed automatic`
   - `drivetrain`: `AWD`
   - `year_start`: 2014
   - `year_end`: 2018 or 2019 only if local source supports the exact end

2. Later / facelift rows if local sources support them:
   - `version_or_trim`: `Executive`
   - same technical fields as above
   - `year_start`: 2022
   - `year_end`: null or 2024/2025 only if local catalog source supports it
   - `version_or_trim`: `M-Sport`
   - same technical fields as above
   - `year_start`: 2022
   - `year_end`: null or 2024/2025 only if local catalog source supports it

Do not keep the empty review profile. Do not put `xDrive20i` in `version_or_trim`; it is the model identity.

---

## BMW X5 3.0d

Embedded local review profile already contains 8 grounded-looking diesel rows but all variants are blocked because `source_indexes` are missing even though `field_sources` point to valid sources.

Existing review sources include:

- iCar X5 catalog: https://www.icar.co.il/bmw/x5/
- Cartube 2019 X5 Israel launch: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x5-החדש-2019-בישראל-מחיר-600000-שקל
- Cartube 2021 X5/X6 engine updates: https://www.cartube.co.il/חדשות-רכב/החל-מ-615000-שקל-דגמי-2021-של-ב-מ-וו-x5-ו-x6-עם-מנועים-חדשים
- Cartube 2024 X5/X6 facelift: https://www.cartube.co.il/חדשות-רכב/מתיחת-פנים-2024-ב-מ-וו-x5-ו-x6-החדשים-בישראל-מחיר-החל-מ-729900-שקל

Additional evidence:

- Cartube 2019 confirms the new X5 Israel launch in `xDrive30d` form with 265 hp, not as a generic `X5 3.0d`.
  - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x5-החדש-2019-בישראל-מחיר-600000-שקל
- Cartube 2024 confirms the facelifted X5 PHEV/diesel generation but modern naming is `xDrive30d` / `xDrive50e` rather than old `3.0d`.
  - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x5-החדש-2024-בישראל-מחיר-685900-שקל

### Required Codex edit — BMW X5 3.0d

Current issue: blocked due missing `source_indexes` and identity pollution between historical `X5 3.0d` and modern `X5 xDrive30d`.

Apply:

1. Historical rows only should remain under `BMW X5 3.0d`:
   - 2002–2003: 2.9L turbo inline-6 diesel, 184 hp, 5AT, AWD.
   - 2004–2006: 3.0L turbo inline-6 diesel, 218 hp, 6AT, AWD.
   - 2007–2010: 3.0L turbo inline-6 diesel, 235 hp, 6AT, AWD.
   - 2010–2013: 3.0L turbo inline-6 diesel, 245 hp, 8AT, AWD.
   - 2014–2018: 3.0L turbo inline-6 diesel, 258 hp, 8AT, AWD.

2. Modern rows in the current review profile must not remain under `X5 3.0d`:
   - 2019–2020 265 hp row is `BMW X5 xDrive30d`.
   - 2021–2023 286 hp row is `BMW X5 xDrive30d`.
   - 2024–2026 298 hp row is `BMW X5 xDrive30d` / current diesel naming if locally supported.

3. Either merge these modern rows into an existing clean `BMW X5 xDrive30d` profile, or create a new clean `BMW X5 xDrive30d` profile with `source_group_key`/alias from the relevant source group.

4. For any retained historical `X5 3.0d` variants, add `source_indexes` equal to the union of all `field_sources` values for that variant. The blocker was technical: field_sources existed but source_indexes were missing.

5. Remove the active review-only blocker after moving/repairing all rows.

---

## BMW X5 M50i

Embedded review profile contains a good single row but is blocked because `source_indexes` are missing.

Sources already embedded in the review profile:

- Cartube: `BMW X5 and X7 M50i in Israel`, supports trim/body/fuel/engine/displacement/hp/transmission/drivetrain/year_start.
  - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x5-ו-x7-בגרסת-m50i-בישראל
- iCar X5 fourth generation catalog.
  - URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X5/ב.מ.וו_X5_יד_שניה_-_דור_4/
- Cartube 2023 X5 facelift/news for year end.
  - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x5-החדש-2023-בישראל-מחיר-החל-מ-719,900-שקל

External evidence also confirms BMW M50i models use 4.4L V8 twin-turbo, 530 hp.

### Required Codex edit — BMW X5 M50i

Repair into clean:

- `model`: `X5 M50i`
- `version_or_trim`: `Superior` if supported by the Israel source; otherwise null and do not put `M50i` in trim.
- `body_type`: `SUV`
- `fuel_type`: `petrol`
- `engine`: `4.4L v8 twin-turbo`
- `engine_displacement_l`: 4.4
- `horsepower_hp`: 530
- `transmission`: `8-speed automatic`
- `drivetrain`: `AWD`
- `year_start`: 2019
- `year_end`: 2023 if iCar/Cartube local sources support; otherwise leave null and do not mark as missing if not critical.
- Add `source_indexes` to the variant, using `[0, 1, 2]` or the exact valid local source indexes in the profile.

Remove the active review-only blocker after repair.

---

## BMW X5 xDrive50e

Current issue: active empty review-only blocker due JSON parsing error.

Evidence:

- Cartube 2024 X5 Israel facelift says the new X5 includes a new PHEV model with about 490 hp and electric range around 104 km.
  - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x5-החדש-2024-בישראל-מחיר-685900-שקל
- Cartube 2025 X5 xDrive50e M-Expressive spec page lists: 2,998 cc, plug-in, 489 hp, 8-speed automatic, 4X4, 25.7 kWh battery, 104 km electric range.
  - URL: https://www.cartube.co.il/מחירון-רכב-חדש/ב-מ-וו/ב-מ-וו-x5/5052-ב-מ-וו-x5-פלאג-אין-5-מושבים-xdrive50e-m-expressive
- Cartube/BMW PDF for 2024 X5 supports X5 xDrive50e technical details.
  - URL: https://www.cartube.co.il/images/mifrat/bmw/37964-BMW-X5-2024-01.pdf

### Required Codex edit — BMW X5 xDrive50e

Create clean profile:

- `model`: `X5 xDrive50e`
- Row 1:
  - `version_or_trim`: `M-Expressive`
  - `body_type`: `SUV`
  - `fuel_type`: `plug_in_hybrid`
  - `engine`: `3.0L inline-6 plug-in hybrid`
  - `engine_displacement_l`: 3.0
  - `horsepower_hp`: 489
  - `transmission`: `8-speed automatic`
  - `drivetrain`: `AWD`
  - `year_start`: 2024
  - `year_end`: 2026 or null only according to current local source support; Cartube 2025 page can support at least current 2025.
- Optional Row 2 only if local source supports it:
  - `version_or_trim`: `M-Sport Pro`
  - same technical fields.

Do not leave the empty review profile.

---

## BMW X7 xDrive30d

Current issue: active empty review-only blocker.

Evidence:

- Cartube 2019 X7 Israel launch price list lists `BMW X7 xDrive30d` in `Pure Excellence` trim.
  - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x7-החדש-בישראל-מחיר-890000-שקל
- Cartube 2019 X7 technical notes say all X7 engines are paired to 8AT and xDrive AWD.
  - URL: https://www.cartube.co.il/חדשות-רכב/2019-ב-מ-וו-x7-נחשף-הענק-של-ב-מ-וו
- iCar X7 2021 pages list 3.0 265 hp xDrive30d variants, and current generation also has later diesel naming such as xDrive40d, not necessarily xDrive30d.

### Required Codex edit — BMW X7 xDrive30d

Create/repair clean profile only for locally grounded years:

- `model`: `X7 xDrive30d`
- `version_or_trim`: `Pure Excellence` if source supports.
- `body_type`: `SUV`
- `fuel_type`: `diesel`
- `engine`: `3.0L inline-6 turbo diesel`
- `engine_displacement_l`: 3.0
- `horsepower_hp`: 265
- `transmission`: `8-speed automatic`
- `drivetrain`: `AWD`
- `year_start`: 2019
- `year_end`: 2021 or 2022 only if iCar/local catalog supports. Do not extend to 2026 under `xDrive30d`; current/facelift diesel should be handled as `xDrive40d` if present.

Remove the empty active blocker.

---

## BMW X7 xDrive40i

Current issue: review profile has good rows but is active blocker due source/index or structure issues.

Evidence:

- Cartube 2019 X7 Israel launch lists `X7 xDrive40i Pure Excellence` and gives initial Israel pricing.
  - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x7-החדש-בישראל-מחיר-890000-שקל
- Cartube 2019 X7 technical data says `xDrive40i` uses 3.0L turbo, 340 hp, 8AT and xDrive AWD.
  - URL: https://www.cartube.co.il/חדשות-רכב/2019-ב-מ-וו-x7-נחשף-הענק-של-ב-מ-וו
- Current/facelift X7 pages in the local repo may support newer `xDrive40i` mild-hybrid / higher hp rows. Only keep them if direct local sources in the repo support the specific horsepower and year range.

### Required Codex edit — BMW X7 xDrive40i

Repair into clean:

- Pre-facelift row:
  - `version_or_trim`: `Pure Excellence` or `M Sport` only if locally supported.
  - `body_type`: `SUV`
  - `fuel_type`: `petrol`
  - `engine`: `3.0L inline-6 turbo`
  - `engine_displacement_l`: 3.0
  - `horsepower_hp`: 340
  - `transmission`: `8-speed automatic`
  - `drivetrain`: `AWD`
  - `year_start`: 2019
  - `year_end`: 2022 if local source supports.

- Facelift/current row only if direct local source supports:
  - `fuel_type`: `mild_hybrid` or `petrol` according to the source.
  - `horsepower_hp`: 381 if source supports current xDrive40i.
  - `year_start`: 2023.
  - `year_end`: 2026/null according to current local source support.

Do not use global-only data for current years. Do not leave the review profile active.

---

## BYD Seal U

Current issue: active review blocker despite having technical variants and sources. It must be repaired into clean if the embedded sources support it.

Evidence:

- Cartube Seal U EV Israel page: Seal U is a larger electric crossover, 218 hp, FWD, range 420–500 km depending version.
  - URL: https://www.cartube.co.il/component/tags/tag/byd-סיל-u-כתבות
- Cartube Seal U DM-i Israel launch: Seal U DM-i PHEV sold in Israel with FWD/AWD versions, 218–324 hp.
  - URL: https://www.cartube.co.il/חדשות-רכב/byd-סיל-u-פלאג-אין-בישראל-מחיר-209990-שקל
- BYD Israel / local sources in review profile support `Seal U` / `Seal U DM-i` official specs and trims.

### Required Codex edit — BYD Seal U

Repair into clean, but do not pollute it with `Song Plus` identity unless the catalog intentionally aliases Song Plus to Seal U.

Recommended clean rows:

1. `Seal U` EV row:
   - `version_or_trim`: use official trim if local source supports; otherwise null.
   - `body_type`: `SUV`
   - `fuel_type`: `electric`
   - `engine`: `electric`
   - `engine_displacement_l`: null
   - `horsepower_hp`: 218
   - `transmission`: `single_speed`
   - `drivetrain`: `FWD`
   - `year_start`: 2024 if local source supports.

2. `Seal U DM-i Comfort` PHEV:
   - `version_or_trim`: `Comfort` or `Comfort DM-i` according to local source.
   - `body_type`: `SUV`
   - `fuel_type`: `plug_in_hybrid`
   - `engine`: `1.5L plug-in hybrid`
   - `engine_displacement_l`: 1.5
   - `horsepower_hp`: 218
   - `transmission`: `automatic`
   - `drivetrain`: `FWD`
   - `year_start`: 2024.

3. `Seal U DM-i Design` PHEV:
   - `version_or_trim`: `Design` or `Design DM-i` according to local source.
   - `fuel_type`: `plug_in_hybrid`
   - `engine`: `1.5L plug-in hybrid`
   - `horsepower_hp`: 324
   - `drivetrain`: `AWD`
   - `year_start`: 2024.

Do not classify `Comfort` or `Design` as invalid trims for Seal U DM-i if official BYD Israel or Cartube supports them.

---

## BYD Song Plus

Current issue: active review blocker. The review profile likely mixes `Song Plus`, `Seal U`, and PHEV data.

Evidence:

- The Israeli official/importer marketing is `BYD Seal U` / `Seal U DM-i`, not `Song Plus`, for the regular importer channel.
- Review sources mention `BYD Song Plus EV Parallel Import Launch in Israel` for an EV row only.

### Required Codex edit — BYD Song Plus

Do not keep PHEV Song Plus rows in clean if they are actually `Seal U DM-i`.

Apply:

1. Move any PHEV Song Plus variants to `BYD Seal U` / `Seal U DM-i` if they match Comfort/Design DM-i local evidence.
2. Keep `BYD Song Plus` clean only if the local embedded source directly supports a parallel-import EV Song Plus profile.
3. If kept as parallel import:
   - `body_type`: `SUV`
   - `fuel_type`: `electric`
   - `engine`: `electric`
   - `horsepower_hp`: 204 if source supports.
   - `transmission`: `single_speed`
   - `drivetrain`: `FWD`
   - `year_start`: source-supported year.
   - add note/source type indicating parallel import, not official importer model.
4. If direct evidence is insufficient, move `Song Plus` to a non-blocking archive/review state; do not count it as an active blocker.

---

## Cadillac ATS

Current issue: active review blocker because variants have `field_sources` but no `source_indexes`, similar to the BMW X5 3.0d issue.

Evidence in review sources:

- iCar ATS Sedan 2013–2019.
- Auto ATS model page.
- Cartube 2016 Cadillac ATS/CTS facelift: 2.0L turbo 272 hp, 8-speed automatic replacing 6-speed.
  - URL: https://www.cartube.co.il/חדשות-רכב/קאדילק-ישראל-cts-ו-ats-מחודשות-2016
- iCar ATS Coupe 2015–2019.

### Required Codex edit — Cadillac ATS

Repair into clean. Add `source_indexes` to every retained row equal to the union of the row’s `field_sources` values.

Rows to retain if local sources support:

1. Sedan 2013–2015 Luxury:
   - 2.0L turbo petrol, 272 hp, 6AT, RWD.
2. Sedan 2013–2015 Premium:
   - same technical fields.
3. Sedan 2016–2019 Luxury:
   - 2.0L turbo petrol, 272 hp, 8AT, RWD.
4. Sedan 2016–2019 Premium:
   - same technical fields.
5. Coupe 2015 Premium:
   - 2.0L turbo petrol, 272 hp, 6AT, RWD.
6. Coupe 2016–2019 Premium:
   - 2.0L turbo petrol, 272 hp, 8AT, RWD.

If exact trim/year is not directly supported by iCar/Auto, move only the unsupported row to non-blocking review. Do not leave the whole ATS profile active blocked.

---

## Cadillac Escalade

Current issue: active empty review-only blocker caused by parser error. Raw values mix petrol Escalade and electric Escalade IQ.

Evidence:

- Cartube 2022 Escalade Israel: 6.2L V8, 420 hp; new Escalade marketed in Israel, price from 899,990 NIS.
  - URL: https://www.cartube.co.il/חדשות-רכב/קאדילק-אסקלייד-החדש-2022-בישראל-מחיר-899990-שקל
- Cartube 2025 Escalade facelift/global: normal Escalade continues with 6.2L V8 420 hp; Escalade V has 682 hp. This is global reveal, use only for technical continuity if local market source exists.
  - URL: https://www.cartube.co.il/חדשות-רכב/2025-קאדילק-אסקלייד-החדש-נחשף-מתיחת-פנים
- Cartube 2025 Escalade IQ Israel: electric Escalade IQ arrived in Israel, 750 hp AWD, 205 kWh battery, 740 km range, price from 700,000 NIS.
  - URL: https://www.cartube.co.il/חדשות-רכב/הענק-החשמלי-נחת-בישראל-קאדילק-iq-במחיר-700000-שקל
- Cartube PDF Escalade IQ 2025 supports electric powertrain details: AWD dual motors, 750 hp, 205 kWh, 740 km.
  - URL: https://www.cartube.co.il/images/mifrat/cadillac/escalade_iq_mifrat-2025-5.pdf

### Required Codex edit — Cadillac Escalade

Split petrol Escalade and electric Escalade IQ.

1. Create/repair clean `Cadillac Escalade` petrol profile:
   - `version_or_trim`: `Luxury Sport` and/or `Sport Platinum` only if local sources support.
   - `body_type`: `SUV`
   - `fuel_type`: `petrol`
   - `engine`: `6.2L v8`
   - `engine_displacement_l`: 6.2
   - `horsepower_hp`: 420
   - `transmission`: `10-speed automatic` if local source supports; otherwise `automatic`.
   - `drivetrain`: `4WD` or `AWD` according to local source/convention.
   - `year_start`: 2022 for the current generation row.
   - Historical 2007/2014/2015 rows may be retained only if local source in the repo supports them.

2. Create/repair separate clean `Cadillac Escalade IQ` profile:
   - `source_group_key` or `split_from_source_group_key`: `IL|Cadillac|Escalade`
   - `version_or_trim`: use official trim if source supports; otherwise null.
   - `body_type`: `SUV`
   - `fuel_type`: `electric`
   - `engine`: `electric`
   - `engine_displacement_l`: null
   - `horsepower_hp`: 750
   - `transmission`: `single_speed`
   - `drivetrain`: `AWD`
   - `year_start`: 2025
   - `year_end`: 2026/null according to current source support.

Do not put Escalade IQ electric rows under the petrol `Escalade` profile. Do not leave Escalade as empty blocker.

---

## Cadillac Lyriq

Current issue: review profile is mostly grounded, but blocked because pure EV row has `transmission=null` and `transmission` is listed in `missing_grounded_fields`; `engine_displacement_l` is also listed as missing despite not applying to EVs.

Evidence:

- Cadillac Israel Lyriq page: `Luxury AWD`, electric motor, 515 hp, 102 kWh battery, AWD.
  - URL: https://www.cadillac.co.il/דגמים/lyriq/
- Cadillac Israel Lyriq technical page: permanent-magnet synchronous AC electric motor, AWD two motors, 515 hp, 102 kWh battery.
  - URL: https://www.cadillac.co.il/LYRIQ/מפרט-טכני/
- Cadillac Israel 2025 PDF: LYRIQ Luxury AWD, electric motor, AWD dual motors, 515 hp, 102 kWh battery.
  - URL: https://www.cadillac.co.il/media/wajbd0yz/lyriq_mifrat_tech_2025_web.pdf
- Cadillac global specs identify dual-motor AWD 515 hp for 2026 Lyriq. Use this only as supplemental technical consistency; Israeli sources are primary.
  - URL: https://www.cadillac.com/electric/lyriq/specs

### Required Codex edit — Cadillac Lyriq

Repair into clean:

- `model`: `Lyriq`
- `version_or_trim`: `Luxury AWD`
- `body_type`: `SUV`
- `fuel_type`: `electric`
- `engine`: `electric`
- `engine_displacement_l`: null
- `horsepower_hp`: 515
- `transmission`: `single_speed` if the catalog requires an EV transmission value; otherwise update validation so pure EV transmission null does not block readiness.
- `drivetrain`: `AWD`
- `year_start`: 2025
- `year_end`: 2026/null according to current Israel source.

Critical validator/data rule:
- Remove `engine_displacement_l` from `missing_grounded_fields` for pure EV rows.
- Do not list `transmission` as missing if the row uses `single_speed` or if EV transmission null is allowed by validator.
- `available_values_for_website.transmission` must not be empty if the website schema requires it; use `single_speed` consistently with other EV profiles.

---

# Special insertion — BYD Atto 3 EVO

RUN 2 found a strong data issue: `Evo` rows were mis-scoped under `BYD Seal` or were not represented as a clean model because the source group did not explicitly run as `Atto 3 EVO`.

Evidence:

- Cartube 10.02.2026: `2026 BYD Atto 3 EVO` on the way to Israel: LFP 74.8 kWh battery, 220 kW fast charge, RWD 313 hp with 510 km range, AWD 449 hp with 470 km range.
  - URL: https://www.cartube.co.il/חדשות-רכב/בדרך-לישראל-2026-byd-אטו-3-החדש-evo
- Cartube 03.06.2026: `BYD Atto 3 EVO` landed in Israel; Design RWD 313 hp and Excellence AWD 449 hp; prices 154,990/164,990 NIS.
  - URL: https://www.cartube.co.il/חדשות-רכב/byd-אטו-3-evo-החדש-נחת-בישראל-מחיר-154990-שקל
- Cartube drive impression 29.04.2026: Atto 3 EVO RWD 313 hp, 510 km range, 0–100 in 5.5s.
  - URL: https://www.cartube.co.il/מבחני-רכב/byd-מבחני-רכב/התרשמות-ראשונה-byd-אטו-3-evo-החדש

### Required Codex edit — BYD Atto 3 EVO

Add/repair clean split profile:

- `market`: `IL`
- `make`: `BYD`
- `model`: `Atto 3 EVO`
- `canonical_model`: `Atto 3 EVO`
- `source_group_key` or `split_from_source_group_key`: `IL|BYD|Atto 3`
- Add alias mapping so this split profile does not become a future unmatched output key.

Rows:

1. Design RWD:
   - `version_or_trim`: `Design`
   - `body_type`: `SUV` or `Crossover` according to catalog convention for Atto 3; use the same convention as existing Atto 3 if possible.
   - `fuel_type`: `electric`
   - `engine`: `electric`
   - `engine_displacement_l`: null
   - `horsepower_hp`: 313
   - `transmission`: `single_speed`
   - `drivetrain`: `RWD`
   - `year_start`: 2026
   - optional if schema supports: `battery_kwh`: 74.8, `range_wltp_km`: 510.

2. Excellence AWD:
   - `version_or_trim`: `Excellence`
   - `fuel_type`: `electric`
   - `engine`: `electric`
   - `engine_displacement_l`: null
   - `horsepower_hp`: 449. If local catalog convention prefers integer from source 448, choose one consistent value and document the alternate source.
   - `transmission`: `single_speed`
   - `drivetrain`: `AWD`
   - `year_start`: 2026
   - optional if schema supports: `battery_kwh`: 74.8, `range_wltp_km`: 470.

Remove any `Evo`, `Evo AWD`, or `Evo RWD` pollution from `BYD Seal`. These are Atto 3 EVO rows, not Seal rows.

---

# Unmatched/split profile reconciliation

## Alfa Romeo Junior Elettrica

Evidence:

- Cartube 15.12.2024: Alfa Romeo Junior landed in Israel with 1.2 turbo 136 hp and two electric versions: normal electric 156 hp and Veloce 280 hp, with Veloce expected Q1 2025.
  - URL: https://www.cartube.co.il/חדשות-רכב/אלפא-רומיאו-ג-וניור-נחת-בישראל-מחיר-169900-שקל
- Local repo already has clean `Alfa Romeo Junior Elettrica` sources from iCar/Cartube.

### Required Codex edit — Junior Elettrica unmatched

Do not delete or collapse `IL|Alfa Romeo|Junior Elettrica`.

Treat it as a legitimate split profile from source group `IL|Alfa Romeo|Junior`.

Required:

- Add one of these to the clean model object:
  - `source_group_key`: `IL|Alfa Romeo|Junior`
  - `split_from_source_group_key`: `IL|Alfa Romeo|Junior`
  - `source_alias_keys`: [`IL|Alfa Romeo|Junior`]
- Update `compute_resume_state()` to treat these alias fields as valid output-to-source mappings.
- Expected EV rows:
  - base electric: `electric`, 156 hp, FWD, year_start 2024 if source supports.
  - Veloce electric: `electric`, 280 hp, likely year_start 2025 if source supports Q1 2025 arrival/launch.

Final resume state must not report `IL|Alfa Romeo|Junior Elettrica` as unmatched.

---

## BMW M850i

Evidence:

- Cartube 26.12.2018: BMW 8 Series coupe launched in Israel as `M850i xDrive`, 4.4L twin-turbo, 530 hp.
  - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-8-החדשה-בישראל-מחיר-1250000-שקל
- Cartube 17.06.2019: BMW 8 Series Cabriolet Israel: `M850i xDrive`, 4.4L V8 twin-turbo, 530 hp, 8AT, AWD.
  - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-8-קבריולט-בישראל-מחיר-1320000-שקל
- Cartube 11.12.2019: BMW 8 Series Gran Coupe Israel: `M850i` uses xDrive AWD; Gran Coupe is a distinct body type.
  - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-8-גראן-קופה-בישראל-מחיר-890000-שקל

### Required Codex edit — M850i unmatched

Do not delete or collapse `IL|BMW|M850i` back into historical `BMW 850i`.

Treat `M850i` as a legitimate split profile from source group `IL|BMW|850i` because modern `M850i xDrive` and historical `850i` are different model identities.

Required:

- Add one of these to clean `BMW M850i`:
  - `source_group_key`: `IL|BMW|850i`
  - `split_from_source_group_key`: `IL|BMW|850i`
  - `source_alias_keys`: [`IL|BMW|850i`]
- Keep rows for:
  - `Coupe`
  - `Convertible`
  - `Gran Coupe`
- Technical fields:
  - `version_or_trim`: `M850i xDrive`
  - `fuel_type`: `petrol`
  - `engine`: `4.4L v8 turbo` or `4.4L v8 twin-turbo` consistently with catalog convention.
  - `engine_displacement_l`: 4.4
  - `horsepower_hp`: 530
  - `transmission`: `8-speed automatic`
  - `drivetrain`: `AWD`
  - `year_start`: 2018 for Coupe, 2019 for Convertible/Gran Coupe if using launch sources.
- Preserve `Gran Coupe` as its own body type. Do not normalize it to `Coupe` or `Sedan`.

Final resume state must not report `IL|BMW|M850i` as unmatched.

---

# Code/reporting fixes required in this RUN

## 1. Resume alias mapping

Update `scripts/catalog_builder.py` / `compute_resume_state()` so legitimate split output profiles do not show as unmatched if they declare source lineage.

Implementation behavior:

1. Build `clean_keys` from output model keys.
2. Build `source_keys` from source groups.
3. For each clean model, collect alias/source keys from optional fields:
   - `source_group_key`
   - `split_from_source_group_key`
   - `source_alias_keys`
4. When calculating unmatched outputs, treat an output profile as matched if any alias exists in `source_keys`.
5. Return:
   - `unmatched_output_keys_count`
   - `unmatched_output_keys_sample`
   - `split_profile_alias_count`
   - `split_profile_alias_sample`

Final expected unmatched count: 0.

## 2. Review-only blockers

Do not count archive/rejected overlap entries as active blockers. Current review-only blockers should be repaired or moved to non-blocking archive.

Final expected:

```json
{
  "models_blocked": 0,
  "review_only_blocked_entries": 0
}
```

## 3. EV validation

Fix EV validation so these do not block readiness:

- pure EV with `engine_displacement_l=null`
- pure EV where transmission is either `single_speed` or explicitly allowed null
- PHEV rows with `engine_displacement_l` reflecting ICE displacement and electric components reflected in fuel/engine text

This is required for `Cadillac Lyriq`, `Escalade IQ`, `BYD Atto 3 EVO`, `Junior Elettrica`, and other EV/PHEV profiles.

---

# Final rebuild and verification commands

After applying RUN 1 + RUN 2 + RUN 3, run:

```bash
pytest -q
python3 -m scripts.catalog_quality_scan
```

Then run the repo readiness rebuild command used by this project, for example the same `merge_and_write_outputs(...)` command used in previous successful commits.

Final required readiness/reporting values:

```json
{
  "models_blocked": 0,
  "review_only_blocked_entries": 0,
  "duplicate_technical_variants": 0,
  "invalid_source_references": 0,
  "unknown_support_values": 0,
  "ready_for_website_upload": true,
  "unmatched_output_keys_count": 0,
  "unmatched_output_keys_sample": []
}
```

After successful verification, delete the temporary task file from the repository.

Report exact changed files and a summary of:

1. Which blockers were repaired into clean.
2. Which rows were moved to non-blocking archive/review.
3. How `BYD Atto 3 EVO` was inserted.
4. How `Junior Elettrica` and `M850i` were reconciled as split profiles.
5. Final readiness values.

