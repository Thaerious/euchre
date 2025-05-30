from euchre.EuchreError import EuchreError
from euchre.card.Card import Card
from euchre.card.Deck import Deck
from euchre.player.Player import Player
import euchre.constants as const


class DealManager:
    def __init__(self, deck: Deck):
        self.deck = deck
        self._up_card = None
        self._down_card = None
        self._discard = None
        
    @property
    def up_card(self) -> Card | None:
        return self._up_card

    @property
    def down_card(self) -> Card | None:
        return self._down_card

    @property
    def discard(self) -> Card | None:
        return self._discard   

    def reset(self):
        """
        Reset the deal state.

        Clears the up card, down card, and discard, typically called at the
        end of a hand or when starting a new deal.
        """        
        self._up_card = None
        self._down_card = None
        self._discard = None        

    def set_discard(self, card) -> Card:
        """
        Set the discarded card after a player picks up the up card.

        This method moves the current up card out of play (sets it to None),
        and stores the given card as the discard. It returns the original up card.

        Args:
            card (Card): The card to discard (replaces the up card in hand).

        Returns:
            Card: The up card that was picked up.

        Raises:
            EuchreError: If a discard has already been set.
        """        
        if self._discard is not None:
            raise EuchreError("Discard already set.")
        
        pick_up_card = self.up_card
        self._discard = card
        self._up_card = None
        return pick_up_card

    def turn_down_card(self) -> None:
        """
        Turn down the up card (pass on making trump if upCard is not desired).

        Raises:
            EuchreException: If a discard is already set.
        """
        if self.discard is not None:
            raise EuchreError("Discard must be None to turn down.")

        self._down_card = self._up_card
        self._up_card = None    

    def make_trump(self, suit: str) -> None:
        """
        Declare the trump suit.
        Will update the maker to the current player.

        Args:
            suit (Optional[str]): The desired trump suit.

        Raises:
            EuchreException: Various conditions (mismatched downCard, missing upCard, etc.).
        """
        # Disallow trump if it matches the downCard's suit
        if self.down_card is not None and self.down_card.suit == suit:
            raise EuchreError("Trump can not match the down card.")

        self.deck.trump = suit
        
    def deal_cards(self, players: list[Player]) -> None:
        """
        Deal 5 cards to each player, then set the upCard from the top of the deck.
        """

        if len(self.deck) < 24:
            raise EuchreError("Not enough cards in the deck to deal.")

        for _ in range(const.NUM_CARDS_PER_PLAYER):
            for player in players:
                card = self.deck.pop(0)
                player.hand.append(card)
        self._up_card = self.deck.pop(0)

    def __repr__(self):
        return f"<DealManager up={self._up_card} down={self._down_card} discard={self._discard}>"