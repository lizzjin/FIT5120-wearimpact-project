"""Epic 3 wardrobe advisor API.

Three endpoints power the front-end advisor experience:

- GET  /api/wardrobe/preset-questions
    Returns the fixed set of preset prompts the user can click. Free-form
    chat is intentionally not offered because constraining the question
    constrains the answer (no styling tips, no AU benchmarks, no fabrications).

- POST /api/wardrobe/audit
    Takes the user's wardrobe contents + chosen preset, runs the deterministic
    audit, then asks Claude to translate the numbers into structured advice.
    Identical (wardrobe, preset) requests return cached advice for up to the
    configured TTL; clients can force a refresh via `?refresh=1`.

- POST /api/wardrobe/advice/follow-up
    A drill-down on a previous answer. Skips the cache (every follow-up is
    fresh) but reuses the same audit + rate limit.

This router stays thin — all heavy lifting lives in the audit, advisor, and
cache services.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

from app.schemas.advisor import (
    Advice,
    FollowUpAdvice,
    PresetKey,
    PresetQuestion,
    list_preset_questions,
)
from app.schemas.wardrobe_audit import AuditRequest, GarmentInput
from app.services import advisor_cache, advisor_rate_limit, llm_advisor_service
from app.services.llm_advisor_service import AdvisorUpstreamError
from app.services.wardrobe_audit_service import compute_audit

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/wardrobe", tags=["Epic 3 — Advisor"])


# Epic 3 Step 1:
# Expose the catalogue of preset questions. Frontend renders these as buttons
# instead of a free-text box.
@router.get("/preset-questions", response_model=list[PresetQuestion])
async def get_preset_questions() -> list[PresetQuestion]:
    """Return the fixed list of preset questions in display order."""
    return list_preset_questions()


# Epic 3 Step 2:
# Run audit + LLM advisor for a given wardrobe and preset, with Redis caching.
@router.post("/audit", response_model=Advice)
async def post_wardrobe_audit(
    payload: AuditRequest,
    request: Request,
    refresh: bool = Query(
        False,
        description="If true, bypass the cache and call Claude again.",
    ),
) -> Advice:
    """Compute audit facts and return structured sustainability advice.

    Cache-first by default: identical (wardrobe contents, preset) return
    memoised advice so users can re-click without burning tokens. Pass
    `?refresh=1` to force a new generation (powers the UI's Re-answer button).

    Cache hits do NOT count against the rate limit — only cache misses (real
    Claude calls) and forced refreshes do. This lets a user click "Re-answer
    this" or revisit the page without immediately tripping the cap, while
    still protecting the token budget from runaway misses.
    """
    cache_key = advisor_cache.make_cache_key(payload.garments, payload.preset)

    if not refresh:
        cached = await advisor_cache.get_cached_advice(cache_key)
        if cached is not None:
            client_ip = request.client.host if request.client else "unknown"
            logger.info("advisor cache HIT %s (ip=%s)", cache_key, client_ip)
            return cached

    client_ip = _enforce_rate_limit(request)
    audit = compute_audit(payload.garments)

    try:
        advice = llm_advisor_service.generate_advice(audit, payload.preset)
    except AdvisorUpstreamError as exc:
        logger.error("Advisor upstream failure: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="The AI advisor is temporarily unavailable. Please try again shortly.",
        ) from exc

    await advisor_cache.set_cached_advice(cache_key, advice)
    logger.info(
        "advisor cache %s, stored %s (ip=%s)",
        "REFRESH" if refresh else "MISS",
        cache_key,
        client_ip,
    )
    return advice


# Epic 3 Step 3:
# Drill-down endpoint. Each call is fresh — no caching — but rate-limited the
# same way so a runaway client cannot drain the token budget.
class FollowUpRequest(BaseModel):
    """Payload for the follow-up endpoint.

    `focus` is the slug of the recommendation the user tapped, or an empty
    string when the user picked a top-level next_question instead. The full
    wardrobe is re-sent (rather than referencing a cache key) so this endpoint
    stays stateless — matches how the audit endpoint already works.
    """

    garments: list[GarmentInput] = Field(max_length=100)
    parent_preset: PresetKey
    focus: str = Field(default="", max_length=40)
    sub_prompt: str = Field(min_length=1, max_length=200)


@router.post("/advice/follow-up", response_model=FollowUpAdvice)
async def post_advice_follow_up(
    payload: FollowUpRequest,
    request: Request,
) -> FollowUpAdvice:
    """Return a compact drill-down answer for a previous advice."""
    _enforce_rate_limit(request)
    audit = compute_audit(payload.garments)

    try:
        return llm_advisor_service.generate_follow_up(
            audit,
            payload.parent_preset,
            payload.focus,
            payload.sub_prompt,
        )
    except AdvisorUpstreamError as exc:
        logger.error("Advisor follow-up upstream failure: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="The AI advisor is temporarily unavailable. Please try again shortly.",
        ) from exc


def _enforce_rate_limit(request: Request) -> str:
    """Shared per-IP rate-limit gate; raises 429 when exceeded.

    Returns the client IP so the caller can log it alongside cache events.
    """
    client_ip = request.client.host if request.client else "unknown"
    allowed, retry_after = advisor_rate_limit.check_and_record(client_ip)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Advisor rate limit reached. Please retry later.",
            headers={"Retry-After": str(retry_after)},
        )
    return client_ip
