import random
from enum import Enum, auto

from termcolor import colored

from classes.colors import Color
from classes.db import not_number


class MagicType(Enum):
    light = auto()
    dark = auto()


class Magic:
    collection = None  # For selecting magic created in main.py

    def __init__(self, name, dmg, mp_cost, type):
        self.name = name
        self.mp_cost = mp_cost
        self.dmg = dmg
        self.type = type
        self.description = colored(
            self.explain(self.type), Color.magic_explain
        ) + colored(f"| -{self.mp_cost} MP", Color.magic_cost)

    def explain(self, type):
        if type == MagicType.dark:
            return f"damage {self.dmg - 15}-{self.dmg + 15} HP "
        else:
            return f"heal {self.dmg - 15}-{self.dmg + 15} HP "

    def damage(self):
        return random.randint(self.dmg - 15, self.dmg + 15)

    @classmethod
    def enchant(cls, attacker, target):
        magic = Magic.choose(attacker)
        if magic is None:
            return False  # The action cannot be carried out

        if attacker.mp < magic.mp_cost:
            print(
                f"{attacker.name.upper()} ({attacker.mp}/{attacker.max_mp}) does not have enough MP."
            )
            print(f"{magic.name.capitalize()} costs {magic.mp_cost} MP.")
            return False

        dmg = magic.damage()

        if magic.type == MagicType.dark:
            attacker.mp -= magic.mp_cost
            target.hp -= dmg
            print(
                f"{target.name.upper()} was enchanted with {magic.name.upper()},",
                end=" ",
            )
            print(f"-{dmg} HP ({target.hp}/{target.max_hp})")
            print(
                f"{attacker.name.upper()} -{magic.mp_cost} MP ({attacker.mp}/{attacker.max_mp})\n"
            )
        elif magic.type == MagicType.light:
            attacker.mp -= magic.mp_cost
            attacker.hp += dmg
            print(
                f"{attacker.name.upper()} was enchanted with {magic.name.upper()},",
                end=" ",
            )
            if attacker.hp > attacker.max_hp:
                attacker.hp = attacker.max_hp
                print(f"HP is full ({attacker.hp}/{attacker.max_hp})")
            else:
                print(f"+{dmg} HP ({attacker.hp}/{attacker.max_hp})")
            print(f"\t-{magic.mp_cost} MP ({attacker.mp}/{attacker.max_mp})\n")
        return True  # The action is carried out successfully

    @staticmethod
    def choose(attacker):
        num_magics = len(Magic.collection)
        magic = None
        if attacker.human_mode:  # human's turn
            while True:
                Magic.show(attacker)
                index = input(colored("Select magic: ", color=Color.command))
                if index == "*":
                    return None
                if not_number(index):
                    continue
                index = int(index)
                if index > num_magics or index < 1:
                    print(f"Please enter only 1-{num_magics}")
                    continue
                magic = Magic.collection[index]
                break
        else:  # computer's turn
            magic = Magic.collection[random.randint(1, num_magics)]
        return magic

    @staticmethod
    def show(attacker):
        """Show magics that are available to use"""
        magics = ""
        for num, magic in Magic.collection.items():
            if attacker.mp < magic.mp_cost:
                continue
            else:
                magics += f"\t{str(num)}: {magic.name} - {magic.description}\n"
        magics += "\t*: Exit"
        print("Available magics")
        print(magics)
