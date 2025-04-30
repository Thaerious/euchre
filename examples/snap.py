from euchre import Game, Snapshot
import copy

game = Game(["Adam", "Eve", "Cain", "Able"])
game1 = copy.deepcopy(game)
game.input(None, "start", None)
snap = Snapshot(game, "Adam")

print(snap)