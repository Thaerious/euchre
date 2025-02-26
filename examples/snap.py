from euchre import *
from euchre.card import *
from euchre.class_getter import *
from euchre.bots.tools.Query import Query
from euchre.bots.tools.denormalize import denormalize

# ["♠", "♥", "♣", "♦"]

names = ["Player1", "Player2", "Player3", "Player4"]
game = Game(names)
game.input(None, "start")
game.input("Player1", "order")
game.input("Player4", "down")

game.set_cards("Player1", ['10♥', 'A♥', 'J♥', 'A♠', 'J♦'])
game.trump = "♥"
# game.up_card = "A♦"

snap = Snapshot(game, "Player1")
# snap.tricks = [Trick(snap.trump, snap.order)]
# snap.tricks[-1].append('9♥')

q = Query().select("♥")
print(q._hand)
print(q.decide(snap))
