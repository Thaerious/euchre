from euchre import *
from euchre.bots import *
from euchre.card import *
from euchre.class_getter import *
from euchre.rotate import rotate_to
import random
import time
import sys
from euchre.custom_json_serializer import custom_json_serializer
import json

game1 = Game(["A", "B", "C", "D"])
game1.input(None, "start")
game1.input(game1.current_player.name, "order")
game1.input(game1.current_player.name, "down")
game1.input(game1.current_player.name, "play", game1.players[0].hand[0])

j = json.dumps(game1, indent=2, default=custom_json_serializer)

game2 = Game.from_json(json.loads(j))

print(game1)
print(game2)
