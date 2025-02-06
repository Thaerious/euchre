from euchre.del_string import del_string
from euchre.card import *
from euchre import *
import random
from euchre.bots.tools.Query import Query
import pytest

def build_hand(cards, trump):     
    deck = Deck()
    deck.trump = trump
    hand = Hand()

    for card in cards:
        if isinstance(card, Card):
            hand.append(card)
        else:
            hand.append(deck.get_card(card))

    return (deck, hand)

def set_hand(snapshot, cards):
    deck = snapshot.hand[0].deck
    snapshot.hand.clear()
    for card in cards:
        snapshot.hand.append(deck.get_card(card))

@pytest.fixture
def snapshot():
    game = Game(["Player1", "Player2", "Player3", "Player4"])
    random.seed(100)
    game.input(None, 'start', None)
    return Snapshot(game, "Player1") # ['J♦', '10♣', '9♣', 'Q♥', 'Q♠']

@pytest.fixture
def game():
    game = Game(["Player1", "Player2", "Player3", "Player4"])
    random.seed(100)
    game.input(None, 'start', None)
    return game

def test_raw(snapshot):
    q = Query(snapshot)
    assert q == ['J♦', '10♣', '9♣', 'Q♥', 'Q♠']

def test_select_all(snapshot):
    q = Query(snapshot)    
    q = q.select("910JQKA♠♥♣♦")
    assert q == ['9♣', '10♣', 'J♦', 'Q♠', 'Q♥']

def test_select_no_trump_is_not_normalized(snapshot):    
    set_hand(snapshot, ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

    # spades and clubs will not return anything when trump is not set
    assert Query(snapshot).select("J♠ J♣").len == 0

    # hearts will return only hearts
    assert Query(snapshot).select("♥") == ['Q♥', 'J♥']

def test_select_with_trump_is_normalized(snapshot):    
    set_hand(snapshot, ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    snapshot.trump = '♦'

    # spades and clubs will now return diamods and hearts
    assert Query(snapshot).select("J♠ J♣") == ['J♦', 'J♥'] 

    # spades will return all diamonds
    assert Query(snapshot).select("♠") == ['J♦', 'J♥']   

    # L (left-bower) will return J♥ when trump is diamonds
    assert Query(snapshot).select("L♠") == ['J♥']  

    # L (left-bower) only works when selecing spades
    assert Query(snapshot).select("L♣") == []

    # Select left bower, suit is implied
    assert Query(snapshot).select("L") == ['J♥']

def test_select_not_trump_not_set(snapshot):
    set_hand(snapshot, ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])

    # select everything except clubs
    assert Query(snapshot).select("~♣") == ['J♦', 'Q♥', 'Q♠', 'J♥']  

def test_select_not_trump_set(snapshot):
    set_hand(snapshot, ['J♦', '10♣', 'Q♥', 'Q♠', 'J♥'])
    snapshot.trump = '♦'

    # select everything except the opposite suit (no hearts)
    assert Query(snapshot).select("~♣") == ['J♦', '10♣', 'Q♠', 'J♥']  

    # select everything except left bower
    assert Query(snapshot).select("~L") == ['J♦', '10♣', 'Q♥', 'Q♠']       

def test_multi_select(snapshot):
    q = Query(snapshot).select("910JQKA♠♥♣♦")
    assert q.select('9♣') == ['9♣']

def test_has_doesnt_clear_on_true(snapshot):
    q = Query(snapshot).select("910JQKA♠♥♣♦")
    assert q.has('9♣') == ['9♣', '10♣', 'J♦', 'Q♠', 'Q♥']

def test_has_clears_on_false(snapshot):
    q = Query(snapshot).select("910JQKA♠♥♣♦")
    assert q.has('J♣') == []

def test_dealer_true(snapshot):
    q = Query(snapshot).select("910JQKA♠♥♣♦").dealer("3")
    assert q == ['9♣', '10♣', 'J♦', 'Q♠', 'Q♥']

def test_dealer_false(snapshot):
    q = Query(snapshot).select("910JQKA♠♥♣♦").dealer("2")
    assert q == []    

def test_maker_false_when_none(snapshot):
    q = Query(snapshot).select("910JQKA♠♥♣♦").maker("0")
    assert q == []    

def test_has_doesnt_refine(snapshot):
    q = Query(snapshot).select("910JQKA♠♥♣♦").maker("0")
    assert q == []    

# for_player = 0
# maker = 0
def test_maker_true(snapshot):
    set_hand(snapshot, ['J♦', '10♣', '9♣', 'Q♥', 'Q♠'])
    snapshot.trump = '♦'
    snapshot.maker = 0
    q = Query(snapshot).maker("0")
    assert q == ['J♦', '10♣', '9♣', 'Q♥', 'Q♠']   

def test_down_true(snapshot):
    set_hand(snapshot, ['J♦', '10♣', '9♣', 'Q♥', 'Q♠'])
    snapshot.trump = None
    snapshot.maker = 0
    snapshot.down_card = snapshot.hand[0]._source.get_card("K♦") # breaking the interface todo fix
    
    q = Query(snapshot).down("K♦") 
    assert q == ['J♦', '10♣', '9♣', 'Q♥', 'Q♠']

def test_down_false(snapshot):
    set_hand(snapshot, ['J♦', '10♣', '9♣', 'Q♥', 'Q♠'])
    snapshot.trump = None
    snapshot.maker = 0
    snapshot.down_card = snapshot.hand[0]._source.get_card("K♦")# breaking the interface todo fix
    
    q = Query(snapshot).down("A♦") 
    assert q == []

# @pytest.mark.parametrize("hand, trump, phrase, expected", [
#     (['J♦', '10♣', '9♣', 'Q♥', 'Q♠'], "♠", "910♠♥♣♦", ["9♣", "10♣"]), # specified values, trump doesn't matter
#     (['J♦', '10♣', '9♣', 'Q♥', 'Q♠'], "♥", "910♠♥♣♦", ["9♣", "10♣"]), # specified values, trump doesn't matter    
#     (['J♦', '10♣', '9♣', 'Q♥', 'Q♠'], "♥", "910QKALJ♠", ["Q♥", "J♦"]), # all trump when trump is ♥    
# ])
# def test_select(snapshot, hand, trump, phrase, expected):
#     set_hand(snapshot, hand)
#     snapshot.trump = trump
#     assert Query(snapshot).select(phrase) == expected

def test_playable_0(game):
    game.input("Player1", "order", None) # J♦, 10♣, 9♣, Q♥, Q♠ trump ♥
    game.input("Player4", "down", None)
    snapshot = Snapshot(game, "Player1")
    assert Query(snapshot).playable().len == 5

def test_playable_1(game):
    test_playable_0(game)
    game.input("Player1", "play", "Q♠")
    snapshot = Snapshot(game, "Player2") # 9♦, K♥, Q♣, K♦, 10♠
    assert Query(snapshot).playable() == ['10♠']

def test_playable_left_bower_not_playable(game):
    # add the A♦ to the first player 
    card = game.deck.get_card("A♦")
    game.get_player("Player1").cards.append(card)

    # add the J♦ to the second player
    card = game.deck.get_card("J♦")
    game.get_player("Player2").cards.append(card)

    # play the game until after first card played
    game.input("Player1", "order", None)
    game.input("Player4", "down", None)
    game.input("Player1", "play", "A♦")

    snapshot = Snapshot(game, "Player2") # 9♦, K♥, Q♣, K♦, 10♠, J♦

    # only the 9♦ & K♦ are playable because the J♦ is trump
    assert Query(snapshot).playable() == ['9♦', 'K♦']

def test_select_not_suit(game):
    game.set_cards("Player1", ["Q♥", "10♦", "K♠", "10♠", "J♦"])
    snapshot = Snapshot(game, "Player1")
    q = Query(snapshot).select("~♠")
    assert "K♠" not in q
    assert "10♠" not in q
    
def test_beats(game):
    game.set_cards("Player1", ["Q♥", "10♦", "K♠", "10♠", "J♦"])
    game.trump = "♦"
    snapshot = Snapshot(game, "Player1")
    q = Query(snapshot).beats(game.deck.get_card("10♥"))
    assert q == ["Q♥", "10♦", "J♦"]
