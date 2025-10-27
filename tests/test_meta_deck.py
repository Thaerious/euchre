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
def deck():
    return MetaDeck()


def test_deal_cards_sets_upcard(deck, players):
    deck.deal_cards(players)
    assert isinstance(deck.up_card, Card)
    for player in players:
        assert len(player.hand) == const.NUM_CARDS_PER_PLAYER


def test_shuffle_clears_all(deck, players):
    deck.deal_cards(players)
    deck.turn_down_card()
    deck.shuffle()
    assert deck.up_card is None
    assert deck.down_card is None
    assert deck.discard is None


def test_set_discard_once_only(deck, players):
    deck.deal_cards(players)
    deck.set_discard(deck.up_card)
    with pytest.raises(EuchreError, match="Discard already set"):
        deck.set_discard(deck.up_card)


def test_turn_down_card_moves_up_to_down(deck, players):
    deck.deal_cards(players)
    up = deck.up_card
    deck.turn_down_card()
    assert deck.up_card is None
    assert deck.down_card == up


def test_turn_down_card_raises_if_discard_set(deck, players):
    deck.deal_cards(players)
    deck.set_discard(deck.up_card)
    with pytest.raises(EuchreError, match="Discard and up_card must be None to turn down."):
        deck.turn_down_card()


def test_make_trump_sets_trump(deck, players):
    deck.deal_cards(players)
    suit = deck.up_card.suit
    deck.trump = suit
    assert deck.trump == suit


def test_make_trump_fails_if_matching_downcard(deck, players):
    deck.deal_cards(players)
    deck.turn_down_card()
    suit = deck.down_card.suit
    with pytest.raises(EuchreError, match="cannot match the down card"):
        deck.trump = suit


def test_deal_cards_fails_with_small_deck():
    deck = MetaDeck()
    deck.pop()
    players = [Player(name, i) for i, name in enumerate(["A", "B", "C", "D"])]
    with pytest.raises(EuchreError, match="Not enough cards in the deck"):
        deck.deal_cards(players)