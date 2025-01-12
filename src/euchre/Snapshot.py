from euchre.Normalized import Normalized
import copy

class Snapshot:
    def __init__(self, game, player):
        if game is None: raise ValueError("Game can not be none.")
        if player is None: raise ValueError("Player can not be none.")

        self.build(game, player)

    def build(self, game, for_player):
        euchre = game.euchre

        self.names = [player.name for player in euchre.players]
        self.tricks = [player.tricks for player in euchre.players]
        self.for_player = euchre.players.index(for_player)
        self.active = euchre.current_player_index
        self.state = game.current_state
        self.up_card = euchre.up_card
        self.trump = euchre.trump
        self.tricks = euchre.tricks
        self.maker = euchre.maker
        self.dealer = euchre.dealer
        self.hand = for_player.cards
        self.order = euchre.order   
        self.hands_played = euchre.hands_played
        self.score = euchre.score
        self.last_action = game.last_action
        self.last_player = game.last_player

        self.normalized = Normalized(euchre, for_player)

        if euchre.dealer == for_player:
            self.down_card = euchre.down_card
        else:
            self.down_card = None

        self.hash = game.hash
    
    def __str__(self):
        sb = ""

        for attr in dir(self):
            if attr.startswith("_"): continue
            attr_value = getattr(self, attr)
            if callable(attr_value): continue
            sb = sb + f"{attr} : {str(attr_value)}\n"

        return sb
