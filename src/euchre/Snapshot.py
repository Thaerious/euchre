from euchre.Normalized import Normalized
import copy

class Snapshot:
    def __init__(this, game, player):
        if game is None: raise ValueError("Game can not be none.")
        if player is None: raise ValueError("Player can not be none.")

        this.build(game, player)

    def build(this, game, forPlayer):
        euchre = game.euchre

        this.names = [player.name for player in euchre.players]
        this.tricks = [player.tricks for player in euchre.players]
        this.forPlayer = euchre.players.index(forPlayer)
        this.active = euchre.currentPlayer
        this.state = int(game.state.__name__[5:])
        this.upCard = euchre.upCard
        this.trump = euchre.trump

        if euchre.maker == None:
            this.maker = None
        else:
            this.maker = euchre.players.index(euchre.maker)

        this.dealer = euchre.dealer
        this.hand = forPlayer.cards
        this.trick = euchre.trick
        this.order = euchre.order   
        this.trickCount = euchre.trickCount
        this.handCount =  euchre.handCount
        this.score = [euchre.players[0].team.score, euchre.players[1].team.score]

        this.normalized = Normalized(euchre, forPlayer)

        if euchre.getDealer() == forPlayer:
            this.downCard = euchre.downCard
        else:
            this.downCard = None
    
    def __str__(this):
        sb = ""

        for attr in dir(this):
            if attr.startswith("_"): continue
            attrValue = getattr(this, attr)
            if callable(attrValue) == True: continue
            sb = sb + f"{attr} : {str(attrValue)}\n"

        return sb
