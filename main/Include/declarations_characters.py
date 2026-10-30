import random

from characters import Androide, Delfo, Human
from weapons import (
    baston_magico,
    canon_de_plasma,
    daga,
    escopeta,
    espada_corta,
    espada_larga,
    granada,
    hacha_de_guerra,
    pistola,
    rifle_de_asalto,
    rifle_laser,
    subfusil,
    varita_electrica,
)

# Base enemy templates (stored as dicts for easy copying)
_HUMAN_TEMPLATES = [
    {
        "name": "Bandido",
        "hp": 80,
        "max_hp": 80,
        "force": 70,
        "speed": 150,
        "debilities": "Fire",
        "hax": "Intimidation",
        "level": 1,
        "weapon": daga,
        "porcent": 0.20,
    },
    {
        "name": "Mercenario",
        "hp": 100,
        "max_hp": 100,
        "force": 100,
        "speed": 170,
        "debilities": "Magic",
        "hax": "Tactics",
        "level": 3,
        "weapon": espada_corta,
        "porcent": 0.20,
    },
    {
        "name": "Caballero",
        "hp": 120,
        "max_hp": 120,
        "force": 140,
        "speed": 120,
        "debilities": "Lightning",
        "hax": "Armor",
        "level": 5,
        "weapon": espada_larga,
        "porcent": 0.20,
    },
    {
        "name": "Guerrero de guerra",
        "hp": 145,
        "max_hp": 145,
        "force": 170,
        "speed": 110,
        "debilities": "Poison",
        "hax": "Berserker",
        "level": 7,
        "weapon": hacha_de_guerra,
        "porcent": 0.20,
    },
    {
        "name": "General",
        "hp": 170,
        "max_hp": 170,
        "force": 200,
        "speed": 180,
        "debilities": "Darkness",
        "hax": "Command",
        "level": 10,
        "weapon": rifle_de_asalto,
        "porcent": 0.20,
    },
]

_ANDROIDE_TEMPLATES = [
    {
        "name": "Dron de combate",
        "hp": 120,
        "max_hp": 120,
        "force": 130,
        "speed": 180,
        "debilities": "EMP",
        "hax": "Target Lock",
        "level": 2,
        "weapon": pistola,
        "porcent": 0.15,
    },
    {
        "name": "Unidad T-800",
        "hp": 175,
        "max_hp": 175,
        "force": 200,
        "speed": 130,
        "debilities": "EMP",
        "hax": "Thermal Vision",
        "level": 4,
        "weapon": subfusil,
        "porcent": 0.15,
    },
    {
        "name": "Unidad pesada",
        "hp": 220,
        "max_hp": 220,
        "force": 260,
        "speed": 90,
        "debilities": "Electricity",
        "hax": "Armor Plating",
        "level": 6,
        "weapon": escopeta,
        "porcent": 0.15,
    },
    {
        "name": "Cazador mecanico",
        "hp": 250,
        "max_hp": 250,
        "force": 300,
        "speed": 210,
        "debilities": "EMP",
        "hax": "Tracking",
        "level": 8,
        "weapon": rifle_laser,
        "porcent": 0.15,
    },
    {
        "name": "Destructor X",
        "hp": 300,
        "max_hp": 300,
        "force": 400,
        "speed": 160,
        "debilities": "EMP",
        "hax": "Overcharge",
        "level": 12,
        "weapon": canon_de_plasma,
        "porcent": 0.15,
    },
]

_DELFO_TEMPLATES = [
    {
        "name": "Aprendiz Delfo",
        "hp": 90,
        "max_hp": 90,
        "force": 110,
        "speed": 180,
        "debilities": "Physical",
        "hax": "Minor Magic",
        "level": 2,
        "weapon": baston_magico,
        "porcent": 0.17,
    },
    {
        "name": "Hechicero",
        "hp": 125,
        "max_hp": 125,
        "force": 150,
        "speed": 200,
        "debilities": "Darkness",
        "hax": "Lightning",
        "level": 4,
        "weapon": varita_electrica,
        "porcent": 0.17,
    },
    {
        "name": "Guardian arcano",
        "hp": 150,
        "max_hp": 150,
        "force": 190,
        "speed": 160,
        "debilities": "Poison",
        "hax": "Arcane Shield",
        "level": 6,
        "weapon": baston_magico,
        "porcent": 0.17,
    },
    {
        "name": "Mago de batalla",
        "hp": 180,
        "max_hp": 180,
        "force": 240,
        "speed": 190,
        "debilities": "Physical",
        "hax": "Elemental Burst",
        "level": 9,
        "weapon": varita_electrica,
        "porcent": 0.17,
    },
    {
        "name": "Archimago",
        "hp": 220,
        "max_hp": 220,
        "force": 350,
        "speed": 220,
        "debilities": "Void",
        "hax": "Arcane Mastery",
        "level": 13,
        "weapon": granada,
        "porcent": 0.17,
    },
]

_TEMPLATES = {
    "human": (_HUMAN_TEMPLATES, Human),
    "androide": (_ANDROIDE_TEMPLATES, Androide),
    "delfo": (_DELFO_TEMPLATES, Delfo),
}


def create_enemy(enemy_type: str, level: int = None, name: str = None):
    """Create a fresh enemy instance with full HP.

    Args:
        enemy_type: "human", "androide", or "delfo"
        level: If specified, pick enemy with closest level. If None, random.
        name: If specified, pick enemy by name (exact match).

    Returns:
        Fresh Character instance.
    """
    enemy_type = enemy_type.lower()
    if enemy_type not in _TEMPLATES:
        raise ValueError(
            f"Unknown enemy type: {enemy_type}. Choose from: {list(_TEMPLATES.keys())}"
        )

    templates, cls = _TEMPLATES[enemy_type]

    if name:
        template = next(
            (t for t in templates if t["name"].lower() == name.lower()), None
        )
        if not template:
            raise ValueError(f"Enemy '{name}' not found in {enemy_type}")
    elif level is not None:
        # Pick closest level
        template = min(templates, key=lambda t: abs(t["level"] - level))
    else:
        template = random.choice(templates)

    # Create fresh instance
    kwargs = {k: v for k, v in template.items() if k != "weapon"}
    kwargs["weapon"] = template[
        "weapon"
    ]  # Weapon instances are immutable, safe to share
    return cls(**kwargs)


def get_available_enemies(enemy_type: str = None):
    """Get list of available enemy names/types for display."""
    if enemy_type:
        enemy_type = enemy_type.lower()
        if enemy_type not in _TEMPLATES:
            return []
        templates, _ = _TEMPLATES[enemy_type]
        return [(t["name"], t["level"]) for t in templates]

    result = {}
    for etype, (templates, _) in _TEMPLATES.items():
        result[etype] = [(t["name"], t["level"]) for t in templates]
    return result


__all__ = [
    "create_enemy",
    "get_available_enemies",
]
