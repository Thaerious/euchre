import re
from euchre.del_string import del_string
from euchre.card.Trick import Trick

class Query(list):
    suits: list[str] = ["♠", "♥", "♣", "♦"] # order matters
    ranks: list[str] = ["9", "10", "J", "Q", "K", "A"]

    def __init__(self, trump, source):
        self.extend(source)
        self._trump = trump

    def copy(self):
        return Query(self._trump, self)

    def trump(self, new_trump):
        return Query(new_trump, self)

    # if the query has any cards, perform this action
    def then(self, cb):
        if len(self) >= 0: cb(self)
        return Query(self._trump, self)

    # return all cards that could win the current trick
    def beats(self, trick):
        result = []

        for card in self:
            if trick.compare_card(card) > 0:
                result.append(card)

        return Query(self._trump, result)

    def loses(self, trick):
        result = []

        for card in self:
            if trick.compare_card(card) <= 0:
                result.append(card)

        return Query(self._trump, result)

    def count(self, phrase = "910JQKA♠♥♣♦"):
         return len(self.select(phrase))

    def select(self, phrase = "910JQKA♠♥♣♦"):
        result = []           
        if len(self) == 0: return Query(self._trump, result)

        phrase = expand_cards(phrase)

        if self._trump is not None:
            phrase = denormalize_phrase(phrase, self._trump)

        for card in self:
            if not card in phrase: continue
            if card in result: continue
            result.append(card)

        return Query(self._trump, result)

    def by_rank(self, phrase = "910JQKA♠♥♣♦"):
        q = self.select(phrase)
        list = sorted(q, key = lambda card: Query.ranks.index(card.rank))        
        return Query(self._trump, list)

    def by_suit(self, phrase = "910JQKA♠♥♣♦"):
        q = self.select(phrase)
        list = sorted(q, key = lambda card: Query.suits.index(card.suit))        
        return Query(self._trump, list)
    
    def __str__(self):
        return f"[{del_string(self, ",", '"')}]"
    
    def __repr__(self):
        return f"[{del_string(self, ",", '"')}]"   

def expand_cards(input_str):
    result = []
    suit_opposites = {"♠": "♣", "♣": "♠", "♦": "♥", "♥": "♦"}

    for part in input_str.split(" "):    
        match = re.match(r'([109JQKAL]*)([♠♣♦♥]*)', part)
        if not match: raise Exception("Invalid input")
        
        ranks, suits = match.groups()
        if len(suits) == 0: suits = "♠♣♦♥"

        ranks = re.findall(r'10|[9JQKAL]', ranks)
        part_result = []

        for suit in suits:
            for rank in _fix_ranks(suit, ranks):
                if rank == "L":
                    part_result.append(f"J{suit_opposites[suit]}")
                else:
                    part_result.append(f"{rank}{suit}")
                    
        result.extend(part_result)

    return result

def _fix_ranks(suit, ranks):
    if len(ranks) > 0: return ranks
    if suit == "♠": return ["9", "10", "Q", "K", "A", "L", "J"]
    return ["9", "10", "J", "Q", "K", "A"]

def denormalize_phrase(source, trump):
    result = []

    iTrump = Query.suits.index(trump)
    opposite = Query.suits[(iTrump + 2) % 4]
    off1 = Query.suits[(iTrump + 1) % 4]
    off2 = Query.suits[(iTrump + 3) % 4]

    for part in source:
        if   "♠" in part: result.append(part.replace("♠", trump))
        elif "♣" in part: result.append(part.replace("♣", opposite))
        elif "♥" in part: result.append(part.replace("♥", off1))
        elif "♦" in part: result.append(part.replace("♦", off2))
        else:             result.append(part)

    return result