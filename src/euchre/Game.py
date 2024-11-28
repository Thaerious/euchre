from euchre.Card import Card, Deck, Trick
from euchre.delString import delString

class ActionException(Exception):
    def __init__(this, msg):
        super().__init__(msg)

class Game:
    def __init__(this, euchre):
        this.euchre = euchre
        this.state = this.state0
        this.activePlayer = None

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
        this.enterState1a()

    def enterState1a(this):
        this.euchre.nextHand()
        this.enterState1()  

    def enterState1(this):
        this.state = this.state1

    def state1(this, player, action, data):         
        this.allowedActions(action, "pass", "order", "alone")

        if action == "pass": 
            this.euchre.nextPlayer()            
            if this.euchre.isAtFirstPlayer(): this.enterState3() # void condition
        elif action == "order":
            this.euchre.orderUp()
            this.enterState2()
        elif action == "alone":      
            this.euchre.orderUp()      
            this.euchre.goAlone()
            if this.getCurrentPlayer().partner != this.euchre.dealer:
                this.enterState2()
            else:
                this.enterState5()
        
    def enterState2(this):
        this.euchre.activateDealer()
        this.state = this.state2

    def state2(this, player, action, card):
        this.allowedActions(action, "down", "up")
        if action == "up": this.euchre.dealerSwapCard(card)
        this.enterState5()

    def enterState3(this):
        this.state = this.State3

    def state3(this, player, action, suit):
        this.allowedActions(action, "pass", "make", "alone")

        if action == "pass":            
            this.euchre.nextPlayer()
            # void condition                
            if this.euchre.isAtFirstPlayer(): this.enterState4()
        elif action == "make":
            this.euchre.makeSuit(player, suit)
            this.enterState5()
        elif action == "alone":
            this.euchre.makeSuit(player, suit)
            this.euchre.goAlone(player)
            this.enterState5()

    def enterState4(this):
        this.state = this.State4

    def state4(this, player, action, suit):
        this.allowedActions(action, "make")
        this.euchre.makeSuit(player, suit)
        this.enterState5a()

    def enterState5(this):
        if this.state == this.state5:
            this.euchre.nextPlayer()
        else:
            this.euchre.activateFirstPlayer()
            this.state = this.state5

    def state5(this, player, action, card):
        this.allowedActions(action, "play")

        if this.euchre.trick.canPlay(card, player.cards, this.euchre.trump) == False:
            raise ActionException("Must play lead suit if possible.") 

        this.euchre.playCard(player, card)

        if this.euchre.isTrickFinished() == False:
            this.enterState5()
            return

        winner = this.euchre.trickWinner()
        winner.tricks += 1    

        this.euchre.nextTrick(winner)

        if this.handFinished(): 
            this.scoreHand()
        else: 
            this.enterState5()

    def scoreHand(this):
        team = this.euchre.maker.team

        if team.tricks() == 5 and maker.alone():
            team.score += 4
        elif team.tricks() == 5:
            team.score += 2
        elif team.tricks() > 3:
            team.score += 1
        else:
            team.score += 2

        if team.score >= 10| team.otherTeam.score >= 10:
            this.state = None
        else:
            this.enterState1a()           
        
    def handFinished(this):
        return len(this.euchre.getCurrentPlayer().cards) == 0

    def allowedActions(this, action, *allowedActions):
        for allowed in allowedActions:
            if action == allowed: return

        raise ActionException("Unhandled Action " + (str)(action))

    def print(this):        
        for player in this.euchre.players:
            if player.alone: print("A", end="")
            else: player.alone: print(" ", end="")

            if (this.euchre.getCurrentPlayer() == player):                
                print(f"> {str(player)}")
            else:
                print(f"  {str(player)}")

        t1Text = f"Team1 [{this.euchre.teams[0].player1.name} {this.euchre.teams[0].player2.name}]"
        t2Text = f"Team2 [{this.euchre.teams[1].player1.name} {this.euchre.teams[1].player2.name}]" 

        if this.euchre.maker == None:
            print (f"{t1Text}: {this.euchre.teams[0].score}")
            print (f"{t2Text}: {this.euchre.teams[1].score}")
        elif this.euchre.maker.team == this.euchre.teams[0]:
            print (f"{t1Text}: {this.euchre.teams[0].score} made by {this.euchre.maker.name}")
            print (f"{t2Text}: {this.euchre.teams[1].score}")
        else:
            print (f"{t1Text}: {this.euchre.teams[0].score}")
            print (f"{t2Text}: {this.euchre.teams[1].score} made by {this.euchre.maker.name}")


        print(this.state.__name__)    
        print("upcard: " + (str)(this.euchre.upcard))
        print("[" + delString(this.euchre.trick) + "] : " + this.euchre.trump)        