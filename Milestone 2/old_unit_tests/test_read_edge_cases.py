import unittest
from unittest.mock import patch
import UVSim

class TestReadFunctionEdgeCases(unittest.TestCase):

    def setUp(self):
        # Reset the words list before each test
        UVSim.words = [""] * 100

    @patch('UVSim.input', return_value="test_input")
    def test_read_negative_location(self, mock_input):
        with self.assertRaises(IndexError):
            UVSim.read(-1)

    @patch('UVSim.input', return_value="test_input")
    def test_read_out_of_bounds_location(self, mock_input):
        with self.assertRaises(IndexError):
            UVSim.read(100)

    @patch('UVSim.input', return_value="test_input")
    def test_read_large_valid_location(self, mock_input):
        UVSim.read(99)  # Last valid index
        self.assertEqual(UVSim.words[99], "test_input")

    @patch('UVSim.input', return_value="a" * 1000)
    def test_read_very_long_input(self, mock_input):
        UVSim.read(0)
        self.assertEqual(UVSim.words[0], "a" * 1000)

if __name__ == '__main__':
    unittest.main()