"""Atomic save layer — write, reload, audit, optional push."""
from __future__ import annotations

import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from engine.audit import audit_canonical
from engine.state import load_canonical


def _refresh_counts(canonical: dict) -> None:
    """Recompute counts from actual data."""
    verified = canonical.get("verified_variants") or []
    partial = canonical.get("partial_variants") or []
    all_variants = verified + partial
    bs = canonical.get("batch_state") or {}

    makes: set[str] = set()
    models: set[tuple[str, str]] = set()
    verified_count = 0
    for v in all_variants:
        if not isinstance(v, dict):
            continue
        if v.get("verification_status") == "verified":
            verified_count += 1
        mk = (v.get("make") or "").strip()
        mo = (v.get("model") or "").strip()
        if mk:
            makes.add(mk)
        if mk or mo:
            models.add((mk, mo))

    canonical["counts"] = {
        "total_variants": len(all_variants),
        "variants": len(all_variants),
        "verified": verified_count,
        "partial": len(all_variants) - verified_count,
        "makes_count": len(makes),
        "models_count": len(models),
        "processed_seeds": len(bs.get("processed_seed_ids") or []),
        "needs_retry_seeds": len(bs.get("needs_retry_seed_ids") or []),
        "total_seeds": bs.get("total_seeds"),
        "unresolved": len(bs.get("failed_seed_ids") or []),
        "last_updated_at": datetime.now(timezone.utc).isoformat(),
    }


def save_canonical_atomic(
    canonical: dict,
    path: str | Path,
    seed_catalog: list[dict] | None = None,
    push_to_github: bool = False,
) -> dict:
    """Atomic save: audit -> write tmp -> reload tmp -> replace -> reload -> audit -> push.

    Returns dict with keys: ok, path, error, push_result.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    # Refresh counts before audit
    _refresh_counts(canonical)

    # Pre-save audit
    ok, errs = audit_canonical(canonical, seed_catalog=seed_catalog)
    if not ok:
        return {"ok": False, "path": str(p), "error": f"pre-save audit failed: {errs}"}

    # Backup
    if p.exists():
        backup_p = p.with_name(p.stem + "_backup_previous.json")
        shutil.copy2(p, backup_p)

    # Write to temp file
    fd, tmp_path = tempfile.mkstemp(
        prefix=".canonical_", suffix=".json", dir=str(p.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(canonical, fh, ensure_ascii=False, indent=2)

        # Reload and validate temp file
        try:
            tmp_data = json.loads(Path(tmp_path).read_text(encoding="utf-8"))
        except Exception as exc:
            return {"ok": False, "path": str(p), "error": f"temp file unreadable: {exc}"}

        ok2, errs2 = audit_canonical(tmp_data, seed_catalog=seed_catalog)
        if not ok2:
            return {"ok": False, "path": str(p), "error": f"temp file audit failed: {errs2}"}

        # Atomic replace
        os.replace(tmp_path, str(p))
    finally:
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    # Reload after replace
    try:
        reloaded = load_canonical(p)
    except Exception as exc:
        return {"ok": False, "path": str(p), "error": f"post-save reload failed: {exc}"}

    # Post-save audit
    ok3, errs3 = audit_canonical(reloaded, seed_catalog=seed_catalog)
    if not ok3:
        return {"ok": False, "path": str(p), "error": f"post-save audit failed: {errs3}"}

    result: dict = {"ok": True, "path": str(p), "error": None, "push_result": None}

    # Optional GitHub push
    if push_to_github:
        try:
            from storage.github_canonical_store import push_canonical
            push_result = push_canonical(canonical)
            result["push_result"] = push_result
            if not push_result.get("ok"):
                result["push_warning"] = push_result.get("error", "push failed")
        except Exception as exc:
            result["push_warning"] = f"push error: {exc}"

    return result
