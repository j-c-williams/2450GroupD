import unittest
import UVSim

class TestAddFunctionEdgeCases(unittest.TestCase):

    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 9999  # Initialize with zero 

    def test_subtract_from_accumulator_pos_overflow(self):
        UVSim.words[5] = "-2"  # Set up a addative
        UVSim.subtract(5)  # Add location 5 content to accumulator
        self.assertEqual(UVSim.accumulator, 1)  # 9999 + 2 = 10001 -> truncated to 0001 or 1

    def test_subtract_negative_overflow(self):
        UVSim.accumulator = -9999
        UVSim.words[6] = "2"  # Set negative
        UVSim.subtract(6) # Add location 6 content to accumulator
        self.assertEqual(UVSim.accumulator, -1) # -9999 + (-2) = -10001 -> truncated to -0001 or -1
        

if __name__ == '__main__':
    unittest.main()
