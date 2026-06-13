# Gemini 3.1 Israeli-Market Vehicle Variant Validation Engine

A practical, **Gemini-only** validation engine with a Streamlit runner. It
validates and lightly enriches all raw vehicle variants into a single output
file, preserving every original `validation_id`.

> **Core principle:** vehicle identity is strict, trim enrichment is flexible.
> A real Israeli-market variant is **never** rejected only because the trim is
> weak, generic, missing, or hard to verify — weak trim becomes `clean_partial`.

No OpenAI. No GPT adjudicator. No dual-model architecture. No old deterministic
QA rejection gate.

## Layout

```
app.py                      Streamlit validation runner
requirements.txt
scripts/
  data_loader.py            load + join + pre-checks (source files are read-only)
  normalization.py          trim/identity normalization, identity-only blockers
  clustering.py             identity-fingerprint clusters (cost control)
  output_writer.py          schema, atomic writes, output + checkpoint store
  validator_engine.py       mock + real run loop, clustering reuse, resume
  gemini_client.py          google-genai client + prompt (Gemini only)
  github_checkpoint.py      GitHub Contents API auto-save
  smoke_test.py             fast smoke checks
  run_gemini31_sampled_validation.py   CLI runner
tests/                      pytest suite
data/
  validation_variants_data_v1.json          (source of truth — do not modify)
  validation_instructions_by_id_v1.json      (source of truth — do not modify)
  validated_vehicle_variants_full_gemini31_v1.json            (generated)
  validated_vehicle_variants_full_gemini31_v1.checkpoint.json (generated)
```

## Secrets

Configure `.streamlit/secrets.toml` (see `.streamlit/secrets.toml.example`):

```toml
[github]
token = ""

[google]
api_key = ""
gemini_validator_model_id = "gemini-3.1-pro-preview"
grounding_enabled = true
```

Secret values are never printed or written to files — only presence is shown.

## Run

```bash
# Streamlit UI
streamlit run app.py

# Smoke checks (fast)
python scripts/smoke_test.py

# Unit tests
pytest -q

# CLI (env vars: GEMINI_API_KEY, GITHUB_TOKEN, GITHUB_REPO, GITHUB_BRANCH)
python scripts/run_gemini31_sampled_validation.py --mock --limit 20
python scripts/run_gemini31_sampled_validation.py --real --limit 20
python scripts/run_gemini31_sampled_validation.py --real
```

## GitHub auto-save

After every validated variant the engine writes the output + checkpoint files
locally (atomically) and then pushes them to GitHub via the Contents API, so
progress is recoverable even on Streamlit's ephemeral filesystem. The repo and
branch are auto-detected from the git remote / environment, with optional
`[github].repo` / `[github].branch` overrides in secrets. If a GitHub save
fails the engine stops safely (unless you opt to continue without a remote
checkpoint).
```
```
