# __init__.py
# euchre/__init__.py

# Import classes and functions to expose them at the package level
from .Game import Game
from .Snapshot import Snapshot
from .Euchre import Euchre
from .EuchreError import EuchreError
from .MetaDeck import MetaDeck
from .PlayerManager import PlayerManager
from .TrickManager import TrickManager
from .Settings import Settings
import euchre.constants
import euchre.card
import euchre.player
import euchre.utility

# Define __all__ to specify what is exported when using 'from euchre import *'
__all__ = [
    "Euchre",
    "Game",
    "Snapshot",
    "EuchreError",
    "MetaDeck",
    "PlayerManager",
    "TrickManager",
    "Settings",
    "constants",
    "card",
    "player",
    "utility",
]
