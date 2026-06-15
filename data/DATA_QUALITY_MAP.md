# מפת איכות הדאטה – קטלוג טכני ישראלי (Israeli Vehicle Technical Catalog)

תאריך הפקה: 2026-06-15 · מקור: `model_technical_catalog_il.json` + `..._quality_scan.json`

## 1. תמונת מצב כללית

| מדד | ערך |
|------|-----|
| דגמים נקיים (website-ready) | **61** |
| גרסאות טכניות | **234** |
| דגמים חסומים (review) | **0** |
| `ready_for_website_upload` | **true** |
| יצרנים מכוסים | 6 (Abarth, Aiways, Alfa Romeo, Alpine, Aston Martin, Audi) |
| היקום הכולל | 1,124 אשכולות דגם · 94 יצרנים · 3,712 גרסאות גלם |
| התקדמות | ~5.4% מהאשכולות (סדר א״ב, הגיע עד Audi) |

## 2. שלמות הדאטה (Completeness) — מצוין

- **100%** מילוי לכל ששת שדות החובה לאתר (body_type, fuel_type, engine, horsepower_hp, transmission, drivetrain) בכל 234 הגרסאות.
- **100%** עיגון תאים (grounded cells): 2,189 / 2,189 — לכל ערך לא-ריק יש לפחות מקור אחד ב-`field_sources`.
- כל 61 הדגמים ב-100% שלמות עיגון.
- `version_or_trim` ריק ב-46% מהגרסאות (108) — תקין: רוב הגרסאות מובחנות לפי מנוע/הספק ולא לפי שם גימור.
- `year_end` ריק ב-8% (19) — תקין: דגמים שעדיין בשיווק.

## 3. אמינות מקורות (Source reliability) — נקודת התורפה העיקרית

| מדד | ערך | משמעות |
|------|-----|--------|
| נתח ציטוט ממרקטפלייס (autoboom/yad2) | **21.1%** | חלק מהשדות נשען על לוחות יד-שנייה ולא על מקור רשמי |
| ממצאי `source_tier_inversion` (leak) | **120** ב-15 דגמים | בעיקר שנות ייצור/גימור שמעוגנים רק במרקטפלייס |
| מקורות לא-ישראליים | **3** | astonmartin.com ב-DB12 / DBS / DBX |

**הדגמים הבעייתיים ביותר (הסתמכות על מרקטפלייס):**
Alfa Romeo 166 (29 ממצאים), Alfa Romeo 75 (12), Alfa Romeo 146/147 (8 כ״א), Aston Martin DB9 (8), Abarth Punto (7).
המכנה המשותף: דגמים ישנים שעבורם אין דף יבואן רשמי, ולכן שנות הייצור נלקחו מ-autoboom.

**מקורות מובילים (לפי שכיחות):** auto.co.il (136), icar.co.il (103), autoboom.co.il (53), cartube.co.il (33), wheel.co.il (13), yad2.co.il (13).

## 4. עקביות מבנית (Structural) — תקין עם הזדמנויות לליטוש

- **17 מועמדים למיזוג שנים** (`year_split_duplicates`): שורות זהות בכל השדות הטכניים שנבדלות רק בטווח השנים (למשל Alfa Romeo Giulia, Audi Q7/RS3). מועמדות לאיחוד לשורה אחת.
- **0** ממצאי נורמליזציה (כל הערכים בתוך הרשימה הקנונית).
- **0** ממצאי באג (אין דחיות-שווא, אין הפרות של support_level).

## 5. פילוח הדאטה

- **דלק:** petrol 167 · electric 24 · mild_hybrid 16 · diesel 14 · plug_in_hybrid 13
- **מרכב:** Sedan 69 · Hatchback 53 · SUV 48 · Coupe 28 · Convertible 14 · Liftback 13 · Crossover 6 · Estate 3
- **רמת ביסוס (support_level):** direct 200 · indirect 30 · unknown 4

## 6. פריטי טיפול מומלצים (לפי עדיפות)

1. **גבוהה** – לחזק עיגון שנות-ייצור/גימור בדגמי Alfa Romeo הישנים (166/75/146/147) ו-Aston Martin DB9 במקור שאינו מרקטפלייס.
2. **בינונית** – למזג 17 מועמדי `year_split_duplicates` לשורות טווח-שנים אחידות.
3. **נמוכה** – 4 שורות עם `support_level=unknown` (Abarth 500e ×2, Audi R8 ×2) ממולאות ומעוגנות במלואן — כדאי לקדם ל-`direct`.
4. **נמוכה** – להחליף את 3 ההפניות ל-astonmartin.com במקור ישראלי כשקיים.
