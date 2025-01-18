from typing import Dict, List, Optional, Union
from euchre.card.Card import Card

class Trick(List[Card]):
    """
    Represents a trick in Euchre, storing cards played in order and tracking the winner.
    """

    def __init__(self, trump: str):
        """
        Initializes an empty trick.

        Args:
            trump (str): The trump suit for this round.
        """
        super().__init__()
        self.who_played: Dict[Card, int] = {}  # Maps cards to player indices
        self._trump: str = trump  # The trump suit for this trick

    @staticmethod
    def build(trump: str, cards: List[tuple[int, Union[Card, str]]], order = [0, 1, 2, 3]) -> "Trick":
        """
        Creates a Trick instance with given cards and their player indices.

        Args:
            trump (str): The trump suit.
            cards (List[tuple[int, Union[Card, str]]]): A list of (player_index, card) pairs.

        Returns:
            Trick: A Trick instance populated with the given cards.
        """

        if len(cards) != len(order):
            raise Exception("Cards and order lists sizes must match.")

        trick = Trick(trump)
        for i, card in enumerate(cards):
            trick.append(order[i], card)
        return trick

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
    def lead_suit(self) -> str:
        """
        Retrieves the lead suit of the trick, considering Left Bower rules.

        Returns:
            str: The suit of the first played card, adjusted for Left Bower.
        """
        return self[0].suit_effective(self._trump)

    def append(self, pIndex: int, card: Union[Card, str]) -> None:
        """
        Adds a card to the trick, associating it with a player.

        Args:
            pIndex (int): The player index who played this card.
            card (Union[Card, str]): The card being played (as a Card object or string).
        """
        if isinstance(card, str):
            card = Card(card)  # Convert string representation to Card

        super().append(card)
        self.who_played[card] = pIndex

    @property
    def best_card(self) -> Optional[Card]:
        """
        Determines the best (winning) card in the trick.

        Returns:
            Optional[Card]: The winning card, or None if the trick is empty.
        """
        if len(self) == 0: return None
        if len(self) == 1: return self[0]

        best_card = self[0]

        for card in self[1:]:  # Start checking from the second card
            if best_card.compare(card, self.lead_suit, self._trump) < 0:
                best_card = card

        return best_card

    @property
    def winner(self) -> Optional[int]:
        """
        Determines the player index of the trick's winner.

        Returns:
            Optional[int]: The index of the winning player, or None if the trick is empty.
        """
        best = self.best_card
        if best is None:
            return None

        return self.who_played.get(best, None)

    def can_play(self, card: Union[Card, str]) -> bool:
        """
        Determines if a given card can be legally played in this trick.

        Args:
            card (Union[Card, str]): The card being checked.

        Returns:
            bool: True if the card is playable, False otherwise.
        """
        if isinstance(card, str):
            card = Card(card)  # Convert string to Card

        if not self:
            return True  # First card of the trick can always be played

        lead_suit = self.lead_suit
        if card.suit_effective(self._trump) == lead_suit:
            return True  # Following suit is always legal

        # Check if player has any other cards matching the lead suit
        for card_in_hand in self:
            if card_in_hand.suit_effective(self._trump) == lead_suit:
                return False  # If another card follows suit, this one must follow suit too

        return True  # No lead suit cards in hand, so playing off-suit is legal

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the trick.

        Returns:
            str: A formatted string showing each player's played card.
        """
        return " ".join(
            f"[{self.who_played[card]}, {card}{'*' if card == self.best_card else ''}]"
            for card in self
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the trick (same as __str__).

        Returns:
            str: A formatted string of the trick's current state.
        """
        return str(self)
