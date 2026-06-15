# Israeli-Market Vehicle Technical Catalog (GPT-5.4)

This project now has **one production path**: GPT-5.4 Israeli vehicle
model/variant *technical catalog* generation.

For each make/model cluster it asks GPT-5.4 a single grounded question — *what
technical versions were actually sold in Israel?* — and collects only technical
data (engines, horsepower, transmissions, drivetrain, body type, fuel type,
years, trims/versions, sources). GPT-5.4 makes **no** publication / route / risk
/ readiness decisions; Python validates the returned profile and routes it to
the website-ready catalog or to review.

> **GPT-5.4 is the only model**, with no fallback model and no second model in
> the loop. One grounded GPT-5.4 call per make/model cluster — never one per
> variant.

## Layout

```
app.py                          Streamlit runner (single GPT-5.4 catalog flow)
scripts/
  config.py                     shared config (OpenAI + GitHub secrets only)
  data_loader.py                load + join the two read-only source files
  catalog_grouping.py           group variants by market+make+model
  openai_catalog_client.py      GPT-5.4 client (one grounded call per cluster)
  json_utils.py                 neutral strict-JSON parser (no provider import)
  catalog_validation.py         schema/identity validation, de-dupe, website values
  catalog_builder.py            orchestrator -> writes the three output files
  catalog_checkpoint.py         model-profile GitHub checkpointing
  github_checkpoint.py          GitHub Contents API saver
  run_model_catalog.py          CLI runner (single entrypoint)
tests/                          pytest suite (GPT-5.4-only contract)
```

Source files (the **only** inputs — never modified):

- `data/validation_variants_data_v1.json` — mapped variants (raw technical values)
- `data/validation_instructions_by_id_v1.json` — optional metadata hints only

Output files (generated, git-ignored):

- `data/model_technical_catalog_il.json` — website-ready models
- `data/model_technical_catalog_il_readiness.json` — QA readiness report
- `data/model_technical_catalog_il_review.json` — incomplete / blocked models

## Secrets

| Name                        | Required | Purpose                                            |
| --------------------------- | -------- | -------------------------------------------------- |
| `OPENAI_API_KEY`            | **yes**  | GPT-5.4 grounded catalog runs (web_search).        |
| `OPENAI_VALIDATOR_MODEL_ID` | no       | Model id override; default `gpt-5.4`.              |
| `GITHUB_TOKEN`              | no       | GitHub checkpoint pushes (only when enabled).      |
| `GITHUB_CHECKPOINT_ENABLED` | no       | Enable per-profile GitHub checkpointing.           |
| `PUSH_EVERY_PROFILES`       | no       | Checkpoint cadence (default `1`).                  |
| `STRICT_GITHUB_CHECKPOINT`  | no       | Abort the run on a checkpoint push failure.        |

Secrets are read from environment variables first, then from Streamlit secrets
using the *same key name* (e.g. `st.secrets["OPENAI_API_KEY"]`). The legacy
nested shapes (`[openai].api_key` / `[openai].validator_model_id` /
`[github].token`) remain only as backward-compatible aliases. Secrets are never
printed, logged, written to output, or included in exceptions.

**Fail closed:** a run without `OPENAI_API_KEY` stops with a clear error and
never synthesizes, falls back, or uses cached data:

> `OPENAI_API_KEY is required for GPT-5.4 grounded catalog runs. Set it in
> environment variables or secrets.`

GitHub checkpointing **fails gracefully** without `GITHUB_TOKEN` (only when it
is enabled):

> `GITHUB_TOKEN is required for GitHub checkpoint pushes. Set it in environment
> variables or secrets, or disable GitHub checkpointing.`

## Web grounding (mandatory)

Runs use the OpenAI **Responses API** with GPT-5.4 and
`tools=[{"type": "web_search"}]`, `max_output_tokens`. The model is instructed
to ground every non-null technical field with at least one Israeli-market
source; raw database values are only search *hints*, never evidence. Each
`technical_variants_il` row carries `source_indexes`, `field_sources`
(per-field source support) and `missing_grounded_fields`. A call is **never**
made without `web_search`.

## GitHub checkpointing (model-profile level)

The pipeline checkpoints **after each completed make/model profile** (never
after each raw variant). After a profile it writes and pushes the three output
files. Config (env or `[catalog]` secrets): `github_checkpoint_enabled`,
`push_every_profiles` (default `1`), `strict_github_checkpoint` (default
`false`). Push failures are logged with sanitized errors and counted in the
readiness report; the run only aborts when `strict_github_checkpoint=true`.

## Run

### Streamlit

```bash
streamlit run app.py
```

The UI shows source/secret/model/output status, lets you filter by make/model,
choose a run count/limit, optionally resume after a cluster key, toggle GitHub
checkpointing, and shows the current item being processed live.

### CLI

```bash
# Process at most 10 clusters
python -m scripts.run_model_catalog --limit-models 10

# One real cluster with GPT-5.4
python -m scripts.run_model_catalog --make "Alfa Romeo" --model Tonale --limit-models 1

# Resume after a cluster key (format: market|make|model)
python -m scripts.run_model_catalog --start-after-key "IL|Abarth|500" --limit-models 5

# One cluster + push a GitHub checkpoint after the profile (needs GITHUB_TOKEN)
python -m scripts.run_model_catalog --make Abarth --model 500 --limit-models 1 --github-checkpoint
```

The CLI prints live `[i/total] RUNNING …` / `[i/total] DONE …` progress to
stderr and the final readiness report (JSON) to stdout.

## Tests

```bash
python -m compileall scripts app.py
pytest -q
```
