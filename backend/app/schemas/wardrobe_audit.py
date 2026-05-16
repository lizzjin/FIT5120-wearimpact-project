"""Epic 3 wardrobe-audit Pydantic schemas.

Defines the request shape sent by the browser (a flat list of garment items
already classified by the model service) and the deterministic facts payload
returned by `wardrobe_audit_service.compute_audit`. The same facts object is
later embedded in the LLM advisor prompt, which is why every quantity carries
its unit in the field name.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.advisor import PresetKey

MainCategory = Literal["upper_body", "lower_body", "footwear"]

# Subcategory whitelist regex: lowercase letters, digits, and underscores only.
# Locks out prompt-injection attempts because the raw string is forwarded to
# the LLM via coverage.unmatched_subcategories. The model classifier emits
# names like "t_shirt", "sports_shorts", etc. — all match this pattern.
_SUBCATEGORY_PATTERN = r"^[a-z0-9_]{1,64}$"

# Same whitelist for fibre keys arriving via wash-label OCR (cotton,
# polyester, wool, ...). The OCR pipeline already normalises to canonical
# kebab-style keys, but we still validate before forwarding to the LLM.
_FIBRE_KEY_PATTERN = r"^[a-z0-9_]{1,32}$"


class MaterialComponent(BaseModel):
    """One row of the wash-label fibre breakdown (e.g. 80% polyester).

    The browser stores extra display fields (`name_en`, `name_zh`, `icon`) from
    the OCR response; those are intentionally not forwarded to the backend
    because the audit only needs the canonical key + percentage. Anything
    extra would just inflate the LLM prompt.
    """

    key: str = Field(pattern=_FIBRE_KEY_PATTERN)
    percent: float = Field(ge=0.0, le=100.0)


class GarmentInput(BaseModel):
    """One row from the browser's IndexedDB, passed to the audit endpoint."""

    main_category: MainCategory
    sub_category: str = Field(pattern=_SUBCATEGORY_PATTERN)
    materials: list[MaterialComponent] | None = Field(default=None, max_length=8)


class AuditRequest(BaseModel):
    """Request body for POST /api/wardrobe/audit.

    `preset` lets the same wardrobe receive different advice angles (impact
    summary vs. reduction plan vs. purchase reflection) and forms part of the
    cache key so each angle is memoised independently.
    """

    garments: list[GarmentInput] = Field(max_length=100)
    preset: PresetKey


class CategoryTotals(BaseModel):
    item_count: int
    co2_kg: float
    water_L: float


class Totals(BaseModel):
    item_count: int
    co2_kg: float
    water_L: float
    by_category: dict[MainCategory, CategoryTotals]


class TopContributor(BaseModel):
    """A single garment subcategory ranked by total CO2 contribution."""

    sub_category: str
    item_count: int
    co2_kg: float
    co2_share_pct: float


class Equivalences(BaseModel):
    """Intuitive comparisons derived from the wardrobe's total CO2."""

    km_driven: float
    km_flown: float
    smartphones_charged: int


class BenchmarkComparison(BaseModel):
    """Wardrobe footprint expressed against EU per-capita annual flows.

    The EU figure is used as a proxy because Australia-specific data is not
    available; the disclaimer surfaces this to the user.
    """

    apparel_co2_pct_of_eu_annual: float
    footwear_co2_pct_of_eu_annual: float
    eu_apparel_kg_co2_year: float
    eu_footwear_kg_co2_year: float


class InterventionSuggestion(BaseModel):
    """A behavioural tip with absolute kg/L savings already computed."""

    key: str
    label: str
    co2_reduction_pct: float | None = None
    co2_kg_saved: float | None = None
    water_reduction_pct: float | None = None
    water_L_saved: float | None = None
    applies_to: str
    source: str


class CoverageReport(BaseModel):
    """How well the reference data covered the user's wardrobe."""

    items_matched: int
    items_unmatched: int
    unmatched_subcategories: list[str]


class MaterialBreakdownEntry(BaseModel):
    """Wardrobe-wide contribution of one fibre type.

    Built only when the user has uploaded wash labels for at least one item.
    `weight_kg` is the total mass of that fibre across the wardrobe (sum of
    `garment_weight × percent / 100`); `co2_kg` / `water_L` follow the same
    pattern using the per-fibre LCA factors. `subcategories` is a small
    sorted list of sub-categories that contain this fibre, useful for the LLM
    to write things like "polyester shows up mainly in your jackets".
    """

    fibre_key: str
    weight_kg: float
    co2_kg: float
    water_L: float
    pct_of_total_co2: float
    pct_of_total_weight: float
    item_count: int
    subcategories: list[str]


class MaterialCoverage(BaseModel):
    """How much of the wardrobe contributed to material_breakdown.

    The advisor falls back to per-garment `dominant_fibre` for items missing
    wash-label data, but only when the dominant fibre is a single canonical
    name (cotton, polyester, …). Blends like "cotton_or_polyester" are
    skipped to avoid invented numbers — `items_skipped_blend_fallback` counts
    those so the LLM can mention them transparently.
    """

    items_with_user_materials: int = 0
    items_with_fallback_fibre: int = 0
    items_skipped_blend_fallback: int = 0
    has_any_material_data: bool = False


class AuditFacts(BaseModel):
    """The deterministic payload handed to the LLM advisor.

    Every number originates from `reference_data.json` and was computed in
    Python — the LLM is forbidden from inventing or recomputing them.
    """

    totals: Totals
    top_contributors: list[TopContributor]
    equivalences: Equivalences
    benchmarks: BenchmarkComparison
    interventions: list[InterventionSuggestion]
    coverage: CoverageReport
    disclaimers: list[str]
    material_breakdown: list[MaterialBreakdownEntry] = Field(default_factory=list)
    material_coverage: MaterialCoverage = Field(default_factory=MaterialCoverage)
