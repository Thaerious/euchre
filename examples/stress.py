from euchre import *
from euchre.bots import Bot
from euchre.card import *
from euchre.class_getter import *
import random

names = ["Player1", "Player2", "Player3", "Player4"]
bot = Bot()

# for i in range(5):

random.shuffle(names)
game = Game(names)
game.input(None, "start")

while game.current_state != 0:
    print(game.current_state)
    if game.current_state == 6:
        game.input(None, "continue", None)    
    if game.current_state == 7:
        game.input(None, "continue", None)    

    (action, data) = bot.decide(Snapshot(game, game.current_player.name))
    game.input(game.current_player.name, action, data)
    print(f"{game.score} {game.is_game_over()}")