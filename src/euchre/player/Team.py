"""
Team.py

Defines the `Team` class for grouping Euchre players into a team.

Tracks:
- players belonging to the team
- cumulative tricks won
- current team score
- whether any player is going alone

Provides utility accessors for game logic and display.
"""
from euchre.utility.del_string import del_string


class Team:
    """Represents a Euchre team consisting of multiple players."""

    def __init__(self, players):
        """Initialize the team with a list of players."""
        self._players = players
        self.score = 0

    def __json__(self):
        return {
            "players": [p.index for p in self._players],
            "score": self.score
        }

    def __str__(self):
        """Return a comma-separated string of player names."""
        return del_string([p.name for p in self._players])

    def __repr__(self):
        """Return a comma-separated string of player names for debug purposes."""
        return del_string([p.name for p in self._players])

    @property
    def has_alone(self):
        """Return True if any player on the team is playing alone."""
        return any(player.alone for player in self._players)

    @property
    def tricks(self):
        """Return the total number of tricks won by all players on the team."""
        tricks = 0
        for player in self._players:
            tricks += player.tricks
        return tricks

    @property
    def players(self):
        """Return a copy of the list of players."""
        return self._players.copy()
