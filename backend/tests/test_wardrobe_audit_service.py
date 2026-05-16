"""Tests for the Epic 3 wardrobe audit service."""

import pytest

from app.schemas.wardrobe_audit import GarmentInput, MaterialComponent
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


# ---------------------------------------------------------------------------
# Material breakdown
# ---------------------------------------------------------------------------


def test_user_materials_recompute_garment_co2_from_fibre_table():
    """A 100% polyester t-shirt must come out heavier in CO2 than the default
    cotton-assumption average (4.6 kg), proving fibre data drives the recalc."""
    poly_t = GarmentInput(
        main_category="upper_body",
        sub_category="t_shirt",
        materials=[MaterialComponent(key="polyester", percent=100)],
    )
    audit = compute_audit([poly_t])

    # 27.2 kg CO2 / kg fabric * 0.21 kg = 5.71 kg
    assert audit.totals.co2_kg == pytest.approx(5.71, abs=0.05)
    assert audit.totals.item_count == 1
    assert audit.material_coverage.items_with_user_materials == 1
    assert audit.material_coverage.has_any_material_data is True

    breakdown = {row.fibre_key: row for row in audit.material_breakdown}
    assert "polyester" in breakdown
    assert breakdown["polyester"].pct_of_total_co2 == pytest.approx(100, abs=0.5)
    assert breakdown["polyester"].subcategories == ["t_shirt"]


def test_blended_user_materials_apportion_weight_per_fibre():
    """80% cotton / 20% polyester on one t-shirt should split mass and CO2
    in those proportions."""
    blended = GarmentInput(
        main_category="upper_body",
        sub_category="t_shirt",
        materials=[
            MaterialComponent(key="cotton", percent=80),
            MaterialComponent(key="polyester", percent=20),
        ],
    )
    audit = compute_audit([blended])

    expected_co2 = (22.0 * 0.21 * 0.8) + (27.2 * 0.21 * 0.2)
    assert audit.totals.co2_kg == pytest.approx(expected_co2, abs=0.05)

    rows = {row.fibre_key: row for row in audit.material_breakdown}
    assert rows["cotton"].pct_of_total_weight == pytest.approx(80, abs=1)
    assert rows["polyester"].pct_of_total_weight == pytest.approx(20, abs=1)


def test_missing_materials_fall_back_to_default_average():
    """No wash-label data -> CO2 stays at the per_garment lifecycle figure and
    the breakdown still surfaces a dominant-fibre row when possible."""
    audit = compute_audit(_wardrobe({"t_shirt": ("upper_body", 1)}))

    # Default per_garment cotton-assumption CO2.
    assert audit.totals.co2_kg == pytest.approx(4.6, abs=0.05)
    # Dominant fibre is "cotton" and resolves in the fibre table, so we still
    # get one breakdown row even without user wash-labels.
    assert audit.material_coverage.items_with_user_materials == 0
    assert audit.material_coverage.items_with_fallback_fibre == 1
    assert audit.material_coverage.has_any_material_data is False
    fibres = {row.fibre_key for row in audit.material_breakdown}
    assert "cotton" in fibres


def test_unknown_fibre_in_user_materials_falls_back_to_default():
    """If wash-label OCR returns a fibre that isn't in our per-kg table
    (e.g. spandex), we fall back to the default average rather than guess."""
    spandex_t = GarmentInput(
        main_category="upper_body",
        sub_category="t_shirt",
        materials=[
            MaterialComponent(key="cotton", percent=95),
            MaterialComponent(key="spandex", percent=5),
        ],
    )
    audit = compute_audit([spandex_t])

    # Mixed-known-and-unknown -> the audit must NOT recompute (would distort
    # the missing 5% mass attribution). Falls back to the per_garment default.
    assert audit.totals.co2_kg == pytest.approx(4.6, abs=0.05)
    assert audit.material_coverage.items_with_user_materials == 0


def test_jacket_with_blend_dominant_skips_breakdown_row():
    """jacket's dominant_fibre is 'polyester_blend' — not a single canonical
    fibre — so without user materials it produces NO breakdown row."""
    audit = compute_audit(_wardrobe({"jacket": ("upper_body", 1)}))

    assert audit.material_breakdown == []
    assert audit.material_coverage.items_skipped_blend_fallback == 1
    assert audit.material_coverage.has_any_material_data is False
