from euchre.card.Trick import Trick
from euchre.card.Hand import Hand

#given a Trick and a Hand object, returns a list of all cards that Hand is allowed to play
def playable(trick: Trick, hand: Hand):
    playable_cards = []

    if len(trick) == 0: return hand.copy()

    for card in hand:
        if card.suit_effective(trick.trump) == trick.lead_suit:
            playable_cards.append(card)
            continue

        if not hand.has_suit(trick.lead_suit, trick.trump):
            playable_cards.append(card)
            continue

    return playable_cards
    