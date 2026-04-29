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


class GarmentInput(BaseModel):
    """One row from the browser's IndexedDB, passed to the audit endpoint."""

    main_category: MainCategory
    sub_category: str = Field(pattern=_SUBCATEGORY_PATTERN)


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
