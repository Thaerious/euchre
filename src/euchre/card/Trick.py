from typing import Dict, List, Optional, Union
from euchre.card.Card import Card
from typeguard import typechecked
from euchre.del_string import del_string

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

    def get_player(self, card):
        if card not in self.who_played: return None
        return self.who_played[card]

    def copy(self) -> "Trick":
        """
        Creates shallow copy of the trick, including the base list and all fields.

        Returns:
            Trick: A new instance of Trick with the same data.
        """
        new_trick = Trick(self._trump)  # Create a new Trick with the same trump suit
        new_trick.extend(self)
        new_trick.who_played = self.who_played
        return new_trick

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
        return self[0].suit_effective()

    def append(self, pIndex: int, card: Card) -> None:
        """
        Adds a card to the trick, associating it with a player.

        Args:
            pIndex (int): The player index who played this card.
            card (Union[Card, str]): The card being played (as a Card object or string).
        """
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
            if best_card.compare(card, self.lead_suit) < 0:
                best_card = card

        return best_card

    # true if card would be the winner of this trick
    # todo test
    def compare_card(self, card):
        best_card = self.best_card
        return best_card.compare(card, self.lead_suit) < 0

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


    def __str__(self) -> str:
        """
        Returns a formatted string representation of the trick.

        Returns:
            str: A formatted string showing each player's played card.
        """
        return f"[{del_string(self, ",", '"')}]:{self.trump}"


    def __repr__(self) -> str:
        """
        Returns a string representation of the trick (same as __str__).

        Returns:
            str: A formatted string of the trick's current state.
        """
        return str(self)
