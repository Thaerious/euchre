import pytest
from euchre.Euchre import *

@pytest.fixture
def euchre():
    names = ["Player1", "Player2", "Player3", "Player4"]
    euchre = Euchre(names)
    return euchre

def test_get_player_int(euchre):
    assert euchre.get_player(0).name == "Player1"
    assert euchre.get_player(1).name == "Player2"
    assert euchre.get_player(2).name == "Player3"
    assert euchre.get_player(3).name == "Player4"

def test_get_player_str(euchre):
    assert euchre.get_player("Player1").name == "Player1"
    assert euchre.get_player("Player2").name == "Player2"
    assert euchre.get_player("Player3").name == "Player3"
    assert euchre.get_player("Player4").name == "Player4"            

def test_initialization(euchre):
    assert len(euchre.players) == 4
    
    # player order in new game is same as player names
    assert euchre.current_player.name == "Player1"
    assert euchre.first_player.name == "Player1"

    # no maker in new game
    assert euchre.maker == None

    # the dealer is the last player in order
    assert euchre.dealer.name == "Player4"

    # the score starts at 0
    assert euchre.score[0] == 0
    assert euchre.score[1] == 0

def test_shuffle_deck(euchre):
    original_deck = euchre.deck.copy()       
    euchre.shuffle_deck()
    shuffled_deck = euchre.deck.copy()       

    # Assert the deck length remains the same
    assert len(original_deck) == len(shuffled_deck), "Deck size changed after shuffle"

    # Assert the deck contains the same cards
    assert set(original_deck) == set(shuffled_deck), "Deck contents changed after shuffle"

    # Assert the deck order has changed (non-trivial shuffle)
    assert original_deck != shuffled_deck, "Deck order did not change after shuffle"


def test_activate_dealer(euchre):
    euchre.activate_dealer()
    assert euchre.current_player == euchre.dealer

def test_activate_first_player(euchre):
    euchre.activate_dealer()
    euchre.activate_first_player()
    assert euchre.current_player.name == "Player1"

def test_activate_next_player(euchre):
    euchre.activate_next_player()
    assert euchre.current_player.name == "Player2"

# activate next player rotates to first player
def test_activate_next_player_x4(euchre):
    euchre.activate_next_player()
    euchre.activate_next_player()
    euchre.activate_next_player()
    euchre.activate_next_player()
    assert euchre.current_player.name == "Player1"

def test_deal_cards(euchre):
    euchre.deal_cards()

    assert euchre.up_card == "J♦"
    assert euchre.down_card == None
    assert euchre.discard == None

    assert set(euchre.players[0].cards) == {"9♥", "K♥", "J♠", "9♣", "K♣"}
    assert set(euchre.players[1].cards) == {"10♥", "A♥", "Q♠", "10♣", "A♣"}
    assert set(euchre.players[2].cards) == {"J♥", "9♠", "K♠", "J♣", "9♦"}
    assert set(euchre.players[3].cards) == {"Q♥", "10♠", "A♠", "Q♣", "10♦"}

def test_turn_down_card(euchre):   
    euchre.deal_cards()
    euchre.turn_down_card()

    assert euchre.up_card == None
    assert euchre.down_card == "J♦"
    assert euchre.discard == None    

def test_pick_up_card(euchre):   
    euchre.deal_cards()
    euchre.dealer_swap_card("Q♥")

    assert euchre.up_card == "J♦"
    assert euchre.down_card == None
    assert euchre.discard == "Q♥" 
    assert "J♦" in euchre.dealer.cards 
    assert "Q♥" not in euchre.dealer.cards
    assert euchre.maker.name == "Player4" #dealer

# can not turn down card after picking up
def test_turn_down_card_exception(euchre):
    euchre.deal_cards()
    euchre.dealer_swap_card("Q♥")

    # ensure precondition
    assert euchre.discard == "Q♥"

    with pytest.raises(EuchreException, match="Discard must be None to turn down."):
        euchre.turn_down_card()

# can not pick up card twice
def test_pick_up_exception_0(euchre):
    euchre.deal_cards()
    euchre.dealer_swap_card("Q♥")

    # ensure precondition
    assert euchre.discard == "Q♥"

    with pytest.raises(EuchreException, match="Discard must be None to swap."):
        euchre.dealer_swap_card("Q♠")    

# can not pick up card twice
def test_pick_up_exception_1(euchre):
    euchre.deal_cards()

    with pytest.raises(EuchreException, match="Must swap card from hand: 9♠"):
        euchre.dealer_swap_card("9♠")             
 

# must make trump before adding trick
def test_add_trick_exception_0(euchre):
    euchre.deal_cards()    

    with pytest.raises(EuchreException, match="Trump must be made before adding a trick."):
        euchre.add_trick()

def test_make_trump_up_card(euchre):
    euchre.deal_cards()    

    # precondition
    assert euchre.up_card == "J♦"

    euchre.make_trump(euchre.up_card.suit)
    assert euchre.trump == "♦"
    assert euchre.maker.name == "Player1"

def test_make_trump(euchre):
    euchre.deal_cards()    
    euchre.make_trump("♠")
    assert euchre.trump == "♠"
    assert euchre.maker.name == "Player1"

# trump can not match the down card
def test_make_trump_exception_0(euchre):
    euchre.deal_cards()    
    euchre.turn_down_card()

    # precondition
    assert euchre.down_card == "J♦"

    with pytest.raises(EuchreException, match="Trump can not match the down card."):
        euchre.make_trump("♦") 

# must make trump before adding trick
def test_add_trick_exception_0(euchre):
    euchre.deal_cards()    

    with pytest.raises(EuchreException, match="Trump must be made before adding a trick."):
        euchre.add_trick()        

def test_add_trick(euchre):
    euchre.deal_cards()    
    euchre.make_trump("♠")
    euchre.add_trick()

    assert len(euchre.tricks) == 1

def test_add_second_trick(euchre):
    euchre.deal_cards()    
    euchre.make_trump("♠")
    euchre.add_trick()

    with pytest.raises(EuchreException, match="Previous trick not complete."):
        euchre.add_trick()

def test_play_card_exception_0(euchre):
    euchre.deal_cards()    
    euchre.make_trump("♠")
    euchre.add_trick()

    with pytest.raises(EuchreException, match="Card 'Q♥' not in hand of 'Player1'."):
        euchre.play_card("Q♥")
    
def test_play_trick(euchre):
    euchre.deal_cards()    
    euchre.make_trump("♠")
    euchre.add_trick()

    euchre.play_card("9♥")

    assert "9♥" in euchre.tricks[-1]

# play 4 cards
def test_play_trick_x4(euchre):
    euchre.deal_cards()    
    euchre.make_trump("♠")
    euchre.add_trick()

    euchre.play_card("9♥")
    euchre.play_card("10♥")
    euchre.play_card("J♥")
    euchre.play_card("Q♥")

    assert len(euchre.tricks[-1]) == 4
    assert euchre.is_trick_finished

# must follow suit
def test_play_card_exception_2(euchre):
    euchre.deal_cards()    
    euchre.make_trump("♠") 

    euchre.add_trick()
    euchre.play_card("9♥")

    with pytest.raises(EuchreException, match="Card 'Q♠' must follow suit '♥'."):  
        euchre.play_card("Q♠")

# trick full can't play card
def test_play_card_exception_1(euchre):
    euchre.deal_cards()    
    euchre.make_trump("♠") 

    euchre.add_trick()
    euchre.play_card("9♥")
    euchre.play_card("10♥")
    euchre.play_card("J♥")
    euchre.play_card("Q♥")

    with pytest.raises(EuchreException, match="Trick full, can't play card 'K♥'."):    
        euchre.play_card("K♥")   

# # test the scoring of a trick by playing a hand
# def test_score_trick(euchre):
#     euchre.deal_cards()    
#     euchre.make_trump("♠")    

#     euchre.add_trick()

#     euchre.play_card("9♥")  #P1
#     euchre.play_card("10♥") #P2
#     euchre.play_card("J♥")  #P3 W
#     euchre.play_card("Q♥")  #P4
#     euchre.score_trick()

#     assert euchre.current_player.name == "Player3"    
#     assert euchre.get_player(2).tricks == 1

#     euchre.add_trick()
#     euchre.play_card("9♣")  #P3
#     euchre.play_card("10♣") #P4
#     euchre.play_card("K♠")  #P1 W
#     euchre.play_card("Q♣")  #P2 
#     euchre.score_trick()

#     assert euchre.current_player.name == "Player1"    
#     assert euchre.get_player(0).tricks == 1

#     euchre.add_trick()
#     euchre.play_card("J♣") #P1 W
#     euchre.play_card("A♠") #P2
#     euchre.play_card("K♣") #P3
#     euchre.play_card("A♣") #P4 
#     euchre.score_trick()

#     assert euchre.current_player.name == "Player1"    
#     assert euchre.get_player(0).tricks == 2

#     euchre.add_trick()
#     euchre.play_card("9♥")  #P1
#     euchre.play_card("10♥") #P2
#     euchre.play_card("J♥")  #P3
#     euchre.play_card("Q♥")  #P4 W
#     euchre.score_trick() 

#     assert euchre.current_player.name == "Player4"    
#     assert euchre.get_player(3).tricks == 1

#     euchre.add_trick()
#     euchre.play_card("10♦") #P4 W
#     euchre.play_card("K♥")  #P1
#     euchre.play_card("A♥")  #P2
#     euchre.play_card("9♦")  #P3
#     euchre.score_trick()     

#     assert euchre.current_player.name == "Player4"    
#     assert euchre.get_player(3).tricks == 2    
#     assert len(euchre.tricks) == 5
#     assert euchre.is_trick_finished    

# def test_clear_tricks(euchre):
#     test_score_trick(euchre)
#     euchre.clear_tricks()
#     assert len(euchre.tricks) == 0

# can't clear unfinished hand
# def test_clear_tricks_exception_0(euchre):
#     euchre.deal_cards()    
#     euchre.make_trump("♠")    

#     euchre.add_trick()

#     euchre.play_card("9♠")  #P1
#     euchre.play_card("10♠") #P2
#     euchre.play_card("J♠")  #P3 W
#     euchre.play_card("Q♠")  #P4
#     euchre.score_trick()

#     with pytest.raises(EuchreException, match="Can not clear an unfinished hand."):    
#         euchre.clear_tricks()

def test_go_alone_exception_0(euchre):
    # Player1 goes alone
    with pytest.raises(EuchreException, match="Trump must be made before going alone."): 
        euchre.go_alone()    

def test_go_alone(euchre):
    euchre.deal_cards()    
    euchre.make_trump("♠")  

    # Ensure the current player is Player1
    assert euchre.current_player.name == "Player1"

    # Player1 goes alone
    euchre.go_alone()

    # Check that Player1 is marked as going alone
    assert euchre.current_player.alone is True

    # Ensure Player1's partner (Player3) has been removed from the order
    partners_index = euchre.players.index(euchre.current_player.partner)
    assert partners_index not in euchre.order

# must have 5 tricks played to advance
def test_next_hand_exception_0(euchre):
    euchre.deal_cards()    
    euchre.make_trump("♠")  

    with pytest.raises(EuchreException, match="Hand not finished."): 
        euchre.next_hand()    

# def test_next_hand(euchre):
#     test_score_trick(euchre)
#     euchre.next_hand()   

#     assert euchre.hands_played == 1 
#     assert euchre.first_player.name == "Player2"
#     assert euchre.dealer.name == "Player1"
#     assert euchre.order[0] == 1
#     assert euchre.order[1] == 2
#     assert euchre.order[2] == 3
#     assert euchre.order[3] == 0

@pytest.mark.parametrize(
    "score, expected",
    [
        # Game over first team has >= 10
        ([11, 5], True),
        ([10, 5], True),

        # Game over second team has >= 10
        ([4, 12], True),
        ([6, 10], True),

        # Game not over neither team has >= 10
        ([4, 0], False),
        ([9, 9], False)
    ]
)
def test_is_game_over(score, expected):
    """
    Test the score_hand function with various scenarios.

    Args:
        maker (int): Index of the maker.
        tricks (List[int]): List of tricks won by each player.
        isAlone (bool): Whether the maker's team went alone.
        expected_score (int): Expected score based on the input.
    """
    assert is_game_over(score) == expected

@pytest.mark.parametrize(
    "maker, tricks, isAlone, expected_score",
    [
        # Maker team wins all 5 tricks, goes alone
        (0, [5, 0, 0, 0], True, [4, 0]),

        # Maker team wins all 5 tricks, does not go alone
        (0, [3, 0, 2, 0], False, [2, 0]),

        # Maker team wins 3 tricks
        (0, [3, 0, 0, 2], False, [1, 0]),

        # Maker team wins 4 tricks
        (0, [4, 0, 0, 1], False, [1, 0]),

        # Maker team loses, opponent team wins all tricks
        (0, [0, 5, 0, 0], False, [0, 2]),

        # Maker team loses, opponent team wins all tricks
        (0, [0, 3, 0, 2], False, [0, 2]),        

        # Maker team loses with mixed tricks
        (0, [2, 1, 0, 2], False, [0, 2]),

        # Maker at a different index, team wins 5 tricks alone
        (2, [0, 0, 5, 0], True, [4, 0]),

        # Maker at a different index, team wins 5 tricks not alone
        (2, [2, 0, 3, 0], False, [2, 0]),

        # Maker team wins exactly 3 tricks, does not go alone
        (1, [1, 2, 1, 1], False, [0, 1]),

        # Maker team loses with mixed tricks, maker at a different index
        (1, [1, 0, 3, 1], False, [2, 0]),
    ],
)
def test_score_hand(maker, tricks, isAlone, expected_score):
    """
    Test the score_hand function with various scenarios.

    Args:
        maker (int): Index of the maker.
        tricks (List[int]): List of tricks won by each player.
        isAlone (bool): Whether the maker's team went alone.
        expected_score (int): Expected score based on the input.
    """
    assert score_hand(maker, tricks, isAlone) == expected_score

# hand is not finished when less than 5 tricks have been added
# def test_is_hand_finished_false_0(euchre):
#     euchre.deal_cards()    
#     euchre.make_trump("♥")    

#     euchre.add_trick()

#     euchre.play_card("9♥")  #P1
#     euchre.play_card("10♥") #P2
#     euchre.play_card("J♥")  #P3 W
#     euchre.play_card("Q♥")  #P4
#     euchre.score_trick()

#     assert euchre.current_player.name == "Player3"    
#     assert euchre.get_player(2).tricks == 1

#     euchre.add_trick()
#     euchre.play_card("9♣")  #P3
#     euchre.play_card("10♣") #P4
#     euchre.play_card("K♠")  #P1 W
#     euchre.play_card("Q♣")  #P2 
#     euchre.score_trick()

#     assert euchre.current_player.name == "Player1"    
#     assert euchre.get_player(0).tricks == 1

#     euchre.add_trick()
#     euchre.play_card("J♣") #P1 W
#     euchre.play_card("A♠") #P2
#     euchre.play_card("K♣") #P3
#     euchre.play_card("A♣") #P4 
#     euchre.score_trick()

#     assert euchre.is_hand_finished == False   

# # hand is not finished when last trick is not finished
# def test_is_hand_finished_false_1(euchre):
#     euchre.deal_cards()    
#     euchre.make_trump("♠")    

#     euchre.add_trick()

#     euchre.play_card("9♠")  #P1
#     euchre.play_card("10♠") #P2
#     euchre.play_card("J♠")  #P3 W
#     euchre.play_card("Q♠")  #P4
#     euchre.score_trick()

#     assert euchre.current_player.name == "Player3"    
#     assert euchre.get_player(2).tricks == 1

#     euchre.add_trick()
#     euchre.play_card("9♣")  #P3
#     euchre.play_card("10♣") #P4
#     euchre.play_card("K♠")  #P1 W
#     euchre.play_card("Q♣")  #P2 
#     euchre.score_trick()

#     assert euchre.current_player.name == "Player1"    
#     assert euchre.get_player(0).tricks == 1

#     euchre.add_trick()
#     euchre.play_card("J♣") #P1 W
#     euchre.play_card("A♠") #P2
#     euchre.play_card("K♣") #P3
#     euchre.play_card("A♣") #P4 
#     euchre.score_trick()

#     assert euchre.current_player.name == "Player1"    
#     assert euchre.get_player(0).tricks == 2

#     euchre.add_trick()
#     euchre.play_card("9♥")  #P1
#     euchre.play_card("10♥") #P2
#     euchre.play_card("J♥")  #P3
#     euchre.play_card("Q♥")  #P4 W
#     euchre.score_trick() 

#     assert euchre.current_player.name == "Player4"    
#     assert euchre.get_player(3).tricks == 1

#     euchre.add_trick()
#     euchre.play_card("10♦") #P4 W
#     euchre.play_card("K♥")  #P1
#     euchre.play_card("A♥")  #P2

#     assert euchre.is_hand_finished == False 

# def test_is_hand_finished_true(euchre):    
    # test_score_trick(euchre)
    # assert euchre.is_hand_finished == True 
