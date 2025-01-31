import pytest
from euchre.Euchre import *
from euchre.Game import *

def test_pass_alot():
    game = Game(["Player1", "Player2", "Player3", "Player4"])
    random.seed(100)
    assert game.current_state == 0

    game.input(None, 'start', None)
    assert game.current_state == 1
    assert game.current_player.name == "Player1"

    game.input('Player1', 'pass', None)
    game.input('Player2', 'pass', None)
    game.input('Player3', 'pass', None)
    game.input('Player4', 'pass', None)

    # all players pass, move to select suit
    assert game.current_state == 3
    assert game.current_player.name == "Player1"

    game.input('Player1', 'pass', None)
    game.input('Player2', 'pass', None)
    game.input('Player3', 'pass', None)

    # non-dealers pass, dealer must choose suit
    assert game.current_state == 4
    assert game.current_player.name == "Player4"
    assert game.current_player.name == game.dealer.name

    game.input('Player4', 'Make', '♠')

    # playing trick
    assert game.current_state == 5
    assert game.current_player.name == "Player1"

    game.input('Player1', 'play', 'A♣')
    game.input('Player2', 'play', '10♣')
    game.input('Player3', 'play', 'A♠')
    game.input('Player4', 'play', '9♣')

    # player3 won
    assert game.current_state == 6
    assert game.get_player("Player3").tricks == 1
    assert game.current_player.name == "Player3"

    # play the next 3 tricks
    game.input(None, 'continue', None)
    game.input('Player3', 'play', 'J♠')
    game.input('Player4', 'play', '9♦')
    game.input('Player1', 'play', '9♠')
    game.input('Player2', 'play', 'Q♠')
    assert game.get_player("Player3").tricks == 2

    game.input(None, 'continue', None)
    game.input('Player3', 'play', 'J♥')
    game.input('Player4', 'play', 'Q♥')
    game.input('Player1', 'play', '9♥')
    game.input('Player2', 'play', '10♥')
    assert game.get_player("Player4").tricks == 1

    # player3 trumps to win the trick
    game.input(None, 'continue', None)
    game.input('Player4', 'play', 'Q♣')
    game.input('Player1', 'play', 'K♣')
    game.input('Player2', 'play', '10♦')
    game.input('Player3', 'play', '10♠')
    assert game.get_player("Player3").tricks == 3

    game.input(None, 'continue', None)
    game.input('Player3', 'play', 'Q♦')
    game.input('Player4', 'play', 'J♦')
    game.input('Player1', 'play', 'K♠')
    game.input('Player2', 'play', 'A♦')
    assert game.get_player("Player1").tricks == 1


def test_play_game():
    game = Game(["Player1", "Player2", "Player3", "Player4"])
    game.seed = 100

    game.input(None, 'start', None)

    game.input('Player1', 'pass', None)
    game.input('Player2', 'pass', None)
    game.input('Player3', 'pass', None)
    game.input('Player4', 'pass', None)

    game.input('Player1', 'pass', None)
    game.input('Player2', 'pass', None)
    game.input('Player3', 'pass', None)
    game.input('Player4', 'Make', '♠')

    # play first trick
    game.input(game.current_player.name, 'play', 'A♣')
    game.input(game.current_player.name, 'play', '10♣')
    game.input(game.current_player.name, 'play', 'A♠')
    game.input(game.current_player.name, 'play', '9♣')
    game.input(None, 'continue', None)
    game.input(game.current_player.name, 'play', 'J♠')
    game.input(game.current_player.name, 'play', '9♦')
    game.input(game.current_player.name, 'play', '9♠')
    game.input(game.current_player.name, 'play', 'Q♠')
    game.input(None, 'continue', None)
    game.input(game.current_player.name, 'play', 'J♥')
    game.input(game.current_player.name, 'play', 'Q♥')
    game.input(game.current_player.name, 'play', '9♥')
    game.input(game.current_player.name, 'play', '10♥')
    game.input(None, 'continue', None)
    game.input(game.current_player.name, 'play', 'Q♣')
    game.input(game.current_player.name, 'play', 'K♣')
    game.input(game.current_player.name, 'play', '10♦')
    game.input(game.current_player.name, 'play', '10♠')
    game.input(None, 'continue', None)
    game.input(game.current_player.name, 'play', 'Q♦')
    game.input(game.current_player.name, 'play', 'J♦')
    game.input(game.current_player.name, 'play', 'K♠')
    game.input(game.current_player.name, 'play', 'A♦')

    print(game)
