from euchre import Game, Euchre
from euchre.utility import custom_json_serializer
import copy
import json

def set_nested_attr(obj, path, value):
    print(f"set_nested_attr({path}, {value})")
    attrs = path.split(".")
    for attr in attrs[:-1]:
        obj = getattr(obj, attr)

    print(obj, attrs[-1], value)
    setattr(obj, attrs[-1], value)

game = Game(["Adam", "Eve", "Cain", "Able"])


set_nested_attr(game, "deck_manager.up_card", "10♣")
