# FINAL UNIFIED CODEX PROMPT — Deep web-backed validation for all 53 requested models

Scope: 50 latest clean models split into Run 1 and Run 2, plus 3 blocked/review models from Run 3.
Date: 2026-06-16.

Codex has no web access. Do not browse. Use only the evidence embedded below and the local repository files.

Global acceptance standard:
1. Preserve only Israeli-market variants.
2. Fix exact body types, engine identities, horsepower, drivetrain, years, and trims.
3. Remove or move to review any row that remains ungrounded after applying the embedded evidence.
4. Rebuild all source mappings and website value lists after editing.
5. Run the local validation/quality tests and report exact changed files.

Execution order:
A. Apply RUN 1 corrections to the first 25 clean models.
B. Apply RUN 2 corrections to the last 25 clean models.
C. Apply RUN 3 repair/rejection decisions for the 3 blocked models.
D. Only then produce the final clean/review JSON outputs and quality scan.

---

# RUN 1 / 3 — Deep web-backed correction prompt for Codex

Scope: first 25 models from the last 50 clean catalog entries, indices 67–91.
Input catalog: `data/model_technical_catalog_il.json` from uploaded zip.
Date: 2026-06-16.

## Mission for Codex
You do **not** have web access. All internet research notes and URLs collected by ChatGPT are embedded here. Use them as offline evidence and update the local JSON files only. Treat the clean catalog as suspicious until every field is grounded.

## Hard rules
1. Israeli market only. Do not keep a row in clean if the only support is a global reveal, European spec page, generic model knowledge, or an Israeli article that says only “expected to arrive”.
2. Validate every retained row field-by-field: make, model/canonical_model, version_or_trim, body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end.
3. A model-level engine name such as `SQ8`, `320i`, `128ti` may have `version_or_trim=null`, but null must never appear in `available_values_for_website` and must not be marked missing if there is no separate marketed trim.
4. Split by real Israeli marketed model/body when needed: Gran Coupe, Active Tourer, GT, Convertible/GTC must not pollute a generic coupe/sedan model unless the catalog intentionally treats them as one canonical family and the website can distinguish body_type clearly.
5. If a field cannot be backed by the URLs and evidence below, either correct it, set it null and list it under `missing_grounded_fields`, or move the row/model to `model_technical_catalog_il_review.json`.
6. After every edit rebuild `sources`, `source_indexes`, `field_sources`, `available_values_for_website`, `invalid_or_non_trim_labels`, and run the catalog quality scan/tests.

## Exact run list
67. Audi SQ7, 68. Audi SQ8, 69. Audi TT, 70. Bentley Bentayga, 71. Bentley Continental GT, 72. Bentley Flying Spur, 73. BMW 116i, 74. BMW 118d, 75. BMW 118i, 76. BMW 120i, 77. BMW 125i, 78. BMW 128ti, 79. BMW 218i, 80. BMW 218i Gran Coupe, 81. BMW 220i, 82. BMW 225xe (Active Tourer PHEV), 83. BMW 230e (Active Tourer PHEV), 84. BMW 316i, 85. BMW 318d, 86. BMW 318i, 87. BMW 320e, 88. BMW 320i, 89. BMW 323i, 90. BMW 325i, 91. BMW 328i

---

## 67. Audi SQ7
Priority: **גבוה**

Verdict: **לתקן לפני השארה בנקי.**

### Current catalog variants
- V00: version_or_trim=None; body_type='SUV'; fuel_type='diesel'; engine='4.0L v8 turbo'; engine_displacement_l=4.0; horsepower_hp=435; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2016; year_end=2020; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='4.0L v8 turbo'; engine_displacement_l=4.0; horsepower_hp=507; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2020; year_end=2024; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube ישראל 07.02.2017: SQ7 TDI הושק בישראל ע״י צ׳מפיון עם 4.0 V8 TDI, 435 כ״ס, מחיר 844,900/845,000 ₪.
- 4x4 ישראל 31.07.2017: מבחן/נתונים ל-SQ7 דיזל 4.0, V8, 3956 סמ״ק, 435 כ״ס, אוטומטית 8 הילוכים, קוואטרו/4x4.
- Cartube 15.07.2020 הוא מקור אירופי ל-SQ7/SQ8 בנזין 507 כ״ס; אין להשתמש בו לבדו לשנת התחלה ישראלית.
- חיפוש מודעות יד2/סנטרו מראה SQ7 Premium Plus בנזין 4.0 507 כ״ס כ-2021, אך מודעה אינה מקור קטלוגי חזק.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/בריון-אודי-sq7-tdi-בישראל-מחיר-החל-מ-855-שקל
- https://www.4x4.co.il/article/11379
- https://www.cartube.co.il/חדשות-רכב/אודי-מציגה-2011-sq8-sq7-עם-מנוע-בנזין-v8-tfsi

Catalog source URLs already present in JSON:
- [0] Cartube IL: אאודי SQ7 בישראל - מחיר החל מ- 845,000 שקל — https://www.cartube.co.il/חדשות-רכב/אאודי-sq7-בישראל-מחיר-החל-מ-845000-שקל — supports=['fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] Cartube IL: בנזין במקום דיזל: 2021 אאודי SQ7 ו- SQ8 החדשים בישראל — https://www.cartube.co.il/חדשות-רכב/בנזין-במקום-דיזל-2021-אאודי-sq7-ו-sq8-החדשים-בישראל — supports=['fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [2] iCar IL: אאודי SQ7 - מחירון רכב, מפרט טכני — https://www.icar.co.il/audi/audi_sq7/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00 דיזל: לשנות year_start מ-2016 ל-2017 אם אין מקור ישראלי ישיר לשיווק ב-2016. המקור הישראלי החזק הוא פברואר/יולי 2017.
- V00 דיזל: להשאיר 4.0L V8 diesel turbo, 435 hp, 8AT, AWD רק עם source_indexes של Cartube/4x4/iCar שמציינים זאת.
- V01 בנזין 507: לא להשאיר year_start=2020 על בסיס מקור אירופי. אם source 1 בקטלוג אכן כתבת ישראל בשם ״בנזין במקום דיזל: 2021 ... בישראל״ — year_start צריך להיות 2021; אם לא, להעביר את השורה ל-review.
- V01 year_end=2024 דורש מקור ישראלי שמראה שה-SQ7 בנזין עדיין נמכר/מופיע עד 2024. אם אין, להוריד year_end ל-null עם missing_grounded_fields=[year_end] או להעביר ל-review.
- version_or_trim יכול להישאר null כי SQ7 הוא model-level performance variant; לא להכניס null ל-available_values_for_website.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 68. Audi SQ8
Priority: **בינוני-גבוה**

Verdict: **כנראה לשמור, אבל לתקן סימון version_or_trim/missing.**

### Current catalog variants
- V00: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='4.0L twin-turbo v8'; engine_displacement_l=4.0; horsepower_hp=507; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2020; year_end=2026; support_level='direct'; missing_grounded_fields=['version_or_trim']

### Web evidence already researched by ChatGPT
- Cartube 17.06.2024: Q8 המחודש בישראל כולל SQ8 עם 507 כ״ס.
- מקור Audi Israel הרשמי בקטלוג אמור לשמש לעיגון current/year_end עד 2026 אם הדף פעיל ומציג SQ8.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/אודי-q8-החדש-2024-נחת-בישראל-מחיר-720000-שקל
- https://www.audi.co.il/models/q8/sq8/

Catalog source URLs already present in JSON:
- [1] Cartube.co.il: אאודי SQ8 ו- RSQ8 בישראל - מחיר החל מ- 847,000 שקל — https://www.cartube.co.il/חדשות-רכב/אאודי-sq8-ו-rsq8-בישראל-מחיר-החל-מ-847000-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [2] Audi Israel: Audi SQ8 | צ'מפיון מוטורס — https://www.audi.co.il/models/q8/sq8/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_end']
- [3] iCar: אאודי SQ8 - מחירון, קטלוג רכב, מבחני דרכים ועוד — https://www.icar.co.il/אאודי/אאודי_SQ8/ — supports=['body_type', 'fuel_type', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [4] Cartube: אודי Q8 | מחירון ומפרט טכני — https://www.cartube.co.il/מחירון-רכב-חדש/אודי/אודי-q8 — supports=['SQ8', 'horsepower_hp', 'year_end', 'fuel_type']

### Required specific Codex edits
- לא לסמן version_or_trim כחסר אם המודל עצמו הוא SQ8 ואין trim שיווקי נפרד. להשאיר version_or_trim=null אבל להסיר missing_grounded_fields=[version_or_trim].
- להשאיר 4.0 V8 twin-turbo petrol, 507 hp, 8AT, AWD רק אם מקור ישראלי/יבואן תומך.
- year_start=2020 תקין רק אם כתבת השקה ישראלית של SQ8 מ-2020 קיימת; אחרת year_start צריך להיות שנת מקור ישראלי ראשון.
- year_end=2026 תקין רק על בסיס Audi Israel/Cartube price-list current; אחרת לא לנחש.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 69. Audi TT
Priority: **גבוה מאוד**

Verdict: **חובה לתקן שורות 245 כ״ס לפני ניקוי.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='1.8L turbo'; engine_displacement_l=1.8; horsepower_hp=180; transmission='manual'; drivetrain='FWD'; year_start=1999; year_end=2006; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='1.8L turbo'; engine_displacement_l=1.8; horsepower_hp=180; transmission='automatic'; drivetrain='FWD'; year_start=1999; year_end=2006; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='1.8L turbo'; engine_displacement_l=1.8; horsepower_hp=225; transmission='manual'; drivetrain='AWD'; year_start=1999; year_end=2006; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=200; transmission='dual_clutch'; drivetrain='FWD'; year_start=2007; year_end=2010; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=211; transmission='dual_clutch'; drivetrain='FWD'; year_start=2010; year_end=2014; support_level='direct'; missing_grounded_fields=[]
- V05: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=230; transmission='dual_clutch'; drivetrain='FWD'; year_start=2015; year_end=2018; support_level='direct'; missing_grounded_fields=[]
- V06: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=245; transmission='dual_clutch'; drivetrain='FWD'; year_start=2019; year_end=2023; support_level='direct'; missing_grounded_fields=[]
- V07: version_or_trim=None; body_type='Roadster'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=230; transmission='dual_clutch'; drivetrain='FWD'; year_start=2015; year_end=2018; support_level='direct'; missing_grounded_fields=[]
- V08: version_or_trim=None; body_type='Roadster'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=245; transmission='dual_clutch'; drivetrain='FWD'; year_start=2019; year_end=2023; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Carzone תוצאת 2021: Audi TTS Coupe 245 כ״ס, 1984 סמ״ק, הנעה 4X4. זה סותר את שורות TT 245 FWD בקובץ.
- מקורות Auto/iCar/Carzone צריכים להיבדק ברמת גרסה: TT רגיל מול TTS, Coupe מול Roadster, FWD מול quattro.

### URLs / offline evidence package for Codex
- https://www.carzone.co.il/Audi/TT/TTS-Coupe/2021/
- https://www.auto.co.il/model/audi-tt
- https://www.icar.co.il/audi/tt

Catalog source URLs already present in JSON:
- [109] Auto.co.il: אאודי TT - מחירון, מפרטים, אמינות - אוטו — https://www.auto.co.il/model/audi-tt — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [110] Carzone: אאודי TT (2015-2023) - מפרט טכני, מחירון, וחוות דעת - קארזון — https://www.carzone.co.il/audi/tt/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [111] iCar: אאודי TT דורות - iCar — https://www.icar.co.il/audi/tt — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V06 ו-V08: אם מקור 245 כ״ס מציין TTS או 4X4 — אסור להשאיר כ-TT רגיל FWD. להעביר למודל TTS/TT S עם drivetrain=AWD או להעביר ל-review.
- כל שורות TT עם version_or_trim=null מותרות רק אם המקור מציג את הגרסה רק כ-TT לפי מנוע/מרכב; אחרת למלא 40 TFSI / 45 TFSI / TTS / Roadster לפי מקור.
- לא לערבב Coupe ו-Roadster תחת אותו ערך trim; body_type מספיק, אבל source_indexes חייבים להיות ספציפיים לכל מרכב.
- להשאיר older rows 1.8/2.0 רק אם Auto/iCar מציגים את השנים וההנעה לכל תת-דור.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 70. Bentley Bentayga
Priority: **גבוה**

Verdict: **לתקן כפילויות ו-null trims.**

### Current catalog variants
- V00: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='4.0L turbo v8'; engine_displacement_l=4; horsepower_hp=550; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2019; year_end=2026; support_level='indirect'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim='Mulliner'; body_type='SUV'; fuel_type='petrol'; engine='4.0L turbo v8'; engine_displacement_l=4; horsepower_hp=550; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2019; year_end=2022; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='SUV'; fuel_type='petrol'; engine='6.0L turbo w12'; engine_displacement_l=6; horsepower_hp=608; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2019; year_end=2022; support_level='indirect'; missing_grounded_fields=['version_or_trim']
- V03: version_or_trim='Mulliner'; body_type='SUV'; fuel_type='petrol'; engine='6.0L turbo w12'; engine_displacement_l=6; horsepower_hp=608; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2019; year_end=2022; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim='S'; body_type='SUV'; fuel_type='petrol'; engine='4.0L turbo v8'; engine_displacement_l=4; horsepower_hp=550; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2023; year_end=2026; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- iCar 2026 Bentayga 4.0 S: 3996 סמ״ק, 8 בוכנות, 550 כ״ס.
- אין מקור ישראלי חזק שנמצא כאן ל-PHEV/EWB בתוך הפרופיל הנוכחי; לא להוסיף אותם.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/בנטלי/בנטלי_בנטאיגה/בנטלי_בנטאיגה_חדש/version24562/
- https://www.cartube.co.il/מחירון-רכב-חדש/בנטלי/בנטלי-בנטיאגה/5714-בנטלי-בנטאיגה-4-0-s

Catalog source URLs already present in JSON:
- [0] iCar: בנטלי בנטאיגה 2019-2025 - iCar model range page — https://www.icar.co.il/%D7%91%D7%A0%D7%98%D7%9C%D7%99/%D7%91%D7%A0%D7%98%D7%9C%D7%99_%D7%91%D7%A0%D7%98%D7%90%D7%99%D7%92%D7%94/%D7%91%D7%A0%D7%98%D7%9C%D7%99_%D7%91%D7%A0%D7%98%D7%90%D7%99%D7%92%D7%94_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9310/ — supports=['body_type', 'year_start', 'year_end', 'version_or_trim']
- [1] iCar: בנטלי בנטאיגה 2019 4.0 - iCar version page — https://www.icar.co.il/%D7%91%D7%A0%D7%98%D7%9C%D7%99/%D7%91%D7%A0%D7%98%D7%9C%D7%99_%D7%91%D7%A0%D7%98%D7%90%D7%99%D7%92%D7%94/%D7%91%D7%A0%D7%98%D7%9C%D7%99_%D7%91%D7%A0%D7%98%D7%90%D7%99%D7%92%D7%94_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9310/version20211/ — supports=['fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [2] iCar: בנטלי בנטאיגה 2019 6.0 - iCar version page — https://www.icar.co.il/%D7%91%D7%A0%D7%98%D7%9C%D7%99/%D7%91%D7%A0%D7%98%D7%9C%D7%99_%D7%91%D7%A0%D7%98%D7%90%D7%99%D7%92%D7%94/%D7%91%D7%A0%D7%98%D7%9C%D7%99_%D7%91%D7%A0%D7%98%D7%90%D7%99%D7%92%D7%94_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9310/version20213/ — supports=['fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [3] iCar: בנטלי בנטאיגה 2022 4.0 Mulliner - iCar version page — https://www.icar.co.il/%D7%91%D7%A0%D7%98%D7%9C%D7%99/%D7%91%D7%A0%D7%98%D7%9C%D7%99_%D7%91%D7%A0%D7%98%D7%90%D7%99%D7%92%D7%94/%D7%91%D7%A0%D7%98%D7%9C%D7%99_%D7%91%D7%A0%D7%98%D7%90%D7%99%D7%92%D7%94_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9310/version25368/ — supports=['version_or_trim', 'engine_displacement_l', 'horsepower_hp', 'year_start', 'year_end']
- [4] iCar: בנטלי בנטאיגה 2025 4.0 S - iCar version page — https://www.icar.co.il/%D7%91%D7%A0%D7%98%D7%9C%D7%99/%D7%91%D7%A0%D7%98%D7%9C%D7%99_%D7%91%D7%A0%D7%98%D7%90%D7%99%D7%92%D7%94/%D7%91%D7%A0%D7%98%D7%9C%D7%99_%D7%91%D7%A0%D7%98%D7%90%D7%99%D7%92%D7%94_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9310/version30901/ — supports=['version_or_trim', 'engine_displacement_l', 'horsepower_hp', 'year_start', 'year_end']
- [5] iCar: בנטלי בנטאיגה 2026 רכב חדש 4.0 — https://www.icar.co.il/בנטלי/בנטלי_בנטאיגה/בנטלי_בנטאיגה_חדש/version18341/ — supports=['4.0', 'year_end', 'body_type', 'drivetrain', 'transmission']
- [6] Cartube: בנטלי בנטאיגה 4.0 S 2026 | מפרט טכני — https://www.cartube.co.il/מחירון-רכב-חדש/בנטלי/בנטלי-בנטיאגה/5714-בנטלי-בנטאיגה-4-0-s — supports=['4.0 S', 'year_end', 'body_type']

### Required specific Codex edits
- V04 S 2023-2026 נראה השורה הכי חזקה; לעגן ל-iCar/Cartube 2026 4.0 S.
- V00 null 4.0 2019-2026 רחבה מדי וכפולה מול S/Mulliner. לפצל לפי שנים/גרסאות מקוריות או להעביר ל-review. אם המקור אומר ״4.0״ כגרסה, version_or_trim צריך להיות "4.0" ולא null.
- V02 null 6.0 W12: אם iCar מציג גרסה בשם 6.0, version_or_trim="6.0"; אם לא — review.
- Mulliner 4.0/W12: להשאיר רק לשנות דגם שמופיעות במקור; לא למתוח עד 2022 אם המקור רק 2022 יחיד.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 71. Bentley Continental GT
Priority: **גבוה**

Verdict: **לתקן 2025+ PHEV ולנעול W12/V8.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='6.0L w12 twin-turbo'; engine_displacement_l=6.0; horsepower_hp=635; transmission='8-speed dual_clutch'; drivetrain='AWD'; year_start=2018; year_end=2024; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='6.0L w12 twin-turbo'; engine_displacement_l=6.0; horsepower_hp=635; transmission='8-speed dual_clutch'; drivetrain='AWD'; year_start=2019; year_end=2024; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V02: version_or_trim='V8'; body_type='Coupe'; fuel_type='petrol'; engine='4.0L v8 twin-turbo'; engine_displacement_l=4.0; horsepower_hp=550; transmission='8-speed dual_clutch'; drivetrain='AWD'; year_start=2020; year_end=2024; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim='V8'; body_type='Convertible'; fuel_type='petrol'; engine='4.0L v8 twin-turbo'; engine_displacement_l=4.0; horsepower_hp=550; transmission='8-speed dual_clutch'; drivetrain='AWD'; year_start=2020; year_end=2024; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim='Speed'; body_type='Coupe'; fuel_type='plug_in_hybrid'; engine='4.0L v8 twin-turbo'; engine_displacement_l=4.0; horsepower_hp=782; transmission='8-speed dual_clutch'; drivetrain='AWD'; year_start=2024; year_end=2025; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 2018: דור חדש Continental GT בישראל עם W12 6.0 ו-635 כ״ס.
- Cartube 2020: V8 החדשה בישראל עם 4.0 V8 ו-550 כ״ס.
- Cartube 25.06.2024/10.04.2025: Speed PHEV 782 וגרסאות בסיס PHEV 680 הן חשיפה/מידע גלובלי; לא בהכרח יבוא ישראלי.
- Cartube 10.04.2025 מדגיש: בסיס PHEV 680 כ״ס, Speed 782 כ״ס — לא לערבב.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/הדור-החדש-של-בנטלי-קונטיננטל-gt-בישראל-מחיר
- https://www.cartube.co.il/חדשות-רכב/בישראל-בנטלי-קונטיננטל-v8-החדשה
- https://www.cartube.co.il/חדשות-רכב/בנטלי-קונטיננטל-gt-ספיד-החדשה-נחשפת-עם-הנעה-היברידית
- https://www.cartube.co.il/חדשות-רכב/בנטלי-משיקה-גרסאות-בסיס-היברידיות-חדשות-לקונטיננטל-gt

Catalog source URLs already present in JSON:
- [0] Cartube: הדור החדש של בנטלי קונטיננטל GT בישראל – החל מ- 1.77 מיליון שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%94%D7%93%D7%95%D7%A8-%D7%94%D7%97%D7%93%D7%A9-%D7%A9%D7%9C-%D7%91%D7%A0%D7%98%D7%9C%D7%99-%D7%A7%D7%95%D7%A0%D7%98%D7%99%D7%A0%D7%A0%D7%98%D7%9C-gt-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%94%D7%97%D7%9C-%D7%9E-177-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C — supports=['year_start', 'body_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'fuel_type']
- [1] Auto.co.il: בנטלי קונטיננטל GT חדשה, מחיר, מפרט - אוטו — https://www.auto.co.il/model/bentley-continental-gt_g119 — supports=['year_end', 'body_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'fuel_type']
- [2] Cartube: בנטלי קונטיננטל GT פתוחה בישראל - מחיר החל מ-2 מיליון שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91%D7%A0%D7%98%D7%9C%D7%99-%D7%A7%D7%95%D7%A0%D7%98%D7%99%D7%A0%D7%A0%D7%98%D7%9C-gt-%D7%A4%D7%AA%D7%95%D7%97%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-2-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C — supports=['year_start', 'year_end', 'body_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'fuel_type']
- [3] Cartube: בישראל: בנטלי קונטיננטל V8 החדשה במחיר של 1.56 מיליון שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%91%D7%A0%D7%98%D7%9C%D7%99-%D7%A7%D7%95%D7%A0%D7%98%D7%99%D7%A0%D7%A0%D7%98%D7%9C-v8-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%9E%D7%97%D7%99%D7%A8-%D7%A9%D7%9C-1-56-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C — supports=['year_start', 'year_end', 'version_or_trim', 'body_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'fuel_type']
- [4] Cartube: בנטלי קונטיננטל 2025 החדשה נחשפת (דור 4) עם פלאג-אין V8 בהספק של 782 כ"ס — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91%D7%A0%D7%98%D7%9C%D7%99-%D7%A7%D7%95%D7%A0%D7%98%D7%99%D7%A0%D7%A0%D7%98%D7%9C-gt-speed-%D7%94%D7%97%D7%93%D7%A9%D7%94-2025-%D7%A0%D7%97%D7%A9%D7%A4%D7%AA-%D7%93%D7%95%D7%A8-4 — supports=['year_start', 'year_end', 'version_or_trim', 'body_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'fuel_type']

### Required specific Codex edits
- V04 Speed PHEV 782: להעביר ל-review אלא אם יש מקור ישראלי מפורש לשיווק/מחיר/יבוא בישראל. חשיפה גלובלית אינה clean.
- V00/V01 W12 null: לשקול version_or_trim="W12" או "GT" לפי מקור; לא להשאיר missing version אם המקור נותן W12.
- V2/V3 V8: להשאיר 2020-2024 רק אם כתבת ישראל/מחירון תומכים; לא להאריך ל-2025 ללא ישראל.
- להבדיל בין Coupe ו-Convertible/GTC בשם/מרכב; Convertible עדיף version_or_trim="GTC" או body_type Convertible עם מקור GTC.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 72. Bentley Flying Spur
Priority: **גבוה**

Verdict: **לשמור דורות ישנים; לבדוק/לחסום 2025 PHEV.**

### Current catalog variants
- V00: version_or_trim='V8'; body_type='Sedan'; fuel_type='petrol'; engine='4.0L v8 twin-turbo'; engine_displacement_l=4.0; horsepower_hp=507; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2014; year_end=2019; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim='W12'; body_type='Sedan'; fuel_type='petrol'; engine='6.0L w12 twin-turbo'; engine_displacement_l=6.0; horsepower_hp=625; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2013; year_end=2019; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim='W12'; body_type='Sedan'; fuel_type='petrol'; engine='6.0L w12 twin-turbo'; engine_displacement_l=6.0; horsepower_hp=635; transmission='8-speed dual_clutch'; drivetrain='AWD'; year_start=2020; year_end=2024; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim='V8'; body_type='Sedan'; fuel_type='petrol'; engine='4.0L v8 twin-turbo'; engine_displacement_l=4.0; horsepower_hp=550; transmission='8-speed dual_clutch'; drivetrain='AWD'; year_start=2021; year_end=2024; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim='Speed'; body_type='Sedan'; fuel_type='plug_in_hybrid'; engine='4.0L v8 twin-turbo phev'; engine_displacement_l=4.0; horsepower_hp=782; transmission='8-speed dual_clutch'; drivetrain='AWD'; year_start=2025; year_end=2026; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 2020: Flying Spur החדשה בישראל.
- Cartube 2021: Flying Spur V8 בישראל.
- Cartube 10.09.2024: Flying Spur Speed החדשה PHEV 782 כ״ס; מצוין ״מתי בישראל? ברבעון הראשון של 2025״ — זו לא בהכרח תחילת שיווק בפועל.
- iCar 11.09.2024: חשיפה לגרסה היברידית-נטענת, 4.0 V8 + חשמלי, 782 כ״ס.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/בנטלי-פליינג-ספור-החדשה-2020-בישראל
- https://www.cartube.co.il/חדשות-רכב/בנטלי-פליינג-ספור-v8-נוחתת-בישראל
- https://www.cartube.co.il/חדשות-רכב/בנטלי-קונטיננטל-פליינג-ספר-ספיד-החדשה-2025-נחשפת
- https://www.icar.co.il/news/b1x11p7c3a/

Catalog source URLs already present in JSON:
- [1] iCar: בנטלי פליינג ספור (2013-2019) - מפרט טכני — https://www.icar.co.il/%D7%91%D7%A0%D7%98%D7%9C%D7%99/%D7%91%D7%A0%D7%98%D7%9C%D7%99_%D7%A4%D7%9C%D7%99%D7%99%D7%A0%D7%92_%D7%A1%D7%A4%D7%95%D7%A8/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Cartube: בנטלי פליינג ספור החדשה 2020 בישראל — https://www.cartube.co.il/חדשות-רכב/בנטלי-פליינג-ספור-החדשה-2020-בישראל-מחיר-החל-מ-185-מיליון-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [3] Cartube: בנטלי פליינג ספור V8 נוחתת בישראל — https://www.cartube.co.il/חדשות-רכב/בנטלי-פליינג-ספור-v8-נוחתת-בישראל-מחיר-החל-מ-1-499-מיליון-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [4] Cartube: עם 782 כ"ס ופלאג-אין: 2025 בנטלי פליינג ספור החדשה — https://www.cartube.co.il/חדשות-רכב/עם-782-כ-ס-ופלאג-אין-2025-בנטלי-פליינג-ספור-החדשה — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']

### Required specific Codex edits
- V04 Speed PHEV 2025-2026: לא clean direct בלי מקור ישראלי אחרי תחילת שיווק/מחירון. אם רק ״צפויה בישראל״ — support_level=indirect/review.
- V00/V01 2013-2019: לעגן ל-iCar מפרט דור ישן; V8 507 ו-W12 625 נשמעים תקינים.
- V02/V03 2020-2024: לעגן ל-Cartube ישראל; W12 635, V8 550. לא להאריך אחרי החלפת W12 ללא מקור.
- לבדוק שהשם Flying Spur לא נכתב בקובץ כ״קונטיננטל פליינג ספר״ אם canonical_model צריך להיות Flying Spur בלבד.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 73. BMW 116i
Priority: **קריטי**

Verdict: **להוציא מהמודל את שורות 2024/2025 החדשות.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=115; transmission='6-speed manual'; drivetrain='RWD'; year_start=2004; year_end=2011; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=115; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2004; year_end=2011; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim='Business'; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=136; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2015; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim='Sport'; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=136; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2015; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim='Luxury'; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=136; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2015; support_level='direct'; missing_grounded_fields=[]
- V05: version_or_trim='M-Drive'; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=136; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2015; support_level='direct'; missing_grounded_fields=[]
- V06: version_or_trim='Essence'; body_type='Hatchback'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=109; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2024; year_end=2025; support_level='direct'; missing_grounded_fields=[]
- V07: version_or_trim='M Design'; body_type='Hatchback'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=109; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2024; year_end=2025; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 01.01.2025: דגם הבסיס החדש הוא BMW 116, לא 116i, עם 1.5 טורבו 122 כ״ס, Essence ו-M-Design.
- Cartube price-list 2026: סדרה 1 116 Essence / 116 M-Design, 122 כ״ס.
- Cartube 2024/2025: סדרה 1 החדשה משווקת בישראל כ-120 ו-M135, ואחר כך 116 — לא 120i/116i.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/חדש-בישראל-2025-ב-מ-וו-סדרה-1-דגם-116
- https://www.cartube.co.il/מחירון-רכב-חדש/ב-מ-וו/ב-מ-וו-סדרה-1
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-1-החדשה-2025-נחתה-בישראל-מחיר-249900-שקל

Catalog source URLs already present in JSON:
- [1] Auto.co.il: ב.מ.וו סדרה 1 (2004-2011) - מפרט טכני וגרסאות — https://www.auto.co.il/model/bmw-1-series_g2 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] iCar: מחירון ומפרט רכב ב.מ.וו סדרה 1 2011 - 2015 116i — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_1/ב.מ.וו_סדרה_1_יד_שניה_ד2/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [3] Cartube.co.il: ב.מ.וו 116i החדשה בישראל מפרט טכני F40 — https://www.cartube.co.il/bmw-116i-f40-israel-specs — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']

### Required specific Codex edits
- V06/V07 שגויות: להעביר ממודל BMW 116i למודל חדש/נפרד BMW 116 או canonical_model="116"; לתקן horsepower_hp מ-109 ל-122; year_start=2025 אלא אם מקור ישראלי מוכיח 2024.
- V06/V07 trims: Essence ו-M-Design תקינים לדגם 116, לא ל-116i.
- V00-V05 ההיסטוריות 116i יכולות להישאר אם iCar/Auto תומכים. לא לערבב הנעה אחורית היסטורית עם FWD F70 תחת אותו 116i.
- אחרי ההעברה: available_values_for_website של 116i לא יכיל Essence/M-Design של 116 החדש.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 74. BMW 118d
Priority: **בינוני**

Verdict: **כנראה לשמור, אבל לא להציג null trim כערך אתר.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Hatchback'; fuel_type='diesel'; engine='2.0L inline-4 turbo'; engine_displacement_l=2.0; horsepower_hp=143; transmission='6-speed manual'; drivetrain='RWD'; year_start=2008; year_end=2011; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='Hatchback'; fuel_type='diesel'; engine='2.0L inline-4 turbo'; engine_displacement_l=2.0; horsepower_hp=143; transmission='6-speed manual'; drivetrain='RWD'; year_start=2011; year_end=2015; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V02: version_or_trim=None; body_type='Hatchback'; fuel_type='diesel'; engine='2.0L inline-4 turbo'; engine_displacement_l=2.0; horsepower_hp=150; transmission='6-speed manual'; drivetrain='RWD'; year_start=2015; year_end=2018; support_level='direct'; missing_grounded_fields=['version_or_trim']

### Web evidence already researched by ChatGPT
- iCar וקיימות מקורות סדרה 1 דור 2004-2011/2011-2015/2015-2019; חיפוש לא מצא כאן מקור חדש שסותר 143/150 כ״ס.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_1/

Catalog source URLs already present in JSON:
- [0] iCar Israel: ב.מ.וו סדרה 1 (2011-2015) מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_1/ב.מ.וו_סדרה_1_דור_2/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] KML Israel: ב.מ.וו סדרה 1 2004-2011 נתונים טכניים — https://kml.co.il/Car/BMW/1-Series_2004-2011 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] iCar Israel: ב.מ.וו סדרה 1 2015-2019 מתיחת פנים - מפרט — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_1/ב.מ.וו_סדרה_1_דור_2_מתוח_פנים/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00-V02: להשאיר רק אם המקורות מציגים במפורש 118d, 2.0 טורבו דיזל, 143/150 כ״ס, ידני/אוטומטי לפי הקיים.
- version_or_trim=null אינו blocker כשגרסת הדגם היא 118d; להסיר missing_grounded_fields=[version_or_trim] אם אין trim שיווקי נפרד.
- לא להכניס null ל-available_values_for_website.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 75. BMW 118i
Priority: **בינוני-גבוה**

Verdict: **לשמור בזהירות; לוודא הספקי 170/136/140.**

### Current catalog variants
- V00: version_or_trim='Vibe'; body_type='Hatchback'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=140; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2019; year_end=2024; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim='Sport'; body_type='Hatchback'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=136; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2015; year_end=2019; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim='Business'; body_type='Hatchback'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=170; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2015; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='2.0L'; engine_displacement_l=2.0; horsepower_hp=143; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2008; year_end=2011; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 2019: סדרה 1 החדשה בישראל, F40, דגם 118i עם 1.5 טורבו 140 כ״ס ו-7 הילוכים DCT.
- Cartube 2015: מתיחת פנים סדרה 1 בישראל עם 118i 1.5/136 כ״ס.
- מקור היסטורי iCar/Auto צריך לתמוך ב-118i 2.0 143 בדור 2008-2011.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-1-החדשה-2019-בישראל
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-1-המחודשת-2015-בישראל
- https://www.cartube.co.il/חדשות-רכב/מהפכת-המחירים-של-ב-מ-וו-ומיני-בישראל

Catalog source URLs already present in JSON:
- [0] Cartube.co.il: ב.מ.וו סדרה 1 החדשה 2019 בישראל - מחיר החל מ-199,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-1-%D7%94%D7%97%D7%93%D7%A9%D7%94-2019-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-199-000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [1] Cartube.co.il: ב.מ.וו סדרה 1 המחודשת 2015 בישראל – מחיר החל מ-169,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-1-%D7%94%D7%9E%D7%97%D7%95%D7%93%D7%A9%D7%AA-2015-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D-%D7%95%D7%94%D7%97%D7%9C-%D7%9E-169-000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [2] Auto.co.il: מבחן דרכים: ב.מ.וו סדרה 1 118i - אוטו — https://www.auto.co.il/article/roadcartest/28929-bmw-1-series — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [3] iCar.co.il: ב.מ.וו סדרה 1 (2004-2011) מפרט טכני — https://www.icar.co.il/bmw/bmw_1_series/bmw_1_series_d1/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00 Vibe 2019-2024 נראה תקין אם Cartube/iCar מציינים Vibe; אחרת trim Vibe דורש אימות נוסף.
- V01 Sport 2015-2019: לוודא שה-trim הוא Sport ולא Sport Line/M Sport. אם מקור רק רמת גימור כללית, לתקן.
- V02 Business 2011-2015 170 כ״ס: לשים לב שיש מקורות שמציגים 118i 184 כ״ס במחירון 2013; אם המקור הישיר לקובץ לא מוכיח 170 — להעביר לשורת 120i/118i נכונה או review.
- V03 2008-2011 2.0 143: להשאיר רק עם מקור iCar מדויק; null לא לערכי אתר.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 76. BMW 120i
Priority: **קריטי**

Verdict: **להוציא את הדגם החדש 120 מהמודל 120i.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='2.0L'; engine_displacement_l=2.0; horsepower_hp=156; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2004; year_end=2011; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=184; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2015; year_end=2019; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=178; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2020; year_end=2024; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Hatchback'; fuel_type='mild_hybrid'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=170; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2024; year_end=2026; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 19.11.2024: סדרה 1 החדשה תשווק בישראל בדגם 120 עם 170 כ״ס או M135; לא 120i.
- Cartube price-list 2026: 120 Pure / Essence / M-Sport, 170 כ״ס.
- Cartube 2024: F70 116/120/123 naming; לא שמות i היסטוריים.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-1-החדשה-2025-נחתה-בישראל-מחיר-249900-שקל
- https://www.cartube.co.il/מחירון-רכב-חדש/ב-מ-וו/ב-מ-וו-סדרה-1
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-משיקה-גרסאות-הנעה-חדשות-לסדרה-1-f70

Catalog source URLs already present in JSON:
- [0] iCar Israel: BMW 1 Series 120i 2020-2024 Specifications - iCar Israel — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_1/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar Israel: BMW 1 Series 120i 2016-2019 Specs — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_1/2016/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] iCar Israel: BMW 1 Series 120i 2004-2011 Specs — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_1/2008/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [3] Cartube Israel: New BMW 1 Series 2024-2025 (120) Launch in Israel — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-1-%D7%94%D7%97%D7%93%D7%A9%D7%94-2025-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-240000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V03 2024-2026: להעביר ממודל BMW 120i למודל BMW 120; לפתוח variants לפי trims Pure, Essence, M-Sport אם מקור price-list מאשר.
- V03: אם שומרים fuel_type=mild_hybrid, חובה מקור שמציין 48V/סיוע חשמלי; אחרת fuel_type=petrol.
- V02 2020-2024 120i 178 FWD: לא להאריך מעבר ל-2024 כי F70 החליף שם ל-120.
- V00/V01 היסטוריים 120i נשארים רק עד שנות המקור.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 77. BMW 125i
Priority: **בינוני**

Verdict: **כנראה לשמור, לוודא שנות דור והספק.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='3.0L inline-6'; engine_displacement_l=3.0; horsepower_hp=218; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2008; year_end=2013; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='3.0L inline-6'; engine_displacement_l=3.0; horsepower_hp=218; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2008; year_end=2013; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=218; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2012; year_end=2016; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Hatchback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=224; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2016; year_end=2019; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- iCar סדרה 1 / סדרה 1 קופה-קבריולה משמש מקור לדורות 125i.
- Cartube 2016 מתיחת פנים: 125i אחרי מתיחה עם 224 כ״ס.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_1/
- https://www.cartube.co.il/חדשות-רכב/2016-ב-מ-וו-סדרה-1-המחודשת-בישראל

Catalog source URLs already present in JSON:
- [0] iCar: ב.מ.וו סדרה 1 (2012-2016) מחירון רכב מפרט ותמונות - iCar — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_1_%D7%93%D7%92%D7%9D_2012/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar: ב.מ.וו סדרה 1 קופה / קבריולה מחירון רכב - iCar — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_1_%D7%A7%D7%95%D7%A4%D7%94/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Cartube: 2016 ב.מ.וו סדרה 1 המחודשת בישראל - מחירון ומפרט — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/2016-%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-1-%D7%94%D7%9E%D7%97%D7%95%D7%93%D7%A9%D7%AA-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8%D7%95%D7%9F-%D7%95%D7%9E%D7%A4%D7%A8%D7%98 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00/V01 Coupe/Convertible 3.0 218 כ״ס 2008-2013: לשמור רק אם מקור ישראלי מראה 125i קופה/קבריולה; אחרת לפצל למודל סדרה 1 קופה/קבריולה.
- V02 2012-2016 218 ו-V03 2016-2019 224: לעגן ל-iCar/Cartube; לשים לב שהשינוי 218→224 נובע ממתיחת פנים.
- version_or_trim=null לא לאתר.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 78. BMW 128ti
Priority: **בינוני-גבוה**

Verdict: **המנוע/הנעה תקינים; trim Superior דורש אימות.**

### Current catalog variants
- V00: version_or_trim='Superior'; body_type='Hatchback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=265; transmission='8-speed automatic'; drivetrain='FWD'; year_start=2021; year_end=2024; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 08.11.2021: BMW 128ti בישראל, 2.0 טורבו, 265 כ״ס, 8AT, הנעה קדמית, מחיר 285,000 ₪.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-128ti-הספורטיבית-2022-בישראל-מחיר-265000-שקל

Catalog source URLs already present in JSON:
- [0] Cartube: ב.מ.וו 128ti בישראל - מחיר החל מ- 284,900 שקלים — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-128ti-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-284-900-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] Auto.co.il: ב.מ.וו סדרה 1 - מחירון, פלוסים ומינוסים — https://www.auto.co.il/model/bmw-1-series_g1323 — supports=['body_type', 'horsepower_hp', 'transmission', 'drivetrain', 'fuel_type', 'year_end']

### Required specific Codex edits
- V00: להשאיר 2.0T 265, 8AT, FWD, year_start=2021.
- version_or_trim="Superior" לא מופיע במקור Cartube שבדקתי. אם Auto/iCar לא תומך ב-Superior, לשנות version_or_trim=null או לרמת גימור המקורית המדויקת.
- year_end=2024 צריך מקור מחירון/דורות; אם אין, year_end=null או review.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 79. BMW 218i
Priority: **קריטי**

Verdict: **למחוק כפילות Gran Coupe ולהוסיף/לתקן קופה חדשה אם צריך.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=136; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2015; year_end=2021; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=140; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2020; year_end=None; support_level='direct'; missing_grounded_fields=['year_end', 'version_or_trim']

### Web evidence already researched by ChatGPT
- iCar 2026 סדרה 2 חדשה: גרסאות 218i M-Sport ו-218i M-Shadow עם 2.0 156 כ״ס — קופה, לא גראן קופה.
- יד2/שוק מציג 218i 2.0 156 לדגם חדש; פחות חזק ממקור iCar אבל תומך כבדיקה משנית.
- Cartube/כתבות 2020 Gran Coupe הן דגם נפרד.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_2/ב.מ.וו_סדרה_2_חדש/
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-2-גראן-קופה-בישראל-מחיר-החל-מ-249000-שקל

Catalog source URLs already present in JSON:
- [0] Cartube.co.il: ב.מ.וו סדרה 2 גראן קופה בישראל - מחיר החל מ- 249,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-2-גראן-קופה-בישראל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] iCar.co.il: ב.מ.וו סדרה 2 קופה - מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_2/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] BMW Israel Official: BMW 2 Series Gran Coupe Specifications - BMW Israel — https://www.bmw.co.il/he/all-models/2-series/gran-coupe/2020/bmw-2-series-gran-coupe-technical-data.html — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain']

### Required specific Codex edits
- V01 Sedan 2020-null הוא Gran Coupe ולכן למחוק מהמודל BMW 218i או להעביר ל-BMW 218i Gran Coupe. אסור כפילות עם מודל 218i Gran Coupe.
- V00 Coupe 2015-2021 1.5 136: לשמור אם iCar קופה מאשר. version_or_trim null לא לאתר.
- להוסיף/לתקן שורת Coupe חדשה 2024/2025-2026: 2.0L turbo, 156 hp, 8AT/RWD? רק אם iCar/יבואן מאשרים; trims M-Sport/M-Shadow לפי iCar.
- אם current new 218i הוא 2.0 ולא 1.5 — לא להאריך את V00 מעבר ל-2021.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 80. BMW 218i Gran Coupe
Priority: **בינוני**

Verdict: **לשמור כמודל נפרד; לא לקבל כפילות מ-218i.**

### Current catalog variants
- V00: version_or_trim='M-Sport'; body_type='Sedan'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=140; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2020; year_end=2021; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim='M-Sport'; body_type='Sedan'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=136; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2021; year_end=2024; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube: סדרה 2 גראן קופה בישראל מ-249,000 ₪; דגם 218i עם 1.5 טורבו 140 כ״ס בתחילת שיווק.
- iCar/יד2 מצביעים על 218i Gran Coupe ברמות גימור M-Sport/M-Shadow/M-Design לפי שנים.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-2-גראן-קופה-בישראל-מחיר-החל-מ-249000-שקל
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_2_גראן_קופה/

Catalog source URLs already present in JSON:
- [0] Cartube: ב.מ.וו סדרה 2 גראן קופה בישראל - מחיר החל מ-249,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-2-%D7%92%D7%A8%D7%90%D7%9F-%D7%A7%D7%95%D7%A4%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-249-000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [1] Icar: ב.מ.וו סדרה 2 גראן קופה - מחירון רכב, מבחן דרכים ומפרט טכני — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_2_%D7%92%D7%A8%D7%90%D7%9F_%D7%A7%D7%95%D7%A4%D7%94/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']

### Required specific Codex edits
- לשמור V00/V01 רק כאן, לא גם ב-BMW 218i.
- V00 140 כ״ס 2020-2021 ו-V01 136 כ״ס 2021-2024 דורשים מקור גרסה מדויק; אם אין מקור לשינוי 140→136, לאחד/לתקן.
- year_end=2024 לא להאריך בלי מקור לגרסת F74 החדשה בישראל.
- available_values_for_website: M-Sport בלבד אם זה היחיד המגובה; לא להוסיף null.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 81. BMW 220i
Priority: **קריטי**

Verdict: **הפרופיל מערבב יותר מדי גופי-דגם ושנים.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=184; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2026; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=184; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2015; year_end=2021; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='MPV'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=192; transmission='8-speed automatic'; drivetrain='FWD'; year_start=2014; year_end=2018; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=178; transmission='7-speed dual_clutch'; drivetrain='FWD'; year_start=2020; year_end=2026; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- iCar 2018 220i Sport: קופה, 2 דלתות, RWD, 8 הילוכים, 1998 סמ״ק, 184 כ״ס.
- iCar 2026 סדרה 2 חדשה לא מציג 220i כגרסה חדשה; מציג 218i ו-M240i, ולכן year_end=2026 לקופה 220i חשוד.
- Cartube Gran Coupe 2020 משויך לדגם גראן קופה, לא קופה/קבריולה.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_2/ב.מ.וו_סדרה_2_יד_שניה_ד10/version19358/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_2/ב.מ.וו_סדרה_2_חדש/

Catalog source URLs already present in JSON:
- [135] iCar: ב.מ.וו סדרה 2 קופה מפרט טכני - iCar — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_2/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [136] iCar: ב.מ.וו סדרה 2 קבריולה מפרט טכני - iCar — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_2_קבריולה/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [137] Auto.co.il: ב.מ.וו סדרה 2 אקטיב טורר 220i - Auto.co.il — https://www.auto.co.il/model/bmw-2-series-active-tourer_g246 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [138] Cartube: ב.מ.וו סדרה 2 גראן קופה בישראל - Cartube — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-2-גראן-קופה-בישראל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00 Coupe 2014-2026: לפצל/לקצר. 2014-2021/2022 בלבד אלא אם מקור ישראלי מראה 220i Coupe חדש עד 2026. כרגע iCar 2026 לא תומך.
- V01 Convertible 2015-2021 כנראה תקין אך נדרש מקור נפרד לקבריולה.
- V02 MPV 220i Active Tourer: לא להשאיר תחת מודל 220i הכללי אם יש canonical_model נפרד לאקטיב טורר; להעביר ל-BMW 220i Active Tourer או Series 2 Active Tourer.
- V03 Sedan 220i Gran Coupe: להעביר ל-220i Gran Coupe אם המערכת מפרידה Gran Coupe.
- לא לערבב Coupe/Convertible/MPV/Sedan תחת אתר אחד אם המשתמש בוחר דגם ולא רק מנוע.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 82. BMW 225xe (Active Tourer PHEV)
Priority: **קריטי**

Verdict: **לשנות/לחסום דור שני; support unknown לא נכנס לנקי.**

### Current catalog variants
- V00: version_or_trim=None; body_type='MPV'; fuel_type='plug_in_hybrid'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=224; transmission='automatic'; drivetrain='AWD'; year_start=2017; year_end=2021; support_level='unknown'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='MPV'; fuel_type='plug_in_hybrid'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=245; transmission='dual_clutch'; drivetrain='AWD'; year_start=2022; year_end=2024; support_level='unknown'; missing_grounded_fields=['version_or_trim']

### Web evidence already researched by ChatGPT
- Cartube/BMW global 2022: הדור השני נקרא 225e xDrive ו-230e xDrive; 225e עם 245 כ״ס, 230e עם 326 כ״ס. לא 225xe.
- Autoboom תוצאה מציינת 225xe 2018-2021 אך גם ״לא זמין בישראל״ — לא מקור מספיק לנקי.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/דור-שני-2022-ב-מ-וו-סדרה-2-אקטיב-טורר-החדשה-נחשפת
- https://autoboom.co.il/catalog/cars/bmw/2-series-active-tourer/1-generation-restyling/compact-van/67702

Catalog source URLs already present in JSON:
- [0] Cartube.co.il: ב.מ.וו משיקה בישראל את דגמי הפלאג-אין iPerformance — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-משיקה-בישראל-את-דגמי-הפלאג-אין-iperformance — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] iCar: ב.מ.וו סדרה 2 אקטיב טורר - מחירון, מפרטים — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_2_אקטיב_טורר/ב.מ.וו_סדרה_2_אקטיב_טורר_יד_שניה_1/ — supports=['year_end', 'horsepower_hp', 'engine', 'drivetrain', 'fuel_type']
- [2] Cartube.co.il: ב.מ.וו סדרה 2 אקטיב טורר החדש 2022 בישראל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-2-אקטיב-טורר-2022-החדש-בישראל-מחיר-החל-מ-289-900-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00 2017-2021 225xe 224 כ״ס: להשאיר רק אם כתבת Cartube ישראל iPerformance או iCar ישראל מוכיחה יבוא/מחיר/מפרט. אחרת review.
- V01 2022-2024 שגוי בשם: זה צריך להיות 225e xDrive Active Tourer, לא 225xe. להעביר למודל 225e (Active Tourer PHEV) או לחסום.
- support_level=unknown אינו מותר בנקי. לשנות ל-direct רק עם מקור ישראלי, או להעביר ל-review.
- version_or_trim null לא חסר אם שם הדגם הוא 225xe/225e, אבל לא לאתר.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 83. BMW 230e (Active Tourer PHEV)
Priority: **בינוני-גבוה**

Verdict: **כנראה לשמור אם מקור ישראלי באמת קיים.**

### Current catalog variants
- V00: version_or_trim='M-Sport'; body_type='MPV'; fuel_type='plug_in_hybrid'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=326; transmission='7-speed dual_clutch'; drivetrain='AWD'; year_start=2022; year_end=2025; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim='M-Express'; body_type='MPV'; fuel_type='plug_in_hybrid'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=326; transmission='7-speed dual_clutch'; drivetrain='AWD'; year_start=2022; year_end=2025; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 2022/2023: 230e xDrive Active Tourer עם 326 כ״ס, מנוע 1.5 + מנוע חשמלי אחורי, פלאג-אין.
- מקור גלובלי בלבד לא מספיק; צריך את כתבת השקה/מחיר בישראל שמופיעה בקבצי הקטלוג.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-2-אקטיב-טורר-פלאג-אין-2023-בישראל-מחיר-החל-מ-289900-שקל
- https://www.cartube.co.il/חדשות-רכב/דור-שני-2022-ב-מ-וו-סדרה-2-אקטיב-טורר-החדשה-נחשפת

Catalog source URLs already present in JSON:
- [1] Cartube: ב.מ.וו סדרה 2 אקטיב טורר פלאג-אין 2023 בישראל - מחיר החל מ-289,900 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-2-%D7%90%D7%A7%D7%98%D7%99%D7%91-%D7%98%D7%95%D7%A8%D7%A8-%D7%A4%D7%9C%D7%90%D7%92-%D7%90%D7%99%D7%9F-2023-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-289,900-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'version_or_trim']
- [2] iCar: ב.מ.וו סדרה 2 אקטיב טורר - מחירון, קטלוג רכב — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_2_%D7%90%D7%A7%D7%98%D7%99%D7%91_%D7%98%D7%95%D7%A8%D7%A8/ — supports=['body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain', 'year_end']

### Required specific Codex edits
- V00/V01 M-Sport/M-Express: לשמור רק אם הכתבה הישראלית מפרטת את רמות הגימור האלה. אם לא, לאחד ל-230e xDrive או review.
- year_start צריך להיות שנת שיווק בישראל: 2022 או 2023 לפי מקור. לא להשתמש רק ב-global reveal.
- year_end=2025 דורש מקור מחירון/יבואן עד 2025. אם אין, year_end=null או review.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 84. BMW 316i
Priority: **בינוני**

Verdict: **לשמור רק עם מקורות דור מדויקים.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.6L turbo'; engine_displacement_l=1.6; horsepower_hp=136; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2013; year_end=2015; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.8L'; engine_displacement_l=1.8; horsepower_hp=115; transmission='automatic'; drivetrain='RWD'; year_start=2002; year_end=2005; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.9L'; engine_displacement_l=1.9; horsepower_hp=105; transmission='automatic'; drivetrain='RWD'; year_start=1999; year_end=2001; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V03: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.6L'; engine_displacement_l=1.6; horsepower_hp=102; transmission='automatic'; drivetrain='RWD'; year_start=1991; year_end=1998; support_level='direct'; missing_grounded_fields=['version_or_trim']

### Web evidence already researched by ChatGPT
- מקורות iCar/Auto לדורות E36/E46/F30 נדרשים; חיפוש Cartube 2011 מדבר על 318i/320i/325i ולא מוכיח 316i.
- 316i F30 1.6 טורבו 136 כ״ס מוכר בדור 2013-2015 אך דורש מקור ישראלי ישיר.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/
- https://www.auto.co.il/cars/bmw/3-series

Catalog source URLs already present in JSON:
- [140] iCar: ב.מ.וו סדרה 3 (2012-2019) מפרט טכני - iCar — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3_דגם_2012/מפרט_טכני/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [141] Auto.co.il: ב.מ.וו 316i במבחן דרכים - אוטו — https://www.auto.co.il/article/roadcartest/29959-road-tests-bmw-3-series — supports=['horsepower_hp', 'engine', 'transmission', 'drivetrain']
- [142] Auto.co.il: ב.מ.וו סדרה 3 (1998-2005) - קטלוג רכב - אוטו — https://www.auto.co.il/catalog/bmw/3-series/1998-2005 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [143] Auto.co.il: ב.מ.וו סדרה 3 (1991-1998) - קטלוג רכב - אוטו — https://www.auto.co.il/catalog/bmw/3-series/1991-1998 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00 2013-2015 1.6T 136: לאשר מול iCar. אם אין, review.
- V01-V03 היסטוריים: לוודא שנות התחלה וסיום לפי דורות בישראל; לא להסתמך על גלובלי.
- version_or_trim=null לא להכניס לערכי אתר; remove missing version_or_trim אם זה שם הדגם עצמו.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 85. BMW 318d
Priority: **גבוה**

Verdict: **לתקן ערבוב Sedan/GT ולוודא דיזל ישראל.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=143; transmission='automatic'; drivetrain='RWD'; year_start=2008; year_end=2015; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=150; transmission='automatic'; drivetrain='RWD'; year_start=2016; year_end=2020; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Liftback'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=143; transmission='automatic'; drivetrain='RWD'; year_start=2013; year_end=2015; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Liftback'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=150; transmission='automatic'; drivetrain='RWD'; year_start=2016; year_end=2020; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 2018/2022 מציג 318d 150 כ״ס בדור G20/מתיחת פנים, אך אלו מקורות הצגה/אירופה בחלקם; צריך לוודא ישראל.
- Cartube/iCar בקובץ אומרים מנועי דיזל חדשים בישראל — להשתמש רק אם אכן כתבה ישראלית.
- GT הוא body/model נפרד מסדאן.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/2019-ב-מ-וו-סדרה-3-החדשה-נחשפת
- https://www.cartube.co.il/חדשות-רכב/מתיחת-פנים-2022-ב-מ-וו-סדרה-3-החדשה
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3_gt/

Catalog source URLs already present in JSON:
- [0] Auto.co.il: ב.מ.וו סדרה 3 מחירון רכב, מפרט טכני וקטלוג רכבים - Auto — https://www.auto.co.il/model/bmw-3-series — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar.co.il: ב.מ.וו סדרה 3 GT מחירון רכב ומפרט טכני - iCar — https://www.icar.co.il/bmw/bmw_3_series_gt/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Cartube.co.il: ב.מ.וו מציגה מנועי דיזל חדשים (150 כ"ס) לסדרה 3 בישראל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-מציגה-מנועי-דיזל-חדשים-לסדרה-3 — supports=['horsepower_hp', 'engine', 'year_start', 'year_end']

### Required specific Codex edits
- V02/V03 Liftback הם Series 3 GT; להעביר למודל BMW 318d GT או canonical_model נפרד, לא לערבב עם Sedan אם האתר מציג דגמים.
- V00 2008-2015 143 כ״ס: טווח רחב מדי; לבדוק אם E90 ו-F30 צריכים פיצול 2008-2011/2012-2015.
- V01 2016-2020 150 כ״ס: לשמור רק עם מקור ישראלי; אחרת review.
- version_or_trim null לא לאתר.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 86. BMW 318i
Priority: **בינוני-גבוה**

Verdict: **המודרנית טובה; היסטוריות דורשות אימות trim.**

### Current catalog variants
- V00: version_or_trim='Business'; body_type='Sedan'; fuel_type='petrol'; engine='2.0L'; engine_displacement_l=2.0; horsepower_hp=136; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2005; year_end=2012; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim='Sport'; body_type='Sedan'; fuel_type='petrol'; engine='1.5L turbo'; engine_displacement_l=1.5; horsepower_hp=136; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2015; year_end=2019; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim='Business / M-Design'; body_type='Sedan'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=156; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2020; year_end=2024; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- iCar 2022 318i Business ו-M-Design מופיעים בדף גרסה; 2.0, 156 כ״ס.
- iCar מבחן 2021: 318i עם 1998 סמ״ק, טורבו בנזין, 156 כ״ס; M-Design בתוספת מחיר.
- Cartube 2023 מחירון: 318i Business ו-318i M-Design בישראל.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שניה_ד12/version24888/
- https://www.icar.co.il/מבחני_רכב/ב.מ.וו_סדרה_3_(2.0_ליטר,_318i)_-_מבחן_רכב/
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-3-החדשה-2023-בישראל-מחיר-290000-שקל

Catalog source URLs already present in JSON:
- [752] iCar Israel: ב.מ.וו סדרה 3 2015 - 2019 - מפרט טכני - iCar — https://www.icar.co.il/bmw/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_d18/version7948/ — supports=['engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'body_type', 'fuel_type', 'year_start', 'year_end', 'version_or_trim']
- [753] iCar Israel: ב.מ.וו 318i סדאן (156 כ"ס) 2020 - מפרט טכני - iCar — https://www.icar.co.il/bmw/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3_%D7%97%D7%93%D7%A9/version15167/ — supports=['engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'body_type', 'fuel_type', 'year_start', 'version_or_trim']
- [754] Auto.co.il: ב.מ.וו סדרה 3 מפרט טכני - אוטו — https://www.auto.co.il/model/bmw-3-series_g250 — supports=['engine', 'horsepower_hp', 'transmission', 'fuel_type', 'version_or_trim', 'year_end']
- [755] iCar Israel: ב.מ.וו סדרה 3 2005 - 2012 - מפרט טכני - iCar — https://www.icar.co.il/bmw/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_d16/version5224/ — supports=['engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'body_type', 'fuel_type', 'year_start', 'year_end', 'version_or_trim']

### Required specific Codex edits
- V02 Business / M-Design 2020-2024: מומלץ לפצל לשתי שורות trim נפרדות: Business ו-M-Design, לא ערך משולב עם slash.
- V01 Sport 2015-2019: לוודא שמקור ישראלי מציין Sport דווקא. אם לא, לתקן ל-trim המדויק.
- V00 Business 2005-2012: trim Business על כל השנים חשוד; אם המקור לא מחזיק אותו לכל הדור, לשנות version_or_trim=null.
- year_end 2024: לוודא שאין המשך/הפסקה לפי מחירון 2025; לא להאריך ל-2026 כי סדרה 3 2023/2024 בישראל עברה להתמקדות 318i/320e/330e.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 87. BMW 320e
Priority: **בינוני**

Verdict: **נראה תקין; לא להאריך בלי מקור.**

### Current catalog variants
- V00: version_or_trim='M-Design'; body_type='Sedan'; fuel_type='plug_in_hybrid'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=204; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2021; year_end=2024; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 28.04.2021: 320e פלאג-אין בישראל, 204 כ״ס, טווח חשמלי 60 ק״מ.
- Cartube 2024 price/spec: 320e M-Design, 1998 סמ״ק, פלאג-אין, 204 כ״ס, RWD, 8AT.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/חדש-בישראל-2021-ב-מ-וו-320e-פלאג-אין-מחיר-289900-שקל
- https://www.cartube.co.il/מחירון-רכב-חדש/ב-מ-וו/ב-מ-וו-סדרה-3/3369-ב-מ-וו-סדרה-3-2-0-320e-m-design

Catalog source URLs already present in JSON:
- [0] Cartube: ב.מ.וו 320e בישראל - מחיר החל מ-290,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%92%D7%A8%D7%A1%D7%AA-%D7%A4%D7%9C%D7%90%D7%92-%D7%90%D7%99%D7%9F-%D7%96%D7%95%D7%9C%D7%94-%D7%99%D7%95%D7%AA%D7%A8-%D7%91-%D7%9E-%D7%95%D7%95-320e-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-290,000-%D7%A9%D7%A7%D7%9C — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] iCar: ב.מ.וו סדרה 3 - מפרט טכני — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3_%D7%99%D7%93_%D7%A8%D7%90%D7%A9%D7%95%D7%A0%D7%94_%D7%93%D7%92%D7%9D_%D7%A9%D7%91%D7%99%D7%A2%D7%99/ — supports=['year_start', 'year_end', 'horsepower_hp', 'fuel_type', 'body_type']

### Required specific Codex edits
- V00: להשאיר M-Design, 2.0 PHEV, 204 hp, 8AT, RWD, 2021-2024 אם Cartube/iCar תומכים.
- אם יש מקור 2025 שמציג 320e, אפשר לעדכן year_end; אחרת לא לנחש.
- לא לערבב 320e עם 330e/330e xDrive.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 88. BMW 320i
Priority: **קריטי**

Verdict: **year_end=2026 חשוד מאוד; צריך פיצול דורות.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L i6'; engine_displacement_l=2.0; horsepower_hp=150; transmission='automatic'; drivetrain='RWD'; year_start=1990; year_end=2000; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.2L i6'; engine_displacement_l=2.2; horsepower_hp=170; transmission='automatic'; drivetrain='RWD'; year_start=2000; year_end=2005; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L i4'; engine_displacement_l=2.0; horsepower_hp=150; transmission='automatic'; drivetrain='RWD'; year_start=2005; year_end=2008; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L i4'; engine_displacement_l=2.0; horsepower_hp=156; transmission='automatic'; drivetrain='RWD'; year_start=2008; year_end=2011; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L i4 turbo'; engine_displacement_l=2.0; horsepower_hp=184; transmission='automatic'; drivetrain='RWD'; year_start=2012; year_end=2026; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 2012: 320i F30 בישראל עם 2.0 טורבו 184 כ״ס ו-8AT.
- Cartube 2018/2019: G20 320i עם 2.0 טורבו 184 כ״ס.
- Cartube 2023 ישראל מחירון: 318i, 320e, 330e — לא 320i; לכן 320i עד 2026 לא מגובה.
- iCar דורות ישנים צריכים לפצל E36/E46/E90 לפי מנוע 2.0/2.2/156.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-3-החדשה-בישראל-מחיר-החל-מ-255000-שקל
- https://www.cartube.co.il/חדשות-רכב/2019-ב-מ-וו-סדרה-3-החדשה-נחשפת
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-3-החדשה-2023-בישראל-מחיר-290000-שקל

Catalog source URLs already present in JSON:
- [0] Cartube.co.il: ב.מ.וו סדרה 3 החדשה 2019 בישראל (G20) — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-3-החדשה-2019-בישראל-מחיר-החל-מ-289,000-שקל — supports=['year_start', 'year_end', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'body_type', 'fuel_type']
- [1] Auto.co.il: ב.מ.וו סדרה 3 (2012-2019) מחירון, מפרטים (F30) — https://www.auto.co.il/model/bmw-3-series_g202 — supports=['year_start', 'year_end', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'body_type', 'fuel_type']
- [2] iCar.co.il: ב.מ.וו סדרה 3 (2005-2011) יד שניה - מפרט טכני (E90) — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שניה_ד3/ — supports=['year_start', 'year_end', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'body_type', 'fuel_type']
- [3] iCar.co.il: ב.מ.וו סדרה 3 (1998-2005) יד שניה - מפרט טכני (E46) — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שניה_ד2/ — supports=['year_start', 'year_end', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'body_type', 'fuel_type']
- [4] iCar.co.il: ב.מ.וו סדרה 3 (1990-1998) יד שניה - מפרט טכני (E36) — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שניה_ד1/ — supports=['year_start', 'year_end', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'body_type', 'fuel_type']

### Required specific Codex edits
- V04 2012-2026 184: לפצל לפחות ל-2012-2018/2019 F30 ו-2019-2020/2021 G20 אם מקור ישראלי תומך. לא להשאיר עד 2026 ללא מקור מחירון עדכני.
- V00 1990-2000 2.0 i6 150: לפצל E36 1990/1991-1998 ו-E46 1998-2000 אם המקורות שונים.
- V01 2000-2005 2.2 i6 170, V02 2005-2008 150, V03 2008-2011 156: לשמור עם iCar ספציפי.
- version null תקין ברמת דגם, לא לערכי אתר.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 89. BMW 323i
Priority: **בינוני**

Verdict: **היסטורי; דורש מקור גרסאות ידני/אוטומטי.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=170; transmission='automatic'; drivetrain='RWD'; year_start=1996; year_end=2000; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=170; transmission='manual'; drivetrain='RWD'; year_start=1996; year_end=2000; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V02: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=170; transmission='automatic'; drivetrain='RWD'; year_start=1996; year_end=2000; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V03: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=170; transmission='manual'; drivetrain='RWD'; year_start=1996; year_end=2000; support_level='direct'; missing_grounded_fields=['version_or_trim']

### Web evidence already researched by ChatGPT
- מקורות Auto/iCar לדורות E36/E46 נדרשים; אין להשתמש בידע גלובלי בלבד.
- שורות manual/automatic צריכות מקור שמציג שניהם בשוק ישראלי.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/
- https://www.auto.co.il/cars/bmw/3-series

Catalog source URLs already present in JSON:
- [148] icar.co.il: ב.מ.וו סדרה 3 (1998-2005) מפרט טכני - Icar — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שניה_דגם_3/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [149] auto.co.il: ב.מ.וו סדרה 3 1990-1998 (E36) - מפרט, גרסאות ומחירים — https://www.auto.co.il/model/bmw-3-series_g131 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00-V03: לאשר 2.5 inline-6, 170 כ״ס, 1996-2000, body Sedan/Coupe, transmission manual/automatic. אם המקור לא מפריד ידני/אוטומטי — לא להחזיק שתי שורות clean.
- year_start עשוי להיות 1995/1996 לפי מקור; לא לנחש.
- support_level direct בלבד אם iCar/Auto מציגים את הגרסה; אחרת review.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 90. BMW 325i
Priority: **בינוני-גבוה**

Verdict: **לשמור אך לתקן שנות E36/מרכבים אם צריך.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=218; transmission='automatic'; drivetrain='RWD'; year_start=2005; year_end=2012; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=218; transmission='automatic'; drivetrain='RWD'; year_start=2006; year_end=2012; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=218; transmission='automatic'; drivetrain='RWD'; year_start=2007; year_end=2012; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=192; transmission='automatic'; drivetrain='RWD'; year_start=2000; year_end=2005; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=192; transmission='automatic'; drivetrain='RWD'; year_start=2000; year_end=2005; support_level='direct'; missing_grounded_fields=[]
- V05: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=192; transmission='automatic'; drivetrain='RWD'; year_start=2000; year_end=2005; support_level='direct'; missing_grounded_fields=[]
- V06: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=192; transmission='automatic'; drivetrain='RWD'; year_start=1990; year_end=1998; support_level='direct'; missing_grounded_fields=[]
- V07: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=192; transmission='automatic'; drivetrain='RWD'; year_start=1992; year_end=1998; support_level='direct'; missing_grounded_fields=[]
- V08: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='2.5L inline-6'; engine_displacement_l=2.5; horsepower_hp=192; transmission='automatic'; drivetrain='RWD'; year_start=1993; year_end=1998; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- iCar E90/E46 ו-Auto E36 הם המקורות הדרושים; הקטלוג כולל 218 כ״ס לדור E90 ו-192 כ״ס לדורות E46/E36.
- שנת 1990 לסדאן E36 325i חשודה; E36 325i לרוב 1991+ וצריך מקור ישראלי.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/
- https://www.auto.co.il/cars/bmw/3-series

Catalog source URLs already present in JSON:
- [0] iCar IL: ב.מ.וו סדרה 3 (2005-2012) מחירון, מפרטים ואמינות — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%933/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar IL: ב.מ.וו סדרה 3 (1998-2005) - iCar — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%932/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Auto.co.il: ב.מ.וו סדרה 3 1990-1998 מפרט טכני - אוטו — https://www.auto.co.il/model/bmw-3-series_g249 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V06 Sedan 1990-1998: לבדוק source; אם אין 1990 ישראלי, לשנות year_start ל-1991/1992 לפי מקור.
- V07 Coupe 1992-1998 ו-V08 Convertible 1993-1998 סבירים אך דורשים מקור לכל body.
- V00-V02 E90 2.5 218 2005-2012: לשמור אם iCar מציג Sedan/Coupe/Convertible.
- V03-V05 E46 192 2000-2005: לשמור אם iCar מציג כל body; null לא לאתר.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 91. BMW 328i
Priority: **גבוה**

Verdict: **F30 תקין; היסטורי indirect לא יכול להישאר clean בלי חיזוק.**

### Current catalog variants
- V00: version_or_trim='Luxury'; body_type='Sedan'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=245; transmission='automatic'; drivetrain='RWD'; year_start=2012; year_end=2016; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim='Sport'; body_type='Sedan'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=245; transmission='automatic'; drivetrain='RWD'; year_start=2012; year_end=2016; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.8L'; engine_displacement_l=2.8; horsepower_hp=193; transmission='automatic'; drivetrain='RWD'; year_start=1998; year_end=2000; support_level='indirect'; missing_grounded_fields=['version_or_trim']
- V03: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.8L'; engine_displacement_l=2.8; horsepower_hp=193; transmission='automatic'; drivetrain='RWD'; year_start=1999; year_end=2000; support_level='indirect'; missing_grounded_fields=['version_or_trim']
- V04: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.8L'; engine_displacement_l=2.8; horsepower_hp=193; transmission='automatic'; drivetrain='RWD'; year_start=1995; year_end=1998; support_level='indirect'; missing_grounded_fields=['version_or_trim']
- V05: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.8L'; engine_displacement_l=2.8; horsepower_hp=193; transmission='manual'; drivetrain='RWD'; year_start=1995; year_end=1998; support_level='indirect'; missing_grounded_fields=['version_or_trim']

### Web evidence already researched by ChatGPT
- Cartube 2012: 328i F30 בישראל עם 2.0 טורבו 245 כ״ס.
- iCar 2012 328i Luxury מציג גרסה 2.0 328i Luxury; יש גם Sport לפי רשימת גרסאות.
- שורות E36/E46 2.8 193 מסומנות support_level=indirect בקובץ — זה לא מספיק ל-clean מוחלט.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-3-החדשה-בישראל-מחיר-החל-מ-255000-שקל
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שניה_ד11/version9573/

Catalog source URLs already present in JSON:
- [0] Auto.co.il: ב.מ.וו סדרה 3 (2012-2018) - מפרט טכני — https://www.auto.co.il/catalog/bmw/3-series/2012-2018 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [1] iCar.co.il: ב.מ.וו סדרה 3 דור 6 (F30) מפרט טכני — https://www.icar.co.il/bmw/3_series/6th_gen/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [2] iCar.co.il: ב.מ.וו סדרה 3 דור 4 (E46) מפרט טכני — https://www.icar.co.il/bmw/3_series/4th_gen/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [3] iCar.co.il: ב.מ.וו סדרה 3 דור 3 (E36) מפרט טכני — https://www.icar.co.il/bmw/3_series/3rd_gen/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [4] iCar.co.il: ב.מ.וו סדרה 3 קופה (E46) מפרט טכני — https://www.icar.co.il/bmw/3_series_coupe/1st_gen/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00/V01 Luxury/Sport 2012-2016: להשאיר אם iCar/Cartube מציגים trim ורכיבים. לוודא שה-transmission הוא 8AT ולא "automatic" כללי אם normalized.
- V02-V05 היסטוריות 2.8 193: להעביר ל-review או להעלות ל-direct רק אחרי פתיחת מקור iCar/Auto ספציפי לגרסה/מרכב/גיר.
- manual row V05: אם המקור לא מוכיח מכירה ישראלית ידנית, למחוק/ל-review.
- לא להשאיר missing version_or_trim כבעיה אם הדגם עצמו 328i, אבל source support חייב להיות direct.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

# Final instruction after RUN 1
Apply only this first batch now. Do not start the last 25 or the 3 blocked models in this run. After edits, output:
1. list of rows kept clean,
2. list of rows corrected,
3. list of rows moved to review,
4. exact JSON paths changed,
5. quality scan/test result.


---

# RUN 2 / 3 — Deep web-backed correction prompt for Codex

Scope: last 25 models from the last 50 clean catalog entries, indices 92–116.
Input catalog: `data/model_technical_catalog_il.json` from uploaded zip.
Date: 2026-06-16.

## Mission for Codex
You do **not** have web access. ChatGPT already performed the external web research and embedded the findings and URLs below. Use this as an offline evidence package and update the local JSON files only. Treat the current clean catalog as suspicious until every retained field is grounded.
1. Israeli market only. Do not retain rows supported only by global reveal/spec articles, overseas specs, generic knowledge, ads, or a source saying the model is only expected to arrive.
2. Validate every retained row field-by-field: make, model/canonical_model, version_or_trim, body_type, fuel_type, engine, engine_displacement_l, horsepower_hp, transmission, drivetrain, year_start, year_end.
3. Model-code rows such as 330e/530e/420i may have `version_or_trim=null` only when the marketed model itself is the variant and no separate Israeli trim is grounded. Never put null/Base/Standard in `available_values_for_website`.
4. BMW M Performance identity must be exact: M340i and M440i are not the same as 340i/440i. Split or rename instead of hiding the M model in `version_or_trim`.
5. Body identity must be exact: Gran Coupe, Gran Turismo/GT, Convertible/Cabriolet and Liftback must not be flattened into Sedan/Coupe if the website needs distinct choices.
6. If a field cannot be backed by the URLs and evidence below, correct it, set it null + mark `missing_grounded_fields`, or move that row/model to `model_technical_catalog_il_review.json`.
7. After edits, rebuild `sources`, `source_indexes`, `field_sources`, `available_values_for_website`, `invalid_or_non_trim_labels`, and run quality scan/tests.

## Exact run list
92. BMW 330e, 93. BMW 330i, 94. BMW 335i, 95. BMW 340i, 96. BMW 420i, 97. BMW 428i, 98. BMW 430i, 99. BMW 435i, 100. BMW 440i, 101. BMW 518i, 102. BMW 520d, 103. BMW 520i, 104. BMW 523i, 105. BMW 525i, 106. BMW 528i, 107. BMW 530e, 108. BMW 530i, 109. BMW 535i, 110. BMW 540i, 111. BMW 545e, 112. BMW 630i GT, 113. BMW 640i GT, 114. BMW 650i, 115. BMW 728i, 116. BMW 730i

---

## 92. BMW 330e
Priority: **גבוה**

Verdict: **לשמור אבל לתקן שנת סיום/רמות גימור ולנקות missing.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='plug_in_hybrid'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=252; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2016; year_end=2018; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='plug_in_hybrid'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=292; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2019; year_end=None; support_level='direct'; missing_grounded_fields=['version_or_trim', 'year_end']

### Web evidence already researched by ChatGPT
- Cartube ישראל 17.06.2019: 330e החדשה בישראל, מנוע 2.0 טורבו 184 כ״ס + מנוע חשמלי, הספק משולב 252 כ״ס או 292 כ״ס ב-XtraBoost, תיבה אוטומטית 8 הילוכים.
- Cartube מחירון 2026: סדרה 3 2.0 330e M-Shadow, פלאג-אין, 292 כ״ס, מחיר 429,900 ₪.
- Auto.co.il 2026: סדרה 3 משווקת בישראל בגרסה אחת 330e וברמת גימור אחת M-Shadow.
- iCar current: סדרה 3 משווקת ב-318 בנזין ושתי גרסאות PHEV 320e/330e, 204/292 כ״ס.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-330e-היברידית-החדשה-2019-בישראל-מחיר-290000-שקל
- https://www.cartube.co.il/מחירון-רכב-חדש/ב-מ-וו/ב-מ-וו-סדרה-3
- https://www.auto.co.il/cars/bmw/3-series/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_חדש/

Catalog source URLs already present in JSON:
- [1] Cartube: ב.מ.וו 330e פלאג-אין בישראל – מחיר החל מ-290 אלף שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-330e-פלאג-אין-בישראל-מחיר-החל-מ-290-אלף-שקל — supports=['year_start', 'horsepower_hp', 'engine', 'engine_displacement_l', 'transmission', 'body_type', 'fuel_type', 'drivetrain']
- [2] Cartube: ב.מ.וו 330e החדשה 2019 בישראל - מחיר החל מ- 299,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-330e-החדשה-2019-בישראל-מחיר-החל-מ-299-000-שקל — supports=['year_start', 'horsepower_hp', 'engine', 'engine_displacement_l', 'transmission', 'body_type', 'fuel_type', 'drivetrain']
- [3] iCar: ב.מ.וו סדרה 3 יד שניה - מחירון, מפרטים, אמינות — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שניה_ד6/ — supports=['year_end', 'drivetrain']

### Required specific Codex edits
- V00 2016-2018 252 כ״ס: לשמור רק אם מקור Cartube/Auto/iCar תומך בדגם F30 330e בישראל; version_or_trim יכול להישאר null רק אם אין trim נפרד.
- V01 2019-null 292 כ״ס: לא להשאיר year_end=null. לעדכן year_end=2026 על בסיס מחירון/Auto 2026.
- לשקול פיצול רמות גימור לשנים המאוחרות: 2025 M-Sport/M-Shadow, 2026 M-Shadow; אם לא מפצלים, אל תציג null ב-available_values_for_website.
- לנקות missing_grounded_fields: year_end כבר מגובה עד 2026; version_or_trim חסר רק אם החלטת שהאתר מחייב trim שיווקי.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 93. BMW 330i
Priority: **גבוה מאוד**

Verdict: **חובה לתקן שורת G20 פתוחה; 330i לא current בישראל.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L inline-6'; engine_displacement_l=3.0; horsepower_hp=231; transmission='5-speed automatic'; drivetrain='RWD'; year_start=2000; year_end=2005; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L inline-6'; engine_displacement_l=3.0; horsepower_hp=258; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2005; year_end=2011; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L turbo inline-4'; engine_displacement_l=2.0; horsepower_hp=252; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2015; year_end=2019; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L turbo inline-4'; engine_displacement_l=2.0; horsepower_hp=258; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2019; year_end=None; support_level='direct'; missing_grounded_fields=['year_end']

### Web evidence already researched by ChatGPT
- Cartube 2015 ישראל: 330i Sport/Luxury ברשימת מחירי סדרה 3 המחודשת, 330i Luxury לצד 340i Luxury.
- Auto/iCar 2019: G20 330i עם מנוע 2.0 טורבו 258 כ״ס ותיבה אוטומטית 8 הילוכים.
- Cartube 10.11.2022: סדרה 3 המחודשת בישראל תשווק בדגם בנזין אחד ושני דגמי פלאג-אין; הדגם הבנזין הוא 318/318i לפי מחירונים עדכניים, לא 330i.
- Auto.co.il 2026: סדרה 3 משווקת בישראל בגרסה אחת 330e בלבד.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/2015-ב-מ-וו-סדרה-3-החדשה-בישראל-–-מחיר-החל-מ-240-אלף-שקל
- https://www.auto.co.il/cars/bmw/3-series/2019/
- https://www.icar.co.il/חדשות_רכב/נחשפה:_ב.מ.וו_סדרה_3_החדשה/
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-3-החדשה-2023-בישראל-מחיר-290000-שקל
- https://www.auto.co.il/cars/bmw/3-series/

Catalog source URLs already present in JSON:
- [0] iCar: ב.מ.וו סדרה 3 יד שניה דור 4 (1998 - 2005) - מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שניה_דור_4/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar: ב.מ.וו סדרה 3 יד שניה דור 5 (2005 - 2011) - מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שניה_דור_5/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Cartube: ב.מ.וו סדרה 3 החדשה 2015 בישראל – מחירים החל מ-240,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-3-החדשה-2015-בישראל-מחירים-החל-מ-240-000-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [3] Cartube: ב.מ.וו סדרה 3 החדשה 2019 בישראל - מחיר החל מ- 289,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-3-החדשה-2019-בישראל-מחיר-החל-מ-289,000-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']

### Required specific Codex edits
- V03 2019-null 258 כ״ס: אסור להשאיר year_end=null. לקבוע year_end לכל המאוחר 2022, או להעביר ל-review אם אין מקור ישראלי שמראה שיווק בפועל עד 2022.
- V02 2015-2019 252 כ״ס: לאחד/לסמן trim Sport/Luxury רק אם המקור מציין. אחרת null סביר כי 330i הוא דגם מנוע.
- V00/V01 היסטוריים: להשאיר רק אם iCar דור 4/5 תומך 231/258 כ״ס ושנות דגם; לא להאריך מעבר לדור.
- available_values_for_website לא יכיל null; אם אין trim, הרשימה ריקה.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 94. BMW 335i
Priority: **בינוני**

Verdict: **בעיקר תקין, אבל צריך לוודא פיצול דור/מרכב ולא למתוח סדאן אחד על שני דורות בלי מקור.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L i6 turbo'; engine_displacement_l=3.0; horsepower_hp=306; transmission='automatic'; drivetrain='RWD'; year_start=2006; year_end=2015; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='3.0L i6 turbo'; engine_displacement_l=3.0; horsepower_hp=306; transmission='automatic'; drivetrain='RWD'; year_start=2007; year_end=2013; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='3.0L i6 turbo'; engine_displacement_l=3.0; horsepower_hp=306; transmission='automatic'; drivetrain='RWD'; year_start=2007; year_end=2014; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- iCar/Auto מקורות קטלוגיים ישראליים תומכים ב-335i סדאן/קופה/קבריולה עם 3.0 טורבו 306 כ״ס.
- 335i הוחלף ב-340i סביב מתיחת הפנים של סדרה 3 ב-2015; אין לשמר 335i אחרי 2015.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שנייה_10/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שנייה_46/
- https://www.auto.co.il/model/bmw-3-series-coupe_g24
- https://www.auto.co.il/model/bmw-3-series-cabriolet_g25

Catalog source URLs already present in JSON:
- [0] iCar: ב.מ.וו סדרה 3 (2006 - 2011) - מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שנייה_10/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] iCar: ב.מ.וו סדרה 3 (2012 - 2019) - מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שנייה_46/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_end']
- [2] Auto.co.il: ב.מ.וו סדרה 3 קופה (2007 - 2013) מחירון רכב, מפרט טכני — https://www.auto.co.il/model/bmw-3-series-coupe_g24 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [3] Auto.co.il: ב.מ.וו סדרה 3 קבריולה (2007 - 2014) מחירון רכב, מפרט טכני — https://www.auto.co.il/model/bmw-3-series-cabriolet_g25 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00 Sedan 2006-2015: אם המקורות מבחינים בין E90 2006-2011 ו-F30 2012-2015, עדיף לפצל; אם כל השדות זהים, אפשר להשאיר טווח אחד עם מקורות לשני הדורות.
- V01/V02 קופה/קבריולה: לשמור year_end 2013/2014 רק אם Auto תומך; לא להעתיק year_end של סדאן.
- version_or_trim=null תקין לדגם מנוע 335i, לא לסמן כחסר.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 95. BMW 340i
Priority: **גבוה מאוד**

Verdict: **לתקן זהות M340i ולבדוק שורת AWD הישנה.**

### Current catalog variants
- V00: version_or_trim='Luxury'; body_type='Sedan'; fuel_type='petrol'; engine='3.0L turbo i6'; engine_displacement_l=3; horsepower_hp=326; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2015; year_end=2018; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L turbo i6'; engine_displacement_l=3; horsepower_hp=326; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2015; year_end=2018; support_level='indirect'; missing_grounded_fields=['version_or_trim']
- V02: version_or_trim='M-Performance'; body_type='Sedan'; fuel_type='mild_hybrid'; engine='3.0L turbo i6'; engine_displacement_l=3; horsepower_hp=374; transmission='automatic'; drivetrain='AWD'; year_start=2020; year_end=2025; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 2015 ישראל: 340i Luxury אוטו׳ ברשימת דגמי סדרה 3 המחודשת, לצד 330i.
- Cartube 04.02.2021: חדש בישראל M340i xDrive, מנוע B58 3.0 שישה צילינדרים, mild-hybrid 48V, 374 כ״ס, 8AT, xDrive.
- Auto.co.il 2021: M340i xDrive M-Performance, שנת השקת הדגם בישראל 2021.
- Auto.co.il 2026: סדרה 3 current בישראל היא 330e בלבד, לכן M340i לא בהכרח current 2026.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/2015-ב-מ-וו-סדרה-3-החדשה-בישראל-–-מחיר-החל-מ-240-אלף-שקל
- https://www.cartube.co.il/חדשות-רכב/חדש-בישראל-2021-ב-מ-וו-318i-ודגם-הביצועים-m340i
- https://www.auto.co.il/cars/bmw/3-series/2021/529605/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_3/ב.מ.וו_סדרה_3_יד_שניה_ד12/version24136/
- https://www.auto.co.il/cars/bmw/3-series/

Catalog source URLs already present in JSON:
- [0] BMW Israel: BMW 3 Series Saloon (F30) LCI catalogue / technical data PDF — https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/Catalogues/New_Catalogues_17.4.18/BMW%203%20Series%20Saloon/BMW%203%20Series%20Saloon%20%28F30%29%20LCI%20-%20Sales%20literature%20-%20Catalogue%20-%20Aug.%202017%20en%201.compressed.pdf?audiences=%7B%7BCAMPAIGN_NAME%7D%7D&creative=%7B%7BCREATIVE_NAME%7D%7D&description=views — supports=['body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'year_start', 'year_end']
- [1] BMW Israel: BMW 3 Series Saloon (F30) LCI catalogue technical table — https://www.bmw.co.il/content/dam/bmw/marketIL/bmw_co_il/Catalogues/New_Catalogues_17.4.18/BMW%203%20Series%20Saloon/BMW%203%20Series%20Saloon%20%28F30%29%20LCI%20-%20Sales%20literature%20-%20Catalogue%20-%20Aug.%202017%20en%201.compressed.pdf?audiences=%7B%7BCAMPAIGN_NAME%7D%7D&creative=%7B%7BCREATIVE_NAME%7D%7D&description=views — supports=['engine_displacement_l', 'horsepower_hp', 'drivetrain']
- [2] auto.co.il: BMW 3 Series 2017 340i Luxury used-car technical page — https://www.auto.co.il/cars/bmw/3-series/2017/529626/ — supports=['version_or_trim', 'engine', 'engine_displacement_l', 'transmission', 'year_start', 'year_end']
- [3] BMW Israel: BMW 3 Series Sedan (G20) technical data - M340i xDrive — https://www.bmw.co.il/he/All-Models/3-series/3-series-sedan/bmw-3-series-sedan-technical-data.html — supports=['body_type', 'fuel_type', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'engine']
- [4] iCar: BMW 3 Series 2021 M340i xDrive M-Performance used-car technical page — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_3_%D7%99%D7%93_%D7%A9%D7%A0%D7%99%D7%94_%D7%9312/version24136/ — supports=['version_or_trim', 'horsepower_hp', 'year_start', 'year_end']

### Required specific Codex edits
- V02 לא שייך תחת model=340i. לפצל/לשנות למודל BMW M340i או BMW M340i xDrive; version_or_trim יכול להיות M-Performance, לא “M-Performance” תחת 340i רגיל.
- V02 year_start צריך להיות 2021 לפי Auto/Cartube, לא 2020, אלא אם יש מקור ישראלי ישיר לשיווק ב-2020.
- V02 year_end=2025 רק אם iCar דף 2020-2025 תומך. לא להאריך ל-2026 בלי מקור current.
- V01 AWD 2015-2018 support_level=indirect: להעביר ל-review אם אין מקור ישראלי רשמי ל-340i xDrive F30.
- V00 Luxury RWD 2015-2018 נראה סביר לפי Cartube/BMW IL, להשאיר עם field_sources מלאים.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 96. BMW 420i
Priority: **גבוה**

Verdict: **השדות הטכניים סבירים, אבל version_or_trim=M-Sport לכל השנים חשוד ומוגזם.**

### Current catalog variants
- V00: version_or_trim='M-Sport'; body_type='Coupe'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=184; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2013; year_end=2026; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim='M-Sport'; body_type='Liftback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=184; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2026; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim='M-Sport'; body_type='Convertible'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=184; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2026; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 02.12.2020: סדרה 4 קופה החדשה בישראל עם 420i 184 כ״ס ועד M440i 374 כ״ס, כסטנדרט חבילת M-Sport בדור החדש.
- Cartube 08.11.2021: סדרה 4 גראן קופה החדשה בישראל בשלב זה 420i בלבד, 184 כ״ס, 8AT.
- Cartube 26.05.2021: קבריולט חדשה בישראל; 420i קבריולט M-Sport.
- Auto/BMW current 2026 מציגים 420i Coupe Style ו-M-Sport, ו-420i Convertible M-Sport.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-4-החדשה-2021-בישראל-מחיר-425000-שקל
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-4-גראן-קופה-החדשה-2022-בישראל-מחיר-425000-שקל
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-4-קבריולט-החדשה-2021-בישראל-מחיר-460000-שקל
- https://www.bmw.co.il/he/All-Models/4-series/4-series-coupe/bmw-4-series-coupe.html
- https://www.auto.co.il/cars/bmw/4-series/

Catalog source URLs already present in JSON:
- [0] iCar: ב.מ.וו סדרה 4 קופה - מחירון, מפרטים, רמות גימור — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_4/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] Cartube: ב.מ.וו סדרה 4 קופה החדשה 2021 בישראל - מחיר החל מ- 425,000 שקלים — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-4-%D7%A7%D7%95%D7%A4%D7%94-%D7%94%D7%97%D7%93%D7%A9%D7%94-2021-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-425-000-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_end']
- [2] Auto.co.il: ב.מ.וו סדרה 4 גראן קופה - מפרט טכני — https://www.auto.co.il/model/bmw-4-series-gran-coupe_g542 — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [3] iCar: ב.מ.וו סדרה 4 קבריולה - מחירון ומידע — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_4_%D7%A7%D7%91%D7%A8%D7%99%D7%95%D7%9C%D7%94/ — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- לא להשאיר version_or_trim=M-Sport לכל 2013-2026. בדור הישן 2013-2020 צריך מקור נפרד לרמת גימור; אחרת version_or_trim=null/או trim אמיתי מהמקור.
- בדור החדש: Coupe current מפוצל Style/M-Sport; Convertible M-Sport; Gran Coupe current כנראה 420i M-Sport בלבד.
- לשמור body_type נפרד Coupe/Liftback/Convertible; לא לערבב בגרסה אחת.
- year_end=2026 תקין רק למרכבים שעדיין מופיעים במקורות current; אם Gran Coupe לא מופיע ב-current, לקבוע לפי Auto/iCar.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 97. BMW 428i
Priority: **בינוני**

Verdict: **כנראה תקין; לוודא שהחלפה ל-430i ב-2016/2017 נעולה.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=245; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2013; year_end=2016; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=245; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2016; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Liftback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=245; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2016; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 2013/2014 ישראל: סדרה 4 הושקה בישראל עם 428i בקופה, קבריולט וגראן קופה, 2.0 טורבו 245 כ״ס.
- ב-2016/2017 דגמי 430i החליפו את 428i לאחר מתיחת פנים/שינוי שמות.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-4-נוחתת-בישראל-החל-מ-330,000-שקל
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-4-קבריולט-בישראל-מחיר-החל-מ-415,000-שקל
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-4-גראן-קופה-בישראל-מחיר-החל-מ-345-000-שקל

Catalog source URLs already present in JSON:
- [0] Cartube.co.il: ב.מ.וו סדרה 4 נוחתת בישראל: החל מ-330,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-4-%D7%A0%D7%95%D7%97%D7%AA%D7%AA-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%94%D7%97%D7%9C-%D7%9E-330,000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] Cartube.co.il: ב.מ.וו סדרה 4 קבריולט בישראל - מחיר החל מ- 415,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-4-%D7%A7%D7%91%D7%A8%D7%99%D7%95%D7%9C%D7%98-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-415,000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [2] Cartube.co.il: ב.מ.וו סדרה 4 גראן קופה בישראל – מחיר החל מ- 345,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-4-%D7%92%D7%A8%D7%90%D7%9F-%D7%A7%D7%95%D7%A4%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-345-000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [3] iCar: ב.מ.וו סדרה 4 החדשה - מחירון, מבחנים ומפרטים — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_4/ — supports=['body_type', 'year_end', 'engine_displacement_l']

### Required specific Codex edits
- להשאיר 428i רק עד 2016 אם המקור תומך; לא להאריך לתוך שנות 430i.
- version_or_trim=null תקין אם אין trim שיווקי נפרד מעבר לדגם מנוע 428i.
- לוודא Coupe 2013, Convertible/Liftback 2014 לפי כתבות ההשקה.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 98. BMW 430i
Priority: **גבוה**

Verdict: **לתקן version_or_trim ולבדוק Gran Coupe current; חלק מהשורות רחבות מדי.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=252; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2016; year_end=2020; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='Liftback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=252; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2016; year_end=2020; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V02: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=252; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2016; year_end=2020; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V03: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=258; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2020; year_end=2022; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V04: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=258; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2021; year_end=2022; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V05: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=245; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2022; year_end=2026; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V06: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=245; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2022; year_end=2026; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V07: version_or_trim=None; body_type='Liftback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=245; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2021; year_end=2026; support_level='direct'; missing_grounded_fields=['version_or_trim']

### Web evidence already researched by ChatGPT
- Cartube 2017 ישראל: סדרה 4 המחודשת עם 420i/430i/440i; 430i 2.0 טורבו 252 כ״ס.
- Auto current 2026 סדרה 4: Coupe/Convertible כוללים 430i M-Shadow; 420i Style/M-Sport; M440i xDrive M-Sport Pro.
- Auto current גראן קופה מציג גרסה אחת 420i M-Sport — לכן 430i Liftback עד 2026 חשוד.
- Cartube/מידע גלובלי 2022 מציין 430i גראן קופה 245 כ״ס אבל לא בהכרח שיווק ישראלי.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-4-החדשה-2017-בישראל-מחיר-367500-שקל
- https://www.auto.co.il/cars/bmw/4-series/
- https://www.auto.co.il/cars/bmw/4-series-gran-coupe/
- https://www.bmw.co.il/he/All-Models/4-series/4-series-coupe/bmw-4-series-coupe.html
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_4/ב.מ.וו_סדרה_4_חדש/version27901/

Catalog source URLs already present in JSON:
- [0] iCar: ב.מ.וו סדרה 4 דור 1 (2014-2020) - מפרט טכני מלא — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_4/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] Cartube: ב.מ.וו סדרה 4 קופה החדשה 2020 בישראל - מחיר החל מ- 425,000 שקלים — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-4-%D7%A7%D7%95%D7%A4%D7%94-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-425000-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Cartube: ב.מ.וו סדרה 4 גראן קופה החדשה 2021 בישראל - מחיר החל מ- 385,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-4-%D7%92%D7%A8%D7%90%D7%9F-%D7%A7%D7%95%D7%A4%D7%94-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-385000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [3] Cartube: ב.מ.וו סדרה 4 קבריולה החדשה בישראל - מחיר החל מ- 460,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-4-%D7%A7%D7%91%D7%A8%D7%99%D7%95%D7%9C%D7%94-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-460000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [4] iCar: ב.מ.וו סדרה 4 (2020+) - מפרט טכני עדכני — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_4/ — supports=['horsepower_hp', 'year_start', 'year_end', 'engine', 'engine_displacement_l', 'transmission', 'drivetrain']

### Required specific Codex edits
- V00-V02 2016-2020 252 כ״ס: להשאיר אם מקורות תומכים; להוסיף/לנקות trim לפי המקור.
- V03/V04 2020-2022 258 כ״ס: לא להאריך מעבר למקור; לרמות 2021 לבדוק M-Sport Pro/M-Superior לפי מרכב.
- V05/V06 2022-2026 245 כ״ס: לשמור Coupe/Convertible current רק עם trim M-Shadow ומקורות current.
- V07 Liftback 2021-2026 245 כ״ס: חשוד. אם המקור הישראלי current לגראן קופה מציג רק 420i, לא להשאיר עד 2026; להעביר ל-review או לקצר לשנים שמקור ישראלי תומך.
- לא להשאיר version_or_trim=null עם missing בכל 8 השורות; לתקן ל-M-Shadow/M-Sport Pro/Style וכו׳ לפי source.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 99. BMW 435i
Priority: **בינוני**

Verdict: **כנראה תקין היסטורית.**

### Current catalog variants
- V00: version_or_trim='Luxury'; body_type='Coupe'; fuel_type='petrol'; engine='3.0L turbo inline-6'; engine_displacement_l=3.0; horsepower_hp=306; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2013; year_end=2016; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim='Luxury'; body_type='Liftback'; fuel_type='petrol'; engine='3.0L turbo inline-6'; engine_displacement_l=3.0; horsepower_hp=306; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2016; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim='Luxury'; body_type='Convertible'; fuel_type='petrol'; engine='3.0L turbo inline-6'; engine_displacement_l=3.0; horsepower_hp=306; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2014; year_end=2016; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Auto/iCar/Cartube תומכים ב-435i דור ראשון סדרה 4 עם 3.0 טורבו 306 כ״ס, קופה/גראן קופה/קבריולה, לפני החלפת השם ל-440i.

### URLs / offline evidence package for Codex
- https://www.auto.co.il/cars/bmw/4-series/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_4/

Catalog source URLs already present in JSON:
- [0] Auto.co.il: ב.מ.וו סדרה 4 (2013-2020) מחירון ומפרטים - אוטו — https://www.auto.co.il/model/bmw-4-series_g1178 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar: ב.מ.וו סדרה 4 קופה 435i אוט' Luxury 2013-2016 - מפרט טכני — https://www.icar.co.il/bmw/4-series-coupe — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [2] KML: מחירון ומפרט טכני ב.מ.וו סדרה 4 גראן קופה 435i 2014-2016 — https://kml.co.il/Car/bmw_4-series-gran-coupe_2014-2016 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [3] KML: מחירון ומפרט טכני ב.מ.וו סדרה 4 קבריולט 435i 2014-2016 — https://kml.co.il/Car/bmw_4-series-convertible_2014-2016 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']

### Required specific Codex edits
- לשמור 2013/2014-2016 בלבד.
- version_or_trim=Luxury תקין רק אם מקור ספציפי מציין Luxury לכל מרכב; אם לא, לשים null או לפצל.
- לא לערבב עם 440i או M440i.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 100. BMW 440i
Priority: **גבוה מאוד**

Verdict: **לתקן זהות M440i; שורות 374 כ״ס לא צריכות להיות 440i רגיל.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='3.0L turbo'; engine_displacement_l=3.0; horsepower_hp=326; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2016; year_end=2020; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='3.0L turbo'; engine_displacement_l=3.0; horsepower_hp=326; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2016; year_end=2020; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Liftback'; fuel_type='petrol'; engine='3.0L turbo'; engine_displacement_l=3.0; horsepower_hp=326; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2016; year_end=2020; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Coupe'; fuel_type='mild_hybrid'; engine='3.0L turbo'; engine_displacement_l=3.0; horsepower_hp=374; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2020; year_end=2026; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim=None; body_type='Convertible'; fuel_type='mild_hybrid'; engine='3.0L turbo'; engine_displacement_l=3.0; horsepower_hp=374; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2021; year_end=2026; support_level='direct'; missing_grounded_fields=[]
- V05: version_or_trim=None; body_type='Liftback'; fuel_type='mild_hybrid'; engine='3.0L turbo'; engine_displacement_l=3.0; horsepower_hp=374; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2021; year_end=2026; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 2017 ישראל: 440i עם 3.0 טורבו 326 כ״ס בדור F32/F33/F36 המחודש.
- Cartube/BMW/Auto current: M440i xDrive Coupe/Convertible עם 3.0 טורבו 374 כ״ס, 8AT, AWD, M-Sport Pro, current 2026.
- iCar/Auto גראן קופה current לא בהכרח תומך M440i Gran Coupe בישראל; current Gran Coupe נראה 420i בלבד.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-4-החדשה-2017-בישראל-מחיר-367500-שקל
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-4-החדשה-2021-בישראל-מחיר-425000-שקל
- https://www.bmw.co.il/he/All-Models/4-series/4-series-coupe/bmw-4-series-coupe.html
- https://www.auto.co.il/cars/bmw/4-series/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_4/ב.מ.וו_סדרה_4_חדש/version27902/

Catalog source URLs already present in JSON:
- [0] iCar: ב.מ.וו סדרה 4 (2014-2020) - מפרט טכני מלא | iCar — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_4_קופה/דור_1/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] Cartube: ב.מ.וו סדרה 4 קופה וקבריולה החדשה 2021 בישראל | Cartube — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-4-החדשה-2021-בישראל-מחיר-החל-מ-425000-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Cartube: ב.מ.וו סדרה 4 גראן קופה החדשה 2022 בישראל | Cartube — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-4-גראן-קופה-החדשה-2022-בישראל-מחיר-החל-מ-385000-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00-V02 326 כ״ס 2016-2020: להשאיר תחת 440i רגיל אם מקורות תומכים.
- V03/V04/V05 374 כ״ס mild-hybrid AWD: לפצל למודל/קנוני M440i xDrive, לא 440i. version_or_trim צריך להיות M-Sport Pro או trim מקור; לא null.
- V03 Coupe year_start=2020 סביר לפי השקת קופה דצמבר 2020; V04 Convertible year_start=2021 סביר; V05 Liftback 2021-2026 דורש מקור ישראלי ספציפי לגראן קופה M440i, אחרת review/קיצור.
- year_end=2026 תקין לקופה/קבריולט על בסיס BMW/Auto current.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 101. BMW 518i
Priority: **נמוך-בינוני**

Verdict: **נראה היסטורי תקין, צריך רק למנוע false missing/trim.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.8L'; engine_displacement_l=1.8; horsepower_hp=113; transmission='manual'; drivetrain='RWD'; year_start=1990; year_end=1993; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.8L'; engine_displacement_l=1.8; horsepower_hp=113; transmission='automatic'; drivetrain='RWD'; year_start=1990; year_end=1993; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.8L'; engine_displacement_l=1.8; horsepower_hp=115; transmission='manual'; drivetrain='RWD'; year_start=1994; year_end=1996; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='1.8L'; engine_displacement_l=1.8; horsepower_hp=115; transmission='automatic'; drivetrain='RWD'; year_start=1994; year_end=1996; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- מקורות קטלוגיים Auto/iCar לקו E34 תומכים ב-518i 1.8, 113/115 כ״ס, ידני/אוטומטי, 1990-1996.

### URLs / offline evidence package for Codex
- https://www.auto.co.il/model/bmw-5-series_g208
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/

Catalog source URLs already present in JSON:
- [785] Auto.co.il: ב.מ.וו סדרה 5 (1988-1996) מפרט טכני — https://www.auto.co.il/catalog/bmw/5-series — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [786] KML Israel: מחירון רכב קמ''ל - ב.מ.וו סדרה 5 1988-1996 (דגמי 518i) — https://www.kml.co.il/car/BMW/5-Series/1988-1996 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start', 'year_end']

### Required specific Codex edits
- להשאיר רק אם המקורות המקומיים תומכים בשתי תיבות ההילוכים.
- version_or_trim=null תקין בדגם מנוע היסטורי; לא לסמן כחסר.
- לוודא year_start/year_end לפי דור E34 ולא לפי שנת ייצור גלובלית בלבד.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 102. BMW 520d
Priority: **בינוני**

Verdict: **כנראה תקין, אבל לא להאריך אחרי 2020.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=177; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2008; year_end=2010; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=184; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2010; year_end=2016; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='diesel'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=190; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2017; year_end=2020; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- סדרה 5 דיזל 520d הופיעה בדורות E60/F10/G30; אין במקורות current 2024-2026 שיווק 520d בישראל.
- Cartube 2020 מציין דיזל/בנזין גלובלי במתיחת פנים, אך current ישראל 2026 מתמקד ב-520i/530e.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/
- https://www.cartube.co.il/חדשות-רכב/מתיחת-פנים-ב-מ-וו-סדרה-5-החדשה-2020

Catalog source URLs already present in JSON:
- [516] iCar: ב.מ.וו סדרה 5 (2010-2017) 520d - מפרט טכני — https://www.icar.co.il/bmw/5_series/f10/specs/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [517] Cartube: ב.מ.וו סדרה 5 החדשה בישראל - מחיר החל מ-390,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-5-החדשה-בישראל-מחיר-החל-מ-390000-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [518] iCar: ב.מ.וו סדרה 5 (2004-2010) - מפרט טכני — https://www.icar.co.il/bmw/5_series/e60/specs/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- להשאיר V00-V02 רק עד 2020 אם iCar/Auto תומכים.
- אין להוסיף 520d mild-hybrid 2021+ ללא מקור ישראלי מפורש.
- version_or_trim=null תקין אם אין trim מקומי נפרד.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 103. BMW 520i
Priority: **גבוה**

Verdict: **לתקן current 2024+ ולהוסיף trim; V00 רחבה מדי אבל סבירה אם מקורות מכסים.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=184; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2010; year_end=2023; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='mild_hybrid'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=208; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2024; year_end=None; support_level='direct'; missing_grounded_fields=['year_end']

### Web evidence already researched by ChatGPT
- Cartube/Auto 2024: סדרה 5 החדשה G60 בישראל — 520i הצטרפה במרץ 2024, 2.0 טורבו 208 כ״ס, mild hybrid, 8AT, RWD.
- BMW Israel official 04/2026: 520i M-Sport SE מחירון 2026.
- Auto.co.il 2026: 520i 2.0 טורבו היברידי מתון M-Sport, שנת השקת דגם בישראל 2024.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/component/tags/tag/ב-מ-וו-סדרה-5
- https://www.auto.co.il/articles/car-news/local-news/137122/
- https://www.auto.co.il/cars/bmw/5-series/2026/581218/
- https://www.bmw.co.il/he/All-Models/5-series/sedan/bmw-5-series-sedan-overview.html
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/ב.מ.וו_סדרה_5_חדש/version27799/

Catalog source URLs already present in JSON:
- [0] iCar: ב.מ.וו סדרה 5 (2017-2023) - מפרט טכני — https://www.icar.co.il/bmw/bmw_5_series/bmw_5_series_spec/ — supports=['year_start', 'year_end', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain']
- [1] Auto.co.il: ב.מ.וו סדרה 5 2010-2016 - מפרט טכני — https://www.auto.co.il/model/bmw-5-series_g258 — supports=['year_start', 'year_end', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain']
- [2] Cartube: החל מ-469,000 שקל: ב.מ.וו סדרה 5 החדשה 2024 בישראל — https://www.cartube.co.il/חדשות-רכב/החל-מ-469-000-שקל-ב-מ-וו-סדרה-5-החדשה-2024-בישראל — supports=['year_start', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain']

### Required specific Codex edits
- V01 2024-null 208 כ״ס: לעדכן year_end=2026 ולשים version_or_trim לפי מקור: M-Sport SE/BMW official או M-Sport/Auto-iCar.
- V00 2010-2023 184 כ״ס: לבדוק אם הוא מאחד F10/G30. אם כן, להשאיר רק אם שני הדורות עם אותם שדות או לפצל לשני טווחים.
- לא לסמן year_end חסר ל-V01 אחרי עיגון ב-BMW/Auto 2026.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 104. BMW 523i
Priority: **בינוני**

Verdict: **היסטורי, בעיקר לבדוק כפילויות trim/null.**

### Current catalog variants
- V00: version_or_trim='Executive'; body_type='Sedan'; fuel_type='petrol'; engine='2.5L i6'; engine_displacement_l=2.5; horsepower_hp=170; transmission='automatic'; drivetrain='RWD'; year_start=1996; year_end=2000; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.5L i6'; engine_displacement_l=2.5; horsepower_hp=170; transmission='manual'; drivetrain='RWD'; year_start=1996; year_end=2000; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim='Executive'; body_type='Sedan'; fuel_type='petrol'; engine='2.5L i6'; engine_displacement_l=2.5; horsepower_hp=177; transmission='automatic'; drivetrain='RWD'; year_start=2005; year_end=2007; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim='Executive'; body_type='Sedan'; fuel_type='petrol'; engine='2.5L i6'; engine_displacement_l=2.5; horsepower_hp=190; transmission='automatic'; drivetrain='RWD'; year_start=2007; year_end=2010; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim='Luxury'; body_type='Sedan'; fuel_type='petrol'; engine='2.5L i6'; engine_displacement_l=2.5; horsepower_hp=204; transmission='automatic'; drivetrain='RWD'; year_start=2010; year_end=2011; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- המעבר מ-523i ל-520i/528i בשנות 2010 נתמך במחירי BMW ישראל/Cartube 2013; 523i לא current.
- מקורות Auto/iCar צריכים לתמוך בדורות E39/E60/F10 המוקדמים.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/מהפכת-המחירים-של-ב-מ-וו-ומיני-בישראל
- https://www.auto.co.il/model/bmw-5-series_g209
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/

Catalog source URLs already present in JSON:
- [179] auto.co.il: ב.מ.וו סדרה 5 (E39) מפרט טכני וגרסאות (1996-2003) — https://www.auto.co.il/model/bmw-5-series-e39 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [513] icar.co.il: ב.מ.וו סדרה 5 E60 (2004-2010) - מפרט טכני — https://www.icar.co.il/bmw/5_series/e60 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [514] kml.co.il: ב.מ.וו 523i מפרט טכני - שנתונים 2010-2011 — https://kml.co.il/car/bmw/5-series/523i — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']

### Required specific Codex edits
- לוודא שהשורות Executive/null 1996-2000 אינן כפולות עבור אותה גרסה. אם מקור לא מבחין trim, לא ליצור שתי שורות זהות רק בגלל null/Executive.
- V04 Luxury 2010-2011 204 כ״ס: לבדוק שהשם Luxury קיים במקור; אחרת trim=null.
- לא להאריך מעבר 2011.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 105. BMW 525i
Priority: **בינוני**

Verdict: **היסטורי סביר; לוודא דורות ושמות trim.**

### Current catalog variants
- V00: version_or_trim='Business'; body_type='Sedan'; fuel_type='petrol'; engine='2.5L i6'; engine_displacement_l=2.5; horsepower_hp=218; transmission='automatic'; drivetrain='RWD'; year_start=2005; year_end=2010; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.5L i6'; engine_displacement_l=2.5; horsepower_hp=192; transmission='automatic'; drivetrain='RWD'; year_start=2003; year_end=2005; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.5L i6'; engine_displacement_l=2.5; horsepower_hp=192; transmission='automatic'; drivetrain='RWD'; year_start=2000; year_end=2003; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.5L i6'; engine_displacement_l=2.5; horsepower_hp=192; transmission='automatic'; drivetrain='RWD'; year_start=1990; year_end=1995; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- iCar/Auto אמורים לתמוך ב-525i E34/E39/E60 עם 2.5 ליטר, 192/218 כ״ס לפי שנים.
- אין קשר לדגמי 525d או 530i; לא לערבב.

### URLs / offline evidence package for Codex
- https://www.auto.co.il/model/bmw-5-series_g208
- https://www.auto.co.il/model/bmw-5-series_g209
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/

Catalog source URLs already present in JSON:
- [0] iCar Israel: ב.מ.וו סדרה 5 E60 (2003-2010) - מחירון רכב, מפרט טכני - iCar — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/ב.מ.וו_סדרה_5_יד_שנייה_1/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [1] iCar Israel: ב.מ.וו סדרה 5 E39 (1996-2003) - מפרט טכני ומחירון - iCar — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/ב.מ.וו_סדרה_5_יד_שנייה_2/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Auto.co.il: ב.מ.וו סדרה 5 1988-1995 E34 מפרט טכני - Auto.co.il — https://www.auto.co.il/catalog/bmw/5-series/g51 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- לבדוק V00 Business 2005-2010: אם Business לא מופיע במקור, להחליף ל-null או trim אמיתי.
- V01/V02/V03 עם null תקינים אם אלו דגמי מנוע ללא trim שיווקי.
- לוודא שאין חפיפה לא מוצדקת 2000-2003 ו-2003-2005 אם אותו דור/שדות.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 106. BMW 528i
Priority: **בינוני-גבוה**

Verdict: **בעיקר תקין, אבל missing version ב-V00 לא מוצדק אם 528i הוא דגם מנוע.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.8L i6'; engine_displacement_l=2.8; horsepower_hp=193; transmission='5-speed automatic'; drivetrain='RWD'; year_start=1996; year_end=2000; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim='Executive'; body_type='Sedan'; fuel_type='petrol'; engine='3.0L i6'; engine_displacement_l=3.0; horsepower_hp=258; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2010; year_end=2011; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim='Luxury Line'; body_type='Sedan'; fuel_type='petrol'; engine='2.0L turbo i4'; engine_displacement_l=2.0; horsepower_hp=245; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2016; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 2013 מחירון BMW ישראל מציין 528i עם 245 כ״ס כמחליף/מחירון סדרה 5.
- מקורות iCar/Auto תומכים ב-528i 2010-2011 3.0 258 כ״ס וב-2011-2016 2.0 טורבו 245 כ״ס.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/מהפכת-המחירים-של-ב-מ-וו-ומיני-בישראל
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/
- https://www.auto.co.il/cars/bmw/5-series/

Catalog source URLs already present in JSON:
- [0] iCar.co.il: ב.מ.וו סדרה 5 E39 (1996-2003) - מפרט טכני — https://www.icar.co.il/bmw/5_series/d3/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] Auto.co.il: ב.מ.וו סדרה 5 F10 - מחירון, מפרט טכני וחדשות — https://www.auto.co.il/model/bmw-5-series_g204 — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Gear.co.il: ב.מ.וו סדרה 5 528i Luxury Line 2.0 (2012) - מפרט רכב — https://www.gear.co.il/bmw/5_series/2012/528i_luxury_line — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00 1996-2000: אם אין trim נפרד, להסיר missing_grounded_fields=[version_or_trim].
- V01/V02: להשאיר trim Executive/Luxury Line רק אם המקורות תומכים.
- לא למזג 3.0 258 ו-2.0T 245; אלו יחידות שונות.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 107. BMW 530e
Priority: **גבוה מאוד**

Verdict: **לתקן year_end ו-trim לדור 2024+; current 530e מגובה.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='plug_in_hybrid'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=252; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2017; year_end=2020; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='plug_in_hybrid'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=292; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2020; year_end=2023; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='plug_in_hybrid'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=299; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2024; year_end=None; support_level='direct'; missing_grounded_fields=['version_or_trim', 'year_end']

### Web evidence already researched by ChatGPT
- iCar/Auto 2018: 530e 2.0 252 כ״ס Sport/Exclusive בדור G30.
- 2021/2022: 530e התחזק ל-292 כ״ס ונמכר ברמות M-Sport/M-Superior/M-Design SE.
- Cartube 20.05.2024: 530e החדשה בישראל, 299 כ״ס, טווח סביב 100 ק״מ, מחיר החל מ-499,000 ₪.
- iCar/Auto 2026: 530e M-Sport ו-M-Expressive current; Auto current מציין 530e 299 כ״ס לצד 520i.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/ב.מ.וו_סדרה_5_יד_שניה_ד12/version19395/
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-5-פלאג-אין-530e-החדשה-2024-בישראל-מחיר-499000-שקל
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/ב.מ.וו_סדרה_5_חדש/version27898/
- https://www.auto.co.il/cars/bmw/5-series/2026/581219/

Catalog source URLs already present in JSON:
- [0] iCar: ב.מ.וו סדרה 5 פלאג-אין (2017-2020) - מחירון מפרטים — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5_פלאג-אין/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] Cartube: ב.מ.וו סדרה 5 החדשה 2021 בישראל - מחיר החל מ- 480,000 שקלים — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-5-החדשה-2021-בישראל-מחיר-החל-מ-480-000-שקלים — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Cartube: ב.מ.וו 530e החדשה 2024 בישראל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-530e-החדשה-2024-בישראל-מחיר-החל-מ-499,000-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']

### Required specific Codex edits
- V02 2024-null 299 כ״ס: לעדכן year_end=2026 ולפצל/למלא version_or_trim=M-Sport ו-M-Expressive לפי מקורות current.
- V00 2017-2020 252: למלא trims Sport/Exclusive אם רוצים רמת גימור; אחרת אל לסמן version חסר.
- V01 2020-2023 292: למלא M-Sport/M-Superior/M-Design SE אם מקור תומך; לא להשאיר missing version אם האתר לא מחייב trim.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 108. BMW 530i
Priority: **בינוני-גבוה**

Verdict: **לתקן missing trim/לא להאריך אחרי 2023; historical סביר.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L turbo i4'; engine_displacement_l=2.0; horsepower_hp=252; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2017; year_end=2023; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L i6'; engine_displacement_l=3.0; horsepower_hp=272; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2007; year_end=2010; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L i6'; engine_displacement_l=3.0; horsepower_hp=258; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2003; year_end=2007; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V03: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L i6'; engine_displacement_l=3.0; horsepower_hp=231; transmission='5-speed automatic'; drivetrain='RWD'; year_start=2000; year_end=2003; support_level='direct'; missing_grounded_fields=['version_or_trim']

### Web evidence already researched by ChatGPT
- Auto 2018 מציג 530i Sport כגרסה בישראל; iCar מציג 530i 252 כ״ס בדור G30.
- בדור 2024+ current בישראל אין 530i; קיימות 520i ו-530e לפי Auto/BMW/iCar.

### URLs / offline evidence package for Codex
- https://www.auto.co.il/cars/bmw/5-series/2018/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/ב.מ.וו_סדרה_5_יד_שניה_ד12/
- https://www.auto.co.il/cars/bmw/5-series/
- https://www.bmw.co.il/he/All-Models/5-series/sedan/bmw-5-series-sedan-overview.html

Catalog source URLs already present in JSON:
- [0] Cartube: ב.מ.וו סדרה 5 החדשה בישראל - מחיר החל מ-390,000 שקל — https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-5-החדשה-בישראל-מחיר-החל-מ-390,000-שקל — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] iCar: ב.מ.וו סדרה 5 יד שניה (2017 - 2024) מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/ב.מ.וו_סדרה_5_יד_שניה_ד4/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] iCar: ב.מ.וו סדרה 5 יד שניה (2003 - 2010) מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/ב.מ.וו_סדרה_5_יד_שניה_ד2/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [3] iCar: ב.מ.וו סדרה 5 יד שניה (1996 - 2003) מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/ב.מ.וו_סדרה_5_יד_שניה_ד1/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00 2017-2023 252: year_end=2023 נכון; לא להאריך ל-2024+.
- V00 version_or_trim: אם המקור אומר Sport/Exclusive, למלא; אם לא, להסיר missing version.
- V01-V03 historical: להשאיר אם iCar/Auto תומכים, עם פיצול דורות ברור.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 109. BMW 535i
Priority: **גבוה**

Verdict: **לתקן זיהום Series 5 GT/Liftback; שאר ההיסטורי סביר.**

### Current catalog variants
- V00: version_or_trim='Exclusive'; body_type='Sedan'; fuel_type='petrol'; engine='3.0L turbo inline-6'; engine_displacement_l=3.0; horsepower_hp=306; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2010; year_end=2016; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Liftback'; fuel_type='petrol'; engine='3.0L turbo inline-6'; engine_displacement_l=3.0; horsepower_hp=306; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2010; year_end=2017; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.5L v8'; engine_displacement_l=3.5; horsepower_hp=245; transmission='5-speed automatic'; drivetrain='RWD'; year_start=1996; year_end=2003; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.4L inline-6'; engine_displacement_l=3.4; horsepower_hp=211; transmission='4-speed automatic'; drivetrain='RWD'; year_start=1988; year_end=1992; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- 535i סדאן F10 2010-2016 עם 3.0 טורבו 306 כ״ס; iCar/Auto תומכים.
- שורת Liftback 2010-2017 היא בפועל BMW 5 Series GT / 535i GT, לא סדאן רגילה; זה מזהם את מודל 535i אם האתר לא מציג GT בנפרד.
- דורות E34/E39 535i היסטוריים תומכים ב-3.4 I6 / 3.5 V8 לפי מקורות קטלוגיים.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/
- https://www.auto.co.il/model/bmw-5-series_g209
- https://www.auto.co.il/cars/bmw/5-series/

Catalog source URLs already present in JSON:
- [0] iCar: ב.מ.וו סדרה 5 2010-2016 (F10) - מפרט טכני — https://www.icar.co.il/bmw/5_series/f10/specs/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end', 'version_or_trim']
- [1] Auto.co.il: ב.מ.וו סדרה 5 GT (F07) מפרט טכני — https://www.auto.co.il/model/bmw-5-series-gt_g117 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] iCar: ב.מ.וו סדרה 5 1996-2003 (E39) - מפרט טכני — https://www.icar.co.il/bmw/5_series/e39/specs/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [3] iCar: ב.מ.וו סדרה 5 1988-1996 (E34) - מפרט טכני — https://www.icar.co.il/bmw/5_series/e34/specs/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V01 Liftback: לפצל למודל BMW 535i GT / Series 5 GT או להעביר ל-review. לא להשאיר תחת 535i Sedan אם אין הבחנה באתר.
- V00 Exclusive Sedan: להשאיר אם trim Exclusive מגובה.
- V02/V03: לוודא מנוע/נפח/כ״ס עם Auto/iCar; אם כן לשמור.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 110. BMW 540i
Priority: **בינוני-גבוה**

Verdict: **סביר, אבל לוודא 333 mild-hybrid ו-year_end=2023; לא להאריך ל-G60.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='4.0L v8'; engine_displacement_l=4.0; horsepower_hp=286; transmission='5-speed automatic'; drivetrain='RWD'; year_start=1992; year_end=1996; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='4.4L v8'; engine_displacement_l=4.4; horsepower_hp=286; transmission='5-speed automatic'; drivetrain='RWD'; year_start=1996; year_end=2003; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='4.0L v8'; engine_displacement_l=4.0; horsepower_hp=306; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2005; year_end=2010; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L turbo'; engine_displacement_l=3.0; horsepower_hp=340; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2017; year_end=2020; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim=None; body_type='Sedan'; fuel_type='mild_hybrid'; engine='3.0L turbo'; engine_displacement_l=3.0; horsepower_hp=333; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2020; year_end=2023; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube 2017 ישראל: סדרה 5 החדשה כוללת 540i 3.0 טורבו 340 כ״ס.
- Cartube 2020 מתיחת פנים גלובלית מציין 540i עם 333 כ״ס ומערכת mild-hybrid; צריך מקור ישראלי/קטלוגי לשיווק בפועל.
- current 2024-2026 Series 5 בישראל לא מציג 540i, אלא 520i/530e.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-5-החדשה-2017-בישראל-מחיר-החל-מ-480-000-שקל
- https://www.cartube.co.il/חדשות-רכב/מתיחת-פנים-ב-מ-וו-סדרה-5-החדשה-2020
- https://www.auto.co.il/cars/bmw/5-series/2018/
- https://www.auto.co.il/cars/bmw/5-series/

Catalog source URLs already present in JSON:
- [0] Cartube: ב.מ.וו סדרה 5 החדשה 2017 בישראל - מחיר החל מ-480,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-5-%D7%94%D7%97%D7%93%D7%A9%D7%94-2017-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-480-000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [1] iCar: ב.מ.וו סדרה 5 (2017-2023) - מחירון מפרטים — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_5/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_5_%D7%97%D7%93%D7%A9/ — supports=['year_end', 'fuel_type', 'horsepower_hp', 'transmission', 'drivetrain']
- [2] iCar: ב.מ.וו סדרה 5 2004-2010 - מחירון מפרטים — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_5/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_5_%D7%99%D7%A9%D7%9F_4/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [3] Auto.co.il: ב.מ.וו סדרה 5 1996-2003 מפרט טכני — https://www.auto.co.il/model/bmw-5-series_g209 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [4] Auto.co.il: ב.מ.וו סדרה 5 דור שלישי (E34) — https://www.auto.co.il/model/bmw-5-series_g208 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V03 2017-2020 340: לשמור אם Auto/iCar/Cartube תומכים.
- V04 2020-2023 333 mild_hybrid: להשאיר רק אם מקור ישראלי/קטלוג ישראלי תומך; אם המקור רק גלובלי, להעביר ל-review או לציין support_level=indirect.
- אין ליצור 540i 2024+ בדור G60 בישראל.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 111. BMW 545e
Priority: **גבוה**

Verdict: **להשלים trim M-Sport או לנעול M-Superior בלבד לפי מקור; שנת התחלה 2021 בסדר בזהירות.**

### Current catalog variants
- V00: version_or_trim='M-Superior'; body_type='Sedan'; fuel_type='plug_in_hybrid'; engine='3.0L turbo'; engine_displacement_l=3.0; horsepower_hp=394; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2021; year_end=2023; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- iCar 07.02.2021 כתב ש-545e xDrive לא הוצעה בישראל בתחילת שיווק מתיחת הפנים; אחר כך 09.09.2021 iCar מציין שיווק 545e בישראל.
- iCar 2022 מציג 545e xDrive M-Sport וגם M-Superior, 3.0 394 כ״ס.
- Auto מבחן 2021 מאשר נוכחות 545e בישראל ומחיר סביב 565-600 אלף ₪.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/רכב_חשמלי/ב.מ.וו:_סדרה_5_מתחדשת,_סדרה_3_מוזלת/
- https://www.icar.co.il/רכב_חשמלי/_ב.מ.וו_סדרה_5_פלאג-אין_מתחזקת/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/ב.מ.וו_סדרה_5_יד_שניה_ד12/version24909/
- https://www.auto.co.il/articles/test-drives/road-tests/134865/

Catalog source URLs already present in JSON:
- [1] iCar: ב.מ.וו 545e פלאג-אין xDrive - מפרט, מחירים, ורמות גימור — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95.%D7%95/%D7%91.%D7%9E.%D7%95.%D7%95_%D7%A1%D7%93%D7%A8%D7%94_5/ — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Gear.co.il: ב.מ.וו סדרה 5 (G30) פלאג אין הייבריד 545e M-Superior 4X4 3.0 — https://gear.co.il/%D7%A8%D7%9B%D7%91%D7%99%D7%9D/%D7%91.%D7%9E.%D7%95.%D7%95-%D7%A1%D7%93%D7%A8%D7%94-5 — supports=['version_or_trim', 'body_type', 'fuel_type', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start']
- [3] Cartube: ב.מ.וו 545e xDrive פלאג-אין - נחשפת רשמית — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-545e-%D7%A4%D7%9C%D7%90%D7%92-%D7%90%D7%99%D7%9F-%D7%A0%D7%97%D7%A9%D7%A4%D7%AA-%D7%A8%D7%A9%D7%9E%D7%99%D7%AA — supports=['engine', 'horsepower_hp', 'transmission', 'drivetrain', 'fuel_type']

### Required specific Codex edits
- V00 M-Superior 2021-2023: לשמור אם מקור תומך.
- אם iCar מציג גם 545e xDrive M-Sport באותן שנים, להוסיף וריאנט M-Sport או לפחות לא לטעון שה-M-Superior היא היחידה.
- year_start=2021 תקין אבל לתעד שהשיווק בפועל החל מאוחר ב-2021; לא 2020.
- אין להאריך אחרי 2023 ללא מקור.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 112. BMW 630i GT
Priority: **בינוני**

Verdict: **כנראה תקין; לוודא מקור ישראלי ולא רק חשיפה גלובלית.**

### Current catalog variants
- V00: version_or_trim='M Sport'; body_type='Liftback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=258; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2017; year_end=2023; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim='Luxury Line'; body_type='Liftback'; fuel_type='petrol'; engine='2.0L turbo'; engine_displacement_l=2.0; horsepower_hp=258; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2017; year_end=2023; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube/Auto 2017 מציינים סדרה 6 GT/Gran Turismo עם 630i 2.0 טורבו 258 כ״ס, 8AT, RWD.
- iCar סדרה 6 GT תומך בשנים ורמות Luxury Line/M Sport עד סביב 2023.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-6-גראן-טוריסמו-החדשה-בישראל-מחיר-החל-מ-545000-שקל
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_6_GT/
- https://www.auto.co.il/articles/car-news/128911/

Catalog source URLs already present in JSON:
- [0] Cartube: ב.מ.וו סדרה 6 גראן טוריסמו החדשה בישראל - מחיר החל מ-545,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-6-%D7%92%D7%A8%D7%90%D7%9F-%D7%98%D7%95%D7%A8%D7%99%D7%A1%D7%9E%D7%95-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-545000-%D7%A9%D7%A7%D7%9C — supports=['version_or_trim', 'year_start', 'horsepower_hp', 'engine', 'engine_displacement_l', 'transmission', 'drivetrain', 'fuel_type']
- [1] iCar: ב.מ.וו סדרה 6 GT - מחירון, מפרטים, אבזור — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_GT/ — supports=['body_type', 'horsepower_hp', 'engine', 'engine_displacement_l', 'transmission', 'drivetrain', 'fuel_type', 'year_start', 'year_end']

### Required specific Codex edits
- לשמור 630i GT רק אם Cartube source אכן כתבת ישראל עם מחיר, לא חשיפה גלובלית בלבד.
- version_or_trim Luxury Line/M Sport: להשאיר רק אם iCar/Cartube תומכים.
- year_end=2023 צריך להיות מגובה ב-iCar; אם לא, year_end=null עם missing או review.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 113. BMW 640i GT
Priority: **גבוה**

Verdict: **לתקן/לאמת 640i GT; לבדוק AWD ו-year_end=2024.**

### Current catalog variants
- V00: version_or_trim='Luxury'; body_type='Liftback'; fuel_type='petrol'; engine='3.0L inline-6 turbo'; engine_displacement_l=3.0; horsepower_hp=340; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2017; year_end=2024; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Cartube/Auto 2017 גלובלי/השקה: 640i GT 3.0 שישה צילינדרים 340 כ״ס, 8AT; ניתן להזמנה גם xDrive.
- Auto 2017 מבחן השקה: GT6 מוצעת 640i עם RWD או AWD, 340 כ״ס, 8AT.
- אם iCar Israel מציג 640i GT Luxury 4X4, זה מקור נקי; אם לא, ה-AWD נשאר חשוד.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-מציגה-2018-סדרה-6-gt-החדשה
- https://www.auto.co.il/articles/car-news/128911/
- https://www.auto.co.il/articles/test-drives/129325/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_6_GT/

Catalog source URLs already present in JSON:
- [0] iCar Israel: ב.מ.וו סדרה 6 GT - מחירון, צריכת דלק, רמות גימור — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_GT/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start', 'year_end', 'version_or_trim']
- [1] Cartube Israel: ב.מ.וו סדרה 6 GT החדשה בישראל - מחיר החל מ- 545,000 שקל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-6-gt-%D7%94%D7%97%D7%93%D7%A9%D7%94-%D7%91%D7%9A%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-545000-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'horsepower_hp', 'transmission', 'drivetrain', 'version_or_trim', 'year_start']

### Required specific Codex edits
- לוודא ש-source URL בקטלוג לא שבור/עם typo; אם Cartube URL לא נפתח, להחליף לכתובת נכונה או למחוק.
- V00 AWD Luxury 2017-2024: להשאיר רק אם iCar ישראל תומך ב-640i GT 4X4 Luxury. אם מקור רק אומר אפשר להזמין xDrive באירופה — review.
- year_end=2024 דורש מקור ישראלי ספציפי. אם iCar לא תומך, לא לנחש.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 114. BMW 650i
Priority: **גבוה מאוד**

Verdict: **לתקן body_type ושנות 407/450; Gran Coupe לא Sedan.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='4.8L v8'; engine_displacement_l=4.8; horsepower_hp=367; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2005; year_end=2010; support_level='direct'; missing_grounded_fields=[]
- V01: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='4.8L v8'; engine_displacement_l=4.8; horsepower_hp=367; transmission='6-speed automatic'; drivetrain='RWD'; year_start=2005; year_end=2010; support_level='direct'; missing_grounded_fields=[]
- V02: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=407; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2012; support_level='direct'; missing_grounded_fields=[]
- V03: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=407; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2012; support_level='direct'; missing_grounded_fields=[]
- V04: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=450; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2012; year_end=2018; support_level='direct'; missing_grounded_fields=[]
- V05: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=450; transmission='8-speed automatic'; drivetrain='AWD'; year_start=2013; year_end=2018; support_level='direct'; missing_grounded_fields=[]
- V06: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=450; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2012; year_end=2018; support_level='direct'; missing_grounded_fields=[]
- V07: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='4.4L v8 turbo'; engine_displacement_l=4.4; horsepower_hp=450; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2012; year_end=2018; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- iCar/Auto תומכים בדור 2004-2011: 650i קופה/קבריולה 4.8 V8 367 כ״ס.
- Auto/Cartube 2011-2018: 650i 4.4 טווין-טורבו, תחילה 407 כ״ס ובהמשך 450 כ״ס.
- Auto 2015: מתיחת פנים סדרה 6 בישראל, 650i 4.4 V8 מייצר 450 כ״ס במקום 407; מחירים לקופה/גראן קופה/קבריולה.
- Auto/Cartube: סדרה 6 גראן קופה היא גרסת ארבע דלתות קופה/Gran Coupe, לא Sedan רגילה.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_6_דגם_2004/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_6_דגם_2011/
- https://www.auto.co.il/articles/car-news/111689/
- https://www.auto.co.il/cars/bmw/6-series-gran-coupe/
- https://www.cartube.co.il/חדשות-רכב/ב-מ-וו-סדרה-6-גראן-קופה-נוחתת-בישראל-מחיר-החל-מ-620-אלף-שקל

Catalog source URLs already present in JSON:
- [0] iCar: ב.מ.וו סדרה 6 (2004-2011) - מפרט טכני — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_%D7%93%D7%92%D7%9D_2004/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar: ב.מ.וו סדרה 6 (2011-2018) - מפרט טכני — https://www.icar.co.il/%D7%91.%D7%9E.%D7%95%D7%95/%D7%91.%D7%9E.%D7%95%D7%95_%D7%A1%D7%93%D7%A8%D7%94_6_%D7%93%D7%92%D7%9D_2011/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] Cartube: ב.מ.וו סדרה 6 גראן קופה נוחתת בישראל — https://www.cartube.co.il/%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%A8%D7%9B%D7%91/%D7%91-%D7%9E-%D7%95%D7%95-%D7%A1%D7%93%D7%A8%D7%94-6-%D7%92%D7%A8%D7%90%D7%9F-%D7%A7%D7%95%D7%A4%D7%94-%D7%A0%D7%95%D7%97%D7%AA%D7%AA-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%97%D7%99%D7%A8-%D7%94%D7%97%D7%9C-%D7%9E-620-%D7%90%D7%9C%D7%A3-%D7%A9%D7%A7%D7%9C — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'year_start']
- [3] Auto.co.il: ב.מ.וו סדרה 6 - אוטו — https://www.auto.co.il/model/bmw-6-series_g250 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V04/V05 body_type=Sedan שגוי. להחליף ל-Gran Coupe/Liftback או לפצל למודל BMW 650i Gran Coupe.
- V02/V03 2011-2012 407 כ״ס ו-V06/V07 2012-2018 450 כ״ס: לבדוק בפועל ממתי 450 בישראל. אם 450 נכנס רק במתיחת פנים 2015, לקצר/לפצל; לא להשאיר 2012-2018 450 אם מקור 2015 סותר.
- V05 AWD Sedan/Gran Coupe: להשאיר xDrive רק אם מקור ישראלי מציין; אחרת review.
- version_or_trim=null תקין אם אין trim, אבל לא להסתיר body_type שגוי.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 115. BMW 728i
Priority: **נמוך-בינוני**

Verdict: **נראה תקין; לעגן עם מקורות ישראליים.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.8L inline-6'; engine_displacement_l=2.8; horsepower_hp=193; transmission='5-speed automatic'; drivetrain='RWD'; year_start=1995; year_end=2001; support_level='direct'; missing_grounded_fields=[]

### Web evidence already researched by ChatGPT
- Auto/iCar דור E38 תומכים ב-728i 2.8 inline-6 193 כ״ס 1995-2001.
- Wheel 2024 נוסטלגיה מאשר ש-728i נמכרה בישראל גם ב-2001 והייתה דגם משמעותי בסדרה 7.

### URLs / offline evidence package for Codex
- https://www.auto.co.il/model/bmw-7-series_g202
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_דור_3/
- https://wheel.co.il/נוסטלגיה-לשבת-ב-מ-וו-סדרה-7-דור-3-e38-סדרה-7-הי/

Catalog source URLs already present in JSON:
- [1] Auto.co.il: ב.מ.וו סדרה 7 (1995-2001) - מחירון רכב, מפרט טכני — https://www.auto.co.il/model/bmw-7-series_g202 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] iCar.co.il: ב.מ.וו סדרה 7 1995 - 2001 - מחירון ומפרט — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_דור_3/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- להשאיר V00 אם Auto/iCar תומכים בשנות 1995-2001, 2.8, 193 כ״ס, 5AT, RWD.
- version_or_trim=null תקין; לא לסמן כחסר.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---

## 116. BMW 730i
Priority: **גבוה**

Verdict: **לתקן פיצול דורות ולקבע 730i/730 בלי לנחש.**

### Current catalog variants
- V00: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='2.0L i4 turbo'; engine_displacement_l=2.0; horsepower_hp=258; transmission='automatic'; drivetrain='RWD'; year_start=2016; year_end=2019; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L i6'; engine_displacement_l=3.0; horsepower_hp=258; transmission='automatic'; drivetrain='RWD'; year_start=2005; year_end=2015; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V02: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L i6'; engine_displacement_l=3.0; horsepower_hp=231; transmission='automatic'; drivetrain='RWD'; year_start=2003; year_end=2005; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V03: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L v8'; engine_displacement_l=3.0; horsepower_hp=218; transmission='automatic'; drivetrain='RWD'; year_start=1994; year_end=1996; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V04: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L i6'; engine_displacement_l=3.0; horsepower_hp=188; transmission='automatic'; drivetrain='RWD'; year_start=1990; year_end=1994; support_level='direct'; missing_grounded_fields=['version_or_trim']

### Web evidence already researched by ChatGPT
- Cartube 2013 מחירון BMW מציין דגם 730 עם 258 כ״ס במחיר 560,000 ₪ — מקור ישראלי לכך ש-730/730i 258 כ״ס שווק.
- iCar 2011 version page מציג 730i 3.0 עם 258 כ״ס.
- iCar/Auto מקורות היסטוריים תומכים בדורות E32/E38/E65/F01/G11, אך לא כולם צריכים להיות שורה אחת.
- Yad2 current אינו מקור קטלוגי חזק, אבל מראה שבשוק ישראלי קיימות גרסאות 730/740 וכו׳; לא להשתמש בו לבדו לשדה נקי.

### URLs / offline evidence package for Codex
- https://www.cartube.co.il/חדשות-רכב/מהפכת-המחירים-של-ב-מ-וו-ומיני-בישראל
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_ד11/version8187/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_ד4/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_ד3/
- https://www.auto.co.il/model/bmw-7-series_g64
- https://www.auto.co.il/model/bmw-7-series_g63

Catalog source URLs already present in JSON:
- [0] iCar: ב.מ.וו סדרה 7 (2016-2019) מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_ד4/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [1] iCar: ב.מ.וו סדרה 7 (2009-2015) מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_ד3/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [2] iCar: ב.מ.וו סדרה 7 (2002-2008) מפרט טכני — https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_7/ב.מ.וו_סדרה_7_יד_שניה_ד2/ — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [3] Auto.co.il: ב.מ.וו סדרה 7 (1994-2001) - מפרט טכני — https://www.auto.co.il/model/bmw-7-series_g64 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']
- [4] Carzone: ב.מ.וו 730 מפרטים — https://www.carzone.co.il/models/bmw/7-series/ — supports=['engine', 'horsepower_hp', 'transmission', 'drivetrain']
- [5] Auto.co.il: ב.מ.וו סדרה 7 (1987-1994) - מפרט טכני — https://www.auto.co.il/model/bmw-7-series_g63 — supports=['body_type', 'fuel_type', 'engine', 'engine_displacement_l', 'horsepower_hp', 'transmission', 'drivetrain', 'year_start', 'year_end']

### Required specific Codex edits
- V00 2016-2019 2.0 i4 258: לשמור רק אם iCar ד4 תומך ב-730i/730Li 2.0 טורבו בישראל. למלא trim Pure/Luxury אם המקור מציין; אחרת null.
- V01 2005-2015 3.0 i6 258 רחב מדי: לפצל E65/E66 2005-2008 ו-F01 2009-2015 אם המקורות נפרדים; אם כל השדות זהים אפשר להשאיר אך field_sources חייבים לכסות שתי תקופות.
- V02 2003-2005 231, V03 1994-1996 V8 218, V04 1990-1994 I6 188: לשמור רק עם Auto/iCar היסטוריים.
- לא לערבב 730i עם 740e/740Le/745Le PHEV.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown` or only global/indirect support for required website fields.
- `available_values_for_website` contains only real visible values; no null/Base/Standard/duplicate body aliases.
- If the model is split/moved, remove duplicate polluted rows from the original model and rebuild both affected model profiles.

---


---

# RUN 3 / 3 — Deep web-backed correction prompt for Codex

Scope: the 3 blocked/review models from `data/model_technical_catalog_il_review.json`: BMW 550i, BMW 630i, BMW 640i.
Input files: `data/model_technical_catalog_il.json` and `data/model_technical_catalog_il_review.json` from the uploaded zip.
Date: 2026-06-16.

## Mission for Codex
You do **not** have web access. ChatGPT already performed the external Israeli-market web research and embedded the findings and URLs below. Use this as an offline evidence package and update local JSON files only.

Hard rules:
1. Israeli market only. Do not use overseas specs or generic BMW knowledge to retain a clean row unless an Israeli source also supports the row.
2. A blocked model may move into `model_technical_catalog_il.json` only if every retained field is grounded: model, canonical_model, body_type, fuel_type, engine, displacement, hp, transmission, drivetrain, year_start, year_end, and trim/version when applicable.
3. `version_or_trim=null` is acceptable only when the model code itself is the marketed variant (550i/630i/640i) and no separate Israeli trim is grounded. Never put null/Base/Standard into `available_values_for_website`.
4. Body type must be exact. Gran Coupe is not Sedan. Cabriolet/Convertible is not Coupe.
5. If a source contradicts another source, prefer direct Israeli catalog/spec pages with complete technical fields; document the contradiction in notes and do not silently use the weaker field.
6. Rebuild `sources`, `source_indexes`, `field_sources`, `available_values_for_website`, `invalid_or_non_trim_labels`, and quality scan outputs after edits.

## Exact blocked run list
1. BMW 550i; 2. BMW 630i; 3. BMW 640i

---

## 1. BMW 550i
Priority: **קריטי**

Verdict: **ניתן לתקן ולהכניס לנקי רק לאחר תיקון שדה-שדה; לא להכניס כפי שהוא.**

### Current review variants
- V00: version_or_trim='Exclusive'; body_type='Sedan'; fuel_type='petrol'; engine='4.8L v8'; engine_displacement_l=4.8; horsepower_hp=367; transmission='automatic'; drivetrain=None; year_start=2007; year_end=2009; support_level='unknown'; missing_grounded_fields=['version_or_trim', 'body_type', 'fuel_type', 'drivetrain']
- V01: version_or_trim='Premium'; body_type='Sedan'; fuel_type='petrol'; engine='4.4L turbo v8'; engine_displacement_l=4.4; horsepower_hp=449; transmission='automatic'; drivetrain=None; year_start=2014; year_end=2014; support_level='unknown'; missing_grounded_fields=['body_type', 'fuel_type', 'drivetrain']
- V02: version_or_trim='Exclusive'; body_type='Sedan'; fuel_type='petrol'; engine='4.4L turbo v8'; engine_displacement_l=4.4; horsepower_hp=None; transmission='automatic'; drivetrain=None; year_start=2015; year_end=2016; support_level='unknown'; missing_grounded_fields=['body_type', 'fuel_type', 'horsepower_hp', 'drivetrain']

### Web evidence already researched by ChatGPT
- iCar ישראל: BMW סדרה 5 2008, גרסה 4.8 550i, דור 2004-2009; 4 דלתות, 5 מושבים, הנעה אחורית, תיבה אוטומטית-טיפטרוניק 6 הילוכים, בנזין, V8, 4799 סמ״ק, 367 כ״ס.
- Yad2 מחירון: BMW סדרה 5 2008 550i אוט׳ 4.8 (367 כ״ס) — מאמת את דגם 550i 4.8 367 לשנת 2008.
- Yad2 מחירון: 2014 קיימות שתי רשומות נפרדות ל-550i 4.4 449 כ״ס: Premium 550i וגם Exclusive 550i. לכן אסור להניח שרק Premium או רק Exclusive קיימת ב-2014 בלי בדיקת כפילות מכוונת.
- Auto.co.il ישראל: BMW סדרה 5 2015 ו-2016 550i אוט׳ 4.4 ל׳ טורבו Exclusive; מקור זה מאמת 4395 סמ״ק, טורבו בנזין, V8, הנעה אחורית, 449 כ״ס, 8 הילוכים.
- Yad2 מחירון: 2016 ו-2017 Exclusive 550i אוט׳ 4.4 (449 כ״ס), מרכב סדאן, תיבה אוטומטית, בנזין, 4395 סמ״ק, 449 כ״ס, 4 דלתות, 5 מושבים.
- מסקנה: מקור Auto חזק ל-2015-2016; Yad2 מחזק 2014/2016/2017. אם הקטלוג דורש רק מקורות קטלוגיים מלאים ולא מחירון, 2017 נשאר פחות חזק מ-2015-2016 ולכן יש לסמן בזהירות.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_5/ב.מ.וו_סדרה_5_יד_שניה_ד10/version2779/
- https://www.yad2.co.il/price-list/sub-model/124620/2008
- https://www.yad2.co.il/price-list/sub-model/102815/2014
- https://www.yad2.co.il/price-list/sub-model/130899/2014
- https://www.auto.co.il/cars/bmw/5-series/2015/531223/
- https://www.auto.co.il/cars/bmw/5-series/2016/531207/
- https://www.yad2.co.il/price-list/sub-model/130899/2016
- https://www.yad2.co.il/price-list/sub-model/130899/2017

### Required specific Codex edits
- V00 2007-2009 4.8 V8 367: לא להשאיר version_or_trim='Exclusive'. המקורות שנמצאו מאמתים 4.8/550i אך לא רמת גימור Exclusive לתקופה הזו. קבע version_or_trim=null או מצא מקור ישיר לרמת הגימור לפני שמירה.
- V00: מלא body_type='Sedan', fuel_type='petrol', drivetrain='RWD', transmission עדיף '6-speed automatic' או לפי סטנדרט הקטלוג 'automatic', על בסיס iCar 2008. year_start=2007 סביר רק לגרסת 367 כ״ס לאחר מתיחת פנים; אם אין מקור 2007 ישיר, שמור 2008-2009 או סמן year_start missing.
- V01 2014 Premium 4.4 449: מקור Yad2 מאמת Premium 2014 4.4 449. מלא body_type='Sedan', fuel_type='petrol'; drivetrain ניתן לגבות מ-Auto/מבנה F10 כ-RWD אם יש מקור. אל תסמן support_level unknown אם כל השדות מגובים.
- בדוק אם צריך להוסיף/לשמור גם 2014 Exclusive 550i 4.4 449, כי נמצא מחירון Yad2 נפרד ל-Exclusive 2014. אם לא מוסיפים, ציין ב-notes למה Premium בלבד נשמר.
- V02 2015-2016 Exclusive 4.4: חובה למלא horsepower_hp=449 ו-drivetrain='RWD' על בסיס Auto.co.il. לא להשאיר horsepower null.
- שקול להאריך את V02 ל-2017 רק אם אתה מקבל את Yad2 2017 כמקור מספיק. אם מדיניות הנקי דורשת מקור קטלוג/מפרט מלא, השאר 2015-2016 והעבר/סמן 2017 לבדיקה.
- model year_end=2017 מותר רק אם נשמרת שורת 2017 עם מקור. אחרת שנה ל-2016.
- available_values_for_website צריך לכלול רק Premium/Exclusive אם הן באמת נשמרו כשורות; לא להכניס null/Base/Standard.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown`.
- No retained row has `missing_grounded_fields` for a field that is actually grounded by the evidence above.
- No ungrounded trim labels are displayed to users.
- The model is either fully moved into clean with rebuilt sources/field_sources or remains in review with a precise reason.

---

## 2. BMW 630i
Priority: **גבוה**

Verdict: **ניתן לתקן; רוב הטכני מגובה, אבל חסרים drivetrain ושנת התחלה/מרכב מדויקים.**

### Current review variants
- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='3.0L i6'; engine_displacement_l=3.0; horsepower_hp=272; transmission='automatic'; drivetrain=None; year_start=2007; year_end=2011; support_level='direct'; missing_grounded_fields=['drivetrain']
- V01: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='3.0L i6'; engine_displacement_l=3.0; horsepower_hp=272; transmission='automatic'; drivetrain=None; year_start=2008; year_end=2010; support_level='direct'; missing_grounded_fields=['drivetrain']

### Web evidence already researched by ChatGPT
- iCar ישראל: BMW סדרה 6 קופה 2010, 3.0 630i, דור 2004-2011; 272 כ״ס, 32.6 קג״מ, 0-100 ב-6.4 שניות, דגם 3.0 630i.
- iCar דף דור קופה 2004-2011 מציג את 3.0 630i כאחת מגרסאות סדרה 6 קופה.
- iCar ישראל: BMW סדרה 6 קבריולה 2008 630i 3.0; הנעה אחורית, אוטומטית-טיפטרוניק, 6 הילוכים, בנזין, 6 צילינדרים, 2996 סמ״ק, 272 כ״ס.
- Auto.co.il: BMW 630ci קבריולה 2010 מאמת 2996 סמ״ק, בנזין, טורי 6, 272 כ״ס, תיבה אוטומטית פלנטרית 6 הילוכים. אבל באותו דף מופיעה 'הנעה קדמית', שזה כמעט בוודאות שגיאת מקור; לא להשתמש ב-Auto הזה ל-drivetrain.
- Auto.co.il: BMW 630ci אוט׳ 2003 מאמת הנעה אחורית, 2996 סמ״ק, בנזין, 6 צילינדרים, 272 כ״ס, 6 הילוכים. השתמש בו רק בזהירות לשדה drivetrain/מבנה, לא להרחבת 272 כ״ס לכל השנים ללא בדיקת מנוע.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_6_קופה/ב.מ.וו_סדרה_6_קופה_יד_שניה_ד10/version24502/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_6_קופה/ב.מ.וו_סדרה_6_קופה_יד_שניה_ד10/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_6_קבריולה/ב.מ.וו_סדרה_6_קבריולה_יד_שניה_ד10/version4414/
- https://www.auto.co.il/cars/bmw/6-series/2010/523036/
- https://www.auto.co.il/cars/bmw/6-series/2003/523013/
- https://www.yad2.co.il/price-list/sub-model/124599/2008
- https://www.yad2.co.il/price-list/sub-model/124599/2010
- https://www.yad2.co.il/price-list/sub-model/102853/2007

### Required specific Codex edits
- שתי השורות צריכות לקבל drivetrain='RWD'. מקור iCar קבריולה מאמת אחורית, ו-BMW 6 Series E63/E64 הוא RWD; אל תשתמש בשדה 'הנעה קדמית' בדף Auto קבריולה 2010 כי הוא סותר מקור iCar ואת מבנה הדגם.
- version_or_trim יכול להישאר null כי 630i הוא מזהה המודל/מנוע ולא trim שיווקי נפרד. אין להכניס null ל-available_values_for_website.
- V00 Coupe 272 hp: שמור year_start=2007 רק אם זה מיועד למנוע 272 כ״ס שלאחר מתיחת פנים. אל תרחיב ל-2004 בלי ליצור שורת 258/272 נפרדת ומקור ישיר.
- V00 Coupe: year_end=2011 נתמך עקרונית ע״י iCar דור 2004-2011 ודף 2011; השאר 2011 אם מקור קיים ב-sources.
- V01 Convertible: year_start=2008 שמרני אבל ייתכן שצריך להיות 2007 על בסיס Auto/Yad2. אם אין מקור iCar 2007 ישיר, השאר 2008-2010 וסמן שהתחלה 2007 לא הוכנסה מחוסר מקור קטלוגי חזק.
- V01 Convertible: year_end=2010 נתמך ע״י Auto 2010; אם משתמשים ב-iCar דף דור 2005-2009 בלבד, אל תסתור אותו בלי מקור נוסף.
- canonical_model צריך להיות עקבי: 'BMW 6 Series 630i' ולא רק '6 Series' אם שאר הקטלוג משתמש בשם מורחב.
- נקה invalid_or_non_trim_labels: Cabriolet הוא body_type, לא trim — נכון להשאיר כ-invalid label ולא כ-version_or_trim.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown`.
- No retained row has `missing_grounded_fields` for a field that is actually grounded by the evidence above.
- No ungrounded trim labels are displayed to users.
- The model is either fully moved into clean with rebuilt sources/field_sources or remains in review with a precise reason.

---

## 3. BMW 640i
Priority: **קריטי**

Verdict: **ניתן לתקן; עיקר הבעיה היא body_type שגוי ל-Gran Coupe ו-version_or_trim null שאינו בעיה אמיתית.**

### Current review variants
- V00: version_or_trim=None; body_type='Coupe'; fuel_type='petrol'; engine='3.0L turbo i6'; engine_displacement_l=3.0; horsepower_hp=320; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2018; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V01: version_or_trim=None; body_type='Sedan'; fuel_type='petrol'; engine='3.0L turbo i6'; engine_displacement_l=3.0; horsepower_hp=320; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2012; year_end=2018; support_level='direct'; missing_grounded_fields=['version_or_trim']
- V02: version_or_trim=None; body_type='Convertible'; fuel_type='petrol'; engine='3.0L turbo i6'; engine_displacement_l=3.0; horsepower_hp=320; transmission='8-speed automatic'; drivetrain='RWD'; year_start=2011; year_end=2018; support_level='direct'; missing_grounded_fields=['version_or_trim']

### Web evidence already researched by ChatGPT
- iCar ישראל: BMW סדרה 6 קופה 2012, 3.0 640i; שנת השקת הדגם 2011, מנוע/ביצועים לגרסת 3.0 640i.
- iCar ישראל: BMW סדרה 6 קבריולה 2011, 3.0 640i; דף דור 2011-2018, שנת השקת דגם 2010, גרסת 3.0 640i.
- iCar כתבה 07.07.2011: סדרה 6 קבריולה החדשה נחתה בישראל; גרסת 640i בסיסית עם מנוע 3.0 ליטר טורבו, 320 כ״ס, 0-100 ב-5.7 שניות; מחיר 845,000 ₪.
- iCar כתבה 18.07.2012: סדרה 6 גראן קופה הגיעה לישראל; גרסת 640i עם מנוע 3.0 ליטר טורבו, 320 כ״ס, 45.9 קג״מ, 0-100 ב-5.4 שניות.
- Auto.co.il גרן קופה 2012: 640i גראן קופה, אוט׳; 2979 סמ״ק, טורבו בנזין, טורי 6, הנעה אחורית, 320 כ״ס, תיבה אוטומטית פלנטרית, 8 הילוכים.
- iCar/Auto מתארים Gran Coupe כמרכב נפרד עם 4 דלתות — לא Sedan רגיל. לכן body_type='Sedan' בקטלוג שגוי וצריך להפוך ל-'Gran Coupe'.

### URLs / offline evidence package for Codex
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_6_קופה/ב.מ.וו_סדרה_6_קופה_יד_שניה_ד11/version11117/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_6_קבריולה/ב.מ.וו_סדרה_6_קבריולה_יד_שניה_ד11/version10104/
- https://www.icar.co.il/חדשות_רכב/נתפסה_בעדשה:_ב.מ.וו_סדרה_6_משתזפת_טופלס/
- https://www.icar.co.il/חדשות_רכב/ב.מ.וו_סדרה_6_גראן_קופה_הגיעה_לישראל/
- https://www.auto.co.il/cars/bmw/6-series-gran-coupe/2012/504689/
- https://www.auto.co.il/cars/bmw/6-series-gran-coupe/
- https://www.icar.co.il/ב.מ.וו/ב.מ.וו_סדרה_6_גראן_קופה/ב.מ.וו_סדרה_6_גראן_קופה_יד_שניה_ד10/
- https://www.carzone.co.il/BMW/6-Series/2011/

### Required specific Codex edits
- V00 Coupe: לשמור body_type='Coupe', fuel_type='petrol', engine='3.0L turbo i6', engine_displacement_l=3.0/2.979, horsepower_hp=320, transmission='8-speed automatic', drivetrain='RWD'. year_start=2011 סביר; אם אין מקור קטלוגי ישראלי לדף 2011 קופה, השתמש ב-2012 כשנה שמרנית או השאר 2011 עם source של שנת השקת דגם.
- V01 כרגע body_type='Sedan' — לתקן ל-body_type='Gran Coupe'. לא להשאיר Sedan. year_start=2012, year_end=2018, 3.0 טורבו, 320 כ״ס, RWD, 8AT.
- V02 Convertible: לשמור body_type='Convertible' או 'Cabriolet' לפי סטנדרט הקטלוג, year_start=2011, year_end=2018, 3.0 טורבו, 320 כ״ס, RWD, 8AT.
- version_or_trim יכול להיות null בכל שלוש השורות כי 640i הוא model/engine code ולא trim שיווקי נפרד. אם הקטלוג מחייב ערך תצוגה, השתמש ב-body_type/engine לבחירה ולא ב-Base/Standard.
- canonical_model='BMW 6 Series 640i' או עקבי עם שאר הקטלוג; אל תשאיר canonical_model='640i' בלבד אם שאר הדאטה משתמש בשם מלא.
- available_values_for_website.body_type חייב לכלול Coupe, Gran Coupe, Convertible/Cabriolet בלבד; לא Sedan.
- אין להעביר את 640i לנקי אם source_indexes/field_sources לא נבנו מחדש אחרי שינוי Sedan→Gran Coupe.

### Acceptance criteria for this model
- No retained clean row has `support_level=unknown`.
- No retained row has `missing_grounded_fields` for a field that is actually grounded by the evidence above.
- No ungrounded trim labels are displayed to users.
- The model is either fully moved into clean with rebuilt sources/field_sources or remains in review with a precise reason.

---