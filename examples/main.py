from euchre import Game, Snapshot
from euchre.bots import Bot
import random

names = ["Player1", "Player2", "Player3", "Player4"]
game = Game(names)

game.debug_seed = 1000

game.set_bot(1, Bot())
game.set_bot(2, Bot())
game.set_bot(3, Bot())

game.input(None, "start")

snap = Snapshot(game, game.euchre.current_player.name)
print(f"{snap.trump} {snap.up_card}")

game.input("Player1", "pass")
print(f"{game.last_player} {game.last_action}")
game.bot_action()
print(f"{game.last_player} {game.last_action}")
game.bot_action()
print(f"{game.last_player} {game.last_action}")
game.bot_action()
print(f"{game.last_player} {game.last_action}")
