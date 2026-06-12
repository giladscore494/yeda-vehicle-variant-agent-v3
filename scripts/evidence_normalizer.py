"""Deterministic evidence normalization for Gemini research packs.

Runs after Gemini returns a research pack and before GPT-5.4 adjudication.
Never trusts the model's self-rated evidence_strength: normalizes source
strength by source type.

Source strength caps (deterministic):
    official_importer, price_list, brochure         => max strong
    israeli_auto_site, dealer_page                  => max medium
    used_listing, non_israeli_technical_source       => max weak
"""

from __future__ import annotations

import re
from typing import Any

# ── Source type enum ──────────────────────────────────────────────────────

VALID_SOURCE_TYPES = frozenset({
    "official_importer",
    "price_list",
    "brochure",
    "israeli_auto_site",
    "dealer_page",
    "used_listing",
    "non_israeli_technical_source",
})

VALID_EVIDENCE_STRENGTHS = frozenset({"strong", "medium", "weak"})

VALID_FIELDS_SUPPORTED = frozenset({
    "israeli_market_presence",
    "model_family",
    "trim_name",
    "official_marketed_name",
    "technical_fingerprint",
})

# ── Strength caps per source type ─────────────────────────────────────────

_STRENGTH_CAP: dict[str, str] = {
    "official_importer": "strong",
    "price_list": "strong",
    "brochure": "strong",
    "israeli_auto_site": "medium",
    "dealer_page": "medium",
    "used_listing": "weak",
    "non_israeli_technical_source": "weak",
}

_STRENGTH_ORDER = {"strong": 3, "medium": 2, "weak": 1}


def cap_strength(source_type: str, claimed: str) -> str:
    """Return the capped evidence strength for a given source type."""
    cap = _STRENGTH_CAP.get(source_type, "weak")
    cap_rank = _STRENGTH_ORDER.get(cap, 1)
    claimed_rank = _STRENGTH_ORDER.get(claimed, 1)
    if claimed_rank > cap_rank:
        return cap
    return claimed if claimed in VALID_EVIDENCE_STRENGTHS else "weak"


# ── URL normalization ─────────────────────────────────────────────────────

_MARKDOWN_URL_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def normalize_url(url: Any) -> str | None:
    """Strip Markdown URL format, return plain URL or None."""
    if url is None:
        return None
    if not isinstance(url, str):
        return None
    url = url.strip()
    if not url:
        return None
    # Extract from Markdown format [text](url) or [url](url)
    match = _MARKDOWN_URL_RE.search(url)
    if match:
        url = match.group(2).strip()
    # Validate it looks like a URL
    if url.startswith(("http://", "https://")):
        return url
    return None


# ── Evidence item normalization ───────────────────────────────────────────

def normalize_evidence_item(item: dict) -> dict | None:
    """Normalize a single evidence item. Returns None if unusable."""
    if not isinstance(item, dict):
        return None

    source_type = (item.get("source_type") or "").strip().lower()
    if source_type not in VALID_SOURCE_TYPES:
        source_type = "non_israeli_technical_source"

    claimed_strength = (item.get("evidence_strength") or "weak").strip().lower()
    normalized_strength = cap_strength(source_type, claimed_strength)

    normalized_url = normalize_url(item.get("source_url"))

    fields = item.get("fields_supported") or []
    if isinstance(fields, list):
        fields = [f for f in fields if f in VALID_FIELDS_SUPPORTED]
    else:
        fields = []

    # Non-Israeli sources must not claim Israeli trim naming support
    if source_type == "non_israeli_technical_source":
        fields = [f for f in fields
                  if f not in ("trim_name", "official_marketed_name",
                               "israeli_market_presence")]

    return {
        "source_title": item.get("source_title") or "",
        "source_type": source_type,
        "source_url": normalized_url if normalized_url else "",
        "language": item.get("language") or "en",
        "fields_supported": fields,
        "evidence_strength": normalized_strength,
        "short_summary": item.get("short_summary") or "",
    }


# ── Deduplication ─────────────────────────────────────────────────────────

def _dedup_key(item: dict) -> str:
    return f"{item.get('source_url', '')}|{item.get('source_title', '')}"


def deduplicate_evidence(items: list[dict]) -> list[dict]:
    """Remove duplicate evidence items by URL+title."""
    seen: set[str] = set()
    result = []
    for item in items:
        key = _dedup_key(item)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def deduplicate_trims(trims: list[dict]) -> list[dict]:
    """Remove duplicate trim entries by normalized trim name."""
    seen: set[str] = set()
    result = []
    for t in trims:
        if not isinstance(t, dict):
            continue
        name = (t.get("trim_name") or "").strip().lower()
        if name and name not in seen:
            seen.add(name)
            result.append(t)
    return result


# ── Full research pack normalization ──────────────────────────────────────

def normalize_research_pack(pack: dict) -> dict:
    """Normalize an entire Gemini research pack in place and return it.

    Applies:
      - Source strength capping
      - URL normalization
      - Evidence deduplication
      - Trim deduplication
      - Invalid source type/field repair
      - Non-Israeli source field stripping
    """
    if not isinstance(pack, dict):
        return pack

    # Normalize evidence items
    raw_items = pack.get("evidence_items") or []
    normalized = []
    for item in raw_items:
        n = normalize_evidence_item(item)
        if n is not None:
            normalized.append(n)
    pack["evidence_items"] = deduplicate_evidence(normalized)

    # Normalize possible trims
    trims = pack.get("possible_israeli_trims_found") or []
    pack["possible_israeli_trims_found"] = deduplicate_trims(trims)

    # Normalize unique mapping candidate
    umc = pack.get("unique_mapping_candidate")
    if isinstance(umc, dict):
        # Cap confidence for weak evidence
        supporting = umc.get("supporting_sources") or []
        if supporting:
            max_strength = max(
                _STRENGTH_ORDER.get(
                    cap_strength(
                        (s.get("source_type") or ""),
                        (s.get("evidence_strength") or "weak"),
                    ),
                    1,
                )
                for s in supporting
                if isinstance(s, dict)
            ) if any(isinstance(s, dict) for s in supporting) else 1
        else:
            max_strength = 1
        conf = umc.get("confidence", 0.0)
        if max_strength == 1 and conf > 0.5:
            umc["confidence"] = 0.5
        elif max_strength == 2 and conf > 0.75:
            umc["confidence"] = 0.75

    # Normalize source_ladder_coverage
    slc = pack.get("source_ladder_coverage")
    if not isinstance(slc, dict):
        pack["source_ladder_coverage"] = {
            "official_importer_checked": False,
            "price_list_or_brochure_checked": False,
            "israeli_auto_sites_checked": False,
            "used_listings_checked_as_weak_support": False,
            "non_israeli_sources_checked_for_technical_only": False,
        }

    return pack


def generate_qa_warnings(pack: dict) -> list[str]:
    """Generate deterministic QA warnings from a normalized research pack."""
    warnings: list[str] = []
    items = pack.get("evidence_items") or []

    if not items:
        warnings.append("no evidence items in research pack")

    strong_items = [i for i in items if i.get("evidence_strength") == "strong"]
    if not strong_items:
        warnings.append("no strong evidence found in research pack")

    slc = pack.get("source_ladder_coverage") or {}
    if not slc.get("official_importer_checked"):
        warnings.append("official importer sources not checked")

    umc = pack.get("unique_mapping_candidate") or {}
    if umc.get("exists") and (umc.get("confidence") or 0) < 0.7:
        warnings.append(
            f"unique mapping candidate confidence too low "
            f"({umc.get('confidence', 0):.2f})")

    split = pack.get("split_indicators") or {}
    if split.get("split_likely"):
        warnings.append("split likely indicated by research")

    return warnings
