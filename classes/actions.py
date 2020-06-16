from termcolor import colored

from classes.colors import Color


class Action:
    text = None  # For printing during player's action selection
    collection = {
        1: ["Slap", "target.slapped()"],
        2: ["Magic", "Magic.enchant(attacker,target)"],
        3: ["Item", "Item.use(attacker,target)"],
    }

    @staticmethod
    def show_actions():
        action = list()
        for k, v in Action.collection.items():
            action += f"{str(k)}: {v[0]}, "
        action.pop(-1)
        action.pop(-1)
        Action.text = (
            colored("Select action ", Color.command)
            + "("
            + "".join(action)
            + ")"
            + colored(": ", Color.command)
        )
