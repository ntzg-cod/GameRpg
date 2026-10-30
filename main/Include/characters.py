import difflib
from abc import ABC

from weapons import weapons


class Character(ABC):
    def __init__(
        self,
        name,
        hp,
        max_hp,
        force,
        speed,
        debilities,
        hax,
        level,
        weapon,
        defending,
        porcent,
    ):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.force = force
        self.speed = speed
        self.debilities = debilities
        self.hax = hax
        self.level = level
        self.weapon = weapon
        self.defending = bool(defending)
        self.porcent = porcent

    def catch_weapon(self, weapon_equipped):
        if isinstance(weapon_equipped, str):
            match = next(
                (w for w in weapons if w.name == weapon_equipped), None
            )
            if match is None:
                names = [w.name for w in weapons]
                close = difflib.get_close_matches(weapon_equipped, names, n=1)
                hint = f" Did you mean '{close[0]}'?" if close else ""
                raise ValueError(
                    f"Unknown weapon '{weapon_equipped}'.{hint} "
                    f"Available: {', '.join(names)}"
                )
            self.weapon = match
        else:
            self.weapon = weapon_equipped

    def begin_turn(self):
        """Reset per-turn state; a guard only lasts until this character's next turn."""
        self.defending = False

    def attack(self, enemy):
        if self.weapon is not None:
            if enemy.defending:
                damage = int(self.weapon.damage * 0.50)
                enemy.hp = max(0, enemy.hp - damage)
                enemy.defending = False
                print(
                    f"{self.name} attacked {enemy.name} for {damage} damage (blocked)"
                )
                return damage
            else:
                damage = int(self.weapon.damage)
                enemy.hp = max(0, enemy.hp - damage)
                print(f"{self.name} attacked {enemy.name} for {damage} damage")
                return damage
        else:
            print(f"{self.name} has no weapon!")
            return 0

    def curar(self):
        if self.hp < self.max_hp:
            heal_amount = int(self.max_hp * self.porcent)
            self.hp = min(self.max_hp, self.hp + heal_amount)
            print(f"{self.name} healed for {heal_amount} HP. Current HP: {self.hp}")
        else:
            print(f"{self.name} is at full HP!")

    def defense(self):
        self.defending = True
        print(f"{self.name} is defending!")

    def __str__(self) -> str:
        return f"==============================\n Name : {self.name} \n HP = {self.hp} \n Force : {self.force} \n Speed : {self.speed} \n Debilities : {self.debilities} \n Hax : {self.hax} \n Level : {self.level}"


class Human(Character):
    def __init__(
        self,
        name,
        hp=100,
        max_hp=100,
        force=100,
        speed=200,
        debilities="love",
        hax="Sociability",
        level=1,
        weapon=None,
        defending=False,
        porcent=0.20,
    ):
        super().__init__(
            name,
            hp,
            max_hp,
            force,
            speed,
            debilities,
            hax,
            level,
            weapon,
            defending,
            porcent,
        )


class Androide(Character):
    def __init__(
        self,
        name,
        hp=175,
        max_hp=175,
        force=200,
        speed=130,
        debilities="Energy",
        hax="Bomb",
        level=1,
        weapon=None,
        defending=False,
        porcent=0.15,
    ):
        super().__init__(
            name,
            hp,
            max_hp,
            force,
            speed,
            debilities,
            hax,
            level,
            weapon,
            defending,
            porcent,
        )


class Delfo(Character):
    def __init__(
        self,
        name,
        hp=125,
        max_hp=125,
        force=175,
        speed=100,
        debilities="Physical",
        hax="Magic",
        level=1,
        weapon=None,
        defending=False,
        porcent=0.17,
    ):
        super().__init__(
            name,
            hp,
            max_hp,
            force,
            speed,
            debilities,
            hax,
            level,
            weapon,
            defending,
            porcent,
        )


__all__ = ["Androide", "Character", "Delfo", "Human"]