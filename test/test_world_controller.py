import unittest
from unittest.mock import Mock, patch
from controller.world_controller import WorldController
from model.world import World, PropertyType, Property
from model.buzzness import Bee, BeeState

class TestWorldController(unittest.TestCase):
    """
    [2.1 World Controller] Test suite for the WorldController class.
    
    This test suite verifies:
    - Controller initialization and basic properties
    - Collision detection between bees and properties
    - Nectar collection from flowers
    - Boundary management and obstacle handling
    """

    def setUp(self):
        """Initialize test environment with common test data"""
        # [2.1 World Controller] Basic setup
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
        """[2.1 World Controller] Test controller initialization"""
        self.assertEqual(self.controller.world, self.world)
        self.assertEqual(self.controller.width, self.world_size[0])
        self.assertEqual(self.controller.height, self.world_size[1])

    def test_update_bee_moved_to_flower(self):
        """[2.1.2 Nectar collection] Test bee movement to flower with nectar"""
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
        """[2.1.2 Nectar collection] Test bee movement to flower without nectar"""
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
        """[2.1.1 Collision detection] Test bee movement to tree"""
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
        """[2.1 World Controller] Test update when bee is in hive"""
        # Setup bee in hive
        self.bee.inhive = True
        
        # Mock update_bee_moved method
        self.controller._WorldController__update_bee_moved = Mock()
        
        # Test update
        self.controller.update(self.bee)
        
        # Verify update_bee_moved was not called
        self.controller._WorldController__update_bee_moved.assert_not_called()

    def test_update_bee_outside_hive(self):
        """[2.1 World Controller] Test update when bee is outside hive"""
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
        """[2.1.2 Nectar collection] Test update when bee already has nectar"""
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

    def test_obstacle_detection(self):
        """[2.1.1 Collision detection] Test obstacle detection and bee movement prevention"""
        # Position bee at tree location
        self.bee.pos = (20, 20)
        self.bee.inhive = False
        self.bee.hasNectar = False
        
        # Mock bee's step_back method
        self.bee.step_back = Mock()
        
        # Test update
        self.controller._WorldController__update_bee_moved(self.bee)
        
        # Verify step_back was called
        self.bee.step_back.assert_called_once()

    def test_multiple_obstacles(self):
        """[2.1.1 Collision detection] Test handling of multiple obstacles"""
        # Add another obstacle near the first one
        self.world.add_property(Property(PropertyType.TREE, (21, 21), 2, 2, False))
        
        # Position bee at first tree
        self.bee.pos = (20, 20)
        self.bee.inhive = False
        self.bee.hasNectar = False
        
        # Mock bee's step_back method
        self.bee.step_back = Mock()
        
        # Test update
        self.controller._WorldController__update_bee_moved(self.bee)
        
        # Verify step_back was called
        self.bee.step_back.assert_called_once()

    def test_obstacle_edge_cases(self):
        """[2.1.1 Collision detection] Test obstacle detection at property edges"""
        # Test bee at property edge
        self.bee.pos = (19, 20)  # Just outside tree
        self.bee.inhive = False
        self.bee.hasNectar = False
        
        # Mock bee's step_back method
        self.bee.step_back = Mock()
        
        # Test update
        self.controller._WorldController__update_bee_moved(self.bee)
        
        # Verify step_back was not called (bee is outside property)
        self.bee.step_back.assert_not_called()
        
        # Test bee at property corner
        self.bee.pos = (20, 20)  # At tree corner
        self.controller._WorldController__update_bee_moved(self.bee)
        
        # Verify step_back was called
        self.bee.step_back.assert_called_once()

    def test_flower_detection_and_pathfinding(self):
        """[2.1.2 Nectar collection] Test complete flow of flower detection and path-finding"""
        # Position bee at flower location
        self.bee.pos = (10, 10)
        self.bee.inhive = False
        self.bee.hasNectar = False
        
        # Mock path-finding methods
        with patch('model.buzzness.find_path_to_flower') as mock_flower_path, \
             patch('model.buzzness.find_path_to_hive') as mock_hive_path:
            
            # Set up mock return values
            mock_flower_path.return_value = [(1, 1), (2, 2)]
            mock_hive_path.return_value = [(3, 3), (4, 4)]
            
            # Test update
            self.controller._WorldController__update_bee_moved(self.bee)
            
            # Verify flower's nectar was removed
            self.assertFalse(self.flower.has_nectar)
            
            # Verify bee's state
            self.assertTrue(self.bee.hasNectar)
            self.assertEqual(self.bee.state, BeeState.RETURNING)
            self.assertFalse(self.bee.inhive)
            
            # Verify paths were set
            self.assertEqual(self.bee.path_to_flower, [(1, 1), (2, 2)])
            self.assertEqual(self.bee.path_to_hive, [(3, 3), (4, 4)])
            
            # Verify path-finding was called with correct positions
            mock_flower_path.assert_called_once_with(
                (self.hive_pos[0], self.hive_pos[1]),
                (10, 10)
            )
            mock_hive_path.assert_called_once_with(
                (self.hive_pos[0], self.hive_pos[1]),
                (10, 10)
            )

if __name__ == '__main__':
    unittest.main() 