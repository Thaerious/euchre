"""
Deck.py

Deck module for Euchre.

This module defines the Deck class, representing a full Euchre card deck
with methods for resetting, shuffling, and card creation.
"""

import random
from euchre.card.Card import Card
from .HasTrump import HasTrump

class Deck(list, HasTrump):
    """
    Represents a Euchre deck (24 cards: 9, 10, J, Q, K, A of each suit).

    Inherits from `list` to store Card objects and from `HasTrump` to track trump state.
    """

    def __init__(self, seed=None):
        """
        Initialize a new Deck instance.

        Args:
            seed (optional): An optional seed value for reproducible shuffling.
        """
        HasTrump.__init__(self)
        self.random = random.Random()
        if seed is not None:
            self.random.seed(seed)

        self.reset()

    def get_card(self, suit: str, value: str | None = None) -> Card:
        """
        Create a new Card associated with this deck.

        Args:
            suit (str): The card suit (e.g., "♠", "♥", "♣", "♦").
            value (str, optional): The card rank (e.g., "J", "A"). If None, suit must include rank.

        Returns:
            Card: The created Card instance.
        """
        return Card(self, suit, value)

    def reset(self):
        """
        Reset the deck to a full set of Euchre cards (24 cards).

        - Clears the current deck.
        - Resets trump to None.
        - Fills the deck with fresh Card objects.
        """
        self.clear()
        self.trump = None

        for suit in Card.suits:
            for value in Card.ranks:
                self.append(Card(self, suit, value))

    def shuffle(self) -> "Deck":
        """
        Shuffle the deck randomly.

        Returns:
            Deck: The shuffled deck (self).
        """
        self.reset()
        self.random.shuffle(self)
        return self
