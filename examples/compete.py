from euchre import *
from euchre.bots import *
from euchre.card import *
from euchre.class_getter import *
from euchre.rotate import rotate_to, rotate
import random
import time
import sys

def play_game(game):
    while game.current_state != 0:
        if game.current_state in [6, 7]:
            game.input(None, "continue", None)
        else: 
            try:
                bot = bots[game.current_player.name].bot
                (action, data) = bot.decide(Snapshot(game, game.current_player.name))
                game.input(game.current_player.name, action, data)
            except:
                print(f"Last Query: {bot.last_query}")
                raise

    for player in game.players:
        if player.team.score >= 10: bots[player.name].wins += 1

run_count = 100
seed = random.randint(0, 100000)

if len(sys.argv) > 1:
    run_count = int(sys.argv[1])

if len(sys.argv) > 2:
    seed = int(sys.argv[2])

random.seed(seed)

bot_a = Bot_1()
bot_b = Bot_2()

class Bot_Record():
    def __init__(self, bot):
        self.bot = bot
        self.wins = 0

bots = {    
    "Bot_10": Bot_Record(bot_a),
    "Bot_20": Bot_Record(bot_b),
    "Bot_11": Bot_Record(bot_a),
    "Bot_21": Bot_Record(bot_b),
}

names = list(bots.keys())
start = time.time()

for i in range(run_count):
    random.seed(seed)

    for i in range(0, random.randint(0, 3)):
        rotate(names)

    #setup game
    game = Game(names)

    #randomize initial dealer
    lead = random.randint(0, 3)
    rotate_to(game.order, lead)

    game.input(None, "start")
    try:
        play_game(game)
        seed = seed + 1
    except Exception:
        print(game.to_json(None))
        raise

end = time.time()

bot_a.print_stats()
print("")
bot_b.print_stats()

print(f"\nElapsed time: {end - start} seconds")
print(f"Average time: {(end - start) / run_count} seconds\n")

for key in bots.keys():
    record = bots[key]
    # print(f"{key} {record.wins}")
    print(f"{key} {(record.wins / run_count):.2f}")
