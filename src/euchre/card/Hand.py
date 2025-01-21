from typing import List, Union
from euchre.card.Card import Card

class Hand(list):
    """
    Represents a player's hand in Euchre, extending `CardList`.
    """

    def __init__(self, cards: List[Union[Card, str]] = []):
        """
        Initializes a Hand with a given list of Card objects.

        Args:
            cards (List[Card]): A list of Card objects to initialize the hand.
        
        Raises:
            TypeError: If any item in `cards` is not an instance of `Card`.
        """
        
        for card in cards:
            if isinstance(card, Card):
                self.append(card)
            else:
                self.append(Card(card))
        

    def has_suit(self, suit: str, trump: str) -> bool:
        """
        Checks if the hand contains at least one card of the specified suit,
        considering effective suits (e.g., Left Bower counting as trump).

        Args:
            suit (str): The suit to check for (e.g., "♠", "♥", "♣", "♦").
            trump (str): The current trump suit in the game.

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
            if card.suit_effective(trump) == suit:
                return True
        return False
    
    def count_suit(self, suit: str, trump: str) -> bool:
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
        count = 0
        for card in self:
            if card.suit_effective(trump) == suit:
                count = count + 1
        return count
    
    def select_cards(self, trump: str, values: List[int] = Card.values, suits: List[str] = Card.suits) -> int:
        selected = []
        for card in self:
            if card.suit_effective(trump) not in suits: continue
            if card.value not in values: continue
            selected.append(card)

        return selected