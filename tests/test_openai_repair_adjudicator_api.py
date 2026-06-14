import json
from types import SimpleNamespace

from scripts.openai_repair_adjudicator import OpenAIRepairAdjudicator, OpenAIRepairAdjudicatorSettings


class _Responses:
    def __init__(self):
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(output_text=json.dumps({
            "repair_decision": "patched",
            "patched_variant": {"validation_id": "VAL-1", "grounding_status": {}},
            "field_patches": [{"field": "canonical_trim", "to": None}],
            "summary_patch": {},
            "routing_patch": {},
            "grounding_patch": {"gpt54_grounding_present": True},
            "remaining_uncertainties": [],
            "blocking_issues_after_repair": [],
            "non_blocking_issues_after_repair": [],
            "confidence": 0.8,
        }))


class _Client:
    def __init__(self):
        self.responses = _Responses()


def test_openai_repair_adjudicator_uses_responses_api_token_param():
    client = _Client()
    adjudicator = OpenAIRepairAdjudicator(OpenAIRepairAdjudicatorSettings(
        api_key="test-key", grounding_required=False, use_web_search=False, max_completion_tokens=1234,
    ))
    adjudicator._client = client

    adjudicator.adjudicate({"guarded_output": {"validation_id": "VAL-1"}})

    assert client.responses.kwargs["max_output_tokens"] == 1234
    assert "max_completion_tokens" not in client.responses.kwargs
