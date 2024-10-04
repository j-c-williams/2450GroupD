import unittest
from unittest.mock import patch
from io import StringIO
import UVSim

class TestReadFunctions(unittest.TestCase):
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

class TestWriteFunction(unittest.TestCase):
    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.words[5] = "test_word"

    def test_write_valid_location(self):
        result = UVSim.write(5, words)
        self.assertEqual(result, "test_word")

    def test_write_empty_location(self):
        # Test reading from an empty location
        result = UVSim.write(10, words)
        self.assertEqual(result, "")
    
    def test_write_negative_location(self):
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

class TestLoadFunction(unittest.TestCase):
    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 0
        UVSim.pointer = 0

    def test_load(self):
        UVSim.words[33] = "+9999"
        UVSim.load(33)
        self.assertEqual(UVSim.accumulator, 9999)

    def test_load_out_of_bounds_pos(self):
        self.assertRaises(IndexError, UVSim.load, 999999)
    
    def test_load_out_of_bounds_neg(self):
        self.assertRaises(IndexError, UVSim.load, -1)

class TestStoreFunction(unittest.TestCase):
    def setUp(self):
        UVSim.words = [""] * 100            # I was having issues with a global accumulator for some reason,
        UVSim.accumulator = "stored_value"  # So I'm editing them on the module level instead

    def test_store_value_in_location(self):
        UVSim.store(7)
        self.assertEqual(UVSim.words[7], "stored_value")

    def test_store_negative_location(self):
        # Test handling a negative index
        with self.assertRaises(IndexError):  # Assuming store should raise an IndexError for negative indices
            UVSim.store(-1)

    def test_store_out_of_bounds_location(self):
        # Test storing to a location outside of the words array bounds
        with self.assertRaises(IndexError):  # Assuming store should raise an IndexError for out-of-bounds indices
            UVSim.store(150)  # Assuming the words array has only 100 elements

    def test_store_empty_accumulator(self):
        # Test storing when the accumulator is an empty string
        UVSim.accumulator = ""  # Set accumulator to an empty string
        UVSim.store(10)
        self.assertEqual(UVSim.words[10], "")

    def test_store_none_accumulator(self):
        # Test storing when the accumulator is None
        UVSim.accumulator = None
        UVSim.store(20)
        self.assertEqual(UVSim.words[20], None)

class TestAddFunction(unittest.TestCase):
    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 0  # Initialize with zero 

    def test_add_to_accumulator(self):
        UVSim.words[5] = "2"  # Set up a addative
        UVSim.add(5)  # Add location 5 content to accumulator
        self.assertEqual(UVSim.accumulator, 2)  # 0 + 2 = 2

    def test_add_negative(self):
        UVSim.words[6] = "-2"  # Set negative
        UVSim.add(6) # Add location 6 content to accumulator
        self.assertEqual(UVSim.accumulator, -2) #: -2 + 0 = -2
    
    def test_add_to_accumulator_pos_overflow(self):
        UVSim.accumulator = 9999
        UVSim.words[5] = "2"  # Set up a addative
        UVSim.add(5)  # Add location 5 content to accumulator
        self.assertEqual(UVSim.accumulator, 1)  # 9999 + 2 = 10001 -> truncated to 0001 or 1

    def test_add_negative_overflow(self):
        UVSim.accumulator = -9999
        UVSim.words[6] = "-2"  # Set negative
        UVSim.add(6) # Add location 6 content to accumulator
        self.assertEqual(UVSim.accumulator, -1) # -9999 + (-2) = -10001 -> truncated to -0001 or -1

class TestSubFunction(unittest.TestCase):
    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 0  # Initialize with zero 

    def test_subtract_from_accumulator(self):
        UVSim.words[5] = "2"  # Set up a addative
        UVSim.subtract(5)  # Add location 5 content to accumulator
        self.assertEqual(UVSim.accumulator, -2)  # 0 + 2 = 2

    def test_subtract_negative(self):
        UVSim.words[6] = "-2"  # Set negative
        UVSim.subtract(6) # Subtract location 6 content from accumulator
        self.assertEqual(UVSim.accumulator, 2) #: 0 - (-2) = 2

    def test_subtract_from_accumulator_pos_overflow(self):
        UVSim.accumulator = 9999
        UVSim.words[5] = "-2"  # Set up a addative
        UVSim.subtract(5)  # Add location 5 content to accumulator
        self.assertEqual(UVSim.accumulator, 1)  # 9999 + 2 = 10001 -> truncated to 0001 or 1

    def test_subtract_negative_overflow(self):
        UVSim.accumulator = -9999
        UVSim.words[6] = "2"  # Set negative
        UVSim.subtract(6) # Add location 6 content to accumulator
        self.assertEqual(UVSim.accumulator, -1) # -9999 + (-2) = -10001 -> truncated to -0001 or -1

class TestDivideFunction(unittest.TestCase):
    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 10  # Initialize with a non-zero value

    def test_divide_by_non_zero(self):
        UVSim.words[5] = "2"  # Set up a divisor
        UVSim.divide(5)  # Divide accumulator by the value at index 5
        self.assertEqual(UVSim.accumulator, 5)  # 10 / 2 = 5

    def test_divide_by_zero(self):
        UVSim.words[6] = "0"  # Set up a divisor of zero
        with self.assertRaises(ZeroDivisionError):
            UVSim.divide(6)  # Attempt to divide by zero

    def test_divide_large_number(self):
        UVSim.accumulator = 1000000  # A large number
        UVSim.words[5] = "100000"  # A large divisor
        UVSim.divide(5)
        self.assertEqual(UVSim.accumulator, 10)  # 1000000 / 100000 = 10

    def test_divide_large_dividend_by_small_divisor(self):
        UVSim.accumulator = 1  # A small number
        UVSim.words[6] = "0.0001"  # A very small divisor
        UVSim.divide(6)
        self.assertEqual(UVSim.accumulator, 10000)  # 1 / 0.0001 = 10000

    def test_divide_zero_accumulator(self):
        UVSim.accumulator = 0  # Set the accumulator to zero
        UVSim.words[7] = "5"  # A normal divisor
        UVSim.divide(7)
        self.assertEqual(UVSim.accumulator, 0)  # 0 / 5 = 0

    def test_divide_negative_number(self):
        UVSim.accumulator = -10  # A negative number
        UVSim.words[8] = "2"  # A positive divisor
        UVSim.divide(8)
        self.assertEqual(UVSim.accumulator, -5)  # -10 / 2 = -5

    def test_divide_negative_divisor(self):
        UVSim.accumulator = 10
        UVSim.words[9] = "-2"  # A negative divisor
        UVSim.divide(9)
        self.assertEqual(UVSim.accumulator, -5)  # 10 / -2 = -5

class TestMultFunction(unittest.TestCase):
    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 3  # Initialize with zero 

    def test_multiply_accumulator(self):
        UVSim.words[5] = "2"  # Set up a addative
        UVSim.multiply(5)  # Add location 5 content to accumulator
        self.assertEqual(UVSim.accumulator, 6)  # 2 * 3 = 6

    def test_multiply_negative(self):
        UVSim.words[6] = "-2"  # Set negative
        UVSim.multiply(6) # Add location 6 content to accumulator
        self.assertEqual(UVSim.accumulator, -6) #: -2 * 3 = -6
    
    def test_multiply_accumulator_large(self):
        UVSim.words[5] = "9999"  # Set up a addative
        UVSim.multiply(5)  # Add location 5 content to accumulator
        self.assertEqual(UVSim.accumulator, 9997)  # 9999 * 3 = 29997 -> 9997(truncatated)

    def test_multiply_zero(self):
        UVSim.words[6] = "0"  # Set negative
        UVSim.multiply(6) # Add location 6 content to accumulator
        self.assertEqual(UVSim.accumulator, 0) #: 0 * 3 = 0

class TestBranchFunction(unittest.TestCase):
    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 0
        UVSim.pointer = 0

    def test_branch(self):
        UVSim.branch(99)
        self.assertEqual(UVSim.pointer, 99) # correctly branches

    def test_branch_out_of_bounds_pos(self):
        self.assertRaises(IndexError, UVSim.branch, 999999)
    
    def test_branch_out_of_bounds_neg(self):
        self.assertRaises(IndexError, UVSim.branch, -1)

class TestBranchNegFunction(unittest.TestCase):
    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 0
        UVSim.pointer = 0

    def test_branch_neg(self):
        UVSim.pointer = 0
        UVSim.accumulator = -1
        UVSim.branch_neg(99)
        self.assertEqual(UVSim.pointer, 99) # branch_neg does branch
    
    def test_branch_neg_pos(self):
        UVSim.pointer = 0
        UVSim.accumulator = 1
        UVSim.branch_neg(99)
        self.assertEqual(UVSim.pointer, 1) # branch_neg does not branch, but moves to the next word

    def test_branch_neg_out_of_bounds_pos(self):
        self.assertRaises(IndexError, UVSim.branch_neg, 999999)
    
    def test_branch_neg_out_of_bounds_neg(self):
        self.assertRaises(IndexError, UVSim.branch_neg, -1)

class TestBranchZeroFunction(unittest.TestCase):
    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 0
        UVSim.pointer = 0

    def test_branch_zero(self):
        UVSim.pointer = 0
        UVSim.accumulator = 0
        UVSim.branch_zero(99)
        self.assertEqual(UVSim.pointer, 99) # branch_zero does branch
    
    def test_branch_non_zero(self):
        UVSim.pointer = 0
        UVSim.accumulator = 1
        UVSim.branch_zero(99)
        self.assertEqual(UVSim.pointer, 1) # branch_zero does not branch, but moves to the next word

    def test_branch_zero_out_of_bounds_pos(self):
        self.assertRaises(IndexError, UVSim.branch_zero, 999999)
    
    def test_branch_zero_out_of_bounds_neg(self):
        self.assertRaises(IndexError, UVSim.branch_zero, -1)

if __name__ == '__main__':
    # Combine all unit tests into one suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestReadFunctions))
    suite.addTest(unittest.makeSuite(TestWriteFunction)) #Commented because they don't work
    suite.addTest(unittest.makeSuite(TestLoadFunction))
    suite.addTest(unittest.makeSuite(TestStoreFunction))
    suite.addTest(unittest.makeSuite(TestAddFunction))
    suite.addTest(unittest.makeSuite(TestSubFunction))
    suite.addTest(unittest.makeSuite(TestDivideFunction))
    suite.addTest(unittest.makeSuite(TestMultFunction))
    suite.addTest(unittest.makeSuite(TestBranchFunction))
    suite.addTest(unittest.makeSuite(TestBranchNegFunction))
    suite.addTest(unittest.makeSuite(TestBranchZeroFunction))

    # Run the whole suite
    runner = unittest.TextTestRunner()
    runner.run(suite)
