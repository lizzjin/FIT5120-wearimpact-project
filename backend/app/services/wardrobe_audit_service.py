"""Epic 3 wardrobe audit calculator.

Pure deterministic logic that converts a user wardrobe (a list of garments
classified by the HuggingFace model service) into an `AuditFacts` payload.
The LLM advisor consumes this payload verbatim — it is responsible for
phrasing, never for arithmetic.

Design rules:
- Every number must be derived from `reference_data.json` via reference_loader.
- Unknown subcategories degrade gracefully: counted in the coverage report but
  excluded from CO2/water totals so users don't see fabricated impacts.
- When a garment carries user-uploaded `materials` (from wash-label OCR), its
  per-item CO2 and water are recomputed from `per_fibre_per_kg_fabric` rather
  than the per_garment average, but only when every fibre key in the breakdown
  is in the canonical fibre table — partial coverage would distort totals.
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
    MaterialBreakdownEntry,
    MaterialCoverage,
    Totals,
    TopContributor,
)
from app.services import reference_loader

# Number of behavioural tips to surface. The LLM trims further if it wants.
_MAX_INTERVENTIONS = 6

# Number of subcategories shown as "top contributors" in the UI.
_TOP_CONTRIBUTOR_LIMIT = 3

# How many fibre rows to surface in material_breakdown — keeps the prompt
# bounded and the UI scannable. Sorted descending by CO2 share.
_MATERIAL_BREAKDOWN_LIMIT = 6


def compute_audit(garments: list[GarmentInput]) -> AuditFacts:
    """Run the full audit pipeline for one wardrobe."""
    per_item = _compute_per_item_impacts(garments)
    totals, coverage = _aggregate_totals(per_item)
    co2_by_sub = _co2_by_subcategory(per_item)

    top_contributors = _rank_top_contributors(co2_by_sub, totals.co2_kg)
    equivalences = _compute_equivalences(totals.co2_kg)
    benchmarks = _compute_benchmarks(totals)

    sub_counts = Counter(g.sub_category for g in garments)
    interventions = _select_interventions(sub_counts.keys(), totals)
    disclaimers = _build_disclaimers(coverage, totals)

    material_breakdown, material_coverage = _compute_material_breakdown(
        per_item, totals.co2_kg
    )

    return AuditFacts(
        totals=totals,
        top_contributors=top_contributors,
        equivalences=equivalences,
        benchmarks=benchmarks,
        interventions=interventions,
        coverage=coverage,
        disclaimers=disclaimers,
        material_breakdown=material_breakdown,
        material_coverage=material_coverage,
    )


# ---------------------------------------------------------------------------
# Per-garment pass — produces one impact record per item so material recalc
# can run before aggregation. Items missing reference data are dropped here
# and surfaced via the coverage report.
# ---------------------------------------------------------------------------

def _compute_per_item_impacts(garments: list[GarmentInput]) -> list[dict]:
    """Return a list of per-item impact dictionaries.

    Each record:
      - sub_category, category
      - co2_kg, water_L (recomputed by fibre when possible, else default)
      - weight_kg
      - fibre_source: "user_materials" | "fallback_dominant" | "default_avg"
      - fibre_components: list of (fibre_key, percent, weight_kg) when fibre
        attribution is possible (user_materials OR fallback_dominant); empty
        otherwise. Used downstream to build the material breakdown.
    """
    records: list[dict] = []
    for g in garments:
        impact = reference_loader.get_garment_impact(g.sub_category)
        if impact is None:
            records.append({
                "sub_category": g.sub_category,
                "category": None,
                "co2_kg": None,
                "water_L": None,
                "weight_kg": None,
                "fibre_source": "unmatched",
                "fibre_components": [],
            })
            continue

        category = impact["category"]
        default_co2 = float(impact["co2_kg_lifecycle"])
        default_water = float(impact["water_L_lifecycle"])
        weight_kg = float(impact.get("weight_kg") or 0.0)
        dominant_fibre = impact.get("dominant_fibre") or ""

        user_components = _normalised_user_components(g.materials)
        if user_components and weight_kg > 0 and _all_fibres_known(user_components):
            co2, water = _recompute_from_fibres(user_components, weight_kg)
            records.append({
                "sub_category": g.sub_category,
                "category": category,
                "co2_kg": co2,
                "water_L": water,
                "weight_kg": weight_kg,
                "fibre_source": "user_materials",
                "fibre_components": [
                    (key, pct, weight_kg * pct / 100.0)
                    for key, pct in user_components
                ],
            })
            continue

        # Fallback: dominant_fibre is a single canonical fibre we can recognise.
        # We keep the default per-garment CO2 (recomputing from a single-fibre
        # guess would mislead since dominant_fibre is just a label) but still
        # attribute the impact to one fibre row for the material breakdown so
        # users who haven't uploaded labels still see something useful.
        if dominant_fibre and reference_loader.get_fibre_impact(dominant_fibre):
            records.append({
                "sub_category": g.sub_category,
                "category": category,
                "co2_kg": default_co2,
                "water_L": default_water,
                "weight_kg": weight_kg,
                "fibre_source": "fallback_dominant",
                "fibre_components": [(dominant_fibre, 100.0, weight_kg)],
            })
            continue

        records.append({
            "sub_category": g.sub_category,
            "category": category,
            "co2_kg": default_co2,
            "water_L": default_water,
            "weight_kg": weight_kg,
            "fibre_source": "default_avg",
            "fibre_components": [],
        })
    return records


def _normalised_user_components(
    materials,
) -> list[tuple[str, float]]:
    """Flatten user-provided MaterialComponent rows into (key, pct) tuples.

    Drops zero-percent entries (OCR sometimes emits placeholders) and
    consolidates duplicate keys (label "60% cotton / 40% cotton" should not
    double-count cotton). Returns [] when nothing usable remains.
    """
    if not materials:
        return []

    bucketed: dict[str, float] = defaultdict(float)
    for m in materials:
        if not m.key or m.percent <= 0:
            continue
        bucketed[m.key] += float(m.percent)
    return list(bucketed.items())


def _all_fibres_known(components: list[tuple[str, float]]) -> bool:
    """True only when every fibre key has a per-kg LCA factor available."""
    return all(reference_loader.get_fibre_impact(k) is not None for k, _ in components)


def _recompute_from_fibres(
    components: list[tuple[str, float]],
    weight_kg: float,
) -> tuple[float, float]:
    """Sum CO2 / water across a garment's fibre composition.

    Each component contributes `factor × weight_kg × percent / 100`. We do not
    normalise percentages to 100 — if a wash label says "98% cotton, 2% other"
    we attribute 98% and let the missing 2% drop. Better to underestimate
    than to attribute mass to a fibre the user did not specify.
    """
    co2_total = 0.0
    water_total = 0.0
    for key, pct in components:
        factor = reference_loader.get_fibre_impact(key)
        if factor is None:
            continue
        share = pct / 100.0
        co2_total += float(factor.get("co2_kg", 0.0)) * weight_kg * share
        water_total += float(factor.get("water_L", 0.0)) * weight_kg * share
    return round(co2_total, 2), round(water_total, 1)


# ---------------------------------------------------------------------------
# Aggregation — sums the per-item impacts into category totals + coverage.
# ---------------------------------------------------------------------------

def _aggregate_totals(per_item: list[dict]) -> tuple[Totals, CoverageReport]:
    co2_by_category: dict[str, float] = defaultdict(float)
    water_by_category: dict[str, float] = defaultdict(float)
    count_by_category: dict[str, int] = defaultdict(int)

    matched_items = 0
    unmatched_items = 0
    unmatched_subs: list[str] = []

    for rec in per_item:
        if rec["category"] is None:
            unmatched_items += 1
            unmatched_subs.append(rec["sub_category"])
            continue
        category = rec["category"]
        co2_by_category[category] += rec["co2_kg"]
        water_by_category[category] += rec["water_L"]
        count_by_category[category] += 1
        matched_items += 1

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

    return totals, coverage


def _co2_by_subcategory(per_item: list[dict]) -> dict[str, float]:
    co2_by_sub: dict[str, float] = defaultdict(float)
    for rec in per_item:
        if rec["category"] is None:
            continue
        co2_by_sub[rec["sub_category"]] += rec["co2_kg"]
    return co2_by_sub


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

    for sub, co2 in ranked[:_TOP_CONTRIBUTOR_LIMIT]:
        impact = reference_loader.get_garment_impact(sub)
        per_item_co2 = float(impact["co2_kg_lifecycle"]) if impact else 0.0
        item_count = int(round(co2 / per_item_co2)) if per_item_co2 else 0
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
    """Surface caveats the LLM must repeat to the user.

    The first entry is always a fully-cited data-sources line built from
    reference_data.sources so the user knows which studies produced every CO2
    and water figure. The system prompt requires the LLM to include this line
    in the rendered caveats — the rest of the list is supporting context.
    """
    notes: list[str] = []

    sources_line = _format_sources_disclaimer()
    if sources_line:
        notes.append(sources_line)

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


def _format_sources_disclaimer() -> str:
    """Build a one-line dataset citation from reference_data.sources.

    The output reads like an academic footnote so it lands as authoritative
    rather than waffly. Format:
        "Data sources: WRAP 2017 (UK cradle-to-grave LCA); IMPRO 2014 (EU per-
         fibre and per-garment LCA); Quantis 2018 (global apparel + footwear)."
    """
    sources = reference_loader.get_sources()
    if not sources:
        return ""

    parts: list[str] = []
    for s in sources:
        sid = s.get("id", "").replace("_", " ")
        scope = (s.get("scope") or "").strip()
        if sid and scope:
            parts.append(f"{sid} ({scope})")
        elif sid:
            parts.append(sid)
    if not parts:
        return ""
    return (
        "Data sources behind every CO2 and water figure: "
        + "; ".join(parts)
        + ". Australia-specific datasets are not available, so these UK / "
        "EU / global studies are used as best proxies."
    )


# ---------------------------------------------------------------------------
# Step 7 — material breakdown
# ---------------------------------------------------------------------------

def _compute_material_breakdown(
    per_item: list[dict],
    total_co2_kg: float,
) -> tuple[list[MaterialBreakdownEntry], MaterialCoverage]:
    """Aggregate per-item fibre contributions into wardrobe-wide rows.

    Returns the breakdown list (sorted by CO2 desc, capped at a small N) plus
    a coverage report so the LLM can introduce the section with the right
    caveat. Items whose dominant_fibre is a blend ("polyester_blend") and
    that lack user-uploaded materials contribute zero fibre rows; they show
    up only in `items_skipped_blend_fallback`.
    """
    fibre_co2: dict[str, float] = defaultdict(float)
    fibre_water: dict[str, float] = defaultdict(float)
    fibre_weight: dict[str, float] = defaultdict(float)
    fibre_subs: dict[str, set[str]] = defaultdict(set)
    fibre_items: dict[str, int] = defaultdict(int)

    items_with_user = 0
    items_with_fallback = 0
    items_skipped = 0

    for rec in per_item:
        if rec["category"] is None:
            continue
        source = rec["fibre_source"]
        if source == "user_materials":
            items_with_user += 1
        elif source == "fallback_dominant":
            items_with_fallback += 1
        else:
            items_skipped += 1
            continue

        weight_kg = float(rec.get("weight_kg") or 0.0)
        if weight_kg <= 0:
            items_skipped += 1
            continue

        # Distribute the item's already-computed CO2/water across its fibre
        # components proportionally to each fibre's mass contribution. Using
        # the already-computed totals (rather than re-multiplying factors)
        # keeps material_breakdown summing back to the wardrobe totals when
        # every item has user materials.
        components = rec["fibre_components"]
        if not components:
            items_skipped += 1
            continue

        for fibre_key, _pct, fibre_weight_kg in components:
            if fibre_weight_kg <= 0:
                continue
            factor = reference_loader.get_fibre_impact(fibre_key)
            if factor is None:
                continue
            fibre_co2[fibre_key] += float(factor.get("co2_kg", 0.0)) * fibre_weight_kg
            fibre_water[fibre_key] += float(factor.get("water_L", 0.0)) * fibre_weight_kg
            fibre_weight[fibre_key] += fibre_weight_kg
            fibre_subs[fibre_key].add(rec["sub_category"])
            fibre_items[fibre_key] += 1

    total_weight_attributed = sum(fibre_weight.values())
    rows: list[MaterialBreakdownEntry] = []
    for fibre_key, co2 in sorted(fibre_co2.items(), key=lambda kv: kv[1], reverse=True):
        pct_co2 = (co2 / total_co2_kg * 100) if total_co2_kg > 0 else 0.0
        pct_weight = (
            fibre_weight[fibre_key] / total_weight_attributed * 100
            if total_weight_attributed > 0
            else 0.0
        )
        rows.append(
            MaterialBreakdownEntry(
                fibre_key=fibre_key,
                weight_kg=round(fibre_weight[fibre_key], 3),
                co2_kg=round(co2, 2),
                water_L=round(fibre_water[fibre_key], 1),
                pct_of_total_co2=round(pct_co2, 1),
                pct_of_total_weight=round(pct_weight, 1),
                item_count=fibre_items[fibre_key],
                subcategories=sorted(fibre_subs[fibre_key]),
            )
        )

    coverage = MaterialCoverage(
        items_with_user_materials=items_with_user,
        items_with_fallback_fibre=items_with_fallback,
        items_skipped_blend_fallback=items_skipped,
        has_any_material_data=items_with_user > 0,
    )

    return rows[:_MATERIAL_BREAKDOWN_LIMIT], coverage
