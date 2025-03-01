from .custom_json_serializer import custom_json_serializer
from typing import Any, Dict
from euchre.card.Hand import Hand
from .Game import Game
from .del_string import del_string
import copy

class Snap_Player:
    def __init__(self, player):
        self.__dict__.update(player.__dict__)
        self.hand = len(player.hand)

    def __json__(self):
        return {
            "name": self.name,
            "tricks": self.tricks,
            "played": self.played,
            "hand": self.hand,
            "alone": self.alone
        }

    def __str__(self):     
        sb = f"({self.name}, {self.hand} cards, [{del_string(self.played)}], T{self.tricks})"
        return sb
    
    def __repr__(self):     
        return str(self)


class Snapshot(Game):
    def __init__(self, game: Game, for_player: str):       
        # self.__dict__ = copy.deepcopy(game.__dict__)
        self.__dict__ = copy.copy(game.__dict__)
        self.players = []
        self.for_index = game.get_player(for_player).index

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