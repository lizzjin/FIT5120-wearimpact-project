"""Epic 3 advisor output schemas.

Defines:
- The list of preset questions the user can pick from on the frontend (free
  chat is intentionally not offered — the preset constrains LLM scope).
- The structured advice payload that Claude returns via tool-use, mirrored as
  Pydantic models so FastAPI can validate / serialise it.
- A compact follow-up advice payload used when the user drills deeper from an
  earlier answer (rendered as a mini-bubble, not a full 4-bubble response).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

PresetKey = Literal[
    "impact_summary",
    "reduce_my_footprint",
    "rethink_purchases",
    "extend_garment_life",
    "material_breakdown",
]

Difficulty = Literal["easy", "medium", "hard"]

# Layout drives which Vue component renders the advice. Each preset is locked
# to one layout so the answers feel visually distinct.
Layout = Literal["report", "playbook", "decision", "care_guide", "material_map"]

# Slug pattern for recommendation IDs the LLM must emit. Permissive on the
# separator (Claude flips between kebab-case and snake_case depending on the
# preset), strict on the alphabet so the slug stays safe to surface in URLs
# and in the follow-up endpoint's `focus` parameter.
_REC_ID_PATTERN = r"^[a-z0-9][a-z0-9_-]{1,39}$"


class PresetQuestion(BaseModel):
    """One item in the preset-question picker shown above the chat area."""

    key: PresetKey
    label: str
    description: str
    layout: Layout


# Catalogue of preset questions. `focus` is appended verbatim to the LLM user
# prompt to steer which audit_facts get emphasised; `voice` is injected into
# the system prompt so each preset reads in a distinct tone; `layout` is
# returned to the frontend so the chosen Vue component renders a different
# visual skeleton per preset.
PRESET_QUESTIONS: dict[PresetKey, dict[str, str]] = {
    "impact_summary": {
        "label": "What's the environmental impact of my wardrobe?",
        "description": "A snapshot of the embodied CO2, water, and how it compares to averages.",
        "layout": "report",
        "voice": (
            "Speak like an accountant presenting the bill: clinical, factual, "
            "and lead with the single biggest number. Open the summary with "
            "the headline figure (kg CO2) rather than commentary."
        ),
        "focus": (
            "Summarise the wardrobe's overall environmental footprint using "
            "audit_facts.totals, equivalences, and benchmarks. Highlight the "
            "single biggest contributor."
        ),
    },
    "reduce_my_footprint": {
        "label": "How can I reduce my wardrobe's footprint?",
        "description": "Specific, evidence-backed actions ranked by impact.",
        "layout": "playbook",
        "voice": (
            "Speak like a coach: action-first, every recommendation begins "
            "with a verb. Make the summary feel like a playbook intro — three "
            "moves the user can make this week. Avoid throat-clearing."
        ),
        "focus": (
            "Recommend the 3 highest-leverage interventions from "
            "audit_facts.interventions. Quote the precomputed kg/L savings "
            "verbatim where available."
        ),
    },
    "rethink_purchases": {
        "label": "Should I keep buying new clothes?",
        "description": "Reflect on consumption habits and second-hand alternatives.",
        "layout": "decision",
        "voice": (
            "Speak like a Socratic interlocutor: ask before you tell. Use "
            "comparisons (your wardrobe vs the EU average) and pose at least "
            "one rhetorical question inside the summary. Never lecture."
        ),
        "focus": (
            "Encourage the user to reconsider new purchases. Lean on the "
            "extend-lifetime, second-hand, and recycled-fibre interventions, "
            "plus the benchmarks comparison."
        ),
    },
    "extend_garment_life": {
        "label": "How can I make my clothes last longer?",
        "description": "Practical care, washing, and repair habits that delay disposal.",
        "layout": "care_guide",
        "voice": (
            "Speak like an artisan giving care instructions: garment-by-"
            "garment, concrete habits, plain verbs. Reference the user's "
            "actual top contributors by sub_category when possible."
        ),
        "focus": (
            "Centre the response on garment longevity. Lean on "
            "extend_lifetime_2x as the headline lever and back it up with the "
            "use-phase interventions (cold wash, full load, line dry). Cite "
            "the precomputed kg/L savings verbatim, and frame longevity as the "
            "single biggest lever an individual user controls."
        ),
    },
    "material_breakdown": {
        "label": "What are my clothes made of?",
        "description": "Fibre-by-fibre look at what your wardrobe is built from.",
        "layout": "material_map",
        "voice": (
            "Speak like a textile engineer reading a swatch book: name each "
            "fibre, state its specific trade-offs (water-thirsty cotton, "
            "microfibre-shedding polyester, methane-heavy wool), and point "
            "at the user's actual sub-categories that carry that fibre. Stay "
            "neutral — no fibre is universally good or bad."
        ),
        "focus": (
            "Build the answer from audit_facts.material_breakdown. Each "
            "recommendation should target one fibre with the highest CO2 "
            "share. If material_coverage.has_any_material_data is false, "
            "open with a clear note that the answer is based on default "
            "fibre assumptions and ask the user to upload wash labels for "
            "item-specific advice. Never invent fibre numbers; quote the "
            "co2_kg / water_L per fibre verbatim from the breakdown."
        ),
    },
}


def list_preset_questions() -> list[PresetQuestion]:
    """Return preset questions in display order for the GET endpoint."""
    return [
        PresetQuestion(
            key=key,
            label=meta["label"],
            description=meta["description"],
            layout=meta["layout"],
        )
        for key, meta in PRESET_QUESTIONS.items()
    ]


# ---------------------------------------------------------------------------
# Structured advice returned by Claude (via tool_use). The same JSON shape is
# enforced by the Anthropic tool schema and validated again by Pydantic.
# ---------------------------------------------------------------------------


class KeyFact(BaseModel):
    label: str = Field(max_length=60)
    value: str = Field(max_length=80)
    # 240 chars rather than 180: Haiku tends to write a "what + why + source"
    # sentence in this field and 180 was tight enough that the salvage layer
    # had to truncate too often. Frontend visually clamps anyway.
    context: str = Field(max_length=240)


class Recommendation(BaseModel):
    """One action card.

    `id` is a kebab-case slug Claude assigns so the frontend can request a
    drill-down without sending the whole action text back. `follow_up_prompts`
    are the chip labels rendered under the card; tapping one POSTs the prompt
    to the follow-up endpoint.
    """

    id: str = Field(pattern=_REC_ID_PATTERN, max_length=40)
    action: str = Field(max_length=140)
    impact: str = Field(max_length=140)
    difficulty: Difficulty
    follow_up_prompts: list[str] = Field(default_factory=list, max_length=2)


class Advice(BaseModel):
    """The structured advisor response. Only field validation lives here —
    the *content* validation (e.g. "no fabricated numbers") is enforced by
    the system prompt + tool schema, not Pydantic.

    `min_length` is intentionally permissive on the array fields. The system
    prompt steers Claude toward fuller responses, but if a single field comes
    back short we'd rather render what we have than 503 the whole turn.
    """

    layout: Layout
    headline: str = Field(max_length=120)
    # 800 chars (was 600) to fit material-breakdown and decision-layout
    # narratives without the salvage layer truncating constantly. The bubble
    # CSS already wraps cleanly at any length.
    summary: str = Field(max_length=800)
    key_facts: list[KeyFact] = Field(min_length=1, max_length=3)
    recommendations: list[Recommendation] = Field(min_length=1, max_length=4)
    caveats: list[str] = Field(default_factory=list, max_length=3)
    next_questions: list[str] = Field(default_factory=list, max_length=3)


class FollowUpAdvice(BaseModel):
    """Compact response for drill-down questions on an existing advice.

    Rendered as a single mini-bubble; intentionally short so users can ask
    several follow-ups without the conversation feeling repetitive.
    """

    headline: str = Field(max_length=120)
    # 700 chars (was 480) so multi-step garment-care answers ("how do I repair
    # a hole" → patch / thread / press) fit without being rejected wholesale.
    body: str = Field(max_length=700)
    mini_facts: list[KeyFact] = Field(default_factory=list, max_length=2)
    next_questions: list[str] = Field(default_factory=list, max_length=3)


# ---------------------------------------------------------------------------
# JSON Schema handed to Anthropic as the tool's `input_schema`. Keep this in
# sync with `Advice` above; the LLM is forced to call this tool, so its output
# is guaranteed to fit the structure.
# ---------------------------------------------------------------------------

ADVICE_TOOL_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "layout": {
            "type": "string",
            "enum": ["report", "playbook", "decision", "care_guide", "material_map"],
            "description": (
                "Must equal the layout assigned to the user's preset in the "
                "user message. Do not choose freely."
            ),
        },
        "headline": {
            "type": "string",
            "maxLength": 120,
            "description": "Punchy 1-line summary the UI shows in large text.",
        },
        "summary": {
            "type": "string",
            "maxLength": 800,
            "description": "2-3 sentence narrative paragraph.",
        },
        "key_facts": {
            "type": "array",
            "minItems": 2,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string", "maxLength": 60},
                    "value": {
                        "type": "string",
                        "maxLength": 80,
                        "description": "Already formatted with units, e.g. '143 kg CO2'.",
                    },
                    "context": {"type": "string", "maxLength": 240},
                },
                "required": ["label", "value", "context"],
            },
        },
        "recommendations": {
            "type": "array",
            "minItems": 2,
            "maxItems": 4,
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "pattern": _REC_ID_PATTERN,
                        "maxLength": 40,
                        "description": (
                            "Short lowercase slug, 2-40 chars, kebab-case or "
                            "snake_case, derived from the action (e.g. "
                            "'extend-lifetime-2x', 'cold_wash', "
                            "'buy_secondhand', 'polyester-filter-bag'). Used "
                            "as a stable anchor for drill-down questions. Do "
                            "not include spaces, uppercase letters, or "
                            "punctuation other than '-' and '_'."
                        ),
                    },
                    "action": {"type": "string", "maxLength": 140},
                    "impact": {
                        "type": "string",
                        "maxLength": 140,
                        "description": "Quantified outcome, e.g. 'Saves ~63 kg CO2'.",
                    },
                    "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
                    "follow_up_prompts": {
                        "type": "array",
                        "maxItems": 2,
                        "items": {"type": "string", "maxLength": 80},
                        "description": (
                            "0-2 short question labels (under 60 chars) the "
                            "user can tap to drill into this recommendation, "
                            "phrased from the user's perspective, e.g. "
                            "'Why does this work?', 'How do I start?'."
                        ),
                    },
                },
                "required": ["id", "action", "impact", "difficulty"],
            },
        },
        "caveats": {
            "type": "array",
            "maxItems": 3,
            "items": {"type": "string"},
        },
        "next_questions": {
            "type": "array",
            "minItems": 2,
            "maxItems": 3,
            "items": {"type": "string", "maxLength": 90},
            "description": (
                "2-3 contextual follow-up questions phrased as the user "
                "would ask them, grounded in this specific answer. These "
                "replace the static preset chips at the bottom of the chat."
            ),
        },
    },
    "required": [
        "layout",
        "headline",
        "summary",
        "key_facts",
        "recommendations",
        "next_questions",
    ],
}


ADVICE_TOOL_DEFINITION: dict = {
    "name": "provide_advice",
    "description": (
        "Return structured sustainability advice for the user's wardrobe. "
        "All numeric values must come from the audit_facts supplied in the "
        "user message — never invent new figures."
    ),
    "input_schema": ADVICE_TOOL_SCHEMA,
}


# ---------------------------------------------------------------------------
# Follow-up tool: smaller schema, single mini-bubble. Reuses the same audit
# facts but produces tighter output.
# ---------------------------------------------------------------------------

FOLLOW_UP_TOOL_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "headline": {"type": "string", "maxLength": 120},
        "body": {
            "type": "string",
            "maxLength": 700,
            "description": "3-4 sentence answer focused on the user's follow-up.",
        },
        "mini_facts": {
            "type": "array",
            "maxItems": 2,
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string", "maxLength": 60},
                    "value": {"type": "string", "maxLength": 80},
                    "context": {"type": "string", "maxLength": 240},
                },
                "required": ["label", "value", "context"],
            },
        },
        "next_questions": {
            "type": "array",
            "maxItems": 3,
            "items": {"type": "string", "maxLength": 90},
        },
    },
    "required": ["headline", "body"],
}


FOLLOW_UP_TOOL_DEFINITION: dict = {
    "name": "provide_follow_up",
    "description": (
        "Return a compact follow-up answer drilling into a previous advice. "
        "All numbers must still come from the supplied audit_facts."
    ),
    "input_schema": FOLLOW_UP_TOOL_SCHEMA,
}
