from euchre.Player import Player, PlayerList, Team
from euchre.Card import Card, Deck, Trick, Hand
from euchre.delString import delString
from euchre.rotate import rotate
import random

class Euchre:
    def __init__(this, names):
        random.shuffle(names)

        this.players = PlayerList(names)
        this.order = [0, 1, 2, 3]
        this.currentPlayer = this.order[0]
        this.dealer = this.order[3]

        this.teams = [this.players[0].team, this.players[1].team]
        this.deck = Deck()

        this.trick = Trick()
        this.upcard = None
        this.downcard = None
        this.trump = ""
        this.maker = None

    def nextHand(this):
        this.dealer = (this.dealer + 1) % 4
        this.currentPlayer = (this.dealer + 1) % 4

        i = this.currentPlayer
        while i <= this.dealer:
            this.order.append(i)
            i = i + 1

        this.deck = Deck().shuffle()
        this.trick = Trick()   
        this.dealCards()

    # advance to the next player in the order
    # circles back to first player
    # returns the matching player object
    def nextPlayer(this):
        currentOrderIndex = this.order.index(this.currentPlayer)
        nextOrderIndex = currentOrderIndex + 1
        if nextOrderIndex >= len(this.order): nextOrderIndex = 0
        this.currentPlayer = this.order[nextOrderIndex]
        return this.players[this.currentPlayer]        

    def isAtFirstPlayer(this):
        return this.getCurrentPlayer() == this.getFirstPlayer()

    def getCurrentPlayer(this):
        return this.players[this.currentPlayer]

    def getFirstPlayer(this):
        index = this.order[0]
        return this.players[index]

    def getDealer(this):
        index = this.order[-1]
        return this.players[index]      

    def activateDealer(this):
        this.currentPlayer = this.order[-1]

    def activateFirstPlayer(this):
        this.currentPlayer = this.order[0]             

    def dealCards(this):
        for i in range(0, 5):
            for player in this.players:
                card = this.deck.pop(0)
                player.cards.append(card)

        this.upcard = this.deck.pop(0)

    def orderUp(this):
        this.maker = this.getCurrentPlayer()
        this.trump = this.upcard.suit

    def goAlone(this):
        this.getCurrentPlayer().alone = True
        i = this.players.index(this.getCurrentPlayer().partner)
        this.order.remove(i)

    def makeSuit(this, player, suit = None):
        this.maker = player
        if suit != None: this.trump = suit     
        else: this.trump = this.upcard.suit

    def isTrickFinished(this):        
        return len(this.trick) == len(this.order)

    def canPlay(this, player, card):       
        if len(this.trick) == 0: return True
        leadSuit = this.trick[0].getSuit(this.trump)
        if card.getSuit(this.trump) == leadSuit: return True        

        for playerCard in player.cards:
            if playerCard.getSuit(this.trump) == leadSuit : return False

        return True

    def dealerSwapCard(this, card):
        this.getDealer().cards.remove(card)
        this.getDealer().cards.append(this.upcard)
        this.downcard = card

    def playCard(this, player, card):
        player.cards.remove(card)   
        player.played.append(card)
        this.trick.append(card)

    def nextTrick(this, player):
        i = this.players.index(player)
        while this.order[0] != i:
            rotate(this.order)

        this.currentPlayer = i
        this.trick = Trick()        

    def trickWinner(this):        
        bestPlayer = this.getFirstPlayer()
        bestCard = bestPlayer.played[-1]

        for i in this.order:
            player = this.players[i]       
            card = player.played[-1]
            compare = bestCard.compare(card, this.trump)

            if (compare < 0):
                 bestPlayer = player
                 bestCard = card

        return bestPlayer 

    def __str__(this):
        sb = ""

        for attr in dir(this):
            if attr.startswith("__"): continue
            attrValue = getattr(this, attr)
            if callable(attrValue) and attr.startswith("get"):
                sb = sb + f"{attr}() : {str(attrValue())}\n"
            elif callable(attrValue) == False:
                sb = sb + f"{attr} : {str(attrValue)}\n"

        for player in this.players:
            sb = sb + f"{str(player)}\n"

        return sb
        
