# test_compare_cards.py
import pytest
from euchre.card.compare_cards import compare_cards, best_card, worst_card
from euchre.card import Card, HasTrump

# Mock HasTrump class
class MockSource(HasTrump):
    def __init__(self, trump=None):
        self.trump = trump

@pytest.fixture
def hearts_trump():
    return MockSource(trump="♥")

@pytest.fixture
def spades_trump():
    return MockSource(trump="♠")

def make_card(trump, rank, suit):
    return Card(MockSource(trump), suit, rank)

def test_compare_cards_same_suit(spades_trump):
    left = Card(spades_trump, "♠", "A")
    right = Card(spades_trump, "♠", "K")
    result = compare_cards(left, right, lead="♠")
    assert result > 0  # A♠ beats K♠

def test_compare_cards_different_suits(spades_trump):
    left = Card(spades_trump, "♠", "9")
    right = Card(spades_trump, "♥", "A")
    result = compare_cards(left, right, lead="♠")
    assert result > 0  # Trump beats non-trump

def test_best_card_trump_vs_nontrump(spades_trump):
    trump_card = Card(spades_trump, "♠", "9")
    normal_card = Card(spades_trump, "♥", "A")
    assert best_card(trump_card, normal_card, lead="♥") == trump_card

def test_best_card_lead_suit_vs_nonlead(hearts_trump):
    lead_card = Card(hearts_trump, "♠", "A")
    non_lead_card = Card(hearts_trump, "♦", "K")
    assert best_card(lead_card, non_lead_card, lead="♠") == lead_card

def test_best_card_higher_rank(hearts_trump):
    card1 = Card(hearts_trump, "♠", "K")
    card2 = Card(hearts_trump, "♠", "Q")
    assert best_card(card1, card2, lead="♠") == card1

def test_best_card_tie(hearts_trump):
    card1 = Card(hearts_trump, "♠", "A")
    card2 = Card(hearts_trump, "♠", "A")
    assert best_card(card1, card2, lead="♠") == card1

def test_worst_card_trump_vs_nontrump(spades_trump):
    trump_card = Card(spades_trump, "♠", "A")
    non_trump_card = Card(spades_trump, "♥", "A")
    assert worst_card(trump_card, non_trump_card, lead="♥") == non_trump_card

def test_worst_card_lower_rank(hearts_trump):
    card1 = Card(hearts_trump, "♠", "9")
    card2 = Card(hearts_trump, "♠", "K")
    assert worst_card(card1, card2, lead="♠") == card1

def test_worst_card_tie(hearts_trump):
    card1 = Card(hearts_trump, "♠", "Q")
    card2 = Card(hearts_trump, "♠", "Q")
    assert worst_card(card1, card2, lead="♠") == card2
