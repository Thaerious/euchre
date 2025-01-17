from euchre.delString import delString

class Card:
    suits = ["♥", "♠", "♣", "♦"]
    values = ["9", "10", "J", "Q", "K", "A"]

    left_bower_suit = {
        "♠": "♣",
        "♣": "♠",
        "♥": "♦",
        "♦": "♥"
    }

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

    def get_suit(self, trump):
        if self.is_left_bower(trump): return trump
        return self.suit

    # compare two cards self and that
    # assume self card is played first
    # return 1 if self beats that, otherwise return -1
    def compare(self, that, trump):        
        if (self.is_right_bower(trump)):
            return 1
        if (that.is_right_bower(trump)):
            return -1
        if (self.is_left_bower(trump)):
            return 1
        if (that.is_left_bower(trump)):
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

    def is_right_bower(self, trump):
        return self.value == "J" and self.suit == trump

    def is_left_bower(self, trump):                
        return self.value == "J" and self.suit == Card.left_bower_suit[trump]
    
