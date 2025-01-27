from euchre.card import *
from euchre import Snapshot
import random

# ["♠", "♥", "♣", "♦"]

class DevBot:
    def decide(self, snap: Snapshot):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
        return method(snap)

    def state_1(self, snap):
        return ("pass", None)

    def state_2(self, snap):       
        return("down", None)

    def state_3(self, snap):
        return ("pass", None)

    def state_4(self, snap):
        q = Query(trump = None, source = snap.hand)

        suits = Card.suits
        suits.remove(snap.up_card.suit)

        for suit in suits:
            if q.count(suit) >= 4: return ("alone", suit)
            if q.count(suit) >= 3: return ("make", suit)

        for suit in suits:
            if q.count(suit) >= 2: return ("make", suit)           

        cards = q.select("".join(suits)).by_rank()
        return ("make", cards[0].suit)
        

    def state_5(self, snap):   
        trick = snap.tricks[-1]

        p = playable(snap.tricks[-1], snap.hand)
        q = Query(trump = snap.trump, source = p)

        if len(trick) == 0:
            if q.count("LJA♠") >= 2: 
                return ("play", q.by_rank("LJA♠")[0])
            
            if q.count("♦") == 1:
                return ("play", q.select("♦")[0])

            if q.count("♥") == 1:
                return ("play", q.select("♥")[0])
            
            if q.count("♣") == 1:
                return ("play", q.select("♣")[0])                
            
            off_suit_by_rank = q.select("♦♥♣").by_rank()
            if off_suit_by_rank: return ("play", off_suit_by_rank[0])

            trump_by_rank = q.select("♠").by_rank()
            if trump_by_rank: return ("play", trump_by_rank[0])
        else:
            # if winning team is not my team
            if trick.winner % 2 != snap.for_player % 2:            
                q1 = q.beats(trick).select("♣♥♦♠")
                if q1.count() > 0: return("play", q1[0])
            else:
                q1 = q.loses(trick).select("♣♥♦♠")
                if q1.count() > 0: return("play", q1[0])

        return("play", random.choice(p))    
