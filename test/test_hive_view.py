import unittest
import numpy as np
import matplotlib.pyplot as plt
from model.hive import Hive, Comb
from model.buzzness import Bee
from view.HiveView import HiveView

class TestHiveView(unittest.TestCase):
    """
    [2.3 Hive View] Test suite for the HiveView class.
    
    This test suite verifies:
    - Proper visualization of hive combs
    - Correct display of bees in the hive
    - Plot configuration (title, labels, etc.)
    """

    def setUp(self):
        """Initialize test environment with common test data"""
        # Create a small hive for testing
        self.hive_size = (5, 5)
        self.hive = Hive(self.hive_size)
        
        # Create some test combs with and without nectar
        self.comb_with_nectar = Comb((1, 1))
        self.comb_with_nectar.has_nectar = True
        self.comb_without_nectar = Comb((2, 2))
        
        # Add combs to hive
        self.hive.clist = [self.comb_with_nectar, self.comb_without_nectar]
        
        # Create test bees
        self.bee_in_hive = Bee(1, (1, 1), (0, 0), self.hive_size, (10, 10))
        self.bee_in_hive.inhive = True
        self.bee_outside = Bee(2, (3, 3), (0, 0), self.hive_size, (10, 10))
        self.bee_outside.inhive = False
        
        # Create HiveView instance
        self.hive_view = HiveView()
        
        # Create figure and axis for testing
        self.fig, self.ax = plt.subplots()

    def tearDown(self):
        """Clean up after each test"""
        plt.close(self.fig)

    def test_comb_visualization(self):
        """[2.3 Hive View] Test visualization of combs with and without nectar"""
        # Plot the hive
        self.hive_view.plot(self.hive, [self.bee_in_hive], self.ax)
        
        # Get the image data
        image_data = self.ax.images[0].get_array()
        
        # Check that combs with nectar have level 5
        self.assertEqual(image_data[1, 1], 5)
        # Check that combs without nectar have level 10
        self.assertEqual(image_data[2, 2], 10)

    def test_bee_visualization(self):
        """[2.3 Hive View] Test visualization of bees in the hive"""
        # Plot the hive with both bees
        self.hive_view.plot(self.hive, [self.bee_in_hive, self.bee_outside], self.ax)
        
        # Get the scatter plot data
        scatter = self.ax.collections[0]
        x_values = scatter.get_offsets()[:, 0]
        y_values = scatter.get_offsets()[:, 1]
        
        # Check that only the bee in hive is plotted
        self.assertEqual(len(x_values), 1)
        self.assertEqual(x_values[0], 1)
        self.assertEqual(y_values[0], 1)

    def test_plot_configuration(self):
        """[2.3 Hive View] Test plot configuration (title, labels)"""
        self.hive_view.plot(self.hive, [self.bee_in_hive], self.ax)
        
        # Check title
        self.assertEqual(self.ax.get_title(), "Bee Hive")
        # Check axis labels
        self.assertEqual(self.ax.get_xlabel(), "X position")
        self.assertEqual(self.ax.get_ylabel(), "Y position")

    def test_empty_hive(self):
        """[2.3 Hive View] Test visualization of empty hive"""
        # Create empty hive
        empty_hive = Hive(self.hive_size)
        empty_hive.clist = []
        
        # Plot empty hive
        self.hive_view.plot(empty_hive, [], self.ax)
        
        # Check that the plot was created without errors
        self.assertTrue(len(self.ax.images) > 0)
        # Check that the scatter plot has no points
        scatter = self.ax.collections[0]
        self.assertEqual(len(scatter.get_offsets()), 0)

    def test_multiple_bees_in_hive(self):
        """[2.3 Hive View] Test visualization of multiple bees in hive"""
        # Create multiple bees in hive
        bees = [
            Bee(1, (1, 1), (0, 0), self.hive_size, (10, 10)),
            Bee(2, (2, 2), (0, 0), self.hive_size, (10, 10)),
            Bee(3, (3, 3), (0, 0), self.hive_size, (10, 10))
        ]
        for bee in bees:
            bee.inhive = True
        
        # Plot hive with multiple bees
        self.hive_view.plot(self.hive, bees, self.ax)
        
        # Get the scatter plot data
        scatter = self.ax.collections[0]
        x_values = scatter.get_offsets()[:, 0]
        y_values = scatter.get_offsets()[:, 1]
        
        # Check that all bees are plotted
        self.assertEqual(len(x_values), 3)
        # Check bee positions
        self.assertIn(1, x_values)
        self.assertIn(2, x_values)
        self.assertIn(3, x_values) 