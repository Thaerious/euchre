from euchre.Card import Card, Deck, Trick
from euchre.delString import delString
from euchre.Euchre import EuchreException

class ActionException(EuchreException):
    def __init__(this, msg):
        super().__init__(msg)

class Game:
    def __init__(this, euchre):
        this.euchre = euchre
        this.state = this.state0
        this.activePlayer = None

    def currentState(this):
        return int(this.state.__name__[5:])

    def input(this, player, action, data = None):        
        if this.state != this.state0 and player != this.euchre.getCurrentPlayer(): 
            raise ActionException(f"Incorrect Player: expected {this.euchre.getCurrentPlayer().name} found {player.name}")
        
        # if data is a string, convert it to a card
        if isinstance(data, str): 
            data = Card(data[-1], data[:-1]) 

        # activate the current state
        this.state(player, action, data)

    def state0(this, player, action, data):
        this.allowedActions(action, "start")
        this.euchre.shuffleDeck()
        this.euchre.dealCards()        
        this.state = this.state1

    def state1(this, player, action, data):         
        this.allowedActions(action, "pass", "order", "alone")

        if action == "pass":
            if this.euchre.activateNextPlayer() == this.euchre.getFirstPlayer():
                this.state = this.state3
        elif action == "order":
            this.euchre.makeTrump()
            this.euchre.activateDealer()
            this.state = this.state2
        elif action == "alone":      
            this.euchre.makeTrump()      
            this.euchre.goAlone()
            if this.euchre.getCurrentPlayer().partner != this.euchre.dealer:
                this.euchre.activateDealer()
                this.state = this.state2
            else:
                this.state = this.state5

    def state2(this, player, action, card):
        this.allowedActions(action, "down", "up")
        if action == "up": this.euchre.dealerSwapCard(card)
        this.euchre.activateFirstPlayer()
        this.state = this.state5

    def state3(this, player, action, suit):
        this.allowedActions(action, "pass", "make", "alone")

        if action == "pass":            
            if this.euchre.activateNextPlayer() == this.euchre.getDealer():     
                this.state = this.state4
        elif action == "make":
            this.euchre.makeTrump(suit)
            this.state = this.state5
            this.euchre.activateFirstPlayer()
        elif action == "alone":
            this.euchre.makeTrump(suit)
            this.euchre.goAlone()
            this.euchre.activateFirstPlayer()
            this.state = this.state5

    def state4(this, player, action, suit):
        this.allowedActions(action, "make", "alone")
        this.euchre.makeTrump(suit)
        this.euchre.activateFirstPlayer()
        this.state = this.state5

    def state5(this, player, action, card):
        this.allowedActions(action, "play")
        this.euchre.playCard(card)

        if this.euchre.isTrickFinished() == False: return

        this.euchre.nextTrick()

        if this.euchre.handFinished():
            this.euchre.scoreHand()
            if this.isGameOver():
                this.state = this.state0
            else:
                this.euchre.nextHand()
                this.euchre.shuffle
                this.euchre.deal      

    def allowedActions(this, action, *allowedActions):
        for allowed in allowedActions:
            if action == allowed: return

        raise ActionException("Unhandled Action " + (str)(action))

    def print(this):        
        for player in this.euchre.players:
            prefix = ""

            if this.euchre.getMaker() == player: prefix = prefix + "M"
            if this.euchre.getDealer() == player: prefix = prefix + "D"
            if player.partner.alone == True: prefix = prefix + "X"
            if player.alone == True: prefix = prefix + "A"

            prefix = prefix.rjust(3, " ")

            if this.euchre.getCurrentPlayer() == player: prefix = prefix + ">"  
            else: prefix = prefix + " "  

            print(f"{prefix} {str(player)}")


        t1Score = this.euchre.players[0].team.score
        t2Score = this.euchre.players[2].team.score

        t1Text = f"Team1 [{this.euchre.players[0].name} {this.euchre.players[2].name}] {t1Score}"
        t2Text = f"Team2 [{this.euchre.players[1].name} {this.euchre.players[3].name}] {t2Score}" 

        print(t1Text)
        print(t2Text)

        print(this.state.__name__)    
        print("upCard: " + (str)(this.euchre.upCard))
        print(f"[{delString(this.euchre.trick)}] : ", end="")
        print(this.euchre.trump if this.euchre.trump is not None else "_")        