# test_game.py
from euchre import Game

# ["♠", "♥", "♣", "♦"]

def test_maker_is_dealer_that_orders_up():
    game = Game(["Player1", "Player2", "Player3", "Player4"])
    game.input(None, "start", None)

    game.input("Player1", "pass", None)
    game.input("Player2", "order", None)
    game.input("Player4", "up", game.players[3].hand[0])

    # the bug incorectly made this Player4
    assert game.maker.name == "Player2"
