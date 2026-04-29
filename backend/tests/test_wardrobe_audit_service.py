"""Tests for the Epic 3 wardrobe audit service."""

import pytest

from app.schemas.wardrobe_audit import GarmentInput
from app.services.wardrobe_audit_service import compute_audit


def _wardrobe(items: dict[str, tuple[str, int]]) -> list[GarmentInput]:
    """Helper: build a flat garment list from {sub: (main_category, count)}."""
    out: list[GarmentInput] = []
    for sub, (main, count) in items.items():
        out.extend(GarmentInput(main_category=main, sub_category=sub) for _ in range(count))
    return out


def test_canonical_wardrobe_totals_match_reference_arithmetic():
    """10 t-shirts (4.6 kg each) + 3 jeans (13.2 kg each) -> 85.6 kg total."""
    audit = compute_audit(_wardrobe({
        "t_shirt": ("upper_body", 10),
        "jeans": ("lower_body", 3),
    }))

    assert audit.totals.item_count == 13
    assert audit.totals.co2_kg == pytest.approx(85.6, abs=0.05)
    assert audit.totals.water_L == pytest.approx(10 * 1480 + 3 * 4020, abs=1)
    assert audit.totals.by_category["upper_body"].co2_kg == pytest.approx(46.0, abs=0.05)
    assert audit.totals.by_category["lower_body"].co2_kg == pytest.approx(39.6, abs=0.05)


def test_top_contributors_are_sorted_descending_with_share():
    audit = compute_audit(_wardrobe({
        "t_shirt": ("upper_body", 10),
        "jeans": ("lower_body", 3),
    }))

    assert len(audit.top_contributors) == 2
    assert audit.top_contributors[0].sub_category == "t_shirt"
    assert audit.top_contributors[0].item_count == 10
    assert audit.top_contributors[0].co2_share_pct > audit.top_contributors[1].co2_share_pct
    assert audit.top_contributors[0].co2_share_pct + audit.top_contributors[1].co2_share_pct == pytest.approx(100, abs=0.5)


def test_unknown_subcategory_excluded_from_totals_but_recorded_in_coverage():
    audit = compute_audit(_wardrobe({
        "t_shirt": ("upper_body", 2),
        "alien_garment": ("upper_body", 5),
    }))

    assert audit.coverage.items_matched == 2
    assert audit.coverage.items_unmatched == 5
    assert audit.coverage.unmatched_subcategories == ["alien_garment"]
    assert audit.totals.co2_kg == pytest.approx(2 * 4.6, abs=0.05)
    # Disclaimer must mention the dropped items so the LLM can repeat it.
    assert any("could not be matched" in d for d in audit.disclaimers)


def test_empty_wardrobe_returns_zeros_and_no_interventions():
    audit = compute_audit([])

    assert audit.totals.item_count == 0
    assert audit.totals.co2_kg == 0
    assert audit.top_contributors == []
    assert audit.interventions == []
    assert any("No matched garments" in d for d in audit.disclaimers)


def test_footwear_only_skips_use_phase_interventions():
    """Sneakers don't get washed, so the 30 degC tip must not appear."""
    audit = compute_audit(_wardrobe({"sneakers": ("footwear", 4)}))

    keys = {i.key for i in audit.interventions}
    assert "extend_lifetime_2x" in keys
    assert "wash_cold_30c" not in keys


def test_intervention_savings_are_precomputed_in_kg():
    """The LLM must never multiply percentages itself — verify kg savings are
    already populated for percentage-based interventions."""
    audit = compute_audit(_wardrobe({
        "t_shirt": ("upper_body", 10),
        "jeans": ("lower_body", 3),
    }))

    extend = next(i for i in audit.interventions if i.key == "extend_lifetime_2x")
    # extend_lifetime_2x reduces CO2 by 44% per WRAP Table 10.
    expected = round(audit.totals.co2_kg * 0.44, 1)
    assert extend.co2_kg_saved == pytest.approx(expected, abs=0.1)
    assert extend.co2_reduction_pct == 44


def test_benchmark_split_apparel_vs_footwear():
    """Apparel and footwear have very different per-capita baselines; the
    audit must report them separately."""
    audit = compute_audit(_wardrobe({
        "t_shirt": ("upper_body", 10),
        "sneakers": ("footwear", 5),
    }))

    apparel_kg = 10 * 4.6
    footwear_kg = 5 * 14.0
    assert audit.benchmarks.apparel_co2_pct_of_eu_annual == pytest.approx(apparel_kg / 442 * 100, abs=0.1)
    assert audit.benchmarks.footwear_co2_pct_of_eu_annual == pytest.approx(footwear_kg / 94 * 100, abs=0.1)


def test_geography_disclaimer_always_present():
    """Australia data is missing — the user must always be told this."""
    audit = compute_audit(_wardrobe({"t_shirt": ("upper_body", 1)}))

    assert any("Australia" in d for d in audit.disclaimers)
