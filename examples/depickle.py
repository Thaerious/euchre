from euchre import *
import pickle

with open("game.file", "rb") as f:
    game = pickle.load(f)
    print(game)
