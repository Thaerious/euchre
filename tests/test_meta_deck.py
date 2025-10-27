import pytest
from euchre.MetaDeck import MetaDeck
from euchre.card.Deck import Deck
from euchre.card.Card import Card
from euchre.player.Player import Player
from euchre.EuchreError import EuchreError
import euchre.constants as const

@pytest.fixture
def players():
    return [Player(name, i) for i, name in enumerate(["A", "B", "C", "D"])]

@pytest.fixture
def manager():
    return MetaDeck()


def test_deal_cards_sets_upcard(manager, players):
    manager.deal_cards(players)
    assert isinstance(manager.up_card, Card)
    for player in players:
        assert len(player.hand) == const.NUM_CARDS_PER_PLAYER


def test_shuffle_clears_all(manager, players):
    manager.deal_cards(players)
    manager.turn_down_card()
    manager.shuffle()
    assert manager.up_card is None
    assert manager.down_card is None
    assert manager.discard is None


def test_set_discard_once_only(manager, players):
    manager.deal_cards(players)
    manager.set_discard(manager.up_card)
    with pytest.raises(EuchreError, match="Discard already set"):
        manager.set_discard(manager.up_card)


def test_turn_down_card_moves_up_to_down(manager, players):
    manager.deal_cards(players)
    up = manager.up_card
    manager.turn_down_card()
    assert manager.up_card is None
    assert manager.down_card == up


def test_turn_down_card_raises_if_discard_set(manager, players):
    manager.deal_cards(players)
    manager.set_discard(manager.up_card)
    with pytest.raises(EuchreError, match="Discard must be None to turn down"):
        manager.turn_down_card()


def test_make_trump_sets_trump(manager, players):
    manager.deal_cards(players)
    suit = manager.up_card.suit
    manager.make_trump(suit)
    assert manager.trump == suit


def test_make_trump_fails_if_matching_downcard(manager, players):
    manager.deal_cards(players)
    manager.turn_down_card()
    suit = manager.down_card.suit
    with pytest.raises(EuchreError, match="Trump can not match the down card"):
        manager.make_trump(suit)


def test_deal_cards_fails_with_small_deck():
    manager = MetaDeck()
    manager.pop()
    players = [Player(name, i) for i, name in enumerate(["A", "B", "C", "D"])]
    with pytest.raises(EuchreError, match="Not enough cards in the deck to deal"):
        manager.deal_cards(players)