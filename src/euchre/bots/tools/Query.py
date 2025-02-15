import array
import re
from euchre import *
from euchre.del_string import del_string
from .Query_Result import Query_Result
from euchre.card.Card import *

RANKS = {'9':0, '10':1, 'J':2, 'Q':3, 'K':4, 'A':5, 'L': -1}
SUITS = {"♠":0, "♥":1, "♣":2, "♦":3}

CARDS = [
    '9♠', '9♥', '9♣', '9♦',
    '10♠', '10♥', '10♣', '10♦',
    'J♠', 'J♥', 'J♣', 'J♦',
    'Q♠', 'Q♥', 'Q♣', 'Q♦',
    'K♠', 'K♥', 'K♣', 'K♦',
    'A♠', 'A♥', 'A♣', 'A♦'
]

INT_TO_CARD = {
    0: '9♠', 1: '9♥', 2: '9♣', 3: '9♦',
    4: '10♠', 5: '10♥', 6: '10♣', 7: '10♦',
    8: 'J♠', 9: 'J♥', 10: 'J♣', 11: 'J♦',
    12: 'Q♠', 13: 'Q♥', 14: 'Q♣', 15: 'Q♦',
    16: 'K♠', 17: 'K♥', 18: 'K♣', 19: 'K♦',
    20: 'A♠', 21: 'A♥', 22: 'A♣', 23: 'A♦',
}

CARD_TO_INT = {
    '9♠': 0, '9♥': 1, '9♣': 2, '9♦': 3,
    '10♠': 4, '10♥': 5, '10♣': 6, '10♦': 7,
    'J♠': 8, 'J♥': 9, 'J♣': 10, 'J♦': 11,
    'Q♠': 12, 'Q♥': 13, 'Q♣': 14, 'Q♦': 15,
    'K♠': 16, 'K♥': 17, 'K♣': 18, 'K♦': 19,
    'A♠': 20, 'A♥': 21, 'A♣': 22, 'A♦': 23,
}

SUIT_TO_INT = {"♠": 0, "♥": 1, "♣": 2, "♦": 3}
INT_TO_SUIT = {0: "♠", 1: "♥", 2: "♣", 3: "♦"}

STATES = {
    "unset": 0,
    "set": 1,
    "none": 2
}  

RETURN_SELECTOR = {
    "random": 0,
    "best": 1,
    "worst": 2
}  

class QueryBase:
    def __init__(self, size, default = STATES['set']):
        self.values = array.array('B', [default] * size)

    def set(self, index):
        self.values[index] = STATES['set']

    def clear(self, index):
        self.values[index] = STATES['unset']

    def set_all(self):
        self.values = array.array('B', [STATES['set']] * self.size)

    def clear_all(self):
        self.values = array.array('B', [STATES['unset']] * self.size)

    @property
    def size(self):
        return len(self.values)

    def test(self, index):
        if index is None: return True
        return self.values[index] == STATES['set']                 

    def set_if(self, eval):
        for i in range(0, self.size):
            if eval(i): self.set(i)
            else: self.clear(i)
    
    def __str__(self):
        return del_string(self.values, ", ", "'")
    
    def __repr__(self):
        return del_string(self.values, ", ", "'")    

class QueryDeck(QueryBase):
    def __init__(self, default = STATES['set']):
        self.default = STATES['set']
        QueryBase.__init__(self, len(INT_TO_CARD), default)
        if default == STATES['set']: 
            self.flag_left_bower = True
        else:
            self.flag_left_bower = False

    def set_all(self):
        super().set_all()
        self.flag_left_bower = True

    def clear_all(self):
        super().clear_all()
        self.flag_left_bower = False
    
    def test(self, card: Card):
        if card is None: return True                
        norm_card = card.normalize()
        norm_index = CARD_TO_INT[norm_card]

        if norm_card == "J♣":
            if card.trump == None: return self.values[norm_index] == STATES['set'] 
            else: return self.flag_left_bower

        return self.values[norm_index] == STATES['set']   

    def select(self, phrase):
        for split in phrase.split():
            self._select(split)

    def _select(self, phrase):  
        if phrase.startswith('~'): 
            phrase = invert_phrase(phrase)

        ranks = re.findall(r'10|[9JQKAL]', phrase)
        suits = re.findall(r'[♠♥♣♦]', phrase)

        if len(suits) == 0: return self._set_cards(ranks, SUITS.keys())
        elif len(ranks) == 0: return self._set_cards(RANKS.keys(), suits)
        else: return self._set_cards(ranks, suits)   

    def _set_cards(self, ranks, suits):
        for rank in ranks:
            for suit in suits:
                self._set_card(rank, suit)

    def _set_card(self, rank, suit):
        rank_idx = RANKS[rank]
        suit_idx = SUITS[suit]

        if rank == "L" and suit == "♠":
            self.flag_left_bower = True

        idx = (rank_idx * 4) + suit_idx
        self.set(idx)

    # return all matching cards
    def all(self, cards):
        selected = Query_Result()
        for card in cards:
            if self.test(card):
                selected.append(card)

        return selected
    
    def __str__(self):
        sb = ""
        for i in INT_TO_CARD.keys():
            if i % 4 == 0: sb = sb + "\n"
            card = INT_TO_CARD[i]
            sb = sb + f"{card}:{self.values[i]} "
        return sb

class QueryDigit(QueryBase):
    def __init__(self, size):
        QueryBase.__init__(self, size)

    def select(self, phrase):
        self.clear_all()
        parts = re.findall(r'[0123456789]', phrase)
        for part in parts:
            self.set(int(part))        

    def __str__(self):
        return f"[{del_string(self.values)}]"

class Query:
    def __init__(self, phrase = None, name = None):
        self._hand = QueryDeck(STATES["unset"])
        self._up_card = QueryDeck(STATES["set"])
        self._down_card = QueryDeck(STATES["set"])
        self._lead = QueryDigit(4)
        self._maker = QueryDigit(4)
        self._dealer = QueryDigit(4)
        self._count =  QueryDigit(6)       
        self._wins = False # only keep cards that beat the best current card
        self._loses = False # only keep cards that the current card beats
        self._best = False # only keep the highest rank card preferably trump
        self._worst = False # only keep the lowest rank card preferably not trump
        self._playable = False # process only cards that are playable
        self.name = name
        if phrase is not None: self.select(phrase)

    def __str__(self):
        return f"[{self.name}]"

    def best(self):
        self.return_selector = RETURN_SELECTOR['best']
        return self

    def worst(self):
        self.return_selector = RETURN_SELECTOR['worst']
        return self   

    # if up and down card tests pass, return all matching hand cards
    def all(self, snap: Snapshot):
        if not self._up_card.test(snap.up_card): return Query_Result([])
        if not self._down_card.test(snap.down_card): return Query_Result([])

        norm_lead = normalize_value(snap.for_index, snap.lead_index)
        norm_maker = normalize_value(snap.for_index, snap.maker_index)
        norm_dealer = normalize_value(snap.for_index, snap.dealer_index)

        if not self._lead.test(norm_lead): return Query_Result([])        
        if not self._maker.test(norm_maker): return Query_Result([])
        if not self._dealer.test(norm_dealer): return Query_Result([])

        print("\n")
        print(self._hand)
        print(self._hand.flag_left_bower)
        all = self._hand.all(snap.hand)
        
        if self._playable == True: all = self.do_playable(all, snap)
        if self._wins == True: all = self.do_wins(all, snap)
        if self._loses == True: all = self.do_loses(all, snap)
        if self._best == True: all = self.do_best(all, snap)
        if self._worst == True: all = self.do_worst(all, snap)
        if not self._count.test(len(all)): return Query_Result([])   

        return all

    def do_playable(self, all: Query_Result, snap: Snapshot):   
        if len(snap.tricks) == 0: return all        
        if len(snap.tricks[-1]) == 0: return all
        if not snap.hand.has_suit(snap.tricks[-1].lead_suit): return all

        playable = Query_Result()
        for card in all:
            if card.suit_effective() == snap.tricks[-1].lead_suit:
                playable.append(card)

        return playable

    def do_loses(self, all, snap: Snapshot):
        if len(snap.tricks) == 0: return all
        if len(snap.tricks[-1]) == 0: return all        

        lead_suit = snap.tricks[-1].lead_suit
        best_card = snap.tricks[-1][0]

        selected = Query_Result()
        for card in all:
            winner = winning_card(lead_suit, best_card, card)
            loser = losing_card(lead_suit, best_card, card)            
            if loser == card: selected.append(loser)

        return selected

    def do_wins(self, all, snap: Snapshot):
        if len(snap.tricks) == 0: return all
        if len(snap.tricks[-1]) == 0: return all        

        lead_suit = snap.tricks[-1].lead_suit
        best_card = snap.tricks[-1][0]

        selected = Query_Result()
        for card in all:
            winner = winning_card(lead_suit, best_card, card)
            if winner == card: selected.append(winner)

        return selected

    def do_best(self, all, snap: Snapshot):
        if len(all) == 0: return Query_Result()
        if len(snap.tricks) == 0: return all
        if len(snap.tricks[-1]) == 0: return all

        lead_suit = snap.tricks[-1].lead_suit
        best_card = all[0]

        selected = Query_Result()
        for card in all:
            if best_card.compare(card, lead_suit) < 0:
                best_card = card

        selected.append(best_card)
        return selected

    def do_worst(self, all, snap: Snapshot):
        if len(all) == 0: return Query_Result()        
        if len(snap.tricks) == 0: return all
        if len(snap.tricks[-1]) == 0: return all        

        lead_suit = snap.tricks[-1].lead_suit
        worst_card = all[0]

        selected = Query_Result()
        for card in all:
            if worst_card.compare(card, lead_suit) > 0:
                worst_card = card

        selected.append(worst_card)
        return selected
    
    def select(self, phrase): 
        if self.name is None: 
            self.name = phrase

        self._hand.select(phrase)
        return self
    
    def count(self, phrase):
        self._count.clear_all()
        self._count.select(phrase)
        return self

    def lead(self, phrase):
        self._lead.clear_all()
        self._lead.select(phrase)
        return self

    def dealer(self, phrase):
        self._dealer.clear_all()
        self._dealer.select(phrase)
        return self

    def maker(self, phrase):
        self._maker.clear_all()
        self._maker.select(phrase)  
        return self

    def up_card(self, phrase):
        self._up_card.clear_all()
        self._up_card.select(phrase)  
        return self

    def down_card(self, phrase):
        self._down_card.clear_all()
        self._down_card.select(phrase) 
        return self

    def wins(self, value = True):
        self._wins = value
        return self
    
    def loses(self, value = True):
        self._loses = value
        return self    
    
    def worst(self, value = True):
        self._worst = value
        return self
    
    def best(self, value = True):
        self._best = value
        return self    

    def playable(self, value = True):
        self._playable = value
        return self          

def invert_phrase(phrase):
    split = re.findall(r"10|[9JQKAL♠♥♣♦]", phrase)
    inverted = re.findall(r"10|[9JQKAL♠♥♣♦]", "910JQKAL♠♥♣♦")
    for part in split:
        inverted.remove(part)

    return "".join(inverted)

def normalize_value(for_index, value, mod = 4):    
    if value is None: return None
    return (for_index + value) % 4