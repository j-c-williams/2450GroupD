import unittest
import UVSim

class TestDivideFunctionEdgeCases(unittest.TestCase):

    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 0

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

if __name__ == '__main__':
    unittest.main()
