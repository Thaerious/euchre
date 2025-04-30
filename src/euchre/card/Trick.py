# Trick.py

"""Trick module for Euchre.

Defines the Trick class, representing a sequence of played cards in a round,
handling trump suit, winner detection, and card comparison.
"""

from colorama import Fore, Style
from euchre.card import Card
from .compare_cards import best_card
from .HasTrump import HasTrump


class Trick(list[Card], HasTrump):
    """
    Represents a trick in Euchre, tracking cards played and determining the winner.

    Inherits from list (to hold Card objects) and HasTrump (to track trump suit).
    """

    def __init__(self, trump: str, order: list[int]):
        """
        Initialize a Trick.

        Args:
            trump (str): The trump suit for this trick.
            order (list[int]): Player order list (seat indices).
            init (list, optional): List of initial cards to populate the trick.
        """
        super().__init__()
        self._trump: str = trump
        self._order: list[int] = order

    def copy(self) -> "Trick":
        """
        Create a shallow copy of the trick.

        Returns:
            Trick: A new Trick with the same trump and played cards.
        """
        new_trick = Trick(self._trump, self._order)
        new_trick.extend(self)
        return new_trick

    def normalize(self) -> "Trick":
        """
        Return a normalized copy of the trick (normalizes all cards).

        Returns:
            Trick: A new normalized Trick.
        """
        norm_trick = Trick(self._trump, self._order)
        for card in self:
            norm_trick.append(card.normalize(self))
        return norm_trick

    def append(self, card: Card):
        """
        Append a card to the trick.

        Args:
            card (Card): The card to add.
        """
        super().append(Card(self, card))

    @property
    def trump(self) -> str:
        """
        The trump suit for this trick.

        Returns:
            str: Trump suit symbol ("♠", "♥", "♣", "♦").
        """
        return self._trump

    @property
    def lead_suit(self) -> str:
        """
        The effective lead suit of the trick (adjusting for Left Bower).

        Returns:
            str: The lead suit symbol.
        """
        if len(self) == 0: return None
        return self[0].suit_effective()

    @property
    def best_card(self) -> Card | None:
        """
        The currently winning card in the trick.

        Returns:
            Card | None: The best card, or None if trick is empty.
        """
        if not self:
            return None
        best = self[0]
        for card in self[1:]:
            best = best_card(best, card, self.lead_suit)
        return best

    @property
    def winner(self) -> int | None:
        """
        The player index who won the trick.

        Returns:
            int | None: The seat index of the winner, or None if trick is empty.
        """
        best = self.best_card
        if best is None:
            return None
        return self.who_played(best)

    def who_played(self, card: Card) -> int | None:
        """
        The index of the player that played the card

        Args:
            card_in_question (Card): The card to locate.

        Returns:
            int | None: Player seat index who played it, or None if not found.
        """

        if not card in self:
             raise ValueError(f"Card {card} was not played in this trick.")

        for i, card_in_trick in enumerate(self):
            if card_in_trick == card:
                return self._order[i]        

    def __str__(self) -> str:
        """
        Human-readable string showing the trick and highlighting the winning card.

        Returns:
            str: A colored string representing the trick.
        """
        sb = "["

        for i, card in enumerate(self):
            if card == self.best_card:
                sb += Fore.LIGHTGREEN_EX + str(card) + Style.RESET_ALL
            else:
                sb += str(card)

            if i != len(self) - 1:
                sb += ", "

        sb += f"]:{self.trump}"
        return sb

    def __repr__(self) -> str:
        """
        Developer-friendly string showing the trick.

        Returns:
            str: Same as __str__().
        """
        return str(self)