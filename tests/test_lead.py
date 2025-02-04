import pytest
from euchre.Euchre import *
from euchre.Game import *
@pytest.fixture
def game():
    game = Game(["Player1", "Player2", "Player3", "Player4"])
    assert game.current_state == 0
    game.input(None, 'start', None)
    
    game.set_cards('Player1', ['J♦','10♣','9♣','Q♥','Q♠'])
    game.set_cards('Player2', ['9♦','K♥','Q♣','K♦','10♠'])
    game.set_cards('Player3', ['9♥','Q♦','A♠','A♦','K♠'])
    game.set_cards('Player4', ['A♣','K♣','A♥','10♦','9♠'])
    game.up_card = '10♥'
    
    return game

def test_before_first_hand(game):
    assert game.current_state == 1
    assert game.current_player.name == "Player1"
    
    # Lead is the first player after the dealer when not playing (state 5)
    assert game.lead_player.name == "Player1"
    
    game.input(game.current_player.name, 'pass', None)
    game.input(game.current_player.name, 'pass', None)
    game.input(game.current_player.name, 'pass', None)
    game.input(game.current_player.name, 'order', None)
    game.input(game.current_player.name, 'up', '9♠')
    
    assert game.current_state == 5
    assert game.current_player.name == "Player1"
    
    #First player is lead when play first begins (state 5)
    assert game.lead_player.name == "Player1"
    
    

def test_play_first_hand(game):
    test_before_first_hand(game)
    assert game.lead_player.name == "Player1"
    
    game.input(game.current_player.name, 'play', '10♣')
    game.input(game.current_player.name, 'play', 'Q♣')
    game.input(game.current_player.name, 'play', 'Q♦')
    game.input(game.current_player.name, 'play', 'A♣')
    game.input(None, 'continue', None)
    
    assert game.lead_player.name == "Player4"
    
    game.input(game.current_player.name, 'play', 'A♥')
    game.input(game.current_player.name, 'play', 'J♦')
    game.input(game.current_player.name, 'play', 'K♥')
    game.input(game.current_player.name, 'play', '9♥')
    game.input(None, 'continue', None)
    
    assert game.lead_player.name == "Player1"
    
    game.input(game.current_player.name, 'play', 'Q♥')
    game.input(game.current_player.name, 'play', '10♠')
    game.input(game.current_player.name, 'play', 'K♠')
    game.input(game.current_player.name, 'play', '10♥')
    game.input(None, 'continue', None)
    
    assert game.lead_player.name == "Player1"
    
    game.input(game.current_player.name, 'play', 'Q♠')
    game.input(game.current_player.name, 'play', '9♦')
    game.input(game.current_player.name, 'play', 'A♠')
    game.input(game.current_player.name, 'play', 'K♣')
    game.input(None, 'continue', None)
    
    assert game.lead_player.name == "Player3"
    
    game.input(game.current_player.name, 'play', 'A♦')
    game.input(game.current_player.name, 'play', '10♦')
    game.input(game.current_player.name, 'play', '9♣')
    game.input(game.current_player.name, 'play', 'K♦')
    game.input(None, 'continue', None)
    
    assert game.lead_player.name == "Player3"
    
    game.input(None, 'continue', None)
    assert game.lead_player.name == "Player2"
    
    print(game)
    

