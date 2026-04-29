"""Epic 3 wardrobe advisor API.

Two endpoints power the front-end advisor experience:

- GET  /api/wardrobe/preset-questions
    Returns the fixed set of preset prompts the user can click. Free-form
    chat is intentionally not offered because constraining the question
    constrains the answer (no styling tips, no AU benchmarks, no fabrications).

- POST /api/wardrobe/audit
    Takes the user's wardrobe contents + chosen preset, runs the deterministic
    audit, then asks Claude to translate the numbers into structured advice.
    Identical (wardrobe, preset) requests return cached advice for 24 h.

This router stays thin — all heavy lifting lives in the audit, advisor, and
cache services.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Request

from app.schemas.advisor import (
    Advice,
    PresetQuestion,
    list_preset_questions,
)
from app.schemas.wardrobe_audit import AuditRequest
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
async def post_wardrobe_audit(payload: AuditRequest, request: Request) -> Advice:
    """Compute audit facts and return structured sustainability advice.

    Cache-first: identical (wardrobe contents, preset) return memoised advice
    so users can re-click without burning tokens.
    """
    # Per-IP rate limit (10 calls / hour) — protects token spend from runaway
    # clients. Cached responses still count so a script cannot probe the
    # cache space at high speed.
    client_ip = request.client.host if request.client else "unknown"
    allowed, retry_after = advisor_rate_limit.check_and_record(client_ip)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Advisor rate limit reached. Please retry later.",
            headers={"Retry-After": str(retry_after)},
        )

    cache_key = advisor_cache.make_cache_key(payload.garments, payload.preset)

    cached = await advisor_cache.get_cached_advice(cache_key)
    if cached is not None:
        logger.info("advisor cache HIT %s", cache_key)
        return cached

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
    logger.info("advisor cache MISS, stored %s", cache_key)
    return advice
