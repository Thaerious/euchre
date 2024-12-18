from euchre.Player import Player, PlayerList
from euchre.Card import Card, Deck, Trick, Hand
from euchre.delString import delString
from euchre.rotate import rotate
import euchre.bots.tools as tools

class EuchreException(Exception):
    def __init__(this, msg):
        super().__init__(msg)

class Euchre:
    def __init__(this, names):
        this.players = PlayerList(names)
        this.order = [0, 1, 2, 3]
        this.currentPIndex = this.order[0]
        this.dealer = this.order[3]
        this.handCount = 0
        this.trickCount = 0

        this.deck = Deck()

        this.upCard = None
        this.downCard = None
        this.trump = None
        this.maker = None 
        this.score = [0, 0]   
        this.clearTricks()

    def hasTrick(this):
        return len(this.tricks) > 0

    def getTrick(this):
        if len(this.tricks) == 0: return None
        return this.tricks[-1]

    def clearTricks(this):
        this.tricks = []

    def addTrick(this):
        if this.trump is None: raise EuchreException(f"to add a trick, trump can not be None.  Must call #MakeTrump.")
        this.tricks.append(Trick(this.trump))

    # shuffle the deck, should be called after nextHand
    def shuffleDeck(this):
        this.deck = Deck().shuffle()

    # advance to the next hand
    # the order reset, the first player becomes the dealer
    # the deck is collected (not shuffled)
    # upCard, downCard, trump, maker, and trick are all cleared
    def nextHand(this):
        this.handCount = this.handCount + 1
        this.order = []

        for i in range(this.handCount, this.handCount + 4):
            this.order.append(i % 4)

        this.currentPIndex = this.order[0]
        this.dealer = this.order[3]

        this.deck = Deck()

        this.trickCount = 0
        this.upCard = None
        this.downCard = None
        this.trump = None
        this.maker = None

    # score the current hand
    # if the score is >= 10 for either team return True
    def scoreHand(this):
        makerTeam = tools.teamOf(this.maker)
        otherTeam = tools.otherTeam(makerTeam)
        tricks = [0, 0]
        
        for trick in this.tricks:
            team = trick.winner() % 2
            tricks[team] = tricks[team] + 1

        if tricks[makerTeam] == 5 and this.maker.alone:
            this.score[makerTeam] += 4
        elif tricks[makerTeam] == 5:
            this.score[makerTeam] += 2
        elif tricks[makerTeam] > 3:
            this.score[makerTeam] += 1
        else:
            this.score[otherTeam] += 2

    def isGameOver(this):
        if this.score[0] >= 10 or this.score[1] >= 10:
            return True
        else:
            return False

    # advance to the next player in the order
    # circles back to first player
    # returns the matching player object
    def activateNextPlayer(this):        
        currentOrderIndex = this.order.index(this.currentPIndex)
        nextOrderIndex = (currentOrderIndex + 1) % len(this.order)
        this.currentPIndex = this.order[nextOrderIndex]
        return this.getCurrentPlayer()       

    # deprecated
    # true if the current player is the first player
    def isAtFirstPlayer(this):
        return this.getCurrentPlayer() == this.getFirstPlayer()

    # retrieve the player object for the current player
    def getCurrentPlayer(this):
        return this.players[this.currentPIndex]

    def getMaker(this):
        return this.players[this.maker]

    # retrieve the player object for the first player
    def getFirstPlayer(this):
        index = this.order[0]
        return this.players[index]

    # retrieve the player object for the dealer
    def getDealer(this):
        return this.players[this.dealer]      

    # make the dealer the current player
    def activateDealer(this):
        this.currentPIndex = this.dealer

    # make the first player the current player
    def activateFirstPlayer(this):
        this.currentPIndex = this.order[0]             

    # deal cards out to players and upCard
    def dealCards(this):
        for i in range(0, 5):
            for player in this.players:
                card = this.deck.pop(0)
                player.cards.append(card)

        this.upCard = this.deck.pop(0)

    # removes the current player's partner from the order,
    # sets the current player's 'alone' flag
    def goAlone(this):
        this.getCurrentPlayer().alone = True
        i = this.players.index(this.getCurrentPlayer().partner)
        this.order.remove(i)

    # the current player declares trump (orders up or declares)
    # if suit is omitted the upCard suit is used
    def makeTrump(this, suit:str = None):
        this.maker = this.currentPIndex
        if suit != None: this.trump = suit     
        else: this.trump = this.upCard.suit

    # true if enough cards have been played to advance to the next trick
    def isTrickFinished(this):        
        return len(this.getTrick()) == len(this.order)

    def __checkFollowSuit(this, player, card):
        if tools.canPlay(this.trump, this.getTrick(), player.cards, card) == False:
            leadSuit = this.getTrick()[0].getSuit(this.trump)
            raise EuchreException(f"card '{card}' must follow suit '{leadSuit}'")

    # the dealer removes card from their hand (it becomes downCard)
    # the upCard is added to the dealers hand
    def dealerSwapCard(this, card):
        print(f"dealerSwapCard {card} {this.upCard}")
        this.getDealer().cards.remove(card)
        this.getDealer().cards.append(this.upCard)
        this.downCard = card

    # the current player plays the specified card
    # it is removed from their hand and switched to played
    # it is added to the trick
    def playCard(this, card, next = True):
        if this.trump is None: raise EuchreException(f"to play card, trump can not be None.  Must call #MakeTrump.")
        if isinstance(card, str): card = Card(card)

        player = this.getCurrentPlayer()

        if card not in player.cards: raise EuchreException(f"card '{card}' not in hand of '{player.name}'")
        this.__checkFollowSuit(player, card)

        player.cards.remove(card)   
        player.played.append(card)
        
        this.getTrick().append(this.currentPIndex, card)

        if next: this.activateNextPlayer()

    # determine the winner of the previous trick,
    # that player becomes the first player in the play order
    # increse the trick count of the trick winner
    # if the trick is not finished, throw an exception
    def nextTrick(this):
        if this.isTrickFinished() == False:
            return False

        player = this.__trickWinner()
        player.tricks = player.tricks + 1
        i = this.players.index(player)

        while this.order[0] != i:
            rotate(this.order)

        this.currentPIndex = i
        if len(this.tricks) < 5: this.addTrick()

        return True

    def isHandFinished(this):
        if len(this.tricks) < 5: return False
        if len(this.tricks[-1]) != len(this.order): return False
        return True

    def __trickWinner(this):
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
        
__all__ = ["Euchre", "EuchreException"]