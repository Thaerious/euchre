from euchre import Game, Snapshot
from euchre.bots import Bot
from euchre.card import *

def decide(game):
    print("-----------------------------------------")
    state_before = game.current_state
    print(f"{game.euchre.current_player}")
    snap = Snapshot(game, game.euchre.current_player.name)
    decision = bot.decide(snap)
    game.input(game.euchre.current_player.name, decision[0], decision[1])
    print(f"{decision} {state_before} -> {game.current_state}")
    

names = ["Player1", "Player2", "Player3", "Player4"]
game = Game(names)

game.debug_seed = 1001
bot = Bot()

game.input(None, "start")

decide(game)
decide(game)
decide(game)
decide(game)
decide(game)
decide(game)

