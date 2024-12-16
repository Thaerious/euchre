import random
from euchre.delString import delString

class CardList(list):
    def __init__(this, stringList = []):
        for string in stringList:
            this.append(Card(string))

    def randomItem(this):
        if len(this) == 0: return None
        index = random.randint(0, len(this)) - 1
        return this[index]     

    def __str__(this):
        return delString(this)

class Hand(CardList):
    # Given 'trick' and 'trump' return the cards in 'this' that can be played.
    def playableCards(this, trick, trump):
        cards = CardList()
        for card in this:
            if trick.canPlay(card, this, trump):
                cards.append(card)
                
        return cards   

# A list of cards starting with the lead player
class Trick(list):
    def __init__(this, trump):
        list.__init__(this)
        this.trump = trump

    # retrieve the pIndex of the lead player
    def getLead(this):
        return this[0][0]

    # retrieve a card by index
    def getCard(this, index):
        return this[index][1]

    # retrieve a card based on the player index that played it
    def getCardByPlayer(this, pIndex):
        for (p, card) in this:  
            if p == pIndex: return card

        return None

    def append(this, pIndex, card):
        list.append(this, (pIndex,card))

    # return the winning card
    def bestCard(this):
        if len(this) < 1: return None
        bestCard = this.getCard(0)
        
        for (pIndex, card) in this:               
            if (bestCard.compare(card, this.trump) < 0):
                 bestCard = card

        return bestCard 
                  
    # return the player index of the winning player
    def winner(this):
        if len(this) < 1: return None
        bestCard = this.bestCard()        

        for (pIndex, card) in this:  
            if card == bestCard: return pIndex
        

    # Can 'card' be played if 'this' is the current trick.
    def canPlay(this, card, hand):
        if not isinstance(card, Card): raise TypeError(f"expected Card, found {type(card)}")
        if not isinstance(hand, CardList): raise TypeError(f"expected CardList, found {type(hand)}")
        if not isinstance(this.trump, str): raise TypeError(f"expected str, found {type(this.trump)}")

        # empty trick
        if len(this) == 0: return True

        # subject card suit matches leading card suit
        leadSuit = this[0].suit
        if card.getSuit(this.trump) == leadSuit: return True

        # if any other card in the hand matches suit
        for (pIndex, cardInHand) in this:
            if cardInHand == card: continue
            if cardInHand.getSuit(this.trump) == leadSuit: return False

        return True  

    def __str__(this):
        return f"([{delString(this)}] : ({this.bestCard()}, {this.trump}, {this.winner()}) )"

    def __repr__(this):
        return str(this)


class Deck(CardList):
    def __init__(this):
        for suit in Card.suits:
            for value in Card.values:
                this.append(Card(suit, value))

    def shuffle(this):
        random.shuffle(this)
        return this

class Card:
    suits = ["♠", "♣", "♥", "♦"]
    values = ["9", "10", "J", "Q", "K", "A"]

    def __init__(this, suit, value = None):
        if value == None:
            # initialize from card string ie "10♥"
            this.suit = suit[-1]
            this.value = suit[:-1]
        else:
            this.suit = suit
            this.value = value

    def __str__(this):
        return this.value + this.suit

    def __repr__(this):
        return this.value + this.suit        

    def __eq__(this, that):        
        if that == None: return False
        if isinstance(that, str): that = Card(that)
        if this.suit != that.suit: return False
        return this.value == that.value

    def getSuit(this, trump):
        if this.isLeftBower(trump): return trump
        return this.suit

    # compare two cards this and that
    # assume this card is played first
    # return 1 if this beats that, otherwise return -1
    def compare(this, that, trump):        
        if (this.isRightBower(trump)):
            return 1
        if (that.isRightBower(trump)):
            return -1
        if (this.isLeftBower(trump)):
            return 1
        if (that.isLeftBower(trump)):
            return -1
        
        if (this.suit == trump and that.suit != trump) :
            return 1
        if (this.suit != trump and that.suit == trump):
            return -1
        if (this.suit != that.suit):
            return 1

        thisIndex = Card.values.index(this.value)
        thatIndex = Card.values.index(that.value)
        
        if (thisIndex > thatIndex): return 1
        if (thisIndex < thatIndex): return -1

        return 0

    def isRightBower(this, trump):
        return this.value == "J" and this.suit == trump

    def isLeftBower(this, trump):                
        return this.value == "J" and this.suit == leftBowerSuit(trump)

    
def leftBowerSuit(suit):
    if suit == "♠":
        return "♣"
    if suit == "♣":
        return "♠" 
    if suit == "♥":
        return "♦"
    if suit == "♦":
        return "♥"