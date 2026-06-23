"""Non-mutating quality scanner for Israeli technical catalog outputs."""

from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from .catalog_builder import CATALOG_OUTPUT_PATH, REVIEW_OUTPUT_PATH, _atomic_write_json
from .catalog_validation import REQUIRED_WEBSITE_FIELDS
from .openai_catalog_client import GROUNDED_TECHNICAL_FIELDS

QUALITY_SCAN_OUTPUT_PATH = os.path.join(os.path.dirname(CATALOG_OUTPUT_PATH), "model_technical_catalog_il_quality_scan.json")
CANONICAL = {
    "body_type": {"Hatchback", "Sedan", "Estate", "Coupe", "Gran Coupe", "Convertible", "Roadster", "SUV", "Crossover", "MPV", "Van", "Pickup", "Liftback"},
    "fuel_type": {"petrol", "diesel", "electric", "hybrid", "plug_in_hybrid", "mild_hybrid", "lpg", "cng", "hydrogen"},
    "transmission": {"manual", "automatic", "dual_clutch", "cvt", "single_speed"},
    "drivetrain": {"FWD", "RWD", "AWD", "4WD"},
}
MARKETPLACE_HOSTS = ("autoboom", "yad2")
OFFICIAL_HINTS = ("importer", "official", "manufacturer", ".co.il")


def _host(url: str) -> str:
    return (urlparse(url or "").hostname or "").lower().removeprefix("www.")


def _signature_value(value: Any) -> Any:
    """Return a stable, hashable representation for variant signature values."""
    if isinstance(value, (str, int, float, bool, type(None))):
        return value
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=False)
    except TypeError:
        return str(value)


def _models(catalog: Dict[str, Any], review: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [m for m in (catalog.get("models", []) + review.get("models", [])) if isinstance(m, dict)]


def _add(findings: List[Dict[str, Any]], typ: str, severity: str, model: Dict[str, Any], detail: str) -> None:
    findings.append({"type": typ, "severity": severity, "make": model.get("make"), "model": model.get("model"), "detail": detail})


def scan_quality(catalog: Dict[str, Any], review: Dict[str, Any], *, output_path: str = QUALITY_SCAN_OUTPUT_PATH) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    all_models = _models(catalog, review)
    values = defaultdict(set)
    total_cells = grounded_cells = 0
    marketplace_cites = official_cites = all_cites = 0

    for model in all_models:
        sources = model.get("sources") or []
        src_by_idx = {s.get("source_index", i): s for i, s in enumerate(sources) if isinstance(s, dict)}
        model_market = model_all = 0
        model_grounded = model_cells = 0
        for src in sources:
            h = _host(src.get("url", ""))
            if h and not (h.endswith(".il") or h == "he.wikipedia.org"):
                _add(findings, "source_domain", "leak", model, f"non Israeli source host: {h}")
        variants = model.get("technical_variants_il") or []
        signatures = defaultdict(list)
        for i, v in enumerate(variants):
            if not isinstance(v, dict):
                continue
            fs = v.get("field_sources") if isinstance(v.get("field_sources"), dict) else {}
            missing = v.get("missing_grounded_fields") or []
            non_null = [f for f in GROUNDED_TECHNICAL_FIELDS if v.get(f) not in (None, "")]
            if v.get("support_level") == "indirect" and non_null and all(fs.get(f) for f in non_null) and not missing:
                _add(findings, "support_level_invariant", "bug", model, f"variant[{i}] is indirect but all non-null fields are grounded")
            for f in ("body_type", "fuel_type", "transmission", "drivetrain", "engine"):
                val = v.get(f)
                if val not in (None, ""):
                    values[f].add(str(val))
            for f in GROUNDED_TECHNICAL_FIELDS:
                if v.get(f) in (None, ""):
                    continue
                total_cells += 1; model_cells += 1
                refs = fs.get(f) or []
                if refs:
                    grounded_cells += 1; model_grounded += 1
                hosts = [_host((src_by_idx.get(r) or {}).get("url", "")) for r in refs]
                for h in hosts:
                    if not h:
                        continue
                    all_cites += 1; model_all += 1
                    if any(x in h for x in MARKETPLACE_HOSTS):
                        marketplace_cites += 1; model_market += 1
                    if any(x in h for x in OFFICIAL_HINTS):
                        official_cites += 1
                if f in {"version_or_trim", "year_start", "year_end"} and refs and all(any(x in h for x in MARKETPLACE_HOSTS) for h in hosts):
                    _add(findings, "source_tier_inversion", "leak", model, f"variant[{i}] {f} grounded only by marketplace/aggregator source(s): {hosts}")
            sig = tuple(_signature_value(v.get(k)) for k in ("body_type", "fuel_type", "engine", "horsepower_hp", "transmission", "drivetrain"))
            signatures[sig].append((i, _signature_value(v.get("year_start")), _signature_value(v.get("year_end"))))
        for sig, rows in signatures.items():
            if len(rows) > 1 and len({(r[1], r[2]) for r in rows}) > 1:
                _add(findings, "year_split_duplicates", "structure", model, f"merge candidate signature={sig} rows={rows}")
        if model_cells:
            _add(findings, "grounding_completeness", "structure", model, f"{model_grounded}/{model_cells} grounded cells ({model_grounded/model_cells:.1%})")
        if model_all and model_market / model_all > 0.5:
            _add(findings, "source_tier_inversion", "leak", model, f"marketplace citation share {model_market/model_all:.1%}")
        for label in model.get("invalid_or_non_trim_labels") or []:
            if not isinstance(label, dict):
                continue
            text = str(label.get("label", "")).strip()
            cls = label.get("classification")
            combined = f"{model.get('model','')}{text}".replace(" ", "")
            if cls in {"engine_size", "horsepower"} and re.match(r"^[A-Za-z]+\d+[A-Za-z0-9]*$", combined):
                _add(findings, "false_rejection_scan", "bug", model, f"candidate designation wrongly rejected: {combined}")

    for field, vals in values.items():
        if field in CANONICAL:
            for val in vals:
                base = re.sub(r"^\d+-speed\s+", "", val.lower()).replace(" ", "_") if field == "transmission" else val
                ok = val in CANONICAL[field] or (field == "transmission" and base in CANONICAL[field])
                if not ok:
                    findings.append({"type": "canonical_consistency", "severity": "normalization", "make": None, "model": None, "detail": f"{field} value outside canonical list: {val}"})
            normalized = defaultdict(list)
            for val in vals:
                normalized[re.sub(r"[^a-z0-9]", "", val.lower())].append(val)
            for group in normalized.values():
                if len(set(group)) > 1:
                    findings.append({"type": "canonical_consistency", "severity": "normalization", "make": None, "model": None, "detail": f"{field} case/format variants: {sorted(group)}"})

    counts_by_type = dict(Counter(f["type"] for f in findings))
    sev_counts = Counter(f["severity"] for f in findings)
    report = {"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "totals": {"models": len(all_models), "findings": len(findings), "grounded_cells": grounded_cells, "total_cells": total_cells, "marketplace_citation_share": (marketplace_cites / all_cites if all_cites else 0), "official_citations": official_cites, "bug": sev_counts.get("bug", 0), "leak": sev_counts.get("leak", 0), "normalization": sev_counts.get("normalization", 0), "structure": sev_counts.get("structure", 0)}, "findings": findings, "counts_by_type": counts_by_type}
    _atomic_write_json(output_path, report)
    return report


def main() -> None:
    """Run the quality scan against the default catalog and review files."""
    with open(CATALOG_OUTPUT_PATH, encoding="utf-8") as f:
        catalog = json.load(f)
    with open(REVIEW_OUTPUT_PATH, encoding="utf-8") as f:
        review = json.load(f)
    scan_quality(catalog, review)


if __name__ == "__main__":
    main()
