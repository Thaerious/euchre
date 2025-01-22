from euchre.card import *
from euchre import Snapshot
import random

# ["♠", "♥", "♣", "♦"]

class Bot:
    def decide(self, snap: Snapshot):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
        print(snap)
        return method(snap)

    def state_1(self, snap):
        # pass / order / alone

        q = Query(
            trump = snap.up_card.suit, 
            hand = snap.hand
        )

        # order when >= 2 face trump
        if q.phrase("A J Q K ♠ J♣").count >= 2: return ("order", None)

        # order when >= 3 trump (one has to be face)
        if q.phrase("♠").count >= 2: return ("order", None)

        return ("pass", None)

    def state_2(self, snap):
        for suit in Card.suits:
            if suit is not snap.trump:
                cards = snap.hand.select(suit = suit, trump = snap.trump)
                if (len(cards) == 1): return("up", cards[0])
       

    def state_3(self, snap):
        pass

    def state_4(self, snap):
        pass

    def state_5(self, snap):
        pass