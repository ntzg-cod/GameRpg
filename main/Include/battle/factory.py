"""Enemy creation behind an abstraction (DIP).

The facade and any future code depend on the ``EnemyFactory`` protocol,
not on ``declarations_characters`` directly, so the concrete template
source can be swapped without ripple changes.
"""

from __future__ import annotations

import declarations_characters as dc

from .protocols import Combatant


class CharacterFactory:
    """Produce fresh enemies via the legacy template module."""

    def create(self, enemy_type: str, level: int | None = None) -> Combatant:
        return dc.create_enemy(enemy_type, level=level)


__all__ = ["CharacterFactory"]
