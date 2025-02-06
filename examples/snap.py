from euchre import *
from euchre.card import *
from euchre.class_getter import *
from euchre.bots.tools.Compiled_Query import CQuery
import random

names = ["Player1", "Player2", "Player3", "Player4"]
game = Game(names)
game.input(None, "start")

game.set_cards("Player1", ['9♦', 'A♥', 'J♥', 'A♠', 'J♦'])
game.trump = "♥"
game.up_card = "A♦"

snap = Snapshot(game, "Player1")
print(snap)

q = CQuery()
q.hand.select("LJ♠")
q.count.set_if(lambda x: x >= 2)
q.worst()

print(q.count)
print(q.test(snap))
print(q.all(snap))
print(q.get(snap))
