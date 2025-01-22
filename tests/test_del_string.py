import unittest
from euchre.del_string import del_string

class Testdel_string(unittest.TestCase):
    def test_three_items(this):
        aList = ["apple", "banana", "carrot"]
        actual = del_string(aList)
        expected = "apple, banana, carrot"
        this.assertEqual(actual, expected)

    def test_one_item(this):
        aList = ["apple"]
        actual = del_string(aList)
        expected = "apple"
        this.assertEqual(actual, expected)        

    def test_no_items(this):
        aList = []
        actual = del_string(aList)
        expected = ""
        this.assertEqual(actual, expected)            

    def test_no_deliter(this):
        aList = ["apple", "banana", "carrot"]
        actual = del_string(aList, "")
        expected = "applebananacarrot"
        this.assertEqual(actual, expected)

    def test_custom_deliter(this):
        aList = ["apple", "banana", "carrot"]
        actual = del_string(aList, "-")
        expected = "apple-banana-carrot"
        this.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()            