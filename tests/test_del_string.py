# test_del_string.py
import unittest

from euchre.del_string import del_string


class TestDelString(unittest.TestCase):
    def test_three_items(self):
        a_list = ["apple", "banana", "carrot"]
        actual = del_string(a_list)
        expected = "apple, banana, carrot"
        self.assertEqual(actual, expected)

    def test_one_item(self):
        a_list = ["apple"]
        actual = del_string(a_list)
        expected = "apple"
        self.assertEqual(actual, expected)

    def test_no_items(self):
        a_list = []
        actual = del_string(a_list)
        expected = ""
        self.assertEqual(actual, expected)

    def test_no_deliter(self):
        a_list = ["apple", "banana", "carrot"]
        actual = del_string(a_list, "")
        expected = "applebananacarrot"
        self.assertEqual(actual, expected)

    def test_custom_deliter(self):
        a_list = ["apple", "banana", "carrot"]
        actual = del_string(a_list, "-")
        expected = "apple-banana-carrot"
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
