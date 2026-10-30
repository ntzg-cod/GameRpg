"""Shared test fixtures and lightweight fakes for the battle tests.

The whole point of the SOLID refactor is that the engine depends on
abstractions, so these fakes (which are *not* ``Character`` instances)
can drive it end-to-end without touching stdin/stdout or sleeping.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make the game modules importable when running pytest from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from battle.actions import DEFAULT_ACTIONS, Action, build_registry
from battle.protocols import BattleContext


class FakeCombatant:
    """A stand-in for Character that records every call (LSP proof)."""

    def __init__(
        self, name: str = "Fake", hp: int = 50, damage: int = 10, max_hp: int | None = None
    ) -> None:
        self.name = name
        self.hp = hp
        self.max_hp = max_hp if max_hp is not None else max(hp, 100)
        self.defending = False
        self.damage = damage
        self.log: list[str] = []

    def attack(self, enemy: "FakeCombatant") -> int:
        dealt = self.damage // 2 if enemy.defending else self.damage
        enemy.hp = max(0, enemy.hp - dealt)
        enemy.defending = False
        self.log.append(f"{self.name}->attack:{dealt}")
        return dealt

    def defense(self) -> None:
        self.defending = True
        self.log.append(f"{self.name}->defense")

    def curar(self) -> None:
        self.hp = min(self.max_hp, self.hp + 5)
        self.log.append(f"{self.name}->curar")

    def begin_turn(self) -> None:
        self.defending = False


class ScriptedController:
    """PlayerController that replays a fixed queue of action codes."""

    def __init__(self, *codes: str) -> None:
        self._queue = list(codes)
        self.prompts: list[str] = []

    def choose_action(self, valid_codes) -> str:
        self.prompts.append("choose")
        return self._queue.pop(0)


class RecordingView:
    """BattleView that records calls instead of printing."""

    def __init__(self) -> None:
        self.status: list[tuple[str, str]] = []
        self.defeats: list[str] = []
        self.separators = 0

    def show_status(self, player, enemy) -> None:
        self.status.append((player.name, enemy.name))

    def show_defeat(self, combatant) -> None:
        self.defeats.append(combatant.name)

    def show_round_separator(self) -> None:
        self.separators += 1


class QueueStrategy:
    """DecisionStrategy that replays a fixed queue of action codes."""

    def __init__(self, *codes: str) -> None:
        self._queue = list(codes)
        self.contexts: list[BattleContext] = []

    def decide(self, context: BattleContext) -> str:
        self.contexts.append(context)
        return self._queue.pop(0)


def flee_action() -> Action:
    """A brand-new action used to prove the engine is open for extension."""

    def _flee(actor, _target) -> None:
        actor.log.append(f"{actor.name}->flee")

    return Action(code="r", label="run", apply=_flee)


ACTIONS_WITH_FLEE = build_registry(
    (*DEFAULT_ACTIONS.values(), flee_action())
)


__all__ = [
    "FakeCombatant",
    "ScriptedController",
    "RecordingView",
    "QueueStrategy",
    "ACTIONS_WITH_FLEE",
]
