"""Tests for the Epic 1 nearby-locations HTTP endpoints.

We mock `app.services.maps_service` directly so tests don't hit Google
Places or require a real API key. The mocks return shapes already verified
by maps_service's own internal contract — keeping these tests focused on
the API layer's contract: validation, error mapping, and pass-through.
"""

from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _sample_place(place_id: str = "abc123", distance_km: float = 1.2) -> dict:
    return {
        "place_id": place_id,
        "name": "Salvos Box Hill",
        "type": "second_hand_shop",
        "lat": -37.8195,
        "lng": 145.1230,
        "distance_km": distance_km,
    }


def _sample_details(place_id: str = "abc123") -> dict:
    return {
        "place_id": place_id,
        "name": "Salvos Box Hill",
        "address": "123 Whitehorse Rd, Box Hill VIC 3128",
        "opening_hours": ["Monday: 9:00 AM – 5:00 PM"],
        "phone": "+61 3 1234 5678",
        "website": "https://example.org",
        "type": "second_hand_shop",
    }


# ---------------------------------------------------------------------------
# /api/locations/nearby
# ---------------------------------------------------------------------------


def test_nearby_returns_places_sorted_by_distance():
    nearer = _sample_place(place_id="near", distance_km=0.4)
    farther = _sample_place(place_id="far", distance_km=2.7)

    async def _fake_fetch(**_kwargs):
        # maps_service is responsible for the sort — tests verify the API
        # forwards whatever order it gets without re-sorting.
        return [nearer, farther]

    with patch("app.api.epic1_locations.maps_service.fetch_nearby_places", side_effect=_fake_fetch):
        r = client.get("/api/locations/nearby", params={"lat": -37.8, "lng": 145.0})

    assert r.status_code == 200
    body = r.json()
    assert body["message"] is None
    assert [p["place_id"] for p in body["results"]] == ["near", "far"]


def test_nearby_empty_results_return_guidance_message():
    async def _fake_fetch(**_kwargs):
        return []

    with patch("app.api.epic1_locations.maps_service.fetch_nearby_places", side_effect=_fake_fetch):
        r = client.get("/api/locations/nearby", params={"lat": -37.8, "lng": 145.0})

    assert r.status_code == 200
    body = r.json()
    assert body["results"] == []
    assert "increasing the search radius" in body["message"].lower()


def test_nearby_rejects_out_of_range_latitude():
    r = client.get("/api/locations/nearby", params={"lat": 91.0, "lng": 145.0})
    assert r.status_code == 422


def test_nearby_rejects_radius_above_cap():
    r = client.get(
        "/api/locations/nearby",
        params={"lat": -37.8, "lng": 145.0, "radius_km": 75},
    )
    assert r.status_code == 422


def test_nearby_rejects_zero_radius():
    r = client.get(
        "/api/locations/nearby",
        params={"lat": -37.8, "lng": 145.0, "radius_km": 0},
    )
    assert r.status_code == 422


def test_nearby_upstream_timeout_returns_503():
    async def _timeout(**_kwargs):
        raise httpx.TimeoutException("simulated timeout")

    with patch("app.api.epic1_locations.maps_service.fetch_nearby_places", side_effect=_timeout):
        r = client.get("/api/locations/nearby", params={"lat": -37.8, "lng": 145.0})

    assert r.status_code == 503
    assert r.json()["detail"]["error"] == "upstream_timeout"


def test_nearby_upstream_runtime_error_returns_503():
    async def _runtime_err(**_kwargs):
        raise RuntimeError("OVER_QUERY_LIMIT")

    with patch("app.api.epic1_locations.maps_service.fetch_nearby_places", side_effect=_runtime_err):
        r = client.get("/api/locations/nearby", params={"lat": -37.8, "lng": 145.0})

    assert r.status_code == 503
    assert r.json()["detail"]["error"] == "upstream_error"


# ---------------------------------------------------------------------------
# /api/locations/details/{place_id}
# ---------------------------------------------------------------------------


def test_details_happy_path_returns_full_payload():
    async def _fake_details(*, place_id):
        return _sample_details(place_id=place_id)

    with patch("app.api.epic1_locations.maps_service.get_place_details", side_effect=_fake_details):
        r = client.get("/api/locations/details/abc123")

    assert r.status_code == 200
    body = r.json()
    assert body["place_id"] == "abc123"
    assert body["name"] == "Salvos Box Hill"
    assert body["opening_hours"] == ["Monday: 9:00 AM – 5:00 PM"]


def test_details_not_found_returns_404():
    async def _fake_details(*, place_id):
        raise RuntimeError("Google API status=NOT_FOUND")

    with patch("app.api.epic1_locations.maps_service.get_place_details", side_effect=_fake_details):
        r = client.get("/api/locations/details/missing_id")

    assert r.status_code == 404
    assert r.json()["detail"]["error"] == "place_not_found"


def test_details_invalid_request_returns_404():
    async def _fake_details(*, place_id):
        raise RuntimeError("Google API status=INVALID_REQUEST")

    with patch("app.api.epic1_locations.maps_service.get_place_details", side_effect=_fake_details):
        r = client.get("/api/locations/details/bad_id")

    assert r.status_code == 404


def test_details_timeout_returns_503():
    async def _timeout(*, place_id):
        raise httpx.TimeoutException("simulated timeout")

    with patch("app.api.epic1_locations.maps_service.get_place_details", side_effect=_timeout):
        r = client.get("/api/locations/details/abc123")

    assert r.status_code == 503
    assert r.json()["detail"]["error"] == "upstream_timeout"


def test_details_generic_runtime_error_returns_503():
    async def _runtime_err(*, place_id):
        raise RuntimeError("REQUEST_DENIED")

    with patch("app.api.epic1_locations.maps_service.get_place_details", side_effect=_runtime_err):
        r = client.get("/api/locations/details/abc123")

    assert r.status_code == 503
    assert r.json()["detail"]["error"] == "upstream_error"


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------


def test_health_endpoint_returns_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
