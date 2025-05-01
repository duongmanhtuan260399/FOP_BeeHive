import unittest
from unittest import TestCase
from model.buzzness import Bee
from model.world import PropertyType, Property, World
import matplotlib.pyplot as plt
import numpy as np


class TestWorld(TestCase):

    def setUp(self):
        """ Set up test fixtures """
        self.bees = [
            Bee("bee1",(5, 5)),
            Bee("bee2",(10, 10)),
            Bee("bee3",(15, 15))
        ]
        self.hive_pos = (2, 2, 5, 5)
        self.world = World(self.bees, self.hive_pos)

    def test_add_property(self):
        """ Test adding a property """
        flower = Property(PropertyType.FLOWER, (1, 1), 2, 2, has_nectar=True)
        self.world.add_property(flower)
        self.assertEqual(len(self.world.properties), 1)
        self.assertIs(self.world.properties[0], flower)

    def test_world_initialization(self):
        """ Test world initialization """
        expected_world = np.full(World.WORLD_SIZE, 5)
        np.testing.assert_array_equal(self.world.world, expected_world)

    def test_plot(self):
        """ Test plot (basic check if plot runs without errors) """
        fig, ax = plt.subplots()
        try:
            self.world.plot(ax)
        except Exception as e:
            self.fail(f"Plotting raised an exception: {e}")
        finally:
            plt.close(fig)

    def test_plot_with_property(self):
        """ Test plot with a property added """
        flower = Property(PropertyType.FLOWER, (1, 1), 2, 2, has_nectar=True)
        self.world.add_property(flower)

        fig, ax = plt.subplots()
        self.world.plot(ax)

        # Check that the flower area in the world array was updated
        expected_value = PropertyType.FLOWER.value
        world_array_section = self.world.world[1:3, 1:3]
        self.assertTrue(np.all(world_array_section == expected_value))

        plt.close(fig)


if __name__ == '__main__':
    unittest.main()