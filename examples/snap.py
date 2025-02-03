from euchre import *
from euchre.card import *
from euchre.class_getter import *

names = ["Player1", "Player2", "Player3", "Player4"]
game = Game(names)
game.input(None, "start")
snap = Snapshot(game, "Player1")
print(snap)
