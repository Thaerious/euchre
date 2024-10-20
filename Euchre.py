from Player import Player, PlayerList, Team
from Card import Card
import random

class Euchre:
    def __init__(this, names):
        random.shuffle(names)
        this.players = PlayerList(names) # the order for the hand
        this.playing = PlayerList() # the order for the trick
        this.pastTricks = []

        this.teams = [this.players[0].team, this.players[1].team]

        this.upcard = None
        this.trump = ""
        this.maker = None
        this.trick = []
        
    def canPlay(this, player, card):
        if len(this.trick) == 0: return True
        leadSuit = this.trick[0].getSuit(this.trump)
        if card.getSuit(this.trump) == leadSuit: return True        

        for playerCard in player.cards:
            if playerCard.getSuit(this.trump) == leadSuit : return False

        return True

    def resetDeck(this):
        this.deck = []
        for suit in Card.suits:
            for value in Card.values:
                this.deck.append(Card(suit, value))

    def shuffle(this):
        random.shuffle(this.deck)

    def dealer(this):
        return this.players[3]

    def copyPlayersToPlaying(this):       
        this.players.clear() 
        this.playing = this.players.copy()

    def dealCards(this):
        for i in range(0, 5):
            for player in this.playing:
                card = this.deck.pop(0)
                player.cards.append(card)

        this.upcard = this.deck.pop(0)

    def orderUp(this, player):
        this.trump = this.upcard.suit
        this.maker = player

    def goAlone(this, player):
        player.alone = True
        this.playing.remove(player.partner)

    def swapCard(this, card):
        this.dealer().cards.remove(card)
        this.dealer().cards.append(this.upcard)

    def makeSuit(this, player, suit = None):
        this.maker = player
        if suit != None: this.trump = suit     
        else: this.trump = this.upcard.suit

    def playCard(this, player, card):
        player.cards.remove(card)   
        this.trick.append(card)
        player.played.append(card)

    def bestCardPlayed(this):
        bestCard = this.trick[0]

        for card in this.trick:
            compare = bestCard.compare(card, this.trump)
            if (compare < 0):
                 bestCard = card

        return bestCard

    def trickWinner(this):
        bestCard = this.bestCardPlayed()
        index = this.trick.index(bestCard)
        return this.playing[index]

    def recordTrick(this):
        record = {}
        for player in this.playing:
            record[player.name] = []

        this.pastTricks.append(record)

        # the trick is recorded in order of playing
        for i in range(0, len(this.trick)):
            record[this.playing[i].name] = this.trick[i]        
