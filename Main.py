from Euchre import Euchre
from Game import Game, ActionException
from delString import delString
from snapshot import snapshot
from pprint import pprint
import random

stateLabels = {
    "state0" : "Game not started (start): ",
    "state1" : "Order up dealer (pass, order): ",
    "state2" : "Go Alone (alone, helper): ",
    "state3" : "Pick up card (up, down): ",
    "state4" : "Make suit (pass, make): ",
    "state5" : "Screw the dealer (make): ",
    "state6" : "Go Alone (alone, helper): ",
    "state7" : "Play a card (play): "
}

class GameLoop:    
    def __init__(this):
        this.euchre = Euchre(["Adam", "Eve", "Cain", "Able"])
        this.game = Game(this.euchre)
        this.history = []
        this.action = ""
        this.isRunning = True
        this.teams = [this.euchre.players[0].team, this.euchre.players[1].team]

    def playerString(this, player):
        return f"{str(player)} {player.tricks} {this.pastTricks(player)}"

    def printGame(this):        
        for player in this.euchre.players:
            if (this.game.activePlayer == player): print(f"> {this.playerString(player)}")
            else:  print(f"  {this.playerString(player)}")

        t1Text = f"Team1 [{this.teams[0].player1.name} {this.teams[0].player2.name}]"
        t2Text = f"Team2 [{this.teams[1].player1.name} {this.teams[1].player2.name}]" 

        if this.euchre.maker == None:
            print (f"{t1Text}: {this.teams[0].score}")
            print (f"{t2Text}: {this.teams[1].score}")
        elif this.euchre.maker.team == this.teams[0]:
            print (f"{t1Text}: {this.teams[0].score} made by {this.euchre.maker.name}")
            print (f"{t2Text}: {this.teams[1].score}")
        else:
            print (f"{t1Text}: {this.teams[0].score}")
            print (f"{t2Text}: {this.teams[1].score} made by {this.euchre.maker.name}")


        print(this.game.state.__name__)    
        print("upcard: " + (str)(this.game.euchre.upcard))
        print("[" + delString(this.game.euchre.trick) + "] : " + this.game.euchre.trump)

    def pastTricks(this, player):
        rvalue = []
        for rvalue in this.euchre.pastTricks:
            prev.append(rvalue[player.name])

        return "[" + delString(prev) + "]"

    def loadHistory(this):
        with open('history.txt', 'r') as file:
            for line in file:
                if line == None: continue
                line = line.strip()
                if line == "": continue
                this.doAction(line)  

    def saveHistory(this):
        with open('history.txt', 'w') as file:
            for line in this.history:
                if line == None: continue
                line = line.strip()
                if line == "": continue
                file.write(line + "\n")

    def parseInput(this, line):
        words = line.split()

        return {
            "action" : words[0] if len(words) > 0 else None,
            "data" : words[1] if len(words) > 1 else None
        }

    def convertData(this, input):
        if input == None:
            return None
        if input.isdigit():
            return this.game.activePlayer.cards[(int)(input)]
        else:
            if   input[0] == "s": return "♠"
            elif input[0] == "c": return "♣"
            elif input[0] == "h": return "♥"
            elif input[0] == "d": return "♦"   

    def doAction(this, line):
        parsed = this.parseInput(line)

        if parsed["action"] == "load":
            this.loadHistory()        
        elif parsed["action"] == "save":
            this.saveHistory()      
        elif parsed["action"] == "exit":
            this.isRunning = False
        elif parsed["action"] == "seed":
            random.seed((int)(parsed["data"]))
            this.history.append(line)
        elif parsed["action"] == "snap":
            print("---------------------------")
            pprint(snapshot(this.game, this.game.activePlayer))
            print("---------------------------")
        else:
            try:
                this.game.input(this.game.activePlayer, parsed["action"], this.convertData(parsed["data"]))
                this.history.append(line)
            except ActionException as ex:
                print("ActionException: " + str(ex))        

    def start(this):
        while this.isRunning:
            this.printGame()
            print("---------------------------")
            line = input(stateLabels[this.game.state.__name__])
            this.doAction(line)

gameLoop = GameLoop()
gameLoop.start()
