import copy

class Snapshot:
    def __init__(this, game, player):
        if game is None: raise ValueError("Game can not be none.")
        if player is None: raise ValueError("Player can not be none.")

        this.player = player
        this.players = this.__orderNames(game, player) 
        this.run(game)

    # return an ordered list of names started with 'self'
    # this ensures self is #0, partner is #2, opponents are #1, #3
    def __orderNames(this, game, player):
        players = game.euchre.players.copy()
        players.rotate(player)
        names = []

        for player in players:
            names.append(player.name)

        return names

    # return the saved index of the player
    # if player is none, returns none
    def playerIndex(this, player):
        if player == None: return None
        return this.players.index(player.name)   

    def run(this, game):
        euchre = game.euchre

        primitive_types = (int, float, str, bool, type(None), bytes)
        snap = {}

        this.state = int(game.state.__name__[5:])
        this.upcard = euchre.upcard
        this.trump = euchre.trump
        this.maker = this.playerIndex(euchre.maker)
        this.dealer = this.playerIndex(euchre.dealer())
        this.cards = this.player.cards
        this.trick = euchre.trick

        if game.activePlayer != None:
            this.activePlayer = this.playerIndex(game.activePlayer)
        else:
            this.activePlayer = -1

        if this.player == euchre.dealer():
            this.downcard = str(euchre.downcard)
        else:
            if euchre.downcard == None: this.downcard = None
            else: this.downcard = "hidden"

        this.playing = []
        for player in euchre.playing: 
            this.playing.append(this.playerIndex(player))

        return snap

    def __str__(this):
        return(
            f"players: {this.players}\n"
            f"state: {this.state}\n"
            f"up-card: {this.upcard}\n"
            f"trump: {this.trump}\n"
            f"maker: {this.maker}\n"
            f"dealer: {this.dealer}\n"
            f"cards: {this.cards}\n"
            f"trick: {this.trick}\n"
        )
