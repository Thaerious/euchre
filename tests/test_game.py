import pytest
from euchre.Euchre import *
from euchre.Game import *

@pytest.fixture
def game():
    names = ["Player1", "Player2", "Player3", "Player4"]
    game = Game(names)
    game.seed = -1
    return game

def test_print(game):
    game.input(None, "start")  
    print(game)   

def test_state_0(game):
    assert game.current_state == 0    

def test_state_0_start(game):
    game.input(None, "start")
    assert game.current_state == 1    
    assert game.current_player.name == "Player1"
    
def test_state_1_pass(game):
    test_state_0_start(game)
    game.input("Player1", "pass")
    assert game.current_state == 1
    assert game.current_player.name == "Player2"

def test_state_1_order(game):
    test_state_0_start(game)

    suit = game.up_card.suit
    game.input("Player1", "order")

    assert game.current_state == 2
    assert game.current_player.name == game.dealer.name
    assert game.trump == suit

def test_state_1_alone(game):
    test_state_0_start(game)

    suit = game.up_card.suit
    game.input("Player1", "alone")
    assert game.current_state == 5
    assert game.current_player == game.first_player
    assert game.trump == suit
    assert game.get_player(0).alone == True

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

    assert game.current_player == game.dealer
    up_card_before = game.up_card

    game.input("Player4", "up", "10♠")

    assert game.discard == "10♠"
    assert game.down_card == None
    assert game.up_card == up_card_before
    assert game.current_state == 5

def test_state_2_down(game):
    test_state_1_order(game)    

    assert game.current_player == game.dealer
    up_card_before = game.up_card

    game.input("Player4", "down")
    
    assert game.discard == None
    assert game.down_card == up_card_before
    assert game.up_card == None
    assert game.current_state == 5    

def test_state_3_pass(game):
    test_state_1_pass_x4(game)    

    assert game.current_player == game.first_player

    game.input("Player1", "pass")
    
    assert game.current_state == 3
    assert game.current_player.name == "Player2"      

def test_state_3_pass_to_dealer(game):
    test_state_1_pass_x4(game)    

    assert game.current_player == game.first_player

    game.input("Player1", "pass")
    game.input("Player2", "pass")
    game.input("Player3", "pass")        
    
    assert game.current_state == 4
    assert game.current_player.name == game.dealer.name

def test_state_3_make(game):
    test_state_1_pass_x4(game)

    assert game.current_player == game.first_player
    up_card_before = game.up_card

    game.input("Player1", "make", "♠")
       
    assert game.current_state == 5
    assert game.trump == "♠"
    assert game.maker.name == "Player1"
    assert game.discard == None
    assert game.down_card == "J♦"
    assert game.up_card == up_card_before    

def test_state_3_alone(game):
    test_state_1_pass_x4(game)

    assert game.current_player == game.first_player
    up_card_before = game.up_card

    game.input("Player1", "alone", "♠")
       
    assert game.current_state == 5
    assert game.trump == "♠"
    assert game.maker.name == "Player1"
    assert game.discard == None
    assert game.down_card == None
    assert game.up_card == up_card_before
    assert game.get_player(0).alone      

def test_state_4_make(game):
    test_state_3_pass_to_dealer(game)

    up_card_before = game.up_card

    game.input("Player4", "make", "♠")

    assert game.current_state == 5
    assert game.trump == "♠"
    assert game.maker.name == "Player4"
    assert game.discard == None
    assert game.down_card == "J♦"
    assert game.up_card == up_card_before

def test_state_4_alone(game):
    test_state_3_pass_to_dealer(game)

    up_card_before = game.up_card

    game.input("Player4", "alone", "♠")

    assert game.current_state == 5
    assert game.trump == "♠"
    assert game.maker.name == "Player4"
    assert game.discard == None
    assert game.down_card == "J♦"
    assert game.up_card == up_card_before   
    assert game.get_player(3).alone      
    assert game.current_player.name == "Player1"

# partner of first player goes alone, 
# first player goes to next player (Player2)
def test_state_3_alone(game):
    test_state_1_pass_x4(game)
    game.input("Player1", "pass")
    game.input("Player2", "pass")
    game.input("Player3", "alone", "♥")

    assert game.current_player.name == "Player2"

# def test_state_5_play_hand(game):
#     test_state_4_make(game)       

#     assert len(game.tricks) == 1
#     game.input("Player1", "play", "9♥")
    
#     assert game.current_state == 5
#     assert game.current_player.name == "Player2"
#     assert len(game.current_trick) == 1

#     game.input("Player2", "play", "10♥")
    
#     assert game.current_state == 5
#     assert game.current_player.name == "Player3"
#     assert len(game.current_trick) == 2

#     game.input("Player3", "play", "J♥")
    
#     assert game.current_state == 5
#     assert game.current_player.name == "Player4"
#     assert len(game.current_trick) == 3    

#     game.input("Player4", "play", "Q♥")
    
#     assert game.current_state == 6
#     assert game.current_player.name == "Player4"
#     assert game.current_player.tricks == 1

#     game.input(None, "continue", None)
#     assert len(game.current_trick) == 0  # new trick

#     assert len(game.tricks) == 2 
#     game.input("Player4", "play", "10♠")
#     game.input("Player1", "play", "J♠")
#     game.input("Player2", "play", "Q♠")    
#     game.input("Player3", "play", "K♠")

#     assert len(game.tricks) == 3     
#     game.input("Player1", "play", "K♥")
#     game.input("Player2", "play", "A♥")
#     game.input("Player3", "play", "9♠")
#     game.input("Player4", "play", "A♠")

#     assert len(game.tricks) == 4
#     game.input("Player4", "play", "Q♣")
#     game.input("Player1", "play", "9♣")
#     game.input("Player2", "play", "10♣")
#     game.input("Player3", "play", "J♣")

#     assert len(game.tricks) == 5
#     game.input("Player3", "play", "9♦")
#     game.input("Player4", "play", "10♦")
#     game.input("Player1", "play", "K♣")
#     game.input("Player2", "play", "A♣")

#     assert game.current_state == 6
#     assert game.score == [0, 1]
    

def test_state_5_alone_play_hand(game):
    test_state_4_alone(game)

    game.input("Player1", "play", "9♥") 
    
    assert game.current_state == 5
    assert game.current_player.name == "Player3" # player 4 went alone so there is no player 2
    assert len(game.current_trick) == 1

    game.input("Player3", "play", "J♥") 
    
    assert game.current_state == 5
    assert game.current_player.name == "Player4" # player 4 went alone so there is no player 2
    assert len(game.current_trick) == 2  

def test_state_6_continue(game):
    test_state_5_play_hand(game)

    game.input(None, "continue") 

    assert game.current_player.name == "Player2"
    assert game.dealer.name == "Player1"
    assert game.hand_count == 1
    assert game.current_state == 1   
