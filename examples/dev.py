from euchre import *

names = ["Player1", "Player2", "Player3", "Player4"]
euchre = Euchre(names)
game = Game(euchre)
snap = Snapshot(game, euchre.getCurrentPlayer())
print(snap)
# euchre.dealCards()

# euchre.makeTrump("♠")
# euchre.playCard("J♣")
# euchre.playCard("10♠")
# euchre.playCard("J♠")
# euchre.playCard("Q♠")  

# euchre.nextTrick() 
# print(euchre)
