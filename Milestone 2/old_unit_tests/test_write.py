import unittest
from UVSim import write, words

class TestWriteFunction(unittest.TestCase):

    def setUp(self):
        global words
        words = [""] * 100
        words[5] = "test_word"

    def test_write_valid_location(self):
        result = write(5, words)
        self.assertEqual(result, "test_word")

    def test_write_empty_location(self):
        # Test reading from an empty location
        result = write(10, words)
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()
