# פרומפט לפאבל / Claude לבניית מנוע Gemini Validation v2 עם שני קבצי קלט

אתה עובד על הריפו:

```text
giladscore494/yeda-vehicle-variant-agent-v3
```

בראנץ׳ יעד:

```text
validation-v2-budgeted-dual-il-trims
```

בראנץ׳ בסיס:

```text
main
```

## המטרה

לבנות מנוע ולידציה סופר אמין למאגר וריאנטים של רכבים בישראל.

המאגר המקורי היה גדול מדי להעלאה כקובץ אחד מעל 25MB, לכן הוא פוצל לשני קבצי קלט עיקריים:

```text
data/validation_variants_data_v1.json
data/validation_instructions_by_id_v1.json
```

שני הקבצים מחוברים לפי:

```text
validation_id
```

המנוע חייב לקרוא לכל וריאנט מידע משני הקבצים.  
אסור לבצע ולידציה רק מאחד מהם.

---

# קבצי הקלט

## 1. קובץ וריאנטים מלא

```text
data/validation_variants_data_v1.json
```

מכיל את כל 3,712 הוריאנטים.

לכל וריאנט יש בין היתר:

```text
validation_id
variant_sequence
source_collection
schema_family
standard_variant
mapping_status
original_status
original_variant_id
original_snapshot
canonical_identity_key
canonical_identity_hash
possible_duplicate_group
is_possible_duplicate_after_mapping
effective_missing_standard_fields
technical_identity_missing_fields
standard_completeness_score
technical_identity_completeness_score
validation_priority
ai_validation_route
validation_tasks
pre_validation_status
```

הנתונים החשובים ביותר עבור Gemini הם:

```text
standard_variant
original_snapshot
original_variant_id
canonical_identity_key
possible_duplicate_group
effective_missing_standard_fields
technical_identity_missing_fields
validation_tasks
```

## 2. קובץ הוראות לפי ID

```text
data/validation_instructions_by_id_v1.json
```

מכיל:

```text
instructions_by_validation_id
```

לכל `validation_id` יש הוראות ייעודיות:

```text
validation_priority
ai_validation_route
pre_validation_status
effective_missing_standard_fields
technical_identity_missing_fields
focus_fields_for_gemini
required_actions
safety_and_quality_rules
```

המנוע חייב לעשות:

```python
variant_record = variants_by_validation_id[validation_id]
instruction_record = instructions_by_validation_id[validation_id]
merged_context = {variant_record + instruction_record}
```

ורק אז לשלוח ל־Gemini.

---

# סיקרטים נדרשים

אין להכניס ערכים אמיתיים לקוד.

השתמש רק בשמות הסיקרטים:

```text
GEMINI_API_KEY
GH_PUSH_TOKEN
```

## Gemini

```text
model_id = gemini-3.1-pro-preview
grounding_enabled = true
```

## GitHub

```text
repo_full_name = giladscore494/yeda-vehicle-variant-agent-v3
target_branch = validation-v2-budgeted-dual-il-trims
base_branch = main
```

---

# דרישות מנוע

לבנות את הקבצים הבאים:

```text
scripts/run_gemini_validation.py
scripts/build_indexes.py
scripts/deterministic_qa.py
scripts/github_checkpoint.py
scripts/resume_state.py
config/validation_schema.json
config/field_rules.json
prompts/gemini_variant_validation_prompt.md
.github/workflows/run-validation.yml
requirements.txt
README_HE.md
```

אפשר לשנות שמות אם יש סיבה טובה, אבל לשמור על מבנה ברור.

---

# התנהגות חובה

## 1. טעינת שני קבצים

המנוע חייב:

```text
1. לטעון את data/validation_variants_data_v1.json
2. לטעון את data/validation_instructions_by_id_v1.json
3. לבנות index לפי validation_id לשני הקבצים
4. לוודא שכל validation_id שקיים בקובץ הוריאנטים קיים גם בקובץ ההוראות
5. לוודא שאין כפילויות validation_id
6. לעצור עם שגיאה ברורה אם חסר ID באחד הקבצים
```

## 2. ריצה לפי עדיפות

סדר מומלץ:

```text
high
medium
low
sample_only
```

חייבים לתמוך גם בפרמטרים:

```text
--only-priority high
--limit 50
--start-after VAL-000123
--validation-id VAL-000001
--dry-run
--resume
```

## 3. קריאה ל־Gemini

כל קריאה ל־Gemini מקבלת merged context:

```json
{
  "variant_record": "...from validation_variants_data_v1.json...",
  "instruction_record": "...from validation_instructions_by_id_v1.json...",
  "global_rules": "...from instruction file...",
  "expected_schema": "...validation_schema.json..."
}
```

חובה להשתמש ב־structured output / JSON בלבד.

אסור לקבל טקסט חופשי.

אם Gemini מחזיר JSON לא תקין:

```text
1. נסה תיקון parsing פעם אחת
2. אם עדיין נכשל — כתוב ל־output/failures.jsonl
3. סמן את הוריאנט כ־failed_model_response
4. המשך לוריאנט הבא
```

## 4. Grounding

אם `grounding_enabled=true`, Gemini צריך להשתמש בחיפוש/grounding כאשר הוא:

```text
- משלים שם דגם בישראל
- משלים שם מותג מקומי בעברית
- מאמת רמת גימור בישראל
- משנה שדה טכני
- מציע פיצול וריאנט
```

אסור לשנות שדה קריטי בלי evidence_summary ברור.

---

# מה Gemini צריך לבדוק לכל וריאנט

## בדיקות זהות

```text
make
model
global_model_name
year_start
year_end
generation
body_type
seats
engine
transmission
fuel_type
drivetrain
trim
```

## השלמות חובה אם חסר

השתמש ב:

```text
effective_missing_standard_fields
technical_identity_missing_fields
```

חובה לנסות להשלים כל שדה חסר.

אבל אם אין ודאות:

```text
value = null
requires_manual_review = true
unresolved_fields כולל את השדה
```

לא להמציא.

## אימות שמות ישראל

חובה לבדוק:

```text
official_marketed_name_il
local_brand_name_il
trim
recommended_display_name_il
```

מטרה:

```text
איך הדגם/וריאנט נקרא בפועל בישראל
איך רמת הגימור נקראת בישראל
האם שם הוריאנט צריך שינוי
```

## רמות גימור מחוברות

אם trim נראה כמו:

```text
"Comfort / Luxury"
"Turismo / Competizione"
"Premium, Luxury"
```

המנוע צריך לבקש מ־Gemini להחליט:

```text
one_real_variant
multiple_variants_should_split
uncertain_manual_review
```

אם צריך פיצול, אסור לשנות בשקט.  
להחזיר:

```text
split_recommendation
requires_manual_review = true
```

## כפילויות

אם:

```text
is_possible_duplicate_after_mapping = true
```

או יש:

```text
possible_duplicate_group
```

המנוע צריך לטעון את כל חברי הקבוצה מתוך קובץ הוריאנטים ולשלוח ל־Gemini גם תקציר שלהם.

Gemini צריך להחזיר:

```text
duplicate_resolution = merge / keep_separate / uncertain
```

---

# סכמה מחייבת לפלט Gemini

Gemini חייב להחזיר JSON במבנה הבא:

```json
{
  "validation_id": "VAL-000001",
  "final_decision": "auto_accept | accepted_with_changes | manual_review | rejected | failed_model_response",
  "is_real_variant": true,
  "is_relevant_to_il_market": true,
  "corrected_variant": {
    "candidate_index": null,
    "make": "",
    "model": "",
    "global_model_name": "",
    "official_marketed_name_il": "",
    "local_brand_name_il": "",
    "alternate_names": [],
    "rebadged_as": null,
    "year_start": null,
    "year_end": null,
    "generation": "",
    "body_type": "",
    "seats": null,
    "engine": "",
    "transmission": "",
    "fuel_type": "",
    "drivetrain": "",
    "trim": "",
    "market_scope": "IL",
    "market_name_confidence": "",
    "confidence_level": "",
    "source_basis": "",
    "source_ids": [],
    "field_sources": {},
    "variant_id": ""
  },
  "name_validation": {
    "official_marketed_name_il_status": "verified | corrected | missing_unresolved | not_applicable | uncertain",
    "local_brand_name_il_status": "verified | corrected | missing_unresolved | not_applicable | uncertain",
    "trim_name_il_status": "verified | corrected | generic | missing_unresolved | uncertain",
    "recommended_display_name_il": "",
    "name_change_needed": false,
    "name_change_reason": ""
  },
  "fields_completed": [],
  "fields_changed": [],
  "critical_fields_changed": [],
  "unresolved_fields": [],
  "duplicate_resolution": {
    "is_duplicate_reviewed": false,
    "duplicate_group": null,
    "decision": "merge | keep_separate | uncertain | not_applicable",
    "canonical_survivor_validation_id": null,
    "reason": ""
  },
  "split_recommendation": {
    "should_split": false,
    "reason": "",
    "proposed_child_variants": []
  },
  "confidence": 0.0,
  "evidence_summary": "",
  "grounding_notes": [],
  "requires_manual_review": true,
  "manual_review_reason": ""
}
```

---

# QA דטרמיניסטי אחרי Gemini

לא לקבל את Gemini אוטומטית.

אחרי כל תשובה להריץ בדיקות:

## חסימת שדות קריטיים

אם Gemini משנה אחד מהשדות:

```text
make
model
year_start
year_end
engine
transmission
fuel_type
drivetrain
trim
```

ו־confidence נמוך מ־0.85:

```text
requires_manual_review = true
```

## חסימת המצאות

אם Gemini מילא שם ישראלי או רמת גימור אבל אין evidence_summary סביר:

```text
manual_review
```

## שדות חובה

`corrected_variant` חייב להכיל את כל `standard_fields`.

אם חסר שדה:

```text
failed_model_response
```

## שמירת מקור

אסור למחוק:

```text
validation_id
original_variant_id
original_snapshot
```

הם צריכים להופיע ב־audit log, לא בהכרח ב־canonical output.

---

# פלטים נדרשים

```text
output/validation_results.jsonl
output/canonical_variants_clean.jsonl
output/manual_review.jsonl
output/failures.jsonl
output/validation_progress.json
output/validation_run_summary.json
output/canonical_vehicle_variants_clean_v1.json
output/audit_log.jsonl
```

## canonical_vehicle_variants_clean_v1.json

זה הקובץ הסופי הנקי.

הוא צריך להכיל:

```text
schema_version
created_at
model_used
source_input_files
total_variants
auto_accepted_count
manual_review_count
failed_count
variants
```

כל וריאנט בפנים צריך להיות flat ונקי, בלי legacy envelope.

---

# שמירה וגיט

דרישת משתמש: שמירה ופוש אוטומטי.

התנהגות חובה:

```text
1. אחרי כל וריאנט לשמור את כל קבצי output הרלוונטיים
2. אחרי כל וריאנט לבצע git add/commit/push
3. אם אין שינוי לא לבצע commit ריק
4. אם push נכשל, לנסות שוב עד 3 פעמים עם backoff
5. אם עדיין נכשל, לשמור failure ולהמשיך מקומית
```

השתמש ב־secret:

```text
GH_PUSH_TOKEN
```

אין להדפיס את הטוקן ללוגים.

קומיט לדוגמה:

```text
validation: process VAL-000001
```

---

# GitHub Actions

לבנות workflow ידני:

```text
.github/workflows/run-validation.yml
```

צריך לתמוך ב־workflow_dispatch inputs:

```text
limit
only_priority
validation_id
start_after
dry_run
```

ה־workflow צריך:

```text
1. checkout target branch
2. setup python
3. pip install -r requirements.txt
4. export GEMINI_API_KEY from secrets.GEMINI_API_KEY
5. export GH_PUSH_TOKEN from secrets.GH_PUSH_TOKEN
6. run scripts/run_gemini_validation.py with inputs
```

---

# צ׳ק ליסט סופי

לפני סיום העבודה ודא:

```text
[ ] שני קבצי הקלט נטענים
[ ] join לפי validation_id עובד
[ ] כמות וריאנטים = 3712
[ ] אין validation_id חסר בין הקבצים
[ ] יש תמיכה ב-resume
[ ] יש תמיכה ב-dry-run
[ ] יש תמיכה בהרצה על ID יחיד
[ ] Gemini נקרא רק עם gemini-3.1-pro-preview
[ ] Grounding מופעל לפי הקונפיג
[ ] Gemini מחזיר JSON בלבד
[ ] QA דטרמיניסטי רץ אחרי כל תשובה
[ ] manual_review מופעל בכל חוסר ודאות
[ ] קבצי output נשמרים אחרי כל וריאנט
[ ] commit/push אחרי כל וריאנט
[ ] אין סודות בקוד
[ ] README_HE מסביר איך להעלות את שני הקבצים לריפו ולהריץ
```

---

# דגש הכי חשוב

המנוע לא נועד “לייפות” את המאגר.  
המנוע נועד ליצור קובץ נקי, אמין, ומגובה audit.

אם אין ודאות — לא ממציאים.  
אם יש שינוי קריטי — manual_review.  
אם שם רמת גימור בישראל לא מאומת — לא לקבל אוטומטית.
