import unittest
from types import SimpleNamespace
from euchre.bots.evals.CountSuitInHand import CountSuitInHand
from euchre.bots.evals.CountTrumpInHand import CountTrumpInHand
from euchre.Card import Hand

class TestCountSuitInHand(unittest.TestCase):
    def test_count_suits_false(this):
        snap = SimpleNamespace()
        snap.cards = Hand(["9♣", "K♣", "Q♥", "Q♣"])

        rulePart = CountSuitInHand()
        rulePart.genotype["suit"] = "♠"
        rulePart.genotype["operator"] = "="
        rulePart.genotype["count"] = 3

        this.assertFalse(rulePart.evaluate(snap))
   
    def test_count_suits_true(this):
        snap = SimpleNamespace()
        snap.cards = Hand(["9♣", "K♣", "Q♠", "Q♣"])

        rulePart = CountSuitInHand()
        rulePart.genotype["suit"] = "♣"
        rulePart.genotype["operator"] = "="
        rulePart.genotype["count"] = 3

        this.assertTrue(rulePart.evaluate(snap))

class TestCountTrumpInHand(unittest.TestCase):
    def test_count_suits_false(this):
        snap = SimpleNamespace()
        snap.cards = Hand(["9♣", "K♣", "Q♥", "Q♣"])
        snap.trump = "♥"

        rulePart = CountTrumpInHand()
        rulePart.genotype["operator"] = "="
        rulePart.genotype["count"] = 3

        this.assertFalse(rulePart.evaluate(snap))
   
    def test_count_suits_true(this):
        snap = SimpleNamespace()
        snap.cards = Hand(["9♣", "K♣", "Q♥", "Q♣"])
        snap.trump = "♥"

        rulePart = CountTrumpInHand()
        rulePart.genotype["operator"] = "="
        rulePart.genotype["count"] = 1

        this.assertTrue(rulePart.evaluate(snap))

if __name__ == '__main__':
    unittest.main()            