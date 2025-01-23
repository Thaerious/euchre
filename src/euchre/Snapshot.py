from .Normalized import Normalized
import json
from typing import Any, Dict

class Snapshot:
    def __init__(self, game, player_name):
        for_player = game.euchre.get_player(player_name)

        self.players = []
        for player in game.euchre.players:
            self.players.append({
                "name": player.name,
                "cards": len(player.cards),
                "tricks": player.tricks
            })

        self.for_player = for_player.index
        self.active = game.euchre.current_player.index
        self.state = game.current_state
        self.up_card = game.euchre.up_card
        self.down_card = game.euchre.down_card        
        self.trump = game.euchre.trump
        self.tricks = game.euchre.tricks 
        self.maker = game.euchre.maker.index if game.euchre.maker != None else None
        self.dealer = game.euchre.dealer.index
        self.hand = for_player.cards
        self.order = game.euchre.order   
        self.hands_played = game.euchre.hands_played
        self.score = game.euchre.score
        self.last_action = game.last_action

        self.last_player = game.last_player.index if game.last_player is not None else None
        
        self.hash = game.hash
        # self.normalized = Normalized(game.euchre, for_player)
        self.state = game.current_state

        if game.euchre.dealer == for_player:
            self.discard = game.euchre.discard
        else:
            self.discard = None      

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Snapshot object to a dictionary suitable for JSON serialization.
        """
        return {
            "players": self.players,
            "tricks": self.tricks,
            "for_player": self.for_player,
            "active_player": self.active,
            "state": self.state,
            "up_card": str(self.up_card) if self.up_card else None,
            "trump": self.trump,
            "current_tricks": self.tricks,
            "maker": self.maker,
            "dealer": self.dealer,
            "hand": [str(card) for card in self.hand],
            "order": self.order,
            "hands_played": self.hands_played,
            "score": self.score,
            "last_action": self.last_action,
            "last_player": self.last_player,
            "hash": self.hash,
            "down_card": str(self.down_card) if self.down_card else None,
            # "normalized": str(self.normalized),  # Assuming Normalized can be converted to a string
        }

    def to_json(self) -> str:
        """
        Converts the Snapshot object to a JSON string.
        """
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the Snapshot object.
        """
        return (
            f"  Players: {self.players}\n"
            f"  Tricks: {self.tricks}\n"
            f"  For Player: {self.for_player}\n"
            f"  Active Player: {self.active}\n"
            f"  Game State: {self.state}\n"
            f"  Up Card: {self.up_card}\n"
            f"  Down Card: {self.down_card if self.down_card else 'None'}\n"            
            f"  Discard: {self.discard if self.down_card else 'None'}\n"
            f"  Trump: {self.trump}\n"
            f"  Current Tricks: {self.tricks}\n"
            f"  Maker: {self.maker}\n"
            f"  Dealer: {self.dealer}\n"
            f"  Hand: {[str(card) for card in self.hand]}\n"
            f"  Order: {self.order}\n"
            f"  Hands Played: {self.hands_played}\n"
            f"  Score: {self.score}\n"
            f"  Last Action: {self.last_action}\n"
            f"  Last Player: {self.last_player}\n"
            f"  State: {self.state}\n"
            f"  Hash: {self.hash}\n"
            # f"  Normalized: {self.normalized}\n"
        )            