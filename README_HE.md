# Validation split package v1

החבילה הזו פיצלה את קובץ המיפוי הגדול לשני קבצי קלט עיקריים כדי שכל אחד יהיה מתחת למגבלת 25MB.

הקובץ המקורי:

```text
resume_package_canonical(10).json
```

גודל מקורי:

```text
26.713 MB
```

## קבצים עיקריים להעלאה לריפו

```text
data/validation_variants_data_v1.json
data/validation_instructions_by_id_v1.json
```

שניהם מחוברים לפי:

```text
validation_id
```

המנוע חייב לקרוא כל וריאנט משני הקבצים.

## גדלים

```text
validation_variants_data_v1.json: 17.85 MB
validation_instructions_by_id_v1.json: 16.268 MB
```

שניהם מתחת ל־25MB.

## קובץ עזר אופציונלי

```text
data/validation_instructions_by_id_v1.jsonl
```

זו גרסת JSONL של קובץ ההוראות, שימושית אם רוצים streaming.

## פרומפטים

```text
PROMPT_FOR_CLAUDE_FABLE_BUILD_ENGINE_HE.md
prompts/gemini_variant_validation_prompt_two_file_context.md
```

הקובץ הראשון הוא הפרומפט לתת לפאבל/Claude כדי לבנות את המנוע.  
הקובץ השני הוא תבנית פרומפט ל־Gemini עבור כל וריאנט.

## סיקרטים

להגדיר ב־GitHub Secrets:

```text
GEMINI_API_KEY
GH_PUSH_TOKEN
```

לא להעלות ערכים אמיתיים לריפו.

## קונפיג יעד

```text
repo_full_name = giladscore494/yeda-vehicle-variant-agent-v3
target_branch = validation-v2-budgeted-dual-il-trims
base_branch = main
gemini_validator_model_id = gemini-3.1-pro-preview
grounding_enabled = true
```
