from euchre.card import *
from euchre import Snapshot
import random

# ["♠", "♥", "♣", "♦"]

class Bot:
    def decide(self, snap: Snapshot):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
        return method(snap)

    def state_1(self, snap):
        # pass / order / alone

        q = Query(trump = snap.up_card.suit, source = snap.hand)

        # order when >= 2 face trump
        if q.select("LJAQK♠").len() >= 2: return ("order", None)

        # order when >= 3 trump (one has to be face)
        if q.select("♠").len() >= 2: return ("order", None)

        return ("pass", None)

    def state_2(self, snap):
        q = Query(trump = snap.trump, hand = snap.hand)
        
        print(snap.hand)
        print(q.select("910JQKA♣♥♦").select)

        if q.select("910JQKA♣♥♦").count > 0: return ("up", q.select[0])
        return("down", None)

    def state_3(self, snap):
        pass

    def state_4(self, snap):
        pass

    def state_5(self, snap):
        pass