import unittest

import matplotlib.pyplot as plt
import numpy as np

from model.buzzness import Bee
from model.hive import Hive, Comb


class TestHive(unittest.TestCase):

    def setUp(self):
        """Set up a Hive object for testing"""
        self.bees = [
            Bee("bee1", (5, 5)),
            Bee("bee2", (10, 10)),
            Bee("bee3", (15, 15))
        ]
        self.hive = Hive(self.bees)

    def test_hive_initialization(self):
        """Test hive is initialized correctly"""
        expected_hive = np.full(Hive.HIVE_SIZE, 10)
        np.testing.assert_array_equal(self.hive.hive, expected_hive)
        self.assertEqual(self.hive.clist, [])
        self.assertEqual(self.hive.blist, self.bees)

    def test_add_comb(self):
        """Test adding a comb to the hive"""
        comb = Comb(pos=(2, 3), level=5)
        self.hive.clist.append(comb)
        self.assertEqual(len(self.hive.clist), 1)
        self.assertEqual(self.hive.clist[0].pos, (2, 3))
        self.assertEqual(self.hive.clist[0].level, 5)

    def test_plot(self):
        """Test plot runs without errors"""
        fig, ax = plt.subplots()
        try:
            self.hive.plot(ax)
        except Exception as e:
            self.fail(f"Plotting the hive raised an exception: {e}")
        finally:
            plt.close(fig)

    def test_plot_with_comb(self):
        """Test plot with a comb present"""
        comb = Comb(pos=(1, 1), level=3)
        self.hive.clist.append(comb)

        fig, ax = plt.subplots()
        self.hive.plot(ax)

        # Check if the hive grid updated correctly at (1,1)
        self.assertEqual(self.hive.hive[1, 1], 3)
        plt.close(fig)


if __name__ == '__main__':
    unittest.main()
