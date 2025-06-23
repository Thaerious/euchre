"""
Player.py

Defines the `Player` class for representing a Euchre player.

Each player tracks:
- name and seat index
- their team and partner
- cards in hand and played cards
- tricks won and whether they are playing alone

Includes methods for state reset, copying, and JSON serialization.
"""
from euchre.card import Hand
from euchre.utility.del_string import del_string

class Player:
    """Represents a single player in Euchre."""

    def __init__(self, name, index):
        """Initialize a player with a name and seat index."""
        self.name = name
        self.partner = None
        self.index = index
        self.team = None
        self.hand = Hand()
        self.played = []
        self.tricks = 0
        self.alone = False

    def __json__(self):
        """Return a JSON-serializable dictionary of player data."""
        return {
            "name": self.name,
            "tricks": self.tricks,
            "played": self.played,
            "hand": self.hand,
            "alone": self.alone,
            "index": self.index
        }

    def __str__(self):
        """Return a string summarizing the player's state."""
        sb = f"#{self.index} {self.name} [{self.hand}] {self.played} T{self.tricks}"
        if self.alone:
            sb += " Alone"
        return sb

    def clear(self):
        """Reset the player's hand, played cards, tricks won, and alone status."""
        self.hand = Hand()
        self.played = []
        self.tricks = 0
        self.alone = False

    def copy(self):
        """Create a shallow copy of the player, including their hand."""
        new_player = Player(self.name, self.index)
        for card in self.hand:
            new_player.hand.append(card)
        return new_player