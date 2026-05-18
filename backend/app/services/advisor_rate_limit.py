"""Epic 3 simple in-memory rate limiter for the advisor endpoint.

Why in-memory rather than Redis:
- Railway runs the FastAPI app as a single worker by default, so a per-process
  dict is consistent and avoids a hard dependency on Redis being reachable.
- Costs of a Redis trip are wasted for the typical use case (one user clicking
  buttons a few times per session).

If the deployment ever scales to multiple workers/replicas, swap this for a
Redis-backed sliding-window implementation; the public API of this module
will not need to change.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import Iterable

# 30 audit calls per IP per rolling hour. The cap exists to keep a runaway
# client (or accidental hot-reload loop) from draining the Claude token
# budget. Empty wardrobes still count, otherwise a script could probe the
# cache key space at high speed. The Re-answer button and per-recommendation
# follow-ups each consume a call too, so 10/hr was too tight for normal use.
_MAX_CALLS = 30
_WINDOW_SECONDS = 3600

_lock = threading.Lock()
_calls: dict[str, deque[float]] = {}


def check_and_record(client_ip: str) -> tuple[bool, int]:
    """Record a call and return (allowed, retry_after_seconds).

    `retry_after_seconds` is 0 when the call is allowed, otherwise the number
    of seconds until the oldest call in the window expires.
    """
    now = time.monotonic()
    cutoff = now - _WINDOW_SECONDS

    with _lock:
        bucket = _calls.setdefault(client_ip, deque())
        _evict_expired(bucket, cutoff)

        if len(bucket) >= _MAX_CALLS:
            retry_after = int(bucket[0] + _WINDOW_SECONDS - now) + 1
            return False, max(retry_after, 1)

        bucket.append(now)
        return True, 0


def _evict_expired(bucket: deque[float], cutoff: float) -> None:
    while bucket and bucket[0] < cutoff:
        bucket.popleft()


def reset_for_tests(ips: Iterable[str] | None = None) -> None:
    """Test helper: drop rate-limit state for a set of IPs (or everything)."""
    with _lock:
        if ips is None:
            _calls.clear()
        else:
            for ip in ips:
                _calls.pop(ip, None)
