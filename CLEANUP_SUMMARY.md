# Repository cleanup summary — validation-v2-budgeted-dual-il-trims

Cleanup performed only after the engine build, the Streamlit runner, the smoke
test (15/15 checks), dry-run limit=3, and mock validation limit=3 all passed.

## Files kept (runtime / documentation)

| File | Reason |
|---|---|
| `app.py` | Main Streamlit validation runner (st.secrets runtime) |
| `data/validation_variants_data_v1.json` | Required input #1 (moved from root to `data/`) |
| `data/validation_instructions_by_id_v1.json` | Required input #2 (moved from root to `data/`) |
| `data/validation_instructions_by_id_v1.jsonl` | Optional streaming/debug helper, kept per spec |
| `scripts/run_gemini_validation.py` | Engine core (reusable from Streamlit + CLI) |
| `scripts/smoke_test.py` | Pre-run safety test (importable from the app) |
| `scripts/deterministic_qa.py` | Deterministic QA after every Gemini response |
| `scripts/github_checkpoint.py` | Checkpoint push (GitHub REST API + git CLI fallback) |
| `scripts/runtime_config.py` | st.secrets / env / defaults resolver |
| `config/validation_schema.json` | Required Gemini response schema |
| `config/field_rules.json` | Critical fields, placeholders, thresholds |
| `prompts/gemini_variant_validation_prompt_two_file_context.md` | Gemini system prompt (moved from root, updated to final schema) |
| `.github/workflows/run-validation.yml` | Kept for smoke/dry-run; degrades to dry-run without secrets |
| `.streamlit/secrets.toml.example` | Documented secrets layout (no real values) |
| `requirements.txt` | Streamlit runtime dependencies |
| `README_HE.md` | Run instructions (rewritten for Streamlit runtime) |
| `manifest.json` | Provenance + sha256 of the two input files — audit metadata |
| `output/` | Run outputs (progress, audit, canonical clean database) |

## Files deleted

| File | Reason |
|---|---|
| `PROMPT_FOR_CLAUDE_FABLE_BUILD_ENGINE_HE.md` | One-time build specification used to construct the engine; fully implemented and superseded by the final task instructions (Streamlit runtime). Not needed at runtime. |

## Files moved (not deleted)

- `validation_variants_data_v1.json` → `data/validation_variants_data_v1.json`
- `validation_instructions_by_id_v1.json` → `data/validation_instructions_by_id_v1.json`
- `validation_instructions_by_id_v1.jsonl` → `data/validation_instructions_by_id_v1.jsonl`
- `gemini_variant_validation_prompt_two_file_context.md` → `prompts/gemini_variant_validation_prompt_two_file_context.md`

The engine also supports reading the input files from the repository root via a
path resolver (`data/` preferred), so no references are broken either way.
`.streamlit/secrets.toml` is gitignored and must never be committed.
