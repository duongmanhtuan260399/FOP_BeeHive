import unittest
import numpy as np
from model.hive import Comb, Hive

class TestCombAndHive(unittest.TestCase):
    """
    [1.3 Hive] Test suite for the Hive and Comb classes.
    
    This test suite verifies:
    - Comb initialization and attributes
    - Hive grid creation and initialization
    - Comb list generation and positioning
    - Default values and states
    """

    def test_comb_initialization(self):
        """[1.3.1 Comb] Test initialization of a single comb cell"""
        # Create a comb at position (2,3)
        pos = (2, 3)
        comb = Comb(pos)
        
        # Verify position is set correctly
        self.assertEqual(comb.pos, pos)
        # Verify comb starts without nectar
        self.assertFalse(comb.has_nectar)

    def test_hive_initialization(self):
        """[1.3 Hive] Test initialization of the hive structure"""
        # Create a hive with size 4x5
        hive_size = (4, 5)
        hive = Hive(hive_size)

        # Verify hive grid is initialized with correct size and default value
        expected_array = np.full(hive_size, 10)
        np.testing.assert_array_equal(hive.hive, expected_array)

        # Verify correct number of combs are created
        self.assertEqual(len(hive.clist), hive_size[0] * hive_size[1])

        # Verify all combs have correct positions
        expected_positions = [(row, col) for row in range(hive_size[0]) for col in range(hive_size[1])]
        actual_positions = [comb.pos for comb in hive.clist]
        self.assertEqual(actual_positions, expected_positions)

        # Verify all combs start without nectar
        for comb in hive.clist:
            self.assertFalse(comb.has_nectar)


if __name__ == '__main__':
    unittest.main()
