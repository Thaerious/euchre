import array
import re
import random

RANKS = {'9':0, '10':1, 'J':2, 'Q':3, 'K':4, 'A':5}
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
    def __init__(self, size, parent):
        self.values = array.array('B', [STATES['set']] * size)
        self.parent = parent

    def set(self, index):
        self.values[index] = STATES['set']

    def clear(self, index):
        self.values[index] = STATES['unset']

    def is_set(self, index):
        if not isinstance(index, int):
            index = CARD_TO_INT[str(index)]        
        return self.values[index] == STATES['set']        

    def set_if(self, eval):
        for i in range(0, len(self.values)):
            if eval(i): self.set(i)
            else: self.clear(i)
        return self.parent

    def test(self, index):
        if index is None: return True
        if not isinstance(index, int):
            index = CARD_TO_INT[str(index)] 
            return self.values[index] == STATES['set']
    
    def __str__(self):
        return str(self.values)    

class QueryDeck(QueryBase):
    def __init__(self, parent):
        QueryBase.__init__(self, 24, parent)
    
    def select(self, phrase):
        self.cards = array.array('B', [STATES['unset']] * 24)
        for split in phrase.split():
            self._select(split)
        return self.parent

    def _select(self, phrase):        
        ranks = re.findall(r'10|[9JQKAL]', phrase)
        suits = re.findall(r'[♠♥♣♦]', phrase)

        if 'L' in ranks and '♠' in suits:
            self.set(10)
            ranks.remove('L')

        for rank in ranks:
            rank_idx = RANKS[rank]
            for suit in suits:
                suit_idx = SUITS[suit]
                idx = (rank_idx * 4) + suit_idx
                self.set(idx)    

    # return all matching cards
    def all(self, cards):
        selected = []

        for card in cards:
            if self.is_set(card):
                selected.append(card)

        return selected
    
    # return true if any cards match
    def any(self, cards):
        for card in cards:
            if self.is_set(card):
                return True
            
        return False

class QueryDigit(QueryBase):
    def __init__(self, size, parent):
        QueryBase.__init__(self, size, parent)

    def select(self, phrase):
        self.digits = array.array('B', [STATES['unset']] * len(self.digits))
        parts = re.findall(r'0123456789', phrase)
        for part in parts:
            self.set(int(part))
        
        return self.parent            

class CQuery:
    def __init__(self):
        self.hand = QueryDeck(self)
        self.up_card = QueryDeck(self)
        self.down_card = QueryDeck(self)
        self.lead_player = QueryDigit(4, self)
        self.maker = QueryDigit(4, self)
        self.dealer = QueryDigit(4, self)
        self.count =  QueryDigit(6, self)        
        self.beats = False # keep cards that beat the best current card
        self.playable = False # keep only playable cards

        self.return_selector = RETURN_SELECTOR['random'] # return worst / best   
 
    def best(self):
        self.return_selector = RETURN_SELECTOR['best']
        return self

    def worst(self):
        self.return_selector = RETURN_SELECTOR['worst']
        return self

    def random(self):
        self.return_selector = RETURN_SELECTOR['worst']
        return self

    # used by bot to retrieve a seingle card, uses return_selector
    def get(self, snap):
        all = self.all(snap)

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

    # used by bot to return a true/false value using count
    def test(self, snap):
        if not self.up_card.test(snap.up_card): return False
        if not self.down_card.test(snap.down_card): return False
        if not self.lead_player.test(snap.lead): return False
        if not self.maker.test(snap.lead): return False
        if not self.dealer.test(snap.lead): return False           

        selected = self.hand.all(snap.hand)
        return self.count.test(len(selected))
    
    # if up and down card tests pass, return all matching hand cards
    def all(self, snap):
        if not self.up_card.test(snap.up_card): return []
        if not self.down_card.test(snap.down_card): return []
        if not self.lead_player.test(snap.lead): return []
        if not self.maker.test(snap.lead): return []
        if not self.dealer.test(snap.lead): return []
        return self.hand.all(snap.hand)
    
    # if up and down card tests pass, return true if any hand card matches
    def any(self, snap):      
        if not self.up_card.test(snap.up_card): return False
        if not self.down_card.test(snap.down_card): return False
        if not self.lead_player.test(snap.lead): return False
        if not self.maker.test(snap.lead): return False
        if not self.dealer.test(snap.lead): return False        
        return self.hand.any(snap.hand)

    def keep_playable(self, cards, snap):
        if len(self.snap.tricks) == 0:
            return cards
        
        if len(self.snap.tricks[-1]) == 0:
            return cards
        
        lead_suit = self.snap.tricks[-1].lead_suit  
        lead_suit = normalize(self.trump, lead_suit)

        with self.select(f"910JLQKA{lead_suit}") as q:
            if q.len > 0: return q
        
        return self.copy()
    
def normalize(trump, string):
    raw = list(string)
    normalized = []

    iTrump = SUITS.index(trump)
    opposite = SUITS.suits[(iTrump + 2) % 4]
    off1 = SUITS.suits[(iTrump + 1) % 4]
    off2 = SUITS.suits[(iTrump + 3) % 4]

    for c in raw:
        if c == trump:      normalized.append("♠")
        elif c == opposite: normalized.append("♣")
        elif c == off1:     normalized.append("♥")
        elif c == off2:     normalized.append("♦")
        else: normalized.append(c)

    return "".join(normalized)

def denormalize(trump, string):
    raw = list(string)
    denormalized = []

    iTrump = SUIT_TO_INT[trump]
    opposite = INT_TO_SUIT[(iTrump + 2) % 4]
    off1 = INT_TO_SUIT[(iTrump + 1) % 4]
    off2 = INT_TO_SUIT[(iTrump + 3) % 4]

    for c in raw:
        if   c == "♠": denormalized.append(trump)
        elif c == "♣": denormalized.append(opposite)
        elif c == "♥": denormalized.append(off1)
        elif c == "♦": denormalized.append(off2)
        else: denormalized.append(c)

    return "".join(denormalized)