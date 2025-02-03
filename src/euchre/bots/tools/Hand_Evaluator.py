import re
from euchre.del_string import del_string

class Hand_Evaluator(list):
    suits: list[str] = ["♠", "♥", "♣", "♦"] # order matters
    ranks: list[str] = ["9", "10", "J", "Q", "K", "A"]

    def __init__(self, trump, source):
        self.extend(source)
        self._trump = trump

    def copy(self):
        return Hand_Evaluator(self._trump, self)

    def trump(self, new_trump):
        return Hand_Evaluator(new_trump, self)

    # if the query has any cards, perform this action
    def then(self, cb):
        if len(self) >= 0: cb(self)
        return Hand_Evaluator(self._trump, self)

    # return all cards that could win the current trick
    def beats(self, trick):
        result = []

        for card in self:
            if trick.compare_card(card) > 0:
                result.append(card)

        return Hand_Evaluator(self._trump, result)

    def loses(self, trick):
        result = []

        for card in self:
            if trick.compare_card(card) <= 0:
                result.append(card)

        return Hand_Evaluator(self._trump, result)

    def count(self, phrase = "910JQKA♠♥♣♦"):
         return len(self.select(phrase))

    def select(self, phrase = "910JQKA♠♥♣♦"):
        result = []           
        if len(self) == 0: return Hand_Evaluator(self._trump, result)

        phrase = expand_cards(phrase)

        if self._trump is not None:
            phrase = denormalize_phrase(phrase, self._trump)

        for card in self:
            if not card in phrase: continue
            if card in result: continue
            result.append(card)

        return Hand_Evaluator(self._trump, result)

    def by_rank(self, phrase = "910JQKA♠♥♣♦"):
        q = self.select(phrase)
        list = sorted(q, key = lambda card: Hand_Evaluator.ranks.index(card.rank))        
        return Hand_Evaluator(self._trump, list)

    def by_suit(self, phrase = "910JQKA♠♥♣♦"):
        q = self.select(phrase)
        list = sorted(q, key = lambda card: Hand_Evaluator.suits.index(card.suit))        
        return Hand_Evaluator(self._trump, list)
    
    def __str__(self):
        return f"[{del_string(self, ",", '"')}]"
    
    def __repr__(self):
        return f"[{del_string(self, ",", '"')}]"   


# turn a card query string into an array of card strings
def expand_cards(phrase):
    cards = []
    suit_opposites = {"♠": "♣", "♣": "♠", "♦": "♥", "♥": "♦"}

    parts = re.findall(r'10|[9JQKAL♠♣♦♥]', phrase)
    for part1 in parts:
        if part1 in Hand_Evaluator.ranks:
            for part2 in parts:
                if part1 in Hand_Evaluator.suits:
                    cards.append(f"{part1}{part2}")
        if part1 in Hand_Evaluator.suits:
            for part2 in parts:
                if part1 in Hand_Evaluator.ranks:
                    cards.append(f"{part2}{part1}")                    

    for i, card in enumerate(cards):
        if card.starts_with("L") and card[-1] == "♠":
            suit = suit_opposites[card[-1]]
            cards[i] = f"J{suit}"

    return cards

# convert a normalized card query string into non-normalized string
def denormalize_phrase(source, trump):
    result = []

    iTrump = Hand_Evaluator.suits.index(trump)
    opposite = Hand_Evaluator.suits[(iTrump + 2) % 4]
    off1 = Hand_Evaluator.suits[(iTrump + 1) % 4]
    off2 = Hand_Evaluator.suits[(iTrump + 3) % 4]

    for part in source:
        if   "♠" in part: result.append(part.replace("♠", trump))
        elif "♣" in part: result.append(part.replace("♣", opposite))
        elif "♥" in part: result.append(part.replace("♥", off1))
        elif "♦" in part: result.append(part.replace("♦", off2))
        else:             result.append(part)

    return result