import pytest
from euchre.PlayerManager import PlayerManager
from euchre.player import Player
from euchre.EuchreError import EuchreError


class DummyTrump:
    def __init__(self, trump=None):
        self.trump = trump


@pytest.fixture
def manager():
    return PlayerManager(["A", "B", "C", "D"], DummyTrump("♠"))


def test_initial_order(manager):
    assert manager.order == [0, 1, 2, 3]


def test_lead_player_on_new_instance(manager):
    assert isinstance(manager.lead_player, Player)
    assert manager.lead_player.name == "A"


def test_dealer_on_new_instance(manager):
    assert isinstance(manager.dealer, Player)
    assert manager.dealer.name == "D"

def test_activate_dealer(manager):
    manager.activate_dealer()
    assert manager.current_player.name == "D"


def test_activate_first_player(manager):
    manager.activate_dealer()
    manager.activate_first_player()
    assert manager.current_player.name == "A"


def test_reset_lead_player(manager):
    manager.activate_dealer()
    manager.reset_lead_player()
    assert manager.lead_player.name == "D"


def test_go_alone_removes_partner(manager):
    manager.activate_first_player()  # player "A", index 0
    manager.go_alone()
    assert manager.current_player.alone is True
    assert 2 not in manager.order  # partner index is 2


def test_go_alone_without_trump():
    pm = PlayerManager(["A", "B", "C", "D"], DummyTrump(trump=None))
    with pytest.raises(EuchreError):
        pm.go_alone()


def test_get_player_by_index(manager):
    assert manager.get_player(1).name == "B"


def test_get_player_by_name(manager):
    assert manager.get_player("C").name == "C"


def test_get_player_invalid_name(manager):
    with pytest.raises(ValueError):
        manager.get_player("Z")


def test_get_player_none(manager):
    with pytest.raises(TypeError):
        manager.get_player(None)


def test_invalid_constructor_param():
    with pytest.raises(TypeError):
        PlayerManager(["A", "B", "C", "D"], has_trump=object())

def test_rotate(manager):
    manager.rotate()
    assert manager.order == [1, 2, 3, 0]
    assert manager.dealer.name == "A"
    assert manager.lead_player.name == "B"
    assert manager.current_player.name == "B"
