"""
Game.py
maintains the finite state machine for a euchre game
"""

# pylint ignore attribute and public method counts
# pylint: disable=R0902, R0904

import json
from collections.abc import Callable
from typing import Any
from euchre import Euchre, EuchreError
from euchre.card import Card, Trick
from .utility.custom_json_serializer import custom_json_serializer


class Game(Euchre):
    """
    Manages the overall flow and state of a Euchre game.

    Attributes:
        euchre (Euchre): Instance of the Euchre game logic.
        state (Callable[[str, Any], None]): Current state function for the game.
        hash (str): Unique identifier for the current state.
        last_action (Optional[str]): Last action performed in the game.
        last_player_index (Optional[Player]): Index of last player who performed an action.
    """

    def __init__(self, names: list[str], seed=None):
        """
        Initialize the Game object with player names.

        Args:
            names (list of str): List of player names.
        """
        super().__init__(names, seed)
        self._state: Callable[[str, Any], None] = self.state_0
        self.last_action: str | None = None
        self.last_data: str | None = None
        self._last_player_index: int | None = None
        self.do_shuffle = True
        self._hooks = {}
        self.hash = ""

    @property
    def last_player(self):
        """Retrieve the last player that performed an action"""
        return self.get_player(self._last_player_index)

    def register_hook(self, event: str, func):
        """Register a function to a hook event."""
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(func)

    def trigger_hook(self, event: str, *args, **kwargs):
        """Trigger all hooks associated with an event."""
        if event in self._hooks:
            for func in self._hooks[event]:
                func(*args, **kwargs)

    @property
    def state(self) -> int:
        """
        Get the current state as an integer based on the function name.

        Returns:
            int: Current state number.
        """
        return int(self._state.__name__[6:])

    def input(
        self,
        player: str | None,
        action: str,
        data: str | Card | None = None,
    ) -> None:
        """
        Process player input based on the current game state.

        Args:
            player (Optional[str]): Name of the player performing the action.
            action (str): Action to perform.
            data (Optional[Union[str, Card]], optional): Additional data for the action.

        Raises:
            ActionException: If the action or player is invalid.
        """
        self.trigger_hook("before_input", action=action, data=data)
        prev_state = self.state

        self.last_action = action

        if action in ["play", "make"]:
            self.last_data = data
        else:
            self.last_data = None

        if player is not None:
            self._last_player_index = self.get_player(player).index
        else:
            self._last_player_index = None

        if self.state == 0:
            self._state(action, data)
        elif self.state in (6, 7):
            self._state(action, data)
        elif self.state in (2, 5):
            # States 2 & 5 expect a card object
            if player != self.current_player.name:
                raise EuchreError(
                    f"Incorrect Player: expected '{self.current_player.name}' found '{player}'."
                )
            if isinstance(data, str):
                data = self.deck.get_card(data[-1], data[:-1])
            self._state(action, data)
        else:
            if player != self.current_player.name:
                raise EuchreError(
                    f"Incorrect Player: expected '{self.current_player.name}' found '{player}'."
                )
            self._state(action, data)

        self.trigger_hook(
            "after_input",
            prev_state=prev_state,
            player=player,
            action=action,
            data=data,
        )

    def state_0(self, action: str, __: Any) -> None:
        """
        Initial state where the game starts.

        Args:
            action (str): Expected action "start".
            __: Unused parameter.
        """
        self.allowed_actions(action, "start")
        self.enter_state_1()

    def enter_state_1(self) -> None:
        """
        Transition to state 1: Shuffle and deal cards.
        """
        if self.do_shuffle:
            self.shuffle_deck()

        self.deal_cards()
        self._state = self.state_1

    def state_1(self, action: str, __: Any) -> None:
        """
        State 1: Players decide to pass, order up, or go alone.

        Args:
            action (str): Action to perform ("pass", "order", "alone").
            __: Unused parameter.
        """
        self.allowed_actions(action, "pass", "order", "alone")

        if action == "pass":
            if self.activate_next_player() == self.first_player:
                self.enter_state_3()
        elif action == "order":
            self.make_trump(self.up_card.suit)
            self.enter_state_2()
        elif action == "alone":
            self.make_trump(self.up_card.suit)
            self.go_alone()
            self.enter_state_2()

    def enter_state_2(self) -> None:
        """
        Transition to state 2: Dealer's turn to decide.
        """
        self.activate_dealer()
        self._state = self.state_2

    def state_2(self, action: str, card: Card | None) -> None:
        """
        State 2: Dealer decides to pick up the card or pass.

        Args:
            action (str): Action to perform ("down", "up").
            card (Card): Card to swap if action is "up".
        """
        self.allowed_actions(action, "down", "up")

        if action == "up":
            self.dealer_swap_card(card)
        else:
            self.turn_down_card()

        self.activate_first_player()
        self.enter_state_5()

    def enter_state_3(self):
        """
        Transition to state 3: Dealer turns down the up-card,
        and players begin selecting a trump suit.
        """
        self.turn_down_card()
        self._state = self.state_3

    def state_3(self, action: str, suit: str | None) -> None:
        """
        State 3: Players decide to pass, make, or go alone for trump.

        Args:
            action (str): Action to perform ("pass", "make", "alone").
            suit (str): Trump suit if "make" or "alone".
        """
        self.allowed_actions(action, "pass", "make", "alone")

        if action == "pass":
            if self.activate_next_player() == self.dealer:
                self._state = self.state_4
        elif action in ["make", "alone"]:
            self.make_trump(suit)
            if action == "alone":
                self.go_alone()
            self.activate_first_player()
            self.enter_state_5()

    def state_4(self, action: str, suit: str | None) -> None:
        """
        State 4: Dealer decides to make trump or go alone.

        Args:
            action (str): Action to perform ("make", "alone").
            suit (str): Trump suit.
        """
        self.allowed_actions(action, "make", "alone")

        self.make_trump(suit)
        if action == "alone":
            self.go_alone()
        self.activate_first_player()
        self.enter_state_5()

    def enter_state_5(self) -> None:
        """
        Transition to state 5: Players play tricks.
        """
        self.add_trick()
        self.reset_lead_player()
        self._state = self.state_5

    def state_5(self, action: str, card: Card) -> None:
        """
        State 5: Players play cards and score tricks.

        Args:
            action (str): Expected action "play".
            card (Card): Card to play.
        """
        self.allowed_actions(action, "play")
        self.play_card(card)

        if not self.is_trick_finished:
            return
        self.enter_state_6()

    def enter_state_6(self) -> None:
        """
        Transition to state 6: Score the current trick and
        determine whether to continue playing or move to scoring the hand.
        """
        self.score_trick()
        self._state = self.state_6

    def state_6(self, action: str, __: Any) -> None:
        """
        State 6: Transition to the next trick.

        Args:
            action (str): Expected action "continue".
            __: Unused parameter.
        """
        self.allowed_actions(action, "continue")

        if not self.is_hand_finished:
            self.rotate_to_winner()
            self.enter_state_5()
            return

        self.score_hand()
        self._state = self.state_7

    def state_7(self, action: str, __: Any) -> None:
        """
        State 7: Transition to the next hand.

        Args:
            action (str): Expected action "continue".
            __: Unused parameter.
        """
        self.allowed_actions(action, "continue")

        if self.is_game_over():
            self._state = self.state_8
        else:
            self.next_hand()
            self.enter_state_1()

    def state_8(self, _: str, __: Any) -> None:
        """
        State 8: Game over, no transitions.
        """
        # pylint: disable=W0107
        pass

    def allowed_actions(self, action: str, *allowed_actions: str) -> None:
        """
        Validate if the given action is allowed in the current state.

        Args:
            action (str): Action to validate.
            allowed_actions (list of str): List of allowed actions.

        Raises:
            ActionException: If the action is not allowed.
        """

        for allowed in allowed_actions:
            if action.lower() == allowed.lower():
                return

        raise EuchreError("Unhandled Action " + str(action))

    def __str__(self) -> str:  # pragma: no cover
        """
        String representation of the Game object for debugging purposes.

        Returns:
            str: Debug information for the game.
        """
        sb = super().__str__()
        sb += f"last action: {self.last_action}\n"
        sb += f"last player: {self._last_player_index} -> {self.get_player(self._last_player_index)}\n"
        sb += f"state: {self.state}\n"

        return sb

    def __json__(self):
        return super().__json__() | {
            "hash": self.hash,
            "state": self.state,
            "last_player": self._last_player_index,
            "last_action": self.last_action,
        }

    def to_json(self, indent=2):
        """
        Serialize the Euchre game state to a JSON-formatted string.

        Args:
            indent (int, optional): Number of spaces to use for indentation in the output. Defaults to 2.

        Returns:
            str: A JSON-formatted string representation of the game state.
        """
        return json.dumps(self, indent=indent, default=custom_json_serializer)

    @staticmethod
    def from_json(json_object):
        """
        Reconstruct a Game instance from a JSON-serializable dictionary.

        Args:
            json_object (dict): JSON-compatible dictionary representing game state.

        Returns:
            Game: A restored Game object with state and players reconstructed.
        """
        # permit pylint access to protected member
        # pylint: disable=W0212
        player_names = [player["name"] for player in json_object["players"]]
        game = Game(player_names)
        game.order = [int(i) for i in json_object["order"]]
        game.trump = json_object["trump"]

        for p in json_object["players"]:
            player = game.get_player(p["name"])
            player.tricks = p["tricks"]
            player.alone = p["alone"]
            cards_from_json(game.deck, player.played, p["played"])
            cards_from_json(game.deck, player.hand, p["hand"])

        game.deck.clear()
        for c in json_object["deck"]:
            game.deck.append(Card(game.deck, c))

        game._tricks.append(Trick(game.trump, game.order))

        game.current_player_index = int_or_none(json_object["current_player"])
        game.dealer_index = int_or_none(json_object["dealer"])
        game.lead_index = int_or_none(json_object["lead"])
        game._maker_index = int_or_none(json_object["maker"])
        game.hand_count = int_or_none(json_object["hand_count"])
        game._up_card = card_or_none(game.deck, json_object["up_card"])
        game._down_card = card_or_none(game.deck, json_object["down_card"])
        game._discard = card_or_none(game.deck, json_object["discard"])
        game._last_player_index = json_object["last_player"]
        game.last_action = json_object["last_action"]
        game._state = getattr(game, f"state_{json_object['state']}")

        return game


def int_or_none(source):
    """
    Convert a value to int if not None.

    Args:
        source (Any): The source value.

    Returns:
        Optional[int]: Integer value or None.
    """
    if source is None:
        return None
    return int(source)


def card_or_none(deck, source):
    """
    Convert a dictionary or string to a Card if not None.

    Args:
        deck (Deck): Reference to the current Deck object.
        source (dict or str): JSON representation of a card.

    Returns:
        Optional[Card]: Card object or None.
    """
    if source is None:
        return None
    return Card(deck, source)


def cards_from_json(deck, target, source):
    """
    Convert a list of serialized cards into Card objects and append to target.

    Args:
        deck (Deck): Reference to the current Deck object.
        target (list): List to which Card objects are appended.
        source (list): List of card representations from JSON.
    """
    for c in source:
        target.append(Card(deck, c))
