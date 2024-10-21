
class snapshot:

    def __init__(this, game, player):
        this.game = game
        this.player = player
        this.players = this.orderNames(game, player) 

    # return an ordered list of names started with 'self'
    # this ensures self is 0, partner is 2, opponents are 1, 3
    def orderNames(this, game, player):
        players = game.euchre.players.copy()
        players.rotate(player)
        names = []
        for player in players:
            names.append(player.name)

        return names

    def index(this, player):
        return this.players.index(player.name)   

    def run(this):
        euchre = this.game.euchre

        primitive_types = (int, float, str, bool, type(None), bytes)
        snap = {}

        snap["state"] = this.game.state.__name__[5:]
        snap["current_player"] = this.index(this.player)
        snap["upcard"] = str(euchre.upcard)
        snap["trump"] = euchre.trump
        snap["maker"] = this.index(euchre.maker)
        snap["dealer"] = this.index(euchre.dealer())
        snap["cards"] = cardsToList(this.player.cards)
        snap["trick"] = cardsToList(euchre.trick)

        if this.game.activePlayer != None:
            snap["activePlayer"] = this.index(this.game.activePlayer)
        else:
            snap["activePlayer"] = -1

        if this.player == euchre.dealer():
            snap["downcard"] = str(euchre.downcard)
        else:
            if euchre.downcard == None: snap["downcard"] = None
            else: snap["downcard"] = "hidden"

        snap["playing"] = []
        for player in euchre.playing: 
            snap["playing"].append(this.index(player))

        snap["players"] = {}
        for player in euchre.players:
            i = this.index(player)
            snap["players"][i] = snapPlayer(player)

        return snap

def snapPlayer(player):
    snap = {}
    snap["name"] = player.name
    snap["played"] = cardsToList(player.played)
    snap["alone"] = player.alone
    snap["tricks"] = player.tricks
    return snap

def cardsToList(cards):
    cardList = []
    for card in cards:
        cardList.append(str(card))
    return cardList