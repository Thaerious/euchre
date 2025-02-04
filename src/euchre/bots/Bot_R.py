from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
import random

# ["♠", "♥", "♣", "♦"]

class Bot_R:
    def decide(self, snap: Snapshot):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
        return method(snap)

    def state_1(self, snap): # pass / order / alone
        return (random.choice(["pass", "order", "alone"]), None)

    def state_2(self, snap): # dealer up / down
        return("down", None)

    def state_3(self, snap): # pass / make / alone
        return ("pass", None)

    def state_4(self, snap): # Dealer make / alone
        suit = snap.down_card.suit        
        q = Query(snap).select(f"~{suit}")
        return ("make", random.choice(q).suit)             

    def state_5(self, snap):   
        with Query(snap).playable() as q:
            return("play", random.choice(q))    
