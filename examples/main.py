from euchre import *
from euchre.bots import *
from euchre.card import *
from euchre.class_getter import *
from euchre.bots.tools.Query import Query
import random
import time
import sys

random.seed(1234)

names = ["Player1", "Player2", "Player3", "Player4"]
game = Game(names)
game.input(None, "start")
game.input("Player1", "order")
game.input("Player4", "down")
snap = Snapshot(game, "Player1")

# print(snap)
# ['A♦', '9♣', 'J♦', 'K♠', 'J♥']

query = Query(snap)
r = query.select("~J♦♥")
print(snap)
