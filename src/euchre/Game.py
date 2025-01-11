from euchre.Card import Card, Deck, Trick
from euchre.delString import delString
from euchre.Euchre import *
import random

class ActionException(EuchreException):
    def __init__(self, msg):
        super().__init__(msg)

class Game:
    def __init__(self, names):
        self.euchre = Euchre(names)
        self.state = self.state_0
        self.update_hash()
        self.last_action = None
        self.last_player = None

    def update_hash(self):
        self.hash = ''.join(random.choices('0123456789abcdef', k=8))

    @property
    def current_state(self):
        return int(self.state.__name__[6:])

    def input(self, player, action, data = None):        
        if self.current_state == 0 or self.current_state == 6:
            if player != None:
                raise ActionException(f"Incorrect Player: expected 'None' found '{player}'.")                
        elif player != self.euchre.current_player.name: 
            raise ActionException(f"Incorrect Player: expected '{self.euchre.current_player.name}' found '{player}'.")
        
        # if data is a string, convert it to a card
        if isinstance(data, str): 
            data = Card(data[-1], data[:-1]) 

        # activate the current state
        self.update_hash()
        self.last_action = action
        self.last_player = self.euchre.current_player
        self.state(action, data)

    def state_0(self, action, __):
        self.allowed_actions(action, "start")         
        self.enter_state_1()

    def enter_state_1(self):
        self.euchre.shuffle_deck()
        self.euchre.deal_cards()
        self.state = self.state_1

    def state_1(self, action, __):         
        self.allowed_actions(action, "pass", "order", "alone")

        if action == "pass":
            if self.euchre.activate_next_player() == self.euchre.first_player:
                self.state = self.state_3
        elif action == "order":
            self.euchre.make_trump()
            self.enter_state_2()
        elif action == "alone":      
            self.euchre.make_trump()      
            self.euchre.go_alone()            
            self.enter_state_5()

    def enter_state_2(self):
        self.euchre.activate_dealer()
        self.state = self.state_2

    def state_2(self, action, card):
        self.allowed_actions(action, "down", "up")

        if action == "up": self.euchre.dealer_swap_card(card)
        else: self.euchre.turn_down_card()

        self.euchre.activate_first_player()
        self.enter_state_5()

    def state_3(self, action, suit):
        self.allowed_actions(action, "pass", "make", "alone")

        if action == "pass":            
            if self.euchre.activate_next_player() == self.euchre.dealer:     
                self.state = self.state_4
        elif action == "make":
            self.euchre.make_trump(suit)
            self.euchre.activate_first_player()
            self.enter_state_5()            
        elif action == "alone":
            self.euchre.make_trump(suit)
            self.euchre.go_alone()
            self.euchre.activate_first_player()
            self.enter_state_5()

    def state_4(self, action, suit):
        self.allowed_actions(action, "make", "alone")

        self.euchre.make_trump(suit)
        if action == "alone": self.euchre.go_alone()
        self.euchre.activate_first_player()
        self.enter_state_5()

    def enter_state_5(self):
        self.euchre.add_trick()
        self.state = self.state_5

    def state_5(self, action, card):
        self.allowed_actions(action, "play")
        self.euchre.play_card(card)
        if not self.euchre.is_trick_finished: return
        
        self.euchre.score_trick()

        if self.euchre.is_hand_finished:
            is_alone = len(self.euchre.order) == 3
            tricks = list(map(lambda p: p.tricks, self.euchre.players))
            hand_score = score_hand(self.euchre.maker.index, tricks, is_alone)
            self.euchre.adjust_score(hand_score)

            if is_game_over(self.euchre.score):
                self.state = self.state_0
            else:
                self.state = self.state_6
        else:
            self.euchre.add_trick()

    def state_6(self, action, __):
        self.allowed_actions(action, "continue")
        self.euchre.next_hand()
        self.euchre.clear_tricks()
        self.enter_state_1()

    # todo: is ref neccisary
    def allowed_actions(self, action, *allowed_actions):
        for allowed in allowed_actions:
            if action.lower() == allowed.lower(): return

        raise ActionException("Unhandled Action " + (str)(action))

    def __str__(self) -> str:  # pragma: no cover
        """
        String representation of the Euchre object, containing debug info.
        """
        sb = str(self.euchre)
        sb = sb + f"last action: {self.last_action}" + "\n"
        sb = sb + f"last player: {self.last_player}" + "\n"
        sb = sb + f"state: {self.current_state}" + "\n"

        return sb