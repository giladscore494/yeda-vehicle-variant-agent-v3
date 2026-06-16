# FINAL UNIFIED CODEX TASK — LAST 40 CLEAN MODELS + RUN 3 BLOCKED REPAIRS

This is the single task file to upload to the repository root for Codex.

Codex has no web access. Do not browse. All external research and URLs are embedded in this file.

Execution order is mandatory:

1. RUN 1 — first 20 of last 40 clean models.
2. RUN 2 — next 20 of last 40 clean models.
3. RUN 3 — current blocked/review-only models and required code/reporting fixes.
4. Rebuild clean/review/readiness/quality outputs.
5. Run tests.
6. Delete this temporary task file only after verification.

---

# FINAL UNIFIED TASK — RUN 1 + RUN 2 deep validation for last 40 clean models

This file combines the completed RUN 1 task and the completed RUN 2 task. Do not execute blocked/review-only repairs yet unless explicitly instructed later. Codex has no web access; use this file and local repo files only.

Execution order: RUN 1 first, then RUN 2. After both, rebuild clean/review/readiness/quality outputs and run tests. Do not delete this task file until verification is complete.

---

# RUN 1 / 3 — Deep internet-backed validation for first 20 of last 40 clean models

Date: 2026-06-16

Scope: the first 20 models from the last 40 clean profiles in `data/model_technical_catalog_il.json`, indices 114–133 in the uploaded repo state.

Codex has no web access. Do not browse. Use this file plus local repo files only.

## Non-negotiable rules

1. Israeli market only. Do not keep a row in clean based only on global data or generic knowledge.
2. Validate and edit each variant field-by-field: model identity, trim/version, body_type, fuel_type, engine, displacement, horsepower, transmission, drivetrain, year_start, year_end.
3. Electric rows must have `engine_displacement_l=null`, but this is not a missing grounded field. Remove `engine_displacement_l` from `missing_grounded_fields` for pure EVs.
4. `version_or_trim=null` is acceptable for model-level rows such as 640i/i7 xDrive60/i8 if no separate marketed trim is present; never expose null in `available_values_for_website`.
5. `Gran Coupe` is a distinct canonical body type. Never normalize it to `Coupe` or `Sedan`.
6. If evidence cannot ground a row, move it to non-blocking review/archive; do not leave active blockers.
7. Rebuild `sources`, `source_indexes`, `field_sources`, `available_values_for_website`, `invalid_or_non_trim_labels`, readiness and quality reports after edits.


## External web evidence used by ChatGPT for this RUN 1 package
Use these as offline evidence. Prefer Israeli/importer/editorial sources over global sources; global sources are only secondary sanity checks.

- Auto.co.il Series 6 Gran Coupe: 640i Gran Coupe 3.0 turbo 320 hp; 650i Gran Coupe 4.4 twin-turbo 450 hp; Gran Coupe is a distinct four-door body. URL: https://www.auto.co.il/cars/bmw/6-series-gran-coupe/
- Auto.co.il Series 6: 3.0 turbo 320 hp; 4.4 turbo 407 hp later 450 hp; regular Coupe/Convertible separated from Gran Coupe. URL: https://www.auto.co.il/cars/bmw/6-series/
- Auto.co.il 728i 2001 version: Israeli launch 1995; 728i 2.8 automatic; sedan. URL: https://www.auto.co.il/cars/bmw/7-series/2001/523107/
- BMW Group Classic 735i E38: production 03/1996-07/2001, 3498 cc V8, 235 bhp. URL: https://www.bmwgroup-classic.com/en/models/bmw-classics/product-description-page.ad-196-1.bmw-735i-e38.html
- Auto.co.il 740e 2016 version: 740e plug-in hybrid Luxury trim evidence. URL: https://www.auto.co.il/cars/bmw/7-series/2016/513773/
- AutoBoom 745i: 745i 4.4 AT petrol, 333 hp, RWD, 2001-2005. URL: https://autoboom.co.il/catalog/cars/bmw/7-series/4-generation/sedan/6253
- Yad2 Series 8 current listings: M850i 4.4 530 hp appears as Series 8 M850i, supporting model identity separate from classic 850i. URL: https://www.yad2.co.il/vehicles/cars?manufacturer=7&model=10102
- Auto.co.il Series 8 Gran Coupe: M850i V8 4.4 and Gran Coupe body separated from Coupe/Convertible. URL: https://www.auto.co.il/cars/bmw/8-series-gran-coupe/
- iCar i3s 2018 version: i3 184 hp `s Loft`, rear drive / automatic EV; shows i3s trim naming. URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_i3/ב.מ.וו_i3_יד_שניה_ד10/version19415/
- Cartube i4 eDrive35 2023 Israel: eDrive35, rear electric motor, 286 hp. URL: https://www.cartube.co.il/חדשות-רכב/חדש-בישראל-2023-ב-מ-וו-i4-edrive35-מחיר-359900-שקל
- Auto.co.il i4 current: eDrive35=286 hp, eDrive40=340 hp; trims Essence and M-Shadow for eDrive35; M-Sport and M-Tech for eDrive40. URL: https://www.auto.co.il/cars/bmw/i4/
- BMW Israel i5 official: i5 eDrive40 packages Elegant and M-Expressive; i5 M60 uses M-Ultimate. URL: https://www.bmw.co.il/he/All-Models/bmw-i/i5/bmw-i5.html
- iCar i5 2026 eDrive40 M-Expressive: current eDrive40 M-Expressive page. URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_i5/ב.מ.וו_i5_חדש/version27699/
- Auto.co.il i7: xDrive60, AWD, 544 hp; eDrive50 is separate current row and must not pollute xDrive60. URL: https://www.auto.co.il/cars/bmw/i7/
- iCar i7 current: electric AWD 544 hp support. URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_i7/ב.מ.וו_i7_חדש/
- Auto.co.il i8 2018: i8 plug-in hybrid 1.5, 362 hp. URL: https://www.auto.co.il/cars/bmw/i8/2018/
- Cartube i8 Roadster reveal: facelift/Roadster system output 374 hp. URL: https://www.cartube.co.il/חדשות-רכב/2018-ב-מ-וו-i8-רודסטר-החדשה-נחשפת
- iCar iX 2021-2025: iX xDrive40 326 hp; xDrive50 separate. URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_iX/ב.מ.וו_iX_יד_שניה_ד10/
- BMW Israel all-models current: BMW iX xDrive40 is listed as an available model card. URL: https://www.bmw.co.il/he/All-Models.html
- Cartube iX1 eDrive20 Israel launch: FWD, 204 hp, X-Line and M-Sport, 2024. URL: https://www.cartube.co.il/חדשות-רכב/חדש-בישראל-2024-ב-מ-וו-ix1-edrive20-החשמלית-מחיר-344900-שקל
- BMW Israel iX1 current price list: iX1 eDrive20 X-Line and M-Sport current 04/2026. URL: https://www.bmw.co.il/he/All-Models/i-series/ix1/bmw-ix1.html
- BMW Israel iX2 official: iX2 eDrive20, 204 hp, 8.6 sec, 170 km/h, 450 km range. URL: https://www.bmw.co.il/he/All-Models/bmw-i/ix2/bmw-ix2.html
- Auto.co.il iX2 current: iX2 eDrive20 FWD, 204 hp, 66.5 kWh gross / 64.7 net, 450 km. URL: https://www.auto.co.il/cars/bmw/ix2/


---

## Exact RUN 1 model list

1. BMW 630i GT
2. BMW 640i
3. BMW 640i GT
4. BMW 650i
5. BMW 728i
6. BMW 730i
7. BMW 735i
8. BMW 740e
9. BMW 745i
10. BMW 750i
11. BMW 850i
12. Bmw 850i
13. BMW i3s
14. BMW i4 eDrive35
15. BMW i5 eDrive40
16. BMW i7 xDrive60
17. BMW i8
18. BMW iX xDrive40
19. BMW iX1 eDrive20
20. BMW iX2 eDrive20

---


## 114. BMW 630i GT

Current profile_confidence: `high`

### Current variants in clean

- V00: version_or_trim='M Sport'; body_type='Liftback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=258; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2017; year_end=2023; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim='Luxury Line'; body_type='Liftback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=258; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2017; year_end=2023; support_level='direct'; missing_grounded_fields=[]

### Local catalog sources already present

- [0] Cartube — ב.מ.וו סדרה 6 גראן טוריסמו החדשה בישראל - מחיר החל מ-545,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-6-%D7%92%D7%A8%D7%90%D7%9F-%D7%98%D7%95%D7%A8%D7%99%D7%A1%D7%9E%D7%95-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-545000-%D7%A9%D7%A7%D7%9C — supports=['version_or_trim', 'year_start', 'horsepower_hp', 'engine', 'engine_displacement_l', 'transmission', 'drivetrain', 'fuel_type']
- [1] iCar — ב.מ.וו סדרה 6 GT - מחירון, מפרטים, אבזור — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_GT/ — supports=['body_type', 'horsepower_hp', 'engine', 'engine_displacement_l', 'transmission', 'drivetrain', 'fuel_type', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: KEEP with strict source mapping; minor naming cleanup only.
Deep validation:
- Current rows are technically plausible and supported by the local Cartube/iCar source set: 630i GT / 6 Series Gran Turismo, 2.0 turbo petrol, 258 hp, 8-speed automatic, RWD, Liftback/Gran Turismo body.
- The two trims should remain only if the local source explicitly lists both `M Sport` and `Luxury Line` for the Israeli 630i GT. Use exact casing from the source.
Required Codex edits:
- Keep V00 `M Sport` if source 0 or 1 lists it directly.
- Keep V01 `Luxury Line`; if the local source says `Luxury` only, normalize to the exact source label; do not invent.
- Do not merge 630i GT into 630i coupe/cabrio. It is a separate GT/Liftback profile.
- If year_end=2023 is not directly supported by iCar/model range, set `year_end=null` and add `year_end` to `missing_grounded_fields`; do not guess.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 115. BMW 640i

Current profile_confidence: `high`

### Current variants in clean

- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='3.0L turbo i6'; engine_displacement_l=3.0; horsepower_hp=320; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2018; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Gran Coupe'; fuel_type='petrol'; engine='3.0L turbo i6'; engine_displacement_l=3.0; horsepower_hp=320; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2012; year_end=2018; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='3.0L turbo i6'; engine_displacement_l=3.0; horsepower_hp=320; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2018; support_level='direct'; missing_grounded_fields=[]

### Local catalog sources already present

- [0] iCar — ב.מ.וו סדרה 6 קופה (2011-2018) - מפרט טכני - iCar — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_%D7%A7%D7%95%D7%A4%D7%94/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_%D7%A7%D7%95%D7%A4%D7%94_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%93%D7%92%D7%9D_2011/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar — ב.מ.וו סדרה 6 גראן-קופה (2012-2018) - מפרט טכני - iCar — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_%D7%92%D7%A8%D7%90%D7%9F-%D7%A7%D7%95%D7%A4%D7%94/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_%D7%92%D7%A8%D7%90%D7%9F-%D7%A7%D7%95%D7%A4%D7%94_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%93%D7%92%D7%9D_2012/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] iCar — ב.מ.וו סדרה 6 קבריולה (2011-2018) - מפרט טכני - iCar — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_%D7%A7%D7%91%D7%A8%D7%99%D7%95%D7%9C%D7%94/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_%D7%A7%D7%91%D7%A8%D7%99%D7%95%D7%9C%D7%94_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%93%D7%92%D7%9D_2011/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: KEEP all three body rows; verify Gran Coupe remains distinct.
Deep validation:
- Israeli Auto/iCar sources support 640i 3.0 turbo, 320 hp, RWD, 8-speed automatic, with Coupe, Convertible/Cabriolet and Gran Coupe body separation. Auto explicitly separates regular Series 6 from the 4-door Gran Coupe page and lists 640i 3.0 turbo 320 hp for Gran Coupe.
Required Codex edits:
- Keep Coupe 2011-2018, Convertible 2011-2018, Gran Coupe 2012-2018 as separate clean rows.
- Ensure `Gran Coupe` is canonical and not normalized to Coupe or Sedan.
- `version_or_trim=null` is acceptable because `640i` is the model-level engine variant; remove it from missing if it appears.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 116. BMW 640i GT

Current profile_confidence: `high`

### Current variants in clean

- V00: version_or_trim='Luxury'; body_type='Liftback'; fuel_type='petrol'; engine='3.0L inline-6 turbo'; engine_displacement_l=3.0; horsepower_hp=340; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2017; year_end=2024; support_level='direct'; missing_grounded_fields=[]

### Local catalog sources already present

- [0] iCar Israel — ב.מ.וו סדרה 6 GT - מחירון, צריכת דלק, רמות גימור — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_GT/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start', 'year_end', 'version_or_trim']
- [1] Cartube Israel — ב.מ.וו סדרה 6 GT החדשה בישראל - מחיר החל מ- 545,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-6-gt-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%9A%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-545000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain', 'version_or_trim', 'year_start']

### Deep validation decision and exact Codex instructions


Verdict: KEEP, but validate trim name and year_end carefully.
Deep validation:
- 640i GT is a 6 Series GT / Gran Turismo liftback, not Series 6 Coupe/Gran Coupe.
- Current row: 3.0 inline-6 turbo, 340 hp, xDrive/AWD, 8AT, Liftback. This is technically consistent for 640i GT xDrive.
Required Codex edits:
- Keep as separate model `640i GT`, not merged with `640i`.
- If the source says `Luxury Line`, change `version_or_trim` from `Luxury` to `Luxury Line`; if it says `Luxury`, keep exact.
- Keep drivetrain AWD only if source explicitly states xDrive/4x4; otherwise move row to review.
- If year_end=2024 lacks direct iCar/current source support, set `year_end=null` with missing field instead of guessing.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 117. BMW 650i

Current profile_confidence: `high`

### Current variants in clean

- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='4.8L v8'; engine_displacement_l=4.8; horsepower_hp=367; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2005; year_end=2010; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='4.8L v8'; engine_displacement_l=4.8; horsepower_hp=367; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2005; year_end=2010; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=407; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2012; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=407; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2012; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim=None; body_type='Gran Coupe'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=450; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2012; year_end=2018; support_level='direct'; missing_grounded_fields=[]
- V05: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=450; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2012; year_end=2018; support_level='direct'; missing_grounded_fields=[]
- V06: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=450; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2012; year_end=2018; support_level='direct'; missing_grounded_fields=[]

### Local catalog sources already present

- [0] iCar — ב.מ.וו סדרה 6 (2004-2011) - מפרט טכני — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_%D7%93%D7%92%D7%9D_2004/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar — ב.מ.וו סדרה 6 (2011-2018) - מפרט טכני — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_%D7%93%D7%92%D7%9D_2011/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Cartube — ב.מ.וו סדרה 6 גראן קופה נוחתת בישראל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-6-%D7%92%D7%A8%D7%90%D7%9F-%D7%A7%D7%95%D7%A4%D7%94-%D7%A0%D7%95%D7%97%D7%AA%D7%AA-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-620-%D7%90%D7%9C%D7%A3-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start']
- [3] Auto.co.il — ב.מ.וו סדרה 6 - אוטו — https://www.auto.co.il/model/bmw-6-series_g250 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: KEEP after Gran Coupe canonical handling.
Deep validation:
- 650i pre-2011 4.8 V8 367 hp Coupe/Convertible is plausible and locally sourced.
- 2011-2012 4.4 turbo V8 407 hp rows are plausible for early F12/F13.
- Later 4.4 turbo V8 450 hp rows for Coupe/Convertible/Gran Coupe are supported by Israeli Auto/Cartube/iCar style sources; Auto states the 650i Gran Coupe uses 4.4 twin-turbo V8 with 450 hp.
Required Codex edits:
- Keep all seven rows only if source_indexes map body-specific sources correctly.
- Keep `Gran Coupe` as a distinct body type and make sure quality scan does not collapse it to `Coupe`.
- Do not promote xDrive/AWD 650i from review unless a local source directly grounds it; current clean rows are RWD.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 118. BMW 728i

Current profile_confidence: `high`

### Current variants in clean

- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.8L inline-6'; engine_displacement_l=2.8; horsepower_hp=193; transmission='5-speed automatic'; drivetrain='RWD'; year_start=1995; year_end=2001; support_level='direct'; missing_grounded_fields=[]

### Local catalog sources already present

- [1] Auto.co.il — ב.מ.וו סדרה 7 (1995-2001) - מחירון רכב, מפרט טכני — https://www.auto.co.il/model/bmw-7-series_g202 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] iCar.co.il — ב.מ.וו סדרה 7 1995 - 2001 - מחירון ומפרט — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_דור_3/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: KEEP.
Deep validation:
- Israeli Auto source confirms 728i 2.8 automatic, sedan, 1995 Israeli launch, matching the E38 row.
Required Codex edits:
- Keep 2.8L inline-6, 193 hp, 5-speed automatic, RWD, 1995-2001.
- `version_or_trim=null` is acceptable for a model-level 728i row; do not put null in website values.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 119. BMW 730i

Current profile_confidence: `high`

### Current variants in clean

- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L i4 turbo'; engine_displacement_l=2.0; horsepower_hp=258; transmission='automatic'; drivetrain='RWD'; year_start=2016; year_end=2019; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L i6'; engine_displacement_l=3.0; horsepower_hp=258; transmission='automatic'; drivetrain='RWD'; year_start=2005; year_end=2015; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L i6'; engine_displacement_l=3.0; horsepower_hp=231; transmission='automatic'; drivetrain='RWD'; year_start=2003; year_end=2005; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L v8'; engine_displacement_l=3.0; horsepower_hp=218; transmission='automatic'; drivetrain='RWD'; year_start=1994; year_end=1996; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L i6'; engine_displacement_l=3.0; horsepower_hp=188; transmission='automatic'; drivetrain='RWD'; year_start=1990; year_end=1994; support_level='direct'; missing_grounded_fields=[]

### Local catalog sources already present

- [0] iCar — ב.מ.וו סדרה 7 (2016-2019) מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_ד4/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar — ב.מ.וו סדרה 7 (2009-2015) מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_ד3/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] iCar — ב.מ.וו סדרה 7 (2002-2008) מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_ד2/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [3] Auto.co.il — ב.מ.וו סדרה 7 (1994-2001) - מפרט טכני — https://www.auto.co.il/model/bmw-7-series_g64 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [4] Carzone — ב.מ.וו 730 מפרטים — https://www.carzone.co.il/models/bmw/7-series/ — supports=['engine', 'horsepower_hp', 'transmission', 'drivetrain']
- [5] Auto.co.il — ב.מ.וו סדרה 7 (1987-1994) - מפרט טכני — https://www.auto.co.il/model/bmw-7-series_g63 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: KEEP, but confirm old generation field precision.
Deep validation:
- Current profile spans multiple 7-Series generations: E32 3.0 I6, E38 3.0 V8, E65/E66 3.0 I6, F01/F02 3.0 I6, and G11 2.0 turbo 258 hp.
- The row with `engine='3.0L v8'`, 218 hp, 1994-1996 is plausible for E38 730i; do not change it to inline-6.
Required Codex edits:
- Keep all five rows only if the linked iCar/Auto sources directly ground each generation.
- Normalize modern transmission to exact source label if available (`8-speed automatic`), not generic `automatic`, but do not invent if source only says automatic.
- Remove `version_or_trim` from missing if present; null is acceptable for 730i.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 120. BMW 735i

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.4L inline-6'; engine_displacement_l=3.4; horsepower_hp=211; transmission='automatic'; drivetrain='RWD'; year_start=1990; year_end=1992; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.5L v8'; engine_displacement_l=3.5; horsepower_hp=235; transmission='automatic'; drivetrain='RWD'; year_start=1996; year_end=2001; support_level='direct'; missing_grounded_fields=[]

### Local catalog sources already present

- [0] iCar Israel — ב.מ.וו סדרה 7 (1995-2001) - מפרט טכני, מחירון - iCar — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7_עד_2001/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] KML Israel — ב.מ.וו סדרה 7 1987-1994 - מחירון ומפרטים — https://www.kml.co.il/Car/ב.מ.וו_סדרה_7_1987-1994_2515 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: KEEP but check the 1990-1992 row dates against KML/source.
Deep validation:
- BMW Group Classic confirms E38 735i production 03/1996-07/2001, 3498 cc V8, 235 hp, matching the 1996-2001 row.
- The older 3.4 inline-6 211 hp row is plausible for E32 735i, but the exact Israeli year_start/year_end must come from KML/local source, not generic memory.
Required Codex edits:
- Keep V01: 3.5L V8, 235 hp, RWD, 1996-2001.
- For V00: keep only if KML source directly lists 735i 3.4 inline-6 211 hp and the exact years 1990-1992. If KML gives a different range, correct the years to the local source; if it only supports model-range not exact variant years, set year_start/year_end null with missing or move V00 to review.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 121. BMW 740e

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim='iPerformance'; body_type='Sedan'; fuel_type='plug_in_hybrid'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=326; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2016; year_end=2019; support_level='direct'; missing_grounded_fields=[]

### Local catalog sources already present

- [0] Cartube Israel — ב.מ.וו סדרה 7 פלאג-אין (740e) בישראל – מחיר החל מ- 730,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-7-פלאג-אין-740e-בישראל-מחיר-החל-מ-730000-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] iCar — ב.מ.וו סדרה 7 (2016-2019) מפרט טכני - דגם פלאג-אין iPerformance — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_דגם_6/ — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: FIX trim labeling; technical row likely keep.
Deep validation:
- Israeli sources/Yad2 support 740e / 740Le plug-in hybrid 2.0 with 326 hp around 2016-2019.
- `iPerformance` is a BMW electrification badge/model descriptor, not necessarily a marketed trim for website filtering.
Required Codex edits:
- Keep technical fields: Sedan, PHEV, 2.0 turbo, 326 hp, 8AT, RWD, 2016-2019.
- Do not expose `iPerformance` as a website trim unless a local source explicitly lists it as the trim field. Preferred: `version_or_trim=null` and add `iPerformance` to invalid/non-trim labels as `electrification_badge`.
- If source explicitly lists `Luxury`, use `version_or_trim='Luxury'` instead of `iPerformance`.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 122. BMW 745i

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='4.4L v8'; engine_displacement_l=4.4; horsepower_hp=333; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2001; year_end=2005; support_level='direct'; missing_grounded_fields=['version_or_trim']

### Local catalog sources already present

- [0] iCar — ב.מ.וו סדרה 7 (2002-2008) מחירון, מפרט טכני - iCar — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_7/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_7_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%932/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] Auto.co.il — ב.מ.וו סדרה 7 - מפרט טכני — https://www.auto.co.il/model/bmw-7-series_g261 — supports=['horsepower_hp', 'engine_displacement_l', 'fuel_type', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: KEEP; fix false missing trim.
Deep validation:
- Israeli/AutoBoom style sources support 745i 4.4 AT petrol, 333 hp, RWD, 2001-2005.
Required Codex edits:
- Keep current technical row.
- Remove `version_or_trim` from `missing_grounded_fields`. In a model-level `745i` profile, null trim is acceptable if no separate Israeli trim exists.
- Do not expose null/Base/Standard in website values.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 123. BMW 750i

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='5.4L v12'; engine_displacement_l=5.4; horsepower_hp=326; transmission='automatic'; drivetrain='RWD'; year_start=1995; year_end=2001; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim='Exclusive'; body_type='Sedan'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=407; transmission='automatic'; drivetrain='RWD'; year_start=2009; year_end=2012; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim='Exclusive'; body_type='Sedan'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=450; transmission='automatic'; drivetrain='RWD'; year_start=2013; year_end=2015; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim='Pure Excellence'; body_type='Sedan'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=450; transmission='automatic'; drivetrain='AWD'; year_start=2016; year_end=2019; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim='Pure Excellence'; body_type='Sedan'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=530; transmission='automatic'; drivetrain='AWD'; year_start=2020; year_end=2022; support_level='direct'; missing_grounded_fields=[]

### Local catalog sources already present

- [0] Auto.co.il — ב.מ.וו סדרה 7 1995-2001 מפרט טכני - אוטו — https://www.auto.co.il/model/bmw-7-series_g157 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar — ב.מ.וו סדרה 7 (2009-2015) - מחירון ומפרטים — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_דגם_2009/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [2] Cartube — ב.מ.וו סדרה 7 החדשה בישראל – מחיר החל מ- 890,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-7-החדשה-בישראל-מחיר-החל-מ-890000-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [3] Cartube — ב.מ.וו סדרה 7 החדשה 2019 בארץ - מחירון ומפרט טכני — https://www.cartube.co.il/חדשות-רכב/2019-ב-מ-וו-סדרה-7-החדשה-בישראל-מחיר-החל-מ-765000-שקל — supports=['engine', 'horsepower_hp', 'drivetrain', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: KEEP, with exact drivetrain/transmission source mapping.
Deep validation:
- Current rows broadly match known Israeli 7-Series variants: E38 750i V12 5.4/326; F01 750i 4.4 turbo 407 then 450; G11/G12 750i xDrive/Pure Excellence 450; facelift 750i 530 hp.
- Yad2/current market snippets also show 750i/Pure Excellence type labels and 449/450 hp variants, but ads should not be the primary source if iCar/Cartube exists.
Required Codex edits:
- Keep all five rows if local source_indexes directly support exact generation and trim.
- For modern rows, if local sources say `xDrive`, drivetrain must be AWD; if they say 4X2/RWD, keep RWD. Do not mix 750i and 750Li unless catalog intentionally models them together.
- Normalize modern transmission to `8-speed automatic` if source explicitly states it.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 124. BMW 850i

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='5.0L v12'; engine_displacement_l=5.0; horsepower_hp=300; transmission='automatic'; drivetrain='RWD'; year_start=1990; year_end=1994; support_level='direct'; missing_grounded_fields=[]

### Local catalog sources already present

- [0] Auto.co.il — ב.מ.וו סדרה 8 (1990-1999) יד שניה - מפרט טכני, מנועים ונתונים — https://www.auto.co.il/model/bmw-8-series_g207 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar.co.il — ב.מ.וו 850i קופה V12 שנות ה-90 - סקירה היסטורית — https://www.icar.co.il/bmw/סדרה_8_קלאסית/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: KEEP classic 850i only.
Deep validation:
- Classic E31 BMW 850i is a 5.0 V12 coupe with 300 hp, fitting 1990-1994. It must remain separate from modern M850i xDrive.
Required Codex edits:
- Keep the single classic 850i row as BMW make casing, model `850i`, Coupe, 5.0L V12, 300 hp, RWD.
- Do not merge modern M850i rows into this profile.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 125. Bmw 850i

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim='M850i xDrive'; body_type='Coupe'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=530; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2018; year_end=2024; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim='M850i xDrive'; body_type='Convertible'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=530; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2019; year_end=2024; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim='M850i xDrive'; body_type='Sedan'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=530; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2019; year_end=2024; support_level='direct'; missing_grounded_fields=[]

### Local catalog sources already present

- [0] Auto.co.il — ב.מ.וו סדרה 8 - מחירון, מפרטים, אמינות וחוות דעת - אוטו — https://www.auto.co.il/model/bmw-8-series_g1405 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [1] Cartube.co.il — ב.מ.וו סדרה 8 החדשה 2018 בישראל - מחיר החל מ-1,250,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-8-החדשה-2018-בישראל-מחיר-החל-מ-1-250-000-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'version_or_trim']
- [2] iCar.co.il — ב.מ.וו סדרה 8 גראן קופה - מחירון וקטלוג רכב - iCar — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_8_גראן_קופה/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']

### Deep validation decision and exact Codex instructions


Verdict: FIX model identity. This is not a clean `Bmw 850i` profile.
Deep validation:
- The rows are modern `M850i xDrive`, not `850i`. Israeli Yad2 and Auto/BMW market references show modern Series 8 rows as M850i 4.4, 530 hp, and the 4-door body is Gran Coupe, not Sedan.
Required Codex edits:
- Change make casing from `Bmw` to `BMW`.
- Rename/split model from `850i` to `M850i` or `M850i xDrive` consistently with repository naming rules.
- Keep Coupe and Convertible rows under the corrected M850i identity.
- Change V02 body_type from `Sedan` to `Gran Coupe`.
- Keep engine 4.4L V8 turbo, 530 hp, 8-speed automatic, AWD if sources support.
- Remove this polluted duplicate `Bmw 850i` profile after moving rows into the corrected model key.
- Rebuild source mappings and website values under the new canonical model.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 126. BMW i3s

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim=None; body_type='Hatchback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=184; transmission='single_speed'; drivetrain='RWD'; year_start=2018; year_end=2022; support_level='direct'; missing_grounded_fields=[]

### Local catalog sources already present

- [1] Cartube — ב.מ.וו i3 החדשה 2018 בישראל - מחיר החל מ- 249,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-i3-%D7%94%D7%97%D7%93%D7%A9%D7%94-2018-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-249-000-%D7%A9%D7%A7%D7%9C — supports=['fuel_type', 'engine', 'horsepower_hp', 'year_start']
- [2] iCar — ב.מ.וו i3 - מחירון, מפרטים, אמינות וחוות דעת — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_i3/ — supports=['body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: KEEP but consider splitting real trims.
Deep validation:
- iCar directly shows 2018 BMW i3 184 hp `s Loft`, with other i3/i3s trim combinations like `s Pulse`; the current generic i3s technical row is grounded, but it may be missing actual trims.
Required Codex edits:
- Keep i3s as electric Hatchback, 184 hp, single-speed/automatic EV, RWD, 2018-2022.
- If iCar/source lists `s Loft` and `s Pulse`, split into two identical technical rows with those version_or_trim values.
- If the source does not support both trims locally, keep null but do not mark version missing.
- Electric `engine_displacement_l=null` is expected and must not be treated as missing.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 127. BMW i4 eDrive35

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim='M-Shadow'; body_type='Liftback'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=286; transmission='single_speed'; drivetrain='RWD'; year_start=2023; year_end=2024; support_level='direct'; missing_grounded_fields=['engine_displacement_l']

### Local catalog sources already present

- [0] Cartube — גרסת כניסה חדשה: ב.מ.וו i4 eDrive35 בישראל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%92%D7%A8%D7%A1%D7%AA-%D7%9B%D7%A0%D7%99%D7%A1%D7%94-%D7%97%D7%93%D7%A9%D7%94-%D7%91-%D7%9E-%D7%95%D7%95-i4-edrive35-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C — supports=['version_or_trim', 'horsepower_hp', 'drivetrain', 'body_type', 'fuel_type', 'engine', 'year_start']
- [1] iCar — ב.מ.וו i4 - מפרט טכני — https://www.icar.co.il/bmw/i4 — supports=['transmission', 'year_start', 'year_end', 'body_type', 'fuel_type', 'version_or_trim']

### Deep validation decision and exact Codex instructions


Verdict: FIX missing trim and year coverage.
Deep validation:
- Cartube confirms i4 eDrive35 arrived in Israel in 2023 with rear electric motor, 286 hp.
- Auto current price/spec page lists eDrive35 trims `Essence` and `M-Shadow`, and also confirms eDrive35=286 hp and eDrive40=340 hp.
Required Codex edits:
- Keep current M-Shadow row.
- Add missing eDrive35 `Essence` row with same technical fields: Liftback, electric, 286 hp, single_speed, RWD, year_start=2023.
- Update year_end to 2026 or null/current according to the repo convention and current source; do not leave 2024 if the current source shows it still offered.
- Remove `engine_displacement_l` from missing fields for electric rows.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 128. BMW i5 eDrive40

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim='M-Expressive'; body_type='Sedan'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=340; transmission='single_speed'; drivetrain='RWD'; year_start=2023; year_end=None; support_level='direct'; missing_grounded_fields=['engine_displacement_l', 'year_end']
- V01: version_or_trim='M-Ultimate'; body_type='Sedan'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=340; transmission='single_speed'; drivetrain='RWD'; year_start=2023; year_end=None; support_level='direct'; missing_grounded_fields=['engine_displacement_l', 'year_end']

### Local catalog sources already present

- [0] Cartube — ב.מ.וו סדרה 5 ו-i5 החשמלית בישראל - מחיר החל מ-469,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-5-ו-i5-החשמלית-בישראל-מחיר-החל-מ-469-000-שקל — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] iCar — ב.מ.וו i5 - מחירון, מפרט טכני וחוות דעת — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_i5/ב.מ.וו_i5_חדש/ — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain']

### Deep validation decision and exact Codex instructions


Verdict: FIX. Current M-Ultimate row is wrong.
Deep validation:
- BMW Israel official price list shows i5 eDrive40 packages `Elegant` and `M-Expressive`; `M-Ultimate` belongs to i5 M60, not eDrive40.
- Auto/iCar confirm eDrive40 has one rear motor, RWD, 340 hp.
Required Codex edits:
- Delete/move the current eDrive40 `M-Ultimate` row to review or to `BMW i5 M60` only if that model exists and source mapping supports it.
- Add missing eDrive40 `Elegant` row.
- Keep eDrive40 `M-Expressive` row.
- Keep body_type Sedan, fuel_type electric, engine electric, horsepower 340, transmission single_speed, drivetrain RWD.
- Set year_end to 2026 or null/current according to repository convention using BMW Israel/iCar current source.
- Remove `engine_displacement_l` from missing fields for electric rows.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 129. BMW i7 xDrive60

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim=None; body_type='Sedan'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=544; transmission='single_speed'; drivetrain='AWD'; year_start=2022; year_end=None; support_level='direct'; missing_grounded_fields=['engine_displacement_l', 'year_end', 'version_or_trim']

### Local catalog sources already present

- [0] Cartube IL — ב.מ.וו סדרה 7 החדשה 2023 בישראל - מחיר החל מ- 869,900 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-7-החדשה-2023-בישראל-מחיר-החל-מ-869,900-שקל — supports=['body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] iCar Israel — BMW i7 - ב.מ.וו i7 מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_i7/ב.מ.וו_i7_חדש/ — supports=['body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain']

### Deep validation decision and exact Codex instructions


Verdict: KEEP; fix false missing fields and current year.
Deep validation:
- BMW Israel/iCar/Auto support i7 xDrive60 as an electric luxury sedan with AWD and 544 hp, available from the new 7-Series/i7 generation starting 2022/2023 and still represented in current pages.
Required Codex edits:
- Keep model-level `version_or_trim=null`; do not mark version_or_trim missing because xDrive60 is the model identity.
- Remove `engine_displacement_l` from missing fields for electric rows.
- Keep horsepower 544, AWD, single_speed, Sedan.
- Set year_end to 2026/current or null according to repo convention; do not mark it missing if current source grounds ongoing/current sale.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 130. BMW i8

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim=None; body_type='Coupe'; fuel_type='plug_in_hybrid'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=362; transmission='6-speed automatic'; drivetrain='AWD'; year_start=2014; year_end=2018; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='Coupe'; fuel_type='plug_in_hybrid'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=374; transmission='6-speed automatic'; drivetrain='AWD'; year_start=2018; year_end=2020; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V02: version_or_trim=None; body_type='Roadster'; fuel_type='plug_in_hybrid'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=374; transmission='6-speed automatic'; drivetrain='AWD'; year_start=2018; year_end=2020; support_level='direct'; missing_grounded_fields=['version_or_trim']

### Local catalog sources already present

- [0] Cartube.co.il — ב.מ.וו i8 נוחתת בישראל - מחיר החל מ-780,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-i8-%D7%A0%D7%95%D7%97%D7%AA%D7%AA-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-780-000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] Cartube.co.il — ב.מ.וו i8 רודסטר בישראל - מחיר החל מ- 890,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-i8-%D7%A8%D7%95%D7%93%D7%A1%D7%98%D7%A8-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-890-000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [2] iCar.co.il — ב.מ.וו i8 - מחירון, מפרט טכני, חוות דעת — https://www.icar.co.il/bmw/bmw_i8/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: KEEP; remove false missing trim.
Deep validation:
- Israeli Cartube/Auto/Yad2-style sources support i8 Coupe plug-in hybrid 1.5 with 362 hp, and the facelift/Roadster era with 374 hp. Cartube’s Roadster reveal states system output 374 hp; Auto supports the 362 hp earlier i8.
Required Codex edits:
- Keep Coupe 2014-2018 362 hp.
- Keep Coupe 2018-2020 374 hp.
- Keep Roadster 2018-2020 374 hp.
- `version_or_trim=null` is acceptable unless source lists a real trim like Luxury; remove false missing `version_or_trim` if it is only a model-level row.
- Do not expose null in website trim values.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 131. BMW iX xDrive40

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim=None; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=326; transmission='single_speed'; drivetrain='AWD'; year_start=2021; year_end=2024; support_level='direct'; missing_grounded_fields=['engine_displacement_l']

### Local catalog sources already present

- [0] Cartube.co.il — ב.מ.וו iX החשמלי בישראל - מחיר החל מ-559,000 שקלים — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-ix-%D7%94%D7%97%D7%A9%D7%9E%D7%9C%D7%99-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-559,000-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D — supports=['body_type', 'fuel_type', 'engine', 'horsepower_hp', 'drivetrain', 'year_start']
- [1] iCar.co.il — ב.מ.וו iX - מחירון, מפרטים, אמינות וחוות דעת — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_iX/%D7%91.%D7%9E.%D7%95%D7%95_iX_%D7%97%D7%93%D7%A9/ — supports=['body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Deep validation decision and exact Codex instructions


Verdict: KEEP; fix electric missing fields and confirm end/current.
Deep validation:
- iCar supports iX 2021-2025 generation with xDrive40 326 hp; current BMW all-models page still lists iX xDrive40 as a model, while one iCar version page says a 2024 xDrive40 Tech version is no longer marketed as new. This means year_end must follow exact local source semantics, not guessing.
Required Codex edits:
- Keep electric SUV, 326 hp, AWD, single_speed, year_start=2021.
- Remove `engine_displacement_l` from missing fields for electric rows.
- Keep year_end=2024 only if the specific clean row is for the old xDrive40 Tech version that iCar marks as not new after 2024. If current BMW official page lists iX xDrive40 current, either create a current row or set year_end per model/package source.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 132. BMW iX1 eDrive20

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim='X-Line / M-Sport'; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=204; transmission='single_speed'; drivetrain='FWD'; year_start=2024; year_end=None; support_level='indirect'; missing_grounded_fields=['engine_displacement_l', 'year_end']

### Local catalog sources already present

- [0] Cartube.co.il — גרסת כניסה חדשה: ב.מ.וו iX1 eDrive20 בישראל - מחיר החל מ-344,900 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%92%D7%A8%D7%A1%D7%AA-%D7%9B%D7%A0%D7%99%D7%A1%D7%94-%D7%97%D7%93%D7%A9%D7%94-%D7%91-%D7%9E-%D7%95%D7%95-ix1-edrive20-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-344900-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'horsepower_hp', 'drivetrain', 'year_start', 'version_or_trim']
- [1] iCar — ב.מ.וו iX1 - מחירון רכב, מבחני דרכים, הנחות ומבצעים — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_iX1/ — supports=['body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain']

### Deep validation decision and exact Codex instructions


Verdict: FIX support level and split trims.
Deep validation:
- Cartube confirms 2024 launch in Israel: iX1 eDrive20 is FWD, 204 hp, 454 km range, sold in X-Line and M-Sport trims. BMW Israel 04/2026 current price page also lists iX1 eDrive20 X-Line and M-Sport.
Required Codex edits:
- Change support_level from `indirect` to `direct` if using Cartube/BMW Israel/iCar direct sources.
- Split `version_or_trim='X-Line / M-Sport'` into two clean rows:
  1. `X-Line`
  2. `M-Sport`
- Keep SUV, electric, 204 hp, FWD, single_speed, year_start=2024.
- Set year_end to 2026 or null/current according to repository convention using BMW Israel current page.
- Remove `engine_displacement_l` from missing fields for electric rows.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


## 133. BMW iX2 eDrive20

Current profile_confidence: `medium`

### Current variants in clean

- V00: version_or_trim='M-Shadow'; body_type='SUV'; fuel_type='electric'; engine='electric'; engine_displacement_l=None; horsepower_hp=204; transmission='single_speed'; drivetrain='FWD'; year_start=2024; year_end=None; support_level='direct'; missing_grounded_fields=['engine_displacement_l', 'year_end']

### Local catalog sources already present

- [0] Cartube — ב.מ.וו iX2 החשמלי בישראל - מחיר החל מ- 354,900 שקל — https://www.cartube.co.il — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] iCar — ב.מ.וו iX2 - מחירון, מפרטים, רמות גימור — https://www.icar.co.il/bmw/ix2/ — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']

### Deep validation decision and exact Codex instructions


Verdict: FIX missing trim coverage, keep technical row.
Deep validation:
- BMW Israel official page and Auto/iCar support iX2 eDrive20 as electric SUV/coupe-SUV, 204 hp, FWD, 8.6 sec 0-100, 450 km range.
- Prior research indicated Israeli trims include M-Design and M-Shadow; current catalog keeps only M-Shadow.
Required Codex edits:
- Keep M-Shadow row if directly supported.
- Add `M-Design` row if local source/price list supports it.
- Keep SUV body_type unless repo has a canonical `SUV Coupe`; do not use generic Sedan/Coupe.
- Keep electric, 204 hp, single_speed, FWD, year_start=2024.
- Set year_end to current/2026 or null according to repo convention using BMW Israel current page.
- Remove `engine_displacement_l` from missing fields for electric rows.


### Acceptance checklist for this model
- No active blocked profile remains for this model.
- No null/Base/Standard/non-trim engine labels appear in website trim values.
- Every retained row has body/fuel/engine/hp/transmission/drivetrain/year fields either grounded or explicitly marked missing when allowed.
- `field_sources` and `source_indexes` are consistent after edits.


---
## Final rebuild instructions for Codex after RUN 1


After applying all RUN 1 corrections:
1. Rebuild `data/model_technical_catalog_il.json` and `data/model_technical_catalog_il_review.json`.
2. Rebuild readiness and quality outputs:
   - `data/model_technical_catalog_il_readiness.json`
   - `data/model_technical_catalog_il_quality_scan.json`
3. Run:
   ```bash
   pytest -q
   python3 -m scripts.catalog_quality_scan
   ```
4. Report exact changed files and final values for:
   - models_blocked
   - review_only_blocked_entries
   - duplicate_technical_variants
   - invalid_source_references
   - unknown_support_values
   - ready_for_website_upload
5. Do not start RUN 2 until the user supplies the next task file.


---

# RUN 2 / 3 — Deep internet-backed validation for next 20 of last 40 clean models

Date: 2026-06-16

Scope: the next 20 models from the last 40 clean profiles in `data/model_technical_catalog_il.json`, indices 134–153 in the uploaded repo state.

Codex has no web access. Do not browse. Use this file plus local repo files only. Every current variant below was checked against Israeli-market web evidence or local embedded sources; if a field cannot be grounded by the listed sources, move it to non-blocking review/archive rather than guessing.

## Non-negotiable rules

1. Israeli market only. Global reveal pages are not enough for clean retention.
2. Validate every retained variant field-by-field: model identity, trim/version, body_type, fuel_type, engine, displacement, horsepower, transmission, drivetrain, year_start, year_end.
3. `Gran Coupe` is a distinct canonical body type; never normalize it to Coupe or Sedan.
4. Pure EV rows must have `engine_displacement_l=null`; that is not a missing grounded field.
5. `version_or_trim=null` is acceptable only when the model name itself is the marketed identity, such as M760Li/M3/M5/iX3, but null must not appear in `available_values_for_website`.
6. Compound trim strings like `Business / Executive / Luxury / M-Sport / X-Line` are not clean website values. Split or normalize them.
7. New-generation naming changes matter: M135i -> M135 xDrive, M235i -> M235 xDrive Gran Coupe, X3 2.0i -> X3 20 xDrive / xDrive20i depending on generation.
8. Rebuild `sources`, `source_indexes`, `field_sources`, `available_values_for_website`, `invalid_or_non_trim_labels`, readiness and quality reports after edits.

## RUN 2 exact model list

- 134. BMW iX3 (1 variants)
- 135. BMW M135i (2 variants)
- 136. BMW M2 (4 variants)
- 137. BMW M235i (2 variants)
- 138. BMW M3 (9 variants)
- 139. BMW M4 (6 variants)
- 140. BMW M5 (6 variants)
- 141. BMW M6 (5 variants)
- 142. BMW M760Li (2 variants)
- 143. BMW M8 (3 variants)
- 144. BMW X1 sDrive20i (4 variants)
- 145. BMW X2 M35i (2 variants)
- 146. BMW X2 sDrive18i (1 variants)
- 147. BMW X2 sDrive20i (2 variants)
- 148. BMW X3 2.0i (3 variants)
- 149. BMW X3 2.5i (2 variants)
- 150. BMW X3 M (1 variants)
- 151. BMW X3 M40i (1 variants)
- 152. BMW X3 xDrive20d (2 variants)
- 153. BMW X3 xDrive30e (1 variants)

## External web evidence used by ChatGPT for RUN 2

### iX3
- Cartube tag/result: iX3 2021 בישראל, 286 hp electric, 454 km range: https://www.cartube.co.il/component/tags/tag/%D7%91-%D7%9E-%D7%95%D7%95-ix3
- BMW Israel all-models currently lists iX3 50 xDrive; do not extend old 286/RWD iX3 into 2026 without old-model evidence: https://www.bmw.co.il/he/All-Models.html

### M135i
- Cartube 2025 Series 1 Israel: new model is M135 xDrive, 300 hp, AWD, not M135i 306 hp: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-1-החדשה-2025-בישראל-מחיר-החל-מ-249900-שקל
- BMW Israel M135 technical data: 300 hp, 7-speed automatic, AWD, 1998 cc: https://www.bmw.co.il/he/All-Models/m-series/bmw-m-135/bmw-m135-5doors-technical-data.html
- Cartube 2026 Series 1 price list: M135 M-Sport Pro 300 hp: https://www.cartube.co.il/מחירון-רכב-חדש/ב-מ-וו/ב-מ-וו-סדרה-1

### M2
- Cartube tag M2: original M2 Israel 370 hp; Competition 410; CS 450; 2023 new M2 460: https://www.cartube.co.il/component/tags/tag/%D7%91-%D7%9E-%D7%95%D7%95-m2
- Cartube Jan 2025: 2025 M2 Israel, Carbon, power upgraded to 480 hp: https://www.cartube.co.il/חדשות-רכב/2025-ב-מ-וו-m2-בישראל-מחיר-659000-שקל
- BMW Israel M2 2026 price table: M2 Coupe Carbon and M2 Coupe xDrive Carbon: https://www.bmw.co.il/he/All-Models/m-series/bmw-2-series-m-models/bmw-m2-coupe.html

### M235i
- Cartube 2020 Series 2 Gran Coupe Israel: M235i 306 hp: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-2-גראן-קופה-בישראל-מחיר-249000-שקל
- Cartube 2025 Series 2 Gran Coupe Israel: new M235 xDrive Gran Coupe 300 hp: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-2-גראן-קופה-2025-החדשה-נחתה-בישראל-מחיר-294900-שקל
- BMW Israel All Models: BMW M235 xDrive Gran Coupé is current: https://www.bmw.co.il/he/All-Models.html
- BMW Israel Series 2 Gran Coupe technical data page: https://www.bmw.co.il/he/All-Models/2-series/gran-coupe/bmw-2-series-gran-coupe-technical-data.html

### M3
- Cartube M3 tag: 2021 M3/M4 Competition Israel, 510 hp RWD; xDrive available: https://www.cartube.co.il/component/tags/tag/%D7%91-%D7%9E-%D7%95%D7%95-m3
- BMW Israel M3 page: M3 still current with 510 hp: https://www.bmw.co.il/he/All-Models/m-series/m3-series/bmw-m3-sedan.html
- Cartube 2024 M3 facelift: M3 Competition xDrive upgraded to 530 hp: https://www.cartube.co.il/חדשות-רכב/מתיחת-פנים-קלה-2024-ב-מ-וו-m3-החדשה
- Cartube M3 Touring article: Touring is Competition xDrive only, 510 hp, 8AT, AWD: https://www.cartube.co.il/חדשות-רכב/סופר-סטיישן-ב-מ-וו-m3-טורינג-בישראל-מחיר-החל-מ-880-000-שקל

### M4
- Cartube M4/M3 2021 Israel: M4 Competition 510 hp RWD: https://www.cartube.co.il/component/tags/tag/%D7%91-%D7%9E-%D7%95%D7%95-m4
- Cartube 2021 M4 Convertible reveal: Competition xDrive Cabriolet 510 hp, 8AT, AWD: https://www.cartube.co.il/חדשות-רכב/2021-ב-מ-וו-m4-קבריולט-החדשה-נחשפת
- Cartube 2024 M4 facelift: Competition xDrive upgraded from 510 to 530 hp: https://www.cartube.co.il/חדשות-רכב/מתיחת-פנים-2024-ב-מ-וו-m4-החדשה
- Cartube 2026 M4 3.0 Competition technical page: 510 hp, RWD, 8AT: https://www.cartube.co.il/מחירון-רכב-חדש/ב-מ-וו/ב-מ-וו-m4/6794-ב-מ-וו-m4-3-0-competition

### M5
- iCar M5 model page: 2013-2016 4.4 V8 560 hp; older V10 era present: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_M5/
- Cartube M5 tag: 2025 M5 PHEV Israel, 727 hp: https://www.cartube.co.il/component/tags/tag/%D7%91-%D7%9E-%D7%95%D7%95-m5
- Cartube 2025 M5 Israel article: https://www.cartube.co.il/חדשות-רכב/עוצמה-היברידית-ב-מ-וו-m5-החדשה-2025-עכשיו-בישראל-מחיר-1199900-שקל

### M6
- iCar M6 model page: M6 2013-2018 exists in Israel: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_M6/
- iCar M6 2016 Gran Coupe version page: body is Gran Coupe, not Sedan: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_M6/ב.מ.וו_M6_יד_שניה_ד10/version16017/

### M760Li
- iCar BMW news: M760Li with 6.6L V12 and around 600 hp: https://www.icar.co.il/ב.מ.וו/
- Local catalog sources must decide 610 hp pre-facelift and 585 hp post-OPF/facelift split: local sources in current profile

### M8
- Cartube M8 Competition Israel source already in catalog: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-m8-קומפטישן-בישראל-מחיר-החל-מ-1-250-000-שקל
- Cartube M8 Gran Coupe Israel source already in catalog: https://www.cartube.co.il/חדשות-רכב/החל-מ-1-25-מיליון-שקל-ב-מ-וו-m8-גראן-קופה-בישראל
- Cartube M8 Gran Coupe reveal confirms body/engine: Gran Coupe, 600/625 hp, 4.4 V8 TT, xDrive; use Israel source for year_start: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-m8-גראן-קופה-נחשפת-2020

### X1 sDrive20i
- Cartube 2015/2016 X1 Israel: engines 136/192 hp, FWD: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x1-החדש-2015-בישראל-–-מחיר-החל-מ-242,000-שקל
- BMW Israel X1 technical data current: 1499 cc, 136 hp for sDrive18i, so do not use it to ground X1 sDrive20i 170/2026: https://www.bmw.co.il/he/All-Models/x-series/x1/bmw-x1-technical-data.html

### X2 M35i
- Cartube sitemap/tag: X2 M35i 306 hp noted for first generation: https://www.cartube.co.il/sitemap
- Cartube/BMW 2025 price list PDF: X2 M35i xDrive M-Sport Pro, 1998 cc: https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/Price_lists/39464%20Mechiron%20BMW%20Site%202025.pdf.asset.1749475023505.pdf
- Cartube/Carzone current X2: M35i 300 hp M-Sport Pro: https://www.cartube.co.il/חדשות-רכב/בישראל-2024-ב-מ-וו-x2-החדש-מחירון-החל-מ-359-900-שקל

### X2 sDrive18i
- Cartube 2018 X2 Israel: sDrive18i 1.5 3-cyl turbo, 140 hp, 7DCT, FWD: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x2-בישראל-מחיר-259900-שקל
- Cartube 2020/2023 PDF: later sDrive18i around 136 hp; do not extend old 140 hp indefinitely: https://www.cartube.co.il/images/mifrat/bmw/bmw-x2-mifrat-2023.pdf

### X2 sDrive20i
- Cartube 2018 X2 Israel: sDrive20i 2.0 turbo 192 hp, 7DCT, FWD: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x2-בישראל-מחיר-259900-שקל
- iCar current X2: 1.5 mild-hybrid 170 hp, 7DCT, FWD: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X2/ב.מ.וו_X2_חדש/
- BMW 2025 price list PDF: X2 sDrive20i Style DA / M-Sport: https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/Price_lists/39464%20Mechiron%20BMW%20Site%202025.pdf.asset.1749475023505.pdf

### X3 2.0i
- Cartube 2018 X3 Israel: 184-360 hp range, xDrive standard: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x3-החדש-2018-בישראל-מחיר-335000-שקל
- Cartube 2022 X3/X4 facelift: X3 xDrive20i 184 hp; M40i 360; xDrive30e 252/292 boost: https://www.cartube.co.il/חדשות-רכב/מתיחת-פנים-2022-ב-מ-וו-x3-x4-החדשים
- Cartube 2025 X3 Israel: new X3 20 xDrive 208 hp, 30e 299 hp, M50 398 hp: https://www.cartube.co.il/חדשות-רכב/2025-ב-מ-וו-x3-החדש-בישראל-מחיר-424900-שקל
- iCar current X3: 208 hp / 398 hp / 299 hp: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X3/ב.מ.וו_X3_חדש/

### X3 2.5i
- iCar X3 generation 1 source in catalog: 2.5i 192/218 hp must be used for years and transmission: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X3/ב.מ.וו_X3_דור_1/

### X3 M
- Cartube 2019 X3M/X4M: Competition upgrades to 510 hp, 8AT, M xDrive: https://www.cartube.co.il/חדשות-רכב/ביצועים-2019-ב-מ-וו-x3m-ו-x4m-החדשים
- iCar X3 M catalog source in current profile: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X3_M/

### X3 M40i
- Cartube 2018 X3 Israel: X3 xDrive M40i with 360 hp: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x3-החדש-2018-בישראל-מחיר-335000-שקל
- Cartube 2022 facelift lists X3 M40i 360 hp: https://www.cartube.co.il/חדשות-רכב/מתיחת-פנים-2022-ב-מ-וו-x3-x4-החדשים

### X3 xDrive20d
- Cartube 2022 X3 facelift: xDrive20d 190 hp, 8AT, AWD: https://www.cartube.co.il/חדשות-רכב/מתיחת-פנים-2022-ב-מ-וו-x3-x4-החדשים
- Gear local price-list source in current profile supports 2018-2022 xLine 190 hp: https://www.gear.co.il/מחירון_רכב/ב.מ.וו-X3/2018

### X3 xDrive30e
- Cartube 2019/2020 X3 xDrive30e: 292 hp, 2.0 turbo + electric, arrival Israel mid-2020: https://www.cartube.co.il/חדשות-רכב/2020-ב-מ-וו-x3-היברידי-פלאג-אין-נחשף-בשנה-הבאה-בישראל
- iCar X3 PHEV: 292 hp and 8-speed automatic: https://www.icar.co.il/חדשות_רכב/ב.%D7%9E.%D7%95%D7%95_X3_מקבל_%D7%92%D7%A8%D7%A1%D7%94_%D7%94%D7%99%D7%91%D7%A8%D7%99%D7%93%D7%99%D7%AA-%D7%A0%D7%98%D7%A2%D7%A0%D7%AA/
- iCar current X3 2024 PHEV M-Sport Edition 30e page; new 2025 G45 is 299 hp, not same row: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X3/ב.מ.וו_X3_חדש/version24667/

---

## 134. BMW iX3

Priority: MEDIUM-HIGH

### Current local sources
- Source 0 / source_index 0: BMW iX3: מחיר, טווח נסיעה חשמלי, מפרט ועיצוב | BMW.co.il — https://www.bmw.co.il/he/all-models/x-series/iX3/2021/bmw-ix3-highlights.html — supports: body_type, fuel_type, engine, year_end
- Source 1 / source_index 1: ב.מ.וו iX3 חדש - מחירון, מבחנים ומפרט טכני - iCar — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/iX3/%D7%91.%D7%9E.%D7%95%D7%95_iX3_%D7%97%D7%93%D7%A9/ — supports: body_type, fuel_type, engine, horsepower_hp, drivetrain, year_start, year_end
- Source 2 / source_index 2: ב.מ.וו iX3 החשמלי בישראל - מחיר החל מ-429,900 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-ix3-%D7%94%D7%97%D7%A9%D7%9E%D7%9C%D7%99-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-429,900-%D7%A9%D7%A7%D7%9C — supports: horsepower_hp, transmission, drivetrain, year_start

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP with cleanup. It is an old G08 iX3 row: SUV, electric, 286 hp, single-speed, RWD, start 2021. `engine_displacement_l=null` is correct for a pure EV and must not be a missing grounded field. Keep `year_end=2025` unless a local source explicitly proves the old 286 hp/RWD iX3 was still sold in 2026. Do not overwrite this row with the newer/current iX3 50 xDrive identity.

#### V00 current row
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "electric",
  "engine": "electric",
  "engine_displacement_l": null,
  "horsepower_hp": 286,
  "transmission": "single_speed",
  "drivetrain": "RWD",
  "year_start": 2021,
  "year_end": 2025,
  "support_level": "direct",
  "missing_grounded_fields": [
    "engine_displacement_l"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.
Specific correction: remove `engine_displacement_l` from `missing_grounded_fields`; pure EV displacement is intentionally null.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 135. BMW M135i

Priority: MEDIUM-HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו M135i בישראל - מחיר החל מ-298 אלף שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-m135i-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-298-%D7%90%D7%9C%D7%A3-%D7%A9%D7%A7%D7%9C — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start
- Source 1 / source_index 1: ב.מ.וו סדרה 1 2012-2015 מחירון, מפרטים, אמינות וחוות דעת — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_1_%D7%99%D7%A9%D7%9F_%D7%A2%D7%93_2015/ — supports: engine, horsepower_hp, year_end
- Source 2 / source_index 2: ב.מ.וו סדרה 1 החדשה 2020 בישראל - מחיר החל מ- 199,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-1-%D7%94%D7%97%D7%93%D7%A9%D7%94-2020-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-199000-%D7%A9%D7%A7%D7%9C — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, version_or_trim
- Source 3 / source_index 3: ב.מ.וו סדרה 1 2020-2024 מחירון, מפרטים, אמינות וחוות דעת — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_1/ — supports: engine, horsepower_hp, transmission, year_end

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP as historical M135i: 3.0 turbo, 320 hp, RWD, hatchback, 2012-2016. V01 KEEP only for the F40-era M135i xDrive 306 hp, but close at `year_end=2024`. Do not extend this row into the 2025/F70 generation. For the current F70 model, create/split a separate BMW `M135` or `M135 xDrive` profile/row only if the catalog design allows it: Hatchback, petrol, 2.0L turbo, 300 hp, 7-speed automatic/DCT, AWD, `version_or_trim="M-Sport Pro"`, `year_start=2025`, `year_end=null/current`. Do not call it M135i.

#### V00 current row
```json
{
  "version_or_trim": null,
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "3.0L turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 320,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2012,
  "year_end": 2016,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": "xDrive",
  "body_type": "Hatchback",
  "fuel_type": "petrol",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 306,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2019,
  "year_end": 2024,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 136. BMW M2

Priority: MEDIUM-HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו M2 בישראל – מחיר החל מ-570,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-m2-בישראל-מחיר-החל-מ-570-000-שקל — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end
- Source 1 / source_index 1: ב.מ.וו M2 קומפטישן בישראל - מחיר החל מ- 585,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-m2-קומפטישן-בישראל-מחיר-החל-מ-585-000-שקל — supports: body_type, fuel_type, version_or_trim, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end
- Source 2 / source_index 2: ב.מ.וו M2 CS בישראל - מחיר החל מ- 710,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-m2-cs-בישראל-מחיר-החל-מ-710-000-שקל — supports: version_or_trim, engine, engine_displacement_l, horsepower_hp, transmission, year_start, year_end
- Source 3 / source_index 3: הדור החדש: 2023 ב.מ.וו M2 החדשה בישראל - מחיר החל מ-620,000 שקל — https://www.cartube.co.il/חדשות-רכב/הדור-החדש-2023-ב-מ-וו-m2-החדשה-בישראל-מחיר-החל-מ-620-000-שקל — supports: body_type, fuel_type, version_or_trim, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP original M2 370 hp 2016-2018. V01 KEEP Competition 410 hp 2018-2021. V02 KEEP CS 450 hp 2020-2021. V03 KEEP Carbon 460 hp for 2023-2024 only. Add/split 2025+ M2 Carbon 480 hp if not present, because the 2025 Israeli source upgrades the M2 to 480 hp. If adding 2026 xDrive Carbon, keep it as a separate row: same M2 Coupe body, AWD, 480 hp, source BMW Israel current price table. Rebuild website values so Carbon is exposed once, not duplicated as separate bad labels.

#### V00 current row
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.0L turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 370,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2016,
  "year_end": 2018,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": "Competition",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 410,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2018,
  "year_end": 2021,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V02 current row
```json
{
  "version_or_trim": "CS",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 450,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2020,
  "year_end": 2021,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V03 current row
```json
{
  "version_or_trim": "Carbon",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 460,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2023,
  "year_end": 2024,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 137. BMW M235i

Priority: HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו סדרה 2 יד שניה - מפרט טכני — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_2/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_2_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_d1/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end
- Source 1 / source_index 1: ב.מ.וו סדרה 2 גראן קופה בישראל - מחיר החל מ- 239,900 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-2-%D7%92%D7%A8%D7%90%D7%9F-%D7%A7%D7%95%D7%A4%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-239900-%D7%A9%D7%A7%D7%9C — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP historical M235i Coupe: 3.0 turbo, 326 hp, RWD, 8AT, 2014-2016; version_or_trim may remain null because M235i is the model-level identity. V01 FIX body_type from `Sedan` to `Gran Coupe`. Keep F44 M235i xDrive Gran Coupe 306 hp for 2020-2024. Do not let Gran Coupe normalize to Coupe/Sedan. Add/split the new 2025+ `M235 xDrive Gran Coupe` only under the correct model identity/name if desired: 2.0 turbo, 300 hp, AWD, 7DCT/automatic, M-Sport Pro. Do not extend 306 hp M235i open-ended into 2025/2026.

#### V00 current row
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.0L turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 326,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2014,
  "year_end": 2016,
  "support_level": "direct",
  "missing_grounded_fields": [
    "version_or_trim"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 306,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2020,
  "year_end": null,
  "support_level": "direct",
  "missing_grounded_fields": [
    "version_or_trim",
    "year_end"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.
Specific correction: change `body_type` from `Sedan` to `Gran Coupe`; close this 306 hp M235i xDrive row at 2024 and do not extend into 2025+ M235 300 hp.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 138. BMW M3

Priority: HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו M3 ו-M4 החדשות 2021 בישראל - מחיר החל מ-760,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-m3-%D7%95-m4-%D7%94%D7%97%D7%93%D7%A9%D7%95%D7%AA-2021-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-760-000-%D7%A9%D7%A7%D7%9C — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, version_or_trim
- Source 1 / source_index 1: ב.מ.וו M3 ו-M4 עם הנעה כפולה xDrive נוחתות בישראל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-m3-%D7%95-m4-%D7%A2%D7%9D-%D7%94%D7%A0%D7%A2%D7%94-%D7%9B%D7%A4%D7%95%D7%9C%D7%94-xdrive-%D7%A0%D7%95%D7%97%D7%AA%D7%95%D7%AA-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, version_or_trim
- Source 2 / source_index 2: סופר סטיישן: ב.מ.וו M3 טורינג בישראל - מחיר — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%A1%D7%95%D7%A4%D7%A8-%D7%A1%D7%98%D7%99%D7%99%D7%A9%D7%9F-%D7%91-%D7%9E-%D7%95%D7%95-m3-%D7%98%D7%95%D7%A8%D7%99%D7%A0%D7%92-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-880-000-%D7%A9%D7%A7%D7%9C — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, version_or_trim
- Source 3 / source_index 3: ב.מ.וו M3 דור 5 (2014-2018) יד שניה מחירון ומפרטים — https://www.icar.co.il/%D7%93%D7%92%D7%9E%D7%99-%D7%A8%D7%9B%D7%91/%D7%91.%D7%9E.%D7%95%D7%95_M3_%D7%93%D7%95%D7%A8_5/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, version_or_trim
- Source 4 / source_index 4: ב.מ.וו M3 דור 4 (2008-2013) מחירון — https://www.icar.co.il/%D7%93%D7%92%D7%9E%D7%99-%D7%A8%D7%9B%D7%91/%D7%91.%D7%9E.%D7%95%D7%95_M3_%D7%93%D7%95%D7%A8_4/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end
- Source 5 / source_index 5: ב.מ.וו M3 דור 3 (2001-2006) יד שניה מחירון — https://www.icar.co.il/%D7%93%D7%92%D7%9E%D7%99-%D7%A8%D7%9B%D7%91/%D7%91.%D7%9E.%D7%95%D7%95_M3_%D7%93%D7%95%D7%A8_3/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP M3 Competition Sedan RWD 510 hp from 2021; remove `year_end` from missing if current source supports it as active. V01 SPLIT: 2021-2024 M3 Competition xDrive Sedan is 510 hp; 2024/2025+ facelift xDrive must be 530 hp. Do not keep one open-ended AWD 510 hp row through current years. V02 KEEP M3 Touring/Estate Competition xDrive 510 hp from 2023; `year_end=null` is acceptable if current. V03 KEEP F80 M3 Sedan base 431 hp 2014-2018; null trim is acceptable and should not be exposed. V04 KEEP Competition 450 hp 2016-2018. V05/V06/V07 KEEP E9x M3 body rows only if iCar local sources support Coupe/Sedan/Convertible 4.0 V8 420 hp; null trim is acceptable. V08 KEEP E46 M3 Coupe 3.2 343 hp only if source supports the automatic/SMG transmission; otherwise correct transmission to source wording or move to review.

#### V00 current row
```json
{
  "version_or_trim": "Competition",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo inline-6",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 510,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2021,
  "year_end": null,
  "support_level": "direct",
  "missing_grounded_fields": [
    "year_end"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": "Competition",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo inline-6",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 510,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2021,
  "year_end": null,
  "support_level": "direct",
  "missing_grounded_fields": [
    "year_end"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.
Specific correction: split the xDrive row so pre-facelift remains 510 hp and 2024/2025+ facelift xDrive becomes 530 hp if retained as current.

#### V02 current row
```json
{
  "version_or_trim": "Competition",
  "body_type": "Estate",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo inline-6",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 510,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2023,
  "year_end": null,
  "support_level": "direct",
  "missing_grounded_fields": [
    "year_end"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V03 current row
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo inline-6",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 431,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2014,
  "year_end": 2018,
  "support_level": "direct",
  "missing_grounded_fields": [
    "version_or_trim"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V04 current row
```json
{
  "version_or_trim": "Competition",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo inline-6",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 450,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2016,
  "year_end": 2018,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V05 current row
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "4.0L v8",
  "engine_displacement_l": 4.0,
  "horsepower_hp": 420,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2008,
  "year_end": 2013,
  "support_level": "direct",
  "missing_grounded_fields": [
    "version_or_trim"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V06 current row
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "4.0L v8",
  "engine_displacement_l": 4.0,
  "horsepower_hp": 420,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2008,
  "year_end": 2013,
  "support_level": "direct",
  "missing_grounded_fields": [
    "version_or_trim"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V07 current row
```json
{
  "version_or_trim": null,
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "4.0L v8",
  "engine_displacement_l": 4.0,
  "horsepower_hp": 420,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2008,
  "year_end": 2013,
  "support_level": "direct",
  "missing_grounded_fields": [
    "version_or_trim"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V08 current row
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.2L inline-6",
  "engine_displacement_l": 3.2,
  "horsepower_hp": 343,
  "transmission": "6-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2001,
  "year_end": 2006,
  "support_level": "direct",
  "missing_grounded_fields": [
    "version_or_trim"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 139. BMW M4

Priority: HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו M4 דור 1 - מפרט טכני — https://www.icar.co.il/bmw/bmw_m4/bmw_m4_gen_1/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, version_or_trim
- Source 1 / source_index 1: ב.מ.וו M4 קבריולה דור 1 - מפרט טכני — https://www.icar.co.il/bmw/bmw_m4_cabriolet/bmw_m4_cabriolet_gen_1/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, version_or_trim
- Source 2 / source_index 2: ב.מ.וו M3 ו-M4 החדשות 2021 בישראל - מחיר החל מ-760,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-m3-ו-m4-החדשות-2021-בישראל-מחיר-החל-מ-760000-שקל — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, version_or_trim
- Source 3 / source_index 3: ב.מ.וו M3 ו-M4 קומפטישן xDrive בישראל - מחיר החל מ-800,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-m3-ו-m4-קומפטישן-xdrive-בישראל-מחיר-החל-מ-800000-שקל — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, version_or_trim

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP F82 M4 Coupe base 431 hp 2014-2020. V01 KEEP F82 Competition 450 hp 2016-2020. V02 KEEP F83 Convertible base 431 hp 2015-2020. V03 KEEP G82 M4 Competition RWD 510 hp 2021-current if current price list supports it. V04/V05 SPLIT xDrive rows: 2022-2024 Competition xDrive Coupe/Convertible 510 hp; from the 2024 facelift onward xDrive is 530 hp. Do not leave open-ended 510 hp xDrive rows if the current Israeli technical page/source shows 530 hp. Rebuild website values for Coupe vs Convertible separately.

#### V00 current row
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo i6",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 431,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2014,
  "year_end": 2020,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": "Competition",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo i6",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 450,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2016,
  "year_end": 2020,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V02 current row
```json
{
  "version_or_trim": null,
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo i6",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 431,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2015,
  "year_end": 2020,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V03 current row
```json
{
  "version_or_trim": "Competition",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo i6",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 510,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2021,
  "year_end": 2026,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V04 current row
```json
{
  "version_or_trim": "Competition xDrive",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo i6",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 510,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2022,
  "year_end": 2026,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.
Specific correction: split the xDrive row so 2022-2024 remains 510 hp and 2024/2025+ facelift xDrive becomes 530 hp if retained as current.

#### V05 current row
```json
{
  "version_or_trim": "Competition xDrive",
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo i6",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 510,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2022,
  "year_end": 2026,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.
Specific correction: split the xDrive row so 2022-2024 remains 510 hp and 2024/2025+ facelift xDrive becomes 530 hp if retained as current.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 140. BMW M5

Priority: HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו M5 - מחירון, חוות דעת ומפרט טכני — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_M5/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end
- Source 1 / source_index 1: ב.מ.וו M5 החדשה (2012) בישראל: החל מ- 955,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-m5-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%94%D7%97%D7%9C-%D7%9E-955,000-%D7%A9%D7%A7%D7%9C — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start
- Source 2 / source_index 2: ב.מ.וו M5 החדשה 2018 בישראל - מחיר החל מ- 1,150,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-m5-%D7%94%D7%97%D7%93%D7%A9%D7%94-2018-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1-150-000-%D7%A9%D7%A7%D7%9C — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start
- Source 3 / source_index 3: ב.מ.וו M5 קומפטישן (Competition) בישראל – מחיר החל מ-1,250,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-m5-%D7%A7%D7%95%D7%9E%D7%A4%D7%98%D7%99%D7%A9%D7%9F-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1250000-%D7%A9%D7%A7%D7%9C — supports: horsepower_hp, version_or_trim, year_start, transmission, drivetrain
- Source 4 / source_index 4: ב.מ.וו M5 CS בישראל - מחיר החל מ- 1,700,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-m5-cs-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1700000-%D7%A9%D7%A7%D7%9C — supports: horsepower_hp, version_or_trim, year_start, year_end, transmission, drivetrain, engine
- Source 5 / source_index 5: ב.מ.וו M5 החדשה 2024 נחשפת - פלאג-אין עם 727 כ״ס — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-m5-%D7%94%D7%97%D7%93%D7%A9%D7%94-2024-%D7%A0%D7%97%D7%A9%D7%A4%D7%AA-%D7%A4%D7%9C%D7%90%D7%92-%D7%90%D7%99%D7%9F-%D7%A2%D7%9D-727-%D7%9B-%D7%A1 — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP E60 V10 507 hp 2005-2010 if local source supports. V01 KEEP F10 4.4 V8 TT 560 hp 2012-2017. V02 KEEP F90 base 600 hp 2018-2023. V03 KEEP Competition 625 hp 2018-2023. V04 KEEP CS 635 hp 2021-2022. V05 FIX year_start from 2024 to 2025 for the new PHEV M5 in Israel; keep 4.4 V8 PHEV, 727 hp, 8AT, AWD. `year_end=null` is acceptable only if current. Do not use global 2024 reveal as Israeli `year_start`.

#### V00 current row
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "5.0L v10",
  "engine_displacement_l": 5.0,
  "horsepower_hp": 507,
  "transmission": "7-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2005,
  "year_end": 2010,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "4.4L v8 twin-turbo",
  "engine_displacement_l": 4.4,
  "horsepower_hp": 560,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2012,
  "year_end": 2017,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V02 current row
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "4.4L v8 twin-turbo",
  "engine_displacement_l": 4.4,
  "horsepower_hp": 600,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2018,
  "year_end": 2023,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V03 current row
```json
{
  "version_or_trim": "Competition",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "4.4L v8 twin-turbo",
  "engine_displacement_l": 4.4,
  "horsepower_hp": 625,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2018,
  "year_end": 2023,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V04 current row
```json
{
  "version_or_trim": "CS",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "4.4L v8 twin-turbo",
  "engine_displacement_l": 4.4,
  "horsepower_hp": 635,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2021,
  "year_end": 2022,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V05 current row
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "plug_in_hybrid",
  "engine": "4.4L v8 twin-turbo",
  "engine_displacement_l": 4.4,
  "horsepower_hp": 727,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2024,
  "year_end": null,
  "support_level": "direct",
  "missing_grounded_fields": [
    "year_end"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.
Specific correction: change `year_start` to 2025 unless a direct Israeli 2024 sales/price source exists; global 2024 reveal is not enough.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 141. BMW M6

Priority: HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו M6 החדשה נוחתת בישראל: קופה וקבריולט - קארטיוב — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-m6-החדשה-נוחתת-בישראל-קופה-וקבריולט — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start
- Source 1 / source_index 1: ב.מ.וו M6 גראן קופה בישראל – החל מ- 1,065,000 שקל - קארטיוב — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-m6-גראן-קופה-החל-מ-1,065,000-שקל — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start
- Source 2 / source_index 2: ב.מ.וו M6 (2005-2010) מחירון, מפרט טכני וחוות דעת - iCar — https://www.icar.co.il/bmw/bmw_m6/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end

### Current variants and required Codex decisions

**Model-level decision:**
V00/V01 KEEP E63/E64 M6 5.0 V10 507 hp Coupe/Convertible 2005-2010. V02/V03 KEEP F12/F13 M6 4.4 V8 TT 560 hp Coupe/Convertible 2012-2018 if source supports. V04 FIX body_type from `Sedan` to `Gran Coupe`. BMW M6 Gran Coupe is not a sedan and must remain canonical `Gran Coupe`. If local source does not support exact year_start=2013, adjust to source. Add `Gran Coupe` to canonical body types if needed. Rebuild website values so body_type includes Coupe, Convertible, Gran Coupe.

#### V00 current row
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "5.0L v10",
  "engine_displacement_l": 5.0,
  "horsepower_hp": 507,
  "transmission": "7-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2005,
  "year_end": 2010,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": null,
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "5.0L v10",
  "engine_displacement_l": 5.0,
  "horsepower_hp": 507,
  "transmission": "7-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2005,
  "year_end": 2010,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V02 current row
```json
{
  "version_or_trim": null,
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "4.4L v8 twin-turbo",
  "engine_displacement_l": 4.4,
  "horsepower_hp": 560,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2012,
  "year_end": 2018,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V03 current row
```json
{
  "version_or_trim": null,
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "4.4L v8 twin-turbo",
  "engine_displacement_l": 4.4,
  "horsepower_hp": 560,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2012,
  "year_end": 2018,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V04 current row
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "4.4L v8 twin-turbo",
  "engine_displacement_l": 4.4,
  "horsepower_hp": 560,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "RWD",
  "year_start": 2013,
  "year_end": 2018,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.
Specific correction: change `body_type` from `Sedan` to `Gran Coupe`; this is not a sedan row.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 142. BMW M760Li

Priority: MEDIUM-HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו M760Li xDrive בישראל - מחיר החל מ-1.15 מיליון שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-m760li-xdrive-בישראל-מחיר-החל-מ-1-15-מיליון-שקל — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start
- Source 1 / source_index 1: ב.מ.וו סדרה 7 החדשה 2019 בישראל - מחיר החל מ- 765,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-7-החדשה-2019-בישראל-מחיר-החל-מ-765-000-שקל — supports: horsepower_hp, year_start, engine, engine_displacement_l, transmission, drivetrain
- Source 2 / source_index 2: ב.מ.וו סדרה 7 - מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_דור_6/מפרט_טכני/ — supports: year_end, body_type, fuel_type

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP M760Li xDrive 6.6 V12 TT 610 hp 2017-2019 if local sources support. V01 KEEP facelift/post-emissions M760Li xDrive 585 hp 2019-2022 if local sources support. Null trim is acceptable because M760Li is model-level identity. Do not merge with older 760i/760Li 6.0 V12 rows and do not expose null trim.

#### V00 current row
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "6.6L v12 twin-turbo",
  "engine_displacement_l": 6.6,
  "horsepower_hp": 610,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2017,
  "year_end": 2019,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "6.6L v12 twin-turbo",
  "engine_displacement_l": 6.6,
  "horsepower_hp": 585,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2019,
  "year_end": 2022,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 143. BMW M8

Priority: HIGH

### Current local sources
- Source 0 / source_index 450: ב.מ.וו M8 קומפטישן בישראל - מחיר החל מ- 1,250,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-m8-%D7%A7%D7%95%D7%9E%D7%A4%D7%98%D7%99%D7%A9%D7%9F-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-1-250-000-%D7%A9%D7%A7%D7%9C — supports: body_type, version_or_trim, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start
- Source 1 / source_index 451: החל מ-1.25 מיליון שקל: ב.מ.וו M8 גראן קופה בישראל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%94%D7%97%D7%9C-%D7%9E-1-25-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C-%D7%91-%D7%9E-%D7%95%D7%95-m8-%D7%92%D7%A8%D7%90%D7%9F-%D7%A7%D7%95%D7%A4%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C — supports: body_type, version_or_trim, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start
- Source 2 / source_index 452: ב.מ.וו M8 - מחירון, מפרטים, ואבזור — https://www.icar.co.il/bmw/m8/ — supports: body_type, version_or_trim, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP M8 Competition Coupe 4.4 V8 TT 625 hp, AWD, 8AT. V01 KEEP M8 Competition Convertible 625 hp. V02 FIX body_type from `Sedan` to `Gran Coupe`; this row is M8 Competition Gran Coupe, not Sedan. Keep 625 hp, AWD, 8AT. Validate year_end=2024 with iCar/current source; if not grounded, set year_end=null/current or move end year to missing, but do not guess. Rebuild body_type website values: Coupe, Convertible, Gran Coupe.

#### V00 current row
```json
{
  "version_or_trim": "Competition",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "4.4L v8 twin-turbo",
  "engine_displacement_l": 4.4,
  "horsepower_hp": 625,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2020,
  "year_end": 2024,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": "Competition",
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "4.4L v8 twin-turbo",
  "engine_displacement_l": 4.4,
  "horsepower_hp": 625,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2020,
  "year_end": 2024,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V02 current row
```json
{
  "version_or_trim": "Competition",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "4.4L v8 twin-turbo",
  "engine_displacement_l": 4.4,
  "horsepower_hp": 625,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2020,
  "year_end": 2024,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.
Specific correction: change `body_type` from `Sedan` to `Gran Coupe`; this is not a sedan row.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 144. BMW X1 sDrive20i

Priority: HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו X1 זוכה במנוע חדש: 2.0 ליטר טורבו - קארטיוב (2011) — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x1-זוכה-במנוע-חדש-2-0-ליטר-טורבו — supports: year_start, year_end, body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain
- Source 1 / source_index 1: ב.מ.וו X1 החדש 2016 בישראל – מחיר החל מ- 239,000 שקל - קארטיוב — https://www.cartube.co.il/חדשות-רכב/2016-ב-מ-וו-x1-החדש-בישראל-מחיר-החל-מ-239000-שקל — supports: year_start, year_end, body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain
- Source 2 / source_index 2: 2019 ב.מ.וו X1 החדש בישראל (מתיחת פנים) - מחיר החל מ- 249,000 שקל - קארטיוב — https://www.cartube.co.il/חדשות-רכב/2019-ב-מ-וו-x1-החדש-בישראל-מחיר-החל-מ-249000-שקל — supports: year_start, year_end, transmission, horsepower_hp, drivetrain
- Source 3 / source_index 3: ב.מ.וו X1 החדש 2023 בישראל - מחיר החל מ- 274,900 שקל - קארטיוב — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x1-החדש-2023-בישראל-מחיר-החל-מ-274900-שקל — supports: year_start, year_end, body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain
- Source 4 / source_index 4: ב.מ.וו X1 - מפרט טכני, מחירון רכב - iCar — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X1/ — supports: year_start, year_end, body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP first-gen/early X1 2.0 turbo 184 hp RWD 2011-2015 if local source supports. V01 KEEP F48 sDrive20i 192 hp FWD 2015-2018. V02 KEEP facelift F48 192 hp FWD with 7DCT 2018-2022. V03 REVIEW/FIX: current BMW Israel technical data shown in web evidence is sDrive18i 136 hp, not sDrive20i 170 hp; the 2023 Israeli launch source says only sDrive18i at first. If local source does not specifically prove X1 sDrive20i 170 hp sold in Israel 2022-2026, move V03 to review or split it to the correct model identity if it is actually X1 sDrive18i/20i from another market. Do not keep an ungrounded current X1 sDrive20i row.

#### V00 current row
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.0L inline-4 turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 184,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2011,
  "year_end": 2015,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.0L inline-4 turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 192,
  "transmission": "8-speed automatic",
  "drivetrain": "FWD",
  "year_start": 2015,
  "year_end": 2018,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V02 current row
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.0L inline-4 turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 192,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2018,
  "year_end": 2022,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V03 current row
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "mild_hybrid",
  "engine": "1.5L inline-3 turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 170,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2022,
  "year_end": 2026,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 145. BMW X2 M35i

Priority: MEDIUM-HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו X2 (2018-2024) - גרסאות ומחירים: X2 M35i — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X2/ב.מ.וו_X2_יד_שניה_דייר_1/גרסאות/ב.מ.וו_X2_M35i_4x4_אוט'_2.0_טורבו/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end
- Source 1 / source_index 1: בישראל: 2024 ב.מ.וו X2 החדש - מחירון החל מ- 359,900 שקל — https://www.cartube.co.il/חדשות-רכב/בישראל-2024-ב-מ-וו-x2-החדש-מחירון-החל-מ-359-900-שקל — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, version_or_trim

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP first-gen X2 M35i 306 hp AWD 2019-2023 if local source supports. V01 KEEP/FIX current U10 X2 M35i xDrive M-Sport Pro 300 hp from 2024/current, 2.0 turbo, AWD, 7-speed DCT/automatic. If year_end=2024 is too short and current 2025 BMW price list supports it, set year_end=null/current rather than 2024. Do not merge 306 hp and 300 hp rows.

#### V00 current row
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 306,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2019,
  "year_end": 2023,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": "M-Sport Pro",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 300,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "AWD",
  "year_start": 2024,
  "year_end": 2024,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 146. BMW X2 sDrive18i

Priority: MEDIUM-HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו X2 בישראל - מחיר החל מ- 289,900 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x2-בישראל-מחיר-החל-מ-289900-שקל — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start
- Source 1 / source_index 1: ב.מ.וו X2 מפרט טכני - iCar — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X2/ב.מ.וו_X2_יד_שניה_דיי1/version16075/ — supports: body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_end

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP only for 2018-2020/2023 span if local sources support 140 hp. Be careful: later BMW X2 2023 PDF shows sDrive18i 136 hp, not 140. If this profile is meant to cover 2018-2023, split into 140 hp early and 136 hp late, or adjust years. Do not leave one 140 hp row through 2023 if source contradicts it.

#### V00 current row
```json
{
  "version_or_trim": null,
  "body_type": "Crossover",
  "fuel_type": "petrol",
  "engine": "1.5L turbo i3",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 140,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2018,
  "year_end": 2023,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 147. BMW X2 sDrive20i

Priority: MEDIUM-HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו X2 (2018-2024) - מחירון מפרטים אמינות ועוד | iCar — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_X2/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, version_or_trim
- Source 1 / source_index 1: ב.מ.וו X2 החדש 2024 בישראל - מחיר החל מ- 389,900 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-x2-%D7%94%D7%97%D7%93%D7%A9-2024-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-389-900-%D7%A9%D7%A7%D7%9C — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, version_or_trim

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP old F39 X2 sDrive20i M-Sport: 2.0 turbo, 192 hp, 7DCT, FWD, 2018-2023. V01 KEEP current U10 X2 sDrive20i M-Sport/Style: 1.5 turbo mild-hybrid, 170 hp, 7DCT, FWD, year_start=2024. `year_end=null` is acceptable/current if BMW price list supports 2025/2026. Add/split `Style DA` if website trim values require both Style DA and M-Sport from BMW price list.

#### V00 current row
```json
{
  "version_or_trim": "M-Sport",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 192,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2018,
  "year_end": 2023,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": "M-Sport",
  "body_type": "SUV",
  "fuel_type": "mild_hybrid",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 170,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2024,
  "year_end": null,
  "support_level": "direct",
  "missing_grounded_fields": [
    "year_end"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 148. BMW X3 2.0i

Priority: HIGH

### Current local sources
- Source 0 / source_index 0: iCar Israel - BMW X3 2.0i (2004-2010) Specs & Trims — https://www.icar.co.il/bmw/x3/generation1 — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, version_or_trim
- Source 1 / source_index 1: Auto.co.il - BMW X3 xDrive20i (2011-2024) Specs — https://www.auto.co.il/model/bmw-x3_g2/xDrive20i — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, version_or_trim
- Source 2 / source_index 2: BMW Israel Official Catalog - New X3 xDrive20 Mild Hybrid — https://www.bmw.co.il/he/all-models/x-series/X3/bmw-x3-overview.html — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, version_or_trim

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP old X3 2.0i LE 150 hp 2004-2010 if local source supports. V01 FIX model identity: from 2011 onward this is marketed as X3 xDrive20i, not generic X3 2.0i. If catalog policy keeps canonical `X3 2.0i`, ensure website can distinguish xDrive20i; otherwise split/move to `BMW X3 xDrive20i`. Do not expose compound trim string `Business / Executive / Luxury / M-Sport / X-Line`; split into individual trim rows or move trim to website list only if source supports each. V02 FIX: new 2025 X3 20 xDrive mild-hybrid has 208 hp and trims M-Sport/M-Tech/M-Launch; year_start should be 2025, not 2024, unless direct Israel launch in 2024. Also identity should be `X3 20 xDrive`, not `X3 2.0i`.

#### V00 current row
```json
{
  "version_or_trim": "LE",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.0L",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 150,
  "transmission": "manual",
  "drivetrain": "AWD",
  "year_start": 2004,
  "year_end": 2010,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": "Business / Executive / Luxury / M-Sport / X-Line",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 184,
  "transmission": "automatic",
  "drivetrain": "AWD",
  "year_start": 2011,
  "year_end": 2024,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.
Specific correction: split compound trim labels into separate clean rows or remove from trim if not directly grounded. Do not expose compound slash-separated trim strings.

#### V02 current row
```json
{
  "version_or_trim": "M-Sport / M-Tech",
  "body_type": "SUV",
  "fuel_type": "mild_hybrid",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 208,
  "transmission": "automatic",
  "drivetrain": "AWD",
  "year_start": 2024,
  "year_end": 2026,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.
Specific correction: split compound trim labels into separate clean rows or remove from trim if not directly grounded. Do not expose compound slash-separated trim strings.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 149. BMW X3 2.5i

Priority: MEDIUM-HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו X3 דור 1 (2004-2010) - מחירון, מפרט טכני וחוות דעת — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_X3/%D7%91.%D7%9E.%D7%95%D7%95_X3_%D7%93%D7%95%D7%A8_1/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end
- Source 1 / source_index 1: ב.מ.וו X3 מידע כללי - אוטו — https://www.auto.co.il/model/bmw-x3_g106 — supports: body_type, fuel_type, horsepower_hp, transmission, drivetrain

### Current variants and required Codex decisions

**Model-level decision:**
V00/V01 KEEP historical X3 2.5i rows only if iCar generation 1 supports both 192 hp 2004-2006 and 218 hp 2006-2010 with automatic AWD. Null trim is acceptable for model-level engine identity and should not be in website trim values.

#### V00 current row
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.5L",
  "engine_displacement_l": 2.5,
  "horsepower_hp": 192,
  "transmission": "automatic",
  "drivetrain": "AWD",
  "year_start": 2004,
  "year_end": 2006,
  "support_level": "direct",
  "missing_grounded_fields": [
    "version_or_trim"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": null,
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.5L",
  "engine_displacement_l": 2.5,
  "horsepower_hp": 218,
  "transmission": "automatic",
  "drivetrain": "AWD",
  "year_start": 2006,
  "year_end": 2010,
  "support_level": "direct",
  "missing_grounded_fields": [
    "version_or_trim"
  ]
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 150. BMW X3 M

Priority: MEDIUM-HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו X3 M קומפטישן בישראל - מחיר החל מ-870,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x3-m-קומפטישן-בישראל-מחיר-החל-מ-870000-שקל — supports: version_or_trim, body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start
- Source 1 / source_index 1: ב.מ.וו X3 M - מחירון, מפרטים ואביזרים — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X3_M/ — supports: version_or_trim, body_type, fuel_type, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP X3 M Competition 510 hp if Israel source says X3 M Competition launched/sold. Current row 2019-2024 is plausible. If there is no local year_end source, keep year_end=null/current or mark year_end missing; do not force 2024 without source. Do not include base 480 hp X3 M unless Israel-specific source confirms sale.

#### V00 current row
```json
{
  "version_or_trim": "Competition",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "3.0L twin-turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 510,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2019,
  "year_end": 2024,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 151. BMW X3 M40i

Priority: MEDIUM-HIGH

### Current local sources
- Source 0 / source_index 1: ב.מ.וו X3 החדש 2018 בישראל - מחיר החל מ- 335,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-x3-%D7%94%D7%97%D7%93%D7%A9-2018-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-335000-%D7%A9%D7%A7%D7%9C — supports: version_or_trim, body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start
- Source 1 / source_index 2: ב.מ.וו X3 - מחירון, מפרטים, אמינות וחוות דעת | iCar — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_X3/ — supports: version_or_trim, body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_end

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP X3 M40i Exclusive 360 hp AWD 8AT from 2018; verify year_end=2024 against local iCar/source. Do not extend into 2025 because the new G45 performance replacement is `X3 M50 xDrive` 398 hp, not M40i. Add/split M50 only under correct model identity if desired.

#### V00 current row
```json
{
  "version_or_trim": "Exclusive",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "3.0L i6 turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 360,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2018,
  "year_end": 2024,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 152. BMW X3 xDrive20d

Priority: MEDIUM-HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו X3 יד שניה - מחירון רכב, חוות דעת, מפרט טכני | iCar — https://www.icar.co.il/bmw/bmw_x3/bmw_x3_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, version_or_trim
- Source 1 / source_index 1: מפרט טכני ב.מ.וו X3 2011-2014, דור שני (F25) - אוטו — https://www.auto.co.il/model/bmw-x3_g1069/2011 — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end
- Source 2 / source_index 2: מפרט טכני ב.מ.וו X3 2014-2017, דור שני - מתיחת פנים - אוטו — https://www.auto.co.il/model/bmw-x3_g1069/2014 — supports: horsepower_hp, engine_displacement_l, engine, year_start, year_end, fuel_type, transmission, drivetrain
- Source 3 / source_index 3: מחירון רכב ב.מ.וו X3 דור שלישי (G01) 2.0d xLine xDrive, 190 כ"ס, 2018-2022 — https://www.gear.co.il/%D7%9E%D7%97%D7%99%D7%A8%D7%95%D7%9F_%D7%A8%D7%9B%D7%91/%D7%91.%D7%9E.%D7%95%D7%95-X3/2018 — supports: horsepower_hp, engine_displacement_l, engine, fuel_type, transmission, drivetrain, body_type, version_or_trim

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP 2011-2014 Executive 184 hp diesel AWD 8AT. V01 KEEP 2014/2018-2022 xLine 190 hp diesel AWD 8AT, but verify the transition: 2014 facelift 190 hp and 2018 G01 xLine may need split by generation if source requires. Do not extend diesel rows beyond 2022 without local evidence.

#### V00 current row
```json
{
  "version_or_trim": "Executive",
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 184,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2011,
  "year_end": 2014,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

#### V01 current row
```json
{
  "version_or_trim": "xLine",
  "body_type": "SUV",
  "fuel_type": "diesel",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 190,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2014,
  "year_end": 2022,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

## 153. BMW X3 xDrive30e

Priority: MEDIUM-HIGH

### Current local sources
- Source 0 / source_index 0: ב.מ.וו X3 פלאג-אין - מחירון, מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X3_פלאג-אין/ — supports: body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end, version_or_trim
- Source 1 / source_index 1: מחירון רכב דגמי ב.מ.וו - BMW Israel — https://www.bmw.co.il/he/topics/offers-and-services/price-list.html — supports: fuel_type, horsepower_hp, drivetrain, year_end, version_or_trim

### Current variants and required Codex decisions

**Model-level decision:**
V00 KEEP/FIX: Israel source validates X3 xDrive30e as PHEV, 2.0 turbo + electric, 292 hp, 8AT, AWD, start 2020. Current clean row year_end=2024 is okay for outgoing generation if local source supports. Do not merge with the new 2025 G45 X3 30e xDrive, which is 299 hp and has different trims such as M-Launch/M-Sport Edition. Add the new row only under correct identity and sources.

#### V00 current row
```json
{
  "version_or_trim": "Executive",
  "body_type": "SUV",
  "fuel_type": "plug_in_hybrid",
  "engine": "2.0L turbo",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 292,
  "transmission": "8-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2020,
  "year_end": 2024,
  "support_level": "direct",
  "missing_grounded_fields": []
}
```
Required action: follow the model-level decision above for this exact row; preserve it only if the listed local/evidence sources ground all displayed fields. Rebuild source indexes and field_sources after any split/fix.

### Website/rebuild requirements
- Rebuild `available_values_for_website` so it contains only real visible values and no nulls or compound bad labels.
- Ensure `invalid_or_non_trim_labels` contains engine-size/powertrain descriptors that are not real trims.
- If any row is moved to review, make it non-blocking and preserve evidence/notes.

---

# RUN 2 verification commands

After applying RUN 2 edits, run:

```bash
pytest -q
python3 -m scripts.catalog_quality_scan
# plus the repo readiness rebuild command used by this project
```

Expected after RUN 2 only: no new active blockers, no duplicate technical variants, no invalid source references, no unknown support values. Review overlap/archive rows are allowed only if non-blocking.

---

# RUN 3 / 3 — Deep internet-backed validation for current blocked/review-only models

Date: 2026-06-16
Scope: current active review-only blockers from the uploaded repo state after RUN 1 + RUN 2 mapping.

Codex has no web access. Do not browse. Use this file plus local repo files only.

## Active blockers found in the uploaded repo state

`data/model_technical_catalog_il_readiness.json` reports:

```text
models_blocked = 6
duplicate_technical_variants = 0
invalid_source_references = 0
unknown_support_values = 0
ready_for_website_upload = false
review_only_blocked_entries = 6
```

The 6 active review-only blockers are:

```text
BMW 740i
BMW 760i
BMW 840i
BMW i3
BMW X1 sDrive18i
BMW X1 xDrive25e
```

The goal of RUN 3 is not to hide blockers. The goal is to repair all variants that can be grounded with the embedded evidence, and move only ungrounded leftovers into a non-blocking review/archive state that overlaps with a clean profile or is explicitly marked as rejected raw evidence. Do not leave empty active blocked profiles.

---

## Global RUN 3 rules

1. Israeli market only. Prefer importer/BMW Israel, iCar, Auto.co.il, Cartube Israel. Marketplace pages may be notes only unless no better source exists.
2. A review profile with `technical_variants_il=[]` caused by model output/JSON errors must not remain an active blocker if embedded evidence below can create a clean grounded profile.
3. If raw database values include years/trims that are not supported by the embedded Israeli evidence, do **not** create guessed rows. Put those unsupported raw clues into a note or non-blocking rejected/archive entry.
4. For every clean row, rebuild `sources`, `source_indexes`, `field_sources`, `available_values_for_website`, `invalid_or_non_trim_labels`, `missing_grounded_fields`, and profile confidence.
5. Never include `Base`, `Standard`, bare engine-size labels, empty strings, or null values in `available_values_for_website.version_or_trim`.
6. After repairs, no active review-only profile should remain for these six model keys.
7. `review_overlap_entries` may remain for rejected variants, but `review_only_blocked_entries` must be `0`.

---

# 1. BMW 740i

Priority: **critical**

Current repo state: review-only profile, empty `technical_variants_il`, error `Extra data: line 435 column 1`, raw years include 1992, 1994, 2001, 2005, 2008, 2015, 2022, 2026; raw trims include `Base`, `Luxury`, `M Expressive`; raw engines include `3.0L I6 Turbo`, `3.0L I6 Turbo Mild Hybrid`, `4.0L V8`, `4.0L V8 / 4.4L V8`.

## Web evidence collected externally

1. Cartube Israel, 28 Oct 2015, launch of 2015 BMW 7 Series in Israel:
   - BMW 740i Luxury, 326 hp, 890,000 NIS.
   - BMW 740i Long Luxury, 326 hp, 935,000 NIS.
   - This is direct Israeli launch evidence for 2015 740i / 740i Long Luxury.
   - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-7-החדשה-2015-בישראל-–-מחיר-החל-מ-890,000-שקל

2. BMW Israel 2015 Series 7 PDF, returned in search as `mifrat-bmw-7-28-10-2015.pdf`:
   - Shows BMW 740i and 740Li, sedan / long sedan body data.
   - Use as importer PDF support for body/trim/model identity.
   - URL: https://www.cartube.co.il/images/stories/bmw/bmw-7/mifrat-bmw-7-28-10-2015.pdf

3. iCar 2009 BMW 7 Series 3.0 740i version page:
   - 2009 3.0 740i, turbo petrol, 2,979 cc, 326 hp, automatic-tiptronic, 6 gears.
   - URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_ד11/version6190/

4. iCar 2008 news article for new 2009 Series 7:
   - 740i has a 3.0 inline-6 twin-turbo petrol engine, 326 hp, 45.8 kgm, automatic 6-speed, expected Israel arrival around October 2008.
   - Treat as model-launch background; use iCar version page for clean row fields.
   - URL: https://www.icar.co.il/חדשות_רכב/ב.מ.וו_סדרה_7_החדשה_2009/

5. Current official BMW Israel / iCar / Auto 2026 pages for Series 7 do **not** show 740i as an official current Israeli model. They show 750e xDrive and M760e xDrive PHEV / i7 rather than 740i. Therefore raw 2022/2026 `740i M Expressive` must not be kept as clean unless a direct local source already exists in the repo.
   - BMW Israel Series 7: https://www.bmw.co.il/he/All-Models/7-series/7-series-sedan/bmw-7-series-sedan.html
   - iCar current Series 7: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_חדש/
   - Auto Series 7 current: https://www.auto.co.il/cars/bmw/7-series/

## Required Codex edits

Create or repair a clean `BMW 740i` profile using only grounded rows:

### Variant 740i-2009
Decision: **KEEP / CREATE**

```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "3.0L inline-6 turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 326,
  "transmission": "6-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2009,
  "year_end": 2015,
  "support_level": "direct"
}
```

Use iCar 2009 version page as primary field source. Do not put null into website values.

### Variant 740i-Luxury-2015
Decision: **KEEP / CREATE**

```json
{
  "version_or_trim": "Luxury",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "3.0L inline-6 turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 326,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2015,
  "year_end": 2018,
  "support_level": "direct"
}
```

Use Cartube 2015 launch + BMW Israel PDF. If the local existing sources prove a different end year, use that. If no end-year source exists, set `year_end` to `null` and add `year_end` to `missing_grounded_fields`; do not guess beyond 2018.

### Variant 740i-Long-Luxury-2015
Decision: **KEEP / CREATE if schema supports long-wheelbase as trim/body distinction**

```json
{
  "version_or_trim": "Long Luxury",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "3.0L inline-6 turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 326,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2015,
  "year_end": 2018,
  "support_level": "direct"
}
```

If the schema has a canonical `Long Sedan` body type already, use it; otherwise keep `body_type="Sedan"` and `version_or_trim="Long Luxury"`.

### Raw rows not to create
Decision: **REVIEW / ARCHIVE ONLY**

- Do not create 2022/2026 `740i M Expressive` rows from raw values unless the repo contains direct Israeli importer/current catalog support. Current official pages show 750e/i7/M760e, not 740i.
- Do not create old 1992/1994/2001/2005 V8 rows unless local sources directly ground them. If unsupported, leave as rejected raw clues, not an active blocker.
- `Base` must be in `invalid_or_non_trim_labels`, never website values.

Expected result: BMW 740i moves from active review-only blocker into clean. Any unsupported raw clues become review overlap/archive notes and do not count as active blocked.

---

# 2. BMW 760i

Priority: **critical**

Current repo state: review-only profile, empty `technical_variants_il`, error `Gemini catalog client returned non-object JSON`, raw years include 2003, 2008, 2009, 2015; raw trims include `Base`, `Long Wheelbase`; raw engines include `6.0L V12`, `6.0L V12 Twin-Turbo`.

## Web evidence collected externally

1. Auto.co.il, 13 Apr 2009, `בקרוב באולמות התצוגה: ב.מ.וו 760i ו-760iL`:
   - 760i and 760iL, 6.0L V12 aluminium engine, twin turbo, direct injection, 544 hp.
   - RWD, new 8-speed automatic transmission.
   - 0-100 km/h 4.6 sec, limited 250 km/h.
   - Direct Israeli-market news that these versions were coming to showrooms.
   - URL: https://www.auto.co.il/articles/car-news/120576/

2. iCar 2012 BMW 7 Series 6.0 760Li Luxury:
   - 2009-2015 Series 7 generation page/version page.
   - Shows `6.0 760Li Luxury`, 544 hp, RWD, automatic, 5 seats, 4 doors.
   - URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_ד11/version11126/

3. iCar 2014 BMW 7 Series 6.0 760Li Luxury:
   - Confirms 544 hp for 2014 760Li Luxury.
   - URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_ד11/version12732/

4. Auto.co.il article `המכוניות החזקות בישראל`:
   - BMW 760 has V12 6.0, 544 hp, normal and long versions.
   - Use only as supporting context, not primary field source.
   - URL: https://www.auto.co.il/articles/car-news/112454/

## Required Codex edits

Repair BMW 760i into clean. If the repository schema allows model split, create distinct `BMW 760i` and `BMW 760Li` profiles. If it does not, keep one `BMW 760i` profile with long-wheelbase represented as `version_or_trim`.

### Variant 760i-2009
Decision: **KEEP / CREATE**

```json
{
  "version_or_trim": null,
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "6.0L v12 twin-turbo",
  "engine_displacement_l": 6.0,
  "horsepower_hp": 544,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2009,
  "year_end": 2015,
  "support_level": "direct"
}
```

Use Auto 2009 for engine/hp/transmission/drivetrain and iCar generation pages if available locally for end year.

### Variant 760Li-Luxury-2009
Decision: **KEEP / CREATE**

```json
{
  "version_or_trim": "Luxury",
  "body_type": "Sedan",
  "fuel_type": "petrol",
  "engine": "6.0L v12 twin-turbo",
  "engine_displacement_l": 6.0,
  "horsepower_hp": 544,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2009,
  "year_end": 2015,
  "support_level": "direct"
}
```

If using a separate model key `BMW 760Li`, put this row there instead and keep `BMW 760i` for the standard-wheelbase row. If not splitting, include a note that `Luxury` is grounded for the 760Li long version and long wheelbase is represented in trim/model identity.

### Raw rows not to create
Decision: **REVIEW / ARCHIVE ONLY**

- Do not create 2003/2008 `6.0L V12` rows unless local source pages directly ground that generation.
- `Base` is invalid/non-trim; never website trim.
- `Long Wheelbase` is a body/model identity clue, not a commercial trim by itself.

Expected result: BMW 760i no longer remains an empty active blocker.

---

# 3. BMW 840i

Priority: **critical**

Current repo state: review-only profile, empty `technical_variants_il`, error `Expecting ',' delimiter`, raw years include 2019 and 2026; raw trim `M-Superior`; raw body types `Convertible`, `Coupe`, `Gran Coupe`; raw engine `3.0L I6 Turbo`; drivetrain `RWD`.

## Web evidence collected externally

1. Cartube current 2026 price/spec page for BMW 8 Series 3.0 Coupe 840i M-Superior:
   - Coupe 840i M-Superior, 2,998 cc, 6 cylinders, turbo petrol, 333 hp, RWD, 8-speed automatic.
   - URL: https://www.cartube.co.il/מחירון-רכב-חדש/ב-מ-וו/ב-מ-וו-סדרה-8/5769-ב-מ-וו-סדרה-8-3-0-קופה-840i-m-superior

2. Cartube current 2026 price/spec page for BMW 8 Series 3.0 Convertible 840i M-Superior:
   - Convertible 840i M-Superior, 2,998 cc, 333 hp, RWD, 8-speed automatic.
   - URL: https://www.cartube.co.il/מחירון-רכב-חדש/ב-מ-וו/ב-מ-וו-סדרה-8/5770-ב-מ-וו-סדרה-8-3-0-קבריולט-840i-m-superior

3. Cartube BMW price list page:
   - Lists BMW 8 Series Gran Coupe 3.0 840i M-Superior, 8 Series Coupe 3.0 840i M-Superior, and 8 Series Cabriolet 3.0 840i M-Superior.
   - URL: https://www.cartube.co.il/מחירון-רכב-חדש/ב-מ-וו

4. BMW Israel 2022/2023 official PDFs:
   - Separate PDF/spec files exist for 840i Gran Coupé M-Superior, 840i Convertible M-Superior, and 840i Coupé M-Superior.
   - Treat these as importer evidence for body/model/trim separation, but keep the standard PDF disclaimer in mind.
   - Gran Coupe PDF URL: https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/technical-specifications---2022/June2022/33450-Mifrat-BMW-8-series-gran-Coupe-%28Ci%29-279B.pdf.asset.1657550825184.pdf
   - Coupe PDF URL: https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/technical-specifications---2022/july-2022/33451%20Mifrat%20BMW%208%20series%20Coup%C3%A9.pdf.asset.1657604590984.pdf
   - Convertible PDF URL: https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/technical-specifications-july-2022/33449_Mifrat_BMW_8_Series_Convertiable_LCI_279B.pdf.asset.1657551263408.pdf

5. Auto.co.il 2019 BMW 8 Series page:
   - Shows 840i Coupe / Convertible, 3.0 turbo, Elegant and M-Sport trims, discontinued; 340 hp.
   - URL: https://www.auto.co.il/cars/bmw/8-series/2019/

6. Auto.co.il 840i Gran Coupe road test:
   - 840i Gran Coupe, 3.0L turbo petrol, 340 hp, 51 kgm.
   - URL: https://www.auto.co.il/articles/test-drives/road-tests/134501/

## Required Codex edits

Create clean BMW 840i profile. Body types must remain distinct:

- `Coupe`
- `Convertible`
- `Gran Coupe`

Never normalize `Gran Coupe` into `Coupe` or `Sedan`.

### Current 2025/2026 M-Superior variants
Decision: **KEEP / CREATE**

Create these three rows:

```json
{
  "version_or_trim": "M-Superior",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.0L inline-6 turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 333,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2025,
  "year_end": 2026,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "M-Superior",
  "body_type": "Convertible",
  "fuel_type": "petrol",
  "engine": "3.0L inline-6 turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 333,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2025,
  "year_end": 2026,
  "support_level": "direct"
}
```

```json
{
  "version_or_trim": "M-Superior",
  "body_type": "Gran Coupe",
  "fuel_type": "petrol",
  "engine": "3.0L inline-6 turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 333,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2025,
  "year_end": 2026,
  "support_level": "direct"
}
```

Use Cartube 2026 specific pages for Coupe/Convertible; use Cartube BMW price list and BMW Israel Gran Coupe PDF for Gran Coupe.

### Historical 2019-2024 variants
Decision: **CREATE ONLY IF already local source support exists; otherwise review/archive**

Auto and BMW PDFs support older 840i Coupe / Convertible / Gran Coupe with 340 hp and trims such as Elegant/M-Sport/M-Superior. If local repo files already contain these sources, create rows such as:

```json
{
  "version_or_trim": "M-Sport",
  "body_type": "Coupe",
  "fuel_type": "petrol",
  "engine": "3.0L inline-6 turbo",
  "engine_displacement_l": 3.0,
  "horsepower_hp": 340,
  "transmission": "8-speed automatic",
  "drivetrain": "RWD",
  "year_start": 2019,
  "year_end": 2024,
  "support_level": "direct"
}
```

But do **not** duplicate by trim if the local source is not precise enough. A conservative clean profile with the 2025/2026 M-Superior rows is acceptable and better than guessed historical rows.

Expected result: BMW 840i moves into clean, with body split preserved and current M-Superior variants grounded.

---

# 4. BMW i3

Priority: **critical code/validation bug**

Current repo state: review profile is not empty; it already contains 3 grounded technical variants, but validation issues say:

```text
variant[0] is electric inside a petrol model profile
variant[2] is electric inside a petrol model profile
```

This is a validator/classification bug, not a data failure. BMW i3 is an electric model family that legitimately includes:

- pure electric i3, 170 hp;
- i3 REx / range extender, represented in this schema as plug-in hybrid or range-extender, 0.6L 2-cylinder extender + electric drive, 170 hp;
- i3s, pure electric, 184 hp.

## Web evidence collected externally

1. iCar BMW i3 2016-2020 page:
   - BMW i3 electric motor produces 170 hp and 25.5 kgm.
   - URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_i3/ב.מ.וו_i3_יד_שניה_ד10/

2. Cartube launch/current Israeli pages already in the repo profile:
   - BMW i3 in Israel, price from 249,000 NIS.
   - BMW i3 2018 facelift in Israel.
   - URLs already present in review profile:
     - https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-i3-בישראל-מחירון-החל-מ-249,000-שקל
     - https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-i3-החדשה-2018-בישראל-מחיר-החל-מ-249,000-שקל

3. Cartube 2018 facelift/source context:
   - i3 continues with 170 hp.
   - i3s has 184 hp.
   - URL: https://www.cartube.co.il/טכנולוגיה-וירוק/2018-ב-מ-וו-i3-החדשה-מתיחת-פנים

## Required Codex edits

Move BMW i3 from review to clean with its existing grounded variants, after fixing validation logic.

### Existing V0 — i3 electric 170 hp
Decision: **KEEP / MOVE TO CLEAN**

Keep the existing row:

```json
{
  "body_type": "Hatchback",
  "fuel_type": "electric",
  "engine": "electric",
  "engine_displacement_l": null,
  "horsepower_hp": 170,
  "transmission": "single_speed",
  "drivetrain": "RWD",
  "year_start": 2016,
  "year_end": 2022,
  "support_level": "direct"
}
```

`engine_displacement_l=null` is correct for pure electric; it may appear in `missing_grounded_fields` only if the schema requires all fields, but it should not block readiness.

### Existing V1 — i3 REx / range extender
Decision: **KEEP / MOVE TO CLEAN**

Keep the existing row, but normalize the naming if schema supports it:

```json
{
  "version_or_trim": "REx",
  "body_type": "Hatchback",
  "fuel_type": "plug_in_hybrid",
  "engine": "0.6L 2-cylinder range extender",
  "engine_displacement_l": 0.6,
  "horsepower_hp": 170,
  "transmission": "single_speed",
  "drivetrain": "RWD",
  "year_start": 2016,
  "year_end": 2018,
  "support_level": "direct"
}
```

If `version_or_trim` was null, add `REx` only if repo sources explicitly mention REx/range extender. If not, keep null and use `engine` to distinguish.

### Existing V2 — i3s electric 184 hp
Decision: **KEEP / MOVE TO CLEAN, but check model identity**

The current row is technically i3s. If the repo already has a separate clean `BMW i3s` profile, do not duplicate this row under `BMW i3`. Instead:

- Prefer moving this row into the existing `BMW i3s` clean profile.
- If no separate `BMW i3s` profile exists, keep it under BMW i3 with `version_or_trim="i3s"`.

Expected row if kept:

```json
{
  "version_or_trim": "i3s",
  "body_type": "Hatchback",
  "fuel_type": "electric",
  "engine": "electric",
  "engine_displacement_l": null,
  "horsepower_hp": 184,
  "transmission": "single_speed",
  "drivetrain": "RWD",
  "year_start": 2018,
  "year_end": 2022,
  "support_level": "direct"
}
```

## Required code fix

Find the validation rule that emits:

```text
is electric inside a petrol model profile
```

Fix it so BMW `i` models are classified as EV-capable model profiles. A profile should not be inferred as petrol just because one variant has `fuel_type=plug_in_hybrid` or a range extender engine.

Required behavior:

- `BMW i3` may contain `electric` rows and `plug_in_hybrid` / range-extender rows.
- `BMW i8` may contain plug-in hybrid rows.
- The warning should only trigger when a clearly petrol-only model profile unexpectedly contains an EV row, not when the model name starts with `i` or sources define it as electrified.

Expected result: BMW i3 no longer active blocked; electric rows are accepted cleanly.

---

# 5. BMW X1 sDrive18i

Priority: **critical**

Current repo state: review-only profile, empty `technical_variants_il`, error `Extra data: line 223 column 1`, raw years include 2010, 2015, 2022, 2026; raw trims include combined labels `Business, Luxury`, `Business, xLine, M-Sport, Exclusive, Sport`, `Style, M-Sport, M-Sport SE, xLine`; raw engines include `1.5L Turbo`, `2.0L`.

## Web evidence collected externally

1. Auto.co.il 2014 BMW X1 page:
   - For 2012+ first-gen X1, sDrive18i petrol 2.0 without turbo, 150 hp; RWD; trims Business and Luxury appear in the version list.
   - URL: https://www.auto.co.il/cars/bmw/x1/2014/

2. iCar 2010-2015 BMW X1 page:
   - Lists 2.0 petrol 18i Business / Luxury among the 2010-2015 generation.
   - URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X1/ב.מ.וו_X1_יד_שניה_ד10/

3. Cartube 2015 launch of new BMW X1 in Israel:
   - New X1 offered in Israel with 136 hp and 192 hp, FWD, from 242,000-277,000 NIS.
   - URL: https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-x1-החדש-2015-בישראל-–-מחיר-החל-מ-242,000-שקל

4. iCar 2016 X1 1.5 turbo-petrol 18i Sport 2x4 page:
   - 2016-2022 X1, 1.5 turbo petrol 18i, Sport, 2x4.
   - Version list includes 18i, Sport, xLine, Business, Exclusive, M-Sport depending on year.
   - URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X1/ב.מ.וו_X1_יד_שניה_ד11/version16402/

5. BMW Israel current X1 official page, price list 04/2026:
   - X1 sDrive18i current trims: M-Sport SE, M-Design, M-Shadow.
   - Listed with 136 hp, 23.45 kgm, 0-100 9.2 sec, 208 km/h.
   - URL: https://www.bmw.co.il/he/All-Models/x-series/x1/bmw-x1.html

6. BMW Israel technical page for X1:
   - Current technical data includes 1,499 cc 3-cylinder petrol, 136 hp, 7-speed automatic, FWD; also shows mild-hybrid variants elsewhere, so Codex must select the row corresponding to `X1 sDrive18i` and not accidentally copy 170 hp mild-hybrid from another model.
   - URL: https://www.bmw.co.il/he/All-Models/x-series/x1/bmw-x1-technical-data.html

7. BMW Israel 2024 X1 PDF:
   - X1 sDrive18i Style and M-Sport SE, 1,499 cc, 136 hp, 7-speed dual-clutch, FWD.
   - URL: https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/technical-specifications-2024/feb2024/240024%2037486%20BMW%20X1.pdf.asset.1708194585698.pdf

## Required Codex edits

Repair BMW X1 sDrive18i into clean. Do not leave combined trim strings.

### Variant X1-sDrive18i-2010-Business
Decision: **KEEP / CREATE if source supports exact trim**

```json
{
  "version_or_trim": "Business",
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "2.0L inline-4",
  "engine_displacement_l": 2.0,
  "horsepower_hp": 150,
  "transmission": "automatic",
  "drivetrain": "RWD",
  "year_start": 2010,
  "year_end": 2015,
  "support_level": "direct"
}
```

### Variant X1-sDrive18i-2010-Luxury
Decision: **KEEP / CREATE if source supports exact trim**

Same as above, `version_or_trim="Luxury"`.

### Variant X1-sDrive18i-2015-to-2022
Decision: **KEEP / CREATE split rows by real trim**

Use the following technical identity:

```json
{
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 136,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2015,
  "year_end": 2022,
  "support_level": "direct"
}
```

Split combined trim strings into separate clean rows only if sources support them:

- `Business`
- `xLine`
- `M-Sport`
- `Exclusive`
- `Sport`

Do not keep a single string like `Business, xLine, M-Sport, Exclusive, Sport`.

### Variant X1-sDrive18i-current-2023/2026
Decision: **KEEP / CREATE current rows, but do not use 170 hp**

Use the following current identity:

```json
{
  "body_type": "SUV",
  "fuel_type": "petrol",
  "engine": "1.5L turbo",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 136,
  "transmission": "7-speed dual_clutch",
  "drivetrain": "FWD",
  "year_start": 2023,
  "year_end": 2026,
  "support_level": "direct"
}
```

Create separate trim rows for:

- `Style` if supported by iCar/BMW PDF.
- `M-Sport SE` if supported by BMW Israel current page/PDF.
- `M-Design` if supported by BMW Israel 04/2026 current page.
- `M-Shadow` if supported by BMW Israel 04/2026 current page.

Do **not** use `xLine` as a current 2026 trim unless a current BMW Israel source supports it.

### Raw rows not to create
Decision: **REVIEW / ARCHIVE ONLY**

- Any 2026 X1 sDrive18i row with 170 hp is likely a cross-contamination from X2 sDrive20i or X1 mild-hybrid non-18i data. Do not keep 170 hp under X1 sDrive18i.
- Do not keep combined trim strings.

Expected result: BMW X1 sDrive18i moves into clean with split trims and no active blocker remains.

---

# 6. BMW X1 xDrive25e

Priority: **critical**

Current repo state: review-only profile, empty `technical_variants_il`, error `Gemini catalog client returned non-object JSON`, raw years 2020-2022; trims `M-Sport`, `X-Line`; engine `1.5L Turbo PHEV`; fuel `plug_in_hybrid`; drivetrain `AWD`.

## Web evidence collected externally

1. Cartube 26 Jul 2020, Israeli launch of BMW X1 xDrive25e PHEV:
   - X1 xDrive25e plug-in hybrid launched in Israel.
   - 220 hp, 57 km electric range, M-Sport trim, price 299,000 NIS.
   - URL: https://www.cartube.co.il/חדשות-רכב/חדש-בישראל-2020-ב-מ-וו-x1-xdrive25e-היברידי-פלאג-אין

2. Cartube tag page for BMW X1:
   - Repeats X1 xDrive25e PHEV with 220 hp and M-Sport.
   - URL: https://www.cartube.co.il/component/tags/tag/ב-מ-וו-x1

3. iCar 2021 BMW X1 1.5 PHEV 25e M-Sport 4x4 version page:
   - 1.5 plug-in hybrid 25e M-Sport 4x4.
   - Version list also includes 25e X-Line 4x4.
   - URL: https://www.icar.co.il/ב.מ.וו/ב.מ.וו_X1/ב.מ.וו_X1_יד_שניה_ד11/version24140/

4. iCar X1 plug-in test, 9 Sep 2020:
   - BMW X1 plug-in, 1.5L plug-in hybrid, automatic 6-speed, 220 hp, 299,000 NIS.
   - URL: https://www.icar.co.il/מבחני_רכב/ב.מ.וו_X1_פלאג_אין_-_מבחן_רכב/

5. BMW Israel 2021 X1 PDF:
   - Contains X1 xDrive25e / X1 sDrive18i M-Sport references and 2021 X1 details.
   - URL: https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/technical-specifications---mar2021/x1/210308%2028688%20Mifrat%20BMW%20X1%20182C%20%28Split%29%204-3-2021.pdf.asset.1615120198560.pdf

## Required Codex edits

Create clean BMW X1 xDrive25e profile with two trim rows if supported by local sources.

### Variant X1-xDrive25e-M-Sport
Decision: **KEEP / CREATE**

```json
{
  "version_or_trim": "M-Sport",
  "body_type": "SUV",
  "fuel_type": "plug_in_hybrid",
  "engine": "1.5L turbo plug-in hybrid",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 220,
  "transmission": "6-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2020,
  "year_end": 2022,
  "support_level": "direct"
}
```

Use Cartube launch + iCar test/version page.

### Variant X1-xDrive25e-X-Line
Decision: **KEEP / CREATE if iCar/local source supports exact trim**

```json
{
  "version_or_trim": "X-Line",
  "body_type": "SUV",
  "fuel_type": "plug_in_hybrid",
  "engine": "1.5L turbo plug-in hybrid",
  "engine_displacement_l": 1.5,
  "horsepower_hp": 220,
  "transmission": "6-speed automatic",
  "drivetrain": "AWD",
  "year_start": 2021,
  "year_end": 2022,
  "support_level": "direct"
}
```

If the repo source only lists X-Line in a version list but does not provide enough field-level support, create only M-Sport clean and move X-Line to review overlap, not active blocker.

### Do not create

- Do not extend xDrive25e after 2022 unless local evidence shows later Israeli marketing.
- Do not use 7-speed dual-clutch for xDrive25e; iCar/Cartube test indicates automatic 6-speed.
- Do not place xDrive25e under X1 sDrive18i or X2.

Expected result: BMW X1 xDrive25e moves into clean or non-blocking review-overlap with at least M-Sport clean if grounded. No active blocker remains.

---

# RUN 3 code/reporting fixes required

## 1. Empty review-only profiles must be repairable or non-blocking

If a review profile has `technical_variants_il=[]` only because the model provider returned malformed JSON/non-object JSON, but this task file gives enough evidence to create clean rows, repair it into clean.

If after all evidence a model still has no grounded clean row, convert the review entry into a non-blocking rejected/archive record with explicit `active_blocker=false` and a reason. Do not leave empty active blockers.

## 2. BMW i3 electrified profile validation

Fix the validator rule that misclassifies BMW i3 as a petrol-only model profile. BMW i3 can contain electric and range-extender/PHEV rows. The validation issue `is electric inside a petrol model profile` must not trigger for BMW i3.

## 3. Gran Coupe canonical body type must remain valid

Ensure earlier RUN 1/RUN 2 fixes remain intact:

- `Gran Coupe` is canonical.
- `Gran Coupe` must not normalize to `Coupe` or `Sedan`.
- A Gran Coupe row must not be counted as duplicate of a Coupe row.

## 4. Review overlap vs active blocked

Keep the fixed semantics:

- `active_blocked_count` = readiness active blocked count / review-only keys, not raw review entries.
- `review_overlap_entries` may be nonzero.
- `review_only_blocked_entries` must be zero after this task.

---

# RUN 3 final verification

After applying RUN 3, rebuild:

```text
data/model_technical_catalog_il.json
data/model_technical_catalog_il_review.json
data/model_technical_catalog_il_readiness.json
data/model_technical_catalog_il_quality_scan.json
```

Run:

```bash
pytest -q
python3 -m scripts.catalog_quality_scan
```

Also run the repository readiness rebuild command used by this project.

Final required state:

```text
models_blocked = 0
review_only_blocked_entries = 0
duplicate_technical_variants = 0
invalid_source_references = 0
unknown_support_values = 0
ready_for_website_upload = true
```

If `review_overlap_entries` remains > 0, that is acceptable only if all such entries overlap with clean model keys and do not block the next source cursor.

Report exact files changed and summarize each repaired blocked model.
