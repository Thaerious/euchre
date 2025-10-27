from euchre import Game, Euchre
from euchre.utility import custom_json_serializer
from euchre.utility import set_nested_attr
import copy
import json


game = Game(["Adam", "Eve", "Cain", "Able"])
game.deck.up_card = "10♣"
game.deck.trump = "♠"