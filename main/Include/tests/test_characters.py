"""Tests for the bug fixes applied to characters.py and weapons.py."""

from __future__ import annotations

import dataclasses

import characters as ch
import pytest
from weapons import Weapon, daga, weapons


def test_weapon_is_immutable():
    """Bug #8: weapons are shared, so mutation must now raise."""
    with pytest.raises(dataclasses.FrozenInstanceError):
        daga.damage = 999


def test_weapon_coerces_damage_to_int():
    w = Weapon(name="Test", damage="7")
    assert w.damage == 7


def test_catch_weapon_by_object():
    hero = ch.Human("Hero")
    hero.catch_weapon(daga)
    assert hero.weapon is daga


def test_catch_weapon_by_valid_name():
    hero = ch.Human("Hero")
    hero.catch_weapon("Daga")
    assert hero.weapon is daga


def test_catch_weapon_unknown_name_raises_with_hint():
    """Bug #3: unknown weapon names now raise instead of silently None."""
    hero = ch.Human("Hero")
    with pytest.raises(ValueError) as exc:
        hero.catch_weapon("Dagg")
    assert "Did you mean 'Daga'?" in str(exc.value)


def test_catch_weapon_unknown_name_totally_off_raises():
    hero = ch.Human("Hero")
    with pytest.raises(ValueError):
        hero.catch_weapon("Zzzzzz")


def test_begin_turn_resets_defending():
    """Bug #1: defending must be cleared at the start of each turn."""
    hero = ch.Human("Hero")
    hero.defense()
    assert hero.defending is True
    hero.begin_turn()
    assert hero.defending is False


def test_guard_expires_after_next_turn_real_character():
    """End-to-end regression on real Character: guard does not linger."""
    hero = ch.Human("Hero")
    foe = ch.Human("Foe")
    foe.catch_weapon(daga)

    hero.defense()  # hero guards
    assert hero.defending is True

    # Enemy does NOT attack this round (e.g. it heals); guard would linger.
    foe.curar()

    hero.begin_turn()  # hero's next turn starts -> guard must be gone
    assert hero.defending is False

    # Now a full-damage hit lands (5 from daga, not the blocked 2).
    foe.catch_weapon(daga)
    dmg = foe.attack(hero)
    assert dmg == daga.damage


def test_attack_clears_target_defending():
    hero = ch.Human("Hero")
    foe = ch.Human("Foe")
    foe.catch_weapon(daga)
    hero.defense()
    foe.attack(hero)
    assert hero.defending is False


def test_character_creator_removed():
    """Dead-code cleanup: the broken Character_creator factory is gone."""
    assert not hasattr(ch, "Character_creator")


def test_destructor_x_removed():
    import declarations_characters as dc

    assert not hasattr(dc, "destructor_x")


def test_all_weapons_still_constructible():
    assert len(weapons) == 20
    assert all(isinstance(w, Weapon) for w in weapons)
