from euchre.Euchre import Euchre
from euchre.Game import Game, ActionException
from euchre.delString import delString
from euchre.Snapshot import Snapshot
from pprint import pprint
from euchre.bots.Bot import Bot
import random

stateLabels = {
    "state0" : "Game not started (start): ",
    "state1" : "Order up dealer (pass, order, alone): ",
    "state2" : "Pick up card (up, down): ",
    "state3" : "Make suit (pass, make, alone): ",
    "state4" : "Screw the dealer (make): ",
    "state5" : "Play a card (play): "
}

class GameLoop:
    def __init__(this):
        this.euchre = Euchre(["Adam", "T100", "Skynet", "Robocop"])
        this.bots = {
            "Adam" : Bot(),
            "T100" : Bot(),
            "Skynet" : Bot(),
            "Robocop" : Bot()
        }

        this.game = Game(this.euchre)
        this.history = []
        this.action = ""
        this.isRunning = True
        this.teams = [this.euchre.players[0].team, this.euchre.players[1].team]

    def playerString(this, player):
        return f"{str(player)} {player.tricks} [{delString(player.played)}]"

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
            return this.euchre.getCurrentPlayer().cards[(int)(input)]
        else:
            if   input[0] == "s": return "♠"
            elif input[0] == "c": return "♣"
            elif input[0] == "h": return "♥"
            elif input[0] == "d": return "♦"   

    def doAction(this, line):
        parsed = this.parseInput(line)
        print("------------------------------------------------------")    

        if parsed["action"] == "load":
            this.loadHistory()        
        elif parsed["action"] == "bot":
            snap = Snapshot(this.game, this.euchre.getCurrentPlayer())
            action = this.bots[this.euchre.getCurrentPlayer().name].decide(snap)
            print(f"Bot: {action}")
            this.history.append(action)
            split = action.split(" ")            
            if len(split) == 1: split.append(None)
            this.game.input(this.euchre.getCurrentPlayer(), split[0], split[1])
            print("------------------------------------------------------")                        
        elif parsed["action"] == "save":
            this.saveHistory()      
        elif parsed["action"] == "exit":
            this.isRunning = False
        elif parsed["action"] == "seed":
            random.seed((int)(parsed["data"]))
            this.history.append(line)
        elif parsed["action"] == "print":
            print("------------------------------------------------------")   
            print(str(this.euchre))
            print("------------------------------------------------------")               
        elif parsed["action"] == "snap":
            print("------------------------------------------------------")   
            print(str(Snapshot(this.game, this.euchre.getCurrentPlayer())))
            print("------------------------------------------------------")   
        else:
            try:
                this.game.input(this.euchre.getCurrentPlayer(), parsed["action"], this.convertData(parsed["data"]))
                this.history.append(line)
            except ActionException as ex:
                print("ActionException: " + str(ex))        

    def start(this):
        while this.isRunning:
            this.game.print()
            print("------------------------------------------------------")   
            if this.game.state.__name__ == "state7": this.printPlayable()
            line = input(stateLabels[this.game.state.__name__])
            this.doAction(line)

    def printPlayable(this):
        i = 0
        for card in this.euchre.getCurrentPlayer().cards:
            if this.game.euchre.trick.canPlay(card, this.euchre.getCurrentPlayer().cards, this.game.euchre.trump):
                print(f"{i}[{card}]", end=" ")
            i = i + 1

        print("")

gameLoop = GameLoop()
gameLoop.start()
