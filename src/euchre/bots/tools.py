from euchre.Card import Card

def allowedSuits(notSuit):
    suits = ["♠", "♣", "♥", "♦"]
    suits.remove(notSuit)
    return suits

def playable(trump, trick, hand):
    playable = []
    for c in hand:
        if canPlay(trump, trick, hand, c):
            playable.append(c)

    return playable

# true if the player is allowed to play card
# only checks the cards, player order is not considered
def canPlay(trump, trick, hand, card):
    if len(trick) == 0: 
        return True

    leadSuit = trick[0].getSuit(trump)
    if card.getSuit(trump) == leadSuit: 
        return True        

    for c in hand:
        if c.getSuit(trump) == leadSuit : return False

    return True