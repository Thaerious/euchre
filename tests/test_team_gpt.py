# test_team.py
import pytest
from euchre.player import Team


class MockPlayer:
    def __init__(self, name, alone=False, tricks=0):
        self.name = name
        self.alone = alone
        self.tricks = tricks


@pytest.fixture
def players():
    return [
        MockPlayer(name="Alice", alone=False, tricks=2),
        MockPlayer(name="Bob", alone=True, tricks=3),
    ]


@pytest.fixture
def team(players):
    return Team(players)


def test_team_str_and_repr(team):
    expected = "Alice, Bob"
    assert str(team) == expected
    assert repr(team) == expected


def test_team_has_alone_true(team):
    assert team.has_alone is True


def test_team_has_alone_false():
    players = [
        MockPlayer(name="Charlie", alone=False, tricks=1),
        MockPlayer(name="Dana", alone=False, tricks=2),
    ]
    team = Team(players)
    assert team.has_alone is False


def test_team_tricks_sum(team):
    assert team.tricks == 5  # 2 + 3


def test_team_players_copy(team, players):
    copy = team.players
    assert copy == players
    assert copy is not players  # must be a different object


def test_team_score_get_set(team):
    team.score = 10
    assert team.score == 10
    team.score = 20
    assert team.score == 20
