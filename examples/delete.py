from euchre.card import Deck, Card
from euchre import Game
import copy

game = Game(["Adam", "Eve", "Cain", "Able"])
game1 = copy.deepcopy(game)
game.input(None, "start", None)

print(game, game1)