import CardList

class Hand(CardList):
    # Given 'trick' return the cards in this hand that can be played.
    def playable_cards(self, trick):
        cards = CardList()
        for card in self:
            if trick.can_play(card):
                cards.append(card)
                
        return cards   