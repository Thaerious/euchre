from euchre.Card import Card

# 0: Unknown
# 1: Player's card
# 2: upCard
# 3: downCard (if dealer)
# 4: Played previous trick
# 5: Played current trick

class Normalized:
    def __init__(this, euchre, player):
        this.deck = {}

        # all cards default to 0
        for suit in Card.suits:
            for value in Card.values:
                card = Card(suit, value)
                this.deck[str(card)] = 0

        # player card set to 1
        for p in euchre.players:
            if p == player:
                for card in player.cards: this.deck[str(card)] = 1
                
            # played cards set to 10 + player-index
            for card in p.played:
                this.deck[str(card)] = 10 + euchre.players.index(p)

        # upCard set to 2
        if euchre.upCard != None:
            this.deck[str(euchre.upCard)] = 2

        # downCard set to 3 if the dealer is the player
        # otherwise set to 0 (unknown)
        if euchre.downCard != None:
            if euchre.getDealer() == player:
                this.deck[str(euchre.downCard)] = 3

        # trick cards set to 4
        if euchre.hasTrick():
            for i, card in enumerate(euchre.tricks[-1]):
                this.deck[str(card)] = 20 + i   

    def __str__(this):
        sb = "\n\t"

        for suit in Card.suits:
            sb = sb + (f"{suit}\t");

        sb = sb + "\n"

        for value in Card.values:
            sb = sb + value
            for suit in Card.suits:
                key = f"{value}{suit}"
                if key in this.deck:
                    v = this.deck[key]
                    sb = sb + (f"\t{v}")
                else:
                    sb = sb + (f"\t?")
            sb = sb + "\n"

        return sb
