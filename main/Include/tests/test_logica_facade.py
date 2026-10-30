"""Tests proving the logica.py facade stays backwards compatible (main.py)."""

from __future__ import annotations

import characters as ch
from logica import enemy_logic, get_enemy_for_level, interfaz
from weapons import escopeta, espada_larga


def test_get_enemy_for_level_returns_fresh_full_hp_enemy():
    enemy = get_enemy_for_level(3, "human")
    assert enemy.hp == enemy.max_hp
    assert enemy.level >= 1


def test_get_enemy_for_level_accepts_each_faction():
    for faction in ("human", "androide", "delfo"):
        enemy = get_enemy_for_level(1, faction)
        assert enemy.hp == enemy.max_hp


def test_get_enemy_for_level_unknown_type_raises():
    import pytest

    with pytest.raises(ValueError):
        get_enemy_for_level(1, "dragon")


def test_enemy_logic_returns_valid_code():
    codes = {enemy_logic() for _ in range(50)}
    assert codes <= {"a", "d", "c"}


def test_interfaz_prints_exact_format(capsys):
    player = ch.Human("Hero")
    player.catch_weapon(espada_larga)
    enemy = get_enemy_for_level(1, "human")
    interfaz(player, enemy)

    out = capsys.readouterr().out.splitlines()
    assert out[0] == f"Name : Hero  HP : {player.hp} Weapon : Espada larga"
    assert out[1] == "-" * 30
    assert out[2] == (
        f"Name : {enemy.name}  HP : {enemy.hp} Weapon : {enemy.weapon.name}"
    )


def test_main_module_uses_facade_only():
    """main.py imports fight + get_enemy_for_level from logica (the facade).

    We read main.py as text instead of importing it, because importing
    ``main`` would execute the whole game (top-level input()/sleep()).
    """
    from pathlib import Path

    source = (Path(__file__).resolve().parents[1] / "main.py").read_text(
        encoding="utf-8"
    )
    assert "from logica import" in source
    assert "import battle" not in source  # main depends on the facade, not the package


def test_escopeta_damage_preserved():
    assert escopeta.name == "Escopeta"
    assert escopeta.damage == 35
