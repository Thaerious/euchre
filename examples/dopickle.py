from euchre import *
import pickle

game_in = Game(["adam", "eve", "cain", "able"])
game_in.input(None, "start")

with open("game.file", "wb") as fp:
    pickle.dump(game_in, fp)

with open("game.file", "rb") as f:
    game_out = pickle.load(f)
    print(game_out)    