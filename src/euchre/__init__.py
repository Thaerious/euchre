# __init__.py
# euchre/__init__.py

# Import classes and functions to expose them at the package level
from . import card    # ✅ import the card module itself
from . import player  # ✅ import the player module itself
from . import utility # ✅ import the utility module itself
from .Euchre import Euchre, EuchreError
from .Game import Game, ActionError
from .Snapshot import Snapshot

# Define __all__ to specify what is exported when using 'from euchre import *'
__all__ = [
    "Game",
    "Snapshot",
    "Euchre",
    "EuchreError",
    "ActionError",
    "card",
    "player",
    "utility"
]
