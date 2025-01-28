from euchre.card import *
from euchre.Euchre import *
from euchre.Player import Player
import random
from typing import *
from typeguard import typechecked

class ActionException(EuchreException):
    """
    Custom exception for handling invalid actions in the game.
    Inherits from the base EuchreException class.
    Used when an exception arrises from user (or server) input.
    """
    def __init__(self, msg: str):
        super().__init__(msg)

class Game(Euchre):
    """
    Manages the overall flow and state of a Euchre game.

    Attributes:
        euchre (Euchre): Instance of the Euchre game logic.
        state (Callable[[str, Any], None]): Current state function for the game.
        hash (str): Unique identifier for the current state.
        last_action (Optional[str]): Last action performed in the game.
        last_player (Optional[Player]): Last player who performed an action.
    """

    @typechecked
    def __init__(self, names: list[str]):
        """
        Initialize the Game object with player names.

        Args:
            names (list of str): List of player names.
        """
        super().__init__(names)
        self.state: Callable[[str, Any], None] = self.state_0
        self.update_hash()
        self.last_action: Optional[str] = None
        self.last_player: Optional[Player] = None
        self.debug_seed = -1 # set to -1 to prevent shuffling
        self._hooks = {}

    @typechecked
    def register_hook(self, event: str, func):
        """Register a function to a hook event."""
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(func)

    @typechecked
    def trigger_hook(self, event: str, *args, **kwargs):
        """Trigger all hooks associated with an event."""
        if event in self._hooks:
            for func in self._hooks[event]:
                func(*args, **kwargs)

    @typechecked
    def update_hash(self) -> None:
        """
        Updates the unique hash identifier for the game state.
        """
        self.hash = ''.join(random.choices('0123456789abcdef', k=8))

    @property
    @typechecked
    def current_state(self) -> int:
        """
        Get the current state as an integer based on the function name.

        Returns:
            int: Current state number.
        """
        return int(self.state.__name__[6:])

    @typechecked
    def input(self, player: Optional[str], action: str, data: Optional[Union[str, Card]] = None) -> None:
        """
        Process player input based on the current game state.

        Args:
            player (Optional[str]): Name of the player performing the action.
            action (str): Action to perform.
            data (Optional[Union[str, Card]], optional): Additional data for the action.

        Raises:
            ActionException: If the action or player is invalid.
        """
        self.trigger_hook("before_input", action = action, data = data)
        prev_state = self.current_state

        self.update_hash() 
        self.last_action = action

        if self.current_state == 0:
            self.state(action, data)
        elif self.current_state == 6 or self.current_state == 7:
            if player is not None:
                raise ActionException(f"Incorrect Player: expected 'None' found '{player}'.")
            self.state(action, data)
        elif self.current_state == 2 or self.current_state == 5:
            # States 2 & 5 expect a card object
            if player != self.current_player.name: raise ActionException(f"Incorrect Player: expected '{self.current_player.name}' found '{player}'.")
            if isinstance(data, str): data = self.deck.get_card(data[-1], data[:-1])
            self.last_player = self.current_player            
            self.state(action, data)
        else:
            if player != self.current_player.name: raise ActionException(f"Incorrect Player: expected '{self.current_player.name}' found '{player}'.")
            self.last_player = self.current_player            
            self.state(action, data)

        self.trigger_hook("after_input", prev_state = prev_state, action = action, data = data)            

    @typechecked
    def state_0(self, action: str, __: Any) -> None:
        """
        Initial state where the game starts.

        Args:
            action (str): Expected action "start".
            __: Unused parameter.
        """
        self.allowed_actions(action, "start")
        self.enter_state_1()

    @typechecked
    def enter_state_1(self) -> None:
        """
        Transition to state 1: Shuffle and deal cards.
        """
        self.shuffle_deck(self.debug_seed)
        self.deal_cards()
        self.state = self.state_1

    @typechecked
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
            self.enter_state_5()

    @typechecked
    def enter_state_2(self) -> None:
        """
        Transition to state 2: Dealer's turn to decide.
        """
        self.activate_dealer()
        self.state = self.state_2

    @typechecked
    def state_2(self, action: str, card: Optional[Card]) -> None:
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

    @typechecked
    def enter_state_3(self):
        self.turn_down_card()
        self.state = self.state_3

    @typechecked
    def state_3(self, action: str, suit: Optional[str]) -> None:
        """
        State 3: Players decide to pass, make, or go alone for trump.

        Args:
            action (str): Action to perform ("pass", "make", "alone").
            suit (str): Trump suit if "make" or "alone".
        """
        self.allowed_actions(action, "pass", "make", "alone")

        if action == "pass":
            if self.activate_next_player() == self.dealer:
                self.state = self.state_4
        elif action in ["make", "alone"]:
            self.make_trump(suit)
            if action == "alone":
                self.go_alone()
            self.activate_first_player()
            self.enter_state_5()

    @typechecked
    def state_4(self, action: str, suit: Optional[str]) -> None:
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

    @typechecked
    def enter_state_5(self) -> None:
        """
        Transition to state 5: Players play tricks.
        """
        self.add_trick()
        self.state = self.state_5

    @typechecked
    def state_5(self, action: str, card: Card) -> None:
        """
        State 5: Players play cards and score tricks.

        Args:
            action (str): Expected action "play".
            card (Card): Card to play.
        """
        self.allowed_actions(action, "play")
        self.play_card(card)

        if not self.is_trick_finished: return
        self.enter_state_6()

    @typechecked
    def enter_state_6(self) -> None:
        self.score_trick()
        self.state = self.state_6

    @typechecked
    def state_6(self, action: str, __: Any) -> None:
        """
        State 6: Transition to the next trick.

        Args:
            action (str): Expected action "continue".
            __: Unused parameter.
        """        
        self.allowed_actions(action, "continue") 

        if not self.is_hand_finished:
            self.enter_state_5()
            return

        self.score_hand()
        if is_game_over(self.score):
            self.state = self.state_0
        else:
            self.state = self.state_7


    @typechecked
    def state_7(self, action: str, __: Any) -> None:
        """
        State 7: Transition to the next hand.

        Args:
            action (str): Expected action "continue".
            __: Unused parameter.
        """
        self.allowed_actions(action, "continue")        
        self.next_hand()
        self.enter_state_1()

    @typechecked
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

        raise ActionException("Unhandled Action " + str(action))

    @typechecked
    def __str__(self) -> str:  # pragma: no cover
        """
        String representation of the Game object for debugging purposes.

        Returns:
            str: Debug information for the game.
        """
        sb = super().__str__()
        sb += f"last action: {self.last_action}\n"
        sb += f"last player: {self.last_player}\n"
        sb += f"state: {self.current_state}\n"

        return sb
