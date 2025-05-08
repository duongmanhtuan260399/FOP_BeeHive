import unittest
from unittest.mock import Mock, patch
from controller.world_controller import WorldController
from model.world import World, PropertyType, Property
from model.buzzness import Bee

class TestWorldController(unittest.TestCase):
    def setUp(self):
        self.hive_pos = (15, 15, 4, 4)
        self.world_size = (50, 50)
        self.world = World(self.hive_pos, self.world_size)
        self.controller = WorldController(self.world, self.world_size)
        
        # Create a test bee
        self.bee = Bee(1, (0, 0), self.hive_pos, (40, 40), self.world_size)
        
        # Create test properties
        self.flower = Property(PropertyType.FLOWER, (10, 10), 2, 2, True)
        self.tree = Property(PropertyType.TREE, (20, 20), 2, 2, False)
        self.water = Property(PropertyType.WATER, (30, 30), 2, 2, False)
        
        # Add properties to world
        self.world.add_property(self.flower)
        self.world.add_property(self.tree)
        self.world.add_property(self.water)

    def test_initialization(self):
        """Test controller initialization"""
        self.assertEqual(self.controller.world, self.world)
        self.assertEqual(self.controller.width, self.world_size[0])
        self.assertEqual(self.controller.height, self.world_size[1])

    def test_update_bee_moved_to_flower(self):
        """Test bee movement to flower with nectar"""
        # Position bee at flower location
        self.bee.pos = (10, 10)
        self.bee.inhive = False
        self.bee.hasNectar = False
        
        # Mock bee's set_nectar_found method
        self.bee.set_nectar_found = Mock()
        
        # Test update
        self.controller._WorldController__update_bee_moved(self.bee)
        
        # Verify flower's nectar was removed
        self.assertFalse(self.flower.has_nectar)
        # Verify bee's set_nectar_found was called
        self.bee.set_nectar_found.assert_called_once()

    def test_update_bee_moved_to_empty_flower(self):
        """Test bee movement to flower without nectar"""
        # Position bee at flower location
        self.bee.pos = (10, 10)
        self.bee.inhive = False
        self.bee.hasNectar = False
        
        # Remove nectar from flower
        self.flower.has_nectar = False
        
        # Mock bee's set_nectar_found method
        self.bee.set_nectar_found = Mock()
        
        # Test update
        self.controller._WorldController__update_bee_moved(self.bee)
        
        # Verify bee's set_nectar_found was not called
        self.bee.set_nectar_found.assert_not_called()

    def test_update_bee_moved_to_tree(self):
        """Test bee movement to tree"""
        # Position bee at tree location
        self.bee.pos = (20, 20)
        self.bee.inhive = False
        self.bee.hasNectar = False
        
        # Mock bee's set_nectar_found method
        self.bee.set_nectar_found = Mock()
        
        # Test update
        self.controller._WorldController__update_bee_moved(self.bee)
        
        # Verify bee's set_nectar_found was not called
        self.bee.set_nectar_found.assert_not_called()

    def test_update_bee_in_hive(self):
        """Test update when bee is in hive"""
        # Setup bee in hive
        self.bee.inhive = True
        
        # Mock update_bee_moved method
        self.controller._WorldController__update_bee_moved = Mock()
        
        # Test update
        self.controller.update(self.bee)
        
        # Verify update_bee_moved was not called
        self.controller._WorldController__update_bee_moved.assert_not_called()

    def test_update_bee_outside_hive(self):
        """Test update when bee is outside hive"""
        # Setup bee outside hive
        self.bee.inhive = False
        self.bee.pos = (10, 10)  # At flower location
        
        # Mock update_bee_moved method
        self.controller._WorldController__update_bee_moved = Mock()
        
        # Test update
        self.controller.update(self.bee)
        
        # Verify update_bee_moved was called
        self.controller._WorldController__update_bee_moved.assert_called_once_with(self.bee)

    def test_update_bee_with_nectar(self):
        """Test update when bee already has nectar"""
        # Setup bee with nectar
        self.bee.hasNectar = True
        self.bee.inhive = False
        self.bee.pos = (10, 10)  # At flower location
        
        # Mock update_bee_moved method
        self.controller._WorldController__update_bee_moved = Mock()
        
        # Test update
        self.controller.update(self.bee)
        
        # Verify update_bee_moved was not called
        self.controller._WorldController__update_bee_moved.assert_called_once()

if __name__ == '__main__':
    unittest.main() 