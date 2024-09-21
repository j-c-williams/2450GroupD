import unittest
import UVSim

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
        

if __name__ == '__main__':
    unittest.main()