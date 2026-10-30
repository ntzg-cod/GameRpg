"""Action commands and their registry (Command pattern, OCP).

Each ``Action`` bundles a code, a display label and the callable that
performs it. The engine only knows how to look up and apply an action;
it never switches on codes. Registering a new action extends the game
*without editing* the engine, the controller or the view.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import MappingProxyType

from .protocols import Combatant


@dataclass(frozen=True)
class Action:
    """An immutable, self-describing combat command."""

    code: str
    label: str
    apply: Callable[[Combatant, Combatant], None]


def _attack(actor: Combatant, target: Combatant) -> None:
    actor.attack(target)


def _defend(actor: Combatant, _target: Combatant) -> None:
    actor.defense()


def _curar(actor: Combatant, _target: Combatant) -> None:
    actor.curar()


ATTACK = Action(code="a", label="attack", apply=_attack)
DEFENSE = Action(code="d", label="defense", apply=_defend)
CURAR = Action(code="c", label="curar", apply=_curar)


def build_registry(actions: tuple[Action, ...]) -> Mapping[str, Action]:
    """Build an immutable code -> Action mapping from a sequence of actions."""
    return MappingProxyType({action.code: action for action in actions})


DEFAULT_ACTIONS: Mapping[str, Action] = build_registry((ATTACK, DEFENSE, CURAR))


__all__ = [
    "Action",
    "ATTACK",
    "DEFENSE",
    "CURAR",
    "DEFAULT_ACTIONS",
    "build_registry",
]
