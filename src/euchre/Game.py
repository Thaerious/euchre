from euchre.Card import Card, Deck, Trick
from euchre.delString import delString
from euchre.Euchre import EuchreException
import random

class ActionException(EuchreException):
    def __init__(self, msg):
        super().__init__(msg)

class Game:
    def __init__(self, euchre):
        self.euchre = euchre
        self.state = self.state_0
        self.update_hash()
        self.last_action = [None, None, None, None]
        self.last_player = None

    def update_hash(self):
        self.hash = ''.join(random.choices('0123456789abcdef', k=8))

    def getState(self):
        return int(self.state.__name__[5:])

    def input(self, player, action, data = None):        
        if self.state != self.state_0 and player != self.euchre.getCurrentPlayer(): 
            raise ActionException(f"Incorrect Player: expected {self.euchre.getCurrentPlayer().name} found {player.name}")
        
        # if data is a string, convert it to a card
        if isinstance(data, str): 
            data = Card(data[-1], data[:-1]) 

        # activate the current state
        self.update_hash()
        self.last_action[self.euchre.current_player_index] = action
        self.last_player = self.euchre.current_player_index
        self.state(player, action, data)

    def state_0(self, action, data):
        self.allowed_actions(action, "start")         
        self.enter_state_1()

    def enter_state_1(self):
        self.euchre.shuffle_deck()
        self.euchre.deal_cards()          
        self.euchre.clear_tricks()
        self.state = self.state_1

    def state_1(self, action, data):         
        self.allowed_actions(action, "pass", "order", "alone")

        if action == "pass":
            if self.euchre.activate_next_player() == self.euchre.getFirstPlayer():
                self.state = self.state_3
        elif action == "order":
            self.euchre.make_trump()
            self.euchre.activate_dealer()
            self.state = self.state_2
        elif action == "alone":      
            self.euchre.make_trump()      
            self.euchre.go_alone()
            if self.euchre.getCurrentPlayer().partner != self.euchre.dealer:
                self.euchre.activate_dealer()
                self.state = self.state_2
            else:
                self.enter_state_5()

    def state_2(self, action, card):
        self.allowed_actions(action, "down", "up")

        if action == "up": self.euchre.dealer_swap_card(card)
        else: self.euchre.turn_down_card()

        self.euchre.activate_first_player()
        self.enter_state_5()

    def state_3(self, action, suit):
        self.allowed_actions(action, "pass", "make", "alone")

        if action == "pass":            
            if self.euchre.activate_next_player() == self.euchre.getDealer():     
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
        if not self.euchre.isTrickFinished(): return
        
        self.euchre.score_trick()

        if self.euchre.isHandFinished():
            self.euchre.score_hand()

            if self.euchre.is_game_over():
                self.state = self.state_0
            else:
                self.euchre.next_hand() # todo test? doc?
                self.enter_state_1()
        else:
            self.euchre.add_trick()

    # todo: is ref neccisary
    def allowed_actions(self, action, *allowed_actions):
        for allowed in allowed_actions:
            if action.lower() == allowed.lower(): return

        raise ActionException("Unhandled Action " + (str)(action))

    def print(self):        
        for player in self.euchre.players:
            prefix = ""

            if self.euchre.getMaker() == player: prefix = prefix + "M"
            if self.euchre.getDealer() == player: prefix = prefix + "D"
            if player.partner.alone == True: prefix = prefix + "X"
            if player.alone == True: prefix = prefix + "A"

            prefix = prefix.rjust(3, " ")

            if self.euchre.getCurrentPlayer() == player: prefix = prefix + ">"  
            else: prefix = prefix + " "  

            print(f"{prefix} {str(player)}")


        t1Score = self.euchre.players[0].team.score
        t2Score = self.euchre.players[2].team.score

        t1Text = f"Team1 [{self.euchre.players[0].name} {self.euchre.players[2].name}] {t1Score}"
        t2Text = f"Team2 [{self.euchre.players[1].name} {self.euchre.players[3].name}] {t2Score}" 

        print(t1Text)
        print(t2Text)

        print(self.state.__name__)    
        print("upCard: " + (str)(self.euchre.upCard))
        print(f"[{delString(self.euchre.trick)}] : ", end="")
        print(self.euchre.trump if self.euchre.trump is not None else "_")        