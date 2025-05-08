import unittest
import numpy as np
from model.hive import Comb, Hive  # Replace 'your_module_name' with the actual module name


class TestCombAndHive(unittest.TestCase):

    def test_comb_initialization(self):
        pos = (2, 3)
        comb = Comb(pos)
        self.assertEqual(comb.pos, pos)
        self.assertFalse(comb.has_nectar)

    def test_hive_initialization(self):
        hive_size = (4, 5)
        hive = Hive(hive_size)

        # Check if hive.hive is correctly initialized
        expected_array = np.full(hive_size, 10)
        np.testing.assert_array_equal(hive.hive, expected_array)

        # Check if the correct number of Comb objects were created
        self.assertEqual(len(hive.clist), hive_size[0] * hive_size[1])

        # Check if Comb objects have the correct positions
        expected_positions = [(row, col) for row in range(hive_size[0]) for col in range(hive_size[1])]
        actual_positions = [comb.pos for comb in hive.clist]
        self.assertEqual(actual_positions, expected_positions)

        # Check that all Combs start without nectar
        for comb in hive.clist:
            self.assertFalse(comb.has_nectar)


if __name__ == '__main__':
    unittest.main()
