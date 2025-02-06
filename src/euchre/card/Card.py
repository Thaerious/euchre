from euchre.class_getter import class_getter

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
        self._source = source

        if rank is None:
            # If rank is not provided, assume `suit` is a full card string (e.g., "10♥")
            self._suit: str = suit[-1]  # Extract suit from last character
            self._rank: str = suit[:-1]  # Extract rank from all preceding characters
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

    def normalize(self, source):
        """ Return a new normalized card """
        if self.trump is None: return Card(source, self.suit, self.rank)

        trump_index = Card.suits.index(self.trump)
        suit_index = Card.suits.index(self.suit)
        norm_index = (suit_index - trump_index) % 4
        norm_suit = Card.suits[norm_index]      
          
        return Card(source, norm_suit, self.rank)

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

    def compare(self, that: "Card", lead: str = None) -> int:
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
        if lead == None:
            lead = self.suit

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
        if self._suit == self.trump and that._suit != self.trump:
            return 1
        if self._suit != self.trump and that._suit == self.trump:
            return -1

        # If both are the same suit (trump or lead), compare by rank
        if self._suit == that._suit:
            selfIndex = Card.ranks.index(self._rank)
            thatIndex = Card.ranks.index(that._rank)
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

