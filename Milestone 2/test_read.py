import unittest
from unittest.mock import patch
from io import StringIO
import UVSim

class TestReadFunctionNormal(unittest.TestCase):

    def setUp(self):
        # Reset the words list before each test
        UVSim.words = [""] * 100

    @patch('UVSim.input', return_value="test_input")
    def test_read_valid_location(self, mock_input):
        UVSim.read(0)
        self.assertEqual(UVSim.words[0], "test_input")

    @patch('UVSim.input', return_value="another_input")
    def test_read_different_location(self, mock_input):
        UVSim.read(50)
        self.assertEqual(UVSim.words[50], "another_input")

    @patch('UVSim.input', return_value="")
    def test_read_empty_input(self, mock_input):
        UVSim.read(0)
        self.assertEqual(UVSim.words[0], "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('UVSim.input', return_value="test_output")
    def test_read_output_message(self, mock_input, mock_stdout):
        UVSim.read(25)
        expected_output = 'Writing "test_output" to register 25.\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()