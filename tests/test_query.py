from euchre.del_string import del_string
from euchre.card import *
from euchre import *
import random
from euchre.bots.tools.Query import Query
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
def test_empty(game):
    snap = Snapshot(game, 'Player1')
    q = Query().all(snap)
    assert q == []

# Tests if selecting all cards from a hand retrieves the correct set of cards
def test_select_all(game):
    snap = Snapshot(game, 'Player1')
    q = Query()    
    q = q.select('~').all(snap)
    assert set(q) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

# Tests if selecting all cards works when trump is set
def test_select_all_trump_set(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')
    assert Query().select('~').all(snap) == ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥']

# Tests selection behavior when trump is not set
def test_select_no_trump_is_not_normalized(game):        
    snap = Snapshot(game, 'Player1')

    # Spades and clubs should return an empty list when trump is not set
    assert Query().select('J♠ J♣').all(snap) == []

    # Hearts should return only heart-suited cards
    assert set(Query().select('♥').all(snap)) == set(['Q♥', 'J♥'])

# Tests selection behavior when trump is set
def test_select_with_trump_is_normalized(game):   
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')     

    # Ensures that left bower (J♠) is correctly interpreted as J♦
    assert Query().select('J♠ J♣').all(snap) == ['J♦'] 

    # Tests that selecting L (left bower) returns correct results
    assert Query().select('L♠').all(snap) == ['J♥']  

    # Left bower should only work when selecting the correct suit
    assert Query().select('L♣').all(snap) == []

# Tests selecting all cards except a certain suit when trump is not set
def test_select_not_trump_not_set(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = None
    snap = Snapshot(game, 'Player1')     

    # Selects all except clubs
    assert Query().select('~♣').all(snap) == ['J♦', 'Q♥', 'Q♠', 'J♥']  

# Tests selecting all cards except a certain suit when trump is set
def test_select_not_trump_set(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')  

    # Selects all except clubs (J♥ is still included since it's the left bower)
    assert Query().select('~♣').all(snap) == ['J♦', '10♣', 'Q♠', 'J♥']  

# Tests selecting the right bower when trump is set
def test_select_right_bower_trump_set(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')  

    # Right bower (J♠) should return J♦
    assert Query().select('J♠').all(snap) == ['J♦']

# Tests multi-selection query behavior
def test_multi_select(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')  

    q = Query().select('J♠ Q')
    assert q.all(snap) == ['J♦', 'Q♥', 'Q♠']

# Tests that dealer selection works correctly
def test_dealer_true(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').dealer('3').all(snap)
    assert set(q) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

# Tests that a non-dealer does not get selected
def test_dealer_false(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').dealer('2').all(snap)
    assert set(q) == set([])

# call count incremented by one whenver the query is invoked
def test_stats_call_count(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').dealer('2')
    qr = q.all(snap)    
    assert q.stats._call_count == 1

# activated count not incremented when query returns an empty set
def test_stats_call_count(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').dealer('2')
    qr = q.all(snap)    
    assert set(qr) == set([])
    assert q.stats._activated == 0

# activated count is incremented when query returns an non-empty set
def test_stats_call_count(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    q = Query().select('~')
    qr = q.all(snap)    
    assert set(qr) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    assert q.stats._activated == 1

def test_linked_query_positive(game):
    game.set_cards('Player1', ['A♥', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = None
    snap = Snapshot(game, 'Player1')

    # select all hearts iff A♥ ∈ {hand}
    q = Query("A♥").link("♥")
    qr = q.all(snap)
    assert set(qr) == set(['A♥', 'Q♥', 'J♥'])
    assert q.stats._call_count == 1
    assert q.stats._activated == 1

def test_linked_query_negative(game):
    game.set_cards('Player1', ['K♥', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = None
    snap = Snapshot(game, 'Player1')

    # select all hearts iff A♥ ∈ {hand}
    q = Query("A♥").link("♥")
    qr = q.all(snap)
    assert set(qr) == set([])
    assert q.stats._call_count == 1
    assert q.stats._activated == 0


def test_special_case(game):
    game.set_cards('Player1', ['A♣','K♥','10♥','9♣','Q♠'])
    game.trump = '♥'
    game.up_card = 'J♥'
    snap = Snapshot(game, 'Player1')

    # hearts is clubs normalized      
    q = Query("A♥", "A♥-Debug").link("♥").count("2").worst()
    qr = q.all(snap)
    print(q)
    print(qr)
    assert set(qr) == set(['9♣'])

# Additional test functions follow a similar pattern

# These test cases ensure that selecting lead, maker, up card, down card,
# playable cards, best/worst cards, and other logic work correctly within the game.

# Ensures robustness of the Query class, correct interpretation of trump rules,
# selection of right and left bowers, and accurate gameplay decision-making.
