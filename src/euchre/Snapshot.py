from .custom_json_serializer import custom_json_serializer
from .Game import Game
from .del_string import del_string
import copy
import json

class Snap_Player:
    def __init__(self, player):
        self.__dict__.update(player.__dict__)
        self.hand_size = len(player.hand)

    def __json__(self):
        return {
            "name": self.name,
            "tricks": self.tricks,
            "played": self.played,
            "hand_size": self.hand_size,
            "alone": self.alone,
            "index": self.index
        }

    def __str__(self):     
        sb = f"({self.name}, {self.hand_size} cards, [{del_string(self.played)}], T{self.tricks})"
        return sb
    
    def __repr__(self):     
        return str(self)


class Snapshot(Game):
    next_serial_id = 0

    def __init__(self, game: Game, for_player: str):       
        self.__dict__ = copy.copy(game.__dict__)
        self.players = []
        self.for_index = game.get_player(for_player).index
        self.serial_id = Snapshot.next_serial_id
        Snapshot.next_serial_id += 1

        # Replace players with Snap_Player versions
        self.players = [Snap_Player(player) for player in game.players]

        self.hand = copy.copy(game.get_player(for_player).hand)

        # Hide discard if not for dealer
        if game.dealer and game.dealer.name != for_player:
            self.discard = None
  
    def __str__(self) -> str:  # pragma: no cover
        """
        String representation of the Snapshot object for debugging purposes.

        Returns:
            str: Debug information for the Snapshot.
        """
        sb = super().__str__()
        sb += f"for player: {self.for_index} -> {self.players[self.for_index]}\n"
        sb += f"hand: {self.hand}\n"

        return sb  
    
    def __json__(self):
        return {
            "type": Snapshot.__name__,
            "for_player": self.for_index,
            "players": self.players,
            "tricks": self.tricks,
            "trump": self.trump,
            "order": self.order, 
            "current_player": self.current_player_index,
            "dealer": self.dealer_index,
            "lead": self.lead_index,
            "maker": self.maker_index,
            "hand_count": self.hand_count,
            "up_card": self.up_card,
            "down_card": self.down_card,
            "hand": self.hand,
            "last_player": self.last_player_index,
            "last_action": self.last_action,
            "last_data": self.last_data,
            "state": self.current_state,
            "score": [self.teams[0].score, self.teams[1].score],
            "serial_id": self.serial_id
        } 
