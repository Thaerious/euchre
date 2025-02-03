import re

class Query(list):
    suits: list[str] = ["♠", "♥", "♣", "♦"] # order matters
    ranks: list[str] = ["9", "10", "J", "Q", "K", "A", "L"]

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

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def copy(self):
        copied = Query(self.snap, self.trump)
        copied.clear()
        copied.extend(self)
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

    def dealer(self, query):
        digits = [int(char) for char in query]        
        if not self.snap.dealer in digits: self.clear()
        return self.copy()

    def maker(self, query):
        if query == "" and self.snap.maker is None:
            return True
        
        digits = [int(char) for char in query]
        if not self.snap.maker in digits: self.clear()
        return self.copy()

    def down(self, query):
        if self.snap.down_card is None: return self.copy()

        expanded = expand_query(query, self.trump is not None)

        if self.trump is not None:
            expanded = denormalize(expanded, self.trump)   

        if self.snap.down_card in expanded:
            return self.copy()
        
        self.clear()
        return self.copy()        

    def has(self, query):
        expanded = expand_query(query)

        if self.trump is not None:
            expanded = denormalize(expanded, self.trump)

        for card in expanded:
            if card in self:
                return self.copy()

        self.clear()
        return self.copy()

    def select(self, query):
        selected = []

        expanded = expand_query(query, self.trump is not None)

        if self.trump is not None:
            expanded = denormalize(expanded, self.trump)

        for card in expanded:
            if card in self:
                selected.append(card)

        return Query(self.snap, self.trump).set(selected)

    @property
    def len(self):
        return len(self)
    
    @property
    def first(self):
        if self.len > 0:
            return self.copy()[0]
        else:        
            return None

def expand_query(phrase, normal = True):
    cards = []    
    for split in phrase.split():
        cards.extend(_expand_cards(split, normal))

    return cards

# turn a card query string into an array of single card strings
# if normal, there is no J♣ it is L♠
# set normal to true when trump is set
def _expand_cards(phrase, normal = True):   
    cards = []
    phrase = correct_phrase(phrase)

    parts = re.findall(r'10|[9JQKAL♠♣♦♥]', phrase)
    for part1 in parts:
        if part1 in Query.ranks:
            for part2 in parts:
                if part2 in Query.suits:
                    card = f"{part1}{part2}"
                    if not card in cards: cards.append(card)
        elif part1 in Query.suits:
            for part2 in parts:
                if part2 in Query.ranks:
                    card = f"{part2}{part1}"
                    if not card in cards: cards.append(card)                      

    if "L♣" in cards: cards.remove("L♣")
    if "L♦" in cards: cards.remove("L♦")
    if "L♥" in cards: cards.remove("L♥")

    if normal:
        if "J♣" in cards: cards.remove("J♣")
        if "L♠" in cards: cards[cards.index("L♠")] = "J♣"
    else:
        if "L♠" in cards: cards.remove("L♠")

    if "~" in phrase:    
        return invert_expanded(cards)    
    else:
        return cards

def invert_expanded(cards):
    result = []
    for rank in ["9", "10", "J", "Q", "K", "A"]:
        for suit in Query.suits:
            card = f"{rank}{suit}"            
            if not card in cards: 
                result.append(card) 
    return result

def correct_phrase(phrase):
    if not any(suit in phrase for suit in Query.suits):
        phrase = phrase + "♠♥♣♦"

    if not any(rank in phrase for rank in Query.ranks):
        phrase = "910JQKAL" + phrase

    return phrase


def normalize(trump, string):
    normed = ""

    iTrump = Query.suits.index(trump)
    opposite = Query.suits[(iTrump + 2) % 4]
    off1 = Query.suits[(iTrump + 1) % 4]
    off2 = Query.suits[(iTrump + 3) % 4]

    for c in string:
        if c == trump:      normed = normed + "♠"
        elif c == opposite: normed = normed + "♣"
        elif c == off1:     normed = normed + "♥"
        elif c == off2:     normed = normed + "♦"
        else: normed = normed + c

    return normed

def denormalize(cards, trump):
    result = []

    iTrump = Query.suits.index(trump)
    opposite = Query.suits[(iTrump + 2) % 4]
    off1 = Query.suits[(iTrump + 1) % 4]
    off2 = Query.suits[(iTrump + 3) % 4]

    for card in cards:
        if   "♠" in card: result.append(card.replace("♠", trump))
        elif "♣" in card: result.append(card.replace("♣", opposite))
        elif "♥" in card: result.append(card.replace("♥", off1))
        elif "♦" in card: result.append(card.replace("♦", off2))

    return result