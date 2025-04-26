# PlayerList.py
from .Player import Player

class PlayerList(list):
    """Represents a list of four Euchre players with automatic partnerships."""

    def __init__(self, names=[]):
        """Initialize the player list, assigning partners based on seating."""
        if len(names) != 4:
            return

        for i, name in enumerate(names):
            self.append(Player(name, i))

        self[0].partner = self[2]
        self[1].partner = self[3]
        self[2].partner = self[0]
        self[3].partner = self[1]

    def get_player(self, name):
        """Return the player object matching the given name, or None if not found."""
        for player in self:
            if player.name == name:
                return player
        return None

    def copy(self):
        """Return a shallow copy of the player list."""
        copied_list = PlayerList()
        for player in self:
            copied_list.append(player)
        return copied_list

    def clear(self):
        """Clear all players' hands, played cards, tricks won, and alone status."""
        for player in self:
            player.clear()

    def rotate(self, player=None):
        """Rotate players so that the given player (if specified) is first."""
        self.append(self.pop(0))
        if player is None:
            return

        while self[0] != player:
            self.append(self.pop(0))

    def activate_next_player(self, after_this):
        """Return the player after the given player, or None if at the end."""
        return_next = False
        for player in self:
            if return_next:
                return player
            if player == after_this:
                return_next = True
        return None

    def __str__(self):
        """Return a comma-separated string of all player names."""
        names = []
        for player in self:
            names.append(player.name)
        return f"[{del_string(names)}]"