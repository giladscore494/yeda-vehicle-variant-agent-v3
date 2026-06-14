import json

from scripts.gemini_client import SYSTEM_PROMPT
from scripts.openai_guard_verifier import OpenAIGuardVerifier, OpenAIGuardVerifierSettings, GUARD_VERIFIER_SYSTEM_PROMPT
from scripts.output_writer import route_validated_rows
from scripts.reconcile import GuardFlag, reconcile_validation_output


def test_stage1_gemini_prompt_contains_required_general_rules():
    text = SYSTEM_PROMPT
    for snippet in [
        "You validate exactly one validation_id",
        "Israeli-market availability",
        "year_end = null does not automatically mean current=true",
        "fields_left_unresolved",
        "A split-required trim issue is not a blocking identity contradiction",
        "Classify source_type by source name/domain",
        "fields_changed must be a list of objects",
    ]:
        assert snippet in text


def test_guard_verifier_uses_openai_api_key_and_validator_model_id():
    settings = OpenAIGuardVerifierSettings(api_key="existing-openai-key", model_id="gpt-5.4", enabled=True)
    verifier = OpenAIGuardVerifier(settings, client=object())
    assert verifier.settings.api_key == "existing-openai-key"
    assert verifier.settings.model_id == "gpt-5.4"


def test_no_new_verifier_secret_names_in_code():
    import pathlib
    code = "\n".join(p.read_text() for p in pathlib.Path("scripts").glob("*.py"))
    assert "gemini_flash_api_key" not in code
    assert "guard_verifier_api_key" not in code


def make_flag(needs=True, name="market_year_conflict"):
    return GuardFlag(
        guard_name=name,
        severity="high" if needs else "low",
        field_affected="year_start" if needs else "canonical_trim",
        original_value=2026,
        guard_value=None,
        reason="Ambiguous market-year conflict." if needs else "Generic trim cleanup.",
        needs_adjudication=needs,
        recommended_verifier_model="gpt-5.4" if needs else "none",
        allowed_decisions=["clean_partial"],
        allowed_patch_fields=["year_start", "validation_decision"] if needs else ["canonical_trim"],
    )


def test_gpt_not_used_for_stage1_and_only_adjudication_flags_are_scoped():
    verifier = OpenAIGuardVerifier(OpenAIGuardVerifierSettings(api_key="k", model_id="gpt-5.4", enabled=True), client=object())
    assert "main validator" in GUARD_VERIFIER_SYSTEM_PROMPT
    assert verifier.adjudication_flags([make_flag(False, "generic_trim")]) == []
    assert verifier.adjudication_flags([make_flag(True)]) == [make_flag(True)]


def test_no_adjudication_flags_means_zero_calls():
    class BadClient:
        pass
    verifier = OpenAIGuardVerifier(OpenAIGuardVerifierSettings(api_key="k", model_id="gpt-5.4", enabled=True), client=BadClient())
    row = {"validation_id": "VAL-1", "adjudication_log": []}
    out = verifier.adjudicate(row, [make_flag(False, "generic_trim")])
    assert verifier.calls == 0
    assert out["adjudication_log"] == []


def test_payload_is_compact_guard_scoped_not_full_row():
    verifier = OpenAIGuardVerifier(OpenAIGuardVerifierSettings(api_key="k", model_id="gpt-5.4", enabled=True), client=object())
    row = {
        "validation_id": "VAL-1",
        "canonical_make": "M",
        "canonical_model": "N",
        "year_start": None,
        "huge_raw_source_field": "must not leak",
        "evidence_sources": [{"source_name": "editorial.example", "source_type": "editorial", "supports": ["official_import_il"], "url": "https://example.test/full"}],
        "grounding_summary": "short",
    }
    payload = verifier.build_payload(row, [make_flag(True)])
    dumped = json.dumps(payload)
    assert "huge_raw_source_field" not in dumped
    assert "full validation task" not in dumped.lower()
    assert payload["guards"][0]["guard_name"] == "market_year_conflict"
    assert set(payload["relevant_fields"]) <= {"canonical_make", "canonical_model", "canonical_trim", "year_start"}
    assert "url" not in payload["evidence_source_summaries"][0]


def test_verifier_cannot_patch_forbidden_fields_or_invalid_json_falls_back():
    payload = {"allowed_decisions": ["clean_partial"], "allowed_patch_fields": ["year_start"]}
    data = {
        "verdict": "modify_guard",
        "selected_decision": "clean_partial",
        "allowed_patch": {"year_start": 2020, "final_route": "clean_catalog"},
        "confidence": 0.8,
        "reason": "Safe correction.",
        "safety_notes": [],
    }
    clean = OpenAIGuardVerifier.validate_response(data, payload)
    assert clean["allowed_patch"] == {"year_start": 2020}

    class InvalidVerifier(OpenAIGuardVerifier):
        def _generate(self, payload):
            return {"bad": "json"}

    verifier = InvalidVerifier(OpenAIGuardVerifierSettings(api_key="k", model_id="gpt-5.4", enabled=True), client=object())
    row = {"validation_id": "VAL-1", "year_start": None, "adjudication_log": []}
    out = verifier.adjudicate(row, [make_flag(True)])
    assert out["year_start"] is None
    assert "stands" in out["adjudication_log"][0]["reason"]


def test_final_python_routing_overrides_verifier_and_is_python_only():
    rows = route_validated_rows([
        {"validation_id": "S", "canonical_model": "A", "validation_decision": "split_required", "fields_left_unresolved": [], "blocking_identity_issues": [], "identity_status": "verified"},
        {"validation_id": "R", "canonical_model": "B", "validation_decision": "reject", "fields_left_unresolved": [], "blocking_identity_issues": [], "identity_status": "invalid"},
        {"validation_id": "P", "canonical_model": "C", "validation_decision": "clean_partial", "fields_left_unresolved": ["canonical_trim"], "blocking_identity_issues": [], "identity_status": "likely_valid"},
        {"validation_id": "T", "canonical_model": "D", "validation_decision": "clean_partial", "fields_left_unresolved": ["transmission"], "blocking_identity_issues": [], "identity_status": "likely_valid"},
    ])
    by_id = {r["validation_id"]: r for r in rows}
    assert by_id["S"]["final_route"] == "split_queue" and by_id["S"]["publishable_to_clean_catalog"] is False
    assert by_id["R"]["final_route"] == "rejected" and by_id["R"]["publishable_to_clean_catalog"] is False
    # clean_partial with an unresolved trim must NEVER enter the clean catalog;
    # it is retained for partial review (strict v4 routing).
    assert by_id["P"]["final_route"] == "partial_queue" and by_id["P"]["publishable_to_clean_catalog"] is False
    # clean_partial with an unresolved critical field is held for review.
    assert by_id["T"]["final_route"] == "review_queue" and by_id["T"]["publishable_to_clean_catalog"] is False


def test_unresolved_language_fields_changed_and_source_type_rules():
    row = {
        "validation_id": "VAL-1",
        "canonical_make": "M",
        "canonical_model": "N",
        "canonical_trim": "Trim",
        "validation_decision": "clean_exact",
        "identity_status": "verified",
        "trim_status": "verified",
        "identity_confidence": 0.9,
        "trim_confidence": 0.9,
        "fields_changed": ["year_start"],
        "fields_left_unresolved": [],
        "decision_reason": "Transmission is uncertain and cannot be determined.",
        "grounding_summary": "",
        "evidence_sources": [{"title": "Importer announces", "source_name": "editorial.example", "source_type": "unknown", "supports": ["official_import_il"]}],
    }
    out = reconcile_validation_output({}, row, run_mode="real")
    assert "transmission" in out["fields_left_unresolved"]
    assert all(isinstance(item, dict) for item in out["fields_changed"])
    assert out["evidence_sources"][0]["source_type"] != "official_importer"
    assert "official_import_il" in out["evidence_sources"][0]["supports"]


def test_openai_responses_parse_preferred_and_create_never_gets_response_format():
    class Parsed:
        def model_dump(self):
            return {"verdict":"accept_guard","selected_decision":None,"allowed_patch":{},"confidence":0.7,"reason":"Guard stands.","safety_notes":[]}
    class Resp:
        output_parsed = Parsed()
    class Responses:
        def __init__(self):
            self.parse_calls = 0
            self.create_calls = []
        def parse(self, **kwargs):
            self.parse_calls += 1
            assert kwargs["text_format"].__name__ == "VerifierOutputModel"
            assert kwargs["max_output_tokens"] == 700
            return Resp()
        def create(self, **kwargs):
            self.create_calls.append(kwargs)
            assert "response_format" not in kwargs
            raise AssertionError("create should not be used when parse works")
    class Client:
        def __init__(self):
            self.responses = Responses()
    client = Client()
    verifier = OpenAIGuardVerifier(OpenAIGuardVerifierSettings(api_key="k", model_id="gpt-5.4", enabled=True), client=client)
    out = verifier.adjudicate({"validation_id":"V", "adjudication_log":[]}, [make_flag(True)])
    assert out["_guard_verifier_success"] is True
    assert client.responses.parse_calls == 1
    assert client.responses.create_calls == []


def test_openai_create_structured_then_json_fallback_without_response_format_retry():
    class Resp:
        def __init__(self, text):
            self.output_text = text
    class Responses:
        parse = None
        def __init__(self):
            self.create_calls = []
        def create(self, **kwargs):
            self.create_calls.append(kwargs)
            assert "response_format" not in kwargs
            if "text" in kwargs:
                raise TypeError("text format unsupported")
            return Resp(json.dumps({"verdict":"accept_guard","selected_decision":None,"allowed_patch":{},"confidence":0.6,"reason":"JSON fallback works.","safety_notes":[]}))
    class Client:
        def __init__(self):
            self.responses = Responses()
    client = Client()
    verifier = OpenAIGuardVerifier(OpenAIGuardVerifierSettings(api_key="k", model_id="gpt-5.4", enabled=True), client=client)
    out = verifier.adjudicate({"validation_id":"V", "adjudication_log":[]}, [make_flag(True)])
    assert out["_guard_verifier_success"] is True
    assert len(client.responses.create_calls) == 2
    assert "text" in client.responses.create_calls[0]
    assert "text" not in client.responses.create_calls[1]
    assert all("response_format" not in c for c in client.responses.create_calls)
