from euchre.Euchre import *
from euchre.Game import *
import pytest
from euchre.card.Card import winning_card, losing_card

# ["♠", ♥, "♣", "♦"]

@pytest.mark.parametrize(
    "lead_suit, card1_str, card2_str, trump, expected_str",
    [
        ("♥", "9♥", "9♣", "♠", "9♥"),    # Lead suit beats non-trump off-suit
        ("♦", "10♦", "J♦", "♠", "J♦"),   # Higher rank in the same suit wins
        ("♠", "J♠", "A♠", "♠", "J♠"),    # Right bower beats all trump cards
        ("♠", "9♠", "10♠", "♠", "10♠"),  # Higher-ranked trump wins
        ("♣", "A♣", "J♠", "♠", "J♠"),    # Left bower  beats all other cards
        ("♦", "K♦", "K♣", "♠", "K♦"),    # Lead suit beats off-suit, even if ranks are the same
        ("♠", "9♣", "9♥", "♠", None),    # Identical ranked off-suit cards result in None
    ]
)
def test_winning_card(lead_suit: str, card1_str: str, card2_str: str, trump: str, expected_str: Optional[str]):
    deck = Deck()
    deck.trump = trump
    card1 = deck.get_card(card1_str)
    card2 = deck.get_card(card2_str)
    expected = deck.get_card(expected_str) if expected_str else None
    
    actual = winning_card(lead_suit, card1, card2)
    assert actual == expected

@pytest.mark.parametrize(
    "lead_suit, card1_str, card2_str, trump, expected_str",
    [
        ("♥", "9♥", "9♣", "♠", "9♣"),    # Lead suit beats non-trump off-suit
        ("♦", "10♦", "J♦", "♠", "10♦"),   # Higher rank in the same suit wins
        ("♠", "J♠", "A♠", "♠", "A♠"),    # Right bower beats all trump cards
        ("♠", "9♠", "10♠", "♠", "9♠"),  # Higher-ranked trump wins
        ("♣", "A♣", "J♠", "♠", "A♣"),    # Left bower  beats all other cards
        ("♦", "K♦", "K♣", "♠", "K♣"),    # Lead suit beats off-suit, even if ranks are the same
        ("♠", "9♣", "9♥", "♠", None),    # Identical ranked off-suit cards result in None
    ]
)
def test_losing_card(lead_suit: str, card1_str: str, card2_str: str, trump: str, expected_str: Optional[str]):
    deck = Deck()
    deck.trump = trump
    card1 = deck.get_card(card1_str)
    card2 = deck.get_card(card2_str)
    expected = deck.get_card(expected_str) if expected_str else None
    
    actual = losing_card(lead_suit, card1, card2)
    assert actual == expected


