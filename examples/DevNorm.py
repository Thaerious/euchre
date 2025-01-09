from types import SimpleNamespace
from euchre import *
from euchre.Card import Deck, Trick
from euchre.Normalized import Normalized
import random

random.seed(1234)
euchre = Euchre(["Adam", "T100", "Skynet", "Robocop"])
game = Game(euchre)

euchre.shuffle()
euchre.players.rotate()
euchre.copyPlayersToPlaying()
euchre.deal_cards()

norm = Normalized(euchre, euchre.players[0])

print("**** Euchre Object ****")
print(euchre)
print("**** Normalized Object ****")
print(norm)
