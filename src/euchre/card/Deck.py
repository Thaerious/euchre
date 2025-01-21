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
        self._trump = None

        for suit in Card.suits:
            for value in Card.values:
                deck.append(Card(self, suit, value))
        super().__init__(deck)  # Pass the full list to the parent class

    @property
    def trump(self):
        return self._trump

    @trump.setter
    def trump(self, trump):
        self._trump = trump

    def get_card(self, suit, value: str | None = None):
        return Card(self, suit, value)

    def shuffle(self) -> "Deck":
        """
        Shuffle the deck in place.

        Returns:
            Deck: The shuffled deck (self).
        """
        random.shuffle(self)
        return self  # Allows method chaining (e.g., deck.shuffle().deal())
