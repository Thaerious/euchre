from euchre import *
from euchre.bots import *
from euchre.bots.Bot_1_5 import Bot_1_5
from euchre.bots import *
from euchre.card import *
from euchre.class_getter import *
from euchre.rotate import rotate
import random
import time
import sys

class Single:
    def __init__(self, bots):
        self.bot_a = bots[0]()
        self.bot_b = bots[1]()

        self.bots = {    
            "Bot_10": self.bot_a,
            "Bot_20": self.bot_b,
            "Bot_11": self.bot_a,
            "Bot_21": self.bot_b,
        }

    def play(self, seed, rotate_count):
        names = list(self.bots.keys())

        for i in range(0, rotate_count):
            rotate(names)
        
        game = Game(names, seed)
        game.input(None, "start")
        self.play_game(game)  

        return game 

    def play_game(self, game: Game):
            while game.current_state != 0:
                if game.current_state == 7:
                    self.score = game.calc_hand()
                    
                if game.current_state in [6, 7]:
                    game.input(None, "continue", None)
                else: 
                    try:
                        bot: Bot_0 = self.bots[game.current_player.name]
                        snap = Snapshot(game, game.current_player.name)
                        (action, data) = bot.decide(snap)
                        game.input(game.current_player.name, action, data)
                    except:
                        print(f"Last Query: {bot.last_query}")
                        print(snap)
                        raise

seed = random.randint(0, 1000)
shift = 0

if len(sys.argv) > 1:
    seed = int(sys.argv[1])

if len(sys.argv) > 2:
    shift = int(sys.argv[1])

print(f"seed : {seed}")
print(f"shift : {shift}")     
single = Single([Bot_1, Bot_1_5])
game = single.play(seed, shift)          
print(game)