from euchre.del_string import del_string
from euchre.card import *
from euchre import *
import random
from euchre.bots.tools.Query import Query, expand_query
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

def test_expand_cards_whole_deck():    
    cards = expand_query("910JQKA♠♣♦♥", False)
    assert cards == ['9♠', '9♣', '9♦', '9♥', '10♠', '10♣', '10♦', '10♥', 'J♠', 'J♣', 'J♦', 'J♥', 'Q♠', 'Q♣', 'Q♦', 'Q♥', 'K♠', 'K♣', 'K♦', 'K♥', 'A♠', 'A♣', 'A♦', 'A♥']

def test_expand_cards_partial():    
    cards = expand_query("910♦♥")
    assert cards == ['9♦', '9♥', '10♦', '10♥']

def test_expand_order_matters_1():    
    cards = expand_query("109♥♦")
    assert cards == ['10♥', '10♦', '9♥', '9♦']

def test_expand_order_matters_2():    
    cards = expand_query("♥109♦")
    assert cards == ['10♥', '9♥', '10♦', '9♦']    

def test_expand_ignore_repeats():    
    cards = expand_query("910♦910♦")
    assert cards == ['9♦', '10♦']

def test_expand_and():    
    cards = expand_query("910♦ 9♣")
    assert cards == ['9♦', '10♦', '9♣']    

def test_expand_left_bower_wont_select():    
    cards = expand_query("910L♦")
    assert cards == ['9♦', '10♦']

def test_expand_left_bower_will_select():    
    cards = expand_query("910L♠")
    assert cards == ['9♠', '10♠', 'J♣']    

def test_invert():
    cards = expand_query("~♣♠")
    print(f"the returned cards {cards}")
    assert set(cards) == set(['9♥', '9♦', '10♥', '10♦', 'J♥', 'J♦', 'Q♥', 'Q♦', 'K♥', 'K♦', 'A♥', 'A♦'])

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
    q = Query(snapshot).select("910JQKA♠♥♣♦")
    assert q == ['9♣', '10♣', 'J♦', 'Q♠', 'Q♥']

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

def test_maker_true(snapshot):
    game = Game(["Player1", "Player2", "Player3", "Player4"])
    random.seed(100)
    game.input(None, 'start', None)
    game.input("Player1", "order", None)
    snapshot = Snapshot(game, "Player1") # ['J♦', '10♣', '9♣', 'Q♥', 'Q♠']
    q = Query(snapshot).select("910JQKAL♠♥♣♦").maker("0")

    print(q)
    assert q == ['9♣', '10♣', 'Q♥', 'Q♠', 'J♦']   

def test_down_true(snapshot):
    game = Game(["Player1", "Player2", "Player3", "Player4"])
    random.seed(100)

    game.input(None, 'start', None)
    game.input("Player1", "pass", None)
    game.input("Player2", "pass", None)
    game.input("Player3", "pass", None)
    game.input("Player4", "pass", None)    
    
    snapshot = Snapshot(game, "Player1") # ['J♦', '10♣', '9♣', 'Q♥', 'Q♠']
    q = Query(snapshot).down("910JQKA♠♥♣")
    assert q == ['J♦', '10♣', '9♣', 'Q♥', 'Q♠']   

def test_down_false(snapshot):
    game = Game(["Player1", "Player2", "Player3", "Player4"])
    random.seed(100)

    game.input(None, 'start', None)
    game.input("Player1", "pass", None)
    game.input("Player2", "pass", None)
    game.input("Player3", "pass", None)
    game.input("Player4", "pass", None)    
    
    snapshot = Snapshot(game, "Player1") # ['J♦', '10♣', '9♣', 'Q♥', 'Q♠']
    q = Query(snapshot).down("910JQKA♠♣♦")
    assert q == []   

@pytest.mark.parametrize("trump, phrase, expected", [
    ("♠", "910♠♥♣♦", ["9♣", "10♣"]), # specified values, trump doesn't matter
    ("♥", "910♠♥♣♦", ["9♣", "10♣"]), # specified values, trump doesn't matter    
    ("♥", "910QKALJ♠", ["Q♥", "J♦"]), # all trump when trump is ♥    
])
def test_select(snapshot, trump, phrase, expected):
    q = Query(snapshot, trump).select(phrase)
    assert q == expected

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
    game.get_player("Player2").cards.append("J♦")

    # play the game until after first card played
    game.input("Player1", "order", None)
    game.input("Player4", "down", None)
    game.input("Player1", "play", "A♦")

    snapshot = Snapshot(game, "Player2") # 9♦, K♥, Q♣, K♦, 10♠, J♦

    # only the 9♦ & K♦ are playable because the J♦ is trump
    assert Query(snapshot).playable() == ['9♦', 'K♦']
