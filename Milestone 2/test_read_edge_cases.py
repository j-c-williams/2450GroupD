import unittest
from UVSim import read, words

class TestReadFunction(unittest.TestCase):

    def setUp(self):
        global words
        words = [""] * 100
        words[5] = "test_word"

    def test_read_negative_location(self):
        # Test reading from a negative location
        with self.assertRaises(IndexError):  # Should raise IndexError for negative indices
            read(-1, words)

    def test_read_out_of_bounds_location(self):
        # Test reading from a location outside the bounds of the array
        with self.assertRaises(IndexError):  # Should raise IndexError for out-of-bounds indices
            read(150, words)  # Assume words only has 100 elements

    def test_read_none_value(self):
        # Test reading a None value from the array
        words[20] = None  # Set location 20 to None
        result = read(20, words)
        self.assertEqual(result, "")  # Expect an empty string for None values

if __name__ == '__main__':
    unittest.main()
