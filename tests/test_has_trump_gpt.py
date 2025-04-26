# test_has_trump.py
import pytest
from euchre.card import HasTrump

def test_initial_trump_none():
    ht = HasTrump()
    assert ht.trump is None

def test_set_valid_trump():
    ht = HasTrump()
    for suit in ["♠", "♥", "♣", "♦"]:
        ht.trump = suit
        assert ht.trump == suit

def test_clear_trump():
    ht = HasTrump()
    ht.trump = "♠"
    ht.trump = None
    assert ht.trump is None

def test_set_invalid_trump():
    ht = HasTrump()
    with pytest.raises(ValueError):
        ht.trump = "X"

def test_set_empty_string_trump():
    ht = HasTrump()
    with pytest.raises(ValueError):
        ht.trump = ""
