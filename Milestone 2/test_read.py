import unittest
from UVSim import read, words

class TestReadFunction(unittest.TestCase):

    def setUp(self):
        global words
        words = [""] * 100
        words[5] = "test_word"

    def test_read_valid_location(self):
        result = read(5, words)
        self.assertEqual(result, "test_word")

    def test_read_empty_location(self):
        # Test reading from an empty location
        result = read(10, words)
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()
