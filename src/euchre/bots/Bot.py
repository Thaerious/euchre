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
        q = Query(trump = snap.trump, source = snap.hand)

        if q.len("910JQKA♣") == 1: 
            return ("up", q.select("910JQKA♣")[0])
        
        if q.len("910JQKA♥") == 1: 
            return ("up", q.select("910JQKA♥")[0])
        
        if q.len("910JQKA♦") == 1: 
            return ("up", q.select("910JQKA♦")[0])

        if q.by_rank("910JQK♣♥♦").len() > 0: 
            return ("up", q.by_rank("910JQK♣♥♦")[0])
        
        return("down", None)

    def state_3(self, snap):
        pass

    def state_4(self, snap):
        pass

    def state_5(self, snap):   
        trick = snap.tricks[-1]

        p = playable(snap.tricks[-1], snap.hand)
        print(f"can play {p}")
        q = Query(trump = snap.trump, source = p)

        if len(trick) == 0:
            if q.len("LJA♠") >= 2: 
                return ("play", q.by_rank("LJA♠")[0])
            
            if q.len("♦") == 1:
                return ("play", q.select("♦")[0])

            if q.len("♥") == 1:
                return ("play", q.select("♥")[0])
            
            if q.len("♣") == 1:
                return ("play", q.select("♣")[0])                

        if trick.winner % 2 != snap.for_player % 2:
            if q.select("♠").len() > 0:
                return ("play", q.select("♠")[0])

        print(snap.tricks[-1])
        print(snap.tricks[-1].winner %2)
        print(snap.for_player % 2)