from euchre.del_string import del_string
from euchre.card import *
from euchre import *
import random
from euchre.bots.tools.Query import Query, normalize_value
import pytest

@pytest.fixture
# Initializes a game with four players, sets up initial hands, and selects an up card.
def game():
    game = Game(['Player1', 'Player2', 'Player3', 'Player4'])
    random.seed(100)  # Ensures deterministic results for tests
    game.input(None, 'start', None)
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.set_cards('Player2', ['9♦', 'K♠', 'Q♣', 'K♦', '10♥'])    
    game.set_cards('Player3', ['9♠', 'Q♦', 'A♥', 'A♦', 'K♥'])
    game.set_cards('Player4', ['A♣', 'K♣', 'A♠', '10♦', '9♥'])      
    game.up_card = "10♠"
    return game

# Tests if an empty Query returns an empty list
def test_default(game):
    snap = Snapshot(game, 'Player1')
    qr = Query().decide(snap)

    assert qr.all == ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥']
    assert qr.action == 'no_action'
    assert qr.data == 'J♦'

# Tests if an empty Query returns an empty list
def test_all(game):
    snap = Snapshot(game, 'Player1')
    qr = Query('~').decide(snap)
    assert qr.all == ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥']
    assert qr.action == 'no_action'
    assert qr.data == 'J♦'    

# Tests if selecting all cards from a hand retrieves the correct set of cards
def test_select_all(game):
    snap = Snapshot(game, 'Player1')
    qr = Query().select('~').decide(snap)
    assert set(qr.all) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    assert qr.action == 'no_action'
    assert qr.data == 'J♦'    

# Tests if selecting all cards works when trump is set
def test_select_all_trump_set(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')
    qr = Query().select('~').decide(snap)
    assert set(qr.all) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    assert qr.action == 'no_action'
    assert qr.data == 'J♦'    

# Tests selection behavior when trump is not set
def test_normalization_no_trump(game):    
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = None        
    snap = Snapshot(game, 'Player1')

    # Spades and clubs should return an empty list when trump is not set, 
    # because there are no spades or clubs in hand    
    qr = Query('J♠ J♣').decide(snap)
    assert qr.all == []
    assert qr.action == 'rejected'
    assert qr.data == None   

    # Hearts should return only heart-suited cards
    assert set(Query('♥').decide(snap).all) == set(['Q♥', 'J♥'])

# Tests selection behavior when trump is set
def test_normalization_with_trump(game):   
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')     

    # Ensures that left bower (J♠) is correctly interpreted as J♦
    qr = Query('J♠ J♣').decide(snap)
    assert qr.all == ['J♦'] 
    assert qr.action == 'no_action'
    assert qr.data == 'J♦'   

    # Tests that selecting L (left bower) returns correct results
    qr = Query('L♠').decide(snap)
    assert qr.all == ['J♥'] 
    assert qr.action == 'no_action'
    assert qr.data == 'J♥'  

    # Left bower should only work when selecting the correct suit
    qr = Query('L♣').decide(snap)
    assert qr.all == [] 
    assert qr.action == 'rejected'
    assert qr.data == None

# Tests selecting all cards except a certain suit when trump is not set
def test_select_not_trump_not_set(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = None
    snap = Snapshot(game, 'Player1')     

    # Selects all except clubs
    qr = Query('~♣').decide(snap)
    assert qr.all == ['J♦', 'Q♥', 'Q♠', 'J♥'] 
    assert qr.action == 'no_action'
    assert qr.data == 'J♦'

# Tests selecting all cards except a certain suit when trump is set
def test_select_not_trump_set(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')  

    # Selects all except clubs (J♥ is still included since it's the left bower, not a club)
    qr = Query('~♣').decide(snap)
    assert qr.all == ['J♦', '10♣', 'Q♠', 'J♥']
    assert qr.action == 'no_action'
    assert qr.data == 'J♦'    

# Tests selecting the right bower when trump is set
def test_select_right_bower_trump_set(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')  

    # Right bower (J♠) should return J♦
    qr = Query('J♠').decide(snap)
    assert qr.all == ['J♦']
    assert qr.action == 'no_action'
    assert qr.data == 'J♦'       

# Tests multi-selection query behavior
def test_multi_select(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')  

    qr = Query('J♠ Q').decide(snap)
    assert qr.all == ['J♦', 'Q♥', 'Q♠']
    assert qr.action == 'no_action'
    assert qr.data == 'J♦' 

# Tests that dealer selection works correctly
def test_dealer_true(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    qr = Query().dealer('3').decide(snap)
    assert qr.all == ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥']
    assert qr.action == 'no_action'
    assert qr.data == 'J♦'     

# Tests that a non-dealer does not get selected
def test_dealer_false(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    qr = Query().dealer('2').decide(snap)
    assert qr.all == ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥']
    assert qr.action == 'rejected'
    assert qr.data == None

# call count incremented by one whenver the query is invoked
def test_stats_call_count(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    q = Query().dealer('2')
    assert q.stats._call_count == 0
    qr = q.decide(snap)    
    assert q.stats._call_count == 1

# activated count not incremented when query is rejected
def test_stats_call_count(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    q = Query().dealer('2')
    qr = q.decide(snap)    
    assert set(qr) == set([])
    assert q.stats._activated == 0

# activated count is incremented when query is not rejected
def test_stats_call_count(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    q = Query()
    qr = q.decide(snap)    
    assert set(qr.all) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    assert q.stats._activated == 1

def test_linked_query_positive(game):
    game.set_cards('Player1', ['A♥', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = None
    snap = Snapshot(game, 'Player1')

    # select all hearts iff A♥ ∈ {hand}
    q = Query("A♥").link("♥")
    qr = q.decide(snap)
    assert set(qr.all) == set(['A♥', 'Q♥', 'J♥'])
    assert q.stats._call_count == 1
    assert q.stats._activated == 1

def test_linked_query_negative(game):
    game.set_cards('Player1', ['K♥', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = None
    snap = Snapshot(game, 'Player1')

    # select all hearts iff A♥ ∈ {hand}
    q = Query("A♥").link("♥")
    qr = q.decide(snap)

    assert set(qr.all) == set([])
    assert q.stats._call_count == 1
    assert q.stats._activated == 0


# select the lowest heart, if there are two hearts, and one is the Ace
def test_link_00(game):
    game.set_cards('Player1', ['A♣','K♥','10♥','9♣','Q♠'])
    game.trump = '♥'
    game.up_card = 'J♥'
    snap = Snapshot(game, 'Player1')

    # hearts is clubs normalized      
    q = Query("A♥", "A♥-Debug").link("♥").count("2").worst()
    qr = q.decide(snap)
    assert qr.data == "9♣"

# select the lowest club, if there are two clubs, and one is the Ace, w/o trump
def test_link_01(game):
    game.set_cards('Player1', ['A♣','K♥','10♥','9♣','Q♠'])
    game.trump = None
    game.up_card = 'J♥'
    snap = Snapshot(game, 'Player1')

    q = Query("A♥", "A♥-Debug").link("♥").count("2").worst()
    qr = q.decide(snap)
    assert set(qr.all) == set([])

# Tests if selecting all cards works when trump is set
def test_lead_self_true(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    game.lead = 0

    snap = Snapshot(game, 'Player1')
    q = Query().lead("0").decide(snap)
    assert set(q.all) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

# Tests if selecting all cards works when trump is set
def test_lead_self_false(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    game.lead_index = 1

    snap = Snapshot(game, 'Player1')        
    q = Query().lead("0") # Gets normalized so that 0 = snap.for_player
    qr = q.decide(snap)
    assert qr.action == "rejected"
    assert qr.data == None
    assert set(qr.all) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

# Tests if selecting all cards works when trump is set
def test_wins(game):
    # game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    # game.set_cards('Player2', ['9♦', 'K♠', 'Q♣', 'K♦', '10♥'])    
    # game.set_cards('Player3', ['9♠', 'Q♦', 'A♥', 'A♦', 'K♥'])
    # game.set_cards('Player4', ['A♣', 'K♣', 'A♠', '10♦', '9♥']) 

    game.input('Player1', 'order')
    game.input('Player4', 'down')
    game.input('Player1', 'play', '10♣')

    snap = Snapshot(game, 'Player2')        
    q = Query().wins()
    qr = q.decide(snap)
    print(qr)

    assert qr.action == "no_action"
    # assert qr.data == None
    assert set(qr.all) == set(['K♠', 'Q♣'])

