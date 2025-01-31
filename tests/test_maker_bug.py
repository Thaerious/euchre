import pytest
from euchre.Euchre import *
from euchre.Game import *

    # Recreate a bug when a player orders up the dealer
    # the dealer swaps a card, the maker should be the player that
    # does the ordering up

@pytest.fixture
def game():
    game = Game(["Player1", "Player2", "Player3", "Player4"])
    random.seed(100)
    game.input(None, 'start', None)

    return game

def test_maker_bug(game):
    game.input('Player1', 'pass', None)
    game.input('Player2', 'order', None)
    game.input('Player4', 'up', '9♠')

    # the bug incorectly makes this Player4
    assert game.maker.name == "Player2"
