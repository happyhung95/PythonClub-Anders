import random
from enum import Enum, auto
from classes.colors import Color
from termcolor import colored

from classes.db import not_number


class ItemType(Enum):
    potion = auto()
    elixer = auto()
    attack = auto()


class Item:
    collection = None  # For selecting items created in main.py

    def __init__(self, name, type, description, property, quantity):
        self.name = name
        self.type = type
        self.description = description
        self.property = property
        self.quantity = quantity

    @staticmethod
    def use(user, target):
        item = Item.choose(user=user)
        if item is None:
            return False  # The action cannot be carried out

        if item.quantity == 0:
            print(f"{item.name.capitalize()} is out of stock. Please pick another.")
            return False

        if item.type == ItemType.potion:
            user.hp += item.property
            print(
                f"{item.name.upper()} was used. {user.name.upper()} revives +{item.property} HP\n"
            )
            if user.hp > user.max_hp:
                user.hp = user.max_hp
        elif item.type == ItemType.elixer:
            user.hp = user.max_hp
            user.mp = user.max_mp
            print(
                f"{item.name.upper()} was used. {user.name.upper()} revives full HP and MP\n"
            )
        elif item.type == ItemType.attack:
            target.hp -= item.property
            print(
                f"{item.name.upper()} was used. {target.name.upper()} sustained the hit. (-{item.property} HP)\n"
            )
        item.quantity -= 1
        return True  # The action is carried out successfully

    @staticmethod
    def choose(user):
        num_items = len(Item.collection)
        item = None
        if user.human_mode:  # human's turn
            while True:
                Item.show()
                index = input(colored("Select item: ", color=Color.command))
                if index == "*":
                    return None
                if not_number(index):
                    continue
                index = int(index)
                if index > num_items or index < 1:
                    print(f"Please enter only 1-{num_items}")
                    continue
                item = Item.collection[index]
                break
        else:  # computer's turn
            item = Item.collection[random.randint(1, num_items)]
        return item

    @staticmethod
    def show():
        """Show items that are available"""
        items = ""
        for num, item in Item.collection.items():
            if item.quantity == 0:
                continue
            else:
                items += (
                    f"\t{str(num)}: {item.name.capitalize()} "
                    f"- {colored(item.description, color=Color.item_description)} "
                    f'- {colored(f"{item.quantity} available", color=Color.item_quantity)}\n'
                )
        items += "\t*: Exit"
        print("Available items")
        print(items)
