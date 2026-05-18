"""Tests for the Epic 3 reference data loader."""

from app.services import reference_loader


def test_loads_reference_data_with_expected_top_level_keys():
    data = reference_loader.get_reference_data()

    expected_keys = {
        "schema_version",
        "sources",
        "per_garment",
        "per_fibre_per_kg_fabric",
        "interventions",
        "benchmarks",
        "equivalences",
        "industry_context",
    }
    assert expected_keys.issubset(data.keys())


def test_t_shirt_has_known_co2_value():
    """The IMPRO 2014 figure is the canonical reference; if this changes the
    LLM-facing numbers change and we need to re-validate the prompt."""
    impact = reference_loader.get_garment_impact("t_shirt")

    assert impact is not None
    assert impact["co2_kg_lifecycle"] == 4.6
    assert impact["category"] == "upper_body"


def test_unknown_garment_returns_none():
    assert reference_loader.get_garment_impact("does_not_exist") is None


def test_aliased_subcategory_resolves_to_canonical_record():
    """The model emits fine-grained labels like 'sports_shorts' that aren't
    in per_garment directly; the alias map must redirect them to 'shorts'."""
    sports_shorts = reference_loader.get_garment_impact("sports_shorts")
    canonical_shorts = reference_loader.get_garment_impact("shorts")

    assert sports_shorts is not None
    assert sports_shorts == canonical_shorts


def test_every_taxonomy_subcategory_resolves():
    """Guards against the model classifier shipping a label our reference
    data cannot translate. Mirrors CATEGORY_TAXONOMY in FIT5120-Classification-Mod/app.py."""
    taxonomy = [
        # upper_body
        "t_shirt", "tank_top_vest", "shirt_blouse", "polo_shirt",
        "hoodie_sweatshirt", "sweater_pullover", "cardigan", "suit_jacket",
        "jacket", "trench_coat", "overcoat", "down_jacket", "dress",
        # lower_body
        "jeans", "dress_pants", "sweatpants_joggers", "leggings",
        "casual_shorts", "sports_shorts", "mini_skirt", "maxi_skirt",
        "pleated_skirt",
        # footwear
        "sneakers", "skate_shoes", "running_shoes", "oxfords", "loafers",
        "derby_shoes", "ankle_boots", "high_boots", "martin_boots",
        "sandals", "slippers", "flip_flops",
    ]
    unresolved = [
        sub for sub in taxonomy
        if reference_loader.get_garment_impact(sub) is None
    ]
    assert unresolved == [], f"Subcategories without LCA data: {unresolved}"


def test_cotton_fibre_lookup():
    cotton = reference_loader.get_fibre_impact("cotton")

    assert cotton is not None
    assert cotton["co2_kg"] == 22.0
    assert cotton["water_L"] == 11000


def test_apparel_wardrobe_yields_use_phase_interventions():
    interventions = reference_loader.get_interventions_for(["t_shirt", "jeans"])

    keys = {item["key"] for item in interventions}
    assert "extend_lifetime_2x" in keys
    assert "wash_cold_30c" in keys


def test_footwear_only_wardrobe_skips_use_phase_interventions():
    """Recommending a 30 degC wash to someone who only stored shoes would be
    nonsense, so the heuristic must drop those tips."""
    interventions = reference_loader.get_interventions_for(["sneakers"])

    keys = {item["key"] for item in interventions}
    assert "extend_lifetime_2x" in keys
    assert "wash_cold_30c" not in keys


def test_empty_wardrobe_returns_no_interventions():
    assert reference_loader.get_interventions_for([]) == []


def test_benchmarks_include_geography_disclaimer():
    """The dataset must continue to flag missing AU data so the advisor never
    invents a local benchmark."""
    benchmarks = reference_loader.get_reference_data()["benchmarks"]

    assert benchmarks["australia_data_status"] == "not_available_use_uk_eu_proxies"
