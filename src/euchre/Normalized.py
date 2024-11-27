from euchre.Card import Card

# Create a normalized deck where spades is trump
# The player in question is player 1
#
# 0: Unknown
# 1: Player's Card
# 2: Upcard
# 3: Downcard
# 4: Played Previous Trick
# 5: Played Current Trick

class Normalized:
    def __init__(this, euchre, player):
        this.euchre = euchre
        this.player = player
        this.buildNames()

        this.deck = {}

        # unknown cards set to 0
        for card in euchre.deck:
            this.deck[str(card)] = 0

        # player card set to 1
        # other player cards set to 0
        for player in euchre.players:
            if this.names.index(player.name) == 0:
                for card in player.cards: this.deck[str(card)] = 1
            else:
                for card in player.cards: this.deck[str(card)] = 0
                
        # played cards set to 10 + player-index
            for card in player.cards:
                this.deck[str(card)] = 10

        # upcard set to 2
        if euchre.upcard != None:
            this.deck[str(euchre.upcard)] = 2

        # downcard set to 3
        if euchre.downcard != None:
            this.deck[str(euchre.upcard)] = 3

        # trick cards set to 4
        for card in euchre.trick:
            this.deck[str(card)] = 4

    def buildNames(this):
        players = this.euchre.players.copy()
        players.rotate(this.player)
        this.names = []

        for player in players:
            this.names.append(player.name)        

    suits = ["♠", "♣", "♥", "♦"]
    values = ["9", "10", "J", "Q", "K", "A"]

    def __str__(this):
        sb = "\t"

        for suit in Card.suits:
            sb = sb + (f"{suit}\t");

        sb = sb + "\n"

        for value in Card.values:
            sb = sb + value
            for suit in Card.suits:
                i = this.deck[f"{value}{suit}"]
                sb = sb + (f"\t{i}")
            sb = sb + "\n"

        return sb
