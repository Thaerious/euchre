import unittest
from euchre.delString import delString

class TestDelString(unittest.TestCase):
    def test_three_items(this):
        aList = ["apple", "banana", "carrot"]
        actual = delString(aList)
        expected = "apple, banana, carrot"
        print(actual)
        this.assertEqual(actual, expected)

    def test_one_item(this):
        aList = ["apple"]
        actual = delString(aList)
        expected = "apple"
        print(actual)
        this.assertEqual(actual, expected)        

    def test_no_items(this):
        aList = []
        actual = delString(aList)
        expected = ""
        print(actual)
        this.assertEqual(actual, expected)            

    def test_no_deliter(this):
        aList = ["apple", "banana", "carrot"]
        actual = delString(aList, "")
        expected = "applebananacarrot"
        print(actual)
        this.assertEqual(actual, expected)

    def test_custom_deliter(this):
        aList = ["apple", "banana", "carrot"]
        actual = delString(aList, "-")
        expected = "apple-banana-carrot"
        print(actual)
        this.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()            