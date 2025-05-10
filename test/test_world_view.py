import unittest
import numpy as np
from model.world import World, PropertyType, Property
from view.WorldView import WorldView
from model.buzzness import Bee
import matplotlib.pyplot as plt

class TestWorldView(unittest.TestCase):
    def setUp(self):
        # Create a small world for testing
        self.world_size = (50, 50)
        self.hive_pos = (15, 15, 2, 2)
        self.world = World(self.hive_pos, self.world_size)
        
        # Add a test property (house) at x=10, y=30 with width=5, height=5
        self.test_property = Property(PropertyType.HOUSE, (10, 30), 5, 5, False)
        self.world.add_property(self.test_property)
        
        # Create a bee that will be used for testing
        self.bee = Bee(1, (0, 0), (self.hive_pos[0], self.hive_pos[1]), (40, 40), self.world_size)
        
        # Create WorldView instance
        self.world_view = WorldView()

    def test_property_display(self):
        """Test if properties are displayed at correct positions"""
        # Create a figure and axis for testing
        fig, ax = plt.subplots()
        
        # Plot the world
        self.world_view.plot(self.world, [self.bee], ax)
        
        # Get the world array after plotting
        world_array = self.world.world
        
        # Check if the property is drawn at the correct position
        # The property should be at x=10, y=30 with width=5, height=5
        property_value = PropertyType.HOUSE.value * (50/20)
        
        # Check the property area
        for x in range(10, 15):  # width=5
            for y in range(30, 35):  # height=5
                self.assertEqual(world_array[y, x], property_value,
                               f"Property not drawn correctly at position ({x}, {y})")
        
        # Check surrounding areas are not affected
        self.assertNotEqual(world_array[29, 10], property_value, "Property drawn outside its area")
        self.assertNotEqual(world_array[35, 10], property_value, "Property drawn outside its area")
        self.assertNotEqual(world_array[30, 9], property_value, "Property drawn outside its area")
        self.assertNotEqual(world_array[30, 15], property_value, "Property drawn outside its area")
        
        plt.close(fig)

    def test_property_matching(self):
        """Test if property matching works correctly with the display"""
        # First plot the world to ensure properties are drawn
        fig, ax = plt.subplots()
        self.world_view.plot(self.world, [self.bee], ax)
        
        # Test bee positions that should match the property
        test_positions = [
            (10, 30),  # Top-left corner
            (14, 34),  # Bottom-right corner
            (12, 32),  # Middle of property
        ]
        
        for x, y in test_positions:
            self.bee.pos = (x, y)
            # Check if the property is at the correct position in the world array
            self.assertEqual(
                self.world.world[y, x],
                PropertyType.HOUSE.value * (50/20),
                f"Property not found at position ({x}, {y})"
            )
        
        plt.close(fig)

if __name__ == '__main__':
    unittest.main() 