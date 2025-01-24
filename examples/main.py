from euchre import Game, Snapshot
from euchre.bots import Bot
from euchre.card import *
from euchre.Euchre import is_game_over
import sys
import random

def decide(game):
    if len(sys.argv) > 1: print("-----------------------------------------")

    if game.current_state == 6:
        if len(sys.argv) > 1:print(game)
        game.input(None, "continue", None)
        return

    state_before = game.current_state
    if len(sys.argv) > 1: print(f"{game.euchre.current_player}")
    if len(sys.argv) > 1 and game.euchre.up_card is not None: print(f"up card {game.euchre.up_card}")
    if len(sys.argv) > 1 and len(game.euchre.tricks) > 0: print(f"trick {game.euchre.tricks[-1]}")
    snap = Snapshot(game, game.euchre.current_player.name)
    decision = bot.decide(snap)
    game.input(game.euchre.current_player.name, decision[0], decision[1])
    if len(sys.argv) > 1: print(f"{decision} {state_before} -> {game.current_state}")
    

if len(sys.argv) == 1:
    for i in range(100):
        names = ["Player1", "Player2", "Player3", "Player4"]
        game = Game(names)

        seed = random.randint(0, 10000)
        print(f"{i} {seed}")
        game.debug_seed = seed
        bot = Bot()

        game.input(None, "start")

        while is_game_over(game.euchre.score) == False:
            decide(game)
else:
    names = ["Player1", "Player2", "Player3", "Player4"]
    game = Game(names)

    seed = int(sys.argv[1])    
    game.debug_seed = seed
    bot = Bot()

    game.input(None, "start")

    while is_game_over(game.euchre.score) == False:
        decide(game)    

    print(game.euchre.score)
