from engine.validation.change_decision_classifier import classify_change_decision


def test_no_action_result_is_no_change_required():
    result = classify_change_decision({"final_recommendation": "no_action"})
    assert result["change_decision"] == "NO_CHANGE_REQUIRED"
    assert result["patchable"] is False
    assert result["patchability_reason"] == "no_change_needed"


def test_vague_recommendation_is_no_change_required():
    result = classify_change_decision({"final_recommendation": "manual_review"})
    assert result["change_decision"] == "NO_CHANGE_REQUIRED"
    assert result["patchable"] is False
    assert result["patchability_reason"] == "vague_recommendation"


def test_cosmetic_difference_is_no_change_required():
    result = classify_change_decision({"final_recommendation": "needs_normalization", "change_reason": "cosmetic typo only"})
    assert result["change_decision"] == "NO_CHANGE_REQUIRED"
    assert result["change_severity"] == "negligible"


def test_critical_field_mismatch_is_change_required():
    result = classify_change_decision(
        {
            "final_recommendation": "manual_review",
            "risk_level": "critical",
            "field_changes": {"v1": {"fuel_type": {"from": "diesel", "to": "hybrid"}}},
            "variant_ids": ["v1"],
        }
    )
    assert result["change_decision"] == "CHANGE_REQUIRED"
    assert result["change_severity"] == "critical"


def test_exact_changes_on_critical_field_are_patchable():
    result = classify_change_decision(
        {
            "final_recommendation": "needs_normalization",
            "risk_level": "high",
            "field_changes": {"v1": {"year_start": {"from": 2020, "to": 2021}}},
            "variant_ids": ["v1"],
        }
    )
    assert result["change_decision"] == "CHANGE_REQUIRED"
    assert result["patchable"] is True
    assert result["patchability_reason"] == "exact_field_changes_available"


def test_reject_merge_year_scope_actions_are_change_required_not_patchable():
    for action in ("reject", "merge", "change_year_range", "change_market_scope", "promote_to_verified"):
        result = classify_change_decision(
            {
                "final_recommendation": action,
                "risk_level": "high",
                "issue_type": "identity_mismatch",
            }
        )
        assert result["change_decision"] == "CHANGE_REQUIRED"
        assert result["patchable"] is False
        assert result["patchability_reason"] == "unsafe_action"


def test_weak_evidence_is_no_change_required():
    result = classify_change_decision(
        {
            "final_recommendation": "update_fields",
            "confidence": 0.2,
            "change_reason": "insufficient evidence for update",
            "field_changes": {"v1": {"model": {"from": "A", "to": "B"}}},
            "variant_ids": ["v1"],
        }
    )
    assert result["change_decision"] == "NO_CHANGE_REQUIRED"
    assert result["patchable"] is False
