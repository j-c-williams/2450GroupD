import unittest
import UVSim

class TestStoreFunction(unittest.TestCase):

    def setUp(self):
        UVSim.words = [""] * 100            # I was having issues with a global accumulator for some reason,
        UVSim.accumulator = "stored_value"  # So I'm editing them on the module level instead

    def test_store_value_in_location(self):
        UVSim.store(7)
        self.assertEqual(UVSim.words[7], "stored_value")

if __name__ == '__main__':
    unittest.main()
