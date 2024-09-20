import unittest
from UVSim import write, words

class TestReadFunction(unittest.TestCase):

    def setUp(self):
        global words
        words = [""] * 100
        words[5] = "test_word"

    def test_read_negative_location(self):
        # Test writing from a negative location
        with self.assertRaises(IndexError):  # Should raise IndexError for negative indices
            write(-1, words)

    def test_write_out_of_bounds_location(self):
        # Test writing from a location outside the bounds of the array
        with self.assertRaises(IndexError):  # Should raise IndexError for out-of-bounds indices
            write(150, words)  # Assume words only has 100 elements

    def test_write_none_value(self):
        # Test writing a None value from the array
        words[20] = None  # Set location 20 to None
        result = write(20, words)
        self.assertEqual(result, "")  # Expect an empty string for None values

if __name__ == '__main__':
    unittest.main()
