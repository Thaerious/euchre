from .Normalized import Normalized
from .custom_json_serializer import custom_json_serializer
import json
from typing import Any, Dict

class Snapshot:
    def __init__(self, game, player_name):
        for_player = game.get_player(player_name)

        self.players = []
        for player in game.players:
            self.players.append({
                "name": player.name,
                "cards": len(player.cards),
                "tricks": player.tricks,
                "index": player.index,
                "played": ""
            })

        if len(game.tricks) > 0:
            trick = game.tricks[-1]
            i = game.lead
            
            for card in trick:
                self.players[i]["played"] = card
                i = (i + 1) % 4

        self.for_player = for_player.index
        self.active = game.current_player.index
        self.state = game.current_state
        self.up_card = game.up_card
        self.down_card = game.down_card        
        self.trump = game.trump
        self.tricks = game.tricks 
        self.maker = game.maker.index if game.maker != None else None
        self.dealer = game.dealer.index
        self.hand = for_player.cards
        self.order = game.order   
        self.hands_played = game.hands_played
        self.score = game.score
        self.last_action = game.last_action
        self.lead = game.lead
        self.last_player = game.last_player
        
        self.hash = game.hash
        # self.normalized = Normalized(game, for_player)
        self.state = game.current_state

        if game.dealer == for_player:
            self.discard = game.discard
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
            "up_card": self.up_card,
            "down_card": self.down_card,
            "trump": self.trump,
            "maker": self.maker,
            "dealer": self.dealer,
            "hand": self.hand,
            "order": self.order,
            "hands_played": self.hands_played,
            "score": self.score,
            "last_action": self.last_action,
            "last_player": self.last_player,
            "hash": self.hash,    
            "lead": self.lead      
            # "normalized": str(self.normalized),  # Assuming Normalized can be converted to a string
        }

    def to_json(self) -> str:
        """
        Converts the Snapshot object to a JSON string.
        """

        return json.dumps(self.to_dict(), indent=2, default=custom_json_serializer)

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