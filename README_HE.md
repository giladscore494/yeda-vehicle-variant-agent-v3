# מנוע ולידציה לוריאנטים של רכבים בישראל — validation-v2-budgeted-dual-il-trims

מנוע ולידציה מבוסס Gemini (`gemini-3.1-pro-preview`) שמאמת 3,712 וריאנטים של רכבים לשוק הישראלי,
משלים שדות חסרים בזהירות, מאמת שמות שיווק ישראליים, מזהה כפילויות ורמות גימור מחוברות,
ומייצר מאגר קנוני נקי עם audit מלא.

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

לפני כל קריאה ל-Gemini רץ אימות פתיחה: שני הקבצים קיימים, JSON תקין, בדיוק 3,712 מזהים
ייחודיים זהים בשני הקבצים, לכל וריאנט יש `standard_variant` והקשר audit, ולכל הוראה יש
`validation_priority` ו-`validation_tasks`. כשל → נכתב `output/startup_failure_report.json`
והריצה נעצרת בלי לקרוא ל-Gemini.

## סיקרטים (GitHub Secrets בלבד)

```text
GEMINI_API_KEY   # מפתח Gemini API
GH_PUSH_TOKEN    # טוקן push לבראנץ' validation-v2-budgeted-dual-il-trims
```

אין ערכים אמיתיים בקוד, בלוגים או בקבצי קונפיג.

## הרצה דרך GitHub Actions (מומלץ)

Actions → **Run Gemini Variant Validation** → Run workflow על הבראנץ'
`validation-v2-budgeted-dual-il-trims`, עם הקלטים:

| input | משמעות | ברירת מחדל |
|---|---|---|
| `limit` | כמה וריאנטים לעבד (ריק = הכול) | ריק |
| `push_every` | תדירות checkpoint push (1 = אחרי כל וריאנט) | `25` |
| `force_reprocess` | לעבד מחדש וריאנטים שכבר הושלמו | `false` |
| `only_priority` | רק קבוצת עדיפות אחת (high/medium/low/sample_only) | ריק |
| `validation_id` | וריאנט בודד | ריק |
| `dry_run` | בניית הקשרים בלי לקרוא ל-Gemini | `false` |

### סדר הרצה בטוח

1. `dry_run=true` עם `limit=3` — בדיקת צנרת בלי Gemini.
2. `limit=3` — ריצה אמיתית קטנה; לבדוק את `output/`.
3. `limit=25` — לבדוק `manual_review.jsonl` ואת הקובץ הקנוני.
4. ריצה מלאה עם `limit` ריק. ה-resume אוטומטי — מזהים שהושלמו לא מעובדים שוב.

## הרצה מקומית

```bash
pip install -r requirements.txt
python scripts/smoke_test.py                       # בלי Gemini
export GEMINI_API_KEY=...                          # מהסיקרט, לא בקוד
python scripts/run_gemini_validation.py --limit 3
python scripts/run_gemini_validation.py            # ריצה מלאה עם resume
```

דגלים שימושיים: `--only-priority high`, `--validation-id VAL-000001`,
`--start-after VAL-000123`, `--dry-run`, `--push-every 1`, `--no-push`.

## עיבוד

- סדר: `high` → `medium` → `low` → `sample_only`, ובתוך כל קבוצה לפי `variant_sequence`.
- Gemini מחזיר JSON קשיח בלבד לפי `config/validation_schema.json`.
- אחרי **כל** תשובה רץ QA דטרמיניסטי (`scripts/deterministic_qa.py`): התאמת validation_id,
  סכמה, שנים, placeholder-ים, סתירות הנעה, שינויי שדות קריטיים בלי ראיות, כפילויות,
  פיצולי trim, וסף ביטחון 0.85 ל-auto_accept.
- תשובה פגומה → עד 3 ניסיונות עם פרומפט מחמיר; אחר כך manual_review/failures.
- grounding מופעל כשנתמך; אם לא — `grounding_enabled=false` בסיכום והמנוע שמרני יותר.
- שמירה מקומית אחרי כל וריאנט; commit+push כל `push_every` וריאנטים (ברירת מחדל 25).

## קבצי פלט (`output/`)

```text
validation_results.jsonl                    # audit מלא, כולל original_snapshot (רק כאן!)
canonical_variants_clean.jsonl              # שורות קנוניות נקיות
manual_review.jsonl                         # וריאנטים לבדיקה ידנית + סיבות
failures.jsonl                              # כשלים/דחיות
validation_progress.json                    # מצב resume (מזהים שעובדו, ספירות)
validation_run_summary.json                 # סיכום ריצה
validation-v2-budgeted-dual-il-trims.json   # *** המאגר הסופי הנקי ***
canonical_vehicle_variants_clean_v1.json    # עותק תאימות זהה
```

הקובץ הסופי הנקי לא מכיל `original_snapshot` ולא שדות legacy — המקור נשמר רק
ב-`validation_results.jsonl`.

## עקרון מנחה

אם אין ודאות — לא ממציאים. שינוי קריטי בלי ראיות חזקות → manual_review.
manual_review עדיף על ודאות כוזבת.
