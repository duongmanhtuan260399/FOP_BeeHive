import unittest
import json
import tempfile
from model.world import World, PropertyType, Property

class TestWorld(unittest.TestCase):
    """
    [1.2 World] Test suite for the World class and its components.
    
    This test suite verifies:
    - World initialization and basic properties
    - Property management and attributes
    - Different property types (FLOWER, TREE, WATER)
    - Property positioning and dimensions
    """

    def setUp(self):
        """Initialize test environment with common test data"""
        # [1.2 World] World configuration
        self.hive_pos = (15, 15, 4, 4)  # (x, y, width, height) of hive
        self.world_size = (50, 50)      # (width, height) of world
        self.world = World(self.hive_pos, self.world_size)
        
        # [1.2.1 Property] Test properties with different types
        self.tree = Property(PropertyType.TREE, (10, 10), 2, 2, False)    # Tree at (10,10) with size 2x2
        self.flower = Property(PropertyType.FLOWER, (20, 20), 1, 1, True) # Flower at (20,20) with size 1x1
        self.water = Property(PropertyType.WATER, (30, 30), 3, 3, False)  # Water at (30,30) with size 3x3

    def test_initialization(self):
        """[1.2 World] Test world initialization and basic properties"""
        # Verify world is created with correct hive position
        self.assertEqual(self.world.hive_pos, self.hive_pos)
        # Verify world starts with no properties
        self.assertEqual(len(self.world.properties), 0)

    def test_add_property(self):
        """[1.2.1 Property] Test adding properties to the world"""
        # Add two different types of properties
        self.world.add_property(self.tree)
        self.world.add_property(self.flower)
        
        # Verify properties were added correctly
        properties = self.world.properties
        self.assertEqual(len(properties), 2)
        self.assertTrue(any(p.type == PropertyType.TREE for p in properties))
        self.assertTrue(any(p.type == PropertyType.FLOWER for p in properties))

    def test_property_types(self):
        """[1.2.1 Property] Test different property types and their management"""
        # Add three different types of properties
        self.world.add_property(self.tree)
        self.world.add_property(self.flower)
        self.world.add_property(self.water)
        
        # Verify all property types are present
        properties = self.world.properties
        self.assertEqual(len(properties), 3)
        self.assertTrue(any(p.type == PropertyType.TREE for p in properties))
        self.assertTrue(any(p.type == PropertyType.FLOWER for p in properties))
        self.assertTrue(any(p.type == PropertyType.WATER for p in properties))

    def test_property_attributes(self):
        """[1.2.1 Property] Test property attributes and their values"""
        # Add a flower property
        self.world.add_property(self.flower)
        flower: Property = next(p for p in self.world.properties if p.type == PropertyType.FLOWER)
        
        # Verify all flower attributes are set correctly
        self.assertEqual(flower.pos, (20, 20))    # Position
        self.assertEqual(flower.width, 1)         # Width
        self.assertEqual(flower.height, 1)        # Height
        self.assertTrue(flower.has_nectar)        # Nectar status


if __name__ == '__main__':
    unittest.main()