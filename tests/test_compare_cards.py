import pytest

from euchre.card import Card, Deck
from euchre.card.compare_cards import best_card

# ["♠", "♥", "♣", "♦"]

@pytest.mark.parametrize(
    "lead_suit, trump, card1_str, card2_str, expected",
    [
        # Standard cases where one card is trump
        ("♥", "♦", "10♣", "9♣", "10♣"),
        ("♠", "♦", "J♠", "9♣", "J♠"),
        ("♣", "♦", "9♣", "J♦", "J♦"),
        ("♠", "♦", "J♦", "A♦", "J♦"),
        ("♠", "♦", "J♦", "J♥", "J♦"),
        # Cases where lead suit is followed but trump card is played
        ("♠", "♦", "A♠", "J♦", "J♦"),  # J♦ is trump, A♠ is lead suit
        ("♥", "♣", "K♥", "J♣", "J♣"),  # J♣ is trump, K♥ is lead suit
        ("♣", "♠", "Q♣", "J♠", "J♠"),  # J♠ is trump, Q♣ is lead suit
        ("♦", "♥", "10♦", "J♥", "J♥"),  # J♥ is trump, 10♦ is lead suit
        ("♠", "♣", "9♠", "J♣", "J♣"),  # J♣ is trump, 9♠ is lead suit
        # Edge cases with lead or trump as None
        (None, "♦", "J♦", "A♦", "J♦"),
        ("♠", None, "A♠", "K♠", "A♠"),
        (None, None, "A♠", "A♦", "A♠"),
        (None, None, "K♠", "Q♠", "K♠"),
        ("♣", None, "10♣", "9♣", "10♣"),
        (None, "♣", "J♣", "J♠", "J♣"),
        # tie - defaults to left hand side
        ("♠", "♦", "J♦", "J♦", "J♦"),
        ("♠", "♦", "9♣", "9♥", "9♣"),
    ],
)

def test_compare_cards(lead_suit, trump, card1_str, card2_str, expected):
    deck = Deck()
    card1 = Card(deck, card1_str)
    card2 = Card(deck, card2_str)
    if trump is not None:
        deck.trump = trump

    actual = best_card(card1, card2, lead_suit)
    assert actual == Card(deck, expected)
