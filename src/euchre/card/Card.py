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

    def suit_effective(self) -> str:
        """
        Determine the effective suit of the card.

        Args:
            trump (str, optional): The trump suit to consider.

        Returns:
            str: The suit considered for trick-taking rules.
        """
        trump = self.trump
        if trump is None:
            return self._suit

        if self.is_left_bower():
            return trump
        return self._suit

    def is_right_bower(self) -> bool:
        """
        Check if this card is the Right Bower (Jack of trump suit).

        Returns:
            bool: True if card is Right Bower; False otherwise.
        """
        return self._rank == "J" and self._suit == self.trump

    def is_left_bower(self) -> bool:
        """
        Check if this card is the Left Bower (Jack of matching color to trump).

        Args:
            trump (str, optional): Trump suit to check against.

        Returns:
            bool: True if card is Left Bower; False otherwise.
        """
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

    def __index__(self):  # pragma: no cover
        """Enable the card to be used in indexed contexts (e.g., arrays)."""
        return self.__int__()
