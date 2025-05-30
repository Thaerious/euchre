# test_hand.py
import pytest

from euchre.card import Card, Deck, Hand


def build_hand(cards):
    deck = Deck()
    deck.trump = "♠"
    hand = Hand()

    for card in cards:
        if isinstance(card, Card):
            hand.append(card)
        else:
            hand.append(deck.get_card(card))

    return hand


def test_hand_has_suit_present():
    """Test has_suit() returns True when the suit is in hand, considering trump."""
    hand = build_hand(["10♠", "J♦", "A♣"])

    assert hand.has_suit(suit="♠") is True, "Hand contains ♠, should return True"
    assert hand.has_suit(suit="♦") is True, "Hand contains ♦, should return True"
    assert hand.has_suit(suit="♣") is True, "Hand contains ♣, should return True"


def test_hand_has_suit_absent():
    """Test has_suit() returns False when the suit is not in hand, considering trump."""
    hand = build_hand(["9♦", "K♦", "J♦"])  # Only diamonds

    assert (
        hand.has_suit(suit="♠") is False
    ), "Hand does not contain ♠, should return False"
    assert (
        hand.has_suit(suit="♣") is False
    ), "Hand does not contain ♣, should return False"


def test_hand_has_suit_mixed():
    """Test has_suit() with a mix of suits, considering trump."""
    hand = build_hand(["A♥", "9♠", "Q♣"])

    assert hand.has_suit(suit="♠") is True, "Hand contains ♠, should return True"
    assert hand.has_suit(suit="♥") is True, "Hand contains ♥, should return True"
    assert (
        hand.has_suit(suit="♦") is False
    ), "Hand does not contain ♦, should return False"


def test_hand_empty():
    """Test has_suit() with an empty hand, considering trump."""
    hand = build_hand([])  # Empty hand

    assert hand.has_suit(suit="♠") is False, "Empty hand should return False"
    assert hand.has_suit(suit="♦") is False, "Empty hand should return False"
    assert hand.has_suit(suit="♣") is False, "Empty hand should return False"


def test_hand_has_all_suits():
    """Test has_suit() when hand contains all four suits, considering trump."""
    hand = build_hand(["10♠", "J♦", "A♣", "K♥"])

    assert hand.has_suit(suit="♠") is True, "Hand contains ♠, should return True"
    assert hand.has_suit(suit="♦") is True, "Hand contains ♦, should return True"
    assert hand.has_suit(suit="♣") is True, "Hand contains ♣, should return True"
    assert hand.has_suit(suit="♥") is True, "Hand contains ♥, should return True"


def test_hand_has_suit_with_only_left_bower():
    """Test has_suit() when the hand contains the Left Bower (acting as trump)."""
    hand = build_hand(["J♣"])  # J♣ is the Left Bower if trump is ♠

    assert hand.has_suit(suit="♠") is True, "J♣ should count as ♠ when ♠ is trump"


@pytest.mark.parametrize(
    "cards, values, suits, expected",
    [
        # Test Case 1: Count all valid cards matching both suit and value
        (
            ["J♠", "J♦", "10♠", "A♣", "Q♠"],
            ["9", "10", "J", "Q", "K", "A"],
            ["♥", "♠", "♣", "♦"],
            5,
        ),
        (["J♠", "J♦", "10♠", "A♣", "Q♠"], ["10", "J", "Q"], ["♠", "♦"], 4),
        # Test Case 2: No matching cards in hand
        (["9♠", "K♦", "A♣", "Q♠"], ["10", "J"], ["♥"], 0),
        (["J♠", "J♦", "10♠", "A♣", "Q♠"], ["9", "10", "J", "Q", "K", "A"], ["♥"], 0),
        # Test Case 3: Only counting trump suit cards
        (["J♠", "J♦", "10♠", "A♣", "Q♠"], ["J", "Q"], ["♠"], 2),
        (["J♠", "J♣", "10♠", "A♣", "Q♠"], ["J", "Q"], ["♠"], 3),
        # Test Case 4: Handling an empty hand
        ([], ["J", "Q"], ["♠"], 0),
        # Test Case 5: Only counting face cards (J, Q, K, A) in a specific suit
        (["J♠", "10♠", "A♠", "9♠", "Q♠"], ["J", "Q", "K", "A"], ["♠"], 3),
        # Test Case 6: Only counting number cards (9, 10) in a specific suit
        (["J♠", "10♠", "A♠", "9♠", "Q♠"], ["9", "10"], ["♠"], 2),
        # Test Case 7: Hand contains all possible values, counting only certain ones
        (["9♠", "10♠", "J♠", "Q♠", "K♠", "A♠"], ["J", "Q", "K"], ["♠"], 3),
        # Test Case 8: Including Left Bower (Left Jack as part of trump suit)
        (
            ["J♠", "J♣", "10♠", "A♣", "Q♠"],
            ["J"],
            ["♠"],
            2,
        ),  # Right Bower (J♠) & Left Bower (J♣)
        # Test Case 9: Checking mixed suits with specific value selections
        (
            ["J♠", "J♦", "9♦", "9♠", "9♥"],
            ["9", "J"],
            ["♠", "♥"],
            3,
        ),  # Includes J♠, J♦, and 9♥
    ],
)
def test_hand_select(cards, values, suits, expected):
    hand = build_hand(cards)
    assert len(hand.select(values, suits)) == expected
