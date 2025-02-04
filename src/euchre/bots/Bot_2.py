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

    # def state_1(self, snap): # pass / order / alone
    #     # when bot is the dealer
    #     with Query(snap).dealer("0") as q:
    #         # alone when face trump >= 4
    #         if Query(snap).select("LJAQK♠").len >= 4: return ("alone", None)            
    #         # order when trump >= 3
    #         if Query(snap).select("♠").len >= 3: return ("order", None)

    #     with Query(snap).dealer("123") as q:
    #         # alone when face trump >= 4
    #         if Query(snap).select("LJAQK♠").len >= 5: return ("alone", None)            
    #         # order when trump >= 3
    #         if Query(snap).select("♠").len >= 4: return ("order", None)

    #     return ("pass", None)

    # def state_2(self, snap): # as dealer up / down
    #     if Query(snap).up("QKALJ♠").len > 0:
    #         q = Query(snap).select("910JQKA♣♥♦♠")
    #         return ("up", q[0])        

    #     with Query(snap).select("910JQKA♣") as q:
    #         if q.len == 1: return("up", q[0])

    #     with Query(snap).select("910JQKA♥") as q:
    #         if q.len == 1: return("up", q[0])

    #     with Query(snap).select("910JQKA♦") as q:
    #         if q.len == 1: return("up", q[0])            
        
    #     return("down", None)

    # def state_3(self, snap): # pass / make / alone
    #     # any suit >= 4 go alone
    #     if Query(snap, trump = None).down("♥♣♦").select("♠").len >= 4: return ("alone", "♠")
    #     if Query(snap, trump = None).down("♠♣♦").select("♥").len >= 4: return ("alone", "♥")
    #     if Query(snap, trump = None).down("♠♥♦").select("♣").len >= 4: return ("alone", "♣")
    #     if Query(snap, trump = None).down("♠♥♣").select("♦").len >= 4: return ("alone", "♦")

    #     # any suit == 3 make
    #     if Query(snap, trump = None).down("♥♣♦").select("♠").len == 3: return ("make", "♠")
    #     if Query(snap, trump = None).down("♠♣♦").select("♥").len == 3: return ("make", "♥")
    #     if Query(snap, trump = None).down("♠♥♦").select("♣").len == 3: return ("make", "♣")
    #     if Query(snap, trump = None).down("♠♥♣").select("♦").len == 3: return ("make", "♦")

    #     return ("pass", None)

    # def state_4(self, snap): # Dealer make / alone
    #     # any suit (except down suit) >= 4 go alone
    #     if Query(snap).down("♥♣♦").select("♠").len >= 4: return ("alone", "♠")
    #     if Query(snap).down("♠♣♦").select("♥").len >= 4: return ("alone", "♥")
    #     if Query(snap).down("♠♥♦").select("♣").len >= 4: return ("alone", "♣")
    #     if Query(snap).down("♠♥♣").select("♦").len >= 4: return ("alone", "♦")

    #     # any suit (except down suit) == 3 make
    #     if Query(snap).down("♥♣♦").select("♠").len == 3: return ("make", "♠")
    #     if Query(snap).down("♠♣♦").select("♥").len == 3: return ("make", "♥")
    #     if Query(snap).down("♠♥♦").select("♣").len == 3: return ("make", "♣")
    #     if Query(snap).down("♠♥♣").select("♦").len == 3: return ("make", "♦")

    #     # make highest ranked card
    #     with Query(snap).down("♦").select("♠♥♣") as q:
    #         if q.len > 0: return("make", q[0].suit)

    #     with Query(snap).down("♥").select("♠♣♦") as q:
    #         if q.len > 0: return("make", q[-1].suit)
        
    #     with Query(snap).down("♣").select("♠♥♦") as q:
    #         if q.len > 0: return("make", q[-1].suit)

    #     with Query(snap).down("♠").select("♥♣♦") as q:
    #         if q.len > 0: return("make", q[-1].suit)                  

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

            suit = snap.tricks[-1].best_card.suit
            suit = q.normalize(suit)
            phrase = f"AKQJ109{suit}"
            r = q.select(phrase)
            if r.len > 0: 
                print(snap.trump, snap.tricks[-1].best_card, phrase, q, r)
                return("play", r[0])    

            return("play", random.choice(q))    
