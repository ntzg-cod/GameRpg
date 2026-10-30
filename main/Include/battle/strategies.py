"""Enemy decision strategies (Strategy pattern, OCP/SRP).

``RandomDecisionStrategy`` reproduces the original behaviour of
``enemy_logic()``: pick one of the registered actions uniformly at
random. New strategies (aggressive, defensive, heal-when-low...) can be
added here and injected into the engine without touching it.
"""

from __future__ import annotations

import random

from .actions import Action
from .protocols import BattleContext


class RandomDecisionStrategy:
    """Pick a random registered action, optionally from an injected RNG."""

    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()

    def decide(self, context: BattleContext) -> str:
        action: Action = self._rng.choice(tuple(context.actions.values()))
        return action.code


__all__ = ["RandomDecisionStrategy"]
