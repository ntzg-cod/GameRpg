"""Tests for the enemy decision Strategy (SRP/OCP)."""

from __future__ import annotations

import random

from battle.actions import DEFAULT_ACTIONS
from battle.protocols import BattleContext
from battle.strategies import RandomDecisionStrategy
from conftest import FakeCombatant


def _context() -> BattleContext:
    return BattleContext(
        player=FakeCombatant("Hero"), enemy=FakeCombatant("Foe"), actions=DEFAULT_ACTIONS
    )


def test_decide_returns_a_registered_code():
    strategy = RandomDecisionStrategy(rng=random.Random(0))
    assert strategy.decide(_context()) in DEFAULT_ACTIONS


def test_seeded_rng_is_deterministic():
    first = RandomDecisionStrategy(rng=random.Random(7))
    second = RandomDecisionStrategy(rng=random.Random(7))
    codes_a = [first.decide(_context()) for _ in range(10)]
    codes_b = [second.decide(_context()) for _ in range(10)]
    assert codes_a == codes_b


def test_strategy_uses_only_given_actions():
    from battle.actions import build_registry
    from battle.actions import ATTACK

    only_attack = build_registry((ATTACK,))
    context = BattleContext(
        player=FakeCombatant("Hero"), enemy=FakeCombatant("Foe"), actions=only_attack
    )
    strategy = RandomDecisionStrategy(rng=random.Random(3))
    assert strategy.decide(context) == "a"
