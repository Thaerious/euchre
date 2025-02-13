from euchre import *
from euchre.bots import *
from euchre.card import *
from euchre.class_getter import *
from euchre.rotate import rotate_to
import random
import time
import sys
from euchre.custom_json_serializer import custom_json_serializer
import json

class Bot_Record():
    def __init__(self, bot):
        self.bot = bot
        self.wins = 0

def do_run(names):
    #setup game
    game = Game(names)
    game.input(None, "start")

    #randomize initial dealer
    # lead = random.randint(0, 3)
    # game.order = rotate_to(game.order, 1)

    game.register_hook("before_input", lambda action, data:
        print(f"{game.current_player.name} {action} {data}")
    )

    #play one hand
    while game.current_state != 0:
        if game.current_state in [6, 7]:
            game.input(None, "continue", None)    
        else:
            bot = bots[game.current_player.name].bot
            (action, data) = bot.decide(Snapshot(game, game.current_player.name))
            game.input(game.current_player.name, action, data)

    # track winners
    if game.teams[0].score > game.teams[1].score:
        for player in game.teams[0].players:
            bots[player.name].wins += 1
    else:
        for player in game.teams[1].players:
            bots[player.name].wins += 1

    print(f"{game.teams[0].score} {game.teams[1].score}")


seed = random.randint(0, 100000)
if len(sys.argv) > 1: seed = int(sys.argv[1])
random.seed(seed)

bots = {    
    "Bot_10": Bot_Record(Bot_1()),
    "Bot_20": Bot_Record(Bot_1()),
    "Bot_11": Bot_Record(Bot_1()),
    "Bot_21": Bot_Record(Bot_1()),
}

as_dict = {
    "name": "name",
    "tricks": 4,
    "played": ["A"],
    "hand": [],
    "alone": True
}

names = list(bots.keys())
game1 = Game(names)
game1.input(None, "start")
game1.input(game1.current_player.name, "order")
game1.input(game1.current_player.name, "down")
game1.input(game1.current_player.name, "play", game1.players[0].hand[0])

print(game1.__dict__)

j = json.dumps(game1, indent=2, default=custom_json_serializer)

game2 = Game.from_json(json.loads(j))

print(game1)
print(game2)
