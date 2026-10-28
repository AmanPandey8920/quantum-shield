from __future__ import annotations

import secrets
import time
from collections import defaultdict
from typing import DefaultDict


class RateLimiter:
    def __init__(self, limit_per_minute: int = 60, window_seconds: int = 60) -> None:
        self.limit_per_minute = limit_per_minute
        self.window_seconds = window_seconds
        self._requests: DefaultDict[str, list[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        timestamps = self._requests[key]
        timestamps[:] = [ts for ts in timestamps if ts > window_start]

        if len(timestamps) >= self.limit_per_minute:
            return False

        timestamps.append(now)
        return True


def generate_device_token() -> str:
    return secrets.token_urlsafe(24)
