from euchre.class_getter import class_getter

class Card:
    """Represents a single card in Euchre, with suit and value."""

    # Suits available in Euchre
    @class_getter
    def suits():
        return ["♥", "♠", "♣", "♦"]

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

    def __init__(self, deck, suit: str, value: str | None = None):
        """
        Initialize a Card object.

        Args:
            suit (str): Either a full card string (e.g., "10♥") or just the suit.
            value (str, optional): The card value (e.g., "10"). If not provided, `suit` is parsed as "10♥".
        """

        if isinstance(deck, str): raise Exception("Sanity Check Failed")

        self._deck = deck

        if value is None:
            # If value is not provided, assume `suit` is a full card string (e.g., "10♥")
            self._suit: str = suit[-1]  # Extract suit from last character
            self._value: str = suit[:-1]  # Extract value from all preceding characters
        else:
            self._suit = suit
            self._value = value

    @property
    def suit(self):
        return self._suit
    
    @property
    def rank(self):
        return self._value    

    @property
    def deck(self):
        return self._deck

    def __str__(self) -> str:
        """Return a string representation of the card."""
        return self._value + self._suit

    def __repr__(self) -> str:
        """Return a formal representation of the card (same as __str__)."""
        return self._value + self._suit

    def __eq__(self, that: object) -> bool:
        """
        Check if two cards are equal.

        Args:
            that (object): The card to compare against.

        Returns:
            bool: True if both cards have the same suit and value, False otherwise.
        """
        if that is None:
            return False
        if isinstance(that, str):
            that = self.deck.get_card(that)
        if not isinstance(that, Card):
            return False
        return self._suit == that._suit and self._value == that._value

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
        if trump is None: return self._suit
        if self.is_left_bower(trump):
            return self._deck.trump  # Left Bower is considered part of the trump suit
        return self._suit

    def compare(self, that: "Card", lead: str) -> int:
        """
        Compare two cards and determine the winner.

        Assumes `self` was played first.

        Args:
            that (Card): The second card to compare against.
            lead (str): The suit that was led in the trick.

        Returns:
            int: 
                - `1` if `self` wins.
                - `-1` if `that` wins.
                - `0` if it's a tie (neither follows lead or is trump).
        """
        # If both cards are the same, `self` wins (played first)
        if self == that:
            return 1

        # Right Bower (Jack of trump) always wins
        if self.is_right_bower():
            return 1
        if that.is_right_bower():
            return -1

        # Left Bower (Jack of same-color suit as trump) wins against non-bowers
        if self.is_left_bower():
            return 1
        if that.is_left_bower():
            return -1

        # Trump suit always wins over non-trump
        if self._suit == self._deck.trump and that._suit != self._deck.trump:
            return 1
        if self._suit != self._deck.trump and that._suit == self._deck.trump:
            return -1

        # If both are the same suit (trump or lead), compare by value
        if self._suit == that._suit:
            selfIndex = Card.ranks.index(self._value)
            thatIndex = Card.ranks.index(that._value)
            return 1 if selfIndex > thatIndex else -1

        # If one follows lead and the other does not, lead suit wins
        if self._suit == lead and that._suit != lead:
            return 1
        if that._suit == lead and self._suit != lead:
            return -1

        # If neither follows lead or is trump, it's a tie
        return 0

    def is_right_bower(self, trump = None) -> bool:
        """
        Determine if the card is the Right Bower (Jack of trump suit).

        Args:
            trump (str): The trump suit.

        Returns:
            bool: True if this card is the Right Bower, False otherwise.
        """
        if trump is None: trump = self.deck.trump
        return self._value == "J" and self._suit == trump

    def is_left_bower(self, trump = None) -> bool:
        """
        Determine if the card is the Left Bower (Jack of the same-color suit as trump).

        Args:
            trump (str): The trump suit.

        Returns:
            bool: True if this card is the Left Bower, False otherwise.
        """
        if trump is None: trump = self.deck.trump
        return self._value == "J" and self._suit == Card.left_bower_suit[trump]