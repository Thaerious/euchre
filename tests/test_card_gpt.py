# test_card_gpt.py
import pytest
from euchre.card import Card, HasTrump

# Mock HasTrump class
class MockSource(HasTrump):
    def __init__(self, trump=None):
        self.trump = trump

@pytest.fixture
def mock_source_no_trump():
    return MockSource()

@pytest.fixture
def mock_source_hearts():
    return MockSource(trump="♥")

def test_card_creation_valid(mock_source_no_trump):
    card = Card(mock_source_no_trump, "♠", "J")
    assert card.suit == "♠"
    assert card.rank == "J"
    assert str(card) == "J♠"
    assert repr(card) == "J♠"
    assert int(card) >= 0

def test_card_creation_from_string(mock_source_no_trump):
    card = Card(mock_source_no_trump, "10♦")
    assert card.suit == "♦"
    assert card.rank == "10"

def test_invalid_suit(mock_source_no_trump):
    with pytest.raises(ValueError):
        Card(mock_source_no_trump, "X", "J")

def test_invalid_rank(mock_source_no_trump):
    with pytest.raises(ValueError):
        Card(mock_source_no_trump, "♠", "7")

def test_invalid_source():
    with pytest.raises(TypeError):
        Card(None, "♠", "J")

def test_none_suit(mock_source_no_trump):
    with pytest.raises(AttributeError):
        Card(mock_source_no_trump, None)

def test_normalize_no_trump(mock_source_no_trump):
    card = Card(mock_source_no_trump, "♠", "J")
    assert card.normalize() is card

def test_normalize_with_trump(mock_source_hearts):
    card = Card(mock_source_hearts, "♠", "J")
    norm_card = card.normalize()
    assert norm_card.suit != card.suit  # Normalization changes suit
    assert norm_card.rank == "J"

def test_right_bower(mock_source_hearts):
    right = Card(mock_source_hearts, "♥", "J")
    not_right = Card(mock_source_hearts, "♠", "J")
    assert right.is_right_bower()
    assert not not_right.is_right_bower()

def test_left_bower(mock_source_hearts):
    left = Card(mock_source_hearts, "♦", "J")
    not_left = Card(mock_source_hearts, "♠", "J")
    assert left.is_left_bower()
    assert not not_left.is_left_bower()

def test_left_bower_no_trump(mock_source_no_trump):
    left = Card(mock_source_no_trump, "♦", "J")
    not_left = Card(mock_source_no_trump, "♠", "J")
    assert not left.is_left_bower()
    assert not not_left.is_left_bower()

def test_suit_effective(mock_source_hearts):
    normal = Card(mock_source_hearts, "♥", "9")
    left_bower = Card(mock_source_hearts, "♦", "J")
    assert normal.suit_effective() == "♥"
    assert left_bower.suit_effective() == "♥"  # Left Bower counts as trump

def test_suit_effective_no_trump(mock_source_no_trump):
    normal = Card(mock_source_no_trump, "♥", "9")
    jack_diamonds = Card(mock_source_no_trump, "♦", "J")
    assert normal.suit_effective() == "♥"
    assert jack_diamonds.suit_effective() == "♦"  # Left Bower counts as trump

def test_card_equality(mock_source_no_trump):
    card1 = Card(mock_source_no_trump, "♠", "J")
    card2 = Card(mock_source_no_trump, "J♠")
    card3 = Card(mock_source_no_trump, "♣", "J")
    assert card1 == card2
    assert card1 != card3
    assert card1 != None

def test_card_hash(mock_source_no_trump):
    card = Card(mock_source_no_trump, "♠", "J")
    assert isinstance(hash(card), int)