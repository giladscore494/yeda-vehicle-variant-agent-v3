"""Fast smoke checks. Run with: python scripts/smoke_test.py

Covers loading, join integrity, schema, clustering determinism, the core
decision rules (weak/missing/Base trim -> clean_partial, contradiction ->
reject), checkpoint resume, atomic write, and the anti-regression guarantees
(no OpenAI, no GPT adjudicator, exact Streamlit secret paths).
"""

from __future__ import annotations

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import clustering, data_loader, normalization  # noqa: E402
from scripts.output_writer import (  # noqa: E402
    OutputStore,
    atomic_write_json,
    build_output_row,
    validate_output_row,
)
from scripts.validator_engine import decide_mock  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_results = []


def check(name: str, cond: bool, detail: str = "") -> None:
    _results.append((name, bool(cond), detail))
    mark = "PASS" if cond else "FAIL"
    print(f"[{mark}] {name}" + (f" — {detail}" if detail and not cond else ""))


def _identity(**kw):
    base = {
        "make": "Toyota", "model": "Corolla", "engine": "1.8L",
        "transmission": "automatic", "fuel_type": "petrol", "drivetrain": "FWD",
        "body_type": "Sedan", "year_start": 2015, "year_end": 2019,
        "generation": "E170", "market_scope": "IL",
    }
    base.update(kw)
    return base


def _trim(value, weak):
    return {"trim": value, "official_marketed_name_il": None,
            "local_brand_name_il": None, "alternate_names": [], "trim_is_weak": weak}


def main() -> int:
    # 1-2. source files exist & parse
    present = data_loader.files_present()
    check("source files exist", all(present.values()), str(present))
    join = data_loader.validate_and_join()
    check("JSON parses & join ok", join.ok, "; ".join(join.errors[:3]))

    # 3-6. structure / join / duplicates
    check("variants structure valid", join.variant_count > 0)
    check("instructions structure valid", join.instruction_count > 0)
    check("join count matches", join.variant_count == len(join.ordered_ids))
    check("no duplicate validation_id", len(set(join.ordered_ids)) == len(join.ordered_ids))

    # 7. output schema valid
    row = build_output_row("VAL-TEST", validation_decision="clean_partial")
    check("output schema valid", not validate_output_row(row), str(validate_output_row(row)))
    check("clean_partial -> partial tier", row["acceptance_tier"] == "partial")

    # 8. cluster key deterministic
    ident = _identity()
    k1, k2 = clustering.cluster_key(ident), clustering.cluster_key(dict(ident))
    check("cluster key deterministic", k1 == k2 and "toyota|corolla" in k1)

    # 9-11. weak/missing/Base trim with valid identity -> clean_partial
    check("missing trim -> clean_partial",
          decide_mock(_identity(), _trim(None, True))["validation_decision"] == "clean_partial")
    check("generic trim -> clean_partial",
          decide_mock(_identity(), _trim("generic", True))["validation_decision"] == "clean_partial")
    check("Base trim -> clean_partial",
          decide_mock(_identity(), _trim("Base", True))["validation_decision"] == "clean_partial")
    check("Standard trim -> clean_partial",
          decide_mock(_identity(), _trim("Standard", True))["validation_decision"] == "clean_partial")

    # 12. identity contradiction -> reject
    contradiction = decide_mock(_identity(year_start=2020, year_end=2010), _trim("XLE", False))
    check("impossible year range -> reject", contradiction["validation_decision"] == "reject")
    missing_make = decide_mock(_identity(make=None), _trim("XLE", False))
    check("missing make -> reject", missing_make["validation_decision"] == "reject")

    # 13. split_required can include split_candidates
    split = decide_mock(_identity(), _trim("Sport / Luxury", False))
    check("split_required includes split_candidates",
          split["validation_decision"] == "split_required" and len(split["split_candidates"]) >= 2)

    # 14-15. checkpoint resume + atomic write
    with tempfile.TemporaryDirectory() as tmp:
        out_p = os.path.join(tmp, "out.json")
        cp_p = os.path.join(tmp, "out.checkpoint.json")
        s1 = OutputStore(out_p, cp_p)
        s1.record(build_output_row("VAL-000001", validation_decision="clean_exact"))
        s1.flush()
        s2 = OutputStore(out_p, cp_p)
        s2.load_existing()
        check("checkpoint can resume", s2.is_completed("VAL-000001"))
        atomic_write_json(out_p, {"k": "v"})
        check("atomic write not corrupt", json.load(open(out_p))["k"] == "v")

    # 16-17. no OpenAI / no GPT adjudicator anywhere in source
    offenders = []
    for base, _dirs, files in os.walk(os.path.join(REPO_ROOT, "scripts")):
        for f in files:
            if f.endswith(".py") and f != "smoke_test.py":  # skip this scanner itself
                text = open(os.path.join(base, f), encoding="utf-8").read().lower()
                if "import openai" in text or "from openai" in text:
                    offenders.append(f"{f}:openai")
                if "gpt_adjudicator" in text or "gpt-4" in text:
                    offenders.append(f"{f}:gpt")
    check("no OpenAI dependency", not offenders, str(offenders))
    reqs = open(os.path.join(REPO_ROOT, "requirements.txt")).read().lower()
    check("no openai in requirements", "openai" not in reqs)

    # 18. Streamlit secret paths present in app.py with exact form
    app_text = open(os.path.join(REPO_ROOT, "app.py"), encoding="utf-8").read()
    for path in (
        'st.secrets["github"]["token"]',
        'st.secrets["google"]["api_key"]',
        'st.secrets["google"]["gemini_validator_model_id"]',
        'st.secrets["google"]["grounding_enabled"]',
    ):
        check(f"secret path used: {path}", path in app_text)

    # 19. github checkpoint module never prints the token
    gh_text = open(os.path.join(REPO_ROOT, "scripts", "github_checkpoint.py")).read()
    check("github module does not print token",
          "print(" not in gh_text or "token" not in gh_text.split("print(")[-1][:80])

    # 20. every built row preserves validation_id
    check("row preserves validation_id",
          build_output_row("VAL-999999")["validation_id"] == "VAL-999999")

    failed = [n for n, ok, _ in _results if not ok]
    print("\n" + "=" * 60)
    print(f"SMOKE RESULT: {len(_results) - len(failed)}/{len(_results)} passed")
    if failed:
        print("FAILED: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
