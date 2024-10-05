
import unittest
from unittest.mock import patch, Mock
from io import StringIO
from UVSim import LogicalOperator



class TestReadFunctions(unittest.TestCase):
    def setUp(self):
        self.mock_interface = Mock()
        self.mock_file_handler = Mock()
        self.logic = LogicalOperator(self.mock_interface, self.mock_file_handler)

        # Initialize words with valid instruction format
        self.logic.words = ["+1000"] * 100  # Fill with READ instructions
        self.logic.accumulator = 0
        self.logic.pointer = 0
        self.logic.wait_for_input = False  # Set this to False to simulate input already provided

    def test_read_valid_location(self):
        self.logic.input = "test_input"
        self.logic.read(0, self.mock_interface)
        self.assertEqual(self.logic.words[0], "test_input")

    def test_read_different_location(self):
        self.logic.input = "another_input"
        self.logic.read(50, self.mock_interface)
        self.assertEqual(self.logic.words[50], "another_input")

    def test_read_empty_input(self):
        self.logic.input = ""
        self.logic.read(0, self.mock_interface)
        self.assertEqual(self.logic.words[0], "")

    def test_read_output_message(self):
        self.logic.input = "test_output"
        self.logic.read(25, self.mock_interface)
        self.mock_interface.add_output_text.assert_any_call("Input: test_output")
        self.mock_interface.add_output_text.assert_any_call("Word test_output read into index 25")

    def test_read_negative_location(self):
        with self.assertRaises(IndexError):
            self.logic.read(-1, self.mock_interface)

    def test_read_out_of_bounds_location(self):
        with self.assertRaises(IndexError):
            self.logic.read(100, self.mock_interface)

    def test_read_large_valid_location(self):
        self.logic.input = "test_input"
        self.logic.read(99, self.mock_interface)  # Last valid index
        self.assertEqual(self.logic.words[99], "test_input")

    def test_read_very_long_input(self):
        self.logic.input = "a" * 1000
        self.logic.read(0, self.mock_interface)
        self.assertEqual(self.logic.words[0], "a" * 1000)

    def test_read_wait_for_input(self):
        self.logic.wait_for_input = True
        self.logic.read(0, self.mock_interface)
        self.mock_interface.add_output_text.assert_called_with("What would you like to write to register 0? ")
        self.assertFalse(self.logic.wait_for_input)

    def tearDown(self):
        # Reset the LogicalOperator state after each test
        self.logic.pointer = 0
        self.logic.wait_for_input = False

class TestWriteFunction(unittest.TestCase):
    def setUp(self):
        self.mock_interface = Mock()
        self.mock_file_handler = Mock()
        self.logic = LogicalOperator(self.mock_interface, self.mock_file_handler)

        self.logic.words = [""] * 100
        self.logic.accumulator = 0
        self.logic.pointer = 0
        self.logic.words[5] = "test_word"

    def test_write_valid_location(self):
        result = self.logic.write(5)
        self.assertEqual(result, "test_word")

    def test_write_empty_location(self):
        # Test reading from an empty locaton
        result = self.logic.write(10)
        self.assertEqual(result, "")
    
    def test_write_negative_location(self):
        # Test writing from a negative location
        with self.assertRaises(IndexError):  # Should raise IndexError for negative indices
            self.logic.write(-1)

    def test_write_out_of_bounds_location(self):
        # Test writing from a location outside the bounds of the array
        with self.assertRaises(IndexError):  # Should raise IndexError for out-of-bounds indices
            self.logic.write(150)  # Assume words only has 100 elements

    def test_write_none_value(self):
        # Test writing a None value from the array
        self.logic.words[20] = None  # Set location 20 to None
        result = self.logic.write(20)
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
        self.mock_interface = Mock()
        self.mock_file_handler = Mock()
        self.logic = LogicalOperator(self.mock_interface, self.mock_file_handler)

        self.logic.words = [""] * 100
        self.logic.pointer = 0
                                   
        self.logic.accumulator = "stored_value"  # intitialize logical operator accumulator with "stored_Value"

    def test_store_value_in_location(self):
        self.logic.store(7)
        self.assertEqual(self.logic.words[7], "stored_value")

    def test_store_negative_location(self):
        # Test handling a negative index
        with self.assertRaises(IndexError):  # Assuming store should raise an IndexError for negative indices
            self.logic.store(-1)

    def test_store_out_of_bounds_location(self):
        # Test storing to a location outside of the words array bounds
        with self.assertRaises(IndexError):  # Assuming store should raise an IndexError for out-of-bounds indices
            self.logic.store(150)  # Assuming the words array has only 100 elements

    def test_store_empty_accumulator(self):
        # Test storing when the accumulator is an empty string
        self.logic.accumulator = ""  # Set accumulator to an empty string
        self.logic.store(10)
        self.assertEqual(self.logic.words[10], "")

    def test_store_none_accumulator(self):
        # Test storing when the accumulator is None
        self.logic.accumulator = None
        self.logic.store(20)
        self.assertEqual(self.logic.words[20], None)

class TestAddFunction(unittest.TestCase):
    def setUp(self):
        self.mock_interface = Mock()
        self.mock_file_handler = Mock()
        self.logic = LogicalOperator(self.mock_interface, self.mock_file_handler)

        self.logic.words = [""] * 100
        self.logic.accumulator = 0
        self.logic.pointer = 0

    def test_add_to_accumulator(self):
        self.logic.words[5] = "2"  # Set up a addative
        self.logic.add(5)  # Add location 5 content to accumulator
        self.assertEqual(self.logic.accumulator, 2)  # 0 + 2 = 2

    def test_add_negative(self):
        self.logic.words[6] = "-2"  # Set negative
        self.logic.add(6) # Add location 6 content to accumulator
        self.assertEqual(self.logic.accumulator, -2) #: -2 + 0 = -2
    
    def test_add_to_accumulator_pos_overflow(self):
        self.logic.accumulator = 9999
        self.logic.words[5] = "2"  # Set up a addative
        self.logic.add(5)  # Add location 5 content to accumulator
        self.assertEqual(self.logic.accumulator, 1)  # 9999 + 2 = 10001 -> truncated to 0001 or 1

    def test_add_negative_overflow(self):
        self.logic.accumulator = -9999
        self.logic.words[6] = "-2"  # Set negative
        self.logic.add(6) # Add location 6 content to accumulator
        self.assertEqual(self.logic.accumulator, -1) # -9999 + (-2) = -10001 -> truncated to -0001 or -1

class TestSubFunction(unittest.TestCase):
    def setUp(self):
        self.mock_interface = Mock()
        self.mock_file_handler = Mock()
        self.logic = LogicalOperator(self.mock_interface, self.mock_file_handler)

        self.logic.words = [""] * 100
        self.logic.accumulator = 0
        self.logic.pointer = 0  # Initialize with zero 

    def test_subtract_from_accumulator(self):
        self.logic.words[5] = "2"  # Set up a addative
        self.logic.subtract(5)  # Add location 5 content to accumulator
        self.assertEqual(self.logic.accumulator, -2)  # 0 + 2 = 2

    def test_subtract_negative(self):
        self.logic.words[6] = "-2"  # Set negative
        self.logic.subtract(6) # Subtract location 6 content from accumulator
        self.assertEqual(self.logic.accumulator, 2) #: 0 - (-2) = 2

    def test_subtract_from_accumulator_pos_overflow(self):
        self.logic.accumulator = 9999
        self.logic.words[5] = "-2"  # Set up a addative
        self.logic.subtract(5)  # Add location 5 content to accumulator
        self.assertEqual(self.logic.accumulator, 1)  # 9999 + 2 = 10001 -> truncated to 0001 or 1

    def test_subtract_negative_overflow(self):
        self.logic.accumulator = -9999
        self.logic.words[6] = "2"  # Set negative
        self.logic.subtract(6) # Add location 6 content to accumulator
        self.assertEqual(self.logic.accumulator, -1) # -9999 + (-2) = -10001 -> truncated to -0001 or -1

class TestDivideFunction(unittest.TestCase):
    def setUp(self):
        self.mock_interface = Mock() #set up logical operator class with mock gui
        self.mock_file_handler = Mock() # mock file handler for logical operator as well
        self.logic = LogicalOperator(self.mock_interface, self.mock_file_handler)

        self.logic.words = [""] * 100
        self.logic.accumulator = 10 # Initialize with a 10 for divison
        self.logic.pointer = 0  

    def test_divide_by_non_zero(self):
        self.logic.words[5] = "2"  # Set up a divisor
        self.logic.divide(5)  # Divide accumulator by the value at index 5
        self.assertEqual(self.logic.accumulator, 5)  # 10 / 2 = 5

    def test_divide_by_zero(self):
        self.logic.words[6] = "0"  # Set up a divisor of zero
        with self.assertRaises(ZeroDivisionError):
            self.logic.divide(6)  # Attempt to divide by zero

    def test_divide_large_number(self):
        self.logic.accumulator = 1000000  # A large number
        self.logic.words[5] = "100000"  # A large divisor
        self.logic.divide(5)
        self.assertEqual(self.logic.accumulator, 10)  # 1000000 / 100000 = 10

    def test_divide_large_dividend_by_small_divisor(self):
        self.logic.accumulator = 1  # A small number
        self.logic.words[6] = "0.0001"  # A very small divisor
        self.logic.divide(6)
        self.assertEqual(self.logic.accumulator, 10000)  # 1 / 0.0001 = 10000

    def test_divide_zero_accumulator(self):
        self.logic.accumulator = 0  # Set the accumulator to zero
        self.logic.words[7] = "5"  # A normal divisor
        self.logic.divide(7)
        self.assertEqual(self.logic.accumulator, 0)  # 0 / 5 = 0

    def test_divide_negative_number(self):
        self.logic.accumulator = -10  # A negative number
        self.logic.words[8] = "2"  # A positive divisor
        self.logic.divide(8)
        self.assertEqual(self.logic.accumulator, -5)  # -10 / 2 = -5

    def test_divide_negative_divisor(self):
        self.logic.accumulator = 10
        self.logic.words[9] = "-2"  # A negative divisor
        self.logic.divide(9)
        self.assertEqual(self.logic.accumulator, -5)  # 10 / -2 = -5

class TestMultFunction(unittest.TestCase):
    def setUp(self):
        self.mock_interface = Mock()
        self.mock_file_handler = Mock()
        self.logic = LogicalOperator(self.mock_interface, self.mock_file_handler)

        self.logic.words = [""] * 100
        self.logic.accumulator = 3 # Initialize with non-zero for multiplication
        self.logic.pointer = 0  

    def test_multiply_accumulator(self):
        self.logic.words[5] = "2"  # Set up a addative
        self.logic.multiply(5)  # Add location 5 content to accumulator
        self.assertEqual(self.logic.accumulator, 6)  # 2 * 3 = 6

    def test_multiply_negative(self):
        self.logic.words[6] = "-2"  # Set negative
        self.logic.multiply(6) # Add location 6 content to accumulator
        self.assertEqual(self.logic.accumulator, -6) #: -2 * 3 = -6
    
    def test_multiply_accumulator_large(self):
        self.logic.words[5] = "9999"  # Set up a addative
        self.logic.multiply(5)  # Add location 5 content to accumulator
        self.assertEqual(self.logic.accumulator, 9997)  # 9999 * 3 = 29997 -> 9997(truncatated)

    def test_multiply_zero(self):
        self.logic.words[6] = "0"  # Set negative
        self.logic.multiply(6) # Add location 6 content to accumulator
        self.assertEqual(self.logic.accumulator, 0) #: 0 * 3 = 0

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
