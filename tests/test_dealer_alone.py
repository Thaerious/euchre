import pytest
from euchre.Euchre import *
from euchre.Game import *

@pytest.fixture
def game():
    random.seed(718)
    game = Game(["Bot_1", "Adam", "Bot_2", "Bot_3"])
    game.input(None, 'start', None)

    return game

def test_dealer_alone(game):
    print(game)

