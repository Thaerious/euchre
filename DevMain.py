from Euchre import Euchre
from Game import Game, ActionException
from delString import delString
from snapshot import snapshot
from pprint import pprint
from bots.Bot import Bot
import random
from pprint import pprint

euchre = Euchre(["Adam", "T100", "Skynet", "Robocop"])
game = Game(euchre)
random.seed(0)
game.input(None, "start")
game.input(game.activePlayer, "order")
game.input(game.activePlayer, "helper")
game.input(game.activePlayer, "down")
game.input(game.activePlayer, "play", game.activePlayer.cards[0])

snap = snapshot(game, game.activePlayer).run()
game.print()
print(type(snap["trick"][0]))

