# euchre/__init__.py

# Import classes and functions to expose them at the package level
from . import card  # ✅ import the card module itself
from .Euchre import Euchre, EuchreError
from .Game import ActionError, Game
from .Player import Player, Team
from .Snapshot import Snapshot

# Define __all__ to specify what is exported when using 'from euchre import *'
__all__ = [
    "Player",
    "Game",
    "Snapshot",
    "Euchre",
    "Team",
    "EuchreError",
    "ActionError",
    "card"
]
