"""Console rendering for battles (SRP/DIP).

The engine depends on the ``BattleView`` abstraction; this module is the
console implementation. It reproduces the exact formatting of the
original ``interfaz()`` helper.
"""

from __future__ import annotations

from .protocols import Combatant


class ConsoleBattleView:
    """Render battle state to stdout."""

    def show_status(self, player: Combatant, enemy: Combatant) -> None:
        print(
            f"Name : {player.name}  HP : {player.hp} "
            f"Weapon : {player.weapon.name}"
        )
        print("-" * 30)
        print(
            f"Name : {enemy.name}  HP : {enemy.hp} "
            f"Weapon : {enemy.weapon.name}"
        )

    def show_defeat(self, combatant: Combatant) -> None:
        print(f"{combatant.name} has been defeated!")

    def show_round_separator(self) -> None:
        print("\n" + "=" * 40 + "\n")


__all__ = ["ConsoleBattleView"]
