import unittest
import UVSim

class TestBranchNegFunction(unittest.TestCase):

    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 0
        UVSim.pointer = 0

    def test_branch_neg(self):
        UVSim.pointer = 0
        UVSim.accumulator = -1
        UVSim.branch_neg(99)
        self.assertEqual(UVSim.pointer, 99) # branch_neg does branch
    
    def test_branch_neg_pos(self):
        UVSim.pointer = 0
        UVSim.accumulator = 1
        UVSim.branch_neg(99)
        self.assertEqual(UVSim.pointer, 1) # branch_neg does not branch, but moves to the next word

    def test_branch_neg_out_of_bounds_pos(self):
        self.assertRaises(IndexError, UVSim.branch_neg, 999999)
    
    def test_branch_neg_out_of_bounds_neg(self):
        self.assertRaises(IndexError, UVSim.branch_neg, -1)
        

if __name__ == '__main__':
    unittest.main()
