import unittest
from Card import Card

class TestCard(unittest.TestCase):
    def test_equality_card_object_true(this):
        card0 = Card("♠", "10")
        card1 = Card("♠", "10")
        this.assertEqual(card0, card1)  
    
    def test_equality_string_true(this):
        card0 = Card("♠", "10")
        this.assertEqual(card0, "10♠")      

    def test_equality_card_object_false(this):
        card0 = Card("♠", "10")
        card1 = Card("♠", "9")
        this.assertNotEqual(card0, card1)  
    
    def test_equality_string_false(this):
        card0 = Card("♠", "10")
        this.assertNotEqual(card0, "9♠")      

if __name__ == '__main__':
    unittest.main()    