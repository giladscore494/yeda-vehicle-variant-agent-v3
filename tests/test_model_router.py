from engine.validation.model_router import route_issue_item


def _item(**overrides):
    item = {
        "item_id": "iq_test",
        "seed_id": "toyota__corolla__2019__2024__il",
        "issue_type": "trim_completeness",
        "risk_level": "medium",
        "requires_model_review": True,
    }
    item.update(overrides)
    return item


def test_low_risk_item_does_not_call_model():
    decision = route_issue_item(_item(risk_level="low"))

    assert decision.should_call_models is False
    assert decision.decision_policy == "deterministic_only"
    assert decision.max_expected_calls == 0


def test_requires_model_review_false_does_not_call_model():
    decision = route_issue_item(_item(requires_model_review=False, risk_level="critical"))

    assert decision.should_call_models is False
    assert decision.decision_policy == "deterministic_only"
    assert decision.primary_provider is None


def test_medium_trim_issue_routes_to_gemini_only_without_web():
    decision = route_issue_item(_item(issue_type="trim_completeness", risk_level="medium"))

    assert decision.should_call_models is True
    assert decision.primary_provider == "gemini"
    assert decision.primary_web_required is False
    assert decision.second_opinion_provider is None
    assert decision.decision_policy == "gemini_light_review"
    assert decision.max_expected_calls == 1


def test_evidence_gap_routes_to_gemini_with_web():
    decision = route_issue_item(_item(issue_type="evidence_gap", risk_level="medium"))

    assert decision.should_call_models is True
    assert decision.primary_provider == "gemini"
    assert decision.primary_web_required is True
    assert decision.second_opinion_provider is None
    assert decision.decision_policy == "gemini_grounded_market_check"


def test_high_risk_routes_to_gemini_and_openai():
    decision = route_issue_item(_item(issue_type="evidence_gap", risk_level="high"))

    assert decision.should_call_models is True
    assert decision.primary_provider == "gemini"
    assert decision.primary_web_required is True
    assert decision.second_opinion_provider == "openai"
    assert decision.second_opinion_web_required is False
    assert decision.decision_policy == "high_risk_dual_model"
    assert decision.max_expected_calls == 2


def test_critical_routes_to_gemini_web_and_openai_web():
    decision = route_issue_item(_item(issue_type="source_conflict", risk_level="critical"))

    assert decision.should_call_models is True
    assert decision.primary_provider == "gemini"
    assert decision.primary_web_required is True
    assert decision.second_opinion_provider == "openai"
    assert decision.second_opinion_web_required is True
    assert decision.decision_policy == "critical_dual_model"
    assert decision.max_expected_calls == 2
