"""
Hand.py

Hand module for Euchre.

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

    def __str__(self):
        """Return a human-readable string of the hand."""
        return del_string(self, ",", "'")

    def __repr__(self):
        """Return a formal string representation of the hand."""
        return del_string(self, ",", "'")

    def __json__(self):
        """Serialize the hand to a JSON-friendly string."""
        return str(self)
