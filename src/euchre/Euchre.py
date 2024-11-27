from euchre.Player import Player, PlayerList, Team
from euchre.Card import Card, Deck, Trick, Hand
from euchre.delString import delString
import random

class Euchre:
    def __init__(this, names):
        random.shuffle(names)
        this.players = PlayerList(names) # the order for the hand
        this.playing = PlayerList() # the order for the trick

        this.teams = [this.players[0].team, this.players[1].team]
        this.deck = Deck()

        this.trick = Trick()
        this.upcard = None
        this.downcard = None
        this.trump = ""
        this.maker = None
        
    def shuffle(this):
        this.deck = Deck().shuffle()
        this.trick = Trick()

    def canPlay(this, player, card):       
        if len(this.trick) == 0: return True
        leadSuit = this.trick[0].getSuit(this.trump)
        if card.getSuit(this.trump) == leadSuit: return True        

        for playerCard in player.cards:
            if playerCard.getSuit(this.trump) == leadSuit : return False

        return True

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

    def dealerSwapCard(this, card):
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
        bestCard = this.playing[0].played[-1]

        for player in this.playing:            
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
            if callable(attrValue): continue
            sb = sb + f"{attr} : {str(attrValue)}\n"

        sb = sb + f"dealer : {this.dealer().name}\n"

        for player in this.players:
            sb = sb + f"{str(player)}\n"

        return sb
        
