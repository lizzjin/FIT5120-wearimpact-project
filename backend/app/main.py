"""WearImpact FastAPI application entry point.

Initialises the app, configures CORS, connects to Redis on startup,
and registers Epic 1 routers.
"""

import logging
import os
from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import epic1_locations, epic3_advisor, epic4_brands
from app.core.config import settings
from app.services import advisor_cache, maps_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage Redis connection across the application lifecycle.

    Opens a connection pool on startup and closes it cleanly on shutdown
    to avoid leaked connections.
    """
    logger.info("Connecting to Redis at %s", settings.redis_url)
    redis_client: aioredis.Redis | None = None
    try:
        redis_client = aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
        # Verify the connection is reachable before accepting traffic
        await redis_client.ping()
        maps_service.set_redis_client(redis_client)
        advisor_cache.set_redis_client(redis_client)
        logger.info("Redis connection established")
    except Exception as exc:
        logger.warning(
            "Redis unavailable (%s) — place details and advisor caching are disabled",
            exc,
        )
        # App continues without cache; details and advisor endpoints work uncached

    yield  # Application runs here

    if redis_client is not None:
        await redis_client.aclose()
        logger.info("Redis connection closed")


app = FastAPI(
    title="WearImpact API",
    description="Backend for WearImpact — Epic 1: Local Eco-Shop Navigator",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS policy is gated by the CORS_STRICT env var so production behaviour
# remains identical to the open-CORS default until the operator opts in.
# Set CORS_STRICT=1 in Railway env after populating CORS_ORIGINS with the
# real Vercel preview + prod URLs; unset it to roll back instantly.
_cors_strict = os.getenv("CORS_STRICT") == "1"
_cors_allow_origins = settings.cors_origins if _cors_strict else ["*"]

if _cors_strict:
    logger.info("CORS strict mode ON — allow_origins=%s", _cors_allow_origins)
else:
    logger.info("CORS strict mode OFF — allow_origins=['*'] (legacy default)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_allow_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(epic1_locations.router)
app.include_router(epic3_advisor.router)
app.include_router(epic4_brands.router)


@app.get("/health")
async def health_check() -> dict:
    """Simple liveness probe for deployment health checks."""
    return {"status": "ok"}
