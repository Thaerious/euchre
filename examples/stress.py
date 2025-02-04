from euchre import *
from euchre.bots import *
from euchre.card import *
from euchre.class_getter import *
import random
import time
import sys

run_count = 10
if len(sys.argv) > 1:
    run_count = int(sys.argv[1])

names = ["Player1", "Player2", "Player3", "Player4"]
bot = Bot_2()

start = time.time()

for i in range(run_count):
    seed = random.randint(0, 1000)
    print(seed)
    random.seed(seed)

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