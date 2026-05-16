"""Tests for the Epic 3 LLM advisor service.

Network calls to Claude are mocked. A separate, opt-in smoke test
(`test_real_api_smoke`) hits the live API only when RUN_LLM_SMOKE=1 is set.
"""

import os
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from app.schemas.advisor import Advice
from app.schemas.wardrobe_audit import GarmentInput
from app.services import llm_advisor_service
from app.services.llm_advisor_service import (
    AdvisorUpstreamError,
    generate_advice,
)
from app.services.wardrobe_audit_service import compute_audit


@pytest.fixture(autouse=True)
def _reset_client_cache():
    """Clear the lru_cache so each test gets a fresh Anthropic stub."""
    llm_advisor_service._client.cache_clear()
    yield
    llm_advisor_service._client.cache_clear()


def _wardrobe(items: dict[str, tuple[str, int]]) -> list[GarmentInput]:
    out: list[GarmentInput] = []
    for sub, (main, count) in items.items():
        out.extend(GarmentInput(main_category=main, sub_category=sub) for _ in range(count))
    return out


def _fake_tool_response(input_payload: dict) -> SimpleNamespace:
    """Mimic the shape of an Anthropic Messages response with one tool_use."""
    block = SimpleNamespace(type="tool_use", name="provide_advice", input=input_payload)
    return SimpleNamespace(content=[block])


def _valid_advice_payload() -> dict:
    return {
        "layout": "report",
        "headline": "Your wardrobe stores ~143 kg of CO2",
        "summary": (
            "Your 17 catalogued items embody about 143 kg of CO2 and 30,640 L "
            "of water. Extending each item's life is the highest-leverage "
            "lever available to you."
        ),
        "key_facts": [
            {
                "label": "Total embodied CO2",
                "value": "143 kg",
                "context": "Across all 17 items in your wardrobe.",
            },
            {
                "label": "Equivalent driving",
                "value": "815 km",
                "context": "Same CO2 as driving an average car this far.",
            },
        ],
        "recommendations": [
            {
                "id": "extend-lifetime-2x",
                "action": "Wear each garment twice as long before disposal",
                "impact": "Saves about 62.9 kg CO2",
                "difficulty": "medium",
                "follow_up_prompts": ["Which item should I start with?"],
            },
            {
                "id": "buy-secondhand",
                "action": "Buy second-hand instead of new for your next purchase",
                "impact": "Avoids around 80% of the embodied CO2 of a new item",
                "difficulty": "easy",
                "follow_up_prompts": [],
            },
        ],
        "caveats": [
            "Australia-specific data is not available; EU/UK datasets used as proxies.",
        ],
        "next_questions": [
            "Which single item is the biggest contributor?",
            "How much would buying one less dress per year save?",
        ],
    }


def test_empty_wardrobe_short_circuits_without_calling_claude():
    """Critical for cost control — empty wardrobes must not hit the API."""
    with patch.object(llm_advisor_service, "_client") as mock_client:
        audit = compute_audit([])

        advice = generate_advice(audit, "impact_summary")

        assert isinstance(advice, Advice)
        assert advice.headline == "Your wardrobe is empty"
        mock_client.assert_not_called()


def test_generate_advice_returns_validated_advice_object():
    audit = compute_audit(_wardrobe({
        "t_shirt": ("upper_body", 10),
        "jeans": ("lower_body", 3),
    }))

    fake_anthropic = SimpleNamespace(
        messages=SimpleNamespace(
            create=lambda **_: _fake_tool_response(_valid_advice_payload())
        )
    )
    with patch.object(llm_advisor_service, "_client", return_value=fake_anthropic):
        advice = generate_advice(audit, "reduce_my_footprint")

    assert isinstance(advice, Advice)
    assert advice.headline.startswith("Your wardrobe")
    assert len(advice.recommendations) >= 2


def test_generate_advice_includes_audit_facts_in_user_prompt():
    """Sanity check: the audit JSON must reach the model verbatim, otherwise
    the LLM has nothing to ground its numbers in."""
    audit = compute_audit(_wardrobe({"t_shirt": ("upper_body", 5)}))
    captured: dict = {}

    def fake_create(**kwargs):
        captured.update(kwargs)
        return _fake_tool_response(_valid_advice_payload())

    fake_anthropic = SimpleNamespace(
        messages=SimpleNamespace(create=fake_create),
    )
    with patch.object(llm_advisor_service, "_client", return_value=fake_anthropic):
        generate_advice(audit, "impact_summary")

    user_message = captured["messages"][0]["content"]
    assert "<audit_facts>" in user_message
    assert '"co2_kg": 23.0' in user_message  # 5 t-shirts * 4.6 kg
    assert captured["tool_choice"] == {"type": "tool", "name": "provide_advice"}


def test_missing_tool_block_raises_upstream_error():
    audit = compute_audit(_wardrobe({"t_shirt": ("upper_body", 1)}))
    response_without_tool = SimpleNamespace(
        content=[SimpleNamespace(type="text", text="hello")]
    )
    fake_anthropic = SimpleNamespace(
        messages=SimpleNamespace(create=lambda **_: response_without_tool)
    )

    with patch.object(llm_advisor_service, "_client", return_value=fake_anthropic):
        with pytest.raises(AdvisorUpstreamError, match="no tool_use block"):
            generate_advice(audit, "impact_summary")


def test_invalid_tool_payload_raises_validation_error():
    audit = compute_audit(_wardrobe({"t_shirt": ("upper_body", 1)}))
    bad_payload = {"headline": "x"}  # missing required fields
    fake_anthropic = SimpleNamespace(
        messages=SimpleNamespace(
            create=lambda **_: _fake_tool_response(bad_payload)
        )
    )

    with patch.object(llm_advisor_service, "_client", return_value=fake_anthropic):
        with pytest.raises(AdvisorUpstreamError, match="schema validation"):
            generate_advice(audit, "impact_summary")


# ---------------------------------------------------------------------------
# Optional live-API smoke test
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    os.environ.get("RUN_LLM_SMOKE") != "1",
    reason="Live-API smoke disabled. Set RUN_LLM_SMOKE=1 to enable.",
)
def test_real_api_smoke():
    """Hits the real Claude API end-to-end. Costs ~$0.001 per run."""
    audit = compute_audit(_wardrobe({
        "t_shirt": ("upper_body", 10),
        "jeans": ("lower_body", 3),
        "sneakers": ("footwear", 2),
    }))
    advice = generate_advice(audit, "reduce_my_footprint")

    assert isinstance(advice, Advice)
    assert len(advice.recommendations) >= 2
    print("\n--- LIVE ADVICE PREVIEW ---")
    print("Headline:", advice.headline)
    print("Summary:", advice.summary)
    for r in advice.recommendations:
        print(f"- [{r.difficulty}] {r.action} -> {r.impact}")
