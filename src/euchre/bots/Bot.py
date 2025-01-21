from euchre.card.Card import Card
from euchre import Snapshot
import random

class Bot:
    def decide(self, snap: Snapshot):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
        print(snap)
        return method(snap)

    def state_1(self, snap):
        # pass / order / alone
        if snap.hand.count(suits = snap.up_card.suit, trump = snap.up_card.suit) < 2:
            return ("pass", None)

        if snap.hand.count(values = ["A", "J", "Q", "K"], suits = snap.up_card.suit, trump = snap.up_card.suit) >= 1:
            return ("order", None)

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