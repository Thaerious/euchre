from .Normalized import Normalized

class Snapshot:
    def __init__(self, game, for_player):
        self.names = [player.name for player in game.euchre.players]
        self.tricks = [player.tricks for player in game.euchre.players]
        self.for_player = game.euchre.players.index(for_player)
        self.active = game.euchre.current_player_index
        self.state = game.current_state
        self.up_card = game.euchre.up_card
        self.trump = game.euchre.trump
        self.tricks = game.euchre.tricks
        self.maker = game.euchre.maker
        self.dealer = game.euchre.dealer
        self.hand = for_player.cards
        self.order = game.euchre.order   
        self.hands_played = game.euchre.hands_played
        self.score = game.euchre.score
        self.last_action = game.last_action
        self.last_player = game.last_player
        self.hash = game.hash
        self.normalized = Normalized(game.euchre, for_player)

        if game.euchre.dealer == for_player:
            self.down_card = game.euchre.down_card
        else:
            self.down_card = None      