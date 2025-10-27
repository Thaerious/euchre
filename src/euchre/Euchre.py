"""
Euchre.py
Main module for euchre state
"""

from euchre.PlayerManager import PlayerManager
from euchre.TrickManager import TrickManager
from euchre.PlayerManager import PlayerManager
from euchre.MetaDeck import MetaDeck
from euchre.Settings import Settings
from euchre.EuchreError import EuchreError
from euchre.card.Card import Card

class Euchre:
    """
    The core class representing a single game of Euchre.
    No meta-state in this class (ie actions).
    """

    deck: MetaDeck
    players: PlayerManager
    tricks: TrickManager
    won_last_hand: int

    def __init__(self, names:list[str], seed:int = None) -> None:
        self.deck = MetaDeck(seed)
        self.players = PlayerManager(names, self.deck)
        self.tricks = TrickManager(self)

    def __json__(self):
        return{
            "deck"   : self.deck,
            "players": self.players,
            "tricks" : self.tricks,
            "won_last_hand": self.won_last_hand
        }

    def __str__(self):
        sb = ""
        sb = sb + (str)(self.players) + "\n"
        sb = sb + (str)(self.deck) + "\n"
        sb = sb + (str)(self.tricks) + "\n"
        return sb

    def is_game_over(self) -> bool:
        """
        Determine if the game is over based on the current score.
        If either team has a score > 10 (win_condition) then return True,
        else return False.

        Args:`
            score (List[int]): A two-element list representing the team scores.

        Returns:
            bool: True if either team has reached or exceeded 10 points, otherwise False.
        """

        for team in self.players.teams:
            if team.score >= Settings.win_condition:
                return True
        return False
    
    def dealer_swap_card(self, card: Card) -> None:
        """
        Put the upcard into the dealers hand, then set 'card' from the dealers hand
        as the discard in the deck manager.

        Args:
            card (Card): The card to remove from the dealer's hand.

        Raises:
            EuchreException: If a discard is already set, or the card is not in the dealer's hand.
        """
        if self.deck.discard is not None:
            raise EuchreError("Discard must be None to swap.")

        if card not in self.players.dealer.hand:
            raise EuchreError(f"Must swap card from hand: {card}")

        # Remove the given card, add the upCard to dealer's hand
        self.players.dealer.hand.remove(card)
        self.players.dealer.hand.append(self.deck.up_card)
        self.deck.discard = card
        self.players.set_maker()