from termcolor import cprint
from classes.game import Game
from classes.db import Database
from classes.colors import Color
from classes.items import Item, ItemType
from classes.magics import Magic, MagicType

computer_names = [
    "Hell Guard",
    "Dark Lord",
    "Evil Angel",
    "Satan",
    "Devil",
]

magics = {
    1: Magic(name="Dark Love", dmg=25, mp_cost=15, type=MagicType.dark),
    2: Magic(name="Banana Bread", dmg=30, mp_cost=20, type=MagicType.dark),
    3: Magic(name="Heart Break", dmg=35, mp_cost=25, type=MagicType.dark),
    4: Magic(name="Pink Depression", dmg=40, mp_cost=30, type=MagicType.dark),
    5: Magic(name="Kiss", dmg=15, mp_cost=10, type=MagicType.light),
    6: Magic(name="Lust", dmg=25, mp_cost=20, type=MagicType.light),
    7: Magic(name="Sex", dmg=35, mp_cost=30, type=MagicType.light),
}

items = {
    1: Item(
        name="potion",
        type=ItemType.potion,
        description="heal 50 HP",
        property=50,
        quantity=10,
    ),
    2: Item(
        name="high potion",
        type=ItemType.potion,
        description="heal 100 HP",
        property=100,
        quantity=10,
    ),
    3: Item(
        name="super potion",
        type=ItemType.potion,
        description="heal 300 HP",
        property=300,
        quantity=1,
    ),
    4: Item(
        name="elixer",
        type=ItemType.elixer,
        description="restore max MP and HP",
        property=None,
        quantity=1,
    ),
    5: Item(
        name="grenade",
        type=ItemType.attack,
        description="300 HP damage",
        property=300,
        quantity=2,
    ),
    6: Item(
        name="machine gun",
        type=ItemType.attack,
        description="40 HP damage",
        property=40,
        quantity=4,
    ),
    7: Item(
        name="cannon",
        type=ItemType.attack,
        description="60 HP damage",
        property=60,
        quantity=3,
    ),
}

GAME_START = """
This game is a classical fight game! It can be an old fashioned slap fight, or use magic or item
You can choose number of players against the computer (maximum 5)
There are 2 play modes of the game:
    1. You and computer will fight against computers OR
    2. You will control all your team and fight against computers
Beware: computers might be geniuses, or dummies depends on the mood, or the weather!

Have fun!

Hung - 15.03.2020
"""


def main():
    stop = False

    cprint(GAME_START, color=Color.start_msg)
    """ Create players and computers"""
    Game.create_players(enemy_names=computer_names)

    """Prepare necessary variables for game run"""
    Game.prep(magic_collection=magics, item_collection=items)

    """Start loop game"""
    while Game.running:
        Game.show_stat()
        """Player's turn"""
        for player in Database.players:
            if player.dead:
                continue
            cprint(
                f"{player.name.upper()}'s turn (HP {player.hp}, MP {player.mp})",
                color=Color.name_human,
                attrs=["bold"],
            )
            victim = Game.choose_victim(attacker=player, targets=Database.computers)
            Game.perform_actions(attacker=player, target=victim)
            if victim.is_dead():
                Database.dead_computer.add(victim)
            """If players win, stop the game"""
            if Game.has_winner():
                stop = True
                break
        if stop:
            break

        """Computer's turn"""
        cprint("----- ENEMIES ARE ATTACKING -----", Color.enemy_attack)
        for computer in Database.computers:
            if computer.dead:
                continue
            victim = Game.choose_victim(attacker=computer, targets=Database.players)
            Game.perform_actions(attacker=computer, target=victim)
            if victim.is_dead():
                Database.dead_player.add(victim)
            if Game.has_winner():
                break
        cprint("---------------------------------", Color.enemy_attack)


if __name__ == "__main__":
    main()
