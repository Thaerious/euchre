class ActionException(Exception):
    def __init__(this, msg):
        super().__init__(msg)

class Game:
    def __init__(this, euchre):
        this.euchre = euchre
        this.state = this.state0
        this.activePlayer = None

    def input(this, player, action, data = None):            
        if this.activePlayer != None and player != this.activePlayer: 
            raise ActionException(f"Incorrect Player: expected {this.activePlayer.name} found {player.name}")
        
        this.state(player, action, data)

    def state0(this, player, action, data):
        if action != "start": raise ActionException("Unhandled Action " + (str)(action))
        this.enterState1a()

    def enterState1a(this):
        this.euchre.resetDeck()
        this.euchre.trick = []
        this.euchre.pastTricks = []
        this.euchre.shuffle()
        this.euchre.players.rotate()
        this.euchre.copyPlayersToPlaying()
        this.euchre.dealCards()      
        this.enterState1()  

    def enterState1(this):    
        if this.state == this.state1:
            this.nextPlayer()
        else:
            this.activePlayer = this.euchre.playing[0]
            this.state = this.state1

    def state1(this, player, action, data):         
        this.allowedActions(action, "pass", "order")

        if action == "pass": 
            if this.activePlayer == this.euchre.dealer(): 
                this.nextPlayer()
                this.enterState4()
            else: 
                this.enterState1()
        elif action == "order":
            this.euchre.makeSuit(this.activePlayer)
            this.enterState2()

    def enterState2(this):
        this.state = this.state2

    def state2(this, player, action, _):
        this.allowedActions(action, "helper", "alone")

        if action == "helper":
            this.enterState3()
        elif this.activePlayer.partner != this.euchre.dealer:
            this.euchre.goAlone(this.activePlayer)
            this.enterState3()
        else:
            this.euchre.goAlone(this.activePlayer)
            this.enterstate7a()
        
    def enterState3(this):
        print(this.euchre.dealer())
        print(this.euchre.players)
        this.activePlayer = this.euchre.dealer()
        this.state = this.state3

    def state3(this, player, action, card):
        this.allowedActions(action, "down", "up")
        if action == "up": this.euchre.swapCard(card)
        this.activePlayer = this.euchre.playing[0]
        this.enterstate7a()

    def enterState4(this):
        if this.state == this.state4:
            this.nextPlayer()
            if this.activePlayer == this.euchre.dealer(): this.state = this.state5
        else:
            this.state = this.state4

    def state4(this, player, action, suit):
        this.allowedActions(action, "pass", "make")

        if action == "pass":
            this.enterState4()
        elif action == "make":
            this.euchre.makeSuit(player, suit)
            this.enterstate6()

    def enterstate5(this):
        this.state = this.state5

    def state5(this, player, action, suit):
        this.allowedActions(action, "make")

        if action != "make": raise ActionException("Unhandled Action " + (str)(action))
        this.euchre.makeSuit(player, suit)
        this.enterstate6()

    def enterstate6(this):
        this.state = this.state6

    def state6(this, player, action, _):
        this.allowedActions(action, "alone", "helper")

        if action == "alone":
            this.euchre.goAlone(this.activePlayer)
        elif action != "helper": raise ActionException("Unhandled Action " + (str)(action))             

        this.enterstate7a()

    def enterstate7a(this):
        this.state = None
        this.enterState7()

    def enterstate7b(this):
        this.state = None
        this.euchre.playing.rotate(this.euchre.trickWinner())
        this.euchre.trick = []
        this.enterState7()

    def enterState7(this):
        if this.state == this.state7:
            this.nextPlayer()
        else:            
            this.activePlayer = this.euchre.playing[0]
            this.state = this.state7

    def state7(this, player, action, card):
        this.allowedActions(action, "play")

        if this.euchre.canPlay(player, card) == False:
            raise ActionException("Must play lead suit if possible.") 

        this.euchre.playCard(player, card)

        if this.trickFinished() == False:
            this.enterState7()
            return

        this.euchre.recordTrick()
        this.euchre.trickWinner().tricks += 1    

        if this.handFinished(): 
            this.scoreHand()
        else: 
            this.enterstate7b()

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

    def trickFinished(this):
        return len(this.euchre.trick) == len(this.euchre.playing)
        
    def handFinished(this):
        return len(this.activePlayer.cards) == 0

    def nextPlayer(this):
        this.activePlayer = this.euchre.playing.nextPlayer(this.activePlayer)

    def allowedActions(this, action, *allowedActions):
        for allowed in allowedActions:
            if action == allowed: return

        raise ActionException("Unhandled Action " + (str)(action))