"""Optional Redis-backed cache for the wardrobe sustainability advisor.

The same wardrobe + preset combination always produces the same advice (since
both the audit calculation and the LLM call are deterministic for a fixed
prompt), so memoising the response saves both Claude tokens and latency on
repeat clicks. Redis is optional — if it is unreachable the service silently
degrades to no-cache, mirroring how `maps_service` handles its place-details
cache.
"""

from __future__ import annotations

import hashlib
import json
import logging
from collections import Counter
from collections.abc import Iterable

import redis.asyncio as aioredis

from app.core.config import settings
from app.schemas.advisor import Advice, PresetKey
from app.schemas.wardrobe_audit import GarmentInput

logger = logging.getLogger(__name__)

_CACHE_KEY_PREFIX = "wardrobe_advice"

# Module-level Redis handle injected by the FastAPI lifespan hook.
_redis_client: aioredis.Redis | None = None


def set_redis_client(client: aioredis.Redis | None) -> None:
    """Wire the connected Redis client in from main.lifespan."""
    global _redis_client
    _redis_client = client


def make_cache_key(garments: Iterable[GarmentInput], preset: PresetKey) -> str:
    """Build a deterministic cache key from sorted (sub_category, count) pairs.

    Item order in the request must not affect the key, so we count occurrences
    and sort. The preset is part of the key because the same wardrobe yields
    different advice for different preset questions.

    Materials matter too: the same t-shirt with no wash-label info should
    produce different advice once the user uploads a label. We fold a sorted
    summary of (sub_category, fibre_key, percent) tuples into the key so that
    uploading a label invalidates only the affected cache entries.
    """
    garments_list = list(garments)
    counts = sorted(Counter(g.sub_category for g in garments_list).items())

    materials_signature: list[tuple] = []
    for g in garments_list:
        if not g.materials:
            continue
        rolled = sorted(
            (m.key, round(float(m.percent), 1)) for m in g.materials if m.percent
        )
        if rolled:
            materials_signature.append((g.sub_category, tuple(rolled)))
    materials_signature.sort()

    payload = json.dumps(
        {"counts": counts, "preset": preset, "materials": materials_signature},
        sort_keys=True,
        default=list,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"{_CACHE_KEY_PREFIX}:{digest}"


async def get_cached_advice(key: str) -> Advice | None:
    """Return cached advice or None on miss / Redis failure."""
    if _redis_client is None:
        return None
    try:
        raw = await _redis_client.get(key)
    except Exception as exc:  # network glitch, auth error, etc.
        logger.warning("Advisor cache GET failed: %s", exc)
        return None
    if raw is None:
        return None
    try:
        return Advice.model_validate_json(raw)
    except Exception as exc:  # corrupted entry from a prior schema version
        logger.warning("Advisor cache decode failed: %s", exc)
        return None


async def set_cached_advice(key: str, advice: Advice) -> None:
    """Persist advice with the configured TTL. Failures are non-fatal."""
    if _redis_client is None:
        return
    try:
        await _redis_client.set(
            key,
            advice.model_dump_json(),
            ex=settings.wardrobe_audit_cache_ttl,
        )
    except Exception as exc:
        logger.warning("Advisor cache SET failed: %s", exc)
