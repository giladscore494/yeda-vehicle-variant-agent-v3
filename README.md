# Israeli-Market Vehicle Technical Catalog (GPT-5.4)

The active pipeline is a **single-GPT-5.4** Israeli-market *technical catalog*
builder. For each make/model it asks GPT-5.4 one question — *what technical
versions were actually sold in Israel?* — and collects only technical data
(engines, horsepower, transmissions, drivetrain, body type, fuel type, years,
trims/versions, sources). GPT-5.4 makes **no** publication / route / risk /
guard / readiness decisions; Python validates the returned profile.

> **No Gemini. No legacy guard verifier. No repair adjudicator. No per-row
> validation. One GPT-5.4 call per make/model cluster — never one per variant.**

## New catalog pipeline

```
scripts/
  catalog_grouping.py       group variants by market+make+model, collect raw values
  openai_catalog_client.py  GPT-5.4 client (one call per cluster) + offline synth
  catalog_validation.py     schema/identity validation, de-dupe, website values
  catalog_builder.py        orchestrator -> writes the three output files
  run_model_catalog.py      CLI runner (supports the one-model test sample)
```

Source files (the **only** inputs — never modified):

- `data/validation_variants_data_v1.json` — mapped variants (raw technical values)
- `data/validation_instructions_by_id_v1.json` — optional metadata hints only

Output files (generated, git-ignored):

- `data/model_technical_catalog_il.json` — website-ready models
- `data/model_technical_catalog_il_readiness.json` — QA readiness report
- `data/model_technical_catalog_il_review.json` — incomplete / blocked models

### Feature flag

`SINGLE_GPT54_MODEL_CATALOG_MODE=true` (default true) enables catalog mode and
disables Gemini, the legacy guard verifier, the repair adjudicator, and per-row
validation.

### Run

```bash
# One-model test sample — offline (no API key, plumbing only). Run this FIRST.
python scripts/run_model_catalog.py --make Abarth --model 500 --limit-models 1 --offline

# One real cluster with GPT-5.4 (needs OPENAI_API_KEY)
python scripts/run_model_catalog.py --make Abarth --model 500 --limit-models 1

# Full run — only after the one-model sample passes
python scripts/run_model_catalog.py
```

The retired Gemini/guard/repair engine below is kept for reference only and is
not part of the new flow. Legacy generated outputs are git-ignored and must
never be used as source data.

---

# (Retired) Gemini 3.1 Validation Engine

A practical, **Gemini-only** validation engine with a Streamlit runner. It
validates and lightly enriches all raw vehicle variants into a single output
file, preserving every original `validation_id`.

> **Core principle:** vehicle identity is strict, trim enrichment is flexible.
> A real Israeli-market variant is **never** rejected only because the trim is
> weak, generic, missing, or hard to verify — weak trim becomes `clean_partial`.

No old deterministic QA rejection gate.

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
