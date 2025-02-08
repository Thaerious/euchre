from euchre.card.Card import Card

SUITS = ["♠", "♥", "♣", "♦"]

class Query_Result(list):
    def denormalize(self, source):
        trump = source.trump
        denorm = Query_Result()
        i = SUITS.index(trump)

        map = {
            "♠": trump,
            "♥": SUITS[(i + 1) % 4],
            "♣": SUITS[(i + 2) % 4],
            "♦": SUITS[(i + 3) % 4]
        }

        for item in self:
            string = str(item)
            rank = string[:-1]
            suit = map[string[-1]]
            denorm.append(Card(source, suit, rank))
        
        return denorm

    def get(self):
        if len(self) == 0: return None
        return self[0]

    def playable(self, snap):        
        if len(snap.tricks) == 0:
            return Query_Result(self)
        
        if len(snap.tricks[-1]) == 0:
            return Query_Result(self)

        if not snap.hand.has_suit(snap.tricks[-1].lead_suit):
            return Query_Result(self)

        playable = Query_Result()
        for card in self:
            if card.suit_effective() == snap.tricks[-1].lead_suit:
                playable.append(card)

        return playable