# מנוע ולידציה לוריאנטים של רכבים בישראל — validation-v2-budgeted-dual-il-trims

מנוע ולידציה מבוסס Gemini (`gemini-3.1-pro-preview`) שמאמת 3,712 וריאנטים של רכבים לשוק הישראלי,
משלים שדות חסרים בזהירות, מאמת שמות שיווק ישראליים, מזהה כפילויות ורמות גימור מחוברות,
ומייצר מאגר קנוני נקי עם audit מלא.

**סביבת הריצה הראשית: אפליקציית Streamlit (`app.py`) עם Streamlit Secrets.**
ה-CLI נשמר לפיתוח/בדיקות, ו-GitHub Actions נשמר ל-smoke/dry-run בלבד.

## קבצי קלט (חובה, מחוברים לפי `validation_id`)

```text
data/validation_variants_data_v1.json        # כל הוריאנטים: standard_variant, original_snapshot, מטא-דאטה
data/validation_instructions_by_id_v1.json   # הוראות לכל validation_id: עדיפות, משימות, שדות חסרים
data/validation_instructions_by_id_v1.jsonl  # אופציונלי: גרסת JSONL ל-streaming/debug
```

המנוע תמיד טוען את **שני** הקבצים וממזג לכל `validation_id`:

```python
merged_context = variant_record + instruction_record
```

ל-Gemini נשלח תמיד רק הקשר של וריאנט אחד + ההוראות שלו — לעולם לא הקבצים המלאים.

לפני כל ריצה אמיתית רץ אימות פתיחה: שני הקבצים קיימים, JSON תקין, בדיוק 3,712 מזהים
ייחודיים זהים בשני הקבצים, לכל וריאנט יש `standard_variant`, ולכל הוראה יש
`validation_priority` ו-`validation_tasks`. כשל → הריצה נחסמת ב-UI ונכתב
`output/startup_failure_report.json`, בלי שום קריאה ל-Gemini.

## סודות (Streamlit Secrets)

הריצה האמיתית משתמשת ב-`st.secrets`. מבנה נתמך (ראו `.streamlit/secrets.toml.example`):

```toml
[google]
api_key = ""                                        # מפתח Gemini
gemini_validator_model_id = "gemini-3.1-pro-preview"
grounding_enabled = true
token = ""                                          # טוקן GitHub (או תחת [github])
repo_full_name = "giladscore494/yeda-vehicle-variant-agent-v3"
target_branch = "validation-v2-budgeted-dual-il-trims"
base_branch = "main"
```

נתמך גם מבנה עם סקשן `[github]` נפרד (token / repo_full_name / target_branch / base_branch).
ל-dev מקומי יש fallback למשתני סביבה: `GEMINI_API_KEY`, `GH_PUSH_TOKEN`,
`GEMINI_VALIDATOR_MODEL_ID`, `GITHUB_REPO_FULL_NAME`, `TARGET_BRANCH`, `BASE_BRANCH`.

כללי אבטחה: ערכי סודות לעולם לא מודפסים, לא נכתבים לפלט ולא נשלחים ל-git.
`.streamlit/secrets.toml` נמצא ב-`.gitignore` — אסור לקמט אותו.
ה-UI מציג רק present/missing.

## הרצה דרך Streamlit (הדרך הראשית)

```bash
pip install -r requirements.txt
streamlit run app.py
```

בדשבורד:

1. **Run startup checks** / **Run smoke test** — חובה לפני ריצה אמיתית.
2. **Run dry-run (limit=3)** — בניית הקשרים בלי Gemini.
3. **Run mock validation (limit=3)** — צנרת מלאה עם לקוח מדומה; הפלט נכתב
   ל-`output/mock/` כדי לא לזהם את ההתקדמות האמיתית. בלי עלות.
4. סימון תיבת האישור *"I understand this will call Gemini and may cost money"* →
   **Run real validation (limit=3)** → בדיקת הפלט → **limit=25** →
   **Continue validation with resume** (מאחורי אישור נוסף).

שום דבר לא רץ אוטומטית בטעינת הדף. רענון דף לא מוחק התקדמות — הכול נשמר בדיסק
אחרי כל וריאנט והריצה ניתנת להמשך גם אחרי restart של האפליקציה.

ברירת מחדל ב-Streamlit: `push_every=1` (checkpoint אחרי כל וריאנט), ניתן לשינוי ב-UI,
וכן `force_reprocess`, `dry_run`, `mock_mode`.

## הרצה מקומית ב-CLI (פיתוח/בדיקות)

```bash
python scripts/smoke_test.py                                  # בלי Gemini
python scripts/run_gemini_validation.py --limit 3 --dry-run   # בלי Gemini
python scripts/run_gemini_validation.py --limit 3 --mock --no-push   # צנרת מלאה, בלי Gemini
export GEMINI_API_KEY=...                                     # רק לריצה אמיתית
python scripts/run_gemini_validation.py --limit 3
```

דגלים: `--only-priority high`, `--validation-id VAL-000001`, `--start-after`,
`--push-every 1`, `--no-push`, `--no-resume`, `--mock`.

## עיבוד

- סדר: `high` → `medium` → `low` → `sample_only`, ובתוך כל קבוצה לפי `variant_sequence`.
- Gemini מחזיר JSON קשיח בלבד לפי `config/validation_schema.json`.
- אחרי **כל** תשובה רץ QA דטרמיניסטי (`scripts/deterministic_qa.py`): התאמת validation_id,
  סכמה, שנים, placeholder-ים, סתירות הנעה, שינויי שדות קריטיים בלי ראיות, כפילויות,
  פיצולי trim, וסף ביטחון 0.85 ל-auto_accept.
- תשובה פגומה → עד 3 ניסיונות עם פרומפט מחמיר; אחר כך manual_review/failures.
- grounding מופעל כשנתמך; אם לא — `grounding_enabled=false` בסיכום והמנוע שמרני יותר.
- שמירה מקומית אחרי כל וריאנט; commit+push לפי `push_every` (ברירת מחדל ב-Streamlit: 1).
- Push מתבצע דרך GitHub REST API (עמיד לסביבת Streamlit Cloud) עם fallback ל-git CLI;
  כשל push נרשם ב-`output/push_failures.jsonl`, מוצג ב-UI וניתן לנסות שוב —
  הפלט המקומי לעולם לא נמחק.

## קבצי פלט (`output/`)

```text
validation_results.jsonl                    # audit מלא, כולל original_snapshot (רק כאן!)
canonical_variants_clean.jsonl              # שורות קנוניות נקיות
manual_review.jsonl                         # וריאנטים לבדיקה ידנית + סיבות
failures.jsonl                              # כשלים/דחיות
push_failures.jsonl                         # כשלי push (הפלט המקומי נשמר)
validation_progress.json                    # מצב resume (מזהים שעובדו, ספירות)
validation_run_summary.json                 # סיכום ריצה
validation-v2-budgeted-dual-il-trims.json   # *** המאגר הסופי הנקי ***
canonical_vehicle_variants_clean_v1.json    # עותק תאימות זהה
```

הקובץ הסופי הנקי לא מכיל `original_snapshot` ולא שדות legacy — המקור נשמר רק
ב-`validation_results.jsonl`. ריצות mock נכתבות ל-`output/mock/` בלבד.

## GitHub Actions

`.github/workflows/run-validation.yml` נשמר ל-smoke/dry-run/mock ידניים.
ברירת המחדל שלו היא `dry_run=true`, ואם סיקרט `GEMINI_API_KEY` חסר הוא יורד
אוטומטית ל-dry-run במקום להיכשל. הריצה האמיתית — דרך Streamlit בלבד.

## עקרון מנחה

אם אין ודאות — לא ממציאים. שינוי קריטי בלי ראיות חזקות → manual_review.
manual_review עדיף על ודאות כוזבת.
