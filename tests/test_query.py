from euchre.del_string import del_string
from euchre.card import *
from euchre import *
import random
from euchre.bots.tools.Query import Query
import pytest

@pytest.fixture
def game():
    game = Game(['Player1', 'Player2', 'Player3', 'Player4'])
    random.seed(100)
    game.input(None, 'start', None)
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.set_cards('Player2', ['9♦', 'K♠', 'Q♣', 'K♦', '10♥'])    
    game.set_cards('Player3', ['9♠', 'Q♦', 'A♥', 'A♦', 'K♥'])
    game.set_cards('Player4', ['A♣', 'K♣', 'A♠', '10♦', '9♥'])      
    game.up_card = "10♠"
    return game

def test_raw(game):
    snap = Snapshot(game, 'Player1')
    q = Query().all(snap)
    assert q == []

def test_select_all(game):
    snap = Snapshot(game, 'Player1')
    q = Query()    
    q = q.select('~').all(snap)
    assert set(q) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

def test_select_all_trump_set(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    assert Query().select('~').all(snap) == ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥']


def test_select_no_trump_is_not_normalized(game):        
    snap = Snapshot(game, 'Player1')

    # spades and clubs will not return anything when trump is not set
    assert Query().select('J♠ J♣').all(snap) == []

    # hearts will return only hearts
    assert set(Query().select('♥').all(snap)) == set(['Q♥', 'J♥'])

def test_select_with_trump_is_normalized(game):   
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')     

    # there is no J♣, to properly get it it use L♠ when trump is set
    assert Query().select('J♠ J♣').all(snap) == ['J♦'] 

    # there is no J♣, to properly get it it use L♣
    assert Query().select('J♠ L♠').all(snap) == ['J♦', 'J♥'] 

    # spades will return all diamonds
    assert Query().select('♠').all(snap) == ['J♦', 'J♥']   

    # clubs will return only the Q♥
    assert Query().select('♣').all(snap) == ['Q♥'] 

    # L (left-bower) will return J♥ when trump is diamonds
    assert Query().select('L♠').all(snap) == ['J♥']  

    # L (left-bower) only works when selecting spades
    assert Query().select('L♣').all(snap) == []

    # Select left bower, suit is implied
    assert Query().select('L').all(snap) == ['J♥']

def test_select_not_trump_not_set(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = None
    snap = Snapshot(game, 'Player1')     

    # select everything except clubs
    assert Query().select('~♣').all(snap) == ['J♦', 'Q♥', 'Q♠', 'J♥']  

def test_select_not_trump_set(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')  

    # select everything except the opposite suit (no hearts) J♥ is not a heart
    assert Query().select('~♣').all(snap) == ['J♦', '10♣', 'Q♠', 'J♥']  

    # select everything except left bower
    assert Query().select('~L').all(snap) == ['J♦', '10♣', 'Q♥', 'Q♠']

def test_select_right_bower_trump_set(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')  

    assert Query().select('J♠').all(snap) == ['J♦']

def test_multi_select(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')  

    q = Query().select('J♠ Q')
    assert q.all(snap) == ['J♦', 'Q♥', 'Q♠']

def test_dealer_true(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').dealer('3').all(snap)
    assert set(q) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

def test_dealer_false(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').dealer('2').all(snap)
    assert set(q) == set([])

def test_maker_true(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.input('Player1', 'order')
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').maker('0').all(snap)
    assert set(q) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

def test_maker_false(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.input('Player1', 'order')
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').maker('2').all(snap)
    assert set(q) == set([])

def test_lead_true(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.input('Player1', 'order')
    game.input('Player4', 'down')
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').lead('0').all(snap)
    assert set(q) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

def test_lead_false(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.input('Player1', 'order')
    game.input('Player4', 'down')
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').lead('2').all(snap)
    assert set(q) == set([])

# this is to make sure that lead player is independent of the winning player
def test_lead_true_when_not_winning(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.set_cards('Player2', ['J♣', '10♠', 'Q♠', 'Q♣', 'J♠'])    
    game.input('Player1', 'order')
    game.input('Player4', 'down')
    game.input('Player1', 'play', 'Q♥')
    game.input('Player2', 'play', '10♠')

    snap = Snapshot(game, 'Player1')

    q = Query().select('~').lead('0').all(snap)
    assert set(q) == set(['J♦', '10♣', 'Q♠', 'J♥'])

def test_lead_different_order(game):
    game.order = [1, 2, 3, 0]
    game.input('Player2', 'order')
    game.input('Player1', 'down')
    snap = Snapshot(game, 'Player2')
    q = Query().select('~').lead("123")
    assert set(q.all(snap)) == set(['9♦', 'K♠', 'Q♣', 'K♦', '10♥'])

def test_lead_different_order_self_not_first(game):
    game.order = [1, 2, 3, 0]
    game.input('Player2', 'order')
    game.input('Player1', 'down')

    # the current lead is Player2, which is '1' in order
    # self is Player3/pindex-2
    # lead 2 means first player after self which is Player4/pindex-3

    snap = Snapshot(game, 'Player3')
    q = Query().select('~').lead("0")
    assert set(q.all(snap)) == set([])

def test_up_card_true(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = None
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').up_card('10♠')
    assert set(q.all(snap)) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

def test_up_card_false(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.trump = '♦'
    snap = Snapshot(game, 'Player1')
    q = Query().select('~')
    q._up_card.select('10♣')

    q = Query().select('~').up_card('10♣').all(snap)
    assert set(q) == set([])

def test_down_card_true(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.input('Player1', 'order')
    game.input('Player4', 'down')
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').down_card('10♠') # trump is ♠
    assert set(q.all(snap)) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

def test_down_card_false(game):
    game.set_cards('Player1', ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    game.input('Player1', 'order')
    game.input('Player4', 'down')
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').down_card('10♣') # trump is ♠
    assert set(q.all(snap)) == set([])
    
def test_beats(game):
    game.input('Player1', 'order')
    game.input('Player4', 'down')
    game.input('Player1', 'play', 'Q♥') # lead card
    game.input('Player2', 'play', '10♥')
    snap = Snapshot(game, 'Player3')

    q = Query().select('~').wins() # lead card
    assert set(q.all(snap)) == set(['9♠', 'A♥', 'K♥'])

def test_loses_to(game):
    game.input('Player1', 'order') # 'J♦', '10♣', 'Q♥', 'Q♠', 'J♥'
    game.input('Player4', 'down')  # '9♦', 'K♠', 'Q♣', 'K♦', '10♥'
    game.input('Player1', 'play', 'Q♥') 
    game.input('Player2', 'play', '10♥')
    snap = Snapshot(game, 'Player3') # '9♠', 'Q♦', 'A♥', 'A♦', 'K♥'

    q = Query().select('~').loses()
    assert set(q.all(snap)) == set(['Q♦', 'A♦'])    

def test_best(game):
    game.input('Player1', 'order') # 'J♦', '10♣', 'Q♥', 'Q♠', 'J♥'
    game.input('Player4', 'down')  # '9♦', 'K♠', 'Q♣', 'K♦', '10♥'
    game.trump = '♥'    
    game.input('Player1', 'play', 'Q♥') 
    game.input('Player2', 'play', '10♥')
    snap = Snapshot(game, 'Player3') # '9♠', 'Q♦', 'A♥', 'A♦', 'K♥'

    q = Query().select('~').best()
    assert set(q.all(snap)) == set(['A♥'])

def test_worst_0(game):
    game.input('Player1', 'order') # 'J♦', '10♣', 'Q♥', 'Q♠', 'J♥'
    game.input('Player4', 'down')  # '9♦', 'K♠', 'Q♣', 'K♦', '10♥'
    game.input('Player1', 'play', 'Q♥') 
    game.input('Player2', 'play', '10♥')
    game.trump = '♥'
    snap = Snapshot(game, 'Player3') # '9♠', 'Q♦', 'A♥', 'A♦', 'K♥'

    q = Query().select('~').worst()
    assert set(q.all(snap)) == set(['9♠'])         

def test_worst_1(game):
    game.input('Player1', 'order') # 'J♦', '10♣', 'Q♥', 'Q♠', 'J♥'
    game.input('Player4', 'down')  # '9♦', 'K♠', 'Q♣', 'K♦', '10♥'
    game.trump = '♠'
    game.input('Player1', 'play', 'Q♥') 
    game.input('Player2', 'play', '10♥')
    snap = Snapshot(game, 'Player3') # '9♠', 'Q♦', 'A♥', 'A♦', 'K♥'

    q = Query().select('~').worst()
    assert set(q.all(snap)) == set(['Q♦'])      


def test_playable_0(game):
    game.input('Player1', 'order') 
    game.input('Player4', 'down')  
    game.trump = '♠'
    snap = Snapshot(game, 'Player1') # 'J♦', '10♣', 'Q♥', 'Q♠', 'J♥'

    q = Query().select('~')
    assert set(q.playable().all(snap)) == set(['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])       

def test_playable_1(game):
    game.input('Player1', 'order') 
    game.input('Player4', 'down')  
    game.trump = '♠'
    game.input('Player1', 'play', 'Q♥') 
    snap = Snapshot(game, 'Player2') #'9♦', 'K♠', 'Q♣', 'K♦', '10♥'

    q = Query().select('~')
    assert set(q.playable().all(snap)) == set(['10♥'])
    
def test_select_all_opposite_suit(game):
    game.set_cards('Player1', ['J♦', 'J♥', 'A♦', 'A♥', 'Q♥', ])   
    game.trump = "♦"
    snap = Snapshot(game, 'Player1')
    q = Query().select('♣')
    assert set(q.all(snap)) == set(['A♥', 'Q♥'])

def test_select_all_trump(game):
    game.set_cards('Player1', ['J♦', 'J♥', 'A♦', 'A♥', 'Q♥', ])   
    game.trump = "♦"
    snap = Snapshot(game, 'Player1')
    q = Query().select('♠')
    assert set(q.all(snap)) == set(['J♦', 'J♥', 'A♦'])

def test_jack_opposite_doesnt_exist(game):
    game.set_cards('Player1', ['J♦', 'J♥', 'A♦', 'A♥', 'Q♥', ])   
    game.trump = "♦"
    snap = Snapshot(game, 'Player1')
    q = Query().select('J♣')
    assert set(q.all(snap)) == set([])

def test_down_card_select_trump(game):
    game.set_cards('Player1', ['10♦', 'J♥', 'A♦', 'A♥', 'Q♥'])   
    game.trump = "♦"
    game.down_card = 'J♦'
    snap = Snapshot(game, 'Player1')
    q = Query().select('~').down_card("♠")
    (q.all(snap))
    assert set(q.all(snap)) == set(['10♦', 'J♥', 'A♦', 'A♥', 'Q♥'])    

def test_down_card_select_trump_down_is_LB(game):
    game.set_cards('Player1', ['J♦', '10♥', 'A♦', 'A♥', 'Q♥'])   
    game.trump = "♦"
    game.down_card = 'J♥'
    snap = Snapshot(game, 'Player1')
    q = Query().select('~').down_card("♠")
    assert set(q.all(snap)) == set(['J♦', '10♥', 'A♦', 'A♥', 'Q♥'])      

def test_down_card_select_opp_down_is_LB(game):
    game.set_cards('Player1', ['J♦', '10♥', 'A♦', 'A♥', 'Q♥'])   
    game.trump = "♦"
    game.down_card = 'J♥'
    snap = Snapshot(game, 'Player1')

    q = Query().select('~').down_card("♣")
    
    assert set(q.all(snap)) == set([])           

def test_down_card_is_LB_select_all(game):
    game.set_cards('Player1', ['J♦', '10♥', 'A♦', 'A♥', 'Q♥'])   
    game.trump = "♦"
    game.down_card = 'J♥'
    snap = Snapshot(game, 'Player1')

    q = Query().select('~')
    
    assert set(q.all(snap)) == set(['J♦', '10♥', 'A♦', 'A♥', 'Q♥'])      

def test_worst_card_with_loses_and_beats(game):
    game.state = game.state_5
    game.set_cards('Player1', ['10♣', 'Q♣', '9♣', '10♥', 'Q♠'])   
    game.trump = "♠"
    game.up_card = None
    game.down_card = 'K♦'
    game.order = [1, 2, 3, 0]

    game.current_player_index = 0
    game._tricks = []
    game._tricks.append(Trick("♠", game.order, ["K♥","Q♥","A♥"]))
    snap = Snapshot(game, 'Player1')
    print(snap)
    
    q1 = Query("~", "beats").lead("123").wins().worst()
    assert q1.all(snap)[0] == "Q♠"

    q2 = Query("~", "loses").lead("123").loses().worst()
    assert q2.all(snap)[0] == "9♣"

def test_playable(game):
    game.state = game.state_5
    game.set_cards('Player1', ['10♣', 'Q♣', '9♣', '10♥', 'Q♠'])   
    game.trump = "♠"
    game.up_card = None
    game.down_card = 'K♦'
    game.order = [1, 2, 3, 0]

    game.current_player_index = 0
    game._tricks = []
    game._tricks.append(Trick("♠", game.order, ["K♥","Q♥","A♥"]))
    snap = Snapshot(game, 'Player1')
    print(snap)
    
    q1 = Query("~", "beats").lead("123").playable().wins().worst()
    assert len(q1.all(snap)) == 0

    q2 = Query("~", "loses").lead("123").playable().loses().worst()
    assert q2.all(snap)[0] == "10♥"