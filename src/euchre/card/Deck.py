import random
from euchre.card.Card import Card

class Deck(list):
    """
    Represents a Euchre deck, extending `CardList` to manage a full set of cards.
    """

    def __init__(self):
        """
        Initialize a full Euchre deck (24 cards: 9, 10, J, Q, K, A of each suit).
        """
        deck = []
        for suit in Card.suits:
            for value in Card.values:
                deck.append(Card(suit, value))
        super().__init__(deck)  # Pass the full list to the parent class

    def shuffle(self) -> "Deck":
        """
        Shuffle the deck in place.

        Returns:
            Deck: The shuffled deck (self).
        """
        random.shuffle(self)
        return self  # Allows method chaining (e.g., deck.shuffle().deal())
