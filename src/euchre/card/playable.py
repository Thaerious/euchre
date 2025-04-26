# playable.py

"""Playable card logic for Euchre.

Determines which cards from a player's hand are legally playable based on the current trick.
"""

from euchre.card.Hand import Hand
from euchre.card.Trick import Trick

def playable(trick: Trick, hand: Hand) -> list:
    """
    Determine which cards from a hand are legally playable for the current trick.

    In Euchre:
    - If it's the first play of the trick, any card can be played.
    - If the player has cards matching the lead suit (effective suit), they must follow suit.
    - Otherwise, the player may play any card.

    Args:
        trick (Trick): The current trick being played.
        hand (Hand): The player's hand.

    Returns:
        List[Card]: A list of cards from the hand that are legally playable.
    """
    playable_cards = []

    if len(trick) == 0:
        return hand.copy()

    for card in hand:
        if card.suit_effective() == trick.lead_suit:
            playable_cards.append(card)
            continue

    # If no cards match the lead suit, all cards are playable
    if not playable_cards:
        return hand.copy()

    return playable_cards
