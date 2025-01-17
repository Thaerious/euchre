from euchre.card.Card import Card

# 0: Unknown
# 1: Player's card
# 2: up_card
# 3: down_card (if dealer)
# 4: Played previous trick
# 5: Played current trick

class Normalized:
    def __init__(self, euchre, player):
        self.deck = {}

        # all cards default to 0
        for suit in Card.suits:
            for value in Card.values:
                card = Card(suit, value)
                self.deck[str(card)] = 0

        # player card set to 1
        for p in euchre.players:
            if p == player:
                for card in player.cards:
                    self.deck[str(card)] = 1

            # played cards set to 10 + player-index
            for card in p.played:
                self.deck[str(card)] = 10 + euchre.players.index(p)

        # up_card set to 2
        if euchre.up_card is not None:
            self.deck[str(euchre.up_card)] = 2

        # down_card set to 3 if the dealer is the player
        # otherwise set to 0 (unknown)
        if euchre.down_card is not None:
            if euchre.dealer == player:
                self.deck[str(euchre.down_card)] = 3

        # trick cards set to 4
        if len(euchre.tricks) > 0:
            for i, card in enumerate(euchre.current_trick):
                self.deck[str(card)] = 20 + i   

    def __str__(self):
        sb = "\n\t"

        for suit in Card.suits:
            sb = sb + (f"{suit}\t")

        sb = sb + "\n"

        for value in Card.values:
            sb = sb + value
            for suit in Card.suits:
                key = f"{value}{suit}"
                if key in self.deck:
                    v = self.deck[key]
                    sb = sb + (f"\t{v}")
                else:
                    sb = sb + (f"\t?")
            sb = sb + "\n"

        return sb
