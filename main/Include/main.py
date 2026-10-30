import time

import characters as ch
from logica import fight, get_enemy_for_level
from weapons import weapons


def equip_weapon(player):
    """Let the player pick a weapon, validating the input."""
    print("Available weapons:")
    for i, w in enumerate(weapons):
        print(f"  {i + 1}. {w.name} (DMG: {w.damage})")
    while True:
        raw = input("Choose weapon (number): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(weapons):
            player.catch_weapon(weapons[int(raw) - 1])
            return
        print(f"Invalid. Enter a number between 1 and {len(weapons)}.")


time.sleep(1)
print("------------------------------")
time.sleep(1)
print("Hi You...")
time.sleep(1)
print("how... are ... yy..")
time.sleep(1)
print("-" * 22)
time.sleep(1)
print("This game was created without end")
time.sleep(1)
print("-" * 22)
time.sleep(1)

declaration: str = input(
    "Hi, you \n What do you want to be?  \n 1- Human \n 2- Delfos \n 3- Androide \n "
)

match declaration:
    case "1":
        print("Has elegido el bando de los humanos")
        name = input("How you would like to name\n Name :")
        player = ch.Human(name)
        time.sleep(2)
        print(player)
        time.sleep(2)
        equip_weapon(player)
        print(f"Equipped: {player.weapon.name}")
        enemy = get_enemy_for_level(player.level, "human")
        fight(player, enemy)

    case "2":
        print("Has elegido el bando de los delfos")
        name = input("How you would like to name\n Name :")
        player = ch.Delfo(name)
        time.sleep(2)
        print(player)
        time.sleep(2)
        equip_weapon(player)
        print(f"Equipped: {player.weapon.name}")
        enemy = get_enemy_for_level(player.level, "delfo")
        fight(player, enemy)

    case "3":
        print("Has elegido el bando de los androides")
        name = input("How you would like to name\n Name :")
        player = ch.Androide(name)
        time.sleep(2)
        print(player)
        time.sleep(2)
        equip_weapon(player)
        print(f"Equipped: {player.weapon.name}")
        enemy = get_enemy_for_level(player.level, "androide")
        fight(player, enemy)
