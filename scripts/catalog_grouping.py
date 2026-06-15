"""Group mapped variants into make/model clusters for the GPT-5.4 catalog.

The new single-model technical-catalog pipeline reads ONLY the two source
files (variants + optional instructions metadata), groups the raw mapped
variants by ``market_scope + make + model`` and collects the distinct raw
technical values seen per cluster. Exactly one GPT-5.4 request is sent per
cluster — never one per variant row.

Nothing here calls a model, validates per row, or reads any legacy generated
output. It only reshapes the source data into compact per-model payloads.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .data_loader import get_standard, get_validation_id


def _clean_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _sorted_unique_strings(values: List[Any]) -> List[str]:
    seen: Dict[str, str] = {}
    for raw in values:
        text = _clean_str(raw)
        if text is None:
            continue
        seen.setdefault(text.lower(), text)
    return [seen[k] for k in sorted(seen)]


def _sorted_unique_numbers(values: List[Any]) -> List[Any]:
    out = set()
    for raw in values:
        if raw is None:
            continue
        try:
            if isinstance(raw, bool):
                continue
            num = int(raw) if float(raw).is_integer() else float(raw)
        except (TypeError, ValueError):
            continue
        out.add(num)
    return sorted(out)


@dataclass
class ModelGroup:
    """One ``market + make + model`` cluster of mapped variants."""

    market_scope: str
    make: str
    model: str
    validation_ids: List[str] = field(default_factory=list)
    source_indexes: List[int] = field(default_factory=list)
    raw_database_values: Dict[str, Any] = field(default_factory=dict)
    instruction_metadata: Dict[str, Any] = field(default_factory=dict)
    raw_variant_count: int = 0

    @property
    def key(self) -> str:
        return f"{self.market_scope}|{self.make}|{self.model}"

    def request_payload(self) -> Dict[str, Any]:
        """The compact JSON sent to GPT-5.4 for this cluster."""
        return {
            "task": "build_israeli_model_technical_catalog",
            "market": self.market_scope or "IL",
            "make": self.make,
            "model": self.model,
            "raw_database_values": self.raw_database_values,
            "sample_validation_ids": self.validation_ids[:25],
            "source_indexes": self.source_indexes,
            "metadata_hints": self.instruction_metadata,
            "question": (
                "Using Israeli-market sources, return the technical versions of "
                "this make/model that were actually sold in Israel. Return only "
                "technical data."
            ),
        }


def _collect_metadata(
    validation_ids: List[str], instructions: Dict[str, Any]
) -> Dict[str, Any]:
    """Pull only optional hints from the instructions file (never facts)."""
    priorities: List[str] = []
    risk_routes: List[str] = []
    problematic = 0
    for vid in validation_ids:
        instr = instructions.get(vid)
        if not isinstance(instr, dict):
            continue
        prio = _clean_str(instr.get("validation_priority"))
        if prio:
            priorities.append(prio)
        route = _clean_str(instr.get("ai_validation_route"))
        if route:
            risk_routes.append(route)
        if instr.get("is_possible_duplicate_after_mapping"):
            problematic += 1
    return {
        "priorities_seen": _sorted_unique_strings(priorities),
        "validation_routes_seen": _sorted_unique_strings(risk_routes),
        "possible_duplicate_rows": problematic,
        "validation_id_count": len(validation_ids),
    }


def group_variants(
    variants: List[Dict[str, Any]],
    instructions: Optional[Dict[str, Any]] = None,
) -> List[ModelGroup]:
    """Group variants by ``market_scope + make + model``.

    Returns one :class:`ModelGroup` per cluster, with the distinct raw values
    seen (years/trims/engines/transmissions/body/fuel/drivetrain/horsepower).
    """
    instructions = instructions or {}
    buckets: Dict[str, Dict[str, Any]] = {}
    order: List[str] = []

    for variant in variants:
        std = get_standard(variant)
        make = _clean_str(std.get("make"))
        model = _clean_str(std.get("model"))
        if not make or not model:
            continue
        market = _clean_str(std.get("market_scope")) or "IL"
        key = f"{market}|{make}|{model}"
        if key not in buckets:
            buckets[key] = {
                "market": market,
                "make": make,
                "model": model,
                "validation_ids": [],
                "source_indexes": [],
                "row_count": 0,
                "years": [],
                "trims": [],
                "engines": [],
                "horsepower": [],
                "transmissions": [],
                "body_types": [],
                "fuel_types": [],
                "drivetrains": [],
            }
            order.append(key)
        b = buckets[key]
        b["row_count"] += 1
        vid = get_validation_id(variant)
        if vid:
            b["validation_ids"].append(vid)
        src_idx = variant.get("source_index")
        if isinstance(src_idx, int):
            b["source_indexes"].append(src_idx)
        b["years"].extend([std.get("year_start"), std.get("year_end")])
        b["trims"].append(std.get("trim"))
        b["engines"].append(std.get("engine"))
        for hp_key in ("horsepower", "horsepower_hp", "hp"):
            if std.get(hp_key) is not None:
                b["horsepower"].append(std.get(hp_key))
        b["transmissions"].append(std.get("transmission"))
        b["body_types"].append(std.get("body_type"))
        b["fuel_types"].append(std.get("fuel_type"))
        b["drivetrains"].append(std.get("drivetrain"))

    groups: List[ModelGroup] = []
    for key in order:
        b = buckets[key]
        raw_values = {
            "years_seen": _sorted_unique_numbers(b["years"]),
            "trims_seen": _sorted_unique_strings(b["trims"]),
            "engines_seen": _sorted_unique_strings(b["engines"]),
            "horsepower_seen": _sorted_unique_numbers(b["horsepower"]),
            "transmissions_seen": _sorted_unique_strings(b["transmissions"]),
            "body_types_seen": _sorted_unique_strings(b["body_types"]),
            "fuel_types_seen": _sorted_unique_strings(b["fuel_types"]),
            "drivetrains_seen": _sorted_unique_strings(b["drivetrains"]),
        }
        groups.append(
            ModelGroup(
                market_scope=b["market"],
                make=b["make"],
                model=b["model"],
                validation_ids=b["validation_ids"],
                source_indexes=sorted(set(b["source_indexes"])),
                raw_database_values=raw_values,
                instruction_metadata=_collect_metadata(
                    b["validation_ids"], instructions
                ),
                raw_variant_count=b["row_count"],
            )
        )
    return groups


def select_groups(
    groups: List[ModelGroup],
    *,
    make: Optional[str] = None,
    model: Optional[str] = None,
    limit_models: Optional[int] = None,
    start_after_key: Optional[str] = None,
) -> List[ModelGroup]:
    """Filter/limit clusters for one run.

    ``start_after_key`` resumes processing AFTER the cluster whose ``key``
    (``market|make|model``) matches, so a long run can be continued in batches.
    """
    selected = groups
    if make:
        selected = [g for g in selected if g.make.lower() == make.lower()]
    if model:
        selected = [g for g in selected if g.model.lower() == model.lower()]
    if start_after_key:
        target = start_after_key.strip()
        keys = [g.key for g in selected]
        if target in keys:
            selected = selected[keys.index(target) + 1:]
    if limit_models is not None and limit_models >= 0:
        selected = selected[:limit_models]
    return selected
