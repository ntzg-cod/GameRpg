"""Time abstraction (SRP/DIP).

``RealClock`` wraps ``time.sleep`` for production; ``FakeClock`` lets
tests run instantly and assert on the delays the engine requested.
"""

from __future__ import annotations

import time


class RealClock:
    """Sleep for real, like the original game loop."""

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)


class FakeClock:
    """Record requested delays instead of sleeping (for tests)."""

    def __init__(self) -> None:
        self.sleeps: list[float] = []

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)


__all__ = ["RealClock", "FakeClock"]
