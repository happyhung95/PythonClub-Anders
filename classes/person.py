import random

from termcolor import cprint, colored

from classes.colors import Color


class Person:
    default_hp = 100
    default_mp = 100

    def __init__(self, name, human_mode, human_team=None):
        """Player class"""
        self.name = name
        self.hp = Person.default_hp
        self.max_hp = Person.default_hp
        self.mp = Person.default_mp
        self.max_mp = Person.default_mp
        self.human_mode = human_mode
        self.human_team = human_team
        self.dead = False

    def get_stat(self):
        """To get player's stat name/hp/maxHP/mp/maxMp"""
        if self.mp < 0:
            self.mp = 0
        """Determine colors to print"""
        if self.human_mode or self.human_team:
            name_color = Color.name_human
            hp_color = Color.hp_human
            mp_color = Color.mp_human
            dead_color = Color.dead_human
        else:
            name_color = Color.name_bot
            hp_color = Color.hp_bot
            mp_color = Color.mp_bot
            dead_color = Color.dead_bot

        if self.dead:
            cprint(f"{self.name.upper():^10}: ", color=name_color, end="")
            cprint("DEAD", color=dead_color)
        else:
            cprint(f"{self.name.upper():^10}: ", color=name_color, end="")
            print(
                colored("HP", hp_color),
                Person.health_bar(
                    num=self.hp,
                    max=self.max_hp,
                    type="hp",
                    hp_color=hp_color,
                    mp_color=mp_color,
                ),
                end="",
            )
            cprint(f"{self.hp:>3}/{self.max_hp}", color=hp_color)
            print(
                f" " * 11,
                colored("MP", color=mp_color),
                Person.health_bar(
                    num=self.mp,
                    max=self.max_mp,
                    type="mp",
                    hp_color=hp_color,
                    mp_color=mp_color,
                ),
                end="",
            )
            cprint(f"{self.mp:>3}/{self.max_mp}", color=mp_color)

    def is_dead(self):
        if self.hp <= 0:
            self.dead = True
            return True
        else:
            return False

    def slapped(self):
        """Get slapped by other player without magic"""
        dmg = random.randint(1, 20)
        self.hp -= dmg
        print(f"{self.name.upper()} got slapped -{dmg} HP ({self.hp}/{self.max_hp})\n")
        return True  # The action is carried out successfully

    @staticmethod
    def health_bar(num, max, type, hp_color, mp_color):
        full_bar = 20
        dash_convert = int(max / full_bar)
        current_dashes = int(num / dash_convert)
        remaining_health = full_bar - current_dashes
        remaining_display = "-" * remaining_health

        if type == "hp":
            health_display = "▓" * current_dashes
            return colored(f"{health_display}{remaining_display} ", color=hp_color)
        elif type == "mp":
            health_display = "░" * current_dashes
            return colored(f"{health_display}{remaining_display} ", color=mp_color)
