# test_trick_manager.py

import pytest
from euchre.card import Card, Deck
from euchre.player import Player
from euchre.TrickManager import TrickManager
from euchre.utility.rotate import rotate_to
from euchre import EuchreError

class DummyGame:
    def __init__(self, player_names, trump="♠"):
        self.players = [Player(name, i) for i, name in enumerate(player_names)]
        self.order = list(range(4))
        self.trump = trump
        self.deck = Deck(seed=42)
        self.current_player_index = 0

    def rotate_to_player(self, index):
        if isinstance(index, Player):
            index = index.index

        rotate_to(self.order, index)
        self.current_player_index = index

    def get_player(self, index):
        return self.players[index]


@pytest.fixture
def setup_game():
    manager = TrickManager(DummyGame(["A", "B", "C", "D"]))
    return manager

def test_add_trick(setup_game):
    manager = setup_game
    manager.add_trick("♠", [0, 1, 2, 3])
    assert manager.current_trick is not None
    assert len(manager) == 1

