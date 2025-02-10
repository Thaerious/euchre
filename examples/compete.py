from euchre import *
from euchre.bots import *
from euchre.card import *
from euchre.class_getter import *
import random
import time
import sys

run_count = 100
if len(sys.argv) > 1:
    run_count = int(sys.argv[1])

bots = {
    "Bot_00": [Bot_1(), 0],
    "Bot_10": [Bot_0(), 0],
    "Bot_01": [Bot_1(), 0],
    "Bot_11": [Bot_0(), 0],
}

# bots = {
#     "Bot_20": [Bot_2(), 0],
#     "Bot_10": [Bot_1(), 0],
#     "Bot_21": [Bot_2(), 0],
#     "Bot_11": [Bot_1(), 0],
# }

names = list(bots.keys())
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
            bot = bots[game.current_player.name][0]
            (action, data) = bot.decide(Snapshot(game, game.current_player.name))
            game.input(game.current_player.name, action, data)

    # print(f"{game.get_player(0).name}-{game.get_player(2).name} vs {game.get_player(1).name}-{game.get_player(3).name} {game.score}")
    
    if game.score[0] > game.score[1]:
        bots[game.get_player(0).name][1] = bots[game.get_player(0).name][1] + 1
        bots[game.get_player(2).name][1] = bots[game.get_player(2).name][1] + 1
    else:
        bots[game.get_player(1).name][1] = bots[game.get_player(1).name][1] + 1
        bots[game.get_player(3).name][1] = bots[game.get_player(3).name][1] + 1

end = time.time()
bots["Bot_10"][0].print_stats()

print(f"\nElapsed time: {end - start} seconds")
print(f"Average time: {(end - start) / run_count} seconds\n")

for key in bots.keys():
    print(f"{key} {round(bots[key][1] / run_count, 2)}")
