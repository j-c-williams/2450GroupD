import unittest
import UVSim

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

if __name__ == '__main__':
    unittest.main()
