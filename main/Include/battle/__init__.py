"""Decoupled, SOLID battle engine for the game.

Public API:

- ``BattleEngine``: the game loop (inject view/controller/strategy/clock).
- ``Action`` + ``DEFAULT_ACTIONS``: Command-pattern action registry.
- ``RandomDecisionStrategy``: default enemy AI (Strategy pattern).
- ``ConsolePlayerController`` / ``ConsoleBattleView``: console adapters.
- ``CharacterFactory``: enemy creation behind the ``EnemyFactory`` protocol.
- ``battle.protocols``: the abstractions everything depends on.
"""

from .actions import ATTACK, CURAR, DEFENSE, DEFAULT_ACTIONS, Action, build_registry
from .clock import FakeClock, RealClock
from .controllers import ConsolePlayerController
from .engine import BattleEngine
from .factory import CharacterFactory
from .protocols import (
    BattleContext,
    BattleView,
    Clock,
    Combatant,
    DecisionStrategy,
    EnemyFactory,
    PlayerController,
)
from .strategies import RandomDecisionStrategy
from .view import ConsoleBattleView

__all__ = [
    "Action",
    "ATTACK",
    "DEFENSE",
    "CURAR",
    "DEFAULT_ACTIONS",
    "build_registry",
    "BattleEngine",
    "BattleContext",
    "BattleView",
    "Clock",
    "Combatant",
    "DecisionStrategy",
    "EnemyFactory",
    "PlayerController",
    "CharacterFactory",
    "RandomDecisionStrategy",
    "ConsolePlayerController",
    "ConsoleBattleView",
    "RealClock",
    "FakeClock",
]
