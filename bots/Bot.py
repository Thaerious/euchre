from Card import Card
import random

class Bot:
    def decide(this, snap):
        this.snap = snap
        if snap.state == 0: return None
        elif snap.state == 1: return this.decideOrderUp()
        elif snap.state == 2: return this.decideAlone()
        elif snap.state == 3: return this.decideCard()
        elif snap.state == 4: return this.decideSuit()
        elif snap.state == 5: return this.dealerSuit()
        elif snap.state == 6: return this.decideAlone()
        elif snap.state == 7: return this.playCard()

    def decideOrderUp(this):
        if random.random() > 0.5: return "pass"
        return "order"

    def decideAlone(this):
        if random.random() > 0.5: return "alone"
        return "helper"        

    def decideCard(this):
        if random.random() > 0.5: return "down"
        card = this.snap.cards.randomItem()
        return f"up {card}"

    def decideSuit(this):
        if random.random() > 0.5: return "pass"
        return this.dealerSuit()

    def dealerSuit(this):
        card = this.snap.cards.randomItem()
        suit = card[-1]
        return f"make {suit}"        

    def playCard(this):
        playable = this.snap.cards.playableCards(this.snap.trick, this.snap.trump)
        card = playable.randomItem()
        return f"play {card}"
