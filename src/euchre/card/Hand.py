from typing import List, Union
from euchre.card.Card import Card
from euchre.del_string import del_string
from .Has_Trump import Has_Trump

class Hand(list):
    """
    Represents a player's hand in Euchre, extending `CardList`.
    """

    def normalize(self, source)-> "Hand":
        norm_hand = Hand()
        for card in self:
            norm_hand.append(card.normalize(source))
        return norm_hand

    def has_suit(self, suit: str) -> bool:
        """
        Checks if the hand contains at least one card of the specified suit,
        considering effective suits (e.g., Left Bower counting as trump).

        Args:
            suit (str): The suit to check for (e.g., "♠", "♥", "♣", "♦").

        Returns:
            bool: 
                - `True` if at least one card in the hand matches the specified suit.
                - `False` if no cards in the hand match the specified suit.

        Example:
            hand = Hand(["10♠", "J♦", "A♣"])
            hand.has_suit("♠", "♠")  # Returns True
            hand.has_suit("♥", "♠")  # Returns False
        """
        for card in self:
            if card.suit_effective() == suit:
                return True
        return False   

    def count_suit(self, suit: str) -> bool:
        """
        Counts the number of cards of the specified suit,
        considering effective suits (e.g., Left Bower counting as trump).

        Args:
            suit (str): The suit to check for (e.g., "♠", "♥", "♣", "♦").
            trump (str): The current trump suit in the game.

        Returns:
            bool: 
                - `True` if at least one card in the hand matches the specified suit.
                - `False` if no cards in the hand match the specified suit.

        Example:
            hand = Hand(["10♠", "J♣", "A♣"])
            hand.has_suit("♠", "♦")  # Returns 1
            hand.has_suit("♠", "♠")  # Returns 2
            hand.has_suit("♦", "♣")  # Returns 0
        """
        return len(self.select(Card.ranks, [suit]))
    
    def select(self, values: List[int] = Card.ranks, suits: List[str] = Card.suits) -> list[Card]:
        """
        Selects and returns a list of cards from the hand that match the given values and suits,
        considering effective suits.

        Args:
            values (List[int], optional): A list of valid card values to match. Defaults to `Card.values`.
            suits (List[str], optional): A list of valid suits to match. Defaults to `Card.suits`.

        Returns:
            List[Card]: A list of cards that match the given criteria.
        """
        selected = []
        for card in self:
            if card.suit_effective() not in suits: continue
            if card.rank not in values: continue
            selected.append(card)

        return selected
    
    def count(self, values: List[int] = Card.ranks, suits: List[str] = Card.suits) -> int:
        return len(self.select(values, suits))
    
    def __str__(self):
        return del_string(self, ",", "'")

    def __repr__(self):
        return del_string(self, ",", "'")
        