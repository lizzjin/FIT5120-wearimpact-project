"""Epic 3 wardrobe audit calculator.

Pure deterministic logic that converts a user wardrobe (a list of garments
classified by the HuggingFace model service) into an `AuditFacts` payload.
The LLM advisor consumes this payload verbatim — it is responsible for
phrasing, never for arithmetic.

Design rules:
- Every number must be derived from `reference_data.json` via reference_loader.
- Unknown subcategories degrade gracefully: counted in the coverage report but
  excluded from CO2/water totals so users don't see fabricated impacts.
- Functions are side-effect free, making them trivial to unit-test.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from app.schemas.wardrobe_audit import (
    AuditFacts,
    BenchmarkComparison,
    CategoryTotals,
    CoverageReport,
    Equivalences,
    GarmentInput,
    InterventionSuggestion,
    Totals,
    TopContributor,
)
from app.services import reference_loader

# Number of behavioural tips to surface. The LLM trims further if it wants.
_MAX_INTERVENTIONS = 6

# Number of subcategories shown as "top contributors" in the UI.
_TOP_CONTRIBUTOR_LIMIT = 3


def compute_audit(garments: list[GarmentInput]) -> AuditFacts:
    """Run the full audit pipeline for one wardrobe."""
    sub_counts = Counter(g.sub_category for g in garments)

    totals, by_subcategory_co2, coverage = _compute_totals(sub_counts)
    top_contributors = _rank_top_contributors(by_subcategory_co2, totals.co2_kg)
    equivalences = _compute_equivalences(totals.co2_kg)
    benchmarks = _compute_benchmarks(totals)
    interventions = _select_interventions(sub_counts.keys(), totals)
    disclaimers = _build_disclaimers(coverage, totals)

    return AuditFacts(
        totals=totals,
        top_contributors=top_contributors,
        equivalences=equivalences,
        benchmarks=benchmarks,
        interventions=interventions,
        coverage=coverage,
        disclaimers=disclaimers,
    )


# ---------------------------------------------------------------------------
# Step 1 — totals
# ---------------------------------------------------------------------------

def _compute_totals(
    sub_counts: Counter[str],
) -> tuple[Totals, dict[str, float], CoverageReport]:
    """Sum CO2 and water across the wardrobe, partitioned by main category.

    Returns (totals, per-subcategory CO2, coverage report). The per-subcategory
    map is used downstream to rank top contributors without re-summing.
    """
    co2_by_category: dict[str, float] = defaultdict(float)
    water_by_category: dict[str, float] = defaultdict(float)
    count_by_category: dict[str, int] = defaultdict(int)
    co2_by_sub: dict[str, float] = defaultdict(float)

    matched_items = 0
    unmatched_items = 0
    unmatched_subs: list[str] = []

    for sub, count in sub_counts.items():
        impact = reference_loader.get_garment_impact(sub)
        if impact is None:
            unmatched_items += count
            unmatched_subs.append(sub)
            continue

        category = impact["category"]
        per_item_co2 = float(impact["co2_kg_lifecycle"])
        per_item_water = float(impact["water_L_lifecycle"])

        co2_by_category[category] += per_item_co2 * count
        water_by_category[category] += per_item_water * count
        count_by_category[category] += count
        co2_by_sub[sub] = per_item_co2 * count
        matched_items += count

    by_category_payload: dict[str, CategoryTotals] = {}
    for category in ("upper_body", "lower_body", "footwear"):
        if count_by_category[category] == 0:
            continue
        by_category_payload[category] = CategoryTotals(
            item_count=count_by_category[category],
            co2_kg=round(co2_by_category[category], 2),
            water_L=round(water_by_category[category], 1),
        )

    totals = Totals(
        item_count=matched_items,
        co2_kg=round(sum(co2_by_category.values()), 2),
        water_L=round(sum(water_by_category.values()), 1),
        by_category=by_category_payload,  # type: ignore[arg-type]
    )

    coverage = CoverageReport(
        items_matched=matched_items,
        items_unmatched=unmatched_items,
        unmatched_subcategories=sorted(set(unmatched_subs)),
    )

    return totals, co2_by_sub, coverage


# ---------------------------------------------------------------------------
# Step 2 — top contributors
# ---------------------------------------------------------------------------

def _rank_top_contributors(
    co2_by_sub: dict[str, float],
    total_co2: float,
) -> list[TopContributor]:
    """Return the N subcategories that drive the biggest share of total CO2."""
    if total_co2 <= 0 or not co2_by_sub:
        return []

    ranked = sorted(co2_by_sub.items(), key=lambda kv: kv[1], reverse=True)
    contributors: list[TopContributor] = []
    sub_counts_lookup: dict[str, int] = {}

    for sub, co2 in ranked[:_TOP_CONTRIBUTOR_LIMIT]:
        impact = reference_loader.get_garment_impact(sub)
        per_item_co2 = float(impact["co2_kg_lifecycle"]) if impact else 0.0
        item_count = int(round(co2 / per_item_co2)) if per_item_co2 else 0
        sub_counts_lookup[sub] = item_count
        contributors.append(
            TopContributor(
                sub_category=sub,
                item_count=item_count,
                co2_kg=round(co2, 2),
                co2_share_pct=round(co2 / total_co2 * 100, 1),
            )
        )
    return contributors


# ---------------------------------------------------------------------------
# Step 3 — equivalences
# ---------------------------------------------------------------------------

def _compute_equivalences(total_co2_kg: float) -> Equivalences:
    """Translate kg CO2 into intuitive comparisons (km driven, etc)."""
    factors = reference_loader.get_equivalences()
    km_per_kg = float(factors.get("km_driven_per_kg_co2", 0))
    flight_per_kg = float(factors.get("km_flown_per_kg_co2", 0))
    phones_per_kg = float(factors.get("smartphones_charged_per_kg_co2", 0))

    return Equivalences(
        km_driven=round(total_co2_kg * km_per_kg, 1),
        km_flown=round(total_co2_kg * flight_per_kg, 1),
        smartphones_charged=int(round(total_co2_kg * phones_per_kg)),
    )


# ---------------------------------------------------------------------------
# Step 4 — benchmark comparison
# ---------------------------------------------------------------------------

def _compute_benchmarks(totals: Totals) -> BenchmarkComparison:
    """Compare wardrobe CO2 against EU per-capita annual figures.

    Apparel and footwear are split because their per-capita totals differ by
    nearly 5x and lumping them together would mislead the user.
    """
    apparel_kg = totals.by_category.get("upper_body", CategoryTotals(item_count=0, co2_kg=0, water_L=0)).co2_kg + \
        totals.by_category.get("lower_body", CategoryTotals(item_count=0, co2_kg=0, water_L=0)).co2_kg
    footwear_kg = totals.by_category.get("footwear", CategoryTotals(item_count=0, co2_kg=0, water_L=0)).co2_kg

    eu_apparel = reference_loader.get_benchmark("eu_per_capita_kg_co2_apparel_year")
    eu_footwear = reference_loader.get_benchmark("eu_per_capita_kg_co2_footwear_year")
    eu_apparel_kg = float(eu_apparel["value"]) if eu_apparel else 442.0
    eu_footwear_kg = float(eu_footwear["value"]) if eu_footwear else 94.0

    return BenchmarkComparison(
        apparel_co2_pct_of_eu_annual=round(apparel_kg / eu_apparel_kg * 100, 1),
        footwear_co2_pct_of_eu_annual=round(footwear_kg / eu_footwear_kg * 100, 1),
        eu_apparel_kg_co2_year=eu_apparel_kg,
        eu_footwear_kg_co2_year=eu_footwear_kg,
    )


# ---------------------------------------------------------------------------
# Step 5 — interventions
# ---------------------------------------------------------------------------

def _select_interventions(
    subcategories,
    totals: Totals,
) -> list[InterventionSuggestion]:
    """Pick interventions and pre-compute absolute savings.

    Pre-computing kg/L saved here means the LLM never multiplies percentages —
    it just reads the savings field and writes prose.
    """
    raw = reference_loader.get_interventions_for(subcategories)
    suggestions: list[InterventionSuggestion] = []

    for entry in raw[:_MAX_INTERVENTIONS]:
        co2_pct = entry.get("co2_reduction_pct")
        water_pct = entry.get("water_reduction_pct")

        co2_saved = (
            round(totals.co2_kg * co2_pct / 100, 1) if co2_pct is not None else None
        )
        water_saved = (
            round(totals.water_L * water_pct / 100, 1) if water_pct is not None else None
        )

        suggestions.append(
            InterventionSuggestion(
                key=entry["key"],
                label=entry["label"],
                co2_reduction_pct=co2_pct,
                co2_kg_saved=co2_saved,
                water_reduction_pct=water_pct,
                water_L_saved=water_saved,
                applies_to=entry["applies_to"],
                source=entry["source"],
            )
        )
    return suggestions


# ---------------------------------------------------------------------------
# Step 6 — disclaimers
# ---------------------------------------------------------------------------

def _build_disclaimers(coverage: CoverageReport, totals: Totals) -> list[str]:
    """Surface caveats the LLM must repeat to the user."""
    notes: list[str] = []

    geo = reference_loader.get_reference_data().get("disclaimers", {}).get("geography")
    if geo:
        notes.append(geo)

    if coverage.items_unmatched:
        notes.append(
            f"{coverage.items_unmatched} item(s) in your wardrobe could not be "
            "matched to reference data and were excluded from the totals."
        )

    if totals.item_count == 0:
        notes.append(
            "No matched garments — totals are zero. Add items to your wardrobe "
            "to receive personalised insights."
        )

    return notes
