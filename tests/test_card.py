from euchre.card.Deck import Deck
from euchre.card.Card import Card
import pytest

@pytest.fixture
def deck():
    return Deck()

def test_string_builder(deck):
    card = deck.get_card("10♠")
    assert card.suit == "♠"
    assert card.rank== "10"
    
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

def test_equality_with_None(deck):
    card0 = deck.get_card("♠", "10")
    assert card0 != None

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
    deck.trump =  '♦'
    card = deck.get_card('A♦')
    assert card.suit_effective() == deck.trump
    
def test_suit_effective_neq(deck):
    deck.trump =  '♠'
    card = deck.get_card('A♦')
    assert card.suit_effective() != deck.trump

def test_suit_effective_rb(deck):
    deck.trump =  '♠'
    card = deck.get_card('J♠')
    assert card.suit_effective() == deck.trump

def test_suit_effective_lb_1(deck):
    deck.trump =  '♠'
    card = deck.get_card('J♣')
    assert card.suit_effective() == deck.trump

def test_suit_effective_lb_2(deck):
    deck.trump =  '♣'
    card = deck.get_card('J♠')
    assert card.suit_effective() == deck.trump

def test_to_str(deck):
    card = deck.get_card('J♣')
    assert str(card) == 'J♣'

def test_repr(deck):
    card = deck.get_card('J♣')
    assert card.__repr__() == 'J♣'

def test_hash_equal(deck):
    card1 = deck.get_card('J♣')
    card2 = deck.get_card('J♣')
    assert card1.__hash__() == card2.__hash__()

def test_hash_not_equal(deck):
    card1 = deck.get_card('J♣')
    card2 = deck.get_card('J♠')
    assert card1.__hash__() != card2.__hash__()    

# Same card returns 1
def test_compare_same_card(deck):
    card1 = deck.get_card('J♠')  # Right Bower (Trump Jack)
    assert card1.compare(card1, lead='♠') == 1  # Right Bower wins

# Right Bower (J of Trump) always wins
def test_compare_right_bower_vs_non_trump(deck):
    deck.trump = "♠"
    card1 = deck.get_card('J♠')  # Right Bower (Trump Jack)
    card2 = deck.get_card('A♠')  # Non-trump Ace
    assert card1.compare(card2, lead='♠') == 1  # Right Bower wins

def test_compare_non_trump_vs_right_bower(deck):
    deck.trump = "♠"
    card1 = deck.get_card('A♠')  # Non-trump Ace
    card2 = deck.get_card('J♠')  # Right Bower (Trump Jack)
    assert card1.compare(card2, lead='♠') == -1  # Right Bower wins

# Left Bower (J of same-color suit as trump) beats everything except Right Bower
def test_compare_left_bower_vs_non_trump(deck):
    deck.trump = "♠"
    card1 = deck.get_card('J♣')  # Left Bower
    card2 = deck.get_card('A♠')  # Non-trump Ace
    assert card1.compare(card2, lead='♠') == 1  # Left Bower wins

def test_compare_non_trump_vs_left_bower(deck):
    deck.trump = "♠"
    card1 = deck.get_card('A♠')  # Non-trump Ace
    card2 = deck.get_card('J♣')  # Left Bower
    assert card1.compare(card2, lead='♠') == -1  # Left Bower wins

def test_compare_left_bower_vs_right_bower(deck):
    deck.trump = "♠"
    card1 = deck.get_card('J♣')  # Left Bower
    card2 = deck.get_card('J♠')  # Right Bower
    assert card1.compare(card2, lead='♠') == -1  # Right Bower wins

def test_compare_right_bower_vs_left_bower(deck):
    deck.trump = "♠"
    card1 = deck.get_card('J♠')  # Right Bower
    card2 = deck.get_card('J♣')  # Left Bower
    assert card1.compare(card2, lead='♠') == 1  # Right Bower wins

# Any trump card beats any non-trump card
def test_compare_trump_vs_non_trump(deck):
    deck.trump = "♦"
    card1 = deck.get_card('9♦')  # Trump suit
    card2 = deck.get_card('K♠')  # Non-trump
    assert card1.compare(card2, lead='♠') == 1  # Trump wins

def test_compare_non_trump_vs_trump(deck):
    deck.trump = "♦"
    card1 = deck.get_card('K♠')  # Non-trump
    card2 = deck.get_card('9♦')  # Trump suit
    assert card1.compare(card2, lead='♠') == -1  # Trump wins

def test_compare_high_trump_vs_low_trump(deck):
    deck.trump = "♦"
    card1 = deck.get_card('A♦')  # High trump
    card2 = deck.get_card('9♦')  # Low trump
    assert card1.compare(card2, lead='♠') == 1  # Higher trump wins

def test_compare_low_trump_vs_high_trump(deck):
    deck.trump = "♦"
    card1 = deck.get_card('9♦')  # Low trump
    card2 = deck.get_card('A♦')  # High trump
    assert card1.compare(card2, lead='♠') == -1  # Higher trump wins

# Lead suit wins over a non-lead, non-trump card
def test_compare_lead_vs_non_lead(deck):
    deck.trump = "♥"
    card1 = deck.get_card('10♠')  # Lead suit
    card2 = deck.get_card('K♦')   # Not lead, not trump
    assert card1.compare(card2, lead='♠') == 1  # Lead wins

def test_compare_non_lead_vs_lead(deck):
    deck.trump = "♥"
    card1 = deck.get_card('K♦')   # Not lead, not trump
    card2 = deck.get_card('10♠')  # Lead suit
    assert card1.compare(card2, lead='♠') == -1  # Lead wins

# If both cards follow lead, highest wins
def test_compare_both_follow_lead(deck):
    deck.trump = "♦"
    card1 = deck.get_card('K♠')  # Lead suit
    card2 = deck.get_card('10♠')  # Lower-ranked lead suit
    assert card1.compare(card2, lead='♠') == 1  # Higher card wins

def test_compare_both_follow_lead_low_vs_high(deck):
    deck.trump = "♦"
    card1 = deck.get_card('10♠')  # Lower-ranked lead suit
    card2 = deck.get_card('K♠')  # Lead suit
    assert card1.compare(card2, lead='♠') == -1  # Higher card wins

# If neither follows suit and neither is trump, it's a tie (0)
def test_compare_both_off_suit_neither_trump(deck):
    deck.trump = "♦"
    card1 = deck.get_card('Q♥')  # Off-suit, not lead or trump
    card2 = deck.get_card('10♣')  # Off-suit, not lead or trump
    assert card1.compare(card2, lead='♠') == 0  # Neither follows lead or is trump → Tie

def test_compare_both_off_suit_neither_trump_different_order(deck):
    deck.trump = "♦"
    card1 = deck.get_card('10♣')  # Off-suit, not lead or trump
    card2 = deck.get_card('Q♥')  # Off-suit, not lead or trump
    assert card1.compare(card2, lead='♠') == 0  # Neither follows lead or is trump → Tie

def test_compare_no_lead_no_trump(deck):
    deck.trump = None
    card1 = deck.get_card('10♣')  # Off-suit, not lead or trump
    card2 = deck.get_card('Q♥')  # Off-suit, not lead or trump
    assert card1.compare(card2, lead=None) == -1  # Neither follows lead or is trump → Tie

def test_effective_suit_trump_not_set_j(deck):
    card1 = deck.get_card('J♣')
    assert card1.suit_effective() == '♣'

def test_effective_suit_override_trump_not_set(deck):
    card1 = deck.get_card('J♣')
    assert card1.suit_effective('♠') == '♠'    

def test_effective_suit_override_trump_set(deck):
    deck.trump = "♦"
    card1 = deck.get_card('J♣')
    assert card1.suit_effective('♠') == '♠'        

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
    ]
)
def test_normalize(suit, trump, expected_suit):
    """Test that normalize correctly converts suits based on trump."""
    deck = Deck()
    deck.trump = trump
    card = Card(deck, suit, "10")
    normalized = card.normalize()

    print(f"{suit} {trump} {expected_suit}")

    assert normalized.suit == expected_suit, f"Expected {expected_suit}, got {normalized.suit}"
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
