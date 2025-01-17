from euchre.Game import Game
from euchre.Snapshot import Snapshot
import random

random.seed(1000)
names = ["Player1", "Player2", "Player3", "Player4"]
game = Game(names)
snap = Snapshot(game)