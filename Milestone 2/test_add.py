import unittest
import UVSim

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
        

if __name__ == '__main__':
    unittest.main()
