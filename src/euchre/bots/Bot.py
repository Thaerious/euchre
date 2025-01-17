from euchre.card.Card import Card
from .tools import *
import random

class Bot:
    def decide(this, snap):
        this.snap = snap
        return getattr(this, f"state{snap.state}")()

    def state1(this):
        return ("pass", None)

    def state2(this):
        return ("down", None)

    def state3(this):
        return ("pass", None)

    def state4(this):
        suits = allowedSuits(this.snap.upCard.suit)
        suit = random.choice(suits)
        return ("make", suit)

    def state5(this):
        trick = None
        if len(this.snap.tricks) > 0: 
            trick = this.snap.tricks[-1]
            
        cards = playable(this.snap.trump, trick, this.snap.hand)
        card = random.choice(cards)
        return ("Play", card)

