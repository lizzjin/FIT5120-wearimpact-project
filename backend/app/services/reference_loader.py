"""Epic 3 reference data loader.

Loads the static `reference_data.json` file once at process start and exposes
typed accessors used by the wardrobe audit service. The file aggregates
per-garment LCA figures (IMPRO 2014), behavioural intervention reductions
(WRAP 2017), and global industry benchmarks (Quantis 2018) so the LLM advisor
never has to invent numbers.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path
from typing import Any

# reference_data.json sits beside this services/ folder, under app/data/
_REFERENCE_PATH = Path(__file__).resolve().parent.parent / "data" / "reference_data.json"


@lru_cache(maxsize=1)
def _load_reference_data() -> dict[str, Any]:
    """Read reference_data.json once and cache it for the process lifetime."""
    if not _REFERENCE_PATH.exists():
        raise FileNotFoundError(
            f"Reference data file not found at {_REFERENCE_PATH}. "
            "Ensure backend/app/data/reference_data.json is present."
        )
    with _REFERENCE_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def get_reference_data() -> dict[str, Any]:
    """Return the full reference dataset (sources, garments, interventions, ...)."""
    return _load_reference_data()


def get_garment_impact(subcategory: str) -> dict[str, Any] | None:
    """Look up per-garment LCA figures by subcategory key (e.g. "t_shirt").

    The model classifier emits ~34 fine-grained subcategories; per_garment only
    carries 15 representative entries. When a direct lookup misses we consult
    the alias map so e.g. "sports_shorts" resolves to the "shorts" record.
    Returns None only when even the alias chain produces no match — the audit
    then drops the item and surfaces it via coverage.unmatched_subcategories.
    """
    data = _load_reference_data()
    garments = data.get("per_garment", {})

    direct = garments.get(subcategory)
    if direct is not None:
        return direct

    aliases = data.get("subcategory_aliases", {})
    target = aliases.get(subcategory)
    if target and target in garments:
        return garments[target]

    return None


def get_fibre_impact(fibre: str) -> dict[str, Any] | None:
    """Look up per-kg-fabric LCA figures by fibre name (e.g. "cotton")."""
    fibres = _load_reference_data().get("per_fibre_per_kg_fabric", {})
    return fibres.get(fibre)


def get_intervention(key: str) -> dict[str, Any] | None:
    """Return a single behavioural intervention by key."""
    interventions = _load_reference_data().get("interventions", {})
    return interventions.get(key)


def get_interventions_for(subcategories: Iterable[str]) -> list[dict[str, Any]]:
    """Pick interventions worth surfacing given the user's wardrobe contents.

    The current heuristic is intentionally simple: always-applicable behaviours
    (extend lifetime, second-hand purchase) come back for any non-empty wardrobe;
    use-phase tips (cold wash, line drying) come back when the wardrobe contains
    any washable garment. The LLM still chooses which 2-4 to surface to the user.
    """
    subcategory_set = {s for s in subcategories if s}
    if not subcategory_set:
        return []

    reference = _load_reference_data()
    data = reference.get("interventions", {})
    garments = reference.get("per_garment", {})

    selected_keys: list[str] = [
        "extend_lifetime_2x",
        "buy_second_hand",
        "donate_dont_landfill",
        "switch_to_recycled_fibre",
    ]

    # Use-phase tips only matter when the user owns washable apparel — footwear
    # alone wouldn't justify recommending a 30 degC wash cycle. Resolve each
    # subcategory's category via the reference data so unknown subcategories
    # don't accidentally trigger laundry tips.
    has_apparel = any(
        garments.get(sub, {}).get("category") in {"upper_body", "lower_body"}
        for sub in subcategory_set
    )
    if has_apparel:
        selected_keys.extend(["wash_cold_30c", "full_load_washing", "line_dry_no_tumble"])

    return [
        {"key": key, **data[key]}
        for key in selected_keys
        if key in data
    ]


def get_benchmark(key: str) -> dict[str, Any] | None:
    """Return a single benchmark entry (e.g. EU per-capita CO2)."""
    benchmarks = _load_reference_data().get("benchmarks", {})
    return benchmarks.get(key)


def get_equivalences() -> dict[str, Any]:
    """Return the kg-CO2 -> intuitive-comparison conversion factors."""
    return _load_reference_data().get("equivalences", {})


def get_sources() -> list[dict[str, Any]]:
    """Return the source citation list for display in the UI."""
    return _load_reference_data().get("sources", [])
