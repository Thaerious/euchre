# Hand.py

"""Hand module for Euchre.

Defines the Hand class, representing a player's set of cards in a Euchre game,
with utilities for suit matching, counting, and selection.
"""

from euchre.card.Card import Card
from euchre.utility.del_string import del_string


class Hand(list):
    """
    Represents a player's hand in Euchre.

    Inherits from Python's list and stores Card objects.
    """

    def normalize(self, source) -> "Hand":
        """
        Normalize all cards in the hand relative to a given source.

        Args:
            source: A context providing a trump attribute (e.g., a Game).

        Returns:
            Hand: A new normalized Hand object.
        """
        norm_hand = Hand()
        for card in self:
            norm_hand.append(card.normalize(source))
        return norm_hand

    def has_suit(self, suit: str) -> bool:
        """
        Check if the hand contains at least one card of the specified effective suit.

        Args:
            suit (str): The suit to check for ("♠", "♥", "♣", or "♦").

        Returns:
            bool: True if the suit is present, False otherwise.

        Example:
            hand.has_suit("♠")
        """
        for card in self:
            if card.suit_effective() == suit:
                return True
        return False

    def count_suit(self, suit: str) -> int:
        """
        Count how many cards in the hand match the specified effective suit.

        Args:
            suit (str): The suit to count ("♠", "♥", "♣", or "♦").

        Returns:
            int: Number of cards matching the suit.

        Example:
            hand.count_suit("♠")
        """
        return len(self.select(values=Card.ranks, suits=[suit]))

    def select(
        self, values: list[str] = Card.ranks, suits: list[str] = Card.suits
    ) -> list[Card]:
        """
        Select cards from the hand that match given values and suits.

        Args:
            values (List[str], optional): List of allowed ranks. Defaults to all ranks.
            suits (List[str], optional): List of allowed suits. Defaults to all suits.

        Returns:
            List[Card]: List of matching cards.
        """
        selected = []
        for card in self:
            if card.suit_effective() not in suits:
                continue
            if card.rank not in values:
                continue
            selected.append(card)

        return selected

    def count(
        self, values: list[str] = Card.ranks, suits: list[str] = Card.suits
    ) -> int:
        """
        Count how many cards match given values and suits.

        Args:
            values (List[str], optional): Allowed ranks. Defaults to all.
            suits (List[str], optional): Allowed suits. Defaults to all.

        Returns:
            int: Number of matching cards.
        """
        return len(self.select(values, suits))

    def __str__(self):
        """Return a human-readable string of the hand."""
        return del_string(self, ",", "'")

    def __repr__(self):
        """Return a formal string representation of the hand."""
        return del_string(self, ",", "'")

    def __json__(self):
        """Serialize the hand to a JSON-friendly string."""
        return str(self)
