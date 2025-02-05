from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
from .Bot_0 import Bot_0

import random

# ["♠", "♥", "♣", "♦"]

class Bot_2(Bot_0):
    def decide(self, snap: Snapshot):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
        return method(snap)

    def state_1(self, snap): # pass / order / alone
        if Query(snap).up("♠").select("♠").len >= 4: return ("order", None) 
        if Query(snap).up("♥").select("♥").len >= 4: return ("order", None) 
        if Query(snap).up("♣").select("♣").len >= 4: return ("order", None) 
        if Query(snap).up("♦").select("♦").len >= 4: return ("order", None) 

        # # when bot is the dealer
        # with Query(snap).dealer("0") as q:
        #     # alone when face trump >= 4
        #     if Query(snap).select("LJAQK♠").len >= 4: return ("alone", None)            
        #     # order when trump >= 3
        #     if Query(snap).select("♠").len >= 3: return ("order", None)

        # with Query(snap).dealer("123") as q:
        #     # alone when face trump >= 4
        #     if Query(snap).select("LJAQK♠").len >= 5: return ("alone", None)            
        #     # order when trump >= 3
        #     if Query(snap).select("♠").len >= 4: return ("order", None)

        return ("pass", None)             

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

            r = q.beats(snap.tricks[-1].best_card)
            if r.len > 0: return("play", r[0]) 

            return("play", random.choice(q))    
