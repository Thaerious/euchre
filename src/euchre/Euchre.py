"""
Euchre.py
Main module for euchre state
"""

# pylint ignore attribute and public method counts
# pylint: disable=R0902, R0904

from .PlayerManager import PlayerManager
from .card.Deck import Deck

NUM_PLAYERS = 4
NUM_CARDS_PER_PLAYER = 5
NUM_TRICKS_PER_HAND = 5
REQUIRED_TRICKS_TO_WIN = 3

class Euchre:
    """
    The core class representing a single game of Euchre.
    """

    def __init__(self, names: list[str], seed=None) -> None:
        self.deck = Deck(seed)
        self.players = PlayerManager(names, self.deck)
        
