"""
trick_manager.py

Manages the trick-related logic for a game of Euchre.

This module provides the TrickManager class, which handles creating,
accessing, and scoring tricks in a hand. It centralizes all operations 
related to trick progression, validation, and winner rotation.

Intended to be used as a component of the main Euchre game logic.
"""

from euchre.card import Trick, playable
from euchre.utility import rotate_to
from euchre.Euchre import EuchreError  # or define your own local error

class TrickManager:
    """
    Manages the trick flow in a Euchre hand, including play order, trick state, and winner logic.
    """

    def __init__(self, order, trump):
        """
        Initialize with reference to the game instance (for players, order, trump, etc.).

        Args:
            game (Euchre): The Euchre game object using this manager.
        """
        if trump is None:
            raise EuchreError("Trump must be declared before starting a trick.")

        self.order = order
        self.trump = trump
        self._tricks = []

    def __len__(self):
        return len(self._tricks)

    def add_trick(self):
        """
        Start a new trick.

        Raises:
            EuchreError: If trump has not been declared or previous trick isn't finished.
        """
        if self.has_trick and not self.is_trick_finished:
            raise EuchreError("Previous trick is still in progress.")
        
        self._tricks.append(Trick(self.game.trump, self.game.order))

    def play_card(self, card):
        """
        Add a card to the current trick.

        Args:
            card (Card | str): The card to play.

        Raises:
            EuchreError: For illegal play, such as wrong suit or missing trump.
        """
        if self.is_trick_finished:
            raise EuchreError("Trick is already complete.")

        player = self.game.current_player
        if isinstance(card, str):
            card = self.game.deck.get_card(card)

        if card not in player.hand:
            raise EuchreError(f"{card} not in {player.name}'s hand.")
        if card not in playable(self.current_trick, player.hand):
            lead = self._tricks[-1].lead_suit
            raise EuchreError(f"{card} must follow lead suit {lead}.")

        player.hand.remove(card)
        player.played.append(card)
        self._tricks[-1].append(card)
        self.game.activate_next_player()

    def score_trick(self):
        """
        Score the latest completed trick.

        Raises:
            EuchreError: If the trick is not yet complete.
        """
        if not self.is_trick_finished:
            raise EuchreError("Trick not yet complete.")
        
        winner_index = self.current_trick.winner
        self.game.players[winner_index].tricks += 1

    def rotate_to_winner(self):
        """
        Rotate player order so that the winner of the current trick goes first.
        """
        winner_index = self.current_trick.winner
        self.game.rotate_to_player(winner_index)

    def clear_tricks(self):
        """
        Clear all trick history (typically between hands).
        """
        self._tricks.clear()

    @property
    def current_trick(self):
        """
        Return the current trick in play.

        Returns:
            Trick | None: The active trick or None.
        """
        return self._tricks[-1] if self._tricks else None

    @property
    def tricks(self):
        """
        Return a copy of the list of completed/active tricks.

        Returns:
            List[Trick]: The tricks played so far.
        """
        return self._tricks.copy()

    @property
    def has_trick(self):
        """
        Check whether any trick has been started.

        Returns:
            bool: True if at least one trick exists.
        """
        return bool(self._tricks)

    @property
    def is_trick_finished(self):
        """
        Check whether the current trick is complete.

        Returns:
            bool: True if the current trick has all required plays.
        """
        return len(self._tricks[-1]) == len(self.game.order) if self._tricks else False
