import unittest
from unittest.mock import patch, Mock
from io import StringIO
from UVSim import LogicalOperator


class TestReadFunctions(unittest.TestCase):
    def setUp(self):
        # Reset the words list before each test
        LogicalOperator.words = [""] * 100

    @patch('LogicalOperator.input', return_value="test_input")
    def test_read_valid_location(self, mock_input):
        LogicalOperator.read(0)
        self.assertEqual(LogicalOperator.words[0], "test_input")

    @patch('LogicalOperator.input', return_value="another_input")
    def test_read_different_location(self, mock_input):
        LogicalOperator.read(50)
        self.assertEqual(LogicalOperator.words[50], "another_input")

    @patch('LogicalOperator.input', return_value="")
    def test_read_empty_input(self, mock_input):
        LogicalOperator.read(0)
        self.assertEqual(LogicalOperator.words[0], "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('LogicalOperator.input', return_value="test_output")
    def test_read_output_message(self, mock_input, mock_stdout):
        LogicalOperator.read(25)
        expected_output = 'Writing "test_output" to register 25.\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('LogicalOperator.input', return_value="test_input")
    def test_read_negative_location(self, mock_input):
        with self.assertRaises(IndexError):
            LogicalOperator.read(-1)

    @patch('LogicalOperator.input', return_value="test_input")
    def test_read_out_of_bounds_location(self, mock_input):
        with self.assertRaises(IndexError):
            LogicalOperator.read(100)

    @patch('LogicalOperator.input', return_value="test_input")
    def test_read_large_valid_location(self, mock_input):
        LogicalOperator.read(99)  # Last valid index
        self.assertEqual(LogicalOperator.words[99], "test_input")

    @patch('LogicalOperator.input', return_value="a" * 1000)
    def test_read_very_long_input(self, mock_input):
        LogicalOperator.read(0)
        self.assertEqual(LogicalOperator.words[0], "a" * 1000)

class TestWriteFunction(unittest.TestCase):
    def setUp(self):
        LogicalOperator.words = [""] * 100
        LogicalOperator.words[5] = "test_word"

    def test_write_valid_location(self):
        result = LogicalOperator.write(5, words)
        self.assertEqual(result, "test_word")

    def test_write_empty_location(self):
        # Test reading from an empty location
        result = LogicalOperator.write(10, words)
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
        self.mock_interface = Mock()
        self.mock_file_handler = Mock()
        self.logic = LogicalOperator(self.mock_interface, self.mock_file_handler)

        self.logic.words = [""] * 100
        self.logic.accumulator = 0
        self.logic.pointer = 0

    def test_load(self):
        self.logic.words[33] = "+9999"
        self.logic.load(33)
        self.assertEqual(self.logic.accumulator, 9999)

    def test_load_out_of_bounds_pos(self):
        self.assertRaises(IndexError, self.logic.load, 999999)
    
    def test_load_out_of_bounds_neg(self):
        self.assertRaises(IndexError, self.logic.load, -1)

class TestStoreFunction(unittest.TestCase):
    def setUp(self):
        LogicalOperator.words = [""] * 100            # I was having issues with a global accumulator for some reason,
        LogicalOperator.accumulator = "stored_value"  # So I'm editing them on the module level instead

    def test_store_value_in_location(self):
        LogicalOperator.store(7)
        self.assertEqual(LogicalOperator.words[7], "stored_value")

    def test_store_negative_location(self):
        # Test handling a negative index
        with self.assertRaises(IndexError):  # Assuming store should raise an IndexError for negative indices
            LogicalOperator.store(-1)

    def test_store_out_of_bounds_location(self):
        # Test storing to a location outside of the words array bounds
        with self.assertRaises(IndexError):  # Assuming store should raise an IndexError for out-of-bounds indices
            LogicalOperator.store(150)  # Assuming the words array has only 100 elements

    def test_store_empty_accumulator(self):
        # Test storing when the accumulator is an empty string
        LogicalOperator.accumulator = ""  # Set accumulator to an empty string
        LogicalOperator.store(10)
        self.assertEqual(LogicalOperator.words[10], "")

    def test_store_none_accumulator(self):
        # Test storing when the accumulator is None
        LogicalOperator.accumulator = None
        LogicalOperator.store(20)
        self.assertEqual(LogicalOperator.words[20], None)

class TestAddFunction(unittest.TestCase):
    def setUp(self):
        LogicalOperator.words = [""] * 100
        LogicalOperator.accumulator = 0  # Initialize with zero 

    def test_add_to_accumulator(self):
        LogicalOperator.words[5] = "2"  # Set up a addative
        LogicalOperator.add(5)  # Add location 5 content to accumulator
        self.assertEqual(LogicalOperator.accumulator, 2)  # 0 + 2 = 2

    def test_add_negative(self):
        LogicalOperator.words[6] = "-2"  # Set negative
        LogicalOperator.add(6) # Add location 6 content to accumulator
        self.assertEqual(LogicalOperator.accumulator, -2) #: -2 + 0 = -2
    
    def test_add_to_accumulator_pos_overflow(self):
        LogicalOperator.accumulator = 9999
        LogicalOperator.words[5] = "2"  # Set up a addative
        LogicalOperator.add(5)  # Add location 5 content to accumulator
        self.assertEqual(LogicalOperator.accumulator, 1)  # 9999 + 2 = 10001 -> truncated to 0001 or 1

    def test_add_negative_overflow(self):
        LogicalOperator.accumulator = -9999
        LogicalOperator.words[6] = "-2"  # Set negative
        LogicalOperator.add(6) # Add location 6 content to accumulator
        self.assertEqual(LogicalOperator.accumulator, -1) # -9999 + (-2) = -10001 -> truncated to -0001 or -1

class TestSubFunction(unittest.TestCase):
    def setUp(self):
        LogicalOperator.words = [""] * 100
        LogicalOperator.accumulator = 0  # Initialize with zero 

    def test_subtract_from_accumulator(self):
        LogicalOperator.words[5] = "2"  # Set up a addative
        LogicalOperator.subtract(5)  # Add location 5 content to accumulator
        self.assertEqual(LogicalOperator.accumulator, -2)  # 0 + 2 = 2

    def test_subtract_negative(self):
        LogicalOperator.words[6] = "-2"  # Set negative
        LogicalOperator.subtract(6) # Subtract location 6 content from accumulator
        self.assertEqual(LogicalOperator.accumulator, 2) #: 0 - (-2) = 2

    def test_subtract_from_accumulator_pos_overflow(self):
        LogicalOperator.accumulator = 9999
        LogicalOperator.words[5] = "-2"  # Set up a addative
        LogicalOperator.subtract(5)  # Add location 5 content to accumulator
        self.assertEqual(LogicalOperator.accumulator, 1)  # 9999 + 2 = 10001 -> truncated to 0001 or 1

    def test_subtract_negative_overflow(self):
        LogicalOperator.accumulator = -9999
        LogicalOperator.words[6] = "2"  # Set negative
        LogicalOperator.subtract(6) # Add location 6 content to accumulator
        self.assertEqual(LogicalOperator.accumulator, -1) # -9999 + (-2) = -10001 -> truncated to -0001 or -1

class TestDivideFunction(unittest.TestCase):
    def setUp(self):
        LogicalOperator.words = [""] * 100
        LogicalOperator.accumulator = 10  # Initialize with a non-zero value

    def test_divide_by_non_zero(self):
        LogicalOperator.words[5] = "2"  # Set up a divisor
        LogicalOperator.divide(5)  # Divide accumulator by the value at index 5
        self.assertEqual(LogicalOperator.accumulator, 5)  # 10 / 2 = 5

    def test_divide_by_zero(self):
        LogicalOperator.words[6] = "0"  # Set up a divisor of zero
        with self.assertRaises(ZeroDivisionError):
            LogicalOperator.divide(6)  # Attempt to divide by zero

    def test_divide_large_number(self):
        LogicalOperator.accumulator = 1000000  # A large number
        LogicalOperator.words[5] = "100000"  # A large divisor
        LogicalOperator.divide(5)
        self.assertEqual(LogicalOperator.accumulator, 10)  # 1000000 / 100000 = 10

    def test_divide_large_dividend_by_small_divisor(self):
        LogicalOperator.accumulator = 1  # A small number
        LogicalOperator.words[6] = "0.0001"  # A very small divisor
        LogicalOperator.divide(6)
        self.assertEqual(LogicalOperator.accumulator, 10000)  # 1 / 0.0001 = 10000

    def test_divide_zero_accumulator(self):
        LogicalOperator.accumulator = 0  # Set the accumulator to zero
        LogicalOperator.words[7] = "5"  # A normal divisor
        LogicalOperator.divide(7)
        self.assertEqual(LogicalOperator.accumulator, 0)  # 0 / 5 = 0

    def test_divide_negative_number(self):
        LogicalOperator.accumulator = -10  # A negative number
        LogicalOperator.words[8] = "2"  # A positive divisor
        LogicalOperator.divide(8)
        self.assertEqual(LogicalOperator.accumulator, -5)  # -10 / 2 = -5

    def test_divide_negative_divisor(self):
        LogicalOperator.accumulator = 10
        LogicalOperator.words[9] = "-2"  # A negative divisor
        LogicalOperator.divide(9)
        self.assertEqual(LogicalOperator.accumulator, -5)  # 10 / -2 = -5

class TestMultFunction(unittest.TestCase):
    def setUp(self):
        LogicalOperator.words = [""] * 100
        LogicalOperator.accumulator = 3  # Initialize with zero 

    def test_multiply_accumulator(self):
        LogicalOperator.words[5] = "2"  # Set up a addative
        LogicalOperator.multiply(5)  # Add location 5 content to accumulator
        self.assertEqual(LogicalOperator.accumulator, 6)  # 2 * 3 = 6

    def test_multiply_negative(self):
        LogicalOperator.words[6] = "-2"  # Set negative
        LogicalOperator.multiply(6) # Add location 6 content to accumulator
        self.assertEqual(LogicalOperator.accumulator, -6) #: -2 * 3 = -6
    
    def test_multiply_accumulator_large(self):
        LogicalOperator.words[5] = "9999"  # Set up a addative
        LogicalOperator.multiply(5)  # Add location 5 content to accumulator
        self.assertEqual(LogicalOperator.accumulator, 9997)  # 9999 * 3 = 29997 -> 9997(truncatated)

    def test_multiply_zero(self):
        LogicalOperator.words[6] = "0"  # Set negative
        LogicalOperator.multiply(6) # Add location 6 content to accumulator
        self.assertEqual(LogicalOperator.accumulator, 0) #: 0 * 3 = 0

class TestBranchFunction(unittest.TestCase):
    def setUp(self):
        self.mock_interface = Mock()
        self.mock_file_handler = Mock()
        self.logic = LogicalOperator(self.mock_interface, self.mock_file_handler)

        self.logic.words = [""] * 100
        self.logic.accumulator = 0
        self.logic.pointer = 0

    def test_branch(self):
        self.logic.branch(99)
        self.assertEqual(self.logic.pointer, 99) # correctly branches

    def test_branch_out_of_bounds_pos(self):
        self.assertRaises(IndexError, self.logic.branch, 999999)
    
    def test_branch_out_of_bounds_neg(self):
        self.assertRaises(IndexError, self.logic.branch, -1)

class TestBranchNegFunction(unittest.TestCase):
    def setUp(self):
        self.mock_interface = Mock()
        self.mock_file_handler = Mock()
        self.logic = LogicalOperator(self.mock_interface, self.mock_file_handler)

        self.logic.words = [""] * 100
        self.logic.accumulator = 0
        self.logic.pointer = 0

    def test_branch_neg(self):
        self.logic.pointer = 0
        self.logic.accumulator = -1
        self.logic.branch_neg(99)
        self.assertEqual(self.logic.pointer, 99) # branch_neg does branch
    
    def test_branch_neg_pos(self):
        self.logic.pointer = 0
        self.logic.accumulator = 1
        self.logic.branch_neg(99)
        self.assertEqual(self.logic.pointer, 1) # branch_neg does not branch, but moves to the next word

    def test_branch_neg_out_of_bounds_pos(self):
        self.assertRaises(IndexError, self.logic.branch_neg, 999999)
    
    def test_branch_neg_out_of_bounds_neg(self):
        self.assertRaises(IndexError, self.logic.branch_neg, -1)

class TestBranchZeroFunction(unittest.TestCase):
    def setUp(self):
        self.mock_interface = Mock()
        self.mock_file_handler = Mock()
        self.logic = LogicalOperator(self.mock_interface, self.mock_file_handler)

        self.logic.words = [""] * 100
        self.logic.accumulator = 0
        self.logic.pointer = 0

    def test_branch_zero(self):
        self.logic.pointer = 0
        self.logic.accumulator = 0
        self.logic.branch_zero(99)
        self.assertEqual(self.logic.pointer, 99) # branch_zero does branch
    
    def test_branch_non_zero(self):
        self.logic.pointer = 0
        self.logic.accumulator = 1
        self.logic.branch_zero(99)
        self.assertEqual(self.logic.pointer, 1) # branch_zero does not branch, but moves to the next word

    def test_branch_zero_out_of_bounds_pos(self):
        self.assertRaises(IndexError, self.logic.branch_zero, 999999)
    
    def test_branch_zero_out_of_bounds_neg(self):
        self.assertRaises(IndexError, self.logic.branch_zero, -1)

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
