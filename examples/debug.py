from euchre import *
from euchre.card.Card import Card

false = False
true = True
null = None

source = {"players": [{"name": "Bot_20", "tricks": 0, "played": [], "hand": ["J\u2663", "A\u2660", "Q\u2665", "9\u2666", "9\u2663"], "alone": false}, {"name": "Bot_11", "tricks": 0, "played": [], "hand": ["K\u2663", "10\u2660", "10\u2665", "A\u2665", "10\u2666"], "alone": false}, {"name": "Bot_21", "tricks": 0, "played": [], "hand": ["K\u2660", "J\u2660", "A\u2666", "Q\u2663", "A\u2663"], "alone": false}, {"name": "Bot_10", "tricks": 0, "played": [], "hand": ["10\u2663", "K\u2666", "J\u2665", "9\u2665", "J\u2666"], "alone": false}], "tricks": [], "deck": ["9\u2660", "K\u2665", "Q\u2660"], "trump": null, "order": [0, 1, 2, 3], "current_player": 3, "dealer": 3, "lead": 0, "maker": null, "hand_count": 0, "up_card": null, "down_card": "Q\u2666", "discard": null, "hash": "65d5ea9b", "state": 4, "last_player": 2, "last_action": "pass"}
game = Game.from_json(source)
game.discard = Card(game.deck, "A♠")

snap = Snapshot(game, "Bot_20")

print(game)
print("-----")
print(snap)
