# test_deck.py
from euchre.card import Card, Deck
import random

def test_deck_initialization():
    """Test that a newly created deck contains exactly 24 Euchre cards."""
    deck = Deck()
    assert len(deck) == 24, "Deck should have 24 cards"

    # Check that all expected cards are present
    expected_cards = {
        deck.get_card(suit, value) for suit in Card.suits for value in Card.ranks
    }
    assert set(deck) == expected_cards, "Deck should contain all Euchre cards"

def test_deck_seed():
    """Test that a newly created deck contains exactly 24 Euchre cards."""
    deck1 = Deck(1234)
    deck2 = Deck(1234)
    
    # new seeded decks are the same before shuffle
    for i in range(len(deck1)):
        assert deck1[i] == deck2[i]

    # decks are the same after shuffle
    deck1.shuffle()
    deck2.shuffle()
    for i in range(len(deck1)):
        assert deck1[i] == deck2[i]

    # using random doesn't affect decks
    deck1.shuffle()
    random.random()
    deck2.shuffle()
    for i in range(len(deck1)):
        assert deck1[i] == deck2[i]


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

    assert (
        first_shuffle != second_shuffle
    ), "Two shuffles should produce different orders"

def test_deck_is_cardlist_instance():
    """Test that Deck is an instance of CardList."""
    deck = Deck()
    assert isinstance(deck, list), "Deck should inherit from CardList"

def test_deck_method_chaining():
    """Test that `shuffle()` returns self, allowing method chaining."""
    deck = Deck()
    assert isinstance(deck.shuffle(), Deck), "shuffle() should return the deck instance"
