from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
import random

# ["♠", "♥", "♣", "♦"]

class Bot_0:
    def __init__(self):
        self.queries = {
            "state_1":[],
            "state_2":[],
            "state_3":[],
            "state_4":[],
            "state_5":[],
        }        

    def decide(self, snap: Snapshot):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
    
    def state_1(self, snap): # pass / order / alone
        for query in self.queries["state_1"]:
            result = query[0].all().get(snap)
            if result is not None:
                return (query[1], result)
            
        return ("pass", None)

    def state_2(self, snap): # dealer up / down
        for query in self.queries["state_1"]:
            result = query[0].all().get(snap)
            if result is not None:
                return (query[1], result)
                    
        return("down", None)

    def state_3(self, snap): # pass / make / alone
        for query in self.queries["state_1"]:
            result = query[0].all().get(snap)
            if result is not None:
                return (query[1], result)
                    
        return ("pass", None)

    def state_4(self, snap): # Dealer make / alone
        for query in self.queries["state_1"]:
            result = query[0].all().get(snap)
            if result is not None:
                return (query[1], result.suit)

        options = ["♠", "♥", "♣", "♦"]
        options.remove(snap.down_card.suit)
        return ("make", random.choice(options))   

    def state_5(self, snap):
        for query in self.queries["state_1"]:
            result = query[0].all(snap).playable(snap)
            if result is not None:                
                return (query[1], result)

        with Query(snap).playable() as q:
            return("play", random.choice(q))    
