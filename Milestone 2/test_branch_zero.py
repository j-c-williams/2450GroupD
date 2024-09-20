import unittest
import UVSim

class TestBranchZeroFunction(unittest.TestCase):

    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = 0
        UVSim.pointer = 0

    def test_branch_zero(self):
        UVSim.pointer = 0
        UVSim.accumulator = 0
        UVSim.branch_zero(99)
        self.assertEqual(UVSim.pointer, 99) # branch_zero does branch
    
    def test_branch_non_zero(self):
        UVSim.pointer = 0
        UVSim.accumulator = 1
        UVSim.branch_zero(99)
        self.assertEqual(UVSim.pointer, 1) # branch_zero does not branch, but moves to the next word

    def test_branch_zero_out_of_bounds_pos(self):
        self.assertRaises(IndexError, UVSim.branch_zero, 999999)
    
    def test_branch_zero_out_of_bounds_neg(self):
        self.assertRaises(IndexError, UVSim.branch_zero, -1)
        

if __name__ == '__main__':
    unittest.main()
