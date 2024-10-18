class Card:
    suits = ["♠", "♣", "♥", "♦"]
    values = ["9", "10", "J", "Q", "K", "A"]

    def __init__(this, suit, value):
        this.suit = suit
        this.value = value

    def __str__(this):
        return this.value + this.suit

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
        
        if (thisIndex > thatIndex):
            return 1

        return -1

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