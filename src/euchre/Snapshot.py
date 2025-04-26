# Snapshot.py
import copy
import hashlib
import json

from .utility.custom_json_serializer import custom_json_serializer
from .utility.del_string import del_string
from .Game import Game


class SnapPlayer:
    """A lightweight copy of a Player object for use in a game snapshot."""

    def __init__(self, player):
        """Initialize a SnapPlayer by copying fields from a Player."""
        self.__dict__.update(player.__dict__)
        self.hand_size = len(player.hand)

    def __json__(self):
        """Return a JSON-serializable dictionary representing the SnapPlayer."""
        return {
            "name": self.name,
            "tricks": self.tricks,
            "played": self.played,
            "hand_size": self.hand_size,
            "alone": self.alone,
            "index": self.index,
        }

    def __str__(self):
        """Return a string representation of the SnapPlayer."""
        return f"({self.name}, {self.hand_size} cards, [{del_string(self.played)}], T{self.tricks})"

    def __repr__(self):
        """Return the same as __str__ for SnapPlayer."""
        return str(self)


class Snapshot(Game):
    """A read-only copy of a Game object customized for a specific player's perspective."""

    def __init__(self, game: Game, for_player: str):
        """
        Initialize a Snapshot of a game, hiding sensitive information not visible to the given player.

        Args:
            game (Game): The current game object to snapshot.
            for_player (str): The name of the player this snapshot is created for.
        """
        self.__dict__ = copy.copy(game.__dict__)
        self.players = []
        self.for_index = game.get_player(for_player).index

        # Replace players with SnapPlayer versions
        self.players = [SnapPlayer(player) for player in game.players]

        # Copy hand for the player the snapshot is created for
        self.hand = copy.copy(game.get_player(for_player).hand)

        # Hide discard pile unless this player is the dealer
        if game.dealer and game.dealer.name != for_player:
            self.discard = None

    def __str__(self) -> str:
        """
        Return a human-readable string of the Snapshot for debugging.

        Returns:
            str: Debug information about the Snapshot.
        """
        sb = super().__str__()
        sb += f"for player: {self.for_index} -> {self.players[self.for_index]}\n"
        sb += f"hand: {self.hand}\n"
        return sb

    def hashable_json(self):
        """
        Create a dictionary of the snapshot suitable for deterministic JSON hashing.

        Returns:
            dict: Hashable JSON-ready data representing the snapshot.
        """
        return {
            "for_player": self.for_index,
            "players": [p.__json__() for p in self.players],
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
        }

    def id_hash(self):
        """
        Generate a unique SHA-256 hash of the snapshot data.

        Returns:
            str: A hexadecimal string representing the hash of the snapshot.
        """
        data = self.hashable_json()
        json_str = json.dumps(data, sort_keys=True, default=custom_json_serializer)
        return hashlib.sha256(json_str.encode("utf-8")).hexdigest()

    def __json__(self):
        """
        Return a JSON-serializable dictionary of the snapshot including a hash and type.

        Returns:
            dict: JSON-ready dictionary representing the snapshot.
        """
        data = self.hashable_json()
        data["type"] = Snapshot.__name__
        data["hash"] = self.id_hash()
        return data

    def __repr__(self):
        """
        Return a short debug string showing the snapshot hash and type.

        Returns:
            str: Debug string with partial hash and class name.
        """
        return f"{self.id_hash()[:8]}:{type(self).__name__}"
