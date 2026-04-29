"""Epic 3 LLM advisor service.

Wraps the Anthropic Messages API for the wardrobe sustainability advisor.

Design rules:
- The LLM is *only* a translator: every number it cites must come from the
  `AuditFacts` supplied by `wardrobe_audit_service`. The system prompt below
  enforces this contractually; tool-use enforces it structurally.
- Empty wardrobes never reach Claude — we return a static advice object so we
  don't pay for a call that has no inputs.
- The HTTP layer is responsible for catching `AdvisorUpstreamError` and
  mapping it to a 503 response.
"""

from __future__ import annotations

import json
import logging
from functools import lru_cache

from anthropic import Anthropic, APIError
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.advisor import (
    ADVICE_TOOL_DEFINITION,
    PRESET_QUESTIONS,
    Advice,
    PresetKey,
)
from app.schemas.wardrobe_audit import AuditFacts

logger = logging.getLogger(__name__)


# Output tokens are bounded by the schema (~4 facts + ~4 recs ~= 600 tokens).
_MAX_OUTPUT_TOKENS = 800


class AdvisorUpstreamError(RuntimeError):
    """Raised when Claude fails or returns malformed output."""


# Loaded only once per process; thread-safe for the FastAPI workers.
@lru_cache(maxsize=1)
def _client() -> Anthropic:
    if not settings.anthropic_api_key:
        raise AdvisorUpstreamError(
            "ANTHROPIC_API_KEY is not configured; cannot call the advisor."
        )
    return Anthropic(api_key=settings.anthropic_api_key)


# ---------------------------------------------------------------------------
# System prompt — the contract the model must obey on every call.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are the WearImpact wardrobe sustainability advisor. \
Your role is to help users understand and reduce the environmental impact \
of the clothes they already own.

You operate under STRICT rules. Violating any of them is a failure.

1. NUMBERS
   Use ONLY the numeric values supplied in the <audit_facts> block of the user
   message. Never compute, estimate, round-up, or invent new numbers. If a
   needed figure is not present, write "not measured" rather than guess.

2. RECOMMENDATIONS
   Choose ONLY from interventions listed in audit_facts.interventions. You may
   rephrase the action label for tone, but do not introduce new actions. Quote
   the precomputed `co2_kg_saved` / `water_L_saved` values verbatim where
   available.

3. SCOPE
   This app fights fast-fashion overconsumption — it is NOT a styling app.
   - DO discuss: emissions, water, garment longevity, second-hand purchase,
     repair, donation, responsible disposal, fibre choices.
   - DO NOT discuss: outfit suggestions, what colours look good, occasion
     dressing, body type, fashion trends, brand recommendations.

4. GEOGRAPHY
   Australia-specific benchmarks are unavailable. Always use the EU/UK
   comparisons supplied and surface this caveat in the `caveats` field.

5. TONE
   Encouraging, specific, never preachy or guilt-inducing. Address the user as
   "you". British spelling. No emojis. No exclamation marks.

6. OUTPUT
   Call the `provide_advice` tool exactly once. Output no prose outside the
   tool call.
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_advice(audit: AuditFacts, preset: PresetKey) -> Advice:
    """Produce an Advice object from an audit + chosen preset question.

    Empty wardrobes are short-circuited (no Claude call). Non-empty wardrobes
    go through tool-use which forces a JSON-Schema-compliant response.
    """
    if audit.totals.item_count == 0:
        return _empty_wardrobe_advice()

    user_prompt = _build_user_prompt(audit, preset)

    try:
        response = _client().messages.create(
            model=settings.anthropic_model,
            max_tokens=_MAX_OUTPUT_TOKENS,
            system=SYSTEM_PROMPT,
            tools=[ADVICE_TOOL_DEFINITION],
            tool_choice={"type": "tool", "name": "provide_advice"},
            messages=[{"role": "user", "content": user_prompt}],
        )
    except APIError as exc:
        raise AdvisorUpstreamError(f"Claude API failed: {exc}") from exc

    # Persistent visibility on cost — aggregate over time via log scraping.
    _log_token_usage(response, preset, audit.totals.item_count)

    return _parse_tool_response(response)


def _log_token_usage(response, preset: PresetKey, item_count: int) -> None:
    """Emit a structured log line with the Claude usage block for cost auditing."""
    usage = getattr(response, "usage", None)
    if usage is None:
        return
    logger.info(
        "advisor_call preset=%s items=%d input_tokens=%d output_tokens=%d",
        preset,
        item_count,
        getattr(usage, "input_tokens", 0),
        getattr(usage, "output_tokens", 0),
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_user_prompt(audit: AuditFacts, preset: PresetKey) -> str:
    preset_meta = PRESET_QUESTIONS[preset]
    facts_json = json.dumps(audit.model_dump(), indent=2, default=str)

    return (
        f'The user picked the preset question: "{preset_meta["label"]}"\n\n'
        "Their wardrobe audit (computed deterministically by the backend; "
        "these numbers are authoritative):\n\n"
        f"<audit_facts>\n{facts_json}\n</audit_facts>\n\n"
        f"Focus your response on: {preset_meta['focus']}\n\n"
        "Now call provide_advice."
    )


def _parse_tool_response(response) -> Advice:
    """Extract the tool_use block, validate it, and return an Advice model."""
    tool_block = next(
        (block for block in response.content if block.type == "tool_use"),
        None,
    )
    if tool_block is None:
        raise AdvisorUpstreamError(
            "Claude returned no tool_use block; check that tool_choice was "
            "honoured."
        )

    try:
        return Advice.model_validate(tool_block.input)
    except ValidationError as exc:
        raise AdvisorUpstreamError(
            f"Claude tool output failed schema validation: {exc}"
        ) from exc


def _empty_wardrobe_advice() -> Advice:
    """Static advice for users who haven't catalogued anything yet."""
    return Advice(
        headline="Your wardrobe is empty",
        summary=(
            "Add a few items to your digital wardrobe so we can estimate its "
            "environmental footprint and suggest specific actions."
        ),
        key_facts=[
            {
                "label": "Items catalogued",
                "value": "0",
                "context": "Upload photos to populate your wardrobe.",
            },
            {
                "label": "EU per-capita apparel CO2",
                "value": "442 kg / year",
                "context": "Average annual apparel footprint per EU resident "
                "(used as a proxy in absence of Australian data).",
            },
        ],
        recommendations=[
            {
                "action": "Catalogue what you already own",
                "impact": "Required before personalised advice can be given.",
                "difficulty": "easy",
            },
            {
                "action": "Take photos of your most-worn items first",
                "impact": "Focuses the audit on garments with the largest use-phase impact.",
                "difficulty": "easy",
            },
        ],
        caveats=[
            "Australia-specific benchmarks are not available; figures use "
            "EU/UK datasets as proxies.",
        ],
    )
