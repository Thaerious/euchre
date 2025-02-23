import random
from euchre.card.Card import Card
from .Has_Trump import Has_Trump

class Deck(list, Has_Trump):
    """
    Represents a Euchre deck, extending `CardList` to manage a full set of cards.
    """

    def __init__(self, seed = None):
        """
        Initialize a full Euchre deck (24 cards: 9, 10, J, Q, K, A of each suit).
        """
        Has_Trump.__init__(self)
        self.random = random.Random()
        if seed is not None: self.random.seed(seed)        

        self.reset()

    def get_card(self, suit, value: str | None = None):
        return Card(self, suit, value)

    def reset(self):
        """
        Initialize a full Euchre deck (24 cards: 9, 10, J, Q, K, A of each suit).
        """                
        self.clear()
        self.trump = None

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
