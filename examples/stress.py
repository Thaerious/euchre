from euchre import *
from euchre.bots import Bot
from euchre.card import *
from euchre.class_getter import *
import random
import time

names = ["Player1", "Player2", "Player3", "Player4"]
bot = Bot()

start = time.time()

for i in range(250):
    random.shuffle(names)
    game = Game(names)
    game.input(None, "start")

    while game.current_state != 0:
        if game.current_state in [6, 7]:
            game.input(None, "continue", None)    
        else:
            (action, data) = bot.decide(Snapshot(game, game.current_player.name))
            game.input(game.current_player.name, action, data)

end = time.time()
print(f"Elapsed time: {end - start} seconds")
print(f"Average time: {(end - start) / 250} seconds")