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
