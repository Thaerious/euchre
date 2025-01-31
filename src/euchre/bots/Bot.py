from euchre.card import *
from euchre import Snapshot
import random

# ["♠", "♥", "♣", "♦"]

class Bot:
    def decide(self, snap: Snapshot):
        method_name = f"state_{snap.state}"
        method = getattr(self, method_name)
        return method(snap)

    def state_1(self, snap): # pass / order / alone        
        q = Query(trump = snap.up_card.suit, source = snap.hand)

        # alone when face trump >= 3
        if q.count("LJAQK♠") >= 3: return ("alone", None)

        # order when face trump >= 2
        if q.count("LJAQK♠") >= 2: return ("order", None)

        # order when trump >= 3
        if q.count("♠") >= 3: return ("order", None)

        return ("pass", None)

    def state_2(self, snap): # dealer up / down
        q = Query(trump = snap.trump, source = snap.hand)

        if q.count("910JQKA♣") == 1: 
            return ("up", q.select("910JQKA♣")[0])
        
        if q.count("910JQKA♥") == 1: 
            return ("up", q.select("910JQKA♥")[0])
        
        if q.count("910JQKA♦") == 1: 
            return ("up", q.select("910JQKA♦")[0])
        
        return("down", None)

    def state_3(self, snap): # pass / make / alone
        q = Query(trump = None, source = snap.hand)

        suits = Card.suits
        down_suit = snap.down_card.suit
        if suits in down_suit:
            suits.remove(snap.down_card.suit)

        # 4 of a suit -> go alone
        # 3 of a suit -> make
        for suit in suits:
            if q.trump(suit).count(suit) >= 4: return ("alone", suit)
            if q.trump(suit).count(suit) >= 3: return ("make", suit)

        return ("pass", None)

    def state_4(self, snap): # Dealer make / alone
        q = Query(trump = None, source = snap.hand)

        suits = Card.suits
        suits.remove(snap.up_card.suit)

        # 4 of a suit -> go alone
        # 3 of a suit -> make
        for suit in suits:
            if q.count(suit) >= 4: return ("alone", suit)
            if q.count(suit) >= 3: return ("make", suit)

        # first suit > 3 make
        for suit in suits:
            if q.count(suit) >= 2: return ("make", suit)           

        # make highest ranked card
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
