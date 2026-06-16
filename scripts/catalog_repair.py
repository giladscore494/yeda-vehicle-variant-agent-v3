"""Targeted repair mode for quality-blocked catalog profiles."""

from __future__ import annotations

import copy
import json
from typing import Any, Callable, Dict, List, Optional

from .catalog_builder import (
    CATALOG_OUTPUT_PATH,
    READINESS_OUTPUT_PATH,
    REVIEW_OUTPUT_PATH,
    _model_key,
    load_existing_outputs,
    merge_and_write_outputs,
)
from .catalog_checkpoint import CatalogCheckpointConfig, CatalogCheckpointer
from .catalog_validation import (
    REQUIRED_WEBSITE_FIELDS,
    _valid_source_indexes,
    derive_available_values,
    validate_profile,
)
from .openai_catalog_client import CatalogClientSettings, GROUNDED_TECHNICAL_FIELDS
from .catalog_provider import CatalogProviderSettings, ProviderUnavailableError, build_catalog_client, check_provider_available
from .security import sanitize_error

MAX_REPAIR_ATTEMPTS = 2

# Substrings that identify a provider/setup/dependency/API-key/import failure
# rather than a genuine model/data repair failure. These must never consume a
# repair attempt or mark a model as repair_exhausted.
PROVIDER_SETUP_ERROR_MARKERS = (
    "Gemini client library is not installed",
    "Gemini client library is unavailable",
    "google-genai",
    "No module named",
    "ImportError",
    "cannot import name",
    "ProviderUnavailableError",
    "API key is missing",
    "Selected provider API key is missing",
    "OpenAI client library is not installed",
    "Google API key is missing",
    "OpenAI API key is missing",
)

_CHECKPOINT_STATE_FIELDS = (
    "github_checkpoint_enabled",
    "github_checkpoint_unit",
    "github_checkpoint_count",
    "github_checkpoint_fail_count",
    "last_github_checkpoint_error",
    "last_checkpointed_profile_id",
    "last_repair_checkpointed_profile_id",
)

# Review-only bookkeeping keys that must never leak into the clean catalog.
_REVIEW_ONLY_KEYS = (
    "validation_issues",
    "repair_attempts",
    "repair_exhausted",
    "last_repair_error",
    "request_payload",
)


def _error_strings(value: Any) -> List[str]:
    """Safely collect candidate error strings from a value of any shape."""
    if value is None:
        return []
    if isinstance(value, dict):
        strings: List[str] = []
        for field in ("last_repair_error", "error"):
            field_value = value.get(field)
            if field_value:
                strings.append(str(field_value))
        return strings
    if isinstance(value, BaseException):
        # repr exposes the exception type name (e.g. ImportError) in addition
        # to the message, so markers like "ImportError" match reliably.
        return [str(value), repr(value)]
    return [str(value)]


def is_provider_setup_error(value: Any) -> bool:
    """Return True when value represents a provider/setup/dependency failure.

    Accepts exceptions, raw strings, or review entries (dicts). Provider/setup
    failures must not be counted as genuine repair attempts.
    """
    for text in _error_strings(value):
        if any(marker in text for marker in PROVIDER_SETUP_ERROR_MARKERS):
            return True
    return False


def _derivable_source_indexes(variant: Dict[str, Any]) -> List[int]:
    """The variant-level source_indexes implied by its grounded field_sources.

    These are the unique source ids that the variant's own ``field_sources``
    already reference for grounded fields — i.e. the deterministic value the
    missing ``source_indexes`` should have had.
    """
    field_sources = variant.get("field_sources")
    if not isinstance(field_sources, dict):
        return []
    refs: set = set()
    for fname in GROUNDED_TECHNICAL_FIELDS:
        for ref in field_sources.get(fname) or []:
            if isinstance(ref, int):
                refs.add(ref)
    return sorted(refs)


def patch_source_indexes_from_field_sources(variant: Dict[str, Any]) -> bool:
    """Deterministically fill a variant's missing ``source_indexes`` (spec 8).

    If ``field_sources`` is populated for grounded fields but the variant-level
    ``source_indexes`` is missing/empty, set ``source_indexes`` to the sorted,
    unique source ids those grounded fields reference. No model call needed.
    Returns True when a patch was applied.
    """
    if not isinstance(variant, dict):
        return False
    existing = variant.get("source_indexes")
    if isinstance(existing, list) and existing:
        return False
    derived = _derivable_source_indexes(variant)
    if not derived:
        return False
    variant["source_indexes"] = derived
    return True


def recover_identity_from_payload(entry: Dict[str, Any]) -> bool:
    """Deterministically restore top-level identity for a review entry (spec 9).

    Identity is recovered ONLY from an attached ``request_payload`` (never
    invented). ``canonical_model`` defaults to ``model`` once ``model`` is known.
    Returns True when any identity field was filled.
    """
    if not isinstance(entry, dict):
        return False
    rp = entry.get("request_payload") if isinstance(entry.get("request_payload"), dict) else {}
    changed = False
    if not entry.get("market"):
        recovered = rp.get("market") or ("IL" if (rp.get("make") or rp.get("model")) else None)
        if recovered:
            entry["market"] = recovered
            changed = True
    if not entry.get("make") and rp.get("make"):
        entry["make"] = rp.get("make")
        changed = True
    if not entry.get("model") and rp.get("model"):
        entry["model"] = rp.get("model")
        changed = True
    if entry.get("model") and not entry.get("canonical_model"):
        entry["canonical_model"] = entry["model"]
        changed = True
    return changed


def apply_deterministic_patches(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Apply model-free repairs (identity + source_indexes) and return a copy."""
    patched = copy.deepcopy(entry)
    recover_identity_from_payload(patched)
    for variant in patched.get("technical_variants_il") or []:
        if isinstance(variant, dict):
            patch_source_indexes_from_field_sources(variant)
    return patched


def derive_repair_targets(profile: Dict[str, Any]) -> Dict[int, List[str]]:
    """Map variant index -> fields a model must re-ground.

    Detects (spec 7): missing required fields, non-null fields lacking
    field_sources, declared missing_grounded_fields, AND structural source
    grounding problems — a variant with no source_indexes that cannot be
    self-healed from field_sources, or source/field_sources references to
    source ids that do not exist. When any structural problem is present, all
    present grounded fields are flagged so the model re-grounds them (the pure
    source_indexes-only case is patched deterministically elsewhere, so it does
    not reach here).
    """
    targets: Dict[int, List[str]] = {}
    variants = profile.get("technical_variants_il") or []
    valid_source_indexes = _valid_source_indexes(profile.get("sources"))
    for idx, variant in enumerate(variants):
        if not isinstance(variant, dict):
            continue
        field_sources = variant.get("field_sources") if isinstance(variant.get("field_sources"), dict) else {}
        missing = set(variant.get("missing_grounded_fields") or [])
        fields = set()
        for fname in REQUIRED_WEBSITE_FIELDS:
            if variant.get(fname) in (None, ""):
                fields.add(fname)
        for fname in GROUNDED_TECHNICAL_FIELDS:
            if variant.get(fname) not in (None, "") and not field_sources.get(fname):
                fields.add(fname)
        fields.update(f for f in missing if isinstance(f, str))

        present_grounded = [
            fname for fname in GROUNDED_TECHNICAL_FIELDS if variant.get(fname) not in (None, "")
        ]

        # Structural source_indexes problems.
        src_indexes = variant.get("source_indexes")
        has_source_indexes = isinstance(src_indexes, list) and bool(src_indexes)
        if not has_source_indexes and not _derivable_source_indexes(variant):
            # Cannot self-heal: the model must re-ground this variant.
            fields.update(present_grounded)

        # References (variant-level or field_sources) to non-existent sources.
        invalid_ref = any(
            isinstance(ref, int) and ref not in valid_source_indexes
            for ref in (src_indexes or [])
        )
        if not invalid_ref:
            for refs in field_sources.values():
                if isinstance(refs, list) and any(
                    isinstance(ref, int) and ref not in valid_source_indexes for ref in refs
                ):
                    invalid_ref = True
                    break
        if invalid_ref:
            fields.update(present_grounded)

        if fields:
            targets[idx] = sorted(fields)
    return targets


def _stable(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def merge_repair(existing: Dict[str, Any], repaired: Dict[str, Any], targets: Dict[int, List[str]]) -> Dict[str, Any]:
    patched = copy.deepcopy(existing)
    old_variants = existing.get("technical_variants_il") or []
    new_variants = repaired.get("technical_variants_il") or []
    if len(old_variants) != len(new_variants):
        raise ValueError("repair changed variant count")
    for idx, (old_v, new_v) in enumerate(zip(old_variants, new_variants)):
        allowed = set(targets.get(idx, []))
        if not allowed:
            if _stable(old_v) != _stable(new_v):
                raise ValueError(f"repair altered untargeted variant[{idx}]")
            continue
        for key, old_value in old_v.items():
            if key in allowed or key in {"field_sources", "missing_grounded_fields", "source_indexes", "support_level"}:
                continue
            if _stable(old_value) != _stable(new_v.get(key)):
                raise ValueError(f"repair altered untargeted variant[{idx}].{key}")
        for field in allowed:
            patched["technical_variants_il"][idx][field] = new_v.get(field)
        for meta in ("field_sources", "missing_grounded_fields", "source_indexes", "support_level"):
            if meta in new_v:
                patched["technical_variants_il"][idx][meta] = copy.deepcopy(new_v[meta])
    if _stable(existing.get("sources")) != _stable(repaired.get("sources")):
        patched["sources"] = copy.deepcopy(repaired.get("sources", []))
    patched["available_values_for_website"] = derive_available_values(patched.get("technical_variants_il") or [])
    return patched


def clear_provider_unavailable_repair_errors(review: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy with provider/setup repair pollution cleared.

    Removes repair metadata whose last error was a provider/setup/dependency
    failure (e.g. the missing google-genai SDK) so those models are retried
    instead of staying stuck as exhausted.
    """
    cleaned = copy.deepcopy(review)
    for entry in cleaned.get("models", []) or []:
        if not isinstance(entry, dict):
            continue
        if not is_provider_setup_error(entry):
            continue
        entry.pop("last_repair_error", None)
        entry.pop("repair_exhausted", None)
        if int(entry.get("repair_attempts", 0) or 0) > 0:
            entry["repair_attempts"] = 0
    return cleaned


FULL_REBUILD_ISSUE_MARKERS = (
    "technical_variants_il missing or not a list",
    "technical_variants_il is empty",
    "catalog client returned non-object JSON",
    "Extra data:",
    "strict JSON",
    "JSON parse",
    "non-object JSON",
)


def _needs_full_rebuild(entry: Dict[str, Any]) -> bool:
    variants = entry.get("technical_variants_il")
    issues = [str(i) for i in (entry.get("validation_issues") or [])]
    texts = issues + [str(entry.get("error") or ""), str(entry.get("last_repair_error") or "")]
    if entry.get("rebuild_required") is True:
        return True
    if entry.get("error") and not variants:
        return True
    marker_match = any(marker in text for marker in FULL_REBUILD_ISSUE_MARKERS for text in texts)
    if marker_match:
        return True
    # Legacy tests/fixtures use empty profiles as generic blocked entries
    # without request_payload; those can still follow the old deterministic
    # revalidate path. Real parse/API failures include request_payload and are
    # marked/validated with the explicit empty-variants issue above.
    return bool((variants == [] or variants is None) and isinstance(entry.get("request_payload"), dict))


def _enforce_rebuilt_identity(rebuilt: Dict[str, Any], request_payload: Dict[str, Any]) -> Dict[str, Any]:
    rebuilt = dict(rebuilt)
    rebuilt["market"] = request_payload["market"]
    rebuilt["make"] = request_payload["make"]
    rebuilt["model"] = request_payload["model"]
    rebuilt["canonical_model"] = rebuilt.get("canonical_model") or request_payload["model"]
    rebuilt["profile_confidence"] = rebuilt.get("profile_confidence") or "medium"
    return rebuilt


def repair_review_models(
    batch: Optional[int] = None,
    *,
    selected_keys: Optional[list[str]] = None,
    provider_settings: Optional[CatalogProviderSettings] = None,
    settings: Optional[CatalogClientSettings] = None,
    checkpoint: Optional[CatalogCheckpointConfig] = None,
    log: Optional[Callable[[str], None]] = None,
    catalog_path: str = CATALOG_OUTPUT_PATH,
    readiness_path: str = READINESS_OUTPUT_PATH,
    review_path: str = REVIEW_OUTPUT_PATH,
) -> Dict[str, Any]:
    emit = log or (lambda _msg: None)
    if provider_settings is None:
        settings = settings or CatalogClientSettings()
        provider_settings = CatalogProviderSettings(
            provider="openai", display_name="GPT-5.4", model_id=settings.model_id,
            api_key=settings.api_key, web_search_enabled=settings.use_web_search
        )
    settings = settings or CatalogClientSettings(api_key=provider_settings.api_key, model_id=provider_settings.model_id, use_web_search=provider_settings.web_search_enabled)

    # Fatal provider preflight — do not write any output.
    try:
        check_provider_available(provider_settings)
        client = build_catalog_client(provider_settings)
    except ProviderUnavailableError:
        raise

    checkpointer = CatalogCheckpointer(checkpoint or CatalogCheckpointConfig(), log=emit)

    catalog, readiness, review = load_existing_outputs(catalog_path, readiness_path, review_path)

    # Carry forward existing checkpoint state so counts and last-id survive restarts.
    for field in _CHECKPOINT_STATE_FIELDS:
        if field in readiness:
            checkpointer.state[field] = readiness[field]

    # Repair must NOT advance the main build resume pointer. Snapshot it so we
    # can restore it after each (potentially github-pushing) checkpoint call,
    # which would otherwise overwrite it with the repaired profile id.
    build_resume_pointer = checkpointer.state.get("last_checkpointed_profile_id")

    review_models = [m for m in review.get("models", []) if isinstance(m, dict)]
    processed = promoted = kept = skipped = 0

    selected_set = set(selected_keys or [])
    for model_entry in review_models:
        key = _model_key(model_entry)
        if selected_keys is not None and key not in selected_set:
            skipped += 1
            continue
        if batch is not None and not selected_keys and processed >= batch:
            break
        if is_provider_setup_error(model_entry):
            # Previous attempts were consumed by a provider/setup/dependency
            # failure, not genuine model/data repair. Discount them so the
            # model is retried instead of staying stuck as exhausted.
            model_entry = dict(model_entry)
            model_entry["repair_attempts"] = 0
            model_entry.pop("repair_exhausted", None)
            model_entry.pop("last_repair_error", None)
            emit(f"RESET provider/setup pollution: {key}")
        attempts = int(model_entry.get("repair_attempts", 0) or 0)
        if attempts >= MAX_REPAIR_ATTEMPTS:
            skipped += 1
            emit(f"SKIP exhausted: {key}")
            continue

        patched_entry = apply_deterministic_patches(model_entry)
        market = patched_entry.get("market") or "IL"
        make = patched_entry.get("make", "")
        model = patched_entry.get("model", "")
        deterministic_changed = _stable(model_entry) != _stable(patched_entry)
        full_rebuild = _needs_full_rebuild(patched_entry)
        targets: Dict[int, List[str]] = {} if full_rebuild else derive_repair_targets(patched_entry)
        if full_rebuild:
            emit(f"REBUILDING WITH {provider_settings.display_name}: {key} | full rebuild from request_payload")
        elif targets:
            emit(f"REPAIRING WITH {provider_settings.display_name}: {key} | targets={targets}")
        elif deterministic_changed:
            emit(f"DETERMINISTIC PATCH ONLY: {key} | no model call")
        else:
            emit(f"NO-OP REPAIR BLOCKED: {key} | full rebuild required")
        processed += 1

        delta_ready: List[Dict[str, Any]] = []
        delta_review: List[Dict[str, Any]] = []
        completed = False

        try:
            if full_rebuild:
                request_payload = patched_entry.get("request_payload") if isinstance(patched_entry.get("request_payload"), dict) else {}
                if not all(request_payload.get(f) for f in ("market", "make", "model")):
                    raise ValueError("full rebuild requires request_payload with market, make, and model")
                rebuilt = client.build_profile(request_payload)
                if not isinstance(rebuilt, dict):
                    raise ValueError("catalog client returned non-object JSON")
                patched = _enforce_rebuilt_identity(rebuilt, request_payload)
                market, make, model = patched["market"], patched["make"], patched["model"]
            elif targets:
                repaired = client.build_repair_profile(make, model, patched_entry, targets)
                patched = merge_repair(patched_entry, repaired, targets)
            else:
                patched = dict(patched_entry)
            result = validate_profile(patched)
            if (not result.ready) and (not full_rebuild) and (not targets) and (not deterministic_changed):
                kept_entry = dict(result.profile)
                kept_entry["validation_issues"] = result.issues
                kept_entry["rebuild_required"] = True
                kept_entry["last_repair_error"] = "No deterministic or targeted repair possible; full rebuild required."
                delta_review = [kept_entry]
                kept += 1
                completed = True
                raise StopIteration
            if result.ready:
                clean_profile = dict(result.profile)
                for review_key in _REVIEW_ONLY_KEYS:
                    clean_profile.pop(review_key, None)
                delta_ready = [clean_profile]
                promoted += 1
                emit(f"PROMOTE {key}")
            else:
                kept_entry = dict(result.profile)
                kept_entry["validation_issues"] = result.issues
                kept_entry["repair_attempts"] = attempts + 1
                if kept_entry["repair_attempts"] >= MAX_REPAIR_ATTEMPTS:
                    kept_entry["repair_exhausted"] = True
                delta_review = [kept_entry]
                kept += 1
                emit(f"KEEP {key}: {len(result.issues)} issue(s)")
            completed = True
        except StopIteration:
            pass
        except ProviderUnavailableError:
            raise
        except Exception as exc:  # noqa: BLE001
            failed = dict(model_entry)
            failed["last_repair_error"] = sanitize_error(exc)
            if is_provider_setup_error(exc):
                # Provider/setup/dependency/import failure: do not consume a
                # repair attempt and do not mark the model as exhausted.
                processed -= 1
                delta_review = [failed]
                kept += 1
                emit(f"KEEP {key}: provider/setup error (no attempt consumed): {sanitize_error(exc)}")
            else:
                failed["repair_attempts"] = attempts + 1
                if failed["repair_attempts"] >= MAX_REPAIR_ATTEMPTS:
                    failed["repair_exhausted"] = True
                delta_review = [failed]
                kept += 1
                emit(f"KEEP {key}: repair failed: {sanitize_error(exc)}")
            completed = True

        if completed:
            profile_id = f"{market}::{make}::{model}"
            # Track the repair pointer separately; the main build resume pointer
            # must stay exactly where the last normal build left it.
            checkpointer.state["last_repair_checkpointed_profile_id"] = profile_id
            checkpointer.state["last_checkpointed_profile_id"] = build_resume_pointer
            merge_and_write_outputs(
                delta_ready,
                delta_review,
                settings=settings,
                checkpoint_state=checkpointer.state,
                catalog_path=catalog_path,
                readiness_path=readiness_path,
                review_path=review_path,
            )
            emit(f"local repair checkpoint written for {profile_id}")
            checkpointer.maybe_checkpoint(
                profile_id=profile_id,
                paths=[catalog_path, readiness_path, review_path],
                market=market,
                make=make,
                model=model,
                force=True,
            )
            # maybe_checkpoint may have set last_checkpointed_profile_id to the
            # repaired profile id on a successful github push; restore the build
            # pointer so repair never moves it.
            checkpointer.state["last_checkpointed_profile_id"] = build_resume_pointer

    # Final harmless refresh — correctness does not depend on this call.
    merged_catalog, merged_readiness, merged_review = merge_and_write_outputs(
        [],
        [],
        settings=settings,
        checkpoint_state=checkpointer.state,
        catalog_path=catalog_path,
        readiness_path=readiness_path,
        review_path=review_path,
    )
    return {
        "selected": selected_keys or [],
        "processed": processed,
        "promoted": promoted,
        "kept": kept,
        "skipped": skipped,
        "catalog": merged_catalog,
        "readiness": merged_readiness,
        "review": merged_review,
    }
