"""
MetaDeck.py

Extends Deck to provide knowledge of up-card, down-card, and discards.
"""

from euchre.EuchreError import EuchreError
from euchre.card.Card import Card
from euchre.card.Deck import Deck
from euchre.card.HasTrump import HasTrump, TrumpSuit
import euchre.constants as const
from .PlayerManager import PlayerManager

class MetaDeck(Deck):
    up_card: Card | None
    """ The card visible to all players. """

    down_card: Card | None
    """ The card that the dealer turned down. """

    discard: Card | None
    """ The card that the dealer discarded. """

    def __init__(self, seed=None):
        self.up_card = None
        self.down_card = None
        self.discard = None
        super().__init__(seed)

    def __json__(self):
        return {
            "deck": self,
            "up_card": self.up_card,
            "down_card": self.down_card,
            "discard": self.discard
        }

    def shuffle(self):
        """
        Reset the deal state.

        Clears the trump, up card, down card, and discard, typically called at the
        end of a hand when starting a new deal.
        """        
        super().shuffle()
        self.up_card = None
        self.down_card = None
        self.discard = None        

    def set_discard(self, card: Card | None) -> Card | None:
        """
        Set the discarded card after a player picks up the up card.

        This method moves the current up card out of play (sets it to None),
        and stores the given card as the discard. It returns the original up card.

        Args:
            card (Card | None): The card to discard (replaces the up card in hand).

        Returns:
            Card | None: The up card that was picked up.

        Raises:
            EuchreError: If a discard has already been set.
        """        
        if self.discard is not None:
            raise EuchreError("Discard already set.")
        
        pickup_card = self.up_card
        self.discard = card
        self.up_card = None
        return pickup_card

    def turn_down_card(self) -> None:
        """
        Turn down the up card (pass on making trump if upCard is not desired).

        Raises:
            EuchreError: If a discard is already set or  up_card is None.
        """

        if self.discard is not None or self.up_card is None:
            raise EuchreError("Discard and up_card must be None to turn down.")

        self.down_card = self.up_card
        self.up_card = None    

    @HasTrump.trump.setter
    def trump(self, trump: TrumpSuit | None):
        # override to permit clearing; forbid matching down_card suit
        if trump is not None and self.down_card is not None and self.down_card.suit == trump:
            raise EuchreError(f"Trump ({trump}) cannot match the down card ({self.down_card}).")
        HasTrump.trump.fset(self, trump)
        
    def deal_cards(self, players: PlayerManager) -> None:
        """
        Deal 5 cards to each player, then set the upCard from the top of the deck.
        """

        if len(self) < 24:
            raise EuchreError(f"Not enough cards in the deck (len={len(self)}) to deal.")

        for _ in range(const.NUM_CARDS_PER_PLAYER):
            for player in players:
                card = self.pop()
                player.hand.append(card)
                
        self.up_card = self.pop()

    def __str__(self):
        return "\n".join([
            f"up card: {self.up_card}",
            f"down card: {self.down_card}",
            f"discard: {self.discard}"
        ])        

    def __repr__(self):
        return f"<MetaDeck up={self.up_card} down={self.down_card} discard={self.discard}>"