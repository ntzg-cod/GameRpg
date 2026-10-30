"""Structural interfaces for the battle engine (ISP + DIP).

These ``Protocol`` classes define the *abstractions* the engine depends on.
Any object that provides the right methods/attributes satisfies them
(duck typing), so the engine never needs to import the concrete
``Character`` class and can be tested with lightweight fakes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Mapping, Protocol, runtime_checkable

if TYPE_CHECKING:  # pragma: no cover - typing only
    from .actions import Action


@runtime_checkable
class Combatant(Protocol):
    """Minimal surface the engine needs from a player or enemy."""

    name: str
    hp: int

    def attack(self, enemy: "Combatant") -> int: ...

    def defense(self) -> None: ...

    def curar(self) -> None: ...

    def begin_turn(self) -> None: ...


@runtime_checkable
class BattleView(Protocol):
    """Output abstraction (SRP): the engine never calls ``print`` directly."""

    def show_status(self, player: Combatant, enemy: Combatant) -> None: ...

    def show_defeat(self, combatant: Combatant) -> None: ...

    def show_round_separator(self) -> None: ...


@runtime_checkable
class PlayerController(Protocol):
    """Input abstraction (DIP): obtains the player's chosen action code."""

    def choose_action(self, valid_codes: Mapping[str, "Action"]) -> str: ...


@runtime_checkable
class DecisionStrategy(Protocol):
    """Strategy abstraction (OCP): decides the enemy's action code."""

    def decide(self, context: "BattleContext") -> str: ...


@runtime_checkable
class Clock(Protocol):
    """Time abstraction (DIP): lets tests run without real delays."""

    def sleep(self, seconds: float) -> None: ...


@runtime_checkable
class EnemyFactory(Protocol):
    """Creation abstraction (DIP): the engine/facade never import factories."""

    def create(self, enemy_type: str, level: int | None = None) -> Combatant: ...


@dataclass(frozen=True)
class BattleContext:
    """Immutable snapshot of the battle handed to a ``DecisionStrategy``."""

    player: Combatant | None
    enemy: Combatant | None
    actions: Mapping[str, "Action"]


__all__ = [
    "BattleContext",
    "BattleView",
    "Clock",
    "Combatant",
    "DecisionStrategy",
    "EnemyFactory",
    "PlayerController",
]
