# test_trick_full_round.py
import pytest
from euchre.card import Card, Trick, HasTrump

class MockSource(HasTrump):
    def __init__(self, trump=None):
        self.trump = trump

def make_card(trump, rank, suit):
    return Card(MockSource(trump), suit, rank)

@pytest.fixture
def player_order():
    return [0, 1, 2, 3]

def test_full_trick_simulation(player_order):
    # Trump is hearts
    trick = Trick(trump="♥", order=player_order)

    # Seat 0 leads with 9♠ (non-trump)
    trick.append(make_card("♥", "9", "♠"))
    # Seat 1 plays A♠ (same suit, higher)
    trick.append(make_card("♥", "A", "♠"))
    # Seat 2 plays 10♥ (trump, beats everything)
    trick.append(make_card("♥", "10", "♥"))
    # Seat 3 plays K♠ (good card but not trump)

    trick.append(make_card("♥", "K", "♠"))

    # Who wins?
    best = trick.best_card
    winner = trick.winner

    # 10♥ should win because it's trump
    assert str(best) == "10♥"
    assert winner == 2  # Seat 2 played it

@pytest.fixture
def player_order():
    return [0, 1, 2, 3]

def test_trump_beats_nontrump(player_order):
    trick = Trick(trump="♠", order=player_order)

    trick.append(make_card("♠", "A", "♥"))  # Seat 0, non-trump A♥
    trick.append(make_card("♠", "9", "♣"))  # Seat 1, non-trump
    trick.append(make_card("♠", "9", "♠"))  # Seat 2, trump!
    trick.append(make_card("♠", "K", "♥"))  # Seat 3, non-trump

    best = trick.best_card
    winner = trick.winner

    assert str(best) == "9♠"
    assert winner == 2

def test_higher_trump_beats_lower_trump(player_order):
    trick = Trick(trump="♠", order=player_order)

    trick.append(make_card("♠", "9", "♠"))  # Seat 0
    trick.append(make_card("♠", "A", "♠"))  # Seat 1
    trick.append(make_card("♠", "K", "♠"))  # Seat 2
    trick.append(make_card("♠", "Q", "♠"))  # Seat 3

    best = trick.best_card
    winner = trick.winner

    assert str(best) == "A♠"
    assert winner == 1

def test_left_bower_beats_normal_trump(player_order):
    trick = Trick(trump="♥", order=player_order)

    trick.append(make_card("♥", "A", "♥"))  # Seat 0 - A♥ (trump)
    trick.append(make_card("♥", "J", "♦"))  # Seat 1 - Left Bower (counts as ♥)
    trick.append(make_card("♥", "Q", "♥"))  # Seat 2
    trick.append(make_card("♥", "K", "♥"))  # Seat 3

    best = trick.best_card
    winner = trick.winner

    assert str(best) == "J♦"
    assert winner == 1

def test_lead_suit_beats_nonlead_when_no_trump(player_order):
    trick = Trick(trump=None, order=player_order)

    trick.append(make_card(None, "9", "♣"))  # Seat 0 - lead
    trick.append(make_card(None, "A", "♠"))  # Seat 1 - non-lead
    trick.append(make_card(None, "K", "♥"))  # Seat 2 - non-lead
    trick.append(make_card(None, "10", "♣")) # Seat 3 - lead suit

    best = trick.best_card
    winner = trick.winner

    assert str(best) == "10♣"
    assert winner == 3

def test_no_trump_highest_card_of_lead_suit(player_order):
    trick = Trick(trump=None, order=player_order)

    trick.append(make_card(None, "Q", "♣"))  # Seat 0 - Q♣
    trick.append(make_card(None, "A", "♣"))  # Seat 1 - A♣
    trick.append(make_card(None, "K", "♣"))  # Seat 2 - K♣
    trick.append(make_card(None, "9", "♣"))  # Seat 3 - 9♣

    best = trick.best_card
    winner = trick.winner

    assert str(best) == "A♣"
    assert winner == 1