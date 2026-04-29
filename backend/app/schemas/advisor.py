"""Epic 3 advisor output schemas.

Defines:
- The list of preset questions the user can pick from on the frontend (free
  chat is intentionally not offered — the preset constrains LLM scope).
- The structured advice payload that Claude returns via tool-use, mirrored as
  Pydantic models so FastAPI can validate / serialise it.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

PresetKey = Literal[
    "impact_summary",
    "reduce_my_footprint",
    "rethink_purchases",
    "extend_garment_life",
]

Difficulty = Literal["easy", "medium", "hard"]


class PresetQuestion(BaseModel):
    """One item in the preset-question picker shown above the chat area."""

    key: PresetKey
    label: str
    description: str


# Catalogue of preset questions. The `focus` line is appended verbatim to the
# LLM user prompt to steer which audit_facts get emphasised.
PRESET_QUESTIONS: dict[PresetKey, dict[str, str]] = {
    "impact_summary": {
        "label": "What's the environmental impact of my wardrobe?",
        "description": "A snapshot of the embodied CO2, water, and how it compares to averages.",
        "focus": (
            "Summarise the wardrobe's overall environmental footprint using "
            "audit_facts.totals, equivalences, and benchmarks. Highlight the "
            "single biggest contributor."
        ),
    },
    "reduce_my_footprint": {
        "label": "How can I reduce my wardrobe's footprint?",
        "description": "Specific, evidence-backed actions ranked by impact.",
        "focus": (
            "Recommend the 3 highest-leverage interventions from "
            "audit_facts.interventions. Quote the precomputed kg/L savings "
            "verbatim where available."
        ),
    },
    "rethink_purchases": {
        "label": "Should I keep buying new clothes?",
        "description": "Reflect on consumption habits and second-hand alternatives.",
        "focus": (
            "Encourage the user to reconsider new purchases. Lean on the "
            "extend-lifetime, second-hand, and recycled-fibre interventions, "
            "plus the benchmarks comparison."
        ),
    },
    "extend_garment_life": {
        "label": "How can I make my clothes last longer?",
        "description": "Practical care, washing, and repair habits that delay disposal.",
        "focus": (
            "Centre the response on garment longevity. Lean on "
            "extend_lifetime_2x as the headline lever and back it up with the "
            "use-phase interventions (cold wash, full load, line dry). Cite "
            "the precomputed kg/L savings verbatim, and frame longevity as the "
            "single biggest lever an individual user controls."
        ),
    },
}


def list_preset_questions() -> list[PresetQuestion]:
    """Return preset questions in display order for the GET endpoint."""
    return [
        PresetQuestion(key=key, label=meta["label"], description=meta["description"])
        for key, meta in PRESET_QUESTIONS.items()
    ]


# ---------------------------------------------------------------------------
# Structured advice returned by Claude (via tool_use). The same JSON shape is
# enforced by the Anthropic tool schema and validated again by Pydantic.
# ---------------------------------------------------------------------------


class KeyFact(BaseModel):
    label: str = Field(max_length=60)
    value: str = Field(max_length=80)
    context: str = Field(max_length=180)


class Recommendation(BaseModel):
    action: str = Field(max_length=140)
    impact: str = Field(max_length=140)
    difficulty: Difficulty


class Advice(BaseModel):
    """The structured advisor response. Only field validation lives here —
    the *content* validation (e.g. "no fabricated numbers") is enforced by
    the system prompt + tool schema, not Pydantic."""

    headline: str = Field(max_length=120)
    summary: str = Field(max_length=600)
    key_facts: list[KeyFact] = Field(min_length=2, max_length=3)
    recommendations: list[Recommendation] = Field(min_length=2, max_length=4)
    caveats: list[str] = Field(default_factory=list, max_length=3)


# ---------------------------------------------------------------------------
# JSON Schema handed to Anthropic as the tool's `input_schema`. Keep this in
# sync with `Advice` above; the LLM is forced to call this tool, so its output
# is guaranteed to fit the structure.
# ---------------------------------------------------------------------------

ADVICE_TOOL_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "headline": {
            "type": "string",
            "maxLength": 120,
            "description": "Punchy 1-line summary the UI shows in large text.",
        },
        "summary": {
            "type": "string",
            "maxLength": 600,
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
                    "context": {"type": "string", "maxLength": 180},
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
                    "action": {"type": "string", "maxLength": 140},
                    "impact": {
                        "type": "string",
                        "maxLength": 140,
                        "description": "Quantified outcome, e.g. 'Saves ~63 kg CO2'.",
                    },
                    "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
                },
                "required": ["action", "impact", "difficulty"],
            },
        },
        "caveats": {
            "type": "array",
            "maxItems": 3,
            "items": {"type": "string"},
        },
    },
    "required": ["headline", "summary", "key_facts", "recommendations"],
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
