import CardList
import Card
import random

class Deck(CardList):
    def __init__(self):
        for suit in Card.suits:
            for value in Card.values:
                self.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self)
        return self