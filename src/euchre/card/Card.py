# Card.py
from .HasTrump import HasTrump

"""Card module for Euchre.

This module defines the Card class representing Euchre cards,
and helper functions for determining winning and losing cards during play.
"""

class Card:
    """Represents a single card in Euchre, with suit and rank."""

    suits = ["♠", "♥", "♣", "♦"]
    ranks = ["9", "10", "J", "Q", "K", "A"]

    # Maps trump suits to their matching Left Bower suits.
    left_bower_suit: dict[str, str] = {"♠": "♣", "♣": "♠", "♥": "♦", "♦": "♥"}

    _normalization_matrix = {
        "♠": {"♠": "♠", "♥": "♥", "♣": "♣", "♦": "♦"},
        "♥": {"♠": "♦", "♥": "♠", "♣": "♥", "♦": "♣"},
        "♣": {"♠": "♣", "♥": "♦", "♣": "♠", "♦": "♥"},
        "♦": {"♠": "♥", "♥": "♣", "♣": "♦", "♦": "♠"},
    }

    def __init__(self, source: HasTrump, suit: str, rank: str | None = None):
        """
        Initialize a Card.

        Args:
            source (HasTrump): Object that provides a 'trump' attribute (e.g., Game, Hand).
            suit (str): Card suit (e.g., "♠") or full card string (e.g., "J♠") if 'rank' is omitted.
            rank (str, optional): Card rank (e.g., "J", "9"). Defaults to None.

        Raises:
            TypeError: If 'source' does not implement HasTrump.
            AttributeError: If 'suit' is None.
            ValueError: If 'suit' or 'rank' is invalid.
        """

        if not isinstance(source, HasTrump):
            raise TypeError("Paramter 'source' must implement HasTrump.")
        if suit is None:
            raise AttributeError("Parameter 'suit' cannot be None.")

        self._source = source

        if rank is None:
            self._suit = str(suit)[-1]
            self._rank = str(suit)[:-1]
        else:
            self._suit = suit
            self._rank = rank

        if not self._suit in Card.suits:
            raise ValueError(f"Invalid suit: {suit!r}. Must be one of {Card.suits}.")

        if not self._rank in Card.ranks:
            raise ValueError(f"Invalid rank: {rank!r}. Must be one of {Card.ranks}.")

    @property
    def trump(self):
        """Current trump suit as determined by the source."""
        return self._source.trump

    @property
    def suit(self):
        """Suit of the card."""
        return self._suit

    @property
    def rank(self):
        """Rank of the card."""
        return self._rank

    def normalize(self):
        """
        Normalize the card relative to the current trump.

        Returns:
            Card: A new normalized Card object, or self if no trump is set.
        """
        if self.trump is None:
            return self
        norm_suit = Card._normalization_matrix[self.trump][self.suit]
        return Card(self._source, norm_suit, self.rank)

    def __str__(self) -> str:
        """Return a user-friendly string representation of the card."""
        return self._rank + self._suit

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the card."""
        return self._rank + self._suit

    def __json__(self):
        """Serialize the card as a string for JSON output."""
        return str(self)

    def __eq__(self, that: object) -> bool:
        """
        Check if two cards are equal.

        Args:
            that (object): Another object to compare.

        Returns:
            bool: True if suits and ranks match; otherwise False.
        """
        if that is None:
            return False
        return str(self) == str(that)

    def __hash__(self) -> int:
        """Compute a hash based on the card's string representation."""
        return hash(str(self))

    def suit_effective(self, trump=None) -> str:
        """
        Determine the effective suit of the card.

        Args:
            trump (str, optional): The trump suit to consider.

        Returns:
            str: The suit considered for trick-taking rules.
        """
        if trump is None:
            trump = self.trump
        if trump is None:
            return self._suit

        if self.is_left_bower(trump):
            return trump
        return self._suit

    def is_right_bower(self, trump=None) -> bool:
        """
        Check if this card is the Right Bower (Jack of trump suit).

        Args:
            trump (str, optional): Trump suit to check against.

        Returns:
            bool: True if card is Right Bower; False otherwise.
        """
        if trump is None:
            trump = self.trump
        return self._rank == "J" and self._suit == trump

    def is_left_bower(self, trump=None) -> bool:
        """
        Check if this card is the Left Bower (Jack of matching color to trump).

        Args:
            trump (str, optional): Trump suit to check against.

        Returns:
            bool: True if card is Left Bower; False otherwise.
        """
        if trump is None:
            trump = self.trump
        if trump is None:
            return False
        return self._rank == "J" and self._suit == Card.left_bower_suit[trump]

    def __int__(self):
        """
        Convert card to a unique integer based on suit and rank position.

        Returns:
            int: Encoded integer value.
        """
        b = Card.suits.index(self.suit) << 3
        b |= Card.ranks.index(self.rank)
        return b

    def __index__(self):
        """Enable the card to be used in indexed contexts (e.g., arrays)."""
        return self.__int__()

    def beats(self, other: "Card", lead_suit: str) -> bool:
        """
        Determine if this card beats another card based on Euchre rules.

        Args:
            other (Card): The card to compare against.
            lead_suit (str): The lead suit of the trick.

        Returns:
            bool: True if this card beats the other card.
        """
        if self.is_right_bower():
            return True
        if other.is_right_bower():
            return False

        if self.is_left_bower():
            return True
        if other.is_left_bower():
            return False

        if self.suit_effective() == self.trump and other.suit_effective() != self.trump:
            return True
        if self.suit_effective() != self.trump and other.suit_effective() == self.trump:
            return False

        if self.suit_effective() == lead_suit and other.suit_effective() != lead_suit:
            return True
        if self.suit_effective() != lead_suit and other.suit_effective() == lead_suit:
            return False

        rank_self = Card.ranks.index(self.rank)
        rank_other = Card.ranks.index(other.rank)

        return rank_self > rank_other

    def loses_to(self, other: "Card", lead_suit: str) -> bool:
        """
        Determine if this card loses to another card.

        Args:
            other (Card): The card to compare against.
            lead_suit (str): The lead suit of the trick.

        Returns:
            bool: True if this card loses to the other card.
        """
        return not self.beats(other, lead_suit)

def winning_card(lead_suit: str, card1: Card, card2: Card) -> Card | None:
    """
    Determine which card wins between two cards based on Euchre rules.

    Args:
        lead_suit (str): The suit that was led.
        card1 (Card): First card played.
        card2 (Card): Second card played.

    Returns:
        Card | None: The winning card, or None if no winner.
    """
    if card1.is_right_bower():
        return card1
    if card2.is_right_bower():
        return card2
    if card1.is_left_bower():
        return card1
    if card2.is_left_bower():
        return card2

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


def losing_card(lead_suit: str, card1: Card, card2: Card) -> Card | None:
    """
    Determine which card loses between two cards based on Euchre rules.

    Args:
        lead_suit (str): The suit that was led.
        card1 (Card): First card played.
        card2 (Card): Second card played.

    Returns:
        Card | None: The losing card, or None if no loser.
    """
    winner = winning_card(lead_suit, card1, card2)
    if winner == card1:
        return card2
    if winner == card2:
        return card1
    return None
