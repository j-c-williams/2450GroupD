import unittest
import UVSim

class TestMultiplyFunctionEdgeCases(unittest.TestCase):

    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 3  # Initialize with zero 

    def test_multiply_accumulator_large(self):
        UVSim.words[5] = "9999"  # Set up a addative
        UVSim.multiply(5)  # Add location 5 content to accumulator
        self.assertEqual(UVSim.accumulator, 9997)  # 9999 * 3 = 29997 -> 9997(truncatated)


    def test_multiply_zero(self):
        UVSim.words[6] = "0"  # Set negative
        UVSim.multiply(6) # Add location 6 content to accumulator
        self.assertEqual(UVSim.accumulator, 0) #: 0 * 3 = 0
        

if __name__ == '__main__':
    unittest.main()
