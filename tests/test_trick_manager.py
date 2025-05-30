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
    game = DummyGame(["A", "B", "C", "D"])
    manager = TrickManager(game)
    return game, manager


def test_add_trick(setup_game):
    _, manager = setup_game
    manager.add_trick()
    assert manager.current_trick is not None
    assert len(manager) == 1

def test_add_trick_fails_without_trump(setup_game):
    game, manager = setup_game
    game.trump = None  # unset trump
    with pytest.raises(EuchreError, match="Trump must be declared"):
        manager.add_trick()

def test_add_trick_fails_if_previous_not_finished(setup_game):
    game, manager = setup_game
    manager.add_trick()
    # Trick not finished — no cards played
    with pytest.raises(EuchreError, match="Previous trick is still in progress."):
        manager.add_trick()