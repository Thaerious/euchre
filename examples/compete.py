from euchre import *
from euchre.bots import *
from euchre.card import *
from euchre.class_getter import *
from euchre.rotate import rotate_to, rotate
import random
import time
import sys
import cProfile
import pstats
from collections import defaultdict

class Bot_Record():
    def __init__(self, bot):
        self.bot = bot
        self.wins = 0

class Compete():
    def __init__(self, seed, bots):
        self.run_count = 0
        self.seed = seed

        self.bot_a = bots[0]()
        self.bot_b = bots[1]()

        self.bots = {    
            "Bot_10": Bot_Record(self.bot_a),
            "Bot_20": Bot_Record(self.bot_b),
            "Bot_11": Bot_Record(self.bot_a),
            "Bot_21": Bot_Record(self.bot_b),
        }

        self.wins = defaultdict(lambda: {"Bot_1": 0, "Bot_2": 0})

    def run(self, count):
        self.start = time.time()

        for i in range(count):
            self.step(self.seed + i, 0)
            self.step(self.seed + i, 1)

        self.end = time.time()

    def step(self, seed, rotate_count):
        self.run_count = self.run_count + 1
        names = list(self.bots.keys())

        for i in range(0, rotate_count):
            rotate(names)
        
        game = Game(names, seed)
        game.input(None, "start")
        self.play_game(game)   

        if game.get_player("Bot_10").team.score >= 10: 
            self.wins[seed]["Bot_1"] += 1
        else:
            self.wins[seed]["Bot_2"] += 1

    def play_game(self, game: Game):
        while game.current_state != 0:
            if game.current_state == 7:
                score = game.calc_hand()
                self.record_hand(score)
                
            if game.current_state in [6, 7]:
                game.input(None, "continue", None)
            else: 
                try:
                    bot: Bot_0 = self.bots[game.current_player.name].bot
                    snap = Snapshot(game, game.current_player.name)
                    (action, data) = bot.decide(snap)
                    game.input(game.current_player.name, action, data)
                except:
                    print(f"Last Query: {bot.last_query}")
                    print(snap)
                    raise

    def record_hand(self, hand_score):
        for team in hand_score.keys():
            for player in team.players:
                self.bots[player.name].bot.score(hand_score[team])

    def report(self):
        print(f"Bot A: {type(self.bot_a).__name__}")
        self.bot_a.print_stats()
        print(f"\nBot B: {type(self.bot_b).__name__}")
        self.bot_b.print_stats()

        print(f"\nElapsed time: {self.end - self.start} seconds")
        print(f"Average time: {(self.end - self.start) / self.run_count} seconds\n")

        WW = 0
        LW = 0
        WL = 0   

        for seed in self.wins:
            result = self.wins[seed]
            # print(f"{seed}: {result}")
            if result["Bot_1"] == 1 and result["Bot_2"] == 1: WW += 1
            elif result["Bot_1"] == 2 and result["Bot_2"] == 0: WL += 1
            elif result["Bot_1"] == 0 and result["Bot_2"] == 2: LW += 1
            else: raise Exception("Sanity Check Failed")

        print("Tie\tBot_1\tBot_2")
        print(f"{WW}\t{WL}\t{LW}")

def main():
    count = 10
    seed = random.randint(0, 100000)

    if len(sys.argv) > 1:
        count = int(sys.argv[1])

    if len(sys.argv) > 2:
        seed = int(sys.argv[2])        

    compete = Compete(seed, [Bot_1, Bot_2])   
    compete.run(count)
    compete.report()

main()

# cProfile.run('main()', 'output.prof')
# stats = pstats.Stats('output.prof')
# # stats.strip_dirs().sort_stats('time').print_stats()

# stats.strip_dirs().print_callers('trump')