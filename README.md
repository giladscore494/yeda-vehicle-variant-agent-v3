# Yeda Vehicle Variant Agent v3

Simplified, reliable data-generation engine for Israeli vehicle model/variant data.

## Setup

1. Copy `secrets.example.py` to `secrets.py` and fill in your API keys.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the UI: `streamlit run app.py`

## Structure

- `core/` — Normalization, schemas, source ID validation, variant ID generation
- `llm/` — LLM client, prompt building, response parsing
- `engine/` — Decision, apply, audit, save, progress, batch orchestration
- `storage/` — GitHub remote push
- `tools/` — Migration and audit utilities
- `tests/` — Unit tests
- `data/canonical/` — Canonical resume package
- `data/seeds/` — Seed catalog
- `data/runtime/` — Runtime progress state (not committed)

## Running Tests

```bash
pytest tests/ -v
```

## Validation File Hierarchy

- **Source database** — `data/canonical/resume_package_canonical.json` is the read-only source of truth for validation. The validation UI and final export must never overwrite it, and the stale root-level `resume_package_canonical.json` is not used by the validation workflow.
- **Issue queue** — `data/validation/issue_queue.json` contains deterministic audit findings that need manual review or model review.
- **Decisions** — `data/validation/decisions.json` stores proposed validation decisions from deterministic tooling and model review. These are working decisions, not direct mutations of the source canonical file.
- **Manifest** — `data/validation/manifest.json` records validation run metadata and final export metadata.
- **Final clean database** — `data/final/resume_package_final_clean.json` is the only final cleaned database output. It is generated separately from the source canonical by the final export step.

## How models are used

- The deterministic audit scans all source data and builds the issue queue.
- Models review only problematic queue items selected for AI review; they do not scan or rewrite the full database.
- Gemini is the primary factual validator for model-reviewed queue items.
- OpenAI is the second-opinion reviewer when routing requests an additional review.
- Model-generated decisions remain manual-review only unless a future workflow explicitly marks a decision `safe_to_auto_apply=true`.
- The source canonical database is never mutated by validation or model review.
- The final clean database is exported separately to `data/final/resume_package_final_clean.json`.
