"""Deterministic-first model routing for validation issue-queue items.

The router is intentionally pure: it decides whether an issue-queue item is
eligible for model review and, if so, which provider roles are planned. It does
not call models and it never mutates canonical data.
"""
from __future__ import annotations

import os
from dataclasses import asdict, dataclass

from engine import config

GEMINI_PROVIDER = "gemini"
OPENAI_PROVIDER = "openai"
ESCALATION_PROVIDER = "openai"

DEFAULT_GEMINI_MODEL = "gemini-3.1-pro-preview"
DEFAULT_OPENAI_MODEL = "gpt-5.4"
DEFAULT_ESCALATION_MODEL = "gpt-5.5"

_GROUNDED_MARKET_ISSUE_TYPES = {
    "evidence_gap",
    "market_plausibility_gap",
    "il_market_plausibility",
    "official_importer_check",
    "failed_seed",
    "manual_review_seed",
    "source_conflict",
    "market_scope_conflict",
    # Task 2 issue names that are equivalent to an evidence gap.
    "partial_variant_too_little_evidence",
    "stale_or_weak_source_evidence",
}

_LIGHT_REVIEW_ISSUE_TYPES = {
    "identity_completeness",
    "identity_gap",
    "identity_trim_completeness",
    "missing_identity_detail",
    "missing_trim",
    "trim_completeness",
    "trim_completeness_gap",
    "trim_identity_gap",
}

_DISAGREEMENT_PRONE_ISSUE_TYPES = {
    "source_conflict",
    "market_scope_conflict",
    "official_importer_check",
}


@dataclass
class ModelRoutingDecision:
    should_call_models: bool
    primary_provider: str | None
    primary_model: str | None
    primary_web_required: bool
    second_opinion_provider: str | None
    second_opinion_model: str | None
    second_opinion_web_required: bool
    escalation_provider: str | None
    escalation_model: str | None
    escalation_web_required: bool
    reason: str
    max_expected_calls: int
    decision_policy: str

    def to_dict(self) -> dict:
        """Return a JSON-serializable representation of the decision."""
        return asdict(self)


def _gemini_model() -> str:
    return config.get("google", "gemini_validator_model_id", DEFAULT_GEMINI_MODEL) or DEFAULT_GEMINI_MODEL


def _openai_model() -> str:
    return config.get("openai", "validator_model_id", DEFAULT_OPENAI_MODEL) or DEFAULT_OPENAI_MODEL


def _escalation_enabled() -> bool:
    return os.environ.get("MODEL_ROUTER_ENABLE_GPT55_ESCALATION", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }


def _escalation_model() -> str:
    return os.environ.get("MODEL_ROUTER_ESCALATION_MODEL", DEFAULT_ESCALATION_MODEL).strip() or DEFAULT_ESCALATION_MODEL


def _base_no_model(reason: str) -> ModelRoutingDecision:
    return ModelRoutingDecision(
        should_call_models=False,
        primary_provider=None,
        primary_model=None,
        primary_web_required=False,
        second_opinion_provider=None,
        second_opinion_model=None,
        second_opinion_web_required=False,
        escalation_provider=None,
        escalation_model=None,
        escalation_web_required=False,
        reason=reason,
        max_expected_calls=0,
        decision_policy="deterministic_only",
    )


def _with_optional_escalation(decision: ModelRoutingDecision, item: dict) -> ModelRoutingDecision:
    issue_type = str(item.get("issue_type") or "").strip()
    risk_level = str(item.get("risk_level") or "").strip().lower()
    if not _escalation_enabled():
        return decision
    if risk_level != "critical" and issue_type not in _DISAGREEMENT_PRONE_ISSUE_TYPES:
        return decision
    decision.escalation_provider = ESCALATION_PROVIDER
    decision.escalation_model = _escalation_model()
    decision.escalation_web_required = risk_level == "critical"
    return decision


def route_issue_item(item: dict) -> ModelRoutingDecision:
    """Route one deterministic issue-queue item to the minimum model review path.

    Models are allowed only when deterministic code already marked the item with
    ``requires_model_review = true``. Low-risk issues remain deterministic-only
    even if another code path accidentally marks them for model review.
    """
    if not item.get("requires_model_review", False):
        return _base_no_model("requires_model_review is false; deterministic result is sufficient")

    risk_level = str(item.get("risk_level") or "").strip().lower()
    issue_type = str(item.get("issue_type") or "").strip()

    if risk_level == "low":
        return _base_no_model("low-risk issue; deterministic review only")

    gemini_model = _gemini_model()
    openai_model = _openai_model()

    if risk_level == "critical":
        decision = ModelRoutingDecision(
            should_call_models=True,
            primary_provider=GEMINI_PROVIDER,
            primary_model=gemini_model,
            primary_web_required=True,
            second_opinion_provider=OPENAI_PROVIDER,
            second_opinion_model=openai_model,
            second_opinion_web_required=True,
            escalation_provider=None,
            escalation_model=None,
            escalation_web_required=False,
            reason="critical issue requires grounded primary validation and web-grounded second opinion",
            max_expected_calls=2,
            decision_policy="critical_dual_model",
        )
        return _with_optional_escalation(decision, item)

    if risk_level == "high":
        decision = ModelRoutingDecision(
            should_call_models=True,
            primary_provider=GEMINI_PROVIDER,
            primary_model=gemini_model,
            primary_web_required=True,
            second_opinion_provider=OPENAI_PROVIDER,
            second_opinion_model=openai_model,
            second_opinion_web_required=False,
            escalation_provider=None,
            escalation_model=None,
            escalation_web_required=False,
            reason="high-risk issue requires grounded Gemini validation and OpenAI safety review",
            max_expected_calls=2,
            decision_policy="high_risk_dual_model",
        )
        return _with_optional_escalation(decision, item)

    if issue_type in _GROUNDED_MARKET_ISSUE_TYPES:
        decision = ModelRoutingDecision(
            should_call_models=True,
            primary_provider=GEMINI_PROVIDER,
            primary_model=gemini_model,
            primary_web_required=True,
            second_opinion_provider=None,
            second_opinion_model=None,
            second_opinion_web_required=False,
            escalation_provider=None,
            escalation_model=None,
            escalation_web_required=False,
            reason="issue type requires external Israeli-market or source evidence",
            max_expected_calls=1,
            decision_policy="gemini_grounded_market_check",
        )
        return _with_optional_escalation(decision, item)

    if risk_level == "medium" and (issue_type in _LIGHT_REVIEW_ISSUE_TYPES or "trim" in issue_type):
        return ModelRoutingDecision(
            should_call_models=True,
            primary_provider=GEMINI_PROVIDER,
            primary_model=gemini_model,
            primary_web_required=False,
            second_opinion_provider=None,
            second_opinion_model=None,
            second_opinion_web_required=False,
            escalation_provider=None,
            escalation_model=None,
            escalation_web_required=False,
            reason="medium-risk identity/trim completeness issue can be checked without web grounding",
            max_expected_calls=1,
            decision_policy="gemini_light_review",
        )

    decision = ModelRoutingDecision(
        should_call_models=True,
        primary_provider=GEMINI_PROVIDER,
        primary_model=gemini_model,
        primary_web_required=False,
        second_opinion_provider=None,
        second_opinion_model=None,
        second_opinion_web_required=False,
        escalation_provider=None,
        escalation_model=None,
        escalation_web_required=False,
        reason="requires model review but does not match grounded or dual-model criteria",
        max_expected_calls=1,
        decision_policy="gemini_light_review",
    )
    return _with_optional_escalation(decision, item)
