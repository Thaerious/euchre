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
        this.active = euchre.current_player_index
        this.state = int(game.state.__name__[5:])
        this.upCard = euchre.upCard
        this.trump = euchre.trump
        this.tricks = euchre.tricks
        this.maker = euchre.maker
        this.dealer = euchre.dealer
        this.hand = forPlayer.cards
        this.order = euchre.order   
        this.hands_played =  euchre.hands_played
        this.score = euchre.score
        this.lastAction = game.lastAction
        this.lastPlayer = game.lastPlayer

        this.normalized = Normalized(euchre, forPlayer)

        if euchre.getDealer() == forPlayer:
            this.downCard = euchre.downCard
        else:
            this.downCard = None

        this.hash = game.hash
    
    def __str__(this):
        sb = ""

        for attr in dir(this):
            if attr.startswith("_"): continue
            attrValue = getattr(this, attr)
            if callable(attrValue) == True: continue
            sb = sb + f"{attr} : {str(attrValue)}\n"

        return sb
