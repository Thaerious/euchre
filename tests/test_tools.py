import unittest
import pytest
from euchre.bots.tools import *
from euchre.card.Card import *

# can_play(trump, trick, hand, _card) : {true, false}
def test_can_play():
    result = can_play("♠", Trick(["9♠"]), Hand(["10♠", "A♠", "10♣", "Q♠"]), Card("10♠"))
    assert result == True

def test_playable():
    result = playable("♠", Trick(["9♠"]), Hand(["10♠", "A♠", "10♣", "Q♠"]))
    print(result)
    assert len(result) == 3