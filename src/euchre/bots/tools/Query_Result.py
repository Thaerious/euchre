SUITS = ["♠", "♥", "♣", "♦"]

class Query_Result(list):
    def denormalize(self, trump):
        denorm = []
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
            denorm.append(f"{rank}{suit}")
        
        return denorm