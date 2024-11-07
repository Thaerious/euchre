import random
from delString import delString

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

class Trick(CardList):
    # Can 'card' be played if 'this' is the current trick.
    def canPlay(this, card, hand, trump):
        if not isinstance(card, Card): raise TypeError(f"expected Card, found {type(card)}")
        if not isinstance(hand, CardList): raise TypeError(f"expected CardList, found {type(hand)}")
        if not isinstance(trump, str): raise TypeError(f"expected str, found {type(trump)}")

        # empty trick
        if len(this) == 0: return True

        # subject card suit matches leading card suit
        leadSuit = this[0].suit
        if card.getSuit(trump) == leadSuit: return True

        # if any other card in the hand matches suit
        for cardInHand in hand:
            if cardInHand == card: continue
            if cardInHand.getSuit(trump) == leadSuit: return False

        return True  

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
            # initialize from card string ie 10♥
            this.suit = suit[-1]
            this.value = suit[:-1]
        else:
            this.suit = suit
            this.value = value

    def __str__(this):
        return this.value + this.suit

    def __eq__(this, that):        
        if that == None: return False
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