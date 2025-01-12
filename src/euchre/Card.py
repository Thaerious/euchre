import random
from euchre.delString import delString

def compare_card_by_suit(card1, card2):
    if isinstance(card1, str): card1 = Card(card1)
    if isinstance(card2, str): card2 = Card(card2)

    suit_index1 = Card.suits.index(card1.suit)
    suit_index2 = Card.suits.index(card2.suit)
    value_index1 = Card.values.index(card1.value)
    value_index2 = Card.values.index(card2.value)

    if suit_index1 != suit_index2:
        return suit_index2 - suit_index1
    else:
        return value_index2 - value_index1    

class CardList(list):
    def __init__(self, stringList = []):
        for string in stringList:
            self.append(Card(string))

    def randomItem(self):
        if len(self) == 0: return None
        index = random.randint(0, len(self)) - 1
        return self[index]     

    def __str__(self):
        return delString(self)

class Hand(CardList):
    # Given 'trick' and 'trump' return the cards in 'self' that can be played.
    def playableCards(self, trick, trump):
        cards = CardList()
        for card in self:
            if trick.canPlay(card, self, trump):
                cards.append(card)
                
        return cards   

# A list of cards starting with the lead player
class Trick(list):
    def __init__(self, trump):
        list.__init__(self)
        self.who_played = {}
        self.trump = trump

    # retrieve the pIndex of the lead player
    def getLead(self):
        return self[0][0]

    def getLeadSuit(self):
        return self[0].getSuit(self.trump)

    def append(self, pIndex, card):
        list.append(self, card)
        self.who_played[card] = pIndex

    # return the winning card
    def bestCard(self):
        if len(self) < 1: return None
        bestCard = self[0]
        
        for card in self:               
            if (bestCard.compare(card, self.trump) < 0):
                 bestCard = card

        return bestCard 
                  
    # return the player index of the winning player
    def winner(self):
        best = self.bestCard()
        for card, pIndex in self.who_played:
            if card == best: return pIndex

    # Can 'card' be played if 'self' is the current trick.
    def canPlay(self, card, hand):
        if not isinstance(card, Card): raise TypeError(f"expected Card, found {type(card)}")
        if not isinstance(hand, CardList): raise TypeError(f"expected CardList, found {type(hand)}")
        if not isinstance(self.trump, str): raise TypeError(f"expected str, found {type(self.trump)}")

        # empty trick
        if len(self) == 0: return True

        # subject card suit matches leading card suit
        leadSuit = self[0].suit
        if card.getSuit(self.trump) == leadSuit: return True

        # if any other card in the hand matches suit
        for cardInHand in self:
            if cardInHand == card: continue
            if cardInHand.getSuit(self.trump) == leadSuit: return False

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


class Deck(CardList):
    def __init__(self):
        for suit in Card.suits:
            for value in Card.values:
                self.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self)
        return self

class Card:
    suits = ["♥", "♠", "♣", "♦"]
    values = ["9", "10", "J", "Q", "K", "A"]

    def __init__(self, suit, value = None):
        if value == None:
            # initialize from card string ie "10♥"
            self.suit = suit[-1]
            self.value = suit[:-1]
        else:
            self.suit = suit
            self.value = value

    def __str__(self):
        return self.value + self.suit

    def __repr__(self):
        return self.value + self.suit        

    def __eq__(self, that):        
        if that == None: return False
        if isinstance(that, str): that = Card(that)
        if not isinstance(that, Card): return False
        if self.suit != that.suit: return False
        return self.value == that.value

    def __hash__(self):
        return hash((self.suit, self.value))

    def getSuit(self, trump):
        if self.isLeftBower(trump): return trump
        return self.suit

    # compare two cards self and that
    # assume self card is played first
    # return 1 if self beats that, otherwise return -1
    def compare(self, that, trump):        
        if (self.isRightBower(trump)):
            return 1
        if (that.isRightBower(trump)):
            return -1
        if (self.isLeftBower(trump)):
            return 1
        if (that.isLeftBower(trump)):
            return -1
        
        if (self.suit == trump and that.suit != trump) :
            return 1
        if (self.suit != trump and that.suit == trump):
            return -1
        if (self.suit != that.suit):
            return 1

        selfIndex = Card.values.index(self.value)
        thatIndex = Card.values.index(that.value)
        
        if (selfIndex > thatIndex): return 1
        if (selfIndex < thatIndex): return -1

        return 0

    def isRightBower(self, trump):
        return self.value == "J" and self.suit == trump

    def isLeftBower(self, trump):                
        return self.value == "J" and self.suit == leftBowerSuit(trump)

    
def leftBowerSuit(suit):
    if suit == "♠":
        return "♣"
    if suit == "♣":
        return "♠" 
    if suit == "♥":
        return "♦"
    if suit == "♦":
        return "♥"