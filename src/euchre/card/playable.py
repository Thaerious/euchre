from euchre.card.Hand import Hand
from euchre.card.Trick import Trick


# given a Trick and a Hand object, returns a list of all cards that Hand is allowed to play
def playable(trick: Trick, hand: Hand):
    playable_cards = []

    if len(trick) == 0:
        return hand.copy()

    for card in hand:
        if card.suit_effective() == trick.lead_suit:
            playable_cards.append(card)
            continue

        if not hand.has_suit(trick.lead_suit):
            playable_cards.append(card)
            continue

    return playable_cards
