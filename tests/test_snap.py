from test_game import *
from euchre.Snapshot import Snapshot

def test_state_0(game):
    snap = Snapshot(game)
    print(snap)