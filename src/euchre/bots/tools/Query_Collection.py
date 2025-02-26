from euchre.card.Card import Card

SUITS = ["♠", "♥", "♣", "♦"]

class Query_Collection(list):
    def __init__(self, query):
        self.query = query

    def get(self):
        if len(self) == 0: return None
        return self[0]