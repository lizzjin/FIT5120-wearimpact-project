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
- Each preset answers in a distinct voice and locks a specific UI layout, so
  the four canned questions feel like four different conversations rather
  than the same template four times.
"""

from __future__ import annotations

import json
import logging
from functools import lru_cache

from anthropic import Anthropic, APIConnectionError, APIError
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.advisor import (
    ADVICE_TOOL_DEFINITION,
    FOLLOW_UP_TOOL_DEFINITION,
    PRESET_QUESTIONS,
    Advice,
    FollowUpAdvice,
    PresetKey,
)
from app.schemas.wardrobe_audit import AuditFacts

logger = logging.getLogger(__name__)


# Output tokens budget for a full advice payload. Earlier sized at 800 for
# the original 5-block schema; bumped to 1300 once recommendations gained
# per-card `follow_up_prompts` and the top level gained `next_questions` so
# Haiku had room to fill every field without truncating the tool call.
_MAX_OUTPUT_TOKENS = 1300
# Follow-ups are intentionally tighter (single mini-bubble).
_FOLLOW_UP_MAX_TOKENS = 500


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

_BASE_RULES = """You are the WearImpact wardrobe sustainability advisor. \
Your role is to help users understand and reduce the environmental impact \
of the clothes they already own.

You operate under STRICT rules. Violating any of them is a failure.

1. NUMBERS
   Use ONLY the numeric values supplied in the <audit_facts> block of the user
   message. Never compute, estimate, round-up, or invent new numbers. If a
   needed figure is not present, write "not measured" rather than guess.
   The audit may contain a `material_breakdown` array with per-fibre CO2 and
   water figures — when you cite a fibre's impact, quote those numbers
   verbatim from that array, never the fabric-table averages from training.

2. RECOMMENDATIONS
   Choose interventions from audit_facts.interventions or, for the material
   preset, fibre-specific actions grounded in audit_facts.material_breakdown
   (e.g. "wash polyester pieces in a microfibre filter bag"). You may rephrase
   action labels for tone, but do not introduce new behavioural percentages.
   Quote the precomputed `co2_kg_saved` / `water_L_saved` values verbatim
   where available. Each recommendation needs a short lowercase slug `id`
   (2-40 chars, kebab-case or snake_case only — no spaces, no uppercase, no
   punctuation other than '-' and '_'). Derive the slug from the
   intervention key or action verb (e.g. `extend-lifetime-2x`, `cold_wash`,
   `polyester-filter-bag`).

3. SCOPE
   This app fights fast-fashion overconsumption — it is NOT a styling app.
   - DO discuss: emissions, water, garment longevity, second-hand purchase,
     repair, donation, responsible disposal, fibre choices.
   - DO NOT discuss: outfit suggestions, what colours look good, occasion
     dressing, body type, fashion trends, brand recommendations.

4. GEOGRAPHY AND CITATIONS
   Australia-specific benchmarks are unavailable. Always use the EU/UK
   comparisons supplied. The first entry in `audit_facts.disclaimers` is a
   fully-cited list of data sources (WRAP 2017, IMPRO 2014, Quantis 2018,
   etc.). You MUST surface that exact sources line as the first entry of
   `caveats`, verbatim or with only minor wording tweaks — never drop the
   dataset names (WRAP / IMPRO / Quantis) or their years, and never
   substitute generic phrases like "UK and EU data".

5. FOLLOW-UPS
   Every answer must end with 2-3 `next_questions` the user is most likely to
   ask next, grounded in *this specific* answer (cite the actual numbers and
   items you discussed). Per-recommendation `follow_up_prompts` are optional
   but encouraged — 0-2 short labels under 60 chars each, phrased from the
   user's first-person perspective ("How do I start?", "Why does this work?").

6. TONE BASELINE
   Encouraging, specific, never preachy or guilt-inducing. Address the user
   as "you". British spelling. No emojis. No exclamation marks.

7. OUTPUT
   Call the tool exactly once. Output no prose outside the tool call.
"""


def _system_prompt_for(preset: PresetKey) -> str:
    """Combine the base contract with the preset-specific voice instruction."""
    voice = PRESET_QUESTIONS[preset]["voice"]
    return _BASE_RULES + "\n8. VOICE FOR THIS QUESTION\n   " + voice + "\n"


def _follow_up_system_prompt(preset: PresetKey) -> str:
    """System prompt for the compact follow-up tool."""
    voice = PRESET_QUESTIONS[preset]["voice"]
    return (
        _BASE_RULES
        + "\n8. VOICE FOR THIS QUESTION\n   "
        + voice
        + "\n\n9. FOLLOW-UP MODE\n"
        + "   This is a drill-down on a previous answer. Keep the body to 3-4\n"
        + "   sentences, include at most 2 mini_facts, and suggest at most 3\n"
        + "   short next_questions. Do not repeat headline figures already\n"
        + "   given unless the user explicitly asked for them again.\n"
    )


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
            system=_system_prompt_for(preset),
            tools=[ADVICE_TOOL_DEFINITION],
            tool_choice={"type": "tool", "name": "provide_advice"},
            messages=[{"role": "user", "content": user_prompt}],
        )
    except APIConnectionError as exc:
        # Network-layer failure: the underlying httpx error often has the
        # actionable detail (DNS, TLS, ECONNREFUSED, etc.). Surface it.
        cause = exc.__cause__ or exc.__context__
        cause_repr = repr(cause) if cause else "no underlying cause"
        logger.error(
            "Advisor connection error: type=%s msg=%r cause=%s",
            type(exc).__name__,
            str(exc),
            cause_repr,
        )
        raise AdvisorUpstreamError(
            f"Claude API connection failed: {cause_repr}"
        ) from exc
    except APIError as exc:
        logger.error(
            "Advisor API error: type=%s status=%s msg=%r",
            type(exc).__name__,
            getattr(exc, "status_code", "n/a"),
            str(exc),
        )
        raise AdvisorUpstreamError(f"Claude API failed: {exc}") from exc

    # Persistent visibility on cost — aggregate over time via log scraping.
    _log_token_usage(response, preset, audit.totals.item_count)

    advice = _parse_tool_response(response, Advice, "provide_advice")
    # The schema lets Claude emit any layout; pin it to the preset's layout
    # so a model slip-up doesn't break the frontend's switch.
    expected_layout = PRESET_QUESTIONS[preset]["layout"]
    if advice.layout != expected_layout:
        logger.warning(
            "advisor layout mismatch: preset=%s expected=%s got=%s — forcing",
            preset,
            expected_layout,
            advice.layout,
        )
        advice = advice.model_copy(update={"layout": expected_layout})

    return _backfill_follow_ups(advice, preset)


def _backfill_follow_ups(advice: Advice, preset: PresetKey) -> Advice:
    """Inject sensible defaults when Claude omits follow-up affordances.

    The tool schema marks `next_questions` / `follow_up_prompts` as required-ish
    (minItems=2 for next_questions), but Haiku occasionally returns empty
    arrays anyway. Without these fields the UI falls back to the static preset
    chip bar, defeating the whole "contextual follow-up" change. Filling in
    sensible defaults keeps the drill-down chips visible even on a misbehaving
    response.
    """
    updates: dict = {}

    if not advice.next_questions:
        updates["next_questions"] = list(_DEFAULT_NEXT_QUESTIONS[preset])

    # Each recommendation needs at least one chip so users always see a
    # "drill into this card" affordance. We don't overwrite Claude's choices —
    # only fill empty slots.
    new_recs = []
    changed = False
    for rec in advice.recommendations:
        if not rec.follow_up_prompts:
            new_recs.append(rec.model_copy(update={
                "follow_up_prompts": ["Tell me more"],
            }))
            changed = True
        else:
            new_recs.append(rec)
    if changed:
        updates["recommendations"] = new_recs

    return advice.model_copy(update=updates) if updates else advice


# Defaults chosen per preset so the chips read naturally even when Claude
# returns nothing. Each list is intentionally 2-3 items long.
_DEFAULT_NEXT_QUESTIONS: dict[PresetKey, tuple[str, ...]] = {
    "impact_summary": (
        "Which single item is the biggest contributor?",
        "How does my wardrobe compare to a low-impact one?",
        "Where do the water figures come from?",
    ),
    "reduce_my_footprint": (
        "Which action should I try first?",
        "How much could I save in a year?",
        "What if I can only do one of these?",
    ),
    "rethink_purchases": (
        "What counts as a low-impact purchase?",
        "Is second-hand always greener?",
        "How often is it OK to buy new?",
    ),
    "extend_garment_life": (
        "How do I start caring for my most-worn item?",
        "Which habit has the biggest payoff?",
        "How do I know when something is past repair?",
    ),
    "material_breakdown": (
        "Which fibre should I avoid buying next?",
        "Are my mixed-fibre items recyclable?",
        "Which piece is hurting my footprint the most?",
    ),
}


def generate_follow_up(
    audit: AuditFacts,
    parent_preset: PresetKey,
    focus: str,
    sub_prompt: str,
) -> FollowUpAdvice:
    """Produce a compact follow-up answer that drills into a previous advice.

    `focus` is the slug of the recommendation the user tapped (or an empty
    string if the user picked a top-level next_question instead). `sub_prompt`
    is the human-readable question text. Both are forwarded to Claude so it
    can ground the reply in the right corner of the audit.
    """
    if audit.totals.item_count == 0:
        return _empty_wardrobe_follow_up()

    user_prompt = _build_follow_up_prompt(audit, parent_preset, focus, sub_prompt)

    try:
        response = _client().messages.create(
            model=settings.anthropic_model,
            max_tokens=_FOLLOW_UP_MAX_TOKENS,
            system=_follow_up_system_prompt(parent_preset),
            tools=[FOLLOW_UP_TOOL_DEFINITION],
            tool_choice={"type": "tool", "name": "provide_follow_up"},
            messages=[{"role": "user", "content": user_prompt}],
        )
    except APIConnectionError as exc:
        cause = exc.__cause__ or exc.__context__
        cause_repr = repr(cause) if cause else "no underlying cause"
        logger.error(
            "Advisor follow-up connection error: type=%s msg=%r cause=%s",
            type(exc).__name__,
            str(exc),
            cause_repr,
        )
        raise AdvisorUpstreamError(
            f"Claude API connection failed: {cause_repr}"
        ) from exc
    except APIError as exc:
        logger.error(
            "Advisor follow-up API error: type=%s status=%s msg=%r",
            type(exc).__name__,
            getattr(exc, "status_code", "n/a"),
            str(exc),
        )
        raise AdvisorUpstreamError(f"Claude API failed: {exc}") from exc

    _log_token_usage(response, parent_preset, audit.totals.item_count, kind="follow_up")
    follow_up = _parse_tool_response(response, FollowUpAdvice, "provide_follow_up")

    # Keep the chip chain alive even when Claude omits next_questions on a
    # drill-down — pull from the same preset defaults so the user can keep
    # exploring without bouncing back to the static preset list.
    if not follow_up.next_questions:
        follow_up = follow_up.model_copy(update={
            "next_questions": list(_DEFAULT_NEXT_QUESTIONS[parent_preset][:2]),
        })
    return follow_up


def _log_token_usage(
    response,
    preset: PresetKey,
    item_count: int,
    kind: str = "advice",
) -> None:
    """Emit a structured log line with the Claude usage block for cost auditing."""
    usage = getattr(response, "usage", None)
    if usage is None:
        return
    logger.info(
        "advisor_call kind=%s preset=%s items=%d input_tokens=%d output_tokens=%d",
        kind,
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
        f'You MUST set advice.layout = "{preset_meta["layout"]}".\n\n'
        "Their wardrobe audit (computed deterministically by the backend; "
        "these numbers are authoritative):\n\n"
        f"<audit_facts>\n{facts_json}\n</audit_facts>\n\n"
        f"Focus your response on: {preset_meta['focus']}\n\n"
        "Now call provide_advice."
    )


def _build_follow_up_prompt(
    audit: AuditFacts,
    parent_preset: PresetKey,
    focus: str,
    sub_prompt: str,
) -> str:
    preset_meta = PRESET_QUESTIONS[parent_preset]
    facts_json = json.dumps(audit.model_dump(), indent=2, default=str)
    focus_line = (
        f"The user is drilling into recommendation `{focus}`.\n"
        if focus
        else "The user is asking a contextual follow-up to the previous answer.\n"
    )

    return (
        f"The user previously asked: \"{preset_meta['label']}\"\n"
        f"They now want to follow up with: \"{sub_prompt}\"\n\n"
        f"{focus_line}\n"
        "Use the same audit_facts (already authoritative) to answer:\n\n"
        f"<audit_facts>\n{facts_json}\n</audit_facts>\n\n"
        "Now call provide_follow_up. Keep the body to 3-4 sentences."
    )


def _parse_tool_response(response, model_cls, tool_name: str):
    """Extract the tool_use block, validate it, and return the model instance.

    Validation failures are noisy in production logs on purpose — when Haiku
    returns a payload that doesn't fit the Pydantic schema, the only way to
    fix the prompt is to know *exactly* which fields it broke. The raw input
    is dumped under DEBUG to keep INFO-level logs lean.
    """
    tool_block = next(
        (block for block in response.content if block.type == "tool_use"),
        None,
    )
    if tool_block is None:
        # Stop reason is the most useful signal here: "max_tokens" means we
        # were truncated mid-tool-call, "end_turn" means the model bailed.
        stop_reason = getattr(response, "stop_reason", "unknown")
        text_preview = ""
        for block in getattr(response, "content", []):
            if getattr(block, "type", None) == "text":
                text_preview = (getattr(block, "text", "") or "")[:200]
                break
        logger.error(
            "Advisor %s missing tool_use block (stop_reason=%s, text_preview=%r)",
            tool_name,
            stop_reason,
            text_preview,
        )
        raise AdvisorUpstreamError(
            f"Claude returned no tool_use block for {tool_name}; "
            f"stop_reason={stop_reason}."
        )

    try:
        return model_cls.model_validate(tool_block.input)
    except ValidationError as exc:
        # Surface every offending field by name + the offending value so the
        # fix is obvious from the log line alone.
        offending = [
            {"loc": list(err.get("loc", [])), "type": err.get("type"), "msg": err.get("msg")}
            for err in exc.errors()
        ]
        logger.error(
            "Advisor %s schema validation failed: errors=%s",
            tool_name,
            offending,
        )
        logger.debug("Advisor %s offending tool input: %r", tool_name, tool_block.input)
        raise AdvisorUpstreamError(
            f"Claude tool output failed schema validation: {offending}"
        ) from exc


def _empty_wardrobe_advice() -> Advice:
    """Static advice for users who haven't catalogued anything yet."""
    return Advice(
        layout="report",
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
                "id": "catalogue-wardrobe",
                "action": "Catalogue what you already own",
                "impact": "Required before personalised advice can be given.",
                "difficulty": "easy",
                "follow_up_prompts": [],
            },
            {
                "id": "photograph-most-worn",
                "action": "Take photos of your most-worn items first",
                "impact": "Focuses the audit on garments with the largest use-phase impact.",
                "difficulty": "easy",
                "follow_up_prompts": [],
            },
        ],
        caveats=[
            "Australia-specific benchmarks are not available; figures use "
            "EU/UK datasets as proxies.",
        ],
        next_questions=[
            "How do I add items to my wardrobe?",
            "Which items should I photograph first?",
        ],
    )


def _empty_wardrobe_follow_up() -> FollowUpAdvice:
    return FollowUpAdvice(
        headline="Add a few items first",
        body=(
            "I cannot drill into specific recommendations until your wardrobe "
            "contains at least one item. Upload a photo to get started."
        ),
        mini_facts=[],
        next_questions=["How do I add items to my wardrobe?"],
    )
