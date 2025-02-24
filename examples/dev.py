from euchre import *

# ["♠", "♥", "♣", "♦"]

deck = Deck()

def build(trump, lead):
    result = {}
    ranks = Card.ranks
    ranks.reverse()
    suits = Card.suits

    v = 24

    # do trumps
    if trump is not None:
        suits.remove(trump)
        result[Card(deck, trump, "J")] = v
        result[Card(deck, Card.left_bower_suit[trump], "J")] = v - 1
        v = v - 2

        for rank in ranks:
            card = Card(deck, trump, rank)
            if not card in result: 
                result[card] = v
                v -= 1

    # do leads
    if lead is not None and lead != trump:
        suits.remove(lead)

        for rank in ranks:
            card = Card(deck, lead, rank)
            if not card in result: 
                result[card] = v
                v -= 1

    # do remainders
    for rank in ranks:
        for suit in suits:
            card = Card(deck, suit, rank)
            if not card in result: 
                result[card] = v
        v -= 1    

    return result

s = Card.suits
s.append(None)

for trump in s:
    for lead in s:
        b = build(trump, lead)

        t = f"'{trump}'" if trump is not None else None
        l = f"'{lead}'" if lead is not None else None

        print(f"compare_cards[{t}][{l}] = {{", end="")
        for key in b.keys():
            print(f"'{key}': {b[key]}, ", end="")
        print("}\n")

        
