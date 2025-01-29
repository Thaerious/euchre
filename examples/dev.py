from euchre import Game, Snapshot
from euchre.bots import Bot
from euchre.card import *
from euchre.class_getter import *

names = ["Player1", "Player2", "Player3", "Player4"]
game = Game(names)
game.seed = 100

game.input(None, "start")
game.input("Player1", "order")
game.input("Player4", "down")
game.input("Player1", "play", "K♠")

snap = Snapshot(game, "Player1")
print(game)
print(snap.to_json())

