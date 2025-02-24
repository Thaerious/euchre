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

    def play_game(self, game):
        while game.current_state != 0:
            if game.current_state == 7:
                score = game.calc_hand()
                self.record_hand(score)
                
            if game.current_state in [6, 7]:
                game.input(None, "continue", None)
            else: 
                try:
                    bot = self.bots[game.current_player.name].bot
                    snap = Snapshot(game, game.current_player.name)
                    (action, data) = bot.decide(snap)
                    game.input(game.current_player.name, action, data)
                except:
                    print(f"Last Query: {bot.last_query}")
                    print(snap)
                    raise

        for player in game.players:
            if player.team.score >= 10: self.bots[player.name].wins += 1

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

        for key in self.bots.keys():
            record = self.bots[key]
            # print(f"{key} {record.wins}")
            print(f"{key} {(record.wins / self.run_count):.2f}")        

def main():
    count = 10
    seed = random.randint(0, 100000)

    if len(sys.argv) > 1:
        count = int(sys.argv[1])

    if len(sys.argv) > 2:
        seed = int(sys.argv[2])        

    compete = Compete(seed, [Bot_2, Bot_3])   
    compete.run(count)
    compete.report()

main()

# cProfile.run('main()', 'output.prof')
# stats = pstats.Stats('output.prof')
# # stats.strip_dirs().sort_stats('time').print_stats()

# stats.strip_dirs().print_callers('trump')