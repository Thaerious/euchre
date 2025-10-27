"""
HasTrump.py

HasTrump mixin module.

Provides a reusable base class for any object that needs to store and access a trump suit.
"""

from typing import Literal

TrumpSuit = Literal["♠", "♥", "♣", "♦"]

class HasTrump:
    """
    A mixin class that provides a `trump` property for classes needing trump suit management.
    """

    def __init__(self):
        """
        Initialize with no trump suit selected.
        """
        self._trump = None

    @property
    def trump(self) -> TrumpSuit | None:
        """
        Get the current trump suit.

        Returns:
            str | None: The trump suit symbol ("♠", "♥", "♣", "♦"), or None if unset.
        """
        return self._trump

    @trump.setter
    def trump(self, trump: TrumpSuit | None):
        """
        Set the current trump suit.

        Args:
            trump (str | None): The trump suit symbol, or None to clear.
        """
        if trump is not None and trump not in ("♠", "♥", "♣", "♦"):
            raise ValueError(f"Invalid trump suit: {trump}")

        self._trump = trump
