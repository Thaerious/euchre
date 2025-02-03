from euchre.card import *
from euchre import Snapshot
from .tools.Query import Query
import random

# ["♠", "♥", "♣", "♦"]

class Bot_2:
    def decide(self, snap: Snapshot):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
        return method(snap)

    def state_1(self, snap): # pass / order / alone
        # alone when face trump >= 3
        if Query(snap).select("LJAQK♠").len >= 3: return ("alone", None)
        
        # order when face trump >= 2
        if Query(snap).select("LJAQK♠").len >= 2: return ("order", None)
        
        # order when trump >= 3
        if Query(snap).select("♠").len >= 3: return ("order", None)

        return ("pass", None)

    def state_2(self, snap): # dealer up / down
        with Query(snap).select("910JQKA♣") as q:
            if q.len == 1: return("up", q[0])

        with Query(snap).select("910JQKA♥") as q:
            if q.len == 1: return("up", q[0])

        with Query(snap).select("910JQKA♦") as q:
            if q.len == 1: return("up", q[0])            
        
        return("down", None)

    def state_3(self, snap): # pass / make / alone
        # any suit >= 4 go alone
        if Query(snap, trump = None).down("♥♣♦").select("♠").len >= 4: return ("alone", "♠")
        if Query(snap, trump = None).down("♠♣♦").select("♥").len >= 4: return ("alone", "♥")
        if Query(snap, trump = None).down("♠♥♦").select("♣").len >= 4: return ("alone", "♣")
        if Query(snap, trump = None).down("♠♥♣").select("♦").len >= 4: return ("alone", "♦")

        # any suit == 3 make
        if Query(snap, trump = None).down("♥♣♦").select("♠").len == 3: return ("make", "♠")
        if Query(snap, trump = None).down("♠♣♦").select("♥").len == 3: return ("make", "♥")
        if Query(snap, trump = None).down("♠♥♦").select("♣").len == 3: return ("make", "♣")
        if Query(snap, trump = None).down("♠♥♣").select("♦").len == 3: return ("make", "♦")

        return ("pass", None)

    def state_4(self, snap): # Dealer make / alone
        # any suit (except down suit) >= 4 go alone
        if Query(snap).down("♥♣♦").select("♠").len >= 4: return ("alone", "♠")
        if Query(snap).down("♠♣♦").select("♥").len >= 4: return ("alone", "♥")
        if Query(snap).down("♠♥♦").select("♣").len >= 4: return ("alone", "♣")
        if Query(snap).down("♠♥♣").select("♦").len >= 4: return ("alone", "♦")

        # any suit (except down suit) == 3 make
        if Query(snap).down("♥♣♦").select("♠").len == 3: return ("make", "♠")
        if Query(snap).down("♠♣♦").select("♥").len == 3: return ("make", "♥")
        if Query(snap).down("♠♥♦").select("♣").len == 3: return ("make", "♣")
        if Query(snap).down("♠♥♣").select("♦").len == 3: return ("make", "♦")

        # make highest ranked card
        with Query(snap).down("♦").select("♠♥♣") as q:
            if q.len > 0: return("make", q[0][-1])

        with Query(snap).down("♥").select("♠♣♦") as q:
            if q.len > 0: return("make", q[-1][-1])
        
        with Query(snap).down("♣").select("♠♥♦") as q:
            if q.len > 0: return("make", q[-1][-1])

        with Query(snap).down("♠").select("♥♣♦") as q:
            if q.len > 0: return("make", q[-1][-1])                  

    def state_5(self, snap):   
        with Query(snap).playable() as q:           
            # if len(trick) == 0:
            #     if q.select("JLA♠").len >= 2:                     
            #         return ("play", q.select("LJA♠")[0])
            #     if q.select("910JQKA♦").len == 1:
            #         return ("play", q.select("910JQKA♦")[0])
            #     if q.select("910JQKA♥").len == 1:
            #         return ("play", q.select("910JQKA♥")[0])              
            #     if q.select("910JQKA♣").len == 1:
            #         return ("play", q.select("910JQKA♣")[0])                       

            return("play", random.choice(q))    
