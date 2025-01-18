import pytest
from euchre.card.Hand import Hand
from euchre.card.Card import Card

def test_hand_empty_constructor():
    hand = Hand()
    assert len(hand) == 0

def test_hand_has_suit_present():
    """Test has_suit() returns True when the suit is in hand, considering trump."""
    hand = Hand(["10♠", "J♦", "A♣"])

    assert hand.has_suit(suit="♠", trump="♠") is True, "Hand contains ♠, should return True"
    assert hand.has_suit(suit="♦", trump="♦") is True, "Hand contains ♦, should return True"
    assert hand.has_suit(suit="♣", trump="♣") is True, "Hand contains ♣, should return True"

def test_hand_has_suit_absent():
    """Test has_suit() returns False when the suit is not in hand, considering trump."""
    hand = Hand(["9♦", "K♦", "J♦"])  # Only diamonds

    assert hand.has_suit(suit="♠", trump="♠") is False, "Hand does not contain ♠, should return False"
    assert hand.has_suit(suit="♣", trump="♣") is False, "Hand does not contain ♣, should return False"

def test_hand_has_suit_mixed():
    """Test has_suit() with a mix of suits, considering trump."""
    hand = Hand(["A♥", "9♠", "Q♣"])

    assert hand.has_suit(suit="♠", trump="♠") is True, "Hand contains ♠, should return True"
    assert hand.has_suit(suit="♥", trump="♥") is True, "Hand contains ♥, should return True"
    assert hand.has_suit(suit="♦", trump="♦") is False, "Hand does not contain ♦, should return False"

def test_hand_empty():
    """Test has_suit() with an empty hand, considering trump."""
    hand = Hand([])  # Empty hand

    assert hand.has_suit(suit="♠", trump="♠") is False, "Empty hand should return False"
    assert hand.has_suit(suit="♦", trump="♦") is False, "Empty hand should return False"
    assert hand.has_suit(suit="♣", trump="♣") is False, "Empty hand should return False"

def test_hand_has_all_suits():
    """Test has_suit() when hand contains all four suits, considering trump."""
    hand = Hand(["10♠", "J♦", "A♣", "K♥"])

    assert hand.has_suit(suit="♠", trump="♠") is True, "Hand contains ♠, should return True"
    assert hand.has_suit(suit="♦", trump="♦") is True, "Hand contains ♦, should return True"
    assert hand.has_suit(suit="♣", trump="♣") is True, "Hand contains ♣, should return True"
    assert hand.has_suit(suit="♥", trump="♥") is True, "Hand contains ♥, should return True"

def test_hand_has_suit_with_left_bower():
    """Test has_suit() when the hand contains the Left Bower (acting as trump)."""
    hand = Hand(["J♠"])  # J♠ is the Left Bower if trump is ♣

    assert hand.has_suit(suit="♠", trump="♠") is True, "J♠ should count as ♠ when ♠ is trump"
    assert hand.has_suit(suit="♠", trump="♣") is False, "J♠ should NOT count as ♠ when ♣ is trump"
    assert hand.has_suit(suit="♣", trump="♣") is True, "J♠ should count as ♣ when ♣ is trump"

def test_hand_has_suit_with_only_left_bower():
    """Test has_suit() when the hand only contains the Left Bower, acting as trump."""
    hand = Hand(["J♠"])  # J♠ is the Left Bower if trump is ♣

    assert hand.has_suit(suit="♠", trump="♠") is True, "J♠ should count as ♠ when ♠ is trump"
    assert hand.has_suit(suit="♣", trump="♣") is True, "J♠ should count as ♣ when ♣ is trump"
    assert hand.has_suit(suit="♠", trump="♣") is False, "J♠ should NOT count as ♠ when ♣ is trump"
