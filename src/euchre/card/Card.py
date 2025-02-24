from euchre.class_getter import class_getter
from typing import Optional
from .compare_cards import compare_cards

class Card:
    """Represents a single card in Euchre, with suit and rank."""

    # Suits available in Euchre
    @class_getter
    def suits():
        return ["♠", "♥", "♣", "♦"]

    @class_getter
    def ranks():
        return ["9", "10", "J", "Q", "K", "A"]

    # Dictionary to determine the left bower suit (Jack of the same color as trump)
    left_bower_suit: dict[str, str] = {
        "♠": "♣",
        "♣": "♠",
        "♥": "♦",
        "♦": "♥"
    }

    def __init__(self, source, suit: str, rank: str | None = None):
        """
        Initialize a Card object.

        Args:
            suit (str): Either a full card string (e.g., "10♥") or just the suit.
            rank (str, optional): The card rank (e.g., "10"). If not provided, `suit` is parsed as "10♥".
        """

        if not hasattr(source, 'trump'): raise NotImplementedError("Expected attribute 'trump' not found.")
        if suit is None: raise AttributeError("Suit can not be None.")
        self._source = source

        if rank is None:
            # If rank is not provided, assume `suit` is a full card string (e.g., "10♥")
            self._suit = str(suit)[-1]  # Extract suit from last character
            self._rank = str(suit)[:-1]  # Extract rank from all preceding characters
        else:
            self._suit = suit
            self._rank = rank

    @property
    def trump(self):
        return self._source.trump

    @property
    def suit(self):
        return self._suit
    
    @property
    def rank(self):
        return self._rank    

    _normalization_matrix = {
        "♠": {"♠": "♠", "♥": "♥", "♣": "♣", "♦": "♦"},
        "♥": {"♠": "♦", "♥": "♠", "♣": "♥", "♦": "♣"},
        "♣": {"♠": "♣", "♥": "♦", "♣": "♠", "♦": "♥"},
        "♦": {"♠": "♥", "♥": "♣", "♣": "♦", "♦": "♠"}
    }

    def normalize(self):
        """ Return a new normalized card """
        if self.trump is None: return self
        norm_suit = Card._normalization_matrix[self.trump][self.suit]
        return Card(self._source, norm_suit, self.rank)

    def __str__(self) -> str:
        """Return a string representation of the card."""
        return self._rank + self._suit

    def __repr__(self) -> str:
        """Return a formal representation of the card (same as __str__)."""
        return self._rank + self._suit

    def __json__(self):
        return str(self)

    def __eq__(self, that: object) -> bool:
        """
        Check if two cards are equal.

        Args:
            that (object): The card to compare against.

        Returns:
            bool: True if both cards have the same suit and rank, False otherwise.
        """
        if that is None:
            return False
        return str(self) == str(that)

    def __hash__(self) -> int:
        """Return a hash value for the card (useful for sets and dictionaries)."""
        return hash(str(self))
    
    def suit_effective(self, trump = None) -> str:
        """
        Determine the effective suit of the card.

        Args:
            trump (str): The trump suit in the current hand.

        Returns:
            str: The effective suit (adjusts for Left Bower being counted as trump).
        """                
        if trump is None: trump = self.trump
        if trump is None: return self._suit

        if self.is_left_bower(trump):
            return trump  # Left Bower is considered part of the trump suit
        return self._suit   

    def is_right_bower(self, trump = None) -> bool:
        """
        Determine if the card is the Right Bower (Jack of trump suit).

        Args:
            trump (str): The trump suit.

        Returns:
            bool: True if this card is the Right Bower, False otherwise.
        """
        if trump is None: trump = self.trump
        return self._rank == "J" and self._suit == trump

    def is_left_bower(self, trump = None) -> bool:
        """
        Determine if the card is the Left Bower (Jack of the same-color suit as trump).

        Args:
            trump (str): The trump suit.

        Returns:
            bool: True if this card is the Left Bower, False otherwise.
        """
        if trump is None: trump = self.trump
        if trump is None: return False
        return self._rank == "J" and self._suit == Card.left_bower_suit[trump]
    
    def __int__(self):
        b = Card.suits.index(self.suit) << 3
        b = b | Card.ranks.index(self.rank)
        return b
    
    def __index__(self):
        return self.__int__()

def winning_card(lead_suit: str, card1: Card, card2: Card) -> Optional[Card]:
    """
    Determines which card wins in a trick based on suit and rank.
    
    The evaluation follows this priority order:
    1. A trump card beats a non-trump card.
    2. A card following the lead suit beats one that does not.    
    3. The higher-ranked card wins if both are the same suit.
    4. If both are off-suit with the same rank, the result is None (moot).
    
    Args:
        lead_suit (str): The suit that was led in the trick.
        card1 (Card): The first card in play.
        card2 (Card): The second card in play.
    
    Returns:
        Optional[Card]: The winning card, or None if neither wins definitively.
    """
    if card1.is_right_bower(): return card1
    if card2.is_right_bower(): return card2
    if card1.is_left_bower(): return card1
    if card2.is_left_bower(): return card2

    if card1.suit_effective() == card1.trump and card2.suit_effective() != card2.trump:
        return card1
    
    if card1.suit_effective() != card1.trump and card2.suit_effective() == card2.trump:
        return card2

    if card1.suit_effective() == lead_suit and card2.suit_effective() != lead_suit:
        return card1
    
    if card1.suit_effective() != lead_suit and card2.suit_effective() == lead_suit:
        return card2   

    rank1_index = Card.ranks.index(card1.rank)
    rank2_index = Card.ranks.index(card2.rank)
    
    if rank1_index > rank2_index:
        return card1
    
    if rank1_index < rank2_index:
        return card2
    
    return None

def losing_card(lead_suit: str, card1: Card, card2: Card) -> Optional[Card]:
    winner = winning_card(lead_suit, card1, card2)
    if winner == card1: return card2
    if winner == card2: return card1
    return None