import unittest
import UVSim

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
        

if __name__ == '__main__':
    unittest.main()
