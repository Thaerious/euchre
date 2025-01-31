import pytest
from euchre.Euchre import *
from euchre.Game import *

@pytest.fixture
def game():
    random.seed(61753)
    game = Game(["Bot_1","Bot_3","Adam","Bot_2"])

    return game

def test_dealer_alone(game):
    game.input(None, 'start', None)
    game.input('Bot_1', 'pass', None)
    game.input('Bot_3', 'pass', None)
    game.input('Adam', 'pass', None)
    game.input('Bot_2', 'pass', None)

    assert game.current_state == 3

    print(game)
