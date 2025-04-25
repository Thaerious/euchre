import pytest

from euchre.card import Card, Deck


@pytest.fixture
def deck():
    return Deck()

def test_string_builder(deck):
    card = deck.get_card("10♠")
    assert card.suit == "♠"
    assert card.rank == "10"

def test_equality_with_string(deck):
    card = deck.get_card("J♦")
    assert card == "J♦"

def test_equality_card_object_true(deck):
    card0 = deck.get_card("♠", "10")
    card1 = deck.get_card("♠", "10")
    assert card0 == card1

def test_equality_card_object_false(deck):
    card0 = deck.get_card("♠", "10")
    card1 = deck.get_card("♠", "9")
    assert card0 != card1

def test_equality_with_none(deck):
    card0 = deck.get_card("♠", "10")
    assert card0 is not None

def test_equality_with_string_true(deck):
    card0 = deck.get_card("♠", "10")
    assert card0 == "10♠"

def test_equality_with_string_false(deck):
    card0 = deck.get_card("♠", "10")
    assert card0 != "10♦"

def test_equality_with_not_card(deck):
    card0 = deck.get_card("♠", "10")
    assert card0 != []

def test_suit_effective_eq(deck):
    deck.trump = "♦"
    card = deck.get_card("A♦")
    assert card.suit_effective() == deck.trump

def test_suit_effective_neq(deck):
    deck.trump = "♠"
    card = deck.get_card("A♦")
    assert card.suit_effective() != deck.trump

def test_suit_effective_rb(deck):
    deck.trump = "♠"
    card = deck.get_card("J♠")
    assert card.suit_effective() == deck.trump

def test_suit_effective_lb_1(deck):
    deck.trump = "♠"
    card = deck.get_card("J♣")
    assert card.suit_effective() == deck.trump

def test_suit_effective_lb_2(deck):
    deck.trump = "♣"
    card = deck.get_card("J♠")
    assert card.suit_effective() == deck.trump

def test_to_str(deck):
    card = deck.get_card("J♣")
    assert str(card) == "J♣"

def test_repr(deck):
    card = deck.get_card("J♣")
    assert card.__repr__() == "J♣"

def test_hash_equal(deck):
    card1 = deck.get_card("J♣")
    card2 = deck.get_card("J♣")
    assert card1.__hash__() == card2.__hash__()

def test_hash_not_equal(deck):
    card1 = deck.get_card("J♣")
    card2 = deck.get_card("J♠")
    assert card1.__hash__() != card2.__hash__()

def test_effective_suit_trump_not_set_j(deck):
    card1 = deck.get_card("J♣")
    assert card1.suit_effective() == "♣"

def test_effective_suit_override_trump_not_set(deck):
    card1 = deck.get_card("J♣")
    assert card1.suit_effective("♠") == "♠"

def test_effective_suit_override_trump_set(deck):
    deck.trump = "♦"
    card1 = deck.get_card("J♣")
    assert card1.suit_effective("♠") == "♠"

@pytest.mark.parametrize(
    "suit, trump, expected_suit",
    [
        ("♠", "♠", "♠"),  # Same suit as trump remains unchanged
        ("♥", "♠", "♥"),
        ("♣", "♠", "♣"),
        ("♦", "♠", "♦"),
        ("♠", "♥", "♦"),  # When trump is ♥, ♠ → ♦
        ("♥", "♥", "♠"),  # Trump suit itself normalizes to ♠
        ("♣", "♥", "♥"),
        ("♦", "♥", "♣"),
        ("♠", "♣", "♣"),  # When trump is ♣
        ("♥", "♣", "♦"),
        ("♣", "♣", "♠"),
        ("♦", "♣", "♥"),
        ("♠", "♦", "♥"),  # When trump is ♦
        ("♥", "♦", "♣"),
        ("♣", "♦", "♦"),
        ("♦", "♦", "♠"),
    ],
)
def test_normalize(suit, trump, expected_suit):
    """Test that normalize correctly converts suits based on trump."""
    deck = Deck()
    deck.trump = trump
    card = Card(deck, suit, "10")
    normalized = card.normalize()

    print(f"{suit} {trump} {expected_suit}")

    assert (
        normalized.suit == expected_suit
    ), f"Expected {expected_suit}, got {normalized.suit}"
    assert normalized.rank == "10"  # Rank should remain unchanged
    assert normalized._source == deck  # Source should be preserved

# def test_normalize_no_trump():
#     """Test normalization when no trump is set (should remain unchanged)."""
#     deck = Deck()
#     deck.trump = trump
#     card = Card(deck, suit, "10")
#     normalized = card.normalize()

#     assert normalized.suit == "♠"
#     assert normalized.rank == "10"
#     assert normalized._source == deck
