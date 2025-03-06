from euchre import *

game = Game(["adam", "eve", "cain", "able"])
game.input(None, "start")
snap = Snapshot(game, "adam")
json = snap.to_json()
print(json)
