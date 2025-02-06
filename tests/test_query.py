from euchre.del_string import del_string
from euchre.card import *
from euchre import *
import random
from euchre.bots.tools.Query import Query
import pytest

@pytest.fixture
def game():
    game = Game(["Player1", "Player2", "Player3", "Player4"])
    random.seed(100)
    game.input(None, 'start', None)
    return game

def test_raw(game):
    snap = Snapshot(game, "Player1")
    q = Query().all(snap)
    assert q == []

def test_select_all(game):
    snap = Snapshot(game, "Player1")
    q = Query()    
    q = q.select("~").all(snap)
    assert set(q) == set(['9♣', '10♣', 'J♦', 'Q♠', 'Q♥'])

def test_select_no_trump_is_not_normalized(game):    
    game.set_cards("Player1", ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    snap = Snapshot(game, "Player1")

    # spades and clubs will not return anything when trump is not set
    assert Query().select("J♠ J♣").all(snap) == []

    # hearts will return only hearts
    assert Query().select("♥").all(snap) == ['Q♥', 'J♥']

# def test_select_with_trump_is_normalized(game):    
#     set_hand(snap, ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
#     snap.trump = '♦'

#     # spades and clubs will now return diamods and hearts
#     assert Query(snap).select("J♠ J♣") == ['J♦', 'J♥'] 

#     # spades will return all diamonds
#     assert Query(snap).select("♠") == ['J♦', 'J♥']   

#     # L (left-bower) will return J♥ when trump is diamonds
#     assert Query(snap).select("L♠") == ['J♥']  

#     # L (left-bower) only works when selecing spades
#     assert Query(snap).select("L♣") == []

#     # Select left bower, suit is implied
#     assert Query(snap).select("L") == ['J♥']

# def test_select_not_trump_not_set(game):
#     set_hand(snap, ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

#     # select everything except clubs
#     assert Query(snap).select("~♣") == ['J♦', 'Q♥', 'Q♠', 'J♥']  

# def test_select_not_trump_set(game):
#     set_hand(snap, ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
#     snap.trump = '♦'

#     # select everything except the opposite suit (no hearts)
#     assert Query(snap).select("~♣") == ['J♦', '10♣', 'Q♠', 'J♥']  

#     # select everything except left bower
#     assert Query(snap).select("~L") == ['J♦', '10♣', 'Q♥', 'Q♠']       

# def test_multi_select(game):
#     q = Query(snap).select("910JQKA♠♥♣♦")
#     assert q.select('9♣') == ['9♣']

# def test_has_doesnt_clear_on_true(game):
#     q = Query(snap).select("910JQKA♠♥♣♦")
#     assert q.has('9♣') == ['9♣', '10♣', 'J♦', 'Q♠', 'Q♥']

# def test_has_clears_on_false(game):
#     q = Query(snap).select("910JQKA♠♥♣♦")
#     assert q.has('J♣') == []

# def test_dealer_true(game):
#     q = Query(snap).select("910JQKA♠♥♣♦").dealer("3")
#     assert q == ['9♣', '10♣', 'J♦', 'Q♠', 'Q♥']

# def test_dealer_false(game):
#     q = Query(snap).select("910JQKA♠♥♣♦").dealer("2")
#     assert q == []    

# def test_maker_false_when_none(game):
#     q = Query(snap).select("910JQKA♠♥♣♦").maker("0")
#     assert q == []    

# def test_has_doesnt_refine(game):
#     q = Query(snap).select("910JQKA♠♥♣♦").maker("0")
#     assert q == []    

# # for_player = 0
# # maker = 0
# def test_maker_true(game):
#     set_hand(snap, ['J♦', '10♣', '9♣', 'Q♥', 'Q♠'])
#     snap.trump = '♦'
#     snap.maker = 0
#     q = Query(snap).maker("0")
#     assert q == ['J♦', '10♣', '9♣', 'Q♥', 'Q♠']   

# def test_down_true(game):
#     set_hand(snap, ['J♦', '10♣', '9♣', 'Q♥', 'Q♠'])
#     snap.trump = None
#     snap.maker = 0
#     snap.down_card = snap.hand[0]._source.get_card("K♦") # breaking the interface todo fix
    
#     q = Query(snap).down("K♦") 
#     assert q == ['J♦', '10♣', '9♣', 'Q♥', 'Q♠']

# def test_down_false(game):
#     set_hand(snap, ['J♦', '10♣', '9♣', 'Q♥', 'Q♠'])
#     snap.trump = None
#     snap.maker = 0
#     snap.down_card = snap.hand[0]._source.get_card("K♦")# breaking the interface todo fix
    
#     q = Query(snap).down("A♦") 
#     assert q == []

# # @pytest.mark.parametrize("hand, trump, phrase, expected", [
# #     (['J♦', '10♣', '9♣', 'Q♥', 'Q♠'], "♠", "910♠♥♣♦", ["9♣", "10♣"]), # specified values, trump doesn't matter
# #     (['J♦', '10♣', '9♣', 'Q♥', 'Q♠'], "♥", "910♠♥♣♦", ["9♣", "10♣"]), # specified values, trump doesn't matter    
# #     (['J♦', '10♣', '9♣', 'Q♥', 'Q♠'], "♥", "910QKALJ♠", ["Q♥", "J♦"]), # all trump when trump is ♥    
# # ])
# # def test_select(snap, hand, trump, phrase, expected):
# #     set_hand(snap, hand)
# #     snap.trump = trump
# #     assert Query(snap).select(phrase) == expected

# def test_playable_0(game):
#     game.input("Player1", "order", None) # J♦, 10♣, 9♣, Q♥, Q♠ trump ♥
#     game.input("Player4", "down", None)
#     snap = Snapshot(game, "Player1")
#     assert Query(snap).playable().len == 5

# def test_playable_1(game):
#     test_playable_0(game)
#     game.input("Player1", "play", "Q♠")
#     snap = Snapshot(game, "Player2") # 9♦, K♥, Q♣, K♦, 10♠
#     assert Query(snap).playable() == ['10♠']

# def test_playable_left_bower_not_playable(game):
#     # add the A♦ to the first player 
#     card = game.deck.get_card("A♦")
#     game.get_player("Player1").cards.append(card)

#     # add the J♦ to the second player
#     card = game.deck.get_card("J♦")
#     game.get_player("Player2").cards.append(card)

#     # play the game until after first card played
#     game.input("Player1", "order", None)
#     game.input("Player4", "down", None)
#     game.input("Player1", "play", "A♦")

#     snap = Snapshot(game, "Player2") # 9♦, K♥, Q♣, K♦, 10♠, J♦

#     # only the 9♦ & K♦ are playable because the J♦ is trump
#     assert Query(snap).playable() == ['9♦', 'K♦']

# def test_select_not_suit(game):
#     game.set_cards("Player1", ["Q♥", "10♦", "K♠", "10♠", "J♦"])
#     snap = Snapshot(game, "Player1")
#     q = Query(snap).select("~♠")
#     assert "K♠" not in q
#     assert "10♠" not in q
    
# def test_beats(game):
#     game.set_cards("Player1", ["Q♥", "10♦", "K♠", "10♠", "J♦"])
#     game.trump = "♦"
#     snap = Snapshot(game, "Player1")
#     q = Query(snap).beats(game.deck.get_card("10♥"))
#     assert q == ["Q♥", "10♦", "J♦"]
