from euchre.card.Card import Card

def allowedSuits(notSuit):
    suits = ["♠", "♣", "♥", "♦"]
    suits.remove(notSuit)
    return suits

def playable(trick, hand):
    playable = []
    for c in hand:
        if trick.can_play(c):
            playable.append(c)

    return playable

def teamOf(pIndex):
    return pIndex % 2

def otherTeam(team):
    return (team + 1) % 2