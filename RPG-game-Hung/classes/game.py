import random
import time

from termcolor import cprint, colored

from classes.colors import Color
from classes.db import Database, not_number
from classes.actions import Action
from classes.person import Person
from classes.items import Item
from classes.magics import Magic



class Game:
    running = True

    @staticmethod
    def prep(magic_collection, item_collection):
        """Run once before game to prepare necessary variables"""
        # Compile string of actions for printing
        Action.show_actions()
        # Initiate variable for Item.choose() function in Item class
        Item.collection = item_collection
        # Initiate variable for Magic.choose() function in Magic class
        Magic.collection = magic_collection

    @staticmethod
    def choose_mode():
        print(
            """Available play mode
    1: You + computer vs computers
    2: You vs computer(s)"""
        )
        while True:
            choice = input(colored("Choose play mode: ", Color.command))
            if not_number(choice):
                continue
            choice = int(choice)
            if choice not in [1, 2]:
                print("Please enter only 1 or 2\n")
                continue
            break
        if choice == 1:
            man_vs_bot = False
        else:
            man_vs_bot = True
        return man_vs_bot

    @staticmethod
    def create_players(enemy_names):
        """Create players - humans and computers"""
        while True:
            man_vs_bot = Game.choose_mode()  # True if in mode players vs computers
            num_player = input(
                colored("Number of players (1-5, or * to go back): ", color=Color.command)
            )
            if num_player == '*' or not_number(num_player):
                continue
            Database.num_player = int(num_player)
            if Database.num_player > 5 or Database.num_player < 1:
                print(
                    "The game can only have 1-5 players. Please enter the number of players again.\n"
                )
                continue
            break
        print("Please enter the name(s) of player(s)")
        for i in range(Database.num_player):
            text = colored(f"Player {i + 1}: ", Color.command)
            if man_vs_bot:  # Players vs computers mode
                Database.players.append(
                    Person(name=input(text).capitalize(), human_mode=True)
                )
            else:  # Player + computer vs computers mode
                if i == 0:
                    Database.players.append(
                        Person(name=input(text).capitalize(), human_mode=True)
                    )
                elif i > 0:
                    Database.players.append(
                        Person(
                            name=input(text).capitalize(),
                            human_mode=False,
                            human_team=True,
                        )
                    )
            Database.computers.append(Person(name=enemy_names[i], human_mode=False, human_team=False))

    @staticmethod
    def show_stat():
        """Show stats of all players and enemies"""
        color = Color.show_stats_dash
        cprint("===========", color=color)
        for player in Database.players:
            player.get_stat()
        cprint("---", color=color)
        for enemy in Database.computers:
            enemy.get_stat()
        cprint("===========\n", color=color)

    @staticmethod
    def show_computers():
        """Show computers that are alive"""
        names = list()
        names += ""
        for num, computer in enumerate(Database.computers):
            if computer.dead:
                continue
            else:
                names += f'\t{str(num + 1)}: {computer.name.upper():<11} {colored(f"|HP {computer.hp}"):>8}\n'
        names.pop(-1)
        msg = "".join(names)
        print("All enemies:")
        print(msg)

    @staticmethod
    def choose_victim(attacker, targets):
        if attacker.human_mode:  # human's mode
            while True:
                Game.show_computers()
                index = input(colored(f"Select enemy to attack: ", color=Color.command))
                if not_number(index):
                    continue
                index = int(index)
                if index > Database.num_player or index < 1:
                    print(f"Please enter only 1-{Database.num_player}\n")
                    continue
                victim = targets[index - 1]
                if victim.dead:
                    print(
                        f"\n{victim.name.upper()} is {colored('DEAD', color=Color.dead_bot)}, pick another target\n"
                    )
                    continue
                break
        else:  # computer's turn
            while True:
                victim = targets[random.randint(0, Database.num_player - 1)]
                if victim.dead:
                    continue
                break
        return victim

    @staticmethod
    def perform_actions(attacker, target):  # Do not remove vars target
        if attacker.human_mode:  # human's turn
            while True:
                action_key = input(f"{Action.text}")
                if not_number(action_key):
                    continue
                action_key = int(action_key)
                if action_key > len(Action.collection) or action_key < 1:
                    print(f"Please enter only 1-{len(Action.collection)}")
                    continue
                action_success = eval(
                    Action.collection[action_key][1]
                )  # Return True or False
                if not action_success:  # if the action cannot be carried out
                    continue
                time.sleep(Database.sleep)
                break
        else:  # computer's turn
            while True:
                if not attacker.human_team:  # if computer not in human team.
                    cprint(
                        f"{attacker.name.upper()}: ",
                        color=Color.name_bot,
                        attrs=["bold"],
                    )
                action_key = random.randint(1, len(Action.collection))
                action_success = eval(Action.collection[action_key][1])
                if not action_success:
                    continue
                time.sleep(Database.sleep)
                break

    @classmethod
    def has_winner(cls):
        if len(Database.dead_computer) == Database.num_player:
            Game.show_stat()
            print("Human WIN!!!")
            Game.running = False
            return True
        elif len(Database.dead_player) == Database.num_player:
            Game.show_stat()
            print("Computer WIN!!")
            Game.running = False
            return True
