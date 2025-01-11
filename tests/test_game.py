import pytest
import numpy as np
from euchre.Euchre import *
from euchre.Game import *
import random

@pytest.fixture
def game():
    random.seed(1000)
    names = ["Player1", "Player2", "Player3", "Player4"]
    game = Game(names)
    return game

def test_print(game):
    game.input(None, "start")  
    print(game)   

def test_state_0(game):
    assert game.current_state == 0    

def test_state_0_start(game):
    game.input(None, "start")
    assert game.current_state == 1    
    assert game.euchre.current_player.name == "Player1"
    
def test_state_1_pass(game):
    test_state_0_start(game)
    game.input("Player1", "pass")
    assert game.current_state == 1
    assert game.euchre.current_player.name == "Player2"

def test_state_1_order(game):
    test_state_0_start(game)

    suit = game.euchre.up_card.suit
    game.input("Player1", "order")
    assert game.current_state == 2
    assert game.euchre.current_player.name == game.euchre.dealer.name
    assert game.euchre.trump == suit

def test_state_1_alone(game):
    test_state_0_start(game)

    suit = game.euchre.up_card.suit
    game.input("Player1", "alone")
    assert game.current_state == 5
    assert game.euchre.current_player == game.euchre.first_player
    assert game.euchre.trump == suit
    assert game.euchre.get_player(0).alone == True

def test_state_1_pass_exception_0(game):
    test_state_0_start(game)

    with pytest.raises(ActionException, match="Incorrect Player: expected 'Player1' found 'Player2'."):
        game.input("Player2", "pass")

def test_state_1_pass_x4(game):
    test_state_0_start(game)
    game.input("Player1", "pass")
    assert game.current_state == 1    
    game.input("Player2", "pass")
    assert game.current_state == 1
    game.input("Player3", "pass")
    assert game.current_state == 1
    game.input("Player4", "pass")
    assert game.current_state == 3

def test_state_2_up(game):
    test_state_1_order(game)    

    assert game.euchre.current_player == game.euchre.dealer

    game.input("Player4", "up", "9♦")

    assert game.euchre.discard == "9♦"
    assert game.euchre.down_card == None
    assert game.euchre.up_card == "J♥"
    assert game.current_state == 5

def test_state_2_down(game):
    test_state_1_order(game)    

    assert game.euchre.current_player == game.euchre.dealer

    game.input("Player4", "down")
    
    assert game.euchre.discard == None
    assert game.euchre.down_card == "J♥"
    assert game.euchre.up_card == None
    assert game.current_state == 5    

def test_state_3_pass(game):
    test_state_1_pass_x4(game)    

    assert game.euchre.current_player == game.euchre.first_player

    game.input("Player1", "pass")
    
    assert game.current_state == 3
    assert game.euchre.current_player.name == "Player2"      

def test_state_3_pass_to_dealer(game):
    test_state_1_pass_x4(game)    

    assert game.euchre.current_player == game.euchre.first_player

    game.input("Player1", "pass")
    game.input("Player2", "pass")
    game.input("Player3", "pass")        
    
    assert game.current_state == 4
    assert game.euchre.current_player.name == game.euchre.dealer.name

def test_state_3_make(game):
    test_state_1_pass_x4(game)

    assert game.euchre.current_player == game.euchre.first_player

    game.input("Player1", "make", "♠")
       
    assert game.current_state == 5
    assert game.euchre.trump == "♠"
    assert game.euchre.maker.name == "Player1"
    assert game.euchre.discard == None
    assert game.euchre.down_card == None
    assert game.euchre.up_card == "J♥"    

def test_state_3_make(game):
    test_state_1_pass_x4(game)

    assert game.euchre.current_player == game.euchre.first_player

    game.input("Player1", "make", "♠")
       
    assert game.current_state == 5
    assert game.euchre.trump == "♠"
    assert game.euchre.maker.name == "Player1"
    assert game.euchre.discard == None
    assert game.euchre.down_card == None
    assert game.euchre.up_card == "J♥"      

def test_state_3_alone(game):
    test_state_1_pass_x4(game)

    assert game.euchre.current_player == game.euchre.first_player

    game.input("Player1", "alone", "♠")
       
    assert game.current_state == 5
    assert game.euchre.trump == "♠"
    assert game.euchre.maker.name == "Player1"
    assert game.euchre.discard == None
    assert game.euchre.down_card == None
    assert game.euchre.up_card == "J♥" 
    assert game.euchre.get_player(0).alone      

def test_state_4_make(game):
    test_state_3_pass_to_dealer(game)
    game.input("Player4", "make", "♠")
    assert game.current_state == 5
    assert game.euchre.trump == "♠"
    assert game.euchre.maker.name == "Player4"
    assert game.euchre.discard == None
    assert game.euchre.down_card == None
    assert game.euchre.up_card == "J♥" 

def test_state_4_alone(game):
    test_state_3_pass_to_dealer(game)
    game.input("Player4", "alone", "♠")
    assert game.current_state == 5
    assert game.euchre.trump == "♠"
    assert game.euchre.maker.name == "Player4"
    assert game.euchre.discard == None
    assert game.euchre.down_card == None
    assert game.euchre.up_card == "J♥"   
    assert game.euchre.get_player(3).alone      
    assert game.euchre.current_player.name == "Player1"

# partner of first player goes alone, 
# first player goes to next player (Player2)
def test_state_3_alone(game):
    test_state_1_pass_x4(game)
    game.input("Player1", "pass")
    game.input("Player2", "pass")
    game.input("Player3", "alone")    

    assert game.euchre.current_player.name == "Player2"

def test_state_5_play_hand(game):
    test_state_4_make(game)       

    assert len(game.euchre.tricks) == 1
    game.input("Player1", "play", "Q♠")
    
    assert game.current_state == 5
    assert game.euchre.current_player.name == "Player2"
    assert len(game.euchre.current_trick) == 1

    game.input("Player2", "play", "9♠")
    
    assert game.current_state == 5
    assert game.euchre.current_player.name == "Player3"
    assert len(game.euchre.current_trick) == 2

    game.input("Player3", "play", "10♠")
    
    assert game.current_state == 5
    assert game.euchre.current_player.name == "Player4"
    assert len(game.euchre.current_trick) == 3    

    game.input("Player4", "play", "A♠")
    
    assert game.current_state == 5
    assert game.euchre.current_player.name == "Player4"
    assert game.euchre.current_player.tricks == 1
    assert len(game.euchre.current_trick) == 0  # new trick

    assert len(game.euchre.tricks) == 2 
    game.input("Player4", "play", "Q♣")
    game.input("Player1", "play", "A♣")
    game.input("Player2", "play", "K♣")
    with pytest.raises(EuchreException, match="Card 'A♥' must follow suit '♣'."):
        game.input("Player3", "play", "A♥")

    game.input("Player3", "play", "9♣")

    assert len(game.euchre.tricks) == 3     
    game.input("Player1", "play", "J♦")
    game.input("Player2", "play", "K♦")
    game.input("Player3", "play", "J♣")
    game.input("Player4", "play", "9♦")
    
    assert len(game.euchre.tricks) == 4
    game.input("Player3", "play", "A♥")
    game.input("Player4", "play", "9♥")
    game.input("Player1", "play", "K♥")
    game.input("Player2", "play", "J♠")

    assert len(game.euchre.tricks) == 5
    game.input("Player2", "play", "Q♦")
    game.input("Player3", "play", "10♣")
    game.input("Player4", "play", "10♥")
    game.input("Player1", "play", "10♦")

    assert game.current_state == 6
    assert game.euchre.score == [0, 1]
    

def test_state_5_alone_play_hand(game):
    test_state_4_alone(game)

    game.input("Player1", "play", "Q♠") 
    
    assert game.current_state == 5
    assert game.euchre.current_player.name == "Player3" # player 4 went alone so there is no player 2
    assert len(game.euchre.current_trick) == 1

    game.input("Player3", "play", "10♠") 
    
    assert game.current_state == 5
    assert game.euchre.current_player.name == "Player4" # player 4 went alone so there is no player 2
    assert len(game.euchre.current_trick) == 2  

def test_state_6_continue(game):
    test_state_5_play_hand(game)

    game.input(None, "continue") 

    assert game.euchre.current_player.name == "Player2"
    assert game.euchre.dealer.name == "Player1"
    assert game.euchre.hand_count == 1
    assert game.current_state == 1

    print(game)
    
