from euchre import Euchre
import pytest

@pytest.fixture
def euchre():
    return Euchre(["A", "B", "C", "D"], 100)

def test_is_game_is_over(euchre):
    euchre.players.teams[0].score = 10
    euchre.players.teams[1].score = 6
    assert euchre.is_game_over() == True

def test_is_game_is_not_over(euchre):
    euchre.players.teams[0].score = 5
    euchre.players.teams[1].score = 7
    assert euchre.is_game_over() == False    