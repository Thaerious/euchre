from euchre import Game, Snapshot

names = ["Player1", "Player2", "Player3", "Player4"]
game = Game(names)
print(game)

snap = Snapshot(game, "Player1")
print(snap)