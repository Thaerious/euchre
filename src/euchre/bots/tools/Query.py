import array
import re
from euchre import *
from euchre.del_string import del_string
from .Query_Result import Query_Result
from euchre.card.Card import *
from .Query_Base import Query_Base
from euchre.card.compare_cards import best_card, worst_card

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

class Query_Part:
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

class Query_Deck(Query_Part):
    def __init__(self, default = STATES['set']):
        self.default = STATES['set']
        Query_Part.__init__(self, len(INT_TO_CARD), default)
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
        selected = Query_Result(self)
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

class Query_Digit(Query_Part):
    def __init__(self, size):
        Query_Part.__init__(self, size)

    def select(self, phrase):
        self.clear_all()
        parts = re.findall(r'[0123456789]', phrase)
        for part in parts:
            self.set(int(part))        

    def __str__(self):
        return f"{del_string(self.values)}"

class Query(Query_Base):
    def __init__(self, phrase = None, name = None):
        if name is None: name = phrase
        if name is None: name = self.__hash__()
        Query_Base.__init__(self, name)

        self._hand = Query_Deck(STATES["unset"])
        self._up_card = Query_Deck(STATES["set"])
        self._down_card = Query_Deck(STATES["set"])
        self._lead = Query_Digit(4)
        self._maker = Query_Digit(4)
        self._dealer = Query_Digit(4)
        self._count =  Query_Digit(6)       
        self._wins = False     # only keep cards that beat the best current card
        self._loses = False    # only keep cards that the current card beats
        self._best = False     # only keep the highest rank card preferably trump
        self._worst = False    # only keep the lowest rank card preferably not trump
        self._playable = False # process only cards that are playable
        self._and = False      
        self._root = self
        self._next = None

        if phrase is not None: self.select(phrase)
        self._hooks = {} 

    def register_hook(self, event: str, func):
        """Register a function to a hook event."""
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(func)

        print(self._hooks, self.__hash__())
        return self

    def _trigger_hook(self, event: str, *args, **kwargs):
        """Trigger all hooks associated with an event."""
        if event in self._hooks:
            for func in self._hooks[event]:
                func(*args, **kwargs)

        return self

    def link(self, phrase = "~"):
        if self._next is not None: raise Exception("A query can only be linked once.")
        new_query = Query(phrase, self.name)
        new_query._root = self._root
        self._next = new_query
        return new_query

    def best(self):
        self.return_selector = RETURN_SELECTOR['best']
        return self

    def worst(self):
        self.return_selector = RETURN_SELECTOR['worst']
        return self   

    def empty_result(self, snap):
        all = Query_Result([]) 
        self._trigger_hook("after_all", query = self, snap = snap, all = all)
        return all 

    def all(self, snap: Snapshot):
        self._stats.called()
        return self._root._all(snap)

    # if up and down card tests pass, return all matching hand cards
    def _all(self, snap: Snapshot):
        self._trigger_hook("before_all", query = self, snap = snap)

        # tests that return an empty result despite the query
        if not self._up_card.test(snap.up_card): return self.empty_result(snap)
        if not self._down_card.test(snap.down_card): return self.empty_result(snap)

        norm_lead = normalize_value(snap.for_index, snap.lead_index)
        norm_maker = normalize_value(snap.for_index, snap.maker_index)
        norm_dealer = normalize_value(snap.for_index, snap.dealer_index)

        if not self._lead.test(norm_lead): return self.empty_result(snap)       
        if not self._maker.test(norm_maker): return self.empty_result(snap)
        if not self._dealer.test(norm_dealer): return self.empty_result(snap)

        # test the query
        all = self._hand.all(snap.hand)        

        # tests that return an empty result using the query
        if not self._count.test(len(all)): return self.empty_result(snap)       

        # tests that change the contents of the query
        if self._playable == True: all = self.do_playable(all, snap)
        if self._wins == True: all = self.do_wins(all, snap)
        if self._loses == True: all = self.do_loses(all, snap)
        if self._best == True: all = self.do_best(all, snap)
        if self._worst == True: all = self.do_worst(all, snap) 

        self._trigger_hook("after_all", query = self, snap = snap, all = all)
        
        if len(all) == 0:
            return all
        elif self._next is not None: 
            self._trigger_hook("on_match", query = self, snap = snap, all = all)
            self._stats.activate()
            return self._next._all(snap)
        else:
            self._trigger_hook("on_match", query = self, snap = snap, all = all)
            self._stats.activate()
            return all

    def do_playable(self, all: Query_Result, snap: Snapshot):   
        if len(snap.tricks) == 0: return all        
        if len(snap.tricks[-1]) == 0: return all
        if not snap.hand.has_suit(snap.tricks[-1].lead_suit): return all

        playable = Query_Result(self)
        for card in all:
            if card.suit_effective() == snap.tricks[-1].lead_suit:
                playable.append(card)

        return playable

    def do_loses(self, all, snap: Snapshot):
        if len(snap.tricks) == 0: return all
        if len(snap.tricks[-1]) == 0: return all        

        lead_suit = snap.tricks[-1].lead_suit
        best_card = snap.tricks[-1][0]

        selected = Query_Result(self)
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

        selected = Query_Result(self)
        for card in all:
            winner = winning_card(lead_suit, best_card, card)
            if winner == card: selected.append(winner)

        return selected

    def do_best(self, all, snap: Snapshot):
        lead_suit = None

        if len(all) == 0: return self.empty_result(snap)   
        if len(snap.tricks) != 0 and len(snap.tricks[-1]) != 0: 
            lead_suit = snap.tricks[-1].lead_suit

        best = all[0]
        for card in all: best = best_card(best, card, lead_suit)

        selected = Query_Result(self)
        selected.append(best)
        return selected

    def do_worst(self, all, snap: Snapshot):
        lead_suit = None

        if len(all) == 0: return self.empty_result(snap)   
        if len(snap.tricks) != 0 and len(snap.tricks[-1]) != 0: 
            lead_suit = snap.tricks[-1].lead_suit

        worst = all[0]        
        for card in all: worst = worst_card(worst, card, lead_suit)

        selected = Query_Result(self)
        selected.append(worst)
        return selected
    
    def select(self, phrase): 
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
