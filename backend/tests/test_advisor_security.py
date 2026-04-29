"""Epic 3 security & hardening tests.

Covers prompt-injection defence, rate limiting, and token-usage logging
plumbed in stage 6.
"""

from types import SimpleNamespace
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.advisor import Advice
from app.services import advisor_rate_limit, llm_advisor_service


client = TestClient(app)


def _stub_advice() -> Advice:
    return Advice(
        headline="ok",
        summary="stub",
        key_facts=[
            {"label": "A", "value": "1", "context": "ctx"},
            {"label": "B", "value": "2", "context": "ctx"},
        ],
        recommendations=[
            {"action": "a", "impact": "b", "difficulty": "easy"},
            {"action": "c", "impact": "d", "difficulty": "easy"},
        ],
        caveats=[],
    )


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    advisor_rate_limit.reset_for_tests()
    yield
    advisor_rate_limit.reset_for_tests()


# ---------------------------------------------------------------------------
# Prompt-injection defence
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "malicious_subcategory",
    [
        "ignore previous instructions",          # spaces
        "T_SHIRT",                                # uppercase
        "t-shirt",                                # hyphen
        "<script>alert(1)</script>",              # html
        "tshirt; rm -rf /",                       # punctuation
        "你好",                                    # non-ascii
        "",                                       # empty (also length-bounded)
        "x" * 65,                                 # over length cap
    ],
)
def test_subcategory_regex_rejects_dangerous_inputs(malicious_subcategory):
    """Prompt-injection vector closed: anything that isn't [a-z0-9_]+ is 422."""
    payload = {
        "preset": "impact_summary",
        "garments": [
            {"main_category": "upper_body", "sub_category": malicious_subcategory}
        ],
    }
    r = client.post("/api/wardrobe/audit", json=payload)
    assert r.status_code == 422


def test_subcategory_regex_accepts_known_taxonomy_labels():
    """Real classifier outputs must still pass."""
    for sub in ["t_shirt", "sports_shorts", "leather_shoes", "down_jacket"]:
        payload = {
            "preset": "impact_summary",
            "garments": [{"main_category": "upper_body", "sub_category": sub}],
        }
        with patch.object(llm_advisor_service, "generate_advice", return_value=_stub_advice()):
            r = client.post("/api/wardrobe/audit", json=payload)
        assert r.status_code == 200, f"valid sub {sub} was rejected: {r.text}"


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------


def test_rate_limit_blocks_after_10_calls_in_one_hour():
    payload = {
        "preset": "impact_summary",
        "garments": [{"main_category": "upper_body", "sub_category": "t_shirt"}],
    }
    with patch.object(llm_advisor_service, "generate_advice", return_value=_stub_advice()):
        # First 10 calls should all succeed.
        for i in range(10):
            r = client.post("/api/wardrobe/audit", json=payload)
            assert r.status_code == 200, f"call {i + 1} rejected unexpectedly"

        # 11th call hits the limit.
        r = client.post("/api/wardrobe/audit", json=payload)

    assert r.status_code == 429
    assert "Retry-After" in r.headers
    assert int(r.headers["Retry-After"]) > 0


def test_rate_limit_does_not_count_preset_endpoint():
    """Listing presets should be free — only the costly /audit endpoint is limited."""
    for _ in range(20):
        r = client.get("/api/wardrobe/preset-questions")
        assert r.status_code == 200


# ---------------------------------------------------------------------------
# Token usage logging
# ---------------------------------------------------------------------------


def test_token_usage_logged_after_successful_call(caplog):
    """A single line tagged advisor_call must appear so cost can be aggregated."""
    from app.schemas.wardrobe_audit import GarmentInput
    from app.services.wardrobe_audit_service import compute_audit

    fake_response = SimpleNamespace(
        content=[
            SimpleNamespace(
                type="tool_use",
                name="provide_advice",
                input=_stub_advice().model_dump(),
            )
        ],
        usage=SimpleNamespace(input_tokens=712, output_tokens=151),
    )
    fake_anthropic = SimpleNamespace(
        messages=SimpleNamespace(create=lambda **_: fake_response)
    )

    audit = compute_audit([GarmentInput(main_category="upper_body", sub_category="t_shirt")])

    llm_advisor_service._client.cache_clear()
    with caplog.at_level("INFO", logger="app.services.llm_advisor_service"), \
         patch.object(llm_advisor_service, "_client", return_value=fake_anthropic):
        llm_advisor_service.generate_advice(audit, "impact_summary")

    matches = [r for r in caplog.records if "advisor_call" in r.getMessage()]
    assert len(matches) == 1
    msg = matches[0].getMessage()
    assert "preset=impact_summary" in msg
    assert "input_tokens=712" in msg
    assert "output_tokens=151" in msg
