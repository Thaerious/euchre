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
        sb = f"{self.name}[{self.hand}][{del_string(self.played)}] {self.tricks}"
        return sb
    
    def __repr__(self):     
        return str(self)


class Snapshot(Game):
    def __init__(self, game: Game, for_player: str):       
        self.__dict__ = copy.deepcopy(game.__dict__)
        self.players = []
        self.for_index = game.get_player(for_player).index

        # Replace players with Snap_Player versions
        self.players = [Snap_Player(player) for player in game.players]

        self.hand = copy.deepcopy(game.get_player(for_player).hand)

        # Hide discard if not for dealer
        if game.dealer and game.dealer.name != for_player:
            self.discard = None

    def normalize_cards(self):
        norm = copy.deepcopy(self)
        norm.hand = self.hand.normalize(norm)
        norm._trump = "♠"

        norm._tricks = []
        for trick in self.tricks:
            norm.tricks.append(trick.normalize())

        norm.up_card = None if self.up_card is None else self.up_card.normalize(self)
        norm.down_card = None if self.down_card is None else self.down_card.normalize(self)

        return norm

    # change player index references so that 'for_player' is index 0
    def normalize_order(self):
        norm = copy.deepcopy(self)
        norm.for_index = 0
        norm.lead_index = (self.lead_index - self.for_index) % 4
        norm.dealer_index = (self.dealer_index - self.for_index) % 4        
        norm.current_player_index = (self.current_player_index - self.for_index) % 4

        if self.last_player is not None:
            norm.last_player = (self.last_player - self.for_index) % 4

        if self.maker is not None:
            norm._maker = (self.maker.index - self.for_index) % 4

        new_order = []
        for i in self.order:
            new_order.append((i - self.for_index) % 4)
        norm.order = new_order

        for player in norm.players:
            player.index = (player.index - self.for_index) % 4

        return norm

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