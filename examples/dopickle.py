import json

from euchre import Game, Snapshot
from euchre.custom_json_serializer import custom_json_serializer

game_in = Game(["adam", "eve", "cain", "able"], seed=0)
game_in.input(None, "start")
snapshot = Snapshot(game_in, "adam")

j = json.dumps(snapshot, indent=2, default=custom_json_serializer)

# print(snapshot.__repr__())
print(j)
