import unittest
import UVSim

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
        

if __name__ == '__main__':
    unittest.main()
