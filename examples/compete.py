from euchre import *
from euchre.bots import *
from euchre.card import *
from euchre.class_getter import *
import random
import time
import sys

run_count = 2000
if len(sys.argv) > 1:
    run_count = int(sys.argv[1])

results = {
    "Bot_00": 0,
    "Bot_10": 0,
    "Bot_01": 0,    
    "Bot_11": 0,
}

bots = {
    "Bot_00": Bot_0(),
    "Bot_01": Bot_0(),
    "Bot_10": Bot_1(),
    "Bot_11": Bot_1(),
}

names = list(results.keys())
start = time.time()
seed = random.randint(0, 1000000)
random.seed(seed)

for i in range(run_count):
    # random.shuffle(names)
    game = Game(names)
    game.input(None, "start")

    while game.current_state != 0:
        if game.current_state in [6, 7]:
            game.input(None, "continue", None)    
        else:
            bot = bots[game.current_player.name]
            (action, data) = bot.decide(Snapshot(game, game.current_player.name))
            game.input(game.current_player.name, action, data)

    # print(f"{game.get_player(0).name}-{game.get_player(2).name} vs {game.get_player(1).name}-{game.get_player(3).name} {game.score}")
    
    if game.score[0] > game.score[1]:
        results[game.get_player(0).name] = results[game.get_player(0).name] + 1
        results[game.get_player(2).name] = results[game.get_player(2).name] + 1
    else:
        results[game.get_player(1).name] = results[game.get_player(1).name] + 1
        results[game.get_player(3).name] = results[game.get_player(3).name] + 1

end = time.time()
print(f"Elapsed time: {end - start} seconds")
print(f"Average time: {(end - start) / run_count} seconds")

for key in results.keys():
    print(f"{key} {round(results[key] / run_count, 2)}")
