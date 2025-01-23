from euchre import Game, Snapshot
from euchre.bots import Bot
from euchre.card import *
import random

def decide(game):
    print("-----------------------------------------")
    print(f"{game.euchre.current_player}")
    snap = Snapshot(game, game.euchre.current_player.name)
    decision = bot.decide(snap)
    print(decision)
    game.input(game.euchre.current_player.name, decision[0], decision[1])
    

names = ["Player1", "Player2", "Player3", "Player4"]
game = Game(names)

game.debug_seed = 1000
bot = Bot()

game.input(None, "start")
print(game)

decide(game)
decide(game)


