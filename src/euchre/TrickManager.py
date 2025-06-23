from typing import Any, Optional
from euchre.card import Trick, playable
from euchre.utility import rotate_to
from euchre.EuchreError import EuchreError
import euchre.constants as const
from euchre import Euchre
from euchre.card.Card import Card


class TrickManager:
    """
    Manages the trick flow in a Euchre hand, including play order, trick state, and winner logic.
    """

    def __init__(self, game: Euchre) -> None:
        self._tricks: list[Trick] = []
        self.game: Euchre = game

    def __str__(self) -> str:
        sb = "tricks:\n"
        for i, trick in enumerate(self._tricks):
            sb += f"  {i}: {trick}"
            if trick != self._tricks[-1]:
                sb += "\n"
        return sb

    def __json__(self) -> list[Trick]:
        return self._tricks

    def __len__(self) -> int:
        return len(self._tricks)

    def reset(self) -> None:
        self._tricks = []

    def add_trick(self, trump: str, order: list[int]) -> None:
        if self.has_trick and not self.is_trick_finished:
            raise EuchreError("Previous trick is still in progress.")
        self._tricks.append(Trick(trump, order))

    def play_card(self, card: Card | str) -> None:
        if self.is_trick_finished:
            raise EuchreError("Trick is already complete.")

        player = self.game.players.current
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
        self.game.players.activate_next_player()

    def trick_winner(self) -> int:
        if not self.is_trick_finished:
            raise EuchreError("Trick not yet complete.")       
        return self.current_trick.winner

    def rotate_to_winner(self) -> None:
        winner_index = self.current_trick.winner
        self.game.players.order
        self.game.players.rotate_to_player(winner_index)

    def clear_tricks(self) -> None:
        self._tricks.clear()

    @property
    def current_trick(self) -> Optional[Trick]:
        return self._tricks[-1] if self._tricks else None

    @property
    def tricks(self) -> list[Trick]:
        return self._tricks.copy()

    @property
    def has_trick(self) -> bool:
        return bool(self._tricks)

    @property
    def is_trick_finished(self) -> bool:
        if not self._tricks:
            return False
        trick = self._tricks[-1]
        return len(trick) == len(trick.order)

    def is_hand_finished(self) -> bool:
        if len(self._tricks) < const.NUM_TRICKS_PER_HAND:
            return False
        return self.is_trick_finished()
