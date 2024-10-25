import unittest
from bots.Bot import randomItem, playableCards, canPlay

class TestBot(unittest.TestCase):
    def test_randomItemEmpty(this):
        items = []
        item = randomItem(items)
        this.assertEqual(item, None)

    def test_randomItem(this):
        items = [1, 3, 5, 8]
        item = randomItem(items)
        this.assertTrue(item in items)

    def test_canplay0(this):
        snap = {
            'cards': ['Q♣', '10♥', '10♠', 'Q♥', 'K♦'],
            'trump': '♥',
            'trick': []
        }

        actual = canPlay('Q♣', snap)
        this.assertEqual(actual, True)

    def test_canplay_must_follow_suit(this):
        snap = {
            'cards': ['Q♣', '10♥', '10♠', 'Q♥', 'K♦'],
            'trump': '♥',
            'trick': ['10♣']
        }

        actual = canPlay('10♥', snap)
        this.assertEqual(actual, False)        

    def test_canplay_left_bower_must_follow(this):
        snap = {
            'cards': ['J♥', '10♥', '10♣', 'Q♥', 'K♦'],
            'trump': '♦',
            'trick': ['9♣']
        }

        actual = canPlay('J♥', snap)
        this.assertEqual(actual, False)  

    def test_canplay_left_bower_no_lead_suit(this):
        snap = {
            'cards': ['J♥', '10♥', '10♦', 'Q♥', 'K♦'],
            'trump': '♦',
            'trick': ['9♣']
        }

        actual = canPlay('J♥', snap)
        this.assertEqual(actual, True)  

    def test_playable(this):
        snap = {
            'cards': ['Q♣', '10♥', '10♠', 'Q♥', 'K♦'],
            'trump': '♥',
            'trick': []
        }

        cards = playableCards(snap)
        this.assertEqual(len(cards), 5)

if __name__ == '__main__':
    unittest.main()    