
class Query:
    suits: list[str] = ["♠", "♥", "♣", "♦"] # order matters
    values: list[str] = ["9", "10", "J", "Q", "K", "A"]

    def __init__(self, trump, hand, phrase = ""):
        self.trump = trump
        self.hand = hand
        self._src_phrase = phrase

    def phrase(self, phrase):
        self._src_phrase = phrase
        return self

    def _denormalize_phrase(self, trump):
        self.denorm_phrase = []
        split = self._src_phrase.split(" ")

        iTrump = Query.suits.index(trump)
        opposite = Query.suits[(iTrump + 2) % 4]
        off1 = Query.suits[(iTrump + 1) % 4]
        off2 = Query.suits[(iTrump + 3) % 4]

        for part in split:
            if   "♠" in part: self.denorm_phrase.append(part.replace("♠", trump))
            elif "♣" in part: self.denorm_phrase.append(part.replace("♣", opposite))
            elif "♥" in part: self.denorm_phrase.append(part.replace("♥", off1))
            elif "♦" in part: self.denorm_phrase.append(part.replace("♦", off2))
            else:             self.denorm_phrase.append(part)

    @property
    def count(self):
         return len(self.select)

    @property
    def select(self):
            result = []           
            if len(self.hand) == 0: return []

            if self.trump is None: raise Exception("Can not query before trump is set")
            self._denormalize_phrase(self.trump)

            has_suits = any(item in Query.suits for item in self.denorm_phrase)
            has_values = any(item in Query.values for item in self.denorm_phrase)
            
            if has_suits and not has_values:
                self.denorm_phrase.extend(Query.values)

            if has_values and not has_suits:
                self.denorm_phrase.extend(Query.suits)   

            for card in self.hand:
                if card.suit_effective(self.trump) in self.denorm_phrase and card.value in self.denorm_phrase: result.append(card)
                elif str(card) in self.denorm_phrase: result.append(card)

            return result        


