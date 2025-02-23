import random
from euchre.card.Card import Card

class Deck(list):
    """
    Represents a Euchre deck, extending `CardList` to manage a full set of cards.
    """

    def __init__(self, seed = None):
        """
        Initialize a full Euchre deck (24 cards: 9, 10, J, Q, K, A of each suit).
        """
        self.random = random.Random()
        if seed is not None: self.random.seed(seed)
        self.reset()

    @property
    def trump(self):
        return self._trump

    @trump.setter
    def trump(self, trump):
        self._trump = trump

    def get_card(self, suit, value: str | None = None):
        return Card(self, suit, value)

    def reset(self):
        """
        Initialize a full Euchre deck (24 cards: 9, 10, J, Q, K, A of each suit).
        """                
        self.clear()
        self._trump = None

        for suit in Card.suits:
            for value in Card.ranks:
                self.append(Card(self, suit, value))

    def shuffle(self) -> "Deck":
        """
        Shuffle the deck in place.

        Returns:
            Deck: The shuffled deck (self).
        """
        self.reset()
        self.random.shuffle(self)
        return self
