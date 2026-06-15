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

### Secrets

The pipeline uses exactly two secret names (no alternatives).

**Required for real GPT-5.4 catalog runs:**

```
OPENAI_API_KEY=<your OpenAI API key>
```

**Required for GitHub checkpoint pushes:**

```
GITHUB_TOKEN=<GitHub token with permission to push to the repository>
```

Both are read from environment variables first, then from Streamlit secrets
using the *same key name* (`st.secrets["OPENAI_API_KEY"]` /
`st.secrets["GITHUB_TOKEN"]`). The legacy nested shapes (`[openai].api_key` /
`[github].token`) remain only as backward-compatible aliases. Secrets are never
printed, logged, written to output, or included in exceptions.

A real run **fails fast** without `OPENAI_API_KEY`:

> `OPENAI_API_KEY is required for real GPT-5.4 grounded catalog runs. Set it in
> environment variables or secrets. Use --offline only for plumbing tests.`

GitHub checkpointing **fails gracefully** without `GITHUB_TOKEN` (only when it
is enabled):

> `GITHUB_TOKEN is required for GitHub checkpoint pushes. Set it in environment
> variables or secrets, or disable GitHub checkpointing.`

Missing `GITHUB_TOKEN` never breaks local/offline runs while checkpointing is off.

**GitHub repository secrets** (Repository → Settings → Secrets and variables →
Actions → New repository secret):

| Name             | Value                                       |
| ---------------- | ------------------------------------------- |
| `OPENAI_API_KEY` | OpenAI API key                              |
| `GITHUB_TOKEN`   | GitHub token with repo push permissions     |

Inside GitHub Actions the built-in `GITHUB_TOKEN` is supported if it has push
permission; outside Actions, provide a personal access token / deploy token as
`GITHUB_TOKEN`.

### Web grounding (mandatory for real runs)

Real catalog runs use the OpenAI **Responses API** with GPT-5.4 and
`tools=[{"type": "web_search"}]`. The model is instructed to ground every
non-null technical field with at least one Israeli-market source; raw database
values are only search *hints*, never evidence. Each `technical_variants_il`
row carries `source_indexes`, `field_sources` (per-field source support), and
`missing_grounded_fields`. A real call is **never** made without `web_search`.
Offline mode is for plumbing tests only and its output is always
`offline_stub=true` / `ready_for_website_upload=false`.

### GitHub checkpointing (model-profile level)

The new pipeline checkpoints **after each completed make/model profile** (never
after each raw variant). After a profile it writes and pushes:

- `data/model_technical_catalog_il.json`
- `data/model_technical_catalog_il_readiness.json`
- `data/model_technical_catalog_il_review.json`

Config (env or `[catalog]` secrets): `github_checkpoint_enabled`,
`push_every_profiles` (real-run default `1`), `strict_github_checkpoint`
(default `false`). Push failures are logged with sanitized errors and counted
in the readiness report (`github_checkpoint_fail_count`,
`last_github_checkpoint_error`); the run only aborts when
`strict_github_checkpoint=true`. No file change → no empty commit.

### Run

```bash
# One-model test sample — offline (no API key, plumbing only). Run this FIRST.
python scripts/run_model_catalog.py --make Abarth --model 500 --limit-models 1 --offline

# One real cluster with GPT-5.4 (needs OPENAI_API_KEY)
python scripts/run_model_catalog.py --make Abarth --model 500 --limit-models 1

# One real cluster + push a GitHub checkpoint after the profile (needs GITHUB_TOKEN)
python scripts/run_model_catalog.py --make Abarth --model 500 --limit-models 1 --github-checkpoint

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
