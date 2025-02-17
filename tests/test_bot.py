from euchre.del_string import del_string
from euchre.card import *
from euchre import *
import random
from euchre.bots.tools.Query import Query
import pytest
from euchre.bots.Bot_0 import Bot_0

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

def test_query_simple(game):
    snap = Snapshot(game, 'Player1')
    bot = Bot_0()

    q = Query("♣").do("order")

    bot.append({
        "state_1" : [
            q
        ]
    })

    (action, data) = bot.decide(snap)
    assert q.stats.call_count == 1
    assert q.stats.activated == 1

def test_query_and_both_true(game):
    snap = Snapshot(game, 'Player1')
    bot = Bot_0()

    queries = {
        "state_1" : [
            Query("J♥").do("and"),
            Query("J♦").do("order"),
            Query("~").do("order")
        ]
    }

    bot.append(queries)

    (action, data) = bot.decide(snap)
    assert queries["state_1"][0].stats.activated == 1
    assert queries["state_1"][1].stats.activated == 1
    assert queries["state_1"][2].stats.activated == 0     

def test_query_and_premise_false_consequent_true(game):
    snap = Snapshot(game, 'Player1')
    bot = Bot_0()

    queries = {
        "state_1" : [
            Query("A♥").do("and"),
            Query("J♦").do("order"),
            Query("~").do("order")
        ]
    }

    bot.append(queries)

    (action, data) = bot.decide(snap)
    assert queries["state_1"][0].stats.activated == 0
    assert queries["state_1"][1].stats.activated == 0    
    assert queries["state_1"][2].stats.activated == 1   

def test_query_and_premise_true_consequent_false(game):
    snap = Snapshot(game, 'Player1')
    bot = Bot_0()

    queries = {
        "state_1" : [
            Query("J♦").do("and"),
            Query("A♥").do("order"),
            Query("~").do("order")
        ]
    }

    bot.append(queries)

    (action, data) = bot.decide(snap)
    assert queries["state_1"][0].stats.activated == 1
    assert queries["state_1"][1].stats.activated == 0      
    assert queries["state_1"][2].stats.activated == 1  

def test_count_if_true(game):
    snap = Snapshot(game, 'Player4') # ['A♣', 'K♣', 'A♠', '10♦', '9♥']
    bot = Bot_0()

    queries = {
        "state_1" : [
            Query("A♣").do("and"),
            Query("♣").count("2").do("order"),
            Query("~").do("order")
        ]
    }

    bot.append(queries)

    (action, data) = bot.decide(snap)
    assert queries["state_1"][0].stats.activated == 1
    assert queries["state_1"][1].stats.activated == 1      
    assert queries["state_1"][2].stats.activated == 0 

def test_count_if_false(game):
    snap = Snapshot(game, 'Player4') # ['A♣', 'K♣', 'A♠', '10♦', '9♥']
    bot = Bot_0()

    queries = {
        "state_1" : [
            Query("Q♣").do("and"),
            Query("♣").count("2").do("order"),
            Query("~").do("order")
        ]
    }

    bot.append(queries)

    (action, data) = bot.decide(snap)
    assert queries["state_1"][0].stats.activated == 0
    assert queries["state_1"][1].stats.activated == 0      
    assert queries["state_1"][2].stats.activated == 1     

def test_chain_and_true(game):
    snap = Snapshot(game, 'Player4') # ['A♣', 'K♣', 'A♠', '10♦', '9♥']
    bot = Bot_0()

    queries = {
        "state_1" : [
            Query("A♣").do("and"),
            Query("K♣").do("and"),
            Query("A♠").do("order"),
            Query("~").do("order")
        ]
    }

    bot.append(queries)

    (action, data) = bot.decide(snap)
    assert queries["state_1"][0].stats.activated == 1
    assert queries["state_1"][1].stats.activated == 1      
    assert queries["state_1"][2].stats.activated == 1  
    assert queries["state_1"][3].stats.activated == 0   

def test_chain_and_false_1(game):
    snap = Snapshot(game, 'Player4') # ['A♣', 'K♣', 'A♠', '10♦', '9♥']
    bot = Bot_0()

    queries = {
        "state_1" : [
            Query("9♣").do("and"),
            Query("K♣").do("and"),
            Query("A♠").do("order"),
            Query("~").do("order")
        ]
    }

    bot.append(queries)

    (action, data) = bot.decide(snap)
    assert queries["state_1"][0].stats.activated == 0
    assert queries["state_1"][1].stats.activated == 0      
    assert queries["state_1"][2].stats.activated == 0  
    assert queries["state_1"][3].stats.activated == 1       