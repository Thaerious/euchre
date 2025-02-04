import re

class Query(list):
    suits: list[str] = ["♠", "♥", "♣", "♦"] # order matters
    ranks: list[str] = ["9", "10", "J", "Q", "K", "A", "L"]
    pattern = re.compile(r"(~)?([910JKQLA]*)([♠♥♣♦]*)")
    rank_pattern = re.compile(r"(9|10|J|Q|K|A|L)")
    suit_pattern = re.compile(r"(♠|♥|♣|♦)")

    def __init__(self, snap, trump = None):
        self.snap = snap
        self.extend(snap.hand)

        if trump is None:
            self.trump = snap.trump
        else:
            self.trump = trump

    @property
    def trump(self):
        return self._trump
    
    @trump.setter
    def trump(self, value):
        if value != None and not value in Query.suits:
            raise Exception(f"Trump must be None or a suit: {value}")
        self._trump = value
    
    @property
    def len(self):
        return len(self)
    
    @property
    def first(self):
        if self.len > 0:
            return self[0]
        else:        
            return None

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def copy(self, cards = None):
        copied = Query(self.snap, self.trump)
        copied.clear()

        if cards == None:
            copied.extend(self)
        else:
            copied.extend(cards)

        return copied

    def set(self, cards):
        self.clear()
        self.extend(cards)
        return self

    def playable(self):
        if len(self.snap.tricks) == 0:
            return self.copy()
        
        if len(self.snap.tricks[-1]) == 0:
            return self.copy()
        
        lead_suit = self.snap.tricks[-1].lead_suit
        lead_suit = normalize(self.trump, lead_suit)

        with self.select(f"910JLQKA{lead_suit}") as q:
            if q.len > 0: return q
        
        return self.copy()

    def dealer(self, phrase):
        d = (self.snap.dealer - self.snap.for_player) % 4
        digits = [int(char) for char in phrase]        
        if not d in digits: return self.copy([])
        return self.copy()

    def maker(self, query):
        m = (self.snap.dealer - self.snap.for_player) % 4
        if query == "" and m is None: self.copy()        
        digits = [int(char) for char in query]
        if not m in digits: return self.copy([])
        return self.copy()

    def lead(self, query):
        l = (self.snap.active_player - self.snap.for_player) % 4
        digits = [int(char) for char in query]
        if not m in digits: return self.copy([])
        return self.copy()

    def down(self, phrase):
        q = self.copy([self.snap.down_card])
        r = q.select(phrase)

        if r.len > 0:
            return self.copy()
        else:
            return self.copy([])

    # if has returns all, doesn't return select
    # if not has returns none
    def has(self, phrase):
        if self.select(phrase).len > 0:
            return self.copy()
        else:
            return self.copy([])
    
    def select(self, phrase):
        all_selected = []

        if self.trump is not None: 
            phrase = denormalize(self.trump, phrase)

        # if the first phrase starts with ~ start with all selected
        if phrase.strip().startswith('~'):
            all_selected.extend(self)

        for split_phrase in phrase.split():
            match = Query.pattern.match(split_phrase)
            (inv, ranks, suits) = match.groups()

            if (inv is None):
                selected = self
                if ranks == "": 
                    selected = select_suits(suits, selected, self.trump)
                elif suits == "": 
                    selected = select_ranks(ranks, selected, self.trump)
                else:
                    selected = select_suits(suits, selected, self.trump)
                    selected = select_ranks(ranks, selected, self.trump)
                all_selected.extend(selected)
            else:
                rejected = self
                if ranks == "": 
                    rejected = select_suits(suits, rejected, self.trump)
                elif suits == "": 
                    rejected = select_ranks(ranks, rejected, self.trump)
                else:
                    rejected = select_suits(suits, rejected, self.trump)
                    rejected = select_ranks(ranks, rejected, self.trump)

                for card in all_selected:
                    if card in rejected:
                        all_selected.remove(card)
            
        return self.copy(all_selected)    

def select_ranks(ranks, cards, trump):
    selected = []
    find_ranks = Query.rank_pattern.findall(ranks)
    for rank in find_ranks:
        for card in cards:
            if card.rank == rank:
                selected.append(card)
            if rank == "L" and card.is_left_bower(trump):
                selected.append(card)
    return selected

def select_suits(suits, cards, trump):
    selected = []
    find_suits = Query.suit_pattern.findall(suits)
    for suit in find_suits:
        for card in cards:
            if card.suit_effective(trump) == suit:
                selected.append(card)
    return selected            

def invert_expanded(cards):
    result = []
    for rank in ["9", "10", "J", "Q", "K", "A"]:
        for suit in Query.suits:
            card = f"{rank}{suit}"            
            if not card in cards: 
                result.append(card) 
    return result

def normalize(trump, string):
    raw = list(string)
    normalized = []

    iTrump = Query.suits.index(trump)
    opposite = Query.suits[(iTrump + 2) % 4]
    off1 = Query.suits[(iTrump + 1) % 4]
    off2 = Query.suits[(iTrump + 3) % 4]

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

    iTrump = Query.suits.index(trump)
    opposite = Query.suits[(iTrump + 2) % 4]
    off1 = Query.suits[(iTrump + 1) % 4]
    off2 = Query.suits[(iTrump + 3) % 4]

    for c in raw:
        if   c == "♠": denormalized.append(trump)
        elif c == "♣": denormalized.append(opposite)
        elif c == "♥": denormalized.append(off1)
        elif c == "♦": denormalized.append(off2)
        else: denormalized.append(c)

    return "".join(denormalized)