import array
import re
import random

RANKS = {'9':0, '10':1, 'J':2, 'Q':3, 'K':4, 'A':5, 'L':2}
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
        if not isinstance(index, int):
            index = CARD_TO_INT[str(index)]        
        return self.values[index] == STATES['set']        

    def set_if(self, eval):
        for i in range(0, self.size):
            if eval(i): self.set(i)
            else: self.clear(i)
    
    def __str__(self):
        return str(self.values)    

class QueryDeck(QueryBase):
    def __init__(self, default = STATES['set']):
        QueryBase.__init__(self, 24, default)
    
    def select(self, phrase):
        if phrase.startswith('~'):
            self.set_all()

        for split in phrase.split():
            self._select(split)

    def _select(self, phrase):        
        ranks = re.findall(r'10|[9JQKAL]', phrase)
        suits = re.findall(r'[♠♥♣♦]', phrase)

        if 'L' in ranks and '♠' in suits:
            self.set(10)
            ranks.remove('L')

        if phrase.startswith('~'):
            if len(suits) == 0: return self._clear_cards(ranks, SUITS.keys())
            elif len(ranks) == 0: return self._clear_cards(RANKS.keys(), suits)
            else: return self._clear_cards(ranks, suits)
        else:
            if len(suits) == 0: return self._set_cards(ranks, SUITS.keys())
            elif len(ranks) == 0: return self._set_cards(RANKS.keys(), suits)
            else: return self._set_cards(ranks, suits)
    
    def _clear_cards(self, ranks, suits):
        for rank in ranks:
            for suit in suits:
                self._clear_card(rank, suit)

    def _set_cards(self, ranks, suits):
        for rank in ranks:
            for suit in suits:
                self._set_card(rank, suit)

    def _clear_card(self, rank, suit):
        rank_idx = RANKS[rank]
        suit_idx = SUITS[suit]

        if rank == "L": 
            suit_idx = (suit_idx + 2) % 4

        idx = (rank_idx * 4) + suit_idx
        self.clear(idx)

    def _set_card(self, rank, suit):
        rank_idx = RANKS[rank]
        suit_idx = SUITS[suit]

        if rank == "L": 
            suit_idx = (suit_idx + 2) % 4

        idx = (rank_idx * 4) + suit_idx
        self.set(idx)

    # return all matching cards
    def all(self, cards):
        selected = []

        for card in cards:
            if self.test(card):
                selected.append(card)

        return selected
    
    # return true if any cards match
    def any(self, cards):
        for card in cards:
            if self.test(card):
                return True
            
        return False

class QueryDigit(QueryBase):
    def __init__(self, size):
        QueryBase.__init__(self, size)

    def select(self, phrase):
        self.clear_all()
        parts = re.findall(r'0123456789', phrase)
        for part in parts:
            self.set(int(part))        

class CQuery:
    def __init__(self):
        self._hand = QueryDeck(STATES["unset"])
        self._up_card = QueryDeck()
        self._down_card = QueryDeck()
        self._lead = QueryDigit(4)
        self._maker = QueryDigit(4)
        self._dealer = QueryDigit(4)
        self._count =  QueryDigit(6)        
        self._beats = False # keep cards that beat the best current card
        self._playable = False # keep only playable cards

        self.return_selector = RETURN_SELECTOR['random'] # return worst / best if not set, random 
 
    def best(self):
        self.return_selector = RETURN_SELECTOR['best']
        return self

    def worst(self):
        self.return_selector = RETURN_SELECTOR['worst']
        return self

    # used by bot to retrieve a single card, uses return_selector
    # must return either a single card or none
    def get(self, snap):
        all = self.all(snap)
        if len(all) == 0: return None

        if self.return_selector == RETURN_SELECTOR['random']:
            return random.choice(all)
        elif self.return_selector == RETURN_SELECTOR['best']:
            best = all[0]
            for card in all[1:]:
                if best.compare(card) < 0: best = card
            return best
        elif self.return_selector == RETURN_SELECTOR['worst']:
            worst = all[0]
            for card in all[1:]:
                print(f"{worst} - {card} = {worst.compare(card)}"); 
                if worst.compare(card) >= 0: worst = card
            return worst
    
    # if up and down card tests pass, return all matching hand cards
    def all(self, snap):
        if not self._up_card.test(snap.up_card): return []
        if not self._down_card.test(snap.down_card): return []
        if not self._lead.test(snap.lead): return []
        if not self._maker.test(snap.maker): return []
        if not self._dealer.test(snap.dealer): return []
        return self._hand.all(snap.hand)

    def playable(self, snap):
        if len(snap.tricks) == 0 or len(snap.tricks[-1]) == 0: 
            self._hand.set_all()
            return self
        
        lead_suit = snap.tricks[-1].lead_suit
        print(lead_suit)
        self.select(f"910JLQKAL{lead_suit}")
        
        return self
    
    def select(self, phrase): 
        self._hand.select(phrase)
        return self
    
    def _count(self, eval):
        self._count.set_if(eval)
        return self
