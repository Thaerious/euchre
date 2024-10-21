from Player import Player, PlayerList, Team
from Card import Card
import random

class Euchre:
    def __init__(this, names):
        random.shuffle(names)
        this.players = PlayerList(names) # the order for the hand
        this.playing = PlayerList() # the order for the trick

        this.teams = [this.players[0].team, this.players[1].team]
        
        this.trick = []
        this.upcard = None
        this.downcard = None
        this.trump = ""
        this.maker = None
        
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
        this.downcard = card

    def makeSuit(this, player, suit = None):
        this.maker = player
        if suit != None: this.trump = suit     
        else: this.trump = this.upcard.suit

    def playCard(this, player, card):
        player.cards.remove(card)   
        player.played.append(card)
        this.trick.append(card)

    def trickWinner(this):
        bestPlayer = this.playing[0]        

        for player in this.playing:
            bestCard = this.playing[0].played[-1]
            card = player.played[-1]
            compare = bestCard.compare(card, this.trump)
            if (compare < 0):
                 bestPlayer = player

        return bestPlayer 
