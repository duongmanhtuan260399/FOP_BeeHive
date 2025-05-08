import unittest
import json
import tempfile
from model.world import World, PropertyType, Property

class TestWorld(unittest.TestCase):
    def setUp(self):
        self.hive_pos = (15, 15, 4, 4)
        self.world_size = (50, 50)
        self.world = World(self.hive_pos, self.world_size)
        
        # Create test properties
        self.tree = Property(PropertyType.TREE, (10, 10), 2, 2, False)
        self.flower = Property(PropertyType.FLOWER, (20, 20), 1, 1, True)
        self.water = Property(PropertyType.WATER, (30, 30), 3, 3, False)

    def test_initialization(self):
        """Test world initialization"""
        self.assertEqual(self.world.hive_pos, self.hive_pos)
        self.assertEqual(len(self.world.properties), 0)

    def test_add_property(self):
        """Test adding properties to the world"""
        self.world.add_property(self.tree)
        self.world.add_property(self.flower)
        
        properties = self.world.properties
        self.assertEqual(len(properties), 2)
        self.assertTrue(any(p.type == PropertyType.TREE for p in properties))
        self.assertTrue(any(p.type == PropertyType.FLOWER for p in properties))

    def test_property_types(self):
        """Test different property types"""
        self.world.add_property(self.tree)
        self.world.add_property(self.flower)
        self.world.add_property(self.water)
        
        properties = self.world.properties
        self.assertEqual(len(properties), 3)
        self.assertTrue(any(p.type == PropertyType.TREE for p in properties))
        self.assertTrue(any(p.type == PropertyType.FLOWER for p in properties))
        self.assertTrue(any(p.type == PropertyType.WATER for p in properties))

    def test_property_attributes(self):
        """Test property attributes"""
        self.world.add_property(self.flower)
        flower: Property = next(p for p in self.world.properties if p.type == PropertyType.FLOWER)
        
        self.assertEqual(flower.pos, (20, 20))
        self.assertEqual(flower.width, 1)
        self.assertEqual(flower.height, 1)
        self.assertTrue(flower.has_nectar)

if __name__ == '__main__':
    unittest.main()