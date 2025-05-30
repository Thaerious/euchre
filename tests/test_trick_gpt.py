# test_trick.py
import pytest
from euchre.card import Card, Trick, HasTrump
from euchre.card.compare_cards import best_card


class MockSource(HasTrump):
    def __init__(self, trump=None):
        self.trump = trump


@pytest.fixture
def player_order():
    return [0, 1, 2, 3]


@pytest.fixture
def trick(player_order):
    return Trick(trump="♠", order=player_order)


def make_card(trump, rank, suit):
    src = MockSource(trump=trump)
    return Card(src, suit, rank)


def test_trick_initialization(trick):
    assert trick.trump == "♠"
    assert trick._order == [0, 1, 2, 3]
    assert len(trick) == 0


def test_trick_append_and_lead_suit(trick):
    card = make_card("♠", "A", "♠")
    trick.append(card)
    assert len(trick) == 1
    assert trick.lead_suit == "♠"


def test_trick_copy(trick):
    card = make_card("♠", "K", "♠")
    trick.append(card)
    copied = trick.copy()
    assert isinstance(copied, Trick)
    assert copied.trump == trick.trump
    assert copied._order == trick._order
    assert len(copied) == len(trick)
    assert str(copied[0]) == str(trick[0])
    assert copied is not trick  # different objects


def test_trick_best_card(trick):
    trick.append(make_card("♠", "9", "♠"))
    trick.append(make_card("♠", "A", "♠"))
    best = trick.best_card
    assert best.rank == "A"


def test_trick_winner(trick):
    trick.append(make_card("♠", "9", "♠"))  # seat 0
    trick.append(make_card("♠", "A", "♠"))  # seat 1
    winner = trick.winner
    assert winner == 1


def test_trick_who_played(trick):
    c1 = make_card("♠", "9", "♠")
    c2 = make_card("♠", "A", "♠")
    trick.append(c1)
    trick.append(c2)
    assert trick.who_played(c2) == 1
    assert trick.who_played(c1) == 0


def test_trick_empty_best_and_winner(trick):
    assert trick.best_card is None
    assert trick.winner is None


def test_trick_str_highlight(trick):
    trick.append(make_card("♠", "9", "♠"))
    trick.append(make_card("♠", "A", "♠"))
    out = str(trick)
    assert "[9♠," in out
    assert "A♠" in out  # A♠ should be highlighted
    assert ":♠" in out  # Trump suit shown


def test_trick_repr(trick):
    trick.append(make_card("♠", "9", "♠"))
    assert repr(trick) == str(trick)
