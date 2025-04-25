# Trick.py
from colorama import Fore, Style

from euchre.card import Card

from .compare_cards import best_card
from .HasTrump import HasTrump


class Trick(list[Card], HasTrump):
    """
    Represents a trick in Euchre, storing cards played in order and tracking the winner.
    """

    def __init__(self, trump: str, order: list[int], init=[]):
        """
        Initializes an empty trick.

        Args:
            trump (str): The trump suit for this round.
        """
        super().__init__()
        self._trump: str = trump  # The trump suit for this trick
        self._order = order

        for card in init:
            self.append(Card(self, card))

    def copy(self) -> "Trick":
        """
        Creates shallow copy of the trick, including the base list and all fields.

        Returns:
            Trick: A new instance of Trick with the same data.
        """
        new_trick = Trick(self._trump)  # Create a new Trick with the same trump suit
        new_trick.extend(self)
        return new_trick

    def normalize(self) -> "Trick":
        norm_trick = Trick("♠", self._order)
        for card in self:
            norm_trick.append(card.normalize(self))
        return norm_trick

    def append(self, card: Card):
        super().append(Card(self, card))

    @property
    def trump(self) -> str:
        """
        Getter for the trump suit of the trick.

        Returns:
            str: The trump suit for this trick.

        Notes:
            - This allows controlled access to the `_trump` attribute.
            - Using `@property` ensures that `trump` is read-only unless explicitly modified via a setter.
            - Prevents accidental modification of the trump suit during gameplay.
        """
        return self._trump

    @property
    def lead_player(self) -> str:
        return self._order[0]

    @property
    def lead_suit(self) -> str:
        """
        Retrieves the lead suit of the trick, considering Left Bower rules.

        Returns:
            str: The suit of the first played card, adjusted for Left Bower.
        """
        return self[0].suit_effective()

    @property
    def best_card(self) -> Card | None:
        """
        Determines the best (winning) card in the trick.

        Returns:
            Optional[Card]: The winning card, or None if the trick is empty.
        """
        if len(self) == 0:
            return None
        if len(self) == 1:
            return self[0]

        best = self[0]

        for card in self[1:]:  # Start checking from the second card
            best = best_card(best, card, self.lead_suit)

        return best

    @property
    def winner(self) -> int | None:
        """
        Determines the player index of the trick's winner.

        Returns:
            Optional[int]: The index of the winning player, or None if the trick is empty.
        """
        best = self.best_card
        if best is None:
            return None
        return self.who_played(best)

    def who_played(self, card_in_question):
        for i, card_in_trick in enumerate(self):
            if card_in_trick == card_in_question:
                return self._order[i]

        return None

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the trick.

        Returns:
            str: A formatted string showing each player's played card.
        """

        sb = "["

        for i in range(0, len(self)):
            card = self[i]
            if card == self.best_card:
                sb += Fore.LIGHTYELLOW_EX + str(card) + Style.RESET_ALL
            else:
                sb += str(card)

            if i != len(self) - 1:
                sb += ", "

        sb += f"]:{self.trump}"
        return sb

    def highlight_if_win(self, card):
        print(card, self.best_card, card == self.best_card)
        if card != self.best_card:
            return str(card)
        return Style.BRIGHT + str(card) + Style.RESET_ALL

    def __repr__(self) -> str:
        """
        Returns a string representation of the trick (same as __str__).

        Returns:
            str: A formatted string of the trick's current state.
        """
        return str(self)
