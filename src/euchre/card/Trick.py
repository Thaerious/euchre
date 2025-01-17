import Card

# A list of cards starting with the lead player
class Trick(list):
    @staticmethod
    def build(trump, cards):
        trick = Trick(trump)
        for i, card in enumerate(cards):
            trick.append(i, card)

    def __init__(self, trump):
        list.__init__(self)
        self.who_played = {}
        self.trump = trump

    # retrieve the pIndex of the lead player
    def getLead(self):
        return self[0][0]

    def getLeadSuit(self):
        return self[0].suit_effective(self.trump)

    def append(self, pIndex, card):
        if isinstance(card, str): card = Card(card)

        list.append(self, card)
        self.who_played[card] = pIndex

    # return the winning card
    def bestCard(self):
        if len(self) < 1: return None
        if len(self) == 1: return self[0]
        
        bestCard = self[0]
        
        for card in self:
            if (bestCard.compare(card, self.getLeadSuit(), self.trump) < 0):
                 bestCard = card

        return bestCard 
                  
    # return the player index of the winning player
    def winner(self):
        best = self.bestCard()
        for card, pIndex in self.who_played:
            if card == best: return pIndex

    # Can 'card' be played on this trick?
    def can_play(self, card):
        if isinstance(card, str): card = Card(card)

        print(f"{self} Trick.can_play({card})")

        # empty trick
        if len(self) == 0: return True

        # subject card suit matches leading card suit
        leadSuit = self[0].suit
        if card.suit_effective(self.trump) == leadSuit: return True

        # if any other card in the hand matches suit
        for cardInHand in self:
            if cardInHand == card: continue
            if cardInHand.suit_effective(self.trump) == leadSuit: return False

        return True

    def __str__(self):
        sb = ""
        for card in self:
            if card == self.bestCard():
                sb = sb + f"[{self.who_played[card]}, {card}*]"
            else:
                sb = sb + f"[{self.who_played[card]}, {card}]"

        return sb

    def __repr__(self):
        return str(self)