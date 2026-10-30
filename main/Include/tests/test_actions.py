"""Tests for the Command-pattern action registry (OCP/SRP)."""

from __future__ import annotations

import pytest

from battle.actions import ATTACK, CURAR, DEFENSE, DEFAULT_ACTIONS, build_registry
from conftest import ACTIONS_WITH_FLEE, FakeCombatant


def test_default_registry_exposes_original_codes():
    assert set(DEFAULT_ACTIONS) == {"a", "d", "c"}


def test_registry_is_immutable():
    with pytest.raises(TypeError):
        DEFAULT_ACTIONS["x"] = ATTACK


def test_build_registry_maps_codes_to_actions():
    registry = build_registry((ATTACK, DEFENSE))
    assert registry == {"a": ATTACK, "d": DEFENSE}


def test_attack_action_hits_target():
    actor, target = FakeCombatant("A"), FakeCombatant("B", hp=30)
    DEFAULT_ACTIONS["a"].apply(actor, target)
    assert target.hp == 20


def test_defense_action_defends_actor_only():
    actor, target = FakeCombatant("A"), FakeCombatant("B")
    DEFAULT_ACTIONS["d"].apply(actor, target)
    assert actor.defending is True
    assert target.defending is False


def test_curar_action_heals_actor():
    actor = FakeCombatant("A", hp=10)
    DEFAULT_ACTIONS["c"].apply(actor, FakeCombatant("B"))
    assert actor.hp == 15


def test_new_action_extends_game_without_touching_engine():
    """OCP: a brand-new action plugs into the registry, no engine edit."""
    registry = ACTIONS_WITH_FLEE
    assert "r" in registry
    actor = FakeCombatant("A")
    registry["r"].apply(actor, FakeCombatant("B"))
    assert "A->flee" in actor.log
