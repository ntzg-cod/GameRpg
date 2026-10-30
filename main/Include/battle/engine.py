"""The battle game loop (SRP/DIP/LSP).

``BattleEngine`` orchestrates a round-based fight. It depends only on
abstractions (``BattleView``, ``PlayerController``, ``DecisionStrategy``,
``Clock``) injected through the constructor, so it never touches
``input``, ``print``, ``random`` or ``time`` directly and can be driven
end-to-end by fakes in tests.

The default factory method ``with_defaults()`` wires the console game
exactly like the original ``fight()`` in ``logica.py``.
"""

from __future__ import annotations

from collections.abc import Mapping

from .actions import DEFAULT_ACTIONS, Action
from .clock import RealClock
from .controllers import ConsolePlayerController
from .protocols import BattleContext, BattleView, Clock, Combatant, DecisionStrategy, PlayerController
from .strategies import RandomDecisionStrategy
from .view import ConsoleBattleView

_ROUND_SECONDS = 1


class BattleEngine:
    """Run a fight between two combatants using injected collaborators."""

    def __init__(
        self,
        view: BattleView,
        player_controller: PlayerController,
        enemy_strategy: DecisionStrategy,
        actions: Mapping[str, Action] | None = None,
        clock: Clock | None = None,
    ) -> None:
        self._view = view
        self._player_controller = player_controller
        self._enemy_strategy = enemy_strategy
        self._actions = actions or DEFAULT_ACTIONS
        self._clock = clock or RealClock()

    @classmethod
    def with_defaults(cls) -> "BattleEngine":
        """Engine wired for the interactive console game."""
        return cls(
            view=ConsoleBattleView(),
            player_controller=ConsolePlayerController(),
            enemy_strategy=RandomDecisionStrategy(),
        )

    def run(self, player: Combatant, enemy: Combatant) -> None:
        """Fight until one combatant's HP reaches zero."""
        while player.hp > 0 and enemy.hp > 0:
            # A guard only lasts until the holder's next turn.
            player.begin_turn()
            enemy.begin_turn()

            self._view.show_status(player, enemy)

            player_choice = self._player_controller.choose_action(self._actions)
            enemy_context = BattleContext(
                player=player, enemy=enemy, actions=self._actions
            )
            enemy_choice = self._enemy_strategy.decide(enemy_context)

            self._apply(player_choice, player, enemy)

            if enemy.hp <= 0:
                self._view.show_defeat(enemy)
                break

            self._apply(enemy_choice, enemy, player)

            if player.hp <= 0:
                self._view.show_defeat(player)
                break

            self._clock.sleep(_ROUND_SECONDS)
            self._view.show_round_separator()

    def _apply(self, code: str, actor: Combatant, target: Combatant) -> None:
        self._actions[code].apply(actor, target)


__all__ = ["BattleEngine"]
