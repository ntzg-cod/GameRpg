"""Backwards-compatible facade over the ``battle`` package.

``main.py`` (and any legacy caller) keeps using these four functions;
internally everything delegates to the decoupled, SOLID ``battle``
package. New code should import from ``battle`` directly.

- ``fight`` -> ``BattleEngine.with_defaults().run``
- ``interfaz`` -> ``ConsoleBattleView.show_status``
- ``enemy_logic`` -> ``RandomDecisionStrategy.decide``
- ``get_enemy_for_level`` -> ``CharacterFactory.create``
"""

from __future__ import annotations

from battle.actions import DEFAULT_ACTIONS
from battle.engine import BattleEngine
from battle.factory import CharacterFactory
from battle.protocols import BattleContext, Combatant
from battle.strategies import RandomDecisionStrategy
from battle.view import ConsoleBattleView

_factory = CharacterFactory()
_strategy = RandomDecisionStrategy()


def interfaz(player: Combatant, enemy: Combatant) -> None:
    """Print the current status of both combatants."""
    ConsoleBattleView().show_status(player, enemy)


def enemy_logic() -> str:
    """Return a random enemy action code ("a", "d" or "c")."""
    context = BattleContext(player=None, enemy=None, actions=DEFAULT_ACTIONS)
    return _strategy.decide(context)


def fight(player: Combatant, enemy: Combatant) -> None:
    """Run a turn-based fight between player and enemy."""
    BattleEngine.with_defaults().run(player, enemy)


def get_enemy_for_level(player_level: int, enemy_type: str = "human") -> Combatant:
    """Get a fresh enemy instance appropriate for player level."""
    return _factory.create(enemy_type, level=player_level)


__all__ = ["enemy_logic", "fight", "get_enemy_for_level", "interfaz"]
