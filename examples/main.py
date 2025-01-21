from euchre import Game, Snapshot
from euchre.bots import Bot

names = ["Player1", "Player2", "Player3", "Player4"]
game = Game(names)
game.set_bot(1, Bot())
game.set_bot(2, Bot())
game.set_bot(3, Bot())

game.input(None, "start")

print(Snapshot(game, "Player1"))

game.input("Player1", "pass")
print(f"{game.last_player} {game.last_action}")
game.bot_action()
print(f"{game.last_player} {game.last_action}")
game.bot_action()
print(f"{game.last_player} {game.last_action}")
game.bot_action()
print(f"{game.last_player} {game.last_action}")

# print(Snapshot(game, "Player1"))
# print(Snapshot(game, "Player1").to_json())
