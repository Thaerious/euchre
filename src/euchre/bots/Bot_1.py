from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
from .Bot_0 import Bot_0

import random

# ["♠", "♥", "♣", "♦"]

class Bot_1(Bot_0):
    def decide(self, snap: Snapshot):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
        return method(snap)              

    def state_5(self, snap):
        with Query(snap).playable() as q:
            if q.len == 1: return ("play", q[0])

            if q.lead("0").select("♥").len > 0:
                return ("play", q.select("AKQJ109♥")[0])
            if q.lead("0").select("♦").len > 0:
                return ("play", q.select("AKQJ109♦")[0])
            if q.lead("0").select("♣").len > 0:
                return ("play", q.select("AKQJ109♣")[0])  
            if q.lead("0").select("♠").len > 0:
                return ("play", q.select("AKQJ109♠")[0])

            try:
                r = q.beats(snap.tricks[-1].best_card)
                if r.len > 0: return("play", r[0])
            except Exception:
                print(snap)
                raise

            return("play", random.choice(q))    
