from euchre.card.Deck import Deck
from euchre.card.Card import Card

def test_deck_initialization():
    """Test that a newly created deck contains exactly 24 Euchre cards."""
    deck = Deck()
    assert len(deck) == 24, "Deck should have 24 cards"

    # Check that all expected cards are present
    expected_cards = {Card(suit, value) for suit in Card.suits for value in Card.values}
    assert set(deck) == expected_cards, "Deck should contain all Euchre cards"

def test_deck_order():
    """Other tests require the deck to be in a predicatable order."""
    deck = Deck()
    assert deck == ["9♥", "10♥", "J♥", "Q♥", "K♥", "A♥",
                    "9♠", "10♠", "J♠", "Q♠", "K♠", "A♠",
                    "9♣", "10♣", "J♣", "Q♣", "K♣", "A♣",
                    "9♦", "10♦", "J♦", "Q♦", "K♦", "A♦"]

def test_deck_shuffling():
    """Test that shuffling the deck changes the order but keeps the same cards."""
    deck = Deck()
    original_order = deck[:]

    # Shuffle the deck
    deck.shuffle()
    shuffled_order = deck[:]

    assert len(deck) == 24, "Shuffled deck should still have 24 cards"
    assert set(deck) == set(original_order), "Shuffled deck should have the same cards"
    assert shuffled_order != original_order, "Shuffling should change card order"

def test_deck_multiple_shuffles():
    """Test that multiple shuffles produce different orders."""
    deck = Deck()
    deck.shuffle()
    first_shuffle = deck[:]

    deck.shuffle()
    second_shuffle = deck[:]

    assert first_shuffle != second_shuffle, "Two shuffles should produce different orders"

def test_deck_is_cardlist_instance():
    """Test that Deck is an instance of CardList."""
    deck = Deck()
    assert isinstance(deck, list), "Deck should inherit from CardList"

def test_deck_method_chaining():
    """Test that `shuffle()` returns self, allowing method chaining."""
    deck = Deck()
    assert isinstance(deck.shuffle(), Deck), "shuffle() should return the deck instance"
