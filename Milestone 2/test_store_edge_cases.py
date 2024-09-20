import unittest
import UVSim

class TestStoreFunction(unittest.TestCase):

    def setUp(self):
        UVSim.words = [""] * 100
        UVSim.accumulator = "stored_value"

    def test_store_negative_location(self):
        # Test handling a negative index
        with self.assertRaises(IndexError):  # Assuming store should raise an IndexError for negative indices
            UVSim.store(-1)

    def test_store_out_of_bounds_location(self):
        # Test storing to a location outside of the words array bounds
        with self.assertRaises(IndexError):  # Assuming store should raise an IndexError for out-of-bounds indices
            UVSim.store(150)  # Assuming the words array has only 100 elements

    def test_store_empty_accumulator(self):
        # Test storing when the accumulator is an empty string
        UVSim.accumulator = ""  # Set accumulator to an empty string
        UVSim.store(10)
        self.assertEqual(UVSim.words[10], "")

    def test_store_none_accumulator(self):
        # Test storing when the accumulator is None
        UVSim.accumulator = None
        UVSim.store(20)
        self.assertEqual(UVSim.words[20], None)

if __name__ == '__main__':
    unittest.main()
