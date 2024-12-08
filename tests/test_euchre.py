import unittest
import pytest
from euchre.Euchre import Euchre, EuchreException

@pytest.fixture
def euchre():
    names = ["Player1", "Player2", "Player3", "Player4"]
    euchre = Euchre(names)
    return euchre

def test_initialization(euchre):
    assert len(euchre.players) == 4
    
    assert euchre.order == [0, 1, 2, 3]
    assert euchre.dealer == 3
    assert euchre.currentPlayer == 0
    
    assert len(euchre.trick) is 0
    assert euchre.upCard is None
    assert euchre.downCard is None
    assert euchre.trump is None
    assert euchre.maker is None

    assert euchre.players[0].cards == []
    assert euchre.players[1].cards == []
    assert euchre.players[2].cards == []
    assert euchre.players[3].cards == []
    assert euchre.players[0].played == []
    assert euchre.players[1].played == []
    assert euchre.players[2].played == []
    assert euchre.players[3].played == []    

def test_next_hand_x1(euchre):
    euchre.nextHand()
    assert euchre.order == [1, 2, 3, 0]
    assert euchre.dealer == 0
    assert euchre.currentPlayer == 1

def test_next_hand_x2(euchre):
    euchre.nextHand()
    euchre.nextHand()

    assert euchre.order == [2, 3, 0, 1]
    assert euchre.dealer == 1
    assert euchre.currentPlayer == 2

# rotates back to the first player
def test_next_hand_x4(euchre):
    euchre.nextHand()
    euchre.nextHand()
    euchre.nextHand()
    euchre.nextHand()

    assert euchre.order == [0, 1, 2, 3]
    assert euchre.dealer == 3
    assert euchre.currentPlayer == 0    

# retrieve the player object for the first player
# when first initialized the player order will the same as the names
def test_get_current_player(euchre):
    assert euchre.getCurrentPlayer().name == "Player1"

# retrieve the player object for the dealer
# when first initialized the player order will the same as the names
def test_get_dealer(euchre):
    assert euchre.getDealer().name == "Player4"

# if next player has not been called,
# is at first player returns true
def test_is_at_first_player(euchre):
    assert euchre.isAtFirstPlayer() == True

# activate dealer makes the current player the dealer
def test_activate_dealer(euchre):
    euchre.activateDealer()
    assert euchre.getCurrentPlayer().name == "Player4"   

# activate next player makes the current player the next in order
def test_activate_next_player_x1(euchre):
    euchre.activateNextPlayer()
    assert euchre.getCurrentPlayer().name == "Player2" 

# activate next player makes the current player the next in order
def test_activate_next_player_x2(euchre):
    euchre.activateNextPlayer()
    euchre.activateNextPlayer()
    assert euchre.getCurrentPlayer().name == "Player3" 

# activate next player makes the current player the next in order
# x4 cycles back to the first player
def test_activate_next_player_x4(euchre):
    euchre.activateNextPlayer()
    euchre.activateNextPlayer()
    euchre.activateNextPlayer()
    euchre.activateNextPlayer()    
    assert euchre.getCurrentPlayer().name == "Player1" 

# activate first player makes the current player the first player
def test_activate_first_player(euchre):
    euchre.activateNextPlayer()
    euchre.activateFirstPlayer()
    assert euchre.getCurrentPlayer().name == "Player1"       

# deal cards to each player and the upCard
# the cards will be in a predictable order because they have not been shuffled
def test_deal_cards(euchre):
    euchre.dealCards()

    assert euchre.players[0].cards == ["9♠", "K♠", "J♣", "9♥", "K♥"]
    assert euchre.players[1].cards == ["10♠", "A♠", "Q♣", "10♥", "A♥"]
    assert euchre.players[2].cards == ["J♠", "9♣", "K♣", "J♥", "9♦"]
    assert euchre.players[3].cards == ["Q♠", "10♣", "A♣", "Q♥", "10♦"]
    assert euchre.players[0].played == []
    assert euchre.players[1].played == []
    assert euchre.players[2].played == []
    assert euchre.players[3].played == []       
    assert euchre.upCard == "J♦"
    assert euchre.trick == []

# playing a card removes it from player.cards and inserts it into player.played and euchre.trick
def test_play_card_x1(euchre):
    euchre.dealCards()
    euchre.makeTrump("♠");
    euchre.playCard("9♠")

    assert euchre.players[0].cards == ["K♠", "J♣", "9♥", "K♥"]
    assert euchre.players[0].played == ["9♠"]
    assert euchre.trick == ["9♠"]

def test_play_card_x2(euchre):
    euchre.dealCards()
    euchre.makeTrump("♠");
    euchre.playCard("9♠")
    euchre.playCard("10♠")

    assert euchre.players[0].cards == ["K♠", "J♣", "9♥", "K♥"]
    assert euchre.players[0].played == ["9♠"]
    assert euchre.players[1].cards == ["A♠", "Q♣", "10♥", "A♥"]
    assert euchre.players[1].played == ["10♠"]    
    assert euchre.trick == ["9♠", "10♠"]

# player must have the card to play the card
def test_play_card_exception_1(euchre):
    euchre.dealCards()
    euchre.makeTrump("♠");

    with pytest.raises(EuchreException):        
        euchre.playCard("10♠")


# player must follow suit
# player2 could follow suit but doesn't
def test_follow_suit_1(euchre):
    euchre.dealCards()
    euchre.makeTrump("♠");
    euchre.playCard("9♠")

    with pytest.raises(EuchreException):        
        euchre.playCard("Q♣")
    
# player must follow suit
# player1 leads left bower
# player2 could follow suit but doesn't
def test_follow_suit_2(euchre):
    euchre.dealCards()
    euchre.makeTrump("♠")
    euchre.playCard("J♣")

    with pytest.raises(EuchreException):        
        euchre.playCard("Q♣")    

# player1 goes alone
# player3 is removed
def test_go_alone(euchre):
    euchre.dealCards()
    euchre.makeTrump("♠")
    euchre.goAlone()

    assert euchre.order == [0, 1, 3]

# trick is not finished if 4 cards have not been played
def test_is_trick_finished_1(euchre):
    euchre.dealCards()
    euchre.makeTrump("♠")
    assert euchre.isTrickFinished() == False

# trick is finished if 4 cards have been played
def test_is_trick_finished_2(euchre):
    euchre.dealCards()
    euchre.makeTrump("♠")

    euchre.playCard("J♣")
    euchre.playCard("10♠")
    euchre.playCard("J♠")
    euchre.playCard("Q♠")

    assert euchre.isTrickFinished() == True    

# if a player has gone alone
# trick is finished if 3 cards have been played
def test_is_trick_finished_3(euchre):
    euchre.dealCards()
    euchre.makeTrump("♠")
    euchre.goAlone()

    euchre.playCard("J♣")
    euchre.playCard("10♠")
    euchre.playCard("Q♠")

    assert euchre.isTrickFinished() == True   

def test_dealer_swap_card(euchre):
    euchre.dealCards()
    euchre.dealerSwapCard("10♦")
    assert euchre.getDealer().cards == ["Q♠", "10♣", "A♣", "Q♥", "J♦"]
    assert euchre.downCard == "10♦"

def test_can_not_advance_incomplete_trick(euchre):
    euchre.dealCards()
    euchre.makeTrump("♠")
    euchre.playCard("J♣")   

    with pytest.raises(EuchreException):        
        euchre.nextTrick()   

def test_next_trick(euchre):
    euchre.dealCards()
    euchre.makeTrump("♠")
    euchre.playCard("J♣")
    euchre.playCard("10♠")
    euchre.playCard("J♠")
    euchre.playCard("Q♠")  

    euchre.nextTrick()       

    assert euchre.players[2].tricks == 1
    assert euchre.order == [2, 3, 0, 1]



