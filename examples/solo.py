from euchre import *
from euchre.Euchre import *
from euchre.bots.Bot import Bot
from euchre.Card import compare_card_by_suit
from functools import cmp_to_key
from euchre.delString import delString
import random

stateLabels = [
    "Game not started",
    "Order up dealer [pass, order, alone]",
    "Pick up card [up, down]",
    "Make suit [pass, make, alone]",
    "Dealer make suit [make, alone]",
    "Play a card"
]

def print_hand(game):
    cards = game.euchre.players[0].cards.copy()
    
    cards = sorted(cards, key=cmp_to_key(compare_card_by_suit))
    for card in cards:
        print(f"[{card}]", end = "")
    print("")        

def print_game(game):
    print("+-----------------------------------------+")
    for player in game.euchre.players:
        print(f"{player.name}", end = "\t")
    print("")

    if game.current_state >= 1 and game.current_state <= 4:
        for player in game.euchre.players:
            if player == game.euchre.current_player:
                print(f"[x]", end = "\t")
            else:
                print(f"[ ]", end = "\t")
        print(f"\nupcard [{game.euchre.up_card}]")
    else:        
        for player in game.euchre.players:
            if player == game.euchre.current_player:
                print(f"[x]", end = "\t")
            else:
                print(f"[]", end = "\t")
        print(f"\ntrump [{game.euchre.trump}]")                
        

    print_hand(game)

random.seed(1234)
game = Game(["Adam", "T100", "Skynet", "Robocop"])

bot = Bot()

game.input(None, "start")

while game.current_state != 0:
    try:
        print_game(game)
        cmd = input(f"\n{stateLabels[game.current_state]}> ")
        if cmd =='': 
            pass
        elif cmd == 'x': 
            break
        elif cmd == 's': 
            snap = Snapshot(game, game.euchre.current_player)
            print(snap)
        elif cmd == 'b' or cmd == 'bot':
            snap = Snapshot(game, game.euchre.current_player)
            action = bot.decide(snap)
            print(f"bot> {action[0]} {action[1]}\n")
            game.input(game.euchre.current_player.name, action[0], action[1])
        else:
            split = cmd.split()

            action = split[0]
            value = None if len(split) <= 1 else split[1]

            game.input(game.euchre.players[0].name, action, value)

    except EuchreException as ex:
        print(ex, end="\n\n")
