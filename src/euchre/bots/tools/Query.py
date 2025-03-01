import array
import re
from euchre import *
from euchre.util.Has_Hooks import Has_Hooks
from euchre.del_string import del_string
from .Query_Collection import Query_Collection
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
        selected = Query_Collection()
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

class Query(Query_Base, Has_Hooks):
    def __init__(self, phrase = '~', name = None, root = None):
        if name is None: name = phrase
        if name is None: name = self.__hash__()
        
        Query_Base.__init__(self, name)
        Has_Hooks.__init__(self)

        if root == None: self._root = self
        else: self._root = root

        self._hand = Query_Deck(STATES["unset"])
        self._up_card = Query_Deck(STATES["set"])
        self._down_card = Query_Deck(STATES["set"])
        self._lead = Query_Digit(4)
        self._maker = Query_Digit(4)
        self._dealer = Query_Digit(4)
        self._count =  Query_Digit(6)       
        self._winner = Query_Digit(4)
        self._wins = False     # only keep cards that beat the best current card
        self._loses = False    # only keep cards that the current card beats
        self._best = False     # only keep the highest rank card preferably trump
        self._worst = False    # only keep the lowest rank card preferably not trump
        self._playable = False # process only cards that are playable
        self._and = False      
        self._next = None

        if phrase is not None: self.select(phrase)

    @property
    def root(self):
        return self._root

    def link(self, phrase = "~"):
        if self._next is not None: 
            raise Exception("A query can only be linked once.")
                
        self._next = Query(phrase, self.name, self.root)
        return self._next

    def action_skip(self, snap, reason, selected):
        self._trigger_hook("after_all", query = self, snap = snap, all = selected)
        return Query_Result("rejected" , None, selected, reason)

    def decide(self, snap: Snapshot):
        self._stats.called()             
        return self._root._decide(snap)

    # if up and down card tests pass, return all matching hand cards
    def _decide(self, snap: Snapshot):
        self._trigger_hook("before_all", query = self, snap = snap)

        # test the query
        selected = self._hand.all(snap.hand) 

        if len(selected) == 0:
            return self.action_skip(snap, "empty hand", selected) 

        # tests that do not change selected
        if not self._up_card.test(snap.up_card): 
            return self.action_skip(snap, "up card", selected)
        
        if not self._down_card.test(snap.down_card): 
            return self.action_skip(snap, "down card", selected)
        
        norm_lead = normalize_value(snap.for_index, snap.lead_index)
        if not self._lead.test(norm_lead): 
            return self.action_skip(snap, "lead", selected)       

        norm_maker = normalize_value(snap.for_index, snap.maker_index)
        if not self._maker.test(norm_maker): 
            return self.action_skip(snap, "maker", selected)

        norm_dealer = normalize_value(snap.for_index, snap.dealer_index)
        if not self._dealer.test(norm_dealer): 
            return self.action_skip(snap, "dealer", selected)

        if snap.current_trick is not None:
            norm_winner = normalize_value(snap.for_index, snap.current_trick.winner)
            if not self._winner.test(norm_winner): 
                return self.action_skip(snap, "winner", selected)

        # tests that return an empty result using the query
        if not self._count.test(len(selected)): 
            return self.action_skip(snap, "count", selected)       

        # tests that change the contents selected
        if self._playable == True: 
            selected = self.do_playable(selected, snap)
            if len(selected) == 0:
                return self.action_skip(snap, "playable", selected) 

        if self._wins == True: 
            selected = self.do_wins(selected, snap)
            if len(selected) == 0:
                return self.action_skip(snap, "wins", selected) 

        if self._loses == True: 
            selected = self.do_loses(selected, snap)
            if len(selected) == 0:
                return self.action_skip(snap, "loses", selected)             

        self._trigger_hook("after_all", query = self, snap = snap, all = selected)

        if self._next is not None:            
            self._trigger_hook("on_match", query = self, snap = snap, all = selected)
            self._stats.activate()
            return self._next._decide(snap)
        else:
            query_result = None
            self._stats.activate()

            if self.data is not None:
                query_result = Query_Result(self.action, self.data, selected, "data provided")
            elif self._best == True:
                query_result = Query_Result(self.action, self.do_best(selected, snap), selected, "best")
            elif self._worst == True:
                query_result = Query_Result(self.action, self.do_worst(selected, snap), selected, "worst")
            else:
                query_result = Query_Result(self.action, selected[0], selected, "default")  
            
            self._trigger_hook("on_match", query = self, snap = snap, result = query_result)
            return query_result          

    def do_playable(self, all: Query_Collection, snap: Snapshot):   
        if len(snap.tricks) == 0: return all        
        if len(snap.tricks[-1]) == 0: return all
        if not snap.hand.has_suit(snap.tricks[-1].lead_suit): return all

        playable = Query_Collection()
        for card in all:
            if card.suit_effective() == snap.tricks[-1].lead_suit:
                playable.append(card)

        return playable

    def do_loses(self, all, snap: Snapshot):
        if len(snap.tricks) == 0: return all
        if len(snap.tricks[-1]) == 0: return all        

        lead_suit = snap.tricks[-1].lead_suit
        best_card = snap.tricks[-1][0]

        selected = Query_Collection()
        for card in all:
            winner = winning_card(lead_suit, best_card, card)
            loser = losing_card(lead_suit, best_card, card)            
            if loser == card: selected.append(loser)

        return selected

    def do_wins(self, all, snap: Snapshot):
        if len(snap.tricks) == 0: return all
        if len(snap.tricks[-1]) == 0: return all        

        lead_suit = snap.tricks[-1].lead_suit
        best_card = snap.tricks[-1].best_card

        selected = Query_Collection()
        for card in all:
            winner = winning_card(lead_suit, best_card, card)
            if winner == card: selected.append(winner)

        return selected

    def do_best(self, all, snap: Snapshot):
        lead_suit = None

        if len(all) == 0: return Query_Collection()  
        if len(snap.tricks) != 0 and len(snap.tricks[-1]) != 0: 
            lead_suit = snap.tricks[-1].lead_suit

        best = all[0]
        for card in all: best = best_card(best, card, lead_suit)

        return best

    def do_worst(self, all, snap: Snapshot):
        lead_suit = None

        if len(all) == 0: return Query_Collection()   
        if len(snap.tricks) != 0 and len(snap.tricks[-1]) != 0: 
            lead_suit = snap.tricks[-1].lead_suit

        worst = all[0]        
        for card in all: worst = worst_card(worst, card, lead_suit)

        return worst
    
    def select(self, phrase): 
        self._hand = Query_Deck(STATES["unset"])
        self._hand.select(phrase)
        return self  

    def winner(self, phrase):
        self._winner.clear_all()
        self._winner.select(phrase)
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
    return (value - for_index) % 4
